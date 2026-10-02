#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para cuota-autonomos-ingresos-reales-regularizacion. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado consultado el 2/10/2026; LGSS art. 308.1.a y c; RDL 13/2022 DT 1.a; RDL 3/2026 art. 3.4 y 3.5 (convalidado, BOE-A-2026-4668);
Orden PJC/297/2026 art. 18; Reglamento General de Cotizacion (RD 2064/1995) arts. 43 bis y 46 en la redaccion del RD 504/2022 y del RD 665/2024):
1. Tramo: rendimiento neto mensual = rendimiento (neto antes de restar la cuota de autonomos) x 0,93 (deduccion 7 % de gastos genericos, LGSS 308.1.c.2.a). Tabla 2026 = tabla 2025 (RDL 3/2026 art. 3.4), bases max. de tramos 11-12 = 5.101,20.
   Reducida: <=670 (T1), >670 y <=900 (T2), >900 y <1.166,70 (T3). General: >=1.166,70 y <=1.300 (T4 = general 1) ... >6.000 (T15 = general 12).
2. Base elegida (DT 1.a RDL 13/2022 ap. 2): entre la base minima del tramo del rendimiento PREVISTO y la base maxima del regimen (5.101,20). Se puede cambiar hasta 6 veces al ano (RGC 43 bis); se modela 1 cambio: nueva base durante los ultimos m meses.
3. Cuota mensual = base x 31,5 % (28,30 CC + 1,30 CP + 0,90 cese, obligatorio por LGSS 327.1 + 0,10 FP + 0,90 MEI; Orden art. 18.2 y 37).
4. Regularizacion (LGSS 308.1.c.3.a-4.a; RGC 46.2): base real = rendimiento real x 0,93 repartido en los meses de alta; tramo real; base provisional media del ano.
   Si media < base minima del tramo real: se reclama N x (min - media) x 31,5 %. Si media > base maxima del tramo real: se devuelve N x (media - max) x 31,5 %. Si esta entre ambas: no hay regularizacion.
   (Meses completos; la norma cuenta dias.) Sin ingresos declarados (rendimiento real 0): base definitiva = minima del grupo 7 (regla 5.a); no se calcula, se bloquea.
5. Recomendada: base mas cercana al rendimiento computable real dentro de [max(min previsto, min real), max real]; si ese intervalo es vacio, la minima del tramo previsto (no se puede elegir menos).
6. Pluriactividad: sin cubrir IT en el RETA, reduccion del 5,5 % sobre la cuota por CC (Orden art. 18.2.a): 0,055 x 28,30 % x base media. Solo informativo.
Uso: python3 ops/verif/cuota-autonomos-ingresos-reales-regularizacion_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias > 1 EUR."""
import json, os, random, subprocess, sys
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# (limite superior del rendimiento neto, base minima, base maxima, es_reducida)
TABLA = [(F(670), F("653.59"), F("718.94")), (F(900), F("718.95"), F("900")), (F("1166.70"), F("849.67"), F("1166.70")),
         (F(1300), F("950.98"), F(1300)), (F(1500), F("960.78"), F(1500)), (F(1700), F("960.78"), F(1700)), (F(1850), F("1143.79"), F(1850)),
         (F(2030), F("1209.15"), F(2030)), (F(2330), F("1274.51"), F(2330)), (F(2760), F("1356.21"), F(2760)), (F(3190), F("1437.91"), F(3190)),
         (F(3620), F("1519.61"), F(3620)), (F(4050), F("1601.31"), F(4050)), (F(6000), F("1732.03"), F("5101.20")), (None, F("1928.10"), F("5101.20"))]
RATE = F("28.30") / 100 + F("1.30") / 100 + F("0.90") / 100 + F("0.10") / 100 + F("0.90") / 100
BMAX = F("5101.20")
def fr(x): return F(str(x))
def tramo(r):  # r = rendimiento neto mensual computable (Fraction)
    for i, (lim, mn, mx) in enumerate(TABLA):
        if lim is None: return i
        if i == 2:
            if r < lim: return i
        elif r <= lim: return i
def clamp(x, lo, hi): return max(lo, min(hi, x))
def calc(d):
    prev, real, base = fr(d["prev"]), fr(d["real"]), fr(d["base"])
    cambio, mc, N, plur = fr(d["cambio"]), int(d["mcambio"]), int(d["meses"]), int(d["plur"])
    cp = prev * 93 / 100; tp = tramo(cp); minP, maxP = TABLA[tp][1], TABLA[tp][2]
    out = dict(compPrev=cp, tramoPrev=tp + 1, minPrev=minP, maxPrev=maxP, bloqueo=0)
    if real <= 0: out["bloqueo"] = 3; return out
    if base < minP: out["bloqueo"] = 1; return out
    if base > BMAX: out["bloqueo"] = 2; return out
    if cambio > 0 and (cambio < TABLA[0][1] or cambio > BMAX or mc < 1 or mc >= N): out["bloqueo"] = 4; return out
    media = (base * (N - mc) + cambio * mc) / N if cambio > 0 else base
    cr = real * 93 / 100; tr = tramo(cr); minR, maxR = TABLA[tr][1], TABLA[tr][2]
    pagado = media * N * RATE
    if media < minR: reg = N * (minR - media) * RATE
    elif media > maxR: reg = -N * (media - maxR) * RATE
    else: reg = F(0)
    lo = max(minP, minR); hi = maxR
    rec = clamp(cr, lo, hi) if lo <= hi else minP
    mr = rec
    if mr < minR: rr = N * (minR - mr) * RATE
    elif mr > maxR: rr = -N * (mr - maxR) * RATE
    else: rr = F(0)
    defin = clamp(media, minR, maxR)
    out.update(compReal=cr, tramoReal=tr + 1, minReal=minR, maxReal=maxR, baseMedia=media, cuotaProv=base * RATE, pagado=pagado, regul=reg,
               baseDefinitiva=defin, definitiva=defin * N * RATE, recomendada=rec, regulRec=rr, plurRed=(F(55, 1000) * F("28.30") / 100 * media if plur else F(0)),
               escenario=(1 if reg > 0 else (2 if reg < 0 else 0)))
    return out
CAMPOS = ["compPrev", "tramoPrev", "minPrev", "maxPrev", "bloqueo", "compReal", "tramoReal", "minReal", "maxReal", "baseMedia", "cuotaProv", "pagado", "regul",
          "baseDefinitiva", "definitiva", "recomendada", "regulRec", "plurRed", "escenario"]
def correr_js(casos):
    js = open(os.path.join(ROOT, "projects/decidir/calcs/cuota-autonomos-ingresos-reales-regularizacion.js")).read().split("function eur(")[0]
    h = js + "\nJSON.stringify(" + json.dumps(casos) + ".map(function(c){return calcular(c);}));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout.strip())
def aleatorio(rng):
    lims = [670, 900, 1166.7, 1300, 1500, 1700, 1850, 2030, 2330, 2760, 3190, 3620, 4050, 6000]
    def rend():
        k = rng.random()
        if k < .35: b = rng.choice(lims) / .93; return round(b + rng.choice([-.02, -.01, 0, .01, .02]), 2)
        if k < .8: return round(rng.uniform(0, 4500), 2)
        return round(rng.uniform(4500, 9000), 2)
    prev = rend(); cp = float(prev) * .93; t = tramo(F(str(prev)) * 93 / 100); minP = float(TABLA[t][1])
    base = round(rng.choice([minP, minP, rng.uniform(minP, 5101.2), 5101.2, rng.uniform(600, 5200)]), 2)
    cambio = 0 if rng.random() < .55 else round(rng.uniform(600, 5200), 2)
    N = rng.randint(1, 12)
    return dict(prev=prev, real=(0 if rng.random() < .03 else rend()), base=base, cambio=cambio, mcambio=rng.randint(0, 12) if cambio else 0, meses=N, plur=rng.randint(0, 1))
if __name__ == "__main__":
    rng = random.Random(2026); casos = [aleatorio(rng) for _ in range(1500)]
    res = correr_js(casos); malos = 0; nbloq = 0
    for d, j in zip(casos, res):
        o = calc(d); nbloq += o["bloqueo"] > 0
        for k in CAMPOS:
            if k not in o: continue
            a, b = float(o[k]), j.get(k)
            if b is None or abs(a - b) > (1 if k in ("pagado", "regul", "definitiva", "regulRec") else 0.01) :
                malos += 1; print("DISCREPANCIA", k, a, b, d); break
    print("casos", len(casos), "bloqueados", nbloq, "discrepancias", malos)
    sys.exit(1 if malos else 0)
