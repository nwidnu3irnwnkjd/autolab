#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/marca-blanca-o-marca-ahorro-anual.js, escrito desde la especificacion.
Uso: python3 ops/verif/marca-blanca-o-marca-ahorro-anual.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "marca-blanca-o-marca-ahorro-anual"
def oraculo(d):
    gasto = d["gasto"] * d["meses"] * 52.0 / 12          # gasto del periodo
    base = gasto * d["pct"] / 100.0 * (1 - d["excl"] / 100.0)   # parte de la cesta que cambiarias
    ahorro = base * d["dif"] / 100.0
    g = 3 if base <= 0 else (0 if ahorro > d["minimo"] + 0.005 else (1 if ahorro < d["minimo"] - 0.005 else 2))
    return {"gastoAnual": gasto, "baseCambio": base, "ahorroAnual": ahorro, "ahorroMes": ahorro / d["meses"],
            "pctGasto": ahorro / gasto * 100 if gasto > 0 else 0, "porPersona": ahorro / d["personas"],
            "difEquilibrio": d["minimo"] / base * 100 if base > 0 else -1, "ganador": g}
B = dict(gasto=120, pct=40, dif=25, excl=20, personas=3, meses=12, minimo=100)
TESTS = [dict(B),                       # base: cambiar
         dict(B, dif=3),                # diferencia pequena: mantener
         dict(B, pct=0),                # nada cambiable
         dict(B, dif=0, minimo=0),      # sin diferencia ni minimo: base>0 empate
         dict(B, excl=100),             # descartas todo
         dict(B, meses=1, personas=1)]  # 1 mes
def rnd(r):
    return dict(gasto=r.choice([0, 40, 80, 120, 200, 350]) + r.random() * 5, pct=r.choice([0, 10, 40, 70, 100]) + r.random(),
                dif=r.choice([0, 3, 10, 25, 50]) + r.random(), excl=r.choice([0, 20, 50, 100]) * (1 if r.random() < .9 else 0) + r.random() * 0,
                personas=r.choice([1, 2, 3, 5]), meses=r.choice([1, 6, 12]), minimo=r.choice([0, 50, 100, 300]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("pctGasto", "difEquilibrio") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["gastoAnual", "baseCambio", "ahorroAnual", "ahorroMes", "pctGasto", "porPersona", "difEquilibrio", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
