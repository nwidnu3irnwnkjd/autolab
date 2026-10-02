#!/usr/bin/env python3
"""Casos del Verificador fiscal (2026-10-03) para jubilarse-en-2026-o-en-2027-edad-y-pension. Ejecuta el JS y comprueba lo que exige journal/verificacion-<slug>.md.
V1 demora: quien alcanzo la edad ordinaria con la regla de 2025 (66a8m, < 38a3m) suma esos meses (art. 210.2.a: 'fecha en que cumplio dicha edad'); demoraPosible debe ser 1.
V2 revalorizacion (art. 58.2): debe existir a26_pension_ene27 = a26_pension x (1 + reval) con reval = 2,7 % (RD 241/2026, hipotesis para 2027) y el veredicto compararla con a27_pension.
V3 regresion: ejemplos de la pagina (96,77 % / 96,17 %, BR 2.022,86; 3.112,75 vs 3.085,71)."""
import json, subprocess, os, sys
base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
js = open(os.path.join(base, "projects/decidir/calcs/jubilarse-en-2026-o-en-2027-edad-y-pension.js")).read().split("function eur(")[0]
C = lambda a, m, ca, cm, br, ba: dict(nac_a=a, nac_m=m, cot_a=ca, cot_m=cm, b_rec=br, b_ant=ba)
casos = [
 ("V1 feb-1959 36a", C(1959, 2, 36, 0, 3000, 2200), lambda r: r.get("demoraPosible") == 1),
 ("V1 mar-1959 36a", C(1959, 3, 36, 0, 3000, 2200), lambda r: r.get("demoraPosible") == 1),
 ("V1 abr-1959 36a", C(1959, 4, 36, 0, 3000, 2200), lambda r: r.get("demoraPosible") == 1),
 ("V1 may-1959 36a (no)", C(1959, 5, 36, 0, 3000, 2200), lambda r: r.get("demoraPosible") == 0),
 ("V2 ene-1960 reval", C(1960, 1, 35, 0, 3000, 2200), lambda r: abs(r.get("a26_pension_ene27", -1) - r["a26_pension"] * 1.027) < 0.01),
 ("V2 ago-1961 reval>dif", C(1961, 8, 45, 3, 1114, 3051), lambda r: r.get("a26_pension_ene27", 0) > r["a27_pension"]),
 ("V3 ene-1960 pct", C(1960, 1, 35, 0, 3000, 2200), lambda r: abs(r["a26_pct"] - 96.77) < 1e-6 and abs(r["a27_pct"] - 96.17) < 1e-6 and abs(r["a26_br"] - 2022.857) < 0.01 and r["a26_t"] == 2026*12+10 and r["a27_t"] == 2027*12),
 ("V3 mar-1960 br", C(1960, 3, 37, 0, 2000, 4000), lambda r: r["a26_estado"] == 1 and abs(r["a27_brNew"] - 3112.75) < 0.01 and abs(r["a27_brOld"] - 3085.71) < 0.01 and r["a27_pct"] == 100),
]
h = js + "\nJSON.stringify(" + json.dumps([c for _, c, _ in casos]) + ".map(function(c){return calcular(c);}));"
res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
bad = 0
for (n, c, f), r in zip(casos, res):
    try: ok = f(r)
    except Exception: ok = False
    bad += not ok; print(("OK  " if ok else "FALLA ") + n)
print(f"{len(casos)} casos, fallos: {bad}"); sys.exit(1 if bad else 0)
