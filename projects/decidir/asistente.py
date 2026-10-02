"""Asistente «¿Cuál es tu situación?» (Diseñador). Mapa en data/asistente.json (editable por el Estratega).
build(dist, calcs, guides, tablas_pages) valida que todos los slugs existan (si no, falla), escribe dist/assets/asistente.json
(datos que el JS pide al abrir el primer paso) y devuelve el bloque HTML + JS inline para la home y /todas/."""
import hashlib, html, json, os
import minify

ROOT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

JS = r'''(function(){var r=document.getElementById("asis");if(!r||!window.fetch)return;var b=r.querySelector(".asis-b"),D,H=r.getAttribute("data-u");
function ev(n,p){try{if(window.gtag)gtag("event",n,p)}catch(x){}}
function h(t,c,x){var n=document.createElement(t);if(c)n.className=c;if(x)n.textContent=x;return n}
function a(u,t,c){var n=h("a",c,t);n.href=u;return n}
function btn(t,c,f){var n=h("button",c,t);n.type="button";n.onclick=f;return n}
function show(el,st,tt){b.textContent="";var p=h("p","asis-p","Paso "+st+" de 3");var t=h("h3","asis-t",tt);t.tabIndex=-1;b.appendChild(p);b.appendChild(t);el(b);t.focus({preventScroll:false})}
function s1(){b.textContent="";r.removeAttribute("data-m");var u=h("ul","asis-g");D.s.forEach(function(s){var l=h("li"),k=btn("","asis-c",function(){s2(s)});k.appendChild(h("strong","",s.t));k.appendChild(h("span","",s.d));l.appendChild(k);u.appendChild(l)});b.appendChild(u)}
function s2(s){ev("asistente_paso",{paso:2,situacion:s.i});show(function(c){var u=h("ul","asis-g asis-o");s.o.forEach(function(o){var l=h("li"),k=btn(o.t,"asis-c",function(){s3(s,o)});l.appendChild(k);u.appendChild(l)});c.appendChild(u);c.appendChild(btn("Volver","btn2",function(){top1()}))},2,s.q)}
function s3(s,o){ev("asistente_resultado",{situacion:s.i,opcion:o.i});show(function(c){c.appendChild(h("p","asis-w",o.p));var l=h("ol","asis-r");o.c.forEach(function(u){var i=h("li");i.appendChild(a(u,D.n[u]));l.appendChild(i)});c.appendChild(l);var x=h("ul","asis-x");[["Guía",o.g],["Tabla oficial",o.b]].forEach(function(q){if(q[1]){var i=h("li");i.appendChild(h("span","",q[0]+": "));i.appendChild(a(q[1],D.n[q[1]]));x.appendChild(i)}});c.appendChild(x);c.appendChild(btn("Volver","btn2",function(){s2(s)}));c.appendChild(btn("Empezar de nuevo","btn2",function(){top1()}))},3,o.t+": mira esto primero")}
function top1(){s1();var t=r.querySelector("h2");t.tabIndex=-1;t.focus()}
function go(){var o;fetch(H).then(function(x){return x.json()}).then(function(d){D=d;o=document.getElementById("situacion");r.hidden=false;if(o){o.hidden=true;o.nextElementSibling.hidden=true}s1();ev("asistente_paso",{paso:1})}).catch(function(){r.hidden=true;if(o){o.hidden=false;o.nextElementSibling.hidden=false}})}
go()})();'''


def build(dist, calcs, guides, tablas_pages, tablas_path="/tablas-2026/"):
    raw = json.load(open(os.path.join(ROOT, "data/asistente.json")))
    cs = {c["slug"]: c["h1"] for c in calcs}
    gs = {g["slug"]: g["h1"] for g in guides}
    ts = {p["slug"]: p["h1"] for p in tablas_pages}
    names, err, out = {}, [], []
    def need(kind, slug, where):
        tab = {"c": cs, "g": gs, "b": ts}[kind]
        if slug not in tab:
            err.append(f"{where}: no existe {slug!r} ({ {'c': 'calculadora', 'g': 'guía', 'b': 'tabla'}[kind] })"); return None
        u = {"c": f"/decidir/{slug}/", "g": f"/guias/{slug}/", "b": f"{tablas_path}{slug}/"}[kind]
        names[u] = tab[slug]; return u
    for s in raw["situaciones"]:
        opts = []
        for o in s["opciones"]:
            w = f'{s["id"]}/{o["id"]}'
            if not 3 <= len(o["calcs"]) <= 5: err.append(f"{w}: debe tener 3-5 calculadoras")
            d = {"i": o["id"], "t": o["titulo"], "p": o["porque"], "c": [u for u in (need("c", x, w) for x in o["calcs"]) if u]}
            if o.get("guia"): d["g"] = need("g", o["guia"], w)
            if o.get("tabla"): d["b"] = need("b", o["tabla"], w)
            opts.append(d)
        out.append({"i": s["id"], "t": s["titulo"], "d": s["desc"], "q": s["pregunta"], "o": opts})
    if err: raise SystemExit("asistente.json inválido:\n  " + "\n  ".join(err))
    data = json.dumps({"s": out, "n": names}, ensure_ascii=False, separators=(",", ":"))
    v = hashlib.sha1(data.encode()).hexdigest()[:10]
    os.makedirs(os.path.join(dist, "assets"), exist_ok=True)
    open(os.path.join(dist, "assets", "asistente.json"), "w").write(data)
    return (f'<section class="asis" id="asis" data-u="/assets/asistente.json?v={v}" aria-labelledby="asis-h" hidden>'
            '<h2 id="asis-h">¿Cuál es tu situación?</h2>'
            '<p class="asis-i">Responde dos preguntas y te decimos qué calculadoras mirar primero. No guardamos nada.</p>'
            '<div class="asis-b" aria-live="polite"></div></section><script>' + minify.js(JS) + '</script>')
