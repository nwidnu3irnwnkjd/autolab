#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/aire-acondicionado-inverter-o-ventilador-coste-verano.js, escrito desde la especificacion.
Uso: python3 ops/verif/aire-acondicionado-inverter-o-ventilador-coste-verano.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "aire-acondicionado-inverter-o-ventilador-coste-verano"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
def oraculo(d):
    pe = max(d["precio"] * (1 + IEE), d["precio"] + IEE_MIN) * (1 + IVA)
    h = d["horas"] * d["dias"]
    ki, ka = d["kwInv"] * h, d["kwAlt"] * h
    ci, ca = ki * pe, ka * pe
    ahorro = ca - ci
    extra = d["compraInv"] - d["compraAlt"]
    ti = d["compraInv"] + d["vida"] * ci
    ta = d["compraAlt"] + d["vida"] * ca
    dif = ta - ti
    if extra <= 0: anios = 0.0 if ahorro >= 0 else -1.0
    else: anios = extra / ahorro if ahorro > 0 else -1.0
    if d["kwAlt"] > d["kwInv"] and extra > 0 and d["dias"] > 0 and d["vida"] > 0 and pe > 0:
        eq = extra / (d["vida"] * d["dias"] * pe * (d["kwAlt"] - d["kwInv"]))
    else: eq = -1.0
    gan = 2 if abs(dif) < 1 else (0 if dif > 0 else 1)   # 0 inverter, 1 alternativa, 2 empate
    return {"precioEf": pe, "kwhInv": ki, "kwhAlt": ka, "costeInv": ci, "costeAlt": ca, "ahorroAnual": ahorro, "extraCompra": extra,
            "totalInv": ti, "totalAlt": ta, "diferencia": dif, "aniosAmort": anios, "horasEq": eq,
            "esVentilador": 1 if d["kwAlt"] < 0.2 * d["kwInv"] else 0, "ganador": gan}
B = dict(kwInv=0.6, kwAlt=0.05, horas=6, dias=90, precio=0.2, compraInv=800, compraAlt=40, vida=10)
TESTS = [dict(B),                                              # ventilador: gana por coste
         dict(B, kwAlt=1.0, compraAlt=500),                    # no inverter: inverter compensa con 6 h/dia
         dict(B, kwAlt=1.0, compraAlt=500, horas=1),           # poco uso: no compensa
         dict(B, horas=0),                                     # sin uso
         dict(B, kwAlt=1.0, compraAlt=800),                    # misma compra: sin amortizar
         dict(B, kwAlt=1.0, compraAlt=900),                    # inverter mas barato de compra
         dict(B, precio=0),                                    # precio 0
         dict(B, kwAlt=1.0, compraAlt=500, horas=24, dias=366, vida=30)]   # maximos
def rnd(r):
    return dict(kwInv=r.choice([0.3, 0.6, 1.0, 1.5]) + r.random() * 0.05, kwAlt=r.choice([0, 0.05, 0.12, 0.6, 1.0, 1.8]) + r.random() * 0.05,
                horas=r.choice([0, 1, 4, 6, 12, 24]) * r.random(), dias=r.choice([0, 30, 90, 150, 366]) * r.random(),
                precio=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02, compraInv=r.choice([0, 500, 800, 1500]) + r.random() * 50,
                compraAlt=r.choice([0, 40, 300, 500, 900, 1600]) + r.random() * 50, vida=r.choice([1, 5, 10, 20, 30]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(41); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "esVentilador") else (0.01 if k in ("aniosAmort", "horasEq", "precioEf") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeInv", "costeAlt", "kwhInv", "kwhAlt", "ahorroAnual", "totalInv", "totalAlt", "diferencia", "aniosAmort", "horasEq", "esVentilador", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
