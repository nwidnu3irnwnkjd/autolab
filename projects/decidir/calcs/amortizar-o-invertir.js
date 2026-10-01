// Amortización francesa. Cuota mensual para capital P, tipo mensual i y n meses.
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
// Simula n meses. d.modo: 1 = al amortizar se reduce el plazo, 2 = se reduce la cuota.
// Amortizar: el importe (menos comisión) baja el capital; lo que ya no pagas de hipoteca cada mes se invierte.
// Invertir: el importe se invierte hoy y la hipoteca sigue igual. La aportación mensual extra se invierte en ambas.
// Al final se descuentan los impuestos sobre la ganancia (beneficio = valor final - dinero aportado).
// Patrimonio tras impuestos si liquidaras la cartera (beneficio = valor - aportado).
function neto(car, apor, imp) { return car - Math.max(car - apor, 0) * imp / 100; }
function simular(d, rentab, conSerie) {
  var n = Math.round(d.anos * 12), i = d.tipo / 1200, j = Math.pow(1 + rentab / 100, 1 / 12) - 1;
  var E = Math.min(d.importe, d.capital) / (1 + d.comision / 100), com = Math.min(d.importe, d.capital) - E;
  var cuota0 = cuotaFrancesa(d.capital, i, n), Pn = d.capital - E;
  var cuotaA = d.modo === 2 ? cuotaFrancesa(Pn, i, n) : cuota0;
  var saldo = Pn, saldoB = d.capital, serie = [], carA = 0, aporA = 0, carB = Math.min(d.importe, d.capital), aporB = carB, intA = 0, mesesA = 0;
  for (var m = 0; m < n; m++) {
    var pago = 0;
    if (saldo > 0.005) { var im = saldo * i; pago = Math.min(cuotaA, saldo + im); saldo -= pago - im; intA += im; mesesA = m + 1; }
    var libre = cuota0 - pago + d.aporte;
    carA = carA * (1 + j) + libre; aporA += libre;
    carB = carB * (1 + j) + d.aporte; aporB += d.aporte;
    if (conSerie) {
      saldoB = Math.max(saldoB - (cuota0 - saldoB * i), 0);
      if ((m + 1) % 12 === 0 || m === n - 1) serie.push({ anio: (m + 1) / 12, amortizar: neto(carA, aporA, d.impuesto) - saldo, invertir: neto(carB, aporB, d.impuesto) - saldoB });
    }
  }
  var t = d.impuesto / 100;
  var netoA = carA - Math.max(carA - aporA, 0) * t, netoB = carB - Math.max(carB - aporB, 0) * t;
  return { serie: serie, E: E, A: netoA, B: netoB, cuota0: cuota0, cuotaA: cuotaA, comision: com, mesesA: mesesA, n: n, intA: intA };
}
function intereses(d) {
  var n = Math.round(d.anos * 12), i = d.tipo / 1200, c = cuotaFrancesa(d.capital, i, n);
  return c * n - d.capital;
}
function calcular(d) {
  var s = simular(d, d.rentab, true), dif = s.B - s.A;
  var lo = -20, hi = 60, eq = null;
  var flo = simular(d, lo), fhi = simular(d, hi);
  if ((flo.B - flo.A) * (fhi.B - fhi.A) <= 0) {
    for (var k = 0; k < 80; k++) {
      var mid = (lo + hi) / 2, sm = simular(d, mid), fm = sm.B - sm.A;
      if ((flo.B - flo.A) * fm <= 0) hi = mid; else { lo = mid; flo = sm; }
    }
    eq = (lo + hi) / 2;
  }
  // Serie anual para el gráfico: año 0 = hoy; después, patrimonio neto (cartera tras impuestos menos deuda pendiente) de cada estrategia.
  var serieAnual = [{ anio: 0, amortizar: -(d.capital - s.E), invertir: Math.min(d.importe, d.capital) - d.capital }].concat(s.serie);
  return {
    serieAnual: serieAnual,
    patrimonioAmortizar: s.A, patrimonioInvertir: s.B, diferencia: dif, rentabilidadDeEquilibrio: eq,
    ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "invertir" : "amortizar"),
    cuotaActual: s.cuota0, cuotaTrasAmortizar: s.cuotaA, mesesTrasAmortizar: s.mesesA,
    interesesAhorrados: intereses(d) - s.intA, comision: s.comision
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function pct(x) { return x.toLocaleString("es-ES", { maximumFractionDigits: 2 }) + " %"; }
function leer() {
  var d = {}; ["capital", "tipo", "anos", "importe", "aporte", "rentab", "impuesto", "comision", "modo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.rentab = parseFloat(document.getElementById("rentab").value); if (isNaN(d.rentab)) d.rentab = 0;
  return d;
}
function pintar() {
  var d = leer(); if (d.capital <= 0 || d.anos < 1 || d.importe <= 0 || d.tipo < 0 || d.aporte < 0) return;
  var r = calcular(d), abs = Math.abs(r.diferencia), inv = r.diferencia > 0, ref = Math.max(Math.abs(r.patrimonioAmortizar), Math.abs(r.patrimonioInvertir), 1);
  var verdict = abs < 1 ? 'Con estos supuestos, amortizar e invertir te dejan el mismo patrimonio dentro de ' + d.anos + ' años.'
    : 'Con estos supuestos, ' + (inv ? 'invertir' : 'amortizar') + ' te deja ' + EM.eur(abs) + ' más de patrimonio dentro de ' + d.anos + ' años.';
  var note = '<p><strong>Lectura:</strong> amortizar equivale a una inversión sin riesgo que rinde el tipo de tu hipoteca (' + pct(d.tipo) + ' al año, sin impuestos sobre esa ganancia). ';
  if (r.rentabilidadDeEquilibrio !== null) note += 'Invertir solo sale mejor si tu inversión rinde más de un <strong>' + pct(r.rentabilidadDeEquilibrio) + ' anual</strong> (antes de impuestos sobre ganancias), y esa rentabilidad no está garantizada: has supuesto ' + pct(d.rentab) + '. ';
  else note += 'En el rango de rentabilidades probado, una de las dos opciones gana siempre. ';
  note += 'Amortizar te ahorra ' + EM.eur(r.interesesAhorrados) + ' de intereses y ' + (d.modo === 2 ? 'baja tu cuota a ' + EM.eur(r.cuotaTrasAmortizar, 2) : 'termina la hipoteca ' + Math.max(Math.round(d.anos * 12) - r.mesesTrasAmortizar, 0) + ' meses antes') + '. ';
  note += 'Antes de decidir, conserva un colchón de liquidez: el dinero amortizado no se recupera, el invertido sí.</p>';
  EM.renderResult({
    winner: abs < 1 ? "empate" : (inv ? "invertir" : "amortizar"),
    verdict: verdict,
    tone: abs < ref * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: abs < 1 ? "de diferencia" : "más de patrimonio si " + (inv ? "inviertes" : "amortizas"), format: EM.eur,
    line: { caption: "Patrimonio neto año a año (cartera tras impuestos menos deuda)", xLabel: "Años", xFormat: function (a) { return "año " + a; }, yFormat: EM.eur,
      series: [{ label: "Amortizar", color: "a", points: r.serieAnual.map(function (v) { return [v.anio, v.amortizar]; }) },
               { label: "Invertir", color: "b", points: r.serieAnual.map(function (v) { return [v.anio, v.invertir]; }) }] },
    barsLabel: "Patrimonio neto dentro de " + d.anos + " años",
    bars: [{ label: "Amortizar" + (!inv && abs >= 1 ? " (gana)" : ""), value: Math.max(r.patrimonioAmortizar, 0), color: "a" },
           { label: "Invertir" + (inv && abs >= 1 ? " (gana)" : ""), value: Math.max(r.patrimonioInvertir, 0), color: "b" }],
    cols: ["Amortizar", "Invertir"],
    rows: [
      ["Cuota de la hipoteca", EM.eur(r.cuotaTrasAmortizar, 2), EM.eur(r.cuotaActual, 2)],
      ["Rentabilidad asumida", pct(d.tipo) + " (el tipo)", pct(d.rentab) + " (no garantizada)"],
      { label: "Patrimonio neto al final", values: [EM.eur(r.patrimonioAmortizar), EM.eur(r.patrimonioInvertir)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
