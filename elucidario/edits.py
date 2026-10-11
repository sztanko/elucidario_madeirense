"""Offset-safe edits on serialised paragraphs (text + styled runs + line breaks + page marks)."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Edit:
    start: int
    end: int
    repl: str
    rule: str
    conf: float = 1.0
    before: str = ""

    def to_json(self) -> dict:
        return asdict(self)


def apply_edits(para: dict, edits: list[Edit]) -> tuple[dict, list[Edit]]:
    """Apply non-overlapping edits to a paragraph dict (see layout.Para.to_json). Returns (new_para, applied)."""
    text = para["text"]
    chosen: list[Edit] = []
    last_end = -1
    for e in sorted(edits, key=lambda e: (e.start, -e.conf)):
        if e.start < last_end or e.start > e.end or e.end > len(text):
            continue
        e.before = text[e.start : e.end]
        if e.before == e.repl:
            continue
        chosen.append(e)
        last_end = e.end
    if not chosen:
        return para, []

    def remap(off: int, is_end: bool = False) -> int:
        shift = 0
        for e in chosen:
            if off < e.start or (off == e.start and not is_end):
                break
            if off >= e.end:
                shift += len(e.repl) - (e.end - e.start)
            else:  # inside an edited span: clamp to the replacement
                return e.start + shift + (len(e.repl) if is_end else 0)
        return off + shift

    out, pos = [], 0
    for e in chosen:
        out.append(text[pos : e.start])
        out.append(e.repl)
        pos = e.end
    out.append(text[pos:])
    new = dict(para)
    new["text"] = "".join(out)
    new["runs"] = [[remap(s), remap(t, True), b, i, size] for s, t, b, i, size in para["runs"]]
    new["runs"] = [r for r in new["runs"] if r[1] > r[0]]
    new["nl"] = sorted({remap(o) for o in para["nl"]})
    new["pages"] = [[remap(o), pg, pp] for o, pg, pp in para["pages"]]
    return new, chosen
