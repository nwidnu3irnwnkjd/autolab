"""Directorio /todas/, bloques de portada (Por situación, Novedades) y sitemaps por secciones (Estratega, c50)."""
import html, json, os, re, datetime
import seo, semana

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = "/todas/"
e = html.escape

def _short(d, n=80):
    d = d.strip()
    m = re.match(r"(.+?[.!?])(\s|$)", d)
    s = m.group(1) if m and len(m.group(1)) <= n else d
    return s if len(s) <= n else s[:n - 1].rsplit(" ", 1)[0] + "…"

def _li(href, title, desc, kw=""):
    k = ' data-k="' + e(kw) + '"' if kw else ""
    return f'<li{k}><a href="{href}">{e(title)}</a> <span class="note">{e(desc)}</span></li>'

def page(calcs, guides, tablas_mod, tablas_pages, tablas_path, active_hubs, notes, icons, tema, base):
    """-> (body, jsonld, lastmod). Lista agrupada por tema de TODAS las calculadoras + guías, tablas, calendario."""
    items = []  # (nombre, ruta) para el ItemList
    secs = []
    by = {}
    for c in calcs: by.setdefault(tema(c), []).append(c)
    for t, (name, _) in icons.items():
        lst = by.get(t)
        if not lst: continue
        h = active_hubs.get(t)
        hl = f' <a class="note" href="{h["path"]}">Ver el mapa «{e(h["nav"])}»</a>' if h else ""
        lis = []
        for c in sorted(lst, key=lambda x: x["h1"].lower()):
            lis.append(_li(f'/decidir/{c["slug"]}/', c["h1"], _short(c["description"])))
            items.append((c["h1"], f'/decidir/{c["slug"]}/'))
        secs.append(f'<section class="grp"><h2>{e(name)} ({len(lst)}){hl}</h2><ul class="guides">{"".join(lis)}</ul></section>')
    if guides:
        lis = []
        for g in guides:
            lis.append(_li(f'/guias/{g["slug"]}/', g["h1"], _short(g["description"]), "guia"))
            items.append((g["h1"], f'/guias/{g["slug"]}/'))
        secs.append(f'<section class="grp"><h2>Guías ({len(guides)})</h2><ul class="guides">{"".join(lis)}</ul></section>')
    lis = [_li(tablas_path, "Tablas 2026: IRPF, autónomos, ITP, pensiones y trabajo", "Índice de las tablas oficiales con fuente y CSV.", "tablas datos oficiales")]
    items.append(("Tablas 2026", tablas_path))
    for p in tablas_pages:
        lis.append(_li(f'{tablas_path}{p["slug"]}/', p["h1"], _short(p["description"]), "tablas datos oficiales"))
        items.append((p["h1"], f'{tablas_path}{p["slug"]}/'))
    secs.append(f'<section class="grp"><h2>Tablas 2026 ({len(tablas_pages)})</h2><ul class="guides">{"".join(lis)}</ul></section>')
    extra = [("/barometro/", "Barómetro de hipoteca, coche y ahorro", "Datos propios del mes con su fecha."),
             ("/calendario/", "Calendario de decisiones", "Fechas que mueven una decisión de dinero en España, con fuente oficial.")]
    extra.append(("/inserta/", "Inserta una calculadora en tu web", "Widget gratis con crédito y enlace, con código para copiar."))  # embed.py (Diseñador)
    extra.append((semana.PATH2027, "Qué cambia el 1 de enero de 2027", "Cifras de 2026 y estado de las de 2027."))
    if notes: extra.append(("/actualidad/", "Actualidad: datos que cambian decisiones", "Notas breves con datos oficiales."))
    for k, h in active_hubs.items(): extra.append((h["path"], h["h1"], _short(h["description"])))
    lis = "".join(_li(p, n, d, "calendario barometro mapa tema") for p, n, d in extra)
    for p, n, d in extra: items.append((n, p))
    secs.append(f'<section class="grp"><h2>Calendario, Barómetro y mapas por tema</h2><ul class="guides">{lis}</ul></section>')
    total = len(items)
    mod = seo.lastmod("directorio.py", extra=[g["modified"] for g in guides] + [tablas_mod])
    pub = seo.published("directorio.py")
    body = f"""<article class="guide hub dir">
<p class="kicker">Directorio</p>
<h1>Todas las calculadoras y guías</h1>
<p class="byline note">Por {seo.AUTHOR} · Actualizado el <time datetime="{mod}">{seo.fecha_es(mod)}</time></p>
<p class="lead">Lista completa de las {len(calcs)} calculadoras de decisión de Entre Muchos, ordenadas por tema, con las {len(guides)} guías, las tablas oficiales de 2026 y el calendario. Escribe una palabra para filtrar.</p>
<div class="search" role="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<label for="dq" class="sr-only">Filtrar la lista</label><input id="dq" type="search" placeholder="Filtra: hipoteca, autónomo, luz, pensión…" autocomplete="off"></div>
<p class="note" id="dc" role="status" aria-live="polite">{total} páginas</p>
{"".join(secs)}
<p class="empty" id="de" hidden>No hay nada con esa palabra. Prueba con otra o <a href="/contacto/">cuéntanos qué te falta</a>.</p>
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>
<script>(function(){{var q=document.getElementById("dq"),c=document.getElementById("dc"),m=document.getElementById("de"),g=document.querySelectorAll(".dir .grp");
function n(s){{return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"")}}
q.addEventListener("input",function(){{var t=n(q.value).trim().split(/\\s+/).filter(Boolean),v=0;
Array.prototype.forEach.call(g,function(s){{var a=0;Array.prototype.forEach.call(s.querySelectorAll("li"),function(l){{var h=n(l.textContent+" "+(l.getAttribute("data-k")||"")),ok=t.every(function(w){{return h.indexOf(w)>-1}});l.hidden=!ok;if(ok)a++}});s.hidden=!a;v+=a}});
c.textContent=v+(v===1?" página":" páginas");m.hidden=v>0}})}})();</script>"""
    url = base + PATH
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Todas las calculadoras y guías", "url": url,
           "description": f"Lista completa de las {len(calcs)} calculadoras de decisión, guías, tablas 2026 y calendario.",
           "inLanguage": "es-ES", "datePublished": pub, "dateModified": mod, "isPartOf": {"@id": base + "/#website"},
           "publisher": seo.org(base),
           "mainEntity": {"@type": "ItemList", "numberOfItems": total, "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "name": n, "url": base + p} for i, (n, p) in enumerate(items)]}},
          seo.breadcrumbs(base, [("Inicio", "/"), ("Todas las calculadoras", None)])]
    return body, ld, mod

# ---------- portada ----------
SITUACIONES = [  # (etiqueta, descripción, destino, tipo de destino: hub|guia|calc)
    ("Soy autónomo", "Cuota, regularización y módulos", "autonomo-2026-cuota-regularizacion-modulos", "guia"),
    ("Tengo hijos o familia", "Guardería, cuidadora o reducir jornada", "guarderia-cuidadora-o-reducir-jornada", "calc"),
    ("Me han despedido o estoy en paro", "Indemnización, paro y plazos", "me-han-despedido-indemnizacion-paro-plazos", "guia"),
    ("Compro vivienda", "Hipoteca paso a paso", "hipoteca", "hub"),
    ("Gasto en casa y luz", "Factura, potencia y tarifa", "energia", "hub"),
    ("Mi coche", "Comprar, renting, combustible", "coche", "hub"),
    ("Jubilación y pensiones", "Anticipada o demorada", "jubilacion-anticipada-o-demorada", "calc"),
    ("Ahorro y dinero", "Dónde poner tu dinero", "ahorro", "hub"),
]

def situacion_html(calcs, guides, active_hubs):
    cs = {c["slug"] for c in calcs}; gs = {g["slug"] for g in guides}; lis = []
    for lab, d, dest, kind in SITUACIONES:
        if kind == "hub" and dest in active_hubs: href = active_hubs[dest]["path"]
        elif kind == "guia" and dest in gs: href = f"/guias/{dest}/"
        elif kind == "calc" and dest in cs: href = f"/decidir/{dest}/"
        else: continue
        lis.append(f'<li><a href="{href}">{e(lab)}</a> <span class="note">{e(d)}</span></li>')
    return ('<h2 id="situacion">Por situación</h2><ul class="guides">' + "".join(lis) + "</ul>") if len(lis) >= 6 else ""

def novedades_html(calcs, guides, params, n=6):
    rows = []
    for c in calcs:
        fs = [os.path.join(ROOT, f) for f in seo.calc_files(c["slug"]) if os.path.exists(os.path.join(ROOT, f))]
        rows.append((seo.published(*seo.calc_files(c["slug"])), max(os.path.getmtime(f) for f in fs), f'/decidir/{c["slug"]}/', c["h1"]))
    for g in guides:
        rows.append((g["published"], os.path.getmtime(os.path.join(ROOT, "content/guias", g["slug"] + ".html")), f'/guias/{g["slug"]}/', g["h1"]))
    rows.sort(reverse=True)
    lis = "".join(f'<li><a href="{p}">{e(t)}</a> <span class="note"><time datetime="{d}">{seo.fecha_es(d)}</time></span></li>' for d, _, p, t in rows[:n])
    return f'<h2 id="novedades">Novedades</h2><ul class="guides">{lis}</ul><p class="more"><a href="{PATH}">Ver la lista completa de calculadoras y guías</a></p>'

# ---------- sitemaps por secciones ----------
def _section(path):
    if path.startswith("/decidir/") and path != "/decidir/": return "calculadoras"
    if path.startswith("/guias/") and path != "/guias/": return "guias"
    if path.startswith("/tablas-2026/") and path != "/tablas-2026/": return "tablas"
    if path.startswith("/actualidad/") and path != "/actualidad/": return "guias"
    return "hubs"

def write_sitemaps(dist, pages, base):
    """pages: (url, lastmod, priority). Escribe sitemap-<sección>.xml y sitemap.xml como <sitemapindex> (misma URL que ya está en Search Console)."""
    secs = {}
    for u, d, p in pages: secs.setdefault(_section(u[len(base):]), []).append((u, d, p))
    idx = []
    for name in ("calculadoras", "guias", "tablas", "hubs"):
        rows = secs.get(name, [])
        if not rows: continue
        x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
            f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in rows) + "</urlset>\n"
        open(os.path.join(dist, f"sitemap-{name}.xml"), "w").write(x)
        idx.append((f"{base}/sitemap-{name}.xml", max(d for _, d, _ in rows)))
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<sitemap><loc>{u}</loc><lastmod>{d}</lastmod></sitemap>\n" for u, d in idx) + "</sitemapindex>\n"
    open(os.path.join(dist, "sitemap.xml"), "w").write(x)
    return len(idx)
