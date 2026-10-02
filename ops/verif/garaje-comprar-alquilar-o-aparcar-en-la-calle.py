#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/garaje-comprar-alquilar-o-aparcar-en-la-calle.js, escrito desde la especificacion
(flujos anuales a fin de año descontados a euros de hoy, sumados año a año).
Uso: python3 ops/verif/garaje-comprar-alquilar-o-aparcar-en-la-calle.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "garaje-comprar-alquilar-o-aparcar-en-la-calle"
def oraculo(d):
    r = d["tasa"] / 100.0
    def pv(flujo, T): return sum(flujo / (1 + r) ** t for t in range(1, T + 1))
    def compra(T): return d["precio"] * (1 + d["gastosPct"] / 100.0) + pv(d["costes"], T) - d["precio"] / (1 + r) ** T
    N = int(d["anios"])
    fa, fc = 12 * d["alq"], 12 * d["calle"] + d["multas"]
    c = [compra(N), pv(fa, N), pv(fc, N)]
    mejor = min(range(3), key=lambda i: (c[i], i))
    seg = min(c[i] for i in range(3) if i != mejor)
    ahorro = seg - c[mejor]
    # año de equilibrio: ultimo T (1..40) donde la alternativa barata es <= comprar; eq = ese T + 1 ; -1 si T=40 aun no compensa comprar
    falt = min(fa, fc); eq = 1
    for T in range(40, 0, -1):
        if pv(falt, T) - compra(T) < 0:
            eq = T + 1 if T < 40 else -1
            break
    A = pv(1.0, N)
    return {"costeCompra": c[0], "costeAlquiler": c[1], "costeCalle": c[2], "desembolso": d["precio"] * (1 + d["gastosPct"] / 100.0),
            "mejor": mejor, "ahorro": ahorro, "minimo": c[mejor], "anioEq": eq,
            "alqEq": c[0] / (12 * A), "calleEq": (c[0] / A - d["multas"]) / 12,
            "ganador": 3 if ahorro <= 0.05 * seg else mejor}
B = dict(precio=15000, gastosPct=10, costes=300, alq=80, calle=40, multas=120, anios=10, tasa=3)
TESTS = [dict(B),                                  # base: gana calle
         dict(B, alq=40, calle=150, multas=0),     # alquilar gana
         dict(B, alq=150, calle=150, multas=300),  # comprar gana
         dict(B, calle=75, multas=0, alq=200),     # calle y comprar casi empatan (empate)
         dict(B, tasa=0, anios=1, calle=0, multas=0),  # borde: calle gratis, 1 año, sin descuento
         dict(B, anios=40, tasa=0, gastosPct=0, costes=0)]  # maximos: comprar casi gratis
def rnd(r):
    return dict(precio=r.choice([500, 5000, 15000, 30000, 60000]) + r.random() * 500, gastosPct=r.choice([0, 4, 8, 10, 15]) + r.random(),
                costes=r.choice([0, 100, 300, 600]) + r.random() * 20, alq=r.choice([0, 30, 80, 150, 300]) + r.random() * 5,
                calle=r.choice([0, 15, 40, 90, 150]) + r.random() * 5, multas=r.choice([0, 60, 120, 400]) + r.random() * 10,
                anios=r.choice([1, 2, 5, 10, 20, 40]), tasa=r.choice([0, 1, 3, 6, 10, 30]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(71); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeCompra", "costeAlquiler", "costeCalle", "mejor", "ahorro", "anioEq", "alqEq", "calleEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
