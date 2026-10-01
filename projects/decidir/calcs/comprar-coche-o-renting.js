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
  var h;
  if (Math.round(abs) === 0) h = '<div class="verdict">Con estos números, comprar y el renting cuestan prácticamente lo mismo.</div>';
  else h = '<div class="verdict">' + gana + ' sale más barato: ' + eur(abs) + ' menos en ' + d.anos + ' años, unos ' + eur(abs / n) + ' al mes.</div>';
  h += '<table><tr><th></th><th class="n">Comprar</th><th class="n">Renting</th></tr>';
  h += '<tr><td>Coste total en ' + d.anos + ' años</td><td class="n">' + eur(r.costeCompra) + '</td><td class="n">' + eur(r.costeRenting) + '</td></tr>';
  h += '<tr><td>Coste mensual equivalente</td><td class="n">' + eur2(r.mesCompra) + '</td><td class="n">' + eur2(r.mesRenting) + '</td></tr>';
  h += '<tr><td>Intereses de la financiación</td><td class="n">' + eur(r.intereses) + '</td><td class="n">&mdash;</td></tr>';
  h += '<tr><td>Valor del coche al final</td><td class="n">' + eur(r.reventa) + '</td><td class="n">No es tuyo</td></tr></table>';
  h += '<div class="box"><strong>Lectura:</strong> el renting te costaría lo mismo que comprar con una cuota de ' + eur2(r.cuotaEquilibrio) + ' al mes (con tu entrada); la que has puesto es ' + eur2(d.cuota) + '. ';
  h += 'El renting incluye seguro y mantenimiento y no asumes el riesgo de reventa, pero al final no tienes el coche. Comprar inmoviliza capital' + (d.tipo > 0 ? ' y te cuesta ' + eur(r.intereses) + ' en intereses' : '') + ' y depende de que el coche valga al final lo que estimas (' + eur(r.reventa) + '). ';
  h += 'Si la diferencia es pequeña, pesan más tus preferencias que el número.</div>';
  var el = document.getElementById("r"); el.innerHTML = h; el.style.display = "block";
}
document.getElementById("anos").value = "4";
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
