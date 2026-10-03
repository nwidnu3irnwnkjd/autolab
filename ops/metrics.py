#!/usr/bin/env python3
"""Métricas de Search Console y GA4 para un proyecto. Uso: python3 ops/metrics.py decidir [dias=28]
Con --inspect añade la URL Inspection API para las URLs clave de data/site.json["inspect"] (o una lista por defecto).
Escribe un resumen en journal/metrics/<proyecto>-<fecha>.md y lo imprime."""
import sys, os, json, datetime, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gauth
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSPECT = "--inspect" in sys.argv; sys.argv = [a for a in sys.argv if a != "--inspect"]
proj = sys.argv[1] if len(sys.argv) > 1 else "decidir"; days = int(sys.argv[2]) if len(sys.argv) > 2 else 28
site = json.load(open(os.path.join(ROOT, "projects", proj, "data/site.json")))
host = site["base_url"].split("//")[1].split("/")[0]
t = gauth.token(); today = datetime.date.today(); start = today - datetime.timedelta(days=days)
out = [f"# Métricas {proj} ({host}) — {today} (últimos {days} días)"]
# Search Console
sc = f"https://www.googleapis.com/webmasters/v3/sites/sc-domain:{host}"
try:
    sm = gauth.get(sc + "/sitemaps", t).get("sitemap", [])
    out.append("## Search Console\n" + "\n".join(f"- sitemap {s['path']}: pendiente={s.get('isPending')} errores={s.get('errors')} descubiertas={sum(int(c.get('submitted',0)) for c in s.get('contents',[]))}" for s in sm))
    q = gauth.post(sc + "/searchAnalytics/query", t, {"startDate": str(start), "endDate": str(today), "dimensions": ["page"], "rowLimit": 50})
    rows = q.get("rows", [])
    tot = {k: sum(r[k] for r in rows) for k in ("clicks", "impressions")}
    out.append(f"- Total: {tot['clicks']} clics, {tot['impressions']} impresiones\n")
    out.append("| Página | Clics | Impr. | CTR | Pos. |\n|---|---|---|---|---|\n" + "\n".join(f"| {r['keys'][0].replace(site['base_url'],'')} | {r['clicks']} | {r['impressions']} | {r['ctr']*100:.1f}% | {r['position']:.1f} |" for r in rows[:20]))
    qq = gauth.post(sc + "/searchAnalytics/query", t, {"startDate": str(start), "endDate": str(today), "dimensions": ["query"], "rowLimit": 25}).get("rows", [])
    if qq: out.append("\n**Consultas:** " + "; ".join(f"{r['keys'][0]} ({r['impressions']} impr., pos. {r['position']:.0f})" for r in qq))
except urllib.error.HTTPError as e: out.append(f"Search Console: error HTTP {e.code}: {e.read().decode()[:200]}")
# URL Inspection API (cuota: 2.000/día por propiedad; solo con --inspect)
if INSPECT:
    urls = site.get("inspect") or ["/", "/decidir/hipoteca-fija-o-variable/", "/guias/euribor-hipoteca/", "/barometro/", "/calendario/", "/noticias/", "/datos/"]
    out.append("\n## Inspección de URLs (URL Inspection API)\n| URL | Veredicto | Cobertura | Rastreo | robots | Fetch | Referentes |\n|---|---|---|---|---|---|---|")
    for u in urls:
        try:
            r = gauth.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect", t,
                {"inspectionUrl": site["base_url"].rstrip("/") + u, "siteUrl": f"sc-domain:{host}", "languageCode": "es-ES"})
            x = r.get("inspectionResult", {}).get("indexStatusResult", {})
            out.append(f"| {u} | {x.get('verdict')} | {x.get('coverageState')} | {x.get('lastCrawlTime', '—')} | {x.get('robotsTxtState','').replace('ROBOTS_TXT_STATE_','')} | {x.get('pageFetchState','').replace('PAGE_FETCH_STATE_','')} | {len(x.get('referringUrls', []))} |")
        except urllib.error.HTTPError as e: out.append(f"| {u} | error HTTP {e.code} | {e.read().decode()[:120]} | | | | |")
# GA4
pid = site.get("ga4_property_id")
if pid:
    try:
        r = gauth.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport", t,
            {"dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "today"}], "dimensions": [{"name": "pagePath"}], "metrics": [{"name": "sessions"}, {"name": "activeUsers"}, {"name": "averageSessionDuration"}], "limit": 20, "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}]})
        rows = r.get("rows", [])
        out.append("\n## GA4\n" + (f"- Sesiones: {sum(int(x['metricValues'][0]['value']) for x in rows)} · Usuarios: {sum(int(x['metricValues'][1]['value']) for x in rows)}\n" if rows else "- Sin datos aún\n") +
                   "\n".join(f"- {x['dimensionValues'][0]['value']}: {x['metricValues'][0]['value']} sesiones, {float(x['metricValues'][2]['value']):.0f}s" for x in rows))
    except urllib.error.HTTPError as e: out.append(f"GA4: error HTTP {e.code}: {e.read().decode()[:200]}")
else: out.append("\n## GA4\n- Falta `ga4_property_id` en data/site.json")
txt = "\n".join(out); print(txt)
os.makedirs(os.path.join(ROOT, "journal/metrics"), exist_ok=True)
open(os.path.join(ROOT, "journal/metrics", f"{proj}-{today}.md"), "w").write(txt + "\n")
