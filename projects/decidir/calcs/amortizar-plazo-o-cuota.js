// Amortización francesa. Devuelve {cuota, meses, intereses} simulando mes a mes (exacto, incluye última cuota parcial).
function simular(P, i, cuota, maxMeses) {
  var intereses = 0, m = 0, saldo = P;
  while (saldo > 0.005 && m < maxMeses + 1) {
    var intMes = saldo * i, amort = Math.min(cuota - intMes, saldo);
    if (amort <= 0) return null; // la cuota no cubre intereses
    intereses += intMes; saldo -= amort; m++;
  }
  return { meses: m, intereses: intereses };
}
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
function calcular(d) {
  var i = d.tipo / 100 / 12, P = d.capital, n = d.meses, E = Math.min(d.extra, P), com = E * d.comision / 100;
  var cuota0 = cuotaFrancesa(P, i, n);
  var base = simular(P, i, cuota0, n);
  var Pn = P - E;
  var cuotaA = cuotaFrancesa(Pn, i, n);          // reducir cuota, mismo plazo
  var A = simular(Pn, i, cuotaA, n);
  var B = simular(Pn, i, cuota0, n);              // reducir plazo, misma cuota
  return {
    cuota0: cuota0, intBase: base.intereses,
    cuotaA: cuotaA, mesesA: A.meses, intA: A.intereses, ahorroA: base.intereses - A.intereses - com, aliviomes: cuota0 - cuotaA,
    cuotaB: cuota0, mesesB: B.meses, intB: B.intereses, ahorroB: base.intereses - B.intereses - com, mesesMenos: n - B.meses,
    comision: com
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function leer() {
  var d = {}; ["capital", "tipo", "meses", "extra", "comision"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.capital <= 0 || d.meses <= 0 || d.extra <= 0) return;
  var r = calcular(d), dif = r.ahorroB - r.ahorroA, anos = Math.floor(r.mesesMenos / 12), mesesR = r.mesesMenos % 12;
  var plazoTxt = (anos ? anos + " año" + (anos > 1 ? "s" : "") : "") + (anos && mesesR ? " y " : "") + (mesesR ? mesesR + " mes" + (mesesR > 1 ? "es" : "") : "");
  var h = '<div class="verdict">Reduciendo plazo ahorras ' + eur(r.ahorroB) + ' en intereses, ' + eur(dif) + ' más que reduciendo cuota.</div>';
  h += '<table><tr><th></th><th class="n">Reducir cuota</th><th class="n">Reducir plazo</th></tr>';
  h += '<tr><td>Cuota mensual</td><td class="n">' + eur2(r.cuotaA) + '</td><td class="n">' + eur2(r.cuotaB) + '</td></tr>';
  h += '<tr><td>Meses restantes</td><td class="n">' + r.mesesA + '</td><td class="n">' + r.mesesB + '</td></tr>';
  h += '<tr><td>Intereses que pagarás</td><td class="n">' + eur(r.intA) + '</td><td class="n">' + eur(r.intB) + '</td></tr>';
  h += '<tr><td><strong>Ahorro de intereses</strong>' + (r.comision ? ' (tras ' + eur2(r.comision) + ' de comisión)' : '') + '</td><td class="n"><strong>' + eur(r.ahorroA) + '</strong></td><td class="n"><strong>' + eur(r.ahorroB) + '</strong></td></tr></table>';
  h += '<div class="box"><strong>Lectura:</strong> hoy pagas ' + eur2(r.cuota0) + ' al mes y te quedan ' + eur(r.intBase) + ' de intereses. ';
  h += 'Si reduces cuota, cada mes te quedas ' + eur2(r.aliviomes) + ' más en el bolsillo. Si reduces plazo, terminas ' + plazoTxt + ' antes. ';
  if (r.aliviomes * 12 * 3 > r.ahorroB) h += 'La diferencia de ahorro es pequeña frente al alivio mensual: si vas justo, reducir cuota es razonable.';
  else h += 'La diferencia de ahorro es grande: salvo que necesites el alivio mensual, reducir plazo es la opción que más dinero te deja.';
  h += '</div>';
  var el = document.getElementById("r"); el.innerHTML = h; el.style.display = "block";
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
