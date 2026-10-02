#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/coche-nuevo-o-seminuevo.js, escrito desde la especificacion con formas cerradas.
Uso: python3 ops/verif/coche-nuevo-o-seminuevo.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "coche-nuevo-o-seminuevo"
ENT, DEP, GAR, PB, PE, PT, CA = 0.20, 0.10, 3, 0.04, 0.03, 0.6, 1000.0

def interes_hasta(precio, tin, N, t):
    """Intereses pagados en los primeros t anios de un prestamo frances de precio*(1-ENT) a N anios."""
    L = precio * (1 - ENT)
    if tin <= 0 or L <= 0: return 0.0
    i = tin / 1200.0; n = 12 * N; m = 12 * t
    c = L * i / (1 - (1 + i) ** -n)
    bal = L * (1 + i) ** m - c * ((1 + i) ** m - 1) / i
    return m * c - (L - bal)

def averias(edad0, garantia, N):
    return sum(0.0 if t <= garantia else min(PT, PB + PE * (edad0 + t - 1)) * CA for t in range(1, N + 1))

def valor_nuevo(d, t): return d["pnuevo"] if t == 0 else d["pnuevo"] * (1 - d["dep1"] / 100) * (1 - DEP) ** (t - 1)
def valor_semi(d, t): return d["psemi"] * (1 - DEP) ** t

def acumulado(d, N, nuevo, psemi=None):
    """Coste acumulado hasta el anio N (lista 1..N) de una opcion."""
    if nuevo: P, V, g, e0, gar = d["pnuevo"], (lambda t: valor_nuevo(d, t)), d["gastos"], 0, GAR
    else:
        P = d["psemi"] if psemi is None else psemi
        V = (lambda t: P * (1 - DEP) ** t); g = d["gastos"] + d["extra"]; e0 = d["edad"]; gar = max(0, GAR - d["edad"])
    out = []
    for t in range(1, N + 1):
        out.append(P - V(t) + interes_hasta(P, d["tin"], N, t) + g * t + averias(e0, gar, t))
    return out

def oraculo(d):
    N = int(d["anos"])
    an, as_ = acumulado(d, N, True), acumulado(d, N, False)
    tn, ts = an[-1], as_[-1]
    dif = tn - ts
    s1 = (an[0] - as_[0]) > 0
    cruce = 0
    for t in range(2, N + 1):
        if ((an[t - 1] - as_[t - 1]) > 0) != s1: cruce = t; break
    a = acumulado(d, N, False, d["psemi"])[-1]; b = acumulado(d, N, False, d["psemi"] + 1000)[-1]
    slope = (b - a) / 1000.0
    return {"tcoNuevo": tn, "tcoSemi": ts,
            "perdidaNuevo": d["pnuevo"] - valor_nuevo(d, N), "perdidaSemi": d["psemi"] - valor_semi(d, N),
            "interesesNuevo": interes_hasta(d["pnuevo"], d["tin"], N, N), "interesesSemi": interes_hasta(d["psemi"], d["tin"], N, N),
            "gastosNuevo": d["gastos"] * N, "gastosSemi": (d["gastos"] + d["extra"]) * N,
            "averiasNuevo": averias(0, GAR, N), "averiasSemi": averias(d["edad"], max(0, GAR - d["edad"]), N),
            "residualNuevo": valor_nuevo(d, N), "residualSemi": valor_semi(d, N),
            "diferencia": dif, "ganador": 0 if dif > 0.5 else (1 if dif < -0.5 else 2), "cruce": cruce,
            "precioEquilibrio": d["psemi"] + dif / slope}

B = dict(pnuevo=25000, psemi=17500, edad=3, anos=5, dep1=18, gastos=1000, extra=300, tin=0)
TESTS = [dict(B),                                   # base, contado, a 5 anios
         dict(B, tin=6.5),                          # con financiacion
         dict(B, anos=1),                           # horizonte 1 anio
         dict(B, anos=10, edad=6, extra=600),       # horizonte largo, seminuevo viejo: el nuevo alcanza
         dict(B, gastos=0, extra=0, tin=0),         # gastos 0
         dict(B, psemi=24000, edad=0, anos=3)]      # seminuevo casi nuevo
def rnd(r):
    pn = r.choice([12000, 20000, 25000, 40000, 60000]) + r.random() * 3000
    return dict(pnuevo=pn, psemi=pn * r.uniform(0.4, 0.95), edad=r.choice([0, 1, 2, 3, 4, 6, 8]), anos=r.randint(1, 10),
                dep1=r.choice([0, 10, 18, 25, 35]) + r.random(), gastos=r.choice([0, 600, 1000, 1800]) + r.random() * 50,
                extra=r.choice([0, 150, 300, 800]) + r.random() * 50, tin=r.choice([0, 0, 3, 6.5, 9, 14]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(1.0 if k not in ("ganador", "cruce") else 0, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["tcoNuevo", "tcoSemi", "perdidaNuevo", "perdidaSemi", "interesesNuevo", "interesesSemi", "averiasNuevo", "averiasSemi", "residualNuevo", "residualSemi", "diferencia", "ganador", "cruce", "precioEquilibrio"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
