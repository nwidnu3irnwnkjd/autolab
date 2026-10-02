"""Interfaz del sitio (dueño: Diseñador): iconos, temas, tarjetas, catálogo, 404, cabecera y formulario de calculadora, head extra."""
import json, os, html, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
site = json.load(open(os.path.join(ROOT, "data/site.json")))
def asset_v(name):
    return hashlib.sha1(open(os.path.join(ROOT, "assets", name), "rb").read()).hexdigest()[:10]
ILL = f'/assets/illustrations.svg?v={asset_v("illustrations.svg")}'  # sprite de ilustraciones (Diseñador, fase 2)
def ill(sym, cls, w, h):
    return f'<svg class="{cls}" viewBox="0 0 160 120" width="{w}" height="{h}" aria-hidden="true" focusable="false"><use href="/assets/illustrations.svg#{sym}"/></svg>'
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
    return f'<li data-q="{q}" data-t="{t}">{ill(t, "ill-s", 88, 66)}<a href="/decidir/{c["slug"]}/">{c["h1"]}</a><p>{c["description"]}</p><span class="tag">{name}</span></li>'

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
<div class="empty-state" id="empty" hidden>{ill("vacio", "ill-e", 160, 120)}
<h2>No hemos encontrado esa calculadora</h2><p>Prueba con otra palabra (por ejemplo «hipoteca» o «coche») o quita el filtro de tema.</p>
<p><button type="button" id="reset" class="btn2">Ver todas las calculadoras</button></p><p class="note">¿Te falta alguna? <a href="/contacto/">Cuéntanoslo</a> y la preparamos.</p></div>"""

def notfound_body():
    return """<section class="nf">""" + ill("perdido", "nf-i", 240, 180) + """<p class="nf-code">Error 404</p><h1>No encontramos esa página</h1>
<p class="lead">Puede que el enlace haya cambiado o esté mal escrito. Busca la calculadora que necesitas:</p>
<form class="search" role="search" action="/decidir/" method="get"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
<label for="q" class="sr-only">Buscar calculadora</label><input id="q" name="q" type="search" placeholder="Busca: hipoteca, renting, Euríbor…" autocomplete="off"></form>
<p><a class="btn" href="/decidir/">Ver todas las calculadoras</a> <a class="btn2" href="/">Ir al inicio</a></p></section>"""
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

HUB_PATHS = {"hipoteca": "/hipoteca/", "coche": "/coche/", "energia": "/energia/"}  # hubs.HUBS (R16.1); resto de temas: ancla del catálogo

def calc_header(c):
    """Cabecera .ph de una calculadora."""
    return f"""<header class="ph ph-{tema(c)}"><p class="kicker"><a href="{HUB_PATHS.get(tema(c), "/decidir/#" + tema(c))}">{ICONS[tema(c)][0]}</a></p>{ill(tema(c), "ph-i", 220, 165)}
<h1>{c["h1"]}</h1>
<p class="lead">{c["lead"]}</p></header>"""

def calc_form(c):
    """Formulario .calc con inputs/selects."""
    inputs = "".join(
        f'<div><label for="{i["id"]}">{i["label"]}</label>'
        + (f'<select id="{i["id"]}">' + "".join(f'<option value="{o["v"]}">{o["t"]}</option>' for o in i["options"]) + "</select>"
           if i.get("type") == "select" else
           f'<input id="{i["id"]}" type="number" inputmode="decimal" value="{i["default"]}" min="{i.get("min",0)}" step="{i.get("step","any")}">')
        + "</div>" for i in c["inputs"])
    return f"""<div class="calc">
<form id="f" onsubmit="return false"><div class="grid">{inputs}</div><button id="go" type="button">Calcular con mis números</button></form>
<div class="result" id="r"></div>
</div>"""
