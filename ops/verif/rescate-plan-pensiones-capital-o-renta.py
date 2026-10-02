#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para rescate-plan-pensiones-capital-o-renta. Escrito desde la norma ANTES del .js. Revisado 2026-10-02 tras la verificacion fiscal (journal/verificacion-rescate.md): arts. 19.2.f y 20.
Norma (Ley 35/2006, BOE-A-2006-20764, consolidada a 30/09/2026):
 - art. 17.2.a.3.a: la prestacion del plan (capital o renta) es rendimiento del trabajo -> base liquidable general.
 - art. 18.1 y 18.3: las reducciones del 30 % no se aplican en renta, y el 30 % de capital solo cubre las prestaciones 17.2.a.1.a y 2.a (no planes de pensiones: 3.a).
 - art. 63.1: cuota estatal = escala(BLG) - escala(parte de la BLG igual al minimo personal y familiar). Idem autonomica con su escala y sus minimos (art. 56.3).
 - art. 19.2.f: otros gastos 2.000 EUR (limitados al rendimiento). Art. 20 (RDL 4/2024): reduccion 7.302 si el rendimiento (neto de gastos a-e; aqui = integro) <= 14.852; 7.302 - 1,75*(R-14.852) hasta 17.673,52; 2.364,34 - 1,14*(R-17.673,52) hasta 19.747,5; 0 por encima.
   Se aplican a la prestacion del plan y a las otras rentas (INTEGRO del trabajo), cada ano. El impuesto ya no es convexo.
 - art. 56.2: si BLG < minimo, el minimo forma parte de la BLG por el importe de esta.
 - arts. 57 y 58: minimo del contribuyente 5.550; descendientes 2.400/2.700/4.000/4.500 (cuarto y siguientes).
Escalas autonomicas y minimos autonomicos: data/params.json (verificados contra BOE por el Verificador, journal/verificacion-irpf.md).
Modelo (supuestos propios, declarados en la pagina): renta = N pagos iguales al INICIO de cada ano (anualidad anticipada) con el saldo restante a rentabilidad g;
 valor de hoy = descontado a g (asi el valor de hoy bruto de la renta es exactamente el saldo y la diferencia es solo impuesto); otras rentas constantes;
 mixto = capital x % en el ano 1 + resto en renta de N pagos (el primero, el mismo ano que el capital). Optimo = menor N <= 40 con impuesto (valor de hoy) <= minimo + 1 EUR.
Uso: python3 ops/verif/rescate-plan-pensiones-capital-o-renta.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]["ccaa"]
EST = [(0, .095), (12450, .12), (20200, .15), (35200, .185), (60000, .225), (300000, .245)]  # art. 63.1 (BOE)
MIN_E, DESC_E = 5550, [2400, 2700, 4000, 4500]                                                    # arts. 57 y 58 (BOE)
NMAX = 40

def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def rate(b, t):
    r = 0.0
    for lo, rr in t:
        if b > lo: r = rr
    return r
def minimos(c, h):
    m = PAR[c].get("minimo")
    pers, dsc = (m["contribuyente"], m["descendientes"]) if m else (MIN_E, DESC_E)
    def suma(d): return sum(d[min(i, 3)] for i in range(h))
    return MIN_E + suma(DESC_E), pers + suma(dsc)
def escc(c): return [(lo, r / 100) for lo, r in PAR[c]["escala_general"]]
def red20(r):
    if r <= 14852: return 7302.0
    if r <= 17673.52: return 7302 - 1.75 * (r - 14852)
    if r < 19747.5: return 2364.34 - 1.14 * (r - 17673.52)
    return 0.0
def cuota(I, c, h):
    b = max(0.0, I - min(2000.0, I) - red20(I))   # base general de un rendimiento integro del trabajo I
    me, mc = minimos(c, h)
    return (esc(b, EST) - esc(min(b, me), EST)) + (esc(b, escc(c)) - esc(min(b, mc), escc(c)))
def marginal(I, c, h):
    b = max(0.0, I - min(2000.0, I) - red20(I))
    me, mc = minimos(c, h)
    return 100 * ((rate(b, EST) if b > me else 0) + (rate(b, escc(c)) if b > mc else 0))

def anualidad(n, g): return sum((1 + g) ** (-k) for k in range(n))     # factor de valor actual de n pagos anticipados
def van_renta(S, O, n, g, c, h):
    a = anualidad(n, g); A = S / a; t = cuota(O + A, c, h) - cuota(O, c, h)
    return A, t, t * a
def model(d):
    S, O, n, g, c, h = d["saldo"], d["otras"], int(d["anos"]), d["rentab"] / 100, d["ccaa"], int(d["hijos"])
    x = d["pctCapital"] / 100
    base = cuota(O, c, h)
    impCap = cuota(O + S, c, h) - base
    A, tA, vanA = van_renta(S, O, n, g, c, h)
    a = anualidad(n, g)
    # mixto
    C = S * x; Am = (S - C) / a
    t0 = cuota(O + C + Am, c, h) - base; t1 = cuota(O + Am, c, h) - base
    impMix = t0 + (n - 1) * t1; vanMix = t0 + t1 * (a - 1)
    brutoRenta = n * A; brutoMix = C + n * Am
    vm = lambda p: (lambda Cp, Ap: (cuota(O + Cp + Ap, c, h) - base) + (cuota(O + Ap, c, h) - base) * (a - 1))(S * p / 100, (S - S * p / 100) / a)
    vmo = min(vm(p) for p in range(101)); pmo = next(p for p in range(101) if vm(p) <= vmo + 1e-9)
    serie = [van_renta(S, O, k, g, c, h)[2] for k in range(1, NMAX + 1)]
    mn = min(serie); nopt = next(k for k in range(1, NMAX + 1) if serie[k - 1] <= mn + 1)
    Ao = van_renta(S, O, nopt, g, c, h)[0]
    return dict(
        pagoRenta=A, impCapital=impCap, impRenta=n * tA, impMixto=impMix,
        vanImpCapital=impCap, vanImpRenta=vanA, vanImpMixto=vanMix,
        netoCapital=S - impCap, netoRenta=brutoRenta - n * tA, netoMixto=brutoMix - impMix,
        vanNetoCapital=S - impCap, vanNetoRenta=S - vanA, vanNetoMixto=S - vanMix,
        ahorroRenta=impCap - vanA, ahorroMixto=impCap - vanMix, costeLiquidez=vanMix - vanA,
        nOptimo=nopt, ahorroOptimo=impCap - serie[nopt - 1], pagoOptimo=Ao,
        tipoMedioCapital=100 * impCap / S if S else 0, tipoMedioRenta=100 * tA / A if A else 0,
        tipoMarginalBase=marginal(O, c, h), tipoMarginalCapital=marginal(O + S, c, h), tipoMarginalRenta=marginal(O + A, c, h),
        serieMin=mn, vanImpMixtoOpt=vmo)
KEYS = list(model(dict(saldo=1, otras=1, anos=2, rentab=1, ccaa="madrid", hijos=0, pctCapital=50)).keys())
def tol(k): return 0.02 if k.startswith("tipo") else (0.001 if k == "nOptimo" else 1)

B = dict(saldo=60000, ccaa="madrid", otras=15000, hijos=0, anos=10, rentab=2, pctCapital=50)
def V(**k): x = dict(B); x.update(k); return x
CASES = [
 ("1 defecto Madrid 60.000, otras 15.000, 10 anos", V()),
 ("2 saldo 0 (sin NaN)", V(saldo=0)),
 ("3 N=1 igual a capital", V(anos=1)),
 ("4 renta muy larga 40 anos", V(anos=40)),
 ("5 otras rentas 0, Madrid", V(otras=0, saldo=100000, anos=8, rentab=3)),
 ("6 otras rentas altas 400.000 (tipo plano)", V(otras=400000, saldo=200000, anos=10)),
 ("7 Cataluna 150.000, otras 25.000, 2 hijos, 15 anos, 100 % capital", V(ccaa="cataluna", saldo=150000, otras=25000, hijos=2, anos=15, pctCapital=100)),
 ("8 Valencia 80.000, 4 hijos, rentab 0, 5 anos, mixto 20 %", V(ccaa="valencia", saldo=80000, otras=18000, hijos=4, anos=5, rentab=0, pctCapital=20)),
 ("9 Extremadura 45.000, rentab -3 %, mixto 100 %", V(ccaa="extremadura", saldo=45000, otras=9000, anos=12, rentab=-3, pctCapital=100)),
 ("10 La Rioja saldo pequeno 12.000 otras 30.000, mixto 0 %", V(ccaa="rioja", saldo=12000, otras=30000, anos=3, pctCapital=0)),
 ("12 INFORME Madrid 60.000/15.000/10 anos (ley real: capital 21.669, renta 25.393, mixto 24.418)", V()),
 ("13 INFORME Madrid 20.000/14.000/5 anos (6.252 / 7.782)", V(saldo=20000, otras=14000, anos=5)),
 ("14 INFORME Andalucia 60.000/12.000/10 anos (21.283 / 17.684 / mixto 12.210 con 40 % capital)", V(ccaa="andalucia", otras=12000)),
 ("15 INFORME Madrid 60.000 / 0 / 10 anos (15.338 / 0)", V(otras=0)),
 ("16 otras ~ limite art. 20 (19.747,5) y pagos en banda", V(otras=19747.5, saldo=30000, anos=4)),
 ("11 Galicia 300.000, otras 12.000, 6 hijos, rentab 6 %, 25 anos", V(ccaa="galicia", saldo=300000, otras=12000, hijos=6, anos=25, rentab=6, pctCapital=30)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/rescate-plan-pensiones-capital-o-renta.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

def properties(d, m):
    """Propiedades que el texto afirma (ya NO se afirma que la renta nunca pague mas ni que el mixto quede entre ambos: con el art. 20 el impuesto no es convexo):
    (1) N=1 = capital; (2) el N optimo no es peor que el N del usuario ni que el capital (N=1); (3) el mixto optimo no es peor que renta ni capital (p=0 y p=100)."""
    e = []
    if int(d["anos"]) == 1 and abs(m["vanImpRenta"] - m["vanImpCapital"]) > 1e-6: e.append("N=1 != capital")
    if m["ahorroOptimo"] < m["ahorroRenta"] - 1.0001 and int(d["anos"]) <= NMAX: e.append("optimo peor que N del usuario")
    if m["ahorroOptimo"] < -1e-6: e.append("optimo peor que capital")
    if m["vanImpMixtoOpt"] > min(m["vanImpRenta"], m["vanImpCapital"]) + 1e-6: e.append("mixto optimo peor que los extremos")
    return e

if __name__ == "__main__":
    rnd = random.Random(11); ca = list(PAR)
    sweep = [dict(saldo=rnd.choice([0, 1000, 8000, 20000, 45000, 90000, 180000, 400000, 1000000]) * rnd.uniform(0.7, 1.3), ccaa=rnd.choice(ca),
                  otras=rnd.choice([0, 3000, 8000, 14000, 22000, 35000, 60000, 100000, 350000]) * rnd.uniform(0.7, 1.3), hijos=rnd.randint(0, 6), anos=rnd.randint(1, 40),
                  rentab=rnd.uniform(-5, 10), pctCapital=rnd.choice([0, 10, 25, 50, 75, 100])) for _ in range(600)]
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0; props = 0
    for i, (name, c) in enumerate(CASES):
        o = model(c); j = jr[i]
        diffs = [(k, round(j[k], 2), round(o[k], 2)) for k in KEYS if abs(j[k] - o[k]) > tol(k)]
        bad += len(diffs)
        print(f"{name}: A={o['pagoRenta']:.2f} impCap={o['impCapital']:.2f} impRen(vh)={o['vanImpRenta']:.2f} ahorro={o['ahorroRenta']:.2f} mixto(vh)={o['vanImpMixto']:.2f} "
              f"Nopt={o['nOptimo']} ahorroOpt={o['ahorroOptimo']:.2f} tmC={o['tipoMedioCapital']:.2f} tmR={o['tipoMedioRenta']:.2f} | {'OK' if not diffs else diffs}")
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        for k in KEYS:
            v = j[k]
            if v is None or v != v or abs(v) == float("inf"): print("NaN/Inf", c, k); bad += 1
        if i >= len(CASES):
            bad += sum(1 for k in KEYS if abs(j[k] - o[k]) > tol(k))
        p = properties(c, o)
        if p: props += 1; print("PROPIEDAD", p, c)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} discrepancias; propiedades rotas: {props}")
    sys.exit(1 if bad or props else 0)
