var NOMBRES = ["Diésel", "Gasolina", "Híbrido", "Eléctrico"];
// Coste total de propiedad de un coche: parte fija (compra - residual + seguro, mantenimiento, impuesto) + energía por km.
function costeTipo(d, t) {
  var precioKm = t.consumo / 100 * t.precioEnergia;               // € por km de energía
  var fijo = t.compra * (1 - t.residual / 100) + (t.seguro + t.mant + t.imp) * d.anos;
  return { fijo: fijo, energiaKm: precioKm, total: fijo + precioKm * d.km * d.anos };
}
function calcular(d) {
  var precioKwh = d.pctCasa / 100 * d.kwhCasa + (1 - d.pctCasa / 100) * d.kwhPublico;
  var tipos = [
    { compra: d.compraDiesel, consumo: d.consDiesel, precioEnergia: d.precioDiesel, seguro: d.seguroDiesel, mant: d.mantDiesel, imp: d.impDiesel, residual: d.resDiesel },
    { compra: d.compraGasolina, consumo: d.consGasolina, precioEnergia: d.precioGasolina, seguro: d.seguroGasolina, mant: d.mantGasolina, imp: d.impGasolina, residual: d.resGasolina },
    { compra: d.compraHibrido, consumo: d.consHibrido, precioEnergia: d.precioGasolina, seguro: d.seguroHibrido, mant: d.mantHibrido, imp: d.impHibrido, residual: d.resHibrido },
    { compra: d.compraElectrico, consumo: d.consElectrico, precioEnergia: precioKwh, seguro: d.seguroElectrico, mant: d.mantElectrico, imp: d.impElectrico, residual: d.resElectrico }
  ];
  var c = tipos.map(function (t) { return costeTipo(d, t); });
  var kmTotal = d.km * d.anos, meses = d.anos * 12;
  var totales = c.map(function (x) { return x.total; });
  var orden = [0, 1, 2, 3].sort(function (a, b) { return totales[a] - totales[b]; });
  var g = orden[0], s = orden[1];
  // Punto en que el primero y el segundo cuestan lo mismo: fijo_g + e_g*k*anos = fijo_s + e_s*k*anos
  var den = (c[g].energiaKm - c[s].energiaKm) * d.anos, kmEq = 0, hay = 0;
  if (den !== 0) { var k = (c[s].fijo - c[g].fijo) / den; if (k > 0 && isFinite(k)) { kmEq = k; hay = 1; } }
  return {
    costeDiesel: totales[0], costeGasolina: totales[1], costeHibrido: totales[2], costeElectrico: totales[3],
    costeKmDiesel: totales[0] / kmTotal, costeKmGasolina: totales[1] / kmTotal, costeKmHibrido: totales[2] / kmTotal, costeKmElectrico: totales[3] / kmTotal,
    mesDiesel: totales[0] / meses, mesGasolina: totales[1] / meses, mesHibrido: totales[2] / meses, mesElectrico: totales[3] / meses,
    costeKmX: totales[g] / kmTotal, ganador: g, segundo: s, orden: orden,
    kmEquilibrio: kmEq, hayEquilibrio: hay, diferencia: totales[s] - totales[g], precioKwh: precioKwh
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
var IDS = ["km", "anos", "compraDiesel", "compraGasolina", "compraHibrido", "compraElectrico", "consDiesel", "consGasolina", "consHibrido", "consElectrico",
  "precioDiesel", "precioGasolina", "kwhCasa", "pctCasa", "kwhPublico", "seguroDiesel", "seguroGasolina", "seguroHibrido", "seguroElectrico",
  "mantDiesel", "mantGasolina", "mantHibrido", "mantElectrico", "impDiesel", "impGasolina", "impHibrido", "impElectrico",
  "resDiesel", "resGasolina", "resHibrido", "resElectrico"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.km <= 0 || d.anos <= 0) return;
  var r = calcular(d), tot = [r.costeDiesel, r.costeGasolina, r.costeHibrido, r.costeElectrico];
  var km = [r.costeKmDiesel, r.costeKmGasolina, r.costeKmHibrido, r.costeKmElectrico], mes = [r.mesDiesel, r.mesGasolina, r.mesHibrido, r.mesElectrico];
  var g = NOMBRES[r.ganador], s = NOMBRES[r.segundo];
  var h = '<div class="verdict">Con estos números, el ' + g.toLowerCase() + ' es el más barato en ' + d.anos + ' años: ' + eur(r.diferencia) + ' menos que el ' + s.toLowerCase() + ' (segundo).</div>';
  h += '<table><tr><th></th><th class="n">Coste total</th><th class="n">€/km</th><th class="n">€/mes</th></tr>';
  r.orden.forEach(function (i, pos) {
    h += '<tr><td>' + (pos + 1) + '. ' + NOMBRES[i] + '</td><td class="n">' + eur(tot[i]) + '</td><td class="n">' + eur2(km[i]) + '</td><td class="n">' + eur2(mes[i]) + '</td></tr>';
  });
  h += '</table><div class="box"><strong>Lectura:</strong> ';
  if (r.hayEquilibrio) h += 'el orden entre ' + g.toLowerCase() + ' y ' + s.toLowerCase() + ' cambia a unos ' + Math.round(r.kmEquilibrio).toLocaleString("es-ES") + ' km al año (tú has puesto ' + d.km.toLocaleString("es-ES") + '). ';
  else h += 'entre ' + g.toLowerCase() + ' y ' + s.toLowerCase() + ' el orden no cambia con los kilómetros: el ganador es más barato tanto de compra como de uso. ';
  h += 'El precio medio del kWh con tu reparto de carga es ' + r.precioKwh.toFixed(3).replace(".", ",") + ' €/kWh. El resultado depende mucho del valor residual y del precio de la energía: cámbialos y compara.</div>';
  var el = document.getElementById("r"); el.innerHTML = h; el.style.display = "block";
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
