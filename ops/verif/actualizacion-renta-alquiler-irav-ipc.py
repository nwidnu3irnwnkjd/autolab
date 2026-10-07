#!/usr/bin/env python3
"""Verificador (2026-10-07, RDL 29/2026): casos propios + barrido con tolerancia 0,011 € mensual / 0,13 € anual (el oraculo del Constructor usa 1 €, demasiado laxa).
Lectura propia del XML BOE-A-2026-20823: DF 6.a (a: renta > indice estatal -> ningun incremento; b: nuevo pacto, sin el <= 2 %),
art. 3.Once (LAU 18.1: sin pacto no hay actualizacion; clausula sin indice -> IRAV; IRAV tope «en todo caso»),
art. 4.Dos (DT 4.a.1 Ley 12/2023: contratos anteriores al 26-5-2023 se actualizan con el limite de la DA 11.a y el 18.1 del RDL 29)."""
import json, os, random, subprocess, sys, importlib.util
B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("o", os.path.join(B, "ops/verif/actualizacion-renta-alquiler-irav-ipc_oraculo.py"))
O = importlib.util.module_from_spec(spec); spec.loader.exec_module(O)
JS = open(os.path.join(B, "projects/decidir/calcs/actualizacion-renta-alquiler-irav-ipc.js")).read().split("function eur(")[0]
def c(**k):
    d = dict(renta=800, firma="post", indice="ipc", aniv="2026-10-08", irav=2.47, ipc=4.3, pide=0, sup="no"); d.update(k); return d
# (entrada, esperado propio: pct, nueva)
PROPIOS = [
    (c(ipc=1.5), 1.5, 812.0),                                   # clausula IPC < 2 % en ventana: manda la clausula (DF 6.a b es techo)
    (c(indice="igc", irav=1.8), 1.8, 814.4),                    # sin indice -> IRAV < 2 %
    (c(sup="si", aniv="2028-01-01"), 2.47, 819.76),             # supera indice fuera de ventana: sin efecto
    (c(sup="si", aniv="2000-01-01"), 2.47, 819.76),             # aniversario hasta el 7-10: sin DF 6.a
    (c(indice="igc", firma="pre", aniv="2028-01-01"), 2.47, 819.76),  # DT 4.a Ley 12/2023 (red. RDL 29): IRAV, no IGC
    (c(irav=-0.5), 0.0, 800.0),                                 # IRAV negativo en ventana
    (c(renta=1234.57, aniv="2027-12-01"), 2.0, 1259.26),        # ultimo tramo de ventana, redondeo
    (c(firma="ant", indice="igc", aniv="2027-06-01"), 2.0, 816.0),
    (c(indice="none", aniv="2028-01-01", ipc=9), 0.0, 800.0),
]
def run(cases):
    h = JS + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    return json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
bad = 0
for (d, p, n), r in zip(PROPIOS, run([x[0] for x in PROPIOS])):
    if abs(r["pct"] - p) > 1e-9 or abs(r["nueva"] - n) > 0.005: bad += 1; print("PROPIO", d, r["pct"], r["nueva"], "esperado", p, n)
random.seed(29); cases = []
for _ in range(1500):
    cases.append(dict(renta=round(random.uniform(1, 3000), 2), firma=random.choice(["post", "pre", "ant"]), indice=random.choice(["none", "ipc", "igc", "otro"]),
                      aniv=random.choice(O.ANIVS), irav=round(random.uniform(-1, 6), 2), ipc=round(random.uniform(-2, 9), 2),
                      pide=random.choice([0, round(random.uniform(0, 3500), 2)]), sup=random.choice(["no", "si", "nls"])))
for d, r in zip(cases, run(cases)):
    for k, v in O.oraculo(d).items():
        tol = 0.13 if k.endswith("Anio") else 0.011   # el oraculo redondea a 0,5 cent distinto y anualiza sin redondear el mes (JS: mes redondeado x 12, correcto)
        if r.get(k) is None or abs(r[k] - v) > tol: bad += 1; print("DIF", d, k, r.get(k), v)
print(f"{len(PROPIOS)} propios + {len(cases)} aleatorios (tol 0,011/0,13): discrepancias {bad}"); sys.exit(1 if bad else 0)
