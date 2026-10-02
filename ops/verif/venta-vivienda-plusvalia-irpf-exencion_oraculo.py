#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para venta-vivienda-plusvalia-irpf-exencion. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado consultado el 2/10/2026; LIRPF arts. 33.4.b, 34, 35, 38, 49, 66, 76, DT 9.ª; RIRPF arts. 41 y 41 bis):
1. Ganancia (arts. 34.1.a y 35): valor de transmision = precio real - gastos y tributos satisfechos por el vendedor (35.2); valor de adquisicion = precio + mejoras + gastos y tributos
   de compra (sin intereses) - amortizaciones (35.1). Ganancia = transmision - adquisicion; si es <= 0 no hay cuota (la perdida no se compensa aqui: art. 49, limite 25 %).
2. Vivienda habitual y 65+ (33.4.b): ganancia exenta al 100 %, sin limite de importe, sin reinvertir (la habitualidad se define en RIRPF 41 bis: 3 anos de residencia o dentro de los 2 anos antes de vender).
3. Vivienda habitual < 65 (art. 38.1 + RIRPF 41.1, 41.3, 41.4): exenta la parte proporcional reinvertido / importe obtenido; importe obtenido = valor de transmision menos principal
   pendiente del prestamo con que se compro la vivienda vendida. Plazo 2 anos desde la venta o 2 anos antes. Si hipoteca > transmision: invalido (nada que reinvertir).
4. No habitual: sin exencion. Base del ahorro = otras rentas del ahorro + ganancia no exenta; cuota = escala(otras + ganancia no exenta) - escala(otras). Escala del ahorro (arts. 66.1 estatal + 76 autonomica,
   iguales, redaccion Ley 7/2024): 9,5/10,5/11,5/13,5/15 % por mitad (tramos 6.000/50.000/200.000/300.000), total = doble: 19/21/23/27/30 %. Se usa la tabla de cuota integra del BOE (columna 'Cuota integra').
   Minimo personal y familiar: se supone absorbido por la base general (no se aplica a la base del ahorro, art. 50 no modelado).
5. DT 9.ª (adquirido antes del 31/12/1994): coeficientes de abatimiento NO modelados (declarado: la cuota real puede ser menor).
6. Neto = precio de venta - gastos de venta - principal de hipoteca pendiente - cuota.
Uso: python3 ops/verif/venta-vivienda-plusvalia-irpf-exencion_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# (desde, cuota integra acumulada en ese punto, tipo) de la escala de UNA mitad, columnas del BOE art. 66.1
TAB = [(0, 0, 9.5), (6000, 570, 10.5), (50000, 5190, 11.5), (200000, 22440, 13.5), (300000, 35940, 15)]
def escala(x):
    if x <= 0: return 0.0
    for desde, cuota, tipo in reversed(TAB):
        if x > desde: return 2 * (cuota + (x - desde) * tipo / 100)
def model(d):
    trans = d["venta"] - d["gventa"]; adq = d["adq"] + d["gcomp"]; g = trans - adq
    obt = trans - d["hipoteca"]
    if d["hipoteca"] > trans or min(d["venta"], d["adq"], d["gventa"], d["hipoteca"], d["reinv"], d["otras"]) < 0:
        return dict(invalido=1, ganancia=0, exenta=0, base=0, cuota=0, neto=0, necesaria=0, cuotaSin=0)
    base_pos = max(g, 0)
    if d["sit"] == "hab65": ex = base_pos
    elif d["sit"] == "hab":
        ex = base_pos * (1.0 if obt <= 0 else min(1.0, d["reinv"] / obt)) if base_pos > 0 else 0.0
    else: ex = 0.0
    base = base_pos - ex
    cuota = escala(d["otras"] + base) - escala(d["otras"])
    cuotaSin = escala(d["otras"] + base_pos) - escala(d["otras"])
    return dict(invalido=0, ganancia=g, exenta=ex, base=base, cuota=cuota, neto=d["venta"] - d["gventa"] - d["hipoteca"] - cuota,
                necesaria=max(obt, 0) if (d["sit"] == "hab" and g > 0) else 0.0, cuotaSin=cuotaSin)
B = dict(venta=320000, adq=180000, gcomp=16000, gventa=9000, hipoteca=60000, sit="hab", reinv=150000, otras=3000)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto reinversion parcial", V()), ("2 perdida", V(venta=150000)), ("3 ganancia 0", V(venta=205000)), ("4 reinversion total", V(reinv=251000)),
 ("5 mayor de 65", V(sit="hab65", reinv=0)), ("6 no habitual", V(sit="nohab", reinv=0)), ("7 sin reinversion", V(reinv=0)), ("8 reinversion mayor que lo obtenido", V(reinv=900000)),
 ("9 no habitual, cruza 50.000 y 200.000", V(sit="nohab", venta=900000, otras=20000, reinv=0)), ("10 hipoteca mayor que transmision", V(hipoteca=400000)),
 ("11 no habitual, 300.000+ de base", V(sit="nohab", venta=1500000, adq=300000, gcomp=0, otras=50000, reinv=0)), ("12 amortizacion resta (gcomp negativo)", V(sit="nohab", gcomp=-20000, otras=0, reinv=0)),
 ("13 reinversion igual a obtenido-1", V(reinv=250999)), ("14 otras = 0 y ganancia 6000", V(sit="nohab", venta=211000, adq=180000, gcomp=16000, gventa=9000, otras=0, reinv=0))]
KEYS = ["invalido", "ganancia", "exenta", "base", "cuota", "neto", "necesaria", "cuotaSin"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/venta-vivienda-plusvalia-irpf-exencion.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(33)
    def mk():
        venta = rnd.choice([0, 50000, 150000, 320000, rnd.uniform(0, 2000000)]); adq = rnd.choice([0, 100000, rnd.uniform(0, 1500000)])
        return dict(venta=round(venta, 2), adq=round(adq, 2), gcomp=round(rnd.choice([0, 15000, -10000, rnd.uniform(-50000, 200000)]), 2), gventa=round(rnd.choice([0, 9000, rnd.uniform(0, 80000)]), 2),
                    hipoteca=round(rnd.choice([0, 60000, rnd.uniform(0, 600000)]), 2), sit=rnd.choice(["hab", "hab", "hab65", "nohab"]), reinv=round(rnd.choice([0, 100000, rnd.uniform(0, 2000000)]), 2),
                    otras=round(rnd.choice([0, 3000, 55000, rnd.uniform(0, 400000)]), 2))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.5]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in KEYS}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
