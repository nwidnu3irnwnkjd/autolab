#!/usr/bin/env python3
"""Oraculo independiente de jubilacion-anticipada-o-demorada (escrito desde la norma antes que el JS).
Norma: LGSS (RDL 8/2015, consolidado a 31/07/2026): art. 205.1, 208, 210, DT 7.ª, DT 9.ª; RD 241/2026 (maxima 3.359,60 EUR/mes, minimas).
Uso: python3 ops/verif/jubilacion-anticipada-o-demorada.py [N_aleatorios]   -> compara con el JS (JavaScriptCore) y sale 1 si hay discrepancias > 1 EUR."""
import json, math, os, random, subprocess, sys

MAX0, TOPE0 = 3359.60, 61214.40       # RD 241/2026 ; 12 x 5.101,20 (Orden PJC/297/2026)
MIN_BAJA, MIN_ALTA = 12441.80, 17592.40  # RD 241/2026: minimo jubilacion 65+, conyuge no a cargo / a cargo (EUR/ano)
REF_Y, REF_M = 2026, 9                 # referencia: octubre de 2026 (indice 9)
# DT 7.ª: ano -> (umbral cotizado en meses para 65 anos, edad exigida en meses si no llega)
DT7 = {2013: (423, 781), 2014: (426, 782), 2015: (429, 783), 2016: (432, 784), 2017: (435, 785), 2018: (438, 786),
       2019: (441, 788), 2020: (444, 790), 2021: (447, 792), 2022: (450, 794), 2023: (453, 796), 2024: (456, 798),
       2025: (459, 800), 2026: (459, 802)}
COEF = {  # meses de anticipo -> % por columna de cotizacion
 24: (21.00, 19.00, 17.00, 13.00), 23: (17.60, 16.50, 15.00, 12.00), 22: (14.67, 14.00, 13.33, 11.00), 21: (12.57, 12.00, 11.43, 10.00),
 20: (11.00, 10.50, 10.00, 9.20), 19: (9.78, 9.33, 8.89, 8.40), 18: (8.80, 8.40, 8.00, 7.60), 17: (8.00, 7.64, 7.27, 6.91),
 16: (7.33, 7.00, 6.67, 6.33), 15: (6.77, 6.46, 6.15, 5.85), 14: (6.29, 6.00, 5.71, 5.43), 13: (5.87, 5.60, 5.33, 5.07),
 12: (5.50, 5.25, 5.00, 4.75), 11: (5.18, 4.94, 4.71, 4.47), 10: (4.89, 4.67, 4.44, 4.22), 9: (4.63, 4.42, 4.21, 4.00),
 8: (4.40, 4.20, 4.00, 3.80), 7: (4.19, 4.00, 3.81, 3.62), 6: (4.00, 3.82, 3.64, 3.45), 5: (3.83, 3.65, 3.48, 3.30),
 4: (3.67, 3.50, 3.33, 3.17), 3: (3.52, 3.36, 3.20, 3.04), 2: (3.38, 3.23, 3.08, 2.92), 1: (3.26, 3.11, 2.96, 2.81)}

# DT 34.ª (transcrita del BOE): meses de anticipo -> [anio 2024..2033][columna] (%), aplicacion gradual del 2.º parrafo del art. 210.3 (pension > maxima)
DT34 = {
 1: [[0.78, 0.76, 0.75, 0.73], [1.05, 1.02, 0.99, 0.96], [1.33, 1.28, 1.24, 1.19], [1.6, 1.54, 1.48, 1.42], [1.88, 1.81, 1.73, 1.66], [2.16, 2.07, 1.98, 1.89], [2.43, 2.33, 2.22, 2.12], [2.71, 2.59, 2.47, 2.35], [2.98, 2.85, 2.71, 2.58], [3.26, 3.11, 2.96, 2.81]],
 2: [[0.79, 0.77, 0.76, 0.74], [1.08, 1.05, 1.02, 0.98], [1.36, 1.32, 1.27, 1.23], [1.65, 1.59, 1.53, 1.47], [1.94, 1.87, 1.79, 1.71], [2.23, 2.14, 2.05, 1.95], [2.52, 2.41, 2.31, 2.19], [2.8, 2.68, 2.56, 2.44], [3.09, 2.96, 2.82, 2.68], [3.38, 3.23, 3.08, 2.92]],
 3: [[0.8, 0.79, 0.77, 0.75], [1.1, 1.07, 1.04, 1.01], [1.41, 1.36, 1.31, 1.26], [1.71, 1.64, 1.58, 1.52], [2.01, 1.93, 1.85, 1.77], [2.31, 2.22, 2.12, 2.02], [2.61, 2.5, 2.39, 2.28], [2.92, 2.79, 2.66, 2.53], [3.22, 3.07, 2.93, 2.79], [3.52, 3.36, 3.2, 3.04]],
 4: [[1.27, 1.25, 1.23, 1.22], [1.53, 1.5, 1.47, 1.43], [1.8, 1.75, 1.7, 1.65], [2.07, 2.0, 1.93, 1.87], [2.34, 2.25, 2.17, 2.09], [2.6, 2.5, 2.4, 2.3], [2.87, 2.75, 2.63, 2.52], [3.14, 3.0, 2.86, 2.74], [3.4, 3.25, 3.1, 2.95], [3.67, 3.5, 3.33, 3.17]],
 5: [[1.28, 1.27, 1.25, 1.23], [1.57, 1.53, 1.5, 1.46], [1.85, 1.8, 1.74, 1.69], [2.13, 2.06, 1.99, 1.92], [2.42, 2.33, 2.24, 2.15], [2.7, 2.59, 2.49, 2.38], [2.98, 2.86, 2.74, 2.61], [3.26, 3.12, 2.98, 2.84], [3.55, 3.39, 3.23, 3.07], [3.83, 3.65, 3.48, 3.3]],
 6: [[1.3, 1.28, 1.26, 1.25], [1.6, 1.56, 1.53, 1.49], [1.9, 1.85, 1.79, 1.74], [2.2, 2.13, 2.06, 1.98], [2.5, 2.41, 2.32, 2.23], [2.8, 2.69, 2.58, 2.47], [3.1, 2.97, 2.85, 2.72], [3.4, 3.26, 3.11, 2.96], [3.7, 3.54, 3.38, 3.21], [4.0, 3.82, 3.64, 3.45]],
 7: [[1.77, 1.75, 1.73, 1.71], [2.04, 2.0, 1.96, 1.92], [2.31, 2.25, 2.19, 2.14], [2.58, 2.5, 2.42, 2.35], [2.85, 2.75, 2.66, 2.56], [3.11, 3.0, 2.89, 2.77], [3.38, 3.25, 3.12, 2.98], [3.65, 3.5, 3.35, 3.2], [3.92, 3.75, 3.58, 3.41], [4.19, 4.0, 3.81, 3.62]],
 8: [[1.79, 1.77, 1.75, 1.73], [2.08, 2.04, 2.0, 1.96], [2.37, 2.31, 2.25, 2.19], [2.66, 2.58, 2.5, 2.42], [2.95, 2.85, 2.75, 2.65], [3.24, 3.12, 3.0, 2.88], [3.53, 3.39, 3.25, 3.11], [3.82, 3.66, 3.5, 3.34], [4.11, 3.93, 3.75, 3.57], [4.4, 4.2, 4.0, 3.8]],
 9: [[1.81, 1.79, 1.77, 1.75], [2.13, 2.08, 2.04, 2.0], [2.44, 2.38, 2.31, 2.25], [2.75, 2.67, 2.58, 2.5], [3.07, 2.96, 2.86, 2.75], [3.38, 3.25, 3.13, 3.0], [3.69, 3.54, 3.4, 3.25], [4.0, 3.84, 3.67, 3.5], [4.32, 4.13, 3.94, 3.75], [4.63, 4.42, 4.21, 4.0]],
 10: [[2.29, 2.27, 2.24, 2.22], [2.58, 2.53, 2.49, 2.44], [2.87, 2.8, 2.73, 2.67], [3.16, 3.07, 2.98, 2.89], [3.45, 3.34, 3.22, 3.11], [3.73, 3.6, 3.46, 3.33], [4.02, 3.87, 3.71, 3.55], [4.31, 4.14, 3.95, 3.78], [4.6, 4.4, 4.2, 4.0], [4.89, 4.67, 4.44, 4.22]],
 11: [[2.32, 2.29, 2.27, 2.25], [2.64, 2.59, 2.54, 2.49], [2.95, 2.88, 2.81, 2.74], [3.27, 3.18, 3.08, 2.99], [3.59, 3.47, 3.36, 3.24], [3.91, 3.76, 3.63, 3.48], [4.23, 4.06, 3.9, 3.73], [4.54, 4.35, 4.17, 3.98], [4.86, 4.65, 4.44, 4.22], [5.18, 4.94, 4.71, 4.47]],
 12: [[2.35, 2.33, 2.3, 2.28], [2.7, 2.65, 2.6, 2.55], [3.05, 2.98, 2.9, 2.83], [3.4, 3.3, 3.2, 3.1], [3.75, 3.63, 3.5, 3.38], [4.1, 3.95, 3.8, 3.65], [4.45, 4.28, 4.1, 3.93], [4.8, 4.6, 4.4, 4.2], [5.15, 4.93, 4.7, 4.48], [5.5, 5.25, 5.0, 4.75]],
 13: [[2.84, 2.81, 2.78, 2.76], [3.17, 3.12, 3.07, 3.01], [3.51, 3.43, 3.35, 3.27], [3.85, 3.74, 3.63, 3.53], [4.19, 4.05, 3.92, 3.79], [4.52, 4.36, 4.2, 4.04], [4.86, 4.67, 4.48, 4.3], [5.2, 4.98, 4.76, 4.56], [5.53, 5.29, 5.05, 4.81], [5.87, 5.6, 5.33, 5.07]],
 14: [[2.88, 2.85, 2.82, 2.79], [3.26, 3.2, 3.14, 3.09], [3.64, 3.55, 3.46, 3.38], [4.02, 3.9, 3.78, 3.67], [4.4, 4.25, 4.11, 3.97], [4.77, 4.6, 4.43, 4.26], [5.15, 4.95, 4.75, 4.55], [5.53, 5.3, 5.07, 4.84], [5.91, 5.65, 5.39, 5.14], [6.29, 6.0, 5.71, 5.43]],
 15: [[2.93, 2.9, 2.87, 2.84], [3.35, 3.29, 3.23, 3.17], [3.78, 3.69, 3.6, 3.51], [4.21, 4.08, 3.96, 3.84], [4.64, 4.48, 4.33, 4.18], [5.06, 4.88, 4.69, 4.51], [5.49, 5.27, 5.06, 4.85], [5.92, 5.67, 5.42, 5.18], [6.34, 6.06, 5.79, 5.52], [6.77, 6.46, 6.15, 5.85]],
 16: [[3.43, 3.4, 3.37, 3.33], [3.87, 3.8, 3.73, 3.67], [4.3, 4.2, 4.1, 4.0], [4.73, 4.6, 4.47, 4.33], [5.17, 5.0, 4.84, 4.67], [5.6, 5.4, 5.2, 5.0], [6.03, 5.8, 5.57, 5.33], [6.46, 6.2, 5.94, 5.66], [6.9, 6.6, 6.3, 6.0], [7.33, 7.0, 6.67, 6.33]],
 17: [[3.5, 3.46, 3.43, 3.39], [4.0, 3.93, 3.85, 3.78], [4.5, 4.39, 4.28, 4.17], [5.0, 4.86, 4.71, 4.56], [5.5, 5.32, 5.14, 4.96], [6.0, 5.78, 5.56, 5.35], [6.5, 6.25, 5.99, 5.74], [7.0, 6.71, 6.42, 6.13], [7.5, 7.18, 6.84, 6.52], [8.0, 7.64, 7.27, 6.91]],
 18: [[3.58, 3.54, 3.5, 3.46], [4.16, 4.08, 4.0, 3.92], [4.74, 4.62, 4.5, 4.38], [5.32, 5.16, 5.0, 4.84], [5.9, 5.7, 5.5, 5.3], [6.48, 6.24, 6.0, 5.76], [7.06, 6.78, 6.5, 6.22], [7.64, 7.32, 7.0, 6.68], [8.22, 7.86, 7.5, 7.14], [8.8, 8.4, 8.0, 7.6]],
 19: [[4.13, 4.08, 4.04, 3.99], [4.76, 4.67, 4.58, 4.48], [5.38, 5.25, 5.12, 4.97], [6.01, 5.83, 5.66, 5.46], [6.64, 6.42, 6.2, 5.95], [7.27, 7.0, 6.73, 6.44], [7.9, 7.58, 7.27, 6.93], [8.52, 8.16, 7.81, 7.42], [9.15, 8.75, 8.35, 7.91], [9.78, 9.33, 8.89, 8.4]],
 20: [[4.25, 4.2, 4.15, 4.07], [5.0, 4.9, 4.8, 4.64], [5.75, 5.6, 5.45, 5.21], [6.5, 6.3, 6.1, 5.78], [7.25, 7.0, 6.75, 6.35], [8.0, 7.7, 7.4, 6.92], [8.75, 8.4, 8.05, 7.49], [9.5, 9.1, 8.7, 8.06], [10.25, 9.8, 9.35, 8.63], [11.0, 10.5, 10.0, 9.2]],
 21: [[4.41, 4.35, 4.29, 4.15], [5.31, 5.2, 5.09, 4.8], [6.22, 6.05, 5.88, 5.45], [7.13, 6.9, 6.67, 6.1], [8.04, 7.75, 7.47, 6.75], [8.94, 8.6, 8.26, 7.4], [9.85, 9.45, 9.05, 8.05], [10.76, 10.3, 9.84, 8.7], [11.66, 11.15, 10.64, 9.35], [12.57, 12.0, 11.43, 10.0]],
 22: [[5.07, 5.0, 4.93, 4.7], [6.13, 6.0, 5.87, 5.4], [7.2, 7.0, 6.8, 6.1], [8.27, 8.0, 7.73, 6.8], [9.34, 9.0, 8.67, 7.5], [10.4, 10.0, 9.6, 8.2], [11.47, 11.0, 10.53, 8.9], [12.54, 12.0, 11.46, 9.6], [13.6, 13.0, 12.4, 10.3], [14.67, 14.0, 13.33, 11.0]],
 23: [[5.36, 5.25, 5.1, 4.8], [6.72, 6.5, 6.2, 5.6], [8.08, 7.75, 7.3, 6.4], [9.44, 9.0, 8.4, 7.2], [10.8, 10.25, 9.5, 8.0], [12.16, 11.5, 10.6, 8.8], [13.52, 12.75, 11.7, 9.6], [14.88, 14.0, 12.8, 10.4], [16.24, 15.25, 13.9, 11.2], [17.6, 16.5, 15.0, 12.0]],
 24: [[5.7, 5.5, 5.3, 4.9], [7.4, 7.0, 6.6, 5.8], [9.1, 8.5, 7.9, 6.7], [10.8, 10.0, 9.2, 7.6], [12.5, 11.5, 10.5, 8.5], [14.2, 13.0, 11.8, 9.4], [15.9, 14.5, 13.1, 10.3], [17.6, 16.0, 14.4, 11.2], [19.3, 17.5, 15.7, 12.1], [21.0, 19.0, 17.0, 13.0]],
}

def anio(m, age_m):
    return REF_Y + (REF_M + (m - age_m)) // 12

def ordinaria(age_m, cot_m):
    for m in range(780, 805):
        y = anio(m, age_m); c = cot_m + (m - age_m)
        if y >= 2027: um, ed = 462, 804
        elif y < 2013: um, ed = 0, 780
        else: um, ed = DT7[y]
        req = 780 if c >= um else ed
        if m >= req: return m
    return 804

def pct_base(c, y):
    if c < 180: return None
    if y >= 2027: a, ra, rb = 248, 0.19, 0.18
    elif y >= 2023: a, ra, rb = 49, 0.21, 0.19
    elif y >= 2020: a, ra, rb = 106, 0.21, 0.19
    else: a, ra, rb = 163, 0.21, 0.19
    x = c - 180
    p = 50 + min(x, a) * ra + max(0, x - a) * rb
    # tramo final: el segundo tipo solo cubre los meses que llevan al 100 %
    return min(p, 100.0)

def pension_inicial(m, ord_m, age_m, cot_m, br, g):
    """Devuelve (estado, pension mensual bruta en 14 pagas al causar)."""
    c = cot_m + (m - age_m); y = anio(m, age_m)
    pc = pct_base(c, y)
    if pc is None: return ("carencia", None)
    f = (1 + g) ** ((m - age_m) / 12.0)
    brn, mx, tope = br * f, MAX0 * f, TOPE0 * f
    pb = brn * pc / 100.0
    if m < ord_m:
        ant = ord_m - m
        if ant > 24: return ("antic24", None)
        if c < 420: return ("antic35", None)
        col = 0 if c < 462 else (1 if c < 498 else (2 if c < 534 else 3))
        # pension teorica > maxima: coeficiente sobre la maxima, gradual por anio del hecho causante (DT 34.ª); desde 2033 el cuadro del 208.2
        cf = (DT34[ant][min(max(y, 2024), 2033) - 2024][col]) if pb > mx else COEF[ant][col]
        p = min(pb, mx) * (1 - cf / 100.0)
        real = p / f * 14
        if real <= MIN_BAJA: return ("minima", None)
        return ("ok", p)
    if m == ord_m: return ("ok", min(pb, mx))
    d = m - ord_m
    if cot_m + (ord_m - age_m) < 180: extra = 0.0           # sin 15 anos al cumplir la edad ordinaria: sin complemento
    else:
        yy, rem = divmod(d, 12)
        extra = 4.0 * yy + (2.0 if (yy >= 2 and rem >= 7) else 0.0)
    if pb >= mx: reg, sin = mx, extra
    else:
        raw = brn * (pc + extra) / 100.0
        if raw <= mx: reg, sin = raw, 0.0
        else: reg, sin = mx, (pc + extra) - mx / brn * 100.0
    comp = sin / 100.0 * mx
    comp = max(0.0, min(comp, tope / 14.0 - reg))
    return ("ok", reg + comp)

def acumulado(start, p0, end_m, age_m, g, net, hasta=None):
    """Serie de acumulado neto por mes natural desde start hasta hasta (exclusive)."""
    out = {}; acc = 0.0; fac = 1.0
    for mm in range(start, hasta if hasta else end_m):
        if mm > start and (REF_M + (mm - age_m)) % 12 == 0: fac *= (1 + g)
        acc += p0 * fac * 14.0 / 12.0 * net
        out[mm] = acc
    return out

def calcular(d):
    age_m = round(d["edad"] * 12); cot_m = math.floor(d["cot"] * 12 + 1e-9)
    m = int(d["eleg_a"]) * 12 + int(d["eleg_m"]); end_m = round(d["fin"] * 12)
    g = d["ipc"] / 100.0; net = 1 - d["irpf"] / 100.0; br = d["br"]
    o = ordinaria(age_m, cot_m)
    res = {"ordM": o}
    if m < age_m: res["estado"] = "pasado"; return res
    if o < age_m: res["estado"] = "ord_pasada"; return res
    s_o, p_o = pension_inicial(o, o, age_m, cot_m, br, g)
    if s_o != "ok": res["estado"] = "carencia_ord"; return res
    s, p = pension_inicial(m, o, age_m, cot_m, br, g)
    res["estado"] = s; res["pensionOrdinaria"] = p_o
    if s != "ok": return res
    res["pensionElegida"] = p
    if m < o:  # art. 208.1.a con la cotizacion real a la fecha elegida (sin seguir cotizando)
        yy = anio(m, age_m); cc = cot_m + (m - age_m)
        um, ed = (462, 804) if yy >= 2027 else (0, 780) if yy < 2013 else DT7[yy]
        res["ordRealM"] = 780 if cc >= um else ed
    else: res["ordRealM"] = o
    f = (1 + g) ** ((m - age_m) / 12.0)
    real_ord_anual = p_o / ((1 + g) ** ((o - age_m) / 12.0)) * 14
    res["aviso_minima"] = 1 if (m < o and p / f * 14 <= MIN_ALTA) else 0
    A = acumulado(m, p, end_m, age_m, g, net); B = acumulado(o, p_o, end_m, age_m, g, net)
    res["acumElegida"] = A[end_m - 1] if (end_m - 1) in A else 0.0
    res["acumOrdinaria"] = B[end_m - 1] if (end_m - 1) in B else 0.0
    res["diferencia"] = res["acumElegida"] - res["acumOrdinaria"]
    if m == o: res["equilibrioEdad"] = None; return res
    (se, pe), (sl, pl) = ((m, p), (o, p_o)) if m < o else ((o, p_o), (m, p))
    top = 1320
    E = acumulado(se, pe, 0, age_m, g, net, top); L = acumulado(sl, pl, 0, age_m, g, net, top)
    eq = None
    for mm in range(sl, top):
        if L[mm] >= E[mm]: eq = (mm + 1) / 12.0; break
    res["equilibrioEdad"] = eq
    return res

CASOS_FIJOS = [
 {"edad": 60, "cot": 30, "br": 2500, "eleg_a": 65, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 2.7},
 # escenarios del verificador (journal/verificacion-jubilacion.md), ipc 0, irpf 0, fin 85
 {"edad": 63, "cot": 37, "br": 5000, "eleg_a": 64, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 0},
 # el 61/34/6000->65 del informe supone edad ordinaria 67, pero con cotizacion continuada se llega a 38a6m a los 65a6m (ordinaria 65a6m, 6 meses de anticipo, 3,10 %); se usa 63/34 para anticipo de 24 meses en 2028
 {"edad": 63, "cot": 34, "br": 6000, "eleg_a": 65, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 0},
 {"edad": 63, "cot": 42, "br": 6000, "eleg_a": 64, "eleg_m": 0, "fin": 90, "irpf": 0, "ipc": 2},
 {"edad": 66, "cot": 40, "br": 3000, "eleg_a": 68, "eleg_m": 8, "fin": 88, "irpf": 0, "ipc": 2.7},
 {"edad": 61, "cot": 36, "br": 2500, "eleg_a": 63, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 0},
]
ESPERADO_VERIFICADOR = [  # (indice en CASOS_FIJOS, pensionElegida, pensionOrdinaria) calculados a mano por el verificador desde la norma
 (1, 3245.37, 3359.60), (2, 2939.65, 3359.60)]

def aleatorio(r):
    edad = r.randint(50, 72); cot = round(r.uniform(15, 48), 2)
    br = r.choice([900, 1500, 2000, 2500, 3200, 4000, 5000, 7000]) * r.uniform(0.8, 1.2)
    eleg_a = r.randint(max(edad, 60), 74); eleg_m = r.randint(0, 11)
    return {"edad": edad, "cot": cot, "br": round(br, 2), "eleg_a": eleg_a, "eleg_m": eleg_m,
            "fin": r.randint(eleg_a + 1, 100), "irpf": r.choice([0, 8, 15, 20]), "ipc": r.choice([0, 1, 2, 2.7, 3.5])}

def ejecutar_js(casos):
    slug = "jubilacion-anticipada-o-demorada"
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(root, "projects", "decidir", "calcs", slug + ".js")).read().split("function eur(")[0]
    h = js + "\nJSON.stringify(" + json.dumps(casos) + ".map(function(c){return calcular(c);}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout.strip())

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    r = random.Random(20261002)
    casos = CASOS_FIJOS + [aleatorio(r) for _ in range(n)]
    # forzar bordes: carencia, justo en ordinaria, 0 meses, demora > 70, pension maxima
    casos += [
     {"edad": 60, "cot": 14.9, "br": 2000, "eleg_a": 67, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 2.7},
     {"edad": 60, "cot": 15, "br": 2000, "eleg_a": 67, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 2.7},
     {"edad": 62, "cot": 40, "br": 3000, "eleg_a": 65, "eleg_m": 0, "fin": 90, "irpf": 10, "ipc": 2},
     {"edad": 65, "cot": 45, "br": 6000, "eleg_a": 72, "eleg_m": 5, "fin": 95, "irpf": 0, "ipc": 2.7},
     {"edad": 66, "cot": 38.5, "br": 5200, "eleg_a": 71, "eleg_m": 0, "fin": 90, "irpf": 0, "ipc": 0},
    ]
    sal = ejecutar_js(casos); mal = 0; estados = {}
    for i, pe, po in ESPERADO_VERIFICADOR:
        for nm, v in (("pensionElegida", pe), ("pensionOrdinaria", po)):
            if abs(sal[i][nm] - v) > 1.0 or abs(calcular(casos[i])[nm] - v) > 1.0: mal += 1; print("VERIFICADOR", casos[i], nm, v, sal[i].get(nm), calcular(casos[i]).get(nm)); estados = {}
    for c, j in zip(casos, sal):
        p = calcular(c); estados[p["estado"]] = estados.get(p["estado"], 0) + 1
        if p["estado"] != j.get("estado") or p["ordM"] != j.get("ordM"):
            mal += 1; print("ESTADO", c, p, j); continue
        if "ordRealM" in p and p["ordRealM"] != j.get("ordRealM"): mal += 1; print("ORDREAL", c, p["ordRealM"], j.get("ordRealM")); continue
        for k in ("pensionElegida", "pensionOrdinaria", "acumElegida", "acumOrdinaria", "diferencia"):
            if k in p and (j.get(k) is None or abs(p[k] - j[k]) > 1.0): mal += 1; print("DIF", k, c, p[k], j.get(k)); break
        else:
            if "equilibrioEdad" in p:
                a, b = p["equilibrioEdad"], j.get("equilibrioEdad")
                if (a is None) != (b is None) or (a is not None and abs(a - b) > 1e-6): mal += 1; print("EQ", c, a, b)
    print(f"{len(casos)} casos, {mal} discrepancias; estados {estados}")
    sys.exit(1 if mal else 0)
