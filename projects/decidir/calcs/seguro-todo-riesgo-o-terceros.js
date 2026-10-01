// Cada año y (0 = año en curso) el coche vale valor·(1-dep)^y a inicio de año. El todo riesgo paga, si hay siniestro con culpa propia,
// el menor entre el coste de reparación y el valor del coche, menos la franquicia. Pérdida esperada cubierta = probabilidad · ese pago.
function cubiertoAnio(d, y) {
  var v = d.valor * Math.pow(1 - d.deprec / 100, y);
  return { valor: v, cubierto: d.prob / 100 * Math.max(Math.min(d.coste, v) - d.franquicia, 0) };
}
function calcular(d) {
  var N = Math.max(Math.round(d.anos), 1), dif = d.primaTR - d.primaTerceros, acum = 0, anoLimite = 0, valores = [];
  for (var y = 0; y < N; y++) {
    var a = cubiertoAnio(d, y); acum += a.cubierto; valores.push(a.valor);
    if (anoLimite === 0 && dif > 0 && a.cubierto < dif) anoLimite = y + 1;
  }
  var p = d.prob / 100, umbral = (dif > 0 && p > 0) ? d.franquicia + dif / p : 0;
  var saldo = acum - dif * N;
  return {
    difPrimaAcum: dif * N, cubiertoEsperado: acum, saldoTodoRiesgo: saldo, valorUmbral: umbral,
    multiploUmbral: (dif > 0 && umbral > 0) ? umbral / dif : 0, anoLimite: anoLimite, valorFinal: valores[N - 1],
    primaExtraAnual: dif, compensaDesdeElInicio: dif <= 0 || anoLimite !== 1,
    ganador: Math.abs(saldo) < 1 ? "empate" : (saldo > 0 ? "todo riesgo" : "terceros")
  };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["valor", "deprec", "primaTerceros", "primaTR", "franquicia", "prob", "coste", "anos"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.valor <= 0 || d.anos < 1 || d.prob < 0 || d.prob > 100 || d.deprec < 0 || d.deprec >= 100) return;
  var r = calcular(d), abs = Math.abs(r.saldoTodoRiesgo), tr = r.saldoTodoRiesgo > 0, ref = Math.max(r.difPrimaAcum, 1);
  var verdict = abs < 1 ? 'Con estos supuestos, el todo riesgo y los terceros te cuestan lo mismo en ' + d.anos + ' años.'
    : 'Con estos supuestos, ' + (tr ? 'el todo riesgo' : 'el seguro a terceros') + ' te sale ' + EM.eur(abs) + ' mejor en ' + d.anos + ' años.';
  var note = '<p><strong>Lectura:</strong> ';
  if (r.primaExtraAnual <= 0) note += 'el todo riesgo no cuesta más que los terceros, así que cubre más por el mismo dinero o menos. ';
  else if (r.valorUmbral <= 0) note += 'con probabilidad 0 el todo riesgo nunca recupera su sobreprima. ';
  else if (r.valorUmbral >= d.coste) note += 'el todo riesgo te cuesta ' + EM.eur(r.primaExtraAnual) + ' más al año y, con una reparación media de ' + EM.eur(d.coste) + ' y esa probabilidad, no recupera esa sobreprima aunque el coche valga mucho. ';
  else {
    note += 'el todo riesgo te cuesta ' + EM.eur(r.primaExtraAnual) + ' más al año y solo compensa mientras el coche valga más de <strong>' + EM.eur(r.valorUmbral) + '</strong> (' + EM.num(r.multiploUmbral, 1) + ' veces esa sobreprima). ';
    if (r.anoLimite === 1) note += 'Con tus datos ya no compensa desde el primer año. ';
    else if (r.anoLimite > 1) note += 'A partir del año ' + r.anoLimite + ' deja de compensar. ';
    else note += 'En los ' + d.anos + ' años comparados no cruzas ese umbral. ';
  }
  note += 'La pérdida es una media: un solo siniestro grave puede superar la cifra, y el todo riesgo también cubre otros daños que aquí no se cuentan. Depende de tu perfil y de tu margen para asumir un golpe.</p>';
  EM.renderResult({
    winner: abs < 1 ? "empate" : (tr ? "todo riesgo" : "terceros"),
    verdict: verdict,
    tone: abs < ref * 0.1 ? "warn" : "ok",
    bigNumber: abs, bigLabel: abs < 1 ? "de diferencia" : "mejor con " + (tr ? "todo riesgo" : "terceros"), format: EM.eur,
    barsLabel: "Sobreprima frente a pérdida esperada cubierta (" + d.anos + " años)",
    bars: [{ label: "Sobreprima del todo riesgo", value: Math.max(r.difPrimaAcum, 0), color: "a" },
           { label: "Pérdida esperada que cubre", value: Math.max(r.cubiertoEsperado, 0), color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Sobreprima acumulada del todo riesgo", EM.eur(r.difPrimaAcum)],
      ["Daños propios esperados que te cubre", EM.eur(r.cubiertoEsperado)],
      ["Valor del coche en el último año", EM.eur(r.valorFinal)],
      { label: "Saldo del todo riesgo (negativo = gana terceros)", values: [EM.eur(r.saldoTodoRiesgo)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
