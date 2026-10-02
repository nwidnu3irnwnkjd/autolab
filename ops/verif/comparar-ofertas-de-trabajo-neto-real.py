#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para comparar-ofertas-de-trabajo-neto-real. Escrito desde la norma ANTES que el JS.
Normas: Orden PJC/297/2026 arts. 2, 17, 18 y 33 (BOE-A-2026-7296): base maxima 5.101,20 EUR/mes, tipos del trabajador 4,70 CC + 1,55 desempleo (indef.) o 1,60 (temporal... aqui solo
indefinido) + 0,10 FP + 0,15 MEI = 6,50 %, y cotizacion adicional de solidaridad (art. 17) sobre la parte del sueldo mensual por encima de la base maxima;
LIRPF (BOE-A-2006-20764): art. 19.2.a (cotizaciones), 19.2.f (2.000 EUR), art. 20 (reduccion; umbral sobre ingresos menos cotizaciones), arts. 57-58 (minimos), 63 y 74 (escalas), DA 61.a (590,89 EUR);
escalas autonomicas y minimos: data/params.json irpf_2026. Horas/ano: ET art. 38.1 (30 dias naturales de vacaciones, minimo) y art. 37.2 (14 fiestas, maximo).
Uso: python3 ops/verif/comparar-ofertas-de-trabajo-neto-real.py -> compara con el JS (osascript); sale 1 si hay diferencias > 1 EUR."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]
EST = [(0, .095), (12450, .12), (20200, .15), (35200, .185), (60000, .225), (300000, .245)]
def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def minimo(c):  # solo minimo del contribuyente (sin hijos)
    return 5550.0 if c is None else c["contribuyente"]
def cuota(base, cc):
    d = IR["ccaa"][cc]; ea = [(lo, r / 100) for lo, r in d["escala_general"]]
    return max(0.0, esc(base, EST) - esc(minimo(None), EST)) + max(0.0, esc(base, ea) - esc(minimo(d["minimo"]), ea))
BMAX = 5101.20
def ss_trab(bruto):
    r = bruto / 12; base = min(r, BMAX)
    s = max(0, min(r, 5611.32) - BMAX) * .0019 + max(0, min(r, 7651.80) - 5611.32) * .0021 + max(0, r - 7651.80) * .0024
    return 12 * (base * (.047 + .0155 + .001 + .0015) + s)
def red20(n):
    if n >= 19747.5: return 0.0
    if n <= 14852: return 7302.0
    if n <= 17673.52: return 7302 - 1.75 * (n - 14852)
    return max(0.0, 2364.34 - 1.14 * (n - 17673.52))
def da61(b):
    if b >= 20048.45: return 0.0
    return 590.89 if b <= 17094 else 590.89 - 0.2 * (b - 17094)
def irpf(bruto, cc):
    ss = ss_trab(bruto); n = bruto - ss
    rn = max(0.0, n - min(2000.0, max(n, 0)) - red20(n))
    ci = cuota(rn, cc)
    return max(0.0, ci - min(da61(bruto), ci))
def neto(bruto, cc): return bruto - ss_trab(bruto) - irpf(bruto, cc)
SEM = 365 / 7 - 30 / 7 - 14 / 5   # semanas laborables efectivas: ET 38.1 (30 d naturales) y 37.2 (14 fiestas)
def bruto_igual(T, cc):
    lo, hi = 0.0, 1e7
    if neto(0, cc) >= T: return 0.0
    for _ in range(100):
        m = (lo + hi) / 2
        if neto(m, cc) >= T: hi = m
        else: lo = m
    return hi
def model(d):
    cc = d["ccaa"]; r = {}
    for k in "AB":
        b = d["bruto" + k]; n = neto(b, cc); t = n - d["despl" + k]
        r["ss" + k] = ss_trab(b); r["irpf" + k] = irpf(b, cc); r["neto" + k] = n; r["netoTras" + k] = t
        r["netoMes" + k] = n / 12; r["netoPaga" + k] = n / d["pagas"]
        h = d["horas" + k] * SEM; r["hora" + k] = t / h if h > 0 else None
    dif = r["netoTrasB"] - r["netoTrasA"]; r["dif"] = dif
    r["ganador"] = "empate" if abs(dif) < 1 else ("b" if dif > 0 else "a")
    r["unaCero"] = 1 if (d["brutoA"] <= 0) != (d["brutoB"] <= 0) else 0   # una sola oferta a 0: sin veredicto ni bruto de igualacion
    if r["ganador"] == "empate" or r["unaCero"]: r["brutoIgual"] = None
    else:
        pe = "A" if dif > 0 else "B"; mej = r["netoTras" + ("B" if dif > 0 else "A")]
        r["brutoIgual"] = bruto_igual(mej + d["despl" + pe], cc)
    return r
B = dict(brutoA=32000, brutoB=36000, ccaa="madrid", pagas=14, desplA=600, desplB=1800, horasA=40, horasB=40)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto Madrid", V()), ("2 bruto 0 ambas", V(brutoA=0, brutoB=0, desplA=0, desplB=0)), ("3 mismo bruto, distinto trayecto", V(brutoA=30000, brutoB=30000)),
 ("4 sobre base maxima 90.000 vs 130.000 Cataluna", V(brutoA=90000, brutoB=130000, ccaa="cataluna", desplA=0, desplB=3000)),
 ("5 SMI 17.094 vs 20.048,45 Andalucia", V(brutoA=17094, brutoB=20048.45, ccaa="andalucia")),
 ("6 banda art. 20 15.000 vs 19.000 Galicia", V(brutoA=15000, brutoB=19000, ccaa="galicia", desplA=0, desplB=0)),
 ("7 mismas ofertas, Extremadura vs Valencia (A)", V(ccaa="extremadura")), ("8 Valencia", V(ccaa="valencia", horasA=37.5, horasB=45)),
 ("9 base maxima exacta 61.214,40", V(brutoA=61214.4, brutoB=61214.4 + 1000, ccaa="madrid", desplB=0)), ("10 horas 0 (sin dato)", V(horasA=0, horasB=0)),
 ("11 solidaridad >7.651,80/mes", V(brutoA=95000, brutoB=150000, ccaa="murcia", desplA=500, desplB=500, pagas=12)),
 ("12 Andalucia 18.500 vs 20.000 (gana la de menos bruto)", V(brutoA=18500, brutoB=20000, ccaa="andalucia", desplA=200, desplB=900)),
 ("13 Baleares 61.214,40 vs 70.000, 40/35 h", V(brutoA=61214.4, brutoB=70000, ccaa="baleares", desplA=500, desplB=4000, horasB=35)),
 ("14 una sola oferta a 0 (Asturias)", V(brutoA=0, brutoB=25000, ccaa="asturias", desplA=0, desplB=0))]
KEYS = ["ssA", "irpfA", "netoA", "netoTrasA", "ssB", "irpfB", "netoB", "netoTrasB", "netoMesA", "netoPagaA", "netoMesB", "netoPagaB", "horaA", "horaB", "dif", "brutoIgual"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/comparar-ofertas-de-trabajo-neto-real.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(23); ca = list(IR["ccaa"])
    if "--mono" in sys.argv:  # monotonia del neto en el bruto (condicion de la biseccion)
        bad = 0
        for cc in ca:
            prev = -1
            for b in range(0, 400001, 25):
                n = neto(b, cc)
                if n < prev - 1e-9: bad += 1; print("NO MONOTONO", cc, b, n, prev)
                prev = n
        print("monotonia: violaciones", bad); sys.exit(0)
    sweep = [dict(brutoA=rnd.choice([0, 9000, 17094, 22000, 30000, 45000, 62000, 90000, 140000]) * rnd.uniform(.9, 1.1), brutoB=rnd.choice([0, 12000, 17094, 25000, 38000, 55000, 80000, 120000, 200000]) * rnd.uniform(.9, 1.1),
                  ccaa=rnd.choice(ca), pagas=rnd.choice([12, 14]), desplA=rnd.choice([0, 300, 900, 2500]) * rnd.uniform(.5, 1.5), desplB=rnd.choice([0, 500, 1800, 4000]) * rnd.uniform(.5, 1.5),
                  horasA=rnd.choice([0, 20, 37.5, 40, 45]), horasB=rnd.choice([0, 30, 37.5, 40, 50])) for _ in range(600)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j[k], o[k]) for k in KEYS if (o[k] is None) != (j[k] is None) or (o[k] is not None and abs(j[k] - o[k]) > (1.0 if not k.startswith("hora") else .01))]
        if j["unaCero"] != o["unaCero"]: diffs.append(("unaCero", j["unaCero"], o["unaCero"]))
        if j["ganador"] != o["ganador"]: diffs.append(("ganador", j["ganador"], o["ganador"]))
        if i < len(CASES): print(CASES[i][0], {k: (round(o[k], 2) if o[k] is not None else None) for k in KEYS}, o["ganador"], "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias > 1 EUR"); sys.exit(1 if bad else 0)
