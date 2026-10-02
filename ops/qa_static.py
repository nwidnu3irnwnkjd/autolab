#!/usr/bin/env python3
"""QA estática determinista (T3/T7.3/T9). Solo stdlib. Sustituye las comprobaciones estáticas del QA Haiku.

Uso:
  python3 ops/qa_static.py                      # todo el sitio (projects/decidir/dist)
  python3 ops/qa_static.py --changed            # YMYL/cifras solo de lo cambiado + lista de rutas dist para el QA con navegador
  python3 ops/qa_static.py --dist DIR           # apunta a otra carpeta dist (pruebas)
  python3 ops/qa_static.py --project decidir
  python3 ops/qa_static.py --fiscal             # T14 v3: control de «solo cifras verificadas» en calculadoras fiscales (sin dist)
  python3 ops/qa_static.py --fiscal --changed   # idem, solo calculadoras cambiadas (git)

Salida: `BLOQUEANTE|AVISO|OK · archivo:línea · mensaje`. Exit 1 solo si hay BLOQUEANTE.
Parseadores: xml.etree (sitemap), html.parser (title, description, canonical, h1, JSON-LD, enlaces), json.loads. Sin regex para estructuras.
"""
import datetime, glob, gzip, html, json, os, re, subprocess, sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

OPS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OPS)
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
PESO_AVISO = 60 * 1024   # raw: solo INFO (no cuenta como AVISO)
GZIP_AVISO = 30 * 1024   # peso transferido (gzip -6, como GitHub Pages): AVISO
PESO_BLOQ = int(float(os.environ.get("QA_PESO_BLOQ_KB", 90)) * 1024)  # raw: informativo (INFO). Manda el gzip:
GZIP_BLOQ = int(float(os.environ.get("QA_GZIP_BLOQ_KB", 60)) * 1024)  # BLOQUEANTE si el peso transferido gzip supera esto (override explícito)
MAX_EDAD, MAX_EDAD_ID = 7, {"euribor12m": 45}

def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else default

PROJ = arg("--project", "decidir")
PDIR = os.path.join(ROOT, "projects", PROJ)
DIST = os.path.abspath(arg("--dist", os.path.join(PDIR, "dist")))
CHANGED = "--changed" in sys.argv
FISCAL = "--fiscal" in sys.argv

out = []  # (nivel, ubicación, mensaje)
def add(level, where, msg): out.append((level, where, msg))
def rel(p):
    try: return os.path.relpath(p, ROOT)
    except ValueError: return p

# ---------- parseo de una página ----------
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None; self.title_line = 0; self._in_title = False
        self.desc = None; self.canon = None; self.og_image = None
        self.h1 = []; self._in_h1 = False
        self.ld = []; self._in_ld = False; self._ld_buf = ""; self._ld_line = 0
        self.links = []   # (attr, valor, línea)
        self.css = []; self.js = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); line = self.getpos()[0]
        if tag == "title": self._in_title = True; self.title = ""; self.title_line = line
        elif tag == "h1": self._in_h1 = True; self.h1.append(line)
        elif tag == "meta":
            n = (a.get("name") or "").lower(); p = (a.get("property") or "").lower()
            if n == "description": self.desc = a.get("content", "")
            if n == "robots" and "noindex" in (a.get("content") or "").lower(): self.noindex = True
            if p == "og:image": self.og_image = a.get("content", "")
        elif tag == "link":
            rl = (a.get("rel") or "").lower()
            if rl == "canonical": self.canon = a.get("href", "")
            if rl == "stylesheet" and a.get("href"):
                if (a.get("media") or "").lower() != "print": self.css.append(a["href"])
        elif tag == "script":
            if (a.get("type") or "").lower() == "application/ld+json":
                self._in_ld = True; self._ld_buf = ""; self._ld_line = line
            elif a.get("src"): self.js.append(a["src"])
        if tag in ("a", "link", "img", "script", "source", "iframe") :
            for k in ("href", "src"):
                if a.get(k) is not None: self.links.append((k, a[k], line))

    def handle_endtag(self, tag):
        if tag == "title": self._in_title = False
        elif tag == "h1": self._in_h1 = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False; self.ld.append((self._ld_line, self._ld_buf))

    def handle_data(self, d):
        if self._in_title and self.title is not None: self.title += d
        if self._in_ld: self._ld_buf += d

def parse(path):
    p = Page(); p.feed(open(path, encoding="utf-8").read()); p.close(); return p

def local(url):
    """Ruta local (con / inicial) de una URL interna o de nuestro dominio; None si es externa/otra."""
    if url.startswith("//") or url.startswith("data:") or url.startswith("mailto:") or url.startswith("tel:") or url.startswith("javascript:"): return None
    u = urlparse(url)
    if u.scheme in ("http", "https"):
        if u.netloc != HOST: return None
    elif u.scheme: return None
    return u.path or None

def exists_in_dist(path):
    p = path.split("?")[0].split("#")[0]
    if not p.startswith("/"): return True  # relativas: fuera de alcance
    fs = os.path.join(DIST, p.lstrip("/"))
    if p.endswith("/") or p == "": return os.path.isfile(os.path.join(fs, "index.html"))
    return os.path.isfile(fs) or os.path.isfile(os.path.join(fs, "index.html"))

def page_url_path(index_html):
    r = os.path.relpath(index_html, DIST).replace(os.sep, "/")
    return "/" + (r[:-len("index.html")] if r.endswith("index.html") else r)

# ---------- configuración ----------
try:
    SITE = json.load(open(os.path.join(PDIR, "data/site.json")))
    BASE = SITE["base_url"].rstrip("/")
except Exception:
    BASE = "https://entremuchos.com"
HOST = urlparse(BASE).netloc

# ---------- páginas cambiadas (git) ----------
def git_changed():
    """Rutas (relativas a la raíz del repo) cambiadas respecto a HEAD, incl. nuevas sin seguimiento."""
    try:
        a = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
        b = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
        return sorted({x for x in a + b if x.strip()})
    except Exception:
        return []

def changed_pages(files):
    """(slugs_cambiados:set, global:bool, rutas_dist:list). Mapa por nombre de archivo -> directorio de dist con ese nombre."""
    dirs = {}
    for idx in glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True):
        pth = page_url_path(idx); dirs.setdefault(pth.strip("/").split("/")[-1] or "home", []).append(pth)
    prefix = f"projects/{PROJ}/"
    slugs, paths, glob_change = set(), set(), False
    for f in files:
        if not f.startswith(prefix): continue
        r = f[len(prefix):]
        top = r.split("/")[0]
        if top in ("calcs", "content"):
            stem = os.path.basename(r).split(".")[0]
            slugs.add(stem)
            for pth in dirs.get(stem, []): paths.add(pth)
            if top == "content" and "/actualidad/" in "/" + r: paths.add("/actualidad/")
            if top == "content" and "/guias/" in "/" + r: paths.add("/guias/")
        elif top in ("templates", "assets", "static") or r in ("build.py", "ui.py", "seo.py", "bundle.py", "minify.py", "ogimg.py", "calcs_loader.py", "barometro.py"):
            glob_change = True
        elif top == "data":
            if r.endswith(("live.json", "params.json")): glob_change = True
            if r.endswith("clusters.json"): glob_change = True
    return slugs, glob_change, sorted(paths)

# ---------- comprobaciones de dist ----------
def check_pages(only_urls=None):
    pages = sorted(glob.glob(os.path.join(DIST, "**", "index.html"), recursive=True))
    if os.path.isfile(os.path.join(DIST, "404.html")): pages.append(os.path.join(DIST, "404.html"))
    n_checks = 0; indexables = []
    for f in pages:
        name = rel(f) if not f.startswith(DIST) else "dist/" + os.path.relpath(f, DIST)
        is404 = os.path.basename(f) == "404.html"
        p = parse(f); size_html = os.path.getsize(f)
        urlp = "/404.html" if is404 else page_url_path(f)
        # title
        if p.title is None or not p.title.strip(): add("BLOQUEANTE", f"{name}:1", "falta <title>")
        else:
            t = html.unescape(p.title).strip(); n_checks += 1
            if len(t) > 60: add("BLOQUEANTE", f"{name}:{p.title_line}", f"title de {len(t)} caracteres (máx. 60): «{t}»")
        # description
        if p.desc is None or not p.desc.strip():
            add("BLOQUEANTE" if not is404 else "AVISO", f"{name}:1", "falta meta description")
        else:
            d = html.unescape(p.desc).strip(); n_checks += 1
            if len(d) > 155: add("BLOQUEANTE", f"{name}:1", f"description de {len(d)} caracteres (máx. 155)")
        # canonical
        if not is404:
            n_checks += 1
            if not p.canon: add("BLOQUEANTE", f"{name}:1", "falta canonical")
            else:
                lp = local(p.canon)
                if lp is None: add("BLOQUEANTE", f"{name}:1", f"canonical fuera del dominio: {p.canon}")
                elif urlp.startswith("/embed/"):  # widget insertable (embed.py): noindex y canonical a la calculadora completa; HTML <= 40 KB
                    if lp != "/decidir/" + urlp[len("/embed/"):]: add("BLOQUEANTE", f"{name}:1", f"canonical del embed {lp} no apunta a su calculadora completa")
                    if not p.noindex: add("BLOQUEANTE", f"{name}:1", "el embed debe ser noindex,follow")
                    if size_html > 40960: add("BLOQUEANTE", f"{name}:1", f"embed de {size_html/1024:.1f} KB > 40 KB")
                elif lp != urlp: add("BLOQUEANTE", f"{name}:1", f"canonical {lp} no coincide con la ruta de la página {urlp}")
        # h1
        n_checks += 1
        if len(p.h1) != 1: add("BLOQUEANTE", f"{name}:{(p.h1 or [1])[0]}", f"{len(p.h1)} elementos h1 (debe haber 1)")
        # JSON-LD
        for line, buf in p.ld:
            n_checks += 1
            try:
                data = json.loads(buf)
            except Exception as e:
                add("BLOQUEANTE", f"{name}:{line}", f"JSON-LD inválido: {e}"); continue
            items = data if isinstance(data, list) else [data]
            for it in items:
                if isinstance(it, dict) and "@graph" in it: items = items + list(it["@graph"])
            for it in items:
                if not isinstance(it, dict) or ("@type" not in it and "@graph" not in it):
                    add("BLOQUEANTE", f"{name}:{line}", "JSON-LD sin @type")
        # og:image
        if p.og_image:
            n_checks += 1
            lp = local(p.og_image)
            if lp is None: add("AVISO", f"{name}:1", f"og:image fuera del dominio: {p.og_image}")
            elif not exists_in_dist(lp): add("BLOQUEANTE", f"{name}:1", f"og:image no existe en dist: {lp}")
        elif not is404 and not p.noindex:
            add("AVISO", f"{name}:1", "sin og:image")
        # enlaces internos y assets
        seen = set()
        for k, v, line in p.links:
            lp = local(v)
            if lp is None or not lp.startswith("/"): continue
            if lp in seen: continue
            seen.add(lp); n_checks += 1
            if not exists_in_dist(lp): add("BLOQUEANTE", f"{name}:{line}", f"enlace interno roto ({k}): {v}")
        # peso cargado (HTML + css + js locales, sin print.css)
        total = size_html; parts = [f"html {size_html/1024:.1f}"]
        gz = len(gzip.compress(open(f, "rb").read(), 6)) if os.path.isfile(f) else 0
        for a in p.css + p.js:
            lp = local(a)
            if not lp or "print.css" in lp: continue
            fp = os.path.join(DIST, lp.lstrip("/"))
            if os.path.isfile(fp):
                total += os.path.getsize(fp); gz += len(gzip.compress(open(fp, "rb").read(), 6)); parts.append(f"{os.path.basename(lp)} {os.path.getsize(fp)/1024:.1f}")
        n_checks += 1
        if not is404:
            if gz > GZIP_BLOQ: add("BLOQUEANTE", f"{name}:1", f"peso transferido gzip {gz/1024:.1f} KB > {GZIP_BLOQ/1024:g} KB (raw {total/1024:.1f} KB; {', '.join(parts)})")
            elif total > PESO_BLOQ: add("INFO", f"{name}:1", f"peso cargado {total/1024:.1f} KB raw > {PESO_BLOQ/1024:g} KB (informativo; manda gzip {gz/1024:.1f} KB) ({', '.join(parts)})")
            elif total > PESO_AVISO: add("INFO", f"{name}:1", f"peso cargado {total/1024:.1f} KB raw > 60 KB ({', '.join(parts)}); gzip {gz/1024:.1f} KB")
            if gz > GZIP_AVISO: add("AVISO", f"{name}:1", f"peso transferido gzip {gz/1024:.1f} KB > 30 KB (raw {total/1024:.1f} KB)")
        if not is404 and not p.noindex: indexables.append(urlp)
    return pages, indexables, n_checks

def check_sitemap(indexables):
    sm = os.path.join(DIST, "sitemap.xml")
    if not os.path.isfile(sm): add("BLOQUEANTE", "dist/sitemap.xml:1", "no existe sitemap.xml"); return 0
    try:
        root = ET.parse(sm).getroot()
        if root.tag == SM_NS + "sitemapindex":  # índice -> sitemap-<sección>.xml (c50)
            locs = []
            for sl in root.iter(SM_NS + "loc"):
                lp = local(sl.text.strip()); fp = os.path.join(DIST, (lp or "/").strip("/"))
                if lp is None or not os.path.isfile(fp): add("BLOQUEANTE", "dist/sitemap.xml:1", f"sitemap hijo inexistente: {sl.text.strip()}"); continue
                locs += [l.text.strip() for l in ET.parse(fp).iter(SM_NS + "loc")]
        else:
            locs = [l.text.strip() for l in root.iter(SM_NS + "loc")]
    except ET.ParseError as e:
        add("BLOQUEANTE", "dist/sitemap.xml:1", f"XML inválido: {e}"); return 0
    paths = {}
    for l in locs:
        lp = local(l)
        if lp is None: add("BLOQUEANTE", "dist/sitemap.xml:1", f"loc fuera del dominio: {l}"); continue
        paths[lp] = l
        if not exists_in_dist(lp): add("BLOQUEANTE", "dist/sitemap.xml:1", f"loc sin página en dist: {l}")
    for u in indexables:
        if u not in paths: add("BLOQUEANTE", "dist" + u + "index.html:1", f"página indexable que no está en sitemap.xml")
    return len(locs)

def check_files():
    for f in ("llms.txt", "robots.txt"):
        fp = os.path.join(DIST, f)
        if not os.path.isfile(fp) or os.path.getsize(fp) == 0: add("BLOQUEANTE", f"dist/{f}:1", "falta o vacío")
    fp = os.path.join(DIST, "barometro/datos.json")
    if not os.path.isfile(fp): add("BLOQUEANTE", "dist/barometro/datos.json:1", "no existe")
    else:
        try: json.load(open(fp, encoding="utf-8"))
        except Exception as e: add("BLOQUEANTE", "dist/barometro/datos.json:1", f"JSON inválido: {e}")

# ---------- datos vivos ----------
def check_live():
    lp = os.path.join(PDIR, "data/live.json")
    try: live = json.load(open(lp, encoding="utf-8"))["datos"]
    except Exception as e:
        add("BLOQUEANTE", rel(lp) + ":1", f"live.json ilegible: {e}"); return 0
    today = datetime.datetime.now(datetime.timezone.utc).date(); n = 0
    for cf in sorted(glob.glob(os.path.join(PDIR, "calcs/*.json"))):
        if cf.endswith(".test.json"): continue
        try: c = json.load(open(cf, encoding="utf-8"))
        except Exception as e: add("BLOQUEANTE", rel(cf) + ":1", f"JSON inválido: {e}"); continue
        for inp in c.get("inputs", []):
            df = inp.get("default_from", "")
            if not df.startswith("live."): continue
            n += 1; ident = df.split(".")[1]; sub = df.split(".")[2:]
            d = live.get(ident); w = f"{rel(cf)}:{inp.get('id')}"
            if d is None: add("BLOQUEANTE", w, f"default_from {df}: no existe «{ident}» en live.json"); continue
            v = d
            try:
                v = d["valor"] if not sub else d
                for k in sub: v = v[k]
            except (KeyError, TypeError):
                add("BLOQUEANTE", w, f"default_from {df}: la subruta no resuelve"); continue
            if not d.get("ok"): add("AVISO", w, f"{df}: dato vivo no ok (el build usa default_fallback)"); continue
            try: age = (today - datetime.date.fromisoformat(d.get("fecha_dato") or d.get("fecha_consulta"))).days
            except Exception: add("AVISO", w, f"{df}: sin fecha_dato legible"); continue
            lim = inp.get("max_edad_dias", MAX_EDAD_ID.get(ident, MAX_EDAD))
            if age > lim: add("AVISO", w, f"{df}: dato de hace {age} d (> {lim} d); el build usa default_fallback")
    return n

# ---------- YMYL determinista (T9) ----------
LEGAL = re.compile(r"\b(Ley|BOE|RDL|Orden|RD|Real Decreto)\b|\bart\.|%|€")
NUM = re.compile(r"\d[\d.,]*\d|\d")

def strip_tags(s): return html.unescape(re.sub(r"<[^>]+>", " ", s))

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡0-9])", re.sub(r"\s+", " ", text)) if s.strip()]

def ymyl_html(path, name):
    """Secciones por h2/h3: frases con referencia legal/cifra y sin enlace http en la sección."""
    raw = open(path, encoding="utf-8").read()
    parts = list(re.finditer(r"<h[23][^>]*>", raw))
    bounds = [(0, 1)] + [(m.start(), raw.count("\n", 0, m.start()) + 1) for m in parts]
    for i, (st, line) in enumerate(bounds):
        en = bounds[i + 1][0] if i + 1 < len(bounds) else len(raw)
        sec = raw[st:en]
        if re.search(r'href="https?://', sec): continue
        sec_text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", sec, flags=re.S)
        hits = [s for s in sentences(strip_tags(sec_text)) if LEGAL.search(s)]
        if hits:
            ej = hits[0][:90] + ("…" if len(hits[0]) > 90 else "")
            add("AVISO", f"{name}:{line}", f"YMYL: {len(hits)} frase(s) con ley/%/€ sin enlace a fuente en la sección (p. ej. «{ej}»)")

ART = re.compile(r"\b[Aa]rt(?:[íi]culos?|s?\.)\s*\d+(?:\.\d+)?(?:\s*(?:,|y|e|a)\s*\d+(?:\.\d+)?)*")

def num_vals(text):
    vals = set(); text = ART.sub(" ", text)   # los números de artículo no son cifras de cálculo
    for m in NUM.findall(text):
        s = m
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", s): s = s.replace(".", "")          # 9.040 -> 9040
        elif "," in s: s = s.replace(".", "").replace(",", ".")                    # 2,8 / 1.234,5
        s = s.rstrip(".,")
        try: v = float(s)
        except ValueError: continue
        vals.add(round(v, 6))
    return vals

def corpus_numbers(slug):
    corp = set()
    def walk(o):
        if isinstance(o, bool): return
        if isinstance(o, (int, float)): corp.add(round(float(o), 6))
        elif isinstance(o, str): corp.update(num_vals(o))
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for f in (os.path.join(PDIR, "data/params.json"), os.path.join(PDIR, "data/live.json"),
              os.path.join(PDIR, f"calcs/{slug}.test.json")):
        try: walk(json.load(open(f, encoding="utf-8")))
        except Exception: pass
    try:
        c = json.load(open(os.path.join(PDIR, f"calcs/{slug}.json"), encoding="utf-8"))
        walk(c.get("inputs", [])); walk(c.get("sources", ""))   # defaults, límites y supuestos declarados en fuentes
    except Exception: pass
    return corp

def covered(v, corp):
    for x in (v, v * 100, v / 100):
        if any(abs(x - c) <= max(1e-6, abs(c) * 1e-4) for c in corp): return True
    return False

def ymyl_calc(cf, slug, check_numbers=True):
    name = rel(cf)
    try: c = json.load(open(cf, encoding="utf-8"))
    except Exception: return
    has_src = bool(re.search(r"https?://", c.get("sources", "")))
    texts = [("lead", c.get("lead", "")), ("veredicto", c.get("veredicto", ""))] + \
            [(f"faq{i+1}", (q[1] if len(q) > 1 else "")) for i, q in enumerate(c.get("faqs", []))]
    if not has_src:
        n = sum(1 for _, t in texts for s in sentences(strip_tags(t)) if LEGAL.search(s))
        if n: add("AVISO", name + ":sources", f"YMYL: {n} frase(s) con ley/%/€ y «sources» sin ningún enlace a fuente")
    if check_numbers:
        corp = corpus_numbers(slug); sueltos = []
        for lab, t in texts:
            for v in num_vals(strip_tags(t)):
                if v == int(v) and (abs(v) < 10 or 1900 <= v <= 2100): continue   # recuentos pequeños y años
                if not covered(v, corp): sueltos.append(f"{lab}:{v:g}")
        if sueltos: add("AVISO", name + ":texto", f"YMYL: números del texto que no salen de params/live/tests/inputs/fuentes: {', '.join(sueltos[:12])}" + (" …" if len(sueltos) > 12 else ""))

def check_ymyl(slugs):
    n = 0
    if slugs is None:
        cfs = [f for f in sorted(glob.glob(os.path.join(PDIR, "calcs/*.json"))) if not f.endswith(".test.json")]
        htmls = sorted(glob.glob(os.path.join(PDIR, "content/**/*.html"), recursive=True))
    else:
        cfs = [os.path.join(PDIR, f"calcs/{s}.json") for s in sorted(slugs) if os.path.isfile(os.path.join(PDIR, f"calcs/{s}.json")) and not s.endswith(".test")]
        htmls = [h for h in sorted(glob.glob(os.path.join(PDIR, "content/**/*.html"), recursive=True)) if os.path.basename(h).split(".")[0] in slugs]
    for cf in cfs:
        ymyl_calc(cf, os.path.basename(cf)[:-5]); n += 1
    for h in htmls:
        ymyl_html(h, rel(h)); n += 1
    return n


# ---------- T14 v3: --fiscal ----------
# Reglas por calculadora fiscal (R1..R7). BLOQUEANTE solo donde no hay falsos positivos (fiscal sin ninguna clave en params).
NO_FISCAL_BLOQUES = ("luz_", "placas_", "caldera_", "punto_carga_")
ABS_RE = re.compile(r"\b(siempre|nunca|garantiza\w*|no existe|no se puede|en todos los casos|cualquier)\b", re.I)
ABS_OK = re.compile(r"\b(siempre (que|y cuando)|si|salvo|cuando|excepto|según|depende|mientras|a menos que|en caso|aunque|hasta)\b", re.I)
LEGAL_T = re.compile(r"\b(art\.|arts\.|artículo|Ley|exent[oa]|tributa|cotiza|IRPF|deduc\w+|retenci\w+)", re.I)
CITA_RE = re.compile(r"(según (el Manual|la AEAT|Hacienda|la Agencia Tributaria|la ley)|la ley (establece|dice|obliga)|Hacienda (exige|obliga|establece))", re.I)
UMBRAL = re.compile(r"\d[\d.,]*\s*(€|%|euros)")
COND_LEAD = re.compile(r"\b(si|cuando|depende|según|salvo|a partir de|hasta|desde|con)\b", re.I)
FECHA_TXT = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2} de [a-záéíóú]+ de \d{4}|\b20\d\d\b|ejercicio)", re.I)
MESES = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}

def parse_fecha(t):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", t)
    try:
        if m: return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
        if m: return datetime.date(int(m[3]), int(m[2]), int(m[1]))
        m = re.search(r"(\d{1,2}) de ([a-záéíóú]+) de (\d{4})", t, re.I)
        if m and m[2].lower() in MESES: return datetime.date(int(m[3]), MESES[m[2].lower()], int(m[1]))
    except ValueError: pass
    return None

def strip_js(src):
    """Quita comentarios, cadenas y regex simples de un .js (para contar literales numéricos)."""
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"|`(?:\\.|[^`\\])*`", '""', src)

def walk_leaves(o, acc, path=""):
    """Hojas numéricas escalares (no elementos de lista) con su ruta: respaldo estricto para escalares de var P."""
    if isinstance(o, bool): return
    if isinstance(o, (int, float)): acc.append((path, round(float(o), 6)))
    elif isinstance(o, dict):
        for k, v in o.items(): walk_leaves(v, acc, path + "." + str(k))

def walk_nums(o, acc):
    if isinstance(o, bool): return
    if isinstance(o, (int, float)): acc.add(round(float(o), 6))
    elif isinstance(o, str): acc.update(num_vals(o))
    elif isinstance(o, dict):
        for v in o.values(): walk_nums(v, acc)
    elif isinstance(o, list):
        for v in o: walk_nums(v, acc)

def check_fiscal(only_slugs=None):
    try: params = json.load(open(os.path.join(PDIR, "data/params.json"), encoding="utf-8"))
    except Exception as e:
        add("BLOQUEANTE", "data/params.json", f"no se puede leer: {e}"); return 0
    keys = [k for k, v in params.items() if isinstance(v, dict)]
    hoy = datetime.date.today(); n = 0
    for jsf in sorted(glob.glob(os.path.join(PDIR, "calcs/*.js"))):
        slug = os.path.basename(jsf)[:-3]
        if only_slugs is not None and slug not in only_slugs: continue
        src = open(jsf, encoding="utf-8").read()
        head = "\n".join(src.split("\n")[:3])
        blocks = [k for k in keys if re.search(r"(?<![A-Za-z0-9_])" + re.escape(k) + r"(?![A-Za-z0-9_])", head)] if "params.json" in head else []
        pv = os.path.join(ROOT, "journal", f"preverif-{slug}.md")
        has_pv = os.path.isfile(pv)
        cj = os.path.join(PDIR, f"calcs/{slug}.json")
        try: c = json.load(open(cj, encoding="utf-8"))
        except Exception: c = {}
        pl = [l for l in src.split("\n") if l.startswith("var P")]
        legal_blocks = [b for b in blocks if b.endswith("_2026") and not b.startswith(NO_FISCAL_BLOQUES)]
        fiscal = has_pv or bool(legal_blocks) or (bool(pl) and bool(re.search(r"\b(Ley 35/2006|LIRPF|LGSS)\b", c.get("sources", ""))))
        if not fiscal: continue
        n += 1; w = f"calcs/{slug}"
        # sin ninguna clave en params
        if not blocks:
            if pl or has_pv:
                add("BLOQUEANTE", w + ".js", "R2 calculadora fiscal con cifras (var P / preverif) y sin ninguna clave de data/params.json en la cabecera")
            else:
                add("AVISO", w + ".js", "R2 calculadora fiscal sin referencia a data/params.json en la cabecera")
        # R1 bloques con fuente, url y consulta ISO
        for b in blocks:
            v = params[b]; f = v.get("fuente") or v.get("base_legal")
            u = any(k.startswith("url") and v[k] for k in v) or bool(re.search(r"https?://", json.dumps(v.get("fuente", ""))))
            cons = v.get("consulta") or v.get("consultado") or v.get("consulta_fecha") or v.get("fecha")
            falta = [x for x, ok in (("fuente", bool(f)), ("url", u), ("consulta", bool(cons))) if not ok]
            if falta: add("AVISO", w, f"R1 params.{b}: falta {', '.join(falta)}")
            elif isinstance(cons, str):
                if not FECHA_TXT.search(cons): add("AVISO", w, f"R1 params.{b}.consulta sin fecha ni ejercicio: «{cons[:40]}»")
                else:
                    d = parse_fecha(cons)
                    if d and (hoy - d).days > 120: add("AVISO", w, f"R1 params.{b}.consulta de hace {(hoy-d).days} días: revisar vigencia")
        # R2 cada número de var P existe en los bloques
        corp = set()
        for b in blocks: walk_nums(params[b], corp)
        sueltos = []
        for l in pl:
            try: obj, _ = json.JSONDecoder().raw_decode(l[l.index("=") + 1:].lstrip())
            except Exception: obj = None
            nums = set()
            if obj is not None: walk_nums(obj, nums)
            else: nums = {float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", l)}
            for v in sorted(nums):
                if v in (0, 1, 12, 100, 365): continue
                if blocks and not covered(v, corp): sueltos.append(v)
        # escalares de primer nivel de var P: deben ser hoja escalar de params (%, x100 si < 1), no coincidir con un elemento de lista
        if blocks and pl:
            hojas = []
            for b in blocks: walk_leaves(params[b], hojas, b)
            vals = {v for _, v in hojas}
            for l in pl:
                try: obj, _ = json.JSONDecoder().raw_decode(l[l.index("=") + 1:].lstrip())
                except Exception: continue
                for k, v in (obj.items() if isinstance(obj, dict) else []):
                    if isinstance(v, bool) or not isinstance(v, (int, float)) or v in (0, 1, 12, 100, 365): continue
                    cand = {round(float(v), 6)} | ({round(v * 100, 6)} if 0 < abs(v) < 1 else set())
                    if not (cand & vals) and float(v) not in sueltos: sueltos.append(float(v))
                    elif not (cand & vals): pass
                    else:
                        if re.search(r"^(?:ss|obl)", k) and not any(re.search(k[:3], pth, re.I) for pth, val in hojas if val in cand):
                            sueltos.append(float(v))   # coincide por valor con una hoja de nombre sin relación (p. ej. ss/oblMulti/oblResto frente a lim81)
        if sueltos:
            add("AVISO", w + ".js", f"R2 {len(sueltos)} cifra(s) de var P sin respaldo en params ({', '.join(f'{x:g}' for x in sueltos[:6])}{' …' if len(sueltos) > 6 else ''})")
        # R3 literales fuera de var P
        body = strip_js("\n".join(l for l in src.split("\n") if not l.startswith("var P")))
        lits = []
        for m in re.finditer(r"(?<![\w.$])(\d+(?:\.\d+)?)(?![\w.])", body):
            v = float(m[1])
            if v in (100, 365, 360, 1000) or (v == int(v) and v <= 12) or v <= 1: continue
            lits.append(m[1])
        if lits:
            uniq = list(dict.fromkeys(lits))
            add("AVISO", w + ".js", f"R3 {len(uniq)} literal(es) numérico(s) fuera de var P ({', '.join(uniq[:6])}{' …' if len(uniq) > 6 else ''}): cifra legal fuera de params")
        # textos: lead/veredicto/faqs + content html
        texts = [("lead", c.get("lead", "")), ("veredicto", c.get("veredicto", ""))] + [(f"faq{i+1}", q[1] if len(q) > 1 else "") for i, q in enumerate(c.get("faqs", []))]
        hp = os.path.join(PDIR, "content", slug + ".html"); raw = ""
        if os.path.isfile(hp):
            raw = open(hp, encoding="utf-8").read()
            texts.append(("html", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)))
        # R4 absolutos; R7b citas sin artículo ni enlace
        abs_hits = []; citas = []
        for lab, t in texts:
            for sn in sentences(strip_tags(t)):
                if ABS_RE.search(sn) and LEGAL_T.search(sn) and not ABS_OK.search(sn): abs_hits.append((lab, sn))
                if CITA_RE.search(sn) and not re.search(r"\b[Aa]rt|https?://", sn): citas.append((lab, sn))
        if abs_hits:
            ej = abs_hits[0][1][:70]
            add("AVISO", w, f"R4 {len(abs_hits)} absoluto(s) sin condición con término legal (p. ej. {abs_hits[0][0]}: «{ej}…»)")
        if citas:
            add("AVISO", w, f"R4b {len(citas)} cita(s) de autoridad sin art. ni enlace (p. ej. «{citas[0][1][:70]}…»)")
        # R5 fechas de vigencia del html en params/preverif
        if raw:
            ref = " ".join(json.dumps(params[b], ensure_ascii=False) for b in blocks)
            if has_pv: ref += " " + open(pv, encoding="utf-8").read()
            ref_l = ref.lower(); faltan = []
            plain = strip_tags(raw)
            for m in re.finditer(r"desde el (\d{1,2}) de ([a-záéíóú]+) de (\d{4})", plain, re.I):
                mes = MESES.get(m[2].lower())
                forms = [m[0][6:].lower(), f"{int(m[1])}/{mes}/{m[3]}", f"{int(m[1])}.{mes}.{m[3]}", f"{m[3]}-{(mes or 0):02d}-{int(m[1]):02d}"]
                if not any(f_ in ref_l for f_ in forms): faltan.append(m[0])
            for m in re.finditer(r"a partir de (?:el )?(\d{4})\b", plain, re.I):
                if m[1] not in ref: faltan.append(m[0])
            if faltan: add("AVISO", w, f"R5 fecha(s) de vigencia del texto sin rastro en params/preverif: {'; '.join(dict.fromkeys(faltan))[:110]}")
        # R6 preverif con T, 8, N, R y S con URL y fecha
        if not has_pv:
            add("AVISO", w, "R6 calculadora fiscal sin journal/preverif-<slug>.md")
        else:
            pt = open(pv, encoding="utf-8").read()
            falta = [x for x in ("T", "8", "N", "R") if not re.search(r"^" + x + r"\s*[·.:]", pt, re.M)]
            s_ok = any(re.search(r"https?://", l) and FECHA_TXT.search(l) for l in pt.split("\n") if re.match(r"S\s*\d*\s*[·.:]", l))
            if falta or not s_ok:
                add("AVISO", w, "R6 preverif: " + (f"faltan líneas {','.join(falta)}" if falta else "") + ("; " if falta and not s_ok else "") + ("ninguna línea «S ·» con URL y fecha" if not s_ok else ""))
        # R7 ámbito forales
        alltxt = strip_tags(raw) + " " + c.get("sources", "") + " " + " ".join(t for _, t in texts[:-1] if isinstance(t, str))
        if not re.search(r"Pa[ií]s Vasco|Navarra|forales?|Euskadi", alltxt, re.I):
            add("AVISO", w, "R7 no menciona el ámbito foral (País Vasco/Navarra)")
        # R8 lead sin condición donde hay umbral
        lead = strip_tags(c.get("lead", ""))
        if UMBRAL.search(lead) and not COND_LEAD.search(lead):
            add("AVISO", w, "R8 lead con cifra/umbral y sin condición (si/cuando/depende)")
    return n

# ---------- main ----------
def main_fiscal():
    slugs = None
    if CHANGED: slugs = changed_pages(git_changed())[0]
    n = check_fiscal(slugs)
    order = {"BLOQUEANTE": 0, "AVISO": 1}
    por_regla = {}
    for lvl, where, msg in out:
        r = msg.split(" ", 1)[0] if re.match(r"R\d", msg) else "otras"
        por_regla[(lvl, r)] = por_regla.get((lvl, r), 0) + 1
    nb = sum(1 for o in out if o[0] == "BLOQUEANTE")
    full = "--full" in sys.argv
    for lvl, where, msg in sorted(out, key=lambda x: order[x[0]])[: (None if full else max(nb, 0) + 5)]:
        print(f"{lvl} · {where} · {msg}")
    if not full and len(out) > nb + 5: print(f"… {len(out) - nb - 5} más (usa --fiscal --full)")
    print("FISCAL: " + str(n) + " calculadoras; " + (", ".join(f"{r}={c}" for (l, r), c in sorted(por_regla.items())) or "sin avisos") + f"; {nb} BLOQUEANTE, {len(out) - nb} AVISO")
    sys.exit(1 if nb else 0)

def main():
    if FISCAL: return main_fiscal()
    if not os.path.isdir(DIST):
        print(f"BLOQUEANTE · {DIST} · no existe el directorio dist (ejecuta build.py)"); sys.exit(1)
    slugs = None; glob_change = False; paths = []
    if CHANGED:
        files = git_changed(); slugs, glob_change, paths = changed_pages(files)
    pages, indexables, n_page = check_pages()
    n_sm = check_sitemap(indexables)
    check_files()
    n_live = check_live()
    n_ymyl = check_ymyl(slugs if CHANGED else None)
    # ordena: BLOQUEANTE primero
    order = {"BLOQUEANTE": 0, "AVISO": 1, "INFO": 2}
    for lvl, where, msg in sorted(out, key=lambda x: order[x[0]]): print(f"{lvl} · {where} · {msg}")
    nb = sum(1 for o in out if o[0] == "BLOQUEANTE"); ni = sum(1 for o in out if o[0] == "INFO"); na = len(out) - nb - ni
    print(f"OK: {len(pages)} páginas, {n_page} comprobaciones de página, {n_sm} URLs en sitemap, {n_live} defaults vivos, {n_ymyl} fuentes YMYL; {nb} BLOQUEANTE, {na} AVISO, {ni} INFO")
    if CHANGED:
        print("Cambios (git): " + ("global (plantillas/assets/datos): " if glob_change else "") +
              ("; ".join(["/ (home)"] + paths) if paths or glob_change else "ninguna página afectada"))
        navegador = sorted(set(["/"] + paths))
        print("PÁGINAS PARA EL QA CON NAVEGADOR (rutas de dist): " + " ".join(navegador))
        if glob_change: print("  (cambio global: añade 1 calculadora y 1 guía de muestra, p. ej. /decidir/hipoteca-fija-o-variable/ y /guias/euribor-hipoteca/)")
    sys.exit(1 if nb else 0)

if __name__ == "__main__":
    main()
