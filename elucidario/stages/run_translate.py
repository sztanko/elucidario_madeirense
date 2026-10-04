"""Production translation run (article bodies + metadata) per language, following kb/translation_config.yaml.

  plan(lang)            -> request files + cost estimate (no spend)
  submit(lang, part)    -> part = "body" | "meta"; Anthropic (cache warmed) or OpenAI batch, split into chunks
  collect(lang, part)   -> results into data/08_tu/tu.sqlite (translations table) + QA; failed entries listed
  retry(lang, part)     -> resubmit failed entries once (single-entry requests)

Body requests: long articles one chunk per request; short articles packed up to PACK_CHARS per request.
Block ids in a request are "E<k>.<bid>" (k = entry index in the request); headwords returned per entry.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone

import yaml

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, KB
from elucidario.stages.translate import LANG_NAMES, Context, qa, system_prompt

DB = DATA / "08_tu" / "tu.sqlite"
RUN = DATA / "10_run"
PACK_CHARS = 7000
SHORT = 3500
CFG = yaml.safe_load(open(KB / "translation_config.yaml"))
USD_PER_GBP = 1.33

BODY_SCHEMA = {
    "type": "object",
    "properties": {
        "blocks": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "text": {"type": "string"},
            "cells": {"type": ["array", "null"], "items": {"type": "array", "items": {"type": "string"}}}},
            "required": ["id", "text", "cells"], "additionalProperties": False}},
        "headwords": {"type": "array", "items": {"type": "object", "properties": {
            "entry": {"type": "integer"}, "text": {"type": "string"}}, "required": ["entry", "text"], "additionalProperties": False}},
        "names": {"type": "array", "items": {"type": "object", "properties": {
            "pt": {"type": "string"}, "rendering": {"type": "string"}}, "required": ["pt", "rendering"], "additionalProperties": False}},
        "flags": {"type": "array", "items": {"type": "object", "properties": {
            "block": {"type": "string"}, "type": {"type": "string"}, "note": {"type": "string"}},
            "required": ["block", "type", "note"], "additionalProperties": False}},
    },
    "required": ["blocks", "headwords", "names", "flags"], "additionalProperties": False,
}
PACK_NOTE = ("The request contains one or more encyclopedia entries (`entries`). Block ids are prefixed with the entry "
             "index (E0.b000, E1.b000 …): return every block with exactly the same id. For every entry whose "
             "`translate_headword` is true, add {entry, text} to `headwords` with the translated entry title. Return in "
             "`names` only proper names that are NOT already in the supplied name tables.")

META_SCHEMA = {"type": "object", "properties": {"units": {"type": "array", "items": {"type": "object", "properties": {
    "uid": {"type": "string"}, "text": {"type": "string"}}, "required": ["uid", "text"], "additionalProperties": False}}},
    "required": ["units"], "additionalProperties": False}


def route(lang: str, part: str) -> dict:
    if part == "body":
        return CFG["article_body"][lang]
    return (CFG.get("metadata_overrides") or {}).get(lang) or CFG["metadata"]["default"]


# ------------------------------------------------------------------ body requests
def body_requests(lang: str) -> list[dict]:
    ctx = Context()
    items = []  # (aid, part, parts, blocks, chars)
    for aid, a in ctx.arts.items():
        if not a["blocks"]:
            continue
        parts = ctx.chunks(aid)
        for k, blocks in enumerate(parts):
            items.append((aid, k, len(parts), blocks, sum(len(b["text"]) for b in blocks)))
    reqs, pack, size = [], [], 0

    def flush():
        nonlocal pack, size
        if pack:
            entries, meta = [], []
            for n, (aid, k, parts, blocks, _) in enumerate(pack):
                pkg = ctx.package(aid, blocks, lang, k, parts)
                for pb in pkg["blocks"]:
                    pb["id"] = f"E{n}.{pb['id']}"
                entries.append(pkg)
                meta.append({"entry": n, "article": aid, "part": k, "blocks": [b["id"].split("#")[1] for b in blocks]})
            reqs.append({"custom_id": f"{lang}-b{len(reqs):05d}", "entries": entries, "meta": meta})
        pack, size = [], 0

    for it in items:
        aid, k, parts, blocks, chars = it
        if parts > 1 or chars > SHORT:
            flush()
            pack = [it]
            flush()
            continue
        if size + chars > PACK_CHARS:
            flush()
        pack.append(it)
        size += chars
    flush()
    return reqs


def provider_request(req: dict, lang: str, route_: dict, system: str) -> dict:
    content = PACK_NOTE + "\n\n" + json.dumps({"entries": req["entries"]}, ensure_ascii=False)
    params = {"model": route_["model"], "max_tokens": 32000,
              "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
              "messages": [{"role": "user", "content": content}],
              "output_config": {"format": {"type": "json_schema", "schema": BODY_SCHEMA},
                                **({"effort": route_["effort"]} if route_.get("effort") else {})}}
    if route_["provider"] == "openai":
        from elucidario.llm.openai_batch import to_openai

        return {"custom_id": req["custom_id"], "body": to_openai(params, route_.get("effort"))}
    return {"custom_id": req["custom_id"], "params": params}


# ------------------------------------------------------------------ metadata requests
def meta_requests(lang: str) -> list[dict]:
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT u.uid, u.text FROM units u JOIN translations t ON t.uid = u.uid AND t.lang = ? "
                       "WHERE u.src_lang = 'en' AND t.status != 'done' ORDER BY u.article, u.uid", (lang,)).fetchall()
    from elucidario.names_table import for_prompt

    names = {k: v for k, v in for_prompt(lang, "rendering").items() if len(k) > 3}
    reqs, cur, size = [], [], 0
    for uid, text in rows:
        cur.append({"uid": uid, "text": text})
        size += len(text)
        if len(cur) >= 50 or size > 9000:
            reqs.append(cur)
            cur, size = [], 0
    if cur:
        reqs.append(cur)
    out = []
    for n, units in enumerate(reqs):
        blob = " ".join(u["text"] for u in units)
        used = {k: v for k, v in names.items() if k in blob}
        out.append({"custom_id": f"{lang}-m{n:05d}", "units": units, "names": dict(list(used.items())[:120])})
    return out


def meta_system(lang: str) -> str:
    from elucidario.stages.meta_pilot import system

    return system(lang) + ("\n\nWhen a unit contains a Portuguese proper name listed in `names`, use that rendering "
                           "exactly. Translate every unit completely; return every uid.")


def meta_provider_request(req: dict, lang: str, route_: dict, system: str) -> dict:
    content = json.dumps({"names": req["names"], "units": req["units"]}, ensure_ascii=False)
    params = {"model": route_["model"], "max_tokens": 32000,
              "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
              "messages": [{"role": "user", "content": content}],
              "output_config": {"format": {"type": "json_schema", "schema": META_SCHEMA},
                                **({"effort": route_["effort"]} if route_.get("effort") else {})}}
    if route_["provider"] == "openai":
        from elucidario.llm.openai_batch import to_openai

        return {"custom_id": req["custom_id"], "body": to_openai(params, route_.get("effort"))}
    return {"custom_id": req["custom_id"], "params": params}


# ------------------------------------------------------------------ plan / estimate
PRICES = {  # batch USD/M: in, cached, out ; output tokens per input content token (measured in pilots)
    "claude-opus-5-5": (2.0, 0.10, 10.0, 0.80),
    "gpt-5.6-sol": (2.0, 0.20, 10.0, 0.85),
    "gpt-6-sol": (1.0, 0.10, 5.0, 0.70),
    "claude-sonnet-5": (1.0, 0.10, 5.0, 0.80),
}


def plan(lang: str, part: str) -> dict:
    from elucidario.llm.client import client

    RUN.mkdir(parents=True, exist_ok=True)
    r = route(lang, part)
    if part == "body":
        reqs = body_requests(lang)
        system = system_prompt(lang)
        texts = [PACK_NOTE + json.dumps({"entries": q["entries"]}, ensure_ascii=False) for q in reqs]
    else:
        reqs = meta_requests(lang)
        system = meta_system(lang)
        texts = [json.dumps({"names": q["names"], "units": q["units"]}, ensure_ascii=False) for q in reqs]
    with open(RUN / f"{lang}_{part}_requests.jsonl", "w") as f:
        for q in reqs:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    c = client()
    sys_tok = c.messages.count_tokens(model="claude-opus-5-5", system=system, messages=[{"role": "user", "content": "x"}]).input_tokens
    sample = texts[:: max(1, len(texts) // 12)][:12]
    per_char = sum(c.messages.count_tokens(model="claude-opus-5-5", messages=[{"role": "user", "content": t}]).input_tokens
                   for t in sample) / sum(len(t) for t in sample)
    content_tok = int(per_char * sum(len(t) for t in texts))
    pin, pcached, pout, ratio = PRICES[r["model"]]
    # outputs are roughly proportional to the source text share of the content (~55% of the payload)
    out_tok = int(content_tok * 0.55 * ratio / 0.55 * 0.6)
    usd = (content_tok * pin + len(reqs) * sys_tok * pcached + out_tok * pout) / 1e6
    est = {"lang": lang, "part": part, "model": r["model"], "requests": len(reqs), "system_tokens": sys_tok,
           "content_tokens": content_tok, "est_output_tokens": out_tok, "est_usd": round(usd, 2),
           "est_gbp": round(usd / USD_PER_GBP, 2)}
    (RUN / f"{lang}_{part}_estimate.json").write_text(json.dumps(est, indent=1))
    return est


# ------------------------------------------------------------------ submit / collect
def _job(lang: str, part: str, suffix: str = "") -> str:
    return f"run_{lang}_{part}{suffix}"


def submit(lang: str, part: str, cap_usd: float, suffix: str = "", only_ids: set | None = None) -> dict:
    r = route(lang, part)
    reqs = [json.loads(l) for l in open(RUN / f"{lang}_{part}_requests.jsonl")]
    if only_ids is not None:
        reqs = [q for q in reqs if q["custom_id"] in only_ids]
    est = json.loads((RUN / f"{lang}_{part}_estimate.json").read_text())
    est_usd = est["est_usd"] * len(reqs) / max(1, est["requests"])
    if est_usd > cap_usd:
        raise RuntimeError(f"{lang}/{part}: estimate ${est_usd:.2f} exceeds cap ${cap_usd:.2f}")
    system = system_prompt(lang) if part == "body" else meta_system(lang)
    build = provider_request if part == "body" else meta_provider_request
    prov = [build(q, lang, r, system) for q in reqs]
    if r["provider"] == "openai":
        from elucidario.llm.openai_batch import OpenAIBatch

        ids = []
        for k in range(0, len(prov), 400):  # keep each batch under the enqueued-token limit
            ob = OpenAIBatch(f"{_job(lang, part, suffix)}_{k // 400:02d}")
            ob.state["model"] = r["model"]
            ids.append(ob.submit(prov[k: k + 400]))
        return {"provider": "openai", "batches": ids, "requests": len(prov), "est_usd": round(est_usd, 2)}
    ids = BatchJob(_job(lang, part, suffix)).submit(prov, budget_usd=cap_usd, est_usd=est_usd)
    return {"provider": "anthropic", "batches": ids, "requests": len(prov), "est_usd": round(est_usd, 2)}


def _results(lang: str, part: str, suffix: str = ""):
    r = route(lang, part)
    if r["provider"] == "openai":
        from elucidario.llm.openai_batch import OpenAIBatch

        k, spent = 0, 0.0
        while (DATA / "batches" / f"openai_{_job(lang, part, suffix)}_{k:02d}").exists():
            ob = OpenAIBatch(f"{_job(lang, part, suffix)}_{k:02d}")
            ob.wait(poll=120)
            for cid, res in ob.results().items():
                yield cid, res["text"]
            spent += ob.state.get("usd") or 0
            k += 1
        return
    job = BatchJob(_job(lang, part, suffix))
    job.wait(poll=120, verbose=False)
    for cid, res in job.results():
        yield cid, message_text(res)


def spent(lang: str, part: str) -> float:
    r = route(lang, part)
    total = 0.0
    for suffix in ("", "_retry"):
        if r["provider"] == "openai":
            from elucidario.llm.openai_batch import OpenAIBatch

            k = 0
            while (DATA / "batches" / f"openai_{_job(lang, part, suffix)}_{k:02d}").exists():
                total += OpenAIBatch(f"{_job(lang, part, suffix)}_{k:02d}").state.get("usd") or 0
                k += 1
        else:
            total += BatchJob(_job(lang, part, suffix)).spent() if (DATA / "batches" / _job(lang, part, suffix)).exists() else 0
    return round(total, 2)


def collect(lang: str, part: str, suffix: str = "") -> dict:
    con = sqlite3.connect(DB)
    reqs = {json.loads(l)["custom_id"]: json.loads(l) for l in open(RUN / f"{lang}_{part}_requests.jsonl")}
    model = route(lang, part)["model"]
    now = datetime.now(timezone.utc).isoformat()
    done = failed = 0
    failed_ids, all_issues, new_names = [], {}, {}
    for cid, text in _results(lang, part, suffix):
        q = reqs.get(cid)
        try:
            out = json.loads(text) if text else None
        except json.JSONDecodeError:
            out = None
        if not q or out is None:
            failed_ids.append(cid)
            failed += 1
            continue
        if part == "meta":
            got = {u["uid"]: u["text"] for u in out["units"]}
            missing = [u["uid"] for u in q["units"] if not got.get(u["uid"], "").strip()]
            for uid, t in got.items():
                con.execute("UPDATE translations SET text=?, status='done', model=?, job=?, updated=? WHERE uid=? AND lang=?",
                            (t, model, _job(lang, part, suffix), now, uid, lang))
                done += 1
            if missing:
                failed_ids.append(cid)
                all_issues[cid] = [f"missing unit {m}" for m in missing]
            continue
        by_id = {b["id"]: b for b in out["blocks"]}
        heads = {h["entry"]: h["text"] for h in out["headwords"]}
        for n, pkg in enumerate(q["entries"]):
            m = q["meta"][n]
            aid = m["article"]
            sub = {"blocks": [{"id": b["id"].split(".", 1)[1], "text": by_id[b["id"]]["text"], "cells": by_id[b["id"]].get("cells")}
                              for b in pkg["blocks"] if b["id"] in by_id]}
            local_pkg = {**pkg, "blocks": [{**b, "id": b["id"].split(".", 1)[1]} for b in pkg["blocks"]]}
            issues = qa([], sub, lang, local_pkg)
            bad = {re.search(r"(b\d+)$", i).group(1) for i in issues
                   if i.startswith(("missing block", "low Cyrillic")) and re.search(r"(b\d+)$", i)}
            if bad:
                failed_ids.append(cid)
            all_issues[f"{cid}/E{n}"] = issues
            for b in sub["blocks"]:
                status = "qa_failed" if b["id"] in bad else "done"
                val = json.dumps({"text": b["text"], "cells": b["cells"]}, ensure_ascii=False) if b.get("cells") else b["text"]
                con.execute("UPDATE translations SET text=?, status=?, model=?, job=?, qa=?, updated=? WHERE uid=? AND lang=?",
                            (val, status, model, _job(lang, part, suffix), json.dumps(issues, ensure_ascii=False), now,
                             f"art:{aid}:{b['id']}", lang))
                done += 1
            if n in heads and m["part"] == 0:
                con.execute("UPDATE translations SET text=?, status='done', model=?, job=?, updated=? WHERE uid=? AND lang=?",
                            (heads[n], model, _job(lang, part, suffix), now, f"art:{aid}:headword", lang))
        for nm in out.get("names", []):
            new_names[nm["pt"]] = nm["rendering"]
    con.commit()
    (RUN / f"{lang}_{part}{suffix}_qa.json").write_text(json.dumps(all_issues, ensure_ascii=False, indent=0))
    (RUN / f"{lang}_{part}{suffix}_failed.json").write_text(json.dumps(sorted(set(failed_ids))))
    (RUN / f"{lang}_{part}{suffix}_new_names.json").write_text(json.dumps(new_names, ensure_ascii=False, indent=0))
    total = con.execute("SELECT COUNT(*), SUM(status='done') FROM translations t JOIN units u USING(uid) WHERE t.lang=? AND u.src_lang=?",
                        (lang, "pt" if part == "body" else "en")).fetchone()
    return {"lang": lang, "part": part, "units_written": done, "failed_requests": len(set(failed_ids)),
            "units_total": total[0], "units_done": total[1], "usd_spent": spent(lang, part)}


def retry(lang: str, part: str, cap_usd: float) -> dict:
    ids = set(json.loads((RUN / f"{lang}_{part}_failed.json").read_text()))
    if not ids:
        return {"retry": 0}
    return submit(lang, part, cap_usd, suffix="_retry", only_ids=ids)


def incomplete_articles(lang: str) -> set[str]:
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT t.uid FROM translations t JOIN units u USING(uid) WHERE t.lang=? AND u.src_lang='pt' "
                       "AND t.status!='done' AND u.kind != 'article.headword'", (lang,)).fetchall()
    return {r[0].split(":")[1] for r in rows}


def retry_articles(lang: str, cap_usd: float, suffix: str = "_retry2") -> dict:
    """Re-translate whole articles that still have missing blocks, one article per request."""
    ctx = Context()
    todo = incomplete_articles(lang)
    reqs = []
    for aid in sorted(todo):
        parts = ctx.chunks(aid)
        for k, blocks in enumerate(parts):
            pkg = ctx.package(aid, blocks, lang, k, len(parts))
            for pb in pkg["blocks"]:
                pb["id"] = f"E0.{pb['id']}"
            reqs.append({"custom_id": f"{lang}-r{len(reqs):05d}", "entries": [pkg],
                         "meta": [{"entry": 0, "article": aid, "part": k, "blocks": [b["id"].split("#")[1] for b in blocks]}]})
    path = RUN / f"{lang}_body_requests.jsonl"
    existing = {json.loads(l)["custom_id"] for l in open(path)}
    with open(path, "a") as f:
        for q in reqs:
            if q["custom_id"] not in existing:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")
    return submit(lang, "body", cap_usd, suffix=suffix, only_ids={q["custom_id"] for q in reqs})


def translate_headwords_direct(lang: str) -> dict:
    """Entries without body blocks (pure 'V. X' headwords): translate the headword with a direct call."""
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT u.uid, u.text FROM translations t JOIN units u USING(uid) WHERE t.lang=? "
                       "AND u.kind='article.headword' AND t.status!='done'", (lang,)).fetchall()
    if not rows:
        return {"headwords": 0}
    r = route(lang, "body")
    prompt = (f"Translate these encyclopedia entry titles (Elucidário Madeirense) into {LANG_NAMES[lang]}, following the "
              "house rules for headwords: Portuguese proper names kept (or transcribed for uk/ru), cross-reference "
              "'V. X' rendered as the language's 'see X'. Return JSON {\"items\":[{\"uid\":...,\"text\":...}]}.\n"
              + json.dumps([{"uid": u, "text": t} for u, t in rows], ensure_ascii=False))
    if r["provider"] == "openai":
        import httpx
        from elucidario.llm.openai_batch import _h

        body = {"model": r["model"], "input": prompt, "reasoning": {"effort": r.get("effort", "low")}}
        j = httpx.post("https://api.openai.com/v1/responses", headers=_h(), json=body, timeout=300).json()
        text = next(c["text"] for o in j["output"] if o.get("type") == "message" for c in o["content"] if c.get("type") == "output_text")
    else:
        from elucidario.llm.client import client

        m = client().messages.create(model=r["model"], max_tokens=4000, messages=[{"role": "user", "content": prompt}],
                                     output_config={"effort": r.get("effort", "low")})
        text = next(b.text for b in m.content if b.type == "text")
    items = json.loads(text[text.find("{"): text.rfind("}") + 1])["items"]
    now = datetime.now(timezone.utc).isoformat()
    for it in items:
        con.execute("UPDATE translations SET text=?, status='done', model=?, job='headwords_direct', updated=? WHERE uid=? AND lang=?",
                    (it["text"], r["model"], now, it["uid"], lang))
    con.commit()
    return {"headwords": len(items)}
