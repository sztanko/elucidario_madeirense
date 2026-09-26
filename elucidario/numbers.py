"""Parse the number, money and measure notations of the 1921/1940 Elucidário, and format them per target language.

Notations handled (all keep the original string in `raw`):
  1:053:000   colon grouping (thousands/millions)            -> 1053000
  5.135.994   dot grouping                                  -> 5135994
  17 677      space grouping (tables)                       -> 17677
  13,8        decimal comma                                 -> 13.8   (flag "ambiguous" for 1,852-like forms)
  20$000 réis mil-réis: "$" before 3 digits = réis           -> 20000 réis
  5:000$000   5 contos (5,000,000 réis)                     -> 5000000 réis
  229.928$090                                               -> 229928090 réis
  4$20 / $28  escudos and centavos (1911 reform: "$" before 2 digits) -> 4.20 / 0.28 escudos
  10.000 contos                                             -> 10000 contos (conto = 1,000,000 réis before 1911,
                                                               1,000 escudos after; unit kept as written)
  85% / 0,8%  percentages
  1.º 2.° 3.ª ordinals
  1498        years (never reformatted)
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

NUM = r"\d{1,3}(?:[.: ]\d{3})+|\d+"
MONEY_REIS = re.compile(rf"(?<![\d$])((?:{NUM})?)\$(\d{{3}})(?!\d)")
MONEY_ESC = re.compile(r"(?<![\d$])(\d{1,3}(?:[.: ]\d{3})*|\d*)\$(\d{2})(?!\d)")
MONEY_WHOLE = re.compile(r"(?<![\d$])(\d{1,3}(?:[.: ]\d{3})*|\d+)\$(?!\d)")  # "1$" = 1 escudo
ORDINAL = re.compile(r"\b(\d{1,3})\.\s?[ºo°ª](?![a-zà-ÿ])")
PERCENT = re.compile(r"(?<![\d,.])(\d+(?:,\d+)?)\s?%")
GROUPED = re.compile(r"(?<![\d.,:$])(\d{1,3}(?:[.:]\d{3})+)(?![\d$]|[.,:]\d)")
SPACED = re.compile(r"(?<![\d.,])(\d{1,3}(?: \d{3})+)(?![\d.,])")
DECIMAL = re.compile(r"(?<![\d.,:$])(\d+),(\d+)(?![\d$])")
PLAIN = re.compile(r"(?<![\d.,:$º°ª])(\d+)(?![\d.,:$]|\s?%|\.\s?[ºo°ª])")
UNITS = {
    "réis": "réis", "reis": "réis", "rs.": "réis", "rs": "réis", "contos": "contos", "conto": "contos",
    "escudos": "escudos", "escudo": "escudos", "centavos": "centavos",
    "quilog.": "kg", "quilogramas": "kg", "quilos": "kg", "kilos": "kg", "kg": "kg", "k.": "kg",
    "litros": "l", "litro": "l", "hectolitros": "hl", "metros": "m", "metro": "m", "m.": "m", "m": "m",
    "quilómetros": "km", "quilometros": "km", "kilometros": "km", "km": "km", "cent.": "cm", "centímetros": "cm",
    "mil.": "mm", "milímetros": "mm", "hectares": "ha", "toneladas": "t", "graus": "°",
    "alqueires": "alqueire", "alqueire": "alqueire", "almudes": "almude", "almude": "almude", "pipas": "pipa",
    "pipa": "pipa", "arrobas": "arroba", "arroba": "arroba", "braças": "braça", "léguas": "légua", "moios": "moio",
    "habitantes": "inhabitants", "fogos": "households",
}
UNIT_RE = re.compile(r"^\s?(" + "|".join(sorted(map(re.escape, UNITS), key=len, reverse=True)) + r")(?![A-Za-zÀ-ÿ])", re.I)


@dataclass
class Num:
    start: int
    end: int
    raw: str
    value: float | int
    kind: str  # integer | decimal | money_reis | money_escudos | percent | ordinal | year | contos
    unit: str | None = None
    ambiguous: bool = False

    def to_json(self) -> dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None and v is not False}


def _int(s: str) -> int:
    return int(re.sub(r"[.: ]", "", s))


def parse(text: str) -> list[Num]:
    """Find every number in a Portuguese passage; overlapping matches resolved by priority."""
    orig = text
    # dot leaders ("1910.......5.135.994") would glue numbers together: mask them, keeping offsets
    text = re.sub(r"\s?\.{3,}\s?|…+", lambda m: " " * len(m.group(0)), text)
    found: list[Num] = []
    taken = [False] * (len(text) + 1)

    def claim(m_start, m_end, num: Num):
        if any(taken[m_start:m_end]):
            return
        for i in range(m_start, m_end):
            taken[i] = True
        found.append(num)

    for m in MONEY_REIS.finditer(text):
        whole = _int(m.group(1)) if m.group(1) else 0
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), whole * 1000 + int(m.group(2)), "money_reis", "réis"))
    for m in MONEY_ESC.finditer(text):
        whole = _int(m.group(1)) if m.group(1) else 0
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), round(whole + int(m.group(2)) / 100, 2), "money_escudos", "escudos"))
    for m in MONEY_WHOLE.finditer(text):
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), _int(m.group(1)), "money_escudos", "escudos"))
    for m in ORDINAL.finditer(text):
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), int(m.group(1)), "ordinal"))
    for m in PERCENT.finditer(text):
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), float(m.group(1).replace(",", ".")), "percent", "%"))
    for rx, kind in ((GROUPED, "integer"), (SPACED, "integer")):
        for m in rx.finditer(text):
            claim(m.start(1), m.end(1), Num(m.start(1), m.end(1), m.group(1), _int(m.group(1)), kind))
    for m in DECIMAL.finditer(text):
        amb = len(m.group(2)) == 3 and len(m.group(1)) <= 3  # "1,852 metros": decimal or thousands?
        claim(m.start(), m.end(), Num(m.start(), m.end(), m.group(0), float(f"{m.group(1)}.{m.group(2)}"), "decimal", ambiguous=amb))
    for m in PLAIN.finditer(text):
        v = int(m.group(1))
        kind = "year" if 1000 <= v <= 1999 and len(m.group(1)) == 4 else "integer"
        claim(m.start(1), m.end(1), Num(m.start(1), m.end(1), m.group(1), v, kind))
    # attach units written after the number; "contos" turns an integer into a money amount
    for n in found:
        um = UNIT_RE.match(text[n.end: n.end + 16])
        if um and n.kind in ("integer", "decimal"):
            unit = UNITS[um.group(1).lower()]
            n.unit = unit
            if unit == "contos":
                n.kind = "contos"
            elif unit == "réis":
                n.kind = "money_reis"
        elif um and n.kind == "money_reis" and UNITS.get(um.group(1).lower()) == "réis":
            pass
        if n.kind == "year" and n.unit:  # "1500 metros" is a quantity, not a year
            n.kind = "integer"
    found.sort(key=lambda n: n.start)
    # "$28 e 29 por quilo": a bare 1-2 digit number joined to a centavo amount shares its currency
    for a, b in zip(found, found[1:]):
        if a.kind == "money_escudos" and a.value < 1 and b.kind == "integer" and b.value < 100 \
                and re.fullmatch(r"\s*(e|a|ou|-|–)\s*", text[a.end: b.start]):
            b.kind, b.value, b.unit = "money_escudos", b.value / 100, "escudos"
    for n in found:
        n.raw = orig[n.start: n.end]
    return found


# ------------------------------------------------------------------ formatting per target language
LOCALE = {  # thousands separator, decimal mark, currency word forms
    "en": (",", "."), "de": (".", ","), "fr": (" ", ","), "it": (".", ","), "hu": (" ", ","),
    "nl": (".", ","), "uk": (" ", ","), "ru": (" ", ","), "pt": (".", ","),
}
MIN_GROUP = {"en": 4, "de": 5, "fr": 5, "it": 5, "hu": 5, "nl": 5, "uk": 5, "ru": 5, "pt": 5}  # digits before grouping


def fmt_int(v: int, lang: str) -> str:
    sep, _ = LOCALE[lang]
    s = str(v)
    if len(s) < MIN_GROUP[lang]:
        return s
    out = ""
    while len(s) > 3:
        out = sep + s[-3:] + out
        s = s[:-3]
    return s + out


def fmt_dec(v: float, lang: str, places: int | None = None) -> str:
    _, dec = LOCALE[lang]
    s = f"{v:.{places}f}" if places is not None else repr(v)
    whole, _, frac = s.partition(".")
    return fmt_int(int(whole), lang) + (dec + frac if frac and frac != "0" else "")


def render(n: dict, lang: str) -> str:
    """Target-language rendering of a parsed number (without the unit word, which the translator places)."""
    k, v = n["kind"], n["value"]
    if k in ("year", "ordinal") or n.get("ambiguous"):
        return n["raw"] if k != "ordinal" else str(v)
    if k == "money_escudos":
        if v < 1:  # style guides: sums under one escudo are given in centavos ("28 centavos")
            return str(int(round(v * 100)))
        return fmt_dec(v, lang, 2) if round(v % 1, 2) else fmt_int(int(v), lang)
    if k in ("decimal", "percent"):
        places = len(n["raw"].split(",")[1].rstrip("%").strip()) if "," in n["raw"] else None
        return fmt_dec(v, lang, places)
    return fmt_int(int(v), lang)
