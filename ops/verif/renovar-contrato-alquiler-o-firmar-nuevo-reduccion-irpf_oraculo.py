#!/usr/bin/env python3
"""Oraculo independiente: casero, prorrogar el contrato de alquiler o firmar uno nuevo (reduccion del rendimiento neto, LIRPF art. 23.2). Escrito desde la norma antes de abrir el .js.
INTERPRETACION
- Texto aplicado: Ley 35/2006 art. 23.2 en la redaccion de la Ley 12/2023 (vigente desde 1-1-2024) y DT 38.ª en esa misma redaccion; NO el RDL 26/2026 (derogado, BOE-A-2026-20526).
- PRORROGAR (arts. 9 y 10 LAU: mismo contrato): contrato anterior al 26-5-2023 -> DT 38.ª: art. 23.2 a 31-12-2021 = 60 % (supuesto S, confianza B: la prorroga no es contrato nuevo).
  Contrato desde el 26-5-2023 -> conserva su reduccion (50/60/70/90): los requisitos se miran al celebrar el contrato y la reduccion sigue «mientras se sigan cumpliendo» (art. 23.2 ult. parr.).
- FIRMAR NUEVO (misma vivienda, ya alquilada -> «por primera vez» imposible, 70 % de joven no existe): a) 90 % si zona tensionada y renta inicial rebajada MAS de un 5 % sobre la ultima renta (estricto);
  c) 60 % si rehabilitacion terminada en los 2 anos previos; d) 50 % en los demas casos.
- Zona tensionada: art. 17.6 LAU: la renta inicial no puede exceder la ultima renta (+10 % maximo con alguna excepcion a-d: rehabilitacion, eficiencia energetica, accesibilidad o contrato de 10 anos; solo la rehabilitacion art. 41.1 RIRPF da ademas el 60 % del 23.2.c).
- Tacita reconduccion (art. 1566 CC) o documento nuevo: contrato nuevo -> pctA = 50 (verificador). Si la excede, el contrato «incumple» y art. 23.2 quita TODAS las reducciones (0 %).
- Resultado anual = 12 x renta - gastos (incluida amortizacion) - cuota; cuota = max(neto - reduccion, 0) x tipo marginal. Reduccion solo sobre neto positivo.
- Renta nueva que compensa: la que iguala el resultado de la prorroga con el % del contrato nuevo (despeje exacto por tramos). Empate practico si |diferencia| < 5 % del mayor resultado en valor absoluto.
"""
import json, os, random, subprocess, sys
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf.js")

def fr(x): return F(str(x))

def resultado(R, g, p, t):
    ing = 12 * R; prev = ing - g
    red = prev * (1 - F(p) / 100) if prev > 0 else prev
    cuota = max(red, 0) * t / 100
    return ing, prev, cuota, ing - g - cuota

def renta_eq(T, g, p, t):
    k = t / 100 * (1 - F(p) / 100)
    x = T / (1 - k) if T > 0 else T
    return max(F(0), (x + g) / 12)

def model(d):
    R0, R1, g, t = fr(d["renta0"]), fr(d["renta1"]), fr(d["gastos"]), fr(d["tipo"])
    tens, exc = d["tensionada"] == "si", d["excepcion176"]
    reh = exc == "rehab"
    pA = 60 if d["fecha"] == "antes" else 50 if d["fecha"] == "reconduccion" else int(d["pctActual"])
    limite = R0 * (F(110, 100) if exc != "ninguna" else 1)
    incumple = tens and R1 > limite
    rebaja_ok = tens and (R0 - R1) * 100 > 5 * R0
    pB = 0 if incumple else 90 if rebaja_ok else 60 if reh else 50
    ingA, prevA, cA, rA = resultado(R0, g, pA, t)
    ingB, prevB, cB, rB = resultado(R1, g, pB, t)
    dif = rB - rA
    gran = max(abs(rA), abs(rB))
    gana = 0 if (gran == 0 or abs(dif) < gran * F(5, 100)) else (2 if dif > 0 else 1)
    req = renta_eq(rA, g, pB, t)
    req90 = renta_eq(rA, g, 90, t)
    rebajaMax = max(F(0), (1 - req90 / R0) * 100) if R0 > 0 else F(0)
    o = dict(pctA=pA, pctB=pB, prevA=prevA, prevB=prevB, cuotaA=cA, cuotaB=cB, resA=rA, resB=rB, dif=dif, gana=gana,
             incumple=int(incumple), rebajaOk=int(rebaja_ok), limite176=(limite if tens else F(-1)), rentaEq=req, r90=req90, rebajaMax90=rebajaMax)
    return {k: float(v) for k, v in o.items()}

KEYS = list(model(dict(renta0=1, renta1=1, gastos=0, tipo=0, tensionada="no", excepcion176="ninguna", fecha="antes", pctActual="50")))
def js(cases):
    src = open(JS).read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
B = dict(fecha="antes", pctActual="50", renta0=800, renta1=800, gastos=7000, tipo=30, tensionada="no", excepcion176="ninguna")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 ejemplo antes 26/5/2023, misma renta", V()), ("2 nuevo con renta equivalente", V(renta1=807.65)),
 ("3 desde 26/5/2023 con 90 % actual", V(fecha="desde", pctActual="90", renta1=900)), ("4 desde con 70 %", V(fecha="desde", pctActual="70")),
 ("5 tensionada rebaja justo 5 %", V(tensionada="si", renta1=760)), ("6 tensionada rebaja 5,01 %", V(tensionada="si", renta1=759.9)),
 ("7 tensionada renta igual (no rebaja)", V(tensionada="si", renta1=800)), ("8 tensionada excede 0,01 -> incumple", V(tensionada="si", renta1=800.01)),
 ("9 tensionada rehab +10 % justo", V(tensionada="si", excepcion176="rehab", renta1=880)), ("10 tensionada rehab +10 % + 0,01", V(tensionada="si", excepcion176="rehab", renta1=880.01)),
 ("11 no tensionada sube renta rehab 60", V(excepcion176="rehab", renta1=900)), ("12 no tensionada sube 30 % sin limite", V(renta1=1040)),
 ("13 perdida: gastos > ingresos", V(gastos=12000)), ("14 gastos 9600 (neto 0)", V(gastos=9600)), ("15 tipo 0", V(tipo=0)),
 ("16 tipo 54", V(tipo=54)), ("17 renta0 0", V(renta0=0, renta1=0)), ("18 renta1 0", V(renta1=0)), ("19 gastos 0", V(gastos=0)), ("21 excepcion 10 anos +10 % justo", V(tensionada="si", excepcion176="diez", renta1=880)), ("22 excepcion +0,01 incumple", V(tensionada="si", excepcion176="energia", renta1=880.01)),
 ("23 reconduccion misma renta", V(fecha="reconduccion")), ("24 reconduccion renta 900", V(fecha="reconduccion", renta1=900)), ("25 excepcion accesibilidad sin rehab no da 60", V(excepcion176="accesib", renta1=900)),
 ("20 desde 50 y nuevo 90 con rebaja", V(fecha="desde", tensionada="si", renta1=700))]
if __name__ == "__main__":
    rnd = random.Random(58)
    def cents(x): return round(x, 2)
    def mk():
        R0 = rnd.choice([0, 500, 800, 1000, 1500, cents(rnd.uniform(0, 3000))])
        tie = rnd.random() < 0.25
        if tie and R0 > 0:
            R1 = cents(R0 * rnd.choice([0.95, 1.0, 1.1, 0.99, 1.05]))
        else:
            R1 = rnd.choice([0, 500, 760, cents(R0 * rnd.uniform(0.7, 1.3)), cents(rnd.uniform(0, 3500))])
        return dict(fecha=rnd.choice(["antes", "desde", "reconduccion"]), pctActual=rnd.choice(["50", "60", "70", "90"]), renta0=R0, renta1=R1,
                    gastos=rnd.choice([0, 3000, 7000, 9600, 12000, cents(rnd.uniform(0, 30000))]), tipo=rnd.choice([0, 19, 30, 37, 54, round(rnd.uniform(0, 54), 1)]),
                    tensionada=rnd.choice(["si", "no"]), excepcion176=rnd.choice(["ninguna", "ninguna", "rehab", "energia", "accesib", "diez"]))
    sweep = [mk() for _ in range(900)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.01]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("pctA", "pctB", "resA", "resB", "dif", "gana", "rentaEq")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print("casos:", len(allc), "discrepancias:", bad)
    sys.exit(1 if bad else 0)
