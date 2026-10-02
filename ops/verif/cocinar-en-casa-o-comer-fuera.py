#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/cocinar-en-casa-o-comer-fuera.js, escrito desde la especificacion.
Uso: python3 ops/verif/cocinar-en-casa-o-comer-fuera.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cocinar-en-casa-o-comer-fuera"
def oraculo(d):
    sem = d["dias"] / 5.0                                  # semanas laborables
    fuera, sust = d["fuera"] * sem, d["sust"] * sem        # comidas al anio
    fuera_c = d["precio"] + d["minDesp"] / 60.0 * d["vh"]  # coste por comida fuera con tiempo
    casa_c = d["racion"] + d["minCook"] / 60.0 * d["vh"]
    ah = sust * (fuera_c - casa_c)
    dm, dt = d["precio"] - d["racion"], d["minCook"] - d["minDesp"]
    eq = dm / (dt / 60.0) if (dt > 0 and dm > 0) else -1
    return {"comidasAnio": fuera, "sustAnio": sust, "gastoFuera": fuera * d["precio"], "gastoCasaMismas": fuera * d["racion"],
            "costeFueraT": fuera * fuera_c, "costeCasaT": fuera * casa_c, "ahorroDinero": sust * dm, "ahorroTiempo": ah,
            "horasExtra": sust * dt / 60.0, "vhEq": eq, "difComida": fuera_c - casa_c,
            "ganador": 0 if ah > 1 else (1 if ah < -1 else 2)}
B = dict(fuera=3, precio=13, racion=4, minCook=30, minDesp=15, vh=0, sust=3, dias=220)
TESTS = [dict(B),                                   # base sin valorar tiempo: cocinar gana
         dict(B, vh=40),                            # hora cara: gana comer fuera
         dict(B, vh=10),                            # hora intermedia
         dict(B, racion=0, precio=0),               # coste 0
         dict(B, sust=0),                           # 0 sustituidas
         dict(B, dias=1, fuera=1, sust=1, minCook=10, minDesp=20, vh=30)]  # cocinar ahorra tiempo
def rnd(r):
    f = r.choice([0, 1, 2, 3, 5, 7])
    return dict(fuera=f, precio=r.choice([0, 9, 12, 15, 25]) + r.random() * 2, racion=r.choice([0, 2, 4, 8, 14]) + r.random() * 2,
                minCook=r.choice([0, 15, 30, 60, 90]) + r.random() * 5, minDesp=r.choice([0, 10, 20, 40]) + r.random() * 5,
                vh=r.choice([0, 0, 6, 12, 25, 60]) + r.random(), sust=r.choice([0, f, f / 2.0, 1]) if f else 0, dias=r.choice([1, 100, 220, 260, 366]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(97); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["comidasAnio", "gastoFuera", "gastoCasaMismas", "costeFueraT", "costeCasaT", "ahorroDinero", "ahorroTiempo", "horasExtra", "vhEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
