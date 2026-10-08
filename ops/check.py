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
# Ejemplos resueltos de las insignia (ops/gen_ejemplos.py --check): el JSON vigente debe coincidir con la calculadora real
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "gen_ejemplos.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "gen_ejemplos.py"), "--check"]).returncode != 0: fails += 1
# Tablas de respuesta de la cola numérica (ops/gen_tablas_respuesta.py --check)
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "gen_tablas_respuesta.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "gen_tablas_respuesta.py"), "--check"]).returncode != 0: fails += 1
# Tabla fija de sueldo-bruto-a-neto-2026 (ops/gen_tabla_sueldo.py --check, R60.2)
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "gen_tabla_sueldo.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "gen_tabla_sueldo.py"), "--check"]).returncode != 0: fails += 1
# Pulso / datos vivos (Estratega): sin red
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "check_live.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "check_live.py")]).returncode != 0: fails += 1
# Campos numéricos (type=text, data-n): normalización de em.js + data-dec (ops/test_numinput.py; BLOQUEANTE)
if "decidir" in projs and os.path.exists(os.path.join(ROOT, "ops", "test_numinput.py")):
    if subprocess.run([sys.executable, os.path.join(ROOT, "ops", "test_numinput.py")]).returncode != 0: fails += 1
print(f"{'OK' if not fails else 'FALLOS'}: {total - fails}/{total} comprobaciones")
sys.exit(1 if fails else 0)
