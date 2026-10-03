#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-03): sueldo-bruto-a-neto-2026. Escrito desde la norma ANTES del .js.
INTERPRETACION
- Neto de NOMINA = bruto - cotizacion del trabajador - retencion. Cotizacion (Orden PJC/297/2026 arts. 2, 4, 16, 17, 33; LGSS 147.1): base mensual = bruto/12 (pagas prorrateadas), tope 5.101,20;
  tipo = CC 4,70 + MEI 0,15 + FP 0,10 + desempleo (1,55 indefinido; 1,60 temporal) sobre la base topada; solidaridad (art. 17) 0,19/0,21/0,24 sobre el exceso mensual en tramos de 10 % y 50 % de la base maxima. Anual = 12 meses.
- Retencion (RIRPF arts. 80-86, 88.2: sin comunicar circunstancias solo cuenta lo que el usuario declara aqui): base = retribucion - SS - 2.000 (19.2.f, limite retribucion - SS) - reduccion art. 20 (sobre retribucion - SS) - 600 si >= 3 descendientes (83.3.e);
  minimo (84) = 5.550 + descendientes 2.400/2.700/4.000/4.500 + 2.800 por menor de 3, enteros (los computa solo el usuario); cuota = escala_ret(base) - escala_ret(minimo) (85.1); si <= 0, tipo 0; si retribucion <= 35.200, cuota <= 43 % x (retribucion - limite 81) (85.3);
  tipo = cuota/retribucion con 2 decimales (86.1); art. 81.1 situacion 3.ª («otras situaciones»): si la retribucion no supera 15.876/16.342/16.867 segun 0/1/2+ descendientes, no se retiene. Temporal de menos de 1 año: tipo >= 2 % (86.2) y el limite del 81 no se aplica (81.3).
- IRPF final 2026 (declaracion individual, solo ese salario): rendimiento neto = bruto - SS; menos 2.000 (19.2.f) y reduccion art. 20 (sobre bruto - SS); cuota = [escala estatal(base) - escala estatal(minimo)] + [escala autonomica(base) - escala autonomica(minimo)] (minimo >= 0; minimo autonomico propio o el estatal);
  DA 61.ª: 590,89 (bruto <= 17.094) o menos 0,2 por el exceso hasta 20.048,45, limitada a la cuota integra. Diferencia retencion - IRPF final = a devolver (positivo) o a pagar (negativo).
- Neto por mes: 12 pagas = neto/12; 14 pagas: mes normal = paga x (1 - tipo) - SS/12; mes con paga extra = 2 x paga x (1 - tipo) - SS/12 (la SS se descuenta cada mes, la retencion sobre cada paga).
- Temporal de menos de 1 año (C1, RIRPF 83.2 regla 1.ª «año natural»): R = bruto equivalente x meses/12 (meses 1-11); SS = SS(bruto equivalente) x meses/12; retencion, IRPF final y DA 61.ª sobre R; neto por mes = neto/meses (sin reparto en pagas).
- Sin obligacion de declarar si R <= 22.000 con un pagador (LIRPF 96.2.a): solo cambia el texto de la pagina.
- Imposibles: meses fuera de 1-11 con temp1; bruto <= 0, forales (sin escala), menores de 3 > hijos, hijos > 10: bloqueado. Fuera: base minima de grupo, situaciones 1.ª y 2.ª del art. 81, ascendientes, discapacidad, deducciones, Ceuta/Melilla, Canarias (IGIC no afecta).
Uso: python3 ops/verif/sueldo-bruto-a-neto-2026_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]
EST = [(0, 9.5), (12450, 12), (20200, 15), (35200, 18.5), (60000, 22.5), (300000, 24.5)]
RET = [(0, 19), (12450, 24), (20200, 30), (35200, 37), (60000, 45), (300000, 47)]
BMAX = 5101.20
DESC = [2400, 2700, 4000, 4500]
def scale(x, esc):
    t = 0.0
    for i, (lo, r) in enumerate(esc):
        hi = esc[i + 1][0] if i + 1 < len(esc) else float("inf")
        if x > lo: t += (min(x, hi) - lo) * r / 100
    return t
def ss(R, temp):
    m = R / 12; base = min(m, BMAX)
    tipo = 4.70 + 0.15 + 0.10 + (1.60 if temp else 1.55)
    ex = max(0.0, m - BMAX)
    t1 = min(ex, 0.10 * BMAX); t2 = min(max(ex - 0.10 * BMAX, 0.0), 0.40 * BMAX); t3 = max(ex - 0.50 * BMAX, 0.0)
    return 12 * (base * tipo / 100 + t1 * 0.19 / 100 + t2 * 0.21 / 100 + t3 * 0.24 / 100)
def art20(rn):
    if rn <= 14852: return 7302.0
    if rn <= 17673.52: return 7302 - 1.75 * (rn - 14852)
    if rn < 19747.5: return 2364.34 - 1.14 * (rn - 17673.52)
    return 0.0
def model(d):
    Req = float(d["bruto"]); meses = int(d.get("meses", 6)); menos = d["contrato"] == "temp1"; R = Req * meses / 12 if menos else Req; n = int(d["hijos"]); m3 = int(d["menores3"]); cc = d["ccaa"]; con = d["contrato"]
    if not (Req > 0) or cc not in PAR["ccaa"] or m3 > n or n > 10 or (menos and not 1 <= meses <= 11): return dict(bloqueado=1)
    temp = con != "indef"; temp1 = con == "temp1"
    S = ss(Req, temp) * (meses / 12 if menos else 1); rn = R - S
    # retencion
    lim = (15876, 16342, 16867)[min(n, 2)]
    g = min(2000, rn)
    base = max(0.0, rn - g - art20(rn) - (600 if n >= 3 else 0))
    mn = 5550 + sum(DESC[min(i, 3)] for i in range(n)) + 2800 * m3
    if (not temp1) and R <= lim: tipo = 0.0
    elif base - mn <= 0: tipo = 0.0
    else:
        cuota = max(0.0, scale(base, RET) - scale(mn, RET))
        if R <= 35200: cuota = min(cuota, 0.43 * max(0.0, R - lim))
        tipo = int(cuota / R * 10000 + 0.5 + 1e-7) / 100
    if temp1: tipo = max(tipo, 2.0)
    ret = R * tipo / 100
    neto = R - S - ret
    # IRPF final
    c = PAR["ccaa"][cc]
    base_f = max(0.0, rn - g - art20(rn))
    mn_e = 5550 + sum(DESC[min(i, 3)] for i in range(n)) + 2800 * m3
    if c["minimo"]:
        mn_a = c["minimo"]["contribuyente"] + sum(c["minimo"]["descendientes"][min(i, 3)] for i in range(n)) + c["minimo"]["menor3"] * m3
    else: mn_a = mn_e
    ci = max(0.0, scale(base_f, EST) - scale(mn_e, EST)) + max(0.0, scale(base_f, [tuple(x) for x in c["escala_general"]]) - scale(mn_a, [tuple(x) for x in c["escala_general"]]))
    da = 0.0
    if R < 20048.45: da = 590.89 if R <= 17094 else 590.89 - 0.2 * (R - 17094)
    irpf = ci - min(da, ci)
    p = R / 14
    return dict(bloqueado=0, ss=S, tipo=tipo, ret=ret, neto=neto, netoMes12=neto / (meses if menos else 12), netoMesNormal14=neto / meses if menos else p * (1 - tipo / 100) - S / 12, netoMesExtra14=neto / meses if menos else 2 * p * (1 - tipo / 100) - S / 12,
                irpfFinal=irpf, netoFinal=R - S - irpf, difRenta=ret - irpf)
KEYS = ["bloqueado", "ss", "tipo", "ret", "neto", "netoMes12", "netoMesNormal14", "netoMesExtra14", "irpfFinal", "netoFinal", "difRenta"]
B = dict(bruto=25200, pagas=14, meses=6, contrato="indef", ccaa="madrid", hijos=0, menores3=0)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto 1.800 x 14", V()), ("2 1.800 x 12", V(bruto=21600, pagas=12)), ("3 15.876", V(bruto=15876)), ("4 15.877", V(bruto=15877)), ("5 17.094", V(bruto=17094)),
 ("6 20.048,45", V(bruto=20048.45)), ("7 35.200", V(bruto=35200)), ("8 61.214,40", V(bruto=61214.4)), ("9 61.214,41", V(bruto=61214.41)), ("10 90.000", V(bruto=90000, ccaa="cataluna")),
 ("11 temporal <1 año 14.400", V(bruto=14400, contrato="temp1")), ("12 temporal >=1 año 14.400", V(bruto=14400, contrato="temp2")), ("13 3 hijos 1 menor de 3", V(bruto=40000, hijos=3, menores3=1, ccaa="galicia")),
 ("14 4 hijos", V(bruto=36000, hijos=4, menores3=2, ccaa="valencia")), ("15 foral", V(ccaa="pv")), ("16 menores3>hijos", V(hijos=1, menores3=2)), ("17 bruto 0", V(bruto=0)),
 ("18 temporal <1 año 30.000", V(bruto=30000, contrato="temp1")), ("19 120.000 Valencia", V(bruto=120000, ccaa="valencia")), ("20 3.000x14", V(bruto=42000, ccaa="andalucia")),
 ("21 temp1 6 meses 25.200 eq", V(contrato="temp1", meses=6)), ("22 temp1 11 meses 60.000 eq", V(contrato="temp1", meses=11, bruto=90000)), ("23 temp1 12 meses invalido", V(contrato="temp1", meses=12)), ("24 temp1 1 mes", V(contrato="temp1", meses=1, bruto=30000, hijos=1))]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/sueldo-bruto-a-neto-2026.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(2026)
    ccs = list(PAR["ccaa"].keys()) + ["pv", "navarra"]
    def mk():
        n = rnd.choice([0, 0, 0, 1, 2, 3, 4, 5, 11]); return dict(bruto=rnd.choice([rnd.uniform(8000, 25000), rnd.uniform(15000, 60000), rnd.uniform(20000, 200000), 15876, 16342, 16867, 17094, 20048.45, 35200, 61214.4, 14400, 16800]),
            pagas=rnd.choice([12, 14]), contrato=rnd.choice(["indef", "indef", "temp1", "temp2"]), ccaa=rnd.choice(ccs), hijos=n, menores3=rnd.randint(0, n + (1 if rnd.random() < 0.03 else 0)), meses=rnd.choice([1, 3, 6, 6, 9, 11, 12, 0]))
    allc = [c for _, c in CASES] + [mk() for _ in range(700)]
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = []
        for k in KEYS:
            if k not in o: continue
            if j.get(k) is None or abs(j[k] - o[k]) > (0.0051 if k == "tipo" else 0.011): diffs.append((k, j.get(k), o[k]))
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("ss", "tipo", "ret", "neto", "netoMesNormal14", "irpfFinal", "difRenta") if k in o}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("DIF", c, diffs)
    print(f"{len(allc)} casos, {bad} discrepancias"); sys.exit(1 if bad else 0)
