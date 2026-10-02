#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal Sonnet, 2026-10-02) para loteria-navidad-premio-neto-hacienda. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado LIRPF leido el 2/10/2026, DA 33.ª; redaccion del apartado 2 por Ley 6/2018 art. 67.1):
1. Premios de Loterias y Apuestas del Estado (y CCAA, ONCE, Cruz Roja) tributan por gravamen especial, NO por la base del IRPF (DA 33.ª ap. 8). Se exige por separado por cada decimo, fraccion o cupon (ap. 1 in fine).
2. Exento el premio integro <= 40.000 EUR; lo que excede de 40.000 EUR tributa (ap. 2). Cuota = 20 % de la base (ap. 4); retencion del 20 % sobre la misma base (ap. 6) en el cobro: el neto cobrado es el definitivo.
3. Titularidad compartida: la cuantia exenta y la base se prorratean entre cotitulares segun su cuota (ap. 2 y 3). Con n cotitulares a partes iguales cada uno ve X/n, exento 40.000/n. Suma de exentos = 40.000 por decimo: compartir NO multiplica la exencion.
4. Si uno solo cobra y reparte despues (sin cotitularidad identificada), el gravamen recae entero sobre quien cobra (misma cuota total); el reparto posterior es una donacion (ISD, no modelado).
5. Varios decimos con el mismo premio: la exencion de 40.000 EUR se aplica a cada decimo. Premio de decimo < 0,50 EUR: no modelado.
Escenarios: 0 invalido; 1 premio por decimo <= 40.000 (sin retencion); 2 > 40.000, un titular; 3 > 40.000, cotitulares; 4 > 40.000, uno cobra y reparte.
Uso: python3 ops/verif/loteria-navidad-premio-neto-hacienda_oraculo.py -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def model(d):
    out = dict(bloqueo=0, esc=0)
    x, nd, np_ = d["premio"], int(round(d["decimos"])), int(round(d["personas"]))
    if not x > 0: out["bloqueo"] = 1
    elif nd < 1: out["bloqueo"] = 2
    elif np_ < 1: out["bloqueo"] = 3
    if out["bloqueo"]: return out
    # por cotitular (partes iguales), cada decimo por separado
    pers_exento = pers_base = pers_ret = pers_neto = 0.0
    share = x / np_; ex_share = 40000.0 / np_
    base_s = max(0.0, share - ex_share)
    ret_s = 0.20 * base_s
    for _ in range(nd):
        pers_exento += min(share, ex_share); pers_base += base_s; pers_ret += ret_s; pers_neto += share - ret_s
    out.update(bruto=x * nd, exento=pers_exento * np_, sujeto=pers_base * np_, retencion=pers_ret * np_, netoTotal=pers_neto * np_,
               netoDecimo=(share - ret_s) * np_, netoPersona=pers_neto, brutoPersona=share * nd, retPersona=pers_ret, sujetoPersona=pers_base)
    out["esc"] = 1 if x <= 40000 else (2 if np_ == 1 else (3 if d["cobro"] == "cotitulares" else 4))
    return out
B = dict(premio=400000, decimos=1, personas=1, cobro="cotitulares")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 Gordo 400000 un decimo", V()), ("2 borde 39999.99", V(premio=39999.99)), ("3 borde 40000", V(premio=40000)), ("4 borde 40000.01", V(premio=40000.01)),
 ("5 segundo 125000 x2", V(premio=125000, decimos=2)), ("6 tercero 50000 entre 5 cotitulares", V(premio=50000, personas=5)), ("7 Gordo entre 10, uno cobra", V(personas=10, cobro="uno")),
 ("8 premio 20000 x 5 decimos", V(premio=20000, decimos=5)), ("9 premio 0", V(premio=0)), ("10 0 decimos", V(decimos=0)), ("11 0 personas", V(personas=0)),
 ("12 gran premio 1e6 entre 3", V(premio=1000000, personas=3)), ("13 6000 x 3 entre 2", V(premio=6000, decimos=3, personas=2)), ("14 300000 x 2 entre 4 cotitulares", V(premio=300000, decimos=2, personas=4))]
KEYS = ["bloqueo", "esc", "bruto", "exento", "sujeto", "retencion", "netoTotal", "netoDecimo", "netoPersona", "brutoPersona", "retPersona", "sujetoPersona"]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/loteria-navidad-premio-neto-hacienda.js")).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
if __name__ == "__main__":
    rnd = random.Random(2026)
    def mk():
        return dict(premio=rnd.choice([0, 100, 6000, 39999.99, 40000, 40000.01, 50000, 125000, 400000, rnd.uniform(1, 2000000), rnd.uniform(30000, 60000)]),
                    decimos=rnd.choice([0, 1, 1, 2, 3, 5, 10, rnd.randint(1, 40)]), personas=rnd.choice([0, 1, 1, 2, 3, 4, 10, rnd.randint(1, 60)]), cobro=rnd.choice(["cotitulares", "uno"]))
    cases = [c for _, c in CASES] + [mk() for _ in range(600)]
    res = js(cases); bad = 0
    for i, (c, r) in enumerate(zip(cases, res)):
        m = model(c)
        for k in KEYS:
            if k not in m: continue
            a, b = m[k], r.get(k)
            if b is None or abs(a - b) > (0 if k in ("bloqueo", "esc") else 0.01): bad += 1; print("DISCREPA", i, c, k, a, b)
    print(len(cases), "casos,", bad, "discrepancias")
    sys.exit(1 if bad else 0)
