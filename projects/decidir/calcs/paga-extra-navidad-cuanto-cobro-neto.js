// Paga extra de Navidad: cuánto toca (proporcional por días) y neto. Parámetros: data/params.json -> paga_extra_navidad_2026 (fuentes y fechas allí) y retencion_irpf_nomina_2026 (cotización del trabajador 6,5 %).
// ET 31 (cuantía y prorrateo por convenio), LGSS 147.1 (cotización ya prorrateada en 12 meses), RIRPF 80.1 y 86.1 (retención = tipo de la nómina sobre la paga).
var P = {"cot": 6.5, "dias": [365, 184], "iniSem": 182, "acum": [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], "md": [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]};
function r2(x) { return Math.round(x * 100 + 1e-7) / 100; }
// d: importe (paga completa), devengo anual|semestral, situacion todo|alta|baja, mes y dia (fecha de alta o último día trabajado), diassin, ret (%), forma 14|prorr
function calcular(d) {
  var imp = +d.importe || 0, ret = +d.ret || 0, mes = Math.floor(+d.mes || 0), dia = Math.floor(+d.dia || 0), sin = Math.max(0, Math.floor(+d.diassin || 0));
  var n = d.devengo === "semestral" ? P.dias[1] : P.dias[0], ini = d.devengo === "semestral" ? P.iniSem : 1, fin = P.dias[0];
  var fechaOk = mes >= 1 && mes <= 12 && dia >= 1 && dia <= P.md[mes - 1];
  if (!(imp > 0) || (d.forma !== "prorr" && d.situacion !== "todo" && !fechaOk)) return { bloqueado: 1, escenario: 0 };
  if (d.forma === "prorr") {
    var m = r2(imp / 12), rm = r2(m * ret / 100);
    return { bloqueado: 0, escenario: 3, dias: n, diasPeriodo: n, bruta: 0, mensual: m, retMensual: rm, netoMensual: r2(m - rm) };
  }
  var f = fechaOk ? P.acum[mes - 1] + dia : 0, dev;
  if (d.situacion === "todo") dev = n;
  else if (d.situacion === "alta") dev = fin - Math.max(f, ini) + 1;
  else dev = f >= ini ? Math.min(f, fin) - ini + 1 : 0;
  dev = Math.max(0, dev);
  var dias = Math.max(0, dev - Math.min(sin, dev));
  var bruta = r2(imp * dias / n), rt = r2(bruta * ret / 100), cz = r2(bruta * P.cot / 100);
  var esc = dias === 0 ? 4 : dias === n ? 1 : d.situacion === "baja" ? 5 : 2;
  return { bloqueado: 0, escenario: esc, dias: dias, diasPeriodo: n, pct: dias / n * 100, bruta: bruta, retencion: rt, neto: r2(bruta - rt), cotizada: cz, netoReal: r2(bruta - rt - cz) };
}
function eur(x) { return EM.eur(x); }
function pct(x) { return EM.num(x, 2) + " %"; }
function leer() {
  var d = {}; ["importe", "mes", "dia", "diassin", "ret"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["devengo", "situacion", "forma"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.ret < 0 || d.ret > 100 || d.diassin < 0) return;
  var r = calcular(d);
  if (r.bloqueado) {
    EM.renderResult({ winner: "bloqueado", tone: "warn", verdict: d.importe > 0 ? "Esa fecha no existe en 2026: revisa el día y el mes." : "Escribe el importe de la paga completa que fija tu convenio.", note: "<p>La calculadora usa el calendario de 2026.</p>" });
    return;
  }
  var per = d.devengo === "semestral" ? "del 1 de julio al 31 de diciembre" : "del 1 de enero al 31 de diciembre";
  var v, tone = "ok", big, bigL, rows = [], note = "";
  if (r.escenario === 3) {
    v = "Con las pagas prorrateadas en las doce mensualidades no hay paga en diciembre: tu nómina de cada mes ya incluye " + eur(r.mensual) + " brutos de esta paga (" + eur(r.netoMensual) + " netos con una retención del " + pct(d.ret) + "), y no queda parte proporcional pendiente.";
    big = r.netoMensual; bigL = "neto al mes por esta paga prorrateada";
    rows = [["Paga completa (bruta)", eur(d.importe)], ["Parte que entra en cada nómina mensual (bruta)", eur(r.mensual)], ["Retención de cada mes", eur(r.retMensual)], { label: "Neto de cada mes por esta paga", values: [eur(r.netoMensual)], strong: true }];
  } else if (r.escenario === 4) {
    v = "Con estas fechas no devengas nada de esta paga: tendrías 0 días sobre un periodo de " + r.diasPeriodo + " (" + per + "), así que no hay paga que cobrar según este cálculo.";
    tone = "warn"; big = 0; bigL = "de paga por devengar";
    rows = [["Días devengados", r.dias + " de " + r.diasPeriodo]];
  } else {
    var ent = r.escenario === 1;
    v = ent ? "Con estos datos cobras la paga entera: " + eur(r.bruta) + " brutos, " + eur(r.neto) + " netos con una retención del " + pct(d.ret) + ". En diciembre no se descuenta cotización aparte, porque ya se cotizó repartida en tus nóminas mensuales."
      : "Con estos datos te corresponde la parte proporcional: " + r.dias + " de " + r.diasPeriodo + " días del periodo, es decir " + pct(r.pct) + " de la paga, " + eur(r.bruta) + " brutos y " + eur(r.neto) + " netos con una retención del " + pct(d.ret) + ".";
    if (r.escenario === 1 && d.situacion === "baja") v += " Como te vas, esa paga se liquida en el finiquito, no en la nómina de diciembre.";
    if (r.escenario === 5) v += " Como te vas, esa parte proporcional se paga en el finiquito, no en diciembre.";
    big = r.neto; bigL = "neto que te ingresan por la paga";
    rows = [["Paga completa (bruta)", eur(d.importe)], ["Días devengados", r.dias + " de " + r.diasPeriodo + " (" + pct(r.pct) + ")"], ["Paga que te toca (bruta)", eur(r.bruta)], ["Retención de IRPF (" + pct(d.ret) + ")", "−" + eur(r.retencion)], { label: "Neto que te ingresan", values: [eur(r.neto)], strong: true }, ["Cotización ya descontada en tus nóminas mensuales (" + pct(P.cot) + ")", "−" + eur(r.cotizada)], ["Neto contando esa cotización", eur(r.netoReal)]];
    note = "<p><strong>Neto que ves y neto real:</strong> la cifra que te ingresan es la bruta menos la retención. La cotización por esta paga ya salió, repartida, de tus nóminas mensuales; si la sumas, la paga te cuesta " + eur(r.cotizada) + " más y su neto real es " + eur(r.netoReal) + " (aproximación al " + pct(P.cot) + " de contrato indefinido, sin tope de base máxima).</p>";
  }
  note += "<p><strong>Qué fija el convenio y no esta calculadora:</strong> la cuantía de la paga, si se devenga en el año o de julio a diciembre, si cuenta días naturales o meses, y si las bajas o excedencias descuentan días. Comprueba tu convenio y edita los datos.</p>";
  EM.renderResult({ winner: "e" + r.escenario, verdict: v, tone: tone, bigNumber: big, bigLabel: bigL, format: EM.eur, cols: ["Importe"], rows: rows, note: note });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
