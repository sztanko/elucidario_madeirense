"""site/public/maps/demo.html: a self-contained showcase of every plate, rendered with the same markup as MapView.astro.

Asset URLs are relative to the demo page, and the engine's base path is derived at runtime, so the page works under any
site base. The engine bundle comes from esbuild (site/public/maps/demo/boot.js); see README.
"""

from __future__ import annotations

import json
from html import escape

from elucidario.cartography.places import region_of
from elucidario.cartography.proj import Projection
from elucidario.paths import ROOT

SITE = ROOT / "site"


def figure(man: dict, geo: dict, rid: str, mode: str, places: list[tuple[str, str]], lang="en", height: str | None = None, title="") -> str:
    R = man["regions"][rid]
    P = Projection(R["proj"]["type"], R["proj"]["lon0"], R["proj"]["lat0"])
    v = f"?v={man['version']}"
    x0, y0, x1, y1 = R["frame"]
    numbered = len(places) <= 12
    toks, mks, abroad = [], [], {}
    isl_ids = ("madeira", "porto-santo", "desertas") if rid == "archipelago" else (rid,)
    for i, (slug, role) in enumerate(places):
        g = geo.get(slug)
        if not g:
            continue
        r = region_of(g)
        toks.append(slug + ("~s" if role == "subject" else "") + (f"~{i + 1}" if numbered else ""))
        if r and r not in isl_ids and r not in ("selvagens",) and R["kind"] == "islands":
            abroad[r] = abroad.get(r, 0) + 1
        if g.get("c") and r in isl_ids and len(mks) < 12:
            X, Y = P.fwd(*g["c"])
            fx, fy = (X - x0) / (x1 - x0) * 100, (Y - y0) / (y1 - y0) * 100
            cls = "em-map__mk" + (" is-subj" if role == "subject" else "")
            mks.append(f'<span class="{cls}" style="left:{fx:.1f}%;top:{fy:.1f}%" data-id="{slug}">{"" if role == "subject" or not numbered else i + 1}</span>')
    rel = ""
    if R.get("relief"):
        s, l = R["relief"]["s"], R["relief"]["l"]
        rel = f'<img class="em-map__relief" src="{s["src"]}{v}" srcset="{s["src"]}{v} {s["w"]}w, {l["src"]}{v} {l["w"]}w" sizes="100vw" alt="" loading="lazy">'
    inset = ""
    if R.get("inset"):
        I = man["regions"][R["inset"]]
        inset = f'<span class="em-map__inset" style="--iar:{I["aspect"]}"><img src="{I["plate"]}{v}" alt=""><img class="em-map__relief" src="{I["relief"]["s"]["src"]}{v}" alt=""><b>Selvagens</b></span>'
    ab = ""
    if abroad:
        ab = '<p class="em-map__abroad"><span class="em-label">Abroad</span>' + "".join(
            f'<button type="button" data-region="{k}" disabled>{man["regions"][k]["name"]} <i>{n}</i></button>' for k, n in abroad.items()) + "</p>"
    style = f"--ar:{R['aspect']};" + (f"height:{height};" if height else "")
    fixed = " em-map--fixed" if height else ""
    return (f'<section><h2>{escape(title)}</h2><figure class="em-map em-map--{mode}{fixed}" data-em-map data-mode="{mode}" data-region="{rid}" '
            f'data-lang="{lang}" data-p="{" ".join(toks)}" style="{style}"><div class="em-map__plate" aria-hidden="true">'
            f'<img class="em-map__base" src="{R["plate"]}{v}" alt="" loading="lazy">{rel}{"".join(mks)}{inset}</div>{ab}</figure></section>')


def build(out) -> None:
    man = json.loads((out / "manifest.json").read_text())
    geo = json.loads((SITE / "data" / "geo.json").read_text())

    def top(pred, n):
        return [k for k, v in sorted(geo.items(), key=lambda kv: -kv[1].get("n", 0)) if v.get("c") and pred(v)][:n]

    def reg(v):
        return region_of(v)

    madeira = [(k, "mention") for k in top(lambda v: reg(v) == "madeira", 80)]
    ps = [("vila-baleira-orto-anto-porto-santo", "subject")] if "vila-baleira-orto-anto-porto-santo" in geo else []
    ps += [(k, "mention") for k in top(lambda v: reg(v) == "porto-santo", 8) if k not in dict(ps)]
    arch = [(k, "mention") for k in top(lambda v: reg(v) in ("madeira", "porto-santo", "desertas", "selvagens"), 160)]
    europe = [(k, "mention") for k in top(lambda v: reg(v) == "europe", 70)]
    calheta = [k for k, v in geo.items() if v.get("tp") == "parish" and v["pt"] == "Calheta" and v.get("g")]
    art = [(calheta[0], "subject")] if calheta else []
    art += [(k, "mention") for k in top(lambda v: v.get("mun") == "Calheta" and reg(v) == "madeira", 8) if k not in calheta][:7]
    art += [(k, "mention") for k in ("lisboa", "acores", "brasil") if k in geo]
    figs = [
        figure(man, geo, "madeira", "article", art, height=None, title="Article map: Calheta (subject municipality hatched, numbered mentions, places abroad)"),
        figure(man, geo, "madeira", "overview", madeira, title="Madeira, overview with 80 places (clustered)"),
        figure(man, geo, "porto-santo", "article", ps[:9], title="Porto Santo"),
        figure(man, geo, "archipelago", "overview", arch, title="The archipelago, with the Selvagens inset"),
        figure(man, geo, "desertas", "place", [(k, "mention") for k in top(lambda v: reg(v) == "desertas", 6)], height="24rem", title="Desertas"),
        figure(man, geo, "europe", "continent", europe, title="Europe"),
    ]
    for cid in ("africa", "south-america", "north-america", "asia", "oceania"):
        figs.append(figure(man, geo, cid, "continent", [(k, "mention") for k in top(lambda v, c=cid: reg(v) == c, 40)], title=man["regions"][cid]["name"]))
    loc = "".join(f'<img src="{f}" alt="{escape(k or "Madeira")}" width="240">' for k, f in man.get("locator", {}).get("files", {}).items())
    css = (SITE / "src" / "map" / "map.css").read_text()
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elucidário Madeirense: atlas plates (demo)</title>
<style>
:root{{--paper:#e8dfca;--paper-light:#f2ead8;--ink:#171b19;--ink-2:#3a3d38;--ink-3:#5e5a4f;--place:#164c59;--place-ink:#123f4a;--person:#bd3426;--person-ink:#a32a1e;--line:rgb(23 27 25/.28);--place-wash:rgb(22 76 89/.09);
--font-label:"Sofia Sans Extra Condensed","Arial Narrow",sans-serif;--font-text:Literata,Georgia,serif;--font-didone:"Playfair Display",Georgia,serif;--ease:cubic-bezier(.2,.7,.1,1)}}
body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--font-text)}} main{{max-width:1180px;margin:auto;padding:16px}}
h1{{font:800 2.2rem/1 var(--font-label);text-transform:uppercase;letter-spacing:.02em}} h2{{font:700 .8rem/1 var(--font-label);letter-spacing:.22em;text-transform:uppercase;margin:2rem 0 .6rem}}
.em-label{{font:600 10px var(--font-label);letter-spacing:.22em;text-transform:uppercase}} .em-sr-only{{position:absolute;clip:rect(0 0 0 0)}} .locs img{{margin:4px;background:var(--paper)}}
{css}
</style></head><body><main><h1>Atlas plates · demo</h1>
<p>Flowline hachures after Samsonov (2014) from Copernicus GLO-30, vector plates from OSM and Natural Earth. Drag, pinch or ⌘/Ctrl + scroll; click a map to activate plain scrolling and one-finger panning.</p>
{"".join(figs)}
<section><h2>Locators (static SVG, for cards and the mobile header)</h2><div class="locs">{loc}</div></section></main>
<script>globalThis.__EM_BASE__ = location.pathname.replace(/maps\\/demo\\.html.*$/, '');</script>
<script type="module" src="demo/boot.js"></script></body></html>"""
    (out / "demo.html").write_text(html)
    print("demo.html written")
