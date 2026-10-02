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

def page(key, spec, calcs, guides, params, live, card, base, baro_text="", baro_slug="/barometro/#hipoteca"):
    """-> (body_html, jsonld, lastmod). Pasos en orden de decisión, 1-2 frases, dato vivo con fecha, calculadora y guía de cada paso."""
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
                fch = f'<time datetime="{m["fecha_euribor"]}">{seo.fecha_es(m["fecha_euribor"])}</time>' if m["fecha_euribor"] else ""
                dtxt = f'<p class="note">{_fill(datos, m)}' + (f" Euríbor: dato del {fch}." if fch else "") + "</p>"
            g = gb.get(st.get("guia"))
            glink = f' <a href="/guias/{g["slug"]}/">Guía: {html.escape(g["h1"])}</a>' if g else ""
            secs.append(f'<section class="box" id="paso-{n}"><h3>Paso {n}: {html.escape(st["name"])}</h3><p>{_fill(st["text"], m)}</p>{dtxt}'
                        f'<p><a class="btn2" href="/decidir/{s}/">{html.escape(c["h1"])}</a>{glink}</p></section>')
            items.append((st["name"], f'/decidir/{s}/'))
    for g in guides_of(spec, guides, calcs): items.append((g["h1"], f'/guias/{g["slug"]}/'))
    items.append(("Barómetro Entre Muchos", "/barometro/"))
    mod = seo.lastmod("hubs.py", extra=[m.get("fecha_tipo_fijo", ""), m.get("fecha_euribor", "")] + [g["modified"] for g in guides_of(spec, guides, calcs)])
    pub = seo.published("hubs.py")
    gl = "".join(f'<li><a href="/guias/{g["slug"]}/">{g["h1"]}</a> <span class="note">{g["description"]}</span></li>' for g in guides_of(spec, guides, calcs))
    body = f"""<article class="guide hub">
<p class="kicker">{spec["kicker"]}</p>
<h1>{spec["h1"]}</h1>
<p class="byline note">Por {AUTHOR} · Publicado el <time datetime="{pub}">{seo.fecha_es(pub)}</time> · Actualizado el <time datetime="{mod}">{seo.fecha_es(mod)}</time></p>
<p class="lead">{_fill(spec["lead"], m)}</p>
{"".join(secs)}
<h2>Guías y datos propios</h2>
<ul class="guides">{gl}<li><a href="{baro_slug}">Barómetro Entre Muchos</a> <span class="note">Cifras propias de cada mes con su fecha: Euríbor de equilibrio, coste por km y rentabilidad para invertir antes que amortizar.</span></li></ul>
<h2>Todas las calculadoras de hipoteca</h2>
<ul class="cards">{"".join(card(c) for c in themes_calcs(spec, calcs))}</ul>
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Los datos de mercado proceden del Banco Central Europeo y se actualizan con cada dato nuevo; las condiciones de tu hipoteca están en tu escritura. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
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
    return "".join(f'<p class="note hub-link"><strong>Temas:</strong> <a href="{s["path"]}">{html.escape(s["h1"])}</a> · {html.escape(s["description"])}</p>' for s in active.values())

def llms_lines(active, base):
    return [f"- [{s['h1']}]({base}{s['path']}): {s['description']}" for s in active.values()]
