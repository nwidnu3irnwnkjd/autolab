#!/usr/bin/env python3
"""Oraculo independiente: jubilarse-en-2026-o-en-2027-edad-y-pension. Escrito desde la norma (LGSS arts. 205.1, 209.1, 210.1-2; DT 4.ª.7, 7.ª, 9.ª, 40.ª) ANTES del .js.
INTERPRETACION
- Fecha de referencia: 1-oct-2026 (mes 0 = oct 2026). Cotizacion acreditada c(t) = cot0 + (t - oct 2026) meses completos: se supone cotizacion continuada hasta el hecho causante (mes t).
- Edad exigida en el mes t (art. 205.1.a + DT 7.ª, segun el AÑO del hecho causante): 65 años (780 m) si c(t) >= 38a3m (459) en 2026 / 38a6m (462) desde 2027; si no, 66a10m (802) en 2026 / 67a (804) desde 2027. Se puede causar en t si edad en meses (t - nacimiento) >= exigida, y c(t) >= 180 (art. 205.1.b; los 2 de los ultimos 15 años se suponen cumplidos).
- Dos opciones comparadas: primer mes posible dentro de 2026 (>= oct) y primer mes posible dentro de 2027; si ninguno, se informa el primer mes posible en cualquier año hasta 2036.
- Porcentaje (art. 210.1 + DT 9.ª): 50 % por 15 años + por cada mes adicional: 2026 -> 0,21 los primeros 49 y 0,19 los siguientes; desde 2027 -> 0,19 los primeros 248 y 0,18 los siguientes; tope 100 %.
- Revalorizacion (art. 58.2): la pension causada en 2026 se revaloriza en enero de 2027 (hipotesis 2,7 %, la de 2026, RD 241/2026): a26_pension_ene27 = a26_pension x 1,027; se compara con a27_pension (que ya nace en 2027). La maxima aplicable en 2027 y despues es la de 2026 x 1,027 (hipotesis). dif = a27_pension - a26_pension_ene27; equilibrio = a26_pension x (meses entre ambos primeros meses) / dif si dif > 0.
- Fecha de referencia movil: ref (mes absoluto, por defecto oct 2026); la cotizacion se cuenta a dia 1 de ese mes.
- Demora (art. 210.2.a): NO se calcula. Cota S1: ademas de d con la regla del año del hecho causante, d' = meses desde el primer mes de un año anterior (2024 en adelante, hasta el año previo al hecho causante) en que ya se cumplia la edad exigida ESE año con la cotizacion de entonces (DT 7.ª 2024: 38 a o 66a6m; 2025: 38a3m o 66a8m); demoraPosible si max(d, d') >= 12.
- (anterior) Demora: NO se calcula. d = t - nacimiento - edad exigida en t (meses por encima de la edad exigida) es una COTA SUPERIOR de la demora real (la norma no aclara si la edad se mide con la cotizacion del hecho causante o con la de entonces). Si d >= 12 en algun escenario se marca demoraPosible=1 y la pagina no emite veredicto de «conviene»; con d < 12 no hay año completo de demora bajo ninguna lectura.
- Base reguladora: bases en euros de hoy: ultimos 60 meses = b_rec, anteriores = b_ant, desde el 2.º mes anterior al hecho causante (t-2 hacia atras). DT 40.ª: suma de las n mejores de N meses / divisor (2026 302/304/352,33; 2027 304/308/354,67; ...). DT 4.ª.7: tambien la regla de 2023 (300 meses / 350) y se aplica la mas favorable. Si c(t) < N+1 la ventana tendria lagunas (no modeladas): pension no calculada.
- Pension = min(BR x pct/100 (sin demora), maxima 2026 3.359,60 EUR/mes en 14 pagas). Sin maxima 2027 publicada: se usa la de 2026. Imposibles: cot < 15 años en todo el año (carencia), nacimiento fuera de rango.
"""
import json, random, subprocess, sys, os
M0 = 2026 * 12 + 9
REVAL = 0.027
ED = {2024: (456, 798), 2025: (459, 800), 2026: (459, 802)}
MAXP = 3359.60
DT40 = {2026: (302, 304, 352.33), 2027: (304, 308, 354.67), 2028: (306, 312, 357.00), 2029: (308, 316, 359.33), 2030: (310, 320, 361.67),
        2031: (312, 324, 364.00), 2032: (314, 328, 366.33), 2033: (316, 332, 368.67), 2034: (318, 336, 371.00), 2035: (320, 340, 373.33), 2036: (322, 344, 375.67)}
def req_age(t, c):
    y = t // 12
    if y in ED: return 780 if c >= ED[y][0] else ED[y][1]
    return 780 if c >= 462 else 804
def pct_base(t, c):
    y = t // 12; x = c - 180
    if y == 2026: p = 50 + 0.21 * min(x, 49) + 0.19 * max(0, x - 49)
    else: p = 50 + 0.19 * min(x, 248) + 0.18 * max(0, x - 248)
    return min(100.0, p)
def br_at(t, c, brec, bant):
    y = t // 12
    n, N, div = DT40[y] if y in DT40 else (324, 348, 378)
    if c < N + 1: return None
    bases = [brec if k < 60 else bant for k in range(N)]
    new = sum(sorted(bases, reverse=True)[:n]) / div
    old = sum(brec if k < 60 else bant for k in range(300)) / 350
    return max(new, old), new, old
def pension_at(t, B, cot0, brec, bant, m0=M0):
    c = cot0 + t - m0
    R = req_age(t, c); d = t - B - R
    o = dict(t=t, cot=c, req=R, demora=d)
    o["pct"] = pct_base(t, c)
    r = br_at(t, c, brec, bant)
    if r is None: o["br"] = None; o["pension"] = None
    else:
        o["br"], o["brNew"], o["brOld"] = r
        full = o["br"] * o["pct"] / 100
        o["pension"] = min(full, MAXP if t // 12 == 2026 else MAXP * (1 + REVAL))
    # cota S1: primer mes de un año anterior (>= 2024) en que ya se cumplia la edad exigida de ese año con la cotizacion de entonces
    dalt = 0
    for y in range(2024, min(t // 12, 2027)):
        for mm in range(y * 12, y * 12 + 12):
            cc = cot0 + mm - m0
            if mm <= t and mm - B >= req_age(mm, cc) and cc >= 180:
                dalt = max(dalt, t - mm); break
    o["demoraAlt"] = dalt
    return o
def primero(B, cot0, lo, hi, m0=M0):
    ageok = False
    for t in range(lo, hi + 1):
        c = cot0 + t - m0
        if t - B >= req_age(t, c):
            ageok = True
            if c >= 180: return t, 0
    return None, (2 if ageok else 1)
def oraculo(d):
    na, nm, ca, cm = int(d["nac_a"]), int(d["nac_m"]), int(d["cot_a"]), int(d["cot_m"])
    brec, bant = float(d["b_rec"]), float(d["b_ant"])
    if not (1955 <= na <= 1966 and 1 <= nm <= 12 and 0 <= ca <= 60 and 0 <= cm <= 11 and 0 < brec <= 5101.2 and 0 < bant <= 5101.2): return dict(bloqueado=1)
    B = na * 12 + nm - 1; cot0 = ca * 12 + cm
    m0 = int(d.get("ref", M0))
    if m0 >= 2027 * 12: return dict(bloqueado=2)
    out = dict(bloqueado=0)
    for Y in (2026, 2027):
        lo = max(m0, Y * 12); hi = Y * 12 + 11
        t, est = primero(B, cot0, lo, hi, m0)
        k = "a%d_" % (Y % 100)
        out[k + "estado"] = est
        if t is None: continue
        p = pension_at(t, B, cot0, brec, bant, m0)
        out[k + "t"] = t; out[k + "req"] = p["req"]; out[k + "cot"] = p["cot"]; out[k + "pct"] = p["pct"]; out[k + "demora"] = p["demora"]; out[k + "demoraAlt"] = p["demoraAlt"]
        if p["pension"] is None: out[k + "estado"] = 3
        else:
            out[k + "br"] = p["br"]; out[k + "brNew"] = p["brNew"]; out[k + "brOld"] = p["brOld"]; out[k + "pension"] = p["pension"]
    tf, est = primero(B, cot0, m0, 2036 * 12 + 11, m0)
    out["pf_t"] = -1 if tf is None else tf
    if tf is not None:
        p = pension_at(tf, B, cot0, brec, bant, m0)
        out["pf_req"] = p["req"]; out["pf_cot"] = p["cot"]; out["pf_pct"] = p["pct"]
        if p["pension"] is not None: out["pf_pension"] = p["pension"]
    out["demoraPosible"] = 1 if max(out.get("a26_demora", 0), out.get("a26_demoraAlt", 0), out.get("a27_demora", 0), out.get("a27_demoraAlt", 0)) >= 12 else 0
    if out.get("a26_pension") is not None and out.get("a27_pension") is not None:
        p6, p7 = out["a26_pension"], out["a27_pension"]; m = out["a27_t"] - out["a26_t"]
        out["a26_pension_ene27"] = p6 * (1 + REVAL)
        out["dif"] = p7 - out["a26_pension_ene27"]
        if out["dif"] > 1e-9: out["equilibrio"] = p6 * m / out["dif"]
    return out
def genera(n, seed=2027):
    random.seed(seed); cs = []
    for _ in range(n):
        cs.append(dict(nac_a=random.randint(1955, 1966), nac_m=random.randint(1, 12), cot_a=random.randint(10, 48), cot_m=random.randint(0, 11),
                       b_rec=round(random.uniform(900, 5101.2), 2), b_ant=round(random.uniform(900, 5101.2), 2), **({} if random.random() < .6 else dict(ref=random.choice([M0 + 1, M0 + 2, M0 + 3])))))
    return cs
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/jubilarse-en-2026-o-en-2027-edad-y-pension.js")).read().split("function eur(")[0]
    cases = genera(1200)
    # barrido fino de bordes: todas las fechas de nacimiento 1959-1962 x cotizacion 36a-39a en pasos de mes (umbrales 38a3m/38a6m, 15 años, ventana)
    for na in (1959, 1960, 1961, 1962):
        for nm in range(1, 13):
            for c in (455, 458, 459, 460, 461, 462, 463, 467, 473, 180, 179, 300, 304, 305, 309):
                cases.append(dict(nac_a=na, nac_m=nm, cot_a=c // 12, cot_m=c % 12, b_rec=3000, b_ant=2200))
    cases += [dict(nac_a=1960, nac_m=1, cot_a=35, cot_m=0, b_rec=2000, b_ant=4000), dict(nac_a=1955, nac_m=1, cot_a=45, cot_m=0, b_rec=5101.2, b_ant=5101.2),
              dict(nac_a=1966, nac_m=12, cot_a=60, cot_m=11, b_rec=1, b_ant=1), dict(nac_a=1954, nac_m=1, cot_a=30, cot_m=0, b_rec=2000, b_ant=2000), dict(nac_a=1960, nac_m=1, cot_a=35, cot_m=0, b_rec=0, b_ant=2000), dict(nac_a=1960, nac_m=1, cot_a=35, cot_m=0, b_rec=3000, b_ant=2200, ref=2027 * 12)]
    for m in (2, 3, 4, 5, 6):
        cases.append(dict(nac_a=1959, nac_m=m, cot_a=36, cot_m=0, b_rec=3000, b_ant=2200))
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0; both = 0; tot = 0
    for c, r in zip(cases, res):
        o = oraculo(c); tot += 1
        if o.get("a26_pension") is not None and o.get("a27_pension") is not None: both += 1
        for k, v in o.items():
            if r.get(k) is None or abs(r[k] - v) > 0.01: bad += 1; print("DIF", c, k, r.get(k), v)
        for k in r:
            if k not in o and r[k] is not None and isinstance(r[k], (int, float)) and k not in ("ok",): bad += 1; print("EXTRA", c, k, r[k])
    print(f"{tot} casos, ambos escenarios con pension: {both}, discrepancias: {bad}"); sys.exit(1 if bad else 0)
