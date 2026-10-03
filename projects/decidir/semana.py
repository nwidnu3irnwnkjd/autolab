"""«Esta semana» (home y /actualidad/) y «Qué cambia el 1 de enero de 2027» (Estratega, c51, PLAN-TRAFICO D). Solo stdlib.
Todo sale de ficheros con fuente: data/live.json (luz, carburantes, Euríbor), data/events.json (eventos con "plazo": true),
journal/vigencias.md (sección «## Novedades normativas», opcional) y data/params.json (cifras 2026). Nada de 2027 se inventa:
data/cambios2027.json solo recibe una fila cuando la norma está publicada (valor + fuente). Revertir: quitar las llamadas
a semana.* en build.py y directorio.py."""
import json, os, re, html, datetime
import seo, noticias

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH2027 = "/que-cambia-1-enero-2027/"
H2027 = "Qué cambia el 1 de enero de 2027: SMI, IPREM y pensiones"
D2027 = "Cifras de 2026 con fuente y estado de las normas de 2027 (SMI, IPREM, pensiones, cotización, autónomos, IRPF): qué es firme y qué falta."
VIGENCIAS = os.path.join(ROOT, "../../journal/vigencias.md")
e = html.escape
STALE = 7  # días; por encima el dato no se presenta como actual: «dato de <fecha>»

def _fe(iso): return seo._fmt_fecha(iso)

# ---------------- ESTA SEMANA ----------------
def _novedad(path=VIGENCIAS):
    """Última línea de «## Novedades normativas» con formato «- **AAAA-MM-DD** · texto · https://url». None si no hay."""
    try: txt = open(path).read()
    except OSError: return None
    m = re.search(r"^## Novedades normativas\s*\n(.*?)(?=^## |\Z)", txt, re.S | re.M)
    if not m: return None
    best = None
    for ln in m.group(1).splitlines():
        r = re.match(r"-\s+\*\*(\d{4}-\d{2}-\d{2})\*\*\s+·\s+(.+?)\s+·\s+(https://\S+)", ln.strip())
        if r and (best is None or r.group(1) > best[0]): best = r.groups()
    return dict(fecha=best[0], texto=best[1], url=best[2]) if best else None

def _proximo_plazo(today, events):
    best = None
    for ev in events:
        if not ev.get("plazo") or ev.get("tipo") != "fechas": continue
        for f in ev["fechas"]:
            d = datetime.date.fromisoformat(f)
            if d >= today and (best is None or d < best[0]): best = (d, ev)
    return best

def cards(live=None, today=None, events=None, vig=None, sin_noticia=False):
    """Lista de tarjetas {id, titulo, valor, unidad, texto, fecha, fuente:{nombre,url}, calc, etiqueta}. Solo datos usables."""
    today = today or datetime.date.today()
    live = live if live is not None else seo.load_live()
    D = live.get("datos", {}) if live else {}
    out = []
    def stale(f): return (today - datetime.date.fromisoformat(f)).days > STALE
    luz = D.get("luz_pvpc")
    if seo._fresh(luz, today):
        x = luz["extra"]
        out.append(dict(id="luz", titulo="Luz (PVPC)", valor=seo._eur(luz["valor"], 3), unidad="€/kWh de media del día", delta=seo._pulso_delta("luz", luz),
                        texto=f"Más barata a las {x['hora_barata']}-{(x['hora_barata'] + 1) % 24} h ({seo._eur(x['precio_hora_barata'], 3)} €/kWh) y más cara a las {x['hora_cara']}-{(x['hora_cara'] + 1) % 24} h ({seo._eur(x['precio_hora_cara'], 3)} €/kWh).",
                        fecha=luz["fecha_dato"], fuente=luz["fuente"], calc="luz-fija-o-indexada"))
    for key, tit, lab in (("gasolina95", "Gasolina 95", "gasolina"), ("diesel", "Diésel", "diésel")):
        d = D.get(key)
        if seo._fresh(d, today):
            out.append(dict(id=key, titulo=tit, valor=seo._eur(d["valor"], 3), unidad="€/l de media", delta=seo._pulso_delta("carburantes", d),
                            texto=f"Media de las estaciones de servicio de la Península y Baleares.", fecha=d["fecha_dato"], fuente=d["fuente"], calc="diesel-gasolina-hibrido-electrico"))
    eu = D.get("euribor12m")
    if seo._fresh(eu, today):
        out.append(dict(id="euribor", titulo="Euríbor 12 meses", valor=seo._eur(eu["valor"], 3), unidad="% de media en " + seo._mes(eu["extra"]["periodo"]), delta=seo._pulso_delta("euribor", eu),
                        texto="Último dato mensual publicado por el BCE: es el que mueve la revisión de una hipoteca variable.", fecha=eu["fecha_dato"], fuente=eu["fuente"], calc="hipoteca-fija-o-variable"))
    ev = seo.load_events() if events is None else events
    pl = _proximo_plazo(today, ev)
    if pl:
        d, evn = pl; n = (d - today).days
        cuando = "hoy" if n == 0 else ("mañana" if n == 1 else f"faltan {n} días")
        out.append(dict(id="plazo", titulo="Próximo plazo", valor=seo._fmt_fecha(d.isoformat()).rsplit(" de ", 1)[0], unidad=cuando,
                        texto=evn["titulo"] + ".", fecha=None, fuente=evn["fuente"], calc=evn["calc"], dia=d.isoformat()))
    nov = _novedad() if vig is None else vig
    nf = noticias.featured(noticias.load(today), today)  # tarjeta «Lo que importa hoy» / «Última hora»: enlaza a la pieza, no al BOE
    if nf:
        lab, nn = nf; pf = noticias.principal(nn) or {"nombre": "Entre Muchos", "url": "/noticias/"}
        if not sin_noticia: out.insert(0, dict(id="noticia", titulo=lab, valor="", unidad="", texto=nn["h1"], fecha=nn["published"], fuente=pf, calc=None, href=nn["path"]))
        if nov and nn.get("tipo") == "alerta" and nn["published"] >= nov["fecha"]: nov = None  # la pieza sustituye a la línea del Vigilante
    if nov:
        out.append(dict(id="novedad", titulo="Novedad normativa", valor="", unidad="", texto=nov["texto"], fecha=nov["fecha"], fuente=dict(nombre="BOE", url=nov["url"]), calc=None))
    for c in out: c["viejo"] = bool(c["fecha"]) and stale(c["fecha"])
    return out

ICON = dict(seo.PULSO_ICON, plazo='<path d="M8 2v4M16 2v4M3 9h18M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/>',
            novedad='<path d="M6 2h9l5 5v15H6zM14 2v6h6M9 13h8M9 17h8"/>')
ICON["gasolina95"] = ICON["diesel"] = ICON["carburantes"]

def _li(c, names):
    f = c["fecha"]
    if f is None: meta = f'Fecha oficial: <time datetime="{c["dia"]}">{_fe(c["dia"])}</time>.'
    elif c["viejo"]: meta = f'<span class="sem-old">Dato de <time datetime="{f}">{_fe(f)}</time></span> (no es de esta semana).'
    else: meta = f'Actualizado: <time datetime="{f}">{_fe(f)}</time>.'
    link = f'<a href="/decidir/{c["calc"]}/">{e(names.get(c["calc"], "Calcula tu caso"))}</a>' if c.get("calc") else ""
    if c.get("href"): link = f'<a href="{c["href"]}">Leer la noticia</a> · <a href="{noticias.PATH}">Todas las noticias</a>'
    val = f'<span class="pk-v">{c["valor"]} <small>{e(c["unidad"])}</small></span>{c.get("delta", "")}' if c["valor"] else ""
    return (f'<li class="pk pk-{c["id"]}{" pk-old" if c["viejo"] else ""}"><span class="pk-h"><svg class="pk-i" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON.get(c["id"], ICON["novedad"])}</svg><strong>{e(c["titulo"])}</strong></span>'
            f'{val}<span class="pk-t">{e(c["texto"])}</span>'
            f'<span class="pulso-meta">{meta} Fuente: <a href="{c["fuente"]["url"]}" rel="noopener">{e(c["fuente"]["nombre"])}</a>.</span>'
            + (f'<span class="pk-l">{link}</span>' if link else "") + '</li>')

def block(live=None, today=None, events=None, vig=None, names=None, sin_noticia=False):
    """Bloque «Esta semana» (home y /actualidad/). '' si no hay ningún dato utilizable."""
    cs = cards(live, today, events, vig, sin_noticia)
    if not cs: return ""
    names = names or NAMES
    return ('<aside class="pulso semana box" aria-label="Esta semana"><h2>Esta semana</h2><ul>' + "".join(_li(c, names) for c in cs)
            + f'</ul><span class="pulso-meta">Se actualiza cada día con datos oficiales. Próxima gran fecha: <a href="{PATH2027}">qué cambia el 1 de enero de 2027</a> · <a href="/calendario/">calendario</a>.</span></aside>\n')

NAMES = {"luz-fija-o-indexada": "Luz fija o indexada", "diesel-gasolina-hibrido-electrico": "Diésel, gasolina o eléctrico",
         "hipoteca-fija-o-variable": "Hipoteca fija o variable", "cuota-autonomos-ingresos-reales-regularizacion": "Cuota de autónomo por ingresos reales",
         "compensar-perdidas-ganancias-irpf-antes-fin-de-ano": "Vender con pérdidas antes de fin de año"}

def fecha_live(live=None, today=None):
    """Fecha de dato más reciente de las tarjetas con dato (para lastmod)."""
    ds = [c["fecha"] for c in cards(live, today) if c["fecha"]]
    return max(ds) if ds else ""

# ---------------- QUÉ CAMBIA EL 1 DE ENERO DE 2027 ----------------
def _p2027():
    try: return json.load(open(os.path.join(ROOT, "data/cambios2027.json"))).get("publicadas", {})
    except Exception: return {}

def _ef(x): return seo._eur(x, 0 if float(x).is_integer() else 2) + " €"
def _pc(x): return seo._eur(x, 2).rstrip("0").rstrip(",") + " %"

def filas(P):
    """Filas {id, concepto, v26, fuente26, url26, conf, norma, calc}. Cifras 2026 solo de params.json (A/B)."""
    S, J, Pa, Vi, A, Cp, Mf, Rf = (P[k] for k in ("smi_2026", "jubilacion_2026", "cuanto_cobro_paro_2026", "viudedad_2026", "autonomo_2026", "capitalizar_paro_2026", "maternidad_familia_2026", "retribucion_flexible_2026"))
    g = A["general"]
    return [
        dict(id="smi", concepto="Salario mínimo (SMI)", v26=f'{_ef(S["mensual_14_pagas"])} al mes en 14 pagas ({_ef(S["anual"])} al año)', fuente=S["fuente"], url=S["url"], conf=S["confianza"],
             norma="Se fija por real decreto del Gobierno y suele aprobarse a lo largo del invierno. El de 2026 se publicó en el BOE del 19 de febrero de 2026; no hay fecha ni cifra para 2027.", calc="comparar-ofertas-de-trabajo-neto-real"),
        dict(id="iprem", concepto="IPREM (referencia del paro y de ayudas)", v26=f'{_ef(Pa["iprem_mensual"])} al mes (prorrogado; con 1/6: {_ef(Pa["iprem_mas_sexta"])})', fuente="SEPE, cuantías 2026", url=Pa["url_sepe_cuantias"], conf=Pa["confianza"],
             norma="Lo fija la Ley de Presupuestos; sin Presupuestos se prorroga el anterior, como en 2026 (Ley 31/2022). Sin norma de 2027 publicada.", calc="cuanto-cobro-de-paro-prestacion-desempleo"),
        dict(id="pension-max", concepto="Pensión máxima de jubilación", v26=f'{_ef(J["max_mes"])} al mes en 14 pagas ({_ef(J["max_anual"])} al año)', fuente="Real Decreto 241/2026", url=J["url_rd"], conf=J["confianza"],
             norma="Se actualiza con la norma de revalorización de pensiones (Presupuestos o real decreto). La de 2026 llegó ya entrado el año; la de 2027 no está publicada.", calc="jubilacion-anticipada-o-demorada"),
        dict(id="pension-min", concepto="Pensiones mínimas (jubilación 65 años sin cónyuge) y revalorización", v26=f'{_ef(J["minima_jubilacion_65_sin_conyuge_unipersonal"])} al año; revalorización 2026: {_pc(J["revalorizacion_2026_pct"])}', fuente="Real Decreto 241/2026", url=J["url_rd"], conf=J["confianza"],
             norma="Misma norma de revalorización que la pensión máxima. Sin cifra de 2027 publicada.", calc="pension-viudedad-cuanto-cobro"),
        dict(id="bases", concepto="Base máxima y tipos de cotización del trabajador", v26=f'Base máxima {_ef(g["base_max_mes"])} al mes; trabajador {_pc(g["trabajador_indefinido_pct"])} y empresa {_pc(g["empresa_indefinido_pct"])} (indefinido, sin AT/EP)', fuente="Orden PJC/297/2026", url=A["url"], conf=A["confianza"],
             norma="Orden ministerial anual de cotización. La de 2026 se publicó ya entrado el año; la de 2027 no está publicada.", calc="retencion-irpf-nomina-subir-o-no"),
        dict(id="mei", concepto="Mecanismo de Equidad Intergeneracional (MEI)", v26="0,15 % trabajador y 0,75 % empresa; 0,90 % en autónomos", fuente="Orden PJC/297/2026", url=A["url"], conf=A["confianza"],
             norma="Su tipo para 2027 se fijará en la Orden de cotización de 2027, aún sin publicar (por confirmar).", calc="cuota-autonomos-ingresos-reales-regularizacion"),
        dict(id="autonomos", concepto="Cuota de autónomos (tramo 1, sin tarifa plana)", v26=f'{_ef(Cp["cuota_minima_mensual"])} al mes; tipo total {_pc(A["reta"]["tipo_total"])}', fuente="Orden PJC/297/2026 y RDL 3/2026", url=A["url"], conf=A["confianza"],
             norma="La tabla de tramos posterior a 2025 la tiene que fijar el Gobierno; la de 2026 repite la de 2025 mientras no haya Presupuestos (RDL 3/2026). Sin tabla de 2027.", calc="cuota-autonomos-ingresos-reales-regularizacion"),
        dict(id="plana", concepto="Tarifa plana de autónomos", v26="Sin cifra verificada en fuente oficial (la Ley 20/2007, art. 38 ter, remite a la Ley de Presupuestos): no la usamos", fuente="Ley 20/2007 (Estatuto del Trabajo Autónomo)", url="https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409", conf="sin verificar",
             norma="Depende de la Ley de Presupuestos. Por confirmar.", calc="cuota-autonomos-ingresos-reales-regularizacion"),
        dict(id="irpf", concepto="Deducciones del IRPF por hijos (maternidad y familia numerosa) y mínimo personal", v26=f'Maternidad {_ef(Mf["maternidad_anual"])} al año; familia numerosa {_ef(Mf["familia_base_anual"])}; mínimo del contribuyente {_ef(P["irpf_2026"]["minimo_estatal"]["contribuyente"])}', fuente="Ley 35/2006 del IRPF", url=Mf["url"], conf=Mf["confianza"],
             norma="Solo cambian si una ley las modifica; no hay ninguna modificación publicada para 2027 a 2 de octubre de 2026. El Real Decreto-ley 26/2026 fue derogado el 2 de octubre de 2026 (BOE-A-2026-20526) y no cambia estas cifras.", calc="deduccion-maternidad-familia-numerosa"),
        dict(id="flex", concepto="Retribución flexible: límites exentos", v26=f'Seguro de salud {_ef(Rf["seguro_persona"])} por persona; comida {_ef(Rf["comida_dia"])} al día; transporte {_ef(Rf["transporte_anual"])} al año; guardería hasta {_ef(Rf["maternidad_guarderia_max"])}', fuente="Ley 35/2006 y Reglamento del IRPF", url=Rf["url"], conf=Rf["confianza"],
             norma="Los límites están en el Reglamento del IRPF y la Ley; solo cambian si se modifican. Las empresas abren la elección para enero a finales de año: decide con las cifras vigentes.", calc="retribucion-flexible-me-conviene"),
    ]

FAQ = [
    ("¿Cuánto será el SMI en 2027?", "Todavía no se sabe: no hay real decreto publicado. El de 2026 es de 1.221 € al mes en 14 pagas (Real Decreto 126/2026) y es el que usan las calculadoras hasta que se publique el nuevo."),
    ("¿Se actualiza el IPREM el 1 de enero?", "Solo si una norma lo fija. En 2026 sigue el IPREM prorrogado (600 € al mes) por falta de Presupuestos nuevos; para 2027 no hay norma publicada."),
    ("¿Suben las pensiones en 2027?", "No hay norma de revalorización de 2027 publicada. La de 2026 fue del 2,7 % (Real Decreto 241/2026) y se aprobó ya entrado el año."),
    ("¿Cambia la cuota de autónomos en 2027?", "La tabla de 2027 no está publicada. La de 2026 repite la de 2025 mientras no haya Presupuestos (RDL 3/2026); la tarifa plana de 2026 no la hemos podido verificar en una fuente oficial."),
    ("¿Cuándo se actualiza esta página?", "Cada vez que se publica una norma de 2027: la fila pasa de «pendiente de norma» a «publicada», con la cifra y su fuente. Hasta entonces, las calculadoras usan las cifras de 2026."),
]

def cambios_page(P, calcs, card, modified, author):
    """-> (body, [JSON-LD sin Article/Breadcrumb]) de PATH2027. Una fila pasa a «publicada» solo desde data/cambios2027.json."""
    pub = _p2027(); by = {c["slug"]: c for c in calcs}
    fs = filas(P); rows = []
    for r in fs:
        p = pub.get(r["id"])
        if p: est = f'<strong>Publicada</strong>: {e(p["valor"])} <span class="note">({e(p["fuente"])}, <a href="{p["url"]}" rel="noopener">BOE</a>)</span>'
        else: est = '<span class="pulso-meta">Pendiente de norma · por confirmar</span>'
        rows.append(f'<tr><th scope="row">{e(r["concepto"])}<br><span class="note">{e(r["norma"])}</span></th>'
                    f'<td>{e(r["v26"])}<br><span class="note"><a href="{r["url"]}" rel="noopener">{e(r["fuente"])}</a> · confianza {e(r["conf"])}</span></td><td>{est}</td></tr>')
    npub = sum(1 for r in fs if r["id"] in pub)
    rel = [by[r["calc"]] for r in fs if r["calc"] in by]; seen = set(); rel = [c for c in rel if not (c["slug"] in seen or seen.add(c["slug"]))]
    faq = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
    body = f"""<article class="guide tablas">
<p class="kicker"><a href="/tablas-2026/">Tablas 2026</a> · Qué viene en 2027</p>
<h1>Qué cambia el 1 de enero de 2027</h1>
<p class="byline note">Por {author} · Revisado el <time datetime="{P['irpf_2026']['consultado']}">{seo.fecha_es(P['irpf_2026']['consultado'])}</time> · Página actualizada el <time datetime="{modified}">{seo.fecha_es(modified)}</time></p>
<div class="box"><p><strong>Respuesta corta:</strong> a día de hoy, <strong>{npub} de {len(fs)}</strong> cifras de 2027 están publicadas. El resto sigue por confirmar: no damos fecha ni cifra hasta que exista la norma. Mientras tanto, las calculadoras usan las cifras de 2026 de la tabla, y esta página se actualiza sola cuando se publique cada una.</p></div>
<h2>Cifras de 2026 y estado de las de 2027</h2>
<div class="em-tw"><table><thead><tr><th scope="col">Concepto y cuándo suele publicarse</th><th scope="col">Cifra 2026 (fuente y confianza)</th><th scope="col">2027</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="note">Confianza A: leída en el texto oficial del BOE o del organismo; B: oficial con algún supuesto de modelo. Todas las cifras de 2026 son las de <a href="/tablas-2026/">Tablas 2026</a> y las que usan las calculadoras.</p>
<h2>Cuándo suele publicarse cada norma</h2>
<ul>
<li><strong>SMI:</strong> real decreto del Gobierno, que suele aprobarse a lo largo del invierno; el de 2026 salió en el BOE del 19 de febrero de 2026.</li>
<li><strong>IPREM y pensiones:</strong> Presupuestos o un real decreto-ley de revalorización, normalmente a final de año; en 2026 la revalorización de pensiones se aprobó ya entrado el año (Real Decreto 241/2026) y el IPREM se prorrogó.</li>
<li><strong>Bases y tipos de cotización (incluido el MEI):</strong> una orden ministerial anual; la de 2026 es la Orden PJC/297/2026.</li>
<li><strong>Cuota de autónomos y tarifa plana:</strong> las fija el Gobierno o la Ley de Presupuestos.</li>
</ul>
<p>Son pautas de otros años, no un calendario: cualquiera de estas normas puede retrasarse. Seguimos el <a href="/calendario/">Calendario de decisiones</a> y lo marcamos aquí en cuanto se publique.</p>
<h2>Qué puedes hacer ya</h2>
<p>Calcula con las cifras de 2026 y repite el cálculo cuando salga la norma. Calculadoras que se verán afectadas:</p>
<ul class="cards">{"".join(card(c) for c in rel)}</ul>
<h2>Preguntas frecuentes</h2>
{faq}
<p class="disclaimer">Información orientativa, no constituye asesoramiento fiscal, laboral ni financiero. Lee <a href="/como-funciona/">cómo trabajamos</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
          {"@context": "https://schema.org", "@type": "Table", "about": "Cifras de 2026 y estado de las de 2027 (SMI, IPREM, pensiones, cotización, autónomos, IRPF)", "inLanguage": "es-ES", "dateModified": modified}]
    return body, ld

FILES = ["semana.py", "data/params.json", "data/cambios2027.json"]
