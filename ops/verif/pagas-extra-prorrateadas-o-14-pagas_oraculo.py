#!/usr/bin/env python3
"""Oraculo independiente: pagas-extra-prorrateadas-o-14-pagas (ET art. 31, LGSS arts. 147.1 y 270.1, Decreto 1646/1972 art. 13, RIRPF arts. 83.2, 86.1). Escrito desde la norma ANTES del .js.
INTERPRETACION
- Mismo bruto anual B cobrado de dos formas. A) 12+n pagas iguales (n extras, n = 2, 3 o 4): cada paga = B/(12+n). B) Pagas prorrateadas (ET 31 parr. 2, solo si lo prevé el convenio): 12 pagas de B/12.
- Cotizacion (LGSS 147.1: las percepciones de vencimiento superior al mensual se prorratean en los 12 meses): base mensual = min(B/12, base maxima) en A y en B; cuota del trabajador = base x 6,5 % (indefinido) o 6,55 % (temporal), cada mes; el mes con paga extra no cotiza aparte. Idéntica en las dos formas.
- Retencion (RIRPF 83.2.1.a y 86.1): el tipo sale de la cuantia total anual de las retribuciones, que es B en las dos formas, asi que el tipo es el mismo y la retencion de cada pago es tipo x pago bruto. Anual = B x tipo en ambas. No se modela el art. 87 (regularizacion) ni la cuota minima del 86.2.
- Paro: base reguladora diaria = base de cotizacion mensual / 30 (LGSS 270.1, promedio de la base cotizada 180 dias; 147.1 prorratea las pagas): igual en A y B (baseDiaria). IT: Decreto 1646/1972 art. 13.1 y 13.4 (sueldo sin pagas / 30 + promedio de las pagas de 12 meses): igual en A y B, cifra no modelada (66,54 con promedio/365). No se calcula la prestacion.
- Calendario de pagas extra en A (supuesto, lo fija el convenio): se devengan en n periodos iguales del año por dias naturales y se cobran al cierre: n=2 jun y dic; n=3 abr, ago y dic; n=4 mar, jun, sep y dic.
- Baja (ultimo dia trabajado = f): se devenga el sueldo ordinario de (mes-1) + dia/dias_del_mes meses; en A ademas cada paga extra por los dias naturales de su periodo transcurridos. Las pagas de periodos cerrados antes del mes de la baja ya se cobraron en nomina; el resto (incluida la de un periodo que acaba en el mes de la baja) se paga en el finiquito. En B no queda nada pendiente. Retencion del finiquito al mismo tipo (supuesto, ver art. 87).
- Imposibles: bruto <= 0; fecha inexistente en 2026 con situacion=baja.
"""
import json, random, subprocess, sys, os, calendar, datetime
YEAR = 2026
BMAX = 5101.20
COT = {"indef": 6.5, "temp": 6.55}
def oraculo(d):
    B = float(d["bruto"]); n = int(d["extras"]); t = float(d["ret"]) / 100; cot = COT[d["contrato"]] / 100
    baja = d["situacion"] == "baja"
    m = int(d["mes"]); dd = int(d["dia"])
    f = None
    if baja:
        try: f = datetime.date(YEAR, m, dd)
        except ValueError: f = None
    if not (B > 0) or (baja and f is None): return dict(bloqueado=1)
    pagas = 12 + n
    pe = B / pagas; m14 = pe; m12 = B / 12
    base = min(B / 12, BMAX); cot_mes = base * cot
    out = dict(bloqueado=0, escenario=2 if baja else 1, pagaExtra=round(pe, 2), mensual14=round(m14, 2), mensual12=round(m12, 2),
               baseCot=round(base, 2), cotMes=round(cot_mes, 2), baseDiaria=round(base / 30, 2),
               retMes14=round(m14 * t, 2), retMesPaga14=round(2 * m14 * t, 2), retMes12=round(m12 * t, 2),
               netoMes14=round(m14 * (1 - t) - cot_mes, 2), netoMesPaga14=round(2 * m14 * (1 - t) - cot_mes, 2), netoMes12=round(m12 * (1 - t) - cot_mes, 2))
    out["difMensual"] = round(out["netoMes12"] - out["netoMes14"], 2) if False else round((m12 * (1 - t) - cot_mes) - (m14 * (1 - t) - cot_mes), 2)
    if not baja:
        pay_months = [12 * (k + 1) // n for k in range(n)]
        net14 = ret14 = 0.0
        for mm in range(1, 13):
            g = m14 + (pe if mm in pay_months else 0.0)
            ret14 += g * t; net14 += g * (1 - t) - cot_mes
        net12 = 12 * (m12 * (1 - t) - cot_mes)
        out.update(netoAnual14=round(net14, 2), netoAnual12=round(net12, 2), difAnual=round(net14 - net12, 2),
                   retAnual14=round(ret14, 2), retAnual12=round(B * t, 2), cotAnual=round(12 * cot_mes, 2))
        return out
    dm = calendar.monthrange(YEAR, m)[1]
    meses = (m - 1) + dd / dm
    pend = paid = 0.0
    for k in range(n):
        sm = 12 * k // n + 1; em = 12 * (k + 1) // n
        s = datetime.date(YEAR, sm, 1); e = datetime.date(YEAR, em, calendar.monthrange(YEAR, em)[1])
        ln = (e - s).days + 1
        acc = max(0, min((f - s).days + 1, ln)) / ln * pe
        if em < m: paid += acc
        else: pend += acc
    g14 = m14 * meses + paid + pend; g12 = m12 * meses
    cot_tot = cot_mes * meses
    out.update(devengado14=round(g14, 2), devengado12=round(g12, 2), difDevengado=round(g14 - g12, 2),
               pendiente14=round(pend, 2), pendienteNeto14=round(pend * (1 - t), 2), nomina14=round(g14 - pend, 2), nomina12=round(g12, 2),
               neto14=round(g14 * (1 - t) - cot_tot, 2), neto12=round(g12 * (1 - t) - cot_tot, 2),
               difNeto=round((g14 - g12) * (1 - t), 2))
    return out
def genera(n, seed=58):
    random.seed(seed); cs = []
    for _ in range(n):
        B = random.choice([0, 9000]) if random.random() < .03 else (round(random.uniform(14000, 150000), 2) if random.random() < .8 else round(random.uniform(14000, 70000), 2))
        cs.append(dict(bruto=B, extras=random.choice([2, 3, 4]), contrato=random.choice(["indef", "temp"]), ret=round(random.uniform(0, 47), 2),
                       situacion=random.choice(["todo", "baja", "baja"]), mes=random.randint(1, 12), dia=random.randint(1, 31)))
    return cs
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/pagas-extra-prorrateadas-o-14-pagas.js")).read().split("function eur(")[0]
    cases = genera(900)
    for ex in (2, 3, 4):
        for (mm, dd) in ((1, 1), (6, 30), (7, 1), (12, 31), (4, 30), (8, 31), (9, 30), (3, 31), (2, 29), (4, 31), (6, 1)):
            cases.append(dict(bruto=24000, extras=ex, contrato="indef", ret=15, situacion="baja", mes=mm, dia=dd))
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0; maxdif = 0; maxan = 0
    for c, r in zip(cases, res):
        o = oraculo(c)
        for k, v in o.items():
            if r.get(k) is None or abs(r[k] - v) > 0.011: bad += 1; print("DIF", c, k, r.get(k), v)
        if o.get("escenario") == 2: maxdif = max(maxdif, abs(o["difDevengado"]))
        if o.get("escenario") == 1: maxan = max(maxan, abs(o["difAnual"]))
    print(f"{len(cases)} casos, discrepancias: {bad}; max |dif devengado| en baja = {maxdif:.2f}; max |dif neto anual| = {maxan:.2f}"); sys.exit(1 if bad else 0)
