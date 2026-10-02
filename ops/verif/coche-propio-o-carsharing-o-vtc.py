#!/usr/bin/env python3
"""Script independiente (Constructor A) de calcs/coche-propio-o-carsharing-o-vtc.js, escrito desde la especificacion.
Uso: python3 ops/verif/coche-propio-o-carsharing-o-vtc.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)
Modelo: km/anio = viajes/mes x 12 x km/viaje. propio = fijos + deprec + km x kmcoche; carsharing = 12 x cuota + km x cskm; vtc = km x vtckm.
Equilibrio de A frente a B: coste = F + v x km. tipo 0 = A siempre <= B; 1 = A nunca mas barato; 2 = A gana a partir de km*; 3 = A gana por debajo de km*."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "coche-propio-o-carsharing-o-vtc"
def eq(Fa, va, Fb, vb):
    if va == vb: return (0, 0.0) if Fa <= Fb else (1, 0.0)
    x = (Fa - Fb) / (vb - va)
    if vb > va: return (0, 0.0) if Fa <= Fb else (2, x)
    return (1, 0.0) if Fa >= Fb else (3, x)
def oraculo(d):
    km = d["viajes"] * 12.0 * d["kmviaje"]
    F = d["fijos"] + d["deprec"]
    c = [F + km * d["kmcoche"], 12.0 * d["cscuota"] + km * d["cskm"], km * d["vtckm"]]
    barato = min(range(3), key=lambda i: (c[i], i))
    t1, k1 = eq(F, d["kmcoche"], 12.0 * d["cscuota"], d["cskm"])
    t2, k2 = eq(F, d["kmcoche"], 0.0, d["vtckm"])
    kv = d["kmviaje"] * 12.0
    return {"km": km, "propio": c[0], "carsharing": c[1], "vtc": c[2],
            "propioKm": c[0] / km if km > 0 else 0, "carsharingKm": c[1] / km if km > 0 else 0, "vtcKm": c[2] / km if km > 0 else 0,
            "barato": barato, "tipoCS": t1, "kmCS": k1, "tipoVTC": t2, "kmVTC": k2,
            "viajesCS": k1 / kv if kv > 0 else 0, "viajesVTC": k2 / kv if kv > 0 else 0}
B = dict(viajes=30, kmviaje=15, fijos=1200, deprec=1500, kmcoche=0.17, cskm=0.45, cscuota=5, vtckm=1.2)
TESTS = [dict(B),                                   # base: gana el carsharing
         dict(B, viajes=70, kmviaje=20),            # muchos km: gana el propio
         dict(B, viajes=0),                         # 0 km
         dict(B, fijos=0, deprec=0),                # coche ya pagado y sin fijos
         dict(B, cskm=0.1, cscuota=0),              # carsharing mas barato por km que el propio: gana siempre
         dict(B, vtckm=0.1, kmcoche=0.1)]           # VTC barato y propio igual de variable
def rnd(r):
    return dict(viajes=r.choice([0, 4, 15, 30, 60, 100]) + r.random(), kmviaje=r.choice([1, 5, 12, 25, 60]) + r.random(),
                fijos=r.choice([0, 600, 1200, 2500]) + r.random() * 50, deprec=r.choice([0, 800, 1500, 3000]) + r.random() * 50,
                kmcoche=r.choice([0, 0.08, 0.17, 0.3]) + r.random() * 0.01, cskm=r.choice([0, 0.2, 0.45, 0.9]) + r.random() * 0.01,
                cscuota=r.choice([0, 0, 5, 20]) + r.random(), vtckm=r.choice([0, 0.6, 1.2, 2]) + r.random() * 0.02)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(41); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("barato", "tipoCS", "tipoVTC") else (0.01 if k in ("propioKm", "carsharingKm", "vtcKm", "viajesCS", "viajesVTC") else 1.0)
            if j.get(k) is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j.get(k), v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
