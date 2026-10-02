#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal Sonnet, 2026-10-02) para baja-medica-cuanto-cobro-incapacidad-temporal. Escrito desde la norma ANTES del .js; calcula DIA A DIA (el JS usa tramos).
INTERPRETACION (BOE consolidado leido el 2/10/2026: LGSS arts. 169, 172, 173, 174; RD 53/1980 art. unico; Decreto 3158/1966 art. 2; Orden 13-10-1967 art. 2; Orden PJC/297/2026 art. 2.1):
1. Enfermedad comun o accidente no laboral: dias 1-3 sin subsidio (173.1: «a partir del cuarto dia de baja»); dias 4-20 el 60 % de la base reguladora (RD 53/1980); desde el dia 21 el 75 % (Decreto 3158/1966 art. 2.1). Dias 4-15 los paga la empresa (173.1) y desde el 16 la entidad gestora o la mutua (Seguridad Social, pagina de cuantia).
2. Accidente de trabajo o enfermedad profesional: el dia de la baja la empresa paga el salario integro (173.1); desde el dia siguiente, subsidio del 75 % de la base reguladora (Decreto 3158/1966 art. 2.1) a cargo de la entidad gestora o la mutua. Sin carencia (172.b).
3. Base reguladora diaria = base de cotizacion del mes anterior / 30 (Decreto 1646/1972 art. 13.1-2; la base no supera la base maxima 5.101,20 EUR/mes, Orden PJC/297/2026 art. 2.1). Sueldo mensual con 14 pagas sin prorratear: base = sueldo x 14 / 12. En AT/EP no se modelan las horas extra (su media se suma a la base: la prestacion real puede ser mayor).
4. Duracion maxima 365 dias + prorroga de 180 (169.1.a); la IT se extingue a los 545 dias naturales (174.1) pero hay prolongacion de efectos economicos hasta la resolucion de la IP (174.5, maximo 730 dias, 174.2): mas de 545 = fuera del modelo (no se calcula).
5. Mejora del convenio (no es de ley): la empresa completa hasta el X % del sueldo habitual cada dia de baja (incluidos los 3 primeros de comun), nunca resta. Perdida = sueldo habitual de los dias de baja - lo cobrado (subsidio + mejora + salario del dia de la baja en AT). Neto aprox. = perdida x (1 - tipo marginal); no se modelan cotizaciones.
Escenarios: 0 invalido; 1 sin perdida (la mejora iguala el sueldo); 2 comun hasta 3 dias (sin subsidio); 3 con perdida y sin mejora; 4 con perdida y mejora parcial.
Uso: python3 ops/verif/baja-medica-cuanto-cobro-incapacidad-temporal_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOPE = 5101.20
def model(d):
    out = dict(bloqueo=0, esc=0)
    n = int(round(d["dias"]))
    if not d["sueldo"] > 0: out["bloqueo"] = 3
    elif n < 1: out["bloqueo"] = 2
    elif n > 545: out["bloqueo"] = 1
    if out["bloqueo"]: return out
    prof = d["cont"] == "prof"
    mens = d["sueldo"] * 14 / 12 if d["pagas"] == "14" else d["sueldo"]
    br = min(mens, TOPE) / 30; sal = mens / 30
    m = min(max(d["mejora"], 0), 100) / 100; t = min(max(d["tipo"], 0), 100) / 100
    prest = compl = salfull = emp_sub = 0.0; perd3 = 0.0
    for k in range(1, n + 1):
        sal_day = False
        if prof:
            if k == 1: sub = 0.0; sal_day = True
            else: sub = 0.75 * br
        else:
            sub = 0.0 if k <= 3 else (0.60 * br if k <= 20 else 0.75 * br)
        c = 0.0 if sal_day else max(0.0, m * sal - sub)
        prest += sub; compl += c
        if sal_day: salfull += sal
        if (not prof) and 4 <= k <= 15: emp_sub += sub
        if k <= 3: perd3 += sal - sub - c - (sal if sal_day else 0.0)
    ingreso = prest + compl + salfull; hab = n * sal; perd = hab - ingreso
    out.update(brDia=br, salDia=sal, prest=prest, compl=compl, ingreso=ingreso, habitual=hab, perdida=perd, perdida3=perd3, perdidaNeta=perd * (1 - t),
               empresa=emp_sub + compl + salfull, entidad=prest - emp_sub)
    out["esc"] = 1 if perd < 0.5 else (2 if prest == 0 else (3 if m == 0 else 4))
    return out
B = dict(sueldo=2200, pagas="prorr", cont="comun", dias=30, mejora=0, tipo=0)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto comun 30 dias", V()), ("2 borde 3 dias", V(dias=3)), ("3 borde 4 dias", V(dias=4)), ("4 borde 15", V(dias=15)), ("5 borde 16", V(dias=16)), ("6 borde 20", V(dias=20)),
 ("7 borde 21", V(dias=21)), ("8 profesional 10", V(cont="prof", dias=10)), ("9 profesional 1 dia", V(cont="prof", dias=1)), ("10 sobre la base maxima", V(sueldo=6000, dias=40)),
 ("11 14 pagas", V(sueldo=1800, pagas="14", dias=45)), ("12 mejora 100", V(mejora=100)), ("13 mejora 60 y tipo 24", V(mejora=60, dias=10, tipo=24)), ("14 mas de 545", V(dias=546)),
 ("15 0 dias", V(dias=0)), ("16 sueldo 0", V(sueldo=0)), ("17 545 dias", V(dias=545)), ("18 365 dias prof con mejora 90", V(cont="prof", dias=365, mejora=90)), ("19 mejora 100 y 3 dias", V(dias=3, mejora=100)),
 ("20 base maxima exacta", V(sueldo=5101.2, dias=25))]
KEYS = ["bloqueo", "esc", "brDia", "salDia", "prest", "compl", "ingreso", "habitual", "perdida", "perdida3", "perdidaNeta", "empresa", "entidad"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/baja-medica-cuanto-cobro-incapacidad-temporal.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(53)
    def mk():
        return dict(sueldo=rnd.choice([0, 1000, 2200, 5101.2, 5101.21, 7000, rnd.uniform(600, 9000)]), pagas=rnd.choice(["prorr", "14"]), cont=rnd.choice(["comun", "comun", "prof"]),
                    dias=rnd.choice([0, 1, 2, 3, 4, 15, 16, 20, 21, 365, 545, 546, rnd.randint(1, 545)]), mejora=rnd.choice([0, 0, 50, 100, rnd.uniform(0, 100)]), tipo=rnd.choice([0, 19, rnd.uniform(0, 47)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o.get(k, 0)) for k in KEYS if k in o and (j.get(k) is None or abs(j[k] - o[k]) > 0.005)]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("bloqueo", "esc", "prest", "compl", "perdida", "perdida3", "empresa", "entidad") if k in o}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
