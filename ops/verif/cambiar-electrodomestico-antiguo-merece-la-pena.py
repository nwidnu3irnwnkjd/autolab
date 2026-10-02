#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/cambiar-electrodomestico-antiguo-merece-la-pena.js, escrito desde la especificacion.
Uso: python3 ops/verif/cambiar-electrodomestico-antiguo-merece-la-pena.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cambiar-electrodomestico-antiguo-merece-la-pena"
def oraculo(d):
    dif = d["act"] - d["nue"]
    ahorro = dif * d["luz"]
    neto = max(d["coste"] - d["reventa"], 0.0)
    if neto == 0: pb = 0.0
    elif ahorro > 0: pb = neto / ahorro
    else: pb = -1.0
    acum = ahorro * d["anos"]
    saldo = acum - neto
    cuota = neto / d["anos"]
    return {"ahorroKwh": dif, "ahorroAnual": ahorro, "neto": neto, "anosAmort": pb, "kwhEvitados": dif * d["anos"],
            "ahorroAcum": acum, "saldo": saldo, "costeAnualizado": cuota, "ventajaAnual": ahorro - cuota,
            "ventajaAdelantar": d["resta"] * (ahorro - cuota),
            "minKwh": neto / (d["anos"] * d["luz"]) if d["luz"] > 0 else -1.0,
            "compensa": 1 if (saldo >= 0 and dif > 0) else 0}
B = dict(act=300, nue=170, coste=650, reventa=0, luz=0.23, anos=10, resta=5)
TESTS = [dict(B),                                                   # nevera ejemplo: no compensa
         dict(act=450, nue=200, coste=700, reventa=100, luz=0.27, anos=10, resta=5),   # secadora: compensa
         dict(B, reventa=650),                                      # coste neto 0
         dict(B, nue=300),                                          # ahorro 0
         dict(B, nue=400),                                          # ahorro negativo
         dict(B, luz=0, resta=0)]                                   # luz 0
def rnd(r):
    return dict(act=r.choice([0, 100, 150, 300, 450, 600]) + r.random() * 30, nue=r.choice([0, 60, 90, 170, 250, 500]) + r.random() * 30,
                coste=r.choice([100, 300, 500, 650, 900, 1500]) + r.random() * 40, reventa=r.choice([0, 0, 50, 150, 400, 900]) + r.random() * 10,
                luz=r.choice([0, 0.1, 0.18, 0.23, 0.3, 0.4]), anos=r.choice([1, 3, 5, 8, 10, 15, 20, 30]), resta=r.choice([0, 1, 3, 5, 10]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["ahorroAnual", "neto", "anosAmort", "saldo", "minKwh", "ventajaAdelantar", "compensa"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
