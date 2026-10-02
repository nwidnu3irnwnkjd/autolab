#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/curso-online-bootcamp-o-fp-coste-y-retorno.js, escrito desde la especificacion.
Uso: python3 ops/verif/curso-online-bootcamp-o-fp-coste-y-retorno.py [--write-tests]  (barrido de 400 casos aleatorios contra el JS real via osascript)"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "curso-online-bootcamp-o-fp-coste-y-retorno"
def oraculo(d):
    mat = d["matricula"] * (1 - d["beca"] / 100.0)
    tiempo = d["sueldo"] * d["renuncia"] / 100.0 * d["meses"]
    coste = mat + tiempo
    gana = max(12 * d["anios"] - d["meses"] - d["busqueda"], 0)
    valor = d["subida"] * gana - coste
    if abs(valor) <= 0.05 * coste: g = 2
    elif valor > 0: g = 0
    else: g = 1
    return {"costeMatricula": mat, "costeTiempo": tiempo, "costeTotal": coste,
            "mesesRecuperar": coste / d["subida"] if d["subida"] > 0 else -1,
            "mesesDesdeInicio": d["meses"] + d["busqueda"] + coste / d["subida"] if d["subida"] > 0 else -1,
            "mesesGana": gana, "valor": valor, "subidaMin": coste / gana if gana > 0 else -1, "ganador": g}
B = dict(matricula=6000, beca=0, meses=6, sueldo=1500, renuncia=50, busqueda=3, subida=500, anios=5)
TESTS = [dict(B),                                   # base: compensa
         dict(B, subida=120),                       # no compensa en el horizonte
         dict(B, matricula=0, beca=0, renuncia=0, subida=0),  # gratis y sin subida: empate 0
         dict(B, subida=206),                       # empate practico
         dict(B, subida=0),                         # sin subida: no se recupera
         dict(B, matricula=3000, beca=100, meses=1, renuncia=100, anios=1, busqueda=36, subida=900),  # borde: no da tiempo
         dict(B, meses=60, anios=30, busqueda=36, beca=100, renuncia=100, sueldo=3000, subida=1000)]  # maximos
def rnd(r):
    return dict(matricula=r.choice([0, 500, 3000, 6000, 12000]) + r.random() * 100, beca=r.choice([0, 25, 50, 100]),
                meses=r.choice([1, 3, 6, 12, 24, 60]), sueldo=r.choice([0, 900, 1500, 3000]) + r.random() * 50,
                renuncia=r.choice([0, 25, 50, 100]), busqueda=r.choice([0, 1, 3, 6, 36]),
                subida=r.choice([0, 100, 300, 500, 1000]) + r.random() * 20, anios=r.choice([1, 2, 5, 10, 30]))
def correr_js(ins):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
if __name__ == "__main__":
    r = random.Random(97); ins = TESTS + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, j in zip(ins, js):
        for k, v in oraculo(d).items():
            if j[k] is None or abs(j[k] - v) > max(0.01, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, j[k], v)
    print("casos:", len(ins), "discrepancias:", bad)
    if "--write-tests" in sys.argv:
        keys = ["costeMatricula", "costeTiempo", "costeTotal", "mesesRecuperar", "mesesGana", "valor", "subidaMin", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".test.json"), "w"), indent=1)
    sys.exit(1 if bad else 0)
