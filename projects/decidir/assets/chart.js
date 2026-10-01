/* Entre Muchos — EM.lineChart (gráfico de línea SVG). Se carga solo en páginas cuya calculadora lo usa (build.py lo detecta). */
(function () {
  "use strict";
  var U = window.EM._, COLORS = U.COLORS, esc = U.esc, reduced = U.reduced, num = EM.num, eur = EM.eur;
  /* EM.lineChart({series:[{label,color:'a'|'b'|'c'|'d'|css,points:[[x,y],...]}], xLabel, yFormat, xFormat, caption, el})
     Devuelve <figure class="em-line">; con `el` (selector o nodo) lo añade ahí. Se dibuja al medir su ancho (ResizeObserver). */
  var DASH = ["", "7 5", "2 4"];
  function lineChart(o) {
    var S = (o.series || []).filter(function (s) { return s.points && s.points.length; }).slice(0, 3);
    var yf = o.yFormat || eur, xf = o.xFormat || function (x) { return String(x); };
    var fig = document.createElement("figure"); fig.className = "em-line";
    if (!S.length) return fig;
    var xs = S[0].points.map(function (p) { return p[0]; }), X0 = xs[0], X1 = xs[xs.length - 1], lo = Infinity, hi = -Infinity;
    S.forEach(function (s) { s.points.forEach(function (p) { lo = Math.min(lo, p[1]); hi = Math.max(hi, p[1]); }); });
    if (lo > 0 && lo < hi * 0.35) lo = 0;
    if (hi === lo) hi = lo + 1;
    var st = Math.pow(10, Math.floor(Math.log(hi - lo) / Math.LN10 - 0.3)), m = [1, 2, 2.5, 5, 10], k = 0;
    while ((hi - lo) / (st * m[k]) > 5 && k < 4) k++;
    st *= m[k]; lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
    var tick = o.yFormat ? o.yFormat : function (v) { return Math.abs(v) >= 1000 ? num(v / 1000, st < 1000 ? 1 : 0).replace(",0", "") + " k€" : eur(v); };
    var col = S.map(function (s, i) { return COLORS[s.color] || s.color || COLORS[["a", "b", "c"][i]]; });
    var cap = '<figcaption>' + esc(o.caption || "Evolución en el tiempo") + '</figcaption><ul class="em-lg">' +
      S.map(function (s, i) { return '<li><svg width="26" height="10" aria-hidden="true"><path d="M1 5h24" stroke="' + col[i] + '" stroke-width="3" stroke-linecap="round" stroke-dasharray="' + DASH[i] + '"/></svg>' + esc(s.label) + '</li>'; }).join("") + '</ul>';
    var tb = '<table class="sr-only"><caption>' + esc(o.caption || "Evolución en el tiempo") + '</caption><thead><tr><th scope="col">' + esc(o.xLabel || "Periodo") + '</th>' +
      S.map(function (s) { return '<th scope="col">' + esc(s.label) + '</th>'; }).join("") + '</tr></thead><tbody>' +
      xs.map(function (x, i) { return '<tr><th scope="row">' + esc(xf(x)) + '</th>' + S.map(function (s) { return '<td>' + (s.points[i] ? esc(yf(s.points[i][1])) : "") + '</td>'; }).join("") + '</tr>'; }).join("") + '</tbody></table>';
    fig.innerHTML = cap + '<div class="em-lw"></div><div class="em-tip" hidden></div>' + tb;
    var wrap = fig.querySelector(".em-lw"), tip = fig.querySelector(".em-tip"), W0 = 0, first = true, idx = -1, g = {};
    function X(x) { return g.l + (x - X0) / (X1 - X0 || 1) * (g.w - g.l - g.r); }
    function Y(y) { return g.t + (1 - (y - lo) / (hi - lo)) * (g.h - g.t - g.b); }
    function draw() {
      var W = Math.max(wrap.clientWidth, 220), H = Math.round(Math.min(Math.max(W * 0.62, 210), 320)), tl = [];
      for (var v = lo; v <= hi + st / 1e6; v += st) tl.push(v);
      var lw = Math.max.apply(null, tl.map(function (v) { return tick(v).length; })) * 6.6 + 12;
      g = { w: W, h: H, l: Math.round(lw), r: 14, t: 12, b: o.xLabel ? 44 : 28 };
      var sv = '<svg width="' + W + '" height="' + H + '" role="img" aria-label="' + esc((o.caption || "Gráfico de evolución") + ": " + S.map(function (s) { var a = s.points[0], z = s.points[s.points.length - 1]; return s.label + " de " + yf(a[1]) + " a " + yf(z[1]); }).join("; ") + ". Hay una tabla con todos los datos justo debajo.") + '">';
      tl.forEach(function (v) { sv += '<line class="gl" x1="' + g.l + '" x2="' + (W - g.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '"/><text class="ax" x="' + (g.l - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + esc(tick(v)) + '</text>'; });
      var nx = Math.max(2, Math.min(xs.length, Math.floor((W - g.l) / 64))), sk = Math.ceil(xs.length / nx);
      xs.forEach(function (x, i) { if (i % sk === 0 || i === xs.length - 1 && (xs.length - 1) % sk > sk / 2) sv += '<text class="ax" x="' + X(x) + '" y="' + (H - g.b + 18) + '" text-anchor="' + (i === 0 ? "start" : "middle") + '">' + esc(xf(x)) + '</text>'; });
      if (o.xLabel) sv += '<text class="ax xl" x="' + (g.l + (W - g.l - g.r) / 2) + '" y="' + (H - 6) + '" text-anchor="middle">' + esc(o.xLabel) + '</text>';
      S.forEach(function (s, i) {
        sv += '<path class="ll" pathLength="1" d="' + s.points.map(function (p, j) { return (j ? "L" : "M") + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1); }).join("") + '" stroke="' + col[i] + '"' + (DASH[i] ? ' stroke-dasharray="' + DASH[i] + '"' : "") + '/>';
      });
      sv += '<line class="cur" y1="' + g.t + '" y2="' + (H - g.b) + '" hidden/>' + S.map(function (s, i) { return '<circle class="dt" r="5" fill="' + col[i] + '" hidden/>'; }).join("") +
        '<rect class="hit" x="' + g.l + '" y="0" width="' + (W - g.l) + '" height="' + (H - g.b) + '" tabindex="0" aria-label="Recorre el gráfico con las flechas izquierda y derecha"/></svg>';
      wrap.innerHTML = sv;
      var paths = wrap.querySelectorAll(".ll");
      if (first && !reduced()) {
        Array.prototype.forEach.call(paths, function (p, i) { p.style.strokeDasharray = "1"; p.style.strokeDashoffset = "1"; p.style.transitionDelay = i * 150 + "ms"; });
        wrap.getBoundingClientRect();
        requestAnimationFrame(function () { Array.prototype.forEach.call(paths, function (p, i) { p.style.strokeDashoffset = "0"; p.addEventListener("transitionend", function () { p.style.strokeDasharray = DASH[i]; p.style.strokeDashoffset = ""; }, { once: true }); }); });
      }
      first = false;
      var hit = wrap.querySelector(".hit"), svg = wrap.firstChild;
      function at(e) {
        var r = svg.getBoundingClientRect(), px = e.clientX - r.left, best = 0, bd = 1e9;
        xs.forEach(function (x, i) { var d = Math.abs(X(x) - px); if (d < bd) { bd = d; best = i; } });
        show(best);
      }
      hit.addEventListener("pointermove", at); hit.addEventListener("pointerdown", at);
      hit.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hide(); });
      hit.addEventListener("blur", hide);
      hit.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0; if (!d) { if (e.key === "Escape") hide(); return; }
        e.preventDefault(); show(Math.max(0, Math.min(xs.length - 1, (idx < 0 ? (d > 0 ? -1 : xs.length) : idx) + d)));
      });
      if (idx >= 0) show(idx);
    }
    function show(i) {
      idx = i; var svg = wrap.firstChild; if (!svg) return;
      var x = X(xs[i]), cur = svg.querySelector(".cur"); cur.setAttribute("x1", x); cur.setAttribute("x2", x); cur.removeAttribute("hidden");
      var h = "<b>" + esc(o.xFormat || !o.xLabel ? xf(xs[i]) : o.xLabel + " " + xf(xs[i])) + "</b>";
      Array.prototype.forEach.call(svg.querySelectorAll(".dt"), function (d, j) {
        var p = S[j].points[i]; if (!p) return;
        d.setAttribute("cx", x); d.setAttribute("cy", Y(p[1])); d.removeAttribute("hidden");
        h += '<span><i style="background:' + col[j] + '"></i>' + esc(S[j].label) + ' <em>' + esc(yf(p[1])) + '</em></span>';
      });
      tip.innerHTML = h; tip.hidden = false;
      var tw = tip.offsetWidth, left = wrap.offsetLeft + x - tw / 2;
      tip.style.left = Math.max(0, Math.min(left, fig.clientWidth - tw)) + "px"; tip.style.top = wrap.offsetTop + g.t + "px";
    }
    function hide() { idx = -1; tip.hidden = true; Array.prototype.forEach.call(wrap.querySelectorAll(".cur,.dt"), function (n) { n.setAttribute("hidden", ""); }); }
    function go() { var w = wrap.clientWidth; if (w && w !== W0) { W0 = w; draw(); } }
    if (window.ResizeObserver) new ResizeObserver(go).observe(wrap); else { window.addEventListener("resize", go); setTimeout(go, 0); }
    if (o.el) { var t = typeof o.el === "string" ? document.querySelector(o.el) : o.el; if (t) { t.innerHTML = ""; t.appendChild(fig); } }
    return fig;
  }

  EM.lineChart = lineChart;
})();
