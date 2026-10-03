#!/usr/bin/env python3
"""Casos del Verificador fiscal (2026-10-03) para nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad.
Ejecuta el JS con los casos y los compara con el oraculo del Constructor; ademas comprueba la coherencia del texto
cuando base27 != base 2026 (sube = dMei + dSol + dBase; la frase de solidaridad debe usar la misma referencia que dSol)."""
import importlib.util, json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(os.path.dirname(here))
s = importlib.util.spec_from_file_location("o", os.path.join(here, "nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad_oraculo.py")); o = importlib.util.module_from_spec(s); s.loader.exec_module(o)
CASOS = [dict(bruto=90000, contrato="indefinido", base27=5356.26), dict(bruto=62000, contrato="indefinido", base27=5356.26),
         dict(bruto=90000, contrato="indefinido", base27=4800), dict(bruto=91821.6, contrato="temporal", base27=5101.2),
         dict(bruto=67335.84, contrato="temporal", base27=5101.2), dict(bruto=1000000, contrato="indefinido", base27=5101.2)]
js = open(os.path.join(root, "projects/decidir/calcs/nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad.js")).read().split("function eur(")[0]
res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(" + json.dumps(CASOS) + ".map(calcular));"], capture_output=True, text=True, check=True).stdout)
bad = 0
for c, r in zip(CASOS, res):
    e = o.oraculo(c)
    for k, v in e.items():
        if abs(r[k] - v) > 0.011: bad += 1; print("DIF", c, k, r[k], v)
    if abs(r["sube"] - (r["dMei"] + r["dSol"] + r["dBase"])) > 0.011: bad += 1; print("SUMA", c)
    if r["dBase"] != 0: print("TEXTO a revisar (dBase != 0):", c["bruto"], c["base27"], "sube", round(r["sube"], 2), "dBase", round(r["dBase"], 2), "sol26->sol27", round(r["sol26"], 2), round(r["sol27"], 2), "dSol", round(r["dSol"], 2))
print(f"{len(CASOS)} casos, discrepancias: {bad}"); sys.exit(1 if bad else 0)
