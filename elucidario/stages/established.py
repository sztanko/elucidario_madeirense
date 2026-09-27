"""Established names of historical figures (Wikidata + Opus verification) and of religious titles (Opus + web search).

historical:  wikidata()  -> data/cache/wikidata/*.json ; submit_hist() / collect_hist() -> kb/historical_figures.yaml,
             data/06_kb/person_duplicates.jsonl
religious:   religious()  -> kb/religious_titles.yaml   (Messages API with web search, not batch)
"""

from __future__ import annotations

import hashlib
import json
import re
import time

import httpx
import yaml

from elucidario.llm.batch import BatchJob, message_text
from elucidario.llm.client import client
from elucidario.paths import DATA, DOCS, KB

LANGS = ["en", "de", "fr", "it", "hu", "nl", "uk", "ru"]
WD = DATA / "cache" / "wikidata"
UA = {"User-Agent": "elucidario-madeirense-pipeline/0.1 (research; github elucidario_madeirense)"}
API = "https://www.wikidata.org/w/api.php"
MODEL = "claude-opus-5-5"


def _get(params: dict) -> dict:
    WD.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:20]
    path = WD / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    for attempt in range(4):
        try:
            r = httpx.get(API, params={**params, "format": "json"}, headers=UA, timeout=30)
            if r.status_code == 200:
                path.write_text(r.text)
                time.sleep(0.2)
                return r.json()
        except httpx.HTTPError:
            pass
        time.sleep(3 * (attempt + 1))
    return {}


def _year(claims: dict, prop: str) -> str | None:
    for c in claims.get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
        t = v.get("time") if isinstance(v, dict) else None
        if t:
            return t[1:5]
    return None


def search_candidates(names: list[str]) -> list[dict]:
    qids = []
    for n in names:
        n = re.sub(r"^(D\.|Dom|Dona)\s+", "", n)
        for lang in ("pt", "en"):
            res = _get({"action": "wbsearchentities", "search": n, "language": lang, "limit": 5, "type": "item"})
            for s in res.get("search", []):
                if s["id"] not in qids:
                    qids.append(s["id"])
    if not qids:
        return []
    ent = _get({"action": "wbgetentities", "ids": "|".join(qids[:12]), "props": "labels|descriptions|sitelinks|claims",
                "languages": "|".join(["pt"] + LANGS), "sitefilter": "|".join(f"{l}wiki" for l in ["pt"] + LANGS)})
    out = []
    for q, e in (ent.get("entities") or {}).items():
        claims = e.get("claims", {})
        if not any(c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5" for c in claims.get("P31", [])):
            continue  # humans only
        out.append({
            "qid": q,
            "label_pt": e.get("labels", {}).get("pt", {}).get("value"),
            "desc": (e.get("descriptions", {}).get("pt") or e.get("descriptions", {}).get("en") or {}).get("value"),
            "born": _year(claims, "P569"), "died": _year(claims, "P570"),
            "wikipedia": {l: e.get("sitelinks", {}).get(f"{l}wiki", {}).get("title") for l in ["pt"] + LANGS},
            "labels": {l: e.get("labels", {}).get(l, {}).get("value") for l in LANGS},
        })
    return out


def wikidata() -> dict:
    cands = json.loads((DOCS / "historical_candidates.json").read_text())
    rows = []
    for i, c in enumerate(cands):
        rows.append({**c, "wikidata_candidates": search_candidates([c["name"]] + c["aliases"][:1])})
    (DATA / "06_kb" / "historical_wikidata.json").write_text(json.dumps(rows, ensure_ascii=False))
    return {"candidates": len(rows), "with_wd_humans": sum(1 for r in rows if r["wikidata_candidates"])}


HIST_SYSTEM = """You verify Wikidata matches for persons mentioned in the *Elucidário Madeirense* (encyclopedia of Madeira,
1921/1940) and choose the name ESTABLISHED in each target language (en, de, fr, it, hu, nl, uk, ru).
For each person: pick the Wikidata candidate that is the same individual (consistent dates, role and Portuguese/Madeiran
context) or null. Then for each language give the established name: normally the Wikipedia article title in that
language with disambiguators removed (e.g. "Henrique, o Navegador" -> en "Henry the Navigator", uk "Енріке Мореплавець";
"Manuel I de Portugal" -> en "Manuel I of Portugal"; "Cristóvão Colombo" -> ru "Христофор Колумб"). If the language
has no article for the person and no standard historiographic name, give null (the name will then be transcribed by
rule). Local Madeiran figures without articles are null everywhere. Also list `same_as`: other ids in this batch that
are the same individual (duplicates such as "João Gonçalves Zarco" / "João Gonçalves Zargo")."""

HIST_SCHEMA = {"type": "object", "properties": {"persons": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "qid": {"type": ["string", "null"]},
    "names": {"type": "object", "properties": {l: {"type": ["string", "null"]} for l in LANGS}, "required": LANGS,
              "additionalProperties": False},
    "same_as": {"type": "array", "items": {"type": "string"}}},
    "required": ["id", "qid", "names", "same_as"], "additionalProperties": False}}},
    "required": ["persons"], "additionalProperties": False}


def submit_hist() -> dict:
    rows = json.loads((DATA / "06_kb" / "historical_wikidata.json").read_text())
    rows.sort(key=lambda r: r["name"])  # keeps name variants of one person in the same request
    reqs = []
    for i in range(0, len(rows), 20):
        chunk = [{k: r[k] for k in ("id", "name", "aliases", "roles", "birth", "death", "summary", "wikidata_candidates")}
                 for r in rows[i: i + 20]]
        reqs.append({"custom_id": f"h{i // 20:04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": HIST_SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}],
            "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": HIST_SCHEMA}}}})
    return {"requests": len(reqs), "batches": BatchJob("historical").submit(reqs, budget_usd=12.0, est_usd=None)}


def collect_hist() -> dict:
    rows = {r["id"]: r for r in json.loads((DATA / "06_kb" / "historical_wikidata.json").read_text())}
    out, dups = {}, []
    for cid, res in BatchJob("historical").results():
        t = message_text(res)
        if not t:
            continue
        for p in json.loads(t)["persons"]:
            r = rows.get(p["id"])
            if not r:
                continue
            if any(p["names"].values()):
                out[p["id"]] = {"pt_name": r["name"], "aliases": r["aliases"], "wikidata": p["qid"],
                                "dates": [r.get("birth"), r.get("death")], "established_names": p["names"]}
            if p["same_as"]:
                dups.append({"keep": p["id"], "merge": [x for x in p["same_as"] if x in rows and x != p["id"]],
                             "reason": f"same individual (qid {p['qid']})"})
    yaml.safe_dump(out, open(KB / "historical_figures.yaml", "w"), allow_unicode=True, sort_keys=True, width=120)
    with open(DATA / "06_kb" / "person_duplicates.jsonl", "w") as f:
        for d in dups:
            if d["merge"]:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
    per_lang = {l: sum(1 for v in out.values() if v["established_names"].get(l)) for l in LANGS}
    return {"figures": len(out), "per_lang": per_lang, "duplicate_groups": sum(1 for d in dups if d["merge"]),
            "usd": round(BatchJob("historical").spent(), 2)}


# ------------------------------------------------------------------ religious titles
REL_SYSTEM = """You are an expert in Catholic hagiography, Marian devotions and liturgical terminology in European
languages. For each Portuguese religious title or saint name from the *Elucidário Madeirense* (Madeira, 1921/1940),
research (use web search: Wikipedia in each language, Catholic encyclopedias, national church sources) and give the
ESTABLISHED equivalent in en (UK), de, fr, it, hu, nl, uk, ru. Never translate literally when a devotion has an
established name: e.g. "Nossa Senhora da Boa Morte" is the Dormition/Assumption devotion -> uk "Успіння Пресвятої
Богородиці"; "Nossa Senhora do Livramento" -> uk "Богородиця Визволителька". Saints: the saint's standard name in that
language (São Tiago = St James the Greater -> de "Jakobus der Ältere", uk "святий Яків"). For uk/ru use Catholic usage
where a Latin devotion has no Eastern counterpart, and say which tradition. Mark `established` false when you had to
coin a descriptive rendering. Note which items are mainly PLACE NAMES in Madeira (e.g. Santa Cruz, São Vicente,
Santo António da Serra) in `also_toponym`."""

REL_SCHEMA = {"type": "object", "properties": {"titles": {"type": "array", "items": {"type": "object", "properties": {
    "pt": {"type": "string"}, "kind": {"type": "string", "enum": ["marian", "christological", "trinitarian", "saint", "institution", "other"]},
    "devotion": {"type": "string"}, "feast": {"type": ["string", "null"]},
    "names": {"type": "object", "properties": {l: {"type": "string"} for l in LANGS}, "required": LANGS, "additionalProperties": False},
    "established": {"type": "boolean"}, "also_toponym": {"type": "boolean"}, "source": {"type": ["string", "null"]}},
    "required": ["pt", "kind", "devotion", "feast", "names", "established", "also_toponym", "source"],
    "additionalProperties": False}}}, "required": ["titles"], "additionalProperties": False}


def religious_items() -> list[str]:
    rows = json.loads((DOCS / "religious_candidates.json").read_text())
    seen, out = set(), []
    for r in rows:
        pt = re.sub(r"^S\. ", "São ", r["pt"])
        pt = pt.replace("Antonio", "António").replace("Catharina", "Catarina").replace("Quiteria", "Quitéria")
        if pt.lower() not in seen:
            seen.add(pt.lower())
            out.append(pt)
    return out


def religious(group: int = 12) -> dict:
    items = religious_items()
    path = KB / "religious_titles.yaml"
    table = yaml.safe_load(path.read_text()) if path.exists() else {}
    todo = [i for i in items if i not in table]
    usd = 0.0
    for k in range(0, len(todo), group):
        chunk = todo[k: k + group]
        msgs = [{"role": "user", "content": "Research and return all of these:\n" + json.dumps(chunk, ensure_ascii=False)}]
        for _ in range(6):  # handle pause_turn from server-side search
            with client().messages.stream(
                model=MODEL, max_tokens=32000, system=REL_SYSTEM, messages=msgs,
                tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}],
                output_config={"effort": "medium", "format": {"type": "json_schema", "schema": REL_SCHEMA}}) as st:
                r = st.get_final_message()
            u = r.usage
            usd += (u.input_tokens * 4 + u.output_tokens * 20 + (u.cache_read_input_tokens or 0) * 0.2) / 1e6
            if r.stop_reason != "pause_turn":
                break
            msgs = msgs + [{"role": "assistant", "content": r.content}]
        text = next((b.text for b in r.content if b.type == "text" and b.text.strip().startswith("{")), None)
        if not text:
            continue
        for t in json.loads(text)["titles"]:
            table[t["pt"]] = {k2: t[k2] for k2 in ("kind", "devotion", "feast", "established", "also_toponym", "source")} | t["names"]
        yaml.safe_dump(table, open(path, "w"), allow_unicode=True, sort_keys=False, width=120)
    return {"titles": len(table), "usd_approx": round(usd, 2)}


def merge_person_duplicates() -> dict:
    """Merge duplicate person entities (data/06_kb/person_duplicates.jsonl) in persons.final.jsonl; keep redirects."""
    path = DATA / "06_kb" / "persons.final.jsonl"
    persons = {json.loads(l)["id"]: json.loads(l) for l in open(path)}
    dup = DATA / "06_kb" / "person_duplicates.jsonl"
    merged, redirects = 0, {}
    for line in (open(dup) if dup.exists() else []):
        d = json.loads(line)
        keep = persons.get(d["keep"])
        if not keep:
            continue
        for mid in d["merge"]:
            m = persons.pop(mid, None)
            if not m:
                continue
            keep["aliases"] = sorted(set(keep["aliases"]) | set(m["aliases"]) | {m["name"]} - {keep["name"]})
            keep["mentions"] += m["mentions"]
            keep["mention_count"] = len(keep["mentions"])
            keep["articles"] = sorted(set(keep["articles"]) | set(m["articles"]))
            keep["roles"] = list(dict.fromkeys(keep.get("roles", []) + m.get("roles", [])))[:6]
            keep["main_article_id"] = keep.get("main_article_id") or m.get("main_article_id")
            redirects[mid] = keep["id"]
            merged += 1
    with open(path, "w") as f:
        for p in persons.values():
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    (DATA / "06_kb" / "person_redirects.json").write_text(json.dumps(redirects, indent=1))
    return {"merged": merged, "persons": len(persons)}
