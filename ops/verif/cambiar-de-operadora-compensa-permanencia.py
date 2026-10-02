#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/cambiar-de-operadora-compensa-permanencia.js, escrito desde la especificacion.
Tres opciones en el horizonte H (meses): quedarse (H x cuota actual), cambiar ya (penalizacion + alta + cuotas nuevas con promo)
y esperar a que acabe la permanencia (cuota actual hasta entonces, luego alta + cuotas nuevas con promo). Sin permanencia, la penalizacion no se aplica.
Uso: python3 ops/verif/cambiar-de-operadora-compensa-permanencia.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "cambiar-de-operadora-compensa-permanencia"
def nuevo(d, n):
    return sum(d["promo"] if t <= d["promoM"] else d["nueva"] for t in range(1, n + 1))
def oraculo(d):
    H = d["horiz"]; W = d["perm"]; pen = d["penal"] if W > 0 else 0
    q = H * d["act"]
    c = pen + d["alta"] + nuevo(d, H)
    e = q if H <= W else W * d["act"] + d["alta"] + nuevo(d, H - W)
    # mes de equilibrio de cambiar ya: primer mes t (1..120) desde el que el ahorro acumulado es >= 0 y se mantiene
    eq = -1
    for t in range(120, 0, -1):
        if t * d["act"] - pen - d["alta"] - nuevo(d, t) >= -1e-9: eq = t
        else: break
    best = min(c, e)
    gan = 2 if q - best <= 1 else (0 if c <= e else 1)
    return {"costeQuedarse": q, "costeCambiar": c, "costeEsperar": e, "ahorroCambiar": q - c, "ahorroEsperar": q - e,
            "mesEq": eq, "penalMax": q - d["alta"] - nuevo(d, H), "penalMaxEsperar": e - d["alta"] - nuevo(d, H), "ganador": gan}
B = dict(act=70, nueva=45, promoM=6, promo=30, perm=8, penal=100, alta=50, horiz=24)
TESTS = [dict(B),                                  # base: cambiar ya
         dict(B, nueva=68, promoM=0, promo=68),    # sin ahorro: quedarse
         dict(B, penal=300, horiz=12),             # penalizacion alta, horizonte corto: esperar
         dict(B, horiz=6, perm=8),                 # horizonte menor que la permanencia
         dict(B, perm=0, penal=100),               # sin permanencia: la penalizacion no cuenta
         dict(B, promo=60, nueva=75, promoM=3)]    # promo barata y luego mas cara que la actual
def rnd(r):
    return dict(act=r.choice([20, 40, 70, 100]) + r.random() * 5, nueva=r.choice([15, 30, 45, 70, 110]) + r.random() * 5,
                promoM=r.choice([0, 3, 6, 12, 24]), promo=r.choice([0, 10, 30, 60]) + r.random() * 5, perm=r.choice([0, 3, 8, 12, 24]),
                penal=r.choice([0, 50, 100, 300, 600]) + r.random() * 5, alta=r.choice([0, 30, 50, 100]) + r.random() * 5,
                horiz=r.choice([1, 6, 12, 18, 24, 36, 60]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(47); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "mesEq") else 1.0
            if j[k] is None or abs(j[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = list(oraculo(B).keys())
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
