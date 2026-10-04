"""Reading kb/names/<lang>.jsonl. A Portuguese name may have several rows with different `sense` values (e.g.
"São Vicente" the parish and "São Vicente" the saint, see docs/naming_latin.md §9); every consumer goes through here.
"""

from __future__ import annotations

import json
from collections import defaultdict

from elucidario.paths import KB

PLACE_SENSES = {"place", "foreign", "building", "religious", "institution"}
PERSON_SENSES = {"person", "saint"}


def rows(lang: str) -> dict[str, list[dict]]:
    """{pt: [row, ...]} — usually one row; homonyms have one row per sense."""
    out: dict[str, list[dict]] = defaultdict(list)
    p = KB / "names" / f"{lang}.jsonl"
    if p.exists():
        for line in open(p):
            x = json.loads(line)
            out[x["pt"]].append(x)
    return out


def pick(cands: list[dict] | None, kind: str | None = None) -> dict | None:
    """The row for this kind of entity ("place" or "person"); the first row when the kind is unknown or absent."""
    if not cands:
        return None
    if kind:
        want = PLACE_SENSES if kind == "place" else PERSON_SENSES if kind == "person" else {kind}
        for x in cands:
            if (x.get("sense") or x.get("type")) in want:
                return x
    return cands[0]


def for_prompt(lang: str, field: str = "first") -> dict[str, str]:
    """{pt: form} for translation prompts. Homonyms list every sense so the translator can choose by context:
    "São Vicente" -> "[place] São Vicente (‘St Vincent’) | [saint] St Vincent of Saragossa (*São Vicente*)"."""
    out = {}
    for pt, cands in rows(lang).items():
        vals = [(x.get("sense") or x.get("type") or "", x.get(field) or x.get("rendering") or pt) for x in cands]
        out[pt] = vals[0][1] if len(vals) == 1 else " | ".join(f"[{s}] {v}" for s, v in vals)
    return out
