#!/usr/bin/env python3
"""Oráculo independiente para calcs/subrogar-hipoteca-merece-la-pena.js (2026-10-02). Sin copiar el JS:
cuota francesa en forma cerrada, saldo en forma cerrada, ahorro neto = k*(cuotaAct - cuotaNueva - vinculación/12) + (saldoAct_k - saldoNuevo_k) - coste.
Barrido aleatorio de 500 casos contra el JS real (osascript/JavaScriptCore). Uso: python3 ops/verif/subrogar-hipoteca-merece-la-pena.py [--casos]"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def cuota(P, r, n):
    i = r / 1200
    return P / n if i == 0 else P * i / (1 - (1 + i) ** -n)
def saldo(P, r, n, k):
    i = r / 1200
    if i == 0: return max(P - P / n * k, 0)
    return max(P * (1 + i) ** k - cuota(P, r, n) * ((1 + i) ** k - 1) / i, 0)
def oraculo(d):
    n = max(round(d["anos"] * 12), 1); coste = d["capital"] * d["comision"] / 100 + d["gastos"]
    ca, cn = cuota(d["capital"], d["tipoActual"], n), cuota(d["capital"], d["tipoNuevo"], n)
    neto = lambda k: k * (ca - cn - d["vinculacion"] / 12) + saldo(d["capital"], d["tipoActual"], n, k) - saldo(d["capital"], d["tipoNuevo"], n, k) - coste
    kh = min(max(round(d["horizonte"] * 12), 1), n)
    eq = next((k for k in range(1, n + 1) if neto(k) >= 0), 0)
    return {"cuotaActual": ca, "cuotaNueva": cn, "ahorroCuota": ca - cn - d["vinculacion"] / 12, "ahorroIntereses": (ca - cn) * n,
            "costeCambio": coste, "mesesEquilibrio": eq, "ahorroNeto5": neto(min(60, n)), "ahorroNetoPlazo": neto(n), "ahorroNetoHorizonte": neto(kh)}

def js_run(casos):
    js = open(os.path.join(ROOT, "projects/decidir/calcs/subrogar-hipoteca-merece-la-pena.js")).read().split("function eur(")[0]
    h = js + f"\nJSON.stringify({json.dumps(casos)}.map(function(d){{return calcular(d);}}));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: sys.exit("error JS: " + o.stderr)
    return json.loads(o.stdout.strip())

if __name__ == "__main__":
    if "--casos" in sys.argv:  # valores para calcs/*.test.json
        d = dict(capital=150000, tipoActual=3.5, anos=20, tipoNuevo=2.76, comision=0.05, gastos=1500, vinculacion=300, horizonte=10)
        print(json.dumps({"in": d, "expect": {k: round(v, 2) for k, v in oraculo(d).items()}}, indent=1)); sys.exit()
    random.seed(7); casos = []
    for _ in range(500):
        casos.append(dict(capital=random.choice([20000, 90000, 150000, 400000]) * random.uniform(0.5, 1.5), tipoActual=random.choice([0, random.uniform(0.5, 7)]),
                          anos=random.randint(1, 35), tipoNuevo=random.choice([0, random.uniform(0.5, 7)]), comision=random.uniform(0, 2),
                          gastos=random.uniform(0, 4000), vinculacion=random.choice([0, random.uniform(0, 600)]), horizonte=random.randint(1, 40)))
    bad = 0
    for d, r in zip(casos, js_run(casos)):
        o = oraculo(d)
        for k, v in o.items():
            if abs(r[k] - v) > (0 if k == "mesesEquilibrio" else 1):
                bad += 1; print("DISCREPANCIA", k, r[k], v, d) if bad < 6 else None
    print(f"{'OK' if not bad else 'FALLOS'}: 500 casos, {bad} discrepancias > 1 €")
    sys.exit(1 if bad else 0)
