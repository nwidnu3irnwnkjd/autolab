// Freidora de aire frente a horno electrico (tradicional o ventilado), microondas u horno de gas: coste de energia por uso y por ano, y amortizacion de la freidora.
// Energia por uso = potencia media en marcha (kW, hipotesis) x (minutos de precalentamiento + de coccion) / 60. Electricidad: precio efectivo = energia + impuesto electrico (con minimo por kWh) + IVA (Ley 38/1992 art. 99, Ley 37/1992).
// Gas: kWh termicos x precio del gas con impuestos (editable). Potencias y precalentamientos por tipo = hipotesis propias en H (no datos de fabricante). No equivalen en capacidad.
// Anual = coste por uso x usos/semana x 52. Freidora anual total = energia + compra / VIDA (la alternativa se supone ya en casa: sin compra). ganador: 0 freidora, 1 alternativa, 2 empate practico (< 5 %).
// usosEq: usos por semana a partir de los cuales la freidora compensa su compra (0 si no hay compra y ahorra, -1 si no ahorra por uso).
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, empate: 0.05, semanas: 52 };
var VIDA = 8, PRE_FR = 3;
var H = [
  { n: "horno eléctrico tradicional", kw: 1.5, pre: 10, min: 35, gas: 0 },
  { n: "horno eléctrico ventilado", kw: 1.2, pre: 8, min: 30, gas: 0 },
  { n: "microondas", kw: 0.8, pre: 0, min: 8, gas: 0 },
  { n: "horno de gas", kw: 2.0, pre: 8, min: 35, gas: 1 }
];
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precio), h = H[Math.round(d.alt)] || H[0];
  var kwhFr = d.kwFr * (PRE_FR + d.minFr) / 60, kwhAlt = h.kw * (h.pre + d.minAlt) / 60;
  var cFr = kwhFr * pe, cAlt = kwhAlt * (h.gas ? d.precioGas : pe), n = d.usos * L.semanas;
  var aFr = cFr * n, aAlt = cAlt * n, am = d.compra / VIDA, tFr = aFr + am, dif = aAlt - tFr, ahorroEn = aAlt - aFr;
  var anios = d.compra <= 0 ? (ahorroEn >= 0 ? 0 : -1) : (ahorroEn > 0 ? d.compra / ahorroEn : -1);
  var usosEq = cAlt - cFr > 0 ? (d.compra > 0 ? am / (L.semanas * (cAlt - cFr)) : 0) : -1;
  var g = Math.abs(dif) < Math.max(1, L.empate * Math.max(tFr, aAlt)) ? 2 : (dif > 0 ? 0 : 1);
  return { precioEf: pe, kwhFr: kwhFr, kwhAlt: kwhAlt, costeFr: cFr, costeAlt: cAlt, usosAno: n, anualFr: aFr, anualAlt: aAlt, amortAnual: am,
    totalFr: tFr, diferencia: dif, ahorroEnergia: ahorroEn, aniosAmort: anios, usosEq: usosEq, esGas: h.gas, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["alt", "usos", "precio", "precioGas", "kwFr", "minFr", "minAlt", "compra"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
document.getElementById("alt").addEventListener("change", function () {
  var h = H[Math.round(parseFloat(this.value))]; if (h) document.getElementById("minAlt").value = h.min;
});
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  var h = H[Math.round(d.alt)];
  if (!h) return;
  if (d.kwFr <= 0 || d.minFr <= 0 || d.minAlt <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica la potencia media de la freidora y los minutos de cocción de las dos opciones (mayores que 0).", tone: "warn", note: "<p>Sin potencia ni tiempo no hay consumo que comparar. Los valores de partida son hipótesis, no datos de tu equipo.</p>" });
    return;
  }
  if (d.usos > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los usos: no puede haber más de 30 a la semana.", tone: "warn", note: "<p>Cuenta solo los cocinados que harías con la freidora en vez de con la otra opción.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), w, verdict, tone = "ok", an = h.n;
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con tus datos, empate práctico: la freidora y el " + an + " cuestan casi lo mismo al año (diferencia de " + EM.eur(ab) + ", con la compra repartida en " + VIDA + " años).";
  } else if (g === 0) {
    w = "freidora";
    verdict = "Con tus datos, gana la freidora de aire por " + EM.eur(ab) + " al año frente al " + an + ", pero no tienen la misma capacidad ni hacen exactamente lo mismo.";
  } else {
    w = "alternativa";
    verdict = "Con tus datos, gana el " + an + " por " + EM.eur(ab) + " al año frente a la freidora" + (d.compra > 0 && r.ahorroEnergia > 0 ? " (la compra de la freidora se come el ahorro de energía)" : "") + ", pero no tienen la misma capacidad.";
  }
  var uni = r.esGas ? "kWh de gas" : "kWh";
  var note = "<p><strong>Lectura:</strong> cada uso con la freidora gasta " + EM.num(r.kwhFr, 2) + " kWh y cuesta <strong>" + EM.eur(r.costeFr, 2) + "</strong>; con el " + an + ", " + EM.num(r.kwhAlt, 2) + " " + uni + " y <strong>" + EM.eur(r.costeAlt, 2) + "</strong> (" + EM.num(h.kw, 1) + " kW de media y " + EM.num(h.pre, 0) + " min de precalentamiento, hipótesis por tipo). Con " + EM.num(r.usosAno, 0) + " usos al año son " + EM.eur(r.anualFr) + " frente a " + EM.eur(r.anualAlt) + " de energía";
  if (d.compra > 0) note += ", más " + EM.eur(r.amortAnual) + " al año de la freidora (" + EM.eur(d.compra) + " repartidos en " + VIDA + " años)";
  note += ". ";
  if (r.usosEq > 0) note += "Con estos tiempos, la freidora compensa su compra a partir de <strong>" + EM.num(r.usosEq, 1) + " usos por semana</strong>. ";
  else if (r.usosEq === 0 && d.compra <= 0) note += "Sin compra que amortizar, la freidora ahorra desde el primer uso. ";
  else if (r.usosEq < 0) note += "Con estos tiempos la freidora no gasta menos que el " + an + " por uso, así que la compra no se amortiza con energía. ";
  if (r.aniosAmort > 0) note += "Se amortizaría en <strong>" + EM.num(r.aniosAmort, 1) + " años</strong>. ";
  note += "</p><p><strong>No son equivalentes:</strong> la freidora cocina raciones pequeñas (de una a pocas personas) y el horno admite bandejas grandes o varios platos a la vez; el microondas calienta pero no dora igual. Si necesitas cocinar para más gente, comparar un uso con otro no es justo. Tampoco incluye el tiempo extra de cocinar por tandas.</p>";
  note += "<p><strong>Hipótesis editables:</strong> potencia media, minutos de cocción y de precalentamiento cambian mucho entre equipos y recetas; los de partida son ejemplos, no datos de fabricante. La potencia y el precalentamiento de la alternativa dependen del tipo que elijas y el tiempo se rellena con un valor típico que puedes cambiar. El gas solo cuenta si eliges horno de gas (kWh térmicos × tu precio del gas, sin término fijo). <strong>No incluye:</strong> término de potencia ni alquiler de contador, mantenimiento, la inflación ni descuentos financieros; se asume que la alternativa ya la tienes. Se usa la media de todas las horas del PVPC; en horas valle el kWh suele ser más barato. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia al año" : (g === 0 ? "menos al año con la freidora" : "menos al año con el " + an), format: EM.eur,
    barsLabel: "Coste al año (energía y, en la freidora, compra repartida)",
    bars: [{ label: "Freidora de aire" + (w === "freidora" ? " (gana)" : ""), value: r.totalFr, color: "a" }, { label: an.charAt(0).toUpperCase() + an.slice(1) + (w === "alternativa" ? " (gana)" : ""), value: r.anualAlt, color: "b" }],
    cols: ["Freidora de aire", an.charAt(0).toUpperCase() + an.slice(1)],
    rows: [
      ["Energía por uso (" + (r.esGas ? "kWh de gas en el horno" : "kWh") + ")", EM.num(r.kwhFr, 2), EM.num(r.kwhAlt, 2)],
      ["Coste por uso", EM.eur(r.costeFr, 2), EM.eur(r.costeAlt, 2)],
      ["Energía al año", EM.eur(r.anualFr), EM.eur(r.anualAlt)],
      ["Compra repartida al año", EM.eur(r.amortAnual), EM.eur(0)],
      { label: "Total al año", values: [EM.eur(r.totalFr), EM.eur(r.anualAlt)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
