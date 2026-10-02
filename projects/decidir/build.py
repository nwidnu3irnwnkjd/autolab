#!/usr/bin/env python3
"""Generador estático de quemeconviene. Sin dependencias. Uso: python3 build.py"""
import json, os, shutil, html, datetime, hashlib
from string import Template
import minify, ogimg, bundle  # minificador y og:image por tema (Diseñador)
import seo  # SEO técnico + GEO (Estratega): lastmod real, clústeres, guías, JSON-LD, llms.txt
import barometro  # /barometro/ con datos propios fechados (Estratega)
import ui, calcs_loader  # interfaz (Diseñador) y carga de calculadoras (Constructor)
from ui import asset_v, ill, ILL, ICONS, tema, card, catalog_body, notfound_body, head_extra

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
site = json.load(open(os.path.join(ROOT, "data/site.json")))
params = json.load(open(os.path.join(ROOT, "data/params.json")))
BASE = Template(open(os.path.join(ROOT, "templates/base.html")).read()
                .replace('/assets/app.css"', f'/assets/app.css?v={asset_v("app.css")}"')
                .replace('/assets/app.js"', f'/assets/app.js?v={asset_v("app.js")}"')
                .replace('__BASE__', site["base_url"].rstrip("/")))
HOME = Template(open(os.path.join(ROOT, "templates/home.html")).read())
pages = []  # (path, lastmod, priority)
GUIDES = seo.load_guides(params)  # content/guias/*.html
LIVE = seo.load_live()  # data/live.json (ops/refresh_data.py): Pulso / «Dato de hoy»
NOTES = seo.load_actualidad()  # content/actualidad/*.html (ops/triggers.py): solo si hay notas
BARO = None  # datos del Barómetro (main)

def write(path, title, description, body, scripts="", jsonld=None, priority="0.6", lastmod=None, og=None):
    """path: '/' o '/decidir/slug/'. Genera index.html en esa carpeta."""
    canonical = site["base_url"].rstrip("/") + path
    extra = head_extra() + "\n" + seo.feed_link()  # Atom /feed.xml (Estratega)
    if jsonld:
        extra += "\n" + "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in jsonld)
    out = BASE.substitute(title=html.escape(title), description=html.escape(description), canonical=canonical,
                          head_extra=extra, body=body, scripts=scripts, site_name=site["name"], year=site["year"]).replace("/assets/illustrations.svg#", ILL + "#")
    if og: out = out.replace("/assets/og.png", "/assets/" + og)
    out = minify.html(out)
    d = os.path.join(DIST, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    pages.append((canonical, lastmod or datetime.date.today().isoformat(), priority))

def render_calc(c, all_calcs):
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faqs"])
    related = sorted([x for x in all_calcs if x["slug"] != c["slug"]], key=lambda x: tema(x) != tema(c))  # mismo tema primero (sort estable)
    _aff = seo.related_slugs(c["slug"])  # data/clusters.json (Estratega): 2-3 más afines
    if _aff: related = [x for s in _aff for x in all_calcs if x["slug"] == s]
    rel_html = seo.guides_html(c["slug"], GUIDES) + barometro.calc_link(c["slug"], BARO) + (("<h2>Otras decisiones relacionadas</h2><ul class=\"cards\">" + "".join(card(x) for x in related) + "</ul>") if related else "")
    body = f"""
{ui.calc_header(c)}
{ui.calc_form(c)}
{c["content"]}
{seo.ahora_html(c["slug"])}{seo.pulso_html(LIVE, c["slug"])}
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
    write(f"/decidir/{c['slug']}/", c["title"], c["description"], body, scripts=f"<script>{minify.js(c['js'])}</script>", jsonld=jsonld, priority="0.9", og=f"og-{tema(c)}.png",
          lastmod=seo.calc_lastmod(c["slug"], params))

def main():
    shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
    ogimg.build_all(os.path.join(ROOT, "assets"), os.path.join(ROOT, ".cache"))  # og-<tema>.png (solo si cambia ogimg.py)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    calcs = calcs_loader.load_calcs(ROOT, params)
    seo.build_clusters(calcs, tema)  # -> data/clusters.json, antes de render_calc
    global BARO
    B = site["base_url"].rstrip("/")
    BARO = barometro.build(DIST, params, B)  # -> dist/barometro/datos.json (antes de render_calc: "Dato del mes")
    for c in calcs: render_calc(c, calcs)
    cards = "".join(card(c) for c in calcs)
    B = site["base_url"].rstrip("/")
    calcs_mod = max([seo.calc_lastmod(c["slug"], params) for c in calcs] + [g["modified"] for g in GUIDES])
    home_desc = "Calculadoras para decidir con tus propios números: amortizar plazo o cuota, hipoteca fija o variable, renting o compra y más. Gratis, sin registro."
    write("/", f'{site["name"]} — {site["tagline"]}', home_desc,
          seo.insert_before(HOME.substitute(cards=cards), "<h2>Cómo funciona</h2>", seo.ahora_html() + seo.actualidad_link(NOTES) + seo.pulso_html(LIVE) + barometro.home_teaser(BARO)),
          priority="1.0", jsonld=seo.home_jsonld(B, home_desc), lastmod=max(calcs_mod, seo.lastmod("templates/home.html", extra=[seo.live_date("/", LIVE)])))
    write("/decidir/", "Todas las calculadoras de decisión", "Lista de comparadores X o Y con tus números: hipoteca, coche, impuestos, energía.",
          catalog_body(calcs), priority="0.8", lastmod=calcs_mod)
    for g in GUIDES:  # guías de apoyo /guias/<slug>/ (Estratega)
        gbody, gld = seo.guide_page(g, calcs, card, B)
        write(f"/guias/{g['slug']}/", g["title"], g["description"], gbody, jsonld=gld, priority="0.7", lastmod=g["modified"])
    bmod = seo.lastmod(*barometro.FILES, extra=[BARO["fecha_datos"]])
    bdesc = f"Datos propios de {barometro.mes_es(BARO['fecha_datos'])}: Euríbor a partir del cual compensa la hipoteca fija, coste por km según motor y cuándo invertir antes que amortizar."
    write(barometro.PATH, f"Barómetro de hipoteca, coche y ahorro ({barometro.mes_es(BARO['fecha_datos'])})", bdesc, barometro.page(BARO, bmod),
          jsonld=barometro.jsonld(BARO, B, bmod, seo.published("barometro.py"), bdesc, seo.org(B), seo.article, seo.breadcrumbs), priority="0.8", lastmod=bmod)
    if GUIDES:
        write("/guias/", "Guías para decidir mejor — Entre Muchos", "Guías cortas con datos y fuentes oficiales para entender tu hipoteca, el Euríbor y la amortización anticipada.",
              seo.guides_index(GUIDES), priority="0.5", lastmod=max(g["modified"] for g in GUIDES))
    cbody, cld, cmod = seo.calendario_page(calcs, B)  # /calendario/: eventos con fuente oficial (Estratega)
    cbody += seo.actualidad_link(NOTES)
    write("/calendario/", "Calendario de decisiones — Entre Muchos", "Fechas que mueven una decisión de dinero en España: Euríbor, tarifa del gas, cambio de hora, Black Friday y Renta, con fuente oficial.",
          cbody, jsonld=cld, priority="0.5", lastmod=cmod)
    if NOTES:  # /actualidad/ solo existe si algún disparador ha generado una nota
        for n in NOTES:
            nbody, nld = seo.actualidad_page(n, calcs, card, B)
            write(f"/actualidad/{n['slug']}/", n["title"], n["description"], nbody, jsonld=nld, priority="0.6", lastmod=n["modified"])
        write("/actualidad/", "Actualidad: datos que cambian decisiones", "Notas breves con datos oficiales cuando el Euríbor, los carburantes, la luz o el tiempo se mueven lo bastante para cambiar una decisión.",
              seo.actualidad_index(NOTES), priority="0.6", lastmod=max(n["modified"] for n in NOTES))
    for slug, title, desc in [("como-funciona", "Cómo funciona", "Qué hacemos, qué no, y cómo se calculan los resultados."),
                              ("aviso-legal", "Aviso legal", "Titular, condiciones de uso y limitación de responsabilidad."),
                              ("privacidad", "Política de privacidad", "Qué datos tratamos (casi ninguno) y con qué base legal."),
                              ("cookies", "Política de cookies", "Cookies que usa el sitio y cómo gestionarlas."),
                              ("politica-ia", "Política de uso de IA", "Cómo usamos inteligencia artificial en los textos y qué revisamos."),
                              ("contacto", "Contacto", "Cómo contactar con el editor del sitio.")]:
        body = open(os.path.join(ROOT, "content", f"{slug}.html")).read().replace("$site_name", site["name"]).replace("$owner", site["owner"]).replace("$email", site["contact_email"])
        write(f"/{slug}/", f'{title} — {site["name"]}', desc, body, priority="0.2", lastmod=seo.lastmod(f"content/{slug}.html"))
    open(os.path.join(DIST, "404.html"), "w").write(BASE.substitute(title="Página no encontrada", description="Esta página no existe. Busca una calculadora en el catálogo.", canonical=site["base_url"], head_extra='<meta name="robots" content="noindex">', body=notfound_body(), scripts="", site_name=site["name"], year=site["year"]).replace("/assets/illustrations.svg#", ILL + "#"))
    bundle.run(ROOT, DIST)  # minifica y recorta CSS/JS por tipo de página (Diseñador)
    seo.copy_static(DIST)  # static/ -> raíz: robots.txt (bots de IA permitidos), clave IndexNow
    seo.write_llms(DIST, site, calcs, GUIDES, params, tema, ICONS, extra=barometro.llms_md(BARO, B), notes=NOTES)  # llms.txt + llms-full.txt
    seo.write_feed(DIST, site, GUIDES, NOTES, BARO, bmod)  # /feed.xml (Atom): actualidad, guías y Barómetro con su fecha real
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in pages) + "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    host = site["base_url"].split("//")[1].split("/")[0]
    if "pages.dev" not in host and "github.io" not in host: open(os.path.join(DIST, "CNAME"), "w").write(host + "\n")
    open(os.path.join(DIST, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    print(f"OK: {len(pages)} páginas, {len(calcs)} calculadoras → dist/")

if __name__ == "__main__":
    main()
