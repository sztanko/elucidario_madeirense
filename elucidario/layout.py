"""Paragraph model built from Phase 1 lines.

A paragraph is normalised running text plus parallel style runs, visual line-break offsets
and page-change offsets, so every later stage can slice by character offset.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from elucidario.paths import DATA


@dataclass
class Run:
    start: int
    end: int
    b: bool
    i: bool
    size: str  # "head" | "normal" | "small"


@dataclass
class Para:
    vol: int
    text: str = ""
    runs: list[Run] = field(default_factory=list)
    nl: list[int] = field(default_factory=list)  # offsets where a visual line break occurred
    pages: list[tuple[int, int, int | None]] = field(default_factory=list)  # (offset, pdf_page, printed_page)

    # ---- construction -------------------------------------------------
    def _append(self, t: str, b: bool, i: bool, size: str) -> None:
        if not t:
            return
        start = len(self.text)
        self.text += t
        if self.runs and (self.runs[-1].b, self.runs[-1].i, self.runs[-1].size) == (b, i, size) and self.runs[-1].end == start:
            self.runs[-1].end = len(self.text)
        else:
            self.runs.append(Run(start, len(self.text), b, i, size))

    def add_line(self, row: dict) -> None:
        page = (row["page"], row["printed_page"])
        if not self.pages or self.pages[-1][1:] != page:
            self.pages.append((len(self.text), *page))
        if self.text:
            self.nl.append(len(self.text))
            if self.text.endswith("-") and not self.text.endswith(" -"):
                pass  # real compound hyphen at line end: join without space
            elif not self.text.endswith(" "):
                self._append(" ", *self._last_style())
        for s in row["spans"]:
            t = re.sub(r"\s+", " ", s["t"].replace(" ", " "))
            if not self.text or self.text.endswith(" "):
                t = t.lstrip(" ")
            self._append(t, s["b"], s["i"], size_class(self.vol, s))

    def _last_style(self) -> tuple[bool, bool, str]:
        r = self.runs[-1]
        return r.b, r.i, r.size

    def finish(self) -> "Para":
        stripped = self.text.rstrip()
        if len(stripped) != len(self.text):
            self.slice_inplace(0, len(stripped))
        return self

    # ---- slicing ------------------------------------------------------
    def slice(self, a: int, b: int | None = None) -> "Para":
        b = len(self.text) if b is None else b
        p = Para(self.vol)
        p.text = self.text[a:b]
        p.runs = [Run(max(r.start, a) - a, min(r.end, b) - a, r.b, r.i, r.size) for r in self.runs if r.end > a and r.start < b]
        p.nl = [o - a for o in self.nl if a < o < b]
        pages = [pg for pg in self.pages if pg[0] <= a]
        first = pages[-1] if pages else self.pages[0]
        p.pages = [(0, first[1], first[2])] + [(o - a, pg, pp) for o, pg, pp in self.pages if a < o < b]
        # trim leading whitespace
        lead = len(p.text) - len(p.text.lstrip())
        if lead:
            p = p.slice(lead) if lead < len(p.text) else p
        return p

    def slice_inplace(self, a: int, b: int) -> None:
        p = self.slice(a, b)
        self.text, self.runs, self.nl, self.pages = p.text, p.runs, p.nl, p.pages

    def style_at(self, off: int) -> Run | None:
        for r in self.runs:
            if r.start <= off < r.end:
                return r
        return None

    @property
    def page_range(self) -> tuple[int, int]:
        return self.pages[0][1], self.pages[-1][1]

    @property
    def printed_range(self) -> tuple[int | None, int | None]:
        return self.pages[0][2], self.pages[-1][2]

    def to_json(self) -> dict:
        return {
            "text": self.text,
            "runs": [[r.start, r.end, int(r.b), int(r.i), r.size] for r in self.runs if (r.b or r.i or r.size != "normal")],
            "nl": self.nl,
            "pages": [list(p) for p in self.pages],
        }

    @classmethod
    def from_json(cls, vol: int, d: dict) -> "Para":
        p = cls(vol)
        p.text = d["text"]
        styled = sorted(d["runs"])
        runs, pos = [], 0
        for s, e, b, i, size in styled:
            if s > pos:
                runs.append(Run(pos, s, False, False, "normal"))
            runs.append(Run(s, e, bool(b), bool(i), size))
            pos = e
        if pos < len(p.text):
            runs.append(Run(pos, len(p.text), False, False, "normal"))
        p.runs = runs
        p.nl = d["nl"]
        p.pages = [tuple(x) for x in d["pages"]]
        return p


def size_class(vol: int, s: dict) -> str:
    if s["size"] <= 8:
        return "small"
    if s["size"] >= 19:
        return "letter"
    if vol in (1, 2) and s["size"] >= 12:
        return "head"
    return "normal"


def load_paragraphs(vol: int) -> list[Para]:
    out: list[Para] = []
    cur: Para | None = None
    with open(DATA / "01_layout" / f"vol_{vol}.jsonl", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row["blank"]:
                if cur and cur.text.strip():
                    out.append(cur.finish())
                cur = None
                continue
            if cur is None:
                cur = Para(vol)
            cur.add_line(row)
    if cur and cur.text.strip():
        out.append(cur.finish())
    return out
