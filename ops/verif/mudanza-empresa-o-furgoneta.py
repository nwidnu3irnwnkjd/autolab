#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/mudanza-empresa-o-furgoneta.js, escrito desde la especificacion.
Uso: python3 ops/verif/mudanza-empresa-o-furgoneta.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, math, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "mudanza-empresa-o-furgoneta"
def coste(d, dist):
    viajes = math.ceil(d["vol"] / 20.0)
    km = viajes * 2.0 * dist
    dias = max(1, math.ceil(km / 600.0))
    h_carga = d["vol"] * 0.6 / (1 + d["nayud"])
    ayud = d["nayud"] * d["eurayud"] * h_carga
    return viajes, km, dias, h_carga, dias * d["alqdia"] + km * d["kmfurgo"] + d["extras"] + ayud, h_carga + km / 80.0
def oraculo(d):
    viajes, km, dias, hc, directo, hu = coste(d, d["dist"])
    reserva = 5.0 * d["vol"]; d1 = d["empresa"] - directo; d2 = d1 - reserva
    tipo = 1 if d1 <= 0 else (2 if d2 <= 0 else 3)
    km_eq = -1
    for x in range(0, 3001):
        if coste(d, x)[4] < d["empresa"]: km_eq = x
        else: break
    return {"costeFurgo": directo, "reserva": reserva, "costeFurgoConReserva": directo + reserva, "costeEmpresa": d["empresa"],
            "m3Furgo": directo / d["vol"], "m3Empresa": d["empresa"] / d["vol"], "viajes": viajes, "dias": dias, "km": km, "horasTuyas": hu,
            "horasCarga": hc, "diferencia": d1, "tipo": tipo, "horaEq": d2 / hu if tipo == 3 else 0.0, "kmEq": km_eq, "presupuestoEq": directo + reserva}
B = dict(vol=20, dist=50, empresa=900, alqdia=90, kmfurgo=0.231, extras=60, nayud=2, eurayud=12)
TESTS = [dict(B),                                      # furgoneta gana en gasto directo; la hora decide
         dict(B, empresa=250),                         # la empresa gana por coste directo
         dict(B, empresa=300, extras=0),               # la reserva de danos da la vuelta
         dict(B, vol=45, dist=400),                    # 3 viajes, varios dias
         dict(B, dist=0),                              # 0 km
         dict(B, nayud=0, extras=0, alqdia=0, kmfurgo=0, empresa=0)]  # costes 0 / empresa gratis
def rnd(r):
    return dict(vol=r.choice([3, 10, 20, 35, 60, 80]) + r.random() * 3, dist=r.choice([0, 5, 30, 150, 600, 2000]) + r.random() * 20, empresa=r.choice([0, 300, 700, 1500, 4000]) + r.random() * 50,
                alqdia=r.choice([0, 60, 120]) + r.random() * 9, kmfurgo=r.choice([0, 0.15, 0.3]), extras=r.choice([0, 40, 150]), nayud=r.randint(0, 6), eurayud=r.choice([0, 10, 18]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(7); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeFurgo", "costeFurgoConReserva", "costeEmpresa", "m3Furgo", "m3Empresa", "viajes", "dias", "horasTuyas", "tipo", "horaEq", "kmEq"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
