"""Widget «Inserta esta calculadora en tu web» (Diseñador, PLAN-TRAFICO F): /embed/<slug>/ (iframe ligero, noindex,follow,
canonical a la completa), bloque plegable en cada calculadora y página /inserta/. No toca calcs/ ni content/ de calculadoras."""
import html, json, os, re
import minify, ui

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = "/inserta/"
SITE = json.load(open(os.path.join(ROOT, "data/site.json")))
B = SITE["base_url"].rstrip("/")
EXAMPLES = ["hipoteca-fija-o-variable", "alquilar-o-comprar", "amortizar-plazo-o-cuota"]  # /inserta/: 3 ejemplos con preview


def height(c):
    """Altura recomendada (px): formulario (2 columnas en pantallas anchas) + resultado con gráfico/tabla; el embed la ajusta con postMessage."""
    n = len(c["inputs"])
    return 700 + 40 * ((n + 1) // 2)


def code(c):
    return (f'<iframe src="{B}/embed/{c["slug"]}/" width="100%" height="{height(c)}" loading="lazy" '
            f'title="{html.escape(c["h1"], quote=True)} — Entre Muchos" style="border:0"></iframe>')


def block(c):
    """Bloque plegable «Insertar en tu web» al final del contenido de cada calculadora."""
    cd = html.escape(code(c))
    cita = html.escape(f'<a href="{B}/decidir/{c["slug"]}/">{c["h1"]}</a> (Entre Muchos, entremuchos.com)')
    return f"""<details class="emb-ins" id="insertar"><summary>Insertar en tu web</summary>
<div class="emb-in"><p>Gratis, con crédito y enlace a Entre Muchos. Copia este código en tu página:</p>
<textarea readonly rows="3" aria-label="Código para insertar la calculadora" data-code>{cd}</textarea>
<p><button type="button" class="btn2" data-copy>Copiar código</button> <span class="em-toast" role="status" aria-live="polite" data-copied></span></p>
<div class="emb-cita"><p>¿Prefieres citarla? Enlace con fuente y fecha:</p>
<textarea readonly rows="2" aria-label="Enlace para citar esta calculadora" data-code>{cita}</textarea>
<p><button type="button" class="btn2" data-copy data-ev="cite_copy">Copiar enlace</button> <span class="em-toast" role="status" aria-live="polite" data-copied></span></p></div>
<p class="note">La altura se ajusta sola con <a href="{PATH}#altura">este script opcional</a>. <a href="{PATH}">Condiciones de uso y ejemplos</a>.</p></div></details>"""


def page_html(c):
    """/embed/<slug>/: solo formulario + resultado, sin cabecera ni pie del sitio."""
    url = f"{B}/decidir/{c['slug']}/"
    title = html.escape(c["title"]); desc = html.escape(c["description"], quote=True)
    t = c["h1"] if len(c["h1"]) <= 90 else c["title"]
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{url}">
<meta name="color-scheme" content="light dark"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="stylesheet" href="/assets/app.css"><style>body{{margin:0;background:#f5f6fa}}@media (prefers-color-scheme:dark){{body{{background:#0a0c13;color:#eceff7}}}}</style>
</head><body class="emb"><main class="emb-m"><h1>{html.escape(t)}</h1>
{ui.calc_form(c)}
<p class="emb-f"><a href="{url}" target="_blank" rel="noopener">Calculadora de Entre Muchos · Ver completa y fuentes</a></p></main>
<script src="/assets/em.js"></script><script>{minify.js(c["js"])}</script>
<script>(function(){{if(parent===window)return;var l=0;function s(){{var h=document.body.offsetHeight;if(h!==l){{l=h;parent.postMessage({{emHeight:h,slug:"{c["slug"]}"}},"*")}}}}if(window.ResizeObserver)new ResizeObserver(s).observe(document.body);addEventListener("load",s)}})()</script>
</body></html>
"""


def build(dist, calcs):
    for c in calcs:
        d = os.path.join(dist, "embed", c["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(minify.html(page_html(c)))
    return len(calcs)


SCRIPT = ('<script>addEventListener("message",function(e){if(e.origin!=="' + B + '"||!e.data||!e.data.emHeight)return;'
          'document.querySelectorAll(\'iframe[src^="' + B + '/embed/"]\').forEach(function(f){if(f.contentWindow===e.source)f.style.height=e.data.emHeight+"px"})})</script>')


def page(calcs):
    """/inserta/ -> (body, jsonld, desc)."""
    by = {c["slug"]: c for c in calcs}
    ex = [by[s] for s in EXAMPLES if s in by]
    desc = "Inserta gratis una calculadora de Entre Muchos en tu web o blog con un iframe ligero: copia el código, mantén el crédito y el enlace."
    faqs = [("¿Cuesta algo insertar una calculadora?", "No. Es gratis; solo pedimos que se vea el crédito «Calculadora de Entre Muchos» y su enlace a la versión completa, que ya incluye el propio widget."),
            ("¿Puedo cambiar las cifras o el diseño?", "No debes modificar los cálculos, las cifras ni el aviso de que no es asesoramiento. Sí puedes ajustar el ancho, el alto y el marco de la página donde lo insertas."),
            ("¿Qué datos recoge el widget?", "Ninguno: los cálculos se hacen en el navegador de quien lo usa y no enviamos sus datos a ningún servidor."),
            ("¿Cómo evito la barra de desplazamiento dentro del iframe?", "Añade el script opcional de esta página: el widget informa de su altura y el script ajusta el iframe. Sin él, usa la altura recomendada de cada calculadora."),
            ("¿Puedo insertar cualquier calculadora?", "Sí, todas las del catálogo tienen versión insertable en /embed/ seguida del nombre de la calculadora. Cada página de calculadora tiene un bloque «Insertar en tu web» con su código.")]
    exs = "".join(f"""<section class="emb-ex"><h3>{html.escape(c["h1"])}</h3>
<textarea readonly rows="3" aria-label="Código de {html.escape(c["slug"], quote=True)}" data-code>{html.escape(code(c))}</textarea>
<p><button type="button" class="btn2" data-copy>Copiar código</button> <span class="em-toast" role="status" aria-live="polite" data-copied></span> <a href="/decidir/{c["slug"]}/">Ver la calculadora completa</a></p>
<details open><summary>Vista previa</summary><iframe src="/embed/{c["slug"]}/" width="100%" height="{height(c)}" loading="lazy" title="Vista previa: {html.escape(c["h1"], quote=True)}" style="border:0"></iframe></details></section>""" for c in ex)
    body = f"""<article class="guide hub">
<p class="kicker">Para webs y blogs</p>
<h1>Inserta una calculadora de Entre Muchos en tu web</h1>
<p class="lead">Cada calculadora de decisión tiene una versión ligera que puedes insertar en tu página con una sola línea de código. Es gratis y funciona en móvil y escritorio, en claro y oscuro.</p>
<h2>Cómo insertarla</h2>
<ol><li>Abre la calculadora que quieras y pulsa «Insertar en tu web» (al final de la página), o usa uno de los ejemplos de abajo.</li>
<li>Pulsa «Copiar código» y pégalo donde quieras que aparezca (en WordPress, bloque «HTML personalizado»).</li>
<li>Opcional: añade el script de altura automática para que el iframe no tenga barra de desplazamiento.</li></ol>
<h2 id="altura">Script opcional de altura automática</h2>
<p>El widget envía su altura a la página que lo contiene. Pega esto una sola vez en tu página:</p>
<textarea readonly rows="4" aria-label="Script de altura automática" data-code>{html.escape(SCRIPT)}</textarea>
<p><button type="button" class="btn2" data-copy>Copiar script</button> <span class="em-toast" role="status" aria-live="polite" data-copied></span></p>
<h2>Condiciones de uso</h2>
<ul><li><strong>Gratis</strong> para webs, blogs y medios, sin registro.</li>
<li><strong>Crédito visible:</strong> no ocultes ni quites el pie «Calculadora de Entre Muchos · Ver completa y fuentes», que enlaza con la versión completa.</li>
<li><strong>No modifiques las cifras</strong>, los cálculos ni los avisos.</li>
<li><strong>No es asesoramiento:</strong> las calculadoras son orientativas y no constituyen asesoramiento financiero, fiscal ni legal; la persona que las usa decide bajo su responsabilidad. Más en el <a href="/aviso-legal/">aviso legal</a>.</li></ul>
<h2>Ejemplos</h2>
{exs}
<h2>Preguntas frecuentes</h2>
{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)}
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. <a href="/como-funciona/">Cómo trabajamos</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": "Inserta una calculadora de Entre Muchos en tu web", "description": desc,
           "url": B + PATH, "inLanguage": "es-ES", "isPartOf": {"@type": "WebSite", "name": SITE["name"], "url": B + "/"}},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    return body, ld, desc
