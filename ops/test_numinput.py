#!/usr/bin/env python3
"""Test de los campos numéricos (type=text, data-n): normalización de em.js + data-dec en el HTML generado.
1) Extrae el getter de `value` de assets/em.js (misma lógica, no copia) y lo ejecuta con JavaScriptCore.
2) Todo input no-select con step<1 en calcs/*.json lleva data-dec en dist/embed/<slug>/index.html.
3) Ningún default con patrón de miles (p. ej. 3.247) en un campo sin data-dec (bloqueante); otros decimales sin data-dec solo avisan.
Requiere build previo de projects/decidir. Salida 1 si falla (bloqueante en check.py)."""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "projects", "decidir")
fails = []
# 1) getter
em = open(os.path.join(P, "assets", "em.js")).read()
m = re.search(r"get: function \(\) \{ var s = VD\.get\.call\(i\);(.*?) \},\s*\n\s*set: function", em, re.S)
if not m: print("✗ test_numinput: no encuentro el getter de value en em.js (¿cambió la estructura?)"); sys.exit(1)
body = m.group(1)
CASES = [("3.248", 1, "3.248"), ("3,248", 1, "3.248"), ("150.000", 0, "150000"), ("1.234,5", 0, "1234.5"),
         ("1.234,5", 1, "1234.5"), ("2,76", 1, "2.76"), ("3.248", 0, "3248"), ("2.76", 0, "2.76"), ("150000", 0, "150000"),
         ("-1.500", 0, "-1500"), (" 1 234 ", 0, "1234"), ("0.5", 0, "0.5")]
js = ("function g(raw,dec){var VD={get:{call:function(){return raw;}}};var i={_u:1,hasAttribute:function(a){return a==='data-dec'&&dec;}};"
      "return (function(){var s=VD.get.call(i);" + body + "})();}\n"
      "JSON.stringify(" + json.dumps(CASES) + ".map(function(c){return g(c[0],!!c[1]);}));")
r = subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True)
if r.returncode != 0: print("✗ test_numinput: error JS:", r.stderr.strip()); sys.exit(1)
for (raw, dec, exp), got in zip(CASES, json.loads(r.stdout.strip())):
    if got != exp: fails.append(f"normalización «{raw}» ({'data-dec' if dec else 'entero'}) → {got!r}, esperado {exp!r}")
# 2) y 3) HTML
n = 0; avisos = []
# Campos con default de 2 decimales y step >= 1 (euros enteros) SIN data-dec a propósito: ui.py solo pone data-dec con step<1.
# Con data-dec, «5.101» (miles escrito a la española) se leería como 5,101; sin él se lee 5101. El default 205.88 / 5101.2 no
# tiene 3 decimales, así que no se confunde con miles. No se cambia el HTML ni el resultado.
SIN_DEC_OK = {"capitalizar-paro-o-cobrarlo/cuota", "nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad/base27"}
cd = os.path.join(P, "calcs")
for f in sorted(os.listdir(cd)):
    if not f.endswith(".json") or f.endswith(".test.json"): continue
    c = json.load(open(os.path.join(cd, f))); slug = c["slug"]
    pg = os.path.join(P, "dist", "embed", slug, "index.html")
    if not os.path.exists(pg): fails.append(f"{slug}: falta dist/embed (¿build previo?)"); continue
    tags = {t.group(1): t.group(0) for t in re.finditer(r'<input id="([^"]+)"[^>]*data-n[^>]*>', open(pg).read())}
    for i in c["inputs"]:
        if i.get("type") == "select": continue
        t = tags.get(i["id"]); n += 1
        if t is None: fails.append(f"{slug}/{i['id']}: input sin data-n en el HTML"); continue
        dec = " data-dec" in t
        if float(i.get("step", 1) or 1) < 1 and not dec: fails.append(f"{slug}/{i['id']}: step<1 sin data-dec")
        v = re.search(r'value="([^"]*)"', t).group(1)
        if re.search(r"\.\d", v) and not dec:
            if re.match(r"^-?[1-9]\d{0,2}(\.\d{3})+$", v): fails.append(f"{slug}/{i['id']}: default {v} sin data-dec se leería como miles")
            elif f"{slug}/{i['id']}" in SIN_DEC_OK: pass
            else: avisos.append(f"{slug}/{i['id']}: default decimal {v} sin data-dec (inocuo hoy: no tiene 3 decimales)")
print(f"{'✗' if fails else 'OK'} test_numinput: {len(CASES)} casos de normalización, {n} campos revisados")
for x in avisos: print("  aviso:", x)
for x in fails: print("  ✗", x)
sys.exit(1 if fails else 0)
