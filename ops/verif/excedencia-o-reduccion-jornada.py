#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/excedencia-o-reduccion-jornada.js, escrito desde la especificacion.
Uso: python3 ops/verif/excedencia-o-reduccion-jornada.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "excedencia-o-reduccion-jornada"
def oraculo(d):
    n, red, M = d["neto"], d["red"], d["dur"]
    pr = d["perdida"] if d["perdida"] > 0 else red          # % de perdida neta con reduccion
    hay = red > 0
    perdRed = n * pr / 100.0 if hay else 0.0
    ahRed = d["cuidados"] * red / 100.0 if hay else 0.0
    ayRed = d["ayudas"] if hay else 0.0
    cRed = perdRed - ayRed - ahRed if hay else 0.0           # coste neto mensual reduccion
    cExc = n - d["ayudas"] - d["cuidados"]                   # coste neto mensual excedencia
    cotRed = d["cotRed"] if d["cotRed"] > 0 else red
    mejor = min([("seguir", 0.0), ("reduccion", cRed), ("excedencia", cExc)], key=lambda x: x[1])
    cands = {"seguir": 0.0, "reduccion": cRed if hay else 1e18, "excedencia": cExc}
    mn = min(cands.values())
    w = [k for k in ("seguir", "reduccion", "excedencia") if abs(cands[k] - mn) < 1e-9]
    return {"perdidaMesRed": perdRed, "ahorroCuidadosRed": ahRed, "costeMesRed": cRed, "costeMesExc": cExc,
            "costeTotalRed": cRed * M, "costeTotalExc": cExc * M,
            "equilibrioCuidadosRed": (perdRed - ayRed) / (red / 100.0) if hay else -1.0,
            "equilibrioCuidadosExc": n - d["ayudas"],
            "costePor10Red": cRed / (red / 10.0) if hay else 0.0, "costePor10Exc": cExc / 10.0,
            "mesesCotRed": M * cotRed / 100.0 if hay else 0.0, "mesesCotExc": M * d["cotExc"] / 100.0,
            "cobertura": d["cuidados"] / n * 100 if n > 0 else 0.0,
            "ganador": {"seguir": 0, "reduccion": 1, "excedencia": 2}[min(cands, key=cands.get)]}
B = dict(neto=1800, red=30, perdida=0, dur=12, ayudas=0, cuidados=400, cotRed=0, cotExc=100)
TESTS = [dict(B),                               # base
         dict(B, perdida=24),                   # perdida neta menor que la reduccion (IRPF)
         dict(B, red=0),                        # 0 % de reduccion
         dict(B, dur=1),                        # 1 mes
         dict(B, cuidados=0, ayudas=0),         # sin ahorro ni ayudas
         dict(B, ayudas=900, cuidados=700)]     # ayudas y cuidados altos: la excedencia sale a favor
def rnd(r):
    return dict(neto=r.choice([900, 1400, 1800, 2600, 4000]) + r.random() * 20, red=r.choice([0, 12.5, 25, 33, 50]) + r.random(),
                perdida=r.choice([0, 0, 10, 25, 40]) + r.random(), dur=r.choice([1, 3, 6, 12, 24, 36]),
                ayudas=r.choice([0, 0, 100, 400, 1000]) + r.random() * 5, cuidados=r.choice([0, 200, 450, 900, 1500]) + r.random() * 5,
                cotRed=r.choice([0, 0, 20, 50]) + r.random(), cotExc=r.choice([0, 50, 100]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(59); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.02 if k.startswith("mesesCot") or k == "cobertura" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["perdidaMesRed", "costeMesRed", "costeMesExc", "costeTotalRed", "costeTotalExc", "equilibrioCuidadosRed", "equilibrioCuidadosExc", "mesesCotRed", "mesesCotExc", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
