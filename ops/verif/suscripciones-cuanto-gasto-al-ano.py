#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/suscripciones-cuanto-gasto-al-ano.js, escrito desde la especificacion (con Fraction para las comparaciones).
Uso: python3 ops/verif/suscripciones-cuanto-gasto-al-ano.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "suscripciones-cuanto-gasto-al-ano"

def oraculo(d):
    pr = [F(str(d["p%d" % i])) for i in (1, 2, 3)]; hs = [F(str(d["h%d" % i])) for i in (1, 2, 3)]
    dto = F(str(d["dto"])) / 100; m = F(str(d["meses"]))
    sp, sh = sum(pr), sum(hs)
    cand_total = F(0); mant_total = F(0); n = 0
    for p, h in zip(pr, hs):
        if p <= 0: continue
        if h <= 0:
            cand_total += 12 * p; n += 1          # sin uso: se cancela
        elif p / h > sp / sh:                      # coste/hora por encima de la media ponderada
            n += 1; cand_total += 12 * p - min(m * p, 12 * p * (1 - dto))
        else:
            mant_total += 12 * p * dto            # se queda, con plan anual
    ch = [float(p / h) if h > 0 else -1 for p, h in zip(pr, hs)]
    mayor = -1; mv = None
    for i, (p, h) in enumerate(zip(pr, hs)):
        if h > 0 and (mv is None or p / h > mv): mv, mayor = p / h, i
    g = 12 * sp
    return {"gastoAnual": float(g), "gastoPagoAnual": float(g * (1 - dto)), "horasMes": float(sh),
            "mediaHora": float(sp / sh) if sh > 0 else -1, "horaG1": ch[0], "horaG2": ch[1], "horaG3": ch[2],
            "mayorCoste": mayor, "nCandidatas": n, "ahorroCandidatas": float(cand_total), "ahorroMantenidas": float(mant_total),
            "ahorroTotal": float(cand_total + mant_total), "gastoTras": float(g - cand_total - mant_total), "descuentoAnual": float(g * dto)}

B = dict(p1=30, h1=20, p2=15, h2=40, p3=45, h3=6, dto=15, meses=5)
TESTS = [dict(B),                                  # base: streaming y otras son candidatas
         dict(B, dto=0),                           # descuento 0
         dict(B, h3=0),                            # uso 0 en un grupo: se cancela
         dict(B, p1=0, p2=0, p3=60, h3=10),        # un solo grupo con gasto
         dict(B, meses=12, dto=0),                 # rotar 12 meses: sin ahorro por rotacion
         dict(B, h1=0, h2=0, h3=0)]                # sin uso en nada: todo cancelable
def rnd(r):
    return dict(p1=r.choice([0, 5, 12, 30, 60]) + r.choice([0, 0.5]), h1=r.choice([0, 0, 3, 10, 30, 80]), p2=r.choice([0, 3, 10, 25]) + r.choice([0, 0.99]),
                h2=r.choice([0, 5, 20, 60]), p3=r.choice([0, 8, 20, 45, 90]), h3=r.choice([0, 2, 6, 15, 40]),
                dto=r.choice([0, 0, 10, 15, 25]) + r.choice([0, 0.5]), meses=r.choice([0, 1, 3, 5, 8, 11, 12]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(5); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("mayorCoste", "nCandidatas") else max(1.0, 1e-6 * abs(v))
            if j[k] is None or abs(j[k] - v) > tol:
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        cases = [{"in": d, "expect": {k: round(v, 2) for k, v in oraculo(d).items()}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
