"""Regenerate the data-driven sections of docs/transcription_{uk,ru}.md from the knowledge base.

Replaced sections (between headings):
  §5.3  monarchs/popes/saints        -> rule: kb/historical_figures.yaml is authoritative (+ excerpt)
  §7    religious names              -> rules + full table from kb/religious_titles.yaml
  §8A   (new) historical, legal and administrative terms -> from kb/termbase.yaml
  §13.2 persons (established forms)  -> excerpt from kb/historical_figures.yaml
  §14   worked examples              -> rebuilt from kb/names_seed_ru_uk.jsonl
"""

from __future__ import annotations

import json
import re

import yaml

from elucidario.paths import DOCS, KB

TERMS = ["sesmaria", "sesmeiro", "morgado", "morgadio", "vínculo", "capela", "capitania", "capitão-donatário", "donatário",
         "foro", "foral", "dízimo", "colonia", "benfeitorias", "senhorio", "caseiro", "colono", "vilão", "provedor",
         "almoxarife", "corregedor", "juiz de fora", "vereador", "câmara", "câmara municipal", "concelho", "freguesia", "sítio",
         "lombo", "fajã", "achada", "levada", "heréu", "poio", "palheiro", "moradia", "quinta", "engenho", "réis", "mil-réis",
         "conto", "alqueire", "almude", "pipa", "braça"]
L = {"uk": {"figs": "Історичні особи", "rel": "Релігійні назви"}, "ru": {"figs": "Исторические лица", "rel": "Религиозные названия"}}


def replace_section(text: str, start_re: str, end_re: str, new: str) -> str:
    m = re.search(start_re, text, re.M)
    if not m:
        raise ValueError(f"heading not found: {start_re}")
    e = re.search(end_re, text[m.end():], re.M)
    end = m.end() + e.start() if e else len(text)
    return text[: m.start()] + new.rstrip() + "\n\n" + text[end:]


def religious_section(lang: str) -> str:
    t = yaml.safe_load(open(KB / "religious_titles.yaml"))
    rows = []
    for pt, e in t.items():
        v = e.get(lang)
        if v:
            rows.append(f"| {pt} | {e['kind']} | {v} | {'yes' if e.get('established') else 'descriptive'} | {'yes' if e.get('also_toponym') else ''} |")
    if lang == "uk":
        rules = """## 7. Religious names

**Authoritative source:** `kb/religious_titles.yaml`. It was researched per title, using Wikipedia in each language and
church sources. Dedications are **never translated word for word**. Every Marian, Christological or Trinitarian title, and
every saint, has the equivalent established in that language's church usage. For example:
- Nossa Senhora da Boa Morte → **Успіння Пресвятої Богородиці**: the Boa Morte devotion is the Dormition/Assumption, not a "good death".
- Livramento → **Богородиця Визволителька**.
- Piedade → **Скорботна Богородиця (П'єта)**.
- São Tiago → **святий Яків (Старший)**.
Where no established Eastern equivalent exists, the table gives the Catholic form and marks it `descriptive`.

### 7.1 Three uses of a dedication
1. **A church, chapel, confraternity or feast named after a dedication.** Translate the generic word (igreja → церква;
   capela, ermida → каплиця; convento → монастир; sé → кафедральний собор; confraria → братство). The dedication follows
   in the genitive of the established title: *каплиця Успіння Пресвятої Богородиці*, *церква святого Роха*. At first
   mention the Portuguese original follows in parentheses: *каплиця Успіння Пресвятої Богородиці (Capela de Nossa Senhora
   da Boa Morte)*.
2. **A place name containing a dedication** (parish, sítio, town): Santa Cruz, São Vicente, Santo António da Serra,
   Nossa Senhora do Monte (parish), Livramento (sítio). This is a **toponym**, so it is transcribed with the place rules
   (§2.1, §4). At first mention, give the established title as the meaning where it helps the reader:
   *Носа-Сеньора-ду-Монті (Богородиця з Монте, Nossa Senhora do Monte)*; *Санта-Круш (Santa Cruz)*. Items the table
   marks `also_toponym: yes` need this check: decide from the context whether the text means the place or the devotion.
3. **The devotion, image or feast itself** ("a imagem de Nossa Senhora da Piedade", "a festa do Espírito Santo"):
   translate with the established title and no transcription: *образ Скорботної Богородиці*, *свято Святого Духа*.

### 7.2 Full table (Ukrainian)
| Portuguese | Kind | Ukrainian | Established | Also a toponym |
|---|---|---|---|---|
"""
    else:
        rules = """## 7. Religious names

**Authoritative source:** `kb/religious_titles.yaml`. It was researched per title, using Wikipedia in each language and
church sources. Dedications are **never translated word for word**. Use the equivalent established in church usage.
For example:
- Nossa Senhora da Boa Morte → **Успение Пресвятой Богородицы**.
- Livramento → **Богородица Избавительница**.
- Piedade → **Скорбящая Богоматерь (Пьета)**.
- São Tiago → **святой Иаков (Старший)**.
Where no established Eastern equivalent exists, the table gives the Catholic form and marks it `descriptive`.

### 7.1 Three uses of a dedication
1. **Church, chapel, confraternity or feast.** Translate the generic word (церковь, часовня, монастырь, кафедральный
   собор, братство) and put the established title in the genitive: *часовня Успения Пресвятой Богородицы (Capela de
   Nossa Senhora da Boa Morte)* at first mention.
2. **Place name containing a dedication** (Santa Cruz, São Vicente, Santo António da Serra, the parish of Nossa Senhora
   do Monte): a **toponym**, transcribed by the place rules. At first mention, give the established title as the meaning
   where it helps: *Носа-Сеньора-ду-Монти (Богоматерь Монте, Nossa Senhora do Monte)*.
3. **The devotion, image or feast itself:** translate with the established title (*образ Скорбящей Богоматери*,
   *праздник Святого Духа*).

### 7.2 Full table (Russian)
| Portuguese | Kind | Russian | Established | Also a toponym |
|---|---|---|---|---|
"""
    return rules + "\n".join(rows) + "\n"


def figures_excerpt(lang: str, n: int = 60) -> str:
    h = yaml.safe_load(open(KB / "historical_figures.yaml"))
    seen, rows = set(), []
    for v in sorted(h.values(), key=lambda v: v["pt_name"]):
        name = (v.get("established_names") or {}).get(lang)
        if not name or v.get("wikidata") in seen:
            continue
        seen.add(v.get("wikidata"))
        first = (v.get("first_mention") or {}).get(lang) or name
        rows.append(f"| {v['pt_name']} | {name} | {first} | {v.get('wikidata') or ''} |")
    head = f"""**Authoritative source:** `kb/historical_figures.yaml`, {len(h)} figures. Each was matched to Wikidata, and the
name is taken from that language's Wikipedia and then harmonised: the same individual always gets the same name. Well-known
figures take the name **established** in the language, never a transcription. For example, Infante D. Henrique →
**{'Енріке Мореплавець' if lang == 'uk' else 'Генрих Мореплаватель'}**; D. Manuel I → **{'Мануел I' if lang == 'uk' else 'Мануэл I'}**;
Cristóvão Colombo → **Христофор Колумб**. Local Madeiran figures who are not in the file are transcribed by §5.1.
Excerpt:

| Portuguese | Running text | First mention | Wikidata |
|---|---|---|---|
"""
    return head + "\n".join(rows[:n]) + "\n"


def terms_section(lang: str) -> str:
    tb = yaml.safe_load(open(KB / "termbase.yaml"))
    rows = []
    for t in TERMS:
        e = tb.get(t)
        if not e:
            continue
        gloss = (e.get("first_mention_gloss") or {}).get(lang) or ""
        rows.append(f"| {t} | {e['policy']} | {e['renderings'].get(lang, '')} | {gloss} |")
    missing = [t for t in TERMS if t not in tb]
    return (f"""## 8A. Historical, legal and administrative terms

These are common nouns, not names. They follow `kb/termbase.yaml`, which is authoritative and consistent across all
entries.
- `translate`: use the fixed equivalent.
- `keep`: transcribe (in italics in Latin-script languages) and give the gloss at first mention in each entry.
- `keep_unit`: keep the historical unit and gloss it.

Inside proper names (Lombo da Guiné, Fajã da Ovelha), these words are part of the toponym and are transcribed with it.

| Portuguese | Policy | {'Ukrainian' if lang == 'uk' else 'Russian'} | First-mention gloss |
|---|---|---|---|
""" + "\n".join(rows) + (f"\n\nNot yet in the termbase (to be added): {', '.join(missing)}\n" if missing else "\n"))


def examples_section(lang: str) -> str:
    rows = [json.loads(l) for l in open(KB / "names_seed_ru_uk.jsonl")]
    lines = [f"| {i + 1} | {r['pt']} | {r['type']} | {r[lang]} | {r.get(lang + '_meaning') or '—'} | {r[lang + '_first']} |"
             for i, r in enumerate(rows)]
    return ("## 14. Worked examples\n\nGenerated from `kb/names_seed_ru_uk.jsonl` (authoritative seed). Religious and "
            "historical rows follow §7 and kb/historical_figures.yaml.\n\n| # | Portuguese | Type | Later mentions | Meaning | "
            "First mention |\n|---|---|---|---|---|---|\n" + "\n".join(lines) + "\n")


def build(lang: str) -> None:
    p = DOCS / f"transcription_{lang}.md"
    t = p.read_text()
    t = replace_section(t, r"^## 7\. Religious names", r"^## 8\. ", religious_section(lang))
    t = replace_section(t, r"^### 5\.3 ", r"^### 5\.4 ", "### 5.3 Monarchs, popes, saints and other historical figures\n\n" + figures_excerpt(lang, 25))
    t = replace_section(t, r"^### 13\.2 Persons", r"^### 13\.3 ", "### 13.2 Persons\n\n" + figures_excerpt(lang, 80))
    if "## 8A." in t:
        t = replace_section(t, r"^## 8A\. ", r"^## 9\. ", terms_section(lang))
    else:
        t = t.replace("\n## 9. ", "\n" + terms_section(lang) + "\n## 9. ", 1)
    t = replace_section(t, r"^## 14\. Worked examples", r"^## 15\. ", examples_section(lang))
    p.write_text(t)
