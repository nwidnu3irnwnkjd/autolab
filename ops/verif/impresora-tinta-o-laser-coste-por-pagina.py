#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/impresora-tinta-o-laser-coste-por-pagina.js, escrito desde la especificacion.
Uso: python3 ops/verif/impresora-tinta-o-laser-coste-por-pagina.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "impresora-tinta-o-laser-coste-por-pagina"
def oraculo(d):
    pag = d["pagMes"] * 12 * d["anios"]
    tot = [d["pT"] + pag * d["cT"], d["pD"] + pag * d["cD"], d["pL"] + pag * d["cL"]]
    mn = min(tot); gan = next(i for i in range(3) if tot[i] <= mn + 1e-9)
    def eq(pa, ca, pb, cb):
        if (pa - pb) * (ca - cb) < 0:
            return abs(pa - pb) / (12 * d["anios"] * abs(ca - cb))
        return -1
    return {"paginas": pag, "totTinta": tot[0], "totDeposito": tot[1], "totLaser": tot[2],
            "pagTinta": tot[0] / pag if pag else -1, "pagDeposito": tot[1] / pag if pag else -1, "pagLaser": tot[2] / pag if pag else -1,
            "eqTintaLaser": eq(d["pT"], d["cT"], d["pL"], d["cL"]), "eqTintaDeposito": eq(d["pT"], d["cT"], d["pD"], d["cD"]),
            "eqDepositoLaser": eq(d["pD"], d["cD"], d["pL"], d["cL"]), "ganador": gan}
B = dict(pagMes=40, anios=3, pT=60, cT=0.07, pD=200, cD=0.01, pL=150, cL=0.03)
TESTS = [dict(B),                       # base: gana tinta con cartuchos
         dict(B, pagMes=150),           # volumen alto: gana deposito
         dict(B, pagMes=100, pD=400),   # gana laser
         dict(B, pagMes=0),             # 0 paginas
         dict(B, pT=150, cT=0.03, pL=150, cL=0.03),  # empate tinta/laser
         dict(B, pD=60, cD=0.07, pL=300, cL=0.2),    # deposito igual que tinta, sin equilibrio
         dict(B, pagMes=65)]             # entre 62 y 69: gana laser
def rnd(r):
    return dict(pagMes=r.choice([0, 10, 40, 100, 400]) + r.random() * 5, anios=r.choice([1, 2, 3, 5, 10]),
                pT=r.choice([0, 40, 60, 100]) + r.random() * 10, cT=r.choice([0.01, 0.03, 0.07, 0.15]) + r.random() * 0.01,
                pD=r.choice([100, 200, 300]) + r.random() * 10, cD=r.choice([0.005, 0.01, 0.03]) + r.random() * 0.005,
                pL=r.choice([80, 150, 300]) + r.random() * 10, cL=r.choice([0.01, 0.03, 0.06]) + r.random() * 0.005)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k == "ganador" else (0.0001 if k.startswith("pag") and k != "paginas" else (0.01 if k.startswith("eq") else 1.0))
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 4) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
