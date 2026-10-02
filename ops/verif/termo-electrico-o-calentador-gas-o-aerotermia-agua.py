#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/termo-electrico-o-calentador-gas-o-aerotermia-agua.js, escrito desde la especificacion.
Uso: python3 ops/verif/termo-electrico-o-calentador-gas-o-aerotermia-agua.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "termo-electrico-o-calentador-gas-o-aerotermia-agua"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
LITROS, SALTO, ETA_T, ETA_G, COP = 40, 45, 0.9, 0.8, 2.8
def oraculo(d):
    pe = max(d["precioLuz"] * (1 + IEE), d["precioLuz"] + IEE_MIN) * (1 + IVA)
    util = d["personas"] * LITROS * 365 * SALTO * 4.186 / 3600 * 1.0       # 4,186 kJ/(kg K) / 3600 = 0,0011628 kWh/(l K)
    util = d["personas"] * LITROS * 365 * SALTO * 0.001163
    k = [util / ETA_T, util / ETA_G, util / COP]
    c = [k[0] * pe, k[1] * d["precioGas"] + d["fijoGas"], k[2] * pe]
    buy = [d["compraTermo"], d["compraGas"], d["compraAero"]]
    tot = [buy[i] + d["vida"] * c[i] for i in range(3)]
    orden = sorted(range(3), key=lambda i: (tot[i], i))
    best, sec = orden[0], tot[orden[1]]
    def anios(i):
        extra, ah = buy[i] - buy[0], c[0] - c[i]
        if extra <= 0: return 0.0 if ah >= 0 else -1.0
        return extra / ah if ah > 0 else -1.0
    def pers(i):
        extra, ah = buy[i] - buy[0], c[0] - c[i]
        return extra / (d["vida"] * ah / d["personas"]) if (extra > 0 and ah > 0) else -1.0
    return {"precioEf": pe, "kwhUtil": util, "kwhTermo": k[0], "kwhGas": k[1], "kwhAero": k[2], "costeTermo": c[0], "costeGas": c[1], "costeAero": c[2],
            "totalTermo": tot[0], "totalGas": tot[1], "totalAero": tot[2], "segundo": sec - tot[best], "aniosGas": anios(1), "aniosAero": anios(2),
            "personasGas": pers(1), "personasAero": pers(2), "ganador": 3 if sec - tot[best] < 1 else best}
B = dict(personas=3, precioLuz=0.2, precioGas=0.064, fijoGas=0, compraTermo=300, compraGas=500, compraAero=2000, vida=10)
TESTS = [dict(B),                                              # gas gana sin fijo
         dict(B, fijoGas=300),                                 # gas con fijo alto: gana la aerotermia
         dict(B, personas=1, compraAero=3000, precioGas=0.3),  # pocas personas y gas caro: gana el termo
         dict(B, personas=6, precioGas=0.12),                  # muchas personas, gas caro: gana la aerotermia
         dict(B, compraGas=300, compraAero=300),               # misma compra: sin amortizar
         dict(B, compraGas=100, compraAero=100, precioGas=0.5),# gas mas caro que luz: no recupera
         dict(B, precioLuz=0, precioGas=0, compraGas=300, compraAero=290.4),  # precios 0: gas y aerotermia a menos de 1 euro: empate
         dict(B, personas=12, vida=30, compraAero=8000)]       # maximos
def rnd(r):
    return dict(personas=r.choice([1, 2, 3, 5, 8, 12]) - r.random() * 0.9 if r.random() < 0.3 else float(r.choice([1, 2, 3, 4, 6, 12])),
                precioLuz=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02, precioGas=r.choice([0, 0.04, 0.064, 0.12, 0.3]) + r.random() * 0.01,
                fijoGas=r.choice([0, 0, 80, 119, 300]), compraTermo=r.choice([0, 150, 300, 600]) + r.random() * 30,
                compraGas=r.choice([0, 300, 500, 900, 1500]) + r.random() * 30, compraAero=r.choice([0, 500, 1500, 2000, 4000, 8000]) + r.random() * 30,
                vida=r.choice([1, 5, 10, 15, 30]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(77); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("aniosGas", "aniosAero", "personasGas", "personasAero", "precioEf") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeTermo", "costeGas", "costeAero", "kwhUtil", "totalTermo", "totalGas", "totalAero", "aniosGas", "aniosAero", "personasGas", "personasAero", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
        for d in TESTS: o = oraculo(d); print({k: round(o[k], 2) for k in ["costeTermo", "costeGas", "costeAero", "totalTermo", "totalGas", "totalAero", "aniosAero", "aniosGas", "personasAero", "personasGas", "ganador"]})
    sys.exit(1 if bad else 0)
