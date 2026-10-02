#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/potencia-contratada-luz-bajar-compensa.js, escrito desde la especificacion.
Uso: python3 ops/verif/potencia-contratada-luz-bajar-compensa.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "potencia-contratada-luz-bajar-compensa"
F = (1 + 5.11269632 / 100) * 1.21   # IEE sobre el termino de potencia e IVA
def oraculo(d):
    baja = d["kwActual"] - d["kwNuevo"]
    ahorro = baja * d["eurKw"] * F if baja > 0 else 0.0
    neto = ahorro * d["anos"] - d["costeCambio"]
    if ahorro <= 0: estado, gan = 3, 1
    elif d["pico"] > d["kwNuevo"]: estado, gan = 1, 1
    elif abs(neto) < 1: estado, gan = 2, 2
    elif neto < 0: estado, gan = 2, 1
    else: estado, gan = 0, 0
    if d["costeCambio"] <= 0: anios = 0.0 if ahorro > 0 else -1.0
    else: anios = d["costeCambio"] / ahorro if ahorro > 0 else -1.0
    return {"costeActual": d["kwActual"] * d["eurKw"] * F, "costeNuevo": d["kwNuevo"] * d["eurKw"] * F, "ahorroAnual": ahorro, "ahorroNeto": neto,
            "aniosAmort": anios, "margen": d["kwNuevo"] - d["pico"], "ahorroMinimo": max(d["kwActual"] - d["pico"], 0) * d["eurKw"] * F,
            "pctBaja": max(baja, 0) / d["kwActual"] * 100 if d["kwActual"] > 0 else 0.0, "estado": estado, "ganador": gan}
B = dict(kwActual=4.6, kwNuevo=3.45, pico=3.0, eurKw=28.429836, costeCambio=0, anos=3)
TESTS = [dict(B),                                  # compensa, sin coste de cambio
         dict(B, costeCambio=30),                  # compensa con coste: 3 anos
         dict(B, pico=3.6),                        # riesgo: pico por encima de los kW nuevos
         dict(B, costeCambio=200),                 # el coste no se recupera en el horizonte
         dict(B, kwNuevo=4.6),                     # no baja (borde: igual)
         dict(B, pico=3.45),                       # borde: pico igual a kW nuevos
         dict(B, eurKw=0),                         # precio 0: sin ahorro
         dict(B, kwActual=10, kwNuevo=1, pico=0.5, anos=30, costeCambio=100)]
def rnd(r):
    ka = r.choice([2.3, 3.45, 4.6, 5.75, 6.9, 9.2, 10, 15]) + r.random() * 0.1
    return dict(kwActual=ka, kwNuevo=ka * r.choice([0.5, 0.7, 0.9, 1.0, 1.2]) , pico=ka * r.choice([0.2, 0.5, 0.7, 0.9, 1.0]) * r.random() + 0.05,
                eurKw=r.choice([0, 20, 28.429836, 35, 45]) + r.random() * 3, costeCambio=r.choice([0, 0, 20, 50, 150, 400]) * r.random(),
                anos=r.choice([1, 3, 5, 10, 30]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(77); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "estado") else (0.01 if k in ("aniosAmort", "margen", "pctBaja") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeActual", "costeNuevo", "ahorroAnual", "ahorroNeto", "aniosAmort", "ahorroMinimo", "estado", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
