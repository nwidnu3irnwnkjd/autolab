"""Sección /noticias/ «Qué cambia para ti» (Constructor técnico/Diseñador, PLAN-NOTICIAS). Solo stdlib.
Contenido: content/noticias/AAAA-MM-DD-slug.html con <!--meta {json}--> (solo estado «publicada» entra en el build; los `_*.html` no se publican).
URLs: /noticias/AAAA/mm/slug/ (el slug es único por mes), /noticias/, /noticias/AAAA/mm/, /noticias/resumen/, sitemap-noticias.xml, /noticias/feed.xml.
Páginas de tema: NO hasta >= 5 piezas del tema (no implementado a propósito). Revertir: quitar las llamadas a noticias.* en build.py/semana.py."""
import json, os, re, html, datetime
import seo

ROOT = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(ROOT, "content/noticias")
PATH = "/noticias/"
FEED_PATH = "/noticias/feed.xml"
RESUMEN_PATH = "/noticias/resumen/"
POLITICA = "/politica-editorial/"
TIPOS = {"alerta": "Alerta normativa", "dato-mes": "Dato del mes", "cuenta-atras": "Cuenta atrás", "explicador": "Explicador",
         "resumen-dia": "Lo que importa hoy", "resumen-semana": "La semana en tu bolsillo"}
RESUMENES = ("resumen-dia", "resumen-semana")
THIN = 3  # archivos mensuales y /noticias/resumen/ con menos elementos van noindex,follow y fuera del sitemap (evita páginas finas)
e = html.escape
_FN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-([a-z0-9][a-z0-9-]*)\.html$")
_CACHE = {}

def _today(today=None): return today or datetime.date.today()
def _iso(d): return d.isoformat() if isinstance(d, datetime.date) else d

def load(today=None, path=DIR):
    """Piezas publicadas (más recientes primero). Cada una: meta + slug, path, body, modified. Ignora borradores, `_*`, fechas futuras."""
    today = _today(today)
    key = (path, _iso(today))
    if key in _CACHE: return _CACHE[key]
    out, seen = [], {}
    if os.path.isdir(path):
        for f in sorted(os.listdir(path), reverse=True):
            m = _FN.match(f)
            if not m: continue
            raw = open(os.path.join(path, f), encoding="utf-8").read()
            mm = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
            if not mm: continue
            n = json.loads(mm.group(1))
            if n.get("estado") != "publicada" or (n.get("published") or "9999") > today.isoformat(): continue
            y, mo, d, slug = m.groups()
            n.update(file=f, y=y, m=mo, slug=slug, path=f"/noticias/{y}/{mo}/{slug}/", body=raw[mm.end():])
            n.setdefault("modified", n["published"])
            n.setdefault("temas", []); n.setdefault("calcs", []); n.setdefault("fuentes", [])
            if (y, mo, slug) in seen: raise ValueError(f"noticias: slug repetido en {y}/{mo}: {slug} ({f} y {seen[(y, mo, slug)]})")
            seen[(y, mo, slug)] = f
            out.append(n)
    out.sort(key=lambda n: (n["published"], n["file"]), reverse=True)
    _CACHE[key] = out
    return out

def caducada(n, today=None):
    return bool(n.get("caduca")) and n["caduca"] < _iso(_today(today))

def _dias(n, today): return (_today(today) - datetime.date.fromisoformat(n["published"])).days
def _fe(iso): return seo.fecha_es(iso)
def tipo_es(n): return TIPOS.get(n.get("tipo"), "Noticia")
def _t(n): return f'<time datetime="{n["published"]}">{_fe(n["published"])}</time>'

def principal(n):
    f = (n.get("fuentes") or [{}])[0]
    return f if f.get("url") else None

# ---------- bloques de enlazado ----------
def featured(news, today=None):
    """(etiqueta, pieza) de la tarjeta «Lo que importa hoy» / «Última hora»; None si no hay nada reciente."""
    today = _today(today)
    for n in news:
        if n.get("tipo") == "resumen-dia" and _dias(n, today) <= 1: return "Lo que importa hoy", n
    for n in news:
        if n.get("tipo") not in RESUMENES and _dias(n, today) <= 7 and not caducada(n, today):
            return ("Última hora" if n.get("tipo") == "alerta" else "Última noticia"), n
    for n in news:
        if _dias(n, today) <= 14: return "Última noticia", n
    return None

def home_card(news, today=None):
    f = featured(news, today)
    if not f: return ""
    lab, n = f
    return (f'<aside class="box noticia-card" aria-label="{e(lab)}"><p class="kicker">{e(lab)}</p>'
            f'<p><a href="{n["path"]}"><strong>{n["h1"]}</strong></a></p>'
            f'<p class="note">{_t(n)} · {e(n["description"])} <a href="{PATH}">Todas las noticias</a></p></aside>\n')

def calc_block(slug, news, today=None, maxn=2):
    """«En las noticias» de una calculadora: ≤ 2 piezas no caducadas de ≤ 60 días con la calculadora en `calcs`; '' si no hay; ≤ 1 KB."""
    today = _today(today)
    its = [n for n in news if slug in n.get("calcs", []) and n.get("tipo") not in RESUMENES and not caducada(n, today) and _dias(n, today) <= 60][:maxn]
    while its:
        h = ('<h2>En las noticias</h2><ul class="guides noticias-calc">' + "".join(
            f'<li><a href="{n["path"]}">{n["h1"]}</a> <span class="note">{_t(n)}</span></li>' for n in its) + "</ul>")
        if len(h.encode()) <= 1024: return h
        its = its[:-1]
    return ""

def llms_md(news, base, today=None, dias=30):
    today = _today(today)
    its = [n for n in news if _dias(n, today) <= dias]
    if not its: return ""
    ls = ["\n## Noticias (últimos 30 días)\n"]
    for n in its:
        p = principal(n)
        ls.append(f"- [{n['h1']}]({base}{n['path']}): {n['description']} ({n['published']}; {tipo_es(n)}" + (f"; fuente oficial: {p['nombre']} {p['url']}" if p else "") + ")")
    return "\n".join(ls)

# ---------- páginas ----------
def _ogurl(base, path, tema):
    nm = path.strip("/").replace("/", "-")
    f = next((nm + x for x in (".png", ".jpg") if os.path.exists(os.path.join(ROOT, "og", nm + x))), None)
    return base + ("/og/" + f if f else f"/assets/og-{tema}.png")

def _ics(n):
    """Enlace «Añadir al calendario» si la pieza declara `plazo` (AAAA-MM-DD) y `plazo_texto`."""
    d = n.get("plazo")
    if not d: return ""
    dd = d.replace("-", "")
    nxt = (datetime.date.fromisoformat(d) + datetime.timedelta(days=1)).strftime("%Y%m%d")
    txt = n.get("plazo_texto") or n["h1"]
    ics = ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Entre Muchos//Noticias//ES\r\nBEGIN:VEVENT\r\n"
           f"UID:{n['file'][:-5]}@entremuchos.com\r\nDTSTAMP:{n['published'].replace('-', '')}T000000Z\r\nDTSTART;VALUE=DATE:{dd}\r\nDTEND;VALUE=DATE:{nxt}\r\n"
           f"SUMMARY:{txt}\r\nURL:https://entremuchos.com{n['path']}\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
    from urllib.parse import quote
    return f'<p><a class="btn" href="data:text/calendar;charset=utf-8,{quote(ics)}" download="plazo-{d}.ics">Añadir al calendario ({_fe(d)})</a></p>'

def piece_page(n, calcs, card, base, today=None, tema=None):
    """(body, jsonld, tema_og). El cuerpo del archivo ya trae sus 4 bloques; aquí van byline, fuentes, corrección y calculadoras."""
    today = _today(today)
    rel = [c for s in n.get("calcs", []) for c in calcs if c["slug"] == s]
    calc_block_ = ('<h2>Calcula tu caso</h2><ul class="cards">' + "".join(card(c) for c in rel[:3]) + "</ul>") if rel else ""
    upd = f' · Actualizado el <time datetime="{n["modified"]}">{_fe(n["modified"])}</time>' if n["modified"] != n["published"] else ""
    cad = ""
    if caducada(n, today):
        a = n.get("actualizacion") or {}
        cad = (f'<p class="note nota-caduca"><strong>Actualización ({_fe(n["caduca"])}):</strong> el dato de esta pieza ya no es el vigente.'
               + (f' {e(a["texto"])}' if a.get("texto") else "") + (f' <a href="{a["url"]}">Ver el dato vigente</a>.' if a.get("url") else "") + "</p>")
    fu = "".join(f'<li><a href="{f["url"]}" rel="noopener">{e(f["nombre"])}</a>' + (f' (<time datetime="{f["fecha"]}">{_fe(f["fecha"])}</time>)' if f.get("fecha") else "") + "</li>" for f in n["fuentes"])
    body = f"""<article class="guide noticia">
<p class="kicker"><a href="{PATH}">Noticias</a> · {e(tipo_es(n))}</p>
<h1>{n["h1"]}</h1>
<p class="byline note">Por <a href="/como-funciona/">{seo.AUTHOR}</a> · Publicado el <time datetime="{n["published"]}">{_fe(n["published"])}</time>{upd}</p>
{cad}{n["body"]}
{_ics(n)}<h2>Fuentes</h2><ul class="fuentes">{fu}</ul>
<p class="note">Si ves un error, escríbenos a <a href="mailto:hola@entremuchos.com">hola@entremuchos.com</a>: lo corregimos y lo dejamos anotado con su fecha (<a href="{POLITICA}">política editorial</a>). ¿Nos lees en Google? Puedes <a href="https://www.google.com/preferences/source?q=entremuchos.com" rel="noopener">añádenos como fuente preferida en Google</a>.</p>
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero, fiscal ni legal. La fuente oficial manda sobre este texto. Lee <a href="/como-funciona/">cómo trabajamos</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{calc_block_}
</article>"""
    from ui import tema as _tema
    tm = _tema(rel[0]) if rel else "ahorro"
    url = base + n["path"]
    art = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": n["h1"][:110], "description": n["description"],
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url, "inLanguage": "es-ES",
           "datePublished": n["published"], "dateModified": n["modified"], "image": [_ogurl(base, n["path"], tm)],
           "author": {"@type": "Organization", "name": seo.AUTHOR, "url": base + "/como-funciona/"}, "publisher": seo.org(base),
           "articleSection": tipo_es(n)}
    if n.get("temas"): art["keywords"] = ", ".join(n["temas"])
    p = principal(n)
    if p: art["isBasedOn"] = p["url"]
    if rel: art["about"] = [{"@type": "WebApplication", "name": c["h1"], "url": f"{base}/decidir/{c['slug']}/"} for c in rel[:3]]
    return body, [art, seo.breadcrumbs(base, [("Inicio", "/"), ("Noticias", PATH), (n["h1"], None)])], tm

def _li(n, extra=""):
    return (f'<li><a href="{n["path"]}">{n["h1"]}</a><p>{_t(n)} · {e(tipo_es(n))} · {e(n["description"])}{extra}</p></li>')

def index_page(news, base, semana_html="", today=None):
    today = _today(today)
    f = featured(news, today)
    dest = ""
    if f:
        lab, n = f
        dest = (f'<section class="box noticia-card destacada" aria-label="{e(lab)}"><p class="kicker">{e(lab)}</p><h2><a href="{n["path"]}">{n["h1"]}</a></h2>'
                f'<p>{e(n["description"])}</p><p class="note">{_t(n)} · {e(tipo_es(n))}</p></section>')
    ult = [n for n in news if n.get("tipo") not in RESUMENES][:20]
    res = [n for n in news if n.get("tipo") in RESUMENES]
    sem = next((n for n in res if n["tipo"] == "resumen-semana"), None)
    dia = next((n for n in res if n["tipo"] == "resumen-dia" and (not f or n is not f[1])), None)
    rl = "".join(f'<li><a href="{n["path"]}">{n["h1"]}</a> <span class="note">{_t(n)}</span></li>' for n in (dia, sem) if n)
    resb = (f'<h2>Resúmenes</h2><ul class="guides">{rl}</ul><p class="more"><a href="{RESUMEN_PATH}">Todos los resúmenes diarios y semanales</a></p>') if res else ""
    meses = sorted({(n["y"], n["m"]) for n in news}, reverse=True)
    arch = ('<h2>Archivo</h2><p>' + " · ".join(f'<a href="/noticias/{y}/{m}/">{_mes_es(y, m)}</a>' for y, m in meses) + "</p>") if meses else ""
    body = (f'<h1>Noticias: qué cambia para ti</h1><p class="lead">Cada hecho oficial que mueve una cifra de tus decisiones (alquiler, hipoteca, impuestos, luz), con su fuente, su fecha y lo que te toca hacer. '
            f'Sin prensa de segunda mano: solo BOE, INE, BCE, AEAT y demás organismos, y tu cifra calculada con nuestras calculadoras. Cómo trabajamos: <a href="{POLITICA}">política editorial</a>.</p>'
            f'{dest}{semana_html}<h2>Últimas noticias</h2><ul class="cards">' + "".join(_li(n) for n in ult) + f'</ul>{resb}{arch}'
            f'<p class="note">Suscríbete por <a href="{FEED_PATH}">feed Atom</a> · <a href="{POLITICA}">Política editorial y correcciones</a> · <a href="https://www.google.com/preferences/source?q=entremuchos.com" rel="noopener">Añádenos como fuente preferida en Google</a>.</p>')
    mod = max(n["modified"] for n in news)
    return body, [seo.breadcrumbs(base, [("Inicio", "/"), ("Noticias", None)])], mod

def _mes_es(y, m):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{meses[int(m) - 1]} de {y}"

def months(news):
    """[(y, m, piezas, lastmod)] de los meses con piezas."""
    out = []
    for y, m in sorted({(n["y"], n["m"]) for n in news}, reverse=True):
        its = [n for n in news if (n["y"], n["m"]) == (y, m)]
        out.append((y, m, its, max(n["modified"] for n in its)))
    return out

def month_page(y, m, its, base):
    body = (f'<h1>Noticias de {_mes_es(y, m)}</h1><p class="lead">Piezas publicadas en {_mes_es(y, m)}, de la más reciente a la más antigua. '
            f'<a href="{PATH}">Últimas noticias</a>.</p><ul class="cards">' + "".join(_li(n) for n in its) + "</ul>")
    return body, [seo.breadcrumbs(base, [("Inicio", "/"), ("Noticias", PATH), (_mes_es(y, m).capitalize(), None)])]

def resumen_page(news, base):
    res = [n for n in news if n.get("tipo") in RESUMENES]
    if not res: return None
    sec = lambda t, tit: (f"<h2>{tit}</h2><ul class=\"cards\">" + "".join(_li(n) for n in res if n["tipo"] == t) + "</ul>") if any(n["tipo"] == t for n in res) else ""
    body = (f'<h1>Resúmenes diarios y semanales</h1><p class="lead">«Lo que importa hoy» y «La semana en tu bolsillo»: los hechos oficiales del día o de la semana, con su fuente y su efecto en tus cuentas. '
            f'<a href="{PATH}">Volver a Noticias</a>.</p>' + sec("resumen-dia", "Lo que importa hoy") + sec("resumen-semana", "La semana en tu bolsillo"))
    return body, [seo.breadcrumbs(base, [("Inicio", "/"), ("Noticias", PATH), ("Resúmenes", None)])], max(n["modified"] for n in res), len(res)

# ---------- feeds ----------
def feed_items(base, news, limit=30):
    return [dict(id=f"tag:entremuchos.com,2026:noticias/{n['y']}/{n['m']}/{n['slug']}", title=n["h1"], url=base + n["path"], published=n["published"],
                 updated=n["modified"], summary=n["description"], cat="Noticias") for n in news[:limit]]

def write_feed(dist, site, news):
    """/noticias/feed.xml (Atom) con hub WebSub, como /feed.xml."""
    if not news: return 0
    base = site["base_url"].rstrip("/"); x = lambda t: html.escape(str(t), quote=True)
    E = sorted(feed_items(base, news), key=lambda i: (i["updated"], i["published"]), reverse=True)
    ent = "".join(f"""<entry><id>{x(i["id"])}</id><title>{x(i["title"])}</title><link rel="alternate" type="text/html" href="{x(i["url"])}"/>"""
                  f"""<published>{seo._atom_dt(i["published"])}</published><updated>{seo._atom_dt(i["updated"])}</updated><category term="{x(i["cat"])}"/>"""
                  f"""<summary type="text">{x(i["summary"])}</summary></entry>\n""" for i in E)
    xml = (f'<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="es-ES">\n'
           f'<id>{base}{PATH}</id><title>Entre Muchos: noticias, qué cambia para ti</title><subtitle>Hechos oficiales con su fuente, su fecha y su efecto en tus cifras.</subtitle>\n'
           f'<link rel="self" type="application/atom+xml" href="{base}{FEED_PATH}"/><link rel="alternate" type="text/html" href="{base}{PATH}"/><link rel="hub" href="https://pubsubhubbub.appspot.com/"/>\n'
           f'<updated>{seo._atom_dt(max(i["updated"] for i in E))}</updated><author><name>{seo.AUTHOR}</name><uri>{base}/como-funciona/</uri></author>\n'
           f'<rights>Textos © {x(site["name"])}; las normas y actos oficiales citados no son objeto de propiedad intelectual</rights>\n{ent}</feed>\n')
    open(os.path.join(dist, FEED_PATH.strip("/")), "w").write(xml)
    return len(E)

# ---------- migración desde /actualidad/ ----------
def stub(BASE, site, dist, path, target_path, title, ILL):
    """Página mínima noindex con canonical + meta refresh hacia la pieza nueva (GitHub Pages no da 301). No entra en sitemap."""
    base = site["base_url"].rstrip("/")
    body = f'<h1>{e(title)}</h1><p>Esta página se ha movido a <a href="{target_path}">{base}{target_path}</a>.</p>'
    out = BASE.substitute(title=e(title), description="Esta página se ha movido a la sección de Noticias.", canonical=base + target_path, og_alt="", og_image=base + "/assets/og.png",
                          head_extra=f'<meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url={target_path}">',
                          body=body, scripts="", site_name=site["name"], year=site["year"]).replace("/assets/illustrations.svg#", ILL + "#")
    d = os.path.join(dist, path.strip("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
