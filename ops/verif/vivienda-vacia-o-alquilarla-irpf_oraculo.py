#!/usr/bin/env python3
"""Oraculo independiente: piso vacio o alquilado, IRPF (imputacion art. 85 LIRPF vs rendimiento del capital inmobiliario). Escrito desde la norma antes de abrir el .js.
INTERPRETACION
- Texto: LIRPF art. 85.1 (Ley 26/2014): renta imputada = 2 % del valor catastral (1,1 % si los valores se revisaron y entraron en vigor en los 10 periodos previos), proporcional a los dias; art. 24 (original 2006); art. 23.1 y 23.2 (Ley 12/2023); NO el RDL 26/2026 (derogado, BOE-A-2026-20526).
- VACIO TODO EL AÑO (365 dias): tributa la imputacion completa; no hay ingresos ni gastos deducibles. Resultado = -gastos - cuota (los gastos se pagan igual; la amortizacion se trata como coste).
- ALQUILADO (365 - dv dias): ingresos = 12 x renta x dias/365; gastos deducibles = gastos anuales x dias/365 (Manual AEAT: amortizacion por dias alquilados; supuesto propio para el resto de gastos);
  rendimiento previo = ingresos - gastos deducibles; reduccion 23.2 solo si es positivo; los dv dias vacios tributan imputacion (art. 85, proporcional a dias).
- FAMILIAR (art. 24, hasta 3.er grado): rendimiento neto reducido = mayor entre el reducido y el minimo = imputacion de los dias alquilados (reglas del art. 85). Manual AEAT: «el mayor de las dos cantidades».
- Cuota = (max(rendimiento final, 0) + imputacion dias vacios) x tipo marginal; las perdidas no se compensan con otras rentas.
- Umbral: renta mensual desde la que alquilar paga mas IRPF que tenerlo vacio = (gastos ded. + minimo/(1-p)) x 365 / (12 x dias alquilados); con familiar es la renta bajo la cual Hacienda aplica el minimo (tributas lo mismo que vacio).
"""
import json, os, random, subprocess, sys
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/vivienda-vacia-o-alquilarla-irpf.js")

def model(d):
    cat, g, R, t, dv = F(str(d["cat"])), F(str(d["gastos"])), F(str(d["renta"])), F(str(d["tipo"])) / 100, int(d["dv"])
    pimp = F(11, 1000) if d["rev"] in ("r", "r12") else F(2, 100)   # r12: DA 55.ª (RDL 29/2026, efectos 1-1-2026): revisiones 2012-2015 tambien 1,1 % en 2026
    p = F(int(d["contrato"]), 100)
    da = 365 - dv
    impA = cat * pimp
    cuotaA = impA * t
    resA = -g - cuotaA
    ing = 12 * R * da / 365
    gded = g * da / 365
    prev = ing - gded
    red = prev * (1 - p) if prev > 0 else prev
    minimo = impA * da / 365
    fam = d["fam"] == "si"
    redf = max(red, minimo) if fam else red
    impdv = impA * dv / 365
    cuotaB = (max(redf, 0) + impdv) * t
    resB = ing - g - cuotaB
    dif = resB - resA
    rstar = (gded + minimo / (1 - p)) * 365 / (12 * da)
    o = dict(impA=impA, cuotaA=cuotaA, resA=resA, ing=ing, prev=prev, red=red, minimo=minimo, redf=redf, impdv=impdv,
             cuotaB=cuotaB, resB=resB, dif=dif, rstar=rstar, famAplica=int(fam and red < minimo), dobleCuota=cuotaB - cuotaA)
    return {k: float(v) for k, v in o.items()}

KEYS = list(model(dict(cat=1, gastos=0, renta=0, tipo=0, dv=0, rev="r", contrato="50", fam="no")))
def js(cases):
    src = open(JS).read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
B = dict(cat=60000, rev="r", dv=0, renta=800, gastos=7000, contrato="50", fam="no", tipo=30)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 ejemplo", V()), ("2 imputacion 2 %", V(rev="g")), ("3 renta en el umbral 693,33", V(renta=693.33)), ("4 familiar renta 650 (minimo)", V(fam="si", renta=650)),
 ("5 familiar renta 800", V(fam="si")), ("6 60 dias vacio", V(dv=60)), ("7 364 dias vacio", V(dv=364)), ("8 reduccion 90", V(contrato="90")), ("9 reduccion 70 familiar", V(contrato="70", fam="si", renta=600)),
 ("10 perdida", V(gastos=12000)), ("11 gastos 0", V(gastos=0)), ("12 renta 0", V(renta=0)), ("13 tipo 0", V(tipo=0)), ("14 tipo 54", V(tipo=54)), ("15 catastral 0", V(cat=0)),
 ("16 neto 0 exacto", V(renta=7000 / 12)), ("17 familiar renta 0", V(fam="si", renta=0)), ("18 familiar con vacio 120", V(fam="si", dv=120, renta=500)), ("19 revision 2012-2015 (DA 55.a, RDL 29)", V(rev="r12")), ("20 r12 familiar vacio 60", V(rev="r12", fam="si", dv=60, renta=500))]
if __name__ == "__main__":
    rnd = random.Random(60)
    def mk():
        return dict(cat=rnd.choice([0, 20000, 60000, 150000, round(rnd.uniform(0, 400000), 2)]), rev=rnd.choice(["r", "r12", "g"]), dv=rnd.choice([0, 0, 1, 30, 180, 364, rnd.randint(0, 364)]),
                    renta=rnd.choice([0, 400, 800, 1500, round(rnd.uniform(0, 3500), 2)]), gastos=rnd.choice([0, 3000, 7000, 12000, round(rnd.uniform(0, 30000), 2)]),
                    contrato=rnd.choice(["50", "60", "70", "90"]), fam=rnd.choice(["no", "si"]), tipo=rnd.choice([0, 19, 30, 37, 45, 54, round(rnd.uniform(0, 54), 1)]))
    sweep = [mk() for _ in range(900)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.01]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("impA", "cuotaA", "resA", "cuotaB", "resB", "dif", "rstar")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print("casos:", len(allc), "discrepancias:", bad)
    sys.exit(1 if bad else 0)
