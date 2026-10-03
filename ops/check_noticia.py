#!/usr/bin/env python3
"""Comprobación mecánica de piezas de noticias (0 tokens). Solo stdlib. Dueño: Orquestador/Constructor (PLAN-NOTICIAS §3 paso 2a).

Uso:
  python3 ops/check_noticia.py                      # todas las piezas de content/noticias (salvo _*.html), con red
  python3 ops/check_noticia.py ARCHIVO [ARCHIVO..]  # piezas concretas (ruta o nombre)
  python3 ops/check_noticia.py --offline            # sin comprobar enlaces (qa_static lo usa así)
  python3 ops/check_noticia.py --estricto           # los AVISO también dan exit 1 (úsalo antes de marcar «publicada»)
Salida: `BLOQUEANTE|AVISO · archivo · mensaje`. Exit 1 si hay BLOQUEANTE (o AVISO con --estricto).

BLOQUEANTE: meta ausente/ inválida o sin campos, estado/tipo desconocido, fecha futura o incoherente, título > 60 o description > 155,
  sin fuente oficial enlazada en el cuerpo, sin <time>, calculadora inexistente, enlace oficial con 4xx.
AVISO: bloques (El hecho / A quién afecta / Tu cifra / Qué hacer y plazo) o lista de 3-6 hechos con fuente (resúmenes), cifras € o % sin
  comentario <!--f: fuente--> ni presencia en params/live/tests, fecha del hecho sin <time>, longitud, enlaces no oficiales, enlace no comprobable.
Enlaces: HTTP 200 con timeout 12 s y caché diaria en ops/noticias/.cache-enlaces.json (misma URL, mismo día: no se repite)."""
import datetime, glob, json, os, re, sys, unicodedata, urllib.request, urllib.error
from urllib.parse import urlparse

OPS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OPS)
PDIR = os.path.join(ROOT, "projects", "decidir")
NDIR = os.path.join(PDIR, "content", "noticias")
CACHE = os.path.join(OPS, "noticias", ".cache-enlaces.json")
TIPOS = {"alerta", "dato-mes", "cuenta-atras", "explicador", "resumen-dia", "resumen-semana"}
RESUMENES = {"resumen-dia", "resumen-semana"}
ESTADOS = {"borrador", "publicada", "retirada"}
REQ = ["title", "h1", "description", "published", "modified", "tipo", "temas", "calcs", "fuentes", "caduca", "estado"]
BLOQUES = ["el hecho", "a quien afecta", "tu cifra", "que hacer"]
LONG = {"alerta": (150, 700), "dato-mes": (150, 600), "cuenta-atras": (120, 500), "explicador": (400, 1100), "resumen-dia": (120, 700), "resumen-semana": (250, 900)}
HECHOS = {"resumen-dia": (3, 6), "resumen-semana": (3, 7)}
OFICIALES = ("boe.es", "ine.es", "bde.es", "cnmc.es", "ree.es", "seg-social.es", "sepe.es", "aeat.es", "ecb.europa.eu", "europa.eu", "congreso.es", "senado.es",
             "dgt.es", "eur-lex.europa.eu")  # + cualquier *.gob.es
HOY = datetime.date.today

def norm(s): return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
def oficial(url):
    h = (urlparse(url).hostname or "").lower()
    return h.endswith(".gob.es") or any(h == d or h.endswith("." + d) for d in OFICIALES)
def interno(url): return url.startswith("/") or (urlparse(url).hostname or "") in ("entremuchos.com", "www.entremuchos.com") or url.startswith(("mailto:", "#", "data:"))
def iso(s):
    try: return datetime.date.fromisoformat(s)
    except Exception: return None

# ---------- corpus de cifras (params, live, tests y definiciones de calculadoras) ----------
_CORPUS = None
def _nums_in(text):
    out = set()
    for m in re.finditer(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?", text):
        t = m.group(0)
        for v in ({t.replace(".", "").replace(",", ".")} | {t.replace(",", ".")} | {t.replace(",", "")}):
            try: out.add(round(float(v), 6))
            except ValueError: pass
    return out
def corpus():
    global _CORPUS
    if _CORPUS is not None: return _CORPUS
    c = set()
    files = [os.path.join(PDIR, "data/params.json"), os.path.join(PDIR, "data/live.json")] + glob.glob(os.path.join(PDIR, "calcs/*.json")) + glob.glob(os.path.join(PDIR, "data/*.json"))
    for f in set(files):
        try: txt = open(f, encoding="utf-8").read()
        except OSError: continue
        c |= _nums_in(txt)
    _CORPUS = c
    return c

def figs(text):
    """Cifras en € o % del texto: [(float, literal)]."""
    out = []
    for m in re.finditer(r"(?<![\w.,])(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)\s?(?:€|%|euros?\b|por ciento)", text):
        t = m.group(1)
        out.append((round(float(t.replace(".", "").replace(",", ".")), 6), m.group(0)))
    return out

# ---------- enlaces ----------
_cache = None
def link_status(url, offline):
    global _cache
    if offline: return None
    if _cache is None:
        try: _cache = json.load(open(CACHE))
        except Exception: _cache = {}
    hoy = HOY().isoformat()
    if url in _cache and _cache[url][0] == hoy: return _cache[url][1]
    st = 0
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (compatible; entremuchos-check/1.0)"})
            with urllib.request.urlopen(req, timeout=12) as r: st = r.status
            break
        except urllib.error.HTTPError as e: st = e.code
        except Exception: st = 0
        if st == 200: break
    if st:  # no cachea fallos de red (0)
        _cache[url] = [hoy, st]
        try: os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(_cache, open(CACHE, "w"))
        except OSError: pass
    return st

# ---------- comprobación de una pieza ----------
def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
    if not m: return None, raw, "falta la cabecera <!--meta {json}-->"
    try: return json.loads(m.group(1)), raw[m.end():], None
    except Exception as e: return None, raw, f"meta JSON inválido: {e}"

def check_file(path, offline=True):
    """Lista de (nivel, mensaje)."""
    R = []; add = lambda lv, msg: R.append((lv, msg))
    meta, body, err = parse(path)
    if err: add("BLOQUEANTE", err); return R
    fn = os.path.basename(path)
    mfn = re.match(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9][a-z0-9-]*)\.html$", fn)
    if not mfn: add("BLOQUEANTE", "el nombre debe ser AAAA-MM-DD-slug.html (minúsculas y guiones)")
    miss = [k for k in REQ if k not in meta]
    if miss: add("BLOQUEANTE", "faltan campos del meta: " + ", ".join(miss)); return R
    tipo = meta["tipo"]
    if meta["estado"] not in ESTADOS: add("BLOQUEANTE", f"estado «{meta['estado']}» no válido (borrador|publicada|retirada)")
    if tipo not in TIPOS: add("BLOQUEANTE", f"tipo «{tipo}» no válido ({'|'.join(sorted(TIPOS))})")
    for k in ("temas", "calcs", "fuentes"):
        if not isinstance(meta[k], list): add("BLOQUEANTE", f"{k} debe ser una lista")
    if len(meta["title"]) > 60: add("BLOQUEANTE", f"title de {len(meta['title'])} caracteres (máx. 60)")
    if not (100 <= len(meta["description"]) <= 155): add("BLOQUEANTE" if len(meta["description"]) > 155 else "AVISO", f"description de {len(meta['description'])} caracteres (ideal 140-155; máx. 155)")
    pub, mod = iso(meta["published"]), iso(meta["modified"])
    if not pub or not mod: add("BLOQUEANTE", "published/modified deben ser AAAA-MM-DD"); return R
    if mfn and mfn.group(1) != meta["published"]: add("AVISO", f"la fecha del nombre ({mfn.group(1)}) no coincide con published ({meta['published']}): la URL usa la del nombre")
    if meta["estado"] == "publicada" and pub > HOY(): add("BLOQUEANTE", "published en el futuro: no se publicará hasta esa fecha")
    if mod < pub: add("BLOQUEANTE", "modified anterior a published")
    cad = meta["caduca"]
    if cad and (not iso(cad) or iso(cad) < pub): add("BLOQUEANTE", "caduca debe ser una fecha >= published (o vacío)")
    if not cad and tipo not in RESUMENES: add("AVISO", "sin fecha de caducidad (`caduca`): ¿cuándo deja de ser vigente la cifra?")
    for s in meta["calcs"]:
        if not os.path.exists(os.path.join(PDIR, "calcs", s + ".json")): add("BLOQUEANTE", f"calculadora inexistente en `calcs`: {s}")
    if tipo not in RESUMENES and not meta["calcs"]: add("AVISO", "sin calculadora en `calcs` (la pieza debe aportar tu cifra)")
    # fuentes
    fu = [f for f in meta["fuentes"] if isinstance(f, dict)]
    if not fu: add("BLOQUEANTE", "sin fuentes en el meta")
    for f in fu:
        if not f.get("url") or not f.get("nombre"): add("BLOQUEANTE", "cada fuente necesita nombre y url")
        elif not oficial(f["url"]): add("BLOQUEANTE", f"fuente no oficial en el meta: {f['url']} (solo organismos primarios; la prensa solo es alerta)")
        d = iso(f.get("fecha") or "")
        if not d: add("AVISO", f"fuente sin fecha válida del hecho: {f.get('nombre', '')[:40]}")
        elif d > pub: add("BLOQUEANTE", f"fecha del hecho {f['fecha']} posterior a la publicación")
    hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', body)
    ext = [h for h in hrefs if not interno(h)]
    ofi = [h for h in ext if oficial(h)]
    if not ofi: add("BLOQUEANTE", "sin enlace a fuente oficial en el cuerpo de la pieza")
    elif fu and fu[0].get("url") and fu[0]["url"].split("#")[0] not in [h.split("#")[0] for h in ofi]: add("AVISO", "la fuente principal del meta no está enlazada en el cuerpo")
    for h in ext:
        if not oficial(h): add("AVISO", f"enlace externo no oficial: {h} (no enlaces prensa ni terceros como fuente)")
    times = re.findall(r'<time\b[^>]*\bdatetime="([^"]+)"', body)
    if not times: add("BLOQUEANTE", "sin <time datetime=…> visible (fecha del hecho)")
    elif fu and fu[0].get("fecha") and fu[0]["fecha"] not in times: add("AVISO", f"la fecha del hecho {fu[0]['fecha']} no aparece en un <time> del cuerpo")
    # estructura
    h2 = [norm(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.S)]
    if tipo in RESUMENES:
        lo, hi = HECHOS[tipo]
        ol = re.findall(r'<(?:ol|ul)\b[^>]*class="[^"]*\bhechos\b[^"]*"[^>]*>(.*?)</(?:ol|ul)>', body, re.S)
        lis = re.findall(r"<li\b[^>]*>(.*?)</li>", ol[0], re.S) if ol else []
        if not ol: add("AVISO", "resumen sin lista de hechos (<ol class=\"hechos\"> con 3-6 <li>)")
        elif not (lo <= len(lis) <= hi): add("AVISO", f"{len(lis)} hechos (debe haber {lo}-{hi})")
        for i, li in enumerate(lis, 1):
            if not any(oficial(h) for h in re.findall(r'href="([^"]+)"', li)): add("AVISO", f"hecho {i} sin enlace a fuente oficial")
            if "<time" not in li: add("AVISO", f"hecho {i} sin <time> con su fecha")
    else:
        pos = -1
        for b in BLOQUES:
            i = next((k for k, t in enumerate(h2) if t.startswith(b)), -1)
            if i < 0: add("AVISO", f"falta el bloque «{b}» (h2: El hecho / A quién afecta / Tu cifra / Qué hacer y plazo)")
            elif i < pos: add("AVISO", f"el bloque «{b}» está fuera de orden")
            pos = max(pos, i)
    # longitud
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", body, flags=re.S)).split())
    lo, hi = LONG.get(tipo, (0, 10 ** 6))
    if not (lo <= words <= hi): add("AVISO", f"{words} palabras (esperado {lo}-{hi} para {tipo})")
    # cifras
    chunks = re.split(r"(?i)</?(?:p|li|h[1-6]|ul|ol|div|section|blockquote|tr|td|th|table)\b[^>]*>", body)
    C = corpus()
    for ch in chunks:
        fs = figs(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", " ", ch, flags=re.S)))
        if not fs: continue
        cm = re.findall(r"<!--\s*f:(.*?)-->", ch, re.S)
        if any(c.strip() for c in cm):
            for c in cm:  # si la nota cita un archivo (.json/.md), debe existir
                for ref in re.findall(r"[\w./-]+\.(?:json|md)\b", c):
                    if not any(os.path.exists(os.path.join(b, ref)) for b in (PDIR, ROOT, os.path.join(PDIR, "data"))): add("AVISO", f"<!--f:--> cita un archivo inexistente: {ref}")
            continue
        for v, lit in fs:
            if v not in C: add("AVISO", f"cifra «{lit}» sin <!--f: fuente--> y no presente en params/live/tests/calculadoras")
    # enlaces: oficiales con 200
    for u in sorted(set(ofi + [f["url"] for f in fu if f.get("url")])):
        st = link_status(u, offline)
        if st is None: continue
        if st == 0: add("AVISO", f"enlace no comprobable (sin respuesta): {u}")
        elif 400 <= st < 500: add("BLOQUEANTE", f"enlace oficial con HTTP {st}: {u}")
        elif st != 200 and not (200 <= st < 400): add("AVISO", f"enlace oficial con HTTP {st}: {u}")
    return R

def pieza_files(args=()):
    if args:
        return [a if os.path.isabs(a) or os.path.exists(a) else os.path.join(NDIR, a if a.endswith(".html") else a + ".html") for a in args]
    return sorted(f for f in glob.glob(os.path.join(NDIR, "*.html")) if not os.path.basename(f).startswith("_"))

def main(argv):
    offline = "--offline" in argv; estricto = "--estricto" in argv
    files = pieza_files([a for a in argv if not a.startswith("--")])
    nb = na = 0
    for f in files:
        rs = check_file(f, offline)
        name = os.path.relpath(f, ROOT) if os.path.exists(f) else f
        for lv, msg in rs:
            print(f"{lv} · {name} · {msg}")
        nb += sum(1 for lv, _ in rs if lv == "BLOQUEANTE"); na += sum(1 for lv, _ in rs if lv == "AVISO")
        if not rs: print(f"OK · {name}")
    print(f"{len(files)} piezas; {nb} BLOQUEANTE, {na} AVISO" + (" (sin comprobar enlaces)" if offline else ""))
    sys.exit(1 if nb or (estricto and na) else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
