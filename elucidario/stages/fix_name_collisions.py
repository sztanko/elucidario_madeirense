"""Repair translations where a PLACE name was rendered as the homonymous PERSON (saint / royal).

kb/names/<lang>.jsonl is keyed by the Portuguese string alone. "São Vicente" (the saint), "São Lourenço" (the saint) and
"Vitória" (Queen Victoria) are person entries, so translators were handed e.g. "Szaragosszai Szent Vince" for the parish
and municipality of São Vicente. This stage finds every translated unit containing one of those person renderings, sends
the source and the translation to Opus with the language's style guide, and keeps the corrected text. The model changes
only place references; genuine references to the saint/queen, and chapel/church dedications that the guide translates,
stay as they are. A log of every change goes to data/10_run/name_collisions_<lang>.json.

    uv run python -c "from elucidario.stages import fix_name_collisions as F; print(F.run())"
"""

from __future__ import annotations

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from elucidario.llm.client import client
from elucidario.paths import DATA, DOCS
from elucidario.stages.run_translate import meta_system

DB = DATA / "08_tu" / "tu.sqlite"
SNAP = DATA / "11_translations"
LOG = DATA / "10_run"
MODEL = "claude-opus-5-5"
JOB = "fix_name_collisions"

PATTERNS = {
    "hu": ["Szaragosszai Szent Vince", "Szent Lőrinc", "Viktória királynő"],
    "uk": ["святий Лаврентій", "святого Лаврентія", "святому Лаврентію", "святим Лаврентієм", "королеви Вікторії",
           "королева Вікторія", "Вікентій", "Вікентія"],
}

SCHEMA = {"type": "object", "properties": {"units": {"type": "array", "items": {"type": "object", "properties": {
    "uid": {"type": "string"}, "changed": {"type": "boolean"}, "text": {"type": "string"}},
    "required": ["uid", "changed", "text"], "additionalProperties": False}}}, "required": ["units"], "additionalProperties": False}

TASK = """TASK: correct a known name-table error in existing translations. Change nothing else.

The name table mapped some PLACE names to the homonymous PERSON:
- São Vicente (parish, municipality, town, river, Cumeada/Encumeada, grottoes...) was given the saint's name (St Vincent of Saragossa).
- São Lourenço (Ponta de São Lourenço, the Fortaleza/Palácio de São Lourenço in Funchal, the lighthouse, the locality) was given the saint's name (St Lawrence).
- Vitória (a locality in Funchal) was given "Queen Victoria".

For each unit you get the source text (Portuguese original, or English for metadata) and the current translation.
- Where the translation renders one of these PLACES with the saint's/queen's name, rewrite that reference using the
  guide's rules for toponyms (Latin-script languages: keep the Portuguese name with native suffixes, e.g. Hungarian
  "São Vicente-i", "São Lourenço-erőd", "Ponta de São Lourenço"; Ukrainian: transcription with Сан-/Санту-/Санта-, e.g.
  "Сан-Вісенті", "палац Сан-Лоуренсу", "мис Сан-Лоуренсу").
- Chapels, churches and confraternities DEDICATED to the saint follow the guide's dedication rule: if the existing
  rendering already follows it (e.g. Ukrainian "каплиця святого Лаврентія"), leave it.
- Real references to the saint himself, Cape St Vincent (Cabo de São Vicente) and Queen Victoria stay unchanged.
- A saint's name in parentheses right after the Portuguese/transcribed place name is the guide's meaning gloss
  (e.g. "Palácio de São Lourenço (Szent Lőrinc-palota)", "Сан-Лоуренсу (святий Лаврентій)"): keep it.
- Keep grammar correct around any change (cases, suffixes, articles). Do not polish or retranslate anything else.
Return every uid with changed=true/false and the full text (identical to the input when unchanged)."""


def _system(lang: str) -> str:
    extra = ""
    t = DOCS / f"transcription_{lang}.md"
    if t.exists():
        extra = "\n\n" + t.read_text()
    return TASK + "\n\n" + meta_system(lang) + extra


def _call(system: str, units: list[dict]) -> list[dict]:
    with client().messages.stream(
        model=MODEL, max_tokens=32000,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps({"units": units}, ensure_ascii=False)}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "low"},
    ) as s:
        msg = s.get_final_message()
    return json.loads(next(b.text for b in msg.content if b.type == "text"))["units"]


def run(langs: list[str] | None = None, workers: int = 6) -> dict:
    con = sqlite3.connect(DB)
    out = {}
    for lang in langs or list(PATTERNS):
        rows = [json.loads(l) for l in open(SNAP / f"{lang}.jsonl")]
        hits = [r for r in rows if r.get("text") and any(p in r["text"] for p in PATTERNS[lang])]
        items = []
        for r in hits:
            src = con.execute("SELECT text FROM units WHERE uid = ?", (r["uid"],)).fetchone()
            items.append({"uid": r["uid"], "source": src[0] if src else "", "translation": r["text"]})
        batches, cur, size = [], [], 0
        for it in items:
            cur.append(it)
            size += len(it["source"]) + len(it["translation"])
            if len(cur) >= 12 or size > 14000:
                batches.append(cur)
                cur, size = [], 0
        if cur:
            batches.append(cur)
        system = _system(lang)
        _call(system, batches[0][:1])  # warm the prompt cache before fanning out
        with ThreadPoolExecutor(workers) as ex:
            results = [u for res in ex.map(lambda b: _call(system, b), batches) for u in res]
        by_uid = {it["uid"]: it for it in items}
        changed = [u for u in results if u["changed"] and u["uid"] in by_uid and u["text"].strip()
                   and u["text"].strip() != by_uid[u["uid"]]["translation"]]
        missing = sorted(set(by_uid) - {u["uid"] for u in results})
        new = {u["uid"]: u["text"].strip() for u in changed}
        now = datetime.now(timezone.utc).isoformat()
        for uid, text in new.items():
            con.execute("UPDATE translations SET text = ?, job = ?, updated = ? WHERE uid = ? AND lang = ?",
                        (text, JOB, now, uid, lang))
        con.commit()
        for r in rows:
            if r["uid"] in new:
                r["text"] = new[r["uid"]]
        with open(SNAP / f"{lang}.jsonl", "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        (LOG / f"name_collisions_{lang}.json").write_text(json.dumps(
            [{"uid": u, "before": by_uid[u]["translation"], "after": t} for u, t in new.items()], ensure_ascii=False, indent=1))
        out[lang] = {"checked": len(items), "changed": len(new), "missing": missing}
        print(lang, out[lang], flush=True)
    return out
