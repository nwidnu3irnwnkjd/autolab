// Plan de pensiones o fondo indexado (IRPF 2026). Parametros (generados desde data/params.json -> irpf_2026 y pensiones_2026; fuentes y fechas alli).
// est: escala estatal general; aho: escala del ahorro (estatal + autonomica, doble de la mitad); minE: minimo del contribuyente; ccaa: escala general y minimo personal de cada comunidad.
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "aho": [[0, 19.0], [6000, 21.0], [50000, 23.0], [200000, 27.0], [300000, 30]], "minE": 5550, "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": 5790, "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": 5550, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": 6105, "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": 5550, "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": 5606, "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": 5550, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": 5550, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": 5550, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": 5550, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": 5550, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": 5789, "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": 5956.65, "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": 5550, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": 5550, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": 6105, "orient": false}}};
var LIM = 1500, LIMPCT = 0.30, ANOS_RENTA = 10;
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function tasa(base, tr) { var t = tr[0][1], i; for (i = 0; i < tr.length; i++) if (base > tr[i][0]) t = tr[i][1]; return t; }
// Cuota del IRPF sobre la base general (estatal + autonomica), con solo el minimo personal.
function cuota(b, cc) { return Math.max(0, escala(b, P.est) - escala(P.minE, P.est)) + Math.max(0, escala(b, cc.esc) - escala(cc.min, cc.esc)); }
function impAhorro(g) { return g > 0 ? escala(g, P.aho) : 0; }
// Aportaciones al inicio de cada ano (n anos) a crecimiento g: valor al final.
function valorAportado(A, g, n) { var s = 0, k; for (k = 1; k <= n; k++) s += A * Math.pow(g, k); return s; }
// Devolucion fiscal s al final de cada ano reinvertida a crecimiento g.
function valorDevolucion(s, g, n) { var t = 0, k; for (k = 0; k < n; k++) t += s * Math.pow(g, k); return t; }
function evaluar(d, n, cc, e, s, gp, gf) {
  var Pv = valorAportado(e, gp, n), F = valorAportado(e, gf, n), R = valorDevolucion(s, gf, n), b0 = d.renta * d.rescate;
  var taxL = cuota(b0 + Pv, cc) - cuota(b0, cc), tax10 = ANOS_RENTA * (cuota(b0 + Pv / ANOS_RENTA, cc) - cuota(b0, cc));
  var taxF = impAhorro(F - e * n), taxR = impAhorro(R - s * n);
  var Fn = valorAportado(Math.max(e - s, 0), gf, n), taxFn = impAhorro(Fn - Math.max(e - s, 0) * n);
  return { Pv: Pv, F: F, R: R, taxL: taxL, tax10: tax10, taxF: taxF, taxR: taxR, planL: Pv - taxL + R - taxR, plan10: Pv - tax10 + R - taxR,
    fondo: F - taxF, planNR: Pv - taxL, fondoNR: Fn - taxFn };
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], n = Math.max(Math.round(d.anos), 1);
  var limite = Math.min(LIM, LIMPCT * Math.max(d.renta, 0)), e = Math.min(d.aportacion, limite);
  var gp = 1 + (d.rentab - d.comPlan) / 100, gf = 1 + (d.rentab - d.comFondo) / 100;
  var s = cuota(d.renta, cc) - cuota(d.renta - e, cc);
  var r = evaluar(d, n, cc, e, s, gp, gf), dif = r.planL - r.fondo, dif10 = r.plan10 - r.fondo;
  var taEq = r.Pv > 0 ? 1 - (r.fondo - (r.R - r.taxR)) / r.Pv : null;
  var serie = [], k;
  for (k = 1; k <= n; k++) { var x = evaluar(d, k, cc, e, s, gp, gf); serie.push({ anio: k, plan: x.planL, fondo: x.fondo }); }
  return {
    limite: limite, aportacionEfectiva: e, excede: d.aportacion > limite + 0.005 ? 1 : 0, ahorroFiscalAnual: s, tipoMarginal: tasa(d.renta, P.est) + tasa(d.renta, cc.esc),
    valorPlanBruto: r.Pv, impuestoRescate: r.taxL, tipoMedioRescate: r.Pv > 0 ? 100 * r.taxL / r.Pv : 0, valorFondoBruto: r.F, impuestoFondo: r.taxF,
    patrimonioPlan: r.planL, patrimonioFondo: r.fondo, diferencia: dif, ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "plan" : "fondo"),
    patrimonioPlan10: r.plan10, diferencia10: dif10, ganador10: Math.abs(dif10) < 1 ? "empate" : (dif10 > 0 ? "plan" : "fondo"),
    diferenciaSinReinvertir: r.planNR - r.fondoNR, tipoEquilibrio: taEq === null ? -1 : 100 * taEq, hayEquilibrio: taEq !== null && taEq > 0 ? 1 : 0,
    orientativo: cc.orient ? 1 : 0, ccaaNombre: cc.n, serieAnual: serie
  };
}
function eur(x) { return EM.eur(x); }
function pct(x, dec) { return EM.num(x, dec === undefined ? 1 : dec) + " %"; }
var IDS = ["aportacion", "anos", "renta", "rescate", "rentab", "comPlan", "comFondo"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.aportacion <= 0 || d.anos < 1 || d.anos > 60 || d.renta <= 0 || d.rescate <= 0 || d.comPlan < 0 || d.comFondo < 0 || 1 + (d.rentab - Math.max(d.comPlan, d.comFondo)) / 100 <= 0) return;
  var r = calcular(d), abs = Math.abs(r.diferencia), plan = r.ganador === "plan", n = Math.max(Math.round(d.anos), 1);
  var verdict = r.ganador === "empate" ? "Con estos supuestos, el plan de pensiones y el fondo indexado te dejan lo mismo después de impuestos."
    : "Con estos supuestos, " + (plan ? "el plan de pensiones" : "el fondo indexado") + " te deja " + EM.eur(abs) + " más después de impuestos en " + n + " años, si rescatas el plan de una vez.";
  var note = "";
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  if (r.excede) {
    if (d.aportacion > LIM + 0.005) note += "<p><strong>Aportación por encima de 1.500 €:</strong> la ley no permite aportar más de 1.500 € al año a planes de pensiones individuales (art. 5.3 del texto refundido de la Ley de Planes y Fondos de Pensiones). El exceso debe retirarse antes del 30 de junio del año siguiente o se multa con el 50 % (art. 36.5). Solo con aportaciones de la empresa o con planes de autónomos sube ese límite, y la calculadora no lo modela: compara únicamente " + EM.eur(r.aportacionEfectiva) + " al año (tu límite deducible es de " + EM.eur(r.limite) + ").</p>";
    else note += "<p><strong>Aportación por encima del límite deducible:</strong> la ley limita la reducción a la menor de estas cantidades: el 30 % de tus rendimientos del trabajo y de actividades o 1.500 € al año (art. 52.1 de la Ley del IRPF). Tu límite es de " + EM.eur(r.limite) + " y la calculadora compara solo esa cantidad; el exceso no reduce tu base este año, pero puedes reducirlo en los 5 ejercicios siguientes (art. 52.2).</p>";
  }
  note += "<p><strong>Lectura:</strong> aportar " + EM.eur(r.aportacionEfectiva) + " al año te devuelve " + EM.eur(r.ahorroFiscalAnual) + " de IRPF (tu tipo marginal actual es de " + pct(r.tipoMarginal) + "), que aquí se reinvierten en el fondo. ";
  note += "Si rescatas de una vez, el rescate tributa como rendimiento del trabajo a un tipo medio del " + pct(r.tipoMedioRescate) + ". ";
  if (r.hayEquilibrio) note += "El plan gana si el tipo medio con que tributa tu rescate queda por debajo del <strong>" + pct(r.tipoEquilibrio) + "</strong>. ";
  else note += "Con estos supuestos el plan no gana al fondo ni aunque el rescate tributara al 0 %. ";
  note += "Repartiendo el cobro en " + ANOS_RENTA + " años el plan te deja " + (r.ganador10 === "empate" ? "lo mismo que el fondo" : EM.eur(Math.abs(r.diferencia10)) + (r.ganador10 === "plan" ? " más" : " menos") + " que el fondo") + ". ";
  note += "Si gastas la devolución en lugar de reinvertirla y comparas a igual esfuerzo neto, la diferencia a favor del plan es de " + EM.eur(r.diferenciaSinReinvertir) + ".</p>";
  note += "<p><strong>Ojo con la liquidez:</strong> el plan está bloqueado, salvo que llegue una contingencia (jubilación, incapacidad, dependencia o fallecimiento) o un supuesto excepcional de liquidez como desempleo de larga duración, enfermedad grave o, si sus especificaciones lo prevén, aportaciones con al menos diez años de antigüedad (art. 8.8 del texto refundido de la Ley de Planes y Fondos de Pensiones); el fondo se puede reembolsar cuando quieras. La rentabilidad es una hipótesis tuya, no una previsión.</p>";
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.orientativo || abs < Math.max(r.patrimonioPlan, r.patrimonioFondo, 1) * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: r.ganador === "empate" ? "de diferencia" : "más con " + (plan ? "el plan de pensiones" : "el fondo indexado"), format: EM.eur,
    line: { caption: "Patrimonio neto tras impuestos si lo cobras ese año (rescate de una vez)", xLabel: "Años", xFormat: function (a) { return "año " + a; }, yFormat: EM.eur,
      series: [{ label: "Plan de pensiones", color: "a", points: r.serieAnual.map(function (v) { return [v.anio, v.plan]; }) },
               { label: "Fondo indexado", color: "b", points: r.serieAnual.map(function (v) { return [v.anio, v.fondo]; }) }] },
    barsLabel: "Patrimonio neto después de impuestos en " + n + " años",
    bars: [{ label: "Plan de pensiones" + (plan ? " (gana)" : ""), value: Math.max(r.patrimonioPlan, 0), color: "a" }, { label: "Fondo indexado" + (r.ganador === "fondo" ? " (gana)" : ""), value: Math.max(r.patrimonioFondo, 0), color: "b" }],
    cols: ["Plan", "Fondo"],
    rows: [
      ["Valor antes de impuestos", EM.eur(r.valorPlanBruto), EM.eur(r.valorFondoBruto)],
      ["Impuesto al rescatar o reembolsar", EM.eur(r.impuestoRescate), EM.eur(r.impuestoFondo)],
      { label: "Patrimonio neto (plan incluye la devolución reinvertida)", values: [EM.eur(r.patrimonioPlan), EM.eur(r.patrimonioFondo)], strong: true },
      ["Patrimonio neto si cobras el plan en " + ANOS_RENTA + " años", EM.eur(r.patrimonioPlan10), EM.eur(r.patrimonioFondo)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
