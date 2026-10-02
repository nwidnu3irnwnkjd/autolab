#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/teletrabajo-o-oficina-coste-real.js, escrito desde la especificacion.
Uso: python3 ops/verif/teletrabajo-o-oficina-coste-real.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "teletrabajo-o-oficina-coste-real"
def oraculo(d):
    # dia a dia: 46 semanas teletrabajables; compensacion mensual x 12; equipamiento / 4 anos; con 0 dias nada de lo fijo aplica
    dias_ano = d["dias"] * 46
    desp = comida = casa = 0.0
    for _ in range(int(round(dias_ano * 2))):          # medio dia como unidad (dias en pasos de 0,5)
        desp += d["desp"] / 2; comida += d["comida"] / 2; casa += d["casa"] / 2
    comp = d["comp"] * 12 if d["dias"] > 0 else 0.0
    equip = d["equip"] / 4 if d["dias"] > 0 else 0.0
    neto = desp + comida + comp - casa - equip
    horas = dias_ano * d["min"] / 60
    U = 46 * (d["desp"] + d["comida"] - d["casa"]); F = d["comp"] * 12 - d["equip"] / 4
    if (U > 0 and F >= 0) or (U == 0 and F > 0): tipo, deq = 0, 0.0
    elif U > 0: tipo, deq = 1, -F / U
    elif U < 0 and F > 0: tipo, deq = 2, F / -U
    else: tipo, deq = 3, 0.0
    return {"ahorroDesplazamiento": desp, "ahorroComida": comida, "costeCasa": casa, "compensacionAnual": comp, "equipamientoAnual": equip,
            "netoAnual": neto, "netoMensual": neto / 12, "horasAhorradas": horas, "valorTiempo": horas * d["valorHora"], "netoConTiempo": neto + horas * d["valorHora"],
            "tipoDias": tipo, "diasEquilibrio": deq, "compensacionEquilibrio": max(0.0, equip - (desp + comida - casa)) / 12}
B = dict(dias=2, desp=6, min=60, valorHora=0, casa=0.7, comida=5, comp=0, equip=300)
TESTS = [dict(B),                                              # ahorra
         dict(B, desp=0, comida=0, casa=2, comp=0, equip=0),   # solo cuesta: nunca ahorras
         dict(B, dias=0),                                      # borde: 0 dias
         dict(B, desp=0, comida=0, casa=0, equip=0, comp=0),   # borde: todo 0
         dict(B, desp=2, comida=1, casa=5, comp=20, equip=0),  # coste por dia, cubierto por la compensacion hasta N dias
         dict(B, dias=5, desp=1, comida=0, casa=0.5, equip=900, comp=0, valorHora=15)]  # equipamiento grande, tiempo valorado
def rnd(r):
    return dict(dias=r.choice([0, 0.5, 1, 2, 3, 4, 5]), desp=r.choice([0, 1, 3, 6, 12]) + r.random(), min=r.choice([0, 30, 60, 120]), valorHora=r.choice([0, 0, 10, 25]),
                casa=r.choice([0, 0.5, 1, 3, 8]) + r.random(), comida=r.choice([0, 3, 6, 10]), comp=r.choice([0, 0, 20, 60, 150]), equip=r.choice([0, 200, 600, 1500]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(23); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if abs(j[k] - v) > max(0.01, 1e-6 * abs(v)): bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["ahorroDesplazamiento", "ahorroComida", "costeCasa", "compensacionAnual", "equipamientoAnual", "netoAnual", "netoMensual", "horasAhorradas", "netoConTiempo", "tipoDias", "diasEquilibrio", "compensacionEquilibrio"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 0 if k in ("netoAnual", "netoConTiempo") else 3) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
