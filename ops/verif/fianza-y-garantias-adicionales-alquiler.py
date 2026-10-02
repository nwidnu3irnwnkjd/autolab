"""Verificador fiscal/legal c57 · fianza-y-garantias-adicionales-alquiler · 2026-10-02.
Casos nuevos (LAU 36.1 + 36.5): el exceso pedido como «fianza» es una garantia adicional en metalico
(art. 36.5: «cualquier tipo de garantia ... adicional a la fianza en metalico») y computa en el tope de 2 mensualidades
junto con la garantia; sin tope (duracion > 5/7 o uso distinto) es exigible.
Uso: python3 ops/verif/fianza-y-garantias-adicionales-alquiler.py  (ejecuta el JS con node si existe; si no, compara con el oraculo del Constructor y muestra la diferencia esperada)."""
import json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/fianza-y-garantias-adicionales-alquiler.js")

def esperado(d):
    R = d["renta"]; viv = d["tipo"] == "viv"
    fm = 1 if viv else 2
    lim = 7 if d["arr"] == "pj" else 5
    tope = viv and d["duracion"] <= lim
    extra_f = max(0, d["fianza"] - fm)            # exceso de «fianza» = garantia adicional en metalico
    g_total = d["garantia"] + extra_f
    exG = max(0, g_total - 2) * R if tope else 0   # exceso conjunto sobre 2 mensualidades
    exA = max(0, d["adelanto"] - 1) * R if viv else 0
    exC = d["comision"] if viv else 0
    return round(exG + exA + exC, 2)

CASOS = [  # (entrada, noExigible esperado)
    (dict(renta=900, tipo="viv", duracion=5, arr="pf", fianza=2, garantia=0, adelanto=1, comision=0), 0),
    (dict(renta=900, tipo="viv", duracion=5, arr="pf", fianza=2, garantia=2, adelanto=1, comision=0), 900),
    (dict(renta=900, tipo="viv", duracion=6, arr="pf", fianza=3, garantia=0, adelanto=1, comision=0), 0),
    (dict(renta=900, tipo="uso", duracion=5, arr="pf", fianza=3, garantia=0, adelanto=1, comision=0), 0),
    (dict(renta=900, tipo="viv", duracion=5, arr="pf", fianza=1, garantia=3, adelanto=1, comision=900), 1800),
    (dict(renta=900, tipo="viv", duracion=7, arr="pj", fianza=1, garantia=3, adelanto=1, comision=0), 900),
]

def js_no_exigible(d):
    src = open(JS, encoding="utf8").read().split("function eur")[0]
    out = subprocess.run(["node", "-e", src + "\nconsole.log(JSON.stringify(calcular(" + json.dumps(d) + ")))"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["noExigible"]

fallos = 0
for d, e in CASOS:
    assert abs(esperado(d) - e) < 0.01, (d, esperado(d), e)
    if shutil.which("node"):
        got = js_no_exigible(d)
        ok = abs(got - e) <= 1
        fallos += not ok
        print("OK " if ok else "FALLO", d, "JS", got, "esperado", e)
    else:
        print("sin node: esperado", e, d)
sys.exit(1 if fallos else 0)
