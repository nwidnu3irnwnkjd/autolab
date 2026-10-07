#!/usr/bin/env python3
"""Generador estático de quemeconviene. Sin dependencias. Uso: python3 build.py"""
import json, os, shutil, html, datetime, hashlib
from string import Template
import minify, ogimg, bundle  # minificador y og:image por tema (Diseñador)
import seo  # SEO técnico + GEO (Estratega): lastmod real, clústeres, guías, JSON-LD, llms.txt
import hubs  # /hipoteca/ y futuros hubs temáticos (Estratega)
import barometro  # /barometro/ con datos propios fechados (Estratega)
import directorio, asistente  # /todas/, Por situación, Novedades, sitemaps por secciones (Estratega, c50)
import plan  # plan completo «Compra de vivienda» (Diseñador, R16.4)
import noticias  # sección /noticias/ «Qué cambia para ti» (Constructor, PLAN-NOTICIAS)
import semana  # «Esta semana» y /que-cambia-1-enero-2027/ (Estratega, c51)
import tablas  # /tablas-2026/: tablas oficiales verificadas + cálculo propio + CSV (Estratega, c36)
import datos  # /datos/<serie>/: IRAV, Euríbor y luz persistentes (Constructor, E3)
import popularidad  # bucle de popularidad: lee data/popularidad.json (ops/popularidad.py)
import embed  # widget insertable /embed/<slug>/ y /inserta/ (Diseñador)
import respuestas  # tablas de respuesta de la cola numérica (lee data/tablas_respuesta.json; ops/gen_tablas_respuesta.py)
import ejemplos  # «Ejemplo resuelto» estático de las insignia (lee data/ejemplos.json; ops/gen_ejemplos.py)
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
NEWS = noticias.load()  # content/noticias/*.html con estado «publicada»
ALL_NOTES = seo.load_actualidad()  # content/actualidad/*.html (ops/triggers.py)
_MIGR = {n['clave']: n for n in NEWS if n.get('clave')}  # notas de actualidad ya migradas a una pieza de noticias: no se duplican
NOTES = [n for n in ALL_NOTES if n.get('clave') not in _MIGR]  # solo si hay notas sin migrar
BARO = None  # datos del Barómetro (main)
ACTIVE_HUBS = {}  # hubs que cumplen el disparador (main)

SPEC = '<script type="speculationrules">{"prefetch":[{"where":{"href_matches":"/decidir/*"},"eagerness":"moderate"}]}</script>'

def write(path, title, description, body, scripts="", jsonld=None, priority="0.6", lastmod=None, og=None, og_tema=None, noindex=False):
    """path: '/' o '/decidir/slug/'. Genera index.html en esa carpeta."""
    canonical = site["base_url"].rstrip("/") + path
    extra = head_extra() + "\n" + seo.feed_link()  # Atom /feed.xml (Estratega)
    if noindex: extra += '\n<meta name="robots" content="noindex,follow">'  # páginas finas (archivos con pocas piezas): fuera del sitemap
    if jsonld:
        extra += "\n" + "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in jsonld)
    if og_tema or og:  # SVG 1200x630 única por página con su título (og-svg/, para rasterizar: ver ogimg.py)
        ogimg.write_svg(os.path.join(ROOT, "og-svg"), (path.strip("/").replace("/", "-") or "home"), title, og_tema or og[3:-4])
    _n = path.strip("/").replace("/", "-") or "home"  # og:image por página: og/<slug>.png|jpg (rasterizado y commiteado, ops/og_raster.py); si no existe, PNG por tema
    _f = next((_n + e for e in (".png", ".jpg") if os.path.exists(os.path.join(ROOT, "og", _n + e))), None)
    _img = site["base_url"].rstrip("/") + ("/og/" + _f if _f else "/assets/" + (og or "og.png"))
    if path in ("/", "/todas/", "/hipoteca/", "/coche/", "/energia/", "/impuestos/", "/ahorro/") or path.startswith("/guias/"):
        scripts += SPEC  # prefetch conservador de calculadoras (solo Chromium; no prerender, no toca cookies)
    out = BASE.substitute(title=html.escape(title), description=html.escape(description), canonical=canonical, og_alt=html.escape(title, quote=True), og_image=_img,
                          head_extra=extra, body=body, scripts=scripts, site_name=site["name"], year=site["year"]).replace("/assets/illustrations.svg#", ILL + "#")
    out = minify.html(out)
    d = os.path.join(DIST, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    if not noindex: pages.append((canonical, lastmod or datetime.date.today().isoformat(), priority))

def render_calc(c, all_calcs):
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faqs"])
    related = sorted([x for x in all_calcs if x["slug"] != c["slug"]], key=lambda x: tema(x) != tema(c))  # mismo tema primero (sort estable)
    _aff = seo.related_slugs(c["slug"])  # data/clusters.json (Estratega): 2-3 más afines
    if _aff: related = [x for s in _aff for x in all_calcs if x["slug"] == s]
    rel_html = noticias.calc_block(c["slug"], NEWS) + seo.guides_html(c["slug"], GUIDES) + barometro.calc_link(c["slug"], BARO) + tablas.calc_link(c["slug"]) + hubs.calc_link(c["slug"], all_calcs, ACTIVE_HUBS) + (("<h2>Otras decisiones relacionadas</h2><ul class=\"cards\">" + "".join(card(x) for x in related) + "</ul>") if related else "")
    _lm = seo.calc_lastmod(c["slug"], params)
    body = f"""
{ui.calc_header(c)}
<p class="note upd">Actualizado: <time datetime="{_lm}">{seo.fecha_es(_lm)}</time></p>
{ui.calc_form(c)}
{ejemplos.block(c['slug'])}
{plan.next_block(c['slug'])}
{c["content"]}
{respuestas.block(c["slug"])}
{seo.ahora_html(c["slug"])}{seo.pulso_html(LIVE, c["slug"])}
<h2>Preguntas frecuentes</h2>
{faqs}
<h2>Supuestos y fuentes</h2>
<p class="note">{c["sources"]} Parámetros actualizados el {params["fecha"]}. Los cálculos se hacen en tu navegador; no enviamos tus datos a ningún servidor.</p>
<p class="disclaimer">Esta herramienta es orientativa y no constituye asesoramiento financiero. Comprueba las condiciones concretas de tu contrato y, si la decisión es importante, consulta con un profesional. Lee nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{embed.block(c)}
{rel_html}{popularidad.otros_block(c['slug'], all_calcs, tema, {x['slug'] for x in related})}
"""
    jsonld = [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
        seo.webapp(c, site["base_url"].rstrip("/"), _lm),
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
    if os.path.isdir(os.path.join(ROOT, "og")): shutil.copytree(os.path.join(ROOT, "og"), os.path.join(DIST, "og"))  # PNG/JPG por página (commiteados)
    calcs = ejemplos.apply(calcs_loader.load_calcs(ROOT, params))
    seo.build_clusters(calcs, tema)  # -> data/clusters.json, antes de render_calc
    global BARO, ACTIVE_HUBS
    ACTIVE_HUBS = popularidad.order_hubs(hubs.eligible(calcs, GUIDES), calcs)  # disparador: >= 6 páginas del tema; orden por popularidad si hay datos
    B = site["base_url"].rstrip("/")
    BARO = barometro.build(DIST, params, B)  # -> dist/barometro/datos.json (antes de render_calc: "Dato del mes")
    plan.validate(calcs)
    for c in calcs: render_calc(c, calcs)
    ASIS = asistente.build(DIST, calcs, GUIDES, tablas.PAGES)  # asistente «¿Cuál es tu situación?» (Diseñador)
    cards = ui.home_cards(calcs)  # R18.1/peso: solo destacadas en la home (resto: lazy desde /decidir/)
    B = site["base_url"].rstrip("/")
    calcs_mod = max([seo.calc_lastmod(c["slug"], params) for c in calcs] + [g["modified"] for g in GUIDES])
    home_desc = "Calculadoras para decidir con tus propios números: amortizar plazo o cuota, hipoteca fija o variable, renting o compra y más. Gratis, sin registro."
    write("/", f'{site["name"]} — {site["tagline"]}', home_desc,
          seo.insert_before(seo.insert_before(HOME.substitute(cards=cards).replace('<a href="/decidir/" id="more">Ver todas las calculadoras</a>', '<a href="/decidir/" id="more">Ver todas las calculadoras</a> · <a href="/todas/">Lista completa</a>', 1), '<h2 id="calculadoras">', popularidad.home_block(calcs) + noticias.home_card(NEWS) + ASIS + directorio.situacion_html(calcs, GUIDES, ACTIVE_HUBS)), "<h2>Cómo funciona</h2>", directorio.novedades_html(calcs, GUIDES, params) + seo.ahora_html() + seo.actualidad_link(NOTES) + hubs.home_link(ACTIVE_HUBS) + semana.block(LIVE, sin_noticia=True) + barometro.home_teaser(BARO)),
          priority="1.0", jsonld=seo.home_jsonld(B, home_desc), lastmod=max(calcs_mod, seo.lastmod("templates/home.html", extra=[seo.live_date("/", LIVE)])))
    write("/decidir/", "Todas las calculadoras de decisión", "Lista de comparadores X o Y con tus números: hipoteca, coche, impuestos, energía.",
          catalog_body(calcs), priority="0.8", lastmod=calcs_mod)
    for g in GUIDES:  # guías de apoyo /guias/<slug>/ (Estratega)
        gbody, gld = seo.guide_page(g, calcs, card, B)
        gbody = seo.insert_before(gbody, '<p class="disclaimer">', hubs.guide_link(g, calcs, GUIDES, ACTIVE_HUBS))
        write(f"/guias/{g['slug']}/", g["title"], g["description"], gbody, jsonld=gld, priority="0.7", lastmod=g["modified"], og=f"og-{(tema(next((c for s_ in g.get('calcs', []) for c in calcs if c['slug'] == s_), {'slug': ''})) if g.get('calcs') else 'ahorro')}.png")
    bmod = seo.lastmod(*barometro.FILES, extra=[BARO["fecha_datos"]])
    bdesc = f"Datos propios de {barometro.mes_es(BARO['fecha_datos'])}: Euríbor a partir del cual compensa la hipoteca fija, coste por km según motor y cuándo invertir antes que amortizar."
    write(barometro.PATH, barometro.titulo_corto(BARO), bdesc, barometro.page(BARO, bmod),
          jsonld=barometro.jsonld(BARO, B, bmod, seo.published("barometro.py"), bdesc, seo.org(B), seo.article, seo.breadcrumbs), priority="0.8", lastmod=bmod)
    TAB = tablas.build(DIST, params, B)  # -> dist/tablas-2026/<slug>/datos.csv y datos.json
    tmod = seo.lastmod(*tablas.FILES); tpub = seo.published("tablas.py")
    for p in tablas.PAGES:
        write(tablas.path(p["slug"]), p["title"], p["description"], tablas.page(p["slug"], TAB, calcs, card, tmod, seo.AUTHOR),
              jsonld=tablas.jsonld(p["slug"], TAB, B, tmod, tpub, seo.org(B), seo.article, seo.breadcrumbs), priority="0.8", lastmod=tmod, og_tema="impuestos")
    tdesc = "Tablas oficiales 2026 con fuente: IRPF por comunidad, cuota de autónomos, ITP y AJD, SMI, paro, pensiones, despido y permisos. Con CSV."
    write(tablas.INDEX, "Tablas 2026: IRPF, autónomos, ITP, pensiones y trabajo", tdesc, tablas.index_page(TAB, tmod, seo.AUTHOR),
          jsonld=tablas.index_jsonld(B, tmod, tpub, seo.org(B), seo.breadcrumbs, tdesc), priority="0.7", lastmod=tmod)
    DAT = datos.build(LIVE, params)  # /datos/*: se regeneran con live.json/params.json
    if DAT:
        dpub = seo.published("datos.py")
        for k, s in DAT.items():
            write(datos.PATHS[k], s["title"], s["description"], s["body"], jsonld=datos.jsonld(k, DAT, B, dpub, seo.org(B), seo.breadcrumbs), priority="0.8", lastmod=s["fecha"], og_tema={"irav": "hipoteca", "euribor": "hipoteca", "luz": "energia"}[k])
            os.makedirs(os.path.join(DIST, datos.PATHS[k].strip("/")), exist_ok=True)
            open(os.path.join(DIST, datos.PATHS[k].strip("/"), "datos.csv"), "w", encoding="utf-8").write(s["csv"])
        dmod_ = max(s["fecha"] for s in DAT.values())
        write(datos.INDEX, "Datos al día: IRAV, Euríbor y precio de la luz", "Series que se actualizan solas con su fecha y fuente: IRAV e IPC del alquiler, Euríbor a 12 meses y precio de la luz (PVPC) de hoy.", datos.index_page(DAT),
              jsonld=datos.index_jsonld(DAT, B, dmod_, dpub, seo.org(B), seo.breadcrumbs), priority="0.7", lastmod=dmod_, og_tema="hipoteca")
    ebody, eld, edesc = embed.page(calcs)  # /inserta/ + /embed/<slug>/ (estos últimos noindex y fuera de sitemap: no pasan por write())
    write(embed.PATH, "Inserta una calculadora en tu web — Entre Muchos", edesc, ebody, jsonld=eld, priority="0.5", lastmod=seo.lastmod("embed.py"))
    embed.build(DIST, calcs)
    HUB_PAGES = []
    for k, spec in ACTIVE_HUBS.items():  # hubs temáticos (hubs.py): mapa en orden de decisión con datos vivos
        hbody, hld, hmod = hubs.page(k, spec, calcs, GUIDES, params, LIVE, card, B, baro_texts=barometro.answers_text(BARO) or [], tablas_items=tablas.hub_items(k))
        if k in ("hipoteca", "impuestos"):
            pl = "".join(plan.hub_link(spec["path"], pk) for pk in (["compra-vivienda", "alquilar-vivienda"] if k == "hipoteca" else ["autonomo", "despido"]))
            hbody = seo.insert_before(hbody, "<h2>Guías y datos propios</h2>", pl)
        _dk = {"hipoteca": ["euribor", "irav"], "energia": ["luz"]}.get(k)
        if _dk and DAT: hbody = seo.insert_before(hbody, "<h2>Guías y datos propios</h2>", "<h2>Datos al día</h2><ul class=\"guides\">" + datos.hub_block(DAT, _dk) + "</ul>")
        write(spec["path"], spec["title"], spec["description"], hbody, jsonld=hld, priority="0.8", lastmod=hmod, og=f"og-{spec['tema']}.png")
        HUB_PAGES.append(dict(spec, modified=hmod, published=seo.published("hubs.py")))
    s27body, s27ld = semana.cambios_page(params, calcs, card, seo.lastmod(*semana.FILES), seo.AUTHOR)  # /que-cambia-1-enero-2027/ (c51)
    s27mod = seo.lastmod(*semana.FILES); s27pub = seo.published("semana.py")
    write(semana.PATH2027, semana.H2027, semana.D2027, s27body, priority="0.8", lastmod=s27mod, og_tema="impuestos",
          jsonld=[seo.article(semana.H2027, semana.D2027, B + semana.PATH2027, s27pub, s27mod, B), seo.breadcrumbs(B, [("Inicio", "/"), ("Qué cambia en 2027", None)])] + s27ld)
    HUB_PAGES.append(dict(path=semana.PATH2027, h1=semana.H2027, description=semana.D2027, modified=s27mod, published=s27pub))
    pmod = seo.lastmod(*plan.FILES); ppub = seo.published("plan.py")
    for pk, pp in plan.PLANES.items():  # planes completos (Diseñador, R16.4): compra de vivienda, autónomo, despido
        if pk.startswith("_"): continue
        pbody, pld = plan.page(pk, calcs, card, B, ppub, pmod)
        write(pp["path"], pp["title"], pp["description"], pbody, jsonld=pld, priority="0.8", lastmod=pmod, og=f"og-{'hipoteca' if pk in ('compra-vivienda', 'alquilar-vivienda') else 'impuestos'}.png")
        HUB_PAGES.append(dict(path=pp["path"], h1=pp["h1"], description=pp["description"], modified=pmod, published=ppub))
    dbody, dld, dmod = directorio.page(calcs, GUIDES, tmod, tablas.PAGES, tablas.INDEX, ACTIVE_HUBS, NOTES, ICONS, tema, B)
    dbody = seo.insert_before(dbody, '<li data-k="calendario barometro mapa tema">', ''.join(plan.dir_li(k) for k in plan.PLANES if not k.startswith('_')))  # planes completos (Diseñador)
    if DAT: dbody = seo.insert_before(dbody, '<li data-k="calendario barometro mapa tema">', ''.join(f'<li data-k="datos al dia hoy {k}"><a href="{datos.PATHS[k]}">{s["h1"]}</a> <span class="note">{s["resumen"]}</span></li>' for k, s in DAT.items()))
    write(directorio.PATH, "Todas las calculadoras de decisión: lista completa", f"Lista completa de las {len(calcs)} calculadoras de decisión por tema (hipoteca, coche, impuestos, energía, ahorro), con guías y tablas 2026. Filtra por palabra.",
          seo.insert_before(seo.insert_before(dbody, '<div class="search" role="search">', ASIS), '<section class="grp">', popularidad.todas_block(calcs, directorio._li)), jsonld=dld, priority="0.8", lastmod=dmod)
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
              semana.block(LIVE) + seo.actualidad_index(NOTES), priority="0.6", lastmod=max(n["modified"] for n in NOTES))
    if NEWS:  # /noticias/ (Constructor): portada, piezas, archivos mensuales y resúmenes; archivo/resúmenes con < 3 elementos van noindex
        for n in NEWS:
            nbody, nld, ntema = noticias.piece_page(n, calcs, card, B, tema=tema)
            write(n["path"], n["title"], n["description"], nbody, jsonld=nld, priority="0.7", lastmod=n["modified"], og_tema=ntema)
        ibody, ild, imod = noticias.index_page(NEWS, B, semana.block(LIVE, sin_noticia=True))
        write(noticias.PATH, "Noticias: qué cambia para ti — Entre Muchos", "Hechos oficiales (BOE, INE, BCE, AEAT) que mueven tus cifras: alquiler, hipoteca, impuestos y luz, con fuente, fecha y qué hacer.", ibody, jsonld=ild, priority="0.8", lastmod=imod, og_tema="impuestos")
        for y_, m_, its, mmod in noticias.months(NEWS):
            mbody, mld = noticias.month_page(y_, m_, its, B)
            write(f"/noticias/{y_}/{m_}/", f"Noticias de {noticias._mes_es(y_, m_)} — Entre Muchos", f"Noticias de {noticias._mes_es(y_, m_)}: hechos oficiales y lo que cambian en tus cifras, con fuente y fecha.", mbody, jsonld=mld, priority="0.5", lastmod=mmod, og_tema="impuestos", noindex=len(its) < noticias.THIN)
        _r = noticias.resumen_page(NEWS, B)
        if _r:
            write(noticias.RESUMEN_PATH, "Resúmenes diarios y semanales — Entre Muchos", "Lo que importa hoy y la semana en tu bolsillo: hechos oficiales con su fuente y su efecto en tus cuentas.", _r[0], jsonld=_r[1], priority="0.5", lastmod=_r[2], og_tema="impuestos", noindex=_r[3] < noticias.THIN)
        noticias.write_feed(DIST, site, NEWS)  # /noticias/feed.xml
    for n_ in ALL_NOTES:  # nota de /actualidad/ migrada a noticias: redirige a la pieza (sin contenido duplicado)
        if n_.get("clave") in _MIGR:
            noticias.stub(BASE, site, DIST, f"/actualidad/{n_['slug']}/", _MIGR[n_["clave"]]["path"], n_["title"], ILL)
    if _MIGR and not NOTES: noticias.stub(BASE, site, DIST, "/actualidad/", noticias.PATH, "Actualidad: ahora en Noticias", ILL)
    for slug, title, desc in [("como-funciona", "Cómo funciona", "Cómo calculamos: fuentes oficiales (BOE, BCE, INE), Barómetro con datos del mes y verificación de cada cifra antes de publicar. Qué hacemos y qué no."),
                              ("politica-editorial", "Política editorial", "Cómo elegimos y verificamos cada noticia: solo fuentes oficiales, correcciones con fecha, uso de IA, derechos de autor y contacto."),
                              ("aviso-legal", "Aviso legal", "Titular, condiciones de uso y limitación de responsabilidad."),
                              ("privacidad", "Política de privacidad", "Qué datos tratamos (casi ninguno) y con qué base legal."),
                              ("cookies", "Política de cookies", "Cookies que usa el sitio y cómo gestionarlas."),
                              ("politica-ia", "Política de uso de IA", "Cómo usamos inteligencia artificial en los textos y qué revisamos."),
                              ("contacto", "Contacto", "Cómo contactar con el editor del sitio.")]:
        body = open(os.path.join(ROOT, "content", f"{slug}.html")).read().replace("$site_name", site["name"]).replace("$owner", site["owner"]).replace("$email", site["contact_email"])
        write(f"/{slug}/", f'{title} — {site["name"]}', desc, body, priority="0.2", lastmod=seo.lastmod(f"content/{slug}.html"))
    open(os.path.join(DIST, "404.html"), "w").write(BASE.substitute(title="Página no encontrada", description="Esta página no existe. Busca una calculadora en el catálogo.", canonical=site["base_url"], og_alt="", og_image=site["base_url"].rstrip("/") + "/assets/og.png", head_extra='<meta name="robots" content="noindex">', body=notfound_body(), scripts="", site_name=site["name"], year=site["year"]).replace("/assets/illustrations.svg#", ILL + "#"))
    bundle.run(ROOT, DIST)  # minifica y recorta CSS/JS por tipo de página (Diseñador)
    seo.copy_static(DIST)  # static/ -> raíz: robots.txt (bots de IA permitidos), clave IndexNow
    seo.write_llms(DIST, site, calcs, GUIDES, params, tema, ICONS, extra=barometro.llms_md(BARO, B), notes=NOTES, news_md=noticias.llms_md(NEWS, B), hubs=HUB_PAGES, tablas=tablas.llms_lines(B), tablas_md=tablas.llms_md(TAB, B))  # llms.txt + llms-full.txt
    seo.write_feed(DIST, site, GUIDES, NOTES, BARO, bmod, hubs=HUB_PAGES, extra=tablas.feed_items(B, tmod, tpub) + noticias.feed_items(B, NEWS))  # /feed.xml (Atom): actualidad, guías y Barómetro con su fecha real
    directorio.write_sitemaps(DIST, pages, B)  # sitemap.xml = índice; sitemap-{calculadoras,guias,tablas,hubs}.xml
    host = site["base_url"].split("//")[1].split("/")[0]
    if "pages.dev" not in host and "github.io" not in host: open(os.path.join(DIST, "CNAME"), "w").write(host + "\n")
    open(os.path.join(DIST, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    print(f"OK: {len(pages)} páginas, {len(calcs)} calculadoras → dist/")

if __name__ == "__main__":
    main()
