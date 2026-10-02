"""Hubs temáticos (dueño: Estratega SEO/GEO). Una página-mapa por tema, en orden de decisión, con datos vivos fechados.
Reutilizable: añade una entrada a HUBS (y nada más) cuando el tema cumpla el disparador: >= MIN_PAGES páginas propias
(calculadoras del tema + guías que enlazan a ellas). build.main llama a hubs.eligible()/page() sin conocer el tema.
Texto: solo cifras de data/live.json (marcadores {{...}}), del Barómetro o de la propia calculadora; nunca de memoria."""
import json, os, html
import seo, calcs_loader

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_PAGES = 6
AUTHOR = seo.AUTHOR

HUBS = {
    "hipoteca": {
        "path": "/hipoteca/",
        "tema": "hipoteca",
        "title": "Calculadoras de hipoteca: decide con tus números",
        "h1": "Hipotecas: decide con tus números",
        "description": "Del ahorro a la amortización: las calculadoras de hipoteca en orden de decisión, con el Euríbor y el tipo fijo medio del BCE de este mes.",
        "kicker": "Tema · Hipoteca y vivienda",
        "nav": "Hipotecas",
        "all_title": "Todas las calculadoras de hipoteca",
        "baro": ("/barometro/#hipoteca", 0, "Cifras propias de cada mes con su fecha: Euríbor de equilibrio, coste por km y rentabilidad para invertir antes que amortizar."),
        "fechas": ["fecha_tipo_fijo", "fecha_euribor"],
        "disclaimer": "Información orientativa, no constituye asesoramiento financiero ni legal. Los datos de mercado proceden del Banco Central Europeo y se actualizan con cada dato nuevo; las condiciones de tu hipoteca están en tu escritura.",
        "lead": ("<strong>Respuesta corta:</strong> una hipoteca se decide en seis pasos y el orden importa: cuánto ahorrar, alquilar o comprar, fija o variable, "
                 "cambiarla de banco, amortizar plazo o cuota y amortizar o invertir. Hoy el Euríbor a 12 meses está en el {{euribor_12m}} % "
                 "(media de {{periodo_euribor_es}}) y las hipotecas fijas nuevas a más de 10 años se firman de media al {{tipo_fijo}} % ({{periodo_tipo_fijo_es}}); fuente: BCE."),
        "groups": [
            ("Antes de firmar", ["cuanto-ahorrar-para-comprar-casa", "alquilar-o-comprar", "hipoteca-fija-o-variable"]),
            ("Con la hipoteca ya firmada", ["subrogar-hipoteca-merece-la-pena", "amortizar-plazo-o-cuota", "amortizar-o-invertir"]),
        ],
        "steps": {
            "cuanto-ahorrar-para-comprar-casa": {
                "name": "Cuánto dinero necesitas",
                "text": "Antes de mirar pisos, calcula el efectivo que hace falta de verdad: la entrada, los impuestos (ITP en vivienda usada; IVA y AJD en nueva) y los gastos de notaría, registro, gestoría y tasación. Es la cifra que te dice si puedes empezar ya o te conviene esperar.",
            },
            "alquilar-o-comprar": {
                "name": "Alquilar o comprar",
                "text": "Comprar no gana siempre: depende de cuántos años te vas a quedar, de cuánto suba la vivienda y de lo que harías con el dinero de la entrada. La calculadora compara el patrimonio de cada opción y dice en qué año compensa comprar.",
            },
            "hipoteca-fija-o-variable": {
                "name": "Fija o variable",
                "text": "La variable paga Euríbor más un diferencial; la fija protege la cuota a cambio de un tipo inicial mayor. La clave es el Euríbor medio a partir del cual la fija te sale más barata.",
                "datos": "{{baro}}",
                "fecha": ("fecha_euribor", "Euríbor"),
                "guia": "euribor-hipoteca",
            },
            "subrogar-hipoteca-merece-la-pena": {
                "name": "Cambiar la hipoteca de banco o a fija",
                "text": "Si ya tienes hipoteca, compara su tipo con lo que se ofrece hoy: el tipo fijo medio de las hipotecas nuevas es del {{tipo_fijo}} % ({{periodo_tipo_fijo_es}}, BCE). Cambiar compensa si el ahorro supera la comisión y los gastos del cambio antes de que acabes el préstamo.",
            },
            "amortizar-plazo-o-cuota": {
                "name": "Amortizar: plazo o cuota",
                "text": "Con la misma cantidad, reducir plazo ahorra más intereses; reducir cuota solo compensa si necesitas respirar cada mes. Antes de pagar, mira qué comisión máxima te puede cobrar el banco.",
                "guia": "amortizacion-anticipada-comisiones",
            },
            "amortizar-o-invertir": {
                "name": "Amortizar o invertir",
                "text": "Amortizar equivale a invertir sin riesgo al tipo de tu hipoteca. Solo compensa invertir si esperas una rentabilidad neta claramente mayor y aceptas que no llegue.",
            },
        },
    },
    "coche": {
        "path": "/coche/",
        "tema": "coche",
        "title": "Calculadoras de coche: cuánto cuesta y qué te conviene",
        "h1": "Coche: decide con tus números",
        "description": "Si necesitas coche, cuál, con qué motor, comprar o renting y qué seguro: las calculadoras en orden, con el precio de los carburantes de hoy (MITECO).",
        "kicker": "Tema · Coche y movilidad",
        "nav": "Coche",
        "all_title": "Todas las calculadoras de coche y movilidad",
        "baro": ("/barometro/#coche", 1, "Cada mes, el coste por km de diésel, gasolina, híbrido y eléctrico con los precios del día y su fecha."),
        "fechas": ["fecha_carburantes"],
        "disclaimer": "Información orientativa, no constituye asesoramiento financiero. Los precios de los carburantes son una media simple de las gasolineras de Península y Baleares publicada por el Ministerio para la Transición Ecológica (MITECO); tu gasolinera, tu consumo y las condiciones de tu oferta mandan.",
        "lead": ("<strong>Respuesta corta:</strong> el coche se decide de lo general a lo concreto: primero si lo necesitas para tus trayectos, después cuál (nuevo o seminuevo, y con qué motor), "
                 "cómo pagarlo (comprar o renting) y qué seguro. El combustible es solo una parte del coste: la depreciación, el seguro y la financiación pesan aunque el coche esté parado. "
                 "Hoy la gasolina 95 cuesta {{gasolina}} €/l y el diésel {{diesel}} €/l de media ({{fecha_carburantes_es}}; fuente: MITECO)."),
        "groups": [
            ("¿Necesitas coche?", ["coche-propio-o-carsharing-o-vtc", "bici-electrica-o-transporte-publico", "tren-avion-o-coche"]),
            ("Si vas a tener coche", ["coche-nuevo-o-seminuevo", "diesel-gasolina-hibrido-electrico", "comprar-coche-o-renting", "seguro-todo-riesgo-o-terceros"]),
        ],
        "steps": {
            "coche-propio-o-carsharing-o-vtc": {
                "name": "Coche propio, carsharing o taxi/VTC",
                "text": "Tener coche tiene costes fijos que pagas aunque no lo uses. La calculadora te da los kilómetros al año a partir de los cuales compensa tenerlo; por debajo, sale más barato el carsharing o el taxi/VTC con tus tarifas.",
            },
            "bici-electrica-o-transporte-publico": {
                "name": "Para ir a trabajar: bici eléctrica, abono o coche",
                "text": "Para los trayectos diarios, compara el coste anual de la bici eléctrica, el abono de transporte y el coche, y en cuántos años se amortiza la bici con tus kilómetros.",
            },
            "tren-avion-o-coche": {
                "name": "Para viajar: tren, avión o coche",
                "text": "En un viaje largo el coche cuesta lo mismo vayas solo o acompañado, y los billetes se multiplican por viajero. La calculadora te dice con cuántos viajeros gana el coche y cuánto tiene que valer tu hora para que compense ir más rápido.",
            },
            "coche-nuevo-o-seminuevo": {
                "name": "Nuevo o seminuevo",
                "text": "La diferencia la marca la pérdida de valor de los primeros años frente a la garantía y las averías del seminuevo. La calculadora te da el año en que se igualan y el precio máximo del seminuevo que compensa.",
                "guia": "cuanto-cuesta-tener-coche",
            },
            "diesel-gasolina-hibrido-electrico": {
                "name": "Diésel, gasolina, híbrido o eléctrico",
                "text": "Cuantos más kilómetros haces, más pesa el coste por kilómetro frente al precio de compra. La calculadora usa el precio medio del día del diésel y la gasolina y te dice desde qué kilometraje cambia el orden.",
                "datos": "{{baro}} Precios de hoy: gasolina 95 a {{gasolina}} €/l y diésel a {{diesel}} €/l (MITECO).",
                "fecha": ("fecha_carburantes", "Carburantes"),
            },
            "comprar-coche-o-renting": {
                "name": "Comprar o renting",
                "text": "Compara el coste real de comprar (préstamo, seguro, mantenimiento y lo que recuperas al venderlo) con la cuota del renting, que lo incluye casi todo. La calculadora da la cuota de renting de equilibrio.",
            },
            "seguro-todo-riesgo-o-terceros": {
                "name": "Seguro: todo riesgo o terceros",
                "text": "El todo riesgo compensa mientras el coche valga bastante más que la diferencia de prima; al depreciarse, deja de hacerlo. La calculadora te dice desde qué año, con tus primas y tu franquicia.",
            },
        },
    },
    "energia": {
        "path": "/energia/",
        "tema": "energia",
        "title": "Calculadoras de energía en casa: luz, calefacción y placas",
        "h1": "Energía en casa: decide con tus números",
        "description": "De la tarifa de luz a las placas solares: las decisiones de energía de tu casa en orden, con el PVPC de hoy (Red Eléctrica) y la tarifa del gas (BOE).",
        "kicker": "Tema · Energía en casa",
        "nav": "Energía",
        "all_title": "Todas las calculadoras de energía",
        "baro": None,
        "fechas": ["fecha_pvpc", "fecha_gas"],
        "disclaimer": "Información orientativa, no constituye asesoramiento. El precio del PVPC es el de la energía publicado por Red Eléctrica (sin peajes, cargos ni impuestos) y la tarifa del gas, la TUR publicada en el BOE; tu factura y tu contrato mandan. No prometemos ahorros: dependen de tu vivienda, tu zona y tu consumo.",
        "lead": ("<strong>Respuesta corta:</strong> en energía, decide primero lo que no cuesta dinero y después lo que exige obra: la tarifa de luz, el sistema de calefacción, las ventanas y el aislamiento, "
                 "las placas solares y, al final, los electrodomésticos. Hoy la energía del PVPC cuesta {{pvpc_hoy}} €/kWh de media ({{fecha_pvpc_es}}, sin peajes ni impuestos; fuente: Red Eléctrica) "
                 "y el gas con la tarifa regulada TUR.2 sale a {{gas_kwh}} €/kWh con impuestos ({{periodo_gas_es}}; fuente: BOE)."),
        "groups": [
            ("Sin obra: lo primero", ["luz-fija-o-indexada", "calefaccion-gas-aerotermia-electrica"]),
            ("Con inversión: cuándo se amortiza", ["cambiar-ventanas-aislamiento-merece-la-pena", "placas-solares-merece-la-pena", "cambiar-electrodomestico-antiguo-merece-la-pena", "reparar-o-comprar-electrodomestico"]),
        ],
        "steps": {
            "luz-fija-o-indexada": {
                "name": "Tarifa de luz: fija o PVPC",
                "text": "No requiere obra y se revisa en una tarde. La tarifa fija compensa si el precio de su energía queda por debajo del punto de equilibrio con el PVPC, que depende de cuándo consumes.",
                "datos": "Precio medio de la energía del PVPC: {{pvpc_hoy}} €/kWh (media de las 24 horas, sin peajes, cargos ni impuestos; Red Eléctrica).",
                "fecha": ("fecha_pvpc", "PVPC"),
                "guia": "checklist-casa-antes-del-invierno",
            },
            "calefaccion-gas-aerotermia-electrica": {
                "name": "Calefacción: gas, aerotermia o eléctrica",
                "text": "La aerotermia suele ser la más barata de usar, pero su instalación es más cara: solo compensa si la casa gasta bastante calefacción y la usas varios años. La calculadora compara el coste total con tu zona y tu aislamiento.",
                "datos": "Gas con la tarifa regulada TUR.2: {{gas_kwh}} €/kWh con impuestos en {{periodo_gas_es}} (BOE).",
                "fecha": ("fecha_gas", "Tarifa del gas"),
            },
            "cambiar-ventanas-aislamiento-merece-la-pena": {
                "name": "Ventanas y aislamiento",
                "text": "El ahorro real depende de la vivienda y no se puede prometer, así que la calculadora da el porcentaje mínimo de ahorro que necesitas para recuperar la obra con tu gasto en calefacción.",
            },
            "placas-solares-merece-la-pena": {
                "name": "Placas solares",
                "text": "Se amortizan antes cuanto más energía consumes en el momento en que la produces. La calculadora estima los años de amortización con tu consumo, tu producción y los excedentes.",
            },
            "cambiar-electrodomestico-antiguo-merece-la-pena": {
                "name": "Cambiar un electrodoméstico que funciona",
                "text": "Cambiar uno que funciona por uno de clase A compensa solo si el ahorro de luz cubre su precio en los años que cuentas: la calculadora te da los kWh al año que tendrías que ahorrar.",
            },
            "reparar-o-comprar-electrodomestico": {
                "name": "Si se estropea: reparar o comprar",
                "text": "Cuando el aparato falla, la decisión cambia: la calculadora da el presupuesto máximo de reparación que compensa con su vida útil, el riesgo de otra avería y el consumo extra del viejo.",
            },
        },
    },
}


def _n(v, dec): return f"{v:.{dec}f}".replace(".", ",")

def markers(params, live, baro_text=""):
    """Marcadores {{...}} del hub: mismos datos vivos que las guías (euribor_12m, periodo_euribor_es) + tipo fijo del BCE."""
    pm = calcs_loader.merge_market(params)
    m = {"euribor_12m": _n(pm["euribor_12m"], 3) if isinstance(pm.get("euribor_12m"), (int, float)) else "", "baro": baro_text}
    m["periodo_euribor_es"] = seo._mes(pm["periodo_euribor"]) if pm.get("periodo_euribor") else ""
    d = (live.get("datos") or {}).get("tipo_hipoteca_fija")
    if d and d.get("ok") and isinstance(d.get("valor"), (int, float)):
        m["tipo_fijo"] = _n(d["valor"], 2); m["periodo_tipo_fijo_es"] = seo._mes(d["extra"]["periodo"]); m["fecha_tipo_fijo"] = d["fecha_dato"]
    else:  # respaldo declarado en params (periodo y fuente fechados)
        m["tipo_fijo"] = _n(params["tipo_hipoteca_fija_medio"], 2); m["periodo_tipo_fijo_es"] = seo._mes(params["tipo_hipoteca_fija_periodo"]); m["fecha_tipo_fijo"] = params.get("fecha", "")
    m["fecha_euribor"] = pm.get("fecha_euribor", "")
    # coche: carburantes del día (MITECO, live.json; respaldo params con su fecha)
    def lv(i):
        x = (live.get("datos") or {}).get(i) or {}
        return x if x.get("ok") and isinstance(x.get("valor"), (int, float)) else None
    g, dsl = lv("gasolina95"), lv("diesel")
    m["gasolina"] = _n(g["valor"] if g else params["gasolina_eur_l"], 3)
    m["diesel"] = _n(dsl["valor"] if dsl else params["diesel_eur_l"], 3)
    m["fecha_carburantes"] = max([x["fecha_dato"] for x in (g, dsl) if x] or [params.get("fecha_combustibles", "")])
    m["fecha_carburantes_es"] = seo.fecha_es(m["fecha_carburantes"]) if m["fecha_carburantes"] else ""
    # energía: PVPC del día (REE, live.json) y gas TUR.2 con impuestos (params, verificado en BOE con su fecha)
    lz = lv("luz_pvpc")
    if lz: m["pvpc_hoy"] = _n(lz["valor"], 3); m["fecha_pvpc"] = lz["fecha_dato"]; m["fecha_pvpc_es"] = seo.fecha_es(lz["fecha_dato"])
    else: m["pvpc_hoy"] = _n(params["luz_2026"]["pvpc_media_ref"]["valor"], 3); m["fecha_pvpc"] = params["luz_2026"]["fecha"]; m["fecha_pvpc_es"] = "media de " + seo._mes(params["luz_2026"]["pvpc_media_ref"]["periodo"])
    m["gas_kwh"] = _n(params["gas_eur_kwh"], 3); m["fecha_gas"] = params.get("fecha_calefaccion", ""); m["periodo_gas_es"] = seo._mes(m["fecha_gas"][:7]) if m["fecha_gas"] else ""
    return m

def _fill(s, m):
    for k, v in m.items(): s = s.replace("{{" + k + "}}", v)
    return s

def themes_calcs(spec, calcs):
    return [c for c in calcs if c.get("tema") == spec["tema"]]

def guides_of(spec, guides, calcs):
    slugs = {c["slug"] for c in themes_calcs(spec, calcs)}
    return [g for g in guides if slugs & set(g.get("calcs", []))]

def eligible(calcs, guides):
    """Hubs que cumplen el disparador (>= MIN_PAGES páginas del tema entre calculadoras y guías)."""
    return {k: s for k, s in HUBS.items() if len(themes_calcs(s, calcs)) + len(guides_of(s, guides, calcs)) >= MIN_PAGES}

def page(key, spec, calcs, guides, params, live, card, base, baro_texts=()):
    """-> (body_html, jsonld, lastmod). Pasos en orden de decisión, 1-2 frases, dato vivo con fecha, calculadora y guía de cada paso."""
    baro = spec.get("baro")  # (ancla, índice de la frase de barometro.answers_text, descripción) o None
    baro_text = baro_texts[baro[1]] if baro and len(baro_texts) > baro[1] else ""
    m = markers(params, live, baro_text); by = {c["slug"]: c for c in calcs}; gb = {g["slug"]: g for g in guides}
    n = 0; secs = []; items = []
    for gname, slugs in spec["groups"]:
        secs.append(f"<h2>{html.escape(gname)}</h2>")
        for s in slugs:
            if s not in by: continue
            n += 1; st = spec["steps"][s]; c = by[s]
            datos = st.get("datos")
            dtxt = ""
            if datos:
                fk, flab = st.get("fecha", ("fecha_euribor", "Euríbor"))
                fch = f'<time datetime="{m[fk]}">{seo.fecha_es(m[fk])}</time>' if m.get(fk) else ""
                dtxt = f'<p class="note">{_fill(datos, m)}' + (f" {flab}: dato del {fch}." if fch else "") + "</p>"
            g = gb.get(st.get("guia"))
            glink = f' <a href="/guias/{g["slug"]}/">Guía: {html.escape(g["h1"])}</a>' if g else ""
            secs.append(f'<section class="box" id="paso-{n}"><h3>Paso {n}: {html.escape(st["name"])}</h3><p>{_fill(st["text"], m)}</p>{dtxt}'
                        f'<p><a class="btn2" href="/decidir/{s}/">{html.escape(c["h1"])}</a>{glink}</p></section>')
            items.append((st["name"], f'/decidir/{s}/'))
    for g in guides_of(spec, guides, calcs): items.append((g["h1"], f'/guias/{g["slug"]}/'))
    if baro: items.append(("Barómetro Entre Muchos", "/barometro/"))
    mod = seo.lastmod("hubs.py", extra=[m.get(k, "") for k in spec.get("fechas", [])] + [g["modified"] for g in guides_of(spec, guides, calcs)])
    pub = seo.published("hubs.py")
    gl = "".join(f'<li><a href="/guias/{g["slug"]}/">{g["h1"]}</a> <span class="note">{g["description"]}</span></li>' for g in guides_of(spec, guides, calcs))
    bl = f'<li><a href="{baro[0]}">Barómetro Entre Muchos</a> <span class="note">{baro[2]}</span></li>' if baro else ""
    body = f"""<article class="guide hub">
<p class="kicker">{spec["kicker"]}</p>
<h1>{spec["h1"]}</h1>
<p class="byline note">Por {AUTHOR} · Publicado el <time datetime="{pub}">{seo.fecha_es(pub)}</time> · Actualizado el <time datetime="{mod}">{seo.fecha_es(mod)}</time></p>
<p class="lead">{_fill(spec["lead"], m)}</p>
{"".join(secs)}
<h2>Guías y datos propios</h2>
<ul class="guides">{gl}{bl}</ul>
<h2>{spec["all_title"]}</h2>
<ul class="cards">{"".join(card(c) for c in themes_calcs(spec, calcs))}</ul>
<p class="disclaimer">{spec["disclaimer"]} Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""
    url = base + spec["path"]
    org = seo.org(base)
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": spec["h1"], "description": spec["description"], "url": url,
           "inLanguage": "es-ES", "datePublished": pub, "dateModified": mod, "isPartOf": {"@id": base + "/#website"},
           "author": {"@type": "Organization", "name": AUTHOR, "url": base + "/como-funciona/"}, "publisher": org,
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListOrder": "https://schema.org/ItemListOrderAscending",
                          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": nm, "url": base + p} for i, (nm, p) in enumerate(items)]}},
          seo.breadcrumbs(base, [("Inicio", "/"), (spec["h1"], None)])]
    return body, ld, mod

# ---------- enlaces desde otras páginas ----------
def calc_link(slug, calcs, active):
    """Párrafo «forma parte del mapa de …» para calculadoras del hub."""
    for k, s in active.items():
        if any(slug in sl for _, sl in s["groups"]):
            return f'<p class="note hub-link">Esta decisión es un paso del mapa <a href="{s["path"]}">{html.escape(s["h1"])}</a>, en orden.</p>'
    return ""

def guide_link(g, calcs, guides, active):
    for k, s in active.items():
        if g in guides_of(s, guides, calcs):
            return f'<p class="note hub-link">Más sobre el tema: <a href="{s["path"]}">{html.escape(s["h1"])}</a> (calculadoras y guías en orden de decisión).</p>'
    return ""

def home_link(active):
    if len(active) == 1:
        s = next(iter(active.values()))
        return f'<p class="note hub-link"><strong>Temas:</strong> <a href="{s["path"]}">{html.escape(s["h1"])}</a> · {html.escape(s["description"])}</p>'
    return ('<p class="note hub-link"><strong>Mapas por tema, en orden de decisión:</strong> '
            + " · ".join(f'<a href="{s["path"]}">{html.escape(s["nav"])}</a>' for s in active.values()) + "</p>") if active else ""

def footer_links(active, skip=("hipoteca",)):
    """Enlaces del pie para hubs que aún no están en templates/base.html (el de hipoteca ya lo está)."""
    return "".join(f'<a href="{s["path"]}">{html.escape(s["nav"])}</a>' for k, s in active.items() if k not in skip)

def llms_lines(active, base):
    return [f"- [{s['h1']}]({base}{s['path']}): {s['description']}" for s in active.values()]
