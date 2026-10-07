#!/usr/bin/env python3
"""Genera projects/decidir/data/tablas_respuesta.json: 4 tablas de respuesta para la cola numérica (acción #4 de OPTIMIZACION.md).
Cada celda sale del calcular() REAL de calcs/<slug>.js (JavaScriptCore vía osascript, como ops/gen_ejemplos.py) con entradas fijas.
El Euríbor se fija aquí con su fecha (valor de data/live.json el día del cálculo, copiado al JSON): no cambia solo.
El build (projects/decidir/respuestas.py, también en GitHub Actions) solo LEE el JSON: no necesita osascript.
Uso:  python3 ops/gen_tablas_respuesta.py          escribe data/tablas_respuesta.json
      python3 ops/gen_tablas_respuesta.py --check  recalcula y exige que el JSON vigente coincida (lo llama ops/check.py); sin osascript, se salta
Solo stdlib. Sin red. Sin cifras legales nuevas: solo las funciones y parámetros ya verificados de cada calculadora."""
import datetime, json, math, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "projects", "decidir")
OUT = os.path.join(PDIR, "data", "tablas_respuesta.json")
LIVE = os.path.join(PDIR, "data", "live.json")

def _r(x, d=0):
    q = 10 ** d
    return math.floor(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)
def num(x, d=0):
    s = f"{abs(_r(x, d)):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if _r(x, d) < 0 else "") + s
def eur(x, d=0): return num(x, d) + " €"

def ejecutar(slug, lista):
    """calcular() real del .js para cada entrada de la lista (funciones puras antes de 'function eur(')."""
    js = open(os.path.join(PDIR, "calcs", slug + ".js"), encoding="utf-8").read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + f"\nJSON.stringify({json.dumps(lista)}.map(function (d) {{ return calcular(d); }}));"], capture_output=True, text=True)
    if o.returncode != 0: raise RuntimeError(f"{slug}: error JS: {o.stderr.strip()}")
    return json.loads(o.stdout.strip())

FIJO = None  # (valor, periodo, url) fijado en el JSON vigente cuando se usa --check
def euribor():
    if FIJO: return FIJO
    d = json.load(open(LIVE, encoding="utf-8"))["datos"]["euribor12m"]
    return d["valor"], d["extra"]["periodo"], d["fuente"]["url"]

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def t_paro():
    bases = list(range(1000, 3001, 200))
    base = dict(extras="si", jornada=100, dias=720)
    sin = ejecutar("cuanto-cobro-de-paro-prestacion-desempleo", [dict(base, base=b, hijos=0) for b in bases])
    con = ejecutar("cuanto-cobro-de-paro-prestacion-desempleo", [dict(base, base=b, hijos=1) for b in bases])
    rows = [dict(ancla=f"nomina-{b}", celdas=[eur(b), f"{eur(s['m1'])} · {eur(s['m2'])}", f"{eur(c['m1'])} · {eur(c['m2'])}"]) for b, s, c in zip(bases, sin, con)]
    return dict(slug="cuanto-cobro-de-paro-prestacion-desempleo", id="tabla-paro",
        h3="¿Cuánto cobro de paro con una nómina de 1.800 €?",
        condiciones="Cuantía mensual bruta de la prestación contributiva con 720 días cotizados (240 días de prestación, 8 meses), jornada completa y una base de cotización igual a la nómina bruta mensual con las pagas extra prorrateadas (sin horas extra). Se muestran los primeros 180 días (70 %) y el resto (60 %), con el máximo y el mínimo de 2026 según hijos a cargo; antes de IRPF. «Nómina» es aquí la base de cotización con las pagas extra prorrateadas: quien cobra 1.800 € en 14 pagas tiene una base de 2.100 € y le salen 1.225 € en los dos tramos.",
        cols=["Nómina (base, con pagas prorrateadas)", "Sin hijos: días 1-180 · después", "1 hijo: días 1-180 · después"], rows=rows,
        fuentes=[["LGSS, arts. 269 y 270 (BOE)", "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724"], ["Cuantías 2026 del SEPE", "https://www.sepe.es/HomeSepe/en/prestaciones-desempleo/Cuantias-anuales.html"]],
        inputs=dict(base=bases, extras="si", jornada=100, dias=720, hijos=[0, 1]))

def t_casa():
    precios = list(range(100000, 500001, 50000))
    base = dict(tipo="usada", entrada=20, gastos=2500, anos=5, rentab=0, interes=4.247)
    ccs = [("madrid", "Madrid"), ("andalucia", "Andalucía"), ("cataluna", "Cataluña")]
    res = {k: ejecutar("cuanto-ahorrar-para-comprar-casa", [dict(base, precio=p, ccaa=k) for p in precios]) for k, _ in ccs}
    rows = [dict(ancla=f"casa-{p}", celdas=[eur(p), eur(res["madrid"][i]["entrada"])] + [eur(res[k][i]["totalNecesario"]) for k, _ in ccs]) for i, p in enumerate(precios)]
    return dict(slug="cuanto-ahorrar-para-comprar-casa", id="tabla-casa",
        h3="¿Cuánto dinero necesito para comprar una casa de 250.000 €?",
        condiciones="Vivienda usada, con entrada del 20 %, 2.500 € de gastos (notaría, registro, gestoría y tasación) y el ITP con el tipo general de cada comunidad (Madrid 6 %, Andalucía 7 %, Cataluña 10 % por debajo de 600.000 €), sin tipos reducidos. El total es entrada + ITP + gastos; la hipoteca cubre el resto del precio.",
        cols=["Precio", "Entrada (20 %)", "Total en Madrid", "Total en Andalucía", "Total en Cataluña"], rows=rows,
        fuentes=[["ITP y AJD (BOE)", "https://www.boe.es/buscar/act.php?id=BOE-A-1993-25359"], ["Normas autonómicas, en «Supuestos y fuentes»", "#supuestos-y-fuentes"]],
        inputs=dict(precio=precios, ccaa=[k for k, _ in ccs], **base))

def t_hipoteca(fecha):
    eur12, periodo, url = euribor()
    tin = round(eur12 + 0.8, 3)
    caps = [100000, 150000, 200000, 250000, 300000]
    res = ejecutar("hipoteca-20-25-o-30-anos-cuota-vs-intereses", [dict(capital=c, tin=tin, ingresos=3500, otras=0, tope=35) for c in caps])
    rows = [dict(ancla=f"hipoteca-{c}", celdas=[eur(c)] + [f"{eur(r['cuota' + str(y)])} · {eur(r['int' + str(y)])}" for y in (20, 25, 30)]) for c, r in zip(caps, res)]
    y, m = periodo.split("-")
    return dict(slug="hipoteca-20-25-o-30-anos-cuota-vs-intereses", id="tabla-hipoteca",
        h3="¿Cuánto pago de hipoteca al mes por 150.000 € a 25 años?",
        condiciones=f"Cuota mensual · intereses totales con un tipo del {num(tin, 3)} % (Euríbor a 12 meses de {num(eur12, 3)} %, media de {MESES[int(m) - 1]} de {y} del BCE, más 0,8 puntos de diferencial supuesto; Euríbor fijado el {fecha}). Sistema francés, sin bonificaciones ni comisiones; la cuota real variará con las revisiones del Euríbor.",
        cols=["Capital", "20 años", "25 años", "30 años"], rows=rows,
        fuentes=[["Euríbor a 12 meses, BCE", url]], inputs=dict(capital=caps, tin=tin, euribor=eur12, euribor_periodo=periodo, diferencial=0.8))

def t_loteria():
    premios = [100, 1000, 10000, 20000, 40000, 50000, 75000, 100000]
    res = ejecutar("loteria-navidad-premio-neto-hacienda", [dict(premio=p, decimos=1, personas=1, cobro="uno") for p in premios])
    rows = [dict(ancla=f"premio-{p}", celdas=[eur(p), eur(r["exentoDecimo"]), eur(r["retDecimo"]), eur(r["netoDecimo"])]) for p, r in zip(premios, res)]
    return dict(slug="loteria-navidad-premio-neto-hacienda", id="tabla-premio",
        h3="¿Cuánto me queda de un premio de 50.000 € de la Lotería de Navidad?",
        condiciones="Premio íntegro de un décimo cobrado por una sola persona: los primeros 40.000 € están exentos y sobre el exceso Hacienda retiene el 20 % (gravamen especial, disposición adicional 33.ª de la Ley del IRPF). No incluye reparto entre varias personas, no residentes ni regímenes forales.",
        cols=["Premio por décimo", "Parte exenta", "Retención (20 % del exceso)", "Neto que cobras"], rows=rows,
        fuentes=[["Ley 35/2006 del IRPF, DA 33.ª (BOE)", "https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#datrigesimatercera"]], inputs=dict(premio=premios, decimos=1, personas=1))

def generar(fecha):
    out = {}
    for t in (t_paro(), t_casa(), t_hipoteca(fecha), t_loteria()):
        t["fecha"] = fecha; out[t["slug"]] = t
    return out

def main():
    check = "--check" in sys.argv
    if not shutil.which("osascript"):
        print("gen_tablas_respuesta: sin osascript (no es macOS): se salta"); return 0
    if check:
        try: cur = json.load(open(OUT, encoding="utf-8"))
        except Exception: print("✗ tablas_respuesta: falta data/tablas_respuesta.json (python3 ops/gen_tablas_respuesta.py)"); return 1
        global FIJO
        h = cur["hipoteca-20-25-o-30-anos-cuota-vs-intereses"]; FIJO = (h["inputs"]["euribor"], h["inputs"]["euribor_periodo"], h["fuentes"][0][1])
        malos = 0; nuevo = json.loads(json.dumps(generar(next(iter(cur.values()))["fecha"])))
        for slug, n in nuevo.items():
            if cur.get(slug) != n: print(f"✗ tablas_respuesta: {slug} no coincide con la calculadora (regenera con python3 ops/gen_tablas_respuesta.py)"); malos += 1
        print(f"{'OK' if not malos else 'FALLOS'}: tablas de respuesta {len(nuevo) - malos}/{len(nuevo)} coinciden con la calculadora"); return 1 if malos else 0
    out = generar(datetime.date.today().isoformat())
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(OUT, "a").write("\n")
    for s, v in out.items(): print(s, v["rows"][3]["celdas"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
