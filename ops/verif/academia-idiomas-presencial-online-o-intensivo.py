#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/academia-idiomas-presencial-online-o-intensivo.js, escrito desde la especificacion.
Uso: python3 ops/verif/academia-idiomas-presencial-online-o-intensivo.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "academia-idiomas-presencial-online-o-intensivo"
def oraculo(d):
    ph = d["acad"] * (1 - d["desc"] / 100.0) + d["desp"]       # precio por hora presencial
    h_onl = d["horas"] / (d["ef"] / 100.0)                     # horas lectivas online para igualar el aprendizaje
    sem = d["horas"] / 20.0                                    # 20 h lectivas por semana de inmersion
    c = [d["horas"] * ph, h_onl * d["onl"], sem * d["inm"]]
    best = min(range(3), key=lambda i: (c[i], i))
    resto = sorted(c[i] for i in range(3) if i != best)
    return {"acadHora": ph, "costeAcad": c[0], "costeOnl": c[1], "costeInm": c[2], "horasOnl": h_onl, "semanasInm": sem,
            "mesesAcad": d["horas"] / d["hs"] / (52 / 12.0), "mesesOnl": h_onl / d["hs"] / (52 / 12.0), "mesesInm": sem * 12 / 52.0,
            "horaAprOnl": d["onl"] / (d["ef"] / 100.0), "horaInm": d["inm"] / 20.0,
            "efEquilibrio": d["onl"] / ph * 100 if ph > 0 else -1,
            "inmEquilibrio": min(c[0], c[1]) / sem if sem > 0 else -1,
            "mejor": best, "ahorro": resto[0] - c[best], "minimo": c[best]}
B = dict(horas=200, hs=4, acad=15, desp=2, desc=10, onl=8, inm=900, ef=80)
TESTS = [dict(B),                                 # base: online mas barato
         dict(B, onl=20),                         # online caro: gana academia
         dict(B, inm=200),                        # inmersion barata: gana inmersion
         dict(B, acad=0, desp=0),                 # academia gratis: coste 0 y sin equilibrio
         dict(B, horas=1, hs=1, ef=100, desc=100),# 1 hora, descuento 100 %
         dict(B, ef=300, hs=60, horas=3000)]      # maximos
def rnd(r):
    return dict(horas=r.choice([1, 50, 120, 200, 500, 1000, 3000]) + r.random() * 10, hs=r.choice([0.5, 2, 4, 8, 20, 60]) + r.random(),
                acad=r.choice([0, 6, 12, 15, 25]) + r.random() * 3, desp=r.choice([0, 1, 3, 8]) + r.random(),
                desc=r.choice([0, 5, 10, 25, 100]), onl=r.choice([0, 3, 8, 15, 30]) + r.random() * 2,
                inm=r.choice([0, 300, 900, 1500, 3000]) + r.random() * 20, ef=r.choice([20, 50, 80, 100, 150, 300]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(53); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeAcad", "costeOnl", "costeInm", "mesesAcad", "mesesOnl", "mesesInm", "efEquilibrio", "inmEquilibrio", "mejor", "ahorro"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
