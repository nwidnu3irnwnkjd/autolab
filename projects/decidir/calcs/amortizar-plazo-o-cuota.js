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
  var pequena = r.aliviomes * 12 * 3 > r.ahorroB;
  var note = '<p><strong>Lectura:</strong> hoy pagas ' + eur2(r.cuota0) + ' al mes y te quedan ' + eur(r.intBase) + ' de intereses. ';
  note += 'Si reduces cuota, cada mes te quedas ' + eur2(r.aliviomes) + ' más en el bolsillo. Si reduces plazo, terminas ' + plazoTxt + ' antes. ';
  if (pequena) note += 'La diferencia de ahorro es pequeña frente al alivio mensual: si vas justo, reducir cuota es razonable.';
  else note += 'La diferencia de ahorro es grande: salvo que necesites el alivio mensual, reducir plazo es la opción que más dinero te deja.';
  note += '</p>';
  EM.renderResult({
    verdict: 'Reduciendo plazo ahorras ' + eur(r.ahorroB) + ' en intereses, ' + eur(dif) + ' más que reduciendo cuota.',
    tone: pequena ? "warn" : "ok",
    bigNumber: r.ahorroB, bigLabel: "de ahorro en intereses si reduces plazo", format: eur,
    barsLabel: "Ahorro de intereses" + (r.comision ? " (tras la comisión)" : ""),
    bars: [{ label: "Reducir cuota", value: r.ahorroA, color: "b" }, { label: "Reducir plazo", value: r.ahorroB, color: "a" }],
    cols: ["Reducir cuota", "Reducir plazo"],
    rows: [
      ["Cuota mensual", eur2(r.cuotaA), eur2(r.cuotaB)],
      ["Meses restantes", r.mesesA, r.mesesB],
      ["Intereses que pagarás", eur(r.intA), eur(r.intB)],
      { label: "Ahorro de intereses" + (r.comision ? " (tras " + eur2(r.comision) + " de comisión)" : ""), values: [eur(r.ahorroA), eur(r.ahorroB)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
