#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/hipoteca-bonificada-o-sin-vinculaciones.js, escrito desde la especificacion (cuadro de amortizacion mes a mes).
Uso: python3 ops/verif/hipoteca-bonificada-o-sin-vinculaciones.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "hipoteca-bonificada-o-sin-vinculaciones"
def opcion(P, plazo, H, tin, apertura, vinc):
    n = plazo * 12; i = tin / 1200.0
    c = P / n if i == 0 else P * i / (1 - (1 + i) ** -n)
    bal = P; inter = 0.0
    for m in range(12 * H):
        it = bal * i; inter += it; bal = bal + it - c
    com = P * apertura / 100; vv = vinc * H
    return dict(cuota=c, intereses=inter, comision=com, vinc=vv, coste=inter + com + vv)
def oraculo(d):
    plazo = max(int(round(d["plazo"])), 1); H = min(max(int(round(d["horizonte"])), 1), plazo)
    b = opcion(d["capital"], plazo, H, d["tin"], d["aperturaBon"], d["vinc"]); s = opcion(d["capital"], plazo, H, d["tin"] + d["bonif"], d["aperturaSin"], 0)
    f = lambda x: opcion(d["capital"], plazo, H, d["tin"] + x, d["aperturaSin"], 0)["coste"] - b["coste"]
    if f(0) >= 0: bm = 0
    elif f(10) < 0: bm = -1
    else:
        lo, hi = 0.0, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        bm = (lo + hi) / 2
    dif = s["coste"] - b["coste"]
    return {"cuotaBon": b["cuota"], "cuotaSin": s["cuota"], "interesesBon": b["intereses"], "interesesSin": s["intereses"], "comisionBon": b["comision"],
            "comisionSin": s["comision"], "vincTotal": b["vinc"], "costeBon": b["coste"], "costeSin": s["coste"], "diferencia": dif,
            "bonifMin": bm, "vincMax": max((s["coste"] - b["intereses"] - b["comision"]) / H, 0), "mejor": 0 if dif > 1 else (1 if dif < -1 else 2)}
B = dict(capital=150000, plazo=25, tin=2.76, bonif=0.5, vinc=300, aperturaBon=0, aperturaSin=0, horizonte=25)
TESTS = [dict(B),                                       # base: bonificada gana por poco o pierde segun vinc
         dict(B, vinc=100),                             # vinculaciones baratas: gana la bonificada
         dict(B, vinc=600),                             # vinculaciones caras: gana sin vinculaciones
         dict(B, tin=0, bonif=0.5, vinc=0, horizonte=25),   # borde TIN 0 %
         dict(B, plazo=1, horizonte=1, vinc=50),        # borde plazo minimo 1 ano
         dict(B, bonif=0, vinc=0)]                      # empate: sin bonificacion ni vinculaciones
def rnd(r):
    return dict(capital=r.choice([20000, 90000, 150000, 300000]) + r.random() * 500, plazo=r.choice([1, 5, 10, 20, 25, 30, 35]),
                tin=r.choice([0, 1, 2.5, 3.5, 5]) + r.random() * 0.4, bonif=r.choice([0, 0.1, 0.25, 0.5, 1, 2]) + r.random() * 0.1,
                vinc=r.choice([0, 100, 250, 500, 900]) + r.random() * 20, aperturaBon=r.choice([0, 0.25, 0.5, 1]) , aperturaSin=r.choice([0, 0.25, 0.5, 1]),
                horizonte=r.choice([1, 3, 7, 15, 25, 40]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(7); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            tol = 0 if k == "mejor" else (0.001 if k == "bonifMin" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["cuotaBon", "cuotaSin", "interesesBon", "interesesSin", "comisionBon", "comisionSin", "vincTotal", "costeBon", "costeSin", "diferencia", "bonifMin", "vincMax", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 3 if k == "bonifMin" else 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
