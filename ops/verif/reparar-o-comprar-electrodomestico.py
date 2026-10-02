#!/usr/bin/env python3
"""Oraculo independiente (Constructor) de calcs/reparar-o-comprar-electrodomestico.js. Escrito desde la especificacion, no desde el JS.
Uso: python3 ops/verif/reparar-o-comprar-electrodomestico.py [--write-tests]  (barrido aleatorio de 400 casos contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "reparar-o-comprar-electrodomestico"
def oraculo(d):
    anos_restantes = d["vida"] - d["edad"]
    h = anos_restantes if anos_restantes > 1 else 1.0
    cobertura = min(d["garantia"], 24.0) / 24.0
    p = d["prob"] / 100.0
    esperado = d["reparacion"] * p * (1.0 - cobertura)
    energia = d["dkwh"] * d["precio"]
    rep = (d["reparacion"] + esperado) / h + energia
    nuevo = d["nuevo"] / d["vida"]
    eq = (nuevo - energia) * h / (1.0 + p * (1.0 - cobertura))
    eq = eq if eq > 0 else 0.0
    return {"horizonteRep": h, "costeEsperadoAveria": esperado, "energiaExtraAnual": energia, "anualReparar": rep, "anualNuevo": nuevo,
            "diferenciaAnual": rep - nuevo, "equilibrioReparacion": eq, "equilibrioPctNuevo": eq / d["nuevo"] * 100,
            "regla50": 1 if d["reparacion"] * 2 <= d["nuevo"] else 0,
            "ganador": "empate" if abs(rep - nuevo) < 1 else ("reparar" if rep < nuevo else "comprar")}
B = dict(vida=11.5, edad=8, reparacion=150, nuevo=430, garantia=6, prob=25, dkwh=0, precio=0.23)
TESTS = [dict(B), dict(B, edad=2, reparacion=250, nuevo=600, vida=12, garantia=12, prob=10),
         dict(B, reparacion=0), dict(B, reparacion=500, nuevo=430, dkwh=150),          # reparacion mas cara que lo nuevo
         dict(B, edad=14, vida=11.5, prob=40, garantia=0),                              # pasa la vida util
         dict(B, dkwh=400, precio=0.25, reparacion=60, edad=10)]
def rnd(r):
    vida = r.choice([8, 10, 11.5, 12, 15, 18]); return dict(vida=vida, edad=r.choice([0, 1, 3, 6, 8, 10, 12, 16, 20]), reparacion=r.choice([0, 40, 90, 150, 220, 300, 600]) + r.random() * 20,
        nuevo=r.choice([250, 430, 600, 900, 1300]) + r.random() * 50, garantia=r.choice([0, 3, 6, 12, 24, 36]), prob=r.choice([0, 10, 25, 40, 80, 100]),
        dkwh=r.choice([0, 30, 100, 250, 500]), precio=r.choice([0.1, 0.18, 0.23, 0.3]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(7); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        o = oraculo(d)
        for k, v in o.items():
            if (isinstance(v, str) and j[k] != v) or (not isinstance(v, str) and abs(j[k] - v) > 1e-6 * max(1, abs(v)) and abs(j[k] - v) > 0.01):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["anualReparar", "anualNuevo", "diferenciaAnual", "equilibrioReparacion", "regla50"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
