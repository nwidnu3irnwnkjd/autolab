// Tener un perro: coste del primer anio, coste anual y total, adoptando o comprando (solo cambia el precio de entrada).
// Anual = 12 x pienso + veterinario y otros + seguro. Primer anio = entrada (cuota de adopcion o compra) + gastos iniciales + anual.
// Total = entrada + iniciales + anios x anual (sin inflacion ni descuento). ganador: 0 adoptar, 1 comprar, 2 empate (diferencia de menos de 1 euro).
function calcular(d) {
  var anual = 12 * d.pienso + d.vet + d.seguro, base = d.iniciales + d.anos * anual;
  var totA = d.adopcion + base, totC = d.compra + base, dif = totC - totA;
  return { anual: anual, mensual: anual / 12, ano1Adopcion: d.adopcion + d.iniciales + anual, ano1Compra: d.compra + d.iniciales + anual,
    totalAdopcion: totA, totalCompra: totC, diferencia: dif, mensualMedioAdopcion: totA / (12 * d.anos), mensualMedioCompra: totC / (12 * d.anos),
    mesesDif: anual > 0 ? Math.abs(dif) / (anual / 12) : -1, pesoSeguro: anual > 0 ? d.seguro / anual * 100 : 0,
    pesoEntradaAdopcion: totA > 0 ? d.adopcion / totA * 100 : 0, pesoEntradaCompra: totC > 0 ? d.compra / totC * 100 : 0,
    ganador: Math.abs(dif) < 1 ? 2 : (dif > 0 ? 0 : 1) };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["pienso", "vet", "seguro", "iniciales", "adopcion", "compra", "anos"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.anos < 1 || d.anos > 25) {
    EM.renderResult({ winner: "invalido", verdict: "Indica entre 1 y 25 años en los que vas a tener al perro.", tone: "warn", note: "<p>Es el periodo en que sumas los gastos; no es una esperanza de vida.</p>" });
    return;
  }
  if (d.pienso <= 0 && d.vet <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica al menos un gasto corriente (pienso o veterinario) mayor que 0.", tone: "warn", note: "<p>Sin gasto corriente no hay coste anual que calcular.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), an = EM.num(d.anos, d.anos % 1 ? 1 : 0) + (d.anos === 1 ? " año" : " años");
  var w = ["adoptar", "comprar", "empate"][g], tone = g === 2 ? "warn" : "ok", verdict;
  var meses = r.mesesDif >= 0 ? ", lo que equivale a " + EM.num(r.mesesDif, 1) + " meses de gasto corriente" : "";
  if (g === 2) verdict = "Con estos datos adoptar y comprar cuestan lo mismo en " + an + " (" + eur(r.totalAdopcion) + "): la cuota de adopción y el precio de compra coinciden, así que el coste no desempata.";
  else if (g === 0) verdict = "Con estos datos adoptar sale " + eur(ab) + " más barato que comprar en " + an + " (" + eur(r.totalAdopcion) + " frente a " + eur(r.totalCompra) + ")" + meses + "; el resto del gasto, " + eur(r.anual) + " al año, es el mismo.";
  else verdict = "Con estos datos comprar sale " + eur(ab) + " más barato que adoptar en " + an + " (" + eur(r.totalCompra) + " frente a " + eur(r.totalAdopcion) + "), porque la cuota de adopción que has puesto es mayor que el precio de compra" + meses + "; el resto del gasto, " + eur(r.anual) + " al año, es el mismo.";
  var note = "<p><strong>Lectura:</strong> el primer año cuesta " + eur(r.ano1Adopcion) + " adoptando y " + eur(r.ano1Compra) + " comprando (entrada, gastos iniciales de " + eur(d.iniciales) + " y " + eur(r.anual) + " de gasto anual); a partir del segundo, " + eur(r.anual) + " al año, es decir, " + eur(r.mensual) + " al mes. En " + an + " la media es de " + eur(r.mensualMedioAdopcion) + " al mes adoptando y " + eur(r.mensualMedioCompra) + " comprando. ";
  note += "La entrada pesa un " + EM.num(r.pesoEntradaAdopcion, 1) + " % del total adoptando y un " + EM.num(r.pesoEntradaCompra, 1) + " % comprando: lo que más pesa es el gasto corriente" + (d.seguro > 0 ? ", con el seguro en un " + EM.num(r.pesoSeguro, 0) + " % del gasto anual" : "") + ". La diferencia entre adoptar y comprar es solo el precio de entrada; esta calculadora no compara nada más.</p>";
  note += "<p><strong>Límites:</strong> los importes son ejemplos tuyos, no precios de mercado ni de ninguna protectora, criadero o clínica; el selector de tamaño solo rellena pienso y veterinario con hipótesis de ejemplo. No incluye urgencias ni tratamientos imprevistos (el seguro, si lo pones, entra como prima fija), ni el coste de la alimentación especial, el paseador, la guardería o los viajes salvo que lo sumes al veterinario y otros gastos. Sin inflación ni descuento. No sustituye el consejo de tu veterinario y no valora la salud, el carácter o la edad del animal.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: r.anual, bigLabel: "de gasto anual a partir del segundo año", format: EM.eur,
    barsLabel: "Coste total en " + an + " (entrada + gastos iniciales + gasto anual)",
    bars: [{ label: "Adoptar" + (w === "adoptar" ? " (más barato)" : ""), value: r.totalAdopcion, color: "a" }, { label: "Comprar" + (w === "comprar" ? " (más barato)" : ""), value: r.totalCompra, color: "b" }],
    cols: ["Adoptar", "Comprar"],
    rows: [
      ["Entrada (cuota o precio)", eur(d.adopcion), eur(d.compra)],
      ["Gastos iniciales", eur(d.iniciales), eur(d.iniciales)],
      ["Primer año", eur(r.ano1Adopcion), eur(r.ano1Compra)],
      ["Gasto anual desde el segundo", eur(r.anual), eur(r.anual)],
      { label: "Total en " + an, values: [eur(r.totalAdopcion), eur(r.totalCompra)], strong: true }
    ],
    note: note
  });
}
var sel = document.getElementById("tamano");
if (sel) sel.addEventListener("change", function () {
  var p = sel.value.split("|");
  if (p.length === 2) { document.getElementById("pienso").value = p[0]; document.getElementById("vet").value = p[1]; pintar(); }
});
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
