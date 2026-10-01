#!/usr/bin/env python3
"""Generador estático de quemeconviene. Sin dependencias. Uso: python3 build.py"""
import json, os, shutil, html, datetime, hashlib
from string import Template
import seo  # SEO técnico + GEO (Estratega): lastmod real, clústeres, guías, JSON-LD, llms.txt

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
site = json.load(open(os.path.join(ROOT, "data/site.json")))
params = json.load(open(os.path.join(ROOT, "data/params.json")))
def asset_v(name):
    return hashlib.sha1(open(os.path.join(ROOT, "assets", name), "rb").read()).hexdigest()[:10]
BASE = Template(open(os.path.join(ROOT, "templates/base.html")).read()
                .replace('/assets/app.css"', f'/assets/app.css?v={asset_v("app.css")}"')
                .replace('/assets/app.js"', f'/assets/app.js?v={asset_v("app.js")}"')
                .replace('__BASE__', site["base_url"].rstrip("/")))
HOME = Template(open(os.path.join(ROOT, "templates/home.html")).read())
# Iconos por tema (D1). Si la calculadora no trae "tema" en su JSON, se deduce del slug.
_S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
    "hipoteca": ("Hipoteca y vivienda", _S + '<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-5h4v5"/></svg>'),
    "coche": ("Coche", _S + '<path d="M5 17H3v-4l2.2-5A2 2 0 0 1 7 7h10a2 2 0 0 1 1.8 1L21 13v4h-2"/><path d="M3 13h18"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M9.5 17h5"/></svg>'),
    "impuestos": ("Impuestos", _S + '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9.5 16.5l5-6"/><circle cx="10" cy="11" r="1"/><circle cx="14" cy="16" r="1"/></svg>'),
    "energia": ("Energía", _S + '<path d="M13 2L4.5 13.5H11L10 22l8.5-11.5H12z"/></svg>'),
    "ahorro": ("Ahorro e inversión", _S + '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/></svg>'),
}
def tema(c):
    if c.get("tema") in ICONS: return c["tema"]
    s = c["slug"]
    for t, kws in [("coche", ["coche", "diesel", "gasolina", "electrico", "renting", "moto"]),
                   ("hipoteca", ["hipoteca", "amortizar-plazo", "vivienda", "alquilar", "casa"]),
                   ("impuestos", ["irpf", "declaracion", "renta", "impuesto", "autonomo", "iva"]),
                   ("energia", ["luz", "energia", "solar", "placas", "gas", "tarifa", "bombona"])]:
        if any(k in s for k in kws): return t
    return "ahorro"
def card(c):
    t = tema(c); name, svg = ICONS[t]
    q = html.escape(f'{c["h1"]} {c["description"]} {name} {c["slug"].replace("-", " ")}', quote=True)
    return f'<li data-q="{q}" data-t="{t}"><span class="ico">{svg}</span><a href="/decidir/{c["slug"]}/">{c["h1"]}</a><p>{c["description"]}</p><span class="tag">{name}</span></li>'

def catalog_body(calcs):
    """Cuerpo de /decidir/ (D3): buscador + chips por tema + contador + estado vacío."""
    n = {}
    for c in calcs: n[tema(c)] = n.get(tema(c), 0) + 1
    chips = f'<button type="button" class="chip" data-t="" aria-pressed="true">Todas <span>{len(calcs)}</span></button>' + "".join(
        f'<button type="button" class="chip" data-t="{t}" aria-pressed="false"><span class="ci" aria-hidden="true">{ICONS[t][1]}</span>{ICONS[t][0]} <span>{n[t]}</span></button>'
        for t in ICONS if n.get(t))
    return f"""<section class="cat-hero"><p class="kicker">Catálogo</p><h1>Calculadoras de decisión</h1>
<p class="lead">Elige un tema o busca tu dilema. Todas se calculan en tu navegador, con tus números.</p>
<div class="search" role="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<label for="q" class="sr-only">Buscar calculadora</label>
<input id="q" type="search" placeholder="Busca: hipoteca, renting, Euríbor…" autocomplete="off" data-filter="#calcs" data-empty="#empty" data-count="#count" data-chips="#chips" data-always="1"></div>
<div class="chips" id="chips" role="group" aria-label="Filtrar por tema">{chips}</div>
<p class="cat-count" id="count" role="status" aria-live="polite">{len(calcs)} calculadoras</p></section>
<ul class="cards" id="calcs">{"".join(card(c) for c in calcs)}</ul>
<div class="empty-state" id="empty" hidden><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5M8.5 11h5"/></svg>
<h2>No hemos encontrado esa calculadora</h2><p>Prueba con otra palabra (por ejemplo «hipoteca» o «coche») o quita el filtro de tema.</p>
<p><button type="button" id="reset" class="btn2">Ver todas las calculadoras</button></p><p class="note">¿Te falta alguna? <a href="/contacto/">Cuéntanoslo</a> y la preparamos.</p></div>"""

def notfound_body():
    return """<section class="nf"><p class="nf-code" aria-hidden="true">404</p><h1>No encontramos esa página</h1>
<p class="lead">Puede que el enlace haya cambiado o esté mal escrito. Busca la calculadora que necesitas:</p>
<form class="search" role="search" action="/decidir/" method="get"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<label for="q" class="sr-only">Buscar calculadora</label><input id="q" name="q" type="search" placeholder="Busca: hipoteca, renting, Euríbor…" autocomplete="off"></form>
<p><a class="btn" href="/decidir/">Ver todas las calculadoras</a> <a class="btn2" href="/">Ir al inicio</a></p></section>"""
pages = []  # (path, lastmod, priority)
GUIDES = seo.load_guides(params)  # content/guias/*.html

def head_extra():
    out = []
    if site.get("search_console_meta"):
        out.append(f'<meta name="google-site-verification" content="{site["search_console_meta"]}">')
    if site.get("analytics_plausible_domain"):
        out.append(f'<script defer data-domain="{site["analytics_plausible_domain"]}" src="https://plausible.io/js/script.js"></script>')
    if site.get("ga4_id"):
        g = site["ga4_id"]
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{g}",{{anonymize_ip:true}});</script>')
    if site.get("adsense_client"):
        out.append(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={site["adsense_client"]}" crossorigin="anonymous"></script>')
    return "\n".join(out)

def write(path, title, description, body, scripts="", jsonld=None, priority="0.6", lastmod=None):
    """path: '/' o '/decidir/slug/'. Genera index.html en esa carpeta."""
    canonical = site["base_url"].rstrip("/") + path
    extra = head_extra()
    if jsonld:
        extra += "\n" + "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    out = BASE.substitute(title=html.escape(title), description=html.escape(description), canonical=canonical,
                          head_extra=extra, body=body, scripts=scripts, site_name=site["name"], year=site["year"])
    d = os.path.join(DIST, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    pages.append((canonical, lastmod or datetime.date.today().isoformat(), priority))

def load_calcs():
    calcs = []
    cdir = os.path.join(ROOT, "calcs")
    for f in sorted(os.listdir(cdir)):
        if f.endswith(".json") and not f.endswith(".test.json"):
            c = json.load(open(os.path.join(cdir, f)))
            c["js"] = open(os.path.join(cdir, c["slug"] + ".js")).read()
            c["content"] = open(os.path.join(ROOT, "content", c["slug"] + ".html")).read()
            calcs.append(c)
    return calcs

def render_calc(c, all_calcs):
    inputs = "".join(
        f'<div><label for="{i["id"]}">{i["label"]}</label>'
        + (f'<select id="{i["id"]}">' + "".join(f'<option value="{o["v"]}">{o["t"]}</option>' for o in i["options"]) + "</select>"
           if i.get("type") == "select" else
           f'<input id="{i["id"]}" type="number" inputmode="decimal" value="{i["default"]}" min="{i.get("min",0)}" step="{i.get("step","any")}">')
        + "</div>" for i in c["inputs"])
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faqs"])
    related = sorted([x for x in all_calcs if x["slug"] != c["slug"]], key=lambda x: tema(x) != tema(c))  # mismo tema primero (sort estable)
    _aff = seo.related_slugs(c["slug"])  # data/clusters.json (Estratega): 2-3 más afines
    if _aff: related = [x for s in _aff for x in all_calcs if x["slug"] == s]
    rel_html = seo.guides_html(c["slug"], GUIDES) + (("<h2>Otras decisiones relacionadas</h2><ul class=\"cards\">" + "".join(card(x) for x in related) + "</ul>") if related else "")
    body = f"""
<h1>{c["h1"]}</h1>
<p class="lead">{c["lead"]}</p>
<div class="calc">
<form id="f" onsubmit="return false"><div class="grid">{inputs}</div><button id="go" type="button">Calcular con mis números</button></form>
<div class="result" id="r"></div>
</div>
{c["content"]}
<h2>Preguntas frecuentes</h2>
{faqs}
<h2>Supuestos y fuentes</h2>
<p class="note">{c["sources"]} Parámetros actualizados el {params["fecha"]}. Los cálculos se hacen en tu navegador; no enviamos tus datos a ningún servidor.</p>
<p class="disclaimer">Esta herramienta es orientativa y no constituye asesoramiento financiero. Comprueba las condiciones concretas de tu contrato y, si la decisión es importante, consulta con un profesional. Lee nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{rel_html}
"""
    jsonld = [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": c["h1"], "applicationCategory": "FinanceApplication",
         "operatingSystem": "Web", "url": site["base_url"] + f"/decidir/{c['slug']}/", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": site["base_url"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Calculadoras", "item": site["base_url"] + "/decidir/"},
            {"@type": "ListItem", "position": 3, "name": c["h1"]}]},
    ] + seo.calc_jsonld(c, site["base_url"].rstrip("/"), params)
    write(f"/decidir/{c['slug']}/", c["title"], c["description"], body, scripts=f"<script>{c['js']}</script>", jsonld=jsonld, priority="0.9",
          lastmod=seo.calc_lastmod(c["slug"], params))

def main():
    shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    calcs = load_calcs()
    seo.build_clusters(calcs, tema)  # -> data/clusters.json, antes de render_calc
    for c in calcs: render_calc(c, calcs)
    cards = "".join(card(c) for c in calcs)
    B = site["base_url"].rstrip("/")
    calcs_mod = max([seo.calc_lastmod(c["slug"], params) for c in calcs] + [g["modified"] for g in GUIDES])
    home_desc = "Calculadoras para decidir con tus propios números: amortizar plazo o cuota, hipoteca fija o variable, renting o compra y más. Gratis, sin registro."
    write("/", f'{site["name"]} — {site["tagline"]}', home_desc,
          HOME.substitute(cards=cards),
          priority="1.0", jsonld=seo.home_jsonld(B, home_desc), lastmod=max(calcs_mod, seo.lastmod("templates/home.html")))
    write("/decidir/", "Todas las calculadoras de decisión", "Lista de comparadores X o Y con tus números: hipoteca, coche, impuestos, energía.",
          catalog_body(calcs), priority="0.8", lastmod=calcs_mod)
    for g in GUIDES:  # guías de apoyo /guias/<slug>/ (Estratega)
        gbody, gld = seo.guide_page(g, calcs, card, B)
        write(f"/guias/{g['slug']}/", g["title"], g["description"], gbody, jsonld=gld, priority="0.7", lastmod=g["modified"])
    if GUIDES:
        write("/guias/", "Guías para decidir mejor — Entre Muchos", "Guías cortas con datos y fuentes oficiales para entender tu hipoteca, el Euríbor y la amortización anticipada.",
              seo.guides_index(GUIDES), priority="0.5", lastmod=max(g["modified"] for g in GUIDES))
    for slug, title, desc in [("como-funciona", "Cómo funciona", "Qué hacemos, qué no, y cómo se calculan los resultados."),
                              ("aviso-legal", "Aviso legal", "Titular, condiciones de uso y limitación de responsabilidad."),
                              ("privacidad", "Política de privacidad", "Qué datos tratamos (casi ninguno) y con qué base legal."),
                              ("cookies", "Política de cookies", "Cookies que usa el sitio y cómo gestionarlas."),
                              ("politica-ia", "Política de uso de IA", "Cómo usamos inteligencia artificial en los textos y qué revisamos."),
                              ("contacto", "Contacto", "Cómo contactar con el editor del sitio.")]:
        body = open(os.path.join(ROOT, "content", f"{slug}.html")).read().replace("$site_name", site["name"]).replace("$owner", site["owner"]).replace("$email", site["contact_email"])
        write(f"/{slug}/", f'{title} — {site["name"]}', desc, body, priority="0.2", lastmod=seo.lastmod(f"content/{slug}.html"))
    open(os.path.join(DIST, "404.html"), "w").write(BASE.substitute(title="Página no encontrada", description="Esta página no existe. Busca una calculadora en el catálogo.", canonical=site["base_url"], head_extra='<meta name="robots" content="noindex">', body=notfound_body(), scripts="", site_name=site["name"], year=site["year"]))
    seo.copy_static(DIST)  # static/ -> raíz: robots.txt (bots de IA permitidos), clave IndexNow
    seo.write_llms(DIST, site, calcs, GUIDES, params, tema, ICONS)  # llms.txt + llms-full.txt
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in pages) + "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    host = site["base_url"].split("//")[1].split("/")[0]
    if "pages.dev" not in host and "github.io" not in host: open(os.path.join(DIST, "CNAME"), "w").write(host + "\n")
    open(os.path.join(DIST, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    print(f"OK: {len(pages)} páginas, {len(calcs)} calculadoras → dist/")

if __name__ == "__main__":
    main()
