#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado leido hoy; ver journal/preverif-incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar.md):
 - Grados (LGSS 194 + DT 26.ª: se aplican las definiciones antiguas, profesion habitual). Parcial: tanto alzado de 24 mensualidades de la base (Decreto 1646/1972 art. 9).
   Total: pension vitalicia 55 % de la BR (Orden 15-4-1969 art. 15.2); +20 % de la BR (75 %) si >= 55 anos y dificultad de empleo (LGSS 196.2 p.2 + Decreto 1646/72 art. 6), en suspenso mientras trabajes.
   Absoluta: 100 % BR (Orden art. 17). Gran incapacidad: 100 % + complemento = 45 % base minima + 30 % ultima base, minimo 45 % de la pension sin complemento (LGSS 196.4).
 - BR (LGSS 197.1 enfermedad comun): bases 96 meses / 112 x % del art. 210.1 con la DT 9.ª de 2023-2026 (50 % hasta 15 anos; +0,21 % x 49 meses; +0,19 % x 209 meses; tope 100 %);
   se cuentan como cotizados los meses que faltan hasta la edad ordinaria (DT 7.ª 2026: 65 anos si >= 38a3m cotizados, si no 66a10m); si no llega a 15 anos, 50 %.
   Accidente no laboral: 24 meses / 28 (Decreto 1646/72 art. 7.1). AT/EP: la BR se introduce directa (salario real; no modelado).
 - Suelo (LGSS 196.2 p.3): total por enfermedad comun >= 9.580,20/ano (684,30/mes) con cualquier sueldo. Complemento por minimos = diferencia hasta el minimo, con tope 9.442 + minimo - ingresos - pension (RD 241/2026 art. 9.2).
 - Limites: pension inicial <= 3.359,60 EUR/mes (LGSS 57, RD 241/2026); 14 pagas; minimos RD 241/2026 anexo I (unidad unipersonal) con complemento por minimos si ingresos <= 9.442 (LGSS 59.1).
 - Acceso comun (195): sin IP comun si ya tiene la edad ordinaria y 15 anos (bloqueo 1); carencia: <31 anos 1/3 del tiempo desde los 16; >= 31, 1/4 desde los 20 con minimo 5 anos (bloqueo 2); parcial 1.800 dias.
   Mayor de la edad ordinaria sin 15 anos: art. 196.5 no modelado (bloqueo 4). Absoluta/gran con trabajo desde la edad ordinaria: art. 198.3 -> jubilacion activa (bloqueo 3). AT/EP: sin carencia.
 - Compatibilidad (198): total compatible con salario solo si las funciones no coinciden (1); absoluta/gran: si el trabajo da alta, el INSS suspende la pension (2); el complemento de gran incapacidad no se suspende.
 - IRPF: absoluta y gran exentas (LIRPF 7.f); parcial y total tributan (17.2.a.1.ª).
Uso: python3 ops/verif/incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar_oraculo.py -> compara con el JS real (osascript); sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar"
SUELO = 9580.20 / 14; MAXM = 3359.60; BMIN = 1424.40; BMAX = 5101.20; LIM = 9442.0
MIN_GRAN, MIN_ABS, MIN_T65, MIN_T60, MIN_TC = 19660.20, 13106.80, 13106.80, 12262.60, 9662.80

def eord(anos):  # meses de la edad ordinaria (DT 7.a, 2026)
    return 65 * 12 if F(str(anos)) * 12 >= 459 else 66 * 12 + 10
def pct_anos(meses):
    if meses < 180: return 50.0
    a = min(meses - 180, 49); b = min(max(meses - 229, 0), 209)
    return min(50 + a * 0.21 + b * 0.19, 100.0)

def model(c):
    g, o, base, edad, anos, tipo, sal = c["grado"], c["origen"], c["base"], c["edad"], c["anos"], c["trabajo"], c["salario"]
    em = eord(anos); comun = o in ("comun", "accidente")
    if comun and edad * 12 >= em:
        return {"bloqueo": 1 if anos >= 15 else 4}
    if o == "comun" and g != "parcial":
        req = (edad - 16) / 3 if edad < 31 else max((edad - 20) / 4, 5)
        if anos + 1e-9 < req: return {"bloqueo": 2}
    if o == "comun" and g == "parcial" and anos * 365 < 1800: return {"bloqueo": 2}
    if g in ("absoluta", "gran") and tipo != "no" and edad * 12 >= em: return {"bloqueo": 3}
    resto = max(em - edad * 12, 0)
    tot = int(anos * 12 + resto + 1e-9)
    pa = pct_anos(tot) if o == "comun" else 0.0
    if o == "comun": br = base * 96 / 112 * pa / 100
    elif o == "accidente": br = base * 24 / 28
    else: br = base
    r = dict(bloqueo=0, br=br, pct_anos=pa, pen=0.0, capado=0, comp=0.0, minimo=0.0, topup=0.0, pen_final=0.0, cual=0.0, tanto=0.0, pagado=0.0, total_mes=0.0, exenta=0, anual=0.0)
    working = tipo != "no"
    ing = sal * 12 if working else 0.0
    r["exenta"] = 1 if g in ("absoluta", "gran") else 0
    if g == "parcial":
        r["tanto"] = 24 * base; r["total_mes"] = sal if working else 0.0
        return r
    pct = 55 if g == "total" else 100
    pre = br * pct / 100
    suelo = SUELO if (g == "total" and o == "comun") else 0.0
    pen = max(min(pre, MAXM), suelo); r["capado"] = 1 if pre > MAXM + 1e-9 else 0; r["pen"] = pen
    if g == "gran":
        r["comp"] = max(0.45 * BMIN + 0.30 * min(base, BMAX), 0.45 * pen)
    if g == "gran": ma = MIN_GRAN
    elif g == "absoluta": ma = MIN_ABS
    else:
        ma = MIN_T65 if edad >= 65 else (MIN_T60 if edad >= 60 else (MIN_TC if o == "comun" else 0.0))
    m = ma / 14; r["minimo"] = m
    def cm(ing_):
        py = (pen + r["comp"]) * 14
        return max(min(ma - py, LIM + ma - ing_ - py), 0.0) / 14 if ma else 0.0
    top = cm(0.0)
    r["topup"] = top; r["pen_final"] = pen + top; r["anual"] = (pen + top + r["comp"]) * 14
    if g == "total" and edad >= 55:
        p75 = max(min(br * 0.75, MAXM), suelo); r["cual"] = p75 + ((max(min(ma - p75 * 14, LIM + ma - p75 * 14), 0.0) / 14) if ma else 0.0)
    if not working: r["pagado"] = r["pen_final"] + r["comp"]
    elif g == "total": r["pagado"] = 0.0 if tipo == "mismas" else pen + cm(ing)
    elif g == "absoluta": r["pagado"] = 0.0
    else: r["pagado"] = r["comp"]
    r["total_mes"] = r["pagado"] + (sal if working else 0.0)
    return r

KEYS = ["bloqueo", "br", "pct_anos", "pen", "capado", "comp", "minimo", "topup", "pen_final", "cual", "tanto", "pagado", "total_mes", "exenta", "anual"]
BASE = dict(grado="total", origen="comun", base=2000, edad=52, anos=25, trabajo="no", salario=0)
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto total comun 52/25", V()),
 ("2 absoluta comun", V(grado="absoluta")),
 ("3 gran comun: complemento", V(grado="gran")),
 ("4 parcial comun", V(grado="parcial")),
 ("5 total AT 58 con trabajo distinto", V(origen="profesional", edad=58, base=1800, trabajo="distintas", salario=900)),
 ("6 absoluta AT con trabajo: suspendida", V(grado="absoluta", origen="profesional", trabajo="distintas", salario=1000)),
 ("7 gran con trabajo: solo complemento", V(grado="gran", trabajo="mismas", salario=1000)),
 ("8 total con mismas funciones", V(trabajo="mismas", salario=1200)),
 ("9 borde edad ordinaria: 66 anos con 30 de cotizacion", V(edad=66, anos=30)),
 ("10 66 anos 10 meses ya no: 67 -> bloqueo 1", V(edad=67, anos=30)),
 ("11 65 anos con 38,25 anos cotizados -> bloqueo 1", V(edad=65, anos=38.25)),
 ("12 65 anos con 38 anos -> sigue < ordinaria", V(edad=65, anos=38)),
 ("13 carencia: 40 anos, 4,99", V(edad=40, anos=4.99)),
 ("14 carencia: 40 anos, 5", V(edad=40, anos=5)),
 ("15 carencia <31: 30 anos, 4,66", V(edad=30, anos=4.66)),
 ("16 carencia <31: 30 anos, 4,67", V(edad=30, anos=4.67)),
 ("17 parcial carencia 1800 dias (4,93)", V(grado="parcial", anos=4.93)),
 ("18 parcial carencia (4,94)", V(grado="parcial", anos=4.94)),
 ("19 AT absoluta tope", V(grado="absoluta", origen="profesional", base=5000)),
 ("20 total minimo <60 comun", V(base=800, edad=45, anos=10)),
 ("21 total 61 anos minimo 60-64", V(base=900, edad=61, anos=30)),
 ("22 total 55 anos cualificada", V(edad=55)),
 ("23 total AT 66 anos minimo 65", V(origen="profesional", edad=66, base=700)),
 ("24 accidente no laboral 24/28", V(origen="accidente", base=2800)),
 ("25 gran minimo", V(grado="gran", base=500, anos=20)),
 ("26 absoluta con trabajo tras edad ordinaria AT -> bloqueo 3", V(grado="absoluta", origen="profesional", edad=67, trabajo="distintas", salario=500)),
 ("27 comun 15 anos borde porcentaje 70 anos", V(edad=60, anos=14.9)),
 ("28 acc no laboral >= edad ordinaria <15 -> bloqueo 4", V(origen="accidente", edad=67, anos=10)),
 ("29 total trabajo bajo mantiene minimo", V(base=700, edad=62, anos=30, trabajo="distintas", salario=700)),
 ("30 total trabajo supera 9.442: complemento parcial", V(base=700, edad=62, anos=30, trabajo="distintas", salario=900)),
 ("31 verificador: 45a, 20 anos, base 1.200, 1.200 EUR", V(base=1200, edad=45, anos=20, trabajo="distintas", salario=1200)),
 ("32 verificador: 61a, 30 anos, base 900, 1.000 EUR", V(base=900, edad=61, anos=30, trabajo="distintas", salario=1000)),
 ("33 verificador: 61a sin trabajo", V(base=900, edad=61, anos=30)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    rnd = random.Random(44)
    sweep = []
    for _ in range(700):
        sweep.append(dict(grado=rnd.choice(["parcial", "total", "total", "absoluta", "gran"]), origen=rnd.choice(["comun", "comun", "accidente", "profesional"]),
            base=rnd.choice([600, 900, 1424.4, 2000, 3000, 4500, 5101.2, 7000]) * rnd.uniform(.9, 1.1), edad=rnd.choice([20, 30, 31, 45, 54, 55, 59, 60, 64, 65, 66, 67, rnd.randint(18, 70)]),
            anos=rnd.choice([2, 4.67, 5, 10, 14.9, 15, 25, 38.24, 38.25, 40, rnd.uniform(1, 45)]), trabajo=rnd.choice(["no", "no", "distintas", "mismas"]),
            salario=rnd.choice([0, 400, 700, 787, 788, 1200, 3000, rnd.uniform(1, 4000)])))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS[1:]:
            v = j.get(k)
            t = 0.01 if k in ("capado", "exenta", "pct_anos") else 1
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > t: print("DIF", c, k, v, o[k]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("br", "pct_anos", "pen", "comp", "minimo", "topup", "pen_final", "cual", "tanto", "pagado", "total_mes", "anual")} if not o["bloqueo"] else o)
    print("barrido %d + %d fijos: %d discrepancias" % (len(sweep), len(CASES), bad))
    sys.exit(1 if bad else 0)
