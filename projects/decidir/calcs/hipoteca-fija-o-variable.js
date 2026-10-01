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
    anosRestantes: d.anos - 1
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function pct(x) { return x.toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " %"; }
function leer() {
  var d = {}; ["capital", "anos", "fijo", "dif", "euribor", "escenario"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.capital <= 0 || d.anos < 2) return;
  var r = calcular(d), abs = Math.abs(r.diferencia);
  var h;
  if (abs < 1) h = '<div class="verdict">En este escenario las dos opciones pagan los mismos intereses.</div>';
  else if (r.diferencia > 0) h = '<div class="verdict">En este escenario la fija te sale ' + eur(abs) + ' más barata en intereses.</div>';
  else h = '<div class="verdict">En este escenario la variable te sale ' + eur(abs) + ' más barata en intereses.</div>';
  h += '<table><tr><th></th><th class="n">Fija</th><th class="n">Variable</th></tr>';
  h += '<tr><td>Cuota el primer año</td><td class="n">' + eur2(r.cuotaFija) + '</td><td class="n">' + eur2(r.cuotaVar1) + '</td></tr>';
  h += '<tr><td>Cuota tras la primera revisión</td><td class="n">' + eur2(r.cuotaFija) + '</td><td class="n">' + eur2(r.cuotaVar2) + '</td></tr>';
  h += '<tr><td>Intereses totales</td><td class="n"><strong>' + eur(r.intFija) + '</strong></td><td class="n"><strong>' + eur(r.intVar) + '</strong></td></tr>';
  h += '<tr><td>Total a devolver</td><td class="n">' + eur(r.totalFija) + '</td><td class="n">' + eur(r.totalVar) + '</td></tr></table>';
  h += '<div class="box"><strong>Lectura:</strong> el Euríbor de equilibrio es <strong>' + pct(r.euriborEquilibrio) + '</strong>. ';
  h += 'Si crees que el Euríbor medio de los próximos ' + r.anosRestantes + ' años estará por encima de ' + pct(r.euriborEquilibrio) + ', te conviene la fija; si crees que estará por debajo, la variable pagará menos intereses. ';
  h += 'Hoy el Euríbor está en ' + pct(d.euribor) + ' y en tu escenario lo usamos a ' + pct(r.euriborEsc) + '. ';
  h += 'Si el Euríbor se descontrola, tu cuota variable puede cambiar mucho en cada revisión; la fija no se mueve.';
  h += '</div>';
  var el = document.getElementById("r"); el.innerHTML = h; el.style.display = "block";
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
