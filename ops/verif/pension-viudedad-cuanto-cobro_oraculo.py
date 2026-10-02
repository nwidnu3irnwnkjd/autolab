#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para pension-viudedad-cuanto-cobro. Escrito desde la norma ANTES del .js.
INTERPRETACION (normas leidas hoy en el BOE consolidado; ver journal/preverif-pension-viudedad-cuanto-cobro.md):
 - Derecho (LGSS arts. 219-222): causante pensionista (217.1.c) sin periodo extra; en alta: 500 dias en 5 anos (219.1) salvo accidente/enf. profesional;
   fuera de alta y sin pension: 15 anos (219.1 p.2); si no, sin derecho. Matrimonio: si muerte por enfermedad comun, 1 ano de matrimonio o hijos comunes (219.2);
   si no, prestacion temporal de 2 anos de igual cuantia (222). Pareja de hecho (221.2): convivencia >= 5 anos salvo hijos comunes + inscripcion >= 2 anos antes;
   inscripcion < 2 anos -> prestacion temporal (222) si cumple el resto (5 anos o hijos); sin 5 anos ni hijos -> sin derecho.
 - Porcentaje (Decreto 3158/1966 art. 31): 52 % base; 70 % (31.2) con cargas familiares (hijos < 26 / incapacitados que conviven, y renta de la unidad familiar
   /miembros <= 75 % SMI sin extras), pension >= 50 % de los ingresos totales y rendimientos <= 9.442 + minimo de viudedad EN FUNCION DE LA EDAD (lectura literal: 19.373,60 / 21.704,60 / 22.548,80); la lectura favorable 27.034,40 (minimo con cargas) solo se avisa (alt);
   cargas se miden sin la pension (al reconocer no se cobraba; en anos siguientes si cuenta: aviso mant). 31.3: pension + rendimientos no pueden pasar del limite (se reduce la pension). 60 % (RD 900/2018 art. 2-3): >= 65 anos, sin otra pension publica,
   sin ingresos por trabajo y capital <= 9.442. RD 900/2018 art. 7: se aplica el 70 % si es mas favorable, no se acumulan.
 - Cuantia: BR mensual x % en 14 pagas. Limite RD 241/2026 art. 3: pension(es) <= 3.359,60 EUR/mes (viudedad + otra pension propia).
 - Minimos 2026 (RD 241/2026 anexo I, EUR/ano / 14): cargas 17.592,40; >= 65 13.106,80; 60-64 12.262,60; < 60 9.931,60.
 - Imposible: causante sin periodo -> bloqueo 1; pareja sin 5 anos ni hijos -> bloqueo 2.
Uso: python3 ops/verif/pension-viudedad-cuanto-cobro_oraculo.py -> compara con el JS real (osascript); sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "pension-viudedad-cuanto-cobro"
SMI_SIN_EXTRAS = 1221 * 12
UMB = 0.75 * SMI_SIN_EXTRAS            # 10.989 por miembro
LIM = 9442.0
MINC, MIN65, MIN60, MINM = 17592.40, 13106.80, 12262.60, 9931.60
LIM70 = LIM + MINC
MAXM = 3359.60

def model(c):
    br, ing, edad, h, anos, otra = c["br"], c["ingresos"], c["edad"], int(c["hijos"]), c["anos"], c["otra"]
    if c["causante"] == "nocumple": return {"bloqueo": 1}
    temporal = 0
    if c["union"] == "matrimonio":
        if c["causante"] != "accidente" and anos < 1 and h == 0: temporal = 1
    else:
        ok = (h > 0) or (anos >= 5)
        if not ok: return {"bloqueo": 2}
        if c["union"] == "pareja_corta": temporal = 1
    n = 1 + h
    rend = ing + otra * 14          # rendimientos anuales sin la pension de viudedad (los del ano anterior: al reconocer, no se cobraba)
    p52 = br * .52 * 14
    p70 = br * .70 * 14
    c_estricta = h >= 1 and rend / n <= UMB
    minedad = MIN65 if edad >= 65 else (MIN60 if edad >= 60 else MINM)
    lim_lit = LIM + minedad         # lectura literal 31.2: minimo de viudedad en funcion de la edad
    def ok70(carg, lim):
        if not carg or rend > lim: return None
        pe = min(p70, lim - rend)
        if pe <= 0 or pe / (pe + rend) < .5: return None
        return pe
    pe_ok = ok70(c_estricta, lim_lit)
    cands = {52: p52}
    if edad >= 65 and otra == 0 and ing == 0: cands[60] = br * .60 * 14
    if pe_ok is not None and pe_ok > p52 and pe_ok > cands.get(60, 0): cands[70] = pe_ok
    pct = max(cands, key=lambda k: cands[k])
    anual_pre = cands[pct]
    pos = 60 if (edad >= 65 and otra == 0 and 0 < ing <= LIM and pct < 60) else 0
    mant = 1 if (pct == 70 and (rend + anual_pre) / n > UMB) else 0
    pe_w = ok70(c_estricta, LIM70)
    mes_pre = anual_pre / 14
    cap = max(MAXM - otra, 0)
    mes = min(mes_pre, cap)
    alt = 0
    if pe_w is not None and pe_w > p52 and pe_w > anual_pre + 0.005 and pe_w > cands.get(60, 0):
        a_m = min(pe_w / 14, cap)
        if a_m > mes + 0.005: alt = a_m
    minimo = (MINC if c_estricta else minedad) / 14
    return {"bloqueo": 0, "temporal": temporal, "pct": pct, "mes_pre": mes_pre, "mes": mes, "anual": mes * 14, "capado": 1 if mes_pre > cap + 1e-9 else 0,
            "minimo": minimo, "falta": max(minimo - mes, 0), "pos": pos, "alt": alt, "mant": mant, "limite": lim_lit}

KEYS = ["bloqueo", "temporal", "pct", "mes_pre", "mes", "anual", "capado", "minimo", "falta", "pos", "alt", "mant", "limite"]
BASE = dict(br=1600, causante="pensionista", ingresos=0, edad=66, hijos=0, union="matrimonio", anos=30, otra=0)
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto 65+ sin ingresos: 60 %", V()),
 ("2 trabajando 66 anos, ingresos 8.000: 52 %", V(ingresos=8000)),
 ("3 menor de 65 sin ingresos: 52 %", V(edad=58)),
 ("4 borde 65 anos: 60 %", V(edad=65)),
 ("5 64 anos: 52 %", V(edad=64)),
 ("6 con 1 hijo, BR 1.200, sin ingresos, 40 anos: 70 %", V(br=1200, edad=40, hijos=1)),
 ("7 con 1 hijo, ingresos 20.000 (/2 = 10.000 <= 10.989) pero 70 % no por 50 %: 52", V(br=1200, edad=40, hijos=1, ingresos=20000)),
 ("8 con 2 hijos, BR 2.000, ingresos 6.000: 70 % y recorte por limite", V(br=2000, edad=45, hijos=2, ingresos=6000)),
 ("9 borde cargas: 1 hijo, ingresos 21.978 (/2 = 10.989)", V(br=500, edad=45, hijos=1, ingresos=21978)),
 ("10 cargas: ingresos 21.979 -> sin cargas", V(br=500, edad=45, hijos=1, ingresos=21979)),
 ("11 otra pension 1.500: limite 3.359,60 con BR 4.800 (60 % no, 52 %)", V(br=4800, otra=1500)),
 ("12 BR alta 5.101,20, 65+ sin nada: 60 %", V(br=5101.2)),
 ("13 70 % con BR 5.101,2 y cargas: tope maximo", V(br=5101.2, edad=45, hijos=1)),
 ("14 matrimonio 0,5 anos sin hijos: temporal", V(anos=0.5)),
 ("15 matrimonio 0,99 anos con hijos: derecho", V(anos=0.99, hijos=1, edad=40)),
 ("16 matrimonio 0,5 anos, accidente: pension", V(anos=0.5, causante="accidente")),
 ("17 pareja >=2 anos, 5 anos exactos", V(union="pareja", anos=5)),
 ("18 pareja 4,99 anos sin hijos: bloqueo 2", V(union="pareja", anos=4.99)),
 ("19 pareja 2 anos con hijos: derecho", V(union="pareja", anos=2, hijos=1, edad=40)),
 ("20 pareja inscrita <2 anos, 6 anos de convivencia: temporal", V(union="pareja_corta", anos=6)),
 ("21 pareja <2 anos, 3 anos, hijos: temporal", V(union="pareja_corta", anos=3, hijos=1, edad=40)),
 ("22 pareja <2 anos, 3 anos, sin hijos: bloqueo 2", V(union="pareja_corta", anos=3)),
 ("23 causante no cumple: bloqueo 1", V(causante="nocumple")),
 ("24 ingresos 9.442 y 65+: 60 posible", V(ingresos=9442)),
 ("25 70 % dudoso: 1 hijo, BR 2.300 sin ingresos (con pension supera 10.989 x 2)", V(br=2300, edad=40, hijos=1)),
 ("26 70 % reducido por art. 31.3: ingresos 20.000, BR 3.000, 1 hijo", V(br=3000, edad=40, hijos=1, ingresos=20000)),
 ("28 BR 2.000, 45 anos, 2 hijos, 6.000: literal 19.373,60 -> aviso alt 1.400", V(br=2000, edad=45, hijos=2, ingresos=6000)),
 ("29 BR 1.200, 66, 1 hijo: literal 65+ no limita, sin alt", V(br=1200, hijos=1)),
 ("30 BR 3.000, 50, 1 hijo: reducido, alt", V(br=3000, edad=50, hijos=1)),
 ("27 70 % con ingresos 27.034,4 limite: no", V(br=1500, edad=40, hijos=1, ingresos=27034.4)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    rnd = random.Random(26)
    sweep = []
    for _ in range(700):
        sweep.append(dict(br=rnd.choice([400, 800, 1200, 1600, 2000, 2500, 3500, 4800, 5101.2]) * rnd.uniform(.9, 1.1), causante=rnd.choice(["pensionista", "alta500", "accidente", "nocumple", "no_alta15"]),
            ingresos=rnd.choice([0, 0, 0, 3000, 9442, 12000, 20000, 25000, 30000, rnd.uniform(0, 40000)]), edad=rnd.choice([30, 45, 58, 59, 60, 64, 65, 66, 80, rnd.randint(25, 90)]),
            hijos=rnd.choice([0, 0, 1, 2, 3]), union=rnd.choice(["matrimonio", "matrimonio", "pareja", "pareja_corta"]),
            anos=rnd.choice([0, 0.5, 0.99, 1, 2, 4.99, 5, 10, 30, rnd.uniform(0, 40)]), otra=rnd.choice([0, 0, 0, 500, 1200, 2000, 3000, 3400])))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS[1:]:
            v = j.get(k)
            t = 0.01 if k in ("temporal", "pct", "capado", "pos", "mant") else 1
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > t: print("DIF", c, k, v, o[k]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("pct", "mes", "temporal", "capado", "pos", "alt", "mant", "minimo")})
    print("barrido %d + %d fijos: %d discrepancias" % (len(sweep), len(CASES), bad))
    sys.exit(1 if bad else 0)
