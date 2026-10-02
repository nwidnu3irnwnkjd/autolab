#!/usr/bin/env python3
"""Oraculo independiente: actualizacion-renta-alquiler-irav-ipc (LAU art. 18.1-2 + DA 11.a). Escrito desde la norma antes del .js.
INTERPRETACION
- Sin clausula de actualizacion (indice 'none'): art. 18.1 "En defecto de pacto expreso, no se aplicara actualizacion": subida 0, sea cual sea la fecha.
- Indice IPC pactado: sube como mucho la variacion del IPC (art. 18.1 ultimo parrafo: tope IPC en todo caso).
- Clausula sin indice (igc): art. 18.1 -> IGC, siempre con tope IPC; no hay IGC en el modelo: se da el TOPE (IPC) y exacto=0.
- Otro indice pactado: igual, solo el TOPE (exacto=0).
- Contratos firmados desde 26-5-2023 ('post'): ademas el IRAV es limite de referencia (DA 11.a, confianza B): tope = min(IPC, IRAV).
- Contratos entre 6-3-2019 y 25-5-2023 ('pre'): regla del art. 18 vigente al firmar (DT 4.a Ley 12/2023): tope IPC; el IRAV no aplica.
- Anteriores a 6-3-2019 ('ant'): no se modela (noModelado=1).
- Variacion <= 0: la subida maxima es 0 (no se calcula bajada de renta). Cobro: mes siguiente al de la notificacion (art. 18.2).
- Tope del 2 % RDL 26/2026: derogado, no existe.
"""
import json, random, subprocess, sys, os
def oraculo(d):
    r = float(d["renta"]); f = d["firma"]; ix = d["indice"]; ipc = float(d["ipc"]); irav = float(d["irav"]); pide = float(d["pide"]); mes = int(d["mes"])
    out = dict(noModelado=0, exacto=1, pct=0.0)
    if f == "ant":
        out.update(noModelado=1, exacto=0); return out
    if ix == "none": pct = 0.0
    else:
        pct = ipc if f == "pre" else min(ipc, irav)
        if ix in ("igc", "otro"): out["exacto"] = 0
        pct = max(pct, 0.0)
    nueva = round(r * (1 + pct / 100), 2)
    out.update(pct=pct, nueva=nueva, subidaMes=round(nueva - r, 2), subidaAnio=round((nueva - r) * 12, 2), mesCobro=mes % 12 + 1)
    ex = max(0.0, pide - nueva) if pide > 0 else 0.0
    out.update(excesoMes=round(ex, 2), excesoAnio=round(ex * 12, 2))
    if ix == "none": esc = 1
    elif pct <= 0: esc = 5
    elif pide <= 0: esc = 4
    elif pide <= nueva + 0.005: esc = 2
    else: esc = 3
    out["escenario"] = esc
    return out
if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    js = open(os.path.join(base, "projects/decidir/calcs/actualizacion-renta-alquiler-irav-ipc.js")).read().split("function eur(")[0]
    random.seed(7); cases = []
    for _ in range(800):
        cases.append(dict(renta=round(random.uniform(0, 3000), 2), firma=random.choice(["post", "pre", "ant"]), indice=random.choice(["none", "ipc", "igc", "otro"]),
                          mes=random.randint(1, 12), irav=round(random.uniform(-1, 6), 2), ipc=round(random.uniform(-2, 9), 2), pide=random.choice([0, round(random.uniform(0, 3500), 2)]), zona=random.choice(["no", "zt", "gt"])))
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    res = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True, check=True).stdout)
    bad = 0
    for c, r in zip(cases, res):
        o = oraculo(c)
        for k, v in o.items():
            if r.get(k) is None or abs(r[k] - v) > 1: bad += 1; print("DIF", c, k, r.get(k), v)
    print(f"{len(cases)} casos, discrepancias: {bad}"); sys.exit(1 if bad else 0)
