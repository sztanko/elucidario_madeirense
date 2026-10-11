"""Mini-pilot: translating English-sourced metadata (abstracts, summaries, notes, events) — Sonnet 5 vs Opus 5.5 low."""

from __future__ import annotations

import json
import random
import sqlite3

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, DOCS
from elucidario.stages.translate import LANG_NAMES, STYLE_FILE

DB = DATA / "08_tu" / "tu.sqlite"
OUT = DATA / "09_translate"
LANGS = ["de", "hu", "ru"]
KINDS = ["enrichment.abstract", "enrichment.chapter_summary", "person.summary", "place.summary", "person.note",
         "place.note", "event.text", "enrichment.chapter_title"]
CONFIGS = {"sonnet": ("claude-sonnet-5", None), "opus_low": ("claude-opus-5-5", "low")}
SCHEMA = {"type": "object", "properties": {"units": {"type": "array", "items": {"type": "object", "properties": {
    "uid": {"type": "string"}, "text": {"type": "string"}}, "required": ["uid", "text"], "additionalProperties": False}}},
    "required": ["units"], "additionalProperties": False}


def sample(n: int = 300, seed: int = 3) -> list[dict]:
    con = sqlite3.connect(DB)
    rows = []
    rng = random.Random(seed)
    for k in KINDS:
        got = con.execute("SELECT uid, kind, text FROM units WHERE kind = ? AND src_lang = 'en'", (k,)).fetchall()
        rows += [{"uid": u, "kind": kk, "text": t} for u, kk, t in rng.sample(got, min(len(got), n // len(KINDS)))]
    return rows


def system(lang: str) -> str:
    core = (DOCS / "style" / "core.md").read_text()
    guide = (DOCS / "style" / f"{STYLE_FILE.get(lang, lang)}.md").read_text()
    return (f"You translate knowledge-base metadata of the Elucidário Madeirense (encyclopedia of Madeira) from British "
            f"English into {LANG_NAMES[lang]}: abstracts, chapter titles and summaries, person/place notes and chronology "
            "entries. Translate each unit completely and naturally; keep Portuguese names per the rules; keep dates and numbers "
            "exact. Return JSON with every uid.\n\n" + core + "\n\n" + guide)


def submit() -> dict:
    units = sample()
    (OUT / "meta_sample.json").write_text(json.dumps(units, ensure_ascii=False))
    out = {}
    for name, (model, effort) in CONFIGS.items():
        reqs = []
        for lang in LANGS:
            for i in range(0, len(units), 50):
                params = {"model": model, "max_tokens": 32000,
                          "system": [{"type": "text", "text": system(lang), "cache_control": {"type": "ephemeral"}}],
                          "messages": [{"role": "user", "content": json.dumps(
                              [{"uid": u["uid"], "text": u["text"]} for u in units[i: i + 50]], ensure_ascii=False)}],
                          "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}, **({"effort": effort} if effort else {})}}
                if model == "claude-sonnet-5":
                    params["thinking"] = {"type": "disabled"}
                reqs.append({"custom_id": f"{lang}-{i // 50:02d}", "params": params})
        out[name] = BatchJob(f"meta_{name}").submit(reqs, budget_usd=5.0, est_usd=None)
    return out


JUDGE = """You review translations of short encyclopedia metadata (English source) into the target language. For each
unit you see the source and two anonymous candidates A and B. Score each 1-5 for accuracy (meaning, dates, names),
and naturalness; note errors briefly. Return JSON."""
JSCHEMA = {"type": "object", "properties": {"units": {"type": "array", "items": {"type": "object", "properties": {
    "uid": {"type": "string"}, "A_acc": {"type": "integer"}, "A_nat": {"type": "integer"}, "B_acc": {"type": "integer"},
    "B_nat": {"type": "integer"}, "errors": {"type": "string"}}, "required": ["uid", "A_acc", "A_nat", "B_acc", "B_nat", "errors"],
    "additionalProperties": False}}}, "required": ["units"], "additionalProperties": False}


def results(name: str) -> dict:
    out = {}
    for cid, res in BatchJob(f"meta_{name}").results():
        t = message_text(res)
        lang = cid.split("-")[0]
        if t:
            for u in json.loads(t)["units"]:
                out[(lang, u["uid"])] = u["text"]
    return out


def judge_submit() -> dict:
    units = {u["uid"]: u for u in json.loads((OUT / "meta_sample.json").read_text())}
    s, o = results("sonnet"), results("opus_low")
    rng = random.Random(9)
    reqs, keymap = [], {}
    for lang in LANGS:
        items = []
        for uid, u in units.items():
            a, b = s.get((lang, uid)), o.get((lang, uid))
            if not a or not b:
                continue
            flip = rng.random() < 0.5
            keymap[f"{lang}|{uid}"] = "opus_low" if flip else "sonnet"  # who is A
            items.append({"uid": uid, "source": u["text"], "A": b if flip else a, "B": a if flip else b})
        for i in range(0, len(items), 40):
            reqs.append({"custom_id": f"{lang}-{i // 40:02d}", "params": {
                "model": "claude-opus-5-5", "max_tokens": 32000,
                "system": [{"type": "text", "text": JUDGE, "cache_control": {"type": "ephemeral"}}],
                "messages": [{"role": "user", "content": f"Target: {LANG_NAMES[lang]}\n" + json.dumps(items[i: i + 40], ensure_ascii=False)}],
                "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": JSCHEMA}}}})
    (OUT / "meta_judge_map.json").write_text(json.dumps(keymap))
    return {"requests": len(reqs), "batches": BatchJob("meta_judge").submit(reqs, budget_usd=5.0, est_usd=None)}


def report() -> dict:
    from collections import defaultdict

    keymap = json.loads((OUT / "meta_judge_map.json").read_text())
    sc = defaultdict(lambda: defaultdict(list))
    errs = defaultdict(list)
    for cid, res in BatchJob("meta_judge").results():
        t = message_text(res)
        lang = cid.split("-")[0]
        if not t:
            continue
        for u in json.loads(t)["units"]:
            a_is = keymap.get(f"{lang}|{u['uid']}")
            if not a_is:
                continue
            b_is = "sonnet" if a_is == "opus_low" else "opus_low"
            sc[(lang, a_is)]["acc"].append(u["A_acc"]); sc[(lang, a_is)]["nat"].append(u["A_nat"])
            sc[(lang, b_is)]["acc"].append(u["B_acc"]); sc[(lang, b_is)]["nat"].append(u["B_nat"])
            if u["errors"]:
                errs[lang].append(u["errors"])
    out = {f"{l}:{m}": {k: round(sum(v) / len(v), 2) for k, v in d.items()} | {"n": len(d["acc"])} for (l, m), d in sorted(sc.items())}
    cost = {n: round(BatchJob(f"meta_{n}").spent(), 2) for n in CONFIGS} | {"judge": round(BatchJob("meta_judge").spent(), 2)}
    rep = {"scores": out, "usd": cost, "sample_errors": {l: v[:6] for l, v in errs.items()}}
    (OUT / "meta_pilot_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    return rep


def sol6_submit() -> dict:
    """gpt-6-sol on the same 296 metadata units (OpenAI Batch API)."""
    from elucidario.llm.openai_batch import OpenAIBatch, to_openai

    units = json.loads((OUT / "meta_sample.json").read_text())
    reqs = []
    for lang in LANGS:
        for i in range(0, len(units), 50):
            params = {"model": "gpt-6-sol", "max_tokens": 32000, "system": system(lang),
                      "messages": [{"role": "user", "content": json.dumps(
                          [{"uid": u["uid"], "text": u["text"]} for u in units[i: i + 50]], ensure_ascii=False)}],
                      "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}}}
            reqs.append({"custom_id": f"{lang}-{i // 50:02d}", "body": to_openai(params, "low")})
    ob = OpenAIBatch("meta_sol6")
    ob.state["model"] = "gpt-6-sol"
    return {"batch": ob.submit(reqs)}


def sol6_results() -> dict:
    from elucidario.llm.openai_batch import OpenAIBatch

    out = {}
    for cid, r in OpenAIBatch("meta_sol6").results().items():
        lang = cid.split("-")[0]
        try:
            for u in json.loads(r["text"])["units"]:
                out[(lang, u["uid"])] = u["text"]
        except (TypeError, json.JSONDecodeError):
            pass
    return out


def judge_sol6_submit() -> dict:
    """A/B: Sonnet 5 vs gpt-6-sol, blind."""
    units = {u["uid"]: u for u in json.loads((OUT / "meta_sample.json").read_text())}
    s, o = results("sonnet"), sol6_results()
    rng = random.Random(11)
    reqs, keymap = [], {}
    for lang in LANGS:
        items = []
        for uid, u in units.items():
            a, b = s.get((lang, uid)), o.get((lang, uid))
            if not a or not b:
                continue
            flip = rng.random() < 0.5
            keymap[f"{lang}|{uid}"] = "sol6" if flip else "sonnet"
            items.append({"uid": uid, "source": u["text"], "A": b if flip else a, "B": a if flip else b})
        for i in range(0, len(items), 40):
            reqs.append({"custom_id": f"{lang}-{i // 40:02d}", "params": {
                "model": "claude-opus-5-5", "max_tokens": 32000,
                "system": [{"type": "text", "text": JUDGE, "cache_control": {"type": "ephemeral"}}],
                "messages": [{"role": "user", "content": f"Target: {LANG_NAMES[lang]}\n" + json.dumps(items[i: i + 40], ensure_ascii=False)}],
                "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": JSCHEMA}}}})
    (OUT / "meta_judge_sol6_map.json").write_text(json.dumps(keymap))
    return {"requests": len(reqs), "batches": BatchJob("meta_judge_sol6").submit(reqs, budget_usd=5.0, est_usd=None)}


def report_sol6() -> dict:
    from collections import defaultdict

    keymap = json.loads((OUT / "meta_judge_sol6_map.json").read_text())
    sc = defaultdict(lambda: defaultdict(list))
    for cid, res in BatchJob("meta_judge_sol6").results():
        t = message_text(res)
        lang = cid.split("-")[0]
        if not t:
            continue
        for u in json.loads(t)["units"]:
            a_is = keymap.get(f"{lang}|{u['uid']}")
            if not a_is:
                continue
            b_is = "sonnet" if a_is == "sol6" else "sol6"
            sc[(lang, a_is)]["acc"].append(u["A_acc"]); sc[(lang, a_is)]["nat"].append(u["A_nat"])
            sc[(lang, b_is)]["acc"].append(u["B_acc"]); sc[(lang, b_is)]["nat"].append(u["B_nat"])
    from elucidario.llm.openai_batch import OpenAIBatch
    rep = {"scores": {f"{l}:{m}": {k: round(sum(v) / len(v), 2) for k, v in d.items()} for (l, m), d in sorted(sc.items())},
           "usd": {"sol6": OpenAIBatch("meta_sol6").state.get("usd"), "judge": round(BatchJob("meta_judge_sol6").spent(), 2)}}
    (OUT / "meta_sol6_report.json").write_text(json.dumps(rep, indent=1))
    return rep
