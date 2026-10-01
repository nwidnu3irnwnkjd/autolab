// Cuota francesa para capital P, tipo anual r (%) y n meses; saldo pendiente tras k cuotas.
function cuotaFr(P, r, n) { var i = r / 1200; return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
function saldoTras(P, r, n, k) {
  var i = r / 1200, c = cuotaFr(P, r, n), s = P;
  for (var m = 0; m < k; m++) s = s * (1 + i) - c;
  return Math.max(s, 0);
}
// Ahorro neto acumulado tras k meses al cambiar: cuotas que dejas de pagar (menos vinculaciones) + deuda que te queda de menos − coste del cambio.
function ahorroNeto(d, tipoNuevo, k) {
  var n = Math.max(Math.round(d.anos * 12), 1), coste = d.capital * d.comision / 100 + d.gastos;
  var ca = cuotaFr(d.capital, d.tipoActual, n), cn = cuotaFr(d.capital, tipoNuevo, n);
  return k * (ca - cn - d.vinculacion / 12) + saldoTras(d.capital, d.tipoActual, n, k) - saldoTras(d.capital, tipoNuevo, n, k) - coste;
}
function calcular(d) {
  var n = Math.max(Math.round(d.anos * 12), 1), coste = d.capital * d.comision / 100 + d.gastos;
  var ca = cuotaFr(d.capital, d.tipoActual, n), cn = cuotaFr(d.capital, d.tipoNuevo, n);
  var intAct = ca * n - d.capital, intNue = cn * n - d.capital;
  var k5 = Math.min(60, n), kh = Math.min(Math.max(Math.round(d.horizonte * 12), 1), n), eq = 0;
  for (var k = 1; k <= n; k++) { if (ahorroNeto(d, d.tipoNuevo, k) >= 0) { eq = k; break; } }
  var netoH = ahorroNeto(d, d.tipoNuevo, kh), tipoEq = null;
  if (ahorroNeto(d, 0, kh) >= 0 && ahorroNeto(d, d.tipoActual, kh) <= 0) {
    var lo = 0, hi = d.tipoActual;
    for (var j = 0; j < 100; j++) { var mid = (lo + hi) / 2; if (ahorroNeto(d, mid, kh) >= 0) lo = mid; else hi = mid; }
    tipoEq = (lo + hi) / 2;
  }
  return {
    cuotaActual: ca, cuotaNueva: cn, ahorroCuota: ca - cn - d.vinculacion / 12, ahorroIntereses: intAct - intNue,
    costeCambio: coste, mesesEquilibrio: eq, nuncaRecupera: eq === 0, ahorroNeto5: ahorroNeto(d, d.tipoNuevo, k5),
    ahorroNetoPlazo: ahorroNeto(d, d.tipoNuevo, n), ahorroNetoHorizonte: netoH, tipoEquilibrio: tipoEq,
    mesesHorizonte: kh, ganador: Math.abs(netoH) < 1 ? "empate" : (netoH > 0 ? "cambiar" : "mantener")
  };
}
function eur(x) { return EM.eur(x); }
function pct(x) { return x.toLocaleString("es-ES", { maximumFractionDigits: 2 }) + " %"; }
function leer() {
  var d = {}; ["capital", "tipoActual", "anos", "tipoNuevo", "comision", "gastos", "vinculacion", "horizonte"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.capital <= 0 || d.anos < 1 || d.tipoActual < 0 || d.tipoNuevo < 0 || d.horizonte < 1 || d.comision < 0 || d.gastos < 0 || d.vinculacion < 0) return;
  var r = calcular(d), abs = Math.abs(r.ahorroNetoHorizonte), ca = r.ganador === "cambiar", hor = r.mesesHorizonte / 12, ref = Math.max(r.costeCambio, 1);
  var verdict = r.ganador === "empate" ? 'Con estos supuestos, cambiar de hipoteca y quedarte como estás te dejan lo mismo a ' + EM.num(hor, 1) + ' años.'
    : 'Con estos supuestos, ' + (ca ? 'cambiar de hipoteca' : 'quedarte como estás') + ' te deja ' + EM.eur(abs) + ' más a ' + EM.num(hor, 1) + ' años.';
  var note = '<p><strong>Lectura:</strong> el cambio te cuesta ' + EM.eur(r.costeCambio) + ' (comisión y gastos). ';
  if (r.nuncaRecupera) note += 'Con estas condiciones no llegas a recuperar ese dinero antes de terminar la hipoteca. ';
  else note += 'Lo recuperas en <strong>' + r.mesesEquilibrio + ' meses</strong> (' + EM.num(r.mesesEquilibrio / 12, 1) + ' años): si piensas vender o cancelar antes, no compensa. ';
  if (r.tipoEquilibrio !== null) note += 'A ese horizonte, el cambio compensa si el tipo nuevo es inferior a <strong>' + pct(r.tipoEquilibrio) + '</strong>. ';
  note += 'Comprueba en tu escritura la comisión de cancelación y el límite legal aplicable (consulta la norma en el BOE); la oferta nueva debe darte una FEIN con las condiciones vinculantes. Las bonificaciones solo valen si mantienes los productos vinculados.</p>';
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: abs < ref * 0.1 ? "warn" : "ok",
    bigNumber: abs, bigLabel: r.ganador === "empate" ? "de diferencia" : "más si " + (ca ? "cambias" : "te quedas"), format: EM.eur,
    barsLabel: "Coste del cambio frente a ahorro de intereses",
    bars: [{ label: "Coste del cambio", value: r.costeCambio, color: "a" }, { label: "Ahorro de intereses (todo el plazo)", value: Math.max(r.ahorroIntereses, 0), color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Cuota actual", EM.eur(r.cuotaActual, 2)],
      ["Cuota nueva (sin vinculaciones)", EM.eur(r.cuotaNueva, 2)],
      ["Ahorro mensual neto de vinculaciones", EM.eur(r.ahorroCuota, 2)],
      ["Ahorro de intereses en todo el plazo", EM.eur(r.ahorroIntereses)],
      ["Ahorro neto a 5 años", EM.eur(r.ahorroNeto5)],
      ["Ahorro neto a plazo restante", EM.eur(r.ahorroNetoPlazo)],
      { label: "Ahorro neto al horizonte elegido (negativo = mejor quedarte)", values: [EM.eur(r.ahorroNetoHorizonte)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
