#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/equipaje-y-asiento-avion-coste-real.js, escrito desde la especificacion.
Uso: python3 ops/verif/equipaje-y-asiento-avion-coste-real.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "equipaje-y-asiento-avion-coste-real"
def oraculo(d):
    lc = lambda n: d["lc"] + n * d["maleta"] + d["extras"]
    no = lambda n: d["normal"] + max(0, n - d["nincl"]) * d["maleta"]
    m = d["pax"] * d["tray"]; a, b = lc(d["nmal"]), no(d["nmal"]); dif = (a - b) * m
    n_eq = next((n for n in range(21) if lc(n) - no(n) > 0.005), -1)
    g = 1 if dif > 0.005 * m else (0 if dif < -0.005 * m else 2)
    return {"totalLC": a * m, "totalNormal": b * m, "porPasajeroLC": a * d["tray"], "porPasajeroNormal": b * d["tray"], "porTrayectoLC": a, "porTrayectoNormal": b,
            "diferencia": dif, "ganador": g, "nEq": n_eq, "extraEq": b - d["lc"] - d["nmal"] * d["maleta"]}
B = dict(lc=40, normal=80, maleta=30, nmal=1, nincl=1, extras=15, pax=2, tray=2)
TESTS = [dict(B),                                  # normal gana por poco con 1 maleta
         dict(B, nmal=0),                          # 0 maletas: low cost
         dict(B, pax=1, tray=1, nmal=2),           # 1 pasajero, 1 trayecto, 2 maletas
         dict(B, normal=85),                        # empate exacto con 1 maleta
         dict(B, lc=0, normal=0, maleta=0, extras=0),  # todo 0
         dict(B, normal=200, nmal=3, pax=4, tray=2)]   # low cost gana siempre
def rnd(r):
    return dict(lc=r.choice([0, 20, 40, 70]) + r.random() * 5, normal=r.choice([0, 50, 80, 150]) + r.random() * 5, maleta=r.choice([0, 15, 30, 55]) + r.random() * 3,
                nmal=r.randint(0, 5), nincl=r.randint(0, 3), extras=r.choice([0, 10, 25, 60]) + r.random() * 3, pax=r.randint(1, 9), tray=r.randint(1, 10))
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
        keys = ["totalLC", "totalNormal", "porPasajeroLC", "porPasajeroNormal", "diferencia", "ganador", "nEq", "extraEq"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
