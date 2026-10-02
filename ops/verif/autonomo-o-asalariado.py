#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para autonomo-o-asalariado. Escrito desde la norma ANTES que el JS.
Normas: Orden PJC/297/2026 (arts. 2, 17, 18, 33; BOE-A-2026-7296); LGSS art. 308.1.c (BOE-A-2015-11724: rendimiento computable = neto + cuotas,
menos 7 % genericos); LIRPF arts. 19, 20, 30.2.4.a, 32.2.3.o, 57-58, 63, DA 61.a (BOE-A-2006-20764); RIRPF art. 30.2.a (5 %, max 2.000 EUR).
Escalas autonomicas: data/params.json irpf_2026 (contrastadas por el Verificador). Metodo del autonomo: punto fijo por enumeracion de cuotas candidatas
(distinto de la iteracion del JS). Uso: python3 ops/verif/autonomo-o-asalariado.py -> compara con el JS (osascript); sale 1 si hay diferencias > 1 EUR."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]
EST = [(0, .095), (12450, .12), (20200, .15), (35200, .185), (60000, .225), (300000, .245)]
DESC_E = [2400, 2700, 4000, 4500]
def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def minimo(n, c):
    if c is None: return 5550 + sum(DESC_E[min(i, 3)] for i in range(n))
    return c["contribuyente"] + sum(c["descendientes"][min(i, 3)] for i in range(n))
def cuota_base(bg, n, cc):
    d = IR["ccaa"][cc]; ea = [(lo, r / 100) for lo, r in d["escala_general"]]
    return max(0, esc(bg, EST) - esc(minimo(n, None), EST)) + max(0, esc(bg, ea) - esc(minimo(n, d["minimo"]), ea))
# ---- Seguridad Social ----
BMAX = 5101.20
def solid(r):  # cotizacion adicional de solidaridad mensual (art. 17): (empresa, trabajador)
    b1 = max(0, min(r, 5611.32) - BMAX); b2 = max(0, min(r, 7651.80) - 5611.32); b3 = max(0, r - 7651.80)
    return b1 * .0096 + b2 * .0104 + b3 * .0122, b1 * .0019 + b2 * .0021 + b3 * .0024
def asalariado_ss(bruto, indef):
    r = bruto / 12; base = min(r, BMAX)
    wt = .047 + (.0155 if indef else .016) + .001 + .0015
    et = .236 + (.055 if indef else .067) + .002 + .006 + .0075
    se, sw = solid(r)
    return 12 * (base * wt + sw), 12 * (base * et + se)
def da61(rit):
    if rit >= 20048.45: return 0.0
    return 590.89 if rit <= 17094 else 590.89 - 0.2 * (rit - 17094)
def red20(n):
    if n >= 19747.5: return 0.0
    if n <= 14852: return 7302.0
    if n <= 17673.52: return 7302 - 1.75 * (n - 14852)
    return max(0.0, 2364.34 - 1.14 * (n - 17673.52))
def irpf_asal(bruto, ssw, n, cc):
    neto = bruto - ssw; otros = min(2000, max(neto, 0)); rn = max(0, neto - otros - red20(neto))
    ci = cuota_base(rn, n, cc)
    return max(0.0, ci - min(da61(bruto), ci))
# ---- Autonomo ----
TABLA = [(670, 653.59), (900, 718.95), (1166.70 - 1e-9, 849.67), (1300, 950.98), (1500, 960.78), (1700, 960.78), (1850, 1143.79), (2030, 1209.15),
         (2330, 1274.51), (2760, 1356.21), (3190, 1437.91), (3620, 1519.61), (4050, 1601.31), (6000, 1732.03), (float("inf"), 1928.10)]
def base_min(R):
    for lim, b in TABLA:
        if R <= lim: return b
def cuota_reta(C):  # C = rendimiento computable anual antes del 7 %
    R = 0.93 * C / 12 if C > 0 else 0.0
    return 12 * base_min(R) * .315
def dj(N): return min(2000.0, .05 * max(N, 0))
def ss_aut(I, G):
    cands = sorted({12 * b * .315 for _, b in TABLA})
    for s in cands:
        N = I - G - s
        if abs(cuota_reta(I - G - dj(N)) - s) < 1e-9: return s
    return cands[-1]
def aut(I, G, n, cc):
    s = ss_aut(I, G); N = I - G - s; rn = N - dj(N); r3 = max(rn, 0)
    red = 0.0
    if 0 < r3 < 12000: red = min(1620.0 if r3 <= 8000 else 1620 - .405 * (r3 - 8000), r3)
    irpf = cuota_base(max(rn - red, 0), n, cc)
    return dict(ss=s, irpf=irpf, neto=I - G - s - irpf, base=s / 12 / .315)
def model(d):
    indef = d["contrato"] == "indef"; n = int(d["hijos"]); cc = d["ccaa"]
    ssw, sse = asalariado_ss(d["bruto"], indef); ir = irpf_asal(d["bruto"], ssw, n, cc); na = d["bruto"] - ssw - ir
    a = aut(d["factura"], d["gastos"], n, cc)
    # facturacion a partir de la cual el neto >= neto asalariado y ya no baja (ultimo punto por debajo en un barrido de 10 EUR, 10.000 EUR tras el primer cruce)
    G = d["gastos"]; I = float(int(max(0, na + G + 2400) // 10) * 10); first = None; last_below = None
    while I <= 2_000_000:
        ok = aut(I, G, n, cc)["neto"] >= na
        if ok and first is None: first = I
        if not ok: last_below = I
        if first is not None and I > first + 10000: break
        I += 10
    fe = None
    if first is not None:
        lo = last_below if last_below is not None else max(0, first - 10); hi = lo + 10
        if aut(hi, G, n, cc)["neto"] < na: hi = first
        for _ in range(60):
            m = (lo + hi) / 2
            if aut(m, G, n, cc)["neto"] >= na: hi = m
            else: lo = m
        fe = hi
    ac = aut(d["bruto"] + sse, G, n, cc)
    return dict(netoAsalariado=na, ssTrabajador=ssw, irpfAsalariado=ir, costeEmpresa=d["bruto"] + sse, netoAutonomo=a["neto"], cuotaReta=a["ss"],
                irpfAutonomo=a["irpf"], facturaIgual=fe, netoAutonomoAlCoste=ac["neto"])
B = dict(bruto=30000, factura=45000, gastos=3000, ccaa="madrid", hijos=0, contrato="indef")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto Madrid", V()), ("2 SMI justo 17.094", V(bruto=17094, factura=20000, gastos=1000, ccaa="andalucia")),
 ("3 bruto 19.000 con 2 hijos, temporal", V(bruto=19000, factura=25000, gastos=2000, ccaa="valencia", hijos=2, contrato="temp")),
 ("4 sobre base maxima: 80.000 Cataluna", V(bruto=80000, factura=120000, gastos=10000, ccaa="cataluna")),
 ("5 bruto 120.000 (solidaridad) Galicia", V(bruto=120000, factura=200000, gastos=20000, ccaa="galicia", hijos=3)),
 ("6 factura 0 y gastos 0", V(factura=0, gastos=0)),
 ("7 factura baja 9.000 (reduccion 32.2.3)", V(bruto=18000, factura=9000, gastos=500, ccaa="canarias")),
 ("8 factura en tramo 12 (>6.000/mes)", V(bruto=90000, factura=150000, gastos=15000, ccaa="baleares", hijos=1)),
 ("9 gastos > factura", V(factura=10000, gastos=15000, ccaa="murcia")),
 ("10 franja no monotona Madrid 40k con 46.000", V(bruto=40000, factura=46000, gastos=3000)),
 ("11 Valencia 25k con 17.060 (tabla reducida)", V(bruto=25000, factura=17060, gastos=2000, ccaa="valencia"))]
KEYS = ["netoAsalariado", "ssTrabajador", "irpfAsalariado", "costeEmpresa", "netoAutonomo", "cuotaReta", "irpfAutonomo", "facturaIgual", "netoAutonomoAlCoste"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/autonomo-o-asalariado.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(11); ca = list(IR["ccaa"])
    sweep = [dict(bruto=rnd.choice([17094, 18000, 22000, 30000, 45000, 62000, 90000, 140000]) * rnd.uniform(.9, 1.1), factura=rnd.uniform(0, 200000), gastos=rnd.choice([0, 1000, 3000, 8000, 20000]) * rnd.uniform(.5, 1.5),
                  ccaa=rnd.choice(ca), hijos=rnd.randint(0, 3), contrato=rnd.choice(["indef", "temp"])) for _ in range(520)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j[k], o[k]) for k in KEYS if (o[k] is None) != (j[k] is None) or (o[k] is not None and abs(j[k] - o[k]) > 1.0)]
        if i < len(CASES):
            print(CASES[i][0], {k: (round(o[k], 2) if o[k] is not None else None) for k in KEYS}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias > 1 EUR"); sys.exit(1 if bad else 0)
