"""Portuguese lexicon with tolerance for 1921/1940 orthography.

`Lexicon.known(word)` accepts a token if it is:
  * in the pt-PT Hunspell dictionary (as-is, lowercased or capitalised), or
  * reducible to a dictionary word by undoing period spellings (ph→f, th→t, y→i, double
    consonants, 1940-era circumflexes/graves, "sc"/"ct"/"pt" clusters, ...), or
  * attested often enough in the corpus itself (proper nouns, regional words).
"""

from __future__ import annotations

import itertools
import re
from collections import Counter
from functools import lru_cache

from spylls.hunspell import Dictionary

from elucidario.paths import DATA

DICT = DATA / "cache" / "dict" / "pt_PT"
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)*")

# Period spellings -> modern: each rule is (pattern, replacement); combinations are tried.
ARCHAIC_RULES = [
    ("ph", "f"), ("th", "t"), ("y", "i"), ("rh", "r"), ("ch", "c"), ("mm", "m"), ("ll", "l"), ("nn", "n"),
    ("tt", "t"), ("cc", "c"), ("ff", "f"), ("pp", "p"), ("ss", "s"), ("sc", "c"), ("ct", "t"), ("pt", "t"),
    ("mn", "n"), ("gm", "m"), ("x", "ks"), ("z", "s"), ("s", "z"), ("ão", "am"), ("am", "ão"), ("e", "i"),
    ("i", "e"), ("u", "o"), ("o", "u"),
]
ACCENT_DROP = str.maketrans("ôêâàèìòùÔÊÂÀÈÌÒÙ", "oeaaeiouOEAAEIOU")
ACCENT_SWAP = {"a": "áâà", "e": "éê", "i": "í", "o": "óô", "u": "ú"}


class Lexicon:
    def __init__(self, corpus_counts: Counter | None = None):
        self.dic = Dictionary.from_files(str(DICT))
        self.corpus = corpus_counts or Counter()
        self.verbs: set[str] = set()
        self.cats: dict[str, set[str]] = {}
        for line in open(str(DICT) + ".dic", encoding="utf-8"):
            if "\t" not in line:
                continue
            head, tags = line.rstrip("\n").split("\t", 1)
            stem = head.split("/")[0]
            for cat in re.findall(r"CAT=([a-z_]+)", tags):
                self.cats.setdefault(stem, set()).add(cat)
            if "CAT=v" in tags:
                self.verbs.add(stem)

    @lru_cache(maxsize=500_000)
    def in_dict(self, w: str) -> bool:
        if not w or any(c.isdigit() for c in w):
            return False
        return self.dic.lookup(w) or self.dic.lookup(w.lower()) or self.dic.lookup(w.capitalize())

    @lru_cache(maxsize=500_000)
    def archaic_ok(self, w: str) -> bool:
        """True if some combination of period-spelling rules maps w to a dictionary word."""
        low = w.lower()
        base = {low, low.translate(ACCENT_DROP)}
        # 1940 accents on otherwise unaccented words and missing modern accents
        for b in list(base):
            for i, ch in enumerate(b):
                for alt in ACCENT_SWAP.get(ch, ""):
                    base.add(b[:i] + alt + b[i + 1 :])
        applicable = [r for r in ARCHAIC_RULES if r[0] in low]
        for b in base:
            if self.in_dict(b):
                return True
        for n in (1, 2):
            for combo in itertools.combinations(applicable, n):
                for b in list(base)[:12]:
                    v = b
                    for a, r in combo:
                        v = v.replace(a, r)
                    if v != b and self.in_dict(v):
                        return True
        return False

    def known(self, w: str, min_corpus: int = 3) -> bool:
        if self.in_dict(w):
            return True
        if self.corpus.get(w, 0) >= min_corpus or self.corpus.get(w.lower(), 0) >= min_corpus:
            return True
        return self.archaic_ok(w)

    @lru_cache(maxsize=200_000)
    def is_verb_form(self, w: str) -> bool:
        low = w.lower()
        try:
            for form in self.dic.lookuper.good_forms(low):
                if form.in_dictionary and form.in_dictionary.stem in self.verbs:
                    return True
        except Exception:
            return False
        return low in self.verbs
