#!/usr/bin/env python3
"""KPIs del PLAN-TRAFICO: añade una fila a journal/kpis.md (tabla acumulativa; una por hora, sin duplicar).
Uso: python3 ops/kpis.py [--dry]   Si una API falla, esa celda queda «n/d». No imprime ni guarda secretos."""
import sys, os, re, json, datetime, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gauth
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "journal/kpis.md")
site = json.load(open(os.path.join(ROOT, "projects/decidir/data/site.json")))
BASE = site["base_url"].rstrip("/"); host = BASE.split("//")[1]; pid = site.get("ga4_property_id")
SAMPLE = ["/", "/hipoteca/", "/impuestos/", "/coche/", "/guias/euribor-hipoteca/", "/guias/amortizacion-anticipada-comisiones/",
          "/guias/autonomo-2026-cuota-regularizacion-modulos/", "/decidir/alquilar-o-comprar/", "/decidir/amortizar-o-invertir/",
          "/decidir/autonomo-o-asalariado/", "/tablas-2026/", "/que-cambia-1-enero-2027/"]
EVENTS = ["share_click", "calc_used", "calendar_add", "asistente_paso", "asistente_resultado"]
ND = "n/d"
def safe(f):
    try: return f()
    except Exception: return ND
now = datetime.datetime.now(datetime.timezone.utc); stamp = now.strftime("%Y-%m-%d %H:00Z")
tok = safe(gauth.token)
def sitemap_urls():
    idx = urllib.request.urlopen(BASE + "/sitemap.xml", timeout=20).read().decode()
    n = 0
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        n += len(re.findall(r"<loc>", urllib.request.urlopen(sm, timeout=20).read().decode()))
    return n
def known():
    """Lee journal/inspeccion.json (ops/inspect_all.py, todas las URL del sitemap, 1 vez/20 h): «conocidas/total (indexadas)»."""
    d = json.load(open(os.path.join(ROOT, "journal/inspeccion.json")))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import inspect_all
    r = inspect_all.summary(d)
    return f"{r['conocidas']}/{r['total']} (idx {r['indexadas']})"
def gsc():
    q = gauth.post(f"https://www.googleapis.com/webmasters/v3/sites/sc-domain:{host}/searchAnalytics/query", tok,
        {"startDate": str(now.date() - datetime.timedelta(days=7)), "endDate": str(now.date())})
    r = q.get("rows", [])
    if not r: return 0, 0, "—"
    return int(r[0]["clicks"]), int(r[0]["impressions"]), f"{r[0]['position']:.1f}"
def ga(body): return gauth.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport", tok, body)
DR = [{"startDate": "7daysAgo", "endDate": "today"}]
def ga_tot():
    r = ga({"dateRanges": DR, "metrics": [{"name": "sessions"}, {"name": "activeUsers"}]}).get("rows", [])
    return (int(r[0]["metricValues"][0]["value"]), int(r[0]["metricValues"][1]["value"])) if r else (0, 0)
def ga_events():
    r = ga({"dateRanges": DR, "dimensions": [{"name": "eventName"}], "metrics": [{"name": "eventCount"}],
            "dimensionFilter": {"filter": {"fieldName": "eventName", "inListFilter": {"values": EVENTS}}}}).get("rows", [])
    d = {x["dimensionValues"][0]["value"]: int(x["metricValues"][0]["value"]) for x in r}
    return [d.get(e, 0) for e in EVENTS]
def ga_top():
    r = ga({"dateRanges": DR, "dimensions": [{"name": "pagePath"}], "metrics": [{"name": "screenPageViews"}], "limit": 5,
            "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}]}).get("rows", [])
    return "; ".join(f"{x['dimensionValues'][0]['value']} ({x['metricValues'][0]['value']})" for x in r) or "—"
n_sm = safe(sitemap_urls)
n_known = safe(known)
g = safe(gsc) if tok != ND else (ND,) * 3
sess = safe(ga_tot) if tok != ND and pid else (ND, ND)
ev = safe(ga_events) if tok != ND and pid else [ND] * 5
top = safe(ga_top) if tok != ND and pid else ND
HEAD = f"""# KPIs de tráfico (PLAN-TRAFICO) · una fila por ejecución (`python3 ops/kpis.py`, 1 vez por ciclo en close_cycle.sh)

**Regla de lectura.** Éxito de la semana 2 (16-oct-2026): **≥ 50 URLs conocidas/indexadas por Google** (con 12 URLs de muestra, «Conocidas» ≥ 12 de 12 y el sitemap procesado en Search Console equivale a ese umbral; hasta entonces, la tendencia de «Conocidas/12» es la señal) **y primeras impresiones** (Impr. 7d > 0). Si el 15-oct «Conocidas» sigue en 0: revisar propiedad y plan B.
Tendencia ↑ ↓ = compara «Conocidas», «Impr.» y «Sesiones» con la fila anterior (en ese orden). n/d = la API falló. Eventos 7 d: share_click / calc_used / calendar_add / asistente_paso / asistente_resultado (0 si aún no existen). «Sesiones» incluye tráfico propio (no separable).

| Fecha (UTC) | URLs sitemap | Conocidas /12 | Clics 7d | Impr. 7d | Pos. | Sesiones 7d | Usuarios 7d | share | calc | cal | as_paso | as_res | Top 5 páginas (vistas) | Tend. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
"""
lines = open(OUT, encoding="utf-8").read().split("\n") if os.path.exists(OUT) else []
rows = [l for l in lines if re.match(r"\| \d{4}-\d\d-\d\d ", l)]
if any(l.startswith(f"| {stamp} ") for l in rows): print(f"Ya hay fila para {stamp}; no se duplica."); sys.exit(0)
def arrow(a, b):
    try: return "↑" if float(a) > float(b) else "↓" if float(a) < float(b) else "="
    except Exception: return "?"
cur = [n_known, g[1], sess[0]]
if rows:
    c = [x.strip() for x in rows[-1].strip("|").split("|")]
    tend = "".join(arrow(a, b) for a, b in zip(cur, [c[2], c[4], c[6]]))
else: tend = "inicio"
row = f"| {stamp} | {n_sm} | {n_known} | {g[0]} | {g[1]} | {g[2]} | {sess[0]} | {sess[1]} | " + " | ".join(str(e) for e in ev) + f" | {top} | {tend} |"
print(row)
if "--dry" not in sys.argv:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(HEAD + "\n".join(rows + [row]) + "\n")
