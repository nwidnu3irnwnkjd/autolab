#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para autonomo-o-sociedad-limitada. Escrito desde la norma ANTES que el JS.
Normas (BOE, consultadas 2/10/2026): LIS Ley 27/2014 art. 29.1 y DT 44.a (2026: micro <1 M EUR 19 % hasta 50.000 y 21 % resto; reducida dimension 23 %; nueva creacion 15 %);
LIRPF arts. 17.2.e, 19.2.a/f, 20 (sin otras rentas > 6.500), 25.1.a, 49, 56.2, 63, 66, 76 (escala del ahorro; el minimo no absorbido por la base general pasa a la del ahorro);
LGSS 305.2.b y 308.1.a regla 4.a / 308.1.c reglas 1.a y 2.a (societario: rendimientos de trabajo + dividendos, deduccion 3 %, base minima grupo 7 = 1.424,40);
Orden PJC/297/2026 arts. 3 y 18; autonomo individual: mismo modelo que ops/verif/autonomo-o-asalariado.py (RETA 31,5 %, 7 %, 5 % dificil justificacion, 32.2.3.o).
Uso: python3 ops/verif/autonomo-o-sociedad-limitada.py -> compara con el JS (osascript); sale 1 si hay diferencias > 1 EUR."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]
EST = [(0, .095), (12450, .12), (20200, .15), (35200, .185), (60000, .225), (300000, .245)]
AH = [(0, .095), (6000, .105), (50000, .115), (200000, .135), (300000, .15)]  # cada mitad (estatal y autonomica)
def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def minimos(cc):
    d = IR["ccaa"][cc]
    return 5550.0, (d["minimo"]["contribuyente"] if d["minimo"] else 5550.0)
def irpf_total(blg, bla, cc):
    """Cuota integra estatal+autonomica: general con el minimo y el exceso del minimo sobre la general a la escala del ahorro (arts. 56.2, 63, 66, 76)."""
    d = IR["ccaa"][cc]; ea = [(lo, r / 100) for lo, r in d["escala_general"]]; mE, mC = minimos(cc)
    tot = 0.0
    for scg, m in ((EST, mE), (ea, mC)):
        gen = max(0.0, esc(blg, scg) - esc(min(blg, m), scg))
        resto = max(0.0, m - blg)               # minimo no absorbido por la base general
        aho = max(0.0, esc(bla, AH) - esc(min(bla, resto), AH))
        tot += gen + aho
    return tot
# ---- RETA (tabla 2026, Orden PJC/297/2026 art. 18) ----
TABLA = [(670, 653.59), (900, 718.95), (1166.70 - 1e-9, 849.67), (1300, 950.98), (1500, 960.78), (1700, 960.78), (1850, 1143.79), (2030, 1209.15),
         (2330, 1274.51), (2760, 1356.21), (3190, 1437.91), (3620, 1519.61), (4050, 1601.31), (6000, 1732.03), (float("inf"), 1928.10)]
def base_min(R):
    for lim, b in TABLA:
        if R <= lim: return b
def cuota_reta_aut(C):
    R = 0.93 * C / 12 if C > 0 else 0.0
    return 12 * base_min(R) * .315
def dj(N): return min(2000.0, .05 * max(N, 0))
def ss_aut(I):
    cands = sorted({12 * b * .315 for _, b in TABLA})
    for s in cands:
        if abs(cuota_reta_aut(I - dj(I - s)) - s) < 1e-9: return s
    return cands[-1]
def aut(I, cc):
    s = ss_aut(I); N = I - s; rn = N - dj(N); r3 = max(rn, 0); red = 0.0
    if 0 < r3 < 12000: red = min(1620.0 if r3 <= 8000 else 1620 - .405 * (r3 - 8000), r3)
    irpf = irpf_total(max(rn - red, 0), 0.0, cc)
    return dict(ss=s, irpf=irpf, neto=I - s - irpf)
def red20(n):
    if n >= 19747.5: return 0.0
    if n <= 14852: return 7302.0
    if n <= 17673.52: return 7302 - 1.75 * (n - 14852)
    return max(0.0, 2364.34 - 1.14 * (n - 17673.52))
def impuesto_sociedades(base, tipo):
    if base <= 0: return 0.0
    if tipo == "nueva": return .15 * base
    if tipo == "reducida": return .23 * base
    return .19 * min(base, 50000) + .21 * max(base - 50000, 0)      # micro
def sl(R, S, p, cc, tipo, C):
    Sx = min(S, max(R - C, 0.0)); base = R - Sx - C
    isoc = impuesto_sociedades(base, tipo); U = base - isoc
    D = p * max(U, 0.0); ret = max(U, 0.0) - D
    comp = (Sx + D) * 0.97                      # 3 % para socio con control (LGSS 308.1.c regla 2.a)
    R_m = comp / 12 if comp > 0 else 0.0
    cuota = 12 * max(base_min(R_m), 1424.40) * .315
    nt = max(0.0, Sx - cuota)                   # rendimiento neto del trabajo tras 19.2.a
    otros = min(2000.0, nt)
    red = red20(nt) if D <= 6500 else 0.0
    blg = max(0.0, nt - otros - red)
    irpf = irpf_total(blg, D, cc)
    return dict(Sx=Sx, base=base, isoc=isoc, U=U, D=D, ret=ret, cuota=cuota, irpf=irpf, neto=Sx + D - cuota - irpf)
def equilibrio(S, p, cc, tipo, C, paso=100, tope=400000):
    f = lambda R: sl(R, S, p, cc, tipo, C)["neto"] - aut(R, cc)["neto"]
    R = 0.0; last_below = None
    while R <= tope:
        if f(R) < 0: last_below = R
        R += paso
    if last_below is None: return 0.0
    lo, hi = last_below, last_below + paso
    if f(hi) < 0: return None
    for _ in range(60):
        m = (lo + hi) / 2
        if f(m) >= 0: hi = m
        else: lo = m
    return hi
def model(d, be=True):
    a = aut(d["benef"], d["ccaa"]); s = sl(d["benef"], d["retrib"], d["pct"] / 100, d["ccaa"], d["tipo"], d["costes"])
    return dict(netoAut=a["neto"], ssAut=a["ss"], irpfAut=a["irpf"], netoSL=s["neto"], isoc=s["isoc"], dividendos=s["D"], retenido=s["ret"], cuotaSL=s["cuota"],
                irpfSL=s["irpf"], retribEf=s["Sx"],
                equilibrio=(equilibrio(d["retrib"], d["pct"] / 100, d["ccaa"], d["tipo"], d["costes"]) if be else "skip"),
                equilibrio100=(equilibrio(d["retrib"], 1.0 if d["pct"] < 100 else d["pct"] / 100, d["ccaa"], d["tipo"], d["costes"]) if be else "skip"))
B = dict(benef=60000, retrib=24000, pct=50, ccaa="madrid", tipo="micro", costes=1800)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto Madrid 60.000", V()), ("2 beneficio 0", V(benef=0, retrib=0, costes=0)), ("3 perdida por costes: 1.000 con costes 1.800", V(benef=1000, retrib=0, pct=100)),
 ("4 dividendos 0 %", V(pct=0)), ("5 dividendos 100 %", V(pct=100)), ("6 nueva creacion 15 %", V(tipo="nueva")), ("7 micro sobre 50.000 de base", V(benef=120000, retrib=30000)),
 ("8 retribucion = beneficio - costes", V(benef=40000, retrib=38200, pct=100)), ("9 retribucion > beneficio (tope)", V(benef=30000, retrib=50000)),
 ("10 reducida dimension 23 %", V(benef=200000, retrib=40000, tipo="reducida", ccaa="cataluna")), ("11 dividendos > 6.500 y sueldo bajo (art. 20)", V(benef=80000, retrib=12000, pct=100, ccaa="galicia")),
 ("12 sueldo 0 y dividendos 100 %", V(benef=50000, retrib=0, pct=100, ccaa="valencia"))]
KEYS = ["netoAut", "ssAut", "irpfAut", "netoSL", "isoc", "dividendos", "retenido", "cuotaSL", "irpfSL", "retribEf", "equilibrio", "equilibrio100"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/autonomo-o-sociedad-limitada.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(23); ca = list(IR["ccaa"])
    sweep = [dict(benef=rnd.choice([0, 5000, 12000, 25000, 40000, 60000, 90000, 150000, 300000]) * rnd.uniform(.5, 1.5), retrib=rnd.choice([0, 0, 12000, 20000, 30000, 50000, 80000]) * rnd.uniform(.5, 1.5),
                  pct=rnd.choice([0, 25, 50, 75, 100, rnd.uniform(0, 100)]), ccaa=rnd.choice(ca), tipo=rnd.choice(["nueva", "micro", "micro", "reducida"]),
                  costes=rnd.choice([0, 800, 1800, 3000, 6000])) for _ in range(560)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0; nbe = 0
    for i, c in enumerate(allc):
        be = i < len(CASES) or i < len(CASES) + 90
        o = model(c, be); j = jr[i]
        diffs = []
        for k in KEYS:
            if o[k] == "skip": continue
            if k.startswith("equilibrio"): nbe += 1
            if (o[k] is None) != (j[k] is None) or (o[k] is not None and abs(j[k] - o[k]) > 1.0): diffs.append((k, j[k], o[k]))
        if i < len(CASES): print(CASES[i][0], {k: (round(o[k], 2) if isinstance(o[k], float) else o[k]) for k in KEYS}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos ({nbe} equilibrios comparados): {bad} casos con discrepancias > 1 EUR"); sys.exit(1 if bad else 0)
