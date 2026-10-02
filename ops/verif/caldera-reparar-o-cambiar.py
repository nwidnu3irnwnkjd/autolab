#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/caldera-reparar-o-cambiar.js, escrito desde la especificacion.
Uso: python3 ops/verif/caldera-reparar-o-cambiar.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "caldera-reparar-o-cambiar"
VN, RIESGO = 15.0, 0.10
def oraculo(d):
    neta = max(d["nueva"] - d["ayuda"], 0.0)
    gas_act = d["consumo"] * d["pgas"]
    gas_nue = d["consumo"] * d["rendAct"] / d["rendNueva"] * d["pgas"]
    ahorro = gas_act - gas_nue
    reserva = RIESGO * d["repar"]
    rep = d["repar"] / d["vida"] + reserva + gas_act
    cam = neta / VN + gas_nue
    flujo = ahorro + reserva
    extra = neta - d["repar"]
    if extra <= 0 and flujo >= 0: vs = 0.0
    elif flujo <= 0: vs = -1.0
    else: vs = extra / flujo
    amort_gas = neta / ahorro if ahorro > 0 else (0.0 if neta <= 0 else -1.0)
    eq = (neta / VN - ahorro) / (1.0 / d["vida"] + RIESGO)
    diff = rep - cam
    gan = 2 if abs(diff) < 1 else (1 if diff > 0 else 0)   # 0 reparar, 1 cambiar, 2 empate
    return {"anualReparar": rep, "anualCambiar": cam, "gasActual": gas_act, "gasNuevo": gas_nue, "ahorroGas": ahorro,
            "neta": neta, "amortVsRep": vs, "amortGas": amort_gas, "equilibrio": eq, "diferencia": diff, "ganador": gan}
B = dict(repar=450, nueva=2500, ayuda=0, consumo=8000, rendAct=0.81, rendNueva=0.92, pgas=0.064, vida=5)
TESTS = [dict(B),                                   # base
         dict(B, repar=900, consumo=15000),         # reparacion cara, mucho gas: cambiar
         dict(B, repar=80, vida=8),                 # reparacion barata: reparar
         dict(B, consumo=0),                        # consumo 0
         dict(B, ayuda=2500, repar=0),              # ayuda cubre todo, reparacion gratis
         dict(B, rendNueva=0.81),                   # mismo rendimiento: ahorro de gas 0
         dict(B, repar=250),                        # reparacion por debajo del equilibrio
         dict(B, repar=351.5),                      # en el equilibrio
         dict(B, consumo=15000)]                    # mas gas: equilibrio mas bajo
def rnd(r):
    return dict(repar=r.choice([0, 100, 450, 900, 1500]) + r.random() * 20, nueva=r.choice([0, 1200, 2500, 4500]) + r.random() * 50,
                ayuda=r.choice([0, 0, 500, 1500, 3000]) + r.random(), consumo=r.choice([0, 3000, 8000, 15000, 25000]) + r.random() * 50,
                rendAct=r.choice([0.6, 0.7, 0.81, 0.9]) + r.random() * 0.02, rendNueva=r.choice([0.6, 0.85, 0.92, 1.0]) + r.random() * 0.02,
                pgas=r.choice([0, 0.04, 0.064, 0.1]) + r.random() * 0.005, vida=r.choice([1, 2, 5, 10, 15]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.01 if k in ("amortVsRep", "amortGas") else 1.0)
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["anualReparar", "anualCambiar", "gasActual", "gasNuevo", "ahorroGas", "neta", "amortVsRep", "amortGas", "equilibrio", "diferencia", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
