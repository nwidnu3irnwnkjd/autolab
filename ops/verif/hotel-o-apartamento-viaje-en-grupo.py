#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/hotel-o-apartamento-viaje-en-grupo.js, escrito desde la especificacion.
Uso: python3 ops/verif/hotel-o-apartamento-viaje-en-grupo.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "hotel-o-apartamento-viaje-en-grupo"
def oraculo(d):
    P, N = d["personas"], d["noches"]
    hotel = d["habs"] * d["precioHab"] * N + d["comerFuera"] * P * N     # dias de comida = noches
    apto = d["precioApto"] * N + d["limpieza"] + d["cocinar"] * P * N
    dif = hotel - apto                                                  # >0: el hotel cuesta mas
    den = d["habs"] * d["precioHab"] - d["precioApto"] + P * (d["comerFuera"] - d["cocinar"])   # diferencia hotel-apto por noche
    n_eq = d["limpieza"] / den if den > 0 else -1                       # el apartamento es mas barato desde N* noches
    e = d["comerFuera"] - d["cocinar"]
    d0 = d["habs"] * d["precioHab"] - d["precioApto"]
    p_eq = -1
    if e != 0:
        p = (d["limpieza"] / N - d0) / e
        if p > 0: p_eq = p
    g = 0 if dif < -1 else (1 if dif > 1 else 2)                        # 0 hotel, 1 apartamento, 2 empate
    return {"totalHotel": hotel, "totalApto": apto, "ppnHotel": hotel / (P * N), "ppnApto": apto / (P * N),
            "diferencia": dif, "nochesEq": n_eq, "personasEq": p_eq, "ganador": g}
B = dict(personas=6, noches=5, habs=3, precioHab=110, precioApto=190, limpieza=90, comerFuera=35, cocinar=14)
TESTS = [dict(B),                                  # base: apartamento gana
         dict(B, personas=2, habs=1, precioHab=100),   # pareja: hotel gana
         dict(B, noches=1),                        # 1 noche: pesa la limpieza
         dict(B, personas=1, habs=1),              # 1 persona
         dict(B, limpieza=0, comerFuera=14),       # sin limpieza y misma comida
         dict(B, precioApto=0, limpieza=0, cocinar=0),   # borde: apartamento gratis
         dict(B, precioApto=330, limpieza=240, noches=1),  # 1 noche: la limpieza inclina al hotel
         dict(B, precioApto=330, limpieza=240)]            # mismas cifras a 5 noches: gana el apartamento
def rnd(r):
    return dict(personas=r.choice([1, 2, 4, 6, 10, 20]), noches=r.choice([1, 2, 4, 7, 14, 30]), habs=r.choice([1, 2, 3, 5]),
                precioHab=r.choice([0, 60, 110, 200]) + r.random() * 5, precioApto=r.choice([0, 90, 190, 400]) + r.random() * 5,
                limpieza=r.choice([0, 50, 120, 250]) + r.random(), comerFuera=r.choice([0, 14, 35, 60]) + r.random(),
                cocinar=r.choice([0, 10, 14, 25]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(37); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("nochesEq", "personasEq", "ppnHotel", "ppnApto") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
