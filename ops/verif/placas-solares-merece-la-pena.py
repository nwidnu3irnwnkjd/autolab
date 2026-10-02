#!/usr/bin/env python3
"""Oraculo independiente (Constructor B) de calcs/placas-solares-merece-la-pena.js, escrito desde la especificacion, antes del .js.
Modelo (años 1..N, euros constantes salvo la subida opcional del precio):
  P_t = kWp * kWh/kWp * (1-deg)^(t-1);  auto_t = min(pct * P_t, consumo);  exc_t = P_t - auto_t;  compra_t = consumo - auto_t
  precio_t = precio * (1+g)^(t-1);  ahorro_t = auto_t * precio_t
  tope_t (RD 244/2019 art. 14.3.ii.b: la compensacion no supera la energia consumida de la red) = compra_t * precio_t / ((1+iee)(1+iva))
  comp_t = min(exc_t * comp, tope_t) * (1+iee)*(1+iva)   [RD 244/2019 art.14.6.ii-iv: se descuenta antes de impuestos y luego se aplican IEE e IVA; Ley 38/1992 art.94.9: compensada exenta de IEE];  flujo_t = ahorro_t + comp_t;  coste neto = max(coste - subv, 0)
Amortizacion = primer momento en que el acumulado (fin de cada año) iguala el coste neto, interpolando linealmente dentro del año; -1 si no llega en N.
Uso: python3 ops/verif/placas-solares-merece-la-pena.py [--write-tests]"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "placas-solares-merece-la-pena"
N, DEG, G0, G_SENS, DTO, IEE, IVA, AUTO_SENS = 25, 0.005, 0.0, 0.03, 0.03, 0.0511269632, 0.21, 10
def flujos(d, g=G0, pct=None):
    pct = d["pctAuto"] if pct is None else pct
    out = []
    for t in range(1, N + 1):
        p = d["potencia"] * d["prod"] * (1 - DEG) ** (t - 1)
        a = min(pct / 100 * p, d["consumo"]); e = p - a; compra = d["consumo"] - a
        pr = d["precio"] * (1 + g) ** (t - 1)
        k = (1 + IEE) * (1 + IVA)   # impuestos que se ahorran sobre cada euro compensado
        comp = min(e * d["comp"], compra * pr / k) * k
        out.append((a * pr, comp, a, e, e * d["comp"] * k))
    return out
def amort(net, fl):
    if net <= 0: return 0.0
    acc = 0.0
    for i, f in enumerate(fl):
        if f > 0 and acc + f >= net: return i + (net - acc) / f
        acc += f
    return -1.0
def tir(net, fl):
    if net <= 0 or sum(fl) <= 0: return None
    f = lambda r: -net + sum(x / (1 + r) ** (i + 1) for i, x in enumerate(fl))
    lo, hi = -0.99, 20.0
    if f(lo) < 0 or f(hi) > 0: return None
    for _ in range(200):
        m = (lo + hi) / 2
        if f(m) > 0: lo = m
        else: hi = m
    return (lo + hi) / 2 * 100
def oraculo(d):
    net = max(d["coste"] - d["subv"], 0.0); F = flujos(d); fl = [a + b for a, b, *_ in F]
    fd = [x / (1 + DTO) ** (i + 1) for i, x in enumerate(fl)]
    t = tir(net, fl); tot = sum(fl)
    return {"neto": net, "ahorro1": fl[0], "ahorroAuto1": F[0][0], "comp1": F[0][1], "compSinTope1": F[0][4], "autoKwh1": F[0][2], "excKwh1": F[0][3],
            "topeAplicado": 1 if F[0][4] > F[0][1] + 1e-9 else 0, "anosAmort": amort(net, fl), "anosAmortDto": amort(net, fd),
            "ahorroNeto": tot - net, "tir": -999.0 if t is None else t, "hayTir": 0 if t is None else 1,
            "anosSubida": amort(net, [a + b for a, b, *_ in flujos(d, g=G_SENS)]),
            "anosAutoMenos": amort(net, [a + b for a, b, *_ in flujos(d, pct=max(d["pctAuto"] - AUTO_SENS, 0))]),
            "costeMaxVida": tot + d["subv"], "costeMax10": sum(fl[:10]) + d["subv"],
            "costeKwp": d["coste"] / d["potencia"] if d["potencia"] > 0 else -1.0}
B = dict(potencia=4, coste=6000, subv=0, consumo=4000, pctAuto=40, prod=1610, precio=0.18, comp=0.07)
TESTS = [dict(B),
         dict(B, pctAuto=0),                                   # todo se vierte: compensacion limitada por el tope
         dict(B, pctAuto=100, consumo=2000),                   # autoconsumo topado por el consumo
         dict(B, coste=0),                                     # coste cero
         dict(B, coste=3000, subv=5000),                       # subvencion mayor que coste
         dict(B, prod=0),                                      # sin produccion
         dict(B, potencia=6, coste=12000, subv=1500, consumo=3000, pctAuto=30, prod=1280, precio=0.25, comp=0.1),
         dict(B, coste=9000, precio=0.13, pctAuto=30, prod=1165),   # amortiza justo al final de la vida
         dict(B, coste=12000, precio=0.13, pctAuto=30, prod=1165),   # no se amortiza en la vida
         dict(potencia=8, coste=9000, subv=0, consumo=3000, pctAuto=20, prod=1667, precio=0.20, comp=0.10),   # tope activo (informe verif.)
         dict(potencia=5, coste=5000, subv=6000, consumo=2000, pctAuto=80, prod=1600, precio=0.18, comp=0.06),  # subv > coste, autoconsumo limitado al consumo
         dict(B, pctAuto=0)]                                   # informe verif.: 4 kWp, 0 % autoconsumo, comp 0,07 (igual que el caso 2, valor de referencia independiente)
def rnd(r):
    return dict(potencia=r.choice([0.5, 2, 3, 4, 5, 8, 15]) + r.random(), coste=r.choice([0, 1500, 4000, 6000, 9000, 14000, 30000]) + r.random() * 300,
                subv=r.choice([0, 0, 500, 2000, 10000]), consumo=r.choice([0, 800, 2500, 4000, 7000, 12000]) + r.random() * 100,
                pctAuto=r.choice([0, 10, 30, 45, 70, 100]), prod=r.choice([0, 1100, 1300, 1600, 1700]) + r.random() * 50,
                precio=r.choice([0, 0.08, 0.15, 0.2, 0.3]) + r.random() * 0.02, comp=r.choice([0, 0.03, 0.07, 0.12]) + r.random() * 0.01)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    rr = random.Random(7); ins = TESTS + [rnd(rr) for _ in range(600)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if not isinstance(j.get(k), (int, float)) or abs(j[k] - v) > 0.01 and abs(j[k] - v) > 1e-6 * abs(v): bad += 1; print("DISCREPANCIA", d, k, j.get(k), v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["neto", "ahorro1", "comp1", "anosAmort", "anosAmortDto", "ahorroNeto", "tir", "anosSubida", "anosAutoMenos", "costeMaxVida"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
