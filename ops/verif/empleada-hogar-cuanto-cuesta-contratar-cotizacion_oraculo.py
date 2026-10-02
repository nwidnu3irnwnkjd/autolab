#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para empleada-hogar-cuanto-cuesta-contratar-cotizacion. Escrito desde la norma ANTES del .js.
INTERPRETACION (BOE consolidado leido el 2/10/2026):
 - Base de cotizacion (Orden PJC/297/2026 art. 15.1): retribucion mensual + prorrata de pagas extra -> escala de 7 tramos (<=329 -> 306; <=510 -> 436; <=693 -> 602; <=877 -> 785; <=1061 -> 970; <=1242 -> 1151;
   <=1424,40 -> 1424,40) y 8.º tramo desde 1424,41: base = retribucion mensual (tope maximo 5101,20, art. 2.1). Misma base para AT/EP, desempleo y Fogasa (arts. 15.4 y 35).
 - Tipos a cargo del empleador: CC 23,60 (art. 15.3); MEI 0,75 (art. 16); AT/EP 1,50 (DA 61.ª LGSS, CNAE 97: IT 0,80 + IMS 0,70); desempleo 5,50 indefinido / 6,70 temporal; Fogasa 0,20 (art. 35).
   A cargo de la empleada: CC 4,70; MEI 0,15; desempleo 1,55 / 1,60. Sin formacion profesional (art. 35 no la incluye).
 - RDL 16/2022 DA 1.ª.1: reduccion del 20 % de la aportacion empresarial por CC y bonificacion del 80 % del desempleo y Fogasa del empleador. DA 1.ª.2: ALTERNATIVA a la reduccion (45/30 % por renta, sin reglamento).
   RDL 1/2023 DA 3.ª bis: 45 % de las cuotas del empleador por cuidadora de familia numerosa (hasta el desarrollo reglamentario); RDL 16/2022 DT 3.ª: incompatible con el 20 %, no con el 80 % (supuesto propio: el 45 % solo sobre CC, el MEI no se reduce).
 - Salario minimo (RD 126/2026): por horas externa 9,55 EUR/h todo incluido (art. 4.2); mensual: 17.094 EUR/ano (1.221 x 14) para 40 h/semana (RD 1620/2011 arts. 8.1 y 9.1), a prorrata de la jornada.
   Horas al mes = horas/semana x 52 / 12 (supuesto propio). Pagas extra: 2, de una mensualidad cada una (supuesto propio, art. 8.4 deja la cuantia a las partes).
 - Art. 15.2 de la Orden: la base no puede ser inferior a la del tramo que corresponde al SMI equivalente (jornada completa, parcial mensual o por horas): base = max(tramo de la retribucion, tramo del minimo).
 - Imposibles: jornada > 40 h/semana (art. 9.1: lo demas son horas extra o presencia), horas <= 0, importe <= 0, meses fuera de 1-12.
Uso: python3 ops/verif/empleada-hogar-cuanto-cuesta-contratar-cotizacion_oraculo.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "empleada-hogar-cuanto-cuesta-contratar-cotizacion"
ESCALA = [(329.00, 306.00), (510.00, 436.00), (693.00, 602.00), (877.00, 785.00), (1061.00, 970.00), (1242.00, 1151.00), (1424.40, 1424.40)]
def base_de(ret):
    ret = round(ret, 2)
    for lim, b in ESCALA:
        if ret <= lim: return b
    return min(ret, 5101.20)
def tramo_de(ret):
    ret = round(ret, 2)
    for i, (lim, b) in enumerate(ESCALA):
        if ret <= lim: return i + 1
    return 8

def model(c):
    modo, h, imp, pagas, fam, meses, tipo = c["modo"], c["horas"], c["importe"], c["pagas"], c["fam"], c["meses"], c["tipo"]
    if h <= 0 or h > 40: return {"bloqueo": 1}
    if imp <= 0: return {"bloqueo": 2}
    if meses < 1 or meses > 12: return {"bloqueo": 3}
    hm = h * 52 / 12
    if modo == "horas":
        ret = imp * hm; minMes = 9.55 * hm; minHora = 9.55; cumple = round(imp, 2) >= 9.55
    else:
        ret = imp * (14 / 12 if pagas == "14" else 1)
        minMes = 17094 / 12 * h / 40; minHora = minMes / hm; cumple = round(ret, 2) >= round(minMes, 2)
    b = max(base_de(ret), base_de(minMes))  # art. 15.2: la base no puede ser inferior a la del tramo del SMI equivalente
    pct = 45 if fam == "si" else 20
    cc = b * 23.60 / 100; rcc = cc * pct / 100
    mei = b * 0.75 / 100; atep = b * 1.50 / 100
    des = b * (6.70 if tipo == "temporal" else 5.50) / 100; fog = b * 0.20 / 100
    bdes = (des + fog) * 0.80
    emp = cc - rcc + mei + atep + des + fog - bdes
    sin = cc + mei + atep + des + fog
    trab = b * (4.70 + 0.15 + (1.60 if tipo == "temporal" else 1.55)) / 100
    coste = ret + emp
    return {"bloqueo": 0, "retMes": ret, "base": b, "tramo": tramo_de(ret), "cuotaEmp": emp, "cuotaSin": sin, "ahorroMes": sin - emp, "cuotaTrab": trab,
            "costeMes": coste, "costeTotal": coste * meses, "netoMes": ret - trab, "minMes": minMes, "minHora": minHora, "cumple": int(cumple), "horasMes": hm, "costeHora": coste / hm,
            "difMin": ret - minMes, "pctEmp": emp / b * 100}
KEYS = ["retMes", "base", "tramo", "cuotaEmp", "cuotaSin", "ahorroMes", "cuotaTrab", "costeMes", "costeTotal", "netoMes", "minMes", "minHora", "cumple", "horasMes", "costeHora", "difMin", "pctEmp"]
BASE = dict(modo="horas", horas=20, importe=10, pagas="prorr", fam="no", meses=12, tipo="indef")
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto: 20 h, 10 EUR/h", V()),
 ("2 por horas en el minimo 9,55", V(importe=9.55)),
 ("3 por horas 9,54: no cumple", V(importe=9.54)),
 ("4 mensual 40 h, 1.424,50 (minimo prorr)", V(modo="mensual", horas=40, importe=1424.50)),
 ("5 mensual 14 pagas 40 h, 1.221", V(modo="mensual", horas=40, importe=1221, pagas="14")),
 ("6 familia numerosa", V(fam="si", modo="mensual", horas=30, importe=1100)),
 ("7 temporal", V(tipo="temporal")),
 ("8 tramo 1 limite 329", V(modo="mensual", horas=10, importe=329)),
 ("9 tramo 1->2 329,01", V(modo="mensual", horas=10, importe=329.01)),
 ("10 limite 510 / 510,01", V(modo="mensual", horas=10, importe=510.01)),
 ("11 limite 693", V(modo="mensual", horas=10, importe=693)),
 ("12 693,01", V(modo="mensual", horas=10, importe=693.01)),
 ("13 877", V(modo="mensual", horas=10, importe=877)),
 ("14 877,01", V(modo="mensual", horas=10, importe=877.01)),
 ("15 1061 / 1061,01", V(modo="mensual", horas=10, importe=1061.01)),
 ("16 1242", V(modo="mensual", horas=10, importe=1242)),
 ("17 1242,01", V(modo="mensual", horas=10, importe=1242.01)),
 ("18 1424,40 / 1424,41", V(modo="mensual", horas=10, importe=1424.41)),
 ("19 horas 41 bloqueo", V(horas=41)),
 ("20 meses 6", V(meses=6)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

def main():
    rnd = random.Random(41)
    sweep = []
    edges = [329, 329.01, 510, 510.01, 693, 693.01, 877, 877.01, 1061, 1061.01, 1242, 1242.01, 1424.40, 1424.41, 5101.20, 6000]
    for _ in range(700):
        modo = rnd.choice(["horas", "mensual", "mensual"])
        if modo == "horas": imp = rnd.choice([9.54, 9.55, 9.56, rnd.uniform(5, 30)])
        else: imp = rnd.choice(edges + [rnd.uniform(100, 3000)])
        sweep.append(dict(modo=modo, horas=rnd.choice([0, 1, 10, 20, 40, 41, rnd.uniform(1, 40)]), importe=round(imp, 2), pagas=rnd.choice(["prorr", "14"]), fam=rnd.choice(["si", "no"]),
                          meses=rnd.choice([0, 1, 6, 12, 13, rnd.randint(1, 12)]), tipo=rnd.choice(["indef", "temporal"])))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS:
            v = j.get(k)
            tol = 0.01 if k in ("tramo", "cumple") else 1
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > tol: print("DIF", c, k, v, o[k]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("retMes", "base", "cuotaEmp", "costeMes", "cumple") if k in o})
    print("barrido %d + %d fijos: %d discrepancias" % (len(sweep), len(CASES), bad))
    return bad

# ---- Escenarios de texto: pagina entera con DOM/EM simulados; comprueba que el veredicto no se contradice ----
def escenarios():
    stub = """var __out = null, __v = {};
function __num(x, d) { d = d || 0; x = +x; var s = Math.abs(x).toFixed(d), p = s.split("."); return (x < 0 ? "-" : "") + p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".") + (p[1] ? "," + p[1] : ""); }
var EM = { num: __num, eur: function (x, d) { return __num(x, d) + "\\u00a0\\u20ac"; }, renderResult: function (o) { __out = o; }, live: function () {} };
var document = { getElementById: function (id) { return { value: __v[id], addEventListener: function () {} }; } };
"""
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read()
    esc = [
     ("defecto: cumple el minimo", V(), ["cumples el mínimo", "9,55", "1.041,49"], ["no llegas", "por debajo"]),
     ("por debajo del minimo", V(importe=8), ["no llegas al mínimo", "9,55"], ["cumples el mínimo"]),
     ("familia numerosa cuidadora", V(fam="si"), ["45 %"], ["reducción del 20 %"]),
     ("mensual 14 pagas", V(modo="mensual", importe=900, pagas="14", horas=30), ["mínimo"], ["por hora trabajada, todo incluido"]),
    ]
    bad = 0
    for nombre, v, debe, no_debe in esc:
        h = stub + "__v = " + json.dumps(v) + ";\n" + src.replace('document.getElementById("go").addEventListener("click", pintar);', "pintar();").split("document.getElementById(\"f\").addEventListener")[0] + "\nJSON.stringify({v: __out.verdict, n: __out.note || \"\"});"
        out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
        if out.returncode: print("ERROR escenario", nombre, out.stderr[:400]); bad += 1; continue
        r = json.loads(out.stdout); txt = r["v"] + " " + r["n"]
        for s in debe:
            if s not in txt: print("FALTA en '%s': %s" % (nombre, s)); bad += 1
        for s in no_debe:
            if s in r["v"]: print("SOBRA en veredicto '%s': %s" % (nombre, s)); bad += 1
        print("escenario", nombre, "->", r["v"][:160])
    return bad

if __name__ == "__main__":
    b = main()
    if "--sin-escenarios" not in sys.argv: b += escenarios()
    sys.exit(1 if b else 0)
