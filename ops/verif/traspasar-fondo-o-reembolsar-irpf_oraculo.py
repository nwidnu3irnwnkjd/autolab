#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para traspasar-fondo-o-reembolsar-irpf. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado Ley 35/2006 consultado el 2/10/2026; arts. 94.1.a y 94.2, DT 36.ª, 37.2, 35, 49.1, 66.1, 76, 101.6; Ley 35/2003 y RD 1082/2012 art. 79 solo por remision):
1. TRASPASAR (94.1.a, 2.º parrafo): el reembolso/transmision de IIC que se destina a suscribir otras IIC no computa ganancia ni perdida y las nuevas participaciones conservan valor y fecha de adquisicion.
   Solo en (1.º) reembolsos de FONDOS de inversion y (2.º) transmisiones de SICAV con >500 socios y tu participacion <=5 % en los ultimos 12 meses. Imposible si te ponen el dinero a disposicion (cualquier medio)
   o si la operacion (origen o destino) es un fondo cotizado/ETF o accion de sociedad del mismo tipo (ultimo parrafo de la letra a). Un ETF o accion vendidos tributan siempre.
2. Si traspasas: sin impuesto hoy, el valor sigue creciendo con rentabilidad r; al reembolsar de verdad en el ano N tributa TODA la ganancia (final - coste original) en la escala del ahorro (66.1+76, doble) sobre las otras rentas del ahorro.
   Comision de cambio: se resta del importe que sigue invertido; el valor de adquisicion fiscal conserva el original.
3. REEMBOLSAR hoy: ganancia = valor - comision de reembolso (35: gastos de transmision minoran el valor de transmision) - coste; paga la escala sobre otras rentas hoy; lo que queda (valor - comision - impuesto) se reinvierte (como no hay
   diferimiento, su coste fiscal pasa a ser lo reinvertido) y en el ano N reembolsa de nuevo pagando solo por la ganancia posterior.
4. Perdida latente: reembolsar la computa (compensa solo el 25 % de las otras rentas del ahorro, 49.1; el resto se arrastra y no se valora); traspasar no la computa. Tipo de vehiculo no traspasable -> la opcion no existe.
5. Escala doble 19/21/23/27/30 % desde 0/6.000/50.000/200.000/300.000. Sin retenciones (101.6 18-19 % es pago a cuenta), sin PGE 2026 ni cambios del RDL 26/2026 en estos articulos.
Uso: python3 ops/verif/traspasar-fondo-o-reembolsar-irpf_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRAMOS = [(0, 6000, 0.19), (6000, 50000, 0.21), (50000, 200000, 0.23), (200000, 300000, 0.27), (300000, 1e18, 0.30)]
def cuota(b):
    return sum(max(0.0, min(b, hi) - lo) * t for lo, hi, t in TRAMOS) if b > 0 else 0.0
def impuesto(g, o):
    """Impuesto (o ahorro si negativo) por una ganancia/perdida g con otras rentas del ahorro o>=0."""
    if g >= 0: return cuota(o + g) - cuota(o)
    comp = min(-g, 0.25 * o)
    return -(cuota(o) - cuota(o - comp))
def finales(V, C, r, N, cT, cR, o):
    g = V - cR - C
    t0 = impuesto(g, o)
    reinv = V - cR - t0
    FR = reinv * (1 + r) ** N
    tR = impuesto(FR - reinv, o)
    FT = (V - cT) * (1 + r) ** N
    tT = impuesto(FT - C, o)
    return g, t0, reinv, FR, tR, FR - tR, FT, tT, FT - tT
def model(d):
    V, C, r, N, veh, o, cT, cR = d["valor"], d["coste"], d["rent"] / 100.0, int(round(d["anios"])), d["vehiculo"], d["otras"], d["comT"], d["comR"]
    if V <= 0 or C < 0 or o < 0 or cT < 0 or cR < 0 or cT >= V or cR >= V or r <= -1 or N < 1: return dict(invalido=1)
    g, t0, reinv, FR, tR, nR, FT, tT, nT = finales(V, C, r, N, cT, cR, o)
    ok = veh in ("fondo", "sicav")
    nEq = 0
    if ok:
        for n in range(1, 41):
            f = finales(V, C, r, n, cT, cR, o)
            if f[8] - f[5] >= 0: nEq = n; break
    return dict(invalido=0, traspasable=1 if ok else 0, ganancia=g, impuestoHoy=t0, reinvertido=reinv, valorReem=FR, impuestoFinalReem=tR, netoReem=nR,
                valorTras=FT if ok else 0.0, impuestoFinalTras=tT if ok else 0.0, netoTras=nT if ok else 0.0, ventaja=(nT - nR) if ok else 0.0, nEq=nEq)
B = dict(valor=40000, coste=25000, rent=4, anios=10, vehiculo="fondo", otras=0, comT=0, comR=0)
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto", V()), ("2 ETF no traspasable", V(vehiculo="etf")), ("3 ganancia 0", V(coste=40000)), ("4 perdida latente", V(coste=55000)),
 ("5 1 ano", V(anios=1)), ("6 30 anos", V(anios=30, valor=100000, coste=40000)), ("7 otras rentas 45.000 (tramo)", V(otras=45000, valor=80000, coste=30000)),
 ("8 comision de traspaso alta", V(comT=800, anios=2)), ("9 SICAV cumple", V(vehiculo="sicav")), ("10 SICAV no cumple", V(vehiculo="sicav_no")),
 ("11 rentabilidad 0", V(rent=0, comT=100)), ("12 rentabilidad negativa", V(rent=-3, anios=5)), ("13 ganancia grande, tramos altos", V(valor=900000, coste=100000, rent=5, anios=20)),
 ("14 comision de reembolso", V(comR=300)), ("15 invalido", V(valor=0)), ("16 perdida con otras rentas", V(coste=60000, otras=20000))]
KEYS = ["invalido", "traspasable", "ganancia", "impuestoHoy", "reinvertido", "valorReem", "impuestoFinalReem", "netoReem", "valorTras", "impuestoFinalTras", "netoTras", "ventaja", "nEq"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/traspasar-fondo-o-reembolsar-irpf.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(35)
    def mk():
        V_ = rnd.choice([1000, 40000, 250000, rnd.uniform(500, 1500000)])
        return dict(valor=round(V_, 2), coste=round(rnd.choice([0, V_, V_ * 0.5, rnd.uniform(0, 1.4) * V_]), 2), rent=round(rnd.choice([0, 4, rnd.uniform(-8, 20)]), 2),
                    anios=rnd.choice([1, 2, 10, 30, rnd.randint(1, 40)]), vehiculo=rnd.choice(["fondo", "fondo", "sicav", "sicav_no", "etf"]),
                    otras=round(rnd.choice([0, 0, 5000, 45000, rnd.uniform(0, 350000)]), 2), comT=round(rnd.choice([0, 0, 50, rnd.uniform(0, 0.03) * V_]), 2), comR=round(rnd.choice([0, 0, 100, rnd.uniform(0, 0.03) * V_]), 2))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if k in o and (j.get(k) is None or abs(j[k] - o[k]) > (0.5 if k != "nEq" else 0.1))]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in KEYS if k in o}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
