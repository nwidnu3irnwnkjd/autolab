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
    return lastmod(*calc_files(slug), extra=[params.get("fecha", "")])


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
    out = {}
    for c in calcs:
        scored = sorted(((10 * (tema(x) == tema(c)) + NEAR.get(tema(c), {}).get(tema(x), 0) + len(_tokens(x) & _tokens(c)), x["slug"])
                         for x in calcs if x["slug"] != c["slug"]), key=lambda t: (-t[0], t[1]))
        top = [s for sc, s in scored if sc >= 10][:k]
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
    gdir = os.path.join(ROOT, "content/guias"); out = []
    if not os.path.isdir(gdir): return out
    for f in sorted(os.listdir(gdir)):
        if not f.endswith(".html"): continue
        raw = open(os.path.join(gdir, f)).read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m: continue
        g = json.loads(m.group(1)); g["slug"] = f[:-5]
        body = raw[m.end():]
        for k, v in params.items():  # {{clave}} -> valor de data/params.json (cifras = datos)
            if isinstance(v, (int, float)): v = f"{v:.2f}".replace(".", ",") if isinstance(v, float) else str(v)
            if isinstance(v, str): body = body.replace("{{" + k + "}}", v)
        g["body"] = body
        rel = f"content/guias/{f}"
        g["modified"] = lastmod(rel, extra=[params.get("fecha", "")] if "{{" in raw else [])
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
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Revisa tu escritura y, si la decisión es importante, consulta con un profesional. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{calc_block}
</article>"""
    url = f"{base}/guias/{g['slug']}/"
    jsonld = [article(g["h1"], g["description"], url, g["published"], g["modified"], base),
              breadcrumbs(base, [("Inicio", "/"), ("Guías", "/guias/"), (g["h1"], None)])]
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

def write_llms(dist, site, calcs, guides, params, tema, icons, extra=""):
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
    if guides:
        lines.append("\n## Guías\n")
        lines += [f"- [{g['h1']}]({base}/guias/{g['slug']}/): {g['description']}" for g in guides]
    if extra:  # Barómetro: datos propios fechados
        lines.append("\n## Datos propios\n")
        lines.append(f"- [Barómetro Entre Muchos]({base}/barometro/): Euríbor de equilibrio fija/variable, coste por km según motor y rentabilidad para que invertir compense frente a amortizar, actualizado cada mes. Datos en JSON: {base}/barometro/datos.json")
    lines.append(f"\n## Optional\n\n- [Texto completo para LLMs]({base}/llms-full.txt): preguntas, criterios de decisión, parámetros y fuentes de cada calculadora.\n"
                 f"- [Catálogo]({base}/decidir/): todas las calculadoras por tema.\n")
    open(os.path.join(dist, "llms.txt"), "w").write("\n".join(lines))

    full = [head]
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
    for g in guides:
        full.append(f"\n---\n\n## {g['h1']}\n\nURL: {base}/guias/{g['slug']}/\nActualizado: {g['modified']}\n\n{html_to_md(g['body'], base)}\n")
    open(os.path.join(dist, "llms-full.txt"), "w").write("\n".join(full))


def insert_before(page, marker, block):
    """Inserta block antes de la primera aparición de marker (o al final si no está). Evita tocar plantillas ajenas."""
    return page.replace(marker, block + marker, 1) if marker in page else page + block

def copy_static(dist):
    s = os.path.join(ROOT, "static")
    if os.path.isdir(s): shutil.copytree(s, dist, dirs_exist_ok=True)
