#!/usr/bin/env python3
"""Rasteriza projects/decidir/og-svg/*.svg -> projects/decidir/og/<slug>.png|jpg (1200x630) con qlmanage+sips (solo macOS).
Los resultados se commitean (la Action corre en Ubuntu). Uso: python3 ops/og_raster.py [--force]. Diseñador."""
import os, subprocess, sys, tempfile, glob
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "projects", "decidir")
SVG, OUT = os.path.join(ROOT, "og-svg"), os.path.join(ROOT, "og")
MAXB = 120 * 1024

def dims(p):
    o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p], capture_output=True, text=True).stdout
    v = {l.split(":")[0].strip(): int(l.split(":")[1]) for l in o.splitlines() if ":" in l and "pixel" in l}
    return v.get("pixelWidth"), v.get("pixelHeight")

def sh(*a): subprocess.run(a, check=True, capture_output=True)

def main():
    force = "--force" in sys.argv; os.makedirs(OUT, exist_ok=True); n = bad = 0
    for svg in sorted(glob.glob(os.path.join(SVG, "*.svg"))):
        slug = os.path.basename(svg)[:-4]
        ex = [p for p in (os.path.join(OUT, slug + ".png"), os.path.join(OUT, slug + ".jpg")) if os.path.exists(p)]
        if ex and not force and all(os.path.getmtime(p) >= os.path.getmtime(svg) for p in ex): continue
        with tempfile.TemporaryDirectory() as t:
            # qlmanage reescala los SVG no cuadrados y sips recorta desde el centro: se rasteriza una copia en lienzo 1200x1200
            # con el contenido desplazado 285 px abajo (queda justo en la franja central 285..915 que recorta sips)
            sq = os.path.join(t, slug + ".svg")
            src = open(svg, encoding="utf-8").read()
            head, rest = src.split(">", 1)
            head = head.replace('height="630" viewBox="0 0 1200 630"', 'height="1200" viewBox="0 0 1200 1200"', 1)
            open(sq, "w", encoding="utf-8").write(head + '><g transform="translate(0 285)">' + rest.replace("</svg>", "</g></svg>"))
            sh("qlmanage", "-t", "-s", "1200", "-o", t, sq)
            raw = os.path.join(t, slug + ".svg.png"); crop = os.path.join(t, "c.png")
            sh("sips", "--cropToHeightWidth", "630", "1200", raw, "--out", crop)
            if dims(crop) != (1200, 630): print("DIM MAL", slug, dims(crop)); bad += 1; continue
            for p in ex: os.remove(p)
            dst = os.path.join(OUT, slug + ".png")
            if os.path.getsize(crop) > MAXB:
                dst = os.path.join(OUT, slug + ".jpg"); sh("sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", crop, "--out", dst)
            else: open(dst, "wb").write(open(crop, "rb").read())
        n += 1
    tot = sum(os.path.getsize(p) for p in glob.glob(OUT + "/*"))
    print(f"{n} rasterizadas, {bad} fallos, {len(os.listdir(OUT))} en og/, {tot/1e6:.1f} MB")
    sys.exit(1 if bad else 0)
main()
