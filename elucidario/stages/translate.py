"""Phase 8c/9: translation request builder, QA and pilot runner (the full translation run is out of scope).

A request = one chapter-sized chunk of one article (blocks), plus a context package:
  article headword + English abstract + outline, chapter summary, termbase subset, name-table subset,
  pre-parsed numbers with their required target-language rendering, table label cells.
The model returns translated blocks keyed by id and the renderings it used for names (for corpus-wide consistency).

QA (code): block completeness, number preservation, termbase compliance, script check (uk/ru), length ratio.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict

import yaml

from elucidario.llm.batch import BatchJob, message_text
from elucidario.numbers import render
from elucidario.paths import DATA, DOCS, KB
from elucidario.text import norm

ART = DATA / "04_structured" / "articles.jsonl"
ENR = DATA / "05_enriched" / "enrichment.jsonl"
OUT = DATA / "09_translate"
LANG_NAMES = {"en": "British English", "de": "German", "fr": "French", "it": "Italian", "hu": "Hungarian",
              "nl": "Dutch", "uk": "Ukrainian", "ru": "Russian"}
STYLE_FILE = {"en": "en-GB"}
CHUNK_CHARS = 7000
LENGTH_RATIO = {"en": (0.75, 1.35), "de": (0.85, 1.5), "fr": (0.85, 1.5), "it": (0.85, 1.45), "hu": (0.8, 1.5),
                "nl": (0.85, 1.5), "uk": (0.8, 1.5), "ru": (0.8, 1.5)}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "blocks": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "text": {"type": "string"},
            "cells": {"type": ["array", "null"], "items": {"type": "array", "items": {"type": "string"}}}},
            "required": ["id", "text", "cells"], "additionalProperties": False}},
        "names": {"type": "array", "items": {"type": "object", "properties": {
            "pt": {"type": "string"}, "rendering": {"type": "string"}}, "required": ["pt", "rendering"],
            "additionalProperties": False}},
        "headword": {"type": ["string", "null"]},
        "flags": {"type": "array", "items": {"type": "object", "properties": {
            "block": {"type": "string"}, "type": {"type": "string", "enum": ["number", "ocr", "ambiguity", "name", "term", "other"]},
            "note": {"type": "string"}}, "required": ["block", "type", "note"], "additionalProperties": False}},
    },
    "required": ["blocks", "names", "headword", "flags"], "additionalProperties": False,
}


def read(p) -> str:
    return p.read_text() if p.exists() else ""


def system_prompt(lang: str) -> str:
    core = read(DOCS / "style" / "core.md")
    lang_guide = read(DOCS / "style" / f"{STYLE_FILE.get(lang, lang)}.md")
    translit = lean_standard(read(DOCS / f"transcription_{lang}.md")) if lang in ("uk", "ru") else ""
    return "\n\n".join(x for x in (
        f"You translate the *Elucidário Madeirense* (encyclopedia of Madeira, 1921/1940) from Portuguese into {LANG_NAMES[lang]}.",
        core, lang_guide, translit,
        "## Output contract\nReturn JSON: `blocks` — one object per input block with the same `id`, the full translation "
        "in `text` (inline italics as *…*), and for table blocks `cells` (the translated label/header cells in the same "
        "shape as given; numeric cells are pre-rendered and must be copied unchanged) else null; `names` — every proper "
        "name you rendered in this chunk, with the Portuguese form and your rendering (first-mention form for uk/ru); "
        "`headword` — the translated entry title when the package says `translate_headword: true`, else null; `flags` — "
        "problems for the editor (suspected OCR error, ambiguous number, unclear name), usually empty. Give the "
        "termbase first-mention gloss only for terms listed in `gloss_first_mention`.",
    ) if x)


def lean_standard(md: str) -> str:
    """Rules only: drop long tables (worked examples, full religious/figure lists) — they reach the model per chunk."""
    out, skip = [], False
    for line in md.splitlines():
        if re.match(r"^#{2,3} (14\. Worked examples|7\.2 Full table|13\.2 Persons|5\.3 )", line):
            skip = True
            out.append(line + "\n(Reference table omitted: the relevant entries are supplied in each request.)")
            continue
        if skip and re.match(r"^#{2,3} ", line):
            skip = False
        if not skip:
            out.append(line)
    return "\n".join(out)


class Context:
    def __init__(self):
        self.arts = {json.loads(l)["id"]: json.loads(l) for l in open(ART)}
        self.enr = {json.loads(l)["id"]: json.loads(l) for l in open(ENR)} if ENR.exists() else {}
        tb = KB / "termbase.yaml"
        self.termbase = yaml.safe_load(tb.read_text()) if tb.exists() else {}
        self.term_variants = {t: [t] for t in self.termbase}
        tbj = DATA / "08_tu" / "termbase.jsonl"
        if tbj.exists():
            for line in open(tbj):
                x = json.loads(line)
                self.term_variants[x["lemma"]] = sorted(set([x["lemma"]] + x.get("variants", [])))
        self.names = defaultdict(dict)  # lang -> pt name -> rendering
        for lang in LANG_NAMES:
            p = KB / "names" / f"{lang}.jsonl"
            if p.exists():
                for line in open(p):
                    x = json.loads(line)
                    self.names[lang][x["pt"]] = x.get("first") or x["rendering"]

    def chunks(self, aid: str) -> list[list[dict]]:
        a = self.arts[aid]
        e = self.enr.get(aid, {})
        blocks = a["blocks"]
        if e.get("chapters"):
            ids = [b["id"].split("#")[1] for b in blocks]
            out = []
            for c in e["chapters"]:
                if c["first_block"] in ids and c["last_block"] in ids:
                    out.append(blocks[ids.index(c["first_block"]): ids.index(c["last_block"]) + 1])
            if sum(len(x) for x in out) == len(blocks):
                return [part for ch in out for part in split_size(ch)]
        return split_size(blocks)

    def package(self, aid: str, blocks: list[dict], lang: str, part: int, parts: int) -> dict:
        a = self.arts[aid]
        e = self.enr.get(aid, {})
        text = " ".join(b["text"] for b in blocks).lower()
        terms = {}
        for lemma, spec in self.termbase.items():
            if any(re.search(rf"\b{re.escape(v.lower())}\b", text) for v in self.term_variants.get(lemma, [lemma])):
                terms[lemma] = {"policy": spec["policy"], "rendering": spec["renderings"].get(lang),
                                "first_mention_gloss": (spec.get("first_mention_gloss") or {}).get(lang)}
        bids = {b["id"].split("#")[1] for b in blocks}
        names_here = sorted({p.get("name") or p.get("full_name") for p in e.get("persons", []) + e.get("places", []) if p["block"] in bids}
                            | {p["as_written"] for p in e.get("persons", []) + e.get("places", []) if p["block"] in bids})
        name_table = {n: self.names[lang][n] for n in names_here if n in self.names[lang]}
        chapter = next((c for c in e.get("chapters", []) if c["first_block"] == blocks[0]["id"].split("#")[1]), None)
        payload_blocks = []
        for b in blocks:
            pb = {"id": b["id"].split("#")[1], "type": b["type"], "text": b["text"]}
            nums = [{"raw": n["raw"], "render": render(n, lang), **({"ambiguous": True} if n.get("ambiguous") else {}),
                     **({"unit": n["unit"]} if n.get("unit") else {})}
                    for n in b.get("numbers", []) if n["kind"] not in ("year",) and render(n, lang) != n["raw"]]
            if nums:
                pb["numbers"] = nums
            if b.get("table"):
                pb["table"] = table_payload(b["table"], lang)
            payload_blocks.append(pb)
        # first-mention glosses: a term is glossed in the chunk where it first occurs in this article (from the source)
        earlier = " ".join(b["text"] for b in a["blocks"] if b["id"] < blocks[0]["id"]).lower()
        gloss_first = sorted(l for l in terms if not any(
            re.search(rf"\b{re.escape(v.lower())}\b", earlier) for v in self.term_variants.get(l, [l])))
        return {
            "entry": {"headword": a["headword"], "abstract_en": e.get("abstract"), "part": f"{part + 1}/{parts}",
                      "outline": [c["title_en"] for c in e.get("chapters", [])]},
            "translate_headword": part == 0,
            "gloss_first_mention": gloss_first,
            "chapter_summary_en": chapter["summary"] if chapter else None,
            "termbase": terms, "names": name_table, "blocks": payload_blocks,
        }


def split_size(blocks: list[dict]) -> list[list[dict]]:
    out, cur, size = [], [], 0
    for b in blocks:
        if cur and size + len(b["text"]) > CHUNK_CHARS:
            out.append(cur)
            cur, size = [], 0
        cur.append(b)
        size += len(b["text"])
    if cur:
        out.append(cur)
    return out


def table_payload(t: dict, lang: str) -> dict:
    cols = t["columns"]
    rows = []
    for r in t["parsed"]:
        row = []
        for c in r:
            if isinstance(c, dict) and "ditto" in c:
                row.append({"ditto": c["ditto"]})
            elif isinstance(c, dict) and "value" in c:
                row.append({"number": render(c, lang)})
            elif isinstance(c, dict):
                row.append({"text": c.get("raw", "")})
            else:
                row.append({"text": c})
        rows.append(row)
    return {"caption": t.get("caption"), "columns": [c["name_pt"] + (f" ({c['unit']})" if c.get("unit") else "") for c in cols],
            "header_rows": t.get("header_rows", []), "rows": rows,
            "instruction": "Translate caption, column names, header rows and text cells; copy number cells exactly."}


# ------------------------------------------------------------------ QA
CYR = re.compile(r"[А-Яа-яЁёЇїІіЄєҐґ]")
LAT = re.compile(r"[A-Za-z]")


def qa(src_blocks: list[dict], out: dict, lang: str, pkg: dict) -> list[str]:
    probs = []
    got = {b["id"]: b for b in out.get("blocks", [])}
    for sb in pkg["blocks"]:
        tb = got.get(sb["id"])
        if not tb or not tb["text"].strip():
            probs.append(f"missing block {sb['id']}")
            continue
        ratio = len(tb["text"]) / max(1, len(sb["text"]))
        lo, hi = LENGTH_RATIO[lang]
        if len(sb["text"]) > 80 and not lo <= ratio <= hi:
            probs.append(f"length ratio {ratio:.2f} in {sb['id']}")
        for n in sb.get("numbers", []):
            if n.get("ambiguous"):
                continue
            want = n["render"].replace(" ", " ").replace(" ", " ")
            have = tb["text"].replace(" ", " ").replace(" ", " ")
            if want not in have:
                probs.append(f"number {n['raw']} -> {n['render']!r} not found in {sb['id']}")
        years = re.findall(r"\b1[0-9]{3}\b", sb["text"])
        for y in set(years):
            if y not in tb["text"]:
                probs.append(f"year {y} missing in {sb['id']}")
        if lang in ("uk", "ru"):
            letters = CYR.findall(tb["text"]) + LAT.findall(tb["text"])
            if letters and len(CYR.findall(tb["text"])) / len(letters) < 0.6:
                probs.append(f"low Cyrillic share in {sb['id']}")
    for lemma, spec in pkg["termbase"].items():
        if spec.get("policy") not in ("translate", "keep", "keep_unit") or len(lemma) < 5:
            continue
        src_all = " ".join(b["text"] for b in pkg["blocks"])
        # skip terms that occur only capitalised (inside proper names: "Porto Santo", "Câmara de Lobos")
        if not any(src_all[m.start()].islower() for m in re.finditer(rf"\b{re.escape(lemma)}\b", src_all, re.I)):
            continue
        r = re.split(r"[(;,/]", (spec.get("rendering") or "").lower())[0].strip(" *")
        stem = r[: max(4, int(len(r) * 0.7))]  # tolerate inflection (Gemeinde/Gemeinden, парафія/парафії)
        if r and not any(stem in b["text"].lower() for b in out.get("blocks", [])):
            probs.append(f"termbase '{lemma}' -> '{spec['rendering']}' not used")
    return probs


# ------------------------------------------------------------------ pilot
def pilot_requests(article_ids: list[str], langs: list[str], model: str, effort: str | None, tag: str) -> list[dict]:
    ctx = Context()
    reqs, meta = [], {}
    for lang in langs:
        system = system_prompt(lang)
        for aid in article_ids:
            parts = ctx.chunks(aid)
            for k, blocks in enumerate(parts):
                pkg = ctx.package(aid, blocks, lang, k, len(parts))
                cid = f"{tag}-{lang}-{len(reqs):05d}"
                meta[cid] = {"article": aid, "lang": lang, "part": k, "pkg": pkg}
                params = {"model": model, "max_tokens": 32000,
                          "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                          "messages": [{"role": "user", "content": json.dumps(pkg, ensure_ascii=False)}],
                          "output_config": {"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
                                            **({"effort": effort} if effort else {})}}
                if model == "claude-sonnet-5" and effort is None:
                    params["thinking"] = {"type": "disabled"}
                if model == "claude-haiku-4-5":
                    params["output_config"].pop("effort", None)
                reqs.append({"custom_id": cid, "params": params})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{tag}_meta.json").write_text(json.dumps(meta, ensure_ascii=False))
    return reqs


def pilot_collect(tag: str) -> dict:
    meta = json.loads((OUT / f"{tag}_meta.json").read_text())
    results, issues = {}, {}
    for cid, res in BatchJob(f"translate_{tag}").results():
        t = message_text(res)
        m = meta[cid]
        if t is None:
            issues[cid] = ["request failed"]
            continue
        out = json.loads(t)
        results[cid] = {"article": m["article"], "lang": m["lang"], "part": m["part"], "out": out}
        issues[cid] = qa([], out, m["lang"], m["pkg"])
    (OUT / f"{tag}_results.json").write_text(json.dumps(results, ensure_ascii=False))
    (OUT / f"{tag}_qa.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1))
    n_issue = sum(1 for v in issues.values() if v)
    return {"requests": len(meta), "with_issues": n_issue, "usd": round(BatchJob(f"translate_{tag}").spent(), 2)}


# ------------------------------------------------------------------ pilot orchestration
CONFIGS = {
    "haiku": ("claude-haiku-4-5", None),
    "sonnet": ("claude-sonnet-5", None),
    "opus_low": ("claude-opus-5-5", "low"),
    "opus_med": ("claude-opus-5-5", "medium"),
}
PILOT_LANGS = ["en", "de", "hu", "ru"]


def pilot_submit(budget_usd: float = 40.0) -> dict:
    arts = json.loads((DATA / "08_tu" / "pilot_articles.json").read_text())
    out = {}
    for name, (model, effort) in CONFIGS.items():
        reqs = pilot_requests(arts, PILOT_LANGS, model, effort, name)
        for r in reqs:  # 1-hour cache: batch requests are processed over a longer window
            r["params"]["system"][0]["cache_control"] = {"type": "ephemeral", "ttl": "1h"}
        out[name] = {"requests": len(reqs), "batches": BatchJob(f"translate_{name}").submit(reqs, budget_usd=budget_usd, est_usd=None)}
    return out


JUDGE_SYSTEM = """You are an expert literary and technical translation reviewer, native-level in Portuguese and the
target language. You evaluate anonymous candidate translations of passages from the *Elucidário Madeirense*
(encyclopedia of Madeira, 1921/1940). The brief: translate EVERY sentence faithfully (no omissions, no additions), in
modern, engaging encyclopedia prose; consistent terminology (Madeiran terms kept or translated per termbase); names per
the language's convention (uk/ru: transcription with meaning and original on first mention); all numbers preserved and
formatted for the target language; old currency rendered in full modern figures (20$000 réis -> 20,000 réis).

For each candidate give integer scores 1-5: `fidelity` (completeness and accuracy — the most important),
`fluency` (natural, modern, readable), `terminology` (terms and names), `format` (numbers, tables, quotes, italics).
List concrete `errors` (max 5, short: "omits sentence about 1566 raid", "mistranslates 'foro'").
Then give `ranking` best to worst by overall quality (fidelity weighted double)."""

JUDGE_SCHEMA = {"type": "object", "properties": {
    "candidates": {"type": "array", "items": {"type": "object", "properties": {
        "label": {"type": "string"}, "fidelity": {"type": "integer"}, "fluency": {"type": "integer"},
        "terminology": {"type": "integer"}, "format": {"type": "integer"},
        "errors": {"type": "array", "items": {"type": "string"}}},
        "required": ["label", "fidelity", "fluency", "terminology", "format", "errors"], "additionalProperties": False}},
    "ranking": {"type": "array", "items": {"type": "string"}}},
    "required": ["candidates", "ranking"], "additionalProperties": False}


def judge_submit(budget_usd: float = 15.0, judge_model: str = "claude-fable-5-1", job: str = "translate_judge", effort: str = "medium",
                 configs: list[str] | None = None, map_name: str = "judge_map.json", langs: list[str] | None = None) -> dict:
    import random

    configs = configs or list(CONFIGS)
    runs = {name: json.loads((OUT / f"{name}_results.json").read_text()) for name in configs}
    if langs:
        runs = {n: {c: r for c, r in res.items() if r["lang"] in langs} for n, res in runs.items()}
    metas = {name: json.loads((OUT / f"{name}_meta.json").read_text()) for name in configs}
    # align chunks across configs by (article, lang, part)
    keyed = {}
    for name, res in runs.items():
        for cid, r in res.items():
            keyed.setdefault((r["article"], r["lang"], r["part"]), {})[name] = (cid, r["out"])
    reqs, key_map = [], {}
    rng = random.Random(5)
    for (aid, lang, part), by in sorted(keyed.items()):
        if len(by) < 2:
            continue
        src_meta = metas[next(iter(by))][by[next(iter(by))][0]]["pkg"]
        names = list(by)
        rng.shuffle(names)
        labels = {n: chr(65 + i) for i, n in enumerate(names)}
        cands = "\n\n".join(
            f"### Candidate {labels[n]}\n" + "\n".join(f"[{b['id']}] {b['text']}" for b in by[n][1].get("blocks", []))
            for n in names)
        src = "\n".join(f"[{b['id']}] ({b['type']}) {b['text']}" for b in src_meta["blocks"])
        cid = f"j{len(reqs):05d}"
        key_map[cid] = {"article": aid, "lang": lang, "part": part, "labels": labels}
        reqs.append({"custom_id": cid, "params": {
            "model": judge_model, "max_tokens": 16000,
            "system": [{"type": "text", "text": JUDGE_SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": f"Target language: {LANG_NAMES[lang]}\n\n## Source (Portuguese)\n{src}\n\n{cands}"}],
            "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
        }})
    (OUT / map_name).write_text(json.dumps(key_map))
    return {"requests": len(reqs), "batches": BatchJob(job).submit(reqs, budget_usd=budget_usd, est_usd=None)}


def judge_report(job: str = "translate_judge", map_name: str = "judge_map.json", report_name: str = "pilot_report.json") -> dict:
    from collections import Counter

    key_map = json.loads((OUT / map_name).read_text())
    scores = defaultdict(lambda: defaultdict(list))
    wins = defaultdict(Counter)
    errors = defaultdict(list)
    for cid, res in BatchJob(job).results():
        t = message_text(res)
        if not t:
            continue
        m = key_map[cid]
        inv = {v: k for k, v in m["labels"].items()}
        j = json.loads(t)
        for c in j["candidates"]:
            name = inv.get(c["label"])
            if not name:
                continue
            for k in ("fidelity", "fluency", "terminology", "format"):
                scores[(m["lang"], name)][k].append(c[k])
            errors[(m["lang"], name)] += c["errors"]
        if j["ranking"]:
            wins[m["lang"]][inv.get(j["ranking"][0])] += 1
    table = {}
    for (lang, name), d in sorted(scores.items()):
        table[f"{lang}:{name}"] = {k: round(sum(v) / len(v), 2) for k, v in d.items()} | {"n": len(d["fidelity"])}
    costs = {name: round(BatchJob(f"translate_{name}").spent(), 2) for name in CONFIGS}
    try:
        from elucidario.llm.openai_batch import OpenAIBatch
        costs |= {n: OpenAIBatch(f"translate_{n}").state.get("usd") for n in list(SOL_CONFIGS) + ["sol6_med", "sol6_high"]}
    except Exception:
        pass
    out = {"scores": table, "wins": {l: dict(c) for l, c in wins.items()}, "pilot_usd": costs,
           "judge_usd": round(BatchJob(job).spent(), 2), "judge_job": job,
           "sample_errors": {f"{k[0]}:{k[1]}": v[:8] for k, v in errors.items()}}
    (OUT / report_name).write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


# ------------------------------------------------------------------ OpenAI Sol benchmark
SOL_CONFIGS = {"sol56": ("gpt-5.6-sol", "low"), "sol6": ("gpt-6-sol", "low")}


def sol_submit(configs: dict | None = None, langs: list[str] | None = None) -> dict:
    from elucidario.llm.openai_batch import OpenAIBatch, to_openai

    arts = json.loads((DATA / "08_tu" / "pilot_articles.json").read_text())
    out = {}
    for name, (model, effort) in (configs or SOL_CONFIGS).items():
        reqs = pilot_requests(arts, langs or PILOT_LANGS, model, effort, name)  # same packages/prompts; writes <name>_meta.json
        ob = OpenAIBatch(f"translate_{name}")
        ob.state["model"] = model
        out[name] = ob.submit([{"custom_id": r["custom_id"], "body": to_openai(r["params"], effort)} for r in reqs])
    return out


def sol_collect(name: str) -> dict:
    from elucidario.llm.openai_batch import OpenAIBatch

    meta = json.loads((OUT / f"{name}_meta.json").read_text())
    ob = OpenAIBatch(f"translate_{name}")
    results, issues = {}, {}
    for cid, r in ob.results().items():
        m = meta[cid]
        try:
            out = json.loads(r["text"])
        except (TypeError, json.JSONDecodeError):
            issues[cid] = ["unparseable output"]
            continue
        results[cid] = {"article": m["article"], "lang": m["lang"], "part": m["part"], "out": out}
        issues[cid] = qa([], out, m["lang"], m["pkg"])
    (OUT / f"{name}_results.json").write_text(json.dumps(results, ensure_ascii=False))
    (OUT / f"{name}_qa.json").write_text(json.dumps(issues, ensure_ascii=False, indent=1))
    return {"requests": len(meta), "results": len(results), "with_issues": sum(1 for v in issues.values() if v),
            "usd": ob.state.get("usd")}


def uk_check_submit() -> dict:
    """Ukrainian: gpt-5.6-sol vs Opus 5.5 low on the pilot articles."""
    from elucidario.llm.openai_batch import OpenAIBatch, to_openai

    arts = json.loads((DATA / "08_tu" / "pilot_articles.json").read_text())
    opus = pilot_requests(arts, ["uk"], "claude-opus-5-5", "low", "uk_opus_low")
    sol = pilot_requests(arts, ["uk"], "gpt-5.6-sol", "low", "uk_sol56")
    ob = OpenAIBatch("translate_uk_sol56")
    ob.state["model"] = "gpt-5.6-sol"
    return {"opus": BatchJob("translate_uk_opus_low").submit(opus, budget_usd=5.0, est_usd=None),
            "sol": ob.submit([{"custom_id": r["custom_id"], "body": to_openai(r["params"], "low")} for r in sol])}
