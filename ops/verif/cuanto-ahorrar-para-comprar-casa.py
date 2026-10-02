#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para cuanto-ahorrar-para-comprar-casa. Escrito desde la norma ANTES que el JS.
Tipos transcritos del BOE consolidado de cada comunidad (leidos el 2/10/2026): ITP (vivienda usada) y AJD tipo general de documentos notariales (vivienda nueva)
mas IVA 10 % (Ley 37/1992 art. 91.Uno.1.7.o). Cada comunidad con su propia funcion (no una tabla generica como el JS).
Uso: python3 ops/verif/cuanto-ahorrar-para-comprar-casa.py -> compara con el JS (osascript); sale 1 si hay diferencias > 0,01 EUR."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def prog(v, tr):  # tarifa progresiva: lista de (desde, tipo)
    s = 0.0
    for i, (lo, r) in enumerate(tr):
        hi = tr[i + 1][0] if i + 1 < len(tr) else float("inf")
        if v > lo: s += (min(v, hi) - lo) * r / 100
    return s
ITP = {
 "andalucia": lambda v: v * .07,
 "aragon": lambda v: prog(v, [(0, 8), (400000, 8.5), (450000, 9), (500000, 9.5), (750000, 10)]),        # cuota integra 32.000/36.250/40.750/64.500
 "asturias": lambda v: v * (.08 if v <= 300000 else .09 if v <= 500000 else .10),                          # tipo segun valor integro, a todo el valor
 "baleares": lambda v: prog(v, [(0, 8), (400000, 9), (600000, 10), (1000000, 12), (2000000, 13)]),        # cuota integra 32.000/50.000/90.000/210.000
 "cantabria": lambda v: v * .09,
 "clm": lambda v: v * .09,
 "cyl": lambda v: v * .08 + max(0, v - 250000) * .02,                                                       # 8 % y 10 % sobre el exceso de 250.000
 "cataluna": lambda v: prog(v, [(0, 10), (600000, 11), (900000, 12), (1500000, 13)]),                      # cuota integra 60.000/93.000/165.000
 "extremadura": lambda v: prog(v, [(0, 8), (360000, 10), (600000, 11)]),
 "galicia": lambda v: v * .08,
 "madrid": lambda v: v * .06,
 "murcia": lambda v: v * .0775,
 "rioja": lambda v: v * .07,
 "valencia": lambda v: v * (.11 if v > 1000000 else .09),
}
AJD = {"andalucia": 1.2, "aragon": 1.5, "asturias": 1.2, "cantabria": 1.5, "clm": 1.5, "cyl": 1.5, "cataluna": 1.5, "extremadura": 1.5,
       "galicia": 1.5, "murcia": 1.5, "rioja": 1.0, "valencia": 1.4}
def ajd(v, c):
    if c == "baleares": return v * (.02 if v >= 1000000 else .015)  # art. 17 bis DLeg 1/2014: 2 % si valor igual o superior a 1.000.000
    if c == "madrid": return v * (.004 if v <= 120000 else .005 if v <= 180000 else .0075)
    return v * AJD[c] / 100
def hab(d):
    """Ahorro total esperado del aviso 'vivienda habitual' (sin requisitos personales), desde la norma."""
    v = d["precio"]; c = d["ccaa"]; nueva = d["tipo"] == "nueva"; a = 0.0
    if nueva:
        g = ajd(v, c)
        if c == "valencia": a = g - v * .001
        elif c == "cantabria": a = g - v * .01
        elif c == "madrid" and v <= 250000: a = g * .10
        elif c == "andalucia" and v <= 150000: a = g - v * .01
        elif c == "baleares" and v <= 270151.2: a = g - v * .01
    else:
        g = ITP[c](v)
        if c == "cantabria" and v <= 300000: a = g - v * .07
        elif c == "madrid" and v <= 250000: a = g * .10
        elif c == "andalucia" and v <= 150000: a = g - v * .06
    return a if a > 0.5 else 0.0
PLAZO = 25
def model(d):
    v = d["precio"]; c = d["ccaa"]
    if d["tipo"] == "nueva": iva = v * .10; aj = ajd(v, c); imp = iva + aj; itp = 0.0
    else: iva = 0.0; aj = 0.0; itp = ITP[c](v); imp = itp
    ent = v * d["entrada"] / 100; hip = v - ent; total = ent + imp + d["gastos"]
    n = int(round(d["anos"] * 12))
    i = (1 + d["rentab"] / 100) ** (1 / 12) - 1
    ah = total / n if abs(i) < 1e-12 else total * i / ((1 + i) ** n - 1)
    j = d["interes"] / 1200; m = PLAZO * 12
    cuota = hip / m if abs(j) < 1e-12 else hip * j / (1 - (1 + j) ** -m)
    return dict(impuestos=imp, itp=itp, iva=iva, ajd=aj, entrada=ent, hipoteca=hip, totalNecesario=total, ahorroMensual=ah, cuotaHipoteca=cuota,
                costeTotal=v + imp + d["gastos"], pctExtra=100 * (imp + d["gastos"]) / v if v else 0)
B = dict(precio=250000, ccaa="madrid", tipo="usada", entrada=20, gastos=2500, anos=5, rentab=0, interes=4.2)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto Madrid usada", V()), ("2 nueva Madrid 250.000 (AJD >180.000)", V(tipo="nueva")), ("3 nueva Madrid 100.000 (AJD 0,4 %)", V(tipo="nueva", precio=100000)),
 ("4 usada Cataluna 1.000.000 (escala)", V(ccaa="cataluna", precio=1000000, entrada=30)), ("5 usada Asturias 300.000 vs 300.001", V(ccaa="asturias", precio=300001)),
 ("6 precio 0", V(precio=0)), ("7 rentabilidad 3 % y 10 anos", V(ccaa="valencia", rentab=3, anos=10, interes=0)), ("8 usada Aragon 750.000", V(ccaa="aragon", precio=750000)),
 ("9 nueva Valencia 400.000", V(ccaa="valencia", tipo="nueva", precio=400000, entrada=10)), ("10 usada Baleares 2.500.000", V(ccaa="baleares", precio=2500000)),
 ("11 nueva Baleares 1.000.000 (AJD 2 %)", V(ccaa="baleares", tipo="nueva", precio=1000000)), ("12 nueva Baleares 999.999", V(ccaa="baleares", tipo="nueva", precio=999999)),
 ("13 nueva Baleares 1.200.000 (144.000)", V(ccaa="baleares", tipo="nueva", precio=1200000)), ("14 nueva Madrid 120.000 (AJD 480)", V(tipo="nueva", precio=120000)),
 ("15 usada CyL 400.000 (ITP 35.000)", V(ccaa="cyl", precio=400000)), ("16 nueva Valencia 250.000 (hab 3.250)", V(ccaa="valencia", tipo="nueva")),
 ("17 usada Cantabria 250.000 (hab 5.000)", V(ccaa="cantabria")), ("18 usada Cantabria 300.001 (sin aviso)", V(ccaa="cantabria", precio=300001)),
 ("19 usada Madrid 250.001 (sin aviso)", V(precio=250001)), ("20 usada Andalucia 150.000 (hab 1.500)", V(ccaa="andalucia", precio=150000)),
 ("21 nueva Baleares 270.151,20 (hab)", V(ccaa="baleares", tipo="nueva", precio=270151.2)), ("22 nueva Baleares 270.151,21 (sin aviso)", V(ccaa="baleares", tipo="nueva", precio=270151.21))]
EXPECT = {"11 nueva Baleares 1.000.000 (AJD 2 %)": ("ajd", 20000), "12 nueva Baleares 999.999": ("ajd", 14999.985), "13 nueva Baleares 1.200.000 (144.000)": ("impuestos", 144000),
 "14 nueva Madrid 120.000 (AJD 480)": ("ajd", 480), "15 usada CyL 400.000 (ITP 35.000)": ("itp", 35000)}
EXPECT_HAB = {"16 nueva Valencia 250.000 (hab 3.250)": 3250, "17 usada Cantabria 250.000 (hab 5.000)": 5000, "18 usada Cantabria 300.001 (sin aviso)": 0, "19 usada Madrid 250.001 (sin aviso)": 0,
 "20 usada Andalucia 150.000 (hab 1.500)": 1500, "22 nueva Baleares 270.151,21 (sin aviso)": 0, "1 defecto Madrid usada": 1500, "2 nueva Madrid 250.000 (AJD >180.000)": 187.5}
KEYS = ["impuestos", "itp", "iva", "ajd", "entrada", "hipoteca", "totalNecesario", "ahorroMensual", "cuotaHipoteca", "costeTotal", "pctExtra"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/cuanto-ahorrar-para-comprar-casa.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(function (d) { var r = calcular(d); r.habTotal = ahorroHab(d, r).reduce(function (a, h) { return a + h.ahorro; }, 0); return r; }));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(5); ca = list(ITP)
    sweep = [dict(precio=rnd.choice([0, 50000, 120000, 180000, 300000, 450000, 750000, 1200000, 2500000]) * rnd.uniform(.8, 1.2), ccaa=rnd.choice(ca), tipo=rnd.choice(["nueva", "usada"]),
                  entrada=rnd.uniform(0, 100), gastos=rnd.uniform(0, 8000), anos=rnd.randint(1, 20), rentab=rnd.uniform(-2, 6), interes=rnd.uniform(0, 7)) for _ in range(600)]
    # bordes exactos de los tramos
    for c, vs in (("asturias", [300000, 300000.01, 500000, 500000.01]), ("madrid", [120000, 120000.01, 180000, 180000.01]), ("valencia", [1000000, 1000000.01]), ("cyl", [250000, 250000.01]), ("baleares", [999999.99, 1000000, 1000000.01, 270151.2, 270151.21]), ("cantabria", [300000, 300000.01]), ("andalucia", [150000, 150000.01]), ("madrid", [250000, 250000.01])):
        for v in vs:
            for t in ("usada", "nueva"): sweep.append(V(ccaa=c, precio=v, tipo=t))
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, round(j[k], 4), round(o[k], 4)) for k in KEYS if abs(j[k] - o[k]) > 0.01]
        if abs(j["habTotal"] - hab(c)) > 0.01: diffs.append(("habTotal", round(j["habTotal"], 4), round(hab(c), 4)))
        if i < len(CASES):
            nm = CASES[i][0]
            if nm in EXPECT and abs(j[EXPECT[nm][0]] - EXPECT[nm][1]) > 0.01: diffs.append(("esperado_informe", EXPECT[nm], j[EXPECT[nm][0]]))
            if nm in EXPECT_HAB and abs(j["habTotal"] - EXPECT_HAB[nm]) > 0.01: diffs.append(("hab_esperado", EXPECT_HAB[nm], j["habTotal"]))
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("impuestos", "totalNecesario", "ahorroMensual", "cuotaHipoteca")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1; print("DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias > 0,01 EUR"); sys.exit(1 if bad else 0)
