"""Plan completo «Compra de vivienda» (Diseñador, R16.4): encadena calculadoras pasando entre ellas los valores compartidos.
Datos en data/planes.json (pasos + mapa de ids de input por enlace). Sin ficheros JS extra: un script inline de ~0,5 KB por calculadora
lee los valores ACTUALES del formulario al pulsar «Continúa con…» y construye `#v=id:valor~...` (el que ya restaura EM.live)."""
import html, json, os
import seo

ROOT = os.path.dirname(os.path.abspath(__file__))
PLANES = json.load(open(os.path.join(ROOT, "data/planes.json")))
FILES = ["plan.py", "data/planes.json"]
e = html.escape

JS = ('(function(){var a=document.querySelector("a[data-pm]");if(!a)return;var h=a.getAttribute("href");'
      'function f(){try{var o=[];a.getAttribute("data-pm").split(",").forEach(function(p){var k=p.split(":"),s=k[0].split("+"),x=document.getElementById(s[0]),v;'
      'if(!x||x.value==="")return;v=x.value;if(s[1]){var y=document.getElementById(s[1]);if(!y||y.value==="")return;v=Math.round(x.value*(1-y.value/100))}'
      'o.push(k[1]+":"+encodeURIComponent(v))});a.href=o.length?h+"#v="+o.join("~"):h}catch(z){}}'
      '["click","auxclick","touchstart","focus"].forEach(function(t){a.addEventListener(t,f,{passive:true})});'
      'a.addEventListener("click",function(){try{gtag("event","plan_siguiente_click",{plan:a.getAttribute("data-plan"),desde:a.getAttribute("data-de"),paso:+a.getAttribute("data-n")})}catch(z){}})})();')


def validate(calcs):
    """Avisa (no rompe) si un id de input del mapa no existe en la calculadora de origen o de destino."""
    by = {c["slug"]: {i["id"] for i in c["inputs"]} for c in calcs}
    for k, p in PLANES.items():
        if k.startswith("_"): continue
        for s in p["steps"]:
            if s["slug"] not in by: print(f"AVISO plan {k}: la calculadora {s['slug']} no existe")
        for l in p["links"]:
            for src, dst in l["map"].items():
                for sid in src.split("+"):
                    if sid not in by.get(l["from"], ()): print(f"AVISO plan {k}: input «{sid}» no existe en {l['from']}")
                if dst not in by.get(l["to"], ()): print(f"AVISO plan {k}: input «{dst}» no existe en {l['to']}")


def _plans_of(slug):
    return [(k, p, i) for k, p in PLANES.items() if not k.startswith("_") for i, s in enumerate(p["steps"]) if s["slug"] == slug]


def _go(k, p, i, slug):
    n = len(p["steps"])
    if i + 1 < n:
        nx = p["steps"][i + 1]
        lk = next((l for l in p["links"] if l["from"] == slug and l["to"] == nx["slug"]), None)
        pm = ",".join(f"{a}:{b}" for a, b in lk["map"].items()) if lk and lk["map"] else ""
        carry = lk.get("carry", "") if pm else ""
        go = (f'<a class="btn2 plan-go" href="/decidir/{nx["slug"]}/" data-plan="{k}" data-de="{slug}" data-n="{i + 1}"' + (f' data-pm="{pm}"' if pm else "") +
              f'>Continúa con {e(nx["name"])} →</a>' + (f'<span class="note plan-t">{e(carry)}</span>' if carry else ""))
        return go, bool(pm)
    return f'<a class="btn2 plan-go" href="{p["path"]}">Has completado el plan: repasa los {n} pasos →</a>', False


def next_block(slug):
    """Bloque «Siguiente paso» tras el resultado de cada calculadora del plan ('' si no está en ningún plan; compacto si está en varios)."""
    ps = _plans_of(slug)
    if not ps: return ""
    multi = len(ps) > 1; out = []; script = False
    for k, p, i in ps:
        n = len(p["steps"])
        head = f'<p class="plan-h">Paso {i + 1} de {n} · <a href="{p["path"]}">{e(p["name"])}</a></p>'
        go, pm = _go(k, p, i, slug)
        if pm and not script: script = True  # el script lee el primer enlace con data-pm
        if multi:
            out.append(f'<div class="plan-one">{head}<div class="plan-act">{go}</div></div>')
        else:
            dots = "".join(
                f'<li><span aria-current="step"><b>{j + 1}</b> {e(s["short"])}</span></li>' if j == i else f'<li><a href="/decidir/{s["slug"]}/"><b>{j + 1}</b> {e(s["short"])}</a></li>'
                for j, s in enumerate(p["steps"]))
            out.append(f'{head}<ol class="plan-dots">{dots}</ol><div class="plan-act">{go}</div>')
    nm = " / ".join(p["name"] for _, p, _ in ps)
    return f'<aside class="plan-next" aria-label="{e(nm)}">{"".join(out)}' + (f"<script>{JS}</script>" if script else "") + "</aside>"


def hub_link(spec_path, key="compra-vivienda"):
    p = PLANES[key]
    return f'<p class="note hub-link"><strong>Plan completo:</strong> <a href="{p["path"]}">{e(p["name"])}</a>, {p["hub_txt"]}</p>'


def dir_li(key="compra-vivienda"):
    p = PLANES[key]
    return f'<li data-k="{e(p["dir_k"])}"><a href="{p["path"]}">{e(p["name"])}</a> <span class="note">{e(p["hub_txt"][0].upper() + p["hub_txt"][1:])}</span></li>'


def page(key, calcs, card, base, pub, mod):
    p = PLANES[key]; by = {c["slug"]: c for c in calcs}
    secs = []
    for i, s in enumerate(p["steps"]):
        c = by.get(s["slug"])
        if not c: continue
        secs.append(f'<section class="box" id="paso-{i + 1}"><h3>Paso {i + 1}: {e(s["name"])}</h3><p>{e(s["text"])}</p>'
                    f'<p><a class="btn2" href="/decidir/{s["slug"]}/">{e(c["h1"])}</a></p></section>')
    faqs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faqs"])
    cards = "".join(card(by[s["slug"]]) for s in p["steps"] if s["slug"] in by)
    body = f"""<article class="guide hub">
<p class="kicker">{e(p["kicker"])}</p>
<h1>{e(p["h1"])}</h1>
<p class="byline note">Por {seo.AUTHOR} · Publicado el <time datetime="{pub}">{seo.fecha_es(pub)}</time> · Actualizado el <time datetime="{mod}">{seo.fecha_es(mod)}</time></p>
<p class="lead">{p["lead"]}</p>
<p><a class="btn2" href="/decidir/{p["steps"][0]["slug"]}/">Empezar por el paso 1</a></p>
{"".join(secs)}
<h2>Preguntas frecuentes</h2>
{faqs}
<h2>Las calculadoras del plan</h2>
<ul class="cards">{cards}</ul>
<p class="note hub-link">Más sobre el tema: <a href="{p["parent"][0]}">{e(p["parent"][1])}: decide con tus números</a> · <a href="/todas/">Lista completa de calculadoras y guías</a>.</p>
<p class="disclaimer">Información orientativa, no constituye asesoramiento financiero ni legal. Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""
    url = base + p["path"]
    ld = [seo.article(p["h1"], p["description"], url, pub, mod, base),
          {"@context": "https://schema.org", "@type": "HowTo", "name": p["h1"], "description": p["description"], "inLanguage": "es-ES",
           "step": [{"@type": "HowToStep", "position": i + 1, "name": s["name"], "text": s["text"], "url": f"{base}/decidir/{s['slug']}/"} for i, s in enumerate(p["steps"])]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
          seo.breadcrumbs(base, [("Inicio", "/"), (p["parent"][1], p["parent"][0]), (p["short"], None)])]
    return body, ld
