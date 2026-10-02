#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para paro-autonomos-cese-actividad-cuanto-cobro. Escrito desde la norma ANTES del .js.
INTERPRETACION (LGSS consolidada, BOE-A-2015-11724, arts. 327-350 leidos el 2/10/2026; versiones vigentes: RDL 13/2022 desde 1-1-2023 y Ley 3/2023 en el 330.1.c):
1. Derecho (art. 330.1): alta; carencia = periodo del art. 338.1 (>= 12 meses cotizados por cese en los 48 anteriores, de ellos >= 12 en los 24 inmediatamente anteriores);
   situacion legal de cese (331.1: economicos [pierdas >10 %, ejecuciones, concurso], fuerza mayor, licencia, violencia, divorcio-ayuda familiar; 333: TRADE por extincion del contrato);
   cese definitivo: no haber cumplido la edad ordinaria de jubilacion (330.1.d; DT 7.a 2026: 65 con 38a3m cotizados, 66a10m si no -> con 67 cumplidos seguro superada).
   Cese voluntario: nunca es situacion legal (331.2.a). Cese parcial (331.1.a 4.o-5.o, fuerza mayor parcial) = 50 %, sin max/min, compatible: NO se modela (bloqueo).
2. Cuantia: BR = media de las bases de los 12 meses anteriores (339.1); 70 % (339.2); max 175/200/225 % y min 80/107 % del IPREM mensual + 1/6 (600 + 100 = 700) (339.3-4):
   1.225/1.400/1.575 y 560/749 euros. 1 hijo -> 200 %, 2 o mas -> 225 % (lectura del 'respectivamente', igual que el paro, art. 270.3; supuesto propio). Min 80 % sin hijos, 107 % con hijos.
3. Duracion (338.1, escala tras RDL 13/2022): meses completos cotizados en 48 meses: 12-17 -> 4, 18-23 -> 6, 24-29 -> 8, 30-35 -> 10, 36-42 -> 12, 43-47 -> 16, >= 48 -> 24 meses. Total = prestacion x meses.
4. Nueva prestacion: solo 18 meses despues del reconocimiento de la anterior (338.3); las cotizaciones ya usadas no cuentan (338.4.b y d): el usuario introduce solo las no usadas.
5. Trabajar por cuenta propia o ajena mientras se cobra: incompatible, suspende (340.1.c, 342.1, 347.e); se calcula 'si dejas de trabajar' con aviso (condTrabajo).
6. Edad 65-66: puede haberse alcanzado la edad ordinaria segun la cotizacion: se calcula con aviso (condEdad); >= 67: sin derecho (bloqueo) salvo falta de carencia de pension (no se modela).
7. La cuota a la SS durante la prestacion la abona el organo gestor (329.1.b); no se calcula importe. Prioridad de bloqueos: 7 (m24 > m48) > 2 (fuera de modelo) > 1 (voluntario) > 5 (anterior < 18 m) > 3 (edad >= 67) > 6 (carencia).
Uso: python3 ops/verif/paro-autonomos-cese-actividad-cuanto-cobro_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias > 1 EUR."""
import json, os, random, subprocess, sys, math
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IPREM = F(600); IPREM_M = IPREM + IPREM / 6
TOPE = [IPREM_M * F(p, 100) for p in (175, 200, 225)]
MINI = [IPREM_M * F(80, 100), IPREM_M * F(107, 100), IPREM_M * F(107, 100)]
ESCALA = [(48, 24), (43, 16), (36, 12), (30, 10), (24, 8), (18, 6), (12, 4)]
ADMITIDAS = {"eco", "fuerza", "licencia", "violencia", "divorcio", "trade"}
def meses(m48):
    for lim, dur in ESCALA:
        if m48 >= lim: return dur
    return 0
def calc(d):
    base, m48, m24 = F(str(d["base"])), math.floor(d["m48"]), math.floor(d["m24"])
    m48 = min(m48, 48); h = min(max(int(d["hijos"]), 0), 2)
    out = dict(bloqueo=0, prest=F(0), tope=TOPE[h], minimo=MINI[h], ap=0, dur=0, total=F(0), condTrabajo=0, condEdad=0)
    if m24 > m48: out["bloqueo"] = 7; return out
    if d["causa"] == "fuera": out["bloqueo"] = 2; return out
    if d["causa"] not in ADMITIDAS: out["bloqueo"] = 1; return out
    if d["anterior"] == "reciente": out["bloqueo"] = 5; return out
    if d["edad"] >= 67: out["bloqueo"] = 3; return out
    if m48 < 12 or m24 < 12: out["bloqueo"] = 6; return out
    raw = base * F(70, 100)
    p = min(max(raw, MINI[h]), TOPE[h])
    out.update(prest=p, ap=(1 if raw > TOPE[h] else (-1 if raw < MINI[h] else 0)), dur=meses(m48))
    out["total"] = p * out["dur"]
    out["condTrabajo"] = 1 if d["trabaja"] == "si" else 0
    out["condEdad"] = 1 if d["edad"] >= 65 else 0
    return out
CAMPOS = ["bloqueo", "prest", "tope", "minimo", "ap", "dur", "total", "condTrabajo", "condEdad"]
def correr_js(casos):
    js = open(os.path.join(ROOT, "projects/decidir/calcs/paro-autonomos-cese-actividad-cuanto-cobro.js")).read().split("function eur(")[0]
    h = js + "\nJSON.stringify(" + json.dumps(casos) + ".map(function(c){return calcular(c);}));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout.strip())
CAUSAS = ["eco", "fuerza", "licencia", "violencia", "divorcio", "trade", "voluntario", "fuera"]
def aleatorio(rng):
    k = rng.random()
    if k < .3: base = rng.choice([800, 1000, 1166.67, 1250, 1750, 2000, 2250, 2500, 1070, 1000]) + rng.choice([-.01, 0, .01])
    else: base = round(rng.uniform(300, 6000), 2)
    m48 = rng.choice([rng.randint(0, 48), rng.choice([11, 12, 17, 18, 23, 24, 29, 30, 35, 36, 42, 43, 47, 48])])
    m24 = min(m48, rng.choice([rng.randint(0, 24), 11, 12, 24])) if rng.random() < .93 else rng.randint(0, 24)
    return dict(base=round(base, 2), m48=m48, m24=m24, hijos=rng.randint(0, 3), causa=rng.choice(CAUSAS[:6] * 3 + CAUSAS[6:]),
                edad=rng.choice([rng.randint(18, 70), 64, 65, 66, 67]), trabaja=rng.choice(["no", "no", "si"]), anterior=rng.choice(["nunca", "nunca", "reciente", "antigua"]))
if __name__ == "__main__":
    rng = random.Random(2026); casos = [aleatorio(rng) for _ in range(1500)]
    res = correr_js(casos); malos = 0; nbloq = 0
    for d, j in zip(casos, res):
        o = calc(d); nbloq += o["bloqueo"] > 0
        for k in CAMPOS:
            a, b = float(o[k]), j.get(k)
            if b is None or abs(a - b) > (1 if k in ("prest", "total", "tope", "minimo") else 0.001):
                malos += 1; print("DISCREPANCIA", k, a, b, d); break
    print("casos", len(casos), "bloqueados", nbloq, "discrepancias", malos)
    sys.exit(1 if malos else 0)
