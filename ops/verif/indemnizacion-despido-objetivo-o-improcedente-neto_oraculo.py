#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para indemnizacion-despido-objetivo-o-improcedente-neto. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado 30/09/2026; ET BOE-A-2015-11430 arts. 53.1.b y 56.1 y DT 11.ª; LIRPF BOE-A-2006-20764 arts. 7.e y 18.2):
1. Salario diario = bruto anual / 365 (art. 56.1: «salario por año de servicio»; el bruto incluye las pagas extra prorrateadas). Antigüedad en MESES completos M = años*12 + meses (los periodos < 1 año se prorratean por meses).
2. Objetivo (art. 53.1.b): 20 dias/año * M/12, tope 12 mensualidades = 360 dias (1 mensualidad = 30 dias, equivalencia de la propia DT 11.ª: 720 dias = 24 mensualidades). Sin tramo de 45 dias (la DT 11.ª solo regula el art. 56).
3. Improcedente sin tramo previo (art. 56.1; DT 11.ª.1: contratos desde el 12-2-2012): 33 dias/año * M/12, tope 24 mensualidades = 720 dias.
4. Improcedente con contrato anterior al 12-2-2012 (DT 11.ª.2): 45 dias/año * A/12 (A = meses de servicio hasta el 11-2-2012) + 33 dias/año * (M-A)/12. Tope: 720 dias, salvo que el tramo de 45 dias solo ya supere 720, en cuyo caso el tope es ese
   numero de dias, y nunca mas de 42 mensualidades = 1.260 dias. Si A = 0 es el caso 3.
5. IRPF art. 7.e: exenta la cuantia obligatoria del ET (20 dias en objetivo, 33/45 en improcedente) con limite de 180.000 €; parr. 2: en el objetivo del art. 52.c ET (causas economicas, tecnicas, organizativas o de produccion; selector causa=eco) queda exenta la parte que no supere
   la del improcedente (con DT 11.ª). Limite exento L = legal del improcedente si objetivo+eco, si no la legal del tipo. Exento = min(oferta, L, 180.000); lo demas es rendimiento
   del trabajo. El improcedente solo esta exento si se reconoce en conciliacion (art. 63 LRJS) o sentencia (aviso en pagina, no cambia el calculo). La comparacion con la oferta (escenarios) sigue contra la legal del tipo (20 dias en objetivo). Sin oferta se supone que cobras la legal.
6. Reduccion del 30 % (art. 18.2): periodo de generacion = años de servicio de la relacion extinguida; > 2 años (M > 24 meses). Se aplica sobre el rendimiento tributable imputado en un unico periodo, con base maxima 300.000 €, que se reduce euro a euro entre
   700.000,01 y 1.000.000 € de rendimiento (cero desde 1.000.000 €). No se aplica la regla de los 5 años a estos rendimientos (art. 18.2, 2.º parrafo).
7. IRPF estimado = (tributable - reduccion) * tipo marginal que escribe el usuario (aproximacion); neto = cobrado - IRPF. Igual con la indemnizacion legal de cada tipo para comparar. Escenarios: 1 oferta < legal del tipo (por mas de 1 €), 2 igual (±1 €), 3 mayor,
   4 sin oferta (oferta = 0). Bloqueos: bruto <= 0, antigüedad 0, meses > 11, antes < 0 o antes > M, tipo marginal fuera de 0-55.
Uso: python3 ops/verif/indemnizacion-despido-objetivo-o-improcedente-neto_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
from fractions import Fraction as F
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "indemnizacion-despido-objetivo-o-improcedente-neto"

def reduccion_base(trib):
    """Base sobre la que se aplica el 30 % (art. 18.2): 300.000 €; entre 700.000,01 y 1.000.000 € baja euro a euro; desde 1.000.000 € es cero."""
    tope = F(300000)
    if trib > 700000: tope = max(F(0), tope - (trib - 700000))
    return min(trib, tope)

def irpf_de(cobrado, legal, M, marg):
    exento = min(cobrado, legal, F(180000))  # 'legal' = limite exento
    trib = cobrado - exento
    red = F(30, 100) * reduccion_base(trib) if M > 24 else F(0)
    return exento, trib, red, (trib - red) * marg / 100

def model(d):
    bruto = F(str(d["bruto"])); a = int(d["anios"]); m = int(d["meses"]); antes = int(d["antes"]); oferta = F(str(d["oferta"])); marg = F(str(d["marginal"]))
    M = a * 12 + m
    z = dict(bloqueado=1, escenario=0, M=0, salDia=0, diasObj=0, legalObj=0, diasImp=0, legalImp=0, legal=0, exento=0, trib=0, red=0, irpf=0, neto=0, netoLegal=0, netoObj=0, netoImp=0, difBruta=0, difNeta=0, impMenosObj=0, topeObj=0, topeImp=0, reduccionAplica=0)
    if bruto <= 0 or M <= 0 or a < 0 or m < 0 or m > 11 or antes < 0 or antes > M or marg < 0 or marg > 55 or oferta < 0:
        return z
    sal = bruto / 365
    raw_obj = F(20) * M / 12; dias_obj = min(raw_obj, F(360))
    if antes == 0:
        raw_imp = F(33) * M / 12; cap = F(720)
    else:
        r45 = F(45) * antes / 12
        raw_imp = r45 + F(33) * (M - antes) / 12
        cap = min(r45, F(1260)) if r45 > 720 else F(720)
    dias_imp = min(raw_imp, cap)
    legal_obj = dias_obj * sal; legal_imp = dias_imp * sal
    tipo_obj = d["tipo"] == "objetivo"
    legal = legal_obj if tipo_obj else legal_imp
    hay = oferta > 0
    cobrado = oferta if hay else legal
    lim = legal_imp if (tipo_obj and d.get("causa", "eco") == "eco") else legal
    exento, trib, red, irpf = irpf_de(cobrado, lim, M, marg)
    neto = cobrado - irpf
    # neto de cada tipo si cobrases solo la legal
    _, _, _, i_obj = irpf_de(legal_obj, legal_obj, M, marg); _, _, _, i_imp = irpf_de(legal_imp, legal_imp, M, marg)
    neto_obj = legal_obj - i_obj; neto_imp = legal_imp - i_imp
    neto_legal = neto_obj if tipo_obj else neto_imp
    dif = cobrado - legal
    if not hay: esc = 4
    elif dif < -1: esc = 1
    elif dif <= 1: esc = 2
    else: esc = 3
    fl = float
    return dict(bloqueado=0, escenario=esc, M=M, salDia=fl(sal), diasObj=fl(dias_obj), legalObj=fl(legal_obj), diasImp=fl(dias_imp), legalImp=fl(legal_imp), legal=fl(legal), exento=fl(exento), trib=fl(trib), red=fl(red), irpf=fl(irpf), neto=fl(neto),
                netoLegal=fl(neto_legal), netoObj=fl(neto_obj), netoImp=fl(neto_imp), difBruta=fl(dif), difNeta=fl(neto - neto_legal), impMenosObj=fl(legal_imp - legal_obj), topeObj=1 if raw_obj > 360 else 0, topeImp=1 if raw_imp > cap else 0, reduccionAplica=1 if M > 24 else 0)

B = dict(bruto=30000, anios=8, meses=0, antes=0, tipo="objetivo", causa="eco", oferta=13150, marginal=30)
def V(**k): x = dict(B); x.update(k); return x
CASES = [
 ("1 defecto: objetivo 8 años, oferta = 20 dias", V()),
 ("2 improcedente 8 años sin oferta", V(tipo="improcedente", oferta=0)),
 ("3 improcedente con oferta superior y reduccion 30 %", V(tipo="improcedente", oferta=30000, marginal=37)),
 ("4 objetivo oferta inferior", V(oferta=10000)),
 ("5 improcedente contrato de 2008 (45+33)", V(bruto=36000, anios=18, meses=6, antes=48, tipo="improcedente", oferta=0)),
 ("6 antes = 0 y alta 12-2-2012 (todo a 33)", V(bruto=36000, anios=14, meses=7, antes=0, tipo="improcedente", oferta=0)),
 ("7 antes = 1 mes (alta 11-1-2012)", V(bruto=36000, anios=14, meses=7, antes=1, tipo="improcedente", oferta=0)),
 ("8 tope 12 mensualidades objetivo (25 años)", V(bruto=48000, anios=25, meses=0, oferta=0)),
 ("9 tope 24 mensualidades improcedente (30 años desde 2012)", V(bruto=48000, anios=30, meses=0, tipo="improcedente", oferta=0)),
 ("10 tope 42 mensualidades (45 dias, 30 años previos)", V(bruto=60000, anios=40, meses=0, antes=360, tipo="improcedente", oferta=0)),
 ("11 45 dias previos > 720 dias pero < 1.260", V(bruto=60000, anios=40, meses=0, antes=216, tipo="improcedente", oferta=0)),
 ("12 limite 180.000 € exentos", V(bruto=400000, anios=20, meses=0, tipo="improcedente", oferta=0, marginal=45)),
 ("13 antigüedad 2 años exactos: sin reduccion", V(anios=2, meses=0, tipo="improcedente", oferta=30000)),
 ("14 antigüedad 2 años y 1 mes: con reduccion", V(anios=2, meses=1, tipo="improcedente", oferta=30000)),
 ("15 base reduccion 300.000 y fase 700.000-1.000.000", V(bruto=1500000, anios=20, meses=0, tipo="improcedente", oferta=0, marginal=47)),
 ("15b fase de salida: rendimiento tributable entre 700.000 y 1.000.000 €", V(bruto=570000, anios=20, meses=0, tipo="improcedente", oferta=0, marginal=47)),
 ("18 objetivo 52.c oferta = improcedente: todo exento", V(oferta=21699)),
 ("19 objetivo 52.c oferta 30.000: exceso sobre el improcedente tributa", V(oferta=30000, marginal=37)),
 ("20 objetivo otra causa oferta 21.699: exceso sobre 20 dias tributa", V(causa="otra", oferta=21699, marginal=37)),
 ("21 objetivo 52.c con tramo de 45 dias: oferta = improcedente", V(bruto=36000, anios=14, meses=8, antes=1, oferta=47564)),
 ("16 antes > M bloqueado", V(anios=1, meses=0, antes=13)),
 ("17 meses 12 bloqueado", V(meses=12)),
]
KEYS = ["bloqueado", "escenario", "M", "salDia", "diasObj", "legalObj", "diasImp", "legalImp", "legal", "exento", "trib", "red", "irpf", "neto", "netoLegal", "netoObj", "netoImp", "difBruta", "difNeta", "impMenosObj", "topeObj", "topeImp", "reduccionAplica"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)

def params_ok():
    P = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))["indemnizacion_despido_2026"]
    esperado = dict(dias_objetivo=20, tope_objetivo_mensualidades=12, dias_improcedente=33, tope_improcedente_mensualidades=24, dias_previo_2012=45, tope_previo_dias_general=720, tope_previo_mensualidades=42,
                    dias_mensualidad=30, dias_anio=365, exencion_tope=180000, reduccion_pct=30, reduccion_base_max=300000, reduccion_desde=700000, reduccion_hasta=1000000, reduccion_min_anios=2, umbral_igual_eur=1, marginal_max=55)
    bad = {k: (P.get(k), v) for k, v in esperado.items() if P.get(k) != v}
    if bad: print("PARAMS != norma:", bad)
    return not bad

if __name__ == "__main__":
    rnd = random.Random(37)
    def mk():
        a = rnd.choice([0, 1, 2, 3, 5, 8, 12, 18, 20, 22, 25, 30, 35, 40, rnd.randint(0, 45)]); m = rnd.randint(0, 11)
        if a == 0 and m == 0: m = rnd.randint(1, 11)
        M = a * 12 + m
        antes = rnd.choice([0, 0, 0, 1, rnd.randint(0, M), rnd.randint(0, M), M, min(M, rnd.randint(150, 400))])
        antes = min(antes, M)
        bruto = rnd.choice([rnd.uniform(9000, 30000), rnd.uniform(20000, 90000), rnd.uniform(60000, 400000), rnd.uniform(300000, 1500000), 30000])
        tipo = rnd.choice(["objetivo", "improcedente"])
        d0 = dict(bruto=round(bruto, 2), anios=a, meses=m, antes=antes, tipo=tipo, causa=rnd.choice(["eco", "otra"]), oferta=0, marginal=rnd.choice([0, 19, 30, 37, 45, 47, rnd.uniform(0, 55)]))
        legal = model(d0)["legal"]
        d0["oferta"] = round(rnd.choice([0, 0, legal * rnd.uniform(0.3, 1.0), legal, legal + 0.5, legal - 0.5, legal * rnd.uniform(1.0, 2.5), model(d0)["legalImp"], model(d0)["legalImp"] + 1000, legal + 100000, rnd.uniform(1000, 3000000)]), 2)
        return d0
    sweep = [mk() for _ in range(900)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.5]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("M", "legalObj", "legalImp", "exento", "trib", "irpf", "neto", "escenario")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    pk = params_ok()
    print("barrido %d + %d fijos: %d casos con discrepancias; params %s" % (len(sweep), len(CASES), bad, "OK" if pk else "DIFIEREN")); sys.exit(1 if (bad or not pk) else 0)
