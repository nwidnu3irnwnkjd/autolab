/* Entre Muchos — módulo diferido: copiar/compartir y informe imprimible (PDF). Lo carga em.js al pulsar un botón o en reposo. */
(function () {
  "use strict";
  var U = window.EM._, esc = U.esc, num = EM.num;
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

  function doAct(b, box, o, hasBig, fmt) {
    var shareText = function () {
      var tmp = document.createElement("div"); tmp.innerHTML = o.verdict;
      var t = tmp.textContent.replace(/\s+/g, " ").trim();
      if (hasBig && t.indexOf(fmt(o.bigNumber)) < 0 && t.replace(/\s/g, "").indexOf(fmt(o.bigNumber).replace(/\s/g, "")) < 0) { var l = document.createElement("div"); l.innerHTML = o.bigLabel || ""; t += " (" + fmt(o.bigNumber) + (l.textContent ? " " + l.textContent.trim() : "") + ")"; }
      return t + "\n" + location.href.split("#")[0];
    };

    var toast = box.querySelector(".em-toast");
    var say = function (m) { toast.textContent = m; clearTimeout(box._t); box._t = setTimeout(function () { toast.textContent = ""; }, 2500); };
    var copy = function (txt, msg) {
      var done = function () { say(msg); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function () { fb(); });
      else fb();
      function fb() { var ta = document.createElement("textarea"); ta.value = txt; ta.style.cssText = "position:fixed;opacity:0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) { say("No se pudo copiar"); } document.body.removeChild(ta); }
    };
    var act = b.getAttribute("data-act");
    if (act === "print") { printReport(); return; }
    var txt = shareText();
    if (act === "share") {
      navigator.share({ title: document.title, text: txt.split("\n")[0], url: location.href.split("#")[0] }).catch(function (err) { if (err && err.name !== "AbortError") copy(location.href.split("#")[0], "Enlace copiado"); });
    } else copy(txt, "Resultado copiado");
  }
  window.EM._x = { act: doAct, print: printReport };
})();
