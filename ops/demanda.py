#!/usr/bin/env python3
"""Señal de demanda gratuita (sin cuenta): sugerencias de autocompletado de Google (es-ES)
para la consulta semilla de cada calculadora/guía. 0 tokens; ~1 petición/0,6 s.
Uso: python3 ops/demanda.py [decidir] [--semillas "q1;q2"] [--out f.md] [--max N]
Semilla por defecto: title de la página hasta ':' / '?' (sin «Calculadora», «2026»).
Salida: por página, nº de sugerencias (0 = la semilla no es una consulta real),
sugerencias con cifras/años (cola larga con intención) y si el title contiene la 1.ª sugerencia.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proj = next((a for a in sys.argv[1:] if not a.startswith("-") and "/" not in a and not a.endswith(".md")), "decidir")
DIST = os.path.join(ROOT, "projects", proj, "dist")
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 999


def suggest(q):
    u = "https://suggestqueries.google.com/complete/search?client=firefox&hl=es&gl=es&q=" + urllib.parse.quote(q)
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=10).read()
    try: s = raw.decode("utf-8")
    except UnicodeDecodeError: s = raw.decode("latin-1")
    return json.loads(s)[1]


def seed(title):
    t = re.split(r"[:?]| — | - ", title.replace("¿", ""))[0]
    t = re.sub(r"\b(calculadora|2026|2027|con tus números)\b", "", t, flags=re.I)
    return " ".join(t.lower().split())


if "--semillas" in sys.argv:
    seeds = [(s.strip(), "") for s in sys.argv[sys.argv.index("--semillas") + 1].split(";") if s.strip()]
else:
    seeds = []
    for sec in ("decidir", "guias"):
        for d in sorted(os.listdir(os.path.join(DIST, sec))):
            p = os.path.join(DIST, sec, d, "index.html")
            if os.path.exists(p):
                m = re.search(r"<title>([^<]+)</title>", open(p, encoding="utf-8").read())
                if m: seeds.append((seed(m.group(1)), "/%s/%s/ · %s" % (sec, d, m.group(1))))
rows, vacias = [], []
for q, page in seeds[:MAX]:
    try: s = suggest(q)
    except Exception as e: s = None; print("error", q, e, file=sys.stderr)
    time.sleep(0.6)
    if s is None: continue
    if not s: vacias.append("%s ← %s" % (q, page)); continue
    larga = [x for x in s if re.search(r"\d", x) and x != q]
    tit = page.split(" · ", 1)[-1].lower() if page else ""
    rows.append("- **%s** (%d) %s%s\n  %s" % (q, len(s), page, "" if not tit or all(w in tit for w in s[0].split() if len(w) > 3) else " · ⚠ title sin «%s»" % s[0],
                                              "; ".join(s[:8]) + (" · cola numérica: " + "; ".join(larga[:6]) if larga else "")))
out = ["# Demanda por autocompletado (%s) · %s" % (proj, time.strftime("%Y-%m-%d")),
       "Semillas sin ninguna sugerencia (%d): la forma del title no es una consulta real → reescribir con la consulta sugerida:" % len(vacias)]
out += ["- " + v for v in vacias] + ["", "## Con sugerencias (%d)" % len(rows)] + rows
txt = "\n".join(out)
if "--out" in sys.argv: open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8").write(txt + "\n")
print(txt)
