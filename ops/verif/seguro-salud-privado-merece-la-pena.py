#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/seguro-salud-privado-merece-la-pena.js, escrito desde la especificacion (bucle ano a ano).
Uso: python3 ops/verif/seguro-salud-privado-merece-la-pena.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "seguro-salud-privado-merece-la-pena"
def oraculo(d):
    H = max(int(round(d["horizonte"])), 1); mia = 1 - min(max(d["empresa"], 0), 100) / 100.0
    con = sin = prim = cop = 0.0; fcs = 0.0
    for y in range(H):
        fp = (1 + d["subidaPrima"] / 100.0) ** y; fc = (1 + d["subidaPrecios"] / 100.0) ** y; fcs += fc
        prim += d["prima"] * mia * fp; cop += d["actos"] * d["copago"] * fc; sin += d["actos"] * d["coste"] * fc
    con = prim + cop; u = d["coste"] - d["copago"]
    return {"conSeguro": con, "sinSeguro": sin, "primas": prim, "copagos": cop, "diferencia": sin - con,
            "primaAno1": d["prima"] * mia, "actosEq": prim / (u * fcs) if u > 0 else -1, "actosEq1": d["prima"] * mia / u if u > 0 else -1,
            "ahorroPorActo": u, "mejor": 0 if con < sin - 1 else (1 if sin < con - 1 else 2)}
B = dict(prima=900, empresa=0, subidaPrima=4, actos=8, coste=60, copago=8, subidaPrecios=2, horizonte=10)
TESTS = [dict(B),                                  # base
         dict(B, actos=25),                        # muchos actos: gana el seguro
         dict(B, actos=0, horizonte=1),            # borde: 0 actos, 1 ano
         dict(B, empresa=50, subidaPrima=0, subidaPrecios=0),  # seguro de grupo, sin subidas
         dict(B, copago=60),                       # copago = coste: sin ahorro por acto
         dict(B, coste=0, copago=0)]               # coste 0
def rnd(r):
    return dict(prima=r.choice([200, 500, 900, 1500, 3000]) + r.random() * 30, empresa=r.choice([0, 0, 25, 50, 100]), subidaPrima=r.choice([0, 3, 6, 12]) + r.random(),
                actos=r.choice([0, 2, 5, 10, 20, 60]) + r.random() * 2, coste=r.choice([0, 30, 60, 120]) + r.random() * 5, copago=r.choice([0, 3, 10, 30, 70]) + r.random(),
                subidaPrecios=r.choice([0, 2, 5]) + r.random(), horizonte=r.choice([1, 3, 10, 20, 40]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "mejor" else 1.0
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["conSeguro", "sinSeguro", "primas", "copagos", "diferencia", "actosEq", "actosEq1", "ahorroPorActo", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 3 if k.startswith("actosEq") else 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
