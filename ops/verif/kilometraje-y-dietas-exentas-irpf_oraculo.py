#!/usr/bin/env python3
"""Oraculo independiente (Constructor fiscal, 2026-10-02) para kilometraje-y-dietas-exentas-irpf. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado 30/09/2026; RIRPF BOE-A-2007-6820 art. 9.A; Orden HFP/792/2023 BOE-A-2023-16461; LIRPF BOE-A-2006-20764 arts. 17.1.d y 19.2.a; LGSS BOE-A-2015-11724 art. 147.2.b):
1. Km: la empresa te paga p EUR/km por km desplazamientos de trabajo FUERA del centro de trabajo habitual (no casa-trabajo). Exento = min(p, 0,26) x km (la Orden HFP/792/2023 sube a 0,26 el 0,19 del texto del Reglamento; hay que justificar el desplazamiento). Lo que pase de 0,26 EUR/km es rendimiento del trabajo (art. 9.A.6) y cotiza (LGSS 147.2.b: solo se excluye «en la cuantia y con el alcance» del IRPF).
2. Peajes y aparcamiento: exentos si se justifican; se supone que los pagas y la empresa te los reembolsa con justificante: efecto neto 0 y todo exento.
3. Manutencion en España (art. 9.A.3.a): sin pernocta exento hasta 26,67 EUR/dia; con pernocta hasta 53,34 EUR/dia (la estancia justificada va aparte y no se modela). El exceso por dia tributa y cotiza. Se supone el mismo importe diario d en ambos tipos de dia.
4. Impuestos del tributable T (km + dietas): cotizacion del trabajador w = 6,5 % x T (LGSS 147.2.b, base por debajo de la maxima); IRPF = (T - w T) x t (la cotizacion es gasto deducible, LIRPF 19.2.a; t = tipo marginal que pone el usuario, que ya incluye art. 20 y DA 61.ª).
5. Neto del coche = km x p - tributable_km x (w + (1-w) t) - km x coste_km (peajes: neutros). Neto de dietas = dietas cobradas - tributable_dietas x (w + (1-w) t) (no se resta tu gasto de comida).
6. Veredicto del coche: ganancia >= 5 % del coste real y > 0 -> compensa (1 todo exento / 2 con parte tributable); perdida >= 5 % -> no compensa (4); entre medias empate practico (3). Sin km (solo dietas): escenario 5. Bloqueo 1: sin km ni dias; bloqueo 2: dias sin + con > 365.
7. Equilibrio: p* = coste si coste <= 0,26; si no, 0,26 + (coste - 0,26) / ((1-w)(1-t)).
No modela: vehiculo de empresa, autonomos, transporte publico (se justifica por factura, exento entero), teletrabajo, forales, transporte por carretera (15/25 EUR de estancia sin justificar), personal de vuelo, mas de 9 meses continuados, extranjero (48,08/91,35), base maxima y solidaridad.
Uso: python3 ops/verif/kilometraje-y-dietas-exentas-irpf_oraculo.py [--contenido] -> compara con el JS (osascript); sale 1 si hay discrepancias."""
import json, os, subprocess, sys, random, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "kilometraje-y-dietas-exentas-irpf"
CD = os.path.join(ROOT, "projects/decidir")
PAR = json.load(open(os.path.join(CD, "data/params.json")))["kilometraje_dietas_2026"]
# cifras de la norma, leidas del BOE (se contrastan con params.json)
KM, SIN, CON, W, UMB = 0.26, 26.67, 53.34, 0.065, 0.05
assert (PAR["km_eur"], PAR["manutencion_sin_pernocta_espana"], PAR["manutencion_con_pernocta_espana"], PAR["cotizacion_trabajador_pct"], PAR["umbral_empate_pct"]) == (KM, SIN, CON, 6.5, 5), "params.json no coincide con la norma"
KEYS = ["bloqueado", "escenario", "cobradoKm", "exentoKm", "tribKm", "exentoPeajes", "exentoSin", "tribSin", "exentoCon", "tribCon", "exentoTotal", "tribTotal", "ssExtra", "irpfExtra", "cargaExtra", "costeCoche", "netoCoche", "netoDietas", "cobradoDietas", "pagoEq", "ahorroIRPF", "ahorroSS", "ganNum"]
def pos(x): return max(float(x or 0), 0.0)
def model(d):
    z = dict.fromkeys(KEYS, 0.0)
    km, p, c, pe, ds, dc, di, t = (pos(d[k]) for k in ("km", "pagokm", "costekm", "peajes", "diasSin", "diasCon", "dieta", "tipo"))
    t = min(t, 47.0) / 100
    if km <= 0 and ds + dc <= 0: z["bloqueado"] = 1; return z
    if ds + dc > 365: z["bloqueado"] = 2; return z
    z["cobradoKm"] = km * p
    z["exentoKm"] = km * min(p, KM); z["tribKm"] = km * max(0.0, p - KM)
    z["exentoPeajes"] = pe
    z["exentoSin"] = ds * min(di, SIN); z["tribSin"] = ds * max(0.0, di - SIN)
    z["exentoCon"] = dc * min(di, CON); z["tribCon"] = dc * max(0.0, di - CON)
    z["cobradoDietas"] = (ds + dc) * di
    z["exentoTotal"] = z["exentoKm"] + pe + z["exentoSin"] + z["exentoCon"]
    T = z["tribKm"] + z["tribSin"] + z["tribCon"]; z["tribTotal"] = T
    z["ssExtra"] = W * T; z["irpfExtra"] = (T - W * T) * t; z["cargaExtra"] = z["ssExtra"] + z["irpfExtra"]
    f = W + (1 - W) * t
    z["costeCoche"] = km * c
    z["netoCoche"] = km * p - z["tribKm"] * f - km * c
    z["netoDietas"] = z["cobradoDietas"] - (z["tribSin"] + z["tribCon"]) * f
    z["pagoEq"] = c if c <= KM else KM + (c - KM) / ((1 - W) * (1 - t))
    z["ahorroIRPF"] = z["exentoTotal"] * (1 - W) * t; z["ahorroSS"] = z["exentoTotal"] * W
    n, cc = z["netoCoche"], z["costeCoche"]
    g = 1 if (n >= UMB * cc and n > 0) else (2 if (n <= -UMB * cc and n < 0) else 0)
    z["ganNum"] = g
    if km <= 0: z["escenario"] = 5
    elif g == 1: z["escenario"] = 1 if z["tribKm"] <= 0 else 2
    elif g == 2: z["escenario"] = 4
    else: z["escenario"] = 3
    return z
def run_js(cases):
    js = open(os.path.join(CD, "calcs", SLUG + ".js"), encoding="utf8").read().split("function eur(")[0]
    harness = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", harness], capture_output=True, text=True)
    if out.returncode != 0: print("error JS:", out.stderr.strip()); sys.exit(1)
    return json.loads(out.stdout.strip())
def base(**kw):
    d = dict(km=8000, pagokm=0.26, costekm=0.17, peajes=300, diasSin=40, diasCon=10, dieta=40, tipo=30); d.update(kw); return d
FIJOS = [base(), base(km=0), base(km=0, diasSin=0, diasCon=0), base(diasSin=200, diasCon=166),
         base(pagokm=0.19, costekm=0.19), base(pagokm=0.2601), base(pagokm=0.26, costekm=0.26), base(pagokm=0.40, costekm=0.30),
         base(pagokm=0.10), base(dieta=26.67, diasCon=0), base(dieta=26.68, diasCon=0), base(dieta=53.34, diasSin=0), base(dieta=53.35, diasSin=0),
         base(pagokm=0.0, costekm=0.17), base(tipo=47, pagokm=0.45), base(tipo=0, pagokm=0.45), base(costekm=0.0)]
def barrido(n=800, seed=7):
    r = random.Random(seed); out = []
    for _ in range(n):
        out.append(dict(km=r.choice([0, 0, r.randint(100, 40000)]), pagokm=round(r.choice([0, 0.19, 0.26, r.uniform(0, 0.6)]), 4),
                        costekm=round(r.uniform(0, 0.5), 4), peajes=r.choice([0, r.randint(0, 2000)]), diasSin=r.choice([0, r.randint(0, 250)]),
                        diasCon=r.choice([0, r.randint(0, 120)]), dieta=round(r.choice([0, 26.67, 53.34, r.uniform(0, 120)]), 2), tipo=r.choice([0, 19, 24, 30, 37, 45, 47, r.uniform(0, 47)])))
    return out
def comparar():
    cases = FIJOS + barrido(); res = run_js(cases); bad = 0
    for d, j in zip(cases, res):
        m = model(d)
        for k in KEYS:
            if j.get(k) is None or abs(j[k] - m[k]) > (0.01 if k in ("escenario", "bloqueado", "ganNum") else 1.0):
                bad += 1
                if bad < 15: print("DISCREPANCIA", d, k, "js", j.get(k), "oraculo", m[k])
    print("%s: %d fijos + %d aleatorios, %d discrepancias" % ("OK" if not bad else "FALLO", len(FIJOS), len(cases) - len(FIJOS), bad))
    return bad
def contenido():
    """Pruebas de contenido: respuesta primero sin absolutos, longitudes, FAQ, fuentes, veredicto sin contradicciones, tema, <= 8 inputs, componente EM."""
    j = json.load(open(os.path.join(CD, "calcs", SLUG + ".json"), encoding="utf8"))
    html = open(os.path.join(CD, "content", SLUG + ".html"), encoding="utf8").read()
    js = open(os.path.join(CD, "calcs", SLUG + ".js"), encoding="utf8").read()
    fails = []
    def chk(c, m):
        if not c: fails.append(m)
    chk(len(j["title"]) <= 60, "title > 60 (%d)" % len(j["title"])); chk(len(j["description"]) <= 155, "description > 155 (%d)" % len(j["description"]))
    chk(j["h1"] and j["lead"] and j["veredicto"], "falta h1/lead/veredicto"); chk(j["tema"] in ("impuestos", "coche"), "tema")
    chk(len(j["faqs"]) == 5, "faqs != 5"); chk(len(j["inputs"]) <= 8, "inputs > 8")
    chk("boe.es" in j["sources"] and "agenciatributaria" in j["sources"].lower(), "sources BOE/AEAT")
    first = re.split(r"\.(?=\s|$)", j["lead"])[0]
    chk(re.search(r"(Te compensa|Compensa|compensa)", first) and re.search(r"\d", first), "lead: 1.ª frase sin veredicto condicionado con cifra")
    for nombre, texto in (("html", html), ("lead", j["lead"]), ("veredicto", j["veredicto"]), ("faqs", json.dumps(j["faqs"], ensure_ascii=False)), ("js", js)):
        for m in re.finditer(r"\b(siempre|nunca|garantiza\w*|solo tiene sentido|en todos los casos|cualquier)\b", texto, re.I):
            ctx = texto[max(0, m.start() - 90):m.end() + 60].replace("\n", " ")
            fails.append("absoluto en %s: ...%s..." % (nombre, ctx))
    for need in ("EM.renderResult", "EM.live", "EM.eur", "EM.num"): chk(need in js, "falta " + need)
    # veredicto sin contradicciones: 4 escenarios + 1 de solo dietas, texto leido del JS real
    esc = {1: base(), 2: base(pagokm=0.40, costekm=0.30), 3: base(pagokm=0.17, costekm=0.17), 4: base(pagokm=0.10)}
    for e, d in esc.items(): chk(model(d)["escenario"] == e, "escenario %d no se produce con %s" % (e, d))
    print("contenido:", "OK" if not fails else "FALLOS"); [print("  -", f) for f in fails]
    return len(fails)
if __name__ == "__main__":
    bad = comparar()
    if "--contenido" in sys.argv: bad += contenido()
    sys.exit(1 if bad else 0)
