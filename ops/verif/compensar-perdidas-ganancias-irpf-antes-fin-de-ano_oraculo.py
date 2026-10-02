#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para compensar-perdidas-ganancias-irpf-antes-fin-de-ano. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado de la Ley 35/2006 consultado el 2/10/2026; arts. 33.5.f-g, 37.2, 46, 49, 66.1, 76, DT 7.ª.7, DA 39.ª):
1. Base del ahorro (art. 49.1) = saldo positivo de sumar DOS compartimentos que se integran SOLO entre si: (a) rendimientos del capital mobiliario (art. 46.a: dividendos, intereses; entrada rcm+otras)
   y (b) ganancias y perdidas por transmisiones (art. 46.b; entrada gp - perd - perdida vendida). Si uno sale negativo se compensa con el saldo positivo del otro con limite del 25 % de ese saldo
   positivo (texto vigente desde 1/1/2015, sin calendario); si aun queda saldo negativo, se arrastra 4 anos (el de 2022 caduca tras 2026).
2. Orden AEAT (Manual Renta, fases 1.ª y 2.ª): primero el ejercicio (incl. 25 % entre cajones), despues el saldo negativo de anos anteriores (input prev) contra el saldo de ganancias restante y luego contra el 25 % restante del capital mobiliario (limite conjunto). Origen 2021 o antes: caducado (no se usa).
3. Perdida vendida (input perdida): solo computa si NO hay recompra de valores homogeneos (33.5.f: 2 meses antes o despues, cotizados; 33.5.g: 1 ano, no cotizados); con recompra no computa en 2026 y se integra
   cuando se transmitan los homogeneos (el ahorro de 2026 es 0). FIFO (37.2): la perdida es la del lote mas antiguo; el usuario ya da el importe.
4. Cuota = escala del ahorro (66.1 estatal + 76 autonomica, iguales; tabla de cuota integra del BOE por mitad: 0/570/5.190/22.440/35.940 en 0/6.000/50.000/200.000/300.000, tipos 9,5/10,5/11,5/13,5/15; total = doble).
   Minimo personal y familiar supuesto absorbido por la base general (no se aplica al ahorro). Sin retenciones ni deducciones.
5. Ahorro fiscal = cuota sin venta - cuota con venta. Capacidad = mayor perdida adicional que aun reduce la base de 2026. Arrastre = saldos negativos que pasan a 2027-2030.
Uso: python3 ops/verif/compensar-perdidas-ganancias-irpf-antes-fin-de-ano_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAB = [(0, 0, 9.5), (6000, 570, 10.5), (50000, 5190, 11.5), (200000, 22440, 13.5), (300000, 35940, 15)]
def escala(x):
    if x <= 0: return 0.0
    for desde, cuota, tipo in reversed(TAB):
        if x > desde: return 2 * (cuota + (x - desde) * tipo / 100)
def liquidar(G, P, R, O, A, loss, y0):
    """Orden AEAT (Manual Renta, fases 1.ª y 2.ª): ejercicio primero (25 % entre cajones), despues saldo antiguo (b restante, luego 25 % restante de a)."""
    a = R + O; b = G - P - loss
    ant = A if y0 in (2022, 2023, 2024, 2025) else 0.0
    nuevo = aneg = 0.0
    if b < 0: nuevo = -b; b = 0.0
    if a < 0: aneg = -a; a = 0.0
    topeA = 0.25 * a; topeB = 0.25 * b
    y = min(nuevo, topeA); nuevo -= y; a -= y; topeA -= y
    z = min(aneg, topeB); aneg -= z; b -= z
    t = min(ant, b); ant -= t; b -= t
    x = min(ant, topeA); ant -= x; a -= x
    return a + b, nuevo + aneg + (0.0 if y0 == 2022 else ant), (ant if y0 == 2022 else 0.0)
def model(d):
    G, P, R, O, A, L = d["gp"], d["perd"], d["rcm"], d["otras"], d["prev"], d["perdida"]
    if min(G, P, A, L) < 0: return dict(invalido=1)
    y0 = int(d["anio"]) if d["anio"].isdigit() else 0
    rec = d["recompra"] == "si"
    b0, c0, k0 = liquidar(G, P, R, O, A, 0.0, y0)
    b1, c1, k1 = liquidar(G, P, R, O, A, 0.0 if rec else L, y0)
    bx, cx, kx = liquidar(G, P, R, O, A, L, y0)
    binf, _, _ = liquidar(G, P, R, O, A, 1e12, y0)
    return dict(invalido=0, baseSin=b0, baseCon=b1, cuotaSin=escala(b0), cuotaCon=escala(b1), ahorro=escala(b0) - escala(b1),
                ahorroSinRecompra=escala(b0) - escala(bx), arrastreSin=c0, arrastreCon=c1, caducaSin=k0, caducaCon=k1, capacidad=b0 - binf)
B = dict(gp=12000, perd=2000, rcm=3000, prev=0, anio="2025", recompra="no", perdida=5000, otras=0)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto: ganancias netas 10.000 absorben 5.000", V()), ("2 recompra", V(recompra="si")), ("3 sin ganancias, solo dividendos (25 %)", V(gp=0, perd=0, rcm=8000, perdida=6000)),
 ("4 sin nada que compensar", V(gp=0, perd=0, rcm=0, perdida=5000)), ("5 saldo 2022 que caduca", V(gp=10000, perd=0, rcm=0, perdida=4000, prev=6000, anio="2022")),
 ("6 saldo 2021 caducado", V(prev=9000, anio="antes", perdida=0)), ("7 perdida mayor que ganancias, parcial", V(gp=3000, perd=0, rcm=4000, perdida=9000)),
 ("8 rcm negativo compensa 25 % de ganancias", V(gp=20000, perd=0, rcm=0, otras=-10000, perdida=0)), ("9 cruza tramo 50.000", V(gp=90000, perd=0, rcm=2000, perdida=30000)),
 ("10 perdida 0", V(perdida=0)), ("11 base exacta 6.000", V(gp=6000, perd=0, rcm=0, perdida=0)), ("12 ano de origen 2023 con ganancias", V(prev=3000, anio="2023", perdida=1000)),
 ("13 perdida del ano + antiguo vs dividendos", V(gp=0, perd=4000, rcm=20000, prev=7000, anio="2024", perdida=2000)), ("14 negativo", V(gp=-1)), ("15 AEAT: caduca 2000 del saldo 2022", V(gp=0, perd=0, rcm=8000, otras=0, prev=2000, anio="2022", perdida=6000)), ("16 AEAT: otras negativas", V(gp=1000, perd=0, rcm=0, otras=-1000, prev=500, anio="2023", perdida=0))]
KEYS = ["invalido", "baseSin", "baseCon", "cuotaSin", "cuotaCon", "ahorro", "ahorroSinRecompra", "arrastreSin", "arrastreCon", "caducaSin", "caducaCon", "capacidad"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/compensar-perdidas-ganancias-irpf-antes-fin-de-ano.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(34)
    def mk():
        f = lambda *c: round(rnd.choice(list(c) + [rnd.uniform(0, 120000)]), 2)
        return dict(gp=f(0, 12000), perd=f(0, 2000), rcm=f(0, 3000), prev=f(0, 0, 6000), anio=rnd.choice(["2022", "2023", "2024", "2025", "antes"]), recompra=rnd.choice(["no", "no", "si"]),
                    perdida=f(0, 5000), otras=round(rnd.choice([0, 0, -4000, rnd.uniform(-30000, 30000)]), 2))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if k in o and (j.get(k) is None or abs(j[k] - o[k]) > 0.5)]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in KEYS if k in o}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
