"""uk/ru: widen meaning glosses for toponyms (owner's decision 2026-10-03; docs/transcription_{uk,ru}.md §10).

Place rows in kb/names/<lang>.jsonl without a `meaning` are sent to Opus with the transcription standard; it returns a
meaning or null. Rows that gain a meaning get `first` = "<rendering> (<meaning>, <Portuguese>)". The previous table is
kept in data/cache/backup/names_<lang>.pre3.jsonl (names_retrofit uses it to find what changed).

    from elucidario.stages import names_widen as W
    W.submit("uk"); W.collect("uk")
"""

from __future__ import annotations

import json
import shutil

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, DOCS, KB

MODEL = "claude-opus-5-5"
CHUNK = 90
NAME = {"uk": "Ukrainian", "ru": "Russian"}
SCHEMA = {"type": "object", "properties": {"names": {"type": "array", "items": {"type": "object", "properties": {
    "pt": {"type": "string"}, "meaning": {"type": ["string", "null"]}}, "required": ["pt", "meaning"],
    "additionalProperties": False}}}, "required": ["names"], "additionalProperties": False}


def _rows(lang: str) -> list[dict]:
    return [json.loads(l) for l in open(KB / "names" / f"{lang}.jsonl")]


def system(lang: str) -> str:
    return (f"You add meaning glosses to Madeiran toponyms in the {NAME[lang]} name table of the Elucidário Madeirense, "
            "following §10 of the standard below INCLUDING the widening of 2026-10-03: single-word toponyms whose element is an "
            "ordinary word, names containing a personal name (gloss the generic part), and regional terms with an established "
            "sense get a meaning. Return `meaning` in natural "
            f"{NAME[lang]}, nominative, no commas, short; or null for personal names, exonyms, institutions, names of unknown or "
            "legendary origin, and names whose meaning is already obvious from the transcription.\n\n"
            + (DOCS / f"transcription_{lang}.md").read_text())


def submit(lang: str, budget_usd: float = 5.0) -> dict:
    todo = [{"pt": x["pt"], "rendering": x["rendering"]} for x in _rows(lang)
            if x.get("type") == "place" and not x.get("meaning")]
    reqs = []
    for i in range(0, len(todo), CHUNK):
        chunk = todo[i: i + CHUNK]
        reqs.append({"custom_id": f"{lang}-w{i // CHUNK:04d}", "params": {
            "model": MODEL, "max_tokens": 16000,
            "system": [{"type": "text", "text": system(lang), "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False) + f"\n\nReturn all {len(chunk)} names."}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}}})
    est = len(reqs) * (len(system(lang)) / 3.0 * 2.0 + 3000 * 2.0 + 4000 * 10.0) / 1e6
    ids = BatchJob(f"names_widen_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"rows": len(todo), "requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def collect(lang: str) -> dict:
    job = BatchJob(f"names_widen_{lang}")
    got = {}
    for _, res in job.results():
        t = message_text(res)
        if t:
            for x in json.loads(t)["names"]:
                if x["meaning"]:
                    got[x["pt"]] = x["meaning"].strip().rstrip(".").replace(",", " —")
    path = KB / "names" / f"{lang}.jsonl"
    backup = DATA / "cache" / "backup" / f"names_{lang}.pre3.jsonl"
    if not backup.exists():
        shutil.copy(path, backup)
    rows = _rows(lang)
    n = 0
    for x in rows:
        if x.get("type") == "place" and not x.get("meaning") and x["pt"] in got:
            x["meaning"] = got[x["pt"]]
            x["first"] = f"{x['rendering']} ({x['meaning']}, {x['pt']})"
            n += 1
    with open(path, "w") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return {"lang": lang, "meanings_added": n, "usd": round(job.spent(), 2)}
