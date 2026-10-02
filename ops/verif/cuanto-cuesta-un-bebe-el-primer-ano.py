#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/cuanto-cuesta-un-bebe-el-primer-ano.js, escrito desde la especificacion.
Uso: python3 ops/verif/cuanto-cuesta-un-bebe-el-primer-ano.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cuanto-cuesta-un-bebe-el-primer-ano"
def oraculo(d):
    p = [d["equip"], d["panalim"] * 12, d["ropa"], d["salud"] * 12, d["cuidado"] * d["mesesC"], d["perdida"]]
    bruto = sum(p); ayu = min(d["ayudas"], bruto); total = bruto - ayu; flex = p[0] + p[2] + p[3]
    m = max(range(6), key=lambda i: (p[i], -i))      # la primera en empate
    return {"bruto": bruto, "ayudasAplicadas": ayu, "total": total, "mensualMedio": total / 12,
            "ahorroPrevio": d["equip"] + 3 * (d["panalim"] + d["salud"]) + d["ropa"] / 4,
            "mayor": m if bruto > 0 else -1, "pesoMayor": p[m] / bruto * 100 if bruto > 0 else 0.0,
            "flexibles": flex, "pesoFlex": flex / bruto * 100 if bruto > 0 else 0.0, "ahorro10": flex * 0.1}
B = dict(equip=900, panalim=130, ropa=350, salud=0, cuidado=350, mesesC=4, perdida=2400, ayudas=0)
TESTS = [dict(B),                                           # ejemplo de la pagina
         dict(B, cuidado=0, mesesC=0, perdida=0),           # sin guarderia ni perdida de ingresos
         dict(B, ayudas=1000),                              # con ayudas escritas
         dict(B, ayudas=99999),                             # ayudas mayores que el coste: se limitan
         dict(B, salud=45, cuidado=420, mesesC=9, perdida=0, equip=1500),   # salud privada y guarderia 9 meses
         dict(equip=0, panalim=0, ropa=0, salud=0, cuidado=0, mesesC=0, perdida=0, ayudas=0)]  # borde: todo 0
EXTRA = [dict(B, equip=1560, panalim=130, perdida=0, cuidado=0, mesesC=0, ropa=0)]   # empate equipamiento = panales y alimentacion
def rnd(r):
    return dict(equip=r.choice([0, 300, 900, 1500, 3000]) + r.random() * 20, panalim=r.choice([0, 60, 130, 250]) + r.random() * 10,
                ropa=r.choice([0, 200, 350, 800]) + r.random() * 20, salud=r.choice([0, 0, 30, 60]) + r.random() * 5,
                cuidado=r.choice([0, 250, 350, 600]) + r.random() * 10, mesesC=r.choice([0, 3, 4, 9, 12]),
                perdida=r.choice([0, 1000, 2400, 6000, 12000]) + r.random() * 50, ayudas=r.choice([0, 0, 500, 1200, 5000, 40000]) + r.random() * 20)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(41); ins = TESTS + EXTRA + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "mayor" else (0.01 if k.startswith("peso") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    keys = ["bruto", "total", "mensualMedio", "ahorroPrevio", "mayor", "pesoMayor", "flexibles", "pesoFlex", "ahorro10"]
    if "--write-tests" in sys.argv:
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    for d in TESTS: o = oraculo(d); print({k: round(o[k], 2) for k in keys})
    sys.exit(1 if bad else 0)
