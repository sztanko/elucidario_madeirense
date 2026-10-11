"""Generates docs/naming_{en,de,fr,it,hu,nl}.md and kb/works.yaml from the tables in ded.py (dedications),
topo.py (toponym meanings), works.py (works and periodicals), examples.py and prose.py.
Run: python tools/naming_gen/build.py"""
import yaml, re, json, os
import pathlib
REPO=str(pathlib.Path(__file__).resolve().parents[2])
HERE=pathlib.Path(__file__).resolve().parent
exec(open(HERE/'ded.py').read()); exec(open(HERE/'topo.py').read())
exec(open(HERE/'works.py').read()); exec(open(HERE/'examples.py').read()); exec(open(HERE/'prose.py').read())
L=['en','de','fr','it','hu','nl']
TB=yaml.safe_load(open(f'{REPO}/kb/termbase.yaml'))
def ap(s):  # typographic apostrophe in target-language text
    return s.replace("'", "’") if isinstance(s,str) else s
def gl(lang,m):
    a,b=P[lang]['gm']; return f"{a}{ap(m)}{b}"
def tq(lang,t):
    a,b=P[lang]['tm']; return f"{a}{ap(t)}{b}"
def esc(s): return s.replace('|','\\|')
LANGNAME={'en':'English','de':'German','fr':'French','it':'Italian','hu':'Hungarian','nl':'Dutch'}

def ded_table(lang):
    rows=["| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |","|---|---|---|---|---|---|---|"]
    for i,d in enumerate(D,1):
        dev,ch=d[lang]
        rows.append(f"| {i} | {d['pt']} | {d['kind']} | {'yes' if d['top'] else ''} | {ap(dev)} | {ap(ch)} | {esc(d['note'])} |")
    return '\n'.join(rows)

def topo_table(lang):
    rows=["| # | Portuguese | Class | Articles | First mention | Notes |","|---|---|---|---|---|---|"]
    i=0
    for t in sorted(T,key=lambda x:-x[1]):
        pt,freq,cls,note=t[:4]; m=t[4+L.index(lang)]
        i+=1
        if m.startswith('='):
            first=f"{ap(m[1:])} (*{pt}*) — established exonym"
        elif m=="":
            first=f"{pt} — no gloss (same or transparent in {LANGNAME[lang]})"
        else:
            first=f"{pt} ({gl(lang,m)})"
        rows.append(f"| {i} | {pt} | {cls} | {freq} | {first} | {esc(note)} |")
    return '\n'.join(rows)

def work_forms(lang,w):
    t,est,src=w['langs'][lang]
    printed=w['pt']
    if w['form']=='keep':
        run=f"*{t}*"; first=run
    elif w['form']=='keep_gloss':
        run=f"*{t}*"; first=f"{run} ({gl(lang,w['langs']['gloss'][lang])})"
    elif w['kind']=='law':
        run=ap(t); first=f"{run} (*{w['pt']}*)"
    else:
        run=f"*{ap(t)}*" if est else tq(lang,t)
        first=f"{run} (*{printed}*)"
    return run,first,est,src

def works_table(lang):
    rows=["| Portuguese (key; printed spellings) | Kind | Author, date | Articles | Running text | First mention | Established | Source |","|---|---|---|---|---|---|---|---|"]
    for w in W:
        run,first,est,src=work_forms(lang,w)
        als='; '.join(w['aliases'])
        key=w['pt']+(f" ({als})" if als else '')
        rows.append(f"| {esc(key)} | {w['kind']} | {esc((w['author'] or '—')+(', '+w['year'] if w['year'] else ''))} | {w['articles']} | {esc(run)} | {esc(first)} | {'yes' if est else 'no'} | {src or '—'} |")
    return '\n'.join(rows)

def per_table(lang):
    rows=["| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |","|---|---|---|---|---|---|"]
    for p in PER:
        m,als,n,yr,note=p[:5]; mean=p[5+L.index(lang)]
        run=f"«{m}»" if lang=='it' else f"*{m}*"
        first=f"{run} ({gl(lang,mean)})"
        rows.append(f"| {esc(m)}{(' ('+esc('; '.join(als))+')') if als else ''} | {yr or '—'} | {n if n is not None else 'n/a'} | {esc(run)} | {esc(first)} | {esc(note)} |")
    return '\n'.join(rows)

INST_TB=[("Câmara Municipal","câmara municipal"),("Junta Geral do Distrito","Junta Geral do Distrito"),("Santa Casa da Misericórdia","Santa Casa da Misericórdia"),
 ("Misericórdia (short form)","misericórdia"),("Santo Ofício","Santo Ofício"),("Cabido (da Sé)","cabido"),("Cortes","Cortes"),("Seminário","seminário"),
 ("Paço Episcopal","paço episcopal"),("Paços do Concelho","paços do concelho"),("Alfândega (do Funchal)","alfândega"),("Governo Civil","governo civil"),
 ("Diocese (do Funchal)","diocese"),("Desembargo do Paço","Desembargo do Paço"),("Junta de Paróquia","junta de paróquia"),("Provedoria da Real Fazenda","Provedoria da Real Fazenda")]
INST_MAN={
 "Universidade de Coimbra":dict(en="the University of Coimbra",de="die Universität Coimbra",fr="l’université de Coimbra",it="l’Università di Coimbra",hu="a Coimbrai Egyetem",nl="de Universiteit van Coimbra"),
 "Torre do Tombo":dict(en="the Torre do Tombo (national archives)",de="das Nationalarchiv Torre do Tombo",fr="les archives nationales de la Torre do Tombo",it="l’archivio nazionale della Torre do Tombo",hu="a Torre do Tombo nemzeti levéltár",nl="het nationaal archief Torre do Tombo"),
 "Colégio dos Jesuítas":dict(en="the Jesuit College",de="das Jesuitenkolleg",fr="le collège des Jésuites",it="il Collegio dei Gesuiti",hu="a jezsuita kollégium",nl="het jezuïetencollege"),
 "Liceu do Funchal":dict(en="the Funchal Lyceum",de="das Gymnasium von Funchal",fr="le lycée de Funchal",it="il liceo di Funchal",hu="a funchali gimnázium",nl="het lyceum van Funchal"),
 "Hospital de Santa Isabel":dict(en="St Elizabeth’s Hospital",de="das St.-Elisabeth-Hospital",fr="l’hôpital Sainte-Élisabeth",it="l’ospedale di Santa Elisabetta",hu="a Szent Erzsébet-kórház",nl="het Sint-Elisabethziekenhuis"),
 "Sé do Funchal":dict(en="Funchal Cathedral (the Sé)",de="die Kathedrale von Funchal",fr="la cathédrale de Funchal",it="la cattedrale di Funchal",hu="a funchali székesegyház",nl="de kathedraal van Funchal"),
}
GRAM=re.compile(r"\s*\((?:m\.|f\.|n\.|de|het|de/het|m\. pl\.|f\. pl\.)(?:, pl\. [^)]*)?\)")
def clean(x): return GRAM.sub('',x).strip()
def inst_table(lang):
    rows=["| Portuguese | Running text | First mention | Source |","|---|---|---|---|"]
    for pt,k in INST_TB:
        r=TB.get(k,{}).get('renderings',{}).get(lang)
        if not r: continue
        r=clean(r)
        f=TB[k].get('first_mention_gloss',{}) or {}
        first=clean(f.get(lang) or '') or f"{r.split(';')[0]} (*{pt.split(' (')[0]}*)"
        rows.append(f"| {pt} | {esc(r)} | {esc(first)} | termbase `{k}` ({TB[k]['policy']}) |")
    for pt,d in INST_MAN.items():
        rows.append(f"| {pt} | {d[lang]} | {d[lang]} (*{pt}*) | this standard |")
    return '\n'.join(rows)

def examples(lang):
    out=[]
    for i,x in enumerate(X,1):
        out.append(f"**{i}. {x['title']}**\n\n> PT: {x['pt']}\n>\n> {lang.upper()}: {ap(x['t'][lang])}\n")
        if x['note']: out.append(f"Note: {x['note']}\n")
    return '\n'.join(out)

def doc(lang):
    p=P[lang]; nm=p['name']
    a,b=p['gm']; ta,tb=p['tm']
    s=f"""# Proper names in the {nm} translation (`{p['code']}`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the {nm} translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the {nm} forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/{p['file']}`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

{p['intro']}

---

## 0. Decision procedure

1. Name table entry → use `rendering` / `first` exactly, inflected as §11 requires.
2. Normalise the Portuguese spelling (NL §1); titles keep the printed spelling.
3. Established exonym or historical figure (§3, §5) → that form, no parenthesis.
4. Classify (NL §2.1): person (§2); dedication: decide use 1, 2 or 3 (§4); place (§5);
   institution (§7); work or periodical (§8).
5. Homonym check (§12).
6. Meaning gloss for kept names (§9); first and later mentions (§10).

---

## 1. Typography of names, glosses and titles

{p['typo']}

---

## 2. Personal names and honorifics

{p['persons']}

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

{p['hist']}

The authoritative list is `kb/historical_figures.yaml` (`established_names.{lang}` for running
text, `first_mention.{lang}` for the first mention). Figures not in the file keep their
Portuguese name. Corrections proposed for this language are in NL §13.1.

---

## 4. Saints and religious names

### 4.1 Three uses of a dedication (NL §6.1)

1. **Building, confraternity, feast, image** → translate (§6 table, column "Building name"):
   first mention translation (*Portuguese dedication*).
2. **Toponym containing a dedication** (São Vicente, Santa Cruz, Santo António da Serra,
   Nossa Senhora do Monte as a parish) → keep the Portuguese; meaning in {a}…{b} (§9).
3. **The devotion or saint itself** → the established form (§6 table, column "Devotion");
   saints as persons get no parenthesis; Marian and Christological titles get
   (*Portuguese*) at first mention.

*a igreja de Santa Cruz* is the church **of the town** (dedicated to São Salvador): use 2.

### 4.2 {nm} conventions

{p['saints']}

---

## 5. Places

{p['places']}

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: {nm} forms

The {len(D)} most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

{ded_table(lang)}

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

{inst_table(lang)}

---

## 8. Works and periodicals

Books, poems, documents and laws are translated: an established published translation in
italics, otherwise a descriptive translation in {ta}…{tb}; the Portuguese original follows in
italics, **as printed in the article** (the key column shows the modern form; the printed
variants are listed in brackets). Periodicals keep the masthead and get the meaning
(NL §2.3, §4). "Articles" = number of articles that mention the work (heuristic count on the
Portuguese text; n/a = unreliable because the title is a common word).

### 8.1 Books, poems, documents, laws

{works_table(lang)}

### 8.2 Periodicals

{per_table(lang)}

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

{topo_table(lang)}

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in {a}…{b}.

---

## 11. Grammar in running text

{p['grammar']}

---

## 12. Homonym traps

Full list: NL §9. {nm} forms of the most frequent ones:

{p['homonyms']}

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

{examples(lang)}

---

## 14. Decisions for the owner to confirm

{p['decisions']}

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
"""
    if lang=='fr':
        s=s.replace('« ','« ').replace(' »',' »')
    return s

for lang in L:
    open(f'{REPO}/docs/naming_{lang}.md','w').write(doc(lang))
    print(lang, len(doc(lang).splitlines()))

# ---------- kb/works.yaml ----------
def wy():
    out={}
    for w in W:
        e=dict(kind=w['kind'],author=w['author'],date=w['year'],articles=w['articles'],aliases=w['aliases'] or [],form=w['form'],note=w['note'] or None)
        for lang in L:
            t,est,src=w['langs'][lang]
            run,first,_,_=work_forms(lang,w)
            if lang=='fr': first=first.replace('« ','«\u202f').replace(' »','\u202f»'); run=run.replace('« ','«\u202f').replace(' »','\u202f»')
            d=dict(title=ap(t),established=bool(est),source=src,kind=w['kind'],author=w['author'],running=run,first=first)
            if w['form']=='keep_gloss': d['gloss']=w['langs']['gloss'][lang]
            e[lang]=d
        out[w['pt']]=e
    for p in PER:
        m,als,n,yr,note=p[:5]
        e=dict(kind='periodical',author=None,date=yr or None,articles=n,aliases=als,form='keep_gloss',note=note or None)
        for i,lang in enumerate(L):
            mean=ap(p[5+i])
            run=f"«{m}»" if lang=='it' else f"*{m}*"
            first=f"{run} ({gl(lang,mean)})"
            if lang=='fr': first=first.replace('« ','«\u202f').replace(' »','\u202f»')
            e[lang]=dict(title=m,established=False,source=None,kind='periodical',author=None,gloss=mean,running=run,first=first)
        out[m]=e
    hdr="""# Works and periodicals cited in the Elucidário Madeirense: target-language titles.
# Standard: docs/naming_latin.md §2.3, §4; per-language tables in docs/naming_<lang>.md §8.
# Key = modern Portuguese title (masthead with its article for periodicals). `aliases` = spellings
# and headword forms found in the source; the first mention reproduces the title AS PRINTED in the article.
# Entry fields: kind (book | poem | document | law | periodical), author, date, articles (number of
#   articles mentioning it; heuristic count on data/04_structured/articles.jsonl, null = unreliable),
#   form: translate  -> running text uses `title`; first mention `title` (*original*)
#         keep_gloss -> running text keeps the original; first mention original (‘gloss’)
#         keep       -> non-Portuguese title or the Elucidário itself: original, no gloss
# Per-language fields: title, established (a published translation with this title exists),
#   source (URL when established), kind, author (repeated for convenience), running, first,
#   (established is also true for kept titles whose original form is the established one: Latin,
#   non-Portuguese titles, the Elucidário itself),
#   gloss (keep_gloss only). Descriptive titles: language title quotes; established: italics.
# Generated 2026-10-03 for owner review; not yet read by the pipeline.
"""
    body=yaml.safe_dump(out,allow_unicode=True,sort_keys=False,width=200,default_flow_style=False)
    open(f'{REPO}/kb/works.yaml','w').write(hdr+body)
    return len(out)
print('works', wy())
