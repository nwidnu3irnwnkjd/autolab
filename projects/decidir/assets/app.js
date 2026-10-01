/* Entre Muchos — componente de resultado y utilidades. Sin dependencias. */
(function () {
  "use strict";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  var COLORS = { a: "var(--c1)", b: "var(--c2)", c: "var(--c3)", d: "var(--c4)", ok: "var(--ok)", warn: "var(--warn)" };
  var ICON = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>',
    warn: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.6v.1"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 11v6M12 7.5v.1"/></svg>'
  };
  function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function reduced() { return !!(RM && RM.matches); }
  var state = new WeakMap();

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

  /* EM.renderResult({verdict, tone:'ok'|'warn'|'info', bigNumber, bigLabel, format, bars:[{label,value,color}],
     barsLabel, cols:[...], rows:[[label, v1, v2] | {label, values, strong}], note, el}) */
  function renderResult(o) {
    var el = typeof o.el === "string" ? document.querySelector(o.el) : (o.el || document.getElementById("r"));
    if (!el) return;
    var tone = o.tone === "warn" || o.tone === "info" ? o.tone : "ok", fmt = o.format || eur;
    var prev = state.get(el) || {};
    el.setAttribute("aria-live", "polite");
    var h = '<div class="em-res em-tone-' + tone + '">';
    h += '<div class="em-verdict ' + tone + '">' + ICON[tone] + '<p>' + o.verdict + '</p></div>';
    var hasBig = typeof o.bigNumber === "number" && isFinite(o.bigNumber);
    if (hasBig) h += '<p class="em-big"><span class="num" aria-hidden="true"></span><span class="sr-only">' + esc(fmt(o.bigNumber)) + '</span><span class="lbl">' + (o.bigLabel || "") + '</span></p>';
    if (o.bars && o.bars.length) h += barsSvg(o.bars, fmt, o.barsLabel);
    if (o.rows && o.rows.length) h += table(o.cols || (o.bars || []).map(function (b) { return esc(b.label); }), o.rows);
    if (o.note) h += '<div class="em-note">' + o.note + '</div>';
    h += '</div>';
    var animateIn = !el.firstChild;
    el.innerHTML = h;
    if (!animateIn) { var res = el.firstChild; res.style.animation = "none"; }
    el.style.display = "block";
    if (hasBig) countTo(el.querySelector(".em-big .num"), prev.big === undefined ? 0 : prev.big, o.bigNumber, fmt);
    var rects = el.querySelectorAll(".br"), pf = prev.f || [], nf = [];
    for (var i = 0; i < rects.length; i++) {
      var f = parseFloat(rects[i].getAttribute("data-f")); nf.push(f);
      if (reduced()) { rects[i].style.transform = "scaleX(" + f + ")"; continue; }
      rects[i].style.transform = "scaleX(" + (pf[i] !== undefined ? pf[i] : 0) + ")";
    }
    if (!reduced() && rects.length) {
      el.getBoundingClientRect();
      requestAnimationFrame(function () { for (var j = 0; j < rects.length; j++) rects[j].style.transform = "scaleX(" + nf[j] + ")"; });
    }
    state.set(el, { big: hasBig ? o.bigNumber : undefined, f: nf });
  }

  /* EM.live(inputs, fn, wait): recalcula al cambiar cualquier input (debounce). inputs: selector, formulario, o lista. */
  function live(inputs, fn, wait) {
    var list;
    if (typeof inputs === "string") list = document.querySelectorAll(inputs);
    else if (inputs && inputs.tagName === "FORM") list = inputs.querySelectorAll("input,select,textarea");
    else list = inputs || [];
    var t = null;
    function run() { clearTimeout(t); t = null; fn(); }
    function deb() { clearTimeout(t); t = setTimeout(run, wait || 250); }
    Array.prototype.forEach.call(list, function (i) {
      if (typeof i === "string") i = document.getElementById(i);
      if (!i) return;
      i.addEventListener("input", deb);
      i.addEventListener("change", run);
    });
    run();
    return run;
  }

  /* Filtro instantáneo de tarjetas: <input data-filter="#lista"> filtra <li data-q="..."> */
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function initFilters() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), function (inp) {
      var list = document.querySelector(inp.getAttribute("data-filter"));
      var empty = document.querySelector(inp.getAttribute("data-empty"));
      var count = document.querySelector(inp.getAttribute("data-count"));
      if (!list) return;
      function apply() {
        var q = norm(inp.value.trim()).split(/\s+/).filter(Boolean), shown = 0;
        Array.prototype.forEach.call(list.children, function (li) {
          var hay = norm(li.getAttribute("data-q") || li.textContent);
          var ok = q.every(function (w) { return hay.indexOf(w) >= 0; });
          li.hidden = !ok; if (ok) shown++;
        });
        if (empty) empty.hidden = shown > 0;
        if (count) count.textContent = q.length ? shown + (shown === 1 ? " calculadora encontrada" : " calculadoras encontradas") : "";
      }
      inp.addEventListener("input", apply);
      apply();
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initFilters); else initFilters();

  window.EM = { renderResult: renderResult, live: live, eur: eur };
})();
