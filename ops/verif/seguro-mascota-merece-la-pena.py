#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/seguro-mascota-merece-la-pena.js, escrito desde la especificacion.
Uso: python3 ops/verif/seguro-mascota-merece-la-pena.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "seguro-mascota-merece-la-pena"
def oraculo(d):
    p = d["prob"] / 100.0; H = int(round(d["horizonte"])); M = int(round(d["carencia"]))
    paga = min(max(d["coste"] - d["franq"], 0.0), d["limite"]); mio = d["coste"] - paga
    sin = p * d["coste"]; con = d["prima"] + p * mio; m = d["prima"] / 12.0; mc = M + 1
    return {"cobertura": paga, "bolsillo": mio, "esperadoSin": sin, "esperadoCon": con, "ahorroEsperado": sin - con,
            "esperadoSinTotal": sin * H, "esperadoConTotal": con * H, "ahorroTotal": (sin - con) * H,
            "probEquilibrio": d["prima"] / paga * 100 if paga > 0 else -1,
            "anoConEventoSin": d["coste"], "anoConEventoCon": d["prima"] + mio,
            "mesesHucha": d["coste"] / m if m > 0 else -1, "huchaFinal": d["prima"] * H,
            "golpeMes1Con": d["coste"] if M > 0 else mio, "golpeMes1Hucha": max(0.0, d["coste"] - m),
            "mesCubierto": mc if mc <= 12 else -1,
            "golpeCubiertoCon": mio if mc <= 12 else -1, "golpeCubiertoHucha": max(0.0, d["coste"] - m * mc) if mc <= 12 else -1,
            "gastoAno1Con": m * mc + mio if mc <= 12 else d["coste"],
            "mejor": 0 if con < sin - 1 else (1 if sin < con - 1 else 2)}
B = dict(prima=300, franq=100, limite=3000, carencia=2, prob=10, coste=1500, horizonte=10)
TESTS = [dict(B),                                  # base: no compensa en valor esperado
         dict(B, prob=25),                         # probabilidad por encima del equilibrio (21,4 %)
         dict(B, coste=0),                         # coste 0
         dict(B, prob=0),                          # probabilidad 0
         dict(B, prob=100, carencia=0, horizonte=1),   # probabilidad 100 %, sin carencia, 1 anio
         dict(B, franq=2000, limite=500, carencia=12)] # franquicia mayor que el coste, carencia de 12 meses
def rnd(r):
    return dict(prima=r.choice([60, 150, 300, 600]) + r.random() * 5, franq=r.choice([0, 50, 150, 2000]) + r.random() * 5,
                limite=r.choice([0, 500, 1500, 5000]) + r.random() * 5, carencia=r.choice([0, 1, 3, 6, 12, 24]),
                prob=r.choice([0, 5, 10, 25, 60, 100]) + r.random(), coste=r.choice([0, 500, 1500, 4000]) + r.random() * 20,
                horizonte=r.choice([1, 3, 10, 15, 30]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(47); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("mejor", "mesCubierto") else (0.01 if k == "probEquilibrio" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["cobertura", "esperadoSin", "esperadoCon", "ahorroEsperado", "esperadoConTotal", "probEquilibrio", "anoConEventoCon", "mesesHucha", "golpeMes1Con", "gastoAno1Con", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
