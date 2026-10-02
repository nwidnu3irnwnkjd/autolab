#!/usr/bin/env python3
"""Script independiente (Constructor A) de calcs/universidad-publica-o-privada-o-master.js, escrito desde la especificacion.
Uso: python3 ops/verif/universidad-publica-o-privada-o-master.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)
Modelo (flujo de caja explicito): la privada cuesta c = matpriv - matpub + vida - ayuda al anio mas que la publica, pagado al INICIO de cada
uno de los `anos` de estudio (t = 0..anos-1). Despues se espera una diferencia de salario `dsal` al FINAL de cada uno de los `ntrab` anios de trabajo
(t = anos+1 .. anos+ntrab). Tasa de descuento r = tasa/100 (0 = sin descontar). VAN = valor actual del salario extra - valor actual del sobrecoste."""
import json, math, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "universidad-publica-o-privada-o-master"
def oraculo(d):
    a = int(d["anos"]); n = int(d["ntrab"]); r = d["tasa"] / 100.0
    c = d["matpriv"] - d["matpub"] + d["vida"] - d["ayuda"]
    pvc = sum(c / (1 + r) ** t for t in range(a))
    fac = sum(1 / (1 + r) ** (a + k) for k in range(1, n + 1))     # valor actual de cobrar 1 EUR al anio durante n anios, tras estudiar
    pvs = d["dsal"] * fac
    van = pvs - pvc
    dmin = pvc / fac
    if pvc <= 0: pay = 0.0
    elif d["dsal"] <= 0: pay = -1.0
    else:
        A = pvc * (1 + r) ** a / d["dsal"]
        if r == 0: pay = A
        elif A * r >= 1: pay = -1.0
        else: pay = -math.log(1 - A * r) / math.log(1 + r)
    return {"matPub": a * d["matpub"], "matPriv": a * d["matpriv"], "extra": a * (d["vida"] - d["ayuda"]), "sobrecoste": a * c,
            "pvSobrecoste": pvc, "van": van, "dsalMin": dmin, "anosAmortizar": pay, "mejor": 1 if van > 0 else 0, "gananciaBruta": d["dsal"] * n}
B = dict(anos=4, matpub=1000, matpriv=8000, vida=0, ayuda=0, dsal=2000, ntrab=10, tasa=0)
TESTS = [dict(B),                                   # base: no se amortiza en 10 anios
         dict(B, dsal=4000),                        # se amortiza
         dict(B, anos=1, dsal=0),                   # 1 anio y diferencia de salario 0
         dict(B, dsal=-1500),                       # diferencia negativa
         dict(B, matpriv=1000, vida=0, ayuda=0),    # sobrecoste 0
         dict(B, tasa=5, dsal=3500, vida=3000)]     # con descuento y vida extra
def rnd(r):
    return dict(anos=r.choice([1, 2, 4, 5, 6]), matpub=r.choice([0, 900, 1500, 3000]) + r.random() * 10, matpriv=r.choice([0, 6000, 9000, 15000]) + r.random() * 10,
                vida=r.choice([-3000, 0, 0, 4000, 9000]) + r.random() * 10, ayuda=r.choice([0, 0, 1500, 6000]) + r.random() * 10,
                dsal=r.choice([-2000, 0, 1500, 3000, 8000]) + r.random() * 10, ntrab=r.choice([1, 5, 10, 25, 40]), tasa=r.choice([0, 0, 2, 5, 12]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    rr = random.Random(57); ins = TESTS + [rnd(rr) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "mejor" else (0.01 if k == "anosAmortizar" else 1.0)
            if j.get(k) is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j.get(k), v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
