#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/movil-reacondicionado-o-nuevo.js, escrito desde la especificacion.
Uso: python3 ops/verif/movil-reacondicionado-o-nuevo.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "movil-reacondicionado-o-nuevo"

def tco(precio, rv, prob, rep, vida, gar):
    sin_garantia = vida - gar if vida > gar else 0
    riesgo = (prob / 100.0) * rep * sin_garantia
    return precio - precio * rv / 100.0 + riesgo, riesgo

def oraculo(d):
    tn, rn = tco(d["pnuevo"], d["reventa"], d["prob"], d["rep"], d["vidaN"], 3)
    tr, rr = tco(d["prec"], d["reventa"], d["prob"], d["rep"], d["vidaR"], d["garR"])
    an, ar = tn / d["vidaN"], tr / d["vidaR"]
    dif = an - ar
    mejor = 2 if abs(dif) < 0.5 else (1 if dif > 0 else 0)
    pe = max(0.0, (an * d["vidaR"] - rr) / (1 - d["reventa"] / 100.0))
    ok = {v: tco(d["pnuevo"], d["reventa"], d["prob"], d["rep"], v, 3)[0] / v <= ar for v in range(1, 31)}
    desde = -1
    for v in range(30, 0, -1):
        if ok[v]: desde = v
        else: break
    return {"tcoNuevo": tn, "tcoReac": tr, "anoNuevo": an, "anoReac": ar, "riesgoNuevo": rn, "riesgoReac": rr,
            "residualNuevo": d["pnuevo"] * d["reventa"] / 100.0, "residualReac": d["prec"] * d["reventa"] / 100.0,
            "diferenciaAno": dif, "mejor": mejor, "precioEquilibrio": pe, "desdeAnos": desde}

B = dict(pnuevo=800, prec=450, vidaN=5, vidaR=3, garR=1, prob=15, rep=150, reventa=15)
TESTS = [dict(B),                                  # base
         dict(B, rep=0),                           # coste de reparacion 0
         dict(B, vidaN=1, vidaR=1),                # 1 anio, sin reparaciones fuera de garantia en el nuevo
         dict(B, prob=0, reventa=0),               # prob 0, sin reventa
         dict(B, prec=700, vidaR=2, garR=3),       # reacondicionado caro y corto: gana el nuevo
         dict(B, pnuevo=450, vidaN=3, vidaR=3, garR=1, prob=0, rep=0, reventa=0)]  # empate exacto
def rnd(r):
    pn = r.choice([300, 600, 900, 1200]) + r.random() * 100
    return dict(pnuevo=pn, prec=pn * r.uniform(0.3, 1.1), vidaN=r.choice([1, 2, 3, 4, 5, 6, 8, 10]) + r.choice([0, 0.5]),
                vidaR=r.choice([1, 2, 3, 4, 5, 6]) + r.choice([0, 0.5]), garR=r.choice([0, 1, 2, 3]),
                prob=r.choice([0, 5, 10, 25, 60, 100]) + r.random(), rep=r.choice([0, 80, 150, 300]) + r.random() * 20,
                reventa=r.choice([0, 10, 20, 40]) + r.random() * 5)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(7); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("mejor", "desdeAnos") else max(1.0, 1e-6 * abs(v))
            if j[k] is None or abs(j[k] - v) > tol:
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        cases = [{"in": d, "expect": {k: round(v, 2) for k, v in oraculo(d).items()}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
