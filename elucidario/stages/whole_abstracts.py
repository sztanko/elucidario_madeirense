"""Whole-article abstracts for articles that were enriched in several parts.

Long articles were enriched part by part (enrich.py), and the merge kept the FIRST part's abstract as the article
abstract ("Opening part of the long entry on…"); the others are in `part_abstracts`. This stage writes one abstract
for the whole article from the part abstracts and all chapter titles/summaries, then:
  - updates data/05_enriched/enrichment.jsonl (`abstract`; the first part's text stays in `part_abstracts[0]`),
  - updates the TU store unit `enr:<id>:abstract` (text + hash) and re-points pending translations to the new hash,
  - translates the new abstract into the languages already translated (status done) and updates both the TU store
    and the data/11_translations/<lang>.jsonl snapshots.

Direct (non-batch) calls: ~30 articles × (1 + languages) small requests.

    uv run python -c "from elucidario.stages import whole_abstracts as W; print(W.run())"
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from elucidario.llm.client import client
from elucidario.paths import DATA
from elucidario.stages.run_translate import META_SCHEMA, meta_system
from elucidario.stages.tu import h

ENR = DATA / "05_enriched" / "enrichment.jsonl"
ARTS = DATA / "04_structured" / "articles.jsonl"
DB = DATA / "08_tu" / "tu.sqlite"
SNAP = DATA / "11_translations"
MODEL = "claude-opus-5-5"
JOB = "whole_abstracts"

ABSTRACT_SCHEMA = {"type": "object", "properties": {"abstract": {"type": "string"}}, "required": ["abstract"],
                   "additionalProperties": False}

SYSTEM = """You write the abstract of an entry in the Elucidário Madeirense (encyclopedia of Madeira, 1921/1940), in British English.
The entry is long and was summarised in parts; you receive the part abstracts and every chapter title and summary, in order.
Write ONE abstract for the WHOLE entry: 2–3 plain sentences, at most 70 words, covering its full scope from first to last
chapter (not only the opening). State what the subject is and what the entry covers; mention key periods or facts only when
they define the entry. Do not say "this entry", "this article", "first part", "opening" or similar; start directly with the
subject, like: "Madeira's irrigation channels: their origin…". Keep Portuguese terms and names as given (e.g. levada,
concelho, Zarco). Same register as an encyclopedia lede."""


def _jl(p):
    return [json.loads(l) for l in open(p)]


def _call(system: str, content: str, schema: dict, effort: str) -> dict:
    with client().messages.stream(
        model=MODEL, max_tokens=16000, system=system, messages=[{"role": "user", "content": content}],
        output_config={"format": {"type": "json_schema", "schema": schema}, "effort": effort},
    ) as s:
        msg = s.get_final_message()
    text = next(b.text for b in msg.content if b.type == "text")
    return json.loads(text)


def write_abstract(e: dict, art: dict) -> str:
    lines = [f"Headword: {art['headword']}", "", "Part abstracts:"]
    lines += [f"{i + 1}. {a}" for i, a in enumerate(e["part_abstracts"])]
    lines += ["", "Chapters:"]
    lines += [f"- {c.get('title_en') or c.get('title_pt')}: {c.get('summary') or ''}" for c in e["chapters"]]
    return _call(SYSTEM, "\n".join(lines), ABSTRACT_SCHEMA, "medium")["abstract"].strip()


def translate(units: list[dict], lang: str) -> dict[str, str]:
    from elucidario.paths import KB

    names = {}
    p = KB / "names" / f"{lang}.jsonl"
    if p.exists():
        for line in open(p):
            x = json.loads(line)
            if len(x["pt"]) > 3:
                names[x["pt"]] = x.get("rendering")
    blob = " ".join(u["text"] for u in units)
    used = {k: v for k, v in names.items() if k in blob}
    out = _call(meta_system(lang), json.dumps({"names": dict(list(used.items())[:150]), "units": units}, ensure_ascii=False),
                META_SCHEMA, "low")
    return {u["uid"]: u["text"].strip() for u in out["units"]}


def run(only: list[str] | None = None) -> dict:
    enr = _jl(ENR)
    arts = {a["id"]: a for a in _jl(ARTS)}
    todo = [e for e in enr if e.get("part_abstracts") and (not only or e["id"] in only)]

    new: dict[str, str] = {}
    for e in todo:
        new[e["id"]] = write_abstract(e, arts[e["id"]])
        print(f"{e['id']}: {new[e['id']]}", flush=True)
    for e in enr:
        if e["id"] in new:
            e["abstract"] = new[e["id"]]
    with open(ENR, "w") as f:
        for e in enr:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    con = sqlite3.connect(DB)
    now = datetime.now(timezone.utc).isoformat()
    uids = {f"enr:{aid}:abstract": text for aid, text in new.items()}
    for uid, text in uids.items():
        con.execute("UPDATE units SET text = ?, hash = ? WHERE uid = ?", (text, h(text), uid))
    langs = [r[0] for r in con.execute(
        f"SELECT DISTINCT lang FROM translations WHERE status = 'done' AND uid IN ({','.join('?' * len(uids))})", list(uids))]
    # Languages not yet translated: just point their pending rows at the new source.
    for uid, text in uids.items():
        con.execute("UPDATE translations SET src_hash = ? WHERE uid = ? AND status != 'done'", (h(text), uid))
    con.commit()

    done = {}
    units = [{"uid": u, "text": t} for u, t in uids.items()]
    for lang in langs:
        got = translate(units, lang)
        missing = [u for u in uids if not got.get(u)]
        if missing:
            raise RuntimeError(f"{lang}: no translation for {missing}")
        for uid, text in got.items():
            if uid in uids:
                con.execute("UPDATE translations SET text = ?, src_hash = ?, status = 'done', model = ?, job = ?, updated = ? "
                            "WHERE uid = ? AND lang = ?", (text, h(uids[uid]), MODEL, JOB, now, uid, lang))
        con.commit()
        snap = SNAP / f"{lang}.jsonl"
        if snap.exists():
            rows = _jl(snap)
            for r in rows:
                if r["uid"] in got:
                    r["text"], r["status"] = got[r["uid"]], "done"
            with open(snap, "w") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        done[lang] = len(got)
        print(f"translated {lang}: {len(got)}", flush=True)
    return {"articles": len(new), "translated": done}
