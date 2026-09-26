"""Phase 4b: taxonomy discovery. Opus proposes free-form types for a stratified sample; a reviewer consolidates.

prepare+submit -> Batch job "taxonomy_discovery"
collect        -> data/04_structured/taxonomy_proposals.jsonl
"""

from __future__ import annotations

import json
import random

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA

IN = DATA / "04_structured" / "articles.jsonl"
OUT = DATA / "04_structured" / "taxonomy_proposals.jsonl"
MODEL = "claude-opus-5-5"

SYSTEM = """You are designing a classification scheme for the entries of the *Elucidário Madeirense* (an encyclopedia of the Madeira archipelago, 1921/1940, ~3,800 entries). You will see one entry. Describe what KIND of entry it is, in English, so that a taxonomy can later be derived from many such descriptions.

Give:
- `primary_type`: the most specific natural category for the entry's subject, 1-4 words, lower case (e.g. "parish", "sítio (hamlet/locality)", "peak", "river/stream", "levada (irrigation channel)", "chapel", "fortress", "clergyman", "governor", "physician", "writer", "noble family/surname", "fish species", "plant species", "bird", "historical event", "epidemic", "storm/flood", "law/decree", "tax", "institution", "newspaper/periodical", "book/work", "custom/tradition", "industry/product", "administrative office", "cross-reference" ...). Invent a better label if none fits.
- `broad_class`: a broader class, 1-3 words (e.g. "person", "place", "building", "organism", "event", "institution", "publication", "concept", "economy", "administration", "culture").
- `secondary_types`: 0-3 other types the entry substantially covers.
- `is_list_of_subentries`: true if the entry is essentially a list of named sub-entries.
- `about`: at most 12 words, what the entry is about."""

SCHEMA = {
    "type": "object",
    "properties": {
        "primary_type": {"type": "string"},
        "broad_class": {"type": "string"},
        "secondary_types": {"type": "array", "items": {"type": "string"}},
        "is_list_of_subentries": {"type": "boolean"},
        "about": {"type": "string"},
    },
    "required": ["primary_type", "broad_class", "secondary_types", "is_list_of_subentries", "about"],
    "additionalProperties": False,
}


def sample(n: int = 300, seed: int = 11) -> list[dict]:
    arts = [json.loads(l) for l in open(IN)]
    arts = [a for a in arts if a["kind"] != "front_matter"]
    rng = random.Random(seed)
    bins: dict[tuple, list] = {}
    for a in arts:
        size = 0 if a["chars"] < 300 else 1 if a["chars"] < 1500 else 2 if a["chars"] < 6000 else 3
        bins.setdefault((a["volume"], size, a["kind"] == "cross_reference"), []).append(a)
    per = {k: max(1, round(n * len(v) / len(arts))) for k, v in bins.items()}
    out = []
    for k, v in bins.items():
        out += rng.sample(v, min(len(v), per[k]))
    rng.shuffle(out)
    return out[:n]


def excerpt(a: dict, limit: int = 3500) -> str:
    parts, size = [], 0
    for b in a["blocks"]:
        t = ("## " if b["type"] == "heading" else "") + b["text"]
        parts.append(t)
        size += len(t)
        if size > limit:
            break
    body = "\n\n".join(parts)[:limit]
    return f"Headword: {a['headword']}\n\n{body}"


def submit() -> dict:
    s = sample()
    reqs = [
        {
            "custom_id": f"t{i:04d}",
            "params": {
                "model": MODEL,
                "max_tokens": 4000,
                "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
                "messages": [{"role": "user", "content": excerpt(a)}],
                "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
            },
        }
        for i, a in enumerate(s)
    ]
    (DATA / "04_structured" / "taxonomy_sample.json").write_text(
        json.dumps({f"t{i:04d}": a["id"] for i, a in enumerate(s)}, indent=0)
    )
    ids = BatchJob("taxonomy_discovery").submit(reqs, budget_usd=3.0, est_usd=1.2)
    return {"requests": len(reqs), "batches": ids}


def collect() -> dict:
    ids = json.loads((DATA / "04_structured" / "taxonomy_sample.json").read_text())
    arts = {json.loads(l)["id"]: json.loads(l) for l in open(IN)}
    n = 0
    with open(OUT, "w") as f:
        for cid, res in BatchJob("taxonomy_discovery").results():
            t = message_text(res)
            if not t:
                continue
            a = arts[ids[cid]]
            f.write(json.dumps({"id": a["id"], "headword": a["headword"], "kind": a["kind"], "chars": a["chars"], **json.loads(t)},
                               ensure_ascii=False) + "\n")
            n += 1
    return {"proposals": n}
