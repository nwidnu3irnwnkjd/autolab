#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/navidad-cuanto-gastar-sin-endeudarte.js. Intereses por simulacion mes a mes del saldo (no formula cerrada).
Uso: python3 ops/verif/navidad-cuanto-gastar-sin-endeudarte.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "navidad-cuanto-gastar-sin-endeudarte"
def interes(P, n, tin):
    if P <= 0: return 0.0, 0.0
    i = tin / 1200.0
    if i == 0: return 0.0, P / n
    lo, hi = 0.0, P * 2  # cuota por biseccion: la que deja saldo 0 tras n meses
    for _ in range(200):
        c = (lo + hi) / 2; s = P
        for _ in range(n): s = s * (1 + i) - c
        if s > 0: lo = c
        else: hi = c
    return c * n - P, c
def oraculo(d):
    margen = d["ingresos"] - d["gastos"] - d["ahorro"]
    presup = max(margen, 0) * d["meses"]
    colchon = d["gastos"] * d["mesesFondo"]
    exceso = max(d["fondo"] - colchon, 0); falta_fondo = max(colchon - d["fondo"], 0)
    falta = max(d["gasto"] - presup, 0)
    i3, _ = interes(d["gasto"], 3, d["tin"]); i6, _ = interes(d["gasto"], 6, d["tin"]); i12, c12 = interes(d["gasto"], 12, d["tin"])
    iF, _ = interes(falta, 12, d["tin"])
    if d["gasto"] <= presup + 0.005: g = 0
    elif d["gasto"] <= presup + exceso + 0.005: g = 1
    else: g = 2
    return {"margen": margen, "presupuesto": presup, "colchon": colchon, "exceso": exceso, "faltaFondo": falta_fondo,
            "ahorroNecesario": d["gasto"] / d["meses"], "falta": falta, "sobra": max(presup - d["gasto"], 0),
            "int3": i3, "int6": i6, "int12": i12, "cuota12": c12 if d["gasto"] > 0 else 0.0, "intFalta12": iF, "ganador": g}
B = dict(ingresos=2200, gastos=1500, ahorro=200, fondo=4000, mesesFondo=3, gasto=600, meses=3, tin=18)
TESTS = [dict(B),                                  # base: margen 500, presupuesto 1500, cabe
         dict(B, gasto=2000),                      # no cabe: falta 500, fondo 4000 < colchon 4500
         dict(B, gasto=1800, fondo=6000),          # solo con exceso del fondo (1500)
         dict(B, ahorro=900),                      # ahorro objetivo mayor que el margen: margen negativo, presupuesto 0
         dict(B, gasto=0),                         # gasto 0
         dict(B, meses=1, tin=0)]                  # 1 mes y TIN 0
def rnd(r):
    return dict(ingresos=r.choice([800, 1500, 2500, 5000]) + r.random() * 50, gastos=r.choice([0, 600, 1200, 2000, 4000]) + r.random() * 50,
                ahorro=r.choice([0, 100, 300, 1000]) + r.random() * 20, fondo=r.choice([0, 1000, 5000, 20000]) + r.random() * 50,
                mesesFondo=r.choice([0, 1, 3, 6, 12]) + r.random(), gasto=r.choice([0, 200, 800, 2500, 8000]) + r.random() * 30,
                meses=r.choice([1, 2, 3, 6, 10, 12]), tin=r.choice([0, 5, 12, 20, 24, 40]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            tol = 0 if k == "ganador" else 1.0
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["margen", "presupuesto", "ahorroNecesario", "falta", "int3", "int6", "int12", "cuota12", "intFalta12", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
