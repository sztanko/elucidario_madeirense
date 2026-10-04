"""Apply the 2026-10 naming standard (docs/naming_latin.md, docs/naming_<lang>.md) to EXISTING translations.

For every article whose Portuguese text contains names whose table form changed (meaning glosses for toponyms,
translated dedications/saints/works, exonyms, established names) and whose translation does not yet show the new
first-mention form, the model receives the names (new first/running forms, old rendering) and the affected translated
blocks with their Portuguese source, and returns exact find/replace edits. Code applies them only where `find` is a
verbatim substring; nothing else in the text changes. Logs: data/10_run/names_retrofit_<lang>.json.

    from elucidario.stages import names_retrofit as R
    R.pilot("en", ["curral-das-freiras-freguesia-do", ...])
    R.submit("en", budget_usd=35); R.collect("en")
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone

from elucidario.llm.batch import BatchJob, message_text
from elucidario.llm.client import client
from elucidario.names_table import rows as name_rows
from elucidario.paths import DATA

MODEL = "claude-opus-5-5"
DB = DATA / "08_tu" / "tu.sqlite"
SNAP = DATA / "11_translations"
LOG = DATA / "10_run"
OLD = DATA / "cache" / "backup"  # names_<lang>.pre2.jsonl: the tables before the 2026-10 standard
CHANGED = ("keep_gloss", "translate", "exonym", "established")
MAX_CHARS = 14000

SCHEMA = {"type": "object", "properties": {"edits": {"type": "array", "items": {"type": "object", "properties": {
    "block": {"type": "string"}, "find": {"type": "string"}, "replace": {"type": "string"}},
    "required": ["block", "find", "replace"], "additionalProperties": False}}}, "required": ["edits"], "additionalProperties": False}

LANGNAME = {"en": "British English", "de": "German", "fr": "French", "it": "Italian", "hu": "Hungarian", "nl": "Dutch",
            "uk": "Ukrainian", "ru": "Russian"}
CYRILLIC = ("uk", "ru")


def system(lang: str) -> str:
    return f"""You correct proper names in an existing {LANGNAME[lang]} translation of the Elucidário Madeirense (encyclopedia
of Madeira) to a new naming standard. You do NOT retranslate: you return minimal find/replace edits.

For each listed name you get its sense(s) and the required forms:
- `first`: the form for the FIRST occurrence in the article (in block order) — e.g. a toponym with its meaning gloss,
  "Câmara de Lobos (‘seals’ den’)", or a translated dedication/title with the Portuguese original in parentheses,
  "chapel of Our Lady of Pity (*Nossa Senhora da Piedade*)", "‘Longing for the Homeland’ (*Saudades da Terra*)";
- `rendering`: the form for every LATER occurrence;
- `old`: how the old name table rendered it (often what the translation contains now).

Rules:
1. Make the first occurrence of each name in the article use `first`, and later occurrences use `rendering`. Only touch
   occurrences of the listed names; change nothing else (no style edits, no other words).
2. OLD STYLE to convert: the previous standard kept religious dedications, saints' names in dedications, institutions
   and work titles in Portuguese with the meaning after them, e.g. "the chapel of Santo António (St Anthony of Padua)",
   "the Espírito Santo (Holy Spirit)". For names whose form is now a translation, rewrite such spots to the new form:
   first occurrence "the chapel of St Anthony (*Santo António*)", later ones "the chapel of St Anthony".
3. Otherwise, if the translation already gives the meaning or the original right there (e.g. the text itself explains that the name
   means "seals' den"), do not add a second gloss — use `rendering`.
4. Homonyms (several senses): decide from context — a parish/town/river vs the saint himself vs a church dedication.
5. Keep the sentence grammatical in {LANGNAME[lang]}: articles, case endings, possessives, capitalisation at the start of
   a sentence. Hungarian: attach suffixes per AkH (São Vicentében, Machicóban, São João-ban).
6. Keep it readable (glosses are short and never stacked):
   - In an ENUMERATION of three or more names (lists of localities, parishes, chapels), do not add meaning glosses —
     use `rendering` (translated dedications still become their translated `rendering`).
   - Never put a gloss directly before or after another parenthesis: if a parenthesis already follows the name
     ("Reis Magos (see …)", "(1921)"), skip the gloss.
   - Do not gloss generic one-word names that are ordinary words in context (Vila, Fajã, Achada, Lombo, Monte, Serra)
     unless the sentence is about the name itself.
7. Never edit inside a quotation of a Portuguese original, verse lines, or text in italics that is the Portuguese original.
8. Each edit: `block` id, `find` = an EXACT substring of that block's current translation (long enough to be unique,
   e.g. include a neighbouring word), `replace` = the corrected substring. Return an empty list if nothing must change."""


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def _plain(s: str) -> str:
    return re.sub(r"[*‘’'“”„«»]", "", s or "")


def _load(lang: str):
    R = name_rows(lang)
    if lang in CYRILLIC:
        # uk/ru tables have no `form`: the names to apply are those whose first-mention form changed (names_widen)
        prev = {x["pt"]: x for x in _jl(OLD / f"names_{lang}.pre3.jsonl")}
        old = {k: v.get("first") for k, v in prev.items()}
        keys = [k for k, v in R.items() if len(k) >= 4 and k in prev and any(x.get("first") != prev[k].get("first") for x in v)]
    else:
        old = {x["pt"]: x.get("rendering") for x in _jl(OLD / f"names_{lang}.pre2.jsonl")}
        keys = [k for k, v in R.items() if len(k) >= 4 and any(x["form"] in CHANGED and x["first"] != k for x in v)]
    pat = re.compile(r"(?<!\w)(" + "|".join(sorted(map(re.escape, keys), key=len, reverse=True)) + r")(?!\w)")
    T = {}
    for r in _jl(SNAP / f"{lang}.jsonl"):
        if r["uid"].startswith("art:") and r.get("text"):
            T[r["uid"]] = r["text"]
    arts = [a for a in _jl(DATA / "04_structured" / "articles.jsonl") if a["kind"] != "front_matter"]
    return R, old, pat, T, arts


def tasks(lang: str, only: set[str] | None = None, mode: str = "new") -> list[dict]:
    """One task per article (long articles split by size): names + affected blocks.
    mode "new": names whose new first-mention form is not yet in the translation.
    mode "oldstyle": only translate-form names still written the old way in the translation, i.e. the Portuguese name
    followed by a parenthesis — "Santo António (St Anthony of Padua)"."""
    R, old, pat, T, arts = _load(lang)
    out = []
    for a in arts:
        if only and a["id"] not in only:
            continue
        pt_text = " ".join(b.get("text") or "" for b in a["blocks"])
        found = set(pat.findall(pt_text))
        if not found:
            continue
        tr_all = _plain(" ".join(T.get(f"art:{a['id']}:{b['id'].split('#')[1]}", "") for b in a["blocks"]))
        if mode == "oldstyle":
            tr_raw = " ".join(T.get(f"art:{a['id']}:{b['id'].split('#')[1]}", "") for b in a["blocks"])
            miss = sorted(k for k in found if any(x.get("form") == "translate" for x in R[k])
                          and re.search(r"(?<!\*)" + re.escape(k) + r"\s*\((?!\*)", tr_raw))
        else:
            miss = sorted(k for k in found if not any(_plain(x["first"])[:40] in tr_all for x in R[k]))
        if not miss:
            continue
        names = [{"pt": k, "old": old.get(k), "senses": [{"sense": x.get("sense") or x.get("type"), "first": x["first"],
                                                            "rendering": x["rendering"]} for x in R[k]]} for k in miss]
        blocks, size, part = [], 0, 0
        for b in a["blocks"]:
            bid = b["id"].split("#")[1]
            tr = T.get(f"art:{a['id']}:{bid}")
            if not tr or not any(k in (b.get("text") or "") or k in tr for k in miss):
                continue
            blocks.append({"block": bid, "portuguese": b["text"], "translation": tr})
            size += len(b["text"]) + len(tr)
            if size > MAX_CHARS:
                out.append({"article": a["id"], "part": part, "names": names, "blocks": blocks})
                blocks, size, part = [], 0, part + 1
        if blocks:
            out.append({"article": a["id"], "part": part, "names": names, "blocks": blocks})
    return out


def _params(lang: str, t: dict) -> dict:
    note = "" if t["part"] == 0 else ("\nThis is a LATER part of the article: earlier parts already carry the first mentions, "
                                      "so use `rendering` for every occurrence here.")
    return {"model": MODEL, "max_tokens": 16000,
            "system": [{"type": "text", "text": system(lang), "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps({"names": t["names"], "blocks": t["blocks"]}, ensure_ascii=False) + note}],
            "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "low"}}


def _apply(T: dict, aid: str, edits: list[dict]) -> tuple[dict, int, int]:
    new, ok, bad = {}, 0, 0
    for e in edits:
        uid = f"art:{aid}:{e['block']}"
        cur = new.get(uid, T.get(uid))
        if cur and e["find"] and e["find"] in cur and e["find"] != e["replace"]:
            new[uid] = cur.replace(e["find"], e["replace"], 1)
            ok += 1
        else:
            bad += 1
    return new, ok, bad


def pilot(lang: str, ids: list[str]) -> list[dict]:
    _, _, _, T, _ = _load(lang)
    out = []
    for t in tasks(lang, set(ids)):
        with client().messages.stream(**_params(lang, t)) as s:
            msg = s.get_final_message()
        edits = json.loads(next(b.text for b in msg.content if b.type == "text"))["edits"]
        new, ok, bad = _apply(T, t["article"], edits)
        out.append({"article": t["article"], "names": [n["pt"] for n in t["names"]], "edits": edits, "applied": ok, "rejected": bad,
                    "usage": [msg.usage.input_tokens, msg.usage.output_tokens]})
    return out


def submit(lang: str, budget_usd: float = 35.0, mode: str = "new", job: str | None = None) -> dict:
    job = job or f"names_retrofit_{lang}"
    ts = tasks(lang, mode=mode)
    keys = {}
    reqs = []
    for i, t in enumerate(ts):
        cid = f"{lang}-r{i:05d}"
        keys[cid] = [t["article"], t["part"]]
        reqs.append({"custom_id": cid, "params": _params(lang, t)})
    (LOG / f"{job}_keys.json").write_text(json.dumps(keys))
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    est = chars / 3.3 / 1e6 * 2.0 + len(reqs) * (1500 / 1e6 * 2.0 + 700 / 1e6 * 10.0)
    ids = BatchJob(job).submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"tasks": len(reqs), "est_usd": round(est, 2), "batches": ids}


def collect(lang: str, job: str | None = None) -> dict:
    name = job or f"names_retrofit_{lang}"
    _, _, _, T, _ = _load(lang)
    keys = json.loads((LOG / f"{name}_keys.json").read_text())
    job = BatchJob(name)
    changed, log, ok_n, bad_n = {}, [], 0, 0
    for cid, res in job.results():
        t = message_text(res)
        if not t:
            continue
        aid = keys[cid][0]
        edits = json.loads(t)["edits"]
        base = {**T, **changed}
        new, ok, bad = _apply(base, aid, edits)
        ok_n += ok
        bad_n += bad
        for uid, text in new.items():
            log.append({"uid": uid, "before": T[uid], "after": text})
            changed[uid] = text
    con = sqlite3.connect(DB)
    now = datetime.now(timezone.utc).isoformat()
    for uid, text in changed.items():
        con.execute("UPDATE translations SET text = ?, job = ?, updated = ? WHERE uid = ? AND lang = ?",
                    (text, name, now, uid, lang))
    con.commit()
    rows = _jl(SNAP / f"{lang}.jsonl")
    for r in rows:
        if r["uid"] in changed:
            r["text"] = changed[r["uid"]]
    with open(SNAP / f"{lang}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (LOG / f"{name}.json").write_text(json.dumps(log, ensure_ascii=False, indent=1))
    return {"blocks_changed": len(changed), "edits_applied": ok_n, "edits_rejected": bad_n, "usd": round(job.spent(), 2)}
