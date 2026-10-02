#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/reformar-o-mudarse.js, escrito desde la especificacion.
Uso: python3 ops/verif/reformar-o-mudarse.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "reformar-o-mudarse"
def oraculo(d):
    neto_ref = d["reforma"] * (1 - d["recup"] / 100.0)                       # inversion - valor recuperado
    fijo_mud = d["valor"] * d["gastosPct"] / 100.0 + d["dif"] + d["extras"]    # compraventa + diferencia + adecuacion
    # el % de gastos se aplica al valor de la vivienda (igual en origen y destino), la diferencia no tributa aqui
    cuota = 12.0 * d["mensual"]
    mud = fijo_mud + cuota * d["anios"]
    dif = mud - neto_ref                    # >0: mudarse cuesta mas
    # cruce: fijo_mud - neto_ref + cuota*T = 0
    t = (neto_ref - fijo_mud) / cuota if cuota != 0 else 0
    eq = t if (cuota != 0 and 0 < t <= 40) else -1
    cruce = (1 if cuota < 0 else 0) if eq > 0 else -1   # 1: tras el cruce gana mudarse; 0: gana reformar
    rmax = mud / (1 - d["recup"] / 100.0) if d["recup"] < 100 else -1
    g = 0 if dif > 1 else (1 if dif < -1 else 2)        # 0 reformar, 1 mudarse, 2 empate
    return {"costeReformar": neto_ref, "fijoMudarse": fijo_mud, "costeMudarse": mud, "diferencia": dif,
            "anioEq": eq, "cruce": cruce, "reformaMax": rmax, "ganador": g}
B = dict(reforma=20000, recup=50, valor=250000, gastosPct=10, dif=0, extras=3000, mensual=-50, anios=10)
TESTS = [dict(B),                                  # base: reformar sale mas barato (mudarse cuesta 28.000 + ahorro)
         dict(B, valor=100000, gastosPct=5, extras=1000, mensual=-150),   # mudarse barato y ahorra al mes
         dict(B, reforma=0),                       # coste 0
         dict(B, anios=1),                         # 1 anio
         dict(B, mensual=0, recup=100),            # sin cuota, recupera todo
         dict(B, mensual=80, reforma=60000, recup=30, gastosPct=3, extras=500)]  # mudarse cuesta mas cada mes
def rnd(r):
    return dict(reforma=r.choice([0, 5000, 15000, 40000, 90000]) + r.random() * 500, recup=r.choice([0, 30, 50, 80, 100]) + r.random(),
                valor=r.choice([0, 80000, 200000, 400000]) + r.random() * 1000, gastosPct=r.choice([0, 3, 8, 12]) + r.random(),
                dif=r.choice([-20000, 0, 10000, 40000]) + r.random() * 100, extras=r.choice([0, 1500, 6000, 20000]) + r.random() * 100,
                mensual=r.choice([-200, -50, 0, 60, 250]) + r.random(), anios=r.choice([1, 3, 7, 15, 40]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "cruce") else (0.01 if k == "anioEq" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
