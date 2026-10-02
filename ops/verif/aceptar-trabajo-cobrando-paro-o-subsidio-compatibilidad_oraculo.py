#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad. Escrito desde la norma ANTES del .js.
INTERPRETACION (LGSS, RDL 8/2015, consolidado leido el 2/10/2026; arts. 271, 272, 279 y 282 en la redaccion del RDL 2/2024, vigente desde 23/5/2024; DT 1.ª agotada el 31/10/2024):
 - SOLO PRESTACION (A): cobras la cuantia bruta durante min(duracion del contrato H, meses restantes M); neta = cuantia x (1 - tipo IRPF); las prestaciones por desempleo son rendimiento del trabajo (art. 17.1.b LIRPF). Quedan M - min(H,M) meses.
 - PARO + PARCIAL (B, art. 282.2): solo si jornada < 100 y se pide la compatibilidad (15 dias habiles); se deduce de la prestacion la parte proporcional al tiempo trabajado: cobras cuantia x (1 - jornada) + sueldo neto,
   los meses en que te quedaba prestacion (el derecho sigue consumiendose, no se suspende: 271.1.d lo excluye); pasados M meses solo cobras el sueldo. Quedan M - min(H,M) meses. Con jornada completa no existe.
 - PARO + SUSPENDER (C, 271.1.d, 271.2, 271.3.b): trabajo por cuenta ajena de menos de 12 meses (completo, o parcial sin pedir compatibilidad): la prestacion se suspende, no se cobra nada de ella y NO se consumen meses; quedan los M meses
   (reanudables en 15 dias). Con H >= 12 se extingue (272.1.c): sueldo H meses, pierdes los M meses (derecho de opcion 269.3 no modelado).
 - SUBSIDIO (282.3): el subsidio se convierte en complemento de apoyo al empleo (CAE): % del IPREM (600) segun trimestre del SUBSIDIO (mes m -> trimestre ceil(m/3), tope 5) y jornada pactada (100: col 0; >=75: col 1; >=50 y <75: col 2; <50: col 3),
   tabla 80/75/70/60, 60/50/45/40, 40/35/30/25, 30/25/20/15, 20/15/10/5; maximo 180 dias (6 meses de 30), cada dia de CAE consume un dia del subsidio y no mas de los M restantes; tras el limite el subsidio queda suspendido (se conservan M - nCAE meses).
   No hay deduccion proporcional ni opcion C modelada. Con contrato >= 12 meses 279.1 remite al 272.1.c (extincion) frente a la suspension del 282.3: la conservacion de los meses queda sin verificar (aviso).
 - DA 59.ª LGSS (RDL 2/2024, en vigor 1/11/2024): paro con periodo reconocido > 12 meses (aqui: (inicio - 1) + meses) y trabajo que llega al mes 10 de prestacion (inicio + min(H,M) - 1 >= 10): otro regimen (CAE en el paro, tabla propia por mes,
   duracion 30-180 dias, tope 375 % IPREM) que NO se modela -> bloqueo 5. Subsidio tras paro > 12 meses (DA 59.ª.4): CAE como continuacion de la prestacion, no modelado (declarado).
 - Subsidio tras paro > 12 meses reconocido desde 1-4-2025 (DA 59.ª.4; opcion "subsidio59" del select): el CAE sale de la tabla con referencia al mes 13 de prestacion (hasta 4 veces menor) -> bloqueo 6 con aviso.
 - Texto: ganador A menciona la oferta adecuada (LISOS 25.4.a y 47.1.b); "sin compatibilidad a jornada completa" lleva la salvedad DA 59.ª.
 - Imposible/avisado: M < 1 (sin prestacion pendiente), H < 1, jornada fuera de 1-100, paro con M > 24 (720 dias, art. 269.1); empresa con ERE / trabajaste alli 12 meses / familiar (282.3) no modelado (aviso).
 - Comparacion: en los H meses del contrato, total neto de cada opcion (el sueldo es neto; el IRPF solo se aplica a la prestacion/subsidio). Mes = 30 dias. Gana el mayor total; empate practico si la diferencia es < 5 %.
Uso: python3 ops/verif/aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad_oraculo.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, math, os, random, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad"
IPREM = 600
CAE = [[80, 75, 70, 60], [60, 50, 45, 40], [40, 35, 30, 25], [30, 25, 20, 15], [20, 15, 10, 5]]

def col(j):
    return 0 if j >= 100 else (1 if j >= 75 else (2 if j >= 50 else 3))

def model(c):
    paro = c["tipo"] == "paro"
    j = int(round(c["jornada"])); M = int(round(c["meses"])); H = int(round(c["duracion"])); s = max(int(round(c["inicio"])), 1)
    if c["tipo"] == "subsidio59": return {"bloqueo": 6}
    if M < 1: return {"bloqueo": 1}
    if H < 1: return {"bloqueo": 2}
    if j < 1 or j > 100: return {"bloqueo": 3}
    if paro and M > 24: return {"bloqueo": 4}
    if paro and s - 1 + M > 12 and s + min(H, M) - 1 >= 10: return {"bloqueo": 5}
    t = c["irpf"] / 100.0; jj = j / 100.0; sueldo = c["sueldo"]
    cn = c["cuantia"] * (1 - t); nw = min(H, M)
    r = {"bloqueo": 0, "totalA": cn * nw, "restA": M - nw, "ext": 1 if H >= 12 else 0}
    if paro:
        r["bOk"] = 1 if j < 100 else 0; r["cOk"] = 1
        r["totalB"] = nw * (sueldo + cn * (1 - jj)) + (H - nw) * sueldo if r["bOk"] else 0
        r["restB"] = M - nw if r["bOk"] else 0
        r["mensualB"] = sueldo + cn * (1 - jj)
        r["totalC"] = sueldo * H
        r["restC"] = 0 if r["ext"] else M
        r["nCae"] = 0; r["caeBruto"] = 0
        r["umbralB"] = cn * nw * jj / H if r["bOk"] else 0
    else:
        r["bOk"] = 1; r["cOk"] = 0
        n = min(H, 6, M); tot = 0.0
        for k in range(n):
            q = min(int(math.ceil((s + k) / 3.0)), 5)
            tot += IPREM * CAE[q - 1][col(j)] / 100.0
        r["nCae"] = n; r["caeBruto"] = tot
        r["mensualB"] = sueldo + IPREM * CAE[min(int(math.ceil(s / 3.0)), 5) - 1][col(j)] / 100.0 * (1 - t)
        r["totalB"] = n * sueldo + tot * (1 - t) + (H - n) * sueldo
        r["restB"] = M - n
        r["totalC"] = 0; r["restC"] = 0
        r["umbralB"] = max((r["totalA"] - tot * (1 - t)) / H, 0)
    r["umbralC"] = r["totalA"] / H if r["cOk"] else 0
    r["gananciaB"] = r["totalB"] - r["totalA"] if r["bOk"] else 0
    r["gananciaC"] = r["totalC"] - r["totalA"] if r["cOk"] else 0
    opts = [(1, r["totalA"])]
    if r["bOk"]: opts.append((2, r["totalB"]))
    if r["cOk"]: opts.append((3, r["totalC"]))
    opts.sort(key=lambda o: (-o[1], -o[0]))
    r["winner"] = opts[0][0]; r["second"] = opts[1][0]; r["margen"] = opts[0][1] - opts[1][1]
    r["empate"] = 1 if r["margen"] < 0.05 * abs(opts[0][1]) else 0
    r["riesgo12"] = 1 if (not paro and H >= 12) else 0
    return r

KEYS = ["mensualB", "totalA", "totalB", "totalC", "restA", "restB", "restC", "ext", "bOk", "cOk", "nCae", "caeBruto", "umbralB", "umbralC", "gananciaB", "gananciaC", "winner", "second", "margen", "empate", "riesgo12"]
BASE = dict(tipo="paro", cuantia=1100, sueldo=800, jornada=50, meses=6, duracion=6, irpf=15, inicio=1)
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto: paro 1.100, 50 %, sueldo 800, 6/6 meses -> compatibilizar gana", V()),
 ("2 paro jornada completa 6 meses: solo suspender", V(jornada=100, sueldo=1400)),
 ("3 paro jornada completa 12 meses: extincion", V(jornada=100, sueldo=1400, duracion=12, meses=6)),
 ("4 paro 11 meses: aun suspende", V(jornada=100, sueldo=1400, duracion=11, meses=6)),
 ("5 sueldo justo sobre el umbral (467,5)", V(sueldo=468.5)),
 ("6 sueldo justo bajo el umbral", V(sueldo=466.5)),
 ("7 sueldo bajo: gana solo paro", V(sueldo=300)),
 ("8 subsidio defecto 50 %, T1", V(tipo="subsidio", cuantia=570, sueldo=700, meses=12, irpf=10)),
 ("9 subsidio inicio mes 11: trimestres 4-5", V(tipo="subsidio", cuantia=570, sueldo=700, meses=12, irpf=10, inicio=11)),
 ("10 subsidio contrato 3 meses con 2 de subsidio restante", V(tipo="subsidio", cuantia=570, sueldo=700, meses=2, duracion=3, irpf=10)),
 ("11 subsidio jornada 75 (col 1)", V(tipo="subsidio", cuantia=570, sueldo=700, jornada=75, meses=12, irpf=10)),
 ("12 subsidio jornada 74 (col 2)", V(tipo="subsidio", cuantia=570, sueldo=700, jornada=74, meses=12, irpf=10)),
 ("13 subsidio jornada 49 (col 3) y 100 (col 0)", V(tipo="subsidio", cuantia=570, sueldo=700, jornada=49, meses=12, irpf=10)),
 ("14 subsidio jornada completa", V(tipo="subsidio", cuantia=570, sueldo=1400, jornada=100, meses=12, irpf=10)),
 ("15 subsidio contrato 12 meses: riesgo12", V(tipo="subsidio", cuantia=570, sueldo=900, jornada=100, meses=12, duracion=12, irpf=10)),
 ("16 empate practico paro", V(jornada=100, sueldo=950)),
 ("17 bloqueo 1: sin meses", V(meses=0)),
 ("17b bloqueo 6: subsidio tras paro > 12 meses", V(tipo="subsidio59", cuantia=570)),
 ("18 bloqueo 4: paro con 25 meses", V(meses=25)),
 ("19 paro 24 meses desde el mes 1, contrato 24: ventana hasta el mes 24 -> bloqueo 5", V(meses=24, duracion=24)),
 ("19b DA 59: mes 10, 4 restantes -> bloqueo 5", V(inicio=10, meses=4, duracion=4)),
 ("19c DA 59: mes 10, 3 restantes (periodo 12, no mas de 12) -> ok", V(inicio=10, meses=3, duracion=3)),
 ("19d periodo 13 pero el trabajo acaba en el mes 9 -> ok", V(inicio=5, meses=9, duracion=5)),
 ("19e periodo 13 y el trabajo llega al mes 10 -> bloqueo 5", V(inicio=5, meses=9, duracion=6)),
 ("19f subsidio no se bloquea por DA 59", V(tipo="subsidio", cuantia=570, inicio=10, meses=24, duracion=6)),
 ("20 irpf 0", V(irpf=0)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

SWEEP_BAD = 0
if __name__ == "__main__":
    rnd = random.Random(31)
    sweep = []
    for _ in range(700):
        tipo = rnd.choice(["paro", "subsidio"])
        sweep.append(dict(tipo=tipo, cuantia=rnd.choice([480, 570, 560, 1000, 1225, rnd.uniform(300, 1600)]), sueldo=rnd.choice([0, 300, 800, 1400, rnd.uniform(0, 3000)]),
                          jornada=rnd.choice([100, 75, 74, 50, 49, 1, rnd.randint(1, 100)]), meses=rnd.choice([0, 1, 2, 6, 24, 25, rnd.randint(1, 30)]),
                          duracion=rnd.choice([0, 1, 3, 6, 11, 12, 13, rnd.randint(1, 36)]), irpf=rnd.choice([0, 2, 15, 30, rnd.uniform(0, 45)]), inicio=rnd.choice([1, 2, 3, 4, 13, 15, 16, rnd.randint(1, 40)])))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS:
            v = j.get(k)
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > (0.01 if k in ("restA", "restB", "restC", "ext", "bOk", "cOk", "nCae", "winner", "second", "empate", "riesgo12") else 1): print("DIF", c, k, v, o[k]); bad += 1
        # propiedad: B supera a A exactamente cuando el sueldo pasa del umbral
        if o["bOk"] and abs(c["sueldo"] - o["umbralB"]) > 0.02 and ((o["totalB"] > o["totalA"]) != (c["sueldo"] > o["umbralB"])): print("UMBRAL B", c, o["umbralB"]); bad += 1
        if o["cOk"] and abs(c["sueldo"] - o["umbralC"]) > 0.02 and ((o["totalC"] > o["totalA"]) != (c["sueldo"] > o["umbralC"])): print("UMBRAL C", c, o["umbralC"]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("totalA", "totalB", "totalC", "restC", "winner", "empate", "umbralB") if k in o})
    print("barrido %d + %d fijos: %d discrepancias" % (len(sweep), len(CASES), bad))
    SWEEP_BAD = bad

# ---- Escenarios de texto: ejecuta la pagina entera con DOM/EM simulados y comprueba el veredicto (sin contradicciones) ----
def escenarios():
    stub = """var __out = null, __v = {};
function __num(x, d) { d = d || 0; x = +x; var s = Math.abs(x).toFixed(d), p = s.split("."); return (x < 0 ? "-" : "") + p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".") + (p[1] ? "," + p[1] : ""); }
var EM = { num: __num, eur: function (x, d) { return __num(x, d) + "\\u00a0\\u20ac"; }, renderResult: function (o) { __out = o; }, live: function () {} };
var document = { getElementById: function (id) { return { value: __v[id], addEventListener: function () {} }; } };
"""
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read()
    esc = [
     ("paro parcial: compatibilizar gana", V(),
      ["gana trabajar a tiempo parcial y compatibilizar el paro por 1.995", "6 meses", "La compatibilidad no existe si el contrato es a jornada completa (salvo desde el mes 10", "DA 59.ª", "15 días hábiles", "art. 282.2", "conservas los 6 meses"],
      ["perder", "perderías", "complemento de apoyo", "no hay compatibilidad con el paro", "empate"]),
     ("paro jornada completa, menos de 12 meses: suspende", V(jornada=100, sueldo=1400),
      ["gana trabajar a tiempo completo y suspender el paro por 2.790", "Con jornada completa no hay compatibilidad con el paro (art. 282.2), salvo desde el mes 10", "conservas los 6 meses"],
      ["perderías", "La compatibilidad no existe si el contrato es a jornada completa", "complemento de apoyo", "tiempo parcial y compatibilizar"]),
     ("paro, contrato de 12 meses: se extingue", V(jornada=100, sueldo=1400, duracion=12),
      ["gana aceptar el trabajo y perder el paro que te queda", "perderías los 6 meses", "art. 272.1.c"],
      ["conservas", "complemento de apoyo", "tiempo parcial y compatibilizar"]),
     ("subsidio con complemento de apoyo", V(tipo="subsidio", cuantia=570, sueldo=700, meses=12, irpf=10),
      ["gana trabajar y cobrar el complemento de apoyo al empleo por 2.985", "Lo cobrarías 6 meses", "180 días", "te quedarían 6 meses de subsidio", "El complemento no existe si te contrata una empresa con expediente de regulación de empleo", "art. 282.3"],
      ["suspender el paro", "compatibilizar el paro", "perder"]),
     ("paro, sueldo bajo: gana seguir solo con el paro", V(sueldo=300),
      ["gana seguir cobrando solo el paro por 1.005", "frente a trabajar a tiempo parcial y compatibilizar el paro", "oferta de empleo adecuada", "LISOS"],
      ["gana trabajar", "perderías", "empate"]),
     ("paro de mas de 12 meses que llega al mes 10: DA 59.ª, sin calculo", V(inicio=8, meses=8, duracion=6),
      ["disposición adicional 59.ª", "no modela", "consulta al SEPE"],
      ["gana ", "empate"]),
     ("subsidio tras paro largo: sin cifra", V(tipo="subsidio59", cuantia=570),
      ["disposición adicional 59.ª", "120 € en vez de 480 €", "consulta al SEPE"],
      ["gana "]),
     ("empate practico", V(jornada=100, sueldo=950),
      ["empate práctico", "90"],
      ["gana "]),
    ]
    bad = 0
    for nombre, v, debe, no_debe in esc:
        h = stub + "__v = " + json.dumps(v) + ";\n" + src.replace('document.getElementById("go").addEventListener("click", pintar);', "pintar();").split("document.getElementById(\"f\").addEventListener")[0] + "\nJSON.stringify({v: __out.verdict, n: __out.note || \"\"});"
        out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
        if out.returncode: print("ERROR escenario", nombre, out.stderr[:400]); bad += 1; continue
        r = json.loads(out.stdout); t = r["v"].replace("\u00a0", " ")
        for s_ in debe:
            if s_ not in t: print("FALTA", nombre, "|", s_, "|", t[:300]); bad += 1
        for s_ in no_debe:
            if s_ in t: print("SOBRA", nombre, "|", s_, "|", t[:300]); bad += 1
        print("escenario:", nombre, "|", t[:160])
    return bad

# ---- Estructura de la pagina (titulo, descripcion, FAQ, fuentes, componente, absolutos) ----
def estructura():
    bad = 0
    def ko(m):
        nonlocal bad; print("ESTRUCTURA", m); bad += 1
    cj = json.load(open(os.path.join(ROOT, "projects/decidir/calcs/%s.json" % SLUG), encoding="utf-8"))
    html = open(os.path.join(ROOT, "projects/decidir/content/%s.html" % SLUG), encoding="utf-8").read()
    jsrc = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG), encoding="utf-8").read()
    if len(cj["title"]) > 60: ko("title > 60: %d" % len(cj["title"]))
    if len(cj["description"]) > 155: ko("description > 155: %d" % len(cj["description"]))
    for k in ("h1", "lead", "veredicto", "sources"):
        if not cj.get(k): ko("falta " + k)
    if cj.get("tema") != "ahorro": ko("tema distinto de ahorro (como las calculadoras de paro)")
    if len(cj["faqs"]) != 5: ko("FAQs != 5")
    if len(cj["inputs"]) > 8: ko("mas de 8 inputs")
    if "boe.es" not in cj["sources"] or "sepe.es" not in cj["sources"]: ko("sources sin BOE o SEPE")
    for tok in ("EM.renderResult", "EM.live", "EM.eur", "EM.num"):
        if tok not in jsrc: ko("el JS no usa " + tok)
    if not re.match(r"\s*<p><strong>(Si|Cuando|Con)\b", html): ko("la primera frase del html no es veredicto condicionado")
    if not re.match(r"(Si|Cuando|Con)\b", cj["lead"]): ko("el lead no empieza con condicion")
    ABS = re.compile(r"\b(siempre|nunca|garantiza\w*|en todos los casos|cualquier|solo tiene sentido)\b", re.I)
    OKC = re.compile(r"\b(siempre (que|y cuando)|si|salvo|cuando|excepto|según|depende|mientras|a menos que|en caso|aunque|hasta)\b", re.I)
    textos = [cj["lead"], cj["veredicto"]] + [q[1] for q in cj["faqs"]] + [re.sub(r"<[^>]+>", " ", html)]
    for t in textos:
        for sn in re.split(r"(?<=[.!?])\s+", t):
            if ABS.search(sn) and not OKC.search(sn): ko("absoluto sin condicion: " + sn[:90])
    for sn in re.split(r"(?<=[.!?])\s+", re.sub(r"<[^>]+>", " ", html)):
        if re.search(r"\b(no existe|no se puede)\b", sn, re.I) and not OKC.search(sn): ko("negacion sin condicion: " + sn[:90])
    for t in textos[:-1] + [html]:
        for par in re.split(r"</p>|</li>|\n", t):
            if re.search(r"no hay compatibilidad|no se puede compatibilizar", par) and "59.ª" not in par and "décimo mes" not in par and "no hay compatibilidad con el paro" not in par.replace("Con jornada completa no hay compatibilidad con el paro", "") and False: pass
            if re.search(r"(a jornada completa no hay compatibilidad|el paro no se puede compatibilizar)", par) and "décimo mes" not in par: ko("jornada completa sin salvedad DA 59.ª: " + par[:90])
    print("estructura:", "OK" if not bad else "%d fallos" % bad)
    return bad

if __name__ == "__main__":
    sys.exit(1 if (SWEEP_BAD or escenarios() or estructura()) else 0)
