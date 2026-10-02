#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/fondo-de-emergencia-cuantos-meses-necesito.js, escrito desde la especificacion.
Uso: python3 ops/verif/fondo-de-emergencia-cuantos-meses-necesito.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, math, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "fondo-de-emergencia-cuantos-meses-necesito"
def oraculo(d):
    base = {0: 3, 1: 6, 2: 6}[d["empleo"]]
    m = base + (1 if d["ingresos"] == 1 else 0) + min(0.5 * d["dep"], 2) - (1 if d["otro"] == 1 else 0)
    m = max(3, min(12, m))
    obj = m * d["gastos"]
    falta = max(obj - d["ahorro"], 0)
    falta1 = max(d["gastos"] - d["ahorro"], 0)
    cob = d["ahorro"] / d["gastos"]
    def tiempo(f):
        if f == 0: return 0
        return math.ceil(f / d["aport"]) if d["aport"] > 0 else -1
    alc, h1 = tiempo(falta), tiempo(falta1)
    if falta == 0: g = 0          # cubierto
    elif alc < 0: g = 3           # sin aportacion
    elif alc <= 12: g = 1         # en 12 meses o menos
    else: g = 2                   # mas de 12
    return {"meses": m, "objetivo": obj, "falta": falta, "cobertura": cob, "mesesAlcanzar": alc, "mesesHito1": h1, "ganador": g}
B = dict(gastos=1500, empleo=0, ingresos=0, dep=1, otro=0, ahorro=3000, aport=200)
TESTS = [dict(B),                                            # base: 3,5 meses, 5250 objetivo
         dict(B, empleo=2, ingresos=1, dep=2),               # autonomo variable con 2 dependientes: 8
         dict(B, ahorro=6000),                               # ya cubierto
         dict(B, aport=0),                                   # sin aportacion
         dict(B, empleo=1, ingresos=1, dep=10, otro=0),      # tope 12
         dict(B, dep=0, otro=1),                             # minimo 3 (3-1=2 -> 3)
         dict(B, ahorro=5250),                               # justo en el objetivo
         dict(B, aport=50, ahorro=0)]                        # largo plazo
def rnd(r):
    return dict(gastos=r.choice([300, 900, 1500, 3000]) + r.random() * 50, empleo=r.choice([0, 1, 2]), ingresos=r.choice([0, 1]),
                dep=r.choice([0, 1, 2, 3, 4, 10]), otro=r.choice([0, 1]),
                ahorro=r.choice([0, 500, 3000, 10000, 40000]) * r.random(), aport=r.choice([0, 0, 50, 200, 800]) + r.random() * 10)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(52); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "mesesAlcanzar", "mesesHito1", "meses") else (0.01 if k == "cobertura" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["meses", "objetivo", "falta", "cobertura", "mesesAlcanzar", "mesesHito1", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
