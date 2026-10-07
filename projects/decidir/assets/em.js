/* Entre Muchos — núcleo del componente de resultado (EM.renderResult, EM.live). Solo en calculadoras. Compartir/PDF en em-x.js y gráfico en chart.js, bajo demanda. */
(function () {
  "use strict";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  var COLORS = { a: "var(--c1)", b: "var(--c2)", c: "var(--c3)", d: "var(--c4)", ok: "var(--ok)", warn: "var(--warn)" };
  var ICON = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>',
    warn: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.6v.1"/></svg>',
    pdf: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 13h6M9 17h6"/></svg>',
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h8"/></svg>',
    share: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 11v6M12 7.5v.1"/></svg>'
  };
  /* EM.num / EM.eur: agrupan miles siempre ("1.143 €"; toLocaleString es-ES no agrupa 4 cifras). d = decimales (0 por defecto). */
  function num(x, d) {
    d = d || 0; x = +x;
    if (!isFinite(x)) return "–";
    var s = Math.abs(x).toFixed(d), neg = x < 0 && /[1-9]/.test(s), p = s.split(".");
    return (neg ? "-" : "") + p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (p[1] ? "," + p[1] : "");
  }
  function eur(x, d) { return num(x, d) + "\u00a0€"; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function reduced() { return !!(RM && RM.matches); }
  var state = new WeakMap();
  /* Medición (UX1.4): calc_used / result_view / calc_error. UV = grupo del A/B de la barra de resultado (UX1.8; solo móvil, "desk" en el resto). */
  /* UX2.1: variante A/B por visita (sessionStorage), no por vista de página. */
  function uvar() { var v; try { v = sessionStorage.getItem("em_uv"); } catch (e) {} if (v !== "bar" && v !== "ctl") { v = Math.random() < 0.5 ? "bar" : "ctl"; try { sessionStorage.setItem("em_uv", v); } catch (e) {} } return v; }
  var CALC = location.pathname.replace(/\/$/, "").split("/").pop(), U = 0, VW = 0, BAD = 0, BR, UV = window.matchMedia && window.matchMedia("(max-width:599px)").matches ? uvar() : "desk";
  function ev(n, p) { try { if (window.gtag) { p = p || {}; p.calc = CALC; p.ux_var = UV; gtag("event", n, p); } } catch (e) {} }
  /* Región viva aparte y breve (≤160 car.): solo el veredicto se anuncia, no la tabla entera (UX1.6). */
  function say(el, t) {
    var l = el._l;
    if (!l) { l = el._l = document.createElement("div"); l.className = "sr-only"; l.setAttribute("aria-live", "polite"); l.setAttribute("aria-atomic", "true"); el.parentNode.insertBefore(l, el); }
    l.textContent = t.length > 160 ? t.slice(0, 157).replace(/\s+\S*$/, "") + "…" : t;
  }
  /* Carga diferida: gráfico de línea (al entrar en pantalla) y módulo de compartir/PDF (al pulsar o en reposo). */
  var SC = document.currentScript, LD = {}, idleX = 0;
  function load(key, cb) {
    var u = SC && SC.getAttribute("data-" + key), L = LD[key] || (LD[key] = { q: [], s: 0 });
    if (L.s === 2 || !u) return cb && cb();
    if (cb) L.q.push(cb);
    if (L.s) return; L.s = 1;
    var s = document.createElement("script"); s.src = u;
    s.onload = function () { L.s = 2; L.q.splice(0).forEach(function (f) { f(); }); };
    document.head.appendChild(s);
  }
  function loadX(cb) { load("x", function () { cb(window.EM._x); }); }
  function lazyChart(slot, cfg) {
    if (!slot) return;
    var go = function () { load("chart", function () { if (slot.isConnected && !slot.firstChild && window.EM.lineChart) slot.appendChild(window.EM.lineChart(cfg)); }); };
    if (window.EM && window.EM.lineChart) return go();
    (window.requestIdleCallback || function (f) { setTimeout(f, 200); })(go, { timeout: 1200 }); // precarga en reposo: el gráfico ya está pintado cuando se llega a él
  }

  function countTo(el, from, to, fmt) {
    if (reduced() || !isFinite(from) || from === to) { el.textContent = fmt(to); return; }
    var t0 = Date.now(), dur = 650, done = false;
    el.textContent = fmt(from);
    function step() {
      if (done) return;
      var p = Math.min((Date.now() - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step); else done = true;
    }
    requestAnimationFrame(step);
    setTimeout(function () { done = true; el.textContent = fmt(to); }, dur + 60); // garantiza la cifra final aunque rAF vaya lento
  }

  function barsSvg(bars, fmt, caption) {
    var max = 0;
    bars.forEach(function (b) { max = Math.max(max, Math.abs(b.value)); });
    var W = "100%", rowH = 58, barH = 18, H = bars.length * rowH - 8, out = [];
    bars.forEach(function (b, i) {
      var y = i * rowH, f = max > 0 ? Math.max(Math.abs(b.value) / max, 0.006) : 0.006;
      var col = COLORS[b.color] || b.color || COLORS[["a", "b", "c", "d"][i % 4]];
      out.push('<text class="bt" x="0" y="' + (y + 16) + '">' + esc(b.label) + '</text>' +
        '<text class="bv" x="' + W + '" y="' + (y + 16) + '" text-anchor="end">' + esc((b.fmt || fmt)(b.value)) + '</text>' +
        '<rect class="tr" x="0" y="' + (y + 26) + '" width="' + W + '" height="' + barH + '" rx="9"/>' +
        '<rect class="br" data-f="' + f.toFixed(4) + '" x="0" y="' + (y + 26) + '" width="' + W + '" height="' + barH + '" rx="9" style="fill:' + col + '"/>');
    });
    return '<figure class="em-chart"><figcaption>' + esc(caption || "Comparación") + '</figcaption>' +
      '<svg width="100%" height="' + H + '" role="img" aria-label="' + esc(bars.map(function (b) { return b.label + ": " + (b.fmt || fmt)(b.value); }).join("; ")) + '">' + out.join("") + '</svg></figure>';
  }

  function table(cols, rows) {
    var h = '<div class="em-tw"><table><thead><tr><th scope="col"><span class="sr-only">Concepto</span></th>';
    cols.forEach(function (c) { h += '<th scope="col" class="n">' + c + '</th>'; });
    h += '</tr></thead><tbody>';
    rows.forEach(function (r) {
      var label = Array.isArray(r) ? r[0] : r.label, vals = Array.isArray(r) ? r.slice(1) : r.values;
      h += '<tr' + (r.strong ? ' class="em-strong"' : '') + '><th scope="row">' + label + '</th>';
      vals.forEach(function (v) { h += '<td class="n">' + v + '</td>'; });
      h += '</tr>';
    });
    return h + '</tbody></table></div>';
  }

  /* result_view (≥ 50 % del veredicto visible, una vez, tras calc_used) y barra fija móvil del A/B (UX1.8). */
  function watch(el, o, hasBig, fmt, vt) {
    if (!U || !("IntersectionObserver" in window)) return;
    if (el._o) el._o.disconnect();
    var bar = UV === "bar" && o.winner !== "revisar";
    if (bar) {
      if (!BR) {
        BR = document.createElement("button"); BR.type = "button"; BR.className = "em-bar"; BR.hidden = true; document.body.appendChild(BR);
        BR.onclick = function () { var v = document.querySelector(".em-verdict"); if (v) v.scrollIntoView({ behavior: reduced() ? "auto" : "smooth", block: "center" }); };
      }
      /* UX2.1: cifra del resultado (no la del usuario) + etiqueta corta, sin elipsis */
      var lb = (o.bigLabel || vt).replace(/<[^>]*>/g, "").replace(/^Con (estos|tus) (datos|supuestos)[,:]?\s*/i, "").split(/[.;:,(]/)[0].trim();
      if (lb.length > 24) lb = lb.slice(0, 24).replace(/\s+\S*$/, "");
      lb = lb.replace(/(\s+(con|la|el|los|las|de|del|a|en|y|que|por|para|un|una|partir|primeros|primer|\d+))+$/i, "");
      BR.textContent = (hasBig ? fmt(o.bigNumber) + (lb ? " · " + lb : "") : lb || vt.slice(0, 30)) + " ↓";
    } else if (BR) BR.hidden = true;
    el._o = new IntersectionObserver(function (en) {
      var on = en[0].isIntersecting;
      if (bar) BR.hidden = on;
      if (on && !VW) { VW = 1; ev("result_view"); }
      if (VW && !bar) el._o.disconnect();
    }, { threshold: 0.5 });
    el._o.observe(el.querySelector(".em-verdict"));
  }

  /* EM.renderResult({verdict, tone:'ok'|'warn'|'info', bigNumber, bigLabel, format, bars:[{label,value,color}],
     barsLabel, cols:[...], rows:[[label, v1, v2] | {label, values, strong}], note, el}) */
  function renderResult(o) {
    var el = typeof o.el === "string" ? document.querySelector(o.el) : (o.el || document.getElementById("r"));
    if (!el || BAD) return;
    var tone = o.tone === "warn" || o.tone === "info" ? o.tone : "ok", fmt = o.format || eur;
    var prev = state.get(el) || {};
    var h = '<div class="em-res em-tone-' + tone + '">';
    h += '<div class="em-verdict ' + tone + '">' + ICON[tone] + '<p>' + o.verdict + '</p></div>';
    var hasBig = typeof o.bigNumber === "number" && isFinite(o.bigNumber);
    if (hasBig) h += '<p class="em-big"><span class="num" aria-hidden="true"></span><span class="sr-only">' + esc(fmt(o.bigNumber)) + '</span><span class="lbl">' + (o.bigLabel || "") + '</span></p>';
    if (o.bars && o.bars.length) h += barsSvg(o.bars, fmt, o.barsLabel);
    if (o.line) h += '<div class="em-line-slot"></div>';
    if (o.rows && o.rows.length) h += table(o.cols || (o.bars || []).map(function (b) { return esc(b.label); }), o.rows);
    if (o.note) h += '<div class="em-note">' + o.note + '</div>';
    h += '<div class="em-share"><button type="button" class="btn2" data-act="copy">' + ICON.copy + 'Copiar resultado</button>' +
      '<button type="button" class="btn2" data-act="share">' + ICON.share + 'Compartir mi resultado</button>' +
      '<button type="button" class="btn2" data-act="print">' + ICON.pdf + 'Descargar informe (PDF)</button>' +
      '<span class="em-toast" role="status" aria-live="polite"></span></div>';
    h += '</div>';
    var tmpV = document.createElement("div"); tmpV.innerHTML = o.verdict;
    var key = o.winner !== undefined ? String(o.winner) : tone + "|" + tmpV.textContent.replace(/[\d.,%€\s\u00a0+\-−]+/g, " ").trim();
    say(el, tmpV.textContent);
    if (o.winner === "revisar") { if (U && !el._av) ev("calc_error", { kind: "aviso" }); el._av = 1; } else el._av = 0;
    var animateIn = !el.firstChild;
    el.innerHTML = h;
    if (!animateIn) { var res = el.firstChild; res.style.animation = "none"; }
    if (prev.key !== undefined && prev.key !== key && !reduced()) el.querySelector(".em-verdict").classList.add("em-win");
    el.style.display = "block";
    var vf = el.querySelector(".em-verdict"); if (vf.offsetHeight < innerHeight * 0.4) vf.classList.add("fx"); // UX2.2: sticky solo si cabe
    if (o.line) lazyChart(el.querySelector(".em-line-slot"), o.line);
    if (hasBig) countTo(el.querySelector(".em-big .num"), prev.big === undefined ? 0 : prev.big, o.bigNumber, fmt);
    var rects = el.querySelectorAll(".br"), pf = prev.f || [], nf = [];
    for (var i = 0; i < rects.length; i++) {
      var f = parseFloat(rects[i].getAttribute("data-f")); nf.push(f);
      if (reduced()) { rects[i].style.transform = "scaleX(" + f + ")"; continue; }
      rects[i].style.transform = "scaleX(" + (pf[i] !== undefined ? pf[i] : 0) + ")";
      rects[i].style.transitionDelay = (pf[i] !== undefined ? 0 : i * 90) + "ms";
    }
    if (!reduced() && rects.length) {
      el.getBoundingClientRect();
      requestAnimationFrame(function () { for (var j = 0; j < rects.length; j++) rects[j].style.transform = "scaleX(" + nf[j] + ")"; });
    }
    var box = el.querySelector(".em-share");
    if (box) box.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (b) loadX(function (X) { X.act(b, box, o, hasBig, fmt); });
    });
    if (!idleX) { idleX = 1; setTimeout(function () { loadX(function () {}); }, 2500); }
    state.set(el, { big: hasBig ? o.bigNumber : undefined, f: nf, key: key });
    watch(el, o, hasBig, fmt, tmpV.textContent);
  }

  /* EM.live(inputs, fn, wait): recalcula al cambiar cualquier input (debounce). inputs: selector, formulario, o lista. */
  function live(inputs, fn, wait) {
    var list;
    if (typeof inputs === "string") list = document.querySelectorAll(inputs);
    else if (inputs && inputs.tagName === "FORM") list = inputs.querySelectorAll("input,select,textarea");
    else list = inputs || [];
    var t = null, used = 0, els = [];
    var m = /[#&]v=([^&]*)/.exec(location.hash);
    if (m) m[1].split("~").forEach(function (p) { var k = p.split(":"), e = document.getElementById(decodeURIComponent(k[0])); if (e && e.form && k[1] !== undefined) e.value = decodeURIComponent(k[1]); });
    function rd(i) { if (i._d) i.setAttribute("aria-describedby", i._d); else i.removeAttribute("aria-describedby"); }
    /* UX3.3: campos data-n (type=text): «2,76», «150.000» y «150000» valen igual. Solo se normaliza lo escrito por el usuario (isTrusted); los valores puestos por código no cambian. */
    var VD = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");
    function prep(i) {
      if (i._d !== undefined || !i.hasAttribute("data-n")) return;
      i._d = i.getAttribute("aria-describedby") || "";
      Object.defineProperty(i, "value", { configurable: true,
        get: function () { var s = VD.get.call(i); if (!i._u) return s; s = s.replace(/\s/g, ""); return s.indexOf(",") > -1 ? s.replace(/\./g, "").replace(",", ".") : /^-?[1-9]\d{0,2}(\.\d{3})+$/.test(s) ? s.replace(/\./g, "") : s; },
        set: function (v) { i._u = 0; VD.set.call(i, v); } });
      i.addEventListener("input", function (e) { if (e.isTrusted) i._u = 1; });
      i.addEventListener("blur", function () { var s = i.value; if (i._u && /^-?\d+(\.\d+)?$/.test(s)) VD.set.call(i, num(s, (s.split(".")[1] || "").length).replace(/^(-?)(\d+)$/, "$1$2")); });
    }
    function used1() { if (used) return; used = U = 1; ev("calc_used"); }
    /* UX1.6: entrada vacía o fuera de rango -> aria-invalid, mensaje bajo el campo y aviso en lugar de un resultado viejo. */
    function gate() {
      var r = document.getElementById("r"), bad = "", hint = "";
      els.forEach(function (i) {
        var m = "", v = i.validity, s = i.value, x = /^-?\d+(\.\d+)?$/.test(s) ? parseFloat(s) : NaN;
        if (i.hasAttribute("data-n")) m = isNaN(x) ? "Escribe un número." : i.min !== "" && x < +i.min ? "Pon un valor de " + i.min.replace(".", ",") + " o más." : "";
        else if (i.type === "number") m = i.value === "" || v.badInput ? "Escribe un número." : v.rangeUnderflow ? "Pon un valor de " + i.min.replace(".", ",") + " o más." : v.rangeOverflow ? "Pon un valor de " + i.max.replace(".", ",") + " o menos." : "";
        var e = i._e, pend = m && i === document.activeElement; // UX2.4: sin rojo mientras se escribe; el error llega al salir del campo
        if (pend) {
          if (e) { e.remove(); i._e = null; i.removeAttribute("aria-invalid"); rd(i); }
          i._p = 1; i._m = ""; if (!hint) hint = (i.labels && i.labels[0] ? i.labels[0].textContent : i.id).split(/[(,]/)[0].trim().slice(0, 40);
          return;
        }
        i._p = 0;
        if (m) {
          if (!e) { e = i._e = document.createElement("p"); e.className = "em-err"; e.id = "e-" + i.id; i.parentNode.appendChild(e); i.setAttribute("aria-describedby", (i._d ? i._d + " " : "") + e.id); }
          if (e.textContent !== m) e.textContent = m;
          i.setAttribute("aria-invalid", "true");
          if (!i._m && U) ev("calc_error", { field: i.id });
          if (!bad) bad = (i.labels && i.labels[0] ? i.labels[0].textContent : i.id) + ": " + m.charAt(0).toLowerCase() + m.slice(1);
        } else if (e) { e.remove(); i._e = null; i.removeAttribute("aria-invalid"); rd(i); }
        i._m = m;
      });
      BAD = bad || hint ? 1 : 0;
      if (r) { if (hint && !bad) r.setAttribute("data-h", "Completa: " + hint); else r.removeAttribute("data-h"); }
      if (hint && !bad) { say(r, "Completa: " + hint); return false; }
      if (BAD && r) {
        r.innerHTML = '<div class="em-res em-tone-warn"><div class="em-verdict warn">' + ICON.warn + "<p>Revisa los datos. " + esc(bad) + "</p></div></div>";
        r.style.display = "block"; say(r, "Revisa los datos. " + bad);
        if (BR) BR.hidden = true;
      }
      return !BAD;
    }
    function run() { clearTimeout(t); t = null; if (gate()) fn(); }
    function deb() { clearTimeout(t); t = setTimeout(run, wait || 250); }
    Array.prototype.forEach.call(list, function (i) {
      if (typeof i === "string") i = document.getElementById(i);
      if (!i) return;
      els.push(i); prep(i);
      i.addEventListener("input", function () { used1(); deb(); });
      i.addEventListener("change", function () { used1(); run(); });
      i.addEventListener("blur", function () { if (i._p) run(); });
    });
    run();
    return run;
  }


  /* UX2.5: «Aplicar este caso» (a.caso, href #v=id:valor~…): rellena el formulario, recalcula y sube al veredicto. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a.caso"); if (!a) return;
    var m = /v=([^&]*)/.exec(a.hash), f = 0; if (!m) return;
    m[1].split("~").forEach(function (p) { var k = p.split(":"), i = document.getElementById(decodeURIComponent(k[0])); if (i && i.form && k[1] !== undefined) { i.value = decodeURIComponent(k[1]); i.dispatchEvent(new Event("input", { bubbles: true })); f = 1; } });
    if (!f) return; e.preventDefault(); ev("caso_click");
    setTimeout(function () { var v = document.querySelector(".em-verdict") || document.getElementById("r"); if (v) v.scrollIntoView({ behavior: reduced() ? "auto" : "smooth", block: "center" }); }, 350);
  });

  window.EM = { renderResult: renderResult, live: live, eur: eur, num: num, _: { COLORS: COLORS, esc: esc, reduced: reduced } };
})();
