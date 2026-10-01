// Coste mensual de cada opción durante la etapa. Reducir jornada = ingreso neto que dejas de ganar + coste de oportunidad opcional.
function calcular(d) {
  var N = Math.max(Math.round(d.meses), 1), pctPerdida = d.perdidaNeta > 0 ? d.perdidaNeta : d.reduccion;
  var perdidaMes = d.salario * pctPerdida / 100, opMes = perdidaMes * d.oportunidad / 100;
  var mG = Math.max(d.guarderia - d.ayuda, 0), mC = d.cuidadora, mR = perdidaMes + opMes;
  var tG = mG * N, tC = mC * N, tR = mR * N;
  var m = Math.min(mG, mC, mR), g = mG === m ? "guardería" : (mC === m ? "cuidadora" : "reducir jornada");
  var otros = [mG, mC, mR].sort(function (a, b) { return a - b; });
  var f = pctPerdida / 100 * (1 + d.oportunidad / 100), mejorExterna = Math.min(mG, mC);
  var ext = mG <= mC ? "guardería" : "cuidadora";
  return {
    costeMesGuarderia: mG, costeMesCuidadora: mC, costeMesReducir: mR, totalGuarderia: tG, totalCuidadora: tC, totalReducir: tR,
    perdidaMes: perdidaMes, oportunidadMes: opMes, ahorroVsSiguiente: (otros[1] - otros[0]) * N,
    salarioEquilibrio: f > 0 ? mejorExterna / f : 0, guarderiaEquilibrio: Math.min(mC, mR) + d.ayuda,
    mejorExterna: ext, ganador: otros[1] - otros[0] < 1 / N ? "empate" : g
  };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["guarderia", "ayuda", "cuidadora", "salario", "reduccion", "perdidaNeta", "oportunidad", "meses"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.meses < 1 || d.salario < 0 || d.reduccion < 0 || d.reduccion > 100 || d.perdidaNeta < 0 || d.perdidaNeta > 100 || d.guarderia < 0 || d.cuidadora < 0 || d.ayuda < 0 || d.oportunidad < 0) return;
  var r = calcular(d), abs = r.ahorroVsSiguiente;
  var verdict = r.ganador === "empate" ? 'Con estos supuestos, las dos opciones más baratas cuestan lo mismo durante la etapa.'
    : 'Con estos supuestos, lo más barato es ' + (r.ganador === "reducir jornada" ? 'reducir jornada' : 'la ' + r.ganador) + ', con ' + EM.eur(abs) + ' menos que la siguiente opción en ' + d.meses + ' meses.';
  var note = '<p><strong>Lectura:</strong> reducir jornada gana a la ' + r.mejorExterna + ' mientras el sueldo neto de quien reduce sea inferior a <strong>' + EM.eur(r.salarioEquilibrio) + ' al mes</strong> (con tu % de pérdida y coste de oportunidad), y la guardería es la más barata mientras cueste menos de <strong>' + EM.eur(r.guarderiaEquilibrio) + ' al mes</strong>. ';
  note += 'Por defecto la pérdida neta es proporcional a la reducción, pero el IRPF y la cotización suelen suavizarla: si conoces tu nómina tras reducir, indica ese % real. Esta comparación solo cuenta dinero: no incluye conciliación, bienestar ni deducciones fiscales.</p>';
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: abs < Math.max(r.totalGuarderia, 1) * 0.05 ? "warn" : "ok",
    bigNumber: abs, bigLabel: r.ganador === "empate" ? "de diferencia" : "menos que la siguiente", format: EM.eur,
    barsLabel: "Coste total de la etapa (" + d.meses + " meses)",
    bars: [{ label: "Guardería", value: r.totalGuarderia, color: "a" }, { label: "Cuidadora", value: r.totalCuidadora, color: "b" }, { label: "Reducir jornada", value: r.totalReducir, color: "c" }],
    cols: ["Al mes", "Total etapa"],
    rows: [
      ["Guardería (menos ayudas)", EM.eur(r.costeMesGuarderia), EM.eur(r.totalGuarderia)],
      ["Cuidadora (con cotización)", EM.eur(r.costeMesCuidadora), EM.eur(r.totalCuidadora)],
      { label: "Reducir jornada (ingreso perdido + oportunidad)", values: [EM.eur(r.costeMesReducir), EM.eur(r.totalReducir)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
