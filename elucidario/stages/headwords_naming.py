"""Apply the 2026-10 naming standard to translated ARTICLE TITLES (headwords) of Latin-script languages.

Titles whose Portuguese headword contains a name that the name table now TRANSLATES (works, saints, religious
dedications, institutions, exonyms, established names) are sent to Opus with the current translated title and the
table forms; it returns the title in the new standard (translated, no quotes/italics/glosses — the Portuguese headword is
shown under every title on the site). Toponym titles stay Portuguese. Updates the TU store and the snapshot.

    from elucidario.stages import headwords_naming as H
    H.submit("hu"); H.collect("hu")
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone

from elucidario.llm.batch import BatchJob, message_text
from elucidario.names_table import rows as name_rows
from elucidario.paths import DATA

MODEL = "claude-opus-5-5"
DB = DATA / "08_tu" / "tu.sqlite"
SNAP = DATA / "11_translations"
LOG = DATA / "10_run"
TRANSLATED = ("translate", "established", "exonym")
CHUNK = 60
LANGNAME = {"en": "British English", "de": "German", "fr": "French", "it": "Italian", "hu": "Hungarian", "nl": "Dutch"}
SCHEMA = {"type": "object", "properties": {"titles": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "title": {"type": "string"}}, "required": ["id", "title"], "additionalProperties": False}}},
    "required": ["titles"], "additionalProperties": False}


def system(lang: str) -> str:
    return f"""You revise {LANGNAME[lang]} TITLES (headwords) of the Elucidário Madeirense, an encyclopedia of Madeira, to a new
naming standard. Each item has the Portuguese headword, the current {LANGNAME[lang]} title and the name-table forms of the
names it contains (`rendering` = running form).

Rules:
- Titles of works and periodicals, saints, religious dedications (chapels, churches, convents, feasts, Marian titles),
  institutions, exonyms and established historical names are TRANSLATED: use the table's `rendering` adapted to a title
  (no quotation marks, no italics, no asterisks, no leading article, capitalised as a title in {LANGNAME[lang]}).
  E.g. "Saudades da Terra" -> the translated title; "Nossa Senhora da Piedade (Capelas de)" -> the chapels of Our Lady of Pity.
- Madeiran toponyms stay in Portuguese, WITHOUT meaning glosses (the article text gives them).
- Keep the structure of the current title (headword order, the qualifier in parentheses such as "(parish)", plural/singular)
  and every part that does not involve such a name. Do not add the Portuguese original: the site shows it under every title.
- If the current title already follows these rules, return it unchanged.
Return every id with its title."""


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def items(lang: str) -> list[dict]:
    R = name_rows(lang)
    keys = [k for k, v in R.items() if len(k) >= 4 and any(x.get("form") in TRANSLATED and x.get("rendering") != k for x in v)]
    pat = re.compile(r"(?<!\w)(" + "|".join(sorted(map(re.escape, keys), key=len, reverse=True)) + r")(?!\w)")
    tr = {r["uid"]: r["text"] for r in _jl(SNAP / f"{lang}.jsonl") if r["uid"].endswith(":headword") and r.get("text")}
    out = []
    for a in _jl(DATA / "04_structured" / "articles.jsonl"):
        uid = f"art:{a['id']}:headword"
        if uid not in tr or a["kind"] == "front_matter":
            continue
        found = sorted(set(pat.findall(a["headword"])))
        if not found:
            continue
        out.append({"id": a["id"], "portuguese": a["headword"], "current": tr[uid],
                    "names": {k: [{"sense": x.get("sense"), "form": x.get("form"), "rendering": x.get("rendering")} for x in R[k]]
                              for k in found}})
    return out


def submit(lang: str, budget_usd: float = 5.0) -> dict:
    it = items(lang)
    reqs = [{"custom_id": f"{lang}-h{i // CHUNK:04d}", "params": {
        "model": MODEL, "max_tokens": 16000,
        "system": [{"type": "text", "text": system(lang), "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": json.dumps(it[i: i + CHUNK], ensure_ascii=False)}],
        "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "low"}}}
        for i in range(0, len(it), CHUNK)]
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    est = chars / 3.3 / 1e6 * 2.0 + len(it) * 40 / 1e6 * 10.0
    ids = BatchJob(f"headwords_naming_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"titles": len(it), "requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def collect(lang: str) -> dict:
    cur = {x["id"]: x["current"] for x in items(lang)}
    job = BatchJob(f"headwords_naming_{lang}")
    new = {}
    for _, res in job.results():
        t = message_text(res)
        if t:
            for x in json.loads(t)["titles"]:
                title = re.sub(r"[*“”„«»]", "", x["title"]).strip()
                if x["id"] in cur and title and title != cur[x["id"]]:
                    new[x["id"]] = title
    con = sqlite3.connect(DB)
    now = datetime.now(timezone.utc).isoformat()
    for aid, title in new.items():
        con.execute("UPDATE translations SET text = ?, job = ?, updated = ? WHERE uid = ? AND lang = ?",
                    (title, f"headwords_naming_{lang}", now, f"art:{aid}:headword", lang))
    con.commit()
    rows = _jl(SNAP / f"{lang}.jsonl")
    for r in rows:
        aid = r["uid"][4:-len(":headword")] if r["uid"].endswith(":headword") else None
        if aid in new:
            r["text"] = new[aid]
    with open(SNAP / f"{lang}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (LOG / f"headwords_naming_{lang}.json").write_text(json.dumps(
        [{"id": k, "before": cur[k], "after": v} for k, v in new.items()], ensure_ascii=False, indent=1))
    return {"lang": lang, "changed": len(new), "usd": round(job.spent(), 2)}
