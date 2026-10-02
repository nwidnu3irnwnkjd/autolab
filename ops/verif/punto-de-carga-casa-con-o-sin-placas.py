#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/punto-de-carga-casa-con-o-sin-placas.js, escrito desde la especificacion.
Uso: python3 ops/verif/punto-de-carga-casa-con-o-sin-placas.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "punto-de-carga-casa-con-o-sin-placas"
ANOS, CGAS, PCOMP = 10.0, 6.5, 0.07 * 1.2718
def pay(coste, ahorro):
    return coste / ahorro if ahorro > 0 else (0.0 if coste <= 0 else -1.0)
def oraculo(d):
    kwh = d["km"] * d["cons"] / 100.0
    casa = kwh * d["pctCasa"] / 100.0; pub = kwh - casa
    p_con = (1 - d["pctPlacas"] / 100.0) * d["pelec"] + d["pctPlacas"] / 100.0 * PCOMP
    c_pub = kwh * d["ppub"]
    c_sin = casa * d["pelec"] + pub * d["ppub"]
    c_con = casa * p_con + pub * d["ppub"]
    c_gas = d["km"] * CGAS / 100.0 * d["pgas"]
    a_sin = c_pub - c_sin; a_con = c_pub - c_con
    den = ANOS * d["cons"] / 100.0 * d["pctCasa"] / 100.0 * (d["ppub"] - p_con)
    kmmin = d["coste"] / den if den > 0 else (0.0 if d["coste"] <= 0 else -1.0)
    pcon = pay(d["coste"], a_con)
    return {"kwhAnual": kwh, "kwhCasa": casa, "precioCasaCon": p_con, "costePublica": c_pub, "costeSin": c_sin, "costeCon": c_con,
            "costeGasolina": c_gas, "ahorroSin": a_sin, "ahorroCon": a_con, "paybackSin": pay(d["coste"], a_sin), "paybackCon": pcon,
            "kmMin": kmmin, "ahorroVsGasolina": c_gas - c_con, "instalar": 1 if (pcon >= 0 and pcon <= ANOS) else 0}
B = dict(km=15000, cons=17, pctCasa=80, coste=1200, pelec=0.1812, ppub=0.45, pctPlacas=40, pgas=1.8323)
TESTS = [dict(B),                          # base
         dict(B, pctPlacas=0),             # sin placas
         dict(B, km=0),                    # 0 km
         dict(B, pctCasa=100),             # 100 % en casa
         dict(B, coste=0),                 # coste 0
         dict(B, ppub=0.15, km=6000),      # publica barata: no amortiza
         dict(B, km=3000),                 # pocos km: borde de 10 anos
         dict(B, ppub=0.20),               # publica a 0,20: solo amortiza con placas a 10,6 anos
         dict(B, coste=2500, km=6000)]     # punto caro y pocos km
def rnd(r):
    return dict(km=r.choice([0, 3000, 8000, 15000, 30000]) + r.random() * 50, cons=r.choice([12, 15, 17, 22]) + r.random(),
                pctCasa=r.choice([0, 30, 80, 100]) + r.random() * 0.5, coste=r.choice([0, 600, 1200, 2500]) + r.random() * 30,
                pelec=r.choice([0.1, 0.18, 0.27, 0.4]) + r.random() * 0.01, ppub=r.choice([0.1, 0.3, 0.45, 0.6]) + r.random() * 0.01,
                pctPlacas=r.choice([0, 40, 100]) + r.random() * 0.5, pgas=r.choice([1.5, 1.83, 2.2]) + r.random() * 0.01)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(37); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "instalar" else (0.01 if k in ("paybackSin", "paybackCon", "precioCasaCon") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["kwhAnual", "kwhCasa", "costePublica", "costeSin", "costeCon", "costeGasolina", "ahorroSin", "ahorroCon", "paybackSin", "paybackCon", "kmMin", "ahorroVsGasolina", "instalar"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
