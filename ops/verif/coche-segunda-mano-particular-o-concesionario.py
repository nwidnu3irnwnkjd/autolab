#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/coche-segunda-mano-particular-o-concesionario.js, escrito desde la especificacion.
Uso: python3 ops/verif/coche-segunda-mano-particular-o-concesionario.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "coche-segunda-mano-particular-o-concesionario"
def oraculo(d):
    esperada = d["prob"] / 100.0 * d["averia"]                  # averia esperada
    part = d["precioPart"] + d["trasp"] + d["revision"] + d["reparPrev"] + esperada
    conc = d["precioConc"] + d["reparPrev"] + esperada * (1 - d["cobertura"] / 100.0)
    eq = d["trasp"] + d["revision"] + esperada * d["cobertura"] / 100.0
    pe = (d["precioConc"] - d["precioPart"] - d["trasp"] - d["revision"]) / (d["averia"] * d["cobertura"] / 100.0) * 100 if d["averia"] * d["cobertura"] > 0 else -1
    return {"costePart": part, "costeConc": conc, "diferencia": part - conc, "prima": d["precioConc"] - d["precioPart"], "primaEquilibrio": eq,
            "probEquilibrio": pe, "ganador": 0 if part < conc else 1}
B = dict(precioPart=12000, precioConc=13500, reparPrev=400, averia=1500, prob=20, cobertura=50, trasp=300, revision=100)
TESTS = [dict(B),                                                    # base: gana particular
         dict(B, precioConc=12500, prob=40, averia=3000),            # riesgo alto y poca prima: gana concesionario
         dict(B, prob=0, averia=0),                                  # sin riesgo: solo gastos de compra
         dict(B, cobertura=0),                                       # garantia que no cubre nada
         dict(B, precioConc=11000),                                  # concesionario mas barato que particular
         dict(B, prob=100, cobertura=100, averia=5000, trasp=0, revision=0)]  # borde: 100 %
def rnd(r):
    return dict(precioPart=r.choice([3000, 8000, 12000, 20000]) + r.random() * 100, precioConc=r.choice([3500, 9000, 13500, 22000]) + r.random() * 100,
                reparPrev=r.choice([0, 200, 800]) + r.random(), averia=r.choice([0, 800, 1500, 4000]) + r.random() * 10,
                prob=r.choice([0, 10, 25, 60, 100]) + r.random() * 0.5, cobertura=r.choice([0, 30, 50, 100]) + r.random() * 0.5,
                trasp=r.choice([0, 300, 900]) + r.random(), revision=r.choice([0, 100, 250]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            tol = 0 if k == "ganador" else (0.01 if k == "probEquilibrio" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                if k == "ganador" and abs(o["diferencia"]) < 1e-6: continue
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costePart", "costeConc", "diferencia", "prima", "primaEquilibrio", "probEquilibrio", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
