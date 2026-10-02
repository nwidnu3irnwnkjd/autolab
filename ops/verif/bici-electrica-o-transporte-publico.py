#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/bici-electrica-o-transporte-publico.js, escrito desde la especificacion.
Uso: python3 ops/verif/bici-electrica-o-transporte-publico.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "bici-electrica-o-transporte-publico"
def oraculo(d):
    km = d["kmdia"] * d["dias"]
    coche = km * d["kmcoche"]; abono = d["abono"] * 12.0
    fijo = d["bici"] / d["vida"] + d["seguro"]            # amortizacion + seguro/robo
    corriente = km * d["mant"] + d["seguro"]               # sin la compra
    bici = fijo + km * d["mant"]
    cands = [(coche, 0), (bici, 2)] + ([(abono, 1)] if d["abono"] > 0 else [])
    barato = min(cands, key=lambda x: (x[0], x[1]))[1]     # empate: gana el de menor indice (coche, abono, bici)
    sc = coche - corriente; sa = abono - corriente
    pc = d["bici"] / sc if sc > 0 else -1
    pa = d["bici"] / sa if (d["abono"] > 0 and sa > 0) else -1
    den = d["kmcoche"] - d["mant"]
    return {"km": km, "cocheAnual": coche, "abonoAnual": abono, "biciAnual": bici, "ahorroVsCoche": coche - bici,
            "ahorroVsAbono": (abono - bici) if d["abono"] > 0 else 0, "paybackCoche": pc, "paybackAbono": pa,
            "kmMinCoche": fijo / den if den > 0 else -1, "abonoMinMes": bici / 12.0, "barato": barato}
B = dict(kmdia=10, dias=220, abono=40, kmcoche=0.199, bici=1800, vida=6, mant=0.023, seguro=60)
TESTS = [dict(B),                         # base
         dict(B, kmdia=25, dias=230),     # trayecto largo: la bici gana al coche
         dict(B, kmdia=0),                # 0 km
         dict(B, abono=0),                # sin transporte publico
         dict(B, bici=0, seguro=0),       # coste de bici 0
         dict(B, vida=1, kmcoche=0.02)]   # vida 1 anio y coche barato (coste < mantenimiento)
def rnd(r):
    return dict(kmdia=r.choice([0, 3, 8, 12, 20, 40]) + r.random(), dias=r.choice([0, 100, 220, 300]) + r.random() * 5,
                abono=r.choice([0, 0, 20, 40, 65, 110]) + r.random(), kmcoche=r.choice([0, 0.03, 0.12, 0.2, 0.35]) + r.random() * 0.01,
                bici=r.choice([0, 800, 1800, 3500]) + r.random() * 100, vida=r.choice([1, 3, 6, 10]), mant=r.choice([0, 0.02, 0.05]) + r.random() * 0.005,
                seguro=r.choice([0, 60, 150]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(23); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("barato",) else (0.01 if k in ("paybackCoche", "paybackAbono") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["km", "cocheAnual", "abonoAnual", "biciAnual", "ahorroVsCoche", "ahorroVsAbono", "paybackCoche", "paybackAbono", "kmMinCoche", "abonoMinMes", "barato"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
