#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/tren-avion-o-coche.js, escrito desde la especificacion.
Uso: python3 ops/verif/tren-avion-o-coche.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, math, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "tren-avion-o-coche"
def eq(cA, tA, cB, tB, n):
    dc, dt = cA - cB, tB - tA
    if dc <= 0 and dt >= 0: return 0, 0.0
    if dc > 0 and dt <= 0: return 1, 0.0
    return (2 if dc > 0 else 3), dc / (n * dt)
def minv(c, b): return math.floor(c / b) + 1 if b > 0 else -1
def oraculo(d):
    cc = d["dist"] * d["kmcoche"] + d["extras"]; ct = d["tren"] * d["viaj"]; ca = d["avion"] * d["viaj"]; tc = d["dist"] / 85.0
    cs = [cc, ct, ca]; ts = [tc, d["htren"], d["havion"]]
    a, b, c = eq(ct, d["htren"], cc, tc, d["viaj"]), eq(ca, d["havion"], cc, tc, d["viaj"]), eq(ca, d["havion"], ct, d["htren"], d["viaj"])
    return {"costeCoche": cc, "costeTren": ct, "costeAvion": ca, "porPersonaCoche": cc / d["viaj"], "tiempoCoche": tc,
            "barato": cs.index(min(cs)), "rapido": ts.index(min(ts)), "minViajerosTren": minv(cc, d["tren"]), "minViajerosAvion": minv(cc, d["avion"]),
            "tipoTrenCoche": a[0], "horaTrenCoche": a[1], "tipoAvionCoche": b[0], "horaAvionCoche": b[1], "tipoAvionTren": c[0], "horaAvionTren": c[1]}
B = dict(dist=620, viaj=2, tren=60, avion=110, htren=3.5, havion=4.5, kmcoche=0.2, extras=40)
TESTS = [dict(B),                                   # tren gana en coste y tiempo
         dict(B, viaj=4),                           # el coche gana en coste con 4 viajeros
         dict(B, viaj=1, tren=150, htren=8),        # un viajero: avion mas rapido, tren caro
         dict(B, dist=0),                           # distancia 0
         dict(B, kmcoche=0, extras=0),              # coste del coche 0
         dict(B, tren=0, avion=0, viaj=1)]          # billetes gratis
def rnd(r):
    return dict(dist=r.choice([0, 50, 200, 620, 1000, 2000]) + r.random() * 10, viaj=r.randint(1, 5), tren=r.choice([0, 20, 60, 120, 200]) + r.random() * 5,
                avion=r.choice([0, 40, 110, 250]) + r.random() * 5, htren=r.choice([0.5, 2, 3.5, 6, 10]), havion=r.choice([1, 2.5, 4.5, 7]),
                kmcoche=r.choice([0, 0.1, 0.2, 0.35]), extras=r.choice([0, 15, 40, 120]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(5); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeCoche", "costeTren", "costeAvion", "tiempoCoche", "barato", "rapido", "minViajerosTren", "minViajerosAvion", "tipoTrenCoche", "horaTrenCoche", "tipoAvionCoche", "horaAvionCoche"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
