#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/seguro-hogar-con-o-sin-franquicia.js, escrito desde la especificacion.
Uso: python3 ops/verif/seguro-hogar-con-o-sin-franquicia.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "seguro-hogar-con-o-sin-franquicia"
def oraculo(d):
    H = max(int(round(d["horizonte"])), 1); ah = d["primaSin"] - d["primaCon"]; pg = min(d["coste"], d["franq"])
    pe = d["frec"] * pg; ne = ah - pe
    return {"ahorroAnual": ah, "ahorroTotal": ah * H, "pagaSiniestro": pg, "perdidaAnual": pe, "perdidaTotal": pe * H,
            "netoAnual": ne, "netoTotal": ne * H, "frecEquilibrio": ah / pg if pg > 0 else -1,
            "aniosEntreSiniestros": pg / ah if (pg > 0 and ah > 0) else -1, "siniestrosEquilibrio": ah * H / pg if pg > 0 else -1,
            "peorAno1": d["franq"] - ah, "fondoCubre": 1 if d["fondo"] >= d["franq"] else 0,
            "tasaSin": d["primaSin"] / d["capital"] * 1000 if d["capital"] > 0 else -1,
            "mejor": 0 if ne > 1 else (1 if ne < -1 else 2)}
B = dict(primaSin=300, primaCon=240, franq=300, frec=0.15, coste=400, capital=100000, horizonte=10, fondo=2000)
TESTS = [dict(B),                       # base: compensa la franquicia
         dict(B, frec=0.5),             # frecuencia alta: compensa sin franquicia
         dict(B, frec=0),               # frecuencia 0
         dict(B, coste=0),              # coste 0
         dict(B, horizonte=1, fondo=100),   # 1 anio, fondo no cubre
         dict(B, primaCon=320)]         # prima con franquicia mayor
def rnd(r):
    return dict(primaSin=r.choice([100, 200, 300, 500]) + r.random() * 5, primaCon=r.choice([60, 150, 240, 450, 600]) + r.random() * 5,
                franq=r.choice([0, 100, 300, 600, 1500]) + r.random() * 5, frec=r.choice([0, 0.05, 0.15, 0.3, 1, 3, 10]),
                coste=r.choice([0, 100, 400, 1500]) + r.random() * 10, capital=r.choice([0, 50000, 100000, 300000]),
                horizonte=r.choice([1, 3, 10, 20, 30]), fondo=r.choice([0, 300, 1000, 5000]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(59); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["ahorroAnual", "perdidaAnual", "netoAnual", "netoTotal", "frecEquilibrio", "siniestrosEquilibrio", "peorAno1", "fondoCubre", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
