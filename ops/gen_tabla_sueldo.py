#!/usr/bin/env python3
"""Tabla fija de sueldo-bruto-a-neto-2026 (acción #5 de OPTIMIZACION.md): bruto por paga de 1.200 a 4.000 € en 12 y 14 pagas.
Ejecuta htmlTabla()/tablaSueldo() REALES de calcs/sueldo-bruto-a-neto-2026.js con JavaScriptCore (osascript, como ops/check.py y gen_ejemplos.py)
con las hipótesis de la tabla (params.sueldo_bruto_neto_2026.tabla_nota: indefinido, Madrid, sin hijos) y escribe:
  - projects/decidir/data/tabla_sueldo.json (filas numéricas + hipótesis)
  - las filas <tr id="bruto-N"> en content/sueldo-bruto-a-neto-2026.html entre <!--TABLA-SUELDO--> y <!--/TABLA-SUELDO--> (el build no ejecuta JS ni osascript).
Uso:  python3 ops/gen_tabla_sueldo.py          escribe ambos
      python3 ops/gen_tabla_sueldo.py --check  exige que JSON y HTML vigentes coincidan con la calculadora (sin osascript, se salta)
Solo stdlib. Sin red. Sin cifras legales nuevas."""
import json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "projects", "decidir")
SLUG = "sueldo-bruto-a-neto-2026"
HTML = os.path.join(PDIR, "content", SLUG + ".html")
OUT = os.path.join(PDIR, "data", "tabla_sueldo.json")
HIP = {"contrato": "indef", "ccaa": "madrid", "hijos": 0, "menores3": 0}
INI, FIN = "<!--TABLA-SUELDO-->", "<!--/TABLA-SUELDO-->"

def ejecutar():
    js = open(os.path.join(PDIR, "calcs", SLUG + ".js"), encoding="utf-8").read().split("function eur(")[0]
    em = open(os.path.join(PDIR, "assets", "em.js"), encoding="utf-8").read()
    m = re.search(r"function num\(x, d\) \{.*?\n  \}\n", em, re.S)
    prelude = "var EM = {};\n" + m.group(0) + "EM.num = num;\n"
    h = prelude + js + "\nJSON.stringify({filas: tablaSueldo(" + json.dumps(HIP) + "), html: htmlTabla(" + json.dumps(HIP) + ")});"
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if o.returncode != 0: raise RuntimeError("error JS: " + o.stderr.strip())
    r = json.loads(o.stdout.strip())
    r["filas"] = [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in f.items()} for f in r["filas"]]
    return r

def main():
    if not shutil.which("osascript"):
        print("gen_tabla_sueldo: sin osascript (no es macOS): se salta"); return 0
    r = ejecutar(); datos = {"slug": SLUG, "hipotesis": HIP, "filas": r["filas"]}
    html = open(HTML, encoding="utf-8").read() if os.path.exists(HTML) else ""
    if INI not in html or FIN not in html:
        print(f"✗ tabla sueldo: faltan los marcadores {INI} ... {FIN} en content/{SLUG}.html"); return 1
    nuevo = html.split(INI)[0] + INI + '<tbody id="tabla-sueldo-cuerpo">' + r["html"] + "</tbody>" + FIN + html.split(FIN, 1)[1]
    if "--check" in sys.argv:
        try: cur = json.load(open(OUT, encoding="utf-8"))
        except Exception: print("✗ tabla sueldo: falta data/tabla_sueldo.json (python3 ops/gen_tabla_sueldo.py)"); return 1
        if cur != json.loads(json.dumps(datos)) or nuevo != html:
            print("✗ tabla sueldo: no coincide con la calculadora (regenera con python3 ops/gen_tabla_sueldo.py)"); return 1
        print(f"OK: tabla de sueldo bruto a neto ({len(datos['filas'])} filas) coincide con la calculadora"); return 0
    json.dump(datos, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(OUT, "a").write("\n")
    open(HTML, "w", encoding="utf-8").write(nuevo)
    for f in datos["filas"]:
        if f["m"] in (1200, 1800, 2000, 4000): print(f)
    return 0

if __name__ == "__main__":
    sys.exit(main())
