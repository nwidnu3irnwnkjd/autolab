// Ahorro neto de desviarte a una gasolinera mas barata: ahorro por litro x litros, menos combustible del desvio y, si quieres, tu tiempo.
function calcular(d) {
  var bruto = d.litros * d.dif;
  var costeKm = d.cons / 100 * d.precio + (d.vel > 0 ? d.valorHora / d.vel : 0);   // € por km de desvio (combustible + tiempo)
  var comb = d.km * d.cons / 100 * d.precio;
  var tiempo = d.vel > 0 ? d.km / d.vel * d.valorHora : 0;
  var neto = bruto - comb - tiempo;
  var kmEq = costeKm > 0 ? bruto / costeKm : -1;                 // -1: sin limite
  var litrosMin = d.dif > 0 ? d.km * costeKm / d.dif : -1;       // -1: no hay ahorro por litro
  return { bruto: bruto, combustible: comb, tiempo: tiempo, neto: neto, kmEquilibrio: kmEq, litrosMin: litrosMin, costeKm: costeKm };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
var IDS = ["litros", "dif", "km", "cons", "precio", "valorHora", "vel"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pintar() {
  var d = leer(), r, v, note, w, tone;
  if (IDS.some(function (k) { return d[k] < 0; })) return;
  if (d.litros <= 0) { aviso("Pon cuántos litros vas a repostar.", "Sin litros no hay ahorro que calcular."); return; }
  if (d.valorHora > 0 && d.vel <= 0) { aviso("Pon la velocidad media del desvío para valorar tu tiempo.", "Sin velocidad no se puede convertir los km del desvío en horas."); return; }
  r = calcular(d);
  if (d.dif <= 0) { v = "Con una diferencia de precio de 0 €/l o menos no hay ahorro: el desvío solo suma coste (" + EM.eur(-r.neto, 2) + ")."; tone = "warn"; w = "no"; }
  else if (r.neto >= 1) { v = "Sí compensa desviarte: ahorras " + EM.eur(r.neto, 2) + " netos tras descontar el combustible del desvío" + (r.tiempo > 0 ? " y tu tiempo" : "") + "."; tone = "ok"; w = "si"; }
  else if (r.neto >= 0) { v = "Compensa por muy poco: " + EM.eur(r.neto, 2) + " netos; con un pequeño cambio en el precio o en el desvío puede dejar de compensar."; tone = "warn"; w = "justo"; }
  else { v = "No compensa desviarte: pierdes " + EM.eur(-r.neto, 2) + " netos, porque el desvío cuesta más de lo que ahorras en el depósito."; tone = "warn"; w = "no"; }
  note = "<p><strong>Lectura:</strong> ";
  if (r.kmEquilibrio >= 0) note += "con esos litros y esa diferencia de precio, el desvío compensa hasta unos <strong>" + EM.num(r.kmEquilibrio, 1) + " km</strong> de ida y vuelta (tú has puesto " + EM.num(d.km, 1) + "). ";
  else note += "con estos datos el desvío no tiene coste por km, así que compensa a la distancia que sea. ";
  if (r.litrosMin >= 0) note += "Para que ese desvío compense necesitas repostar al menos <strong>" + EM.num(r.litrosMin, 1) + " litros</strong> (tú repostas " + EM.num(d.litros, 0) + "). ";
  else note += "Sin ahorro por litro, ningún depósito compensa el desvío. ";
  note += "</p><p><strong>No incluido:</strong> el desgaste del coche, las colas, ni que el consumo real cambie con el tráfico. Si ya pasas por esa gasolinera de camino, el desvío es 0 km y el ahorro es el bruto. Precio de referencia: el que pagas por litro (por defecto, la gasolina 95 de hoy). Mira también <a href=\"/decidir/diesel-gasolina-hibrido-electrico/\">diésel, gasolina, híbrido o eléctrico</a>.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: tone,
    bigNumber: r.neto, bigLabel: "de ahorro neto por repostaje (negativo: pierdes)", format: function (x) { return EM.eur(x, 2); },
    barsLabel: "Ahorro frente a coste del desvío",
    bars: [{ label: "Ahorro en el depósito", value: r.bruto, color: "a" }, { label: "Coste del desvío", value: r.combustible + r.tiempo, color: "b" }],
    cols: ["Importe"],
    rows: [
      { label: "Ahorro neto", values: [EM.eur(r.neto, 2)], strong: true },
      ["Ahorro bruto en el depósito", EM.eur(r.bruto, 2)],
      ["Combustible del desvío", EM.eur(r.combustible, 2)],
      ["Tu tiempo", EM.eur(r.tiempo, 2)],
      ["Km de desvío de equilibrio", r.kmEquilibrio >= 0 ? EM.num(r.kmEquilibrio, 1) + " km" : "sin límite"],
      ["Litros mínimos para compensar", r.litrosMin >= 0 ? EM.num(r.litrosMin, 1) + " l" : "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
