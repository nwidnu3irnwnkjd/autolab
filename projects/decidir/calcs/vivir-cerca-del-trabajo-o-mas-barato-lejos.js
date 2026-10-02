// Vivir cerca del trabajo o mas lejos y mas barato. Solo cuenta la DIFERENCIA entre las dos opciones (lo que es igual en ambas se cancela).
// Ahorro de alquiler/cuota = (cerca - lejos) x 12. Desplazamiento extra = km extra de ida x 2 x dias x coste por km + abono extra x 12.
// Tiempo extra = minutos extra de ida x 2 x dias / 60, valorado a la hora que pone el usuario (0 = no se valora). Ahorro neto de vivir lejos = ahorro de alquiler - desplazamiento - tiempo valorado.
// Empate practico: |neto| < 5 % del mayor coste anual de vivienda mas desplazamiento (alquiler/cuota + extras).
function calcular(d) {
  var A = (d.alq_cerca - d.alq_lejos) * 12;
  var kmCoste = d.km * 2 * d.dias * d.cpk, abonoAnual = d.abono * 12, desplaz = kmCoste + abonoAnual;
  var horas = d.min * 2 * d.dias / 60, tiempoVal = horas * d.vh, extra = desplaz + tiempoVal;
  var neto = A - extra, netoSin = A - desplaz;
  var costeCerca = d.alq_cerca * 12, costeLejos = d.alq_lejos * 12 + extra;
  var base = Math.max(costeCerca, costeLejos);
  var tipo = Math.abs(neto) < 0.05 * base ? 2 : (neto > 0 ? 0 : 1);
  var vhEq = (horas > 0 && netoSin > 0) ? netoSin / horas : -1;
  var minKm = d.km > 0 ? d.min / d.km : 0;
  var den = 2 * d.dias * (d.cpk + d.vh * minKm / 60), rest = A - abonoAnual;
  var kmEq = (den > 0 && rest > 0) ? rest / den : -1;
  return { ahorroAlquiler: A, kmCoste: kmCoste, abonoAnual: abonoAnual, desplaz: desplaz, horas: horas, tiempoVal: tiempoVal, extra: extra,
    neto: neto, netoSin: netoSin, costeCerca: costeCerca, costeLejos: costeLejos, tipo: tipo, vhEq: vhEq, alqEq: d.alq_lejos + extra / 12, kmEq: kmEq };
}
function eur(x, d) { return EM.eur(x, d); }
var IDS = ["alq_cerca", "alq_lejos", "km", "min", "cpk", "abono", "dias", "vh"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function hh(x) { return EM.num(x, 0) + " h"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.alq_cerca <= 0 || d.alq_lejos <= 0 || d.dias <= 0) { aviso("Escribe el alquiler o la cuota de las dos opciones y los días al año que vas al trabajo, todos mayores que 0.", "Sin precio de vivienda en las dos opciones o sin días de desplazamiento no hay nada que comparar."); return; }
  if (d.dias > 365 || d.cpk > 2 || d.km > 300 || d.min > 300 || d.vh > 500) { aviso("Revisa los límites: hasta 365 días al año, 300 km y 300 minutos extra de ida, 2 €/km y 500 €/h.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), t = r.tipo, w, v, a = Math.abs(r.neto);
  var tiempoTxt = d.vh > 0 ? " (incluye tu tiempo a " + eur(d.vh, 2) + " la hora)" : "";
  if (t === 2) {
    w = "empate";
    v = "Con tus datos, es un empate práctico: la diferencia es de " + eur(a) + " al año" + tiempoTxt + ", menos del 5 % del coste de vivienda y desplazamiento. Decide por lo que no sale en la cuenta: tiempo libre, entorno y tu rutina.";
  } else if (t === 0) {
    w = "lejos";
    v = "Con tus datos, vivir lejos gana por " + eur(a) + " al año" + tiempoTxt + ": ahorras " + eur(r.ahorroAlquiler) + " de alquiler o cuota y el desplazamiento extra cuesta " + eur(r.desplaz) + (d.vh > 0 ? " más " + eur(r.tiempoVal) + " de tiempo" : "") + ".";
    if (d.vh <= 0 && r.vhEq > 0) v += " No valoras tu tiempo: las " + hh(r.horas) + " extra al año compensan mientras tu hora valga menos de " + eur(r.vhEq, 2) + ".";
  } else {
    w = "cerca";
    v = "Con tus datos, vivir cerca gana por " + eur(a) + " al año" + tiempoTxt + ": ";
    if (r.ahorroAlquiler <= 0) v += "vivir lejos ni siquiera te ahorra alquiler o cuota, y encima suma " + eur(r.desplaz) + " de desplazamiento.";
    else v += "el alquiler o cuota que ahorras (" + eur(r.ahorroAlquiler) + ") no cubre " + eur(r.extra) + " de desplazamiento" + (d.vh > 0 ? " y tiempo" : "") + ".";
    if (d.vh > 0 && r.netoSin > 0) v += " Sin valorar tu tiempo, vivir lejos ahorraría " + eur(r.netoSin) + ": solo gana si tu hora vale menos de " + eur(r.vhEq, 2) + ".";
  }
  var eq = "<p><strong>Puntos de equilibrio:</strong> vivir lejos compensa si el alquiler o cuota de cerca supera " + eur(r.alqEq, 2) + " al mes";
  eq += r.kmEq > 0 ? "; o hasta unos " + EM.num(r.kmEq, 1) + " km extra de ida (con el mismo coste por km y los mismos minutos por km)" : (r.ahorroAlquiler - r.abonoAnual > 0 ? "" : "; con estos precios no hay distancia extra que compense");
  eq += r.vhEq > 0 ? "; o mientras tu hora valga menos de " + eur(r.vhEq, 2) + "." : ".";
  eq += "</p>";
  var note = "<p><strong>Lectura:</strong> el cálculo solo compara la diferencia entre las dos opciones: " + EM.num(d.dias, 0) + " días al año de ida y vuelta, " + hh(r.horas) + " extra al año de desplazamiento" + (d.vh > 0 ? " valoradas a " + eur(d.vh, 2) + " la hora" : " (sin valorar, tú decides cuánto vale)") + ".</p>" + eq;
  note += "<p><strong>Condiciones y límites:</strong> los precios de vivienda, el abono de transporte, los kilómetros, los minutos y el valor de la hora son datos tuyos o ejemplos editables, no cifras de ninguna ciudad. El coste por km del coche incluye combustible y desgaste de ejemplo; no incluye aparcamiento, peajes ni el seguro, que sumas en el abono extra si cambian. No incluye gastos de la vivienda que cambian de zona (suministros, comunidad, impuestos locales), la comida fuera, ni el valor de lo que haces con el tiempo libre. Información orientativa, no asesoramiento.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: "ok",
    bigNumber: a, format: EM.eur,
    bigLabel: t === 2 ? "de diferencia al año (empate práctico)" : (t === 0 ? "al año más barato vivir lejos" : "al año más barato vivir cerca"),
    barsLabel: "Coste anual de vivienda y desplazamiento",
    bars: [{ label: "Vivir cerca" + (t === 1 ? " (gana)" : ""), value: r.costeCerca, color: "a", fmt: EM.eur }, { label: "Vivir lejos" + (t === 0 ? " (gana)" : ""), value: r.costeLejos, color: "b", fmt: EM.eur }],
    cols: ["Vivir cerca", "Vivir lejos"],
    rows: [
      ["Alquiler o cuota al año", eur(d.alq_cerca * 12), eur(d.alq_lejos * 12)],
      ["Desplazamiento extra al año", eur(0), eur(r.desplaz)],
      ["Horas extra al año", hh(0), hh(r.horas)],
      ["Tiempo valorado", eur(0), eur(r.tiempoVal)],
      { label: "Coste anual total", values: [eur(r.costeCerca), eur(r.costeLejos)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
