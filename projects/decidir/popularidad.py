"""Bucle de popularidad (Constructor): lee data/popularidad.json (lo escribe ops/popularidad.py) y solo lee; sin datos o con datos
insuficientes usa un orden editorial fijo, y el build funciona igual (también en GitHub Actions, donde no hay credenciales)."""
import json, os, html
ROOT = os.path.dirname(os.path.abspath(__file__))
e = html.escape
EDITORIAL = ["sueldo-bruto-a-neto-2026", "alquilar-o-comprar", "hipoteca-fija-o-variable", "capitalizar-paro-o-cobrarlo", "actualizacion-renta-alquiler-irav-ipc"]  # más buscadas (ops/OPTIMIZACION.md, demanda)
try: D = json.load(open(os.path.join(ROOT, "data/popularidad.json")))
except Exception: D = {}
OK = bool(D.get("suficiente"))
def short(c): return c["h1"].split(":")[0].strip()
def ranked(kind="calculadoras"):
    """Slugs por popularidad real (si hay datos suficientes), si no vacío."""
    return [x["slug"] for x in D.get("ranking", {}).get(kind, [])] if OK else []
def order_calcs(calcs):
    """Slugs ordenados: popularidad real, o el orden editorial."""
    return ranked() or list(EDITORIAL)
def _by(calcs): return {c["slug"]: c for c in calcs}

def home_block(calcs):
    """«Lo más usado» (4-6, con datos suficientes) o «Empieza por aquí» (5 más buscadas). Enlace directo a cada calculadora."""
    by = _by(calcs); slugs = [s for s in order_calcs(calcs) if s in by][:6]
    if len(slugs) < 4: return ""
    lis = "".join(f'<li><a href="/decidir/{s}/">{e(short(by[s]))}</a></li>' for s in slugs)
    if OK: h, sub = "Lo más usado", "Las calculadoras que más usan nuestros lectores estas semanas."
    else: h, sub = "Empieza por aquí", "Calcula en 1 minuto: las decisiones más buscadas, ya con un caso típico rellenado."
    return f'<h2 id="top">{h}</h2><p class="note">{sub}</p><ul class="guides">{lis}</ul>'

def order_hubs(active, calcs):
    """Reordena los hubs por popularidad (suma de score de sus calculadoras), conservando el orden si no hay datos o hay empate."""
    if not OK: return active
    sc = {x["slug"]: x["score"] for x in D["ranking"]["calculadoras"]}
    sc_h = {x["slug"]: x["score"] for x in D["ranking"]["hubs"]}
    def val(item):
        k, s = item
        return sum(sc.get(sl, 0) for _, sls in s["groups"] for sl in sls) + sc_h.get(s["path"].strip("/"), 0)
    items = sorted(active.items(), key=lambda it: -val(it))  # sorted es estable: los empates mantienen el orden original
    return dict(items)

def todas_block(calcs, li):
    """Sección «Más consultadas» al principio de /todas/ (li = directorio._li)."""
    by = _by(calcs); slugs = [s for s in order_calcs(calcs) if s in by][:8]
    if len(slugs) < 4: return ""
    return f'<section class="grp"><h2>Más consultadas</h2><ul class="guides">{"".join(li(f"/decidir/{s}/", by[s]["h1"], "", "mas consultadas populares") for s in slugs)}</ul></section>'

def otros_block(slug, calcs, tema, exclude=()):
    """«Otros también usan»: 2-3 calculadoras populares (mismo tema primero) que no estén ya en las relacionadas. ≤ 3 enlaces."""
    by = _by(calcs); me = by.get(slug)
    if not me: return ""
    cand = [s for s in order_calcs(calcs) if s in by and s != slug and s not in exclude]
    cand.sort(key=lambda s: tema(by[s]) != tema(me))  # estable: dentro de cada grupo se mantiene el orden de popularidad
    cand = cand[:3]
    if len(cand) < 2: return ""
    return '<p class="note pop-link"><strong>Otros también usan:</strong> ' + " · ".join(f'<a href="/decidir/{s}/">{e(short(by[s]))}</a>' for s in cand) + "</p>"
