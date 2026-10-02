#!/usr/bin/env python3
"""Pruebas de pagina de finiquito-baja-voluntaria-vacaciones-preaviso (Constructor, 2026-10-02): absolutos, SEO, FAQ, inputs, componente EM y veredicto en 4 escenarios (pintar() con DOM/EM simulados en JavaScriptCore)."""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = "finiquito-baja-voluntaria-vacaciones-preaviso"; D = os.path.join(ROOT, "projects", "decidir")
j = json.load(open(f"{D}/calcs/{S}.json")); html = open(f"{D}/content/{S}.html").read(); src = open(f"{D}/calcs/{S}.js").read()
bad = []
def chk(c, m):
    if not c: bad.append(m)
chk(len(j["title"]) <= 60, "title > 60"); chk(len(j["description"]) <= 155, "description > 155"); chk(j["h1"] and j["lead"], "h1/lead")
chk(len(j["faqs"]) == 5, "faqs != 5"); chk(len(j["inputs"]) <= 8, "inputs > 8"); chk(j["tema"] in ("impuestos", "empleo"), "tema"); chk(j["veredicto"], "veredicto")
chk("boe.es" in j["sources"], "sources sin BOE")
for t in ("EM.renderResult", "EM.live", "EM.eur", "EM.num"): chk(t in src, "falta " + t)
chk(j["lead"].split(",")[0].lower().startswith("al irte"), "lead no responde primero")
txt = json.dumps(j, ensure_ascii=False) + html
for m in re.finditer(r"(?i)\b(siempre|nunca|garantiza\w*|solo tiene sentido|en todos los casos|cualquier)\b", txt): bad.append("absoluto: " + m.group(0))
# veredicto en 4 escenarios con DOM simulado
stub = """
var __r=null, __v={};
var document={getElementById:function(id){return {get value(){return __v[id];},set value(x){__v[id]=x;},addEventListener:function(){}};}};
var EM={eur:function(x){return Math.round(x).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')+' €';},num:function(x,n){return x.toFixed(n).replace('.',',');},renderResult:function(o){__r=o;},live:function(){}};
function go2(v){__v=v;pintar();return __r;}
"""
body = src.split('document.getElementById("go")')[0]
base = dict(bruto=24000, pagas="14", mes="10", dia=15, vacAnual=30, vacDisf=18, incumple=0, tipo=15)
esc = {1: dict(base, vacDisf=24, dia=15), 2: base, 3: dict(base, incumple=15), 4: dict(base, vacDisf=28)}
# escenario 1: vacaciones devengadas 23,67 -> disfrutadas 24 = exceso 0,33 < 0,5 (sin aviso) y pendientes 0
harness = stub + body + "\nJSON.stringify([1,2,3,4].map(function(k){var m=" + json.dumps({str(k): v for k, v in esc.items()}) + "[k];m=JSON.parse(JSON.stringify(m));return go2(m);}));"
o = subprocess.run(["osascript", "-l", "JavaScript", "-e", harness], capture_output=True, text=True)
if o.returncode: print(o.stderr); sys.exit(2)
rs = json.loads(o.stdout)
for k, r in zip((1, 2, 3, 4), rs):
    v = r["verdict"]; chk(r["winner"] == f"e{k}", f"escenario {k}: winner {r['winner']}")
    has_pre = "preaviso" in v and "descontar" in v; has_pag = "Te pagan" in v; has_exc = "más de los devengados" in v
    chk(has_pre == (k == 3), f"esc {k}: preaviso en veredicto = {has_pre}")
    chk(has_pag == (k in (2, 3)), f"esc {k}: 'Te pagan' = {has_pag}")
    chk(has_exc == (k == 4), f"esc {k}: exceso = {has_exc}")
    chk(("No hay vacaciones pendientes" in v) == (k == 1), f"esc {k}: 'no hay pendientes'")
    chk("netos" in v, f"esc {k}: sin neto")
    print(k, r["tone"], v[:160].replace("\n", " "), "...")
print("FALLOS:" if bad else "OK: pagina y veredicto sin contradicciones (4 escenarios)", *bad, sep="\n" if bad else " ")
sys.exit(1 if bad else 0)
