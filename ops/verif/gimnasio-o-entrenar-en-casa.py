#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/gimnasio-o-entrenar-en-casa.js, escrito desde la especificacion.
Uso: python3 ops/verif/gimnasio-o-entrenar-en-casa.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "gimnasio-o-entrenar-en-casa"
def oraculo(d):
    W = d["meses"] * 52.0 / 12
    sg, sc = d["sg"] * W, d["sc"] * W
    fijo = d["matricula"] + d["cuota"] * d["meses"]
    cg = fijo + d["desp"] * sg
    cc = d["equipo"] - d["reventa"]
    pg = cg / sg if sg > 0 else -1
    pc = cc / sc if sc > 0 else -1
    if sg == 0 and sc == 0: gan = 3
    elif sg == 0: gan = 1
    elif sc == 0: gan = 0
    elif abs(pg - pc) <= 0.005: gan = 2
    else: gan = 0 if pg < pc else 1
    eqg = fijo / (W * (pc - d["desp"])) if pc > d["desp"] else -1
    eqc = cc / (W * pg) if pg > 0 else -1
    return {"semanas": W, "costeGim": cg, "costeCasa": cc, "sesGim": sg, "sesCasa": sc, "cpsGim": pg, "cpsCasa": pc,
            "eqGim": eqg, "eqCasa": eqc, "diferencia": cg - cc, "ganador": gan}
B = dict(cuota=30, matricula=20, desp=1, sg=3, sc=3, equipo=800, reventa=200, meses=24)
TESTS = [dict(B),                                   # base: casa gana
         dict(B, equipo=3000, reventa=500, sc=1),   # equipo caro y poco uso: gana gimnasio
         dict(B, sg=0),                             # 0 sesiones en el gimnasio
         dict(B, cuota=0, matricula=0, desp=0, equipo=0, reventa=0),  # todo a coste 0: empate
         dict(B, meses=1, sg=1, sc=1),              # 1 mes
         dict(B, sg=0, sc=0)]                       # 0 sesiones en ambos
def rnd(r):
    eq = r.choice([0, 100, 400, 800, 2000, 5000]) + r.random() * 30
    return dict(cuota=r.choice([0, 15, 30, 45, 80]) + r.random() * 5, matricula=r.choice([0, 20, 60, 150]) + r.random() * 5,
                desp=r.choice([0, 0.5, 1, 3]) + r.random(), sg=r.choice([0, 0.5, 1, 2, 3, 5, 7]) + r.random(),
                sc=r.choice([0, 0.5, 1, 2, 3, 5, 7]) + r.random(), equipo=eq, reventa=eq * r.choice([0, 0.2, 0.5, 1]),
                meses=r.choice([1, 6, 12, 18, 24, 36, 60]) + r.random() * 2)
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(71); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeGim", "costeCasa", "sesGim", "sesCasa", "cpsGim", "cpsCasa", "eqGim", "eqCasa", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
