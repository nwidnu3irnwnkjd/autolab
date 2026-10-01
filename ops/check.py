#!/usr/bin/env python3
"""Ejecuta los casos de prueba de cada calculadora con JavaScriptCore (osascript -l JavaScript; viene con macOS).
Convención: en cada calcs/<slug>.js, las funciones puras van antes de la línea que empieza por 'function eur('.
Uso: python3 ops/check.py [proyecto]  (por defecto, todos)"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
projs = [sys.argv[1]] if len(sys.argv) > 1 else sorted(os.listdir(os.path.join(ROOT, "projects")))
fails = 0; total = 0
for p in projs:
    cdir = os.path.join(ROOT, "projects", p, "calcs")
    if not os.path.isdir(cdir): continue
    for f in sorted(os.listdir(cdir)):
        if not f.endswith(".test.json"): continue
        slug = f[:-10]; t = json.load(open(os.path.join(cdir, f)))
        js = open(os.path.join(cdir, slug + ".js")).read().split("function eur(")[0]
        harness = js + f"\nJSON.stringify({json.dumps(t['cases'])}.map(function(c){{return {t['func']}(c['in']);}}));"
        out = subprocess.run(["osascript", "-l", "JavaScript", "-e", harness], capture_output=True, text=True)
        if out.returncode != 0: print(f"✗ {p}/{slug}: error JS: {out.stderr.strip()}"); fails += 1; continue
        results = json.loads(out.stdout.strip())
        for c, r in zip(t["cases"], results):
            for k, v in c["expect"].items():
                total += 1
                if r.get(k) is None or abs(r[k] - v) > c.get("tol", 0.01):
                    print(f"✗ {p}/{slug} {c['in']} → {k}={r.get(k)} (esperado {v})"); fails += 1
# Barómetro (Estratega): cada cifra de /barometro/ debe coincidir con la calculadora real
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "check_barometro.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "check_barometro.py")]).returncode != 0: fails += 1
print(f"{'OK' if not fails else 'FALLOS'}: {total - fails}/{total} comprobaciones")
sys.exit(1 if fails else 0)
