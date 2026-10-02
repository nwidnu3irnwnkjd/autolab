#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/vivir-cerca-del-trabajo-o-mas-barato-lejos.js, escrito desde la especificacion.
Uso: python3 ops/verif/vivir-cerca-del-trabajo-o-mas-barato-lejos.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "vivir-cerca-del-trabajo-o-mas-barato-lejos"
def oraculo(d):
    ahorro = 12 * (d["alq_cerca"] - d["alq_lejos"])
    desplaz = 2 * d["dias"] * d["km"] * d["cpk"] + 12 * d["abono"]
    horas = 2 * d["dias"] * d["min"] / 60.0
    tval = horas * d["vh"]
    neto = ahorro - desplaz - tval
    cerca = 12 * d["alq_cerca"]; lejos = 12 * d["alq_lejos"] + desplaz + tval
    tipo = 2 if abs(neto) < 0.05 * max(cerca, lejos) else (0 if neto > 0 else 1)
    vh_eq = (ahorro - desplaz) / horas if horas > 0 and ahorro - desplaz > 0 else -1
    pkm = d["min"] / d["km"] if d["km"] > 0 else 0.0
    den = 2 * d["dias"] * (d["cpk"] + d["vh"] * pkm / 60.0)
    resto = ahorro - 12 * d["abono"]
    km_eq = resto / den if den > 0 and resto > 0 else -1
    return {"ahorroAlquiler": ahorro, "desplaz": desplaz, "horas": horas, "tiempoVal": tval, "extra": desplaz + tval, "neto": neto,
            "netoSin": ahorro - desplaz, "costeCerca": cerca, "costeLejos": lejos, "tipo": tipo, "vhEq": vh_eq,
            "alqEq": d["alq_lejos"] + (desplaz + tval) / 12.0, "kmEq": km_eq}
B = dict(alq_cerca=1000, alq_lejos=750, km=22, min=30, cpk=0.2, abono=0, dias=220, vh=0)
TESTS = [dict(B),                                        # lejos gana sin valorar el tiempo
         dict(B, vh=12),                                 # con la hora a 12 EUR gana cerca
         dict(B, cpk=0, abono=90, vh=6),                 # transporte publico
         dict(B, alq_lejos=1000, vh=0),                  # mismo alquiler: cerca gana
         dict(B, km=0, min=0),                           # sin desplazamiento extra: lejos gana por el ahorro
         dict(B, alq_lejos=700, km=10, min=10, cpk=0.1, dias=100)]  # borde con pocos dias
def rnd(r):
    return dict(alq_cerca=r.choice([300, 600, 1000, 1500, 2500]) + r.random() * 50, alq_lejos=r.choice([250, 500, 750, 1100, 2000]) + r.random() * 50,
                km=r.choice([0, 3, 10, 22, 50, 120]) + r.random() * 3, min=r.choice([0, 10, 30, 60, 120]) + r.random() * 5,
                cpk=r.choice([0, 0.1, 0.2, 0.4]) + r.random() * 0.02, abono=r.choice([0, 0, 25, 60, 150]),
                dias=r.choice([60, 100, 180, 220, 250]), vh=r.choice([0, 0, 3, 8, 15, 40]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["ahorroAlquiler", "desplaz", "horas", "tiempoVal", "neto", "netoSin", "costeCerca", "costeLejos", "tipo", "vhEq", "alqEq", "kmEq"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
