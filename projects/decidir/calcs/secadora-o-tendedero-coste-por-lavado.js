// Secadora (condensacion o bomba de calor) frente a tendedero: coste de energia por colada y por ano, tiempo y amortizacion de la compra.
// Coste por colada = kWh por ciclo (hipotesis editable) x precio efectivo; precio efectivo = energia + impuesto electrico (con minimo por kWh) + IVA (Ley 38/1992 art. 99, Ley 37/1992).
// Tendedero: 0 EUR de energia; su coste es el tiempo extra de tender y recoger, valorado con el valor de la hora que pone el usuario (0 por defecto).
// Total = compra + vida x coste anual de la secadora, frente a vida x valor del tiempo del tendedero (sin descontar ni inflacion; sin mantenimiento ni potencia contratada).
// ganador: 0 secadora, 1 tendedero, 2 empate practico (< 5 %). valorEq: valor de la hora a partir del cual la secadora compensa (-1 si no hay).
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, empate: 0.05 };
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precio), ciclo = d.kwh * pe, n = d.coladas * d.semanas;
  var kwhAno = d.kwh * n, energiaAno = ciclo * n, horas = d.minutos * n / 60, tiempoAno = horas * d.valorHora;
  var totS = d.compra + d.vida * energiaAno, totT = d.vida * tiempoAno, dif = totT - totS;
  var base = d.minutos / 60 * d.vida * n;
  var valorEq = (base > 0 && totS > 0) ? totS / base : -1;
  var den = d.vida * (d.valorHora * d.minutos / 60 - ciclo);
  var coladasEq = (den > 0 && d.semanas > 0 && d.compra > 0) ? d.compra / den / d.semanas : -1;
  var g = Math.abs(dif) < Math.max(1, L.empate * Math.max(totS, totT)) ? 2 : (dif > 0 ? 0 : 1);
  return { precioEf: pe, ciclo: ciclo, coladasAno: n, kwhAno: kwhAno, energiaAno: energiaAno, horasAno: horas, tiempoAno: tiempoAno,
    totalSecadora: totS, totalTendedero: totT, diferencia: dif, valorEq: valorEq, coladasEq: coladasEq, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["coladas", "semanas", "kwh", "precio", "minutos", "valorHora", "compra", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.kwh <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica los kWh que gasta la secadora por ciclo (mayor que 0).", tone: "warn", note: "<p>Sin consumo no hay coste que comparar. Míralo en la ficha o en la etiqueta energética de tu secadora; el valor de partida es solo un ejemplo.</p>" });
    return;
  }
  if (d.coladas > 30 || d.semanas > 52) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el uso: no puede haber más de 52 semanas al año ni de 30 coladas por semana.", tone: "warn", note: "<p>Cuenta solo las coladas que secarías en la secadora en vez de en el tendedero.</p>" });
    return;
  }
  if (d.vida < 1 || d.vida > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica una vida útil de entre 1 y 30 años.", tone: "warn", note: "<p>Es el periodo en que repartes la compra; no es una garantía del fabricante.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), vid = EM.num(d.vida, d.vida % 1 ? 1 : 0) + (d.vida === 1 ? " año" : " años"), w, verdict, tone = "ok";
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con tus datos, empate práctico: la secadora y el tendedero cuestan casi lo mismo en " + vid + " (diferencia de " + EM.eur(ab) + ", contando tu tiempo).";
  } else if (g === 0) {
    w = "secadora";
    verdict = "Con tus datos, gana la secadora por " + EM.eur(ab) + " en " + vid + ": el tiempo que ahorras, valorado a " + EM.eur(d.valorHora, 2) + " la hora, supera su compra más la energía.";
  } else {
    w = "tendedero";
    verdict = "Con tus datos, gana el tendedero por " + EM.eur(ab) + " en " + vid + (d.valorHora > 0 ? " (contando tu tiempo)" : "") + ", pero tender y recoger lleva tiempo y en invierno o con humedad la ropa tarda en secar.";
  }
  var note = "<p><strong>Lectura:</strong> con " + EM.num(r.precioEf, 3) + " €/kWh con impuestos, cada colada en la secadora cuesta <strong>" + EM.eur(r.ciclo, 2) + "</strong> de energía (" + EM.num(d.kwh, 2) + " kWh) y el tendedero, 0 €. Con " + EM.num(r.coladasAno, 0) + " coladas al año son " + EM.num(r.kwhAno, 0) + " kWh y " + EM.eur(r.energiaAno) + " al año de energía, además de la compra (" + EM.eur(d.compra) + ", " + EM.eur(d.compra / d.vida) + " al año repartida en " + vid + "). El tendedero te lleva " + EM.num(r.horasAno, 0) + " horas al año de tender y recoger. ";
  if (r.valorEq > 0) note += "La secadora compensa si valoras tu hora por encima de <strong>" + EM.eur(r.valorEq, 2) + "</strong>. ";
  if (r.coladasEq > 0) note += "Con tu valor de la hora, compensaría a partir de <strong>" + EM.num(r.coladasEq, 1) + " coladas por semana</strong>. ";
  note += "</p><p><strong>Tiempo y humedad no son lo mismo que euros:</strong> secar dentro de casa sube la humedad y puede dar moho si no ventilas; fuera, depende del clima y de tener sitio. Si tendedero y secadora no son alternativas reales para ti (por ejemplo, sin balcón en invierno), esta cifra solo te dice cuánto cuesta la comodidad. Un deshumidificador es otra opción que esta calculadora no compara.</p>";
  note += "<p><strong>No incluye:</strong> el término de potencia ni el alquiler del contador, un aumento de potencia contratada, el mantenimiento ni el desgaste de la ropa, la compra del tendedero, la inflación del precio de la luz ni descuentos financieros. Los kWh por ciclo son una hipótesis tuya: cambian mucho entre equipos y programas. Se usa la media de todas las horas del PVPC; si la pones en horas valle, el kWh suele ser más barato. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia en " + vid : (g === 0 ? "menos con la secadora en " + vid : "menos con el tendedero en " + vid), format: EM.eur,
    barsLabel: "Coste total en " + vid + " (compra, energía y tu tiempo)",
    bars: [{ label: "Secadora" + (w === "secadora" ? " (gana)" : ""), value: r.totalSecadora, color: "a" }, { label: "Tendedero" + (w === "tendedero" ? " (gana)" : ""), value: r.totalTendedero, color: "b" }],
    cols: ["Secadora", "Tendedero"],
    rows: [
      ["Energía por colada", EM.eur(r.ciclo, 2), EM.eur(0, 2)],
      ["Energía al año", EM.eur(r.energiaAno), EM.eur(0)],
      ["Tiempo de tender y recoger al año (h)", "0", EM.num(r.horasAno, 0)],
      ["Compra", EM.eur(d.compra), EM.eur(0)],
      { label: "Total en " + vid, values: [EM.eur(r.totalSecadora), EM.eur(r.totalTendedero)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
