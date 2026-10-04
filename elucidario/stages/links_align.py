"""Carry the in-text link plan (data/12_links/pt.jsonl) into a translation: find, in each translated block, the exact
phrase that corresponds to each Portuguese anchor. Text is never changed; only link metadata is produced.

  1. deterministic: the anchor's expected renderings (the Portuguese phrase, the target's translated headword with and
     without its qualifier, the name-table rendering) searched as whole words in the translated block;
  2. the rest via one LLM batch: per block, the Portuguese text with anchors marked ⟦L03⟧…⟦/L03⟧ and the translation;
     the model returns, for each anchor, an exact substring of the translation (or null). Code verifies every substring.

Output data/12_links/<lang>.jsonl: {"article", "links": [{"id", "block", "phrase", "kind", "to", "mandatory"}]}.
This is a standard step after translating a language (see docs/HANDOVER.md, "Adding a language").

    from elucidario.stages import links_align as A
    A.submit("uk")          # deterministic pass + batch for the remainder (budget-guarded)
    A.collect("uk")         # after the batch ends: verify, merge, write data/12_links/uk.jsonl
"""

from __future__ import annotations

import json
import re
from collections import defaultdict

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, KB

OUT = DATA / "12_links"
MODEL = "claude-sonnet-5"
SCHEMA = {"type": "object", "properties": {"blocks": {"type": "array", "items": {"type": "object", "properties": {
    "block": {"type": "string"}, "links": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"}, "phrase": {"type": ["string", "null"]}}, "required": ["id", "phrase"],
        "additionalProperties": False}}}, "required": ["block", "links"], "additionalProperties": False}}},
    "required": ["blocks"], "additionalProperties": False}
SYSTEM = """You align hyperlinks between a Portuguese encyclopedia text and its translation.
For each block you get the Portuguese original, where each link anchor is marked ⟦L03⟧like this⟦/L03⟧, and the translation.
For every anchor id, return the phrase of the TRANSLATION that expresses the same reference: an exact, verbatim substring
of the translation (same characters, case, inflection and punctuation), as short as possible but covering the name or
term (e.g. Portuguese "V. Paoli (Guido)" -> English "Paoli (Guido)"; "o concharéu" -> Ukrainian "кончареу"; an inflected
form like "Фуншала" is fine). Do not include surrounding words such as "see" or articles unless they are part of the name.
If the translation has no counterpart, return null. Never invent text that is not in the translation."""


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def _find(text: str, phrase: str, taken: list[tuple[int, int]]) -> tuple[int, int] | None:
    if not phrase or len(phrase) < 2:
        return None
    for m in re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text):
        s, e = m.span()
        if all(e <= a or s >= b for a, b in taken):
            return s, e
    return None


def _load(lang: str, plan: list[dict] | None = None):
    plan = plan if plan is not None else _jl(OUT / "pt.jsonl")
    tr = {}
    for r in _jl(DATA / "11_translations" / f"{lang}.jsonl"):
        if r["uid"].startswith("art:") and r.get("text"):
            tr[r["uid"]] = r["text"]
    from elucidario.names_table import rows as name_rows

    names = {pt: [x.get("rendering") for x in rs if x.get("rendering")] for pt, rs in name_rows(lang).items()}
    pt = {a["id"]: {b["id"].split("#")[-1]: b.get("text") or "" for b in a["blocks"]}
          for a in _jl(DATA / "04_structured" / "articles.jsonl")}
    return plan, tr, names, pt


def _deterministic(plan, tr, names):
    """Returns ({(article, block): {link id: phrase}}, [(article, block, [pending links])])."""
    done, pending = defaultdict(dict), []
    for r in plan:
        aid = r["article"]
        by_block = defaultdict(list)
        for l in r["links"]:
            by_block[l["block"]].append(l)
        for bid, ls in by_block.items():
            text = tr.get(f"art:{aid}:{bid}")
            if not text:
                continue
            taken, rest = [], []
            for l in ls:
                cands = [l["phrase"]]
                if l["kind"] == "article":
                    h = tr.get(f"art:{l['to']}:headword") or ""
                    cands += [h, re.sub(r"\s*\(.*$", "", h)]
                cands += [re.sub(r"[*‘’']", "", r) for r in names.get(l["phrase"], [])]
                span = None
                for c in sorted({c for c in cands if c and len(c) >= 3}, key=len, reverse=True):
                    if span := _find(text, c, taken):
                        break
                if span:
                    taken.append(span)
                    done[(aid, bid)][l["id"]] = text[span[0]:span[1]]
                else:
                    rest.append(l)
            if rest:
                pending.append((aid, bid, rest, ls))
    return done, pending


def _balanced(ph: str | None) -> str | None:
    """Drop a half-open parenthetical the model sometimes includes ("… IX (Capela de São Luís")."""
    if not ph:
        return ph
    ph = ph.strip()
    if ph.count("(") > ph.count(")"):
        ph = ph[: ph.rfind("(")].rstrip(" ,;:")
    return ph or None


def _marked(pt_text: str, ls: list[dict]) -> str:
    out, pos = [], 0
    for l in sorted(ls, key=lambda x: x["start"]):
        if l["start"] < pos:
            continue
        out += [pt_text[pos:l["start"]], f"⟦{l['id']}⟧", pt_text[l["start"]:l["end"]], f"⟦/{l['id']}⟧"]
        pos = l["end"]
    return "".join(out + [pt_text[pos:]])


def requests(lang: str, model: str = MODEL, plan: list[dict] | None = None) -> list[dict]:
    plan, tr, names, pt = _load(lang, plan)
    _, pending = _deterministic(plan, tr, names)
    by_article = defaultdict(list)
    for aid, bid, rest, _ in pending:
        by_article[aid].append({"block": bid, "pt": _marked(pt[aid][bid], rest), "translation": tr[f"art:{aid}:{bid}"],
                                "ids": [l["id"] for l in rest]})
    reqs, cur, size, n = [], [], 0, 0

    def flush():
        nonlocal cur, size, n
        if cur:
            params = {"model": model, "max_tokens": 8000, "thinking": {"type": "disabled"},
                      "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
                      "messages": [{"role": "user", "content": json.dumps(cur, ensure_ascii=False)}],
                      "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}}}
            reqs.append({"custom_id": f"{lang}-k{n:05d}", "params": params})
            n += 1
        cur, size = [], 0

    for aid, blocks in by_article.items():
        for b in blocks:
            b = {"block": f"{aid}:{b['block']}", **{k: v for k, v in b.items() if k != "block"}}
            cur.append(b)
            size += len(b["pt"]) + len(b["translation"])
            if size > 12000 or len(cur) >= 25:
                flush()
    flush()
    return reqs


PRICE = {"claude-sonnet-5": (1.0, 5.0), "claude-haiku-4-5-20251001": (0.5, 2.5), "claude-opus-5-5": (2.0, 10.0)}  # batch $/M


def submit(lang: str, budget_usd: float = 15.0, model: str = MODEL, job: str = "links") -> dict:
    reqs = requests(lang, model)
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    pi, po = PRICE[model]
    est = chars / 3.2 / 1e6 * pi + len(reqs) * 600 / 1e6 * po
    ids = BatchJob(f"{job}_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def collect(lang: str, job: str = "links", retry_job: str | None = None) -> dict:
    """Merge deterministic matches with the batch answers (and, if given, a retry job that only fills gaps)."""
    plan, tr, names, pt = _load(lang)
    done, pending = _deterministic(plan, tr, names)
    retries = [r for r in (retry_job or "").split(",") if r]  # several retry passes: "links2r,links2r2"
    jobs = [BatchJob(f"{job}_{lang}")] + [BatchJob(f"{r}_{lang}") for r in retries]
    got = defaultdict(dict)
    for j in jobs:
        for _, res in j.results():
            text = message_text(res)
            if not text:
                continue
            for b in json.loads(text)["blocks"]:
                aid, _, bid = b["block"].rpartition(":")
                for l in b["links"]:
                    ph = _balanced(l["phrase"])
                    if ph and _find(tr.get(f"art:{aid}:{bid}", ""), ph, []) and l["id"] not in got[(aid, bid)]:
                        got[(aid, bid)][l["id"]] = ph
    llm_ok = llm_bad = 0
    for aid, bid, rest, all_ls in pending:
        text = tr[f"art:{aid}:{bid}"]
        taken = []
        for lid, ph in done[(aid, bid)].items():
            if s := _find(text, ph, taken):
                taken.append(s)
        for l in rest:
            ph = _balanced(got.get((aid, bid), {}).get(l["id"]))
            span = _find(text, ph, taken) if ph else None
            if span:
                taken.append(span)
                done[(aid, bid)][l["id"]] = text[span[0]:span[1]]
                llm_ok += 1
            else:
                llm_bad += 1
    OUT.mkdir(parents=True, exist_ok=True)
    total = kept = mandatory_lost = 0
    with open(OUT / f"{lang}.jsonl", "w") as f:
        for r in plan:
            ls = []
            for l in r["links"]:
                total += 1
                ph = done.get((r["article"], l["block"]), {}).get(l["id"])
                if ph:
                    kept += 1
                    ls.append({"id": l["id"], "block": l["block"], "phrase": ph, "kind": l["kind"], "to": l["to"],
                               "mandatory": l["mandatory"]})
                elif l["mandatory"]:
                    mandatory_lost += 1
            f.write(json.dumps({"article": r["article"], "links": ls}, ensure_ascii=False) + "\n")
    return {"links": total, "aligned": kept, "by_llm": llm_ok, "llm_unaligned": llm_bad,
            "mandatory_unaligned": mandatory_lost, "usd": round(sum(j.spent() for j in jobs), 2)}


def retry(lang: str, model: str = "claude-sonnet-5", job: str = "links", retry_job: str = "links_retry",
          budget_usd: float = 10.0) -> dict:
    """Second pass for anchors the first model could not place (after collect wrote data/12_links/<lang>.jsonl)."""
    have = {(r["article"], l["id"]) for r in _jl(OUT / f"{lang}.jsonl") for l in r["links"]}
    plan = [{"article": r["article"], "links": [l for l in r["links"] if (r["article"], l["id"]) not in have]}
            for r in _jl(OUT / "pt.jsonl")]
    plan = [r for r in plan if r["links"]]
    reqs = requests(lang, model, plan)
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    pi, po = PRICE[model]
    est = chars / 3.2 / 1e6 * pi + len(reqs) * 600 / 1e6 * po
    ids = BatchJob(f"{retry_job}_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"links": sum(len(r["links"]) for r in plan), "requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def pilot(lang: str, plan: list[dict], model: str) -> dict:
    """Direct (non-batch) alignment of a small plan with a given model: {(article, block, link id): phrase}."""
    from elucidario.llm.client import client
    out = {}
    plan_, tr, names, pt = _load(lang, plan)
    done, _ = _deterministic(plan_, tr, names)
    for r in requests(lang, model, plan):
        p = {k: v for k, v in r["params"].items()}
        with client().messages.stream(**p) as s:
            msg = s.get_final_message()
        for b in json.loads(next(x.text for x in msg.content if x.type == "text"))["blocks"]:
            aid, _, bid = b["block"].rpartition(":")
            text = tr.get(f"art:{aid}:{bid}", "")
            for l in b["links"]:
                ph = _balanced(l["phrase"])
                out[(aid, bid, l["id"])] = ph if ph and _find(text, ph, []) else None
    return {"llm": out, "deterministic": sum(len(v) for v in done.values())}
