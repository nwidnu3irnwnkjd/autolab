#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para cuanto-cobro-de-paro-prestacion-desempleo. Escrito desde la norma ANTES del .js.
INTERPRETACION (LGSS, RDL 8/2015, consolidado leido el 2/10/2026; arts. 269 y 270 sin cambios desde 1/1/2023; el RDL 26/2026 no toca estos articulos):
 - Art. 270.1: base reguladora = promedio de la base de cotizacion por desempleo de los ultimos 180 dias (sin horas extra). Art. 147.1: la base incluye
   la parte proporcional de las pagas extra (vencimiento superior al mensual, prorrateado en 12 meses). Entrada = base mensual media ya prorrateada;
   si el usuario dice que NO incluye las 2 extras, base x 14/12 (supuesto aritmetico, 2 pagas extra).
 - Art. 270.2: 70 % de la BR los 180 primeros dias, 60 % desde el dia 181. Mes = 30 dias (prestacion diaria x 30).
 - Art. 270.3: maximo 175 % / 200 % / 225 % del IPREM (0 / 1 / 2+ hijos a cargo); minimo 80 % (sin hijos) o 107 % (con hijos) del IPREM; el IPREM mensual
   vigente al nacer el derecho "incrementado en una sexta parte" = 600 + 100 = 700 (IPREM 2026 600 EUR, SEPE). Con tiempo parcial, maximo y minimo se
   calculan con el IPREM segun el promedio de horas de los ultimos 180 dias: modelado como x jornada/100 (fraccion de jornada media).
 - Art. 269.1: duracion en dias segun dias cotizados en los 6 anos anteriores: 360-539:120, 540-719:180, 720-899:240, 900-1079:300, 1080-1259:360,
   1260-1439:420, 1440-1619:480, 1620-1799:540, 1800-1979:600, 1980-2159:660, 2160+:720. Menos de 360 dias: sin prestacion contributiva (bloqueo).
 - Total = diario1 x min(D,180) + diario2 x max(D-180,0), con diario = mensual/30, tope/minimo aplicados a cada tramo.
 - Imposible: dias < 360 (bloqueo); hijos 3+ se tratan como 2+; jornada fuera de 1-100 se aviso.
Uso: python3 ops/verif/cuanto-cobro-de-paro-prestacion-desempleo.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cuanto-cobro-de-paro-prestacion-desempleo"
IPREM = 600.0; B = IPREM * 7 / 6   # 700
MAXP = [1.75, 2.00, 2.25]; MINP = [0.80, 1.07, 1.07]
ESCALA = [(2160, 720), (1980, 660), (1800, 600), (1620, 540), (1440, 480), (1260, 420), (1080, 360), (900, 300), (720, 240), (540, 180), (360, 120)]

def dur(dias):
    for lim, d in ESCALA:
        if dias >= lim: return d
    return 0

def clamp(x, lo, hi): return min(max(x, lo), hi)

def model(c):
    dias = int(round(c["dias"]))
    if dias < 360: return {"bloqueo": 1}
    h = min(max(int(round(c["hijos"])), 0), 2); j = c["jornada"] / 100.0
    br = c["base"] * (14 / 12 if c["extras"] == "no" else 1)
    lo, hi = B * MINP[h] * j, B * MAXP[h] * j
    r = {"bloqueo": 0, "br": br, "tope": hi, "minimo": lo}
    D = dur(dias); d1, d2 = min(D, 180), max(D - 180, 0)
    for n, pct in (("1", .70), ("2", .60)):
        raw = br * pct; v = clamp(raw, lo, hi)
        r["m" + n] = v; r["dia" + n] = v / 30; r["ap" + n] = 1 if raw > hi else (-1 if raw < lo else 0)
    r["dur"] = D; r["meses"] = D / 30; r["total"] = r["dia1"] * d1 + r["dia2"] * d2
    return r

KEYS = ["br", "tope", "minimo", "m1", "m2", "dia1", "dia2", "ap1", "ap2", "dur", "meses", "total"]
BASE = dict(base=1500, extras="si", hijos=0, jornada=100, dias=720)
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto 1.500, 0 hijos, 720 dias", V()),
 ("2 tope maximo: 2.500, 0 hijos (1.225)", V(base=2500, dias=1080)),
 ("3 base justo en el tope tramo 1: 1.750 (0,7x=1.225)", V(base=1750)),
 ("4 minimo: 600 sin hijos (560)", V(base=600)),
 ("5 base justo en minimo tramo 1: 800 (0,7x=560)", V(base=800)),
 ("6 minimo tramo 2: 900 (0,6x=540<560) sin hijos", V(base=900)),
 ("7 1 hijo: 2.500 (tope 1.400)", V(base=2500, hijos=1, dias=1260)),
 ("8 2 hijos: 3.000 (tope 1.575)", V(base=3000, hijos=2, dias=2160)),
 ("9 1 hijo minimo 749: base 600", V(base=600, hijos=1)),
 ("10 parcial 50 %: base 600, topes a la mitad (min 280)", V(base=600, jornada=50)),
 ("11 parcial 50 % con tope: base 1.800 (tope 612,5)", V(base=1800, jornada=50, dias=900)),
 ("12 359 dias -> bloqueo", V(dias=359)),
 ("13 360 dias exactos: 120 dias", V(dias=360)),
 ("14 539/540 limite 120/180", V(dias=539)),
 ("15 540", V(dias=540)),
 ("16 2159 -> 660", V(dias=2159)),
 ("17 2160 -> 720", V(dias=2160)),
 ("18 5000 dias -> 720", V(dias=5000)),
 ("19 extras no incluidas 1.500 -> 1.750", V(extras="no")),
 ("20 hijos 5 -> 2+", V(hijos=5, base=3000)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    rnd = random.Random(11)
    sweep = [dict(base=rnd.choice([300, 600, 800, 933, 1200, 1750, 2042, 2800, 4500]) * rnd.uniform(.9, 1.1), extras=rnd.choice(["si", "si", "no"]), hijos=rnd.randint(0, 4),
                  jornada=rnd.choice([100, 100, 80, 75, 50, 25, 10, rnd.randint(1, 100)]), dias=rnd.choice([rnd.randint(300, 2400), 359, 360, 539, 540, 719, 720, 1079, 1080, 2159, 2160])) for _ in range(600)]
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo")); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS:
            v = j.get(k)
            t = 0.01 if k in ("ap1", "ap2", "dur", "meses", "dia1", "dia2") else 1
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > t: print("DIF", c, k, v, o[k]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("m1", "m2", "ap1", "ap2", "dur", "total")})
    print("barrido %d + %d fijos: %d discrepancias" % (len(sweep), len(CASES), bad))
    sys.exit(1 if bad else 0)
