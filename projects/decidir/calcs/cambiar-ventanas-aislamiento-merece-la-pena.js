// Ventanas / aislamiento: amortizacion con tu gasto, tu % de ahorro y tu coste. Sin datos legales: todo lo pone el usuario.
// ahorro del año t = gasto * pct * (1+subida)^(t-1). Amortizacion = año (con fraccion lineal dentro del año) en que el acumulado iguala el coste neto.
var MAXANOS = 60;
function payback(net, a1, g, r, desc) {
  if (net <= 0) return 0;
  if (a1 <= 0) return -1;
  var cum = 0, t, s;
  for (t = 1; t <= MAXANOS; t++) {
    s = a1 * Math.pow(1 + g, t - 1); if (desc) s = s / Math.pow(1 + r, t);
    if (cum + s >= net) return t - 1 + (net - cum) / s;
    cum += s;
  }
  return -1;
}
function calcular(d) {
  var g = d.subida / 100, r = d.tasa / 100, net = Math.max(d.coste - d.ayuda, 0), a1 = d.gasto * d.ahorro / 100, n = Math.round(d.anos);
  var acum = 0, vanAcc = 0, fac = 0, facD = 0, t;
  for (t = 1; t <= n; t++) {
    var s = a1 * Math.pow(1 + g, t - 1); acum += s; vanAcc += s / Math.pow(1 + r, t);
    fac += Math.pow(1 + g, t - 1); facD += Math.pow(1 + g, t - 1) / Math.pow(1 + r, t);
  }
  var pb = payback(net, a1, g, r, false), pbd = payback(net, a1, g, r, true);
  var minPct = d.gasto > 0 && fac > 0 ? net / (d.gasto * fac) * 100 : -1, minPctVan = d.gasto > 0 && facD > 0 ? net / (d.gasto * facD) * 100 : -1;
  var ok = pb >= 0 && pb <= n;
  return {
    neto: net, ahorroAnual1: a1, anosSimple: a1 > 0 ? net / a1 : -1, anosAmort: pb, anosDesc: pbd,
    ahorroAcum: acum, saldoAcum: acum - net, van: vanAcc - net, minPct: minPct, minPctVan: minPctVan,
    compensa: ok ? 1 : 0, compensaVan: vanAcc - net >= 0 ? 1 : 0
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["gasto", "ahorro", "coste", "ayuda", "anos", "subida", "tasa"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function an(x) { return x < 0 ? "más de " + MAXANOS + " años" : EM.num(x, 1) + " años"; }
function pintar() {
  var d = leer();
  if (d.gasto < 0 || d.coste < 0 || d.ayuda < 0 || d.anos < 1 || d.anos > 60 || d.subida < -20 || d.tasa < -5) return;
  if (d.ahorro < 0 || d.ahorro > 80) {
    EM.renderResult({ winner: "invalido", verdict: "El porcentaje de ahorro debe estar entre 0 y 80 %.", tone: "warn",
      note: "<p>Un ahorro del 100 % significaría no gastar nada en climatización, y por encima del 80 % no es un supuesto realista para ventanas o aislamiento. Revisa el dato.</p>" });
    return;
  }
  if (d.ayuda > d.coste) {
    EM.renderResult({ winner: "invalido", verdict: "La ayuda no puede ser mayor que el coste de la actuación.", tone: "warn",
      note: "<p>Escribe solo el importe de ayuda o deducción que tengas confirmado y que no supere lo que pagas.</p>" });
    return;
  }
  var r = calcular(d), n = Math.round(d.anos), c = r.compensa === 1, v = c ? "compensa" : "no";
  var verdict = d.coste - d.ayuda <= 0 ? "Sin coste neto, la actuación no tiene nada que amortizar: lo que ahorres es ganancia."
    : r.ahorroAnual1 <= 0 ? "Con un ahorro del 0 %, la actuación no se amortiza nunca."
    : c ? "Con estos supuestos, el ahorro acumulado cubre el coste en " + an(r.anosAmort) + ", dentro de tu horizonte de " + n + " años."
    : "Con estos supuestos, el ahorro no cubre el coste en " + n + " años: se amortizaría en " + an(r.anosAmort) + ".";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.neto > 0 && r.ahorroAnual1 > 0) {
    note += "ahorras " + EM.eur(r.ahorroAnual1) + " el primer año sobre un coste neto de " + EM.eur(r.neto) + " (amortización simple, sin subida de la energía: " + an(r.anosSimple) + "; con la subida que indicas: " + an(r.anosAmort) + "; valorando el dinero a tu tasa: " + an(r.anosDesc) + "). ";
    note += "Para amortizarla en " + n + " años necesitarías ahorrar al menos un <strong>" + EM.num(r.minPct, 1) + " %</strong> de tu gasto (" + EM.num(r.minPctVan, 1) + " % si descuentas el dinero a tu tasa). ";
    note += r.compensa === 1 && r.compensaVan === 0 ? "Ojo: amortiza en años, pero con la tasa que has puesto el VAN a " + n + " años es negativo. " : "";
  } else if (r.neto > 0) note += "con ahorro cero no hay amortización posible; el mínimo para amortizar en " + n + " años sería " + EM.num(r.minPct, 1) + " % de tu gasto. ";
  note += "</p><p><strong>Ojo:</strong> el ahorro real depende de cómo esté hoy tu vivienda, del aislamiento, de tus hábitos y de la orientación: el porcentaje es tu supuesto, no una promesa (según el IDAE, mejorar las ventanas puede reducir hasta un 45 % las pérdidas de calor de la vivienda en su ejemplo; tu caso puede ser mucho menor). Esta cuenta no pone precio al confort, al ruido ni a las humedades o condensaciones, que a veces son la razón real para reformar. No incluye la vida útil de la obra (se calcula solo hasta tu horizonte), ni financiación ni mantenimiento. Las deducciones del IRPF por eficiencia energética (20 %, 40 % o 60 % según el caso y con límites) tienen requisitos y certificado: consulta requisitos y, si las tienes confirmadas, mete su importe en «Ayudas».</p>";
  EM.renderResult({
    winner: v, verdict: verdict, tone: c || d.coste - d.ayuda <= 0 ? "ok" : "warn",
    bigNumber: r.saldoAcum, bigLabel: r.saldoAcum >= 0 ? "de ahorro neto acumulado en " + n + " años (ahorro menos coste)" : "te faltan por recuperar en " + n + " años",
    format: function (x) { return EM.eur(Math.abs(x)); },
    barsLabel: "Coste neto frente al ahorro acumulado en " + n + " años",
    bars: [{ label: "Coste neto de la actuación", value: r.neto, color: "a" }, { label: "Ahorro acumulado", value: r.ahorroAcum, color: "b" }],
    cols: ["Resultado"],
    rows: [
      ["Ahorro el primer año", EM.eur(r.ahorroAnual1)],
      ["Años de amortización simple", r.anosSimple < 0 ? "no se amortiza" : EM.num(r.anosSimple, 1)],
      ["Años con subida de la energía", r.anosAmort < 0 ? "más de " + MAXANOS : EM.num(r.anosAmort, 1)],
      ["Años descontando a tu tasa", r.anosDesc < 0 ? "más de " + MAXANOS : EM.num(r.anosDesc, 1)],
      ["Ahorro acumulado en " + n + " años", EM.eur(r.ahorroAcum)],
      ["VAN a " + n + " años (a tu tasa)", EM.eur(r.van)],
      ["% mínimo de ahorro para amortizar en " + n + " años", r.minPct < 0 ? "—" : EM.num(r.minPct, 1) + " %"]
    ],
    note: note
  });
}
(function () {
  var s = document.getElementById("ahorroSel"), a = document.getElementById("ahorro");
  s.value = "20"; a.value = "20";
  s.addEventListener("change", function () { a.value = s.value; pintar(); });
})();
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
