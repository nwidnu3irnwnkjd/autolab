#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/residencia-o-cuidador-a-domicilio.js, escrito desde la especificacion.
Uso: python3 ops/verif/residencia-o-cuidador-a-domicilio.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "residencia-o-cuidador-a-domicilio"
def oraculo(d):
    f = 365.0 / 12                                         # dias por mes
    tarifa = d["costeh"] * (1 + d["cotiz"] / 100.0) * f     # coste mensual de 1 h diaria de cuidador, con cotizacion
    cuid = d["horas"] * tarifa
    adapt = d["adapt"] / (d["anios"] * 12.0)
    resi = d["resi"] - d["ayudas"]
    dom = cuid + adapt + d["fam"] - d["ayudas"]
    domEf = cuid + adapt - d["ayudas"]
    eq = max(0.0, (d["resi"] - adapt - d["fam"]) / tarifa) if tarifa > 0 else -1
    g = 0 if dom < resi - 0.005 else (1 if dom > resi + 0.005 else 2)
    return {"cuidadorMes": cuid, "adaptMes": adapt, "costeResi": resi, "costeDom": dom, "costeDomEfectivo": domEf,
            "diferencia": resi - dom, "horasEquilibrio": eq, "ganador": g}
B = dict(resi=2500, horas=6, costeh=12, cotiz=30, adapt=6000, anios=5, fam=400, ayudas=0)
TESTS = [dict(B),                                   # base
         dict(B, horas=16),                         # muchas horas: residencia
         dict(B, horas=0, adapt=0, fam=0),          # sin cuidado
         dict(B, horas=2, fam=0),                     # pocas horas: domicilio gana
         dict(B, resi=0),                             # residencia 0: equilibrio 0
         dict(B, ayudas=500, anios=1),
         dict(B, costeh=0, horas=0, adapt=0, fam=2500)]  # tarifa 0 y empate exacto              # ayudas y adaptacion a 1 anio
def rnd(r):
    return dict(resi=r.choice([0, 1500, 2500, 3500]) + r.random() * 50, horas=r.choice([0, 2, 6, 10, 16, 24]) + r.random() * 0.9,
                costeh=r.choice([0, 8, 12, 15]) + r.random(), cotiz=r.choice([0, 20, 33, 40]) + r.random(),
                adapt=r.choice([0, 3000, 8000]) + r.random() * 100, anios=r.choice([1, 3, 5, 10, 20]), fam=r.choice([0, 200, 600, 1500]) + r.random() * 20,
                ayudas=r.choice([0, 0, 200, 600]) + r.random() * 10)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(37); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k == "horasEquilibrio" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["cuidadorMes", "adaptMes", "costeResi", "costeDom", "costeDomEfectivo", "diferencia", "horasEquilibrio", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
