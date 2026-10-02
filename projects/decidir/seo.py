"""SEO técnico + GEO para build.py (dueño: Estratega SEO/GEO). Solo stdlib.
- lastmod real por página (git log del contenido; si hay cambios sin commit, fecha del archivo).
- Afinidad entre calculadoras -> data/clusters.json (render_calc la usa si existe).
- Guías de apoyo (content/guias/*.html con cabecera <!--meta {json} -->).
- JSON-LD (Article, HowTo opcional, Organization, WebSite+SearchAction).
- llms.txt y llms-full.txt generados desde las calculadoras y guías.
"""
import json, os, re, html, subprocess, datetime, shutil, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
AUTHOR = "Equipo de Entre Muchos"
TODAY = datetime.date.today().isoformat()


# ---------- fechas reales ----------
def _git(args):
    try:
        r = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""

def _file_date(rel, first=False):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): return ""
    if not first and _git(["status", "--porcelain", "--", rel]):  # modificado o sin seguimiento: cambia hoy
        return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    if first:
        d = _git(["log", "--diff-filter=A", "--follow", "--format=%cs", "--", rel]).splitlines()
        if d: return d[-1]
    d = _git(["log", "-1", "--format=%cs", "--", rel])
    return d or datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()

def lastmod(*rels, extra=()):
    ds = [d for d in [_file_date(r) for r in rels] + list(extra) if d]
    return max(ds) if ds else TODAY

def published(*rels):
    ds = [d for d in (_file_date(r, first=True) for r in rels) if d]
    return min(ds) if ds else TODAY

def calc_files(slug):
    return [f"calcs/{slug}.json", f"calcs/{slug}.js", f"content/{slug}.html"]

def calc_lastmod(slug, params):
    # La fecha de parámetros (p. ej. Euríbor) aparece en la página: es contenido.
    # También la fecha de los datos vivos (Pulso) que se muestran en esa página.
    return lastmod(*calc_files(slug), extra=[params.get("fecha", ""), live_date(slug)])


# ---------- clústeres ----------
_STOP = {"o", "y", "de", "la", "el", "los", "las", "con", "que", "cual", "para", "mas", "por", "una", "un", "tu", "tus", "sale", "barato", "barata", "mejor", "conviene", "anos", "dinero"}
def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
def _tokens(c):
    txt = _norm(c["slug"].replace("-", " ") + " " + c["h1"])
    return {(w[:-1] if len(w) > 5 and w[-1] in "ao" else w) for w in re.findall(r"[a-z]{3,}", txt) if w not in _STOP}  # electrico ~ electrica

# Temas vecinos (para completar enlaces entre temas con sentido: energía <-> coche eléctrico, vivienda <-> calefacción, hipoteca <-> ahorro)
NEAR = {"energia": {"coche": 5, "hipoteca": 5}, "coche": {"energia": 5}, "hipoteca": {"ahorro": 5, "energia": 2},
        "ahorro": {"hipoteca": 5}, "impuestos": {"ahorro": 3}}

def build_clusters(calcs, tema, path=os.path.join(ROOT, "data/clusters.json"), k=3):
    """Afinidad = 10 si comparten tema + cercanía de temas (NEAR) + nº de palabras clave compartidas. Top k (mín. 2)."""
    out = {}; slugs = {x["slug"] for x in calcs}
    try: FIJOS = json.load(open(os.path.join(os.path.dirname(path), "clusters_fijos.json")))
    except Exception: FIJOS = {}
    for c in calcs:
        scored = sorted(((10 * (tema(x) == tema(c)) + NEAR.get(tema(c), {}).get(tema(x), 0) + len(_tokens(x) & _tokens(c)), x["slug"])
                         for x in calcs if x["slug"] != c["slug"]), key=lambda t: (-t[0], t[1]))
        top = [s for sc, s in scored if sc >= 10][:k]
        pin = [x for x in FIJOS.get(c["slug"], []) if x in slugs and x != c["slug"]]  # afinidades editoriales (data/clusters_fijos.json): mandan sobre el cálculo
        if pin: top = (pin + [x for x in top if x not in pin])[:k]
        for sc, s in scored:  # completa hasta 2 con los más cercanos de otros temas
            if len(top) >= min(2, len(scored)): break
            if s not in top: top.append(s)
        out[c["slug"]] = top
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: json.dump(out, f, ensure_ascii=False, indent=1)
    return out

def related_slugs(slug, path=os.path.join(ROOT, "data/clusters.json")):
    try: return json.load(open(path)).get(slug, [])
    except Exception: return []


# ---------- guías ----------
def load_guides(params):
    import calcs_loader
    pm = calcs_loader.merge_market(params)
    if pm.get("periodo_euribor"): pm["periodo_euribor_es"] = _mes(pm["periodo_euribor"])
    live = load_live()
    def _lv(i):
        d = (live.get("datos") or {}).get(i) or {}
        return d if d.get("ok") and isinstance(d.get("valor"), (int, float)) else None
    def _n(v, nd=3): return f"{v:.{nd}f}".replace(".", ",")
    ex = {}  # marcadores de datos vivos propios de las guías (luz y carburantes con su fecha)
    if _lv("luz_pvpc"):
        d = _lv("luz_pvpc"); ex["pvpc_hoy"] = _n(d["valor"]); ex["fecha_pvpc_es"] = fecha_es(d["fecha_dato"])
        if (d.get("extra") or {}).get("media_mes"): ex["pvpc_media_mes"] = _n(d["extra"]["media_mes"]); ex["mes_pvpc_es"] = _mes(d["extra"]["mes"])
    mt = _lv("madrid_tiempo")
    if mt and (mt.get("extra") or {}).get("min_semana") is not None:
        ex["temp_madrid"] = _n(mt["valor"], 1); ex["min_semana_madrid"] = _n(mt["extra"]["min_semana"], 1); ex["fecha_tiempo_es"] = fecha_es(mt["fecha_dato"])
    if params.get("fecha_calefaccion"): ex["fecha_gas_es"] = fecha_es(params["fecha_calefaccion"])
    if _lv("gasolina95"): ex["fecha_gasolina_es"] = fecha_es(_lv("gasolina95")["fecha_dato"])
    ex["fecha_datos_es"] = fecha_es(params.get("fecha") or TODAY)
    pm.update(ex)
    gdates = [d["fecha_dato"] for d in (_lv("luz_pvpc"), _lv("gasolina95")) if d]
    gdir = os.path.join(ROOT, "content/guias"); out = []
    if not os.path.isdir(gdir): return out
    for f in sorted(os.listdir(gdir)):
        if not f.endswith(".html"): continue
        raw = open(os.path.join(gdir, f)).read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m: continue
        g = json.loads(m.group(1)); g["slug"] = f[:-5]
        body = raw[m.end():]
        # bloques condicionales por calculadora: <!--si:slug-->A[<!--sino-->B]<!--/si--> solo si existe calcs/<slug>.json (sin enlaces rotos)
        body = re.sub(r"<!--si:([a-z0-9-]+)-->(.*?)<!--/si-->", lambda mm: mm.group(2).split("<!--sino-->")[0 if os.path.exists(os.path.join(ROOT, "calcs", mm.group(1) + ".json")) else -1] if (os.path.exists(os.path.join(ROOT, "calcs", mm.group(1) + ".json")) or "<!--sino-->" in mm.group(2)) else "", body, flags=re.S)
        for k, v in pm.items():  # {{clave}} -> valor de data/params.json con el mercado de data/live.json (cifras = datos)
            if isinstance(v, (int, float)): v = (f"{v:.3f}".rstrip("0") + "0" * max(0, 2 - len(f"{v:.3f}".rstrip("0").split(".")[1]))).replace(".", ",") if isinstance(v, float) else str(v)
            if isinstance(v, str): body = body.replace("{{" + k + "}}", v)
        g["body"] = body
        rel = f"content/guias/{f}"
        g["modified"] = lastmod(rel, extra=[params.get("fecha", "")] + gdates if "{{" in raw else [])
        g["published"] = g.get("published") or published(rel)
        out.append(g)
    return out

def guides_for(slug, guides):
    return [g for g in guides if slug in g.get("calcs", [])]

def guides_html(slug, guides):
    gs = guides_for(slug, guides)
    if not gs: return ""
    return '<h2>Guías para entenderlo</h2><ul class="guides">' + "".join(
        f'<li><a href="/guias/{g["slug"]}/">{g["h1"]}</a> <span class="note">{g["description"]}</span></li>' for g in gs) + "</ul>"

def fecha_es(iso):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    y, m, d = iso.split("-"); return f"{int(d)} de {meses[int(m) - 1]} de {y}"

def guide_page(g, calcs, card, base):
    rel = [c for s in g.get("calcs", []) for c in calcs if c["slug"] == s]
    calc_block = ('<h2>Calcúlalo con tus números</h2><ul class="cards">' + "".join(card(c) for c in rel) + "</ul>") if rel else ""
    body = f"""<article class="guide">
<p class="kicker"><a href="/guias/">Guías</a></p>
<h1>{g["h1"]}</h1>
<p class="byline note">Por {AUTHOR} · Publicado el <time datetime="{g["published"]}">{fecha_es(g["published"])}</time> · Actualizado el <time datetime="{g["modified"]}">{fecha_es(g["modified"])}</time></p>
{g["body"]}
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Revisa tus documentos (factura, contrato o escritura) y, si la decisión es importante, consulta con un profesional. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{calc_block}
</article>"""
    url = f"{base}/guias/{g['slug']}/"
    jsonld = [article(g["h1"], g["description"], url, g["published"], g["modified"], base),
              breadcrumbs(base, [("Inicio", "/"), ("Guías", "/guias/"), (g["h1"], None)])]
    if g.get("faq"):  # opcional en el meta: [[pregunta, respuesta], ...]; cada respuesta repite cifras ya presentes en el cuerpo
        jsonld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]})
    return body, jsonld

def guides_index(guides):
    return '<h1>Guías para decidir mejor</h1><p class="lead">Explicaciones cortas, con datos y fuentes, para usar las calculadoras con criterio.</p><ul class="cards">' + "".join(
        f'<li><a href="/guias/{g["slug"]}/">{g["h1"]}</a><p>{g["description"]}</p></li>' for g in guides) + "</ul>"


# ---------- JSON-LD ----------
def org(base):
    return {"@type": "Organization", "@id": base + "/#org", "name": "Entre Muchos", "url": base + "/",
            "logo": base + "/assets/og.png", "email": "hola@entremuchos.com"}

def article(headline, desc, url, pub, mod, base):
    return {"@context": "https://schema.org", "@type": "Article", "headline": headline[:110], "description": desc,
            "mainEntityOfPage": url, "url": url, "inLanguage": "es-ES", "datePublished": pub, "dateModified": mod,
            "author": {"@type": "Organization", "name": AUTHOR, "url": base + "/como-funciona/"},
            "publisher": org(base)}

def breadcrumbs(base, items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i + 1, "name": n}, **({"item": base + p} if p else {})) for i, (n, p) in enumerate(items)]}

def webapp(c, base, mod):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": c["h1"], "description": c["description"],
            "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "browserRequirements": "Requiere JavaScript",
            "inLanguage": "es-ES", "url": f"{base}/decidir/{c['slug']}/", "dateModified": mod,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            "author": {"@type": "Organization", "name": "Entre Muchos", "url": base + "/"}, "publisher": org(base)}

def calc_jsonld(c, base, params):
    url = f"{base}/decidir/{c['slug']}/"
    out = [article(c["h1"], c["description"], url, published(*calc_files(c["slug"])), calc_lastmod(c["slug"], params), base)]
    if c.get("howto"):  # opcional: lista de pasos en el JSON de la calculadora
        out.append({"@context": "https://schema.org", "@type": "HowTo", "name": c["h1"], "step": [
            {"@type": "HowToStep", "position": i + 1, "text": s} for i, s in enumerate(c["howto"])]})
    return out

def home_jsonld(base, desc):
    o = dict(org(base)); o["@context"] = "https://schema.org"
    return [o, {"@context": "https://schema.org", "@type": "WebSite", "@id": base + "/#website", "name": "Entre Muchos",
                "url": base + "/", "inLanguage": "es-ES", "description": desc, "publisher": {"@id": base + "/#org"},
                "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": base + "/decidir/?q={search_term_string}"},
                                    "query-input": "required name=search_term_string"}}]


# ---------- llms.txt ----------
def html_to_md(h, base):
    h = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", h, flags=re.S)
    h = re.sub(r'<a [^>]*href="(/[^"]*)"[^>]*>(.*?)</a>', lambda m: f"[{m.group(2)}]({base}{m.group(1)})", h, flags=re.S)
    h = re.sub(r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", h, flags=re.S)
    h = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n### \1\n", h, flags=re.S)
    h = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n#### \1\n", h, flags=re.S)
    h = re.sub(r"</?(strong|b)>", "**", h)
    h = re.sub(r"<li[^>]*>", "\n- ", h)
    h = re.sub(r"<tr[^>]*>", "\n| ", h); h = re.sub(r"</t[dh]>", " | ", h)
    h = re.sub(r"</p>|<br\s*/?>|</ul>|</ol>|</table>", "\n", h)
    h = html.unescape(re.sub(r"<[^>]+>", "", h))
    h = re.sub(r"[ \t]+", " ", h); h = re.sub(r"\n\s*\n\s*\n+", "\n\n", h)
    return "\n".join(l.strip() for l in h.splitlines()).strip()

def write_llms(dist, site, calcs, guides, params, tema, icons, extra="", notes=(), hubs=(), tablas=(), tablas_md=""):
    base = site["base_url"].rstrip("/")
    head = (f"# {site['name']}\n\n> {site['name']} ({base}) reúne calculadoras gratuitas en español para decidir entre dos o más opciones "
            "con tus propios números (hipoteca, coche, impuestos, energía, ahorro) en España. Cada página da un veredicto, la cifra que lo justifica, "
            "los supuestos y las fuentes oficiales. Los cálculos se hacen en el navegador; no es asesoramiento financiero.\n\n"
            f"Autoría: {AUTHOR}. Parámetros de mercado actualizados el {params.get('fecha', TODAY)}. "
            f"Metodología: {base}/como-funciona/ · Política de IA: {base}/politica-ia/\n")
    by_t = {}
    for c in calcs: by_t.setdefault(tema(c), []).append(c)
    lines = [head]
    for t, cs in by_t.items():
        lines.append(f"\n## Calculadoras: {icons[t][0]}\n")
        lines += [f"- [{c['h1']}]({base}/decidir/{c['slug']}/): {c['description']}" for c in cs]
    if hubs:
        lines.append("\n## Temas (mapas de decisión)\n")
        lines += [f"- [{h['h1']}]({base}{h['path']}): {h['description']}" for h in hubs]
    if guides:
        lines.append("\n## Guías\n")
        lines += [f"- [{g['h1']}]({base}/guias/{g['slug']}/): {g['description']}" for g in guides]
    lines.append(f"\n## Calendario\n\n- [Calendario de decisiones]({base}/calendario/): fechas que mueven una decisión de dinero (revisión de la TUR de gas, Euríbor mensual, cambio de hora, Black Friday, retribución flexible, cierre del IRPF y ventas con pérdidas, cambio de base y regularización de autónomos, renuncia a módulos, Renta, y lo pendiente de norma: SMI, IPREM y pensiones de 2027) con su fuente oficial.")
    if notes:
        lines.append("\n## Actualidad\n")
        lines += [f"- [{n['h1']}]({base}/actualidad/{n['slug']}/): {n['description']}" for n in notes[:10]]
    if extra:  # Barómetro: datos propios fechados
        lines.append("\n## Datos propios\n")
        lines.append(f"- [Barómetro Entre Muchos]({base}/barometro/): Euríbor de equilibrio fija/variable, coste por km según motor y rentabilidad para que invertir compense frente a amortizar, actualizado cada mes. Datos en JSON: {base}/barometro/datos.json · CSV: {base}/barometro/datos.csv · Licencia de las cifras propias: CC BY 4.0 (cita «Barómetro Entre Muchos» y la fecha de los datos).")
    if tablas:  # c36 T24: tablas oficiales 2026 con cálculo propio y CSV (tablas.py)
        lines.append(f"\n## Tablas 2026 (cifras oficiales verificadas, con fuente y CSV)\n\n- [Tablas 2026]({base}/tablas-2026/): índice; todas las tablas en JSON: {base}/tablas-2026/datos.json")
        lines += list(tablas)
    lines.append(f"\n## Optional\n\n- [Texto completo para LLMs]({base}/llms-full.txt): preguntas, criterios de decisión, parámetros y fuentes de cada calculadora.\n"
                 f"- [Catálogo]({base}/decidir/): todas las calculadoras por tema.\n"
                 f"- [Feed Atom]({base}{FEED_PATH}): notas de actualidad, guías y Barómetro mensual con su fecha.\n")
    open(os.path.join(dist, "llms.txt"), "w").write("\n".join(lines))

    full = [head]
    if hubs:  # c48: índice de temas también en llms-full (antes solo en llms.txt)
        full.append("\n## Temas (mapas de decisión)\n\n" + "\n".join(f"- [{h['h1']}]({base}{h['path']})" for h in hubs)
                    + f"\n- [Calendario de decisiones]({base}/calendario/) · [Actualidad]({base}/actualidad/) · [Índice corto]({base}/llms.txt)\n")
    for c in calcs:
        url = f"{base}/decidir/{c['slug']}/"
        ins = "\n".join(f"- {re.sub('<[^>]+>', '', i['label'])}: " + (", ".join(o["t"] for o in i["options"]) if i.get("type") == "select" else f"por defecto {i.get('default')}")
                        for i in c["inputs"])
        faqs = "\n\n".join(f"**{q}**\n{re.sub('<[^>]+>', '', a)}" for q, a in c["faqs"])
        full.append(f"\n---\n\n## {c['h1']}\n\nURL: {url}\nActualizado: {calc_lastmod(c['slug'], params)}\n\n"
                    f"**Pregunta que responde:** {c['h1']}\n\n**Respuesta corta:** {html_to_md(c.get('veredicto') or c['lead'], base)}\n\n"
                    f"### Criterios de decisión\n{html_to_md(c['content'], base)}\n\n### Parámetros que introduce el usuario\n{ins}\n\n"
                    f"### Preguntas frecuentes\n{faqs}\n\n### Supuestos y fuentes\n{html_to_md(c['sources'], base)}\n")
    if extra: full.append(extra)
    if tablas_md: full.append(tablas_md)
    for g in guides:
        full.append(f"\n---\n\n## {g['h1']}\n\nURL: {base}/guias/{g['slug']}/\nActualizado: {g['modified']}\n\n{html_to_md(g['body'], base)}\n")
    open(os.path.join(dist, "llms-full.txt"), "w").write("\n".join(full))


# ---------- Feed Atom (/feed.xml): solo contenido real y fechado (actualidad, guías, Barómetro) ----------
FEED_PATH = "/feed.xml"
FEED_TITLE = "Entre Muchos: actualidad, guías y Barómetro"

def feed_link():
    """<link rel=alternate> para el <head> de todas las páginas (lo añade build.write)."""
    return f'<link rel="alternate" type="application/atom+xml" title="{FEED_TITLE}" href="{FEED_PATH}">'

def _atom_dt(iso):
    return iso if "T" in iso else iso + "T00:00:00Z"

def feed_entries(base, guides, notes, baro=None, baro_mod=None, hubs=(), extra=()):
    E = list(extra)  # c36: entradas ya formadas (tablas.feed_items)
    for h in hubs:
        E.append(dict(id=f"tag:entremuchos.com,2026:temas{h['path'].rstrip('/')}", title=h["h1"], url=f"{base}{h['path']}", published=h["published"], updated=h["modified"], summary=h["description"], cat="Temas"))
    for n in notes:
        E.append(dict(id=f"tag:entremuchos.com,2026:actualidad/{n['slug']}", title=n["h1"], url=f"{base}/actualidad/{n['slug']}/",
                      published=n["published"], updated=n["modified"], summary=n["description"], cat="Actualidad"))
    for g in guides:
        E.append(dict(id=f"tag:entremuchos.com,2026:guias/{g['slug']}", title=g["h1"], url=f"{base}/guias/{g['slug']}/",
                      published=g["published"], updated=g["modified"], summary=g["description"], cat="Guías"))
    if baro:  # una entrada por mes del histórico (el mes en curso se actualiza; los cerrados quedan fijos)
        import barometro
        for m in baro.get("historico", []):
            prov = m.get("estado") == "provisional"
            E.append(dict(id=f"tag:entremuchos.com,2026:barometro/{m['mes']}", title=f"Barómetro de {barometro.mes_es(m['fecha_datos'])}" + (" (en curso)" if prov else ""),
                          url=f"{base}/barometro/", published=m["mes"] + "-01", updated=max(m["fecha_datos"], baro_mod or "") if prov else m["fecha_datos"],
                          summary=" ".join(barometro.answers_text(baro)) if prov else f"Euríbor de equilibrio {m['euribor_equilibrio']} % con fija al {m['tipo_fijo_referencia']} %; coche más barato a 15.000 km: {m['coche_ganador_15000km']}.",
                          cat="Barómetro"))
    return sorted(E, key=lambda e: (e["updated"], e["published"]), reverse=True)[:30]

def write_feed(dist, site, guides, notes, baro=None, baro_mod=None, hubs=(), extra=()):
    base = site["base_url"].rstrip("/"); x = lambda t: html.escape(str(t), quote=True)
    E = feed_entries(base, guides, notes, baro, baro_mod, hubs, extra)
    if not E: return None
    ent = "".join(f"""<entry><id>{x(e["id"])}</id><title>{x(e["title"])}</title><link rel="alternate" type="text/html" href="{x(e["url"])}"/>"""
                  f"""<published>{_atom_dt(e["published"])}</published><updated>{_atom_dt(e["updated"])}</updated><category term="{x(e["cat"])}"/>"""
                  f"""<summary type="text">{x(e["summary"])}</summary></entry>\n""" for e in E)
    xml = (f'<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="es-ES">\n'
           f'<id>{base}/</id><title>{x(FEED_TITLE)}</title><subtitle>Notas con datos oficiales, guías y el Barómetro mensual de {x(site["name"])}. Cada entrada lleva su fecha real.</subtitle>\n'
           f'<link rel="self" type="application/atom+xml" href="{base}{FEED_PATH}"/><link rel="alternate" type="text/html" href="{base}/"/>\n'
           f'<updated>{_atom_dt(max(e["updated"] for e in E))}</updated><author><name>{AUTHOR}</name><uri>{base}/como-funciona/</uri></author>\n'
           f'<rights>Textos © {x(site["name"])}; cifras del Barómetro CC BY 4.0</rights>\n{ent}</feed>\n')
    open(os.path.join(dist, FEED_PATH.strip("/")), "w").write(xml)
    return len(E)

def insert_before(page, marker, block):
    """Inserta block antes de la primera aparición de marker (o al final si no está). Evita tocar plantillas ajenas."""
    return page.replace(marker, block + marker, 1) if marker in page else page + block

def copy_static(dist):
    s = os.path.join(ROOT, "static")
    if os.path.isdir(s): shutil.copytree(s, dist, dirs_exist_ok=True)


# ---------- Pulso: datos de hoy (data/live.json, generado por ops/refresh_data.py) ----------
LIVE_PATH = os.path.join(ROOT, "data/live.json")
MAX_EDAD = 7  # días; por encima, el dato no se muestra (nunca datos viejos como si fueran de hoy)
# id del bloque -> calculadoras afines (la primera es el enlace principal)
PULSO_CALCS = {
    "luz": ["luz-fija-o-indexada", "calefaccion-gas-aerotermia-electrica", "reparar-o-comprar-electrodomestico", "cambiar-electrodomestico-antiguo-merece-la-pena"],  # las que usan live.luz_pvpc como defecto
    "carburantes": ["diesel-gasolina-hibrido-electrico"],
    "euribor": ["hipoteca-fija-o-variable", "amortizar-plazo-o-cuota", "cuanto-ahorrar-para-comprar-casa"],
    "tiempo": ["calefaccion-gas-aerotermia-electrica"],
}
PULSO_LABEL = {"amortizar-plazo-o-cuota": "¿Amortizar plazo o cuota?"}
PULSO_HOME = ["luz", "carburantes", "euribor"]  # máx. 3 en la home
_LIVE = {}

def load_live(path=LIVE_PATH):
    """live.json o {} si no existe / está roto."""
    try:
        with open(path) as f: d = json.load(f)
        return d if isinstance(d.get("datos"), dict) else {}
    except Exception:
        return {}

def _fresh(d, today):
    """Dato utilizable: valor, ok, fecha_dato reciente."""
    if not d or d.get("valor") is None or not d.get("fecha_dato"): return False
    try: f = datetime.date.fromisoformat(d["fecha_dato"])
    except ValueError: return False
    return -1 <= (today - f).days <= d.get("max_edad_dias", MAX_EDAD)

def _eur(x, dec=2): return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def _num(x, dec=1): return f"{x:.{dec}f}".replace(".", ",")
def _mes(ym): return MESES_ES[int(ym[5:7]) - 1] + " de " + ym[:4]
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def _var(d, unit_pct=True, ref="ayer"):
    """'un 7,0 % más que ayer' / 'igual que ayer' / '' si no hay referencia."""
    p = d.get("variacion_pct")
    if p is None: return ""
    if abs(p) < 0.5: return f"prácticamente igual que {ref}"
    return f"un {_num(abs(p))} % {'más' if p > 0 else 'menos'} que {ref}"

def pulso_items(live, today=None):
    """Lista de bloques calculados: {id, texto, fecha, fuente, url_fuente, calc, titulo}. Solo con datos frescos."""
    today = today or datetime.date.today()
    D = live.get("datos", {}) if live else {}
    out = []
    luz = D.get("luz_pvpc")
    if _fresh(luz, today):
        x = luz["extra"]; v = _var(luz)
        t = f"La luz (PVPC) cuesta de media {_eur(luz['valor'], 3)} €/kWh" + (f", {v}" if v else "") + "."
        t += f" Hora más barata: {x['hora_barata']}-{(x['hora_barata'] + 1) % 24} h ({_eur(x['precio_hora_barata'], 3)} €/kWh); más cara: {x['hora_cara']}-{(x['hora_cara'] + 1) % 24} h ({_eur(x['precio_hora_cara'], 3)} €/kWh)."
        out.append(dict(id="luz", titulo="Luz", texto=t, fecha=luz["fecha_dato"], fuente=luz["fuente"], datos=[luz]))
    di, ga = D.get("diesel"), D.get("gasolina95")
    if _fresh(di, today) and _fresh(ga, today):
        vd = _var(di, ref="el dato anterior")
        t = f"Diésel a {_eur(di['valor'], 3)} €/l y gasolina 95 a {_eur(ga['valor'], 3)} €/l de media en España"
        t += f" (diésel {vd})." if vd else "."
        t += f" La diferencia entre ambos es de {_eur(abs(ga['valor'] - di['valor']) * 100, 0)} céntimos por litro."
        out.append(dict(id="carburantes", titulo="Carburantes", texto=t, fecha=min(di["fecha_dato"], ga["fecha_dato"]), fuente=di["fuente"], datos=[di, ga]))
    eu = D.get("euribor12m")
    if _fresh(eu, today):
        x = eu["extra"]; t = f"A 12 meses está en el {_eur(eu['valor'], 3)} % de media en {_mes(x['periodo'])}"
        if eu.get("variacion_abs") is not None:
            dif = eu["variacion_abs"]
            t += f", {_eur(abs(dif), 2)} puntos {'más' if dif > 0 else 'menos'} que en {_mes(eu['anterior_fecha']).split(' de ')[0]}" if abs(dif) >= 0.005 else ", igual que el mes anterior"
        t += "."
        out.append(dict(id="euribor", titulo="Euríbor", texto=t, fecha=eu["fecha_dato"], fuente=eu["fuente"], datos=[eu], fecha_txt=_mes(x["periodo"])))
    tm = D.get("madrid_tiempo")
    if _fresh(tm, today):
        x = tm["extra"]
        t = f"Madrid: {_num(tm['valor'])} °C ahora y mínima de {_num(x['min_semana'])} °C en los próximos {x['dias_prevision']} días."
        out.append(dict(id="tiempo", titulo="Tiempo", texto=t, fecha=tm["fecha_dato"], fuente=tm["fuente"], datos=[tm]))
    return out

def live_date(slug, live=None, today=None):
    """Fecha del dato fresco más reciente que se muestra en la página (para lastmod/dateModified). '' si no hay."""
    live = live if live is not None else load_live()
    ids = PULSO_HOME if slug == "/" else [i for i, cs in PULSO_CALCS.items() if slug in cs]
    ds = [it["fecha"] for it in pulso_items(live, today) if it["id"] in ids]
    return max(ds) if ds else ""

def _fmt_fecha(iso):
    d = datetime.date.fromisoformat(iso); return f"{d.day} de {MESES_ES[d.month - 1]} de {d.year}"

PULSO_ICON = {
    "luz": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "carburantes": '<path d="M4 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M3 21h12M14 9h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V8l-3-3M7 8h4"/>',
    "euribor": '<path d="M3 10 12 4l9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 21h18"/>',
    "tiempo": '<path d="M14 14.8V4a2 2 0 0 0-4 0v10.8a4 4 0 1 0 4 0z"/>',
}

def _pulso_valor(i, d):
    v = d["valor"]
    if i == "luz": return _eur(v, 3), "€/kWh"
    if i == "carburantes": return _eur(v, 3), "€/l diésel"
    if i == "euribor": return _eur(v, 3), "% a 12 meses"
    return _num(v), "°C en Madrid"

def _pulso_delta(i, d):
    """Variación con flecha y color semántico: sube=ámbar, baja=verde, neutro=gris. '' si no hay referencia."""
    if i == "euribor":
        x = d.get("variacion_abs")
        if x is None: return ""
        txt = f"{_eur(abs(x), 2)} pts"; q = x
    else:
        x = d.get("variacion_pct")
        if x is None: return ""
        txt = f"{_num(abs(x))} %"; q = x if abs(x) >= 0.5 else 0
    if abs(q) < 0.005: return '<span class="pk-d eq"><span aria-hidden="true">=</span> igual</span>'
    up = q > 0
    return f'<span class="pk-d {"up" if up else "dn"}"><span aria-hidden="true">{"▲" if up else "▼"}</span> {"+" if up else "−"}{txt}<span class="sr"> {"más" if up else "menos"} que antes</span></span>'

def pulso_html(live=None, slug=None, today=None):
    """Bloque «Pulso: datos de hoy» (home, slug=None) o «Dato de hoy» (calculadora afín). '' si no hay datos frescos."""
    live = live if live is not None else load_live()
    items = pulso_items(live, today)
    if slug is None: sel = [i for i in items if i["id"] in PULSO_HOME][:3]
    else: sel = [i for i in items if slug in PULSO_CALCS[i["id"]]][:3]
    if not sel: return ""
    li = []
    for it in sel:
        calcs = PULSO_CALCS[it["id"]]
        link = f'<a href="/decidir/{calcs[0]}/">{"Calcula tu caso" if slug is None else "Ver calculadora"}</a>'
        if slug is None and len(calcs) > 1: link += f' · <a href="/decidir/{calcs[1]}/">{PULSO_LABEL.get(calcs[1], "Otra calculadora")}</a>'
        fecha = it["fecha"]
        when = f'<time datetime="{fecha}">{it.get("fecha_txt") or _fmt_fecha(fecha)}</time>'
        d0 = it["datos"][0]; vt, un = _pulso_valor(it["id"], d0)
        dl = _pulso_delta(it["id"], d0)
        li.append(f'<li class="pk pk-{it["id"]}"><span class="pk-h"><svg class="pk-i" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{PULSO_ICON[it["id"]]}</svg><strong>{it["titulo"]}</strong></span>'
                  f'<span class="pk-v">{vt} <small>{un}</small></span>{dl}'
                  f'<span class="pk-t">{html.escape(it["texto"])}</span>'
                  f'<span class="pulso-meta">Dato de {when}. Fuente: <a href="{it["fuente"]["url"]}" rel="noopener">{html.escape(it["fuente"]["nombre"])}</a>.</span> <span class="pk-l">{link}</span></li>')
    h = "Pulso: datos de hoy" if slug is None else "Dato de hoy"
    tag = "h2" if slug is None else "h3"
    nota = ' <span class="pulso-meta">Previsión del tiempo: <a href="https://open-meteo.com/" rel="noopener">Open-Meteo</a> (CC BY 4.0).</span>' if any(i["id"] == "tiempo" for i in sel) else ""
    return f'<aside class="pulso box" aria-label="{h}"><{tag}>{h}</{tag}><ul>{"".join(li)}</ul>{nota}</aside>\n'


# ---------- Calendario de eventos (data/events.json) y banner «Ahora» ----------
EVENTS_PATH = os.path.join(ROOT, "data/events.json")

def load_events(path=EVENTS_PATH):
    """Eventos con fuente oficial. Descarta los que no tengan fuente https (regla: ninguno sin fuente)."""
    try:
        ev = json.load(open(path)).get("eventos", [])
    except Exception:
        return []
    return [e for e in ev if str(e.get("fuente", {}).get("url", "")).startswith("https://") and e.get("calc") and e.get("titulo")]

def load_pendientes(path=EVENTS_PATH):
    """Lo que llegará sin fecha verificable (pendiente de norma o de notificación): solo para /calendario/, nunca en el banner."""
    try:
        pe = json.load(open(path)).get("pendientes", [])
    except Exception:
        return []
    return [e for e in pe if str(e.get("fuente", {}).get("url", "")).startswith("https://") and e.get("calc") and e.get("titulo") and e.get("aviso")]

def _d(iso): return datetime.date.fromisoformat(iso)

def _ocurrencias(e, hoy):
    """Ocurrencias {inicio, fin, fecha} del evento alrededor de `hoy` (año anterior, actual y siguiente)."""
    out = []
    t = e.get("tipo")
    if t == "fechas":
        for f in e.get("fechas", []):
            d = _d(f); out.append(dict(inicio=d - datetime.timedelta(days=e.get("antes", 7)), fin=d + datetime.timedelta(days=e.get("despues", 3)), fecha=d))
    elif t == "anual":
        mi, di = map(int, e["desde"].split("-")); mf, df = map(int, e["hasta"].split("-"))
        for y in (hoy.year - 1, hoy.year, hoy.year + 1):
            out.append(dict(inicio=datetime.date(y, mi, di), fin=datetime.date(y, mf, df), fecha=None))
    elif t == "mensual":
        for k in range(-1, 14):
            y, m = divmod(hoy.year * 12 + hoy.month - 1 + k, 12)
            out.append(dict(inicio=datetime.date(y, m + 1, e.get("dia_desde", 1)), fin=datetime.date(y, m + 1, e.get("dia_hasta", 10)), fecha=None))
    return sorted(out, key=lambda o: o["inicio"])

def eventos_estado(hoy=None, events=None):
    """Para cada evento, su ocurrencia activa o la próxima: dict(evento, inicio, fin, fecha, activo). Activos primero."""
    hoy = hoy or datetime.date.today()
    res = []
    for e in (load_events() if events is None else events):
        occ = _ocurrencias(e, hoy)
        act = [o for o in occ if o["inicio"] <= hoy <= o["fin"]]
        nxt = [o for o in occ if o["inicio"] > hoy]
        o = act[0] if act else (nxt[0] if nxt else None)
        if o: res.append(dict(o, evento=e, activo=bool(act)))
    return sorted(res, key=lambda r: (not r["activo"], r["inicio"]))

def eventos_activos(fecha=None, events=None):
    """Eventos cuya ventana de relevancia incluye `fecha` (date o 'YYYY-MM-DD'; por defecto hoy)."""
    if isinstance(fecha, str): fecha = _d(fecha)
    return [r for r in eventos_estado(fecha, events) if r["activo"]]

def _texto_ahora(r, hoy):
    e = r["evento"]
    if r["fecha"] is None: return e["texto"]
    k = "texto_antes" if r["fecha"] >= hoy else "texto_despues"
    return e[k].replace("{fecha}", fecha_es(r["fecha"].isoformat()).rsplit(" de ", 1)[0])

def ahora_html(slug=None, hoy=None, events=None):
    """Banner discreto «Ahora: …» (home con slug=None, o calculadora afín). '' si no hay evento activo. Máx. 1."""
    hoy = hoy or datetime.date.today()
    act = eventos_activos(hoy, events)
    if slug is not None: act = [r for r in act if r["evento"]["calc"] == slug]
    if not act: return ""
    r = act[0]; e = r["evento"]
    link = f'<a href="/decidir/{e["calc"]}/">Calcula tu caso</a>' if slug is None else '<a href="/calendario/">Calendario</a>'
    return (f'<p class="ahora note"><strong>Ahora:</strong> {html.escape(_texto_ahora(r, hoy))} {link}'
            + (' · <a href="/calendario/">Calendario</a>' if slug is None else "")
            + f' <span class="pulso-meta">Fuente: <a href="{e["fuente"]["url"]}" rel="noopener">{html.escape(e["fuente"]["nombre"])}</a>.</span></p>\n')

def _rango_es(a, b):
    if a.year == b.year: return f"{a.day} de {MESES_ES[a.month - 1]} al {b.day} de {MESES_ES[b.month - 1]} de {b.year}"
    return f"{_fmt_fecha(a.isoformat())} al {_fmt_fecha(b.isoformat())}"

def calendario_page(calcs, base, hoy=None, events=None):
    """(body, jsonld, lastmod) de /calendario/. Event JSON-LD solo si la ocurrencia tiene fecha concreta."""
    hoy = hoy or datetime.date.today()
    est = eventos_estado(hoy, events)
    names = {c["slug"]: c["h1"] for c in calcs}
    items, ld = [], []
    for r in est:
        e = r["evento"]
        if e["calc"] not in names: continue
        if r["fecha"]:
            cuando = f'<time datetime="{r["fecha"].isoformat()}">{fecha_es(r["fecha"].isoformat())}</time>'
            if e.get("tipo") == "fechas" and len(e["fechas"]) > 1:
                sig = [f for f in e["fechas"] if _d(f) > r["fecha"]][:1]
                if sig: cuando += f' (siguiente: <time datetime="{sig[0]}">{fecha_es(sig[0])}</time>)'
            if e.get("estado") != "por confirmar": ld.append({"@context": "https://schema.org", "@type": "Event", "name": e["titulo"], "startDate": r["fecha"].isoformat(),
                       "endDate": r["fecha"].isoformat(), "eventStatus": "https://schema.org/EventScheduled",
                       "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
                       "location": {"@type": "VirtualLocation", "url": f'{base}/decidir/{e["calc"]}/'},
                       "description": e["que_hacer"], "url": f"{base}/calendario/", "organizer": {"@type": "Organization", "name": "Entre Muchos", "url": base + "/"}})
        else:
            cuando = f'<time datetime="{r["inicio"].isoformat()}">{_rango_es(r["inicio"], r["fin"])}</time>'
            if e.get("periodo_habitual"): cuando += f' · periodo habitual: {e["periodo_habitual"]}'
        estado = ('<span class="pulso-meta">Activo ahora</span>' if r["activo"] else "") + (' <span class="pulso-meta">Fecha por confirmar</span>' if e.get("estado") == "por confirmar" else "")
        items.append(f'<article class="box"><h2>{html.escape(e["titulo"])}</h2><p class="note">{cuando} {estado}</p>'
                     f'<p><strong>Decisión que toca:</strong> {html.escape(e["decision"])}.</p><p><strong>Qué hacer:</strong> {html.escape(e["que_hacer"])}</p>'
                     f'<p><a href="/decidir/{e["calc"]}/">{html.escape(names[e["calc"]])}</a></p>'
                     f'<p class="note">{html.escape(e["aviso"])} Fuente: <a href="{e["fuente"]["url"]}" rel="noopener">{html.escape(e["fuente"]["nombre"])}</a>.</p></article>')
    # «pendientes» de events.json: sin fecha verificable (pendiente de norma o de notificación); solo aquí, nunca en el banner
    pend = [e for e in load_pendientes() if e["calc"] in names] if events is None else []
    ptxt = ("<h2>Pendiente de fecha o de norma</h2><p>Lo que llegará pero aún no tiene fecha oficial ni cifras publicadas. No damos fecha hasta que exista la norma o la notificación.</p>"
            + "".join(f'<article class="box"><h3>{html.escape(e["titulo"])}</h3><p class="note"><span class="pulso-meta">Pendiente de norma o de fecha</span></p>'
                      f'<p><strong>Decisión que toca:</strong> {html.escape(e["decision"])}.</p><p><strong>Qué hacer:</strong> {html.escape(e["que_hacer"])}</p>'
                      f'<p><a href="/decidir/{e["calc"]}/">{html.escape(names[e["calc"]])}</a></p>'
                      f'<p class="note">{html.escape(e["aviso"])} Fuente: <a href="{e["fuente"]["url"]}" rel="noopener">{html.escape(e["fuente"]["nombre"])}</a>.</p></article>' for e in pend)) if pend else ""
    body = ('<h1>Calendario de decisiones</h1><p class="lead">Fechas que mueven una decisión de dinero en España, con su fuente oficial: '
            'cuándo mirar tu hipoteca, tu calefacción, tu declaración, tu cuota de autónomo o una compra a plazos. Solo incluimos lo que podemos verificar; '
            'lo recurrente sin fecha oficial se marca como periodo habitual o «por confirmar», y lo que depende de una norma aún no publicada va al final, sin fecha. '
            'Tablas con las cifras oficiales de 2026: <a href="/tablas-2026/">Tablas 2026</a>.</p>' + "".join(items) + ptxt
            + '<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a>.</p>')
    jl = [breadcrumbs(base, [("Inicio", "/"), ("Calendario", None)])] + ld
    return body, jl, lastmod("data/events.json", "seo.py")


# ---------- Actualidad: notas por disparador (content/actualidad/*.html, generadas por ops/triggers.py) ----------
def load_actualidad(path=os.path.join(ROOT, "content/actualidad")):
    out = []
    if not os.path.isdir(path): return out
    for f in sorted(os.listdir(path), reverse=True):
        if not f.endswith(".html"): continue
        raw = open(os.path.join(path, f)).read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m: continue
        n = json.loads(m.group(1)); n["slug"] = f[:-5]; n["body"] = raw[m.end():]
        n.setdefault("modified", n["published"])
        out.append(n)
    return out

def actualidad_index(notes):
    return ('<h1>Actualidad</h1><p class="lead">Notas breves cuando un dato oficial se mueve lo bastante como para cambiar una decisión. '
            'Cada nota sale de una regla objetiva y lleva su dato, su fecha y su fuente.</p><ul class="cards">' + "".join(
        f'<li><a href="/actualidad/{n["slug"]}/">{n["h1"]}</a><p><time datetime="{n["published"]}">{fecha_es(n["published"])}</time> · {n["description"]}</p></li>' for n in notes) + "</ul>")

def actualidad_page(n, calcs, card, base):
    rel = [c for c in calcs if c["slug"] == n.get("calc")]
    calc_block = ('<h2>Calcúlalo con tus números</h2><ul class="cards">' + "".join(card(c) for c in rel) + "</ul>") if rel else ""
    body = f"""<article class="guide">
<p class="kicker"><a href="/actualidad/">Actualidad</a></p>
<h1>{n["h1"]}</h1>
<p class="byline note">Por {AUTHOR} · <time datetime="{n["published"]}">{fecha_es(n["published"])}</time></p>
{n["body"]}
<p class="disclaimer">Nota generada a partir de datos oficiales con una regla objetiva ({html.escape(n.get("regla", ""))}); sin opinión. Información orientativa, no constituye asesoramiento financiero. Lee nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{calc_block}
</article>"""
    url = f"{base}/actualidad/{n['slug']}/"
    art = article(n["h1"], n["description"], url, n["published"], n["modified"], base)
    art["@type"] = "NewsArticle"
    return body, [art, breadcrumbs(base, [("Inicio", "/"), ("Actualidad", "/actualidad/"), (n["h1"], None)])]

def actualidad_link(notes):
    """Enlace discreto a la última nota; '' si no hay notas (así /actualidad/ solo se enlaza si existe)."""
    if not notes: return ""
    n = notes[0]
    return f'<p class="note actualidad-link">Actualidad: <a href="/actualidad/{n["slug"]}/">{n["h1"]}</a> (<time datetime="{n["published"]}">{fecha_es(n["published"])}</time>) · <a href="/actualidad/">Todas las notas</a></p>\n'
