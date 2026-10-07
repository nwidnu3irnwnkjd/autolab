#!/usr/bin/env python3
"""Oraculo independiente (Verificador, re-verificacion tarea 8, 2026-10-07) para alquilar-o-comprar.
Modelo escrito desde la descripcion economica (no copiado del JS):
- Hipoteca francesa: saldo por formula cerrada B_k = L(1+i)^k - c((1+i)^k - 1)/i.
- Comprar: valor P(1+g)^t * (1 - venta) - saldo + cartera del comprador (cuando alquilar cuesta mas al mes).
- Alquilar: entrada + gastos de compra invertidos al rendimiento mensual equivalente (1+r)^(1/12)-1,
  mas cada mes la diferencia si comprar cuesta mas. Coste comprar = cuota + (IBI+comunidad)/12 + mant% del valor al inicio del ano.
  Alquiler y valor suben por escalones anuales (constantes dentro de cada ano).
- Ano de cruce = primer ano completo en que comprar > alquilar.
Sensibilidades (no estan en el JS; sirven para el informe): impuestos del ahorro sobre la ganancia de las carteras,
IBI/comunidad indexados, deduccion estatal del 10 % del alquiler (RDL 29/2026, pendiente de convalidacion).
Uso: python3 ops/verif/alquilar-o-comprar.py -> casos fijos + 600 aleatorios JS vs Python (osascript); sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/alquilar-o-comprar.js")
TEST = os.path.join(ROOT, "projects/decidir/calcs/alquilar-o-comprar.test.json")
AHORRO = [(0, .19), (6000, .21), (50000, .23), (200000, .27), (300000, .30)]  # LIRPF art. 66.1/76 (Ley 7/2024), 2025+

def tax_ahorro(g):
    if g <= 0: return 0.0
    t = 0.0
    for k, (lo, r) in enumerate(AHORRO):
        hi = AHORRO[k + 1][0] if k + 1 < len(AHORRO) else float("inf")
        if g > lo: t += (min(g, hi) - lo) * r
    return t

def oraculo(d, impuestos=False, indexa_fijos=0.0, deduccion_alquiler=False):
    P = d["precio"]; E = P * d["entrada"] / 100; L = P - E; n = round(d["plazo"] * 12); i = d["interes"] / 1200
    c = L / n if i == 0 else L * i / (1 - (1 + i) ** -n)
    def saldo(k):
        k = min(k, n)
        return L - c * k if i == 0 else L * (1 + i) ** k - c * ((1 + i) ** k - 1) / i
    j = (1 + d["rentab"] / 100) ** (1 / 12) - 1
    H = round(d["horizonte"] * 12)
    alq, com = E + P * d["gastos"] / 100, 0.0
    apA, apC = alq, 0.0  # aportaciones (para la ganancia patrimonial)
    anos = []
    for m in range(H):
        a = m // 12
        fijos = (d["ibi"] + d["comunidad"]) * (1 + indexa_fijos / 100) ** a / 12
        mant = P * (1 + d["revaloriza"] / 100) ** a * d["mant"] / 1200
        cc = (c if m < n else 0) + fijos + mant
        ra = d["alquiler"] * (1 + d["subida"] / 100) ** a
        if deduccion_alquiler:  # 10 % del alquiler anual, base max 11.630 -> max 1.163 EUR/ano, se cobra prorrateado
            ra -= min(ra * 12, 11630) * .10 / 12
        alq *= 1 + j; com *= 1 + j
        if cc > ra: alq += cc - ra; apA += cc - ra
        else: com += ra - cc; apC += ra - cc
        if (m + 1) % 12 == 0:
            t = (m + 1) / 12
            vc = P * (1 + d["revaloriza"] / 100) ** t * (1 - d["venta"] / 100) - max(saldo(m + 1), 0) + com
            va = alq
            if impuestos:
                vc -= tax_ahorro(com - apC); va -= tax_ahorro(alq - apA)
            anos.append((vc, va))
    eq = next((k + 1 for k, (x, y) in enumerate(anos) if x > y), 0)
    cruces = sum(1 for k in range(1, len(anos)) if (anos[k][0] > anos[k][1]) != (anos[k - 1][0] > anos[k - 1][1]))
    vc, va = anos[-1]
    return dict(patrimonioComprar=vc, patrimonioAlquilar=va, diferencia=vc - va, anosEquilibrio=eq, ultimoAnoComprar=max([k + 1 for k, (x, y) in enumerate(anos) if x > y] or [0]), cuotaHipoteca=c,
                costeMensualCompra=c + (d["ibi"] + d["comunidad"]) / 12 + P * d["mant"] / 1200, costeMensualAlquiler=d["alquiler"],
                cruces=cruces, anos=anos)

def js(cases):
    src = open(JS).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(function (d) { var r = calcular(d); delete r.serieAnual; return r; }));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)

BASE = dict(precio=250000, entrada=20, interes=3.0, plazo=30, gastos=10, ibi=400, comunidad=700, mant=1, revaloriza=2,
            alquiler=900, subida=2, rentab=4, venta=3, horizonte=15)
def V(**k): d = dict(BASE); d.update(k); return d
KEYS = ["patrimonioComprar", "patrimonioAlquilar", "diferencia", "anosEquilibrio", "ultimoAnoComprar", "cuotaHipoteca", "costeMensualCompra", "costeMensualAlquiler"]
CASES = [("defecto (ejemplo resuelto: +32.772, ano 9)", BASE), ("tipo 0", V(interes=0)), ("entrada 0", V(entrada=0)),
         ("horizonte > plazo", V(plazo=10, horizonte=25)), ("revaloriza negativa", V(revaloriza=-3)), ("alquiler caro", V(alquiler=2000)),
         ("horizonte 1", V(horizonte=1)), ("plazo 15,5", V(plazo=15.5)), ("subida 0", V(subida=0))]

if __name__ == "__main__":
    tests = json.load(open(TEST))["cases"]
    rnd = random.Random(8)
    sweep = [dict(precio=rnd.uniform(60000, 900000), entrada=rnd.uniform(0, 60), interes=rnd.uniform(0, 7), plazo=rnd.randint(5, 40),
                  gastos=rnd.uniform(0, 14), ibi=rnd.uniform(0, 2000), comunidad=rnd.uniform(0, 3000), mant=rnd.uniform(0, 2.5),
                  revaloriza=rnd.uniform(-3, 7), alquiler=rnd.uniform(300, 3500), subida=rnd.uniform(-1, 6), rentab=rnd.uniform(-2, 9),
                  venta=rnd.uniform(0, 8), horizonte=rnd.randint(1, 40)) for _ in range(600)]
    allc = [c for _, c in CASES] + [t["in"] for t in tests] + sweep
    jr = js(allc); bad = 0
    for k, (d, r) in enumerate(zip(allc, jr)):
        o = oraculo(d)
        for key in KEYS:
            if abs(o[key] - r[key]) > 0.01 * max(1, abs(o[key]) * 1e-9 + 1):
                bad += 1; print("DIF", k, key, o[key], r[key]); break
    for t in tests:
        o = oraculo(t["in"])
        for key, v in t["expect"].items():
            if abs(o[key] - v) > t.get("tol", 0.01): bad += 1; print("TEST", key, o[key], v)
    b = oraculo(BASE)
    print("casos: %d fijos+test, %d aleatorios, discrepancias JS-oraculo: %d" % (len(CASES) + len(tests), len(sweep), bad))
    print("defecto: comprar %.2f alquilar %.2f dif %.2f ano %d cuota %.2f coste %.2f" % (b["patrimonioComprar"], b["patrimonioAlquilar"], b["diferencia"], b["anosEquilibrio"], b["cuotaHipoteca"], b["costeMensualCompra"]))
    print("  serie dif por ano:", [round(x - y) for x, y in b["anos"]])
    multi = [d for d in sweep if oraculo(d)["cruces"] > 1]
    print("aleatorios con >1 cruce (comprar gana y luego pierde, o al reves): %d de %d" % (len(multi), len(sweep)))
    tard = [d for d in sweep if oraculo(d)["anosEquilibrio"] and not (oraculo(d)["diferencia"] > 0)]
    print("  de ellos, 'gana desde el ano N' pero pierde al final del horizonte: %d" % len(tard))
    for lab, kw in (("impuestos del ahorro sobre las carteras", dict(impuestos=True)), ("IBI y comunidad +2 %/ano", dict(indexa_fijos=2)),
                    ("deduccion 10 % alquiler (RDL 29, si convalida)", dict(deduccion_alquiler=True)),
                    ("las tres", dict(impuestos=True, indexa_fijos=2, deduccion_alquiler=True))):
        s = oraculo(BASE, **kw); print("sens. %s: dif %.0f ano %d" % (lab, s["diferencia"], s["anosEquilibrio"]))
    for lab, d in (("subida 3 %", V(subida=3)), ("subida 1 %", V(subida=1)), ("gastos 8 %", V(gastos=8)), ("venta 6 %", V(venta=6)),
                   ("revaloriza 1 %", V(revaloriza=1)), ("rentab 6 %", V(rentab=6)), ("horizonte 8", V(horizonte=8)), ("horizonte 9", V(horizonte=9))):
        s = oraculo(d); print("sens. %s: dif %.0f ano %d" % (lab, s["diferencia"], s["anosEquilibrio"]))
    sys.exit(1 if bad else 0)
