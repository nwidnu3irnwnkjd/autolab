#!/usr/bin/env python3
"""Oraculo independiente: deposito, Letras del Tesoro o fondo monetario (neto tras IRPF del ahorro).
Escrito desde la norma ANTES del .js. Norma: Ley 35/2006 art. 25.2 (intereses y rendimiento de Letras = capital mobiliario),
art. 37/94 (fondos: ganancia solo al reembolso), arts. 49.1 y 66.1/76 (base del ahorro; escala TOTAL = estatal + autonomica,
cuotas acumuladas de la tabla del BOE duplicadas: 0, 1.140, 10.380, 44.880, 71.880), art. 101.4 y 101.6 (retencion 19 %),
RIRPF art. 75.3.b (sin retencion en Letras del Tesoro). Letras: tipo de interes simple base 360 (Tesoro): P = 100/(1 + i*d/360) con d = dias reales hasta el vencimiento (la de 9 m del 8/9/2026 dura 266 dias; por defecto, 365*m/12).
Uso: python3 ops/verif/deposito-letras-o-fondo-monetario.py  -> casos fijos + barrido aleatorio JS vs Python."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "deposito-letras-o-fondo-monetario"
# (limite inferior, cuota acumulada hasta ese limite, tipo del tramo) segun la tabla del art. 66.1 duplicada
TABLA = [(0, 0, 19), (6000, 1140, 21), (50000, 10380, 23), (200000, 44880, 27), (300000, 71880, 30)]

def cuota(b):
    if b <= 0: return 0.0
    for lo, acum, t in reversed(TABLA):
        if b > lo: return acum + (b - lo) * t / 100
    return 0.0

def impuesto(otras, g):
    return cuota(otras + g) - cuota(otras) if g > 0 else 0.0

def oraculo(imp, m, tin, letras, rent, com, otras, ambito="comun", dl=None):
    if ambito not in ("comun", "ceutamelilla"): return {"invalido": 1}
    if imp <= 0:
        z = dict(invalido=0, gDep=0, gLet=0, gFon=0, taxDep=0, taxLet=0, taxFon=0, netoDep=0, netoLet=0, netoFon=0, retDep=0, retLet=0, retFon=0,
                 taeDep=0, taeLet=0, taeFon=0)
        return z
    gdep = imp * tin / 100 * m / 12
    dias = 365.0 * m / 12 if not dl or dl <= 0 else min(max(dl, 1), 400)  # dias reales de la Letra (Tesoro: base 360)
    glet = imp * letras / 100 * dias / 360
    gfon = imp * ((1 + (rent - com) / 100) ** (m / 12) - 1)
    out = {"invalido": 0, "gDep": gdep, "gLet": glet, "gFon": gfon}
    for k, g in (("Dep", gdep), ("Let", glet), ("Fon", gfon)):
        t = impuesto(otras, g)
        out["tax" + k] = t
        out["neto" + k] = g - t
        out["ret" + k] = 0.0 if k == "Let" else (0.19 * g if g > 0 else 0.0)
        out["tae" + k] = 100 * (((imp + g - t) / imp) ** ((365.0 / dias) if k == "Let" else (12 / m)) - 1)
    mejor = max(gdep, glet)
    out["rentFondoEquilibrio"] = 100 * ((1 + mejor / imp) ** (12 / m) - 1) + com
    out["tinEquilibrioLetras"] = 100 * glet / (imp * m / 12)
    nets = sorted([("dep", out["netoDep"]), ("letras", out["netoLet"]), ("fondo", out["netoFon"])], key=lambda x: -x[1])
    out["_gap"] = nets[0][1] - nets[1][1]
    out["_ganador"] = "empate" if out["_gap"] < 1 else nets[0][0]
    return out

def js_eval(cases):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: sys.exit("error JS: " + out.stderr)
    return json.loads(out.stdout.strip())

def main():
    random.seed(20261002)
    fijos = [  # importe, plazo, tin, letras, rent, com, otras
        (20000, 9, 2.5, 2.776, 2.4, 0.2, 0), (0, 9, 2.5, 2.776, 2.4, 0.2, 0), (20000, 1, 2.5, 2.776, 2.4, 0.2, 0),
        (20000, 12, 3.0, 2.8, 2.0, 0.3, 6000), (20000, 12, 3.0, 2.8, 2.0, 0.3, 5999), (20000, 12, 3.0, 2.8, 2.0, 0.3, 6001),
        (50000, 12, 3.0, 2.8, 2.0, 0.3, 50000), (50000, 12, 3.0, 2.8, 2.0, 0.3, 49000), (300000, 12, 3.0, 2.8, 3.0, 0.3, 200000),
        (100000, 6, 3.0, 2.8, 3.0, 0.3, 199000), (20000, 9, 2.5, 2.776, -3.0, 0.2, 0), (20000, 9, 2.5, 2.776, 0.2, 0.2, 10000),
        (20000, 12, 0, 0, 0, 0, 0), (20000, 12, 2.5, 2.5, 2.5, 0, 299999), (1000, 3, 4.0, 3.0, 2.0, 0.1, 400000)]
    casos = [dict(importe=a, plazo=b, tin=c, letras=d, rentFondo=e, comFondo=f, otras=g, ambito="comun") for a, b, c, d, e, f, g in fijos]
    casos += [dict(importe=20000, plazo=9, tin=2.5, letras=2.776, rentFondo=2.4, comFondo=0.2, otras=0, ambito=a) for a in ("vasco", "navarra", "ceutamelilla")]
    for _ in range(600):
        casos.append(dict(importe=random.choice([0.0, 500.0, round(random.uniform(1, 5000), 2), round(random.uniform(1, 120000), 2), round(random.uniform(1, 800000), 2)]),
                          plazo=random.randint(1, 12), tin=round(random.uniform(0, 5), 3), letras=round(random.uniform(0, 5), 3),
                          rentFondo=round(random.uniform(-6, 7), 3), comFondo=round(random.uniform(0, 1.5), 3),
                          otras=random.choice([0, round(random.uniform(0, 8000), 2), round(random.uniform(0, 60000), 2), round(random.uniform(0, 400000), 2)]),
                          diasLetra=random.choice([0, 0, random.randint(1, 400), random.choice([91, 182, 266, 371])]), ambito="comun"))
    # casos de los cambios: Letra a 9 m con 266 dias reales (8/9/2026), a 12 m con 371 dias, sin dias (365*m/12), ceuta/melilla
    casos += [dict(importe=20000, plazo=9, tin=2.5, letras=2.776, rentFondo=2.4, comFondo=0.2, otras=0, diasLetra=266, ambito="comun"),
              dict(importe=20000, plazo=12, tin=2.8, letras=2.832, rentFondo=2.4, comFondo=0.2, otras=0, diasLetra=371, ambito="comun"),
              dict(importe=20000, plazo=9, tin=2.5, letras=2.776, rentFondo=2.4, comFondo=0.2, otras=0, diasLetra=0, ambito="comun"),
              dict(importe=20000, plazo=9, tin=2.5, letras=2.776, rentFondo=2.4, comFondo=0.2, otras=0, diasLetra=266, ambito="ceutamelilla")]
    res = js_eval(casos); mal = 0; nprop = 0
    for c, r in zip(casos, res):
        o = oraculo(c["importe"], c["plazo"], c["tin"], c["letras"], c["rentFondo"], c["comFondo"], c["otras"], c["ambito"], c.get("diasLetra"))
        for k, v in o.items():
            if k.startswith("_"): continue
            x = r.get(k)
            tol = 0.01 if k.startswith("tae") or k in ("rentFondoEquilibrio", "tinEquilibrioLetras") else 1
            if x is None or x != x or abs(x - v) > tol:
                mal += 1; print("DISCREPANCIA", c, k, x, v)
        if "_ganador" in o and o["_gap"] >= 2:
            if r.get("ganador") != o["_ganador"]: mal += 1; print("GANADOR", c, r.get("ganador"), o["_ganador"])
        if "_ganador" in o:
            # propiedad: el orden por neto coincide con el orden por rendimiento bruto (misma escala del ahorro)
            brutos = sorted([("dep", o["gDep"]), ("letras", o["gLet"]), ("fondo", o["gFon"])], key=lambda x: -x[1])
            nets = sorted([("dep", o["netoDep"]), ("letras", o["netoLet"]), ("fondo", o["netoFon"])], key=lambda x: -x[1])
            nprop += 1
            if abs(brutos[0][1] - brutos[1][1]) > 1e-6 and brutos[0][0] != nets[0][0]:
                mal += 1; print("PROPIEDAD orden bruto != orden neto", c)
    print(f"{len(casos)} casos (15 fijos + 3 ambitos + 600 aleatorios con dias de Letra variables + 4 de los cambios; {nprop} con propiedad orden-bruto=orden-neto): {mal} discrepancias")
    sys.exit(1 if mal else 0)
if __name__ == "__main__":
    main()
