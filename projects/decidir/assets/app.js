/* Entre Muchos — núcleo: navegación activa, pulsación de botones y revelado al hacer scroll. Sin dependencias. */
(function () {
  "use strict";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  function reduced() { return !!(RM && RM.matches); }
  /* Movimiento: revelado al hacer scroll, parallax del hero, pulsación de botones, nav activa */
  function initMotion() {
    var path = location.pathname;
    Array.prototype.forEach.call(document.querySelectorAll(".site-h nav a"), function (a) {
      var h = a.getAttribute("href"); if (h !== "/" && path.indexOf(h) === 0) a.setAttribute("aria-current", "page");
    });
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("button:not(.chip),.btn"); if (!b || reduced()) return;
      b.classList.remove("tap"); void b.offsetWidth; b.classList.add("tap");
    });
    if (reduced()) return;
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          var t = en.target; io.unobserve(t); t.classList.add("in");
          setTimeout(function () { t.classList.remove("rv", "in"); t.style.removeProperty("--rd"); }, 1100);
        });
      }, { rootMargin: "0px 0px -24px 0px" });
      var vh = window.innerHeight;
      Array.prototype.forEach.call(document.querySelectorAll("main h2, ul.cards>li, ul.guides>li, .steps>li, .trust>div, main details, article.guide table"), function (n) {
        if (n.getBoundingClientRect().top < vh * 0.95) return;
        var sib = n.parentNode ? Array.prototype.indexOf.call(n.parentNode.children, n) : 0;
        n.classList.add("rv"); n.style.setProperty("--rd", (/^(LI|DIV)$/.test(n.tagName) ? (sib % 4) * 70 : 0) + "ms"); io.observe(n);
      });
    }
  }
  /* Tablas de guías: etiqueta por celda (data-label) y roles ARIA para conservar la semántica al apilarse en tarjetas a ≤ 480 px */
  function initTables() {
    Array.prototype.forEach.call(document.querySelectorAll("article.guide table"), function (t) {
      var hs = Array.prototype.map.call(t.querySelectorAll("thead th"), function (h) { return h.textContent.trim(); });
      t.setAttribute("role", "table");
      Array.prototype.forEach.call(t.querySelectorAll("thead,tbody"), function (g) { g.setAttribute("role", "rowgroup"); });
      Array.prototype.forEach.call(t.rows, function (r) {
        r.setAttribute("role", "row");
        Array.prototype.forEach.call(r.cells, function (c, i) {
          c.setAttribute("role", c.tagName === "TH" ? (c.parentNode.parentNode.tagName === "THEAD" ? "columnheader" : "rowheader") : "cell");
          if (hs[i] && c.tagName === "TD") c.setAttribute("data-label", hs[i]);
        });
      });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initTables); else initTables();
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initMotion); else initMotion();
})();
