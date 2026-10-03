#!/usr/bin/env python3
"""Bucle de popularidad: lo que más gusta a los usuarios recibe más visibilidad (home, hubs, /todas/, enlaces).
Uso: python3 ops/popularidad.py [--dry] [--force]
  --dry    consulta GA4/Search Console, imprime el ranking y si hay datos suficientes; NO escribe nada.
  --force  ignora la caché diaria. Sin flags: máximo 1 ejecución al día (si el JSON ya es de hoy, no consulta).
Salida: projects/decidir/data/popularidad.json (lo lee projects/decidir/popularidad.py en el build; sin datos, el build usa el orden editorial).
Credenciales solo vía ops/gauth.py; no imprime ni guarda secretos. Si una API falla, conserva el JSON anterior y sale con 0.
Score transparente por página = 3·calc_used + 3·share_click + 2·calendar_add + 2·news_to_calc + vistas + tiempo_medio_s/30 + 2·clics_GSC + impresiones_GSC/50.
Umbral: ≥ 30 sesiones totales en 28 d y ≥ 5 vistas por página; además ≥ 4 calculadoras con datos para activar «Lo más usado».
Tráfico propio: se filtra hostName == dominio del sitio (excluye localhost, vistas previas y dev). GA4 NO permite filtrar por «tráfico interno»
desde la Data API: si el filtro de datos de tráfico interno está activo en la propiedad, ya llega excluido; si no, las visitas de Andoni cuentan (límite declarado)."""
import sys, os, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gauth
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "projects/decidir/data/popularidad.json")
site = json.load(open(os.path.join(ROOT, "projects/decidir/data/site.json")))
host = site["base_url"].split("//")[1].split("/")[0]; pid = site.get("ga4_property_id")
DAYS = 28; MIN_SESIONES = 30; MIN_VISTAS_PAG = 5; MIN_CALCS = 4; TOP = 12
EVENTS = ["calc_used", "share_click", "calendar_add", "news_to_calc"]
HUB_PREFIX = ("/hipoteca/", "/impuestos/", "/coche/", "/energia/", "/ahorro/", "/tablas-2026/", "/datos/", "/barometro/", "/calendario/", "/que-cambia-1-enero-2027/", "/plan/")
DRY = "--dry" in sys.argv; FORCE = "--force" in sys.argv
today = datetime.date.today().isoformat()

def kind(path):
    if path.startswith("/decidir/") and path != "/decidir/": return "calculadoras", path.strip("/").split("/")[-1]
    if path.startswith("/guias/") and path != "/guias/": return "guias", path.strip("/").split("/")[-1]
    if path.startswith("/noticias/") and path.count("/") >= 4 and not path.startswith("/noticias/resumenes"): return "noticias", path.strip("/").split("/")[-1]
    if path in ("/hipoteca/", "/impuestos/", "/coche/", "/energia/", "/ahorro/", "/tablas-2026/", "/datos/", "/barometro/", "/calendario/", "/que-cambia-1-enero-2027/") or path.startswith(("/datos/", "/tablas-2026/")): return "hubs", path.strip("/")
    return None, None

def score(p):
    return round(3 * p["calc_used"] + 3 * p["share_click"] + 2 * p["calendar_add"] + 2 * p["news_to_calc"] + p["vistas"] + p["tiempo_medio_s"] / 30 + 2 * p["clics"] + p["impresiones"] / 50, 1)

def fetch():
    t = gauth.token(); pages = {}
    def pg(path): return pages.setdefault(path, dict(vistas=0, usuarios=0, sesiones=0, tiempo_medio_s=0.0, calc_used=0, share_click=0, calendar_add=0, news_to_calc=0, clics=0, impresiones=0, ctr=0.0, posicion=0.0))
    ga = lambda b: gauth.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport", t, b).get("rows", [])
    dr = [{"startDate": f"{DAYS}daysAgo", "endDate": "today"}]
    hostf = {"filter": {"fieldName": "hostName", "stringFilter": {"matchType": "EXACT", "value": host}}}
    # vistas, usuarios, sesiones y tiempo de interacción por página
    for r in ga({"dateRanges": dr, "dimensions": [{"name": "pagePath"}], "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}, {"name": "sessions"}, {"name": "userEngagementDuration"}],
                 "dimensionFilter": hostf, "limit": 1000}):
        v = [float(m["value"]) for m in r["metricValues"]]; p = pg(r["dimensionValues"][0]["value"])
        p.update(vistas=int(v[0]), usuarios=int(v[1]), sesiones=int(v[2]), tiempo_medio_s=round(v[3] / v[1], 1) if v[1] else 0.0)
    # eventos por página
    for r in ga({"dateRanges": dr, "dimensions": [{"name": "pagePath"}, {"name": "eventName"}], "metrics": [{"name": "eventCount"}], "limit": 5000,
                 "dimensionFilter": {"andGroup": {"expressions": [hostf, {"filter": {"fieldName": "eventName", "inListFilter": {"values": EVENTS}}}]}}}):
        pth, ev = (d["value"] for d in r["dimensionValues"]); pg(pth)[ev] += int(r["metricValues"][0]["value"])
    tot = ga({"dateRanges": dr, "metrics": [{"name": "sessions"}, {"name": "activeUsers"}], "dimensionFilter": hostf})
    sesiones = int(tot[0]["metricValues"][0]["value"]) if tot else 0; usuarios = int(tot[0]["metricValues"][1]["value"]) if tot else 0
    # Search Console
    sc = f"https://www.googleapis.com/webmasters/v3/sites/sc-domain:{host}/searchAnalytics/query"
    end = datetime.date.today(); start = end - datetime.timedelta(days=DAYS)
    for r in gauth.post(sc, t, {"startDate": str(start), "endDate": str(end), "dimensions": ["page"], "rowLimit": 1000}).get("rows", []):
        path = r["keys"][0].replace(site["base_url"].rstrip("/"), "") or "/"; p = pg(path)
        p.update(clics=int(r["clicks"]), impresiones=int(r["impressions"]), ctr=round(r["ctr"], 4), posicion=round(r["position"], 1))
    q = gauth.post(sc, t, {"startDate": str(start), "endDate": str(end), "dimensions": ["query"], "rowLimit": 25}).get("rows", [])
    consultas = [dict(consulta=r["keys"][0], impresiones=int(r["impressions"]), clics=int(r["clicks"]), ctr=round(r["ctr"], 4), posicion=round(r["position"], 1)) for r in q]
    return pages, sesiones, usuarios, consultas

def build(pages, sesiones, usuarios, consultas):
    rank = {"calculadoras": [], "guias": [], "noticias": [], "hubs": []}
    for path, p in pages.items():
        k, slug = kind(path)
        if not k or p["vistas"] < MIN_VISTAS_PAG: continue
        rank[k].append(dict(slug=slug, path=path, score=score(p), **p))
    for k in rank: rank[k] = sorted(rank[k], key=lambda x: -x["score"])[:40]
    suficiente = sesiones >= MIN_SESIONES and len(rank["calculadoras"]) >= MIN_CALCS
    return {"fecha": today, "ventana_dias": DAYS, "umbral": {"sesiones_total": MIN_SESIONES, "vistas_por_pagina": MIN_VISTAS_PAG, "calculadoras_min": MIN_CALCS},
            "sesiones_total": sesiones, "usuarios_total": usuarios, "suficiente": suficiente,
            "motivo": "" if suficiente else f"sin datos suficientes: {sesiones} sesiones (mín. {MIN_SESIONES}) y {len(rank['calculadoras'])} calculadoras con ≥ {MIN_VISTAS_PAG} vistas (mín. {MIN_CALCS}); se usa el orden editorial",
            "score": "3·calc_used + 3·share_click + 2·calendar_add + 2·news_to_calc + vistas + tiempo_medio_s/30 + 2·clics + impresiones/50",
            "limites": ["Tráfico propio: se filtra el hostName del sitio; GA4 no permite excluir tráfico interno vía API (depende del filtro de datos de la propiedad).",
                        "GSC solo muestra consultas con volumen suficiente (anonimizadas las raras)."],
            "ranking": rank if suficiente else {k: [] for k in rank}, "consultas": consultas}

def show(d):
    print(f"Fecha {d['fecha']} · ventana {d['ventana_dias']} d · sesiones {d['sesiones_total']} · usuarios {d['usuarios_total']} · umbral ≥{d['umbral']['sesiones_total']} sesiones")
    print("DATOS SUFICIENTES:", "SÍ" if d["suficiente"] else "NO — " + d["motivo"])
    for k, lst in d["ranking"].items():
        if lst: print(f"  {k}: " + "; ".join(f"{x['slug']} ({x['score']})" for x in lst[:6]))
    if d["consultas"]: print("  consultas: " + "; ".join(f"{c['consulta']} ({c['impresiones']} impr.)" for c in d["consultas"][:8]))

if __name__ == "__main__":
    if not DRY and not FORCE and os.path.exists(OUT):
        try:
            if json.load(open(OUT)).get("fecha") == today: print("popularidad.json ya es de hoy; no se consulta."); sys.exit(0)
        except Exception: pass
    if not pid: print("Falta ga4_property_id; sin cambios."); sys.exit(0)
    try: d = build(*fetch())
    except Exception as e:
        print(f"popularidad: API no disponible ({type(e).__name__}); se conserva el JSON anterior."); sys.exit(0)
    show(d)
    if not DRY:
        json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("escrito", os.path.relpath(OUT, ROOT))
