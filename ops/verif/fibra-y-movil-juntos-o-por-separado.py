#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/fibra-y-movil-juntos-o-por-separado.js, escrito desde la especificacion.
Uso: python3 ops/verif/fibra-y-movil-juntos-o-por-separado.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "fibra-y-movil-juntos-o-por-separado"
def oraculo(d):
    H = int(round(d["horizonte"])); P = int(round(d["permanencia"])); s = d["subida"] / 100.0
    def f(t): return (1 + s) ** ((t - 1) // 12)
    pack = lambda t: (d["packPromo"] if t <= d["promoMeses"] else d["packTras"]) * f(t)
    sep = lambda t: d["suelto"] * f(t)
    adv = lambda h: -d["unico"] + sum(sep(t) - pack(t) for t in range(1, h + 1))
    cp = d["unico"] + sum(pack(t) for t in range(1, H + 1)); cs = sum(sep(t) for t in range(1, H + 1))
    rec = agota = 0; prev = -d["unico"]; best = None; bestm = 0; a = -d["unico"]
    for t in range(1, 601):
        a += sep(t) - pack(t)
        if not rec and a >= 0: rec = t
        if not agota and prev >= 0 and a < 0: agota = t
        if t <= H and (best is None or a > best): best, bestm = a, t
        prev = a
    if d["promoMeses"] > 0 and d["packPromo"] > d["suelto"]: caro = 1
    elif d["packTras"] > d["suelto"]: caro = d["promoMeses"] + 1
    else: caro = 0
    exp = sum(max(0, pack(t) - sep(t)) for t in range(1, min(P, H) + 1) if pack(t) - sep(t) > 1e-9)
    atr = sum(1 for t in range(1, min(P, H) + 1) if pack(t) - sep(t) > 1e-9)
    mejor = 0 if cp < cs - 1 else (1 if cs < cp - 1 else 2)
    return {"costePack": cp, "costeSuelto": cs, "medioPack": cp / H, "medioSuelto": cs / H, "ventaja": cs - cp,
            "ventaja12": adv(12), "ventaja24": adv(24), "ventaja36": adv(36), "mesRecupera": rec, "mesAgota": agota, "mesCaro": caro,
            "ventajaMax": best, "mesVentajaMax": bestm, "exposicion": exp, "mesesAtrapado": atr,
            "permanenciaMayorQueHorizonte": 1 if P > H else 0, "mejor": mejor}
B = dict(packPromo=50, promoMeses=12, packTras=65, suelto=58, permanencia=12, unico=40, horizonte=36, subida=0)
TESTS = [dict(B),                                                   # base: promo, salto y pack caro tras la promo
         dict(B, packTras=55, subida=3, horizonte=24),              # pack siempre mas barato, con subida
         dict(B, promoMeses=0, packPromo=65, unico=0, horizonte=1), # sin promo, 1 mes, coste 0
         dict(B, packPromo=45, packTras=45, suelto=45, unico=0),    # empate
         dict(B, horizonte=12, permanencia=24, unico=0),            # horizonte corto y permanencia mayor
         dict(B, horizonte=60, subida=5, permanencia=0)]            # horizonte largo, pack pierde
def rnd(r):
    pp = r.choice([20, 35, 50, 60]) + r.random() * 3
    return dict(packPromo=pp, promoMeses=r.choice([0, 3, 6, 12, 24]), packTras=pp + r.choice([0, 5, 15, 30]) + r.random(),
                suelto=r.choice([25, 45, 60, 80]) + r.random() * 3, permanencia=r.choice([0, 12, 24]), unico=r.choice([0, 0, 40, 120]) + r.random(),
                horizonte=r.choice([1, 6, 12, 24, 36, 60, 120]), subida=r.choice([0, 2, 5, 10]) + r.random())
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(31); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("mejor", "mesRecupera", "mesAgota", "mesCaro", "mesVentajaMax", "mesesAtrapado", "permanenciaMayorQueHorizonte") else 1.0
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costePack", "costeSuelto", "medioPack", "ventaja", "ventaja12", "ventaja24", "ventaja36", "mesRecupera", "mesAgota", "mesCaro", "exposicion", "mesesAtrapado", "mejor"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
