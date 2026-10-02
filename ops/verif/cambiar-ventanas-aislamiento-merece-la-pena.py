#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/cambiar-ventanas-aislamiento-merece-la-pena.js, escrito desde la especificacion.
Amortizacion = momento en que el acumulado (fin de cada año) iguala el coste neto, interpolando linealmente dentro del año; maximo 60 años.
Uso: python3 ops/verif/cambiar-ventanas-aislamiento-merece-la-pena.py [--write-tests]"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cambiar-ventanas-aislamiento-merece-la-pena"
def amort(net, flujos):
    if net <= 0: return 0.0
    acc = 0.0
    for i, f in enumerate(flujos):          # flujos[i] = ahorro del año i+1 (ya descontado si procede)
        if f > 0 and acc + f >= net: return i + (net - acc) / f
        acc += f
    return -1.0
def oraculo(d):
    q, r = 1 + d["subida"] / 100, 1 + d["tasa"] / 100
    net = max(d["coste"] - d["ayuda"], 0.0); a1 = d["gasto"] * d["ahorro"] / 100; n = int(round(d["anos"]))
    fl = [a1 * q ** i for i in range(60)]; fd = [fl[i] / r ** (i + 1) for i in range(60)]
    acum, vanb = sum(fl[:n]), sum(fd[:n])
    fac, facd = sum(q ** i for i in range(n)), sum(q ** i / r ** (i + 1) for i in range(n))
    pb = amort(net, fl)
    return {"neto": net, "ahorroAnual1": a1, "anosSimple": net / a1 if a1 > 0 else -1.0, "anosAmort": pb, "anosDesc": amort(net, fd),
            "ahorroAcum": acum, "saldoAcum": acum - net, "van": vanb - net,
            "minPct": net / (d["gasto"] * fac) * 100 if d["gasto"] > 0 else -1.0, "minPctVan": net / (d["gasto"] * facd) * 100 if d["gasto"] > 0 else -1.0,
            "compensa": 1 if 0 <= pb <= n else 0, "compensaVan": 1 if vanb - net >= 0 else 0}
B = dict(gasto=800, ahorro=20, coste=6000, ayuda=0, anos=15, subida=2, tasa=3)
TESTS = [dict(B), dict(B, coste=0), dict(B, ahorro=0), dict(B, anos=1, coste=300, gasto=1500, ahorro=30),
         dict(B, gasto=2000, ahorro=30, coste=12000, ayuda=3000, anos=20, subida=3, tasa=6),
         dict(B, gasto=1000, ahorro=18, coste=5500, anos=9, subida=0, tasa=8)]   # amortiza en años (0 % subida) pero VAN negativo a 8 %
def rnd(r):
    return dict(gasto=r.choice([0, 200, 500, 800, 1500, 3000]) + r.random() * 30, ahorro=r.choice([0, 5, 10, 20, 30, 45, 70]), coste=r.choice([0, 800, 3000, 6000, 15000, 40000]) + r.random() * 200,
                ayuda=r.choice([0, 0, 500, 2000]), anos=r.choice([1, 3, 5, 10, 15, 25, 40]), subida=r.choice([-2, 0, 2, 5]), tasa=r.choice([-1, 0, 3, 6, 10]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    rr = random.Random(11); ins = TESTS + [rnd(rr) for _ in range(400)]; ins = [dict(d, ayuda=min(d["ayuda"], d["coste"])) for d in ins]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if abs(j[k] - v) > 0.01 and abs(j[k] - v) > 1e-6 * abs(v): bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["neto", "ahorroAnual1", "anosAmort", "ahorroAcum", "van", "minPct", "compensa", "compensaVan"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
