#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para irpf-alquilar-vivienda-rendimiento-neto. Escrito desde la norma ANTES del .js.
INTERPRETACION (norma leida en el BOE consolidado el 2/10/2026):
1. Rendimiento integro = renta mensual x meses alquilados (LIRPF art. 22.2: todo lo que paga el arrendatario, sin IVA). Neto previo = integro - gastos (art. 23.1; RIRPF art. 13).
2. Intereses de financiacion + reparacion y conservacion: su suma deducible no excede los rendimientos integros (art. 23.1.a.1.o; el exceso va a los 4 anos siguientes: NO modelado, se declara).
3. Amortizacion: 3 % x mayor de (coste de adquisicion satisfecho, valor catastral) sin suelo (art. 23.1.b; RIRPF art. 14.2.a). Proporcional a meses alquilados: criterio prudente (el art. 14 dice «en cada ano»; la proporcion es criterio administrativo, se declara).
4. Reduccion del neto POSITIVO (art. 23.2), redaccion Ley 12/2023 vigente desde 1/1/2024 (RDL 26/2026 derogado el 2/10/2026; desde el 8/10/2026 la DT 38.a LIRPF (RDL 29/2026, BOE-A-2026-20823) fija el corte 1/12/2026: contratos de 26/5/2023 a 1/12/2026 -> art. 23.2 vigente a 31/12/2025 (Ley 12/2023); desde el 2/12/2026 nuevo art. 23.2, NO modelado):
   contrato anterior a 26/5/2023 -> texto a 31/12/2021: 60 %; contrato de 26/5/2023 a 1/12/2026: 90 % (zona tensionada, nuevo contrato, renta rebajada > 5 %), 70 % (1.a vez en zona tensionada con inquilino 18-35,
   o alquiler social/programa publico), 60 % (rehabilitacion terminada en los 2 anos previos), 50 % resto. 0 % = sin reduccion (no vivienda, art. 17.6 LAU incumplido, regularizacion).
5. Cuota estimada = neto reducido positivo x tipo marginal (base general). Neto en mano = ingresos - gastos pagados (otros + intereses/reparaciones, sin amortizacion, que no es salida de caja) - cuota. Perdidas: cuota 0, sin compensacion (se declara).
6. Rebaja que compensa: renta mensual R' con la que, con la reduccion p' mayor, el neto en mano iguala al actual (biseccion).
Uso: python3 ops/verif/irpf-alquilar-vivienda-rendimiento-neto.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PCT = {"a60": 60, "b50": 50, "b60": 60, "b70": 70, "b70s": 70, "b90": 90, "n0": 0}
def neto_en_mano(d, R, p):
    m = d["meses"]; ing = R * m
    fin = min(d["interep"], ing)
    am = 0.03 * max(d["adq"], d["cat"]) * m / 12
    prev = ing - d["otros"] - fin - am
    red = prev * (1 - p / 100) if prev > 0 else prev
    cuota = max(red, 0) * d["tipo"] / 100
    return ing - d["otros"] - d["interep"] - cuota, prev, red, cuota, am, fin
def model(d):
    p = PCT[d["contrato"]]; R = d["renta"]; m = d["meses"]
    neto, prev, red, cuota, am, fin = neto_en_mano(d, R, p)
    o = dict(noModelado=0, ingresos=R * m, amort=am, finDeducido=fin, previo=prev, pct=p, reduccion=max(prev, 0) * p / 100, reducido=red, cuota=cuota, neto=neto,
             rentaCubre=(d["otros"] + d["interep"]) / m, rentaIrpf=(d["otros"] + d["interep"] + am) / m)
    for q in (50, 60, 70, 90): o["n%d" % q] = neto_en_mano(d, R, q)[0]
    for q in (60, 70, 90):
        if q <= p: o["r%d" % q] = R; continue
        lo, hi = 0.0, R
        for _ in range(100):
            mid = (lo + hi) / 2
            if neto_en_mano(d, mid, q)[0] < neto: lo = mid
            else: hi = mid
        o["r%d" % q] = hi
    return o
B = dict(contrato="b50", renta=800, meses=12, otros=900, interep=2500, adq=120000, cat=60000, tipo=30)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto 50 %", V()), ("2 60 % anterior a mayo 2023", V(contrato="a60")), ("3 70 % joven zona tensionada", V(contrato="b70", renta=1100, tipo=37)),
 ("4 90 % zona tensionada", V(contrato="b90", renta=950, tipo=30)), ("5 gastos > ingresos", V(renta=300, meses=12)), ("6 intereses limitados por ingresos", V(renta=400, interep=9000, otros=200)),
 ("7 valor catastral 0 y adquisicion 0", V(adq=0, cat=0)), ("8 catastral mayor que adquisicion, 1 mes", V(adq=50000, cat=90000, meses=1, renta=900)),
 ("9 sin reduccion", V(contrato="n0", meses=6)), ("10 60 % rehabilitada 12 meses tipo 45", V(contrato="b60", tipo=45, renta=1500))]
KEYS = ["noModelado", "ingresos", "amort", "finDeducido", "previo", "pct", "reduccion", "reducido", "cuota", "neto", "rentaCubre", "rentaIrpf", "n50", "n60", "n70", "n90", "r60", "r70", "r90"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/irpf-alquilar-vivienda-rendimiento-neto.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(26)
    def mk():
        return dict(contrato=rnd.choice(list(PCT) * 2), renta=rnd.choice([0, 200, 500, 800, 1500, 3000, rnd.uniform(0, 4000)]), meses=rnd.randint(1, 12),
                    otros=rnd.choice([0, 300, rnd.uniform(0, 5000)]), interep=rnd.choice([0, rnd.uniform(0, 15000)]), adq=rnd.choice([0, rnd.uniform(0, 400000)]),
                    cat=rnd.choice([0, rnd.uniform(0, 200000)]), tipo=rnd.choice([19, 24, 30, 37, 45, 47, rnd.uniform(0, 55)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.005]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("ingresos", "previo", "reduccion", "cuota", "neto", "rentaIrpf", "r90")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
