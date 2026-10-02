// Agua caliente sanitaria: termo electrico, calentador de gas o aerotermia (bomba de calor para agua caliente), coste total en la vida util.
// Energia util = personas x litros/persona/dia x salto de temperatura x 0,001163 kWh/(l K) x 365. Energia final = util / rendimiento (COP en la aerotermia).
// Precio de la luz = energia + impuesto electrico (con minimo por kWh) + IVA (Ley 38/1992 art. 99, Ley 37/1992); el precio del gas lo pone el usuario (con impuestos).
// Total = compra + vida x coste anual (sin descontar ni inflacion; sin mantenimiento ni potencia contratada). ganador: 0 termo, 1 gas, 2 aerotermia, 3 empate.
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, litros: 40, salto: 45, kwhLK: 0.001163, etaTermo: 0.9, etaGas: 0.8, cop: 2.8 };
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precioLuz), util = d.personas * L.litros * L.salto * L.kwhLK * 365;
  var kT = util / L.etaTermo, kG = util / L.etaGas, kA = util / L.cop;
  var cT = kT * pe, cG = kG * d.precioGas + d.fijoGas, cA = kA * pe;
  var tT = d.compraTermo + d.vida * cT, tG = d.compraGas + d.vida * cG, tA = d.compraAero + d.vida * cA;
  var arr = [tT, tG, tA], best = 0, i;
  for (i = 1; i < 3; i++) if (arr[i] < arr[best]) best = i;
  var second = Infinity;
  for (i = 0; i < 3; i++) if (i !== best && arr[i] < second) second = arr[i];
  function anios(extra, ahorro) { return extra <= 0 ? (ahorro >= 0 ? 0 : -1) : (ahorro > 0 ? extra / ahorro : -1); }
  function perEq(extra, ahorro) { return (extra > 0 && ahorro > 0 && d.vida > 0) ? extra / (d.vida * ahorro / d.personas) : -1; }
  var exG = d.compraGas - d.compraTermo, exA = d.compraAero - d.compraTermo, sG = cT - cG, sA = cT - cA;
  return { precioEf: pe, kwhUtil: util, kwhTermo: kT, kwhGas: kG, kwhAero: kA, costeTermo: cT, costeGas: cG, costeAero: cA,
    totalTermo: tT, totalGas: tG, totalAero: tA, segundo: second - arr[best], aniosGas: anios(exG, sG), aniosAero: anios(exA, sA),
    personasGas: perEq(exG, sG), personasAero: perEq(exA, sA), ganador: (second - arr[best]) < 1 ? 3 : best };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["personas", "precioLuz", "precioGas", "fijoGas", "compraTermo", "compraGas", "compraAero", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.personas < 1 || d.personas > 12) {
    EM.renderResult({ winner: "invalido", verdict: "Indica entre 1 y 12 personas que usan el agua caliente.", tone: "warn", note: "<p>Sin personas no hay consumo de agua caliente que comparar.</p>" });
    return;
  }
  if (d.vida < 1 || d.vida > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica una vida útil de entre 1 y 30 años.", tone: "warn", note: "<p>Es el periodo en que repartes la compra; no es una garantía del fabricante.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, vid = EM.num(d.vida, d.vida % 1 ? 1 : 0) + (d.vida === 1 ? " año" : " años");
  var NOM = ["Termo eléctrico", "Calentador de gas", "Aerotermia"], TOT = [r.totalTermo, r.totalGas, r.totalAero];
  var w = ["termo", "gas", "aerotermia", "empate"][g], verdict, tone = "ok";
  if (g === 3) {
    tone = "warn";
    verdict = "Con estos datos las dos opciones más baratas cuestan lo mismo en " + vid + " (compra más energía), con una diferencia de menos de 1 €.";
  } else {
    var ord = [0, 1, 2].filter(function (i) { return i !== g; }).sort(function (a, b) { return TOT[a] - TOT[b]; });
    verdict = "Con estos datos " + ["el termo eléctrico", "el calentador de gas", "la aerotermia"][g] + " es la opción más barata en " + vid + " (compra más energía): " + eur(TOT[g]) + ", y la siguiente (" + NOM[ord[0]].toLowerCase() + ") cuesta " + eur(TOT[ord[0]] - TOT[g]) + " más.";
    if (g === 1 && d.fijoGas === 0) verdict += " No incluye el término fijo del gas: si no lo tienes ya, indícalo y vuelve a calcular.";
  }
  var note = "<p><strong>Lectura:</strong> el agua caliente de " + EM.num(d.personas, 0) + (d.personas === 1 ? " persona" : " personas") + " necesita unos " + EM.num(r.kwhUtil, 0) + " kWh útiles al año; el termo gasta " + EM.num(r.kwhTermo, 0) + " kWh de electricidad, el calentador " + EM.num(r.kwhGas, 0) + " kWh de gas y la aerotermia " + EM.num(r.kwhAero, 0) + " kWh de electricidad. Con la luz a " + EM.num(r.precioEf, 3) + " €/kWh con impuestos, cada año cuestan " + eur(r.costeTermo) + ", " + eur(r.costeGas) + " y " + eur(r.costeAero) + ". ";
  if (r.aniosAero > 0) note += "La aerotermia recupera su mayor compra frente al termo eléctrico en <strong>" + EM.num(r.aniosAero, 1) + " años</strong>" + (r.aniosAero > d.vida ? ", más que la vida útil que has puesto" : "") + (r.personasAero > 0 ? " y empata con él a partir de <strong>" + EM.num(r.personasAero, 1) + " personas</strong> con tu vida útil" : "") + ". ";
  else if (r.aniosAero === 0) note += "La aerotermia no cuesta más que el termo y gasta menos, así que no hay nada que amortizar. ";
  else note += "Con estos datos la aerotermia no recupera su compra frente al termo eléctrico. ";
  if (r.aniosGas > 0) note += "El calentador de gas recupera su mayor compra frente al termo en <strong>" + EM.num(r.aniosGas, 1) + " años</strong>" + (r.aniosGas > d.vida ? ", más que la vida útil que has puesto" : "") + ". ";
  else if (r.aniosGas === 0) note += "El calentador de gas no cuesta más que el termo y gasta menos. ";
  else note += "Con estos datos el calentador de gas no recupera su compra frente al termo. ";
  note += "</p><p><strong>Avisos:</strong> el precio del gas lo pones tú, con impuestos y según tu factura (el de partida es la TUR.2 de octubre de 2026 y puede cambiar). Si no tienes gas, suma el término fijo y la instalación; si lo tienes, pon 0. No incluye mantenimiento, revisiones de gas, potencia eléctrica contratada ni obras (chimenea, depósito). Rendimientos del modelo (hipótesis, no de un fabricante): 0,9 el termo, 0,8 el calentador y COP 2,8 la aerotermia, con 40 litros por persona y día y un salto de 45 K. Sin inflación ni descuento. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: g === 3 ? Math.min(r.totalTermo, r.totalGas, r.totalAero) : TOT[g], bigLabel: "coste total en " + vid + " de la opción más barata", format: EM.eur,
    barsLabel: "Coste total en " + vid + " (compra más energía)",
    bars: NOM.map(function (n, i) { return { label: n + (i === g ? " (gana)" : ""), value: TOT[i], color: ["a", "b", "c"][i] }; }),
    cols: NOM,
    rows: [
      ["Energía final al año (kWh)", EM.num(r.kwhTermo, 0), EM.num(r.kwhGas, 0), EM.num(r.kwhAero, 0)],
      ["Coste de energía al año", eur(r.costeTermo), eur(r.costeGas), eur(r.costeAero)],
      ["Compra e instalación", eur(d.compraTermo), eur(d.compraGas), eur(d.compraAero)],
      { label: "Total en " + vid, values: [eur(r.totalTermo), eur(r.totalGas), eur(r.totalAero)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
