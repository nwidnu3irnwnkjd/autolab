#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/comprar-o-alquilar-herramienta.js, escrito desde la especificacion (suma explicita por anios).
Uso: python3 ops/verif/comprar-o-alquilar-herramienta.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "comprar-o-alquilar-herramienta"
def oraculo(d):
    P, a, u, N, R, m, al, r = d["precio"], d["alq"], d["usos"], int(d["anios"]), d["reventa"] / 100.0 * d["precio"], d["mant"], d["alm"], d["tasa"] / 100.0
    v = 1.0 / (1 + r)
    A = sum(v ** t for t in range(1, N + 1))
    pvc = P + (m + al) * A - R * v ** N
    pva = u * a * A
    dif = pva - pvc
    # anios para amortizar: menor T con s*A(T) + R*v^T >= P (T continuo), s = ahorro anual neto de alquiler
    s = u * a - m - al
    def f(T):
        AT = T if r == 0 else (1 - v ** T) / r
        return s * AT + R * v ** T - P
    if P - R <= 0: pay = 0.0
    elif f(100) < 0: pay = -1.0
    else:
        lo, hi = 0.0, 100.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        pay = hi
    return {"pvCompra": pvc, "pvAlquiler": pva, "diferencia": dif,
            "costeUsoCompra": pvc / (u * A) if u > 0 else 0.0,
            "usosEqAnio": pvc / (a * A) if a > 0 else -1.0,
            "usosEqTotal": pvc / (a * A) * N if a > 0 else -1.0,
            "payback": pay, "ganador": 0 if dif > 1 else (1 if dif < -1 else 2)}
B = dict(precio=400, alq=45, usos=3, anios=8, reventa=25, mant=10, alm=15, tasa=0)
TESTS = [dict(B),                       # base: compra gana, equilibrio 1,39 usos/anio
         dict(B, usos=1),               # pocos usos: alquilar
         dict(B, alq=0),                # alquiler a coste 0
         dict(B, anios=1, usos=1),      # 1 anio de horizonte
         dict(B, tasa=5, reventa=0),    # con coste de oportunidad y sin reventa
         dict(B, usos=0)]               # 0 usos
def rnd(r):
    return dict(precio=r.choice([20, 150, 400, 1200, 5000]) + r.random() * 10, alq=r.choice([0, 15, 45, 120]) + r.random() * 5,
                usos=r.choice([0, 1, 2, 5, 12, 40]) + r.random(), anios=r.choice([1, 2, 5, 8, 15, 25]),
                reventa=r.choice([0, 15, 30, 60, 100]) + r.random(), mant=r.choice([0, 10, 60, 300]) + r.random() * 5,
                alm=r.choice([0, 15, 80]) + r.random() * 5, tasa=r.choice([0, 1, 3, 8, 15]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(53); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.02 if k in ("payback", "usosEqAnio", "usosEqTotal") else 1.0)
            if k in ("ganador",) and abs(oraculo(d)["diferencia"]) - 1 < 1e-6 and abs(oraculo(d)["diferencia"]) - 1 > -1e-6: continue
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["pvCompra", "pvAlquiler", "diferencia", "costeUsoCompra", "usosEqAnio", "usosEqTotal", "payback", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
