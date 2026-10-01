#!/usr/bin/env python3
"""Generador estático de quemeconviene. Sin dependencias. Uso: python3 build.py"""
import json, os, shutil, html, datetime
from string import Template

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
site = json.load(open(os.path.join(ROOT, "data/site.json")))
params = json.load(open(os.path.join(ROOT, "data/params.json")))
BASE = Template(open(os.path.join(ROOT, "templates/base.html")).read())
pages = []  # (path, lastmod, priority)

def head_extra():
    out = []
    if site.get("search_console_meta"):
        out.append(f'<meta name="google-site-verification" content="{site["search_console_meta"]}">')
    if site.get("analytics_plausible_domain"):
        out.append(f'<script defer data-domain="{site["analytics_plausible_domain"]}" src="https://plausible.io/js/script.js"></script>')
    if site.get("ga4_id"):
        g = site["ga4_id"]
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{g}",{{anonymize_ip:true}});</script>')
    if site.get("adsense_client"):
        out.append(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={site["adsense_client"]}" crossorigin="anonymous"></script>')
    return "\n".join(out)

def write(path, title, description, body, scripts="", jsonld=None, priority="0.6"):
    """path: '/' o '/decidir/slug/'. Genera index.html en esa carpeta."""
    canonical = site["base_url"].rstrip("/") + path
    extra = head_extra()
    if jsonld:
        extra += "\n" + "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    out = BASE.substitute(title=html.escape(title), description=html.escape(description), canonical=canonical,
                          head_extra=extra, body=body, scripts=scripts, site_name=site["name"], year=site["year"])
    d = os.path.join(DIST, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    pages.append((canonical, datetime.date.today().isoformat(), priority))

def load_calcs():
    calcs = []
    cdir = os.path.join(ROOT, "calcs")
    for f in sorted(os.listdir(cdir)):
        if f.endswith(".json") and not f.endswith(".test.json"):
            c = json.load(open(os.path.join(cdir, f)))
            c["js"] = open(os.path.join(cdir, c["slug"] + ".js")).read()
            c["content"] = open(os.path.join(ROOT, "content", c["slug"] + ".html")).read()
            calcs.append(c)
    return calcs

def render_calc(c, all_calcs):
    inputs = "".join(
        f'<div><label for="{i["id"]}">{i["label"]}</label>'
        + (f'<select id="{i["id"]}">' + "".join(f'<option value="{o["v"]}">{o["t"]}</option>' for o in i["options"]) + "</select>"
           if i.get("type") == "select" else
           f'<input id="{i["id"]}" type="number" inputmode="decimal" value="{i["default"]}" min="{i.get("min",0)}" step="{i.get("step","any")}">')
        + "</div>" for i in c["inputs"])
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faqs"])
    related = [x for x in all_calcs if x["slug"] != c["slug"]]
    rel_html = ("<h2>Otras decisiones relacionadas</h2><ul class=\"cards\">" + "".join(
        f'<li><a href="/decidir/{x["slug"]}/">{x["h1"]}</a><p>{x["description"]}</p></li>' for x in related) + "</ul>") if related else ""
    body = f"""
<h1>{c["h1"]}</h1>
<p class="lead">{c["lead"]}</p>
<div class="calc">
<form id="f" onsubmit="return false"><div class="grid">{inputs}</div><button id="go" type="button">Calcular con mis números</button></form>
<div class="result" id="r"></div>
</div>
{c["content"]}
<h2>Preguntas frecuentes</h2>
{faqs}
<h2>Supuestos y fuentes</h2>
<p class="note">{c["sources"]} Parámetros actualizados el {params["fecha"]}. Los cálculos se hacen en tu navegador; no enviamos tus datos a ningún servidor.</p>
<p class="disclaimer">Esta herramienta es orientativa y no constituye asesoramiento financiero. Comprueba las condiciones concretas de tu contrato y, si la decisión es importante, consulta con un profesional. Lee nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
{rel_html}
"""
    jsonld = [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]]},
        {"@context": "https://schema.org", "@type": "WebApplication", "name": c["h1"], "applicationCategory": "FinanceApplication",
         "operatingSystem": "Web", "url": site["base_url"] + f"/decidir/{c['slug']}/", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": site["base_url"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Calculadoras", "item": site["base_url"] + "/decidir/"},
            {"@type": "ListItem", "position": 3, "name": c["h1"]}]},
    ]
    write(f"/decidir/{c['slug']}/", c["title"], c["description"], body, scripts=f"<script>{c['js']}</script>", jsonld=jsonld, priority="0.9")

def main():
    shutil.rmtree(DIST, ignore_errors=True); os.makedirs(DIST)
    calcs = load_calcs()
    for c in calcs: render_calc(c, calcs)
    cards = "".join(f'<li><a href="/decidir/{c["slug"]}/">{c["h1"]}</a><p>{c["description"]}</p></li>' for c in calcs)
    write("/", f'{site["name"]} — {site["tagline"]}',
          "Calculadoras para decidir con tus propios números: amortizar plazo o cuota, hipoteca fija o variable, renting o compra y más. Gratis, sin registro.",
          f'<h1>{site["tagline"]}</h1><p class="lead">Google te da la respuesta genérica. Aquí metes <strong>tus</strong> números y ves cuál te conviene a ti, con el cálculo explicado.</p><h2>Calculadoras</h2><ul class="cards">{cards}</ul>',
          priority="1.0")
    write("/decidir/", "Todas las calculadoras de decisión", "Lista de comparadores X o Y con tus números: hipoteca, coche, impuestos, energía.",
          f'<h1>Calculadoras de decisión</h1><ul class="cards">{cards}</ul>', priority="0.8")
    for slug, title, desc in [("como-funciona", "Cómo funciona", "Qué hacemos, qué no, y cómo se calculan los resultados."),
                              ("aviso-legal", "Aviso legal", "Titular, condiciones de uso y limitación de responsabilidad."),
                              ("privacidad", "Política de privacidad", "Qué datos tratamos (casi ninguno) y con qué base legal."),
                              ("cookies", "Política de cookies", "Cookies que usa el sitio y cómo gestionarlas."),
                              ("politica-ia", "Política de uso de IA", "Cómo usamos inteligencia artificial en los textos y qué revisamos."),
                              ("contacto", "Contacto", "Cómo contactar con el editor del sitio.")]:
        body = open(os.path.join(ROOT, "content", f"{slug}.html")).read().replace("$site_name", site["name"]).replace("$owner", site["owner"]).replace("$email", site["contact_email"])
        write(f"/{slug}/", f'{title} — {site["name"]}', desc, body, priority="0.2")
    open(os.path.join(DIST, "404.html"), "w").write(BASE.substitute(title="Página no encontrada", description="", canonical=site["base_url"], head_extra="", body='<h1>No encontramos esa página</h1><p><a href="/">Volver al inicio</a></p>', scripts="", site_name=site["name"], year=site["year"]))
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {site['base_url']}/sitemap.xml\n")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n" for u, d, p in pages) + "</urlset>\n"
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
    host = site["base_url"].split("//")[1].split("/")[0]
    if "pages.dev" not in host and "github.io" not in host: open(os.path.join(DIST, "CNAME"), "w").write(host + "\n")
    open(os.path.join(DIST, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    print(f"OK: {len(pages)} páginas, {len(calcs)} calculadoras → dist/")

if __name__ == "__main__":
    main()
