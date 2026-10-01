// Préstamo francés: cuota mensual para capital P, tipo mensual i, n meses.
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
function calcular(d) {
  var n = d.anos * 12, i = d.tipo / 100 / 12;
  var intereses = d.tipo > 0 ? cuotaFrancesa(d.precio, i, n) * n - d.precio : 0;
  var reventa = d.precio * d.reventa / 100;
  var gastosAnuales = d.seguro + d.mantenimiento + d.impuesto;
  var costeCompra = d.precio + intereses + gastosAnuales * d.anos - reventa;
  var costeRenting = d.entrada + d.cuota * n;
  return {
    costeCompra: costeCompra, costeRenting: costeRenting,
    mesCompra: costeCompra / n, mesRenting: costeRenting / n,
    cuotaEquilibrio: (costeCompra - d.entrada) / n,
    intereses: intereses, reventa: reventa,
    diferencia: costeRenting - costeCompra
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function leer() {
  var d = {}; ["precio", "anos", "reventa", "seguro", "mantenimiento", "impuesto", "tipo", "cuota", "entrada"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.precio <= 0 || d.anos <= 0) return;
  var r = calcular(d), n = d.anos * 12, gana = r.diferencia > 0 ? "Comprar" : "El renting", abs = Math.abs(r.diferencia);
  var empate = Math.round(abs) === 0, verdict;
  if (empate) verdict = 'Con estos números, comprar y el renting cuestan prácticamente lo mismo.';
  else verdict = gana + ' sale más barato: ' + EM.eur(abs) + ' menos en ' + d.anos + ' años, unos ' + EM.eur(abs / n) + ' al mes.';
  var note = '<p><strong>Lectura:</strong> el renting te costaría lo mismo que comprar con una cuota de ' + EM.eur(r.cuotaEquilibrio, 2) + ' al mes (con tu entrada); la que has puesto es ' + EM.eur(d.cuota, 2) + '. ';
  note += 'El renting incluye seguro y mantenimiento y no asumes el riesgo de reventa, pero al final no tienes el coche. Comprar inmoviliza capital' + (d.tipo > 0 ? ' y te cuesta ' + EM.eur(r.intereses) + ' en intereses' : '') + ' y depende de que el coche valga al final lo que estimas (' + EM.eur(r.reventa) + '). ';
  note += 'Si la diferencia es pequeña, pesan más tus preferencias que el número.</p>';
  EM.renderResult({
    winner: empate ? "empate" : (r.diferencia > 0 ? "comprar" : "renting"),
    verdict: verdict,
    tone: empate || abs < r.costeCompra * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: empate ? "de diferencia" : "menos en " + d.anos + " años " + (r.diferencia > 0 ? "si compras" : "con renting"),
    format: EM.eur,
    barsLabel: "Coste total en " + d.anos + " años",
    bars: [{ label: "Comprar", value: r.costeCompra, color: "a" }, { label: "Renting", value: r.costeRenting, color: "b" }],
    cols: ["Comprar", "Renting"],
    rows: [
      { label: "Coste total en " + d.anos + " años", values: [EM.eur(r.costeCompra), EM.eur(r.costeRenting)], strong: true },
      ["Coste mensual equivalente", EM.eur(r.mesCompra, 2), EM.eur(r.mesRenting, 2)],
      ["Intereses de la financiación", EM.eur(r.intereses), "&mdash;"],
      ["Valor del coche al final", EM.eur(r.reventa), "No es tuyo"]
    ],
    note: note
  });
}
document.getElementById("anos").value = "4";
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
