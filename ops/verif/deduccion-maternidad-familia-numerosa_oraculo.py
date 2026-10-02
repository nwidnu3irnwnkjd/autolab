#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para deduccion-maternidad-familia-numerosa. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado, consultado el 2/10/2026; LIRPF art. 81 en vigor desde 1/1/2023, art. 81 bis desde 5/7/2018; RIRPF arts. 60 y 60 bis; Ley 40/2003 art. 4):
1. Maternidad (art. 81.1): 1.200 EUR/ano por hijo menor de 3 anos, proporcional a los meses posteriores al cumplimiento del requisito de actividad (paro al nacer, o alta con 30 dias cotizados entonces o despues; NO hay que seguir de alta; mesesMat) en que tiene derecho al minimo por descendientes (art. 81.3, RIRPF 60.2.1.a). Reembolsable: minora la cuota DIFERENCIAL. SIN limite por cotizaciones (el art. 81 vigente no lo contiene; el limite es solo del art. 81 bis).
2. Guarderia (art. 81.2-3, RIRPF 60.1): +hasta 1.000 EUR/ano por hijo, proporcional a los meses completos de guarderia autorizada simultaneos con (1), con tope = gasto efectivo no subvencionado del hijo en el ano.
3. Familia numerosa (art. 81 bis.1.c): 1.200 EUR/ano con actividad (alta en SS, paro o pension), proporcional a meses con alta o prestacion (mesesFam, 81 bis.2). Con paro o pension no hay limite (RIRPF 60 bis.1): el usuario escribe cotiz >= 1.200. LIMITE: cotizaciones y cuotas SS devengadas en el ano (integras) para ESTA parte (1.200).
   Categoria especial: +100 % (otros 1.200 EUR) y +600 EUR por hijo que exceda el minimo (3 en general, 5 en especial, Ley 40/2003 art. 4.1): ambos incrementos NO cuentan para el limite (81 bis.1.c y RIRPF 60 bis.1).
   Ascendiente separado o sin vinculo con 2 hijos sin anualidades por alimentos y con derecho a todo el minimo: 1.200 EUR (misma letra c), sin incrementos de familia numerosa.
   Dos contribuyentes con derecho (mismo hijo/familia): importe prorrateado por partes iguales (81 bis.1 penultimo parrafo); el limite se aplica a cada uno.
4. Maternidad y 81 bis son deducciones distintas, acumulables (ningun precepto las hace incompatibles). Abono anticipado (Modelo 140 / 143; art. 81.4 y 81 bis.3): 100 EUR/mes por hijo; 81 bis: 100 (200 especial) +50 por hijo extra, dividido entre titulares;
   la guarderia NO se anticipa. Lo anticipado no minora luego la cuota diferencial (el total anual es el mismo).
Uso: python3 ops/verif/deduccion-maternidad-familia-numerosa_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def model(d):
    n3, mm, mf, gm, gasto, fam, h, cot = int(d["n3"]), d["mesesMat"], d["mesesFam"], d["guarMeses"], d["guarGasto"], d["fam"], d["hijosFam"], d["cotiz"]
    t = 2 if fam.endswith("x2") else 1; fam = fam[:-2] if t == 2 else fam
    bad = (fam == "general" and (h < 3 or n3 > h)) or (fam == "especial" and (h < 4 or n3 > h)) or (fam == "mono2" and n3 > 2) or not (0 <= mm <= 12) or not (0 <= mf <= 12)
    if bad: return dict(invalido=1, mat=0, guar=0, fam=0, especial=0, exceso=0, deduccion=0, recorte=0, anticipoMes=0, anticipoAnual=0, resto=0)
    mat = n3 * 1200 * mm / 12
    guar = n3 * min(1000 * min(gm, mm) / 12, gasto)
    fam_b = esp = exc = rec = 0.0
    famMes = 0.0
    if fam != "no":
        base = 1200 * mf / 12 / t
        fam_b = min(base, cot); rec = base - fam_b
        famMes = 100.0 / t
        if fam == "especial":
            esp = 1200 * mf / 12 / t; famMes += 100.0 / t
        if fam in ("general", "especial"):
            e = max(0, h - (3 if fam == "general" else 5))
            exc = 600 * e * mf / 12 / t; famMes += 50.0 * e / t
    ded = mat + guar + fam_b + esp + exc
    am = 100.0 * n3 * mm + famMes * mf
    return dict(invalido=0, mat=mat, guar=guar, fam=fam_b, especial=esp, exceso=exc, deduccion=ded, recorte=rec, anticipoMes=100.0 * n3 + famMes, anticipoAnual=am, resto=ded - am)
B = dict(n3=1, mesesMat=12, mesesFam=12, guarMeses=10, guarGasto=3000, fam="general", hijosFam=3, cotiz=3500)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto", V()), ("2 solo maternidad 12 meses sin guarderia", V(fam="no", mesesFam=0, guarMeses=0, guarGasto=0)), ("3 0 hijos sin familia", V(n3=0, fam="no", mesesFam=0)),
 ("4 cotizacion 0 (especial 6 hijos)", V(fam="especial", hijosFam=6, cotiz=0, n3=0)), ("5 general cotizacion 0", V(cotiz=0)), ("6 gasto guarderia menor que tope", V(guarGasto=400)),
 ("7 especial 5 hijos dos titulares", V(fam="especialx2", hijosFam=5, n3=2)), ("8 general 5 hijos 7 meses", V(hijosFam=5, mesesMat=7, mesesFam=7, guarMeses=7, cotiz=500, n3=2)),
 ("9 monoparental 2 hijos", V(fam="mono2", hijosFam=2, n3=1)), ("10 invalido general 2 hijos", V(hijosFam=2)), ("11 12 meses guarderia 12", V(guarMeses=12, guarGasto=5000, n3=3, hijosFam=4)),
 ("A maternidad 12, familia 6, cotiz 2000", V(mesesFam=6, cotiz=2000)), ("B paro/pensión todo el año, sin hijos <3, cotiz>=1200", V(n3=0, guarMeses=0, guarGasto=0, cotiz=1200)),
 ("C solo maternidad con guardería 12 meses", V(fam="no", mesesFam=0, guarMeses=12, guarGasto=5000)), ("D mono2 un titular", V(fam="mono2", hijosFam=2, n3=0, guarMeses=0, guarGasto=0))]
KEYS = ["invalido", "mat", "guar", "fam", "especial", "exceso", "deduccion", "recorte", "anticipoMes", "anticipoAnual", "resto"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/deduccion-maternidad-familia-numerosa.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(81)
    def mk():
        return dict(n3=rnd.choice([0, 1, 1, 2, 3, 4]), mesesMat=rnd.choice([0, 1, 6, 12, rnd.randint(0, 12)]), mesesFam=rnd.choice([0, 6, 12, rnd.randint(0, 12)]), guarMeses=rnd.randint(0, 12), guarGasto=rnd.choice([0, 300, 2000, rnd.uniform(0, 6000)]),
                    fam=rnd.choice(["no", "general", "generalx2", "especial", "especialx2", "mono2"]), hijosFam=rnd.randint(2, 9), cotiz=rnd.choice([0, 100, 1200, rnd.uniform(0, 9000)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.005]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("mat", "guar", "fam", "especial", "exceso", "deduccion", "anticipoMes")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
