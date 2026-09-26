"""Benchmark Jev (TypeSafe System One) against Claude on two closed-set tasks from this corpus.

Task A - OCR triage: is an out-of-lexicon token an OCR/typing error or a legitimate word?
         Gold labels: Claude Opus 5.5 (medium effort), with a correction for errors.
Task B - Segmentation: article / subarticle / reject for the 197 reviewed boundary candidates.
         Gold labels: the reviewed decisions (data/02_segments/decisions_review.yaml).

Run: uv run python -m elucidario.bench.jev_bench [prepare|gold|run|report]
Outputs in data/bench/.
"""

from __future__ import annotations

import asyncio
import json
import random
import re
import sys
from collections import Counter

import yaml

from elucidario.lexicon import WORD_RE, Lexicon
from elucidario.llm.client import client, load_env
from elucidario.paths import DATA

OUT = DATA / "bench"
OCR_ITEMS = OUT / "ocr_items.jsonl"
SEG_ITEMS = OUT / "seg_items.jsonl"

OCR_INSTR = (
    "The token comes from a Portuguese encyclopedia printed in 1921/1940 and digitised by OCR. "
    "Decide whether the token, as written, is an OCR or typing error, or a legitimate form."
)
OCR_CRITERIA = {
    "ocr_error": "Garbled or misspelt: wrong, missing, extra or swapped letters or digits that a correct printing would not have "
    "(e.g. 'Madeisra' for Madeira, 'denominagao' for denominação, 'fundaçâo', 'amtes' for antes).",
    "legitimate": "Correct as printed: an ordinary Portuguese word, an old spelling of the period (pharmacia, theatro, pôrto, "
    "acquiriu, vehiculos), a proper name, a Latin scientific name, an abbreviation, or a word in another language.",
}
SEG_INSTR = (
    "An encyclopedia of Madeira is being split into entries. 'text' starts at a candidate headword. "
    "Decide what this candidate is, using the neighbouring accepted headwords and the preceding text."
)
SEG_CRITERIA = {
    "article": "A separate encyclopedia entry with its own headword in the alphabetical sequence (ordering can be loose).",
    "subarticle": "A named sub-entry inside the preceding umbrella article, e.g. one river in a list of rivers, one wheat "
    "variety inside 'Trigo', one folk remedy inside 'Medicina Campestre', one club inside 'Clubes'.",
    "reject": "Not a heading: a sentence start, table row, cross-reference continuation ('V. X'), a label ending in ':' "
    "or an all-caps table heading.",
}


# ---------------------------------------------------------------- prepare
def prepare(n: int = 300, seed: int = 7) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    arts = [json.loads(l) for l in open(DATA / "02_segments" / "articles.jsonl")]
    cnt: Counter = Counter()
    ctx: dict[str, str] = {}
    for a in arts:
        for p in a["paragraphs"]:
            for m in WORD_RE.finditer(p["text"]):
                w = m.group(0)
                cnt[w] += 1
                if w not in ctx:
                    ctx[w] = p["text"][max(0, m.start() - 90) : m.end() + 90]
    lex = Lexicon(cnt)
    unknown = [w for w in cnt if not w.isdigit() and not any(c.isdigit() for c in w) and len(w) > 2 and not lex.known(w)]
    random.Random(seed).shuffle(unknown)
    with open(OCR_ITEMS, "w") as f:
        for w in unknown[:n]:
            f.write(json.dumps({"id": w, "token": w, "context": ctx[w], "freq": cnt[w]}, ensure_ascii=False) + "\n")
    # segmentation items with reviewed labels
    dec = yaml.safe_load(open(DATA / "02_segments" / "decisions_review.yaml"))
    with open(SEG_ITEMS, "w") as f:
        for line in open(DATA / "02_segments" / "review_packet.jsonl"):
            it = json.loads(line)
            d = dec.get(it["cid"])
            if not d:
                continue
            it["gold"] = d["decision"]
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print("ocr items", n, "of", len(unknown), "unknown; seg items", sum(1 for _ in open(SEG_ITEMS)))


# ---------------------------------------------------------------- claude
def claude_labels(task: str, model: str, effort: str | None = None, chunk: int = 25) -> dict[str, dict]:
    items = [json.loads(l) for l in open(OCR_ITEMS if task == "ocr" else SEG_ITEMS)]
    key = "id" if task == "ocr" else "cid"
    crit = OCR_CRITERIA if task == "ocr" else SEG_CRITERIA
    instr = OCR_INSTR if task == "ocr" else SEG_INSTR
    labels = list(crit)
    schema = {
        "type": "object",
        "properties": {
            "answers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string", "enum": labels},
                        **({"correction": {"type": "string"}} if task == "ocr" else {}),
                    },
                    "required": ["id", "label"] + (["correction"] if task == "ocr" else []),
                    "additionalProperties": False,
                },
            }
        },
        "required": ["answers"],
        "additionalProperties": False,
    }
    system = instr + "\nLabels:\n" + "\n".join(f"- {k}: {v}" for k, v in crit.items())
    if task == "ocr":
        system += "\nFor ocr_error give the corrected token in 'correction'; for legitimate repeat the token unchanged."
    out: dict[str, dict] = {}
    c = client()
    for i in range(0, len(items), chunk):
        batch = items[i : i + chunk]
        payload = [
            {"id": it[key], **({"token": it["token"], "context": it["context"]} if task == "ocr" else
             {"head": it["head"], "prev_headwords": it["prev_headwords"], "next_headwords": it["next_headwords"],
              "before": it["before"][-200:], "text": it["text"][:300]})}
            for it in batch
        ]
        kwargs = dict(
            model=model,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": "Label every item:\n" + json.dumps(payload, ensure_ascii=False)}],
            output_config={"format": {"type": "json_schema", "schema": schema}, **({"effort": effort} if effort else {})},
        )
        if model.startswith("claude-sonnet"):
            kwargs["thinking"] = {"type": "disabled"}
        r = c.messages.create(**kwargs)
        text = next(b.text for b in r.content if b.type == "text")
        for a in json.loads(text)["answers"]:
            out[a["id"]] = a
        usage = (r.usage.input_tokens, r.usage.output_tokens)
        print(f"  {model} {task} {i + len(batch)}/{len(items)} usage={usage}", file=sys.stderr)
    return out


# ---------------------------------------------------------------- jev
async def jev_labels(task: str, concurrency: int = 16) -> dict[str, dict]:
    from typesafe_sdk import AsyncTypeSafeClient, Choice

    load_env()
    items = [json.loads(l) for l in open(OCR_ITEMS if task == "ocr" else SEG_ITEMS)]
    key = "id" if task == "ocr" else "cid"
    q = Choice(instructions=OCR_INSTR if task == "ocr" else SEG_INSTR, criteria=OCR_CRITERIA if task == "ocr" else SEG_CRITERIA)
    sem = asyncio.Semaphore(concurrency)
    out: dict[str, dict] = {}
    tokens = 0
    async with AsyncTypeSafeClient() as c:

        async def one(it):
            nonlocal tokens
            state = (
                {"token": it["token"], "context": it["context"]}
                if task == "ocr"
                else {"candidate_headword": it["head"], "previous_accepted_headwords": it["prev_headwords"],
                      "next_accepted_headwords": it["next_headwords"], "preceding_text": it["before"][-200:],
                      "text": it["text"][:300]}
            )
            async with sem:
                r = await c.system_one(state=state, questions={"q": q})
            a = r.choices["q"]
            tokens += r.usage.input_tokens
            out[it[key]] = {"label": a.choice, "confidence": a.confidence, "probabilities": dict(a.probabilities)}

        await asyncio.gather(*(one(it) for it in items))
    print(f"  jev {task} input tokens {tokens}", file=sys.stderr)
    return out


# ---------------------------------------------------------------- orchestration
def save(name: str, data: dict) -> None:
    (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))


def load(name: str) -> dict:
    return json.loads((OUT / f"{name}.json").read_text())


def report() -> str:
    lines = []
    ocr_gold = {k: v["label"] for k, v in load("ocr_gold_opus").items()}
    seg_items = [json.loads(l) for l in open(SEG_ITEMS)]
    seg_gold = {it["cid"]: it["gold"] for it in seg_items}
    for task, gold, systems in (
        ("ocr", ocr_gold, ["ocr_sonnet", "ocr_haiku", "ocr_jev"]),
        ("seg", seg_gold, ["seg_opus", "seg_sonnet", "seg_haiku", "seg_jev"]),
    ):
        lines.append(f"## Task {task}: n={len(gold)}, gold distribution {dict(Counter(gold.values()))}")
        for s in systems:
            try:
                pred = load(s)
            except FileNotFoundError:
                continue
            ks = [k for k in gold if k in pred]
            acc = sum(pred[k]["label"] == gold[k] for k in ks) / max(1, len(ks))
            row = f"- {s}: accuracy {acc:.1%} on {len(ks)}"
            if "jev" in s:
                for th in (0.5, 0.7, 0.85):
                    hi = [k for k in ks if pred[k]["confidence"] >= th]
                    if hi:
                        a2 = sum(pred[k]["label"] == gold[k] for k in hi) / len(hi)
                        row += f"; conf≥{th}: {a2:.1%} on {len(hi)} ({len(hi) / len(ks):.0%} coverage)"
            # per-class recall
            rec = []
            for lab in sorted(set(gold.values())):
                kk = [k for k in ks if gold[k] == lab]
                if kk:
                    rec.append(f"{lab} recall {sum(pred[k]['label'] == lab for k in kk) / len(kk):.0%}")
            lines.append(row + " | " + ", ".join(rec))
    return "\n".join(lines)


def main(cmd: str) -> None:
    if cmd == "prepare":
        prepare()
    elif cmd == "gold":
        save("ocr_gold_opus", claude_labels("ocr", "claude-opus-5-5", effort="medium"))
    elif cmd == "run":
        save("ocr_sonnet", claude_labels("ocr", "claude-sonnet-5"))
        save("ocr_haiku", claude_labels("ocr", "claude-haiku-4-5"))
        save("ocr_jev", asyncio.run(jev_labels("ocr")))
        save("seg_opus", claude_labels("seg", "claude-opus-5-5", effort="medium"))
        save("seg_sonnet", claude_labels("seg", "claude-sonnet-5"))
        save("seg_haiku", claude_labels("seg", "claude-haiku-4-5"))
        save("seg_jev", asyncio.run(jev_labels("seg")))
    elif cmd == "report":
        r = report()
        (OUT / "report.md").write_text(r)
        print(r)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "report")
