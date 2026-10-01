#!/usr/bin/env python3
"""Oraculo independiente del Verificador fiscal (2026-10-02) para plan-pensiones-o-fondo-indexado.
Escribe desde la norma: Ley 35/2006 art. 52.1 (limite), 17.2.a.3.a (rescate = trabajo, base general),
63.1 (escala estatal, transcrita del BOE), 66.1+76 (ahorro, transcrita del BOE), 56.2 (remanente del minimo al ahorro, opcional).
Escalas autonomicas: data/params.json (Madrid contrastada en BOE). Mismos supuestos de modelo declarados en la pagina.
Uso: python3 ops/verif/plan-pensiones-o-fondo-indexado.py  -> compara con el JS (osascript) y sale 1 si hay diferencias > tol."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["irpf_2026"]["ccaa"]
EST = [(0, .095), (12450, .12), (20200, .15), (35200, .185), (60000, .225), (300000, .245)]   # art. 63.1 BOE
AHO = [(0, .19), (6000, .21), (50000, .23), (200000, .27), (300000, .30)]                     # arts. 66.1 + 76 (9,5+9,5 ...)
MIN_E = 5550                                                                                    # art. 57
def esc(b, t):
    s = 0.0
    for i, (lo, r) in enumerate(t):
        hi = t[i + 1][0] if i + 1 < len(t) else float("inf")
        if b > lo: s += (min(b, hi) - lo) * r
    return s
def ccaa(c): d = PR[c]; return [(lo, r / 100) for lo, r in d["escala_general"]], (d["minimo"] or {"contribuyente": MIN_E})["contribuyente"]
def irpf(bg, ba, c, remanente=False):
    """Cuota integra estatal+autonomica: general y ahorro, con minimo personal (art. 56: se aplica primero a la general)."""
    ea, ma = ccaa(c); tot = 0.0
    for t, m in ((EST, MIN_E), (ea, ma)):
        mg = min(m, bg); tot += esc(bg, t) - esc(mg, t)
        mr = (m - mg) if remanente else 0
        # ahorro: la mitad estatal/autonomica es identica (AHO/2 cada una)
        half = [(lo, r / 2) for lo, r in AHO]
        mra = min(mr, ba); tot += esc(ba, half) - esc(mra, half)
    return tot
def model(d, remanente=False):
    n = max(round(d["anos"]), 1); c = d["ccaa"]
    lim = min(1500.0, 0.30 * d["renta"]); e = min(d["aportacion"], lim)          # art. 52.1 (limite general)
    s = irpf(d["renta"], 0, c) - irpf(d["renta"] - e, 0, c)                          # ahorro fiscal anual
    gp = 1 + (d["rentab"] - d["comPlan"]) / 100; gf = 1 + (d["rentab"] - d["comFondo"]) / 100
    def run(n):
        # saldo plan al cierre del ano n con aportacion e a principio de ano
        Pv = 0.0; F = 0.0; R = 0.0
        for _ in range(n): Pv = (Pv + e) * gp; F = (F + e) * gf; R = R * gf + s   # devolucion al cierre, reinvertida
        b0 = d["renta"] * d["rescate"]
        gR = max(R - s * n, 0); gF = max(F - e * n, 0)
        taxL = irpf(b0 + Pv, gR, c, remanente) - irpf(b0, 0, c, remanente)          # rescate de una vez + reembolso de R
        tax10 = 10 * (irpf(b0 + Pv / 10, 0, c) - irpf(b0, 0, c)) + (irpf(b0, gR, c, remanente) - irpf(b0, 0, c, remanente))
        taxF = irpf(b0, gF, c, remanente) - irpf(b0, 0, c, remanente)
        en = max(e - s, 0); Fn = 0.0
        for _ in range(n): Fn = (Fn + en) * gf
        taxFn = irpf(b0, max(Fn - en * n, 0), c, remanente) - irpf(b0, 0, c, remanente)
        taxPL = irpf(b0 + Pv, 0, c) - irpf(b0, 0, c)
        return dict(e=e, s=s, Pv=Pv, planL=Pv + R - taxL, plan10=Pv + R - tax10, fondo=F - taxF, sinR=(Pv - taxPL) - (Fn - taxFn), taxPL=taxPL, R=R, F=F, taxF=taxF, taxR=taxL - taxPL)
    r = run(n)
    teq = 100 * (1 - (r["fondo"] - (r["R"] - r["taxR"])) / r["Pv"]) if r["Pv"] > 0 else -1
    return dict(aportacionEfectiva=e, ahorroFiscalAnual=s, patrimonioPlan=r["planL"], patrimonioFondo=r["fondo"], diferencia=r["planL"] - r["fondo"],
                patrimonioPlan10=r["plan10"], diferencia10=r["plan10"] - r["fondo"], diferenciaSinReinvertir=r["sinR"],
                tipoMedioRescate=100 * r["taxPL"] / r["Pv"] if r["Pv"] else 0, tipoEquilibrio=teq)
B = dict(aportacion=1500, anos=25, renta=35000, ccaa="madrid", rescate=1, rentab=4, comPlan=1.0, comFondo=0.2)
def V(**k): x = dict(B); x.update(k); return x
CASES = [
 ("1 defecto Madrid", V()),
 ("2 aportacion 5.000 > 1.500 (no legal en plan individual)", V(aportacion=5000, renta=45000)),
 ("3 limite 30 %: renta 3.000, aporta 2.000, rescate x2", V(aportacion=2000, renta=3000, ccaa="andalucia", rescate=2, anos=10)),
 ("4 autonomo plan simplificado aporta 5.750 (1.500+4.250)", V(aportacion=5750, renta=40000, ccaa="valencia")),
 ("5 rescate x0,5 (menor), una vez vs 10 pagos", V(renta=60000, rescate=0.5, anos=20, rentab=5, comPlan=0.5, comFondo=0.5)),
 ("6 horizonte 1 ano CyL", V(aportacion=1500, anos=1, renta=45000, ccaa="cyl")),
 ("7 rescate x2 (mayor) Cataluna 60.000, 30 anos", V(renta=60000, ccaa="cataluna", rescate=2, anos=30)),
 ("8 renta 20.000 Extremadura rescate x0,5", V(renta=20000, ccaa="extremadura", rescate=0.5, anos=30)),
 ("9 renta 150.000 La Rioja, 6 %/0,3/0,1", V(renta=150000, ccaa="rioja", rentab=6, comPlan=0.3, comFondo=0.1, anos=15)),
 ("10 rentabilidad -2 % Galicia 10 anos", V(renta=30000, ccaa="galicia", rentab=-2, anos=10)),
 ("11 renta 8.000 rescate x0,5 (minimo sobrante -> ahorro, art. 56.2)", V(renta=8000, ccaa="madrid", rescate=0.5, aportacion=1500, anos=30, rentab=6, comPlan=0.2, comFondo=0.2)),
]
KEYS = ["aportacionEfectiva", "ahorroFiscalAnual", "patrimonioPlan", "patrimonioFondo", "diferencia", "patrimonioPlan10", "diferencia10", "diferenciaSinReinvertir", "tipoMedioRescate", "tipoEquilibrio"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/plan-pensiones-o-fondo-indexado.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    return json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True).stdout)
if __name__ == "__main__":
    rnd = random.Random(7); ca = list(PR)
    sweep = [dict(aportacion=rnd.choice([300, 1000, 1500, 3000]), anos=rnd.randint(1, 45), renta=rnd.choice([4000, 9000, 15000, 25000, 40000, 70000, 120000, 400000]),
                  ccaa=rnd.choice(ca), rescate=rnd.choice([0.5, 1, 2]), rentab=rnd.uniform(-3, 9), comPlan=rnd.uniform(0, 2), comFondo=rnd.uniform(0, 1)) for _ in range(500)]
    jr = js([c for _, c in CASES] + sweep); bad = 0
    for i, (name, c) in enumerate(CASES):
        o = model(c); j = jr[i]; o2 = model(c, remanente=True)
        diffs = [(k, round(j[k], 2), round(o[k], 2)) for k in KEYS if abs(j[k] - o[k]) > (0.02 if k.startswith("tipo") else 1)]
        bad += len(diffs)
        print(f"{name}: e={o['aportacionEfectiva']:.0f} s={o['ahorroFiscalAnual']:.2f} plan={o['patrimonioPlan']:.2f} fondo={o['patrimonioFondo']:.2f} dif={o['diferencia']:.2f} "
              f"plan10={o['patrimonioPlan10']:.2f} dif10={o['diferencia10']:.2f} sinR={o['diferenciaSinReinvertir']:.2f} tmr={o['tipoMedioRescate']:.2f} teq={o['tipoEquilibrio']:.2f} | JS dif={j['diferencia']:.2f} "
              f"| art56.2 dif={o2['diferencia']:.2f} {'OK' if not diffs else diffs}")
    sb = sum(1 for k2, c in enumerate(sweep) for k in KEYS if abs(jr[len(CASES) + k2][k] - model(c)[k]) > (0.02 if k.startswith("tipo") else 1))
    print(f"barrido 500: {sb} discrepancias"); sys.exit(1 if bad or sb else 0)
