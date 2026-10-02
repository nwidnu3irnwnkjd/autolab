#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/comedor-escolar-o-tupper.js, escrito desde la especificacion.
Uso: python3 ops/verif/comedor-escolar-o-tupper.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "comedor-escolar-o-tupper"
def oraculo(d):
    pago = d["menu"] * (1 - d["desc"] / 100)          # lo que pagas por menu y hijo
    comedor = pago * d["dias"] * d["hijos"]
    horas = d["dias"] * d["minutos"] / 60
    tiempo = horas * d["valorHora"]
    compra = d["compra"] * d["hijos"] * d["dias"]
    tupper = compra + tiempo + d["material"]
    dif = comedor - tupper
    gan = 2 if (abs(dif) < 0.05 * min(comedor, tupper) or abs(dif) < 1e-9) else (1 if dif > 0 else 0)   # 0 comedor, 1 tupper, 2 empate
    eq = tupper / (d["hijos"] * d["dias"] * (1 - d["desc"] / 100)) if d["desc"] < 100 else -1.0
    return {"comedor": comedor, "comedorDia": pago * d["hijos"], "tupper": tupper, "tupperDia": tupper / d["dias"], "compra": compra,
            "tiempo": tiempo, "horas": horas, "diferencia": dif, "menuEq": eq, "ganador": gan}
B = dict(menu=6, dias=170, desc=0, hijos=1, compra=3, minutos=20, valorHora=0, material=30)
TESTS = [dict(B),                                  # gana el tupper (sin valorar tiempo)
         dict(B, valorHora=10),                    # con el tiempo valorado gana el comedor
         dict(B, desc=50),                         # descuento declarado del 50 %
         dict(B, hijos=2, compra=3.5),             # dos hijos
         dict(B, desc=100),                        # comedor gratuito por beca
         dict(B, menu=3.2),                         # cerca del empate
         dict(B, minutos=0, material=0, compra=0), # tupper sin coste
         dict(B, dias=366, hijos=10, minutos=240, valorHora=30)]  # maximos
def rnd(r):
    return dict(menu=r.choice([1, 3, 5, 7, 9]) + r.random(), dias=r.choice([1, 40, 120, 170, 366]), desc=r.choice([0, 20, 50, 100, 33.3]),
                hijos=r.choice([1, 2, 3, 10]), compra=r.choice([0, 1, 2.5, 4, 8]) * r.random() * 1.2, minutos=r.choice([0, 10, 25, 240]) * r.random(),
                valorHora=r.choice([0, 0, 8, 20]) * r.random(), material=r.choice([0, 20, 80]) * r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(63); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("menuEq", "comedorDia", "tupperDia", "horas") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["comedor", "tupper", "compra", "tiempo", "horas", "diferencia", "menuEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
