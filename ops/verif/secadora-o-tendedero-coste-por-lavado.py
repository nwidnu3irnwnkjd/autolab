#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/secadora-o-tendedero-coste-por-lavado.js, escrito desde la especificacion.
Uso: python3 ops/verif/secadora-o-tendedero-coste-por-lavado.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "secadora-o-tendedero-coste-por-lavado"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
def oraculo(d):
    pe = max(d["precio"] * (1 + IEE), d["precio"] + IEE_MIN) * (1 + IVA)
    ciclo = d["kwh"] * pe; n = d["coladas"] * d["semanas"]
    energia = ciclo * n; horas = d["minutos"] * n / 60; tiempo = horas * d["valorHora"]
    ts = d["compra"] + d["vida"] * energia; tt = d["vida"] * tiempo; dif = tt - ts
    base = d["minutos"] / 60 * d["vida"] * n
    veq = ts / base if (base > 0 and ts > 0) else -1.0
    den = d["vida"] * (d["valorHora"] * d["minutos"] / 60 - ciclo)
    ceq = d["compra"] / den / d["semanas"] if (den > 0 and d["semanas"] > 0 and d["compra"] > 0) else -1.0
    gan = 2 if abs(dif) < max(1.0, 0.05 * max(ts, tt)) else (0 if dif > 0 else 1)
    return {"precioEf": pe, "ciclo": ciclo, "coladasAno": n, "kwhAno": d["kwh"] * n, "energiaAno": energia, "horasAno": horas, "tiempoAno": tiempo,
            "totalSecadora": ts, "totalTendedero": tt, "diferencia": dif, "valorEq": veq, "coladasEq": ceq, "ganador": gan}
B = dict(coladas=4, semanas=40, kwh=2.0, precio=0.2, minutos=15, valorHora=0, compra=450, vida=10)
TESTS = [dict(B),                                   # tiempo valorado a 0: gana el tendedero
         dict(B, valorHora=15),                     # tiempo valioso: gana la secadora
         dict(B, valorHora=8),                      # cerca del equilibrio
         dict(B, coladas=0),                        # sin uso
         dict(B, coladas=0, compra=0),              # empate exacto
         dict(B, compra=0),                         # secadora ya comprada
         dict(B, minutos=0, valorHora=15),          # tendedero sin tiempo
         dict(B, precio=0),                         # precio 0
         dict(B, valorHora=40, coladas=10, semanas=52, vida=30)]   # maximos de uso
def rnd(r):
    return dict(coladas=r.choice([0, 1, 3, 5, 10, 30]) * r.random(), semanas=r.choice([0, 10, 40, 52]) * r.random(),
                kwh=r.choice([0.5, 1.0, 2.0, 3.5]) + r.random() * 0.2, precio=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02,
                minutos=r.choice([0, 5, 15, 30]) * r.random(), valorHora=r.choice([0, 0, 5, 12, 40]) * r.random(),
                compra=r.choice([0, 300, 450, 900]) + r.random() * 50, vida=r.choice([1, 5, 10, 20, 30]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(61); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("valorEq", "coladasEq", "precioEf", "ciclo") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["ciclo", "coladasAno", "kwhAno", "energiaAno", "horasAno", "tiempoAno", "totalSecadora", "totalTendedero", "diferencia", "valorEq", "coladasEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
