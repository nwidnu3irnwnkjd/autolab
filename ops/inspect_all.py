#!/usr/bin/env python3
"""Inspecciona con la URL Inspection API todas las URL del sitemap (máx. 1 vez cada 20 h; cuota 2.000/día).
Escribe journal/inspeccion.json y devuelve «total · conocidas · rastreadas · indexadas · rastreada-sin-indexar».
Uso: python3 ops/inspect_all.py [--force]. No imprime secretos."""
import sys, os, re, json, time, datetime, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gauth
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "journal/inspeccion.json")
site = json.load(open(os.path.join(ROOT, "projects/decidir/data/site.json")))
BASE = site["base_url"].rstrip("/"); host = BASE.split("//")[1]
def urls():
    idx = urllib.request.urlopen(BASE + "/sitemap.xml", timeout=20).read().decode()
    out = []
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        out += re.findall(r"<loc>([^<]+)</loc>", urllib.request.urlopen(sm, timeout=20).read().decode())
    return sorted(set(out))
def summary(d):
    r = d["resultados"]; tot = len(r)
    conoc = sum(1 for v in r.values() if v["estado"] and "no reconoce" not in v["estado"].lower() and "unknown" not in v["estado"].lower())
    indexed = sum(1 for v in r.values() if v.get("veredicto") == "PASS")
    sin = sum(1 for v in r.values() if "sin indexar" in (v["estado"] or "").lower() or "not indexed" in (v["estado"] or "").lower())
    rastr = sum(1 for v in r.values() if v.get("ultimo_rastreo"))
    return dict(total=tot, conocidas=conoc, rastreadas=rastr, indexadas=indexed, rastreada_sin_indexar=sin, fecha=d["fecha"])
if __name__ == "__main__":
    force = "--force" in sys.argv
    if os.path.exists(OUT) and not force:
        d = json.load(open(OUT))
        if time.time() - d.get("ts", 0) < 20 * 3600:
            print(json.dumps(summary(d))); sys.exit(0)
    tok = gauth.token(); res = {}
    for u in urls():
        try:
            r = gauth.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect", tok,
                {"inspectionUrl": u, "siteUrl": f"sc-domain:{host}", "languageCode": "es-ES"})
            i = r.get("inspectionResult", {}).get("indexStatusResult", {})
            res[u] = {"estado": i.get("coverageState", ""), "veredicto": i.get("verdict", ""), "ultimo_rastreo": i.get("lastCrawlTime", "")}
        except Exception as e:
            res[u] = {"estado": "", "veredicto": "ERROR", "ultimo_rastreo": ""}
        time.sleep(0.3)
    d = {"ts": time.time(), "fecha": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ"), "resultados": res}
    json.dump(d, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(summary(d)))
