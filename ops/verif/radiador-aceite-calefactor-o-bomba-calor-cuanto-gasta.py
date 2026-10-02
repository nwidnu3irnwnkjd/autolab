#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/radiador-aceite-calefactor-o-bomba-calor-cuanto-gasta.js, escrito desde la especificacion.
Uso: python3 ops/verif/radiador-aceite-calefactor-o-bomba-calor-cuanto-gasta.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "radiador-aceite-calefactor-o-bomba-calor-cuanto-gasta"
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
def oraculo(d):
    pe = max(d["precio"] * (1 + IEE), d["precio"] + IEE_MIN) * (1 + IVA)
    kr = d["potencia"] * d["aisl"]; kb = kr / d["cop"]
    hr, hb = kr * pe, kb * pe
    dr, db = hr * d["horas"], hb * d["horas"]
    ar, ab = dr * d["dias"], db * d["dias"]
    tr = d["vida"] * ar; tb = d["compraExtra"] + d["vida"] * ab; dif = tr - tb
    ahorro = ar - ab
    if d["compraExtra"] <= 0: anios = 0.0 if ahorro >= 0 else -1.0
    else: anios = d["compraExtra"] / ahorro if ahorro > 0 else -1.0
    if d["compraExtra"] > 0 and d["cop"] > 1 and d["horas"] > 0 and kr > 0 and pe > 0:
        eq = d["compraExtra"] / (d["vida"] * pe * kr * d["horas"] * (1 - 1 / d["cop"]))
    else: eq = -1.0
    umbral = max(1.0, 0.05 * max(tr, tb))
    gan = 2 if abs(dif) < umbral else (1 if dif > 0 else 0)
    return {"precioEf": pe, "kwR": kr, "kwB": kb, "horaR": hr, "horaB": hb, "diaR": dr, "diaB": db, "mesR": dr * 30, "mesB": db * 30,
            "anoR": ar, "anoB": ab, "kwhAnoR": kr * d["horas"] * d["dias"], "kwhAnoB": kb * d["horas"] * d["dias"], "ahorroAnual": ahorro,
            "totalR": tr, "totalB": tb, "diferencia": dif, "aniosAmort": anios, "diasEq": eq, "ganador": gan}
B = dict(potencia=1.0, aisl=1.0, horas=6, dias=120, precio=0.2, cop=3.0, compraExtra=600, vida=10)
TESTS = [dict(B),                                   # bomba gana
         dict(B, compraExtra=3000),                 # compra extra grande: gana la resistencia
         dict(B, cop=1.0),                          # COP 1: sin ahorro de energia
         dict(B, compraExtra=0),                    # misma compra: sin amortizar
         dict(B, horas=0),                          # sin uso
         dict(B, aisl=1.3, potencia=1.5),           # mal aislamiento
         dict(B, dias=20, compraExtra=1000),        # poco uso
         dict(B, cop=1.0, compraExtra=0),           # empate exacto
         dict(B, precio=0, compraExtra=200),        # precio 0
         dict(B, horas=24, dias=366, vida=30, cop=4.5)]  # maximos
def rnd(r):
    return dict(potencia=r.choice([0.3, 0.8, 1.2, 2.0]) + r.random() * 0.1, aisl=r.choice([0.7, 1.0, 1.3]),
                horas=r.choice([0, 1, 4, 8, 24]) * r.random(), dias=r.choice([0, 20, 90, 150, 366]) * r.random(),
                precio=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02, cop=1 + r.random() * 5,
                compraExtra=r.choice([0, 0, 200, 600, 2000]) + r.random() * 50, vida=r.choice([1, 5, 10, 20, 30]) * (0.9 + r.random() * 0.1) + 0.1)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(53); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("aniosAmort", "diasEq", "precioEf") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["horaR", "horaB", "diaR", "diaB", "mesR", "mesB", "anoR", "anoB", "kwhAnoR", "kwhAnoB", "ahorroAnual", "totalR", "totalB", "diferencia", "aniosAmort", "diasEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
