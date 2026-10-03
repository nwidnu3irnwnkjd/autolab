"""Páginas de dato persistentes /datos/<serie>/ (Constructor, E3 de ops/OPTIMIZACION.md). Solo stdlib.
Una URL por serie que se regenera en cada build desde data/live.json y data/params.json (el bot refresh.yml ya los actualiza):
sin tokens. dateModified = fecha del dato. Nada de memoria: si un dato no está con fuente en el repo, no se muestra.
Revertir: quitar `import datos` y el bloque datos.* de build.py (y 'datos' en directorio._section)."""
import html, json, os
from barometro import num, pct, fecha_es, mes_es
e = html.escape
INDEX = "/datos/"
PATHS = {"irav": "/datos/irav-ipc-alquiler/", "euribor": "/datos/euribor-hoy/", "luz": "/datos/precio-luz-hoy/"}
LIC = "https://creativecommons.org/licenses/by/4.0/deed.es"
A = lambda u, t: f'<a href="{e(u)}" rel="noopener">{e(t)}</a>'

def _live(live, k):
    d = (live or {}).get("datos", {}).get(k)
    return d if d and d.get("ok") else None

def _eur3(x): return num(x, 3) + " €/kWh"

def _build(live, params):
    """-> dict por serie con h1, title, description, fecha (dateModified), body, extra de JSON-LD; omite la serie si falta el dato."""
    out = {}
    r = params.get("renta_alquiler_2026")
    if r and r.get("irav_pct") is not None:
        out["irav"] = _irav(r)
    d = _live(live, "euribor12m")
    if d and d.get("extra", {}).get("serie_mensual"):
        out["euribor"] = _euribor(d)
    d = _live(live, "luz_pvpc")
    if d and d.get("extra", {}).get("hora_barata") is not None:
        out["luz"] = _luz(d)
    return out

def _cite(path, fecha, nombre):
    return (f'<h2 id="citar">Cómo citar</h2><p>«{e(nombre)}», Entre Muchos, <a href="{path}">entremuchos.com{path}</a>, dato del {fecha_es(fecha)}. '
            f'Licencia <a href="{LIC}" rel="noopener">CC BY 4.0</a> para la tabla y el texto; las cifras son de la fuente oficial citada. Si una cifra no coincide con la fuente, escríbenos desde <a href="/contacto/">contacto</a>.</p>')

def _more(path):
    o = [(p, t) for k, p, t in (("irav", PATHS["irav"], "IRAV e IPC del alquiler"), ("euribor", PATHS["euribor"], "Euríbor a 12 meses"), ("luz", PATHS["luz"], "Precio de la luz hoy")) if p != path]
    return '<p class="note">Más datos al día: ' + " · ".join(f'<a href="{p}">{t}</a>' for p, t in o) + f' · <a href="{INDEX}">todas las series</a> · <a href="/barometro/">Barómetro</a>.</p>'

def _irav(r):
    mes = mes_es(r["irav_periodo"] + "-01"); pub = r["irav_publicado"]
    irav, ipc = r["irav_pct"], r["ipc_pct"]
    h1 = f"IRAV de {mes}: {pct(irav)}"
    ej = round(800 * (1 + irav / 100), 2)
    rows = (f'<tr id="irav-{r["irav_periodo"]}"><th scope="row">IRAV, {mes}</th><td>{pct(irav)}</td><td>Publicado el {fecha_es(pub)}</td><td>{A(r["url_irav"], "INE, IRAV")}</td></tr>'
            f'<tr id="ipc-{r["irav_periodo"]}"><th scope="row">IPC, {mes} (índice definitivo, tasa anual)</th><td>{pct(ipc)}</td><td>Último definitivo publicado</td><td>{A(r["url_ipc"], "INE, IPC")}</td></tr>')
    body = f"""<article class="guide barometro tablas">
<p class="kicker"><a href="{INDEX}">Datos al día</a> · Alquiler</p>
<h1>{e(h1)}</h1>
<p class="byline note">Por Equipo de Entre Muchos · Dato publicado el <time datetime="{pub}">{fecha_es(pub)}</time> · Esta página se regenera con cada dato nuevo</p>
<p class="lead"><strong>Respuesta corta:</strong> el IRAV (Índice de Referencia para la Actualización de los Alquileres) de {mes} es del <strong>{pct(irav)}</strong> y el IPC de ese mes, <strong>{pct(ipc)}</strong> (índice definitivo), según el {A(r["url_irav"], "INE")}; el IRAV se publicó el {fecha_es(pub)}.</p>
<h2 id="datos">Último dato publicado</h2>
<div class="em-tw"><table><thead><tr><th scope="col">Índice</th><th scope="col">Valor</th><th scope="col">Publicación</th><th scope="col">Fuente</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Solo mostramos los meses de 2026 que hemos leído con fuente en el INE; cada mes nuevo se añadirá aquí con su fecha de publicación. El IRAV de septiembre se publica con el IPC de septiembre, a mediados de octubre de 2026. El avance del IPC de septiembre (4,9 %) se publicó el 29 de septiembre y no es el índice definitivo, así que no sirve para actualizar un alquiler.</p>
<h2 id="contrato">Cómo se aplica a tu contrato</h2>
<ul>
<li><strong>Contrato firmado desde el 26 de mayo de 2023:</strong> la actualización anual no puede superar el IRAV (disposición adicional 11.ª de la {A(r["url"], "Ley 29/1994")}, añadida por la Ley 12/2023, y {A(r["url_resolucion_irav"], "Resolución del INE")}), salvo que el contrato fije otro índice más bajo. Con el IRAV de {mes}, una renta de 800 € subiría como máximo a {num(ej, 2)} € al mes.</li>
<li><strong>Contrato anterior:</strong> la referencia sigue siendo la que pacte el contrato, y a falta de pacto, el IPC (art. 18 de la Ley 29/1994). Con el IPC de {mes}, 800 € serían {num(round(800 * (1 + ipc / 100), 2), 2)} € (importe de ejemplo, no oficial).</li>
<li>Una norma de urgencia (RDL 26/2026) fijó un tope del 2 % y estuvo en vigor solo del 1 al 2 de octubre de 2026; fue derogada ({A(r["url_derogacion"], "BOE-A-2026-20526")}). Hoy no hay tope del 2 %.</li>
<li>El índice que corresponde es el último publicado en la fecha de actualización de tu contrato. Confianza {e(r.get("confianza", ""))}: que el IRAV limite solo a los contratos firmados desde el 26/5/2023 se apoya en la ley y en el criterio del INE, sin sentencia que lo cierre; si tu caso es dudoso, consulta con un profesional.</li>
</ul>
<h2 id="calcula">Calcula tu actualización y entiende el resto del alquiler</h2>
<ul class="guides">
<li><a href="/decidir/actualizacion-renta-alquiler-irav-ipc/">Calculadora: actualización de la renta del alquiler con IRAV o IPC</a> <span class="note">tu renta, tu fecha de firma y el índice que toca</span></li>
<li><a href="/decidir/gastos-alquiler-quien-paga/">Gastos del alquiler: quién paga qué</a></li>
<li><a href="/decidir/fianza-y-garantias-adicionales-alquiler/">Fianza y garantías adicionales</a></li>
<li><a href="/guias/revisa-tu-contrato-de-alquiler-checklist/">Guía: revisa tu contrato de alquiler, lista de comprobación</a></li>
<li><a href="/guias/clausulas-contrato-alquiler/">Guía: cláusulas del contrato de alquiler</a></li>
</ul>
{_cite(PATHS["irav"], pub, h1)}
{_more(PATHS["irav"])}
<p class="disclaimer">Información orientativa, no constituye asesoramiento legal. Las cifras se leyeron en INEbase ({e(r["consulta"])}). Lee <a href="/como-funciona/">cómo trabajamos</a>.</p>
</article>"""
    desc = f"IRAV de {mes}: {pct(irav)}, e IPC definitivo {pct(ipc)}, con fuente del INE y fecha de publicación. Cómo se aplica a la actualización de tu alquiler."
    ds = dict(name=f"IRAV e IPC para actualizar el alquiler ({mes})", variables=["IRAV (%)", "IPC tasa anual (%)"], keywords=["IRAV", "IPC", "actualización alquiler", "INE"],
              based=[r["url_irav"], r["url_ipc"], r["url_resolucion_irav"]], cov=r["irav_periodo"])
    return dict(h1=h1, title=f"IRAV hoy: {pct(irav)} en {mes} y IPC del alquiler", description=desc, fecha=pub, body=body, ds=ds, nav="IRAV e IPC del alquiler", resumen=f"IRAV {mes}: {pct(irav)}")

def _euribor(d):
    x = d["extra"]; ser = x["serie_mensual"]; per = x["periodo"]; mes = mes_es(per + "-01"); v = d["valor"]; f = d["fecha_dato"]
    fu = d["fuente"]; prev = x.get("periodo_anterior"); h1 = f"Euríbor hoy: {pct(v, 3)} en {mes}"
    rows = ""; last = None
    for i, (m, val) in enumerate(reversed(ser)):
        old = ser[len(ser) - 2 - i][1] if len(ser) - 2 - i >= 0 else None
        dv = "" if old is None else f'{"+" if val - old >= 0 else "−"}{num(abs(val - old), 3)}'
        rows += f'<tr id="{m}"><th scope="row">{mes_es(m + "-01").capitalize()}</th><td>{num(val, 3)} %</td><td>{dv}</td></tr>'
    mx = max(ser, key=lambda t: t[1]); mn = min(ser, key=lambda t: t[1])
    var = f'; en {mes_es(prev + "-01")} fue del {pct(d["anterior"], 3)}, {num(abs(d["variacion_abs"]), 3).replace(".", ",")} puntos {"más" if d["variacion_abs"] >= 0 else "menos"}' if prev else ""
    body = f"""<article class="guide barometro tablas">
<p class="kicker"><a href="{INDEX}">Datos al día</a> · Hipoteca</p>
<h1>{e(h1)}</h1>
<p class="byline note">Por Equipo de Entre Muchos · Dato del <time datetime="{f}">{fecha_es(f)}</time> · Consultado el {fecha_es(d["fecha_consulta"])} · Esta página se regenera con cada dato nuevo</p>
<p class="lead"><strong>Respuesta corta:</strong> el Euríbor a 12 meses fue del <strong>{pct(v, 3)}</strong> de media en {mes}{e(var)} (dato del {fecha_es(f)}; fuente: {A(fu["url"], "Banco Central Europeo")}).</p>
<h2 id="historico">Histórico mensual del Euríbor a 12 meses</h2>
<div class="em-tw"><table><thead><tr><th scope="col">Mes</th><th scope="col">Media mensual</th><th scope="col">Variación (puntos)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Media mensual del Euríbor a 1 año, serie del BCE ({A(fu["url"], "Data Portal")}). En los últimos {len(ser)} meses el máximo fue {pct(mx[1], 3)} ({mes_es(mx[0] + "-01")}) y el mínimo {pct(mn[1], 3)} ({mes_es(mn[0] + "-01")}). Una hipoteca variable se revisa con el Euríbor de la media del mes que fije tu contrato (a menudo el penúltimo o el de dos meses antes), no con el del día.</p>
<h2 id="que-hacer">Qué hacer con este dato</h2>
<ul class="guides">
<li><a href="/decidir/hipoteca-fija-o-variable/">Hipoteca fija o variable: con tus números</a> <span class="note">con el Euríbor actual y el tipo fijo medio</span></li>
<li><a href="/barometro/#hipoteca">Barómetro Entre Muchos</a> <span class="note">Euríbor de equilibrio a partir del cual compensa la fija</span></li>
<li><a href="/decidir/amortizar-plazo-o-cuota/">Amortizar: ¿plazo o cuota?</a></li>
<li><a href="/guias/euribor-hipoteca/">Guía: qué es el Euríbor y cómo mueve tu hipoteca</a></li>
<li><a href="/hipoteca/">Mapa «Hipotecas»: decisiones en orden</a></li>
</ul>
{_cite(PATHS["euribor"], f, h1)}
{_more(PATHS["euribor"])}
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero. Lee <a href="/como-funciona/">cómo trabajamos</a>.</p>
</article>"""
    desc = f"Euríbor a 12 meses: {pct(v, 3)} de media en {mes} (BCE), con el histórico mensual de los últimos {len(ser)} meses y cómo afecta a tu hipoteca."
    ds = dict(name="Euríbor a 12 meses, media mensual", variables=["Euríbor 12 meses, media mensual (%)"], keywords=["Euríbor", "hipoteca variable", "BCE"], based=[fu["url"]], cov=f"{ser[0][0]}/{ser[-1][0]}")
    return dict(h1=h1, title=f"Euríbor hoy: {pct(v, 3)} ({mes}) e histórico", description=desc, fecha=f, body=body, ds=ds, nav="Euríbor a 12 meses", resumen=f"Euríbor {mes}: {pct(v, 3)}")

def _luz(d):
    x = d["extra"]; f = d["fecha_dato"]; v = d["valor"]; fu = d["fuente"]
    hb, hc = x["hora_barata"], x["hora_cara"]; pb, pc = x["precio_hora_barata"], x["precio_hora_cara"]
    hh = lambda h: f"{h:02d}:00 a {(h + 1) % 24:02d}:00"
    h1 = f"Precio de la luz hoy, {fecha_es(f)}: {_eur3(v)}"
    rows = ""
    for i, (dia, val) in enumerate(reversed(d.get("historial", []))):
        rows += f'<tr id="{dia}"><th scope="row">{fecha_es(dia)}</th><td>{_eur3(val)}</td></tr>'
    mm = f' La media de {mes_es(x["mes"] + "-01")} hasta hoy ({x["dias_mes"]} días) es de {_eur3(x["media_mes"])}.' if x.get("media_mes") is not None and x.get("mes") else ""
    body = f"""<article class="guide barometro tablas">
<p class="kicker"><a href="{INDEX}">Datos al día</a> · Energía</p>
<h1>{e(h1)}</h1>
<p class="byline note">Por Equipo de Entre Muchos · Dato del <time datetime="{f}">{fecha_es(f)}</time> · Consultado el {fecha_es(d["fecha_consulta"])} · Esta página se regenera cada día</p>
<p class="lead"><strong>Respuesta corta:</strong> el PVPC (tarifa regulada) del {fecha_es(f)} cuesta de media <strong>{_eur3(v)}</strong>; la hora más barata es de {hh(hb)} ({_eur3(pb)}) y la más cara, de {hh(hc)} ({_eur3(pc)}). Fuente: {A(fu["url"], "Red Eléctrica de España (REData)")}.</p>
<h2 id="hoy">El día, de un vistazo</h2>
<div class="em-tw"><table><thead><tr><th scope="col">Concepto</th><th scope="col">Precio</th><th scope="col">Hora</th></tr></thead><tbody>
<tr id="media"><th scope="row">Media de las 24 horas</th><td>{_eur3(v)}</td><td>Todo el día</td></tr>
<tr id="barata"><th scope="row">Hora más barata</th><td>{_eur3(pb)}</td><td>{hh(hb)}</td></tr>
<tr id="cara"><th scope="row">Hora más cara</th><td>{_eur3(pc)}</td><td>{hh(hc)}</td></tr>
</tbody></table></div>
<p class="note">Precio de la energía por hora en el mercado regulado (PVPC), media de las 24 horas, en €/kWh sin peajes, cargos ni impuestos: no es lo que pagas en la factura final.{e(mm)}</p>
<h2 id="dias">Media diaria reciente</h2>
<div class="em-tw"><table><thead><tr><th scope="col">Día</th><th scope="col">Media PVPC</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2 id="que-hacer">Qué hacer con este dato</h2>
<ul class="guides">
<li><a href="/decidir/luz-fija-o-indexada/">Luz: ¿tarifa fija o indexada?</a></li>
<li><a href="/decidir/horas-valle-luz-lavadora-termo-cuanto-ahorro/">Horas valle: cuánto ahorras con la lavadora y el termo</a></li>
<li><a href="/decidir/potencia-contratada-luz-bajar-compensa/">¿Compensa bajar la potencia contratada?</a></li>
<li><a href="/guias/cambio-de-hora-octubre-horas-valle-luz/">Guía: cambio de hora del 25 de octubre y horas valle</a></li>
<li><a href="/energia/">Mapa «Energía»: decisiones en orden</a></li>
</ul>
{_cite(PATHS["luz"], f, h1)}
{_more(PATHS["luz"])}
<p class="disclaimer">Información orientativa, no constituye asesoramiento. Lee <a href="/como-funciona/">cómo trabajamos</a>.</p>
</article>"""
    desc = f"PVPC del {fecha_es(f)}: media {_eur3(v)}, hora más barata {hh(hb)} y más cara {hh(hc)} (Red Eléctrica)."
    ds = dict(name="Precio de la luz PVPC por día (€/kWh)", variables=["PVPC media diaria (€/kWh)", "PVPC hora más barata (€/kWh)", "PVPC hora más cara (€/kWh)"], keywords=["precio luz hoy", "PVPC", "hora más barata"], based=[fu["url"]], cov=f)
    return dict(h1=h1, title=f"Precio de la luz hoy, {fecha_es(f)}: {_eur3(v)}", description=desc, fecha=f, body=body, ds=ds, nav="Precio de la luz hoy", resumen=f"PVPC {fecha_es(f)}: {_eur3(v)}")

def build(live, params):
    return _build(live, params)

def jsonld(k, S, base, pub, org, breadcrumbs):
    s = S[k]; ds = s["ds"]; url = base + PATHS[k]
    return [{"@context": "https://schema.org", "@type": "Dataset", "name": ds["name"], "description": s["description"], "url": url, "inLanguage": "es-ES",
             "isAccessibleForFree": True, "creator": org, "publisher": {"@id": base + "/#org"}, "dateModified": s["fecha"], "datePublished": pub,
             "temporalCoverage": ds["cov"], "spatialCoverage": {"@type": "Place", "name": "España"}, "keywords": ds["keywords"],
             "variableMeasured": ds["variables"], "license": LIC, "isBasedOn": ds["based"]},
            breadcrumbs(base, [("Inicio", "/"), ("Datos al día", INDEX), (s["nav"], None)])]

def index_page(S):
    lis = "".join(f'<li><a href="{PATHS[k]}"><strong>{e(s["h1"])}</strong></a><br><span class="note">{e(s["description"])}</span></li>' for k, s in S.items())
    return f"""<article class="guide tablas">
<p class="kicker">Datos al día</p>
<h1>Datos al día: IRAV, Euríbor y precio de la luz</h1>
<p class="lead">Una URL por dato, que se actualiza sola cada vez que hay una cifra nueva y siempre muestra la fecha y la fuente. Para las cifras fijas de 2026 (IRPF, autónomos, pensiones) mira las <a href="/tablas-2026/">Tablas 2026</a>; para el cruce de datos del mes, el <a href="/barometro/">Barómetro</a>.</p>
<ul class="guides">{lis}</ul>
<p class="disclaimer">Información orientativa. Lee <a href="/como-funciona/">cómo trabajamos</a>.</p>
</article>"""

def index_jsonld(S, base, mod, pub, org, breadcrumbs):
    return [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Datos al día", "url": base + INDEX, "inLanguage": "es-ES", "datePublished": pub, "dateModified": mod, "publisher": org,
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(S), "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["h1"], "url": base + PATHS[k]} for i, (k, s) in enumerate(S.items())]}},
            breadcrumbs(base, [("Inicio", "/"), ("Datos al día", None)])]

def hub_block(S, keys):
    li = "".join(f'<li><a href="{PATHS[k]}">{e(S[k]["nav"])}</a> <span class="note">{e(S[k]["resumen"])}, con fecha y fuente</span></li>' for k in keys if k in S)
    return li
