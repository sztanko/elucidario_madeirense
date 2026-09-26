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
    },
    "required": ["blocks", "names"], "additionalProperties": False,
}


def read(p) -> str:
    return p.read_text() if p.exists() else ""


def system_prompt(lang: str) -> str:
    core = read(DOCS / "style" / "core.md")
    lang_guide = read(DOCS / "style" / f"{STYLE_FILE.get(lang, lang)}.md")
    translit = read(DOCS / f"transcription_{lang}.md") if lang in ("uk", "ru") else ""
    return "\n\n".join(x for x in (
        f"You translate the *Elucidário Madeirense* (encyclopedia of Madeira, 1921/1940) from Portuguese into {LANG_NAMES[lang]}.",
        core, lang_guide, translit,
        "## Output contract\nReturn JSON: `blocks` — one object per input block with the same `id`, the full translation "
        "in `text` (inline italics as *…*), and for table blocks `cells` (the translated label/header cells in the same "
        "shape as given; numeric cells are pre-rendered and must be copied unchanged) else null; `names` — every proper "
        "name you rendered in this chunk, with the Portuguese form and your rendering (first-mention form for uk/ru).",
    ) if x)


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
        names_here = sorted({p["name"] for p in e.get("persons", []) + e.get("places", []) if p["block"] in bids}
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
        return {
            "entry": {"headword": a["headword"], "abstract_en": e.get("abstract"), "part": f"{part + 1}/{parts}",
                      "outline": [c["title_en"] for c in e.get("chapters", [])]},
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
        r = (spec.get("rendering") or "").lower()
        if r and not any(r.split("/")[0].strip() in b["text"].lower() for b in out.get("blocks", [])):
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
