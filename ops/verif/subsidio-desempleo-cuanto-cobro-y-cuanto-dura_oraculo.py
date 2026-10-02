#!/usr/bin/env python3
"""Oraculo independiente (Constructor Sonnet, 2026-10-02) para subsidio-desempleo-cuanto-cobro-y-cuanto-dura. Escrito desde la norma ANTES del .js.
INTERPRETACION (LGSS, RDL 8/2015, consolidado leido el 2/10/2026; arts. 274-278 y 280 en la redaccion del RDL 2/2024, vigente desde 23/5/2024; DT 1.ª del RDL 2/2024 agotada el 31/10/2024):
 - Art. 274.1.a: agotar la prestacion; si edad < 45 y sin responsabilidades familiares, la prestacion agotada debe haber durado >= 360 dias. 274.1.b: sin periodo para la prestacion y >= 90 dias cotizados.
 - Art. 274.2: carecer de rentas propias O (alternativa) acreditar responsabilidades familiares. 275.1: rentas propias del mes anterior <= 75 % del SMI sin pagas (1.221 x 0,75 = 915,75).
   275.2: familiares = (rentas de la unidad familiar / miembros) <= 75 % SMI; unidad = solicitante + conyuge/pareja + hijos < 26 (275.3). Se exige al menos un miembro mas.
 - Art. 277.1 (agotado): sin cargas: < 45 y >= 360 dias de prestacion -> 6 meses; >= 45 y >= 120 -> 6 meses (la tabla dice «>45»; la edad exacta 45 se trata como >45: supuesto propio). Con cargas: >= 120 dias -> 24 meses; >= 180 -> 30.
 - Art. 277.2 (insuficiente): 90 dias -> 3 meses, 120 -> 4, 150 -> 5, 180 -> 6 sin cargas o 21 con cargas. >= 360 dias cotizados: hay prestacion contributiva (no hay subsidio por b).
 - Art. 278: 95 % IPREM dias 1-180, 90 % dias 181-360, 80 % desde el 361; IPREM 2026 = 600 -> 570 / 540 / 480. Mes = 30 dias (convencion del modelo).
 - Art. 280: >= 52 anos + requisitos de jubilacion salvo edad + 6 anos cotizados por desempleo + rentas PROPIAS <= 75 % SMI (no cuenta la familia); 80 % IPREM = 480; dura hasta la edad ordinaria
   de jubilacion (272.d por 280.6; 205.1.a: 67, o 65 con 38 anos y 6 meses): cotas 65 y 67 anos, edad en anos enteros.
 - Imposible: agotado con < 120 dias de prestacion (dato no valido); insuficiente con < 90 dias (sin derecho) o >= 360 (hay prestacion). Sin rentas ok: sin subsidio.
Uso: python3 ops/verif/subsidio-desempleo-cuanto-cobro-y-cuanto-dura_oraculo.py -> compara con el JS real (osascript) y sale 1 si hay diferencias."""
import json, os, subprocess, sys, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "subsidio-desempleo-cuanto-cobro-y-cuanto-dura"
IPREM_C = 60000                      # centimos
SMI_C = 122100
UMBRAL_C = SMI_C * 75 // 100         # 91575

def model(c):
    sit, dias, edad = c["situ"], int(round(c["dias"])), c["edad"]
    h = max(int(round(c["hijos"])), 0); conv = 1 if c["conyuge"] == "si" else 0
    if sit == "agotado" and dias < 120: return {"bloqueo": 1}
    if sit == "insuf" and dias < 90: return {"bloqueo": 2}
    if sit == "insuf" and dias >= 360: return {"bloqueo": 3}
    prop_c = round(c["renta"] * 100); fam_c = round((c["renta"] + c["rentaOtros"]) * 100)
    miembros = 1 + conv + h
    prop_ok = prop_c <= UMBRAL_C
    cargas = miembros > 1 and fam_c <= UMBRAL_C * miembros
    renta_ok = prop_ok or cargas
    r = {"bloqueo": 0, "rentaOk": int(renta_ok), "cargas": int(cargas), "miembros": miembros, "umbral": UMBRAL_C / 100}
    gen, motivo, meses = 0, 0, 0
    if not renta_ok: motivo = 1
    elif sit == "agotado":
        if edad < 45 and not cargas and dias < 360: motivo = 2
        else:
            gen = 1
            meses = (30 if dias >= 180 else 24) if cargas else 6
    else:
        gen = 1
        if dias < 120: meses = 3
        elif dias < 150: meses = 4
        elif dias < 180: meses = 5
        else: meses = 21 if cargas else 6
    r["gen"], r["motivo"], r["meses"] = gen, motivo, meses
    if gen:
        D = meses * 30
        t1 = min(D, 180); t2 = max(min(D, 360) - 180, 0); t3 = max(D - 360, 0)
        r["m1"], r["m2"], r["m3"] = IPREM_C * .95 / 100, IPREM_C * .90 / 100, IPREM_C * .80 / 100
        r["total"] = (r["m1"] * t1 + r["m2"] * t2 + r["m3"] * t3) / 30
        r["dur"] = D
    d52 = int(edad >= 52 and edad < 67 and c["jub"] == "si" and prop_ok)
    r["d52"] = d52
    if d52:
        r["m52"] = IPREM_C * .80 / 100
        r["meses52min"] = max(65 - edad, 0) * 12; r["meses52max"] = (67 - edad) * 12
        r["total52min"] = r["m52"] * r["meses52min"]; r["total52max"] = r["m52"] * r["meses52max"]
    return r

KEYS = ["rentaOk", "cargas", "miembros", "umbral", "gen", "motivo", "meses", "dur", "m1", "m2", "m3", "total", "d52", "m52", "meses52min", "meses52max", "total52min", "total52max"]
BASE = dict(situ="agotado", dias=360, edad=40, hijos=1, conyuge="no", renta=0, rentaOtros=0, jub="no")
def V(**k): x = dict(BASE); x.update(k); return x
CASES = [
 ("1 defecto: agotado 360 d, 40 anos, 1 hijo, sin rentas -> 30 meses", V()),
 ("2 sin cargas, 40 anos, 360 d -> 6 meses", V(hijos=0)),
 ("3 sin cargas, 40 anos, 359 d -> sin subsidio (motivo 2)", V(hijos=0, dias=359)),
 ("4 sin cargas, 45 anos, 120 d -> 6 meses", V(hijos=0, edad=45, dias=120)),
 ("5 cargas, 120 d -> 24 meses", V(dias=120)),
 ("6 cargas, 179 d -> 24; 180 d -> 30", V(dias=179)),
 ("7 renta propia = 915,75 exacta", V(hijos=0, renta=915.75)),
 ("8 renta propia 915,76 sin cargas -> no", V(hijos=0, renta=915.76)),
 ("9 renta propia 1.500, 1 hijo sin renta (per capita 750) -> cargas", V(renta=1500)),
 ("10 unidad 3 miembros: total 2.747,25 -> cargas; 2.747,26 -> no", V(hijos=1, conyuge="si", renta=1000, rentaOtros=1747.25)),
 ("11 idem +0,01", V(hijos=1, conyuge="si", renta=1000, rentaOtros=1747.26)),
 ("12 insuf 89 d -> bloqueo 2", V(situ="insuf", dias=89)),
 ("13 insuf 90 d -> 3 meses", V(situ="insuf", dias=90, hijos=0)),
 ("14 insuf 149 d -> 4; 150 -> 5; 179 -> 5", V(situ="insuf", dias=179, hijos=0)),
 ("15 insuf 180 d sin cargas -> 6; con cargas -> 21", V(situ="insuf", dias=180)),
 ("16 insuf 360 d -> bloqueo 3", V(situ="insuf", dias=360)),
 ("17 52+: 55 anos, jubilacion si, sin renta", V(edad=55, hijos=0, jub="si")),
 ("18 52 exactos y 51", V(edad=51, hijos=0, jub="si")),
 ("19 52+ con familia rica pero propia ok", V(edad=60, hijos=0, conyuge="si", renta=0, rentaOtros=5000, jub="si")),
 ("20 agotado 119 d -> bloqueo 1", V(dias=119)),
]
def js(cases):
    src = open(os.path.join(ROOT, "projects/decidir/calcs/%s.js" % SLUG)).read().split("function eur(")[0]
    h = src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: print(out.stderr); sys.exit(2)
    return json.loads(out.stdout)

if __name__ == "__main__":
    rnd = random.Random(23)
    def rent(): return rnd.choice([0, 0, 300, 915.75, 915.76, 915.74, 1000, 1500, 2747.25, 2747.26, rnd.uniform(0, 3000)])
    sweep = []
    for _ in range(700):
        s = rnd.choice(["agotado", "agotado", "insuf"])
        dias = rnd.choice([119, 120, 179, 180, 359, 360, rnd.randint(100, 800)]) if s == "agotado" else rnd.choice([89, 90, 119, 120, 149, 150, 179, 180, 359, 360, rnd.randint(50, 400)])
        sweep.append(dict(situ=s, dias=dias, edad=rnd.choice([18, 30, 44, 45, 46, 51, 52, 53, 60, 64, 65, 66, 67, 70, rnd.randint(18, 70)]), hijos=rnd.randint(0, 4),
                          conyuge=rnd.choice(["si", "no"]), renta=round(rent(), 2), rentaOtros=round(rent(), 2), jub=rnd.choice(["si", "no"])))
    allc = [c for _, c in CASES] + sweep
    jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        if j.get("bloqueo") != o["bloqueo"]: print("BLOQUEO", c, j.get("bloqueo"), o["bloqueo"]); bad += 1; continue
        if o["bloqueo"]: continue
        for k in KEYS:
            if k not in o:
                if j.get(k) not in (None, 0): print("EXTRA", c, k, j.get(k)); bad += 1
                continue
            v = j.get(k)
            if v is None or v != v or abs(v) == float("inf") or abs(v - o[k]) > (0.01 if k in ("rentaOk", "cargas", "miembros", "gen", "motivo", "meses", "dur", "d52") else 1): print("DIF", c, k, v, o[k]); bad += 1
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("gen", "motivo", "meses", "total", "d52") if k in o})
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
     ("default: derecho con cargas", dict(situ="agotado", dias=360, edad=40, hijos=1, conyuge="no", renta=0, rentaOtros=0, jub="no"),
      ["tendrías derecho al subsidio por responsabilidades familiares", "570", "540", "480", "30 meses", "15.300"], ["no tendrías derecho", "mayores de 52"]),
     ("renta superada: la opcion no existe", dict(situ="agotado", dias=360, edad=40, hijos=0, conyuge="no", renta=2000, rentaOtros=0, jub="no"),
      ["no tendrías derecho", "no existe si superas la renta", "915,75"], ["durante", "570"]),
     ("menor de 45 sin cargas con paro de 359 dias", dict(situ="agotado", dias=359, edad=40, hijos=0, conyuge="no", renta=0, rentaOtros=0, jub="no"),
      ["no tendrías derecho", "menos de 45 años", "359", "360"], ["15.300", "durante", "no existe si superas"]),
     ("mayor de 52 con requisitos de jubilacion", dict(situ="agotado", dias=360, edad=55, hijos=0, conyuge="no", renta=0, rentaOtros=0, jub="si"),
      ["tendrías derecho al subsidio para mayores de 52", "480", "57.600", "69.120", "no se cobra a la vez"], ["no tendrías derecho", "570", "6 meses"]),
    ]
    bad = 0
    for nombre, v, debe, no_debe in esc:
        h = stub + "__v = " + json.dumps(v) + ";\n" + src.replace('document.getElementById("go").addEventListener("click", pintar);', "pintar();").split("document.getElementById(\"f\").addEventListener")[0] + "\nJSON.stringify({v: __out.verdict, n: __out.note || \"\"});"
        out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
        if out.returncode: print("ERROR escenario", nombre, out.stderr[:400]); bad += 1; continue
        r = json.loads(out.stdout); t = r["v"].replace(" ", " ").replace("€", "€")
        for s in debe:
            if s not in t: print("FALTA", nombre, s, "|", t[:200]); bad += 1
        for s in no_debe:
            if s in t: print("SOBRA", nombre, s, "|", t[:200]); bad += 1
        print("escenario OK:" if not bad else "escenario:", nombre, "|", t[:140])
    return bad

if __name__ == "__main__":
    sys.exit(1 if (SWEEP_BAD or escenarios()) else 0)
