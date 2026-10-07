#!/usr/bin/env python3
"""Oráculo independiente de calcs/hipoteca-fija-o-variable.js (Verificador, re-verificación 2026-10-07).
Simulación mes a mes (no fórmula cerrada para los intereses): cuota francesa, revisión anual única tras el mes 12.
Uso: python3 ops/verif/hipoteca-fija-o-variable.py  -> casos fijos + barrido 600 casos JS vs Python + sensibilidad a la senda."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/hipoteca-fija-o-variable.js")

def cuota(P, i, n): return P / n if i == 0 else P * i / (1 - (1 + i) ** -n)

def simular(P, n, tipos_anuales):
    """tipos_anuales[k] = TIN (%) del año k; revisión anual con recálculo de cuota sobre saldo y meses restantes."""
    saldo, inter = P, 0.0
    for m in range(n):
        if m % 12 == 0:
            i = max(tipos_anuales[min(m // 12, len(tipos_anuales) - 1)], 0) / 1200
            c = cuota(saldo, i, n - m)
        im = saldo * i; inter += im; saldo -= c - im
    return inter, saldo

def calcular(d):
    P, n = d["capital"], round(d["anos"] * 12)
    intF, _ = simular(P, n, [d["fijo"]])
    t1, t2 = d["euribor"] + d["dif"], d["euribor"] + d["escenario"] + d["dif"]
    intV, _ = simular(P, n, [t1, t2])
    lo, hi = -5.0, 30.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if simular(P, n, [t1, mid + d["dif"]])[0] > intF: hi = mid
        else: lo = mid
    return {"cuotaFija": cuota(P, d["fijo"] / 1200, n), "intFija": intF, "intVar": intV, "diferencia": intV - intF, "euriborEquilibrio": (lo + hi) / 2}

def js_run(cases):
    js = open(JS).read().split("function eur(")[0]
    h = js + f"\nJSON.stringify({json.dumps(cases)}.map(function(c){{return calcular(c);}}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    return json.loads(out.stdout.strip())

FIJOS = [
    ({"capital": 150000, "anos": 25, "fijo": 2.8, "dif": 0.8, "euribor": 3.247, "escenario": 0}, {"intFija": 58743.52, "intVar": 88695.94, "diferencia": 29952.41, "euriborEquilibrio": 1.9018}),
    ({"capital": 150000, "anos": 25, "fijo": 2.76, "dif": 0.8, "euribor": 3.247, "escenario": 0}, {"intFija": 57820.32, "intVar": 88695.94, "diferencia": 30875.62, "euriborEquilibrio": 1.8585}),
    ({"capital": 150000, "anos": 25, "fijo": 0, "dif": 0.8, "euribor": 3.247, "escenario": 0}, {"intFija": 0, "diferencia": 88695.94, "euriborEquilibrio": -5.0}),  # sin equilibrio: la página dice «no hay equilibrio»
    ({"capital": 200000, "anos": 30, "fijo": 3.0, "dif": 1.0, "euribor": 2.10, "escenario": 2}, {"intFija": 103554.90, "intVar": 185824.44, "diferencia": 82269.54}),
]

if __name__ == "__main__":
    fails = 0
    for d, exp in FIJOS:
        o = calcular(d)
        for k, v in exp.items():
            if abs(o[k] - v) > (0.001 if k == "euriborEquilibrio" else 0.05): print("FALLO fijo", d, k, o[k], v); fails += 1
    random.seed(7); cases = []
    for _ in range(600):
        cases.append({"capital": random.choice([50000, 120000, 150000, 300000, 600000]), "anos": random.randint(2, 40),
                      "fijo": round(random.uniform(0, 6), 2), "dif": round(random.uniform(0, 2.5), 2),
                      "euribor": round(random.uniform(-0.6, 5), 3), "escenario": random.choice([-1, 0, 1, 2])})
    for d, j in zip(cases, js_run(cases)):
        p = calcular(d)
        for k in ("intFija", "intVar", "diferencia"):
            if abs(p[k] - j[k]) > 0.01: print("DISC", d, k, p[k], j[k]); fails += 1
        if abs(p["euriborEquilibrio"] - j["euriborEquilibrio"]) > 1e-6: print("DISC eq", d, p["euriborEquilibrio"], j["euriborEquilibrio"]); fails += 1
    # Sensibilidad: misma media aritmética (años 2-25) que el umbral, senda creciente vs decreciente
    P, n, intF = 150000, 300, simular(150000, 300, [2.76])[0]
    sube = [3.247 + .8] + [1.0 + .8] * 12 + [2.95 + .8] * 12   # media años 2-25 = 1,975 % > 1,86 % (umbral con fija 2,76 %)
    baja = [3.247 + .8] + [2.95 + .8] * 12 + [1.0 + .8] * 12
    d1, d2 = simular(P, n, sube)[0] - intF, simular(P, n, baja)[0] - intF
    if abs(d1 + 7200) > 1 or abs(d2 - 12372) > 1: print("FALLO cifras de la frase T (gen_ejemplos.py)", d1, d2); fails += 1
    print(f"senda media 1,975 %: sube -> var-fija {simular(P, n, sube)[0] - intF:+.0f} €; baja -> {simular(P, n, baja)[0] - intF:+.0f} €")
    print(f"{'OK' if not fails else 'FALLOS'}: {len(FIJOS)} fijos + {len(cases)} aleatorios, discrepancias {fails}")
    sys.exit(1 if fails else 0)
