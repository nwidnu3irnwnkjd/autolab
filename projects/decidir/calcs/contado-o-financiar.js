// Amortización francesa: cuota mensual para capital P, tipo mensual i y n meses.
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
// Condiciones del préstamo: importe financiado, cuota (con seguro) y comisión de apertura.
function prestamo(d) {
  var L = Math.max(d.precio - d.entrada, 0), n = Math.max(Math.round(d.plazo), 1);
  var cuota = L > 0 ? cuotaFrancesa(L, d.tin / 1200, n) + d.seguro : 0;
  return { L: L, n: n, cuota: cuota, com: L * d.comision / 100 };
}
// Financiar: conservas invertido el dinero que costaría pagar al contado (con descuento), menos la entrada y la comisión,
// y de ahí sale cada cuota. Pagar al contado: ese dinero se gasta hoy (patrimonio 0). Devuelve la ventaja de financiar al final.
// La ganancia de la inversión tributa una vez al final (solo si es positiva).
function simular(d, rentab) {
  var p = prestamo(d), K = d.precio * (1 - d.descuento / 100), B = K - d.entrada - p.com, j = Math.pow(1 + rentab / 100, 1 / 12) - 1, G = 0;
  for (var m = 0; m < p.n; m++) { G += B * j; B = B * (1 + j) - p.cuota; }
  var imp = d.impuesto / 100 * Math.max(G, 0);
  return { ventaja: B - imp, ganancia: G, rendimientoNeto: G - imp, p: p };
}
// Coste efectivo anual del préstamo por bisección: valor actual de las cuotas = importe recibido menos comisión.
function taeReal(p) {
  if (p.L <= 0) return null;
  var neto = p.L - p.com, lo = -0.05, hi = 1;
  for (var k = 0; k < 200; k++) {
    var mid = (lo + hi) / 2, pv = 0;
    for (var m = 1; m <= p.n; m++) pv += p.cuota / Math.pow(1 + mid, m);
    if (pv > neto) lo = mid; else hi = mid;
  }
  return (Math.pow(1 + (lo + hi) / 2, 12) - 1) * 100;
}
function calcular(d) {
  var s = simular(d, d.rentab), p = s.p, desc = d.precio * d.descuento / 100;
  var coste = p.cuota * p.n - p.L + p.com;
  var lo = -20, hi = 60, flo = simular(d, lo).ventaja, fhi = simular(d, hi).ventaja, eq = null;
  if (flo * fhi <= 0) {
    for (var k = 0; k < 200; k++) {
      var mid = (lo + hi) / 2, fm = simular(d, mid).ventaja;
      if (flo * fm <= 0) hi = mid; else { lo = mid; flo = fm; }
    }
    eq = (lo + hi) / 2;
  }
  return {
    costeFinanciar: coste, rendimientoNeto: s.rendimientoNeto, descuentoPerdido: desc, ventajaFinanciar: s.ventaja,
    tae: taeReal(p), rentabilidadDeEquilibrio: eq, cuota: p.cuota, comision: p.com, importeFinanciado: p.L,
    ganador: Math.abs(s.ventaja) < 1 ? "empate" : (s.ventaja > 0 ? "financiar" : "contado")
  };
}
function eur(x) { return EM.eur(x); }
function pct(x) { return x.toLocaleString("es-ES", { maximumFractionDigits: 2 }) + " %"; }
function leer() {
  var d = {}; ["precio", "entrada", "tin", "comision", "plazo", "seguro", "rentab", "impuesto", "descuento"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.rentab = parseFloat(document.getElementById("rentab").value); if (isNaN(d.rentab)) d.rentab = 0;
  return d;
}
function pintar() {
  var d = leer(); if (d.precio <= 0 || d.plazo < 1 || d.entrada < 0 || d.entrada > d.precio || d.tin < 0) return;
  var r = calcular(d), abs = Math.abs(r.ventajaFinanciar), fin = r.ventajaFinanciar > 0, ref = Math.max(r.costeFinanciar, d.precio * 0.02, 1);
  var verdict = abs < 1 ? 'Con estos supuestos, pagar al contado y financiar te dejan el mismo dinero al final.'
    : 'Con estos supuestos, ' + (fin ? 'financiar' : 'pagar al contado') + ' te deja ' + EM.eur(abs) + ' más al terminar de pagar.';
  var note = '<p><strong>Lectura:</strong> ';
  if (r.importeFinanciado <= 0) note += 'no financias nada (la entrada cubre el precio), así que solo cuenta el descuento por pago al contado. ';
  else {
    note += 'financiar cuesta ' + EM.eur(r.costeFinanciar) + ' entre intereses, comisión y seguros, y el préstamo sale a una TAE real del <strong>' + pct(r.tae) + '</strong>. ';
    if (r.rentabilidadDeEquilibrio !== null) note += 'Financiar solo compensa si tu dinero rinde más de un <strong>' + pct(r.rentabilidadDeEquilibrio) + ' anual</strong> antes de impuestos, y esa rentabilidad no está garantizada: has supuesto ' + pct(d.rentab) + '. ';
    else note += 'En el rango de rentabilidades probado, una de las dos opciones gana siempre. ';
  }
  if (d.descuento > 0) note += 'Pagar al contado te ahorra ' + EM.eur(r.descuentoPerdido) + ' por el descuento. ';
  note += 'Si el dinero lo necesitas como colchón, financiar te da liquidez; si no, comprueba que las cuotas no te aprieten.</p>';
  EM.renderResult({
    winner: abs < 1 ? "empate" : (fin ? "financiar" : "contado"),
    verdict: verdict,
    tone: abs < ref * 0.1 ? "warn" : "ok",
    bigNumber: abs, bigLabel: abs < 1 ? "de diferencia" : "más si " + (fin ? "financias" : "pagas al contado"), format: EM.eur,
    barsLabel: "Lo que pesa en cada lado",
    bars: [{ label: "Coste de financiar", value: Math.max(r.costeFinanciar + r.descuentoPerdido, 0), color: "a" },
           { label: "Rendimiento neto de tu dinero", value: Math.max(r.rendimientoNeto, 0), color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Intereses, comisión y seguros", EM.eur(r.costeFinanciar)],
      ["Descuento perdido por no pagar al contado", EM.eur(r.descuentoPerdido)],
      ["Rendimiento neto de mantener el dinero", EM.eur(r.rendimientoNeto)],
      ["Cuota mensual (con seguro)", EM.eur(r.cuota, 2)],
      { label: "Ventaja de financiar (negativa = gana el contado)", values: [EM.eur(r.ventajaFinanciar)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
