#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/hipoteca-20-25-o-30-anos-cuota-vs-intereses.js, escrito desde la especificacion (cuadro de amortizacion mes a mes
y plazo minimo por busqueda de meses, no por formula cerrada).
Uso: python3 ops/verif/hipoteca-20-25-o-30-anos-cuota-vs-intereses.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "hipoteca-20-25-o-30-anos-cuota-vs-intereses"
def cuadro(P, tin, anos):
    n = anos * 12; i = tin / 1200.0
    c = P / n if i == 0 else P * i / (1 - (1 + i) ** -n)
    bal = P; inter = 0.0
    for _ in range(n):
        it = bal * i; inter += it; bal = bal + it - c
    return c, inter
def cuota_n(P, tin, n):
    i = tin / 1200.0
    return P / n if i == 0 else P * i / (1 - (1 + i) ** -n)
def oraculo(d):
    P = d["capital"]; r = {}
    for a in (20, 25, 30):
        c, it = cuadro(P, d["tin"], a); r["cuota%d" % a] = c; r["int%d" % a] = it
        r["esf%d" % a] = (c + d["otras"]) / d["ingresos"] * 100
    cmax = d["tope"] / 100 * d["ingresos"] - d["otras"]; r["cuotaMax"] = cmax
    # plazo minimo en meses: biseccion continua sobre la cuota (decreciente en n); -1 si ni n enorme llega
    if cmax <= 0 or cuota_n(P, d["tin"], 1e9) > cmax: r["plazoMinAnos"] = -1
    else:
        lo, hi = 1.0, 1e9
        for _ in range(200):
            mid = (lo + hi) / 2
            if cuota_n(P, d["tin"], mid) > cmax: lo = mid
            else: hi = mid
        r["plazoMinAnos"] = hi / 12
    ok = [r["esf%d" % a] <= d["tope"] for a in (20, 25, 30)]
    e = 20 if ok[0] else (25 if ok[1] else (30 if ok[2] else 0)); r["elegido"] = e
    ref = r["int%d" % e] if e else r["int30"]; refc = r["cuota%d" % e] if e else r["cuota30"]
    r["extra30"] = r["int30"] - ref; r["alivio30"] = refc - r["cuota30"]
    r["extra25"] = r["int25"] - r["int20"]; r["alivio25"] = r["cuota20"] - r["cuota25"]; r["extra30vs25"] = r["int30"] - r["int25"]
    return r
B = dict(capital=150000, tin=2.76, ingresos=3500, otras=0, tope=35)
TESTS = [dict(B),                                  # 20 anos cumple
         dict(B, ingresos=2200),                   # 20 no, 25 si
         dict(B, ingresos=1900),                   # solo 30
         dict(B, ingresos=1200),                   # ninguno
         dict(B, tin=0, capital=168000, ingresos=2000),   # borde TIN 0 y esfuerzo exactamente igual al tope (35 %) a 20 anos
         dict(B, capital=12000, tin=0, otras=300, ingresos=2000)]  # capital pequeno, otras deudas
def rnd(r):
    return dict(capital=r.choice([10000, 60000, 120000, 200000, 400000]) + r.random() * 5000, tin=r.choice([0, 1, 2.5, 3.5, 5, 7]) + r.random() * 0.4,
                ingresos=r.choice([900, 1500, 2200, 3000, 4500, 8000]) + r.random() * 100, otras=r.choice([0, 0, 150, 400, 900]), tope=r.choice([25, 30, 35, 40, 50]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            tol = 0 if k == "elegido" else (0.001 if k in ("plazoMinAnos",) or k.startswith("esf") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 3 if (k == "plazoMinAnos" or k.startswith("esf")) else 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
