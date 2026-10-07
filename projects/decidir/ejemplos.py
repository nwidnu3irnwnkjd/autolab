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

def _pub(t):
    """Texto público del veredicto: sin la nota interna «; cifras comprobadas con ops/verif/…»."""
    return re.sub(r";\s*cifras comprobadas con ops/verif/[\w.-]+\.py", "", t).strip()

def _split(t):
    """(frase_en_negrita ≤160 car., resto): la negrita solo cubre la primera frase; si es larga, se corta en el último «;»/«,» que quepa."""
    m = re.search(r"[.;:] ", t)
    first = t[:m.start() + 1] if m else t
    if len(first) <= 160: return first, t[len(first):]
    cut = max(first.rfind("; ", 0, 160), first.rfind(", ", 0, 160))
    if cut < 40: return "", t
    return t[:cut + 1], t[cut + 1:]

def _hash(inputs):
    """Enlace #v=id:valor~… (formato de em.js) para «Aplicar este caso»; vacío si no hay entradas."""
    if not inputs: return ""
    f = lambda v: (str(int(v)) if isinstance(v, float) and v == int(v) else str(v))
    return "#v=" + "~".join(f"{k}:{f(v)}" for k, v in inputs.items())

def _aplicar(inputs):
    h = _hash(inputs)
    return f' <a class="caso" href="{html.escape(h)}">Aplicar este caso</a>' if h else ""

def _vered(t):
    b, r = _split(_pub(t))
    return (f"<strong>{html.escape(b)}</strong>" if b else "") + html.escape(r)

def block(slug):
    """HTML del bloque (bajo el lead); '' si la calculadora no tiene ejemplo."""
    e = DATA.get(slug)
    if not e: return casos(slug)
    rows = "".join(f'<tr><th scope="row">{html.escape(a)}</th><td>{html.escape(b)}</td></tr>' for a, b in e["filas"])
    return (f'<section class="ejemplo" id="ejemplo-resuelto"><h2>Ejemplo resuelto ({fecha_es(e["fecha"])})</h2>'
            f'<p>Entradas: {html.escape(e["entradas_texto"])}.</p><table><tbody>{rows}</tbody></table>'
            f'<p>{_vered(e["veredicto_texto"])}{_aplicar(e.get("inputs"))}</p></section>')

def casos(slug):
    """«Casos típicos» (2-3 casos con la calcular() real y entradas fijas; ops/gen_ejemplos.py CASOS). '' si no hay."""
    c = DATA.get("_casos", {}).get(slug)
    if not c: return ""
    lis = "".join(f'<li><strong>{html.escape(x["titulo"])}</strong>: {html.escape(x["texto"])}{_aplicar(x.get("inputs"))}</li>' for x in c["casos"])
    return (f'<section class="ejemplo" id="casos-tipicos"><h2>Casos típicos ({fecha_es(c["fecha"])})</h2>'
            f'<p>Resultados de esta calculadora con estas entradas, a la fecha indicada; no son una predicción: cambia las tuyas arriba.</p><ul>{lis}</ul></section>')

def apply(calcs):
    """Añade el veredicto numérico al `veredicto` en memoria (lo usan llms-full.txt y las versiones .md); no toca los JSON de calcs/."""
    for c in calcs:
        e = DATA.get(c["slug"])
        if e and _pub(e["veredicto_texto"]) not in c.get("veredicto", ""):
            c["veredicto"] = (c.get("veredicto", "").rstrip() + " Ejemplo (" + fecha_es(e["fecha"]) + "): " + _pub(e["veredicto_texto"])).strip()
    return calcs
