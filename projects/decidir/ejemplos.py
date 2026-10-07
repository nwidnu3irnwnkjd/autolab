"""«Ejemplo resuelto» de las calculadoras insignia, renderizado en el HTML estático (los rastreadores de IA no ejecutan JS).
Solo LEE data/ejemplos.json, generado en local por ops/gen_ejemplos.py (que ejecuta el calcular() real del .js con
JavaScriptCore). Así el build funciona también en GitHub Actions (Linux, sin osascript). Si falta el JSON o la calculadora, no hay bloque.
Revertir: quitar la llamada a ejemplos.* en build.py (render_calc y main)."""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE = "data/ejemplos.json"
try:
    DATA = json.load(open(os.path.join(ROOT, FILE), encoding="utf-8"))
except Exception:
    DATA = {}

def fecha_es(iso):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    y, m, d = iso.split("-"); return f"{int(d)} de {meses[int(m) - 1]} de {y}"

def block(slug):
    """HTML del bloque (bajo el lead); '' si la calculadora no tiene ejemplo."""
    e = DATA.get(slug)
    if not e: return casos(slug)
    rows = "".join(f'<tr><th scope="row">{html.escape(a)}</th><td>{html.escape(b)}</td></tr>' for a, b in e["filas"])
    return (f'<section class="ejemplo" id="ejemplo-resuelto"><h2>Ejemplo resuelto ({fecha_es(e["fecha"])})</h2>'
            f'<p>Entradas: {html.escape(e["entradas_texto"])}.</p><table><tbody>{rows}</tbody></table>'
            f'<p><strong>{html.escape(e["veredicto_texto"])}</strong></p></section>')

def casos(slug):
    """«Casos típicos» (2-3 casos con la calcular() real y entradas fijas; ops/gen_ejemplos.py CASOS). '' si no hay."""
    c = DATA.get("_casos", {}).get(slug)
    if not c: return ""
    lis = "".join(f'<li><strong>{html.escape(x["titulo"])}</strong>: {html.escape(x["texto"])}</li>' for x in c["casos"])
    return (f'<section class="ejemplo" id="casos-tipicos"><h2>Casos típicos ({fecha_es(c["fecha"])})</h2>'
            f'<p>Resultados de esta calculadora con estas entradas, a la fecha indicada; no son una predicción: cambia las tuyas más abajo.</p><ul>{lis}</ul></section>')

def apply(calcs):
    """Añade el veredicto numérico al `veredicto` en memoria (lo usan llms-full.txt y las versiones .md); no toca los JSON de calcs/."""
    for c in calcs:
        e = DATA.get(c["slug"])
        if e and e["veredicto_texto"] not in c.get("veredicto", ""):
            c["veredicto"] = (c.get("veredicto", "").rstrip() + " Ejemplo (" + fecha_es(e["fecha"]) + "): " + e["veredicto_texto"]).strip()
    return calcs
