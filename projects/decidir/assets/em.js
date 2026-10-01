/* Entre Muchos — componente de resultado (EM.renderResult, EM.live, informe imprimible). Solo en calculadoras. */
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
    if (o.line) h += '<div class="em-line-slot"></div>';
    if (o.rows && o.rows.length) h += table(o.cols || (o.bars || []).map(function (b) { return esc(b.label); }), o.rows);
    if (o.note) h += '<div class="em-note">' + o.note + '</div>';
    h += '<div class="em-share"><button type="button" class="btn2" data-act="copy">' + ICON.copy + 'Copiar resultado</button>' +
      (navigator.share ? '<button type="button" class="btn2" data-act="share">' + ICON.share + 'Compartir</button>' : '') +
      '<button type="button" class="btn2" data-act="print">' + ICON.pdf + 'Descargar informe (PDF)</button>' +
      '<span class="em-toast" role="status" aria-live="polite"></span></div>';
    h += '</div>';
    var tmpV = document.createElement("div"); tmpV.innerHTML = o.verdict;
    var key = o.winner !== undefined ? String(o.winner) : tone + "|" + tmpV.textContent.replace(/[\d.,%€\s\u00a0+\-−]+/g, " ").trim();
    var animateIn = !el.firstChild;
    el.innerHTML = h;
    if (!animateIn) { var res = el.firstChild; res.style.animation = "none"; }
    if (prev.key !== undefined && prev.key !== key && !reduced()) el.querySelector(".em-verdict").classList.add("em-win");
    el.style.display = "block";
    if (o.line && window.EM.lineChart) { var slot = el.querySelector(".em-line-slot"); if (slot) slot.appendChild(window.EM.lineChart(o.line)); }
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
    var shareText = function () {
      var tmp = document.createElement("div"); tmp.innerHTML = o.verdict;
      var t = tmp.textContent.replace(/\s+/g, " ").trim();
      if (hasBig && t.indexOf(fmt(o.bigNumber)) < 0 && t.replace(/\s/g, "").indexOf(fmt(o.bigNumber).replace(/\s/g, "")) < 0) { var l = document.createElement("div"); l.innerHTML = o.bigLabel || ""; t += " (" + fmt(o.bigNumber) + (l.textContent ? " " + l.textContent.trim() : "") + ")"; }
      return t + "\n" + location.href.split("#")[0];
    };
    var box = el.querySelector(".em-share");
    if (box && !box._b) {
      box._b = 1;
      var toast = box.querySelector(".em-toast");
      var say = function (m) { toast.textContent = m; clearTimeout(box._t); box._t = setTimeout(function () { toast.textContent = ""; }, 2500); };
      var copy = function (txt, msg) {
        var done = function () { say(msg); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function () { fb(); });
        else fb();
        function fb() { var ta = document.createElement("textarea"); ta.value = txt; ta.style.cssText = "position:fixed;opacity:0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) { say("No se pudo copiar"); } document.body.removeChild(ta); }
      };
      box.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        var txt = shareText();
        if (b.getAttribute("data-act") === "print") { printReport(); return; }
        if (b.getAttribute("data-act") === "share") {
          navigator.share({ title: document.title, text: txt.split("\n")[0], url: location.href.split("#")[0] }).catch(function (err) { if (err && err.name !== "AbortError") copy(location.href.split("#")[0], "Enlace copiado"); });
        } else copy(txt, "Resultado copiado");
      });
    }
    state.set(el, { big: hasBig ? o.bigNumber : undefined, f: nf, key: key });
  }

  /* Informe imprimible (PDF): cabecera + datos introducidos + resultado + supuestos/disclaimer/URL. El CSS @media print oculta el resto. */
  function mk(id, cls) { var d = document.getElementById(id); if (!d) { d = document.createElement("div"); d.id = id; d.className = cls || ""; } return d; }
  function prepPrint() {
    var main = document.querySelector("main"), calc = main && main.querySelector(".calc"), res = calc && calc.querySelector(".em-res");
    if (!res) return false;
    var h1 = main.querySelector("h1"), form = document.getElementById("f"), now = new Date(), rows = "";
    if (form) Array.prototype.forEach.call(form.querySelectorAll(".grid > div"), function (w) {
      var l = w.querySelector("label"), c = w.querySelector("input,select"); if (!l || !c) return;
      var v = c.tagName === "SELECT" ? c.options[c.selectedIndex].text : (isFinite(+c.value) && c.value !== "" ? num(+c.value, +c.value % 1 ? 2 : 0).replace(/(,\d*?)0+$/, "$1").replace(/,$/, "") : c.value);
      rows += "<li><span>" + l.innerHTML + "</span><b>" + esc(v) + "</b></li>";
    });
    var head = mk("em-pr-head");
    head.innerHTML = '<div class="pr-top"><span class="pr-brand">entre <b>muchos</b></span><span>' + now.toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" }) + '</span></div>' +
      '<p class="pr-kicker">Informe de decisión</p><h1>' + (h1 ? esc(h1.textContent) : esc(document.title)) + '</h1>' +
      (rows ? '<h2>Datos introducidos</h2><ul class="pr-in">' + rows + '</ul>' : '') + '<h2>Resultado</h2>';
    var foot = mk("em-pr-foot"), h = "";
    Array.prototype.forEach.call(main.querySelectorAll("h2"), function (x) {
      if (/^Supuestos/i.test(x.textContent)) {
        h += "<h2>Supuestos y fuentes</h2>";
        for (var n = x.nextElementSibling; n && n.tagName !== "H2"; n = n.nextElementSibling) if (/(^|\s)(note|disclaimer)(\s|$)/.test(n.className)) h += n.outerHTML;
      }
    });
    foot.innerHTML = h + '<p class="pr-url">' + esc(location.href.split("#")[0]) + '<br>Informe generado en tu navegador; tus datos no se envían a ningún servidor.</p>';
    main.insertBefore(head, calc); main.insertBefore(foot, calc.nextSibling);
    document.body.classList.add("em-pr");
    return true;
  }
  function printReport() { if (prepPrint()) window.print(); }
  window.addEventListener("beforeprint", prepPrint);
  window.addEventListener("afterprint", function () { document.body.classList.remove("em-pr"); });

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


  window.EM = { renderResult: renderResult, live: live, eur: eur, num: num, _: { COLORS: COLORS, esc: esc, reduced: reduced } };
})();
