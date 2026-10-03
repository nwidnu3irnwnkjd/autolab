#!/usr/bin/env python3
"""Auditoría SEO/GEO técnica de dist/ (stdlib). Optimizador de tráfico.
Uso: python3 ops/seo_audit.py [decidir] [--json salida.json] [--top N]
Mide: title/description (únicos, longitud), canonical, noindex, H1, JSON-LD
(parse + tipos), enlaces internos entrantes, profundidad de clic desde la home,
huérfanas, cobertura de sitemaps, peso HTML, palabras, primer párrafo,
fecha visible, robots.txt, llms.txt, feed.
"""
import json, os, re, sys, collections
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj = next((a for a in sys.argv[1:] if not a.startswith("-") and not a.endswith(".json")), "decidir")
DIST = os.path.join(ROOT, "projects", proj, "dist")
HOST = "entremuchos.com"
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 15


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.desc = None; self.canon = None; self.robots = ""
        self.h1 = []; self.links = []; self.ld = []; self.text = []
        self._in = None; self._buf = []; self.first_p = None; self.times = 0
        self.imgs_noalt = 0; self.skip = 0; self.in_main = False; self.h2 = 0
        self.tables = 0
    def handle_starttag(self, t, a):
        a = dict(a)
        if t in ("script", "style"):
            self.skip += 1
            if t == "script" and a.get("type") == "application/ld+json":
                self._in = "ld"; self._buf = []
            return
        if t == "title": self._in = "title"; self._buf = []
        elif t == "h1": self._in = "h1"; self._buf = []
        elif t == "p" and self.first_p is None and self.h1: self._in = "p"; self._buf = []
        elif t == "meta":
            n = (a.get("name") or "").lower()
            if n == "description": self.desc = a.get("content", "")
            if n == "robots": self.robots = a.get("content", "")
        elif t == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        elif t == "a" and a.get("href"): self.links.append(a["href"])
        elif t == "time": self.times += 1
        elif t == "img" and not a.get("alt") and a.get("alt") != "": self.imgs_noalt += 1
        elif t == "h2": self.h2 += 1
        elif t == "table": self.tables += 1
    def handle_endtag(self, t):
        if t in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            if self._in == "ld":
                self.ld.append("".join(self._buf)); self._in = None
            return
        if self._in == "title" and t == "title": self.title = "".join(self._buf).strip(); self._in = None
        elif self._in == "h1" and t == "h1": self.h1.append(" ".join("".join(self._buf).split())); self._in = None
        elif self._in == "p" and t == "p":
            self.first_p = " ".join("".join(self._buf).split()); self._in = None
    def handle_data(self, d):
        if self._in: self._buf.append(d)
        if not self.skip: self.text.append(d)


def url_of(path):
    rel = os.path.relpath(path, DIST).replace(os.sep, "/")
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def norm(href, base):
    u = urlparse(urljoin("https://%s%s" % (HOST, base), href))
    if u.netloc and u.netloc not in (HOST, "www." + HOST): return None
    p = u.path or "/"
    if p.endswith("index.html"): p = p[:-10]
    if not os.path.splitext(p)[1] and not p.endswith("/"): p += "/"
    return p


def ld_types(o, acc):
    if isinstance(o, dict):
        t = o.get("@type")
        if t: acc.extend(t if isinstance(t, list) else [t])
        for v in o.values(): ld_types(v, acc)
    elif isinstance(o, list):
        for v in o: ld_types(v, acc)


pages = {}
for d, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith(".html"):
            fp = os.path.join(d, f); u = url_of(fp)
            raw = open(fp, encoding="utf-8", errors="replace").read()
            p = P(); p.feed(raw)
            types, bad = [], 0
            for s in p.ld:
                try: ld_types(json.loads(s), types)
                except Exception: bad += 1
            words = len(re.findall(r"\w+", " ".join(p.text)))
            pages[u] = dict(title=p.title, desc=p.desc, canon=p.canon, robots=p.robots, h1=p.h1,
                            links=[x for x in (norm(h, u) for h in p.links) if x], ld_types=types,
                            ld_bad=bad, bytes=len(raw.encode()), words=words, first_p=p.first_p or "",
                            times=p.times, noalt=p.imgs_noalt, h2=p.h2, tables=p.tables,
                            year_in_title="2026" in p.title or "2027" in p.title)

noindex = {u for u, v in pages.items() if "noindex" in v["robots"].lower()}
idx = {u: v for u, v in pages.items() if u not in noindex and u != "/404.html"}

# sitemaps
sm_urls = set()
for f in os.listdir(DIST):
    if f.startswith("sitemap") and f.endswith(".xml"):
        x = open(os.path.join(DIST, f), encoding="utf-8").read()
        for loc in re.findall(r"<loc>([^<]+)</loc>", x):
            if not loc.endswith(".xml"): sm_urls.add(urlparse(loc).path or "/")
lastmods = re.findall(r"<lastmod>([^<]+)</lastmod>", "".join(open(os.path.join(DIST, f), encoding="utf-8").read() for f in os.listdir(DIST) if f.startswith("sitemap-")))

# inlinks y profundidad
inl = collections.Counter(); inl_src = collections.defaultdict(set)
for u, v in idx.items():
    for l in set(v["links"]):
        if l != u: inl[l] += 1; inl_src[l].add(u)
depth = {"/": 0}; q = collections.deque(["/"])
while q:
    u = q.popleft()
    for l in set(pages.get(u, {}).get("links", [])):
        if l in idx and l not in depth: depth[l] = depth[u] + 1; q.append(l)
broken = collections.Counter()
for u, v in idx.items():
    for l in v["links"]:
        if not os.path.splitext(l)[1] and l not in pages: broken[l] += 1

R = []; out = R.append
titles = collections.Counter(v["title"] for v in idx.values())
descs = collections.Counter(v["desc"] for v in idx.values())
tl = [len(v["title"]) for v in idx.values()]
out("# Auditoría técnica %s · %d HTML (%d indexables, %d noindex)" % (proj, len(pages), len(idx), len(noindex)))
out("- Titles duplicados: %d · >60 car.: %d · <30: %d · media %.0f" % (sum(c - 1 for c in titles.values() if c > 1), sum(l > 60 for l in tl), sum(l < 30 for l in tl), sum(tl) / len(tl)))
out("- Descriptions ausentes: %d · duplicadas: %d · >160: %d" % (sum(1 for v in idx.values() if not v["desc"]), sum(c - 1 for c in descs.values() if c > 1), sum(1 for v in idx.values() if v["desc"] and len(v["desc"]) > 160)))
out("- Canonical ausente: %d · canonical ≠ URL: %d" % (sum(1 for v in idx.values() if not v["canon"]), sum(1 for u, v in idx.items() if v["canon"] and urlparse(v["canon"]).path != u)))
out("- H1 ≠ 1: %d · JSON-LD con error de parseo: %d · sin JSON-LD: %d" % (sum(1 for v in idx.values() if len(v["h1"]) != 1), sum(v["ld_bad"] for v in idx.values()), sum(1 for v in idx.values() if not v["ld_types"])))
tc = collections.Counter(t for v in idx.values() for t in set(v["ld_types"]))
out("- Tipos JSON-LD (páginas): " + ", ".join("%s %d" % kv for kv in tc.most_common(12)))
out("- Sitemap: %d URLs · indexables fuera de sitemap: %d · en sitemap sin HTML o noindex: %d · lastmod distintos: %d" % (len(sm_urls), len(set(idx) - sm_urls), len({u for u in sm_urls if u not in idx}), len(set(lastmods))))
out("- Huérfanas (0 inlinks): %d · inaccesibles desde home: %d · profundidad máx %d · media %.2f" % (sum(1 for u in idx if inl[u] == 0 and u != "/"), sum(1 for u in idx if u not in depth), max(depth.values()), sum(depth.values()) / len(depth)))
out("- Enlaces internos rotos: %d únicos (%d apariciones)" % (len(broken), sum(broken.values())))
b = sorted(v["bytes"] for v in idx.values()); w = sorted(v["words"] for v in idx.values())
out("- Peso HTML: mediana %d KB, máx %d KB · palabras: mediana %d, mín %d" % (b[len(b) // 2] // 1024, b[-1] // 1024, w[len(w) // 2], w[0]))
out("- Con <time>: %d · con tabla: %d · año en title: %d · imgs sin alt: %d" % (sum(1 for v in idx.values() if v["times"]), sum(1 for v in idx.values() if v["tables"]), sum(1 for v in idx.values() if v["year_in_title"]), sum(v["noalt"] for v in idx.values())))
il = sorted(((inl[u], u) for u in idx))
out("- Inlinks: mediana %d; menos enlazadas: %s" % (il[len(il) // 2][0], "; ".join("%s (%d)" % (u, n) for n, u in il[:TOP])))
out("- Más enlazadas: " + "; ".join("%s (%d)" % (u, n) for n, u in il[::-1][:8]))
sec = collections.defaultdict(list)
for u in idx: sec[u.split("/")[1] or "home"].append(u)
out("- Por sección (n, inlinks medianos, prof. media): " + "; ".join("%s %d/%d/%.1f" % (s, len(us), sorted(inl[x] for x in us)[len(us) // 2], sum(depth.get(x, 9) for x in us) / len(us)) for s, us in sorted(sec.items(), key=lambda kv: -len(kv[1]))))
for d in titles:
    if titles[d] > 1: out("  dup title: %s ×%d" % (d, titles[d]))
long_t = [(len(v["title"]), u, v["title"]) for u, v in idx.items() if len(v["title"]) > 60]
for n, u, t in sorted(long_t, reverse=True)[:TOP]: out("  title %d: %s · %s" % (n, u, t))
for l, n in broken.most_common(10): out("  roto: %s ×%d" % (l, n))
for f in ("robots.txt", "llms.txt", "llms-full.txt", "feed.xml"):
    fp = os.path.join(DIST, f)
    out("- %s: %s" % (f, "%d KB" % (os.path.getsize(fp) // 1024) if os.path.exists(fp) else "FALTA"))
print("\n".join(R))
if "--json" in sys.argv:
    json.dump({u: dict(v, inlinks=inl[u], depth=depth.get(u), links=None) for u, v in idx.items()},
              open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False, indent=0)
