#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para retencion-irpf-nomina-subir-o-no. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado 30/09/2026; LIRPF BOE-A-2006-20764 arts. 19, 20, 52, 57-58, 61, 63, 74, 96, 103 y DA 61.ª; RIRPF BOE-A-2007-6820 arts. 80-88):
1. Impuesto del ejercicio 2026 (declaracion individual, solo rentas del trabajo): rendimiento = bruto1 + bruto2; gastos: SS del trabajador (6,50 % = 4,70+1,55+0,10+0,15, con tope de base 5.101,20 EUR/mes) y 2.000 EUR
   (art. 19.2.f, limite = rendimiento menos SS); reduccion art. 20 sobre (integro - SS) y aplicada al neto; cuota estatal (art. 63) y autonomica (art. 74) = escala(BLG) - escala(minimo), minimo >= 0;
   DA 61.ª: 590,89 EUR (<=17.094) o menos 0,2 por el exceso hasta 20.048,45, limitada a la cuota integra; resultado = cuota liquida - retenciones (art. 103: devolucion si es negativo).
2. Retencion del pagador 1 (RIRPF 80.1.1.º, 82-86): base = retribucion - SS - 2.000 - reduccion art. 20 (calculada sobre integro - SS, 83.3.d) - 600 si >= 3 descendientes (83.3.e);
   cuota = escala_ret(base) - escala_ret(minimo retencion); minimo = 5.550 + descendientes (por mitad salvo uso exclusivo, art. 84.2.º) + 2.800 por menor de 3; tipo = cuota/retribucion a 2 decimales (86.1).
   Sin retencion si la retribucion no supera el limite del art. 81.1 (situacion 3.ª «otras situaciones»: 15.876 / 16.342 / 16.867 segun 0, 1, 2+ descendientes); si retribucion <= 35.200 la cuota no pasa de 43 % de (retribucion - limite) (85.3).
3. Pagador 2: se supone que retiene sin circunstancias comunicadas (art. 88.2): minimo del contribuyente, 0 descendientes, limite 15.876; no hay regla de «exceso a retener» entre pagadores en los arts. 80-88.
4. Tipo voluntario (art. 88.5): se puede pedir un tipo superior; el tipo que deja el resultado en 0 es (cuota liquida - retenido por pagador 2) / bruto1, nunca negativo.
5. Obligacion de declarar (art. 96.2.a y 96.3.a): limite 22.000; 15.876 si hay 2.º pagador cuyo importe supera 1.500; obligado si el total es MAYOR que el limite. El «segundo pagador» es el de menor cuantia (96.3.a.1.º, «por orden de cuantia»).
6. Coste de adelantar/prestar: |resultado| x Euribor/100 durante ~12 meses (supuesto); Hacienda no paga interes salvo demora (art. 103.4).
Uso: python3 ops/verif/retencion-irpf-nomina-subir-o-no_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]
SCALE_EST = [(0, 9.5), (12450, 12), (20200, 15), (35200, 18.5), (60000, 22.5), (300000, 24.5)]
SCALE_RET = [(0, 19), (12450, 24), (20200, 30), (35200, 37), (60000, 45), (300000, 47)]
def scale(x, esc):
    t = 0.0
    for i, (lo, r) in enumerate(esc):
        hi = esc[i + 1][0] if i + 1 < len(esc) else float("inf")
        if x > lo: t += (min(x, hi) - lo) * r / 100
    return t
def minimo(cont, desc, m3, n, k3, mitad):
    return cont + (sum(desc[min(i, 3)] for i in range(n)) + m3 * k3) * (0.5 if mitad else 1)
def art20(rn):
    if rn <= 14852: return 7302
    if rn <= 17673.52: return 7302 - 1.75 * (rn - 14852)
    if rn < 19747.5: return 2364.34 - 1.14 * (rn - 17673.52)
    return 0
SS_R, SS_TOPE = 0.065, 5101.20 * 12
def lim81(n):
    return [15876, 16342, 16867][min(n, 2)]
def retencion(R, n, m3, mitad):
    """tipo de retencion (%, 2 decimales) para un pagador con retribucion R y n descendientes."""
    if R <= 0: return 0.0
    if R <= lim81(n): return 0.0
    ss = SS_R * min(R, SS_TOPE); rn_ab = R - ss
    g = min(2000, rn_ab)
    red = min(art20(rn_ab) if rn_ab < 19747.5 else 0, rn_ab)
    base = max(0.0, rn_ab - g - red - (600 if n >= 3 else 0))
    mn = minimo(5550, [2400, 2700, 4000, 4500], 2800, n, m3, mitad)
    if base - mn <= 0: return 0.0
    cuota = max(0.0, scale(base, SCALE_RET) - scale(mn, SCALE_RET))
    if R <= 35200: cuota = min(cuota, 0.43 * max(0.0, R - lim81(n)))
    return round(cuota / R * 100 + 1e-9, 2)
def model(d):
    R1, ret, n, m3, mitad, R2, cc, eu = d["bruto"], d["ret"], int(d["hijos"]), int(d["menores3"]), d["reparto"] == "mitad", d["pagador2"], d["ccaa"], d["euribor"]
    if cc in ("pv", "navarra") or m3 > n or n > 10 or R1 <= 0:
        return dict(bloqueado=1, escenario=0, tipo0p2=0, cuota=0, cuotaIntegra=0, ded=0, ret1=0, ret2=0, retenido=0, resultado=0, tipo0=0, tipoLegal=0, tipo2=0, obligado=0, limiteObl=0, coste=0)
    R = R1 + R2
    ss = SS_R * min(R, SS_TOPE); rn_ab = R - ss
    g = min(2000, rn_ab)
    rnr = max(0.0, rn_ab - g - art20(rn_ab))
    blg = rnr
    c = PAR["ccaa"][cc]
    desc_e = PAR["minimo_estatal"]["descendientes"]
    mn_e = minimo(PAR["minimo_estatal"]["contribuyente"], desc_e, PAR["minimo_estatal"]["menor3"], n, m3, mitad)
    mc = c["minimo"] or {"contribuyente": 5550, "descendientes": desc_e, "menor3": 2800}
    mn_a = minimo(mc["contribuyente"], mc["descendientes"], mc["menor3"], n, m3, mitad)
    esc_a = [tuple(x) for x in c["escala_general"]]
    ci_e = max(0.0, scale(blg, SCALE_EST) - scale(mn_e, SCALE_EST))
    ci_a = max(0.0, scale(blg, esc_a) - scale(mn_a, esc_a))
    ci = ci_e + ci_a
    ded = 0.0
    if R < 20048.45:
        ded = 590.89 if R <= 17094 else 590.89 - 0.2 * (R - 17094)
        ded = max(0.0, min(ded, ci))
    cuota = ci - ded
    t1 = retencion(R1, n, m3, mitad); t2 = retencion(R2, 0, 0, False) if R2 > 0 else 0.0
    ret1 = R1 * ret / 100; ret2 = R2 * t2 / 100
    resultado = cuota - ret1 - ret2
    tipo0 = min(100.0, max(0.0, (cuota - ret2) / R1 * 100))
    lim = 22000 if ((min(R1, R2) if R2 > 0 else 0) <= 1500) else 15876
    obligado = 1 if R > lim else 0
    esc = (1 if obligado else 4) if resultado > 100 else (2 if resultado < -100 else 3)
    return dict(bloqueado=0, escenario=esc, tipo0p2=min(100.0, max(0.0, (cuota - ret1) / R2 * 100)) if R2 > 0 else 0.0, cuota=cuota, cuotaIntegra=ci, ded=ded, ret1=ret1, ret2=ret2, retenido=ret1 + ret2, resultado=resultado, tipo0=tipo0, tipoLegal=t1, tipo2=t2,
                obligado=obligado, limiteObl=lim, coste=abs(resultado) * eu / 100)
B = dict(bruto=30000, ret=12, hijos=0, menores3=0, reparto="entero", pagador2=0, ccaa="madrid", euribor=3.247)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto", V()), ("2 dos hijos mitad Madrid", V(bruto=40000, hijos=2, reparto="mitad", ret=14)), ("3 segundo pagador 6.000", V(bruto=28000, pagador2=6000, ret=11)),
 ("4 bruto 15.876 (no retiene)", V(bruto=15876, ret=0)), ("5 bruto 15.877", V(bruto=15877, ret=1)), ("6 DA 61 bruto 17.094", V(bruto=17094, ret=0)), ("7 bruto 20.048,45", V(bruto=20048.45, ret=5)),
 ("8 hijo menor de 3 y 3 hijos Cataluna", V(bruto=55000, hijos=3, menores3=1, ccaa="cataluna", ret=20)), ("9 pv bloqueado", V(ccaa="pv")), ("10 alto 120.000", V(bruto=120000, ret=30, ccaa="valencia")),
 ("11 segundo pagador 1.500 / 1.501", V(bruto=21000, pagador2=1501, ret=9)), ("12 retencion 0 devuelve", V(bruto=45000, ret=0)), ("13 tope SS", V(bruto=80000, ret=25, ccaa="andalucia")),
 ("14 4 hijos exclusivo", V(bruto=36000, hijos=4, menores3=2, ret=8)), ("15 bruto 35.200", V(bruto=35200, ret=15, ccaa="galicia")), ("16 menores3 > hijos", V(hijos=1, menores3=2)),
 ("17 pagador2 18.000", V(bruto=30000, pagador2=18000, ret=13, ccaa="clm"))]
KEYS = ["bloqueado", "escenario", "tipo0p2", "cuota", "cuotaIntegra", "ded", "ret1", "ret2", "retenido", "resultado", "tipo0", "tipoLegal", "tipo2", "obligado", "limiteObl", "coste"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/retencion-irpf-nomina-subir-o-no.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(26)
    ccs = list(PAR["ccaa"].keys()) + ["pv"]
    def mk():
        n = rnd.choice([0, 0, 1, 2, 3, 4, 5]); return dict(bruto=rnd.choice([rnd.uniform(8000, 25000), rnd.uniform(15000, 60000), rnd.uniform(20000, 150000), 15876, 17094, 20048.45, 35200]),
            ret=rnd.choice([0, rnd.uniform(0, 30)]), hijos=n, menores3=rnd.randint(0, n), reparto=rnd.choice(["entero", "mitad"]), pagador2=rnd.choice([0, 0, 800, 1500, 1501, rnd.uniform(0, 30000)]),
            ccaa=rnd.choice(ccs), euribor=rnd.choice([3.247, rnd.uniform(0, 5)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > (0.005 if k in ("tipoLegal", "tipo2", "tipo0", "tipo0p2") else 0.5)]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("cuota", "ret1", "ret2", "resultado", "tipo0", "tipoLegal", "obligado")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
