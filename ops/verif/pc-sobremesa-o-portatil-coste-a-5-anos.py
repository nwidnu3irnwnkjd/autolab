#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/pc-sobremesa-o-portatil-coste-a-5-anos.js, escrito desde la especificacion.
Uso: python3 ops/verif/pc-sobremesa-o-portatil-coste-a-5-anos.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "pc-sobremesa-o-portatil-coste-a-5-anos"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
KW_S, KW_P = 0.15, 0.04
def oraculo(d):
    pe = max(d["precioKwh"] * (1 + IEE), d["precioKwh"] + IEE_MIN) * (1 + IVA)
    horas_tot = d["horas"] * 365 * d["anios"]
    ks, kp = KW_S * horas_tot, KW_P * horas_tot
    es, ep = ks * pe, kp * pe
    f = 1 - d["resid"] / 100
    ts = d["precioSob"] * f + d["extraSob"] + es
    tp = d["precioPort"] * f + d["repPort"] + ep
    dif = ts - tp
    menor = min(ts, tp)
    gan = 2 if (abs(dif) < 0.05 * menor or abs(dif) < 1e-9) else (1 if dif > 0 else 0)  # 0 sobremesa, 1 portatil, 2 empate
    # precio del portatil que iguala: tp(x) = ts  ->  x*f + repPort + ep = ts
    ppeq = (ts - d["repPort"] - ep) / f if f > 0 else -1
    # extras del sobremesa que igualan: precioSob*f + x + es = tp
    seq = tp - d["precioSob"] * f - es
    return {"kwhSob": ks, "kwhPort": kp, "energiaSob": es, "energiaPort": ep, "totalSob": ts, "totalPort": tp,
            "anualSob": ts / d["anios"], "anualPort": tp / d["anios"], "diferencia": dif,
            "precioPortEq": ppeq if ppeq > 0 else -1.0, "extraSobEq": seq if seq > 0 else -1.0, "precioEf": pe, "ganador": gan}
B = dict(precioSob=700, precioPort=900, extraSob=250, repPort=100, anios=5, horas=4, precioKwh=0.2, resid=0)
TESTS = [dict(B),                                           # portatil gana (ejemplo de la pagina)
         dict(B, precioPort=1300, extraSob=150),            # sobremesa gana
         dict(B, resid=30),                                 # con valor residual
         dict(B, precioPort=1040),                         # cercano al empate practico
         dict(B, horas=12, anios=8),                        # mucho uso, vida larga
         dict(B, horas=0, extraSob=0, repPort=0),           # sin uso ni extras
         dict(B, resid=90, precioKwh=0),                    # maximos de residual, luz a 0
         dict(B, anios=1, horas=24)]                        # minimos/maximos
def rnd(r):
    return dict(precioSob=r.choice([300, 700, 1200, 2500]) + r.random() * 80, precioPort=r.choice([350, 900, 1500, 2800]) + r.random() * 80,
                extraSob=r.choice([0, 100, 250, 600, 1500]) * r.random(), repPort=r.choice([0, 50, 100, 300]) * r.random(),
                anios=r.choice([1, 3, 5, 8, 15]) * (0.9 + r.random() * 0.1) + (0.1 if r.random() < .5 else 0), horas=r.choice([0, 1, 4, 8, 24]) * r.random(),
                precioKwh=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02, resid=r.choice([0, 10, 40, 90]) * r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(52); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k == "precioEf" else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["totalSob", "totalPort", "energiaSob", "energiaPort", "anualSob", "anualPort", "diferencia", "precioPortEq", "extraSobEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
