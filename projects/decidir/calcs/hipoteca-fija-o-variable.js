// Amortización francesa. Cuota mensual para capital P, tipo mensual i y n meses.
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
// Intereses totales de un préstamo a tipo fijo.
function interesesFijo(P, i, n) { return cuotaFrancesa(P, i, n) * n - P; }
// Variable: tipo1 (% anual) el primer año; después tipo2 (% anual), recalculando la cuota en la revisión.
// Devuelve {cuota1, cuota2, intereses}. El tipo nunca baja de 0 %.
function simularVariable(P, n, tipo1, tipo2) {
  var i1 = Math.max(tipo1, 0) / 1200, i2 = Math.max(tipo2, 0) / 1200;
  var c1 = cuotaFrancesa(P, i1, n), saldo = P, inter = 0, m = Math.min(12, n);
  for (var k = 0; k < m; k++) { var im = saldo * i1; inter += im; saldo -= c1 - im; }
  if (n <= 12) return { cuota1: c1, cuota2: c1, intereses: inter };
  var c2 = cuotaFrancesa(saldo, i2, n - 12);
  return { cuota1: c1, cuota2: c2, intereses: inter + c2 * (n - 12) - saldo };
}
// Euríbor medio (años 2 en adelante) a partir del cual la variable paga más intereses que la fija. Bisección.
function euriborEquilibrio(P, n, euribor, dif, intFija) {
  var lo = -5, hi = 30;
  for (var k = 0; k < 100; k++) {
    var mid = (lo + hi) / 2;
    if (simularVariable(P, n, euribor + dif, mid + dif).intereses > intFija) hi = mid; else lo = mid;
  }
  return (lo + hi) / 2;
}
function calcular(d) {
  var P = d.capital, n = Math.round(d.anos * 12), iF = d.fijo / 1200;
  var cuotaFija = cuotaFrancesa(P, iF, n), intFija = interesesFijo(P, iF, n);
  var euriborEsc = d.euribor + d.escenario;
  var v = simularVariable(P, n, d.euribor + d.dif, euriborEsc + d.dif);
  var eq = euriborEquilibrio(P, n, d.euribor, d.dif, intFija);
  return {
    cuotaFija: cuotaFija, intFija: intFija, totalFija: cuotaFija * n,
    cuotaVar1: v.cuota1, cuotaVar2: v.cuota2, intVar: v.intereses, totalVar: P + v.intereses,
    euriborEsc: euriborEsc, euriborEquilibrio: eq,
    diferencia: v.intereses - intFija, // >0: la fija paga menos; <0: la variable paga menos
    // Sin cruce dentro de [-5 %, 30 %]: la bisección se queda en un extremo. «fija»: la variable cuesta más con cualquier Euríbor (p. ej. fija al 0 %).
    sinEquilibrio: eq <= -4.99 ? "fija" : eq >= 29.99 ? "variable" : "",
    anosRestantes: Math.round((d.anos - 1) * 10) / 10
  };
}
function anosTxt(x) { return (Math.round(x * 10) / 10).toLocaleString("es-ES", { maximumFractionDigits: 1 }); }
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function pct(x) { return x.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + "\u00a0%"; }
function leer() {
  var d = {}; ["capital", "anos", "fijo", "dif", "euribor", "escenario"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.capital <= 0 || d.anos < 2) return;
  var r = calcular(d), abs = Math.abs(r.diferencia), verdict, gana;
  if (abs < 1) verdict = 'En este escenario las dos opciones pagan los mismos intereses.';
  else if (r.diferencia > 0) { gana = "fija"; verdict = 'En este escenario la fija te sale ' + EM.eur(abs) + ' más barata en intereses.'; }
  else { gana = "variable"; verdict = 'En este escenario la variable te sale ' + EM.eur(abs) + ' más barata en intereses.'; }
  var note = '<p><strong>Lectura:</strong> ';
  if (r.sinEquilibrio === "fija") note += 'con estos tipos la fija paga menos intereses con cualquier Euríbor razonable (no hay Euríbor de equilibrio). ';
  else if (r.sinEquilibrio === "variable") note += 'con estos tipos la variable paga menos intereses con cualquier Euríbor razonable (no hay Euríbor de equilibrio). ';
  else {
    note += 'el Euríbor de equilibrio es <strong>' + pct(r.euriborEquilibrio) + '</strong>. ';
    note += 'Si el Euríbor se queda, de forma estable, por encima de ' + pct(r.euriborEquilibrio) + ' durante los ' + anosTxt(r.anosRestantes) + ' años siguientes al primero, te conviene la fija; si se queda por debajo, la variable pagará menos intereses. ';
    note += 'Si sube o baja con el tiempo el resultado cambia, y los primeros años pesan más. ';
  }
  note += 'Hoy el Euríbor está en ' + pct(d.euribor) + ' y en tu escenario lo usamos a ' + pct(r.euriborEsc) + '. ';
  note += 'Si el Euríbor se descontrola, tu cuota variable puede cambiar mucho en cada revisión; la fija no se mueve.</p>';
  EM.renderResult({
    winner: gana || "empate",
    verdict: verdict,
    tone: !gana || abs < r.intFija * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: gana ? "menos de intereses con la " + gana + " en tu escenario" : "de diferencia en intereses",
    format: EM.eur,
    barsLabel: "Intereses totales que pagarías",
    bars: [{ label: "Fija", value: r.intFija, color: "a" }, { label: "Variable", value: r.intVar, color: "b" }],
    cols: ["Fija", "Variable"],
    rows: [
      ["Cuota el primer año", EM.eur(r.cuotaFija, 2), EM.eur(r.cuotaVar1, 2)],
      ["Cuota tras la primera revisión", EM.eur(r.cuotaFija, 2), EM.eur(r.cuotaVar2, 2)],
      { label: "Intereses totales", values: [EM.eur(r.intFija), EM.eur(r.intVar)], strong: true },
      ["Total a devolver", EM.eur(r.totalFija), EM.eur(r.totalVar)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
