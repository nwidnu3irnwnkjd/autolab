#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para retribucion-flexible-me-conviene. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado 30/09/2026; LIRPF BOE-A-2006-20764 arts. 19, 20, 42, 63, 74, 81 y DA 61.ª; RIRPF BOE-A-2007-6820 arts. 45, 46, 46 bis; LGSS BOE-A-2015-11724 art. 147; ET BOE-A-2015-11430 art. 26.1):
1. Sin retribucion flexible (A): cobras S en dinero, cotizas y tributas por S y pagas tu el producto (coste C, ya tributado). Con ella (B): cobras S-X en dinero y la empresa te da el producto en especie (valorado X); neto B = S - X - SS - IRPF_B.
2. Cotizacion: la base es la «remuneracion total, en metalico o en especie» (art. 147.1) y la lista de excluidos del 147.2 es cerrada («unicamente») y no incluye seguro, comida, transporte ni guarderia: la SS de B es la de A (base S).
3. IRPF: lo exento (art. 42.3) no es rendimiento integro: ingresos = S - exento; SS deducible = la de S; gastos 2.000 (art. 19.2.f) y reduccion art. 20 sobre (ingresos - SS); cuota = escala(base) - escala(minimo) estatal + autonomica (arts. 63, 74); DA 61.ª sobre los ingresos integros.
4. Exento por producto: seguro de enfermedad min(X, 500 por persona o 1.500 si discapacidad) (42.3.c, RIRPF 46); comida min(X, 11 EUR x dias habiles) por formula indirecta (42.3.a, RIRPF 45.2); transporte min(X, 1.500) (42.3.e, RIRPF 46 bis; 136,36/mes no binds con reparto en 12); guarderia 1.er ciclo infantil sin tope (42.3.b); otro producto: 0. Lo que excede es especie tributable igual que el dinero.
5. Limite laboral (ET 26.1): el salario en especie no supera el 30 % de las percepciones salariales (S) ni deja el dinero por debajo del SMI anual (17.094 EUR en jornada completa): maxX = max(0, min(0,30 S, S - 17.094)). Si X > maxX la opcion no es posible.
6. Ahorro neto = (C - X) + (IRPF_A - IRPF_B). Guarderia: ceder C-1.000 conserva el incremento (ahorroAlt = solo IRPF de esa parte; el resto lo pagas tu). El 30 % de ET 26.1 cuenta tambien la especie ya cobrada (no modelado, declarado). El incremento de 1.000 EUR de la deduccion por maternidad (art. 81.2) no cuenta gastos exentos por 42.3.b/d: perdida = min(1000,C) - min(1000, max(0, C - exento)).
7. Veredicto: umbral 5 % de C (empate practico). Escenario 1 exencion total; 2 exencion parcial; 3 no conviene o empate (incluye sin exencion); 5 sin exencion pero ganas por precio; 4 no permitido por el 30 %/SMI; 0 bloqueado (foral o datos invalidos).
Uso: python3 ops/verif/retribucion-flexible-me-conviene_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARS = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))
PAR = PARS["irpf_2026"]
SOL = PARS["autonomo_2026"]["general"]["solidaridad_mes"]
SCALE_EST = [(0, 9.5), (12450, 12), (20200, 15), (35200, 18.5), (60000, 22.5), (300000, 24.5)]
def scale(x, esc):
    t = 0.0
    for i, (lo, r) in enumerate(esc):
        hi = esc[i + 1][0] if i + 1 < len(esc) else float("inf")
        if x > lo: t += (min(x, hi) - lo) * r / 100
    return t
def art20(n):
    if n <= 14852: return 7302.0
    if n <= 17673.52: return 7302 - 1.75 * (n - 14852)
    if n < 19747.5: return 2364.34 - 1.14 * (n - 17673.52)
    return 0.0
def ss(S):
    r = S / 12; t = min(r, 5101.2) * 0.065
    for lo, hi, _e, w in SOL:
        t += max(0.0, min(r, hi if hi is not None else float("inf")) - lo) * w / 100
    return 12 * t
def irpf(ingresos, cot, cc):
    neto = ingresos - cot
    g = min(2000, max(neto, 0))
    base = max(0.0, neto - g - art20(neto))
    c = PAR["ccaa"][cc]
    mn_a = (c["minimo"] or {"contribuyente": 5550})["contribuyente"]
    ci = max(0.0, scale(base, SCALE_EST) - scale(5550, SCALE_EST)) + max(0.0, scale(base, [tuple(x) for x in c["escala_general"]]) - scale(mn_a, [tuple(x) for x in c["escala_general"]]))
    da = 0.0
    if ingresos < 20048.45: da = 590.89 if ingresos <= 17094 else 590.89 - 0.2 * (ingresos - 17094)
    return ci - min(da, ci)
def neto_sin_producto(S, cc): return S - ss(S) - irpf(S, ss(S), cc)
KEYS = ["bloqueado", "escenario", "exento", "cap", "maxX", "permitido", "ss", "irpfA", "irpfB", "ahorroIRPF", "netoA", "netoB", "ahorroNeto", "brutoEq", "tipoEf", "perdidaMat", "ahorroTrasMat", "ahorroAlt", "ganNum"]
def model(d):
    S, cc, prod, C, X = d["bruto"], d["ccaa"], d["producto"], d["coste"], d["sustituir"]
    n = int(max(1, min(8, d["personas"]))); m = int(max(0, min(n, d["discap"]))); D = max(0, min(260, d["dias"]))
    z = dict.fromkeys(KEYS, 0.0)
    if cc == "foral" or S <= 0 or X <= 0 or C < 0:
        z["bloqueado"] = 1; return z
    cap = {"seguro": 500 * (n - m) + 1500 * m, "comida": 11 * D, "transporte": 1500, "guarderia": float("inf"), "otro": 0}[prod]
    exento = min(X, cap)
    maxX = max(0.0, min(0.3 * S, S - 17094))
    permitido = 1 if X <= maxX + 1e-9 else 0
    cot = ss(S); iA = irpf(S, cot, cc); iB = irpf(S - exento, cot, cc)
    nA = S - cot - iA - C; nB = S - X - cot - iB
    ah = nB - nA
    # bruto adicional que costearia el producto por tu cuenta
    base0 = neto_sin_producto(S, cc); lo, hi = 0.0, 1e7
    if C > 0:
        for _ in range(200):
            mid = (lo + hi) / 2
            if neto_sin_producto(S + mid, cc) - base0 >= C: hi = mid
            else: lo = mid
        beq = hi
    else: beq = 0.0
    perd = (min(1000, C) - min(1000, max(0.0, C - exento))) if prod == "guarderia" else 0.0
    alt = (iA - irpf(S - (C - 1000), cot, cc)) if (prod == "guarderia" and C > 1000) else 0.0
    thr = 0.05 * C
    gan = 1 if ah >= thr and ah > 0 else (2 if ah <= -thr and ah < 0 else 0)
    if gan == 0 and thr == 0 and ah == 0: gan = 0
    if not permitido: esc = 4
    elif gan == 1: esc = 5 if exento <= 0 else (1 if exento >= X - 1e-9 else 2)
    else: esc = 3
    return dict(bloqueado=0, escenario=esc, exento=exento, cap=(cap if cap != float("inf") else -1), maxX=maxX, permitido=permitido, ss=cot, irpfA=iA, irpfB=iB, ahorroIRPF=iA - iB, netoA=nA, netoB=nB,
                ahorroNeto=ah, brutoEq=beq, tipoEf=((iA - iB) / exento * 100 if exento > 0 else 0.0), perdidaMat=perd, ahorroTrasMat=ah - perd, ahorroAlt=alt, ganNum=gan)
B = dict(bruto=30000, ccaa="madrid", producto="seguro", coste=600, sustituir=600, personas=1, discap=0, dias=220)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto seguro 600/600 Madrid", V()),
 ("2 seguro: borde 500 exacto", V(coste=500, sustituir=500)),
 ("3 seguro: borde 501", V(coste=501, sustituir=501)),
 ("4 seguro 3 personas, 1 con discapacidad, 2.500", V(personas=3, discap=1, coste=2500, sustituir=2500)),
 ("5 seguro: 1 persona discapacidad 1.500/1.501", V(personas=1, discap=1, coste=1501, sustituir=1501)),
 ("6 comida 11 EUR/dia x 220 = 2.420 exacto", V(producto="comida", coste=2420, sustituir=2420)),
 ("7 comida 2.421", V(producto="comida", coste=2421, sustituir=2421)),
 ("8 transporte 1.500", V(producto="transporte", coste=1500, sustituir=1500)),
 ("9 transporte 1.501", V(producto="transporte", coste=1501, sustituir=1501)),
 ("10 guarderia 3.000 sin tope", V(producto="guarderia", coste=3000, sustituir=3000)),
 ("11 otro producto sin exencion", V(producto="otro", coste=600, sustituir=600)),
 ("12 otro producto con mejor precio", V(producto="otro", coste=800, sustituir=600)),
 ("13 limite 30 %: 9.000 de 30.000", V(producto="guarderia", coste=9000, sustituir=9000)),
 ("14 limite 30 %: 9.001", V(producto="guarderia", coste=9001, sustituir=9001)),
 ("15 limite SMI: bruto 20.000 X 2.906 / 2.907", V(bruto=20000, producto="guarderia", coste=2906, sustituir=2906)),
 ("16 limite SMI 2.907", V(bruto=20000, producto="guarderia", coste=2907, sustituir=2907)),
 ("17 bruto 17.094 (sin margen)", V(bruto=17094, producto="seguro")),
 ("18 foral bloqueado", V(ccaa="foral")),
 ("19 bruto alto 90.000 Cataluna", V(bruto=90000, ccaa="cataluna", producto="transporte", coste=1500, sustituir=1500)),
 ("20 sustituir mas que el coste", V(coste=300, sustituir=500)),
 ("21 coste 0", V(coste=0, sustituir=500))]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/retribucion-flexible-me-conviene.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(38)
    ccs = list(PAR["ccaa"].keys()) + ["foral"]
    def mk():
        S = rnd.choice([rnd.uniform(14000, 25000), rnd.uniform(18000, 60000), rnd.uniform(20000, 150000), 17094, 20048.45, 35200])
        p = rnd.choice(["seguro", "comida", "transporte", "guarderia", "otro"])
        cx = rnd.choice([rnd.uniform(100, 4000), 500, 1500, 2420, 600, rnd.uniform(0.2, 0.35) * S])
        return dict(bruto=S, ccaa=rnd.choice(ccs), producto=p, coste=rnd.choice([cx, cx * rnd.uniform(0.7, 1.4)]), sustituir=cx, personas=rnd.randint(1, 5), discap=rnd.randint(0, 3), dias=rnd.choice([220, 100, rnd.randint(0, 260)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > (0.005 if k == "tipoEf" else 0.5)]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("exento", "ahorroIRPF", "ahorroNeto", "escenario")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
