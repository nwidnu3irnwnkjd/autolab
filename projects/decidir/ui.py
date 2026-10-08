"""Interfaz del sitio (dueño: Diseñador): iconos, temas, tarjetas, catálogo, 404, cabecera y formulario de calculadora, head extra."""
import json, os, html, hashlib, re

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
# UX2.9: etiqueta visible (no cambia URL, tema, hub ni og) para las calculadoras laborales que caían en «Ahorro e inversión»
_LAB = ("paro", "subsidio", "despido", "finiquito", "baja-medica", "incapacidad", "jubila", "permiso", "viudedad", "excedencia", "nomina", "sueldo", "empleada-hogar", "aceptar-trabajo", "pagas-extra", "teletrabajo", "reduccion-jornada", "guarderia-cuidadora")
LAB_NAME = "Trabajo y prestaciones"
def etiqueta(c):
    t = tema(c)
    return LAB_NAME if t == "ahorro" and any(k in c["slug"] for k in _LAB) else ICONS[t][0]
def card(c):
    t = tema(c); name, svg = ICONS[t]
    k = c["slug"].replace("-", " ")  # el buscador usa textContent + data-k (antes data-q repetía título, descripción y tema: ~11 KB en la home)
    return f'<li data-k="{k}" data-t="{t}"><svg class="ill-s" viewBox="0 0 160 120" aria-hidden="true"><use href="/assets/illustrations.svg#{t}"/></svg><a href="/decidir/{c["slug"]}/">{c["h1"]}</a><p>{c["description"]}</p><span class="tag">{etiqueta(c)}</span></li>'

HOME_N = 6
def home_cards(calcs, n=HOME_N):
    """Home: n tarjetas destacadas (reparto por tema, orden estable) + enlace al catálogo; el resto se carga de /decidir/ al buscar o pulsar (home.js, data-more)."""
    by = {}
    for c in calcs: by.setdefault(tema(c), []).append(c)
    pick, i = [], 0
    while len(pick) < min(n, len(calcs)):
        for lst in by.values():
            if i < len(lst) and len(pick) < n: pick.append(lst[i])
        i += 1
    keep = {c["slug"] for c in pick}
    return "".join(card(c) for c in calcs if c["slug"] in keep)

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
        # UX1.4: GA4 solo en el dominio de producción (localhost/QA no cuentan). Sin gtag definido, los hooks `window.gtag&&` no hacen nada.
        # Modo básico (AEPD): gtag.js y config NO se cargan hasta que el usuario acepta (em_ck "1|AAAAMMDD", o "1" antiguo). Elección válida 24 meses.
        # Solo en entremuchos.com; en localhost con ?cookies=1 se ve el banner (sin gtag).
        host_js = ('var P=location.hostname==="entremuchos.com",L=location.hostname==="localhost"&&/[?&]cookies=1/.test(location.search),K="em_ck",v=null,r=null;try{r=localStorage.getItem(K)}catch(e){}'
                   'if(r){var q=r.split("|");if(q[0]==="1"||q[0]==="0"){v=q[0];if(/^\\d{8}$/.test(q[1]||"")){var t=q[1];if(new Date()-new Date(+t.slice(0,4),+t.slice(4,6)-1,+t.slice(6,8))>730*864e5)v=null}}}'
                   'function T(){var n=new Date();return n.getFullYear()*10000+(n.getMonth()+1)*100+n.getDate()}')
        gt = ('function G(){if(!P||window.gtag)return;window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};'
              'gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied"});gtag("consent","update",{analytics_storage:"granted"});'
              'gtag("js",new Date());gtag("config","' + g + '");var s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id=' + g + '";document.head.appendChild(s)}'
              'function X(){window["ga-disable-' + g + '"]=true;if(window.gtag){try{gtag("consent","update",{analytics_storage:"denied"})}catch(e){}window.gtag=null}'
              'var h=location.hostname.split("."),ds=[""],i,n,c=document.cookie.split(";"),j;for(i=0;i<h.length-1;i++){n=h.slice(i).join(".");ds.push(";domain="+n);ds.push(";domain=."+n)}'
              'for(j=0;j<c.length;j++){n=c[j].split("=")[0].trim();if(n==="_ga"||n.indexOf("_ga_")===0)for(i=0;i<ds.length;i++)document.cookie=n+"=;expires=Thu, 01 Jan 1970 00:00:00 GMT;max-age=0;path=/"+ds[i]}}'
              'if(v==="1")G();else if(v==="0")X();')
        bn = ('function B(){var d=document.getElementById("ckb");if(d)return;d=document.createElement("div");d.id="ckb";d.setAttribute("role","dialog");d.setAttribute("aria-label","Cookies");'
              'd.innerHTML=\'<p>Usamos Google Analytics para medir visitas, solo si aceptas. <a href="/cookies/">Más información</a></p><button type="button" data-v="1">Aceptar</button><button type="button" data-v="0">Rechazar</button>\';'
              'd.onclick=function(e){var b=e.target.closest("button");if(!b)return;try{localStorage.setItem(K,b.dataset.v+"|"+T())}catch(x){}'
              'if(b.dataset.v==="1")G();else X();d.remove()};document.body.appendChild(d)}'
              'var st=document.createElement("style");st.textContent="#ckb{position:fixed;left:0;right:0;bottom:0;z-index:99;display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;padding:10px 16px;background:#fff;color:#1a1d29;border-top:1px solid #c9ccd8;font:14px/1.4 system-ui,sans-serif}#ckb p{margin:0;flex:1 1 260px}#ckb a{color:inherit;text-decoration:underline}#ckb button{font:inherit;font-weight:600;padding:7px 16px;border-radius:8px;border:1px solid #1a1d29;background:transparent;color:inherit;cursor:pointer}@media (prefers-color-scheme:dark){#ckb{background:#161a26;color:#eceff7;border-color:#3a4054}#ckb button{border-color:#eceff7}}html:has(#ckb){scroll-padding-bottom:150px}body:has(#ckb){padding-bottom:140px}";document.head.appendChild(st);'
              'document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("[data-ck]");if(a&&(P||L)){e.preventDefault();B()}});'
              'document.addEventListener("DOMContentLoaded",function(){if((P||L)&&v!=="1"&&v!=="0")B()})')
        out.append('<script>(function(){' + host_js + gt + bn + '})()</script>')
    if site.get("adsense_client"):
        out.append(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={site["adsense_client"]}" crossorigin="anonymous"></script>')
    return "\n".join(out)

HUB_PATHS = {"hipoteca": "/hipoteca/", "coche": "/coche/", "energia": "/energia/", "impuestos": "/impuestos/", "ahorro": "/ahorro/"}  # hubs.HUBS (R16.1); resto de temas: ancla del catálogo

def calc_header(c):
    """Cabecera .ph de una calculadora."""
    return f"""<header class="ph ph-{tema(c)}"><p class="kicker"><a href="{HUB_PATHS.get(tema(c), "/decidir/#" + tema(c))}">{etiqueta(c)}</a></p>{ill(tema(c), "ph-i", 220, 165)}
<h1>{c["h1"]}</h1>
<p class="lead">{c["lead"]}</p></header>"""

def split_label(lab):
    """Etiqueta corta (con la unidad) + texto de ayuda. Solo si la etiqueta supera 45 caracteres."""
    if len(lab) <= 45: return lab, ""
    m = re.match(r"^(.*?) \((.*)\)(.*)$", lab)
    if m:
        base, inner, tail = m.group(1), m.group(2), m.group(3)
        p = re.split(r"\s*[;,]\s*", inner, 1)
        if len(p[0]) <= 12: short, rest = f"{base} ({p[0]}){tail}", (p[1] if len(p) > 1 else "")
        else: short, rest = base + tail, inner
    elif "; " in lab: short, rest = lab.split("; ", 1)
    else: return lab, ""
    rest = rest.strip()
    return short, (rest[:1].upper() + rest[1:] if rest else "")

def calc_form(c):
    """Formulario .calc con inputs/selects. Los numéricos son type=text inputmode=decimal data-n: em.js acepta coma decimal y puntos de miles."""
    def one(i):
        short, hint = split_label(i["label"])
        h = f'<small class="hint" id="h-{i["id"]}">{hint}</small>' if hint else ""
        d = f' aria-describedby="h-{i["id"]}"' if hint else ""
        return (f'<div><label for="{i["id"]}">{short}</label>{h}'
            + (f'<select id="{i["id"]}"{d}>' + "".join(f'<option value="{o["v"]}">{o["t"]}</option>' for o in i["options"]) + "</select>"
               if i.get("type") == "select" else
               f'<input id="{i["id"]}" type="text" inputmode="decimal" autocomplete="off" data-n{" data-dec" if float(i.get("step",1) or 1) < 1 else ""} value="{i["default"]}" min="{i.get("min",0)}"' + f'{d}>')
            + "</div>")
    inputs = "".join(one(i) for i in c["inputs"])
    return f"""<div class="calc">
<form id="f" onsubmit="return false"><div class="grid">{inputs}</div><button id="go" type="button">Calcular con mis números</button></form>
<div class="result" id="r"></div>
</div>"""


_NUMC = re.compile(r"^[\s<>/a-z]*[-+~≈]?\s*\d[\d.,\s]*(?:%|€|\s*(?:€|%|años?|meses|días|h|km|kg|l|m2|m²|kWh)\b)?[^a-záéíóúñ]*$", re.I)
def mark_num(h):
    """Tablas: marca `.n` (texto a la derecha) en las columnas cuyas celdas son todas cifras; el resto queda a la izquierda."""
    def tb(m):
        t = m.group(0); rows = re.findall(r"<tr>(.*?)</tr>", t, re.S)
        if not rows: return t
        cells = [re.findall(r"<(t[dh])([^>]*)>(.*?)</t[dh]>", r, re.S) for r in rows]
        ncol = max(len(c) for c in cells); num = set()
        for j in range(ncol):
            vals = [re.sub(r"<[^>]+>", "", c[j][2]).strip() for c in cells if len(c) > j and c[j][0] == "td"]
            if vals and all(_NUMC.match(v) for v in vals if v): num.add(j)
        out = []
        for c, r in zip(cells, rows):
            k = [0]
            def cell(mm):
                j = k[0]; k[0] += 1
                if j in num and (mm.group(1) == "td" or j > 0): return f'<{mm.group(1)}{mm.group(2)} class="n">'
                return mm.group(0)
            out.append(re.sub(r"<(t[dh])([^>]*)>", cell, r))
        for r, o in zip(rows, out): t = t.replace(r, o, 1)
        return t
    return re.sub(r"<table.*?</table>", tb, h, flags=re.S)
