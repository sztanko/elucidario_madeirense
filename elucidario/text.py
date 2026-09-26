"""Shared text helpers: normalisation, collation keys, paragraph assembly."""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

from pyuca import Collator

_collator = Collator()


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(s: str) -> str:
    """Lowercase, accent-free, alphanumerics and single spaces only."""
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


@lru_cache(maxsize=None)
def sort_key(headword: str) -> tuple:
    """Collation key used by the book: headword without qualifier, accent/case-insensitive."""
    main = re.split(r"[(,.]", headword, maxsplit=1)[0]
    n = norm(main)
    # OCR digits inside headwords (e.g. "P6rto") should not break ordering
    n = n.translate(str.maketrans("0156", "olso"))
    return _collator.sort_key(n)


def join_lines(lines: list[str]) -> str:
    """Join visual lines into running text. Line-final hyphens are real compounds (kept, no space)."""
    out = ""
    for ln in lines:
        ln = ln.replace(" ", " ")
        if not out:
            out = ln.lstrip()
        elif out.rstrip().endswith("-") and not out.rstrip().endswith(" -"):
            out = out.rstrip() + ln.lstrip()
        else:
            out = out.rstrip() + " " + ln.lstrip()
    return re.sub(r"[ \t]+", " ", out).strip()


@lru_cache(maxsize=None)
def coarse_key(headword: str, n: int = 3) -> tuple:
    main = re.split(r"[(,.]", headword, maxsplit=1)[0]
    k = norm(main).replace(" ", "").translate(str.maketrans("0156", "olso"))
    return _collator.sort_key(k[:n])
