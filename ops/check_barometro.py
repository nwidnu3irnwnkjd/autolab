#!/usr/bin/env python3
"""Comprueba que cada cifra del Barómetro (/barometro/ y /barometro/datos.json) coincide con lo que da la
calculadora real: ejecuta las funciones puras de calcs/<slug>.js con JavaScriptCore (osascript) con las mismas
entradas que usó barometro.py y compara. También verifica que dist/barometro/datos.json está al día.
Uso: python3 ops/check_barometro.py   (lo llama ops/check.py decidir)"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "projects", "decidir")
sys.path.insert(0, P)
import barometro  # noqa: E402

site = json.load(open(os.path.join(P, "data/site.json")))
params = json.load(open(os.path.join(P, "data/params.json")))
D = barometro.compute(params, site["base_url"].rstrip("/"))
fails = total = 0
dj = os.path.join(P, "dist", "barometro", "datos.json")
if os.path.exists(dj):
    total += 1
    if json.load(open(dj)) != json.loads(json.dumps(D, ensure_ascii=False)):
        print("✗ barometro: dist/barometro/datos.json no coincide con el cálculo actual (¿falta python3 build.py?)"); fails += 1
by_calc = {}
for c in D["comprobaciones"]: by_calc.setdefault(c["calc"], []).append(c)
for slug, cs in by_calc.items():
    js = open(os.path.join(P, "calcs", slug + ".js")).read().split("function eur(")[0]
    calls = [{"f": c["func"], "a": c["args"]} for c in cs]
    harness = js + f"\nJSON.stringify({json.dumps(calls)}.map(function(c){{return eval(c.f).apply(null, c.a);}}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", harness], capture_output=True, text=True)
    if out.returncode != 0:
        print(f"✗ barometro/{slug}: error JS: {out.stderr.strip()}"); fails += 1; continue
    for c, res in zip(cs, json.loads(out.stdout.strip())):
        for k, v in c["salida"].items():
            total += 1
            got = res.get(k)
            if got is None or v is None or abs(got - v) > 0.01:
                print(f"✗ barometro/{slug} {c['func']} {k}: JS={got} barómetro={v}"); fails += 1
print(f"{'OK' if not fails else 'FALLOS'} barómetro: {total - fails}/{total} cifras coinciden con las calculadoras")
sys.exit(1 if fails else 0)
