"""Verificador fiscal (Opus, 2026-10-02): casos propios con el ORDEN de la AEAT (Manual Renta 2025, cap. 12,
'Fase 1.ª' = integración y compensación del ejercicio, incluido el 25 % entre cajones; 'Fase 2.ª' = saldos de
ejercicios anteriores con el 25 % restante, límite conjunto). Ejecuta el JS con osascript y compara."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/compensar-perdidas-ganancias-irpf-antes-fin-de-ano.js")
TAB = [(0, 0, 9.5), (6000, 570, 10.5), (50000, 5190, 11.5), (200000, 22440, 13.5), (300000, 35940, 15)]
def escala(x):
    if x <= 0: return 0.0
    for d, c, t in reversed(TAB):
        if x > d: return 2 * (c + (x - d) * t / 100)
def liq(gp, perd, rcm, otras, prev, anio, loss):
    a = rcm + otras; b = gp - perd - loss
    ant = prev if anio in ("2022", "2023", "2024", "2025") else 0.0
    nuevo = aneg = 0.0
    # Fase 1: ejercicio
    if b < 0: nuevo = -b; b = 0.0
    if a < 0: aneg = -a; a = 0.0
    topeA = 0.25 * a; topeB = 0.25 * b
    y = min(nuevo, topeA); nuevo -= y; a -= y; topeA -= y
    z = min(aneg, topeB); aneg -= z; b -= z
    # Fase 2: saldo antiguo de ganancias/pérdidas: primero b restante, luego 25 % conjunto de a
    t = min(ant, b); ant -= t; b -= t
    x = min(ant, topeA); ant -= x; a -= x
    cad = ant if anio == "2022" else 0.0
    return a + b, nuevo + aneg + (0.0 if anio == "2022" else ant), cad
CASOS = [  # (datos, campo, esperado)
    (dict(gp=0, perd=0, rcm=8000, otras=0, prev=2000, anio="2022", recompra="no", perdida=6000), "caducaCon", 2000),
    (dict(gp=0, perd=0, rcm=8000, otras=0, prev=2000, anio="2022", recompra="no", perdida=6000), "arrastreCon", 4000),
    (dict(gp=1000, perd=0, rcm=0, otras=-1000, prev=500, anio="2023", recompra="no", perdida=0), "baseSin", 250),
]
def js(d):
    src = open(JS, encoding="utf-8").read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(calcular(%s))" % json.dumps(d)], capture_output=True, text=True).stdout
    return json.loads(out)
fallos = 0
for d, k, esp in CASOS:
    s = liq(d["gp"], d["perd"], d["rcm"], d["otras"], d["prev"], d["anio"], 0)
    c = liq(d["gp"], d["perd"], d["rcm"], d["otras"], d["prev"], d["anio"], d["perdida"])
    ref = {"baseSin": s[0], "arrastreCon": c[1], "caducaCon": c[2]}[k]
    assert abs(ref - esp) < 0.01, (k, ref, esp)
    got = js(d)[k]; ok = abs(got - esp) < 0.01; fallos += not ok
    print(("OK " if ok else "FALLO ") + k, "JS", got, "esperado", esp)
sys.exit(1 if fallos else 0)
