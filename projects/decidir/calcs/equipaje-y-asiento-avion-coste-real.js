// Billete de avion: low cost (base + maletas + extras) frente a tarifa normal (precio base con nincl maletas incluidas; las de mas se pagan al precio de maleta).
// Todo por pasajero y trayecto; los precios deben incluir tasas. Equilibrio: menor numero de maletas (0-20) con el que la normal sale mas barata.
var MAXMAL = 20, TOL = 0.005;
function pplc(d, n) { return d.lc + n * d.maleta + d.extras; }
function ppnor(d, n) { return d.normal + Math.max(0, n - d.nincl) * d.maleta; }
function calcular(d) {
  var m = d.pax * d.tray, ppL = pplc(d, d.nmal), ppN = ppnor(d, d.nmal), totL = ppL * m, totN = ppN * m, dif = totL - totN, n, nEq = -1;
  for (n = 0; n <= MAXMAL; n++) { if (pplc(d, n) - ppnor(d, n) > TOL) { nEq = n; break; } }
  return {
    totalLC: totL, totalNormal: totN, porPasajeroLC: ppL * d.tray, porPasajeroNormal: ppN * d.tray, porTrayectoLC: ppL, porTrayectoNormal: ppN,
    diferencia: dif, ganador: dif > TOL * m ? 1 : (dif < -TOL * m ? 0 : 2), nEq: nEq, extraEq: ppN - d.lc - d.nmal * d.maleta
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["lc", "normal", "maleta", "nmal", "nincl", "extras", "pax", "tray"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.pax < 1 || d.tray < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe al menos 1 pasajero y 1 trayecto.", tone: "warn", note: "<p>Sin pasajeros o trayectos no hay billete que comparar.</p>" });
    return;
  }
  if (d.pax > 9 || d.tray > 10 || d.nmal > 5 || d.nincl > 5 || Math.floor(d.pax) !== d.pax || Math.floor(d.tray) !== d.tray || Math.floor(d.nmal) !== d.nmal || Math.floor(d.nincl) !== d.nincl) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: de 1 a 9 pasajeros, de 1 a 10 trayectos y hasta 5 maletas, todo en números enteros.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, abs = Math.abs(r.diferencia), m = d.pax * d.tray, w, verdict;
  var pas = EM.num(d.pax, 0) + (d.pax === 1 ? " pasajero" : " pasajeros"), tr = EM.num(d.tray, 0) + (d.tray === 1 ? " trayecto" : " trayectos");
  var mal = function (n) { return EM.num(n, 0) + (n === 1 ? " maleta" : " maletas"); };
  if (g === 2) {
    w = "empate";
    verdict = "Con estos datos la low cost y la tarifa normal cuestan lo mismo para " + pas + " y " + tr + " (unos " + eur(r.totalLC) + "): estás en el punto de equilibrio.";
  } else if (g === 0) {
    w = "low cost";
    verdict = "Con estos datos compensa la low cost: te sale " + eur(abs) + " más barata que la tarifa normal para " + pas + " y " + tr + " con " + mal(d.nmal) + " por pasajero y trayecto" + (r.nEq > 0 ? ", pero con " + mal(r.nEq) + " o más la tarifa normal pasaría a salir más barata" : "") + ".";
  } else {
    w = "tarifa normal";
    verdict = "Con estos datos compensa la tarifa normal: te sale " + eur(abs) + " más barata que la low cost para " + pas + " y " + tr + " con " + mal(d.nmal) + " por pasajero y trayecto" + (r.nEq > 0 ? "; con menos de " + mal(r.nEq) + " la low cost saldría más barata" : "") + ".";
  }
  var note = "<p><strong>Lectura:</strong> la low cost cuesta " + eur(r.porTrayectoLC, 2) + " por pasajero y trayecto y la normal, " + eur(r.porTrayectoNormal, 2) + " (" + eur(r.porPasajeroLC) + " y " + eur(r.porPasajeroNormal) + " por pasajero en todo el viaje). ";
  if (r.nEq > 0) note += "La tarifa normal sale más barata a partir de <strong>" + mal(r.nEq) + "</strong> por pasajero y trayecto. ";
  else if (r.nEq === 0) note += "La tarifa normal sale más barata incluso sin maletas. ";
  else note += "Con estos precios la low cost sale más barata o igual con cualquier número de maletas (hasta " + MAXMAL + "). ";
  if (r.extraEq > 0) note += "Con tus " + mal(d.nmal) + ", la tarifa normal compensa si los extras de la low cost (asiento, embarque prioritario, comida) superan " + eur(r.extraEq, 2) + " por pasajero y trayecto; ahora son " + eur(d.extras, 2) + ".</p>";
  else note += "Con tus " + mal(d.nmal) + ", la tarifa normal compensa incluso con extras de 0 € en la low cost.</p>";
  note += "<p>Las políticas de equipaje, asiento y embarque cambian por aerolínea y por tarifa: pon lo que incluye <strong>tu</strong> billete. Se supone que los precios ya incluyen tasas, que la tarifa normal incluye " + mal(d.nincl) + " facturada(s) por pasajero y trayecto y que cada maleta adicional cuesta lo mismo que en la low cost. No incluye cambios o cancelaciones, seguros ni el equipaje de mano si no lo sumas en los extras.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: Math.min(r.totalLC, r.totalNormal), bigLabel: "€ en total para " + pas + " y " + tr + " con la tarifa más barata", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste total para " + pas + " y " + tr,
    bars: [{ label: "Low cost" + (w === "low cost" ? " (gana)" : ""), value: r.totalLC, color: "a" }, { label: "Tarifa normal" + (w === "tarifa normal" ? " (gana)" : ""), value: r.totalNormal, color: "b" }],
    cols: ["Low cost", "Tarifa normal"],
    rows: [
      ["Coste total", eur(r.totalLC), eur(r.totalNormal)],
      ["Por pasajero (todo el viaje)", eur(r.porPasajeroLC), eur(r.porPasajeroNormal)],
      ["Por pasajero y trayecto", eur(r.porTrayectoLC, 2), eur(r.porTrayectoNormal, 2)],
      ["Maletas con las que la normal sale más barata", "—", r.nEq < 0 ? "nunca" : String(r.nEq)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
