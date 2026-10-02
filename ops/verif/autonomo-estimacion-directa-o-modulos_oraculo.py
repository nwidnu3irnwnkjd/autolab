#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para autonomo-estimacion-directa-o-modulos. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado consultado el 2/10/2026; LIRPF arts. 30, 31, 32; RIRPF arts. 28-30, 32-34, 109-110; Orden HAC/1425/2025; LGSS art. 308.1.c; Orden PJC/297/2026):
1. Directa simplificada (art. 28 RIRPF, cifra de negocios < 600.000 EUR el ano anterior; bloqueada si la actividad no esta en la Orden o se renuncio hace < 3 anos, art. 34.3 y 33.3 RIRPF):
   rendimiento neto = ingresos - gastos - cuota RETA del titular (deducible) - 5 % de difícil justificacion (max 2.000 EUR; RIRPF 30.2.2.a y LIRPF 30.2.4.a).
   RETA (LGSS 308.1.c): rendimiento computable = neto + cuotas; menos 7 % de gastos genericos; tramo de la tabla 2026 (base minima) x 31,5 %; la cuota depende del neto y el neto de la cuota (punto fijo).
2. Modulos (EO, LIRPF art. 31, RIRPF 37, Orden HAC/1425/2025): el usuario declara el rendimiento neto PREVIO (fase 1) y el rendimiento neto de MODULOS (fase 3, tras amortizaciones e indices). El IRPF grava el neto de modulos
   reducido un 5 % (DA 1.a Orden 2026); NO se resta la cuota RETA ni los gastos reales (el procedimiento de la Orden solo admite amortizacion e incentivos). RETA en EO = rendimiento neto PREVIO (LGSS 308.1.c, 4.o parrafo), menos 7 %.
3. Reduccion 32.2.3.o LIRPF (ambos metodos): rentas totales (actividad + otras) < 12.000 EUR: 1.620 (<= 8.000) o 1.620 - 0,405 x (rentas - 8.000); nunca mas que el rendimiento; el tope conjunto con el art. 20 (3.700 EUR) no se modela.
4. IRPF atribuible = cuota(otras + rendimiento reducido) - cuota(otras): escala estatal + autonomica menos la cuota del minimo personal (sin hijos), por diferencia (no hay otras deducciones). Una perdida se integra con las otras rentas (base >= 0).
5. Neto en caja = ingresos - gastos reales - RETA - IRPF atribuible, en ambos metodos (en modulos los gastos reales se pagan igual aunque no se deduzcan).
6. Pagos fraccionados anuales: directa (modelo 130) 20 % del neto (art. 110.1.a RIRPF); modulos (modelo 131) 2 % por trimestre del neto de modulos reducido (sin asalariados, Orden anexo II, pagos fraccionados 4) = 8 % al ano.
   Retenciones no se restan. Exentos del 130 solo actividades profesionales con >= 70 % de ingresos con retencion el ano anterior (art. 109.2).
7. Bloqueos: ingresos > 250.000 EUR (excluye modulos con cualquier lectura de art. 31.1.3.a.b.a' / DT 32.a); situacion directa por renuncia/exclusion < 3 anos (LIRPF 31.1.5.a); actividad fuera de la Orden.
8. Umbral de gastos: gasto minimo para que la carga de la directa (RETA + IRPF) no supere la de modulos; la carga es no creciente en los gastos, biseccion sobre [0, ingresos].
Uso: python3 ops/verif/autonomo-estimacion-directa-o-modulos_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias > 1 EUR."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRM = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))
IR = PRM["irpf_2026"]
EST = [(lo, r / 100) for lo, r in IR["escala_estatal_general"]["tramos"]]
DESC_E = IR["minimo_estatal"]["contribuyente"]
def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def cuota_base(bg, cc):
    d = IR["ccaa"][cc]; ea = [(lo, r / 100) for lo, r in d["escala_general"]]
    mn = d["minimo"]["contribuyente"] if d["minimo"] else DESC_E
    return max(0, esc(bg, EST) - esc(DESC_E, EST)) + max(0, esc(bg, ea) - esc(mn, ea))
TABLA = [(670, 653.59), (900, 718.95), (1166.70 - 1e-9, 849.67), (1300, 950.98), (1500, 960.78), (1700, 960.78), (1850, 1143.79), (2030, 1209.15),
         (2330, 1274.51), (2760, 1356.21), (3190, 1437.91), (3620, 1519.61), (4050, 1601.31), (6000, 1732.03), (float("inf"), 1928.10)]
def base_min(R):
    for lim, b in TABLA:
        if R <= lim: return b
def reta(C):  # C = rendimiento computable anual antes del 7 %
    return 12 * base_min(0.93 * C / 12 if C > 0 else 0.0) * .315
def dj(N): return min(2000.0, .05 * max(N, 0))
def ss_directa(I, G):
    for s in sorted({12 * b * .315 for _, b in TABLA}):
        N = I - G - s
        if abs(reta(I - G - dj(N)) - s) < 1e-9: return s
    return 12 * 1928.10 * .315
def reduccion(rn, otras):
    if rn <= 0: return 0.0
    t = rn + otras
    if t >= 12000: return 0.0
    return min(1620.0 if t <= 8000 else 1620 - .405 * (t - 8000), rn)
def irpf_attr(rn, otras, cc):
    red = reduccion(rn, otras)
    return cuota_base(max(otras + rn - red, 0), cc) - cuota_base(max(otras, 0), cc)
def directa(I, G, otras, cc):
    s = ss_directa(I, G); N = I - G - s; rn = N - dj(N)
    ir = irpf_attr(rn, otras, cc)
    return dict(ss=s, rn=rn, irpf=ir, neto=I - G - s - ir)
def modulos(I, G, previo, mod, otras, cc):
    s = reta(previo); rn = .95 * mod
    ir = irpf_attr(rn, otras, cc)
    return dict(ss=s, rn=rn, irpf=ir, neto=I - G - s - ir)
def model(d):
    I, G, cc, o = d["ingresos"], d["gastos"], d["ccaa"], d["otras"]
    a = directa(I, G, o, cc); m = modulos(I, G, d["previo"], d["modulos"], o, cc)
    carga_m = m["ss"] + m["irpf"]
    def ok(g): x = directa(I, g, o, cc); return x["ss"] + x["irpf"] <= carga_m + 1e-9
    if ok(0): ge = 0.0
    elif not ok(max(I, 0)): ge = None
    else:
        lo, hi = 0.0, float(max(I, 0))
        for _ in range(80):
            mid = (lo + hi) / 2
            if ok(mid): hi = mid
            else: lo = mid
        ge = hi
    bloq = 0
    if d["situacion"] == "directa_bloqueo": bloq = 1
    elif d["situacion"] == "sin_modulos": bloq = 2
    elif I > 250000: bloq = 3
    dif = m["neto"] - a["neto"]
    return dict(ssDirecta=a["ss"], rnDirecta=a["rn"], irpfDirecta=a["irpf"], netoDirecta=a["neto"], ssModulos=m["ss"], rnModulos=m["rn"], irpfModulos=m["irpf"],
                netoModulos=m["neto"], diferencia=dif, pagoDirectaAnual=.20 * max(a["rn"], 0), pagoModulosAnual=.08 * max(m["rn"], 0),
                gastosEquilibrio=ge, exento130=1 if d["retencion"] >= 70 else 0, bloqueo=bloq)
B = dict(ingresos=60000, gastos=40000, previo=22000, modulos=19000, otras=0, ccaa="madrid", retencion=0, situacion="modulos")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto Madrid", V()), ("2 ingresos bajos, reduccion 32.2.3", V(ingresos=14000, gastos=6000, previo=7000, modulos=6000, ccaa="andalucia")),
 ("3 gastos altos: directa gana", V(ingresos=90000, gastos=75000, previo=20000, modulos=17000, ccaa="valencia")),
 ("4 gastos casi cero: modulos gana", V(ingresos=60000, gastos=5000, previo=30000, modulos=24000, ccaa="cataluna")),
 ("5 otras rentas 30.000 Galicia", V(ingresos=70000, gastos=45000, previo=21000, modulos=18000, otras=30000, ccaa="galicia")),
 ("6 ingresos 0 y gastos 0, previo 0", V(ingresos=0, gastos=0, previo=0, modulos=0)),
 ("7 perdida en directa (gastos > ingresos)", V(ingresos=20000, gastos=26000, previo=6000, modulos=5000, otras=15000, ccaa="murcia")),
 ("8 ingresos 250.000 exactos (limite) Baleares", V(ingresos=250000, gastos=180000, previo=60000, modulos=55000, ccaa="baleares")),
 ("9 ingresos 250.001 (bloqueo 3)", V(ingresos=250001, gastos=180000, previo=60000, modulos=55000)),
 ("10 situacion directa por renuncia reciente (bloqueo 1)", V(situacion="directa_bloqueo")),
 ("11 retencion 70 % exacto (exento 130)", V(retencion=70, ccaa="canarias")),
 ("12 retencion 69,99 %", V(retencion=69.99)),
 ("13 rentas totales 12.000 exactos (modulos)", V(ingresos=20000, gastos=12000, previo=5000, modulos=4000, otras=8200, ccaa="clm")),
 ("13b rentas totales 8.000 exactos (modulos)", V(ingresos=20000, gastos=12000, previo=5000, modulos=4000, otras=4200, ccaa="clm")),
 ("13c gastos 30.000 (modulos gana)", V(gastos=30000)), ("13d gastos 20.000", V(gastos=20000)),
 ("14 sin_modulos (bloqueo 2)", V(situacion="sin_modulos")),
 ("15 neto previo en borde de tramo RETA 1.166,70/mes", V(ingresos=40000, gastos=26000, previo=14000 / .93 + 0.01, modulos=13000))]
KEYS = ["ssDirecta", "rnDirecta", "irpfDirecta", "netoDirecta", "ssModulos", "rnModulos", "irpfModulos", "netoModulos", "diferencia", "pagoDirectaAnual", "pagoModulosAnual", "gastosEquilibrio", "exento130", "bloqueo"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/autonomo-estimacion-directa-o-modulos.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(26); ca = list(IR["ccaa"])
    sweep = []
    for _ in range(520):
        I = rnd.choice([0, 8000, 15000, 30000, 60000, 120000, 200000, 260000]) * rnd.uniform(.7, 1.3)
        G = I * rnd.choice([0, .1, .3, .6, .8, .95, 1.1])
        pr = I * rnd.uniform(0, .6)
        sweep.append(dict(ingresos=I, gastos=G, previo=pr, modulos=pr * rnd.uniform(.6, 1.3), otras=rnd.choice([0, 0, 4000, 10000, 25000, 60000, 150000]) * rnd.uniform(.8, 1.2),
                          ccaa=rnd.choice(ca), retencion=rnd.choice([0, 30, 70, 100]), situacion=rnd.choice(["modulos"] * 4 + ["inicio", "directa_libre", "directa_bloqueo", "sin_modulos"])))
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j[k], o[k]) for k in KEYS if (o[k] is None) != (j[k] is None) or (o[k] is not None and abs(j[k] - o[k]) > 1.0)]
        if i < len(CASES): print(CASES[i][0], {k: (round(o[k], 2) if o[k] is not None else None) for k in KEYS}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias > 1 EUR"); sys.exit(1 if bad else 0)
