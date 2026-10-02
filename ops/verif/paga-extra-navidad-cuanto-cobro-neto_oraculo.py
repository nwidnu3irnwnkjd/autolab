#!/usr/bin/env python3
"""Oraculo independiente: paga-extra-navidad-cuanto-cobro-neto (ET art. 31, LGSS art. 147.1, RIRPF arts. 80.1 y 86.1). Escrito desde la norma antes del .js.
INTERPRETACION
- Paga de Navidad (ET 31): su cuantia y devengo los fija el convenio; el usuario da el importe de la paga COMPLETA y el periodo de devengo (anual 1-1 a 31-12 de 2026, o semestral 1-7 a 31-12). Supuesto S: proporcional por DIAS NATURALES devengados / dias del periodo.
- 'todo' = trabajo todo el periodo; 'alta' = entro en la fecha dada (cuenta ese dia, inclusive); 'baja' = ultimo dia trabajado inclusive (la parte proporcional se liquida en el finiquito, ET 49.2). Dias sin devengo (excedencia, etc., segun convenio) se restan, sin pasar de los dias devengados.
- Retencion (RIRPF 80.1.1.o y 86.1): se aplica a la cuantia total el tipo de la nomina; retencion = bruta x tipo, neto = bruta - retencion. Sin tipo distinto para la paga (no se modela el art. 87).
- Cotizacion (LGSS 147.1): las percepciones de vencimiento superior al mensual se prorratean en los 12 meses, asi que en el mes de la paga NO se cotiza aparte: el neto a ingresar es bruta - retencion. 'Neto equivalente' = ademas se resta la cotizacion del trabajador (6,5 %) ya descontada mes a mes (aproximacion, sin tope de base maxima).
- Pagas prorrateadas en las 12 mensualidades (ET 31 parr.2, por convenio): no hay paga en diciembre; la cuantia mensual = importe/12 bruta. 
- Imposibles: dia que no existe en el mes (31 de febrero), importe <= 0, dias sin devengo negativos.
- Escenarios: 1 paga entera; 2 proporcional; 3 prorrateada; 4 sin devengo (0 dias); 5 baja (se paga en el finiquito).
"""
import json, random, subprocess, sys, os, datetime
YEAR = 2026
def oraculo(d):
    imp = float(d["importe"]); ret = float(d["ret"]); cot = 6.5
    dia = int(d["dia"]); mes = int(d["mes"])
    sin = max(0, int(d["diassin"]))
    try: f = datetime.date(YEAR, mes, dia)
    except ValueError: f = None
    if not (imp > 0) or (d["forma"] != "prorr" and d["situacion"] != "todo" and f is None):
        return dict(bloqueado=1)
    ini = datetime.date(YEAR, 1, 1) if d["devengo"] == "anual" else datetime.date(YEAR, 7, 1)
    fin = datetime.date(YEAR, 12, 31)
    n = (fin - ini).days + 1
    if d["forma"] == "prorr":
        m = round(imp / 12, 2); r = round(m * ret / 100, 2)
        return dict(bloqueado=0, escenario=3, dias=n, diasPeriodo=n, bruta=0.0, mensual=m, retMensual=r, netoMensual=round(m - r, 2))
    if d["situacion"] == "todo": dev = n
    elif d["situacion"] == "alta": dev = (fin - max(f, ini)).days + 1 if f <= fin else 0
    else: dev = (min(f, fin) - ini).days + 1 if f >= ini else 0
    dev = max(0, dev)
    dias = max(0, dev - min(sin, dev))
    bruta = round(imp * dias / n, 2)
    r = round(bruta * ret / 100, 2)
    cotz = round(bruta * cot / 100, 2)
    if dias == 0: esc = 4
    elif dias == n: esc = 1
    elif d["situacion"] == "baja": esc = 5
    else: esc = 2
    return dict(bloqueado=0, escenario=esc, dias=dias, diasPeriodo=n, pct=dias / n * 100, bruta=bruta, retencion=r, neto=round(bruta - r, 2), cotizada=cotz, netoReal=round(bruta - r - cotz, 2))
def genera(n, seed=11):
    random.seed(seed); cs = []
    for _ in range(n):
        cs.append(dict(importe=random.choice([0, round(random.uniform(100, 4000), 2)]) if random.random() < .05 else round(random.uniform(100, 4000), 2),
                       devengo=random.choice(["anual", "semestral"]), situacion=random.choice(["todo", "alta", "baja"]),
                       mes=random.randint(1, 12), dia=random.randint(1, 31), diassin=random.choice([0, 0, random.randint(0, 200)]),
                       ret=round(random.uniform(0, 47), 2), forma=random.choice(["14", "14", "14", "prorr"])))
    return cs
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/paga-extra-navidad-cuanto-cobro-neto.js")).read().split("function eur(")[0]
    cases = genera(800)
    # bordes: 1-jul, 30-jun, 31-dic, 1-ene, 29-feb (no existe en 2026), 31-abr
    for devengo in ("anual", "semestral"):
        for s in ("alta", "baja"):
            for (m, dd) in ((7, 1), (6, 30), (12, 31), (1, 1), (2, 29), (4, 31), (12, 1)):
                cases.append(dict(importe=1500, devengo=devengo, situacion=s, mes=m, dia=dd, diassin=0, ret=15, forma="14"))
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0
    for c, r in zip(cases, res):
        o = oraculo(c)
        for k, v in o.items():
            if r.get(k) is None or abs(r[k] - v) > 0.011: bad += 1; print("DIF", c, k, r.get(k), v)
    print(f"{len(cases)} casos, discrepancias: {bad}"); sys.exit(1 if bad else 0)
