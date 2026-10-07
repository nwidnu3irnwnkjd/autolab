#!/usr/bin/env python3
"""Tolerancia 0,011 EUR (RDL 29, verificador): subidaAnio = mes redondeado x 12, como el JS.
Oraculo independiente v2 (2026-10-07): actualizacion-renta-alquiler-irav-ipc. Escrito desde la norma (informe journal/verificacion-rdl-28-29-2026.md,
que cita el XML del BOE nº 249: RDL 29/2026 BOE-A-2026-20823, DF 6.ª y art. 3 que reforma LAU 18.1) ANTES de reescribir el .js.
INTERPRETACION (todo «en vigor desde el 8-10-2026, pendiente de convalidacion»)
- Sin clausula de actualizacion (indice 'none'): art. 18.1, sin pacto no hay actualizacion: subida 0, sea cual sea la fecha o el 2 % (la DF 6.ª no crea derecho a subir sin clausula: lectura propia).
- Indice IPC pactado: tope = min(IPC, IRAV) (art. 18.1: IRAV «en todo caso»; DT 4.ª Ley 12/2023 lo extiende a contratos anteriores al 26-5-2023): vale para firma post, pre y ant.
- Clausula sin indice (igc): se actualiza con IRAV (antes IGC): pct = IRAV, exacto. Otro indice pactado: el tope es el IRAV, la subida real puede ser menor (exacto 0).
- firma 'ant' (antes del 6-3-2019): mismo calculo pero orientativo (exacto 0): el regimen anterior a 2019 puede variar segun la clausula.
- DF 6.ª RDL 29/2026: aniversario entre 8-10-2026 y 31-12-2027, cualquier fecha de firma: (a) si la renta supera el limite del indice estatal de precios de referencia: ninguna subida;
  (b) si no, lo que fije un nuevo pacto y, sin el, maximo 2 %: pct = min(pct del contrato, 2). Con 'no lo sé' se calcula como «no supera» pero exacto 0.
- Aniversario fuera de ventana (hasta 7-10-2026 o desde 1-1-2028): solo art. 18.1 (sin tope del 2 %).
- Variacion <= 0: subida maxima 0 (no se calcula bajada). Cobro: mes siguiente al de la notificacion (art. 18.2), asumida en el mes del aniversario; 0 si no se conoce el mes.
- Salida extra: nuevaSinTope = renta actualizada sin el RDL 29 (valor si se derogara, sin efecto retroactivo); ventana = 1 si el aniversario esta en la ventana.
"""
import json, random, subprocess, sys, os
from decimal import Decimal, ROUND_HALF_UP
def redo(x): return float(Decimal(repr(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
INI, FIN = "2026-10-08", "2027-12-31"
def oraculo(d):
    r = float(d["renta"]); f = d["firma"]; ix = d["indice"]; ipc = float(d["ipc"]); irav = float(d["irav"]); pide = float(d["pide"]); an = d["aniv"]; sup = d["sup"]
    out = dict(noModelado=0, exacto=1)
    if ix == "none": base = 0.0
    elif ix == "ipc": base = min(ipc, irav)
    else: base = irav
    base = max(base, 0.0)
    if ix == "otro" or f == "ant": out["exacto"] = 0
    vent = 1 if (INI <= an <= FIN and an != "2000-01-01") else 0
    pct = base
    if ix != "none" and vent:
        if sup == "si": pct = 0.0
        else:
            pct = min(base, 2.0)
            if sup == "nls": out["exacto"] = 0
    nueva = float((Decimal(repr(r)) * (Decimal(100) + Decimal(repr(pct))) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    out.update(pct=pct, nueva=nueva, subidaMes=round(nueva - r, 2), subidaAnio=round(round(nueva - r, 2) * 12, 2),
               mesCobro=0 if an == "2000-01-01" else int(an[5:7]) % 12 + 1, ventana=vent,
               nuevaSinTope=float((Decimal(repr(r)) * (Decimal(100) + Decimal(repr(base))) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
    ex = max(0.0, pide - nueva) if pide > 0 else 0.0
    out.update(excesoMes=round(ex, 2), excesoAnio=round(ex * 12, 2))
    if ix == "none": esc = 1
    elif vent and sup == "si": esc = 6
    elif pct <= 0: esc = 5
    elif pide <= 0: esc = 4
    elif pide <= nueva + 0.005: esc = 2
    else: esc = 3
    out["escenario"] = esc
    return out
ANIVS = ["2000-01-01", "2026-10-08", "2026-11-01", "2026-12-01"] + ["2027-%02d-01" % m for m in range(1, 13)] + ["2028-01-01"]
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/actualizacion-renta-alquiler-irav-ipc.js")).read().split("function eur(")[0]
    random.seed(11); cases = []
    for _ in range(900):
        cases.append(dict(renta=round(random.uniform(1, 3000), 2), firma=random.choice(["post", "pre", "ant"]), indice=random.choice(["none", "ipc", "igc", "otro"]),
                          aniv=random.choice(ANIVS), irav=round(random.uniform(-1, 6), 2), ipc=round(random.uniform(-2, 9), 2),
                          pide=random.choice([0, round(random.uniform(0, 3500), 2)]), sup=random.choice(["no", "si", "nls"])))
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0
    for c, r in zip(cases, res):
        o = oraculo(c)
        for k, v in o.items():
            if r.get(k) is None or abs(r[k] - v) > 0.011: bad += 1; print("DIF", c, k, r.get(k), v)
    print(f"{len(cases)} casos, discrepancias: {bad}"); sys.exit(1 if bad else 0)
