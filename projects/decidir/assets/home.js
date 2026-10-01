/* Entre Muchos — portada y catálogo: filtro instantáneo de tarjetas + movimiento del hero. */
(function () {
  "use strict";
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  function reduced() { return !!(RM && RM.matches); }
  /* Filtro instantáneo de tarjetas: <input data-filter="#lista"> filtra <li data-q="..."> */
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function initFilters() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-filter]"), function (inp) {
      var list = document.querySelector(inp.getAttribute("data-filter"));
      var empty = document.querySelector(inp.getAttribute("data-empty"));
      var count = document.querySelector(inp.getAttribute("data-count"));
      var chipBox = document.querySelector(inp.getAttribute("data-chips") || "x-none");
      var always = inp.hasAttribute("data-always"), tema = "";
      if (!list) return;
      var chips = chipBox ? Array.prototype.slice.call(chipBox.querySelectorAll("[data-t]")) : [];
      function setTema(t, silent) {
        tema = t;
        chips.forEach(function (c) { c.setAttribute("aria-pressed", c.getAttribute("data-t") === t ? "true" : "false"); });
        if (!silent) { try { history.replaceState(null, "", t ? "#" + t : location.pathname + location.search); } catch (e) {} }
      }
      function apply() {
        var q = norm(inp.value.trim()).split(/\s+/).filter(Boolean), shown = 0;
        Array.prototype.forEach.call(list.children, function (li) {
          var hay = norm(li.getAttribute("data-q") || li.textContent);
          var ok = q.every(function (w) { return hay.indexOf(w) >= 0; }) && (!tema || li.getAttribute("data-t") === tema);
          li.hidden = !ok; if (ok) shown++;
        });
        list.hidden = shown === 0;
        if (empty) empty.hidden = shown > 0;
        if (count) count.textContent = (q.length || tema || always) ? (shown === 0 ? "Sin resultados" : shown + (shown === 1 ? " calculadora" : " calculadoras")) : "";
      }
      chips.forEach(function (c) { c.addEventListener("click", function () { setTema(c.getAttribute("data-t")); apply(); }); });
      var reset = document.getElementById("reset");
      if (reset) reset.addEventListener("click", function () { inp.value = ""; setTema(""); apply(); inp.focus(); });
      inp.addEventListener("input", apply);
      var m = /[?&]q=([^&]*)/.exec(location.search);
      if (m) { try { inp.value = decodeURIComponent(m[1].replace(/\+/g, " ")); } catch (e) {} }
      var h = location.hash.slice(1);
      if (h && chips.some(function (c) { return c.getAttribute("data-t") === h; })) setTema(h, true);
      apply();
    });
  }
  function initHero() {
    if (reduced()) return;
    var ill = document.querySelector(".hero-ill");
    if (ill) {
      var mo = ill.querySelector("animateMotion");
      setTimeout(function () { if (mo && mo.beginElement) { try { mo.beginElement(); ill.classList.add("run"); } catch (e) {} } }, 1700);
      if ("IntersectionObserver" in window && ill.pauseAnimations) new IntersectionObserver(function (es) { if (es[0].isIntersecting) ill.unpauseAnimations(); else ill.pauseAnimations(); }).observe(ill);
      if (window.matchMedia("(pointer:fine)").matches) {
        var hero = ill.closest(".hero") || ill, raf = 0, mx = 0, my = 0;
        hero.addEventListener("pointermove", function (e) {
          var r = hero.getBoundingClientRect();
          mx = ((e.clientX - r.left) / r.width - 0.5) * 2; my = ((e.clientY - r.top) / r.height - 0.5) * 2;
          if (!raf) raf = requestAnimationFrame(function () { raf = 0; ill.style.setProperty("--mx", mx.toFixed(3)); ill.style.setProperty("--my", my.toFixed(3)); });
        });
        hero.addEventListener("pointerleave", function () { ill.style.setProperty("--mx", 0); ill.style.setProperty("--my", 0); });
      }
    }
  }
  function init() { initFilters(); initHero(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
