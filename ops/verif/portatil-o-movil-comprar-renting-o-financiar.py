#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/portatil-o-movil-comprar-renting-o-financiar.js, escrito desde la especificacion.
Uso: python3 ops/verif/portatil-o-movil-comprar-renting-o-financiar.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "portatil-o-movil-comprar-renting-o-financiar"
def cuota_iter(L, tin, n):
    """Cuota por busqueda: la que deja saldo 0 tras n meses (distinto de la formula cerrada)."""
    i = tin / 1200.0
    if i == 0: return L / n
    lo, hi = 0.0, L * 2
    for _ in range(200):
        c = (lo + hi) / 2; s = L
        for _ in range(n): s = s * (1 + i) - c
        if s > 0: lo = c
        else: hi = c
    return (lo + hi) / 2
def tae(cuota, n, neto):
    """Tasa efectiva anual por secante sobre VAN(r)=0 con r anual."""
    if neto <= 0 or cuota <= 0: return None
    f = lambda r: sum(cuota / (1 + r) ** (m / 12.0) for m in range(1, n + 1)) - neto
    a, b = -0.5, 5.0
    for _ in range(300):
        c = (a + b) / 2
        if f(c) > 0: a = c
        else: b = c
    return (a + b) / 2 * 100
def oraculo(d):
    n = max(round(d["meses"]), 1); H = d["vida"]
    cont = d["precio"] * (1 - d["descuento"] / 100); rev = d["precio"] * d["reventa"] / 100; com = d["precio"] * d["comision"] / 100
    c = cuota_iter(d["precio"], d["tin"], n); fin = c * n + com; ren = d["renting"] * 12 * H
    cs = [cont - rev, fin - rev, ren]; best = cs.index(min(cs))
    otros = sorted(cs[:best] + cs[best + 1:])
    return {"costeContado": cs[0], "costeFinanciar": cs[1], "costeRenting": cs[2], "anoContado": cs[0] / H, "anoFinanciar": cs[1] / H, "anoRenting": cs[2] / H,
            "cuota": c, "comision": com, "sobrecosteFinanciar": fin - cont, "interesesYComision": fin - d["precio"],
            "tae": tae(c, n, d["precio"] - com), "taeConDescuento": tae(c, n, cont - com),
            "cuotaRentingEquilibrio": min(cs[0], cs[1]) / (12 * H), "mejor": best, "diferenciaSegundo": otros[0] - cs[best]}
B = dict(precio=900, descuento=5, tin=9, comision=0, meses=12, renting=45, reventa=20, vida=4)
TESTS = [dict(B),                                                 # contado gana, renting caro
         dict(B, renting=10),                                     # renting barato: gana renting
         dict(B, tin=0, comision=0, descuento=0),                 # borde: sin interes ni descuento, contado y financiar empatan
         dict(B, tin=0, descuento=8),                             # 0 % de interes con descuento perdido
         dict(B, vida=1, meses=6, tin=12, comision=2.5),          # 1 ano, comision
         dict(B, reventa=0, descuento=0, renting=0)]              # renting a 0, sin reventa
def rnd(r):
    vida = r.choice([1, 2, 3, 4, 5, 8]); return dict(precio=r.choice([100, 400, 900, 1500, 3000]) + r.random() * 20, descuento=r.choice([0, 0, 3, 5, 10]),
        tin=r.choice([0, 3, 9, 15, 22]) + r.random(), comision=r.choice([0, 0, 1, 2.5]), meses=r.randint(1, vida * 12), renting=r.choice([0, 10, 25, 45, 90]) + r.random() * 5,
        reventa=r.choice([0, 10, 20, 40]), vida=vida)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(11); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            jv = j[k]
            if v is None or jv is None:
                if v is not jv: bad += 1; print("DISCREPANCIA", d, k, jv, v)
                continue
            tol = 0.001 if k in ("tae", "taeConDescuento") else 0.01
            if abs(jv - v) > max(tol, 1e-6 * abs(v)): bad += 1; print("DISCREPANCIA", d, k, jv, v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeContado", "costeFinanciar", "costeRenting", "anoContado", "cuota", "sobrecosteFinanciar", "tae", "taeConDescuento", "cuotaRentingEquilibrio", "mejor"]
        cases = []
        for d in TESTS:
            o = oraculo(d); cases.append({"in": d, "expect": {k: round(o[k], 0 if k in ("sobrecosteFinanciar", "costeFinanciar") else 3) for k in keys if o[k] is not None}, "tol": 1})
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
