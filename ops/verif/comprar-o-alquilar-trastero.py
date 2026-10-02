#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/comprar-o-alquilar-trastero.js, escrito desde la especificacion con tabla anual explicita (flujos por anio).
Uso: python3 ops/verif/comprar-o-alquilar-trastero.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "comprar-o-alquilar-trastero"
def tabla(d, T):
    """Devuelve (coste compra acumulado, coste alquiler acumulado) a T anios, en euros de hoy, con flujos al final de cada anio."""
    r = d["tasa"] / 100.0; c = d["precio"] * (1 + d["gastosPct"] / 100.0); a = 0.0; cuota = 12 * d["alq"]
    for t in range(1, T + 1):
        f = (1 + r) ** -t
        c += d["costes"] * f
        a += cuota * f
        cuota *= 1 + d["subida"] / 100.0
    c -= d["precio"] * (1 + d["reval"] / 100.0) ** T * (1 + r) ** -T
    return c, a
def oraculo(d):
    N = int(d["anios"]); c, a = tabla(d, N); dif = a - c
    # anio de equilibrio: ultimo anio (1..40) con alquiler < compra, mas 1; -1 si el 40 aun no compensa; 1 si compensa siempre
    neg = [T for T in range(1, 41) if tabla(d, T)[1] - tabla(d, T)[0] < 0]
    eq = 1 if not neg else (-1 if max(neg) == 40 else max(neg) + 1)
    # alquiler de equilibrio: cuota mensual que iguala a N anios (alquiler proporcional a la cuota)
    r = d["tasa"] / 100.0; fac = sum((1 + d["subida"] / 100.0) ** (t - 1) * (1 + r) ** -t for t in range(1, N + 1))
    return {"pvCompra": c, "pvAlquiler": a, "diferencia": dif, "valorResidual": d["precio"] * (1 + d["reval"] / 100.0) ** N,
            "desembolso": d["precio"] * (1 + d["gastosPct"] / 100.0), "anioEq": eq, "alqEq": c / (12 * fac),
            "ganador": 0 if dif > 1 else (1 if dif < -1 else 2)}
B = dict(precio=9000, gastosPct=10, costes=250, alq=70, subida=3, anios=10, reval=1, tasa=2)
TESTS = [dict(B),                          # base
         dict(B, alq=30),                  # alquiler barato: alquilar
         dict(B, anios=1),                 # 1 anio
         dict(B, costes=0, tasa=0),        # coste 0 y sin oportunidad
         dict(B, alq=0),                   # alquiler 0
         dict(B, reval=-3, anios=25)]      # revalorizacion negativa, horizonte largo
def rnd(r):
    return dict(precio=r.choice([1500, 5000, 9000, 20000]) + r.random() * 100, gastosPct=r.choice([0, 5, 10, 15]) + r.random(),
                costes=r.choice([0, 100, 250, 600]) + r.random() * 10, alq=r.choice([0, 25, 70, 150]) + r.random() * 5,
                subida=r.choice([0, 2, 5, 10]) + r.random(), anios=r.choice([1, 2, 5, 10, 20, 40]),
                reval=r.choice([-5, -1, 0, 2, 5, 10]) + r.random(), tasa=r.choice([0, 1, 3, 8, 15]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(77); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            tol = 0 if k in ("ganador", "anioEq") else (0.02 if k == "alqEq" else 1.0)
            if k == "ganador" and abs(abs(o["diferencia"]) - 1) < 1e-6: continue
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["pvCompra", "pvAlquiler", "diferencia", "valorResidual", "anioEq", "alqEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
