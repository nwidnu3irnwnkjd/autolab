#!/usr/bin/env python3
"""Verificador fiscal para retencion-irpf-nomina-subir-o-no. Ejecuta el JS con osascript (JavaScriptCore) y comprueba:
A) Casos del Verificador Opus (2026-10-02):
V1 LIRPF 96.3.a.1.º: el «segundo pagador» es el de menor cuantía -> bruto 1.000 + pagador2 20.000 => limite 22.000, no obligado.
V2 bruto 20.000 + pagador2 1.000 => limite 22.000, no obligado.
V3 tipo voluntario mostrado nunca > 100 % (bruto 20.000, pagador2 1.000).
B) Oráculo independiente (re-verificación Opus 2026-10-07), escrito desde el BOE consolidado actualizado el 7/10/2026
   (RIRPF BOE-A-2007-6820 arts. 81, 83, 84, 85, 86, 88.5; LIRPF BOE-A-2006-20764 arts. 19.2, 20, 57, 58, 61, 63, 96, DA 61.ª).
   Cifras legales escritas aquí a mano (no del JS); escalas y mínimos autonómicos leídos de data/params.json (irpf_2026).
   RDL 29/2026 (art. 68.6 deducción 10 % alquiler, desde 8/10/2026) no toca RIRPF 80-88: no cambia la retención; la deducción
   no se modela (excluida como «deducciones estatales»).
C) Los 3 «Casos típicos» (24.000 € al 10 %, 30.000 € al 12 %, 45.000 € al 20 %, Madrid) con cifras recalculadas a mano.
Uso: python3 ops/verif/retencion-irpf-nomina-subir-o-no.py [N aleatorios, def. 800]. Sale 1 si algo falla."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, "projects/decidir/calcs/retencion-irpf-nomina-subir-o-no.js"), encoding="utf-8").read()
src = src[:src.index("function eur(")]
PAR = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json"), encoding="utf-8"))["irpf_2026"]

def run_js(casos):
    js = src + "\nJSON.stringify(%s.map(calcular));" % json.dumps(casos)
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True)
    return json.loads(out.stdout)

# ---------- oráculo ----------
EST = [(0, 9.5), (12450, 12), (20200, 15), (35200, 18.5), (60000, 22.5), (300000, 24.5)]        # LIRPF 63.1
RET = [(0, 19), (12450, 24), (20200, 30), (35200, 37), (60000, 45), (300000, 47)]               # RIRPF 85.1
MIN_EST = (5550, (2400, 2700, 4000, 4500), 2800)                                                 # LIRPF 57, 58
LIM81 = (15876, 16342, 16867)                                                                    # RIRPF 81.1 situación 3.ª
SS, TOPE = 0.047 + 0.0155 + 0.001 + 0.0015, 5101.20 * 12                                         # trabajador indefinido 2026

def tramos(x, esc):
    out = 0.0
    for k, (desde, tipo) in enumerate(esc):
        hasta = esc[k + 1][0] if k + 1 < len(esc) else 1e18
        if x > desde: out += (min(x, hasta) - desde) * tipo / 100.0
    return out

def esc_ccaa(c):
    """Escala y mínimos autonómicos desde params.json (formato tolerante)."""
    d = PAR["ccaa"][c]
    esc = [(float(a), float(b)) for a, b in d["escala_general"]]
    m = d.get("minimo")
    if isinstance(m, dict) and m.get("contribuyente"):
        return esc, (m["contribuyente"], tuple(m["descendientes"]), m["menor3"])
    return esc, None

def min_pf(m, n, m3, mitad):
    """LIRPF 57-58 y 61.1.ª / RIRPF 84: descendientes y menor de 3 por mitad si se comparten."""
    pers, desc, men3 = m
    fam = sum(desc[min(i, 3)] for i in range(n)) + men3 * m3
    return pers + fam * (0.5 if mitad else 1.0)

def red20(rn):  # LIRPF 20 (RDL 4/2024) = RIRPF 83.3.d
    if rn <= 14852: return 7302.0
    if rn <= 17673.52: return 7302 - 1.75 * (rn - 14852)
    if rn < 19747.5: return 2364.34 - 1.14 * (rn - 17673.52)
    return 0.0

def tipo_ret(R, n, m3, mitad):
    if R <= 0 or R <= LIM81[min(n, 2)]: return 0.0                       # 81.1 «no supere»
    neto_ab = R - SS * min(R, TOPE)                                          # 83.3.a-b
    gastos = min(2000.0, neto_ab)                                            # 83.3.c
    base = neto_ab - gastos - min(red20(neto_ab), neto_ab) - (600 if n > 2 else 0)  # 83.3.d-e
    base = max(base, 0.0)
    mpf = min_pf(MIN_EST, n, m3, mitad)                                      # 84
    if base - mpf <= 0: return 0.0                                           # 86.1
    cuota = max(0.0, tramos(base, RET) - tramos(mpf, RET))                   # 85.1
    if R <= 35200: cuota = min(cuota, 0.43 * (R - LIM81[min(n, 2)]))         # 85.3
    return float(int(cuota / R * 10000 + 0.5 + 1e-7)) / 100                  # 86.1 dos decimales

def oraculo(d):
    R1, R2, n, m3 = d["bruto"], d["pagador2"], d["hijos"], d["menores3"]
    mitad = d["reparto"] == "mitad"
    R = R1 + R2
    neto_ab = R - SS * min(R, TOPE)
    blg = max(0.0, neto_ab - min(2000.0, neto_ab) - red20(neto_ab))          # 19.2.f + 20
    esc, mca = esc_ccaa(d["ccaa"])
    mca = mca or MIN_EST
    ci = max(0.0, tramos(blg, EST) - tramos(min_pf(MIN_EST, n, m3, mitad), EST)) + \
         max(0.0, tramos(blg, esc) - tramos(min_pf(mca, n, m3, mitad), esc))
    ded = 0.0
    if R < 20048.45:                                                         # DA 61.ª
        ded = min(590.89 if R <= 17094 else 590.89 - 0.2 * (R - 17094), ci)
    cuota = ci - ded
    t2 = tipo_ret(R2, 0, 0, False) if R2 > 0 else 0.0                        # 88.2: sin comunicación
    retenido = R1 * d["ret"] / 100 + R2 * t2 / 100
    res = cuota - retenido
    menor = min(R1, R2) if R2 > 0 else 0.0                                   # 96.3.a.1.º «por orden de cuantía»
    lim = 22000 if menor <= 1500 else 15876
    obl = 1 if R > lim else 0                                                # 96.2.a «no superen»
    esc_n = (1 if obl else 4) if res > 100 else (2 if res < -100 else 3)
    tipo0 = min(100.0, max(0.0, (cuota - R2 * t2 / 100) / R1 * 100))
    return dict(cuota=cuota, retenido=retenido, resultado=res, tipoLegal=tipo_ret(R1, n, m3, mitad), tipo2=t2,
                tipo0=tipo0, limiteObl=lim, obligado=obl, escenario=esc_n)

def main():
    fallos = []
    B = dict(ret=0, hijos=0, menores3=0, reparto="mitad", ccaa="madrid", euribor=2.5)
    r = run_js([dict(B, bruto=1000, pagador2=20000), dict(B, bruto=20000, pagador2=1000)])
    if r[0]["limiteObl"] != 22000 or r[0]["obligado"] != 0: fallos.append("V1")
    if r[1]["limiteObl"] != 22000 or r[1]["obligado"] != 0: fallos.append("V2")
    if max(x["tipo0"] for x in r) > 100 or max(x["tipo0p2"] for x in r) > 100: fallos.append("V3")
    # C) casos típicos recalculados a mano (journal/verificacion-retencion-reverif-2026-10-07.md)
    M = dict(hijos=0, menores3=0, reparto="entero", pagador2=0, ccaa="madrid", euribor=3.247)
    tip = [(dict(M, bruto=24000, ret=10), 3038.44, 638.44, 12.66, 13.51, 1),
           (dict(M, bruto=30000, ret=12), 4598.02, 998.02, 15.33, 16.42, 1),
           (dict(M, bruto=45000, ret=20), 8881.46, -118.54, 19.74, 21.06, 2)]
    rj = run_js([t[0] for t in tip]); assert len(rj) == 3
    for (d, cu, res, t0, tl, esc), j in zip(tip, rj):
        if abs(j["cuota"] - cu) > 0.01 or abs(j["resultado"] - res) > 0.01 or abs(j["tipo0"] - t0) > 0.005 or j["tipoLegal"] != tl or j["escenario"] != esc:
            fallos.append("tipico %s: %s" % (d["bruto"], {k: j[k] for k in ("cuota", "resultado", "tipo0", "tipoLegal", "escenario")}))
    # B) barrido aleatorio
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    rnd = random.Random(20261007)
    ccaa = list((PAR["ccaa"] if "ccaa" in PAR else {}).keys()) or ["madrid"]
    ccaa = [c for c in ccaa if c in ("andalucia", "aragon", "asturias", "baleares", "canarias", "cantabria", "clm", "cyl", "cataluna",
                                       "extremadura", "galicia", "madrid", "murcia", "rioja", "valencia")]
    casos = []
    for i in range(N):
        n = rnd.choice([0, 0, 0, 1, 2, 3, 4, 5])
        R1 = rnd.choice([rnd.uniform(1000, 25000), rnd.uniform(14000, 22000), rnd.uniform(25000, 80000), rnd.uniform(80000, 400000),
                         rnd.choice([15876, 15877, 16342, 16867, 17094, 20048.45, 22000, 35200, 35201, 61214.4])])
        R2 = rnd.choice([0, 0, 0, rnd.uniform(100, 3000), rnd.uniform(1000, 30000), 1500, 1500.01, 15876, 15877])
        casos.append(dict(bruto=round(R1, 2), ret=round(rnd.uniform(0, 40), 2), hijos=n, menores3=rnd.randint(0, n),
                          reparto=rnd.choice(["entero", "mitad"]), pagador2=round(R2, 2), ccaa=rnd.choice(ccaa), euribor=2.5))
    rj = []
    for k in range(0, N, 200): rj += run_js(casos[k:k + 200])
    assert len(rj) == N and len(r) == 2, "el JS no devolvio todos los casos"
    disc = 0
    for d, j in zip(casos, rj):
        o = oraculo(d)
        bad = [k for k in ("cuota", "retenido", "resultado", "tipo0") if abs(o[k] - j[k]) > 0.01] + \
              [k for k in ("tipoLegal", "tipo2", "limiteObl", "obligado", "escenario") if abs(o[k] - j[k]) > 1e-9]
        if bad:
            disc += 1
            if disc <= 5: fallos.append("disc %s: %s" % (d, {k: (round(o[k], 4), round(j[k], 4)) for k in bad}))
    print("aleatorios: %d, discrepancias: %d" % (N, disc))
    print("\n".join(fallos) or "OK"); sys.exit(1 if fallos else 0)

if __name__ == "__main__":
    main()
