#!/usr/bin/env python3
"""Oraculo independiente (Constructor, 2026-10-02) para obligado-a-declarar-renta-dos-pagadores. Escrito desde la norma ANTES del .js.
Normas (BOE consolidado, leidas el 2/10/2026): LIRPF (BOE-A-2006-20764) art. 96.2 (22.000 EUR trabajo; 1.600 EUR capital mobiliario y ganancias con retencion; 1.000 EUR rentas inmobiliarias imputadas, Letras del Tesoro
y ayudas VPO; 1.000 EUR conjunto general; alta en RETA obliga siempre), art. 96.3 (15.876 EUR: mas de un pagador con el 2.o y siguientes > 1.500 EUR, pension compensatoria/alimentos, pagador no obligado a retener, tipo fijo;
vuelve a 22.000 si 2.o y siguientes <= 1.500 o solo prestaciones pasivas con procedimiento especial), art. 96.4 y RIRPF art. 61.1 (plan de pensiones/doble imposicion internacional: obligado en todo caso);
IMV: Ley 19/2021 (obligados aunque no lleguen a los limites; AEAT Manual Renta 2025). Convencion: «con el limite de X» = no obliga hasta X inclusive; supera X = obliga.
Codigos: estado 0 no obligado / 1 obligado / 2 depende / 3 foral (no modelado); supuesto 0 ninguno, 1 trabajo > 22.000, 2 varios pagadores > 15.876, 3 pension compensatoria > 15.876, 4 pagador sin obligacion de retener > 15.876,
5 tipo fijo > 15.876, 6 capital+ganancias con retencion > 1.600, 7 inmobiliarias/Letras/VPO > 1.000, 10 RETA, 11 plan pensiones/doble imposicion, 12 IMV, 13 otras rentas con total > 1.000, 14 depende (otras rentas, total <= 1.000).
Uso: python3 ops/verif/obligado-a-declarar-renta-dos-pagadores.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
L_GEN, L_MULTI, L_CAP, L_INM, L_TOT, TOL2 = 22000.0, 15876.0, 1600.0, 1000.0, 1000.0, 1500.0
def model(d):
    if d["reg"] == "foral": return dict(estado=3, supuesto=0, limiteTrabajo=0, totalTrabajo=0, resto=0, exceso=0, limite=0, nMotivos=0, margen=0)
    pag = sorted([max(0.0, float(d[k])) for k in ("t1", "t2", "t3") if float(d[k]) > 0], reverse=True)
    cap, inm = max(0.0, float(d["capRet"])), max(0.0, float(d["inmo"]))
    esp, obl, noret = int(d["esp"]), int(d.get("obl", 0)), int(d["noRet"]) == 1
    total = sum(pag); resto = sum(pag[1:]) if pag else 0.0
    # art. 96.3.a: mas de un pagador -> 15.876, salvo que el 2.o y siguientes no superen 1.500 o solo pasivas con procedimiento especial (esp 7)
    causas = []
    if len(pag) >= 2 and resto > TOL2 and esp != 7: causas.append(2)
    if esp == 1: causas.append(3)
    if noret and pag: causas.append(4)
    if esp == 2: causas.append(5)
    lim = L_MULTI if causas else L_GEN
    trig = []   # (prioridad, supuesto, exceso, limite)
    if obl == 3: trig.append((10, 0, 0))
    if obl == 4: trig.append((11, 0, 0))
    if obl == 6: trig.append((12, 0, 0))
    if total > lim: trig.append((causas[0] if causas and lim == L_MULTI else 1, total - lim, lim))
    if cap > L_CAP: trig.append((6, cap - L_CAP, L_CAP))
    if inm > L_INM: trig.append((7, inm - L_INM, L_INM))
    todo = total + cap + inm
    if esp == 5 and todo > L_TOT: trig.append((13, todo - L_TOT, L_TOT))
    r = dict(limiteTrabajo=lim, totalTrabajo=total, resto=resto, nMotivos=len(trig), margen=max(0.0, lim - total))
    if trig:
        s, ex, li = trig[0]; r.update(estado=1, supuesto=s, exceso=ex, limite=li)
    elif esp == 5: r.update(estado=2, supuesto=14, exceso=0, limite=L_TOT)
    else: r.update(estado=0, supuesto=0, exceso=0, limite=0)
    return r
B = dict(t1=18000, t2=2000, t3=0, noRet="0", capRet=0, inmo=0, esp="0", reg="comun")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 defecto: 18.000 + 2.000 (2.o > 1.500)", V()), ("2 22.000 exacto, un pagador", V(t1=22000, t2=0)), ("3 22.001", V(t1=22001, t2=0)),
 ("4 15.876 exacto con dos pagadores", V(t1=13876, t2=2000)), ("5 15.877 con dos pagadores", V(t1=13877, t2=2000)),
 ("6 2.o pagador 1.500 exacto, 20.000", V(t1=18500, t2=1500)), ("7 2.o pagador 1.501, 20.001", V(t1=18500, t2=1501)),
 ("8 cero pagadores y todo 0", V(t1=0, t2=0)), ("9 tres pagadores, resto 1.200+500", V(t1=15000, t2=1200, t3=500)),
 ("10 capital 1.600 / 1.601", V(t1=0, t2=0, capRet=1601)), ("11 inmobiliarias 1.000 / 1.001", V(t1=10000, t2=0, inmo=1001)),
 ("12 RETA", V(obl="3", t1=5000, t2=0)), ("13 IMV", V(obl="6", t1=0, t2=0)), ("14 otras rentas, total <= 1.000", V(esp="5", t1=600, t2=0)),
 ("15 pasivas con procedimiento especial, 2 pensiones 20.000", V(esp="7", t1=15000, t2=5000)), ("16 pagador sin retencion 16.000", V(noRet="1", t1=16000, t2=0)),
 ("17 compensatoria 15.000+1.000 sin retencion", V(t1=15000, t2=1000, esp="1", noRet="1")), ("18 22.000+1.600+1.000", V(t1=22000, t2=0, capRet=1600, inmo=1000)),
 ("19 15.000+876+1", V(t1=15000, t2=876, t3=1)), ("20 plan pensiones + compensatoria", V(t1=5000, t2=0, esp="1", obl="4"))]
KEYS = ["estado", "supuesto", "limiteTrabajo", "totalTrabajo", "resto", "exceso", "limite", "nMotivos", "margen"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/obligado-a-declarar-renta-dos-pagadores.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(31)
    def mk():
        pick = lambda xs: rnd.choice(xs)
        edge = [0, 0, 1, 1500, 1501, 1600, 1601, 1000, 1001, 15876, 15877, 22000, 22001, 5000, 12000, 18000, 24000, 40000]
        v = lambda: pick(edge) if rnd.random() < .5 else rnd.uniform(0, 30000)
        return dict(t1=v(), t2=v() if rnd.random() < .7 else 0, t3=v() if rnd.random() < .3 else 0, noRet=pick(["0", "0", "1"]), capRet=v() if rnd.random() < .5 else 0,
                    inmo=v() if rnd.random() < .5 else 0, esp=pick(["0"] * 4 + ["1", "2", "5", "7"]), obl=pick(["0"] * 5 + ["3", "4", "6"]), reg=pick(["comun"] * 12 + ["foral"]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.005]
        if i < len(CASES): print(CASES[i][0], {k: o[k] for k in KEYS}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} casos con discrepancias"); sys.exit(1 if bad else 0)
