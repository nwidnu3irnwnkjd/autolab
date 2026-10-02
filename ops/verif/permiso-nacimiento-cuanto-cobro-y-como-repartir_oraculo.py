#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para permiso-nacimiento-cuanto-cobro-y-como-repartir. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado leido el 2/10/2026; ET art. 48.4 y 48.6 y RDL 9/2025 DT unica; LGSS arts. 177-179; LIRPF art. 7.h; Orden PJC/297/2026 art. 2.1):
1. Cada progenitor tiene un derecho INDIVIDUAL e INTRANSFERIBLE de 19 semanas (48.4): 6 obligatorias a jornada completa tras el parto + 11 hasta los 12 meses + 2 hasta los 8 anos (monoparental: 32 = 6 + 22 + 4). Ambito: nacimientos desde el 31-7-2025 (19 semanas; los del 2-8-2024 al 30-7-2025 tienen 16 + 2 por la DT unica del RDL 9/2025: fuera). Ampliacion (48.6): +1 semana por progenitor por cada hijo ademas del primero y +1 por discapacidad del hijo; con un solo progenitor, +2 por cada una (ampliaciones completas).
2. Prestacion (LGSS 179.1): 100 % de la base reguladora = base de cotizacion por contingencias comunes (mensual) / 30 por dia natural; se cobra cada semana disfrutada (7 dias). Sin base minima propia; la base de cotizacion no supera el tope maximo 2026 (5.101,20 EUR/mes, Orden PJC/297/2026 art. 2.1), por lo que la prestacion semanal = min(sueldo bruto mensual, tope) * 7 / 30. Sueldo = base de cotizacion sin tope (pagas prorrateadas).
3. Con 1-5 semanas el progenitor no cumple las 6 obligatorias (todo o nada: 0 = no disfruta, p. ej. sin derecho o sin empleo); mas del maximo no existe. Monoparental: solo el progenitor A; B se ignora.
4. Complemento de empresa (convenio, no es de ley): completa la prestacion hasta el X % del sueldo bruto semanal; nunca resta (max(0, ...)).
5. Perdida bruta de un progenitor = sueldo*7/30*semanas - (prestacion + complemento). Sin IRPF (la prestacion esta exenta, 7.h; el complemento no) ni cotizaciones: no se calcula el neto.
6. Reparto: derecho intransferible, asi que solo se reasigna el TOTAL de semanas disfrutadas entre los dos (cada uno 6..max): el dinero depende solo de cuantas semanas toma cada uno (simultaneo o sucesivo da igual). Optimo = minima perdida total; empate -> el reparto mas cercano al actual. Solo si ambos disfrutan (>= 6) y no es monoparental.
Escenarios: 0 invalido; 1 sin perdida bruta; 2 con perdida y reparto actual ya optimo; 3 con perdida y reparto mejorable (ahorro >= 1 EUR); 4 monoparental o solo disfruta uno (no hay reparto).
Uso: python3 ops/verif/permiso-nacimiento-cuanto-cobro-y-como-repartir_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOPE = 5101.20
def model(d):
    mono = d["mono"] == "si"; amp = int(round(d["amp"]))
    mx = 32 + 2 * amp if mono else 19 + amp
    a = int(round(d["semA"])); b = 0 if mono else int(round(d["semB"]))
    out = dict(bloqueo=0, esc=0, maxA=mx, maxB=0 if mono else mx)
    if a < 0 or b < 0 or a > mx or b > mx: out["bloqueo"] = 1
    elif 0 < a < 6 or 0 < b < 6: out["bloqueo"] = 2
    elif a + b == 0: out["bloqueo"] = 3
    elif (a > 0 and d["sueldoA"] <= 0) or (b > 0 and d["sueldoB"] <= 0): out["bloqueo"] = 4
    if out["bloqueo"]: return out
    def per(s, sem, pct):
        pct = min(max(pct, 0), 100)
        base = min(s, TOPE); wk = base * 7 / 30; cw = max(0.0, pct / 100 * s * 7 / 30 - wk)
        return wk, cw, s * 7 / 30 - wk - cw
    wa, ca, ra = per(d["sueldoA"], a, d["complA"])
    wb, cb, rb = per(d["sueldoB"], b, d["complB"]) if not mono and b > 0 else (0.0, 0.0, 0.0)
    pa, pb = wa * a, wb * b; ka, kb = ca * a, cb * b
    ta, tb = pa + ka, pb + kb
    la, lb = ra * a, rb * b
    out.update(prestA=pa, prestB=pb, complA=ka, complB=kb, totalA=ta, totalB=tb, dejadoA=d["sueldoA"] * 7 / 30 * a, dejadoB=(d["sueldoB"] * 7 / 30 * b if b else 0.0),
               perdidaA=la, perdidaB=lb, prest=pa + pb, compl=ka + kb, total=ta + tb, perdida=la + lb, semanalA=wa, semanalB=wb, rateA=ra, rateB=rb if b else 0.0)
    two = (not mono) and a >= 6 and b >= 6
    if not two:
        out.update(esc=4, optA=a, optB=b, perdidaOpt=la + lb, ahorro=0.0); return out
    T = a + b; best = None
    for x in range(6, mx + 1):
        y = T - x
        if y < 6 or y > mx: continue
        c = x * ra + y * rb
        key = (round(c, 9), abs(x - a))
        if best is None or key < best[0]: best = (key, x, y, c)
    _, x, y, c = best
    ahorro = max(0.0, la + lb - c)
    out.update(optA=x, optB=y, perdidaOpt=c, ahorro=ahorro)
    out["esc"] = 1 if la + lb < 0.5 else (3 if ahorro >= 1 else 2)
    return out
B = dict(sueldoA=3200, sueldoB=2400, mono="no", amp=0, semA=19, semB=19, complA=0, complB=0)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto sin perdida", V()), ("2 A sobre el tope, 19 y 6", V(sueldoA=5800, sueldoB=2400, semA=19, semB=6)), ("3 A en el tope exacto", V(sueldoA=5101.2, semA=19, semB=19)),
 ("4 0 semanas B", V(semB=0)), ("5 monoparental 32", V(mono="si", semA=32, semB=19)), ("6 mono con amp 1", V(mono="si", amp=1, semA=34)),
 ("7 amp parto doble", V(amp=1, semA=20, semB=20)), ("8 complemento 100 % sobre tope", V(sueldoA=6500, complA=100, semA=19, semB=19)), ("9 1 semana invalida", V(semA=3)),
 ("10 mas del maximo", V(semA=20)), ("11 todo 0", V(semA=0, semB=0)), ("12 ambos sobre tope y empate de tasas", V(sueldoA=6000, sueldoB=6000, semA=19, semB=10)),
 ("13 reparto mejorable A 5800 B 3000", V(sueldoA=5800, sueldoB=3000, semA=19, semB=8)), ("14 reparto optimo ya", V(sueldoA=5800, sueldoB=3000, semA=8, semB=19)),
 ("15 complemento 80 %", V(sueldoA=2000, sueldoB=2000, complA=80, complB=100, semA=16, semB=16)), ("16 sueldo B 0 con semanas", V(sueldoB=0))]
KEYS = ["bloqueo", "esc", "maxA", "maxB", "prestA", "prestB", "complA", "complB", "totalA", "totalB", "dejadoA", "dejadoB", "perdidaA", "perdidaB", "prest", "compl", "total", "perdida", "optA", "optB", "perdidaOpt", "ahorro", "semanalA", "semanalB"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/permiso-nacimiento-cuanto-cobro-y-como-repartir.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(48)
    def mk():
        mono = rnd.choice(["no", "no", "no", "si"]); amp = rnd.choice([0, 0, 1, 2, 3])
        mx = 32 + 2 * amp if mono == "si" else 19 + amp
        s = lambda: rnd.choice([0, 1500, 2400, 5101.2, 5101.21, 6000, rnd.uniform(800, 9000)])
        w = lambda: rnd.choice([0, 6, mx, rnd.randint(0, mx + 2), rnd.randint(6, mx)])
        return dict(sueldoA=s(), sueldoB=s(), mono=mono, amp=amp, semA=w(), semB=w(), complA=rnd.choice([0, 0, 60, 100, rnd.uniform(0, 100)]), complB=rnd.choice([0, 0, 80, 100, rnd.uniform(0, 100)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o.get(k, 0)) for k in KEYS if k in o and (j.get(k) is None or abs(j[k] - o[k]) > 0.005)]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("bloqueo", "esc", "total", "perdida", "optA", "optB", "ahorro") if k in o}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
