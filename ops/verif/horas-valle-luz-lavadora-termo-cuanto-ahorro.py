#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/horas-valle-luz-lavadora-termo-cuanto-ahorro.js, escrito desde la especificacion.
Uso: python3 ops/verif/horas-valle-luz-lavadora-termo-cuanto-ahorro.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "horas-valle-luz-lavadora-termo-cuanto-ahorro"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
def pe(p): return max(p * (1 + IEE), p + IEE_MIN) * (1 + IVA)
def oraculo(d):
    anio = (d["kwhUso"] * d["usosSem"] + d["kwhTermo"]) / 7 * 365
    desp = anio * d["pctDesp"] / 100
    if d["franja"] == 1: o = pe(d["precioPunta"])
    elif d["franja"] == 2: o = (pe(d["precioPunta"]) + pe(d["precioLlano"])) / 2
    else: o = pe(d["precioLlano"])
    v = pe(d["precioValle"]); dif = o - v; ah = desp * dif
    if desp <= 0: est, gan = 3, 1
    elif abs(ah) < 1: est, gan = 1, 2
    elif ah < 0: est, gan = 2, 1
    else: est, gan = 0, 0
    return {"kwhAnio": anio, "kwhDesp": desp, "precioOrigen": o, "precioValle": v, "ahorroKwh": dif, "ahorroAnual": ah, "ahorroMes": ah / 12,
            "ahorroMax": anio * dif, "costeHoy": desp * o, "costeValle": desp * v, "estado": est, "ganador": gan}
B = dict(kwhUso=1.0, usosSem=6, kwhTermo=10, pctDesp=70, precioPunta=0.2048, precioLlano=0.1331, precioValle=0.1194, franja=0)
TESTS = [dict(B),                                   # llano -> valle: ahorro pequeno
         dict(B, franja=1),                         # punta -> valle
         dict(B, franja=2),                         # mitad punta, mitad llano
         dict(B, precioPunta=0.15, precioLlano=0.15, precioValle=0.15, franja=1),   # tarifa de precio unico: empate
         dict(B, precioValle=0.2, franja=0),        # valle mas caro: no mover
         dict(B, pctDesp=0),                        # nada que mover (borde 0 %)
         dict(B, pctDesp=100, franja=1, kwhUso=0, kwhTermo=0),    # sin consumo
         dict(B, pctDesp=100, franja=1, kwhUso=2.5, usosSem=70, kwhTermo=60)]     # maximos
def rnd(r):
    pv = r.choice([0, 0.05, 0.1, 0.12]) + r.random() * 0.03
    return dict(kwhUso=r.choice([0, 0.8, 1.2, 2.5]) * r.random() + 0.01, usosSem=r.choice([0, 3, 7, 14, 70]) * r.random(), kwhTermo=r.choice([0, 5, 20, 60]) * r.random(),
                pctDesp=r.choice([0, 30, 70, 100]) * r.random(), precioPunta=pv + r.random() * 0.2, precioLlano=pv + r.random() * 0.15, precioValle=pv + r.random() * 0.1,
                franja=r.choice([0, 1, 2]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(99); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "estado") else (0.0005 if k in ("precioOrigen", "precioValle", "ahorroKwh") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["kwhAnio", "kwhDesp", "ahorroAnual", "ahorroMes", "ahorroMax", "costeHoy", "costeValle", "estado", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
