#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/hipoteca-mas-entrada-o-conservar-ahorros.js, escrito desde la especificacion
y por simulacion mes a mes (el JS usa formulas cerradas). Uso: python3 ops/verif/hipoteca-mas-entrada-o-conservar-ahorros.py [--write-tests]
(barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "hipoteca-mas-entrada-o-conservar-ahorros"
def cuota(P, i, n):
    if P <= 0: return 0.0
    return P / n if i == 0 else P * i / (1 - (1 + i) ** (-n))
def simula(P, i, c, m):
    """Devuelve (saldo, intereses pagados) tras m cuotas, mes a mes."""
    s, it = P, 0.0
    for _ in range(m):
        inte = s * i; it += inte; s = s + inte - c
    return max(s, 0.0), it
def wealth(d, rent, k):
    """(patrimonio A, patrimonio B) tras k meses, simulando mes a mes. A reinvierte la cuota que se ahorra respecto a B."""
    n = round(d["plazo"] * 12)
    iB, iA = d["tin"] / 1200.0, max(d["tin"] - d["baja"], 0) / 1200.0
    j = (1 + rent / 100.0) ** (1 / 12.0) - 1
    CA, E = d["capital"] - d["extra"], d["extra"]; cA, cB = cuota(CA, iA, n), cuota(d["capital"], iB, n)
    sa, sb, fa, fb = CA, d["capital"], 0.0, E
    for _ in range(k):
        sa = sa * (1 + iA) - cA; sb = sb * (1 + iB) - cB; fa = fa * (1 + j) + (cB - cA); fb = fb * (1 + j)
    return fa - max(sa, 0), fb - max(sb, 0), fa, fb, max(sa, 0), max(sb, 0)
def oraculo(d):
    n, m = round(d["plazo"] * 12), round(d["anos"] * 12)
    iB, iA = d["tin"] / 1200.0, max(d["tin"] - d["baja"], 0) / 1200.0
    CA, E = d["capital"] - d["extra"], d["extra"]; cA, cB = cuota(CA, iA, n), cuota(d["capital"], iB, n)
    pa, pb, fa, fb, sA, sB = wealth(d, d["rent"], m)
    df = pa - pb
    tipo = 2 if abs(df) < 0.05 * E else (0 if df > 0 else 1)
    f = lambda r: (lambda w: w[0] - w[1])(wealth(d, r, m))
    if f(-20) <= 0: rent_eq = -999
    elif f(20) >= 0: rent_eq = 999
    else:
        # cuadricula gruesa + refinado (independiente de la biseccion del JS)
        r0 = -20.0
        while f(r0 + 1) > 0: r0 += 1
        lo, hi = r0, r0 + 1
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
        rent_eq = (lo + hi) / 2
    sg = lambda x: 1 if x > 0.005 else (-1 if x < -0.005 else 0)
    sN = sg(df); mes = 0
    if sN != 0:
        for k in range(1, m + 1):
            w = wealth(d, d["rent"], k)
            if sg(w[0] - w[1]) != sN: mes = k + 1
    return {"capitalA": CA, "cuotaA": cA, "cuotaB": cB, "ahorroCuota": cB - cA, "saldoA": sA, "saldoB": sB, "ahorroA": fa, "valorAhorro": fb,
            "patrimonioA": pa, "patrimonioB": pb, "dif": df, "interesesA": cA * m - (CA - sA), "interesesB": cB * m - (d["capital"] - sB),
            "rentEq": rent_eq, "mesEq": mes, "tipo": tipo, "cubreCuotas": E / cB}
B = dict(capital=150000, extra=30000, tin=2.76, baja=0, plazo=25, anos=10, rent=2)
TESTS = [dict(B),                                  # aportar gana (rent 2 % < TIN 2,76 %)
         dict(B, rent=5),                          # conservar gana
         dict(B, rent=2.8, anos=5),                # casi empate
         dict(B, baja=0.4, rent=3),                # la bajada de tipo inclina hacia aportar
         dict(B, tin=0, rent=0),                   # tipo 0 %: empate
         dict(B, extra=149000, anos=25, plazo=25)] # borde: entrada casi igual al capital, horizonte = plazo
def rnd(r):
    plazo = r.choice([10, 15, 20, 25, 30, 35, 40]); cap = r.choice([50000, 100000, 150000, 250000, 400000]) + r.random() * 1000
    return dict(capital=cap, extra=cap * r.choice([0.02, 0.1, 0.25, 0.5, 0.9]), tin=r.choice([0, 1, 2.76, 4, 7]) + r.random() * 0.3,
                baja=r.choice([0, 0, 0.25, 0.5, 3]), plazo=plazo, anos=r.randint(1, plazo), rent=r.choice([-3, 0, 1.5, 2, 3.5, 6, 12]) + r.random() * 0.4)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(23); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01 if k != "rentEq" else 1e-5, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    for d in ins:  # la frase "aportar gana mientras tu ahorro rinda menos de rentEq" debe cumplirse (monotonia)
        o = oraculo(d)
        if o["tipo"] != 2 and abs(o["rentEq"]) < 900 and (o["tipo"] == 0) != (d["rent"] < o["rentEq"]):
            bad += 1; print("INCONSISTENCIA rentEq/tipo", d, o["rentEq"], o["tipo"])
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["capitalA", "cuotaA", "cuotaB", "saldoA", "saldoB", "ahorroA", "valorAhorro", "patrimonioA", "patrimonioB", "dif", "interesesA", "interesesB", "rentEq", "mesEq", "tipo"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
