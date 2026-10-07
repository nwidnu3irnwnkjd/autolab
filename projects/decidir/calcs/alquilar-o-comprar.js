// Amortización francesa. Cuota mensual para capital P, tipo mensual i y n meses.
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
// Simula mes a mes los dos escenarios y devuelve el patrimonio neto de cada uno al final de cada año.
// Comprar: valor de la vivienda - saldo pendiente - coste de venta + ahorro invertido (si alquilar costara más al mes).
// Alquilar: entrada + gastos de compra invertidos + cada mes la diferencia a favor (si comprar cuesta más al mes).
function simular(d) {
  var P = d.precio, down = P * d.entrada / 100, L = P - down, n = Math.round(d.plazo * 12);
  var i = d.interes / 1200, cuota = cuotaFrancesa(L, i, n);
  var j = Math.pow(1 + d.rentab / 100, 1 / 12) - 1;       // rentabilidad mensual equivalente
  var fijoMes = (d.ibi + d.comunidad) / 12;
  var carteraAlq = down + P * d.gastos / 100, carteraCom = 0, saldo = L, meses = Math.round(d.horizonte * 12);
  var porAno = [], costeMesCompra0 = 0;
  for (var m = 0; m < meses; m++) {
    var ano = Math.floor(m / 12);
    var valorIni = P * Math.pow(1 + d.revaloriza / 100, ano);
    var pagoHip = m < n ? cuota : 0;
    var costeCompra = pagoHip + fijoMes + valorIni * d.mant / 100 / 12;
    var alquiler = d.alquiler * Math.pow(1 + d.subida / 100, ano);
    if (m === 0) costeMesCompra0 = costeCompra;
    var dif = costeCompra - alquiler;
    carteraAlq = carteraAlq * (1 + j) + (dif > 0 ? dif : 0);
    carteraCom = carteraCom * (1 + j) + (dif < 0 ? -dif : 0);
    if (m < n) { var im = saldo * i; saldo -= cuota - im; }
    if ((m + 1) % 12 === 0) {
      var valor = P * Math.pow(1 + d.revaloriza / 100, (m + 1) / 12);
      porAno.push({ comprar: valor * (1 - d.venta / 100) - Math.max(saldo, 0) + carteraCom, alquilar: carteraAlq });
    }
  }
  return { porAno: porAno, cuota: cuota, costeMesCompra0: costeMesCompra0 };
}
function calcular(d) {
  var s = simular(d), fin = s.porAno[s.porAno.length - 1], eq = 0, ult = 0;
  for (var k = 0; k < s.porAno.length; k++) { if (s.porAno[k].comprar > s.porAno[k].alquilar) { if (!eq) eq = k + 1; ult = k + 1; } }
  // Serie anual para el gráfico: año 0 = recién comprado (si vendieras hoy: entrada menos gastos de venta) y al final de cada año.
  var P0 = d.precio, d0 = P0 * d.entrada / 100, serie = [{ anio: 0, comprar: P0 * (1 - d.venta / 100) - (P0 - d0), alquilar: d0 + P0 * d.gastos / 100 }];
  s.porAno.forEach(function (v, k) { serie.push({ anio: k + 1, comprar: v.comprar, alquilar: v.alquilar }); });
  return {
    serieAnual: serie,
    patrimonioComprar: fin.comprar, patrimonioAlquilar: fin.alquilar, diferencia: fin.comprar - fin.alquilar,
    anosEquilibrio: eq, ultimoAnoComprar: ult, cuotaHipoteca: s.cuota, costeMensualCompra: s.costeMesCompra0, costeMensualAlquiler: d.alquiler
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
var IDS = ["precio", "entrada", "interes", "plazo", "gastos", "ibi", "comunidad", "mant", "revaloriza", "alquiler", "subida", "rentab", "venta", "horizonte"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.precio <= 0 || d.plazo < 1 || d.horizonte < 1 || d.entrada < 0 || d.entrada >= 100) return;
  var r = calcular(d), abs = Math.abs(r.diferencia), comprar = r.diferencia > 0, ref = Math.max(Math.abs(r.patrimonioComprar), Math.abs(r.patrimonioAlquilar), 1);
  var verdict = (comprar ? 'Con estos supuestos, comprar te deja ' : 'Con estos supuestos, alquilar e invertir te deja ') + EM.eur(abs) + ' más de patrimonio dentro de ' + d.horizonte + ' años.';
  if (abs < 1) verdict = 'Con estos supuestos, comprar y alquilar te dejan el mismo patrimonio dentro de ' + d.horizonte + ' años.';
  var note = '<p><strong>Lectura:</strong> ';
  if (r.anosEquilibrio > 0 && !comprar && r.ultimoAnoComprar >= r.anosEquilibrio) note += 'comprar supera a alquilar entre los años <strong>' + r.anosEquilibrio + '</strong> y <strong>' + r.ultimoAnoComprar + '</strong>, pero al final de los ' + d.horizonte + ' años vuelve a ganar alquilar e invertir. ';
  else if (r.anosEquilibrio > 0) note += 'comprar empieza a superar a alquilar a partir del <strong>año ' + r.anosEquilibrio + '</strong>: si vas a vivir ahí menos tiempo, con estos supuestos alquilar sale mejor. ';
  else note += 'en estos ' + d.horizonte + ' años comprar no llega a superar a alquilar: necesitaría más revalorización, menos rentabilidad en la inversión o, según el caso, más años (con rentabilidad alta la diferencia puede empeorar con el tiempo). ';
  note += 'Comprar cuesta al mes ' + EM.eur(r.costeMensualCompra) + ' (cuota de ' + EM.eur(r.cuotaHipoteca) + ' más IBI, comunidad, seguro y mantenimiento) frente a ' + EM.eur(r.costeMensualAlquiler) + ' de alquiler. ';
  note += 'El resultado depende sobre todo del horizonte y de la revalorización que supongas: cambia esos dos datos antes de decidir.</p>';
  EM.renderResult({
    winner: abs < 1 ? "empate" : (comprar ? "comprar" : "alquilar"),
    verdict: verdict,
    tone: abs < ref * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: abs < 1 ? "de diferencia" : "más de patrimonio con " + (comprar ? "comprar" : "alquilar e invertir"),
    format: EM.eur,
    line: { caption: "Patrimonio neto año a año (comprar, tras gastos de venta)", xLabel: "Años", xFormat: function (a) { return "año " + a; }, yFormat: EM.eur,
      series: [{ label: "Comprar", color: "a", points: r.serieAnual.map(function (v) { return [v.anio, v.comprar]; }) },
               { label: "Alquilar", color: "b", points: r.serieAnual.map(function (v) { return [v.anio, v.alquilar]; }) }] },
    barsLabel: "Patrimonio neto dentro de " + d.horizonte + " años",
    bars: [{ label: "Comprar" + (comprar && abs >= 1 ? " (gana)" : ""), value: Math.max(r.patrimonioComprar, 0), color: "a" },
           { label: "Alquilar" + (!comprar && abs >= 1 ? " (gana)" : ""), value: Math.max(r.patrimonioAlquilar, 0), color: "b" }],
    cols: ["Comprar", "Alquilar"],
    rows: [
      ["Coste mensual al empezar", EM.eur(r.costeMensualCompra), EM.eur(r.costeMensualAlquiler)],
      { label: "Patrimonio neto al final", values: [EM.eur(r.patrimonioComprar), EM.eur(r.patrimonioAlquilar)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
