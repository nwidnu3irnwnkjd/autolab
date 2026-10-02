#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/adoptar-o-comprar-perro-coste-anual.js, escrito desde la especificacion.
Uso: python3 ops/verif/adoptar-o-comprar-perro-coste-anual.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "adoptar-o-comprar-perro-coste-anual"
def oraculo(d):
    anual = d["pienso"] * 12 + d["vet"] + d["seguro"]
    ta = d["adopcion"] + d["iniciales"] + anual * d["anos"]
    tc = d["compra"] + d["iniciales"] + anual * d["anos"]
    dif = tc - ta
    return {"anual": anual, "mensual": anual / 12, "ano1Adopcion": d["adopcion"] + d["iniciales"] + anual, "ano1Compra": d["compra"] + d["iniciales"] + anual,
            "totalAdopcion": ta, "totalCompra": tc, "diferencia": dif, "mensualMedioAdopcion": ta / d["anos"] / 12, "mensualMedioCompra": tc / d["anos"] / 12,
            "mesesDif": abs(dif) / (anual / 12) if anual > 0 else -1.0, "pesoSeguro": d["seguro"] / anual * 100 if anual > 0 else 0.0,
            "pesoEntradaAdopcion": d["adopcion"] / ta * 100 if ta > 0 else 0.0, "pesoEntradaCompra": d["compra"] / tc * 100 if tc > 0 else 0.0,
            "ganador": 2 if abs(dif) < 1 else (0 if dif > 0 else 1)}   # 0 adoptar, 1 comprar, 2 empate
B = dict(pienso=40, vet=250, seguro=0, iniciales=250, adopcion=200, compra=800, anos=12)
TESTS = [dict(B),                                  # adoptar mas barato
         dict(B, seguro=300),                      # con seguro
         dict(B, adopcion=500, compra=300),        # cuota de adopcion mayor que el precio de compra
         dict(B, adopcion=500, compra=500),        # empate
         dict(B, pienso=25, vet=200, anos=1),      # perro pequeno, 1 anio
         dict(B, pienso=0, vet=0, seguro=0, adopcion=0, compra=0, iniciales=0),   # borde: todo 0
         dict(B, pienso=60, vet=300, seguro=400, anos=25, compra=3000)]           # grande, maximo
def rnd(r):
    return dict(pienso=r.choice([0, 20, 25, 40, 60, 90]) + r.random() * 5, vet=r.choice([0, 150, 250, 400, 900]) + r.random() * 20,
                seguro=r.choice([0, 0, 150, 300, 600]) + r.random() * 20, iniciales=r.choice([0, 100, 250, 600]) + r.random() * 20,
                adopcion=r.choice([0, 100, 200, 400, 700]) + r.random() * 20, compra=r.choice([0, 300, 800, 1500, 3000]) + r.random() * 20,
                anos=r.choice([1, 5, 10, 12, 25]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(23); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("mesesDif", "pesoSeguro", "pesoEntradaAdopcion", "pesoEntradaCompra") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["anual", "ano1Adopcion", "ano1Compra", "totalAdopcion", "totalCompra", "diferencia", "mensualMedioAdopcion", "mesesDif", "pesoSeguro", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
        for d in TESTS: o = oraculo(d); print({k: round(o[k], 2) for k in keys})
    sys.exit(1 if bad else 0)
