#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/gasolinera-low-cost-compensa-desviarse.js, escrito desde la especificacion.
Uso: python3 ops/verif/gasolinera-low-cost-compensa-desviarse.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "gasolinera-low-cost-compensa-desviarse"
def oraculo(d):
    bruto = d["litros"] * d["dif"]
    lkm = d["cons"] / 100.0                                       # litros por km
    comb = d["km"] * lkm * d["precio"]
    horas = d["km"] / d["vel"] if d["vel"] > 0 else 0
    tiempo = horas * d["valorHora"]
    ckm = lkm * d["precio"] + ((d["valorHora"] / d["vel"]) if d["vel"] > 0 else 0)
    return {"bruto": bruto, "combustible": comb, "tiempo": tiempo, "neto": bruto - comb - tiempo,
            "kmEquilibrio": bruto / ckm if ckm > 0 else -1, "litrosMin": (d["km"] * ckm / d["dif"]) if d["dif"] > 0 else -1}
B = dict(litros=40, dif=0.08, km=6, cons=6.5, precio=1.833, valorHora=0, vel=40)
TESTS = [dict(B),                                  # base: compensa
         dict(B, km=40),                           # desvio largo: no compensa
         dict(B, km=0),                            # 0 km: ahorro bruto
         dict(B, dif=0),                           # sin diferencia de precio
         dict(B, valorHora=15, km=10),             # contando el tiempo
         dict(B, cons=0, valorHora=0)]             # sin coste por km: sin limite
def rnd(r):
    return dict(litros=r.choice([5, 20, 40, 70]) + r.random(), dif=r.choice([0, 0.03, 0.08, 0.15]) + r.random() * 0.01,
                km=r.choice([0, 2, 6, 15, 40]) + r.random(), cons=r.choice([0, 4.5, 6.5, 9]) + r.random() * 0.1,
                precio=r.choice([1.4, 1.833, 1.95]) + r.random() * 0.01, valorHora=r.choice([0, 0, 8, 20]) + r.random(),
                vel=r.choice([0, 30, 40, 60]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(37); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0.01 if k in ("kmEquilibrio", "litrosMin") else 1.0
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["bruto", "combustible", "tiempo", "neto", "kmEquilibrio", "litrosMin"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
