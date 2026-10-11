"""Phase 3a: deterministic OCR/typesetting fixes with a reversible edit log.

Input:  data/02_segments/articles.jsonl
Output: data/03_clean/articles.rules.jsonl   (paragraphs after rule fixes)
        data/03_clean/edits.rules.jsonl      (one row per applied edit)
        data/03_clean/suspects.jsonl         (unresolved suspects for the LLM proofreading pass)

Period orthography (ph/th/y, pôrto, Agôsto, quoted 16th-century spellings) is never changed.
"""

from __future__ import annotations

import itertools
import json
import re
from collections import Counter

from elucidario.edits import Edit, apply_edits
from elucidario.lexicon import WORD_RE, Lexicon
from elucidario.paths import DATA

IN = DATA / "02_segments" / "articles.jsonl"
OUT = DATA / "03_clean"

DIGIT_SUBST = {"0": "oO", "1": "liI", "6": "óôo", "5": "s", "3": "eê", "4": "a", "8": "a", "7": "l"}
SEED_FIXES = {  # legacy/convert.py remove_ocr_errors (verified list)
    "Ant6nio": "António", "ilh6u": "ilhéu", "Ju1ho": "Julho", "del1e": "dele", "ing1ês": "inglês",
    "Gonça1ves": "Gonçalves", "MadaZe7ia": "Madalena", "dó1ar": "dólar", "Hist6rico": "Histórico",
    "Hist6ria": "História", "col6nia": "colónia", "tamb6m": "também", "Cust6dio": "Custódio", "Vlt6ria": "Vitória",
    "Al1guns": "Alguns", "a1çapremas": "alçapremas", "Si1va": "Silva",
}
UNIT_TOKEN = re.compile(r"^\d+(?:m|km|cm|mm|kg|g|h|ha|l|mil|s|a|o|º|ª)$|^[nN]\d+$|^m\d+$|^k\d+$")
CLITICS = ("se", "me", "te", "lhe", "lhes", "lo", "la", "los", "las")
NOT_VERBS = {"a", "o", "e", "as", "os", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "que", "um", "uma",
             "com", "por", "para", "ao", "aos", "à", "às", "á", "ás", "também", "logo", "já", "ainda", "este", "esta",
             "entre", "sobre", "até", "desde", "neste", "nesta", "muito", "mais", "bem", "então"}
# verbs after which "se" usually means "whether/if" (sabendo se ..., verificar se ...)
WHETHER_VERBS = {"saber", "sabendo", "sabe", "sabia", "sabiam", "sabemos", "verificar", "verificando", "verificou", "dizer",
                 "diz", "disse", "perguntar", "perguntou", "perguntando", "ver", "vendo", "averiguar", "ignora", "ignorando",
                 "ignoramos", "duvidar", "duvida", "examinar", "indagar", "resolver", "decidir", "consultar", "informar"}


def corpus_counts(arts: list[dict]) -> Counter:
    c: Counter = Counter()
    for a in arts:
        c.update(WORD_RE.findall(a["headword"]))
        for p in a["paragraphs"]:
            c.update(WORD_RE.findall(p["text"]))
    return c


def hyphenated_counts(arts: list[dict]) -> Counter:
    c: Counter = Counter()
    pat = re.compile(r"\b([A-Za-zÀ-ÿ]+)-(" + "|".join(CLITICS) + r")\b")
    for a in arts:
        for p in a["paragraphs"]:
            for m in pat.finditer(p["text"]):
                c[(m.group(1).lower(), m.group(2))] += 1
    return c


class Rules:
    def __init__(self, lex: Lexicon, counts: Counter, hyph: Counter):
        self.lex, self.counts, self.hyph = lex, counts, hyph

    # ---- token-level -------------------------------------------------
    def digit_in_word(self, tok: str) -> tuple[str, float] | None:
        if tok in SEED_FIXES:
            return SEED_FIXES[tok], 1.0
        letters = sum(c.isalpha() for c in tok)
        digits = [i for i, c in enumerate(tok) if c.isdigit()]
        if letters < 2 or not digits or len(digits) > 2 or UNIT_TOKEN.match(tok):
            return None
        # digits must sit inside or at the edge of a letter run, not be a leading number ("12h")
        if tok[0].isdigit() and tok[-1].isalpha() and all(c.isdigit() for c in tok[: digits[-1] + 1]):
            return None
        options = [DIGIT_SUBST.get(tok[i], "") for i in digits]
        if not all(options):
            return None
        cands = []
        for combo in itertools.product(*options):
            w = list(tok)
            for i, ch in zip(digits, combo):
                w[i] = ch
            w = "".join(w)
            if self.lex.in_dict(w) or self.counts.get(w, 0) >= 2:
                cands.append(w)
        if not cands:
            return None
        # candidates are generated in substitution-priority order (6 -> ó before ô before o)
        conf = 0.95 if len(cands) == 1 else 0.7
        return cands[0], conf

    @staticmethod
    def letters_in_number(tok: str) -> str | None:
        """l748 -> 1748, 182l -> 1821, I910 -> 1910, 3O -> 30 (only when the rest are digits)."""
        if re.fullmatch(r"[I1]{2,4}", tok) and "I" in tok:
            return tok.replace("1", "I")  # garbled Roman numeral: "I1" -> "II"
        if not re.fullmatch(r"[0-9lIO]{2,6}", tok):
            return None
        if sum(c.isdigit() for c in tok) < max(1, len(tok) - 2):
            return None
        fixed = tok.replace("l", "1").replace("I", "1").replace("O", "0")
        return fixed if fixed != tok and fixed.isdigit() else None

    # ---- paragraph-level ---------------------------------------------
    def paragraph_edits(self, para: dict) -> tuple[list[Edit], list[dict]]:
        text = para["text"]
        edits: list[Edit] = []
        suspects: list[dict] = []
        for m in WORD_RE.finditer(text):
            tok = m.group(0)
            if any(c.isdigit() for c in tok) and any(c.isalpha() for c in tok):
                num = self.letters_in_number(tok)
                if num:
                    edits.append(Edit(m.start(), m.end(), num, "letters-in-number", 0.95))
                    continue
                fix = self.digit_in_word(tok)
                if fix:
                    edits.append(Edit(m.start(), m.end(), fix[0], "digit-in-word", fix[1]))
                elif not UNIT_TOKEN.match(tok):
                    suspects.append({"start": m.start(), "end": m.end(), "token": tok, "why": "digit-mix"})
        # "0" used for the article "O"
        for m in re.finditer(r"(?:(?<=^)|(?<=[.!?:;»”\"(] )|(?<=[(«“\"]))0(?= [A-Za-zÀ-ÿ])", text):
            edits.append(Edit(m.start(), m.end(), "O", "zero-for-O", 0.95))
        for m in re.finditer(r"(?<=[a-zà-ÿ,] )0(?= ([a-zà-ÿA-ZÀ-Ý])[a-zà-ÿ]{2,})", text):
            prev = text[max(0, m.start() - 12) : m.start()]
            nxt = text[m.end() : m.end() + 8]
            if re.search(r"\b(das|às|ás|as)\s*$", prev) or re.match(r"\s+(até|horas|e)\b", nxt):
                continue
            if not re.search(r"\d[\s,.]*$|n\.[ºo°] ?$", prev):
                # before a capital it is the article of a title: "o jornal 0 Povo" -> "O Povo"
                repl = "O" if m.group(1).isupper() else "o"
                edits.append(Edit(m.start(), m.end(), repl, "zero-for-o", 0.85))
        for m in re.finditer(r"\((0)\)", text):
            edits.append(Edit(m.start(1), m.end(1), "O", "zero-for-O", 0.95))
        # stray soft-hyphen sign
        for m in re.finditer(r"(?<=[A-Za-zÀ-ÿ])¬ ?(?=[a-zà-ÿ])", text):
            edits.append(Edit(m.start(), m.end(), "", "not-sign", 0.98))
        # glued words at an italic boundary ("géneroOcimum", "nesteElucidário"): lower|Upper across the boundary
        for s_, e_, b, i, size in para["runs"]:
            for off in (s_, e_):
                if 0 < off < len(text) and text[off - 1].islower() and text[off].isupper() and size != "small":
                    edits.append(Edit(off, off, " ", "glued-style-boundary", 0.9))
        # space before punctuation (not dot leaders, not "V. X ." inside tables)
        for m in re.finditer(r"(?<=[A-Za-zÀ-ÿ0-9»”)]) +(?=[,;:!?](?![,;:!?])|\.(?![.\d]|\s\.))", text):
            edits.append(Edit(m.start(), m.end(), "", "space-before-punct", 0.9))
        # doubled full stop ("etc..") but not an ellipsis
        for m in re.finditer(r"(?<![.\s])\.\.(?![.])", text):
            edits.append(Edit(m.start(), m.end(), ".", "double-period", 0.9))
        # missing space after ":" / ";" before a letter ("1521:e"), not the period ":—"
        for m in re.finditer(r"(?<=[0-9a-zà-ÿ])([:;])(?=[A-Za-zÀ-ÿ«“])", text):
            edits.append(Edit(m.end(), m.end(), " ", "space-after-colon", 0.85))
        # doubled spaces
        for m in re.finditer(r"  +", text):
            edits.append(Edit(m.start(), m.end(), " ", "double-space", 1.0))
        # hyphen + space inside a word: broken line-end split ("britani- cos") or compound ("estabeleceram- se")
        for m in re.finditer(r"(?<=[a-zà-ÿ])- (?=[a-zà-ÿ])", text):
            left = re.search(r"[A-Za-zÀ-ÿ]+$", text[: m.start()]).group(0)
            right = re.match(r"[A-Za-zÀ-ÿ]+", text[m.end() :]).group(0)
            if right in CLITICS or self.lex.in_dict(f"{left}-{right}"):
                edits.append(Edit(m.start(), m.end(), "-", "hyphen-space", 0.85))
            elif self.lex.known(left + right) and not self.lex.in_dict(left):
                edits.append(Edit(m.start(), m.end(), "", "split-word", 0.8))
            elif self.lex.known(left) and self.lex.known(right):
                edits.append(Edit(m.start(), m.end(), " — ", "hyphen-as-dash", 0.8))
        # missing clitic hyphen ("Destinava se a publicação" -> "Destinava-se")
        for m in re.finditer(r"\b([A-Za-zÀ-ÿ]{3,}) (" + "|".join(CLITICS) + r")\b", text):
            verb, cl = m.group(1), m.group(2)
            if not self.lex.is_verb_form(verb):
                continue
            if cl == "se":
                prev_word = re.search(r"(\S+)\s+$", text[: m.start()])
                nxt = re.match(r"\s*([A-Za-zÀ-ÿ]+)", text[m.end() :])
                if verb.lower() in WHETHER_VERBS or (prev_word and prev_word.group(1).lower() in ("não", "se")):
                    continue
                # "se" before another finite verb belongs to that verb ("estabeleceu se dissolvesse")
                w2 = nxt.group(1).lower() if nxt else ""
                if w2 and w2 not in NOT_VERBS and self.lex.is_verb_form(w2) and not w2.endswith(("ado", "ada", "ados", "adas", "ido", "ida", "idos", "idas")):
                    suspects.append({"start": m.start(), "end": m.end(), "token": m.group(0), "why": "clitic-se-before-verb"})
                    continue
            seen = self.hyph.get((verb.lower(), cl), 0)
            if cl in ("lo", "la", "los", "las") and verb[-1] in "áéêíóô":
                edits.append(Edit(m.end(1), m.start(2), "-", "clitic-hyphen", 0.9))
            elif seen >= 2 or (seen >= 1 and cl != "se"):
                edits.append(Edit(m.end(1), m.start(2), "-", "clitic-hyphen", 0.85))
            elif cl != "se" or seen:
                suspects.append({"start": m.start(), "end": m.end(), "token": m.group(0), "why": "clitic"})
            elif re.match(r"^(ava|ou|ia|iu|eu|ram|am|em|ando|endo|indo|ar|er|ir)$", verb.lower()[-4:][-3:]) or verb[0].isupper():
                suspects.append({"start": m.start(), "end": m.end(), "token": m.group(0), "why": "clitic-se"})
        return edits, suspects


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    arts = [json.loads(l) for l in open(IN)]
    counts = corpus_counts(arts)
    lex = Lexicon(counts)
    rules = Rules(lex, counts, hyphenated_counts(arts))
    by_rule: Counter = Counter()
    n_susp = 0
    with open(OUT / "articles.rules.jsonl", "w") as fa, open(OUT / "edits.rules.jsonl", "w") as fe, open(
        OUT / "suspects.jsonl", "w"
    ) as fs:
        for a in arts:
            new_paras = []
            for pi, p in enumerate(a["paragraphs"]):
                edits, suspects = rules.paragraph_edits(p)
                newp, applied = apply_edits(p, edits)
                new_paras.append(newp)
                for e in applied:
                    by_rule[e.rule] += 1
                    fe.write(json.dumps({"seq": a["seq"], "para": pi, **e.to_json()}, ensure_ascii=False) + "\n")
                for s in suspects:
                    n_susp += 1
                    s.update(seq=a["seq"], para=pi, context=p["text"][max(0, s["start"] - 80) : s["end"] + 80])
                    fs.write(json.dumps(s, ensure_ascii=False) + "\n")
            # headword: digit/letter fixes only
            head = a["headword"]
            for m in list(WORD_RE.finditer(head))[::-1]:
                fix = rules.letters_in_number(m.group(0)) or (rules.digit_in_word(m.group(0)) or (None,))[0]
                if fix:
                    head = head[: m.start()] + fix + head[m.end() :]
                    by_rule["headword-digit"] += 1
            head = re.sub(r"\(0\)", "(O)", head)
            if head != a["headword"]:
                a["headword_raw"] = a["headword"]
                a["headword"] = head
            a["paragraphs"] = new_paras
            fa.write(json.dumps(a, ensure_ascii=False) + "\n")
    stats = {"edits": sum(by_rule.values()), "by_rule": dict(by_rule.most_common()), "suspects": n_susp}
    (OUT / "stats.rules.json").write_text(json.dumps(stats, indent=2))
    return stats
