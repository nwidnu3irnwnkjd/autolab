#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para capitalizar-paro-o-cobrarlo. Escrito desde la norma ANTES del .js.
Norma (BOE consolidado, leido 2/10/2026; corregido tras la verificacion Opus, journal/verificacion-paro.md):
 - LGSS (RDL 8/2015) art. 270.2: 70 % de la base reguladora los 180 primeros dias y 60 % desde el dia 181 (meses 1-6 y 7+).
   Art. 270.3: maximo 175/200/225 % del IPREM (sin hijos / 1 / 2 o mas), minimo 80 % (sin hijos) o 107 % (con hijos), sobre el IPREM mensual + 1/6
   (600 + 100 = 700): 1.225 / 1.400 / 1.575 y 560 / 749. Duracion maxima 720 dias = 24 meses (art. 269.1).
 - Ley 20/2007 (LETA) art. 34.1 (anadido por la Ley 31/2015): regla 1.a (hasta el 100 % del valor actual; para autonomos, por el importe de la inversion
   necesaria incluidos tributos; se deduce el interes legal del dinero), regla 2.a (el resto se abona como subvencion de la cuota, importe fijo = aportacion
   integra, nunca por debajo de la base minima; calculada en dias completos de prestacion: se sigue abonando mientras sigas de alta HASTA AGOTAR los dias/importe
   no capitalizados; SEPE FAQ: «mientras continues en la actividad... o hasta agotar el total de la cuantia»), regla 3.a (solicitud anterior al alta).
 - Ley 20/2007 art. 33: compatibilizar la prestacion con el alta por cuenta propia como maximo 270 dias (9 mensualidades) -> «cobrar mes a mes» siendo autonomo = min(n, 9).
 - RD 1044/1985 art. 2: al menos 3 mensualidades pendientes.
 - Pago unico solo si hay actividad nueva (autonomo): si no, no se puede capitalizar (bloqueo).
Modelo (supuestos propios declarados): descuento por interes legal simple, mensualidad k pendiente (k = 1..n) se descuenta k/12 anos; X proporcional
 (fraccion capitalizada X/V de la prestacion); resto R = T - X*T/V pagado como subvencion fija sm = max(cuota, cuota minima) durante R/sm meses; el interes
 legal NO se descuenta de la parte subvencionada (capTotal = X + R, supuesto declarado; entre V y X+R).
Segundo oraculo: ops/verif/capitalizar-paro-o-cobrarlo-verificador.py (Opus): T, V, capTotal y coste deben coincidir con este y con el JS (<= 1 EUR).
Uso: python3 ops/verif/capitalizar-paro-o-cobrarlo.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, os, subprocess, sys, random, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IPREM = 600.0; BASE = IPREM + IPREM / 6          # 700
TOPE = [BASE * 1.75, BASE * 2.00, BASE * 2.25]
MINI = [BASE * 0.80, BASE * 1.07, BASE * 1.07]
INT = 0.0325
CUOTA_MIN = 653.59 * 0.315

def model(d):
    n, ya, h = int(round(d["meses"])), int(round(d["cobrados"])), min(int(round(d["hijos"])), 2)
    br, inv, cuota, M = d["br"], d["inversion"], d["cuota"], int(round(d["arranque"]))
    if d["actividad"] != "si": return {"bloqueo": 1}
    if n < 3: return {"bloqueo": 2}
    if ya + n > 24: return {"bloqueo": 3}
    c = []
    for k in range(1, n + 1):
        j = ya + k
        raw = br * (0.70 if j <= 6 else 0.60)
        c.append(min(max(raw, MINI[h]), TOPE[h]))
    T = sum(c)
    V = sum(c[k - 1] * (1 - INT * k / 12) for k in range(1, n + 1))
    X = min(inv, V)
    R = T - X * T / V                     # prestacion no capitalizada, se cobra como subvencion de cuota hasta agotarla
    sm = max(cuota, CUOTA_MIN)
    msub = R / sm
    capT = X + R
    coste = T - capT
    mc = min(n, 9)                        # compatibilidad: 270 dias
    Tc = sum(c[:mc])
    recCap = X + min(M, msub) * sm
    recCob = sum(c[:min(M, mc)])
    sCap = recCap - inv - M * cuota
    sCob = recCob - inv - M * cuota
    return {"bloqueo": 0, "primera": c[0], "total": T, "totalCob": Tc, "mesesCob": mc, "valorActual": V, "pagoUnico": X, "mesesSub": msub, "subMes": sm, "subTotal": R,
            "capTotal": capT, "coste": coste, "dif": capT - Tc,
            "propioCap": max(0.0, inv - X), "propioCob": inv, "saldoCap": sCap, "saldoCob": sCob,
            "colchonCap": sCap / cuota if cuota > 0 else 0, "colchonCob": sCob / cuota if cuota > 0 else 0,
            "recCap": recCap, "recCob": recCob, "reintegro": X, "costeTodo": T - V}
KEYS = [k for k in model(dict(meses=12, cobrados=0, hijos=0, br=1500, inversion=6000, cuota=205.88, arranque=6, actividad="si"))]
def tol(k): return 0.01 if k in ("bloqueo",) else (0.05 if k in ("mesesSub", "colchonCap", "colchonCob", "mesesCob") else 1)

B = dict(meses=12, cobrados=0, hijos=0, br=1500, inversion=6000, cuota=205.88, arranque=6, actividad="si")
def V(**k): x = dict(B); x.update(k); return x
CASES = [
 ("1 defecto 12 meses, BR 1.500, inversion 6.000", V()),
 ("2 0 meses -> bloqueo", V(meses=0)),
 ("3 1 mes -> bloqueo", V(meses=1)),
 ("4 2 meses -> bloqueo", V(meses=2)),
 ("5 3 meses exactos (limite RD art. 2)", V(meses=3, inversion=1000)),
 ("6 sin actividad -> bloqueo", V(actividad="no")),
 ("7 tope maximo 2 hijos: BR 4.000, 18 meses pendientes", V(br=4000, hijos=2, meses=18, inversion=20000)),
 ("8 tope maximo sin hijos y 70/60: BR 2.500, ya 3 cobrados, 10 pendientes", V(br=2500, cobrados=3, meses=10, inversion=8000)),
 ("9 minimo con hijos: BR 700, 1 hijo", V(br=700, hijos=1, meses=9, inversion=3000)),
 ("10 inversion > valor actual (se capitaliza todo, sin subvencion)", V(inversion=50000)),
 ("11 inversion 0 (todo subvencion de cuotas)", V(inversion=0, meses=10)),
 ("11b verificador: 12, 1.500, 0, 0, 6.000", V()),
 ("12 ya+n=24 (limite) y ya+n=25 bloqueo", V(cobrados=12, meses=12)),
 ("13 ya+n=25 -> bloqueo", V(cobrados=13, meses=12)),
 ("14 cuota baja 80 (suelo base minima) ", V(cuota=80)),
 ("15 arranque 0 meses", V(arranque=0)),
 ("16 arranque 30 > n", V(arranque=30, meses=8)),
 ("17 cuota 0 (sin NaN)", V(cuota=0)),
 ("19 verificador 2: 18, 4.000, 2 hijos, inv 20.000, cuota 300", V(meses=18, br=4000, hijos=2, inversion=20000, cuota=300)),
 ("20 verificador 3: 9, 900, 1 hijo, 4 cobrados, inv 3.000", V(meses=9, br=900, hijos=1, cobrados=4, inversion=3000)),
 ("21 verificador 4: 24, 2.000, inv 0, cuota 350 (~83 meses de alta)", V(meses=24, br=2000, inversion=0, cuota=350)),
 ("22 n = 9 exacto (limite compatibilidad 270 dias)", V(meses=9)),
 ("23 n = 10 (primer caso con meses no compatibles)", V(meses=10)),
 ("24 n = 12, inversion 12.000 (toda la prestacion capitalizada, cobrar = 9 meses)", V(inversion=12000)),
 ("18 todo a 60 %: cobrados 6, 12 pendientes, BR 1.200", V(cobrados=6, br=1200, inversion=9000)),
]
_sp = importlib.util.spec_from_file_location("verif2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "capitalizar-paro-o-cobrarlo-verificador.py"))
_v2 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_v2)
def oraculo2(c):
    """Segundo oraculo (Opus): devuelve T, V, capTotal, coste; None si hay bloqueo."""
    n, ya, h = int(round(c["meses"])), int(round(c["cobrados"])), min(max(int(round(c["hijos"])), 0), 2)
    if c["actividad"] != "si" or n < 3 or ya + n > 24: return None
    m = _v2.norma(n, c["br"], h, ya, max(c["inversion"], 0), c["cuota"])
    return {"total": m["T"], "valorActual": m["V"], "capTotal": m["cap"], "coste": m["coste"], "subTotal": m["sub"], "pagoUnico": m["X"]}
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/capitalizar-paro-o-cobrarlo.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    rnd = random.Random(7)
    sweep = [dict(meses=rnd.randint(0, 24), cobrados=rnd.randint(0, 22), hijos=rnd.randint(0, 4), br=rnd.choice([400, 900, 1300, 1800, 2500, 3500, 6000]) * rnd.uniform(.8, 1.2),
                  inversion=rnd.choice([0, 1500, 5000, 12000, 30000, 80000]) * rnd.uniform(.7, 1.3), cuota=rnd.choice([0, 80, 205.88, 300, 500, 1000]),
                  arranque=rnd.randint(0, 36), actividad=rnd.choice(["si"] * 6 + ["no"])) for _ in range(600)]
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        ks = ["bloqueo"] if o["bloqueo"] else KEYS
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        diffs = []
        for k in ks:
            v = j.get(k)
            if v is None or v != v or abs(v) == float("inf"): diffs.append((k, "NaN/Inf"))
            elif abs(v - o[k]) > tol(k): diffs.append((k, round(v, 2), round(o[k], 2)))
        o2 = oraculo2(c)
        if o2:
            for k, v2 in o2.items():
                if abs(j[k] - v2) > 1: diffs.append(("oraculo2:" + k, round(j[k], 2), round(v2, 2)))
        bad += len(diffs)
        if i < len(CASES):
            name = CASES[i][0]
            print(f"{name}: " + (f"bloqueo={o['bloqueo']}" if o["bloqueo"] else f"T={o['total']:.2f} V={o['valorActual']:.2f} X={o['pagoUnico']:.2f} sub={o['subTotal']:.2f} cap={o['capTotal']:.2f} coste={o['coste']:.2f} totalCob={o['totalCob']:.2f} dif={o['dif']:.2f} mesesSub={o['mesesSub']:.1f}") + f" | {'OK' if not diffs else diffs}")
        elif diffs: print("DIF", c, diffs)
        # propiedades: capitalizar nunca recibe mas que cobrar en total; pago unico <= inversion
        if not o["bloqueo"]:
            if o["capTotal"] > o["total"] + 1e-6 or o["pagoUnico"] > c["inversion"] + 1e-6: print("PROPIEDAD", c); bad += 1
    print(f"barrido {len(sweep)} + {len(CASES)} fijos: {bad} discrepancias")
    sys.exit(1 if bad else 0)
