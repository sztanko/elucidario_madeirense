"""Phase 6: knowledge-base consolidation.

Input:  data/04_structured/articles.jsonl, data/05_enriched/enrichment.jsonl
Output: data/06_kb/
    headwords.json          headword index used for resolution
    links.jsonl             resolved links per article block (explicit + implicit)
    persons.jsonl           clustered persons with mentions (and main_article_id when one exists)
    places.jsonl            clustered places with mentions
    events.jsonl            chronology: clustered dated events
    terms.jsonl             glossary candidates grouped by lemma
    adjudicate_*.jsonl      ambiguous clusters/links sent to an LLM for decision
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

from rapidfuzz import fuzz, process

from elucidario.paths import DATA
from elucidario.text import norm

ART = DATA / "04_structured" / "articles.jsonl"
ENR = DATA / "05_enriched" / "enrichment.jsonl"
OUT = DATA / "06_kb"

HONORIFICS = r"(d|dr|dra|sr|sra|padre|pe|frei|fr|conego|conselheiro|cons|comendador|visconde|conde|condessa|marques|barao|baronesa|bispo|dom|dona|sir|miss|mrs|mr|capitao|major|coronel|tenente|general|almirante|comandante|doutor|prof|professor|engenheiro|eng|rev|monsenhor|mons|deao|arcediago|vigario|juiz)"
PARTICLES = {"de", "da", "do", "das", "dos", "e", "d"}


# ------------------------------------------------------------------ helpers
def load():
    arts = {json.loads(l)["id"]: json.loads(l) for l in open(ART)}
    enr = {json.loads(l)["id"]: json.loads(l) for l in open(ENR)} if ENR.exists() else {}
    return arts, enr


def person_key(name: str) -> str:
    n = norm(name)
    n = re.sub(rf"^(?:{HONORIFICS}\s+)+", "", n)
    toks = [t for t in n.split() if t not in PARTICLES]
    return " ".join(toks)


def headword_person_name(headword: str) -> str | None:
    """'Zargo (João Gonçalves)' -> 'João Gonçalves Zargo'; 'Abreu (D. Isabel de)' -> 'D. Isabel de Abreu'."""
    m = re.match(r"^(.+?)\s*\((.+)\)\s*$", headword)
    if not m:
        return None
    return f"{m.group(2)} {m.group(1)}".strip()


def year(edtf: str | None) -> int | None:
    if not edtf:
        return None
    m = re.match(r"^~?(\d{4})", edtf)
    return int(m.group(1)) if m else None


# ------------------------------------------------------------------ headword index + link resolution
class HeadwordIndex:
    def __init__(self, arts: dict):
        self.full: dict[str, list[str]] = defaultdict(list)  # norm(headword)
        self.main: dict[str, list[str]] = defaultdict(list)  # norm(main) for headwords without a person qualifier
        self.person: dict[str, list[str]] = defaultdict(list)  # person_key("Given Surname")
        for a in arts.values():
            if a["kind"] == "front_matter":
                continue
            self.full[norm(a["headword"])].append(a["id"])
            self.main[norm(a["main"])].append(a["id"])
            pn = headword_person_name(a["headword"])
            if pn:
                self.person[person_key(pn)].append(a["id"])
        self.full_keys = list(self.full)
        self.arts = arts

    def resolve(self, target: str) -> tuple[list[str], float]:
        k = norm(target)
        if k in self.full:
            return self.full[k], 100.0
        m = process.extractOne(k, self.full_keys, scorer=fuzz.ratio, score_cutoff=90)
        if m:
            return self.full[m[0]], float(m[1])
        pk = person_key(headword_person_name(target) or target)
        if pk in self.person:
            return self.person[pk], 96.0
        if "(" not in target:
            if k in self.main:
                return self.main[k], 92.0
        return [], 0.0


def resolve_links(arts: dict, enr: dict, idx: HeadwordIndex) -> tuple[list[dict], list[dict]]:
    links, ambiguous = [], []
    for aid, e in enr.items():
        for l in e["links"]:
            ids, score = idx.resolve(l["target"])
            ids = [i for i in ids if i != aid]
            row = {"article": aid, "block": l["block"], "phrase": l["phrase"], "target_text": l["target"],
                   "explicit": l["explicit"], "candidates": ids, "score": score}
            if len(ids) == 1:
                row["target"] = ids[0]
            elif len(ids) > 1:
                ambiguous.append(row)
            links.append(row)
    # cross-reference entries: redirect targets
    for a in arts.values():
        for t in a.get("redirect_to", []):
            ids, score = idx.resolve(t)
            ids = [i for i in ids if i != a["id"]]
            row = {"article": a["id"], "block": a["blocks"][0]["id"].split("#")[1] if a["blocks"] else None,
                   "phrase": t, "target_text": t, "explicit": True, "redirect": True, "candidates": ids, "score": score}
            if len(ids) == 1:
                row["target"] = ids[0]
            elif ids:
                ambiguous.append(row)
            links.append(row)
    return links, ambiguous


# ------------------------------------------------------------------ persons
def cluster_persons(arts: dict, enr: dict) -> list[dict]:
    mentions = []
    for aid, e in enr.items():
        for p in e["persons"]:
            mentions.append({**p, "article": aid, "key": person_key(p["full_name"] or p["as_written"])})
    # articles whose subject is a person
    subjects = {}
    for aid, e in enr.items():
        if any(t.startswith("person.") and t != "person.family" for t in e["types"]):
            name = headword_person_name(arts[aid]["headword"]) or arts[aid]["headword"]
            subjects[aid] = person_key(name)
    # block on the last surname token, then greedy clustering by token-set similarity + date compatibility
    blocks: dict[str, list[int]] = defaultdict(list)
    for i, m in enumerate(mentions):
        toks = m["key"].split()
        if toks:
            blocks[toks[-1]].append(i)
    clusters: list[dict] = []
    for surname, idxs in blocks.items():
        local: list[dict] = []
        for i in idxs:
            m = mentions[i]
            best, best_s = None, 0.0
            for c in local:
                s = fuzz.token_set_ratio(m["key"], c["key"])
                if s < 90:
                    continue
                # birth/death incompatibility breaks a match
                by, dy = year(m.get("birth")), year(m.get("death"))
                if (by and c["birth"] and abs(by - c["birth"]) > 2) or (dy and c["death"] and abs(dy - c["death"]) > 2):
                    continue
                # a short key ("joao") must not absorb longer ones
                if min(len(m["key"].split()), len(c["key"].split())) < 2 and m["key"] != c["key"]:
                    continue
                if s > best_s:
                    best, best_s = c, s
            if best is None:
                best = {"key": m["key"], "names": Counter(), "roles": Counter(), "birth": None, "death": None,
                        "mentions": [], "uncertain": False}
                local.append(best)
            best["names"][m["full_name"]] += 1
            best["roles"].update(m["roles"])
            best["birth"] = best["birth"] or year(m.get("birth"))
            best["death"] = best["death"] or year(m.get("death"))
            if best_s and best_s < 97:
                best["uncertain"] = True
            best["mentions"].append({"article": m["article"], "block": m["block"], "as_written": m["as_written"],
                                     "note": m["note"], "own_entry": m["has_own_entry"]})
            if len(m["key"]) > len(best["key"]):
                best["key"] = m["key"]
        clusters.extend(local)
    # attach main articles
    subj_by_key = defaultdict(list)
    for aid, k in subjects.items():
        subj_by_key[k].append(aid)
    out = []
    for n, c in enumerate(clusters):
        own = [mm["article"] for mm in c["mentions"] if mm["own_entry"]]
        main = own[0] if own else None
        if not main:
            cand = subj_by_key.get(c["key"], [])
            if len(cand) == 1:
                main = cand[0]
        name = c["names"].most_common(1)[0][0]
        out.append({
            "id": f"person:{re.sub(r'[^a-z0-9]+', '-', c['key'])[:60]}",
            "name": name, "aliases": sorted(set(c["names"]) - {name}), "key": c["key"],
            "roles": [r for r, _ in c["roles"].most_common(6)], "birth": c["birth"], "death": c["death"],
            "main_article_id": main, "mention_count": len(c["mentions"]),
            "articles": sorted({mm["article"] for mm in c["mentions"]}), "mentions": c["mentions"],
            "uncertain_merge": c["uncertain"],
        })
    # unique ids
    seen = Counter()
    for p in out:
        seen[p["id"]] += 1
        if seen[p["id"]] > 1:
            p["id"] = f"{p['id']}-{seen[p['id']]}"
    return out


# ------------------------------------------------------------------ places
PLACE_ARTICLE_TYPES = ("place.",)
TAXON_TO_PLACE_TYPE = {
    "place.island": "island", "place.municipality": "municipality", "place.parish": "parish",
    "place.locality": "sítio/locality", "place.mountain": "peak/mountain", "place.stream": "river/stream",
    "place.levada": "levada", "place.faja": "coast/bay/beach", "place.headland": "cape/point",
    "place.bay_port": "coast/bay/beach", "place.street": "street/square", "place.quinta": "quinta/estate",
    "place.region": "region", "building.church": "church/chapel", "building.chapel": "church/chapel",
    "building.convent": "building", "building.fortress": "fort", "building.hospital": "building",
    "building.maritime": "port/quay", "building.monument": "building", "building.other": "building",
}
# qualifiers that only state the type of the headword ("Arco da Calheta (Freguesia do)")
TYPE_QUALIFIERS = re.compile(r"^(freguesia|concelho|municipio|município|sitio|sítio|lugar|povoacao|povoação|vila|cidade)\b", re.I)


def place_name_from_headword(headword: str) -> str:
    """'Laranjeira (Rua da)' -> 'Rua da Laranjeira'; 'Arco da Calheta (Freguesia do)' -> 'Arco da Calheta'."""
    m = re.match(r"^(.+?)\s*\(([^()]*)\)?\s*$", headword)
    if not m:
        return headword.strip(" .")
    main, qual = m.group(1).strip(), (m.group(2) or "").strip()
    if not qual or TYPE_QUALIFIERS.match(qual) or re.search(r"[A-Z][a-z]+ [a-z]+$", qual) and " " not in qual:
        return main
    # "Rua da", "Pico do", "Capela de", "Ilhéu das", "Porto e Praia do", "Montado do"
    if re.search(r"\b(d[aoe]s?|de)$", qual):
        return f"{qual} {main}"
    return main


def cluster_places(arts: dict, enr: dict) -> list[dict]:
    groups: dict[tuple, dict] = {}
    for aid, e in enr.items():
        for p in e["places"]:
            key = (norm(p["name"]), p["island"] if p["island"] != "none" else "", norm(p.get("parish") or ""))
            g = groups.setdefault(key, {"name": Counter(), "types": Counter(), "parish": Counter(), "municipality": Counter(),
                                        "island": Counter(), "geometry": Counter(), "mentions": []})
            g["name"][p["name"]] += 1
            g["types"][p["place_type"]] += 1
            if p.get("parish"):
                g["parish"][p["parish"]] += 1
            if p.get("municipality"):
                g["municipality"][p["municipality"]] += 1
            g["island"][p["island"]] += 1
            g["geometry"][p["geometry_hint"]] += 1
            g["mentions"].append({"article": aid, "block": p["block"], "as_written": p["as_written"], "note": p["note"]})
    # merge groups that differ only by a missing parish when the name+island is otherwise unique
    by_name: dict[tuple, list[tuple]] = defaultdict(list)
    for k in groups:
        by_name[(k[0], k[1])].append(k)
    merged: dict[tuple, dict] = {}
    for nk, keys in by_name.items():
        with_parish = [k for k in keys if k[2]]
        without = [k for k in keys if not k[2]]
        for k in with_parish:
            merged[k] = groups[k]
        if without:
            if len(with_parish) == 1:
                tgt = merged[with_parish[0]]
                for k in without:
                    for f in ("name", "types", "parish", "municipality", "island", "geometry"):
                        tgt[f].update(groups[k][f])
                    tgt["mentions"] += groups[k]["mentions"]
            else:
                for k in without:
                    merged[k] = groups[k]
                    merged[k]["ambiguous_parish"] = len(with_parish) > 1
    # main article: place/building-typed article whose (inverted) headword equals the place name
    place_arts = defaultdict(list)
    subject: dict[str, tuple[str, str]] = {}
    for aid, e in enr.items():
        if e["types"] and e["types"][0].split(".")[0] in ("place", "building"):
            name = place_name_from_headword(arts[aid]["headword"])
            subject[aid] = (name, e["types"][0])
            place_arts[norm(name)].append(aid)
            if norm(arts[aid]["main"]) != norm(name):
                place_arts[norm(arts[aid]["main"])].append(aid)
    out = []
    for k, g in merged.items():
        name = g["name"].most_common(1)[0][0]
        cands = place_arts.get(k[0], [])
        own = [m["article"] for m in g["mentions"] if m["article"] in cands]
        main = own[0] if own else (cands[0] if len(cands) == 1 else None)
        out.append({
            "id": "place:" + re.sub(r"[^a-z0-9]+", "-", "-".join(x for x in k if x))[:80],
            "name": name, "aliases": sorted(set(g["name"]) - {name}),
            "place_type": g["types"].most_common(1)[0][0], "island": g["island"].most_common(1)[0][0],
            "parish": g["parish"].most_common(1)[0][0] if g["parish"] else None,
            "municipality": g["municipality"].most_common(1)[0][0] if g["municipality"] else None,
            "geometry_hint": g["geometry"].most_common(1)[0][0], "main_article_id": main,
            "main_article_candidates": cands if not main else [], "ambiguous_parish": g.get("ambiguous_parish", False),
            "mention_count": len(g["mentions"]), "articles": sorted({m["article"] for m in g["mentions"]}),
            "mentions": g["mentions"],
        })
    # every place/building article that no mention cluster claimed becomes its own place entity
    claimed = {p["main_article_id"] for p in out if p["main_article_id"]}
    for aid, (name, taxon) in subject.items():
        if aid in claimed:
            continue
        e = enr[aid]
        par = Counter(p["parish"] for p in e["places"] if p.get("parish"))
        mun = Counter(p["municipality"] for p in e["places"] if p.get("municipality"))
        isl = Counter(p["island"] for p in e["places"] if p["island"] != "none")
        ptype = TAXON_TO_PLACE_TYPE.get(taxon, "other")
        out.append({
            "id": "place:" + re.sub(r"[^a-z0-9]+", "-", norm(name) + "-" + aid)[:80],
            "name": name, "aliases": [arts[aid]["headword"]], "place_type": ptype,
            "island": isl.most_common(1)[0][0] if isl else "Madeira",
            "parish": par.most_common(1)[0][0] if par else None,
            "municipality": mun.most_common(1)[0][0] if mun else None,
            "geometry_hint": "line" if ptype in ("levada", "river/stream") else "area" if ptype in ("parish", "municipality", "island", "region") else "point",
            "main_article_id": aid, "main_article_candidates": [], "ambiguous_parish": False, "mention_count": 0,
            "articles": [aid], "mentions": [], "from_headword": True,
        })
    seen = Counter()
    for p in out:
        seen[p["id"]] += 1
        if seen[p["id"]] > 1:
            p["id"] = f"{p['id']}-{seen[p['id']]}"
    return out


# ------------------------------------------------------------------ events
def cluster_events(enr: dict) -> list[dict]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for aid, e in enr.items():
        for d in e["dates"]:
            by_date[d["start"]].append({**d, "article": aid})
    out = []
    for start, ds in by_date.items():
        clusters: list[list[dict]] = []
        for d in ds:
            for c in clusters:
                if fuzz.token_set_ratio(d["event"], c[0]["event"]) >= 72 and (d.get("end") or "") == (c[0].get("end") or ""):
                    c.append(d)
                    break
            else:
                clusters.append([d])
        for c in clusters:
            sig = "major" if any(x["significance"] == "major" for x in c) else "minor"
            out.append({
                "id": f"event:{start}:{len(out)}", "start": start, "end": c[0].get("end"), "significance": sig,
                "event": max((x["event"] for x in c), key=len), "variants": [x["event"] for x in c],
                "articles": sorted({x["article"] for x in c}),
                "mentions": [{"article": x["article"], "block": x["block"], "as_written": x["as_written"]} for x in c],
            })
    out.sort(key=lambda e: (e["start"].lstrip("~")[:4], e["start"]))
    return out


# ------------------------------------------------------------------ terms
def group_terms(enr: dict) -> list[dict]:
    g: dict[str, dict] = {}
    for aid, e in enr.items():
        for t in e["terms"]:
            k = norm(t["term_pt"])
            x = g.setdefault(k, {"lemma": Counter(), "glosses": Counter(), "categories": Counter(), "articles": set()})
            x["lemma"][t["term_pt"]] += 1
            x["glosses"][t["gloss_en"]] += 1
            x["categories"][t["category"]] += 1
            x["articles"].add(aid)
    out = []
    for k, x in g.items():
        out.append({"id": "term:" + re.sub(r"[^a-z0-9]+", "-", k), "term_pt": x["lemma"].most_common(1)[0][0],
                    "variants": sorted(set(x["lemma"])), "category": x["categories"].most_common(1)[0][0],
                    "glosses": [gl for gl, _ in x["glosses"].most_common(5)], "article_count": len(x["articles"]),
                    "articles": sorted(x["articles"])[:50]})
    out.sort(key=lambda t: -t["article_count"])
    return out


def link_to_entities(links: list[dict], persons: list[dict], places: list[dict]) -> None:
    """Links with no article target point to a person or place entity page when the name matches exactly."""
    pidx: dict[str, list[str]] = defaultdict(list)
    for p in persons:
        pidx[p["key"]].append(p["id"])
        for a in p["aliases"]:
            pidx[person_key(a)].append(p["id"])
    lidx: dict[str, list[str]] = defaultdict(list)
    for p in places:
        lidx[norm(p["name"])].append(p["id"])
    for l in links:
        if l.get("target") or l["candidates"]:
            continue
        pk = person_key(headword_person_name(l["target_text"]) or l["target_text"])
        hits = sorted(set(pidx.get(pk, []))) or sorted(set(lidx.get(norm(l["target_text"]), [])))
        if len(hits) == 1:
            l["entity"] = hits[0]
        elif hits:
            l["entity_candidates"] = hits[:8]


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    arts, enr = load()
    idx = HeadwordIndex(arts)
    links, amb = resolve_links(arts, enr, idx)
    persons = cluster_persons(arts, enr)
    places = cluster_places(arts, enr)
    events = cluster_events(enr)
    terms = group_terms(enr)
    link_to_entities(links, persons, places)
    write_jsonl(OUT / "links.jsonl", links)
    write_jsonl(OUT / "adjudicate_links.jsonl", amb)
    write_jsonl(OUT / "persons.jsonl", persons)
    write_jsonl(OUT / "places.jsonl", places)
    write_jsonl(OUT / "events.jsonl", events)
    write_jsonl(OUT / "terms.jsonl", terms)
    stats = {
        "articles_enriched": len(enr),
        "links": len(links), "links_resolved": sum(1 for l in links if l.get("target")),
        "links_ambiguous": len(amb), "links_unresolved": sum(1 for l in links if not l["candidates"]),
        "links_to_entity": sum(1 for l in links if l.get("entity")),
        "person_mentions": sum(p["mention_count"] for p in persons), "persons": len(persons),
        "persons_with_article": sum(1 for p in persons if p["main_article_id"]),
        "persons_uncertain": sum(1 for p in persons if p["uncertain_merge"]),
        "place_mentions": sum(p["mention_count"] for p in places), "places": len(places),
        "places_with_article": sum(1 for p in places if p["main_article_id"]),
        "events": len(events), "events_major": sum(1 for e in events if e["significance"] == "major"),
        "terms": len(terms),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    return stats
