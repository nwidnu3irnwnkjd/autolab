#!/usr/bin/env python3
"""Oraculo independiente: nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad. Escrito desde la norma (LGSS 19 bis, 127 bis, DT 42.a, DT 43.a, DT 38.a; Orden PJC/297/2026 arts. 2, 4, 16, 17, 33) antes del .js.
INTERPRETACION
- Cotizacion del trabajador por cuenta ajena, Regimen General, con la base mensual = bruto anual / 12 (pagas prorrateadas en la base, Orden art. 1.1 regla 2.a; supuesto: sueldo igual todos los meses).
- Hasta la base maxima B: CC 4,70 % + MEI (DT 43.a: 0,15 en 2026 y 0,17 en 2027) + desempleo (1,55 indefinido, 1,60 temporal, Orden art. 33) + FP 0,10 %, todos sobre min(base, B) (el tope de desempleo y FP es el mismo tope maximo, Orden art. 2 y 33.1).
- Solidaridad (LGSS 19 bis, DT 42.a, RGC 72 bis, Orden art. 17): sobre el exceso de la remuneracion mensual sobre B, en tres tramos: hasta B*1,10; de B*1,10 a B*1,50; mas de B*1,50. Tipos totales 2026 1,15/1,25/1,46 y 2027 1,38/1,50/1,75; parte del trabajador = proporcion de CC (4,70/28,30), redondeada a 2 decimales como en la Orden 2026 (0,19/0,21/0,24; 2027 derivado 0,23/0,25/0,29: SUPUESTO, la orden 2027 no existe).
- Base maxima 2026 = 5.101,20 (Orden art. 2). La de 2027 no esta publicada: input editable.
- Cada concepto se redondea a centimos por mes; anual = 12 meses. Comparacion 2026 (B26) frente a 2027 (B27 del usuario) con el mismo sueldo y mismos tipos de CC/desempleo/FP (supuesto).
- Imposibles: bruto <= 0 o B27 <= 0 (bloqueado). Base minima de grupo y bases fijas no modeladas (declarado).
"""
import json, random, subprocess, sys, os
B26 = 5101.20
MEI = {26: 0.15, 27: 0.17}
SOL_TOTAL = {26: (1.15, 1.25, 1.46), 27: (1.38, 1.50, 1.75)}
def r2(x): return round(x + 1e-9, 2)
def sol_trab(y): return tuple(round(t * 4.70 / 28.30 + 1e-9, 2) for t in SOL_TOTAL[y])
def cuota(y, B, m, temporal):
    base = min(m, B)
    des = 1.60 if temporal else 1.55
    cc = r2(base * 4.70 / 100); mei = r2(base * MEI[y] / 100); de = r2(base * des / 100); fp = r2(base * 0.10 / 100)
    ex = max(0.0, m - B)
    a, b, c = sol_trab(y)
    t1 = min(ex, 0.10 * B); t2 = min(max(ex - 0.10 * B, 0.0), 0.40 * B); t3 = max(ex - 0.50 * B, 0.0)
    sol = r2(t1 * a / 100) + r2(t2 * b / 100) + r2(t3 * c / 100)
    sol = r2(sol)
    return dict(cc=cc, mei=mei, des=de, fp=fp, sol=sol, total=r2(cc + mei + de + fp + sol))
def oraculo(d):
    anual = float(d["bruto"]); B27 = float(d["base27"]); temporal = d["contrato"] == "temporal"
    if not (anual > 0) or not (B27 > 0): return dict(bloqueado=1)
    m = anual / 12
    c26 = cuota(26, B26, m, temporal); c27 = cuota(27, B27, m, temporal); c26b = cuota(26, B27, m, temporal)
    dmei = 12 * (c27["mei"] - c26b["mei"]); dsol = 12 * (c27["sol"] - c26b["sol"]); dbase = 12 * (c26b["total"] - c26["total"])
    sube = 12 * (c27["total"] - c26["total"])
    return dict(bloqueado=0, escenario=(2 if m > B27 else 1), mes26=c26["total"], mes27=c27["total"], anual26=12 * c26["total"], anual27=12 * c27["total"],
                sube=sube, dMei=dmei, dSol=dsol, dBase=dbase, mei27=12 * c27["mei"], sol26=12 * c26["sol"], sol27=12 * c27["sol"], solMes27=c27["sol"])
def genera(n, seed=58):
    random.seed(seed); cs = []
    for _ in range(n):
        B = random.choice([5101.2, 5101.2, round(random.uniform(4000, 6500), 2)])
        r = random.random()
        if r < .35: anual = round(random.uniform(6000, 61000), 2)
        elif r < .7: anual = round(random.uniform(61000, 120000), 2)
        elif r < .9: anual = round(random.uniform(120000, 300000), 2)
        else: anual = random.choice([0, -5, round(12 * B, 2), round(12 * B * 1.1, 2), round(12 * B * 1.5, 2), round(12 * B * 1.5 + .12, 2)])
        cs.append(dict(bruto=anual, contrato=random.choice(["indefinido", "temporal"]), base27=random.choice([B, 0]) if random.random() < .03 else B))
    return cs
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad.js")).read().split("function eur(")[0]
    cases = genera(800)
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0
    for c, r in zip(cases, res):
        for k, v in oraculo(c).items():
            if r.get(k) is None or abs(r[k] - v) > 0.011: bad += 1; print("DIF", c, k, r.get(k), v)
    print(f"{len(cases)} casos, discrepancias: {bad}"); sys.exit(1 if bad else 0)
