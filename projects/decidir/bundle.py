"""Post-proceso de assets (Diseñador): minifica JS/CSS de dist, recorta (tree-shake) el CSS por tipo de página
y carga solo el JS necesario (core / em / chart / home). Se llama al final de build.main()."""
import hashlib, os, re
import minify

JS_SRC = ["app.js", "em.js", "chart.js", "home.js"]


def _h(s): return hashlib.sha1(s.encode()).hexdigest()[:10]


def run(root, dist):
    A = os.path.join(root, "assets"); D = os.path.join(dist, "assets")
    js = {f: minify.js(open(os.path.join(A, f)).read()) for f in JS_SRC}
    jsv = {f: _h(js[f]) for f in js}
    css = minify.css(open(os.path.join(A, "app.css")).read())
    pcss = minify.css(open(os.path.join(A, "print.css")).read()); pv = _h(pcss)
    for f in JS_SRC + ["app.css", "print.css"]:
        p = os.path.join(D, f)
        if os.path.exists(p): os.remove(p)
    for f in JS_SRC: open(os.path.join(D, f), "w").write(js[f])
    open(os.path.join(D, "print.css"), "w").write(pcss)
    pages = {}
    for dp, _, fs in os.walk(dist):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(dp, f); h = open(p).read()
                if "/assets/app.css" not in h: continue
                if 'class="calc"' in h: kind = "calc"
                elif p == os.path.join(dist, "index.html"): kind = "home"
                elif "data-filter" in h: kind = "cat"
                else: kind = "page"
                chart = kind == "calc" and bool(re.search(r"lineChart|\bline\s*:", h))
                use = ["app.js"] + (["em.js"] if kind == "calc" else []) + (["chart.js"] if chart else []) + (["home.js"] if kind in ("home", "cat") else [])
                pages[p] = (h, kind + ("-chart" if chart else ""), use)
    pools = {}
    for p, (h, key, use) in pages.items():
        pool, pre = pools.setdefault(key, (set(), set()))
        txt = h + "".join(js[u] for u in use)
        pool.update(re.findall(r"[\w-]+", txt)); pre.update(re.findall(r"[\"']([\w]+-[\w-]*-)[\"']", txt))
    cssf = {}
    for key, (pool, pre) in pools.items():
        c = minify.shake(css, pool, tuple(pre)); name = f"site-{key}.css"
        open(os.path.join(D, name), "w").write(c); cssf[key] = (name, _h(c))
    for p, (h, key, use) in pages.items():
        name, v = cssf[key]
        tag = f'<link rel="stylesheet" href="/assets/{name}?v={v}">' + (f'<link rel="stylesheet" href="/assets/print.css?v={pv}" media="print">' if key.startswith("calc") else "")
        h = re.sub(r'<link rel="stylesheet" href="/assets/app\.css[^"]*">', tag, h)
        tags = "".join(f'<script src="/assets/{u}?v={jsv[u]}"></script>' for u in use)
        h = re.sub(r'<script src="/assets/app\.js[^"]*"></script>', tags, h)
        open(p, "w").write(h)
    return {k: v[0] for k, v in cssf.items()}
