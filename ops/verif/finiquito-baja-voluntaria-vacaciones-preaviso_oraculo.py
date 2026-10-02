#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para finiquito-baja-voluntaria-vacaciones-preaviso. Escrito desde la norma ANTES del .js.
INTERPRETACION (ET BOE-A-2015-11430 arts. 29, 31, 38.1, 49.1.d, 49.2; LGSS BOE-A-2015-11724 art. 147.1 y Orden PJC/297/2026; RIRPF art. 80.1; LIRPF art. 17.1.a):
1. Finiquito de baja voluntaria = lo adeudado al extinguirse el contrato (art. 49.2: propuesta de liquidacion): salario del mes de salida (art. 29: se paga lo trabajado),
   parte proporcional de las pagas extra (art. 31) y vacaciones devengadas y no disfrutadas. Convencion propia (la ley no la fija): salario del mes = mensual ordinario x dia de salida / dias naturales del mes (2026).
2. Pagas: con 12 pagas el bruto anual ya las prorratea en la mensualidad (bruto/12): nada pendiente. Con 14, mensual ordinario = bruto/14 y 2 pagas de una mensualidad; supuesto (convenio puede cambiarlo):
   verano devenga 1-ene..30-jun y se cobra en junio, Navidad devenga 1-jul..31-dic y se cobra en diciembre -> pendiente = mensual x dias del semestre en curso hasta la salida (incluida) / dias del semestre (181 o 184 en 2026).
3. Vacaciones (art. 38.1: minimo 30 dias naturales, "no sustituible por compensacion economica"): la compensacion al extinguirse la relacion es doctrina del TS y art. 11 Convenio 132 OIT, no literal del ET; LGSS 147.1 confirma que se
   liquidan y cotizan. Devengadas = dias del anio (convenio, >= 30) x dia del anio de salida / 365 (se supone alta anterior al 1-ene); pendientes = max(0, devengadas - disfrutadas); valor = pendientes x bruto/365 (supuesto: dia natural = bruto anual/365).
   Si disfrutadas > devengadas hay exceso (aviso; no se descuenta).
4. Preaviso (art. 49.1.d: el que fijen convenios o la costumbre; la consecuencia economica la fija convenio/contrato): descuento = dias incumplidos x bruto/365. No supera el finiquito devengado (el resto se avisa).
5. Cotizacion del trabajador 6,5 % (4,70 CC + 1,55 desempleo indefinido + 0,10 FP + 0,15 MEI; Orden de cotizacion 2026) sobre (salario del mes + prorrata mensual de pagas del mes: 2*m/12*dia/diasMes; la paga pendiente YA cotizo por prorrata, RD 2064/1995 art. 23.1.A) con tope 5.101,20 EUR/mes mas vacaciones con tope 5.101,20 por mes afectado
   (LGSS 147.1: liquidacion complementaria sin prorrateo y con el tope del mes o meses afectados; meses = ceil(dias/30)). Aproximacion declarada. Solidaridad (>5.101,20) no modelada.
6. IRPF: sueldos y salarios (LIRPF 17.1.a); retencion = tipo x cuantia total de las retribuciones (RIRPF 80.1) = tipo del usuario x bruto devengado (antes del descuento por preaviso).
7. Neto = bruto devengado - descuento aplicado - cotizacion - IRPF (no negativo). Escenarios: 3 preaviso incumplido; 4 exceso de vacaciones disfrutadas; 2 vacaciones pendientes; 1 resto.
Bloqueos: bruto<=0, pagas no 12/14, mes fuera 1-12, dia fuera del mes, vacaciones del anio < 30 o > 90, disfrutadas < 0 o > del anio, preaviso <0 o >90, tipo fuera 0-47.
Uso: python3 ops/verif/finiquito-baja-voluntaria-vacaciones-preaviso_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random, math
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "finiquito-baja-voluntaria-vacaciones-preaviso"
DM = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TOPE = F("5101.2")

def model(d):
    bruto = F(str(d["bruto"])); pagas = int(d["pagas"]); mes = int(d["mes"]); dia = int(d["dia"]); va = F(str(d["vacAnual"])); vd = F(str(d["vacDisf"])); inc = F(str(d["incumple"])); tipo = F(str(d["tipo"]))
    z = dict(bloqueado=1, escenario=0, salMes=0, pagasPend=0, vacDev=0, vacPend=0, vacImporte=0, brutoDev=0, descuento=0, descAplicado=0, cot=0, irpf=0, neto=0, exceso=0, salDia=0, doy=0)
    if bruto <= 0 or pagas not in (12, 14) or not (1 <= mes <= 12) or dia < 1 or dia > DM[mes - 1] or va < 30 or va > 90 or vd < 0 or vd > va or inc < 0 or inc > 90 or tipo < 0 or tipo > 47:
        return z
    m = bruto / pagas
    sal_dia = bruto / 365
    doy = sum(DM[:mes - 1]) + dia
    sal_mes = m * dia / DM[mes - 1]
    if pagas == 14:
        if doy <= 181: pp = m * doy / 181
        else: pp = m * (doy - 181) / 184
    else:
        pp = F(0)
    dev = va * doy / 365
    pend = max(F(0), dev - vd); exceso = max(F(0), vd - dev)
    imp = pend * sal_dia
    bruto_dev = sal_mes + pp + imp
    desc = inc * sal_dia
    desc_ap = min(desc, bruto_dev)
    meses_vac = math.ceil(pend / 30) if pend > 0 else 0
    prorr = (2 * m / 12) * dia / DM[mes - 1] if pagas == 14 else F(0)  # RGC art. 23.1.A: pagas prorrateadas en 12 meses (ya cotizaron)
    base = min(sal_mes + prorr, TOPE) + min(imp, TOPE * meses_vac)
    cot = base * F(65, 1000)
    irpf = bruto_dev * tipo / 100
    neto = max(F(0), bruto_dev - desc_ap - cot - irpf)
    esc = 3 if inc > 0 else (4 if exceso > F(1, 2) else (2 if pend > F(1, 2) else 1))
    return dict(bloqueado=0, escenario=esc, salMes=float(sal_mes), pagasPend=float(pp), vacDev=float(dev), vacPend=float(pend), vacImporte=float(imp), brutoDev=float(bruto_dev), descuento=float(desc), descAplicado=float(desc_ap),
                cot=float(cot), irpf=float(irpf), neto=float(neto), exceso=float(exceso), salDia=float(sal_dia), doy=doy)
KEYS = ["bloqueado", "escenario", "salMes", "pagasPend", "vacDev", "vacPend", "vacImporte", "brutoDev", "descuento", "descAplicado", "cot", "irpf", "neto", "exceso", "salDia", "doy"]

def js(cases):
    src = open(os.path.join(ROOT, "projects", "decidir", "calcs", SLUG + ".js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)

FIX = [
    ("defecto: 24000, 14 pagas, 15 oct, 30 dias, 18 disfrutados", dict(bruto=24000, pagas=14, mes=10, dia=15, vacAnual=30, vacDisf=18, incumple=0, tipo=15)),
    ("ultimo dia del mes (31 oct), 12 pagas", dict(bruto=24000, pagas=12, mes=10, dia=31, vacAnual=30, vacDisf=18, incumple=0, tipo=15)),
    ("0 dias pendientes (disfrutadas = devengadas)", dict(bruto=24000, pagas=12, mes=12, dia=31, vacAnual=30, vacDisf=30, incumple=0, tipo=15)),
    ("preaviso incumplido 15 dias, 14 pagas", dict(bruto=30000, pagas=14, mes=3, dia=20, vacAnual=30, vacDisf=0, incumple=15, tipo=18)),
    ("exceso de vacaciones disfrutadas", dict(bruto=24000, pagas=12, mes=3, dia=31, vacAnual=30, vacDisf=20, incumple=0, tipo=15)),
    ("14 pagas el 30 de junio (verano completa)", dict(bruto=21000, pagas=14, mes=6, dia=30, vacAnual=30, vacDisf=10, incumple=0, tipo=12)),
    ("14 pagas el 1 de julio (Navidad 1 dia)", dict(bruto=21000, pagas=14, mes=7, dia=1, vacAnual=30, vacDisf=10, incumple=0, tipo=12)),
    ("tope de cotizacion, sueldo alto", dict(bruto=120000, pagas=12, mes=8, dia=31, vacAnual=30, vacDisf=0, incumple=0, tipo=40)),
    ("febrero 28", dict(bruto=18000, pagas=12, mes=2, dia=28, vacAnual=23 + 7, vacDisf=0, incumple=0, tipo=2)),
    ("bloqueo: 31 de abril", dict(bruto=24000, pagas=12, mes=4, dia=31, vacAnual=30, vacDisf=0, incumple=0, tipo=15)),
    ("bloqueo: disfrutadas > anuales", dict(bruto=24000, pagas=12, mes=4, dia=30, vacAnual=30, vacDisf=31, incumple=0, tipo=15)),
    ("bloqueo: tipo 48", dict(bruto=24000, pagas=12, mes=4, dia=30, vacAnual=30, vacDisf=0, incumple=0, tipo=48)),
]
if __name__ == "__main__":
    rnd = random.Random(38)
    def mk():
        mes = rnd.randint(1, 12); va = rnd.choice([30, 30, 30, 31, 32, 36, rnd.uniform(30, 60)])
        return dict(bruto=rnd.choice([rnd.uniform(9000, 25000), rnd.uniform(15000, 60000), rnd.uniform(40000, 200000), 14000, 24000]), pagas=rnd.choice([12, 14]), mes=mes, dia=rnd.choice([1, DM[mes - 1], rnd.randint(1, DM[mes - 1])]),
                    vacAnual=va, vacDisf=rnd.choice([0, round(rnd.uniform(0, va), 1), va, round(rnd.uniform(0, va), 0)]), incumple=rnd.choice([0, 0, 7, 15, 30, rnd.randint(0, 90)]), tipo=rnd.choice([0, 2, 15, rnd.uniform(0, 47), 47]))
    sweep = [mk() for _ in range(900)]
    allc = [c for _, c in FIX] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > (0.5 if k not in ("bloqueado", "escenario", "doy") else 0)]
        if i < len(FIX): print(FIX[i][0], {k: round(o[k], 2) for k in ("brutoDev", "descAplicado", "cot", "irpf", "neto", "escenario")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(FIX): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(FIX)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
