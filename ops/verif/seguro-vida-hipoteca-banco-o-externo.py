#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/seguro-vida-hipoteca-banco-o-externo.js, escrito desde la especificacion (cuadro de amortizacion mes a mes).
Uso: python3 ops/verif/seguro-vida-hipoteca-banco-o-externo.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "seguro-vida-hipoteca-banco-o-externo"
def opcion(P, plazo, H, tin, prima, evol):
    n = plazo * 12; i = tin / 1200.0
    if P <= 0: return dict(cuota=0, intereses=0, primas=prima * H if not evol else prima * H * 0 + prima * H, coste=0)
    c = P / n if i == 0 else P * i / (1 - (1 + i) ** -n)
    bal = P; inter = 0.0; primas = 0.0
    for m in range(12 * H):
        if m % 12 == 0: primas += prima * (bal / P if evol else 1)
        it = bal * i; inter += it; bal = bal + it - c
    return dict(cuota=c, intereses=inter, primas=primas, coste=inter + primas)
def oraculo(d):
    plazo = max(int(round(d["plazo"])), 1); H = min(max(int(round(d["horizonte"])), 1), plazo); ev = 1 if d["evol"] == 1 else 0
    b = opcion(d["capital"], plazo, H, d["tin"], d["primaBanco"], ev); e = opcion(d["capital"], plazo, H, d["tin"] + d["bonif"], d["primaExt"], ev)
    f = lambda x: opcion(d["capital"], plazo, H, d["tin"] + x, d["primaExt"], ev)["coste"] - b["coste"]
    if f(0) >= 0: bm = 0
    elif f(10) < 0: bm = -1
    else:
        lo, hi = 0.0, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        bm = (lo + hi) / 2
    dif = e["coste"] - b["coste"]
    return {"cuotaBanco": b["cuota"], "cuotaExt": e["cuota"], "interesesBanco": b["intereses"], "interesesExt": e["intereses"],
            "primasBanco": b["primas"], "primasExt": e["primas"], "costeBanco": b["coste"], "costeExt": e["coste"], "diferencia": dif,
            "extraIntereses": e["intereses"] - b["intereses"], "bonifMin": bm, "mejor": 0 if dif > 1 else (1 if dif < -1 else 2)}
B = dict(capital=150000, plazo=25, tin=2.76, bonif=0.5, primaBanco=450, primaExt=250, horizonte=25, evol=1)
TESTS = [dict(B),                                       # base
         dict(B, bonif=0.1),                            # bonificacion pequena: gana la externa
         dict(B, bonif=0, horizonte=1),                 # borde: sin bonificacion y 1 ano
         dict(B, primaBanco=250, bonif=0.3),            # primas iguales: gana el banco, bonifMin 0
         dict(B, evol=0, horizonte=10, tin=0),          # prima fija, TIN 0
         dict(B, capital=0, primaBanco=0, primaExt=0)]  # coste 0
def rnd(r):
    return dict(capital=r.choice([0, 30000, 90000, 150000, 300000]) + r.random() * 500, plazo=r.choice([1, 5, 10, 20, 25, 30, 35]),
                tin=r.choice([0, 1, 2.5, 3.5, 5]) + r.random() * 0.4, bonif=r.choice([0, 0.1, 0.25, 0.5, 1, 2]) + r.random() * 0.1,
                primaBanco=r.choice([0, 150, 300, 600, 1200]) + r.random() * 20, primaExt=r.choice([0, 100, 250, 400, 800]) + r.random() * 20,
                horizonte=r.choice([1, 3, 7, 15, 25, 40]), evol=r.choice([0, 1]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(7); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        if d["capital"] <= 0: continue_keys = ("mejor",)
        for k, v in o.items():
            if d["capital"] <= 0 and k in ("primasBanco", "primasExt", "costeBanco", "costeExt", "diferencia"): continue
            tol = 0 if k == "mejor" else (0.001 if k == "bonifMin" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["cuotaBanco", "cuotaExt", "interesesBanco", "interesesExt", "primasBanco", "primasExt", "costeBanco", "costeExt", "diferencia", "bonifMin", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 3 if k == "bonifMin" else 2) for k in keys}, "tol": 1} for d in TESTS[:5]]
        z = TESTS[5]; cases.append({"in": z, "expect": {"cuotaBanco": 0, "costeBanco": 0, "costeExt": 0, "diferencia": 0, "mejor": 2}, "tol": 1})
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
