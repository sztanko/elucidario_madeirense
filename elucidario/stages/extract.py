"""Phase 1: layout extraction.

Reads the three source PDFs with PyMuPDF and writes one JSONL row per *visual line*
(spans that share a baseline are merged), with page furniture removed.

Output: data/01_layout/vol_{n}.jsonl, rows:
    {vol, page, printed_page, y, x, blank, spans: [{t, font, size, b, i}]}

`x`/`y` are logical coordinates (reading direction), so rotated vol 3 pages look like vols 1-2.
`blank` is True for whitespace-only lines, which the book uses as paragraph separators.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pymupdf

from elucidario.paths import DATA, SOURCE

OUT = DATA / "01_layout"

# Fonts that only ever carry running headers, page numbers or front-matter decoration.
FURNITURE_FONTS = {
    1: {"Century"},
    2: {"Century"},
    3: {"ArialNarrow,Bold", "PalatinoLinotype,Bold", "PalatinoLinotype", "Courier", "Courier-Bold"},
}
PAGE_NUMBER_FONTS = {"TimesNewRomanPSMT", "Courier"}
# Two private glyphs in vol 1 (Times New Roman 14px) are opening/closing quotes.
GLYPH_FIXES = {"Ҙ": "“", "ҙ": "”", "­": ""}


def _logical(line: dict, page_height: float) -> tuple[float, float]:
    x0, y0, x1, y1 = line["bbox"]
    dx, dy = line["dir"]
    if round(dx) == 1:
        return x0, y1
    # vol 3: text runs bottom-to-top on an unrotated portrait page
    return page_height - y1, x1


def _span(s: dict) -> dict:
    font = s["font"]
    text = s["text"]
    for a, b in GLYPH_FIXES.items():
        text = text.replace(a, b)
    return {
        "t": text,
        "font": font,
        "size": round(s["size"], 1),
        "b": "Bold" in font or bool(s["flags"] & 16),
        "i": "Italic" in font or bool(s["flags"] & 2),
    }


def extract_volume(vol: int) -> list[dict]:
    doc = pymupdf.open(SOURCE / f"vol_{vol}.pdf")
    rows: list[dict] = []
    for page in doc:
        height = page.mediabox.height
        raw: list[tuple[float, float, list[dict]]] = []
        printed = None
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                x, y = _logical(line, height)
                spans = [_span(s) for s in line["spans"]]
                fonts = {s["font"] for s in spans if s["t"].strip()}
                if fonts and fonts <= PAGE_NUMBER_FONTS:
                    txt = "".join(s["t"] for s in spans).strip()
                    if re.fullmatch(r"\d{1,4}", txt):
                        printed = int(txt)
                        continue
                if fonts and fonts <= FURNITURE_FONTS[vol]:
                    continue
                if vol in (1, 2) and y < 60:  # whitespace header rule
                    continue
                if not fonts and any(s["font"] in FURNITURE_FONTS[vol] | PAGE_NUMBER_FONTS for s in spans):
                    continue
                raw.append((y, x, spans))
        # merge fragments sharing a visual line (e.g. 14px "(Vid. 1-289)." inside an 11px line)
        merged: list[dict] = []
        for y, x, spans in raw:
            if merged and abs(merged[-1]["_y"] - y) <= 4.5 and x >= merged[-1]["_xend"] - 2:
                cur = merged[-1]
                cur["spans"].extend(spans)
                cur["_xend"] = x + 1
                continue
            merged.append({"_y": y, "x": round(x, 1), "_xend": x + 1, "spans": spans})
        for m in merged:
            spans = [s for s in m["spans"] if s["t"] != ""]
            text = "".join(s["t"] for s in spans)
            rows.append(
                {
                    "vol": vol,
                    "page": page.number + 1,
                    "printed_page": printed,
                    "y": round(m["_y"], 1),
                    "x": m["x"],
                    "blank": not text.strip(),
                    "spans": [] if not text.strip() else _compact(spans),
                }
            )
    return rows


def _compact(spans: list[dict]) -> list[dict]:
    """Merge adjacent spans with identical style; normalise whitespace-only spans to the previous style."""
    out: list[dict] = []
    for s in spans:
        if out and (not s["t"].strip() or _style(out[-1]) == _style(s)):
            out[-1]["t"] += s["t"]
            continue
        out.append(dict(s))
    return out


def _style(s: dict) -> tuple:
    return (s["font"], s["size"], s["b"], s["i"])


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    stats = {}
    for vol in (1, 2, 3):
        rows = extract_volume(vol)
        with open(OUT / f"vol_{vol}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        fonts = Counter()
        for r in rows:
            for s in r["spans"]:
                fonts[(s["font"], s["size"])] += len(s["t"].strip())
        stats[vol] = {
            "lines": len(rows),
            "text_lines": sum(not r["blank"] for r in rows),
            "chars": sum(fonts.values()),
            "pages_without_printed_number": sum(1 for p in {(r["page"], r["printed_page"]) for r in rows} if p[1] is None),
            "fonts": {f"{k[0]} {k[1]}": v for k, v in fonts.most_common(12)},
        }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats
