#!/usr/bin/env python3
"""Oraculo independiente: fianza y garantias adicionales del alquiler (LAU 36.1, 36.5, 17.2, 20.1). Escrito desde la norma antes de abrir el .js.
INTERPRETACION
- Fianza (art. 36.1): obligatoria en metalico, 1 mensualidad en vivienda, 2 en uso distinto. Lo pedido por encima como «fianza» es garantia adicional en metalico (art. 36.5) y suma en el tope de 2 mensualidades (o sin tope donde no aplica).
- Garantia adicional (art. 36.5): cualquier tipo, pero en VIVIENDA con contrato de hasta 5 anos (hasta 7 si el arrendador es persona juridica) su valor <= 2 mensualidades.
  Borde: «hasta» = incluido el 5 (o el 7). Por encima de esa duracion pactada, y en uso distinto, la ley no pone tope: se admite lo pedido.
- Pago anticipado (art. 17.2, solo vivienda): nunca mas de 1 mensualidad (incluye la del primer mes). En uso distinto no hay tope en la tabla: se admite lo pedido.
- Gestion inmobiliaria y formalizacion (art. 20.1, vivienda): a cargo del arrendador SIEMPRE (persona fisica o juridica, Ley 12/2023): la comision pedida no es exigible.
  En uso distinto el art. 20 no aplica: se admite lo pedido.
- Duracion = la pactada (sin prorrogas tacitas). Renta e importes en euros; meses decimales admitidos.
"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/fianza-y-garantias-adicionales-alquiler.js")

def model(d):
    R = d["renta"]; viv = d["tipo"] == "viv"
    fl = (1 if viv else 2) * R
    lim = 7 if d["arr"] == "pj" else 5
    sin = 0 if (viv and d["duracion"] <= lim) else 1
    extra_f = max(0, d["fianza"] * R - fl)
    pg = d["garantia"] * R + extra_f
    gm = pg if sin else 2 * R
    adm = (1 * R) if viv else d["adelanto"] * R
    cm = 0 if viv else d["comision"]
    ex_f = 0
    ex_g = max(0, pg - gm)
    ex_a = max(0, d["adelanto"] * R - adm)
    ex_c = max(0, d["comision"] - cm)
    ped = (d["fianza"] + d["garantia"] + d["adelanto"]) * R + d["comision"]
    no = ex_f + ex_g + ex_a + ex_c
    return dict(fianzaLegal=fl, garantiaMax=gm, sinTope=sin, limiteAnios=lim, maxLegal=fl + gm + adm + cm, pedido=ped, exigible=ped - no, noExigible=no,
                exFianza=ex_f, exGarantia=ex_g, exAdelanto=ex_a, exComision=ex_c)

KEYS = list(model(dict(renta=1, tipo="viv", duracion=5, arr="pf", fianza=1, garantia=1, adelanto=1, comision=0)))
def js(cases):
    src = open(JS).read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
B = dict(renta=900, tipo="viv", duracion=5, arr="pf", fianza=1, garantia=3, adelanto=1, comision=900)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 ejemplo", V()), ("2 garantia justa 2", V(garantia=2, comision=0)), ("3 garantia 2,01", V(garantia=2.01, comision=0)), ("4 5 anos pf limita", V(duracion=5, garantia=4)),
 ("5 6 anos pf sin tope", V(duracion=6, garantia=4, comision=0)), ("6 7 anos pj limita", V(arr="pj", duracion=7, garantia=3)), ("7 8 anos pj sin tope", V(arr="pj", duracion=8, garantia=3)),
 ("8 uso distinto", V(tipo="uso", fianza=3, garantia=5, adelanto=2, comision=500)), ("9 fianza 2 en vivienda", V(fianza=2, garantia=0, adelanto=2, comision=0)), ("10 todo cero", V(fianza=0, garantia=0, adelanto=0, comision=0))]
if __name__ == "__main__":
    rnd = random.Random(57)
    def mk():
        return dict(renta=rnd.choice([0, 300, 900, rnd.uniform(0, 4000)]), tipo=rnd.choice(["viv", "viv", "uso"]), duracion=rnd.choice([1, 3, 5, 5.5, 6, 7, 8, 10, rnd.uniform(0.5, 12)]),
                    arr=rnd.choice(["pf", "pj"]), fianza=rnd.choice([0, 1, 2, 3, rnd.uniform(0, 4)]), garantia=rnd.choice([0, 1, 2, 2.0001, 3, rnd.uniform(0, 6)]),
                    adelanto=rnd.choice([0, 1, 2, rnd.uniform(0, 3)]), comision=rnd.choice([0, 300, rnd.uniform(0, 3000)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.005]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("fianzaLegal", "garantiaMax", "maxLegal", "pedido", "exigible", "noExigible")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
