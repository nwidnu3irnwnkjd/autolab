#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para jubilacion-activa-o-dejar-de-trabajar. Escrito desde la norma ANTES del .js.
INTERPRETACION (LGSS consolidada BOE-A-2015-11724 leida hoy, arts. 153, 205, 210, 214, 310; RDL 11/2024 art. 1.3; ver journal/preverif-jubilacion-activa-o-dejar-de-trabajar.md):
 - ACTIVA (art. 214 vigente desde 1-4-2025): se pide la pension (hecho causante, HC) >= 1 ano despues de la edad ordinaria (EO) con 15 anos cotizados a la EO; sin anticipo.
   Cobras un % del importe del reconocimiento inicial (art. 210 incl. complemento de demora, sin complemento por minimos): 45/55/65/80/100 % con 1/2/3/4/5+ anos COMPLETOS de demora;
   autonomo con un trabajador indefinido (18 meses o nuevo): 75 % si demora 1-3 anos (desde el 4.o ano, la escala). +5 puntos por cada 12 meses seguidos en activa (desde el mes siguiente), tope 100 %.
   Ademas trabajas y cobras el sueldo; cotizas solo IT/CP + solidaridad 9 % (art. 153: 7 empresa + 2 trabajador; art. 310: 9 % autonomo sobre su base de CC). Sin mas pension por ello (214.4).
   Desde la edad ordinaria (arts. 152 y 311, Orden PJC/297/2026 art. 32): sin pension solo IT (trabajador 0,25 %; autonomo 1,56 % IT + 1,30 % CP); en activa eso mas la solidaridad.
 - JUBILARSE DEL TODO: misma pension (100 %) desde el HC, sin sueldo. DEMORAR: sigues trabajando N anos mas SIN pension (solo IT/CP, ver arriba; base minima del tramo RETA)
   y luego cobras la pension con la demora de D+N meses (4 puntos por ano completo, +2 desde 2 anos si sobran > 6 meses; art. 210.2.a), tope art. 57 con el exceso como cantidad anual (tope base cotizacion/14).
 - EO (205.1.a, DT 7.ª segun el ANIO en que se cumple, tomando el HC en julio): 65 anos si a esa edad hay los meses del cuadro (2024 456, 2025-26 459, 2027+ 462), si no la edad del cuadro (798/800/802/804); con cotizacion continuada se alcanzan antes (edad intermedia). Porcentaje de la BR (art. 210.1, DT 9.ª): 2027+ 0,19 x 248 + 0,18; 2023-26 0,21 x 49 + 0,19.
 - Imposible: HC < EO (anticipada, no activa) -> estado 1; < 15 anos al HC -> estado 2; 15 anos solo despues de la EO -> estado 3 (214.1 in fine: activa posible, sin complemento; no se calcula); demora < 12 meses -> sin activa (activa=0).
Uso: python3 ops/verif/jubilacion-activa-o-dejar-de-trabajar_oraculo.py -> compara con el JS real (osascript); sale 1 si hay diferencias > 1 EUR."""
import json, os, subprocess, sys, random, math
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "jubilacion-activa-o-dejar-de-trabajar"
MAXM, TOPE, BMAX = 3359.60, 61214.40, 5101.20
TRAMOS = [(670, 653.59), (900, 718.95), (1166.7, 849.67), (1300, 950.98), (1500, 960.78), (1700, 960.78), (1850, 1143.79),
          (2030, 1209.15), (2330, 1274.51), (2760, 1356.21), (3190, 1437.91), (3620, 1519.61), (4050, 1601.31), (6000, 1732.03), (None, 1928.10)]

def base_reta(rend):
    r = 0.93 * rend if rend > 0 else 0.0
    for i, (lim, b) in enumerate(TRAMOS):
        if lim is None or (r < lim if i == 2 else r <= lim): return b

DT7 = {2013: (423, 781), 2014: (426, 782), 2015: (429, 783), 2016: (432, 784), 2017: (435, 785), 2018: (438, 786), 2019: (441, 788), 2020: (444, 790),
       2021: (447, 792), 2022: (450, 794), 2023: (453, 796), 2024: (456, 798), 2025: (459, 800), 2026: (459, 802)}

def pct_br(c, y):                    # porcentaje de la BR por meses cotizados (DT 9.ª)
    x = c - 180
    if y >= 2027: return min(100.0, 50 + 0.19 * min(x, 248) + 0.18 * max(0, x - 248))
    return min(100.0, 50 + 0.21 * min(x, 49) + 0.19 * max(0, x - 49))

def eo_de(cot65, hc, anio):
    for m in range(780, 805):
        y = anio + (6 + m - hc) // 12
        um, ed = (462, 804) if y >= 2027 else DT7.get(y, (0, 780))
        if m >= (780 if cot65 + m - 780 >= um else ed): return m
    return 804

def pension(BR, cotm, dm, y):        # pension mensual (paga de 14) con demora dm meses
    pc = pct_br(cotm, y); yy, rem = divmod(dm, 12)
    extra = 4 * yy + (2 if (yy >= 2 and rem >= 7) else 0)
    pb = BR * pc / 100
    if pb >= MAXM: reg, sin = MAXM, extra
    else:
        raw = BR * (pc + extra) / 100
        if raw <= MAXM: reg, sin = raw, 0.0
        else: reg, sin = MAXM, pc + extra - MAXM / BR * 100
    return reg + max(0.0, min(sin / 100 * MAXM, TOPE / 14 - reg))

def nets(s, propia):
    if not propia: b = min(s, BMAX); return s - 0.0225 * b, s - 0.0025 * b
    b = base_reta(s); return s - (0.09 + 0.0156 + 0.013) * b, s - (0.0156 + 0.013) * b

def model(c):
    hc = round(c["edad_a"]) * 12 + round(c["edad_m"]); cotm = math.floor(c["cot"] * 12 + 1e-9)
    cot65 = cotm - (hc - 780)
    anio = round(c["anio"]); eo = eo_de(cot65, hc, anio)
    if hc < eo: return {"estado": 1, "ordM": eo}
    if cot65 + eo - 780 < 180: return {"estado": 3 if cotm >= 180 else 2, "ordM": eo}
    D = hc - eo; N = round(c["n"]); propia = c["tipo"] != "ajena"
    BR = min(c["pension"], MAXM) * 100 / pct_br(cotm, anio)
    P = pension(BR, cotm, D, anio)
    nA, nC = nets(c["salario"], propia)
    d = D // 12; activa = 1 if D >= 12 else 0
    base = {1: 45, 2: 55, 3: 65, 4: 80}.get(d, 100 if d >= 5 else 0)
    if c["tipo"] == "propia_contrata" and 1 <= d <= 3: base = 75
    TA = 0.0; TB = 0.0; TC = 0.0; perd = 0.0; pcts = []
    for t in range(12 * N):
        pt = min(100, base + 5 * (t // 12))
        pcts.append(pt)
        if activa: TA += P * pt / 100 * 14 / 12 + nA
        perd += (1 - pt / 100) * P * 14 / 12
        TB += P * 14 / 12; TC += nC
    P2 = pension(BR, cotm + 12 * N, D + 12 * N, anio + N); G = P2 - P
    best = max(TA, TB) if activa else TB
    eq = None
    if G > 1e-9: eq = (hc + 12 * N) / 12 + max(0.0, best - TC) / (G * 14 / 12) / 12
    umbral = None
    if activa:
        loss = perd / (12 * N)
        for s in range(0, 40001):
            if nets(s, propia)[0] >= loss - 1e-9: umbral = s; break
    out = {"estado": 0, "ordM": eo, "demora": D, "activa": activa, "pension": P, "pensionDemora": P2, "ganancia": G,
           "netoActiva": nA, "netoDemora": nC, "TB": TB, "TC": TC}
    if activa:
        out.update({"pctInicial": base, "pctFinal": pcts[-1], "TA": TA, "dif": TA - TB, "mensualA": TA / (12 * N), "umbral": umbral})
    out["eq"] = eq
    return out

def V(**k):
    d = dict(pension=2000, cot=40, edad_a=67, edad_m=0, anio=2027, salario=2000, tipo="ajena", n=3); d.update(k); return d
CASES = [
 ("1 base 2.000, 40 anos, 67: EO 65, demora 2 -> 55 %", V()),
 ("2 un ano justo de demora (66): 45 %", V(edad_a=66)),
 ("3 11 meses de demora: sin activa", V(edad_a=65, edad_m=11)),
 ("4 antes de la EO: bloqueo 1", V(edad_a=65, edad_m=0, cot=36)),
 ("5 carencia: 14 anos", V(cot=14, edad_a=70)),
 ("6 autonomo con contratacion, demora 3: 75 %", V(tipo="propia_contrata", edad_a=68, salario=2500)),
 ("7 autonomo sin contratar, demora 3: 65 %", V(tipo="propia", edad_a=68, salario=2500)),
 ("8 demora 5 anos: 100 %", V(edad_a=70)),
 ("9 demora 4 anos y contrata: escala 80 %", V(tipo="propia_contrata", edad_a=69)),
 ("10 pension maxima, 45 anos, demora 3", V(pension=3359.6, cot=45, edad_a=68, salario=3000)),
 ("11 cotizacion 30 anos (EO 67), edad 68: demora 1", V(cot=30, pension=1500, edad_a=68)),
 ("12 sueldo sobre base maxima", V(salario=7000, pension=2500)),
 ("13 HC 2026 a 67a9m, 35 cot: EO 66a8m en 2025 -> demora 13 m, 45 %", V(anio=2026, edad_a=67, edad_m=9, cot=35, pension=1500)),
 ("14 HC 2027 a 67a10m, 30 cot: EO 66a10m en 2026 -> demora 12 m", V(anio=2027, edad_a=67, edad_m=10, cot=30, pension=1500)),
 ("15 14 anos a la EO y 16 al HC (69): estado 3", V(edad_a=69, cot=16, anio=2026)),
 ("16 autonomo 2.500, neto sin pension solo IT+CP", V(tipo="propia", salario=2500, n=3)),
]
KEYS = ["ordM", "demora", "activa", "pension", "pensionDemora", "ganancia", "netoActiva", "netoDemora", "TB", "TC", "pctInicial", "pctFinal", "TA", "dif", "mensualA", "umbral", "eq"]

def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    if "--casos" in sys.argv:
        for n, c in CASES: print(n, json.dumps(model(c), ensure_ascii=False))
        sys.exit(0)
    rnd = random.Random(2610)
    sweep = []
    for _ in range(700):
        sweep.append(dict(pension=rnd.choice([600, 900, 1300, 1800, 2400, 3000, 3359.6, rnd.uniform(500, 3359.6)]), cot=rnd.choice([14.5, 15, 20, 30, 36, 37, 38, 38.5, 40, 45, rnd.uniform(15, 48)]),
            edad_a=rnd.randint(65, 76), edad_m=rnd.randint(0, 11), anio=rnd.randint(2026, 2031), salario=rnd.choice([300, 800, 1200, 1500, 2000, 3000, 5101.2, 6500, rnd.uniform(200, 8000)]),
            tipo=rnd.choice(["ajena", "propia", "propia_contrata"]), n=rnd.randint(1, 15)))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0; compared = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("estado") != o["estado"]: print("ESTADO", c, j.get("estado"), o["estado"]); bad += 1; continue
        if o["estado"]: continue
        for k in KEYS:
            if k not in o and k not in j: continue
            a, b = o.get(k), j.get(k)
            if (a is None) != (b is None) or (a is not None and (not isinstance(b, (int, float)) or abs(a - b) > (0.01 if k in ("ordM", "demora", "activa", "pctInicial", "pctFinal") else (0.05 if k == "eq" else 1)))):
                print("DIF", k, c, "oraculo", a, "js", b); bad += 1
            compared += 1
    print("casos %d, comparaciones %d, discrepancias %d" % (len(allc), compared, bad)); sys.exit(1 if bad else 0)
