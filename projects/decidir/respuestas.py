"""Tablas de respuesta (acción #4 de OPTIMIZACION.md): cifras precalculadas con el calcular() real, renderizadas en el HTML estático.
Solo LEE data/tablas_respuesta.json (generado en local por ops/gen_tablas_respuesta.py); el build no necesita osascript.
Revertir: quitar la llamada a respuestas.block en build.py (render_calc)."""
import html, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
try:
    DATA = json.load(open(os.path.join(ROOT, "data/tablas_respuesta.json"), encoding="utf-8"))
except Exception:
    DATA = {}

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fecha_es(iso):
    y, m, d = iso.split("-"); return f"{int(d)} de {MESES[int(m) - 1]} de {y}"

def block(slug):
    t = DATA.get(slug)
    if not t: return ""
    e = html.escape
    head = "".join(f'<th scope="col">{e(c)}</th>' for c in t["cols"])
    rows = "".join(f'<tr id="{r["ancla"]}"><th scope="row">{e(r["celdas"][0])}</th>' + "".join(f"<td>{e(c)}</td>" for c in r["celdas"][1:]) + "</tr>" for r in t["rows"])
    src = " · ".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in t["fuentes"])
    return (f'<section class="respuestas" id="{t["id"]}"><h3>{e(t["h3"])}</h3><p class="note">{e(t["condiciones"])}</p>'
            f'<div class="em-tw"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="note">Calculado el {fecha_es(t["fecha"])} con esta misma calculadora. Fuente: {src}.</p></section>')
