#!/usr/bin/env python3
"""Script independiente (Constructor) de calcs/freidora-de-aire-u-horno-cuanto-gasta.js, escrito desde la especificacion.
Uso: python3 ops/verif/freidora-de-aire-u-horno-cuanto-gasta.py [--write-tests]
Hace: barrido de 400 casos aleatorios contra el JS real (osascript), bordes, 4 escenarios de veredicto con EM simulado y comprobaciones de contenido."""
import json, os, random, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "freidora-de-aire-u-horno-cuanto-gasta"
CD = os.path.join(ROOT, "projects/decidir")
IEE, IEE_MIN, IVA = 5.11269632 / 100, 0.001, 0.21
# alternativa: (kW medios, min precalentamiento, min coccion tipico, es gas)
ALT = [(1.5, 10, 35, 0), (1.2, 8, 30, 0), (0.8, 0, 8, 0), (2.0, 8, 35, 1)]
def oraculo(d):
    pe = max(d["precio"] * (1 + IEE), d["precio"] + IEE_MIN) * (1 + IVA)
    kw, pre, _, gas = ALT[int(round(d["alt"]))]
    kfr = d["kwFr"] * (3 + d["minFr"]) / 60
    kal = kw * (pre + d["minAlt"]) / 60
    cfr = kfr * pe
    cal = kal * (d["precioGas"] if gas else pe)
    n = d["usos"] * 52
    afr, aal = cfr * n, cal * n
    am = d["compra"] / 8
    tot = afr + am
    dif = aal - tot
    ah = aal - afr
    if d["compra"] <= 0: anios = 0.0 if ah >= 0 else -1.0
    else: anios = d["compra"] / ah if ah > 0 else -1.0
    if cal - cfr > 0: ueq = am / (52 * (cal - cfr)) if d["compra"] > 0 else 0.0
    else: ueq = -1.0
    gan = 2 if abs(dif) < max(1.0, 0.05 * max(tot, aal)) else (0 if dif > 0 else 1)
    return {"precioEf": pe, "kwhFr": kfr, "kwhAlt": kal, "costeFr": cfr, "costeAlt": cal, "usosAno": n, "anualFr": afr, "anualAlt": aal,
            "amortAnual": am, "totalFr": tot, "diferencia": dif, "ahorroEnergia": ah, "aniosAmort": anios, "usosEq": ueq, "esGas": gas, "ganador": gan}
B = dict(alt=0, usos=4, precio=0.2, precioGas=0.064, kwFr=1.4, minFr=20, minAlt=35, compra=80)
TESTS = [dict(B),                                                      # tradicional: gana la freidora
         dict(B, alt=1, minAlt=30),                                    # ventilado
         dict(B, alt=2, minAlt=8),                                     # microondas: gana el microondas
         dict(B, alt=3, minAlt=35),                                    # gas barato: gana el gas
         dict(B, compra=400),                                          # compra alta: no amortiza, gana el horno
         dict(B, usos=0, compra=0)]                                    # sin usos ni compra: empate
BORDES = [dict(B, compra=0), dict(B, precio=0), dict(B, usos=30, compra=0, alt=0), dict(B, usos=0), dict(B, alt=3, precioGas=0),
          dict(B, kwFr=0.1, minFr=1), dict(B, compra=0, alt=2)]
def rnd(r):
    return dict(alt=r.choice([0, 1, 2, 3]), usos=r.choice([0, 1, 3, 7, 14, 30]) * r.random(), precio=r.choice([0, 0.05, 0.2, 0.3]) + r.random() * 0.02,
                precioGas=r.choice([0, 0.04, 0.064, 0.1]) + r.random() * 0.01, kwFr=0.2 + r.random() * 2.3, minFr=1 + r.random() * 50,
                minAlt=1 + r.random() * 90, compra=r.choice([0, 0, 40, 80, 150, 400]) * r.random())
def js_src():
    return open(os.path.join(CD, "calcs", SLUG + ".js")).read()
def correr_js(ins):
    js = js_src().split("function eur(")[0]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)], capture_output=True, text=True)
    return json.loads(out.stdout)
STUB = """
var __out = [], __vals = {};
var EM = { eur: function(x, n){ n = (n === undefined ? 0 : n); return x.toFixed(n).replace('.', ',') + ' EUR'; }, num: function(x, n){ return Number(x).toFixed(n === undefined ? 0 : n).replace('.', ','); },
  renderResult: function(o){ __out.push(o); }, live: function(f, fn){ fn(); } };
var document = { getElementById: function(id){ return { value: String(__vals[id]), addEventListener: function(){ } }; } };
"""
def veredictos(ins):
    js = js_src()
    res = []
    for d in ins:
        code = STUB + "__vals = %s;\n" % json.dumps(d) + js + "\nJSON.stringify(__out);"
        out = subprocess.run(["osascript", "-l", "JavaScript", "-e", code], capture_output=True, text=True)
        res.append(json.loads(out.stdout)[0] if out.stdout.strip() else {"err": out.stderr})
    return res
def contenido():
    bad = 0
    j = json.load(open(os.path.join(CD, "calcs", SLUG + ".json")))
    html = open(os.path.join(CD, "content", SLUG + ".html")).read()
    def chk(c, m):
        nonlocal bad
        if not c: bad += 1; print("CONTENIDO", m)
    chk(len(j["title"]) <= 60, "title %d" % len(j["title"]))
    chk(len(j["description"]) <= 155, "description %d" % len(j["description"]))
    chk(j.get("h1") and j.get("tema") == "energia" and j.get("veredicto"), "h1/tema/veredicto")
    chk(len(j["inputs"]) <= 8, "inputs %d" % len(j["inputs"]))
    chk(3 <= len(j["faqs"]) <= 5, "faqs")
    for q, a in j["faqs"]: chk(len(a.split()) <= 50, "FAQ %d palabras: %s" % (len(a.split()), q))
    chk("https://www.boe.es" in j["sources"] and "ree.es" in j["sources"], "sources enlazadas")
    t = json.load(open(os.path.join(CD, "calcs", SLUG + ".test.json")))["cases"][0]["expect"]
    lead = j["lead"]
    fm = lambda x: ("%.2f" % x).replace(".", ",")
    chk(fm(t["costeFr"]) in lead and fm(t["costeAlt"]) in lead, "lead sin cifra del ejemplo")
    chk(re.search(r"\b(si|salvo|cuando|a partir)\b", lead.split(".")[0]) is not None, "lead sin condicion en la 1.a frase")
    chk(html.lstrip().startswith("<p><strong>"), "respuesta primero")
    todo = html + json.dumps(j, ensure_ascii=False)
    for m in re.finditer(r"(?i)\b(siempre|nunca|garantiza|en todos los casos|cualquier)\b", todo): chk(False, "absoluto: " + m.group(0))
    chk(not re.search(r"(?i)\b(philips|cosori|ninja|tefal|xiaomi|moulinex|cecotec|taurus|bosch|balay|samsung|ariete)\b", todo), "marcas")
    src_js = js_src()
    for m in ["EM.renderResult", "EM.live", "EM.eur", "EM.num"]: chk(m in src_js, "falta " + m)
    return bad
if __name__ == "__main__":
    r = random.Random(53); ins = TESTS + BORDES + [rnd(r) for _ in range(400)]; js = correr_js(ins); bad = 0
    for d, o in zip(ins, js):
        for k, v in oraculo(d).items():
            tol = 0 if k in ("ganador", "esGas", "usosAno") else (0.01 if k in ("aniosAmort", "usosEq", "precioEf", "kwhFr", "kwhAlt") else 1.0)
            if o[k] is None or abs(o[k] - v) > max(tol, 1e-6 * abs(v)):
                bad += 1; print("DISCREPANCIA", d, k, o[k], v)
        for k, v in o.items():
            if v is None or (isinstance(v, float) and (v != v or abs(v) == float("inf"))): bad += 1; print("NaN/Inf", d, k)
    print("casos:", len(ins), "discrepancias:", bad)
    esc = [TESTS[0], TESTS[2], TESTS[4], TESTS[5]]
    for d, v in zip(esc, veredictos(esc)):
        o = oraculo(d); txt = v.get("verdict", "ERR")
        ok = ("gana la freidora" in txt and o["ganador"] == 0) or ("gana el " in txt and o["ganador"] == 1) or ("empate" in txt and o["ganador"] == 2)
        ok = ok and v.get("winner") in ("freidora", "alternativa", "empate")
        print("escenario", "OK" if ok else "FALLA", "|", txt)
        if not ok: bad += 1
    if "--write-tests" in sys.argv:
        keys = ["costeFr", "costeAlt", "kwhFr", "kwhAlt", "anualFr", "anualAlt", "amortAnual", "totalFr", "diferencia", "ahorroEnergia", "aniosAmort", "usosEq", "ganador"]
        cases = [{"in": d, "expect": {k: round(oraculo(d)[k], 2) for k in keys}, "tol": 1} for d in TESTS]
        json.dump({"func": "calcular", "cases": cases}, open(os.path.join(CD, "calcs", SLUG + ".test.json"), "w"), indent=1)
        print("test.json escrito"); sys.exit(1 if bad else 0)
    if os.path.exists(os.path.join(CD, "content", SLUG + ".html")): bad += contenido()
    sys.exit(1 if bad else 0)
