// Finiquito de baja voluntaria: salario, pagas, vacaciones, preaviso, cotizacion e IRPF. Parametros generados desde data/params.json -> finiquito_baja_voluntaria_2026 (fuentes y fechas alli).
var P = {"dm": [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], "anio": 365, "semV": 181, "semN": 184, "vacMin": 30, "vacMax": 90, "preMax": 90, "cotPct": 6.5, "tope": 5101.2, "tipoMax": 47, "diasMesCot": 30, "umbral": 0.5, "defMes": 10};
function calcular(d) {
  var bruto = +d.bruto || 0, pagas = Math.floor(+d.pagas || 0), mes = Math.floor(+d.mes || 0), dia = Math.floor(+d.dia || 0), va = +d.vacAnual || 0, vd = +d.vacDisf || 0, inc = +d.incumple || 0, tipo = +d.tipo || 0;
  var z = { bloqueado: 1, escenario: 0, salMes: 0, pagasPend: 0, vacDev: 0, vacPend: 0, vacImporte: 0, brutoDev: 0, descuento: 0, descAplicado: 0, cot: 0, irpf: 0, neto: 0, exceso: 0, salDia: 0, doy: 0, netoSinDesc: 0, resto: 0, valorDiaNeto: 0, motivo: "" };
  if (bruto <= 0 || (pagas !== 12 && pagas !== 14) || mes < 1 || mes > 12) { z.motivo = "datos"; return z; }
  if (dia < 1 || dia > P.dm[mes - 1]) { z.motivo = "dia"; return z; }
  if (va < P.vacMin || va > P.vacMax || vd < 0 || vd > va) { z.motivo = "vac"; return z; }
  if (inc < 0 || inc > P.preMax || tipo < 0 || tipo > P.tipoMax) { z.motivo = "datos"; return z; }
  var m = bruto / pagas, salDia = bruto / P.anio, doy = dia, i;
  for (i = 0; i < mes - 1; i++) doy += P.dm[i];
  var salMes = m * dia / P.dm[mes - 1], pp = 0;
  if (pagas === 14) pp = doy <= P.semV ? m * doy / P.semV : m * (doy - P.semV) / P.semN;
  var dev = va * doy / P.anio, pend = Math.max(0, dev - vd), exceso = Math.max(0, vd - dev), imp = pend * salDia;
  var brutoDev = salMes + pp + imp, desc = inc * salDia, descAp = Math.min(desc, brutoDev), mesesVac = pend > 0 ? Math.ceil(pend / P.diasMesCot) : 0;
  var prorr = pagas === 14 ? (2 * m / 12) * dia / P.dm[mes - 1] : 0, base = Math.min(salMes + prorr, P.tope) + Math.min(imp, P.tope * mesesVac), cot = base * P.cotPct / 100, irpf = brutoDev * tipo / 100;
  var neto = Math.max(0, brutoDev - descAp - cot - irpf), netoSin = Math.max(0, brutoDev - cot - irpf);
  var esc = inc > 0 ? 3 : exceso > P.umbral ? 4 : pend > P.umbral ? 2 : 1;
  return { bloqueado: 0, escenario: esc, salMes: salMes, pagasPend: pp, vacDev: dev, vacPend: pend, vacImporte: imp, brutoDev: brutoDev, descuento: desc, descAplicado: descAp, cot: cot, irpf: irpf, neto: neto, exceso: exceso, salDia: salDia, doy: doy,
    netoSinDesc: netoSin, resto: desc - descAp, valorDiaNeto: salDia * (1 - P.cotPct / 100 - tipo / 100), motivo: "" };
}
function eur(x) { return EM.eur(x); }
var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
function dias(x) { return EM.num(x, 1) + " días"; }
function leer() {
  var d = {}; ["bruto", "dia", "vacAnual", "vacDisf", "incumple", "tipo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.pagas = document.getElementById("pagas").value; d.mes = document.getElementById("mes").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.bruto <= 0) return;
  var r = calcular(d);
  if (r.bloqueado) {
    var msg = r.motivo === "dia" ? "Ese día no existe en el mes elegido: revisa el día de salida." : r.motivo === "vac" ? "Revisa las vacaciones: el Estatuto fija al menos " + P.vacMin + " días naturales al año (máximo " + P.vacMax + " aquí) y no puedes haber disfrutado más días de los que tiene el año." : "Revisa los datos: hace falta un salario positivo, preaviso incumplido entre 0 y " + P.preMax + " días y un tipo de IRPF entre 0 y " + P.tipoMax + " %.";
    EM.renderResult({ winner: "bloqueado", verdict: msg, tone: "warn", note: "<p>La calculadora no puede dar una cifra con estos datos.</p>" });
    return;
  }
  var fecha = Math.floor(d.dia) + " de " + MESES[Math.floor(d.mes) - 1], pg = Math.floor(d.pagas), ver, tone, extra = "";
  ver = "Con tus datos (" + eur(d.bruto) + " brutos al año en " + pg + " pagas, salida el " + fecha + "), el finiquito bruto es de " + eur(r.brutoDev) + " (salario del mes " + eur(r.salMes) + (pg === 14 ? ", pagas extra " + eur(r.pagasPend) : "") + ", vacaciones " + eur(r.vacImporte) + ") y te quedarían unos " + eur(r.neto) + " netos tras " + eur(r.cot) + " de cotización y " + eur(r.irpf) + " de IRPF estimado.";
  tone = "ok";
  if (r.escenario === 3) {
    ver += " Si tu convenio o contrato prevé descontar el preaviso, " + dias(d.incumple) + " incumplidos son " + eur(r.descuento) + " menos (" + eur(r.netoSinDesc) + " netos si no lo aplican).";
    if (r.resto > 0.005) ver += " Ese descuento supera el finiquito en " + eur(r.resto) + ", que la empresa tendría que reclamar aparte.";
    tone = "warn";
  }
  if (r.vacPend > P.umbral) ver += " Te pagan " + dias(r.vacPend) + " de vacaciones sin disfrutar (unos " + eur(r.valorDiaNeto) + " netos por día); si la empresa te deja disfrutarlas antes de irte, cobras tu salario de esos días en nómina y descansas.";
  if (r.escenario === 4 || r.exceso > P.umbral) { ver += " Has disfrutado " + dias(r.exceso) + " más de los devengados hasta tu salida: según tu convenio la empresa podría reclamarlos o descontarlos, y aquí no se descuentan."; if (r.escenario === 4) tone = "warn"; }
  if (r.escenario === 1) ver += " No hay vacaciones pendientes ni descuento por preaviso.";
  extra += "<p><strong>Qué mirar en tu finiquito:</strong> (1) que los días de salario del mes sean los trabajados; (2) las pagas extra proporcionales, si las cobras aparte; (3) los días de vacaciones pendientes y el valor de cada día (aquí " + eur(r.salDia) + " brutos por día natural); (4) los descuentos que aparezcan (preaviso u otro) con su base en el convenio o el contrato; (5) el tipo de retención de IRPF (al extinguirse el contrato suele regularizarse con las retribuciones reales del año, por lo que puede diferir del de tu última nómina) y la cotización. Puedes pedir la presencia de un representante legal de los trabajadores al firmar (art. 49.2 del Estatuto de los Trabajadores) y reclamar diferencias durante un año desde la terminación del contrato (art. 59.1).</p>";
  extra += "<p><strong>Vacaciones: ¿disfrutarlas o cobrarlas?</strong> Las vacaciones devengadas y no disfrutadas se liquidan al irte (cotizan aparte, art. 147.1 de la Ley General de la Seguridad Social, y tributan como salario). " + (r.vacPend > P.umbral ? "Cobradas, los " + dias(r.vacPend) + " pendientes suponen " + eur(r.vacImporte) + " brutos; disfrutadas antes de irte, cobras tu salario de esos días y descansas, pero tu fecha de salida se retrasa si las usas al final. " : "No tienes días pendientes con estos datos. ") + "Elegir una u otra suele ser un acuerdo con la empresa y depende del convenio; lo que cambia es cuándo empiezas en el nuevo empleo y cuánto descansas.</p>";
  extra += "<p><strong>Si fuera un despido:</strong> el finiquito sería el mismo, pero en un despido objetivo (20 días por año) o improcedente (33) se añade la indemnización (<a href=\"/decidir/indemnizacion-despido-objetivo-o-improcedente-neto/\">calcúlala aquí</a>; el disciplinario procedente no la tiene) y tendrías situación legal de desempleo (art. 267.1.a de la Ley General de la Seguridad Social: <a href=\"/decidir/cuanto-cobro-de-paro-prestacion-desempleo/\">cuánto cobrarías de paro</a>). En una baja voluntaria no hay indemnización y, en general, tampoco paro; la excepción son los supuestos de los arts. 40, 41.3, 49.1.m y 50 del Estatuto (traslado, modificación sustancial, víctimas de violencia de género o extinción pedida al juez por incumplimientos graves como impagos continuados), que dan paro y, en 40, 41.3 y 50, indemnización.</p>";
  extra += "<p><strong>Qué no se modela:</strong> el convenio (días de vacaciones, plazo y consecuencia del preaviso, si cobras vacaciones con pluses o la media de variables), bonus o comisiones pendientes, pluses, horas extra, stock options, regímenes forales, despido o ERE, contratos temporales con indemnización, paro y su compatibilidad con otros ingresos. Se supone que trabajaste todo el año desde el 1 de enero, pagas extra en junio y diciembre con devengo por semestre (si tu convenio devenga la de verano de julio a junio y la de Navidad por año natural, las pagas pendientes del ejemplo serían unos 1.855 € en vez de 997 €), cotización de contrato indefinido y un tipo de retención que escribes tú.</p>";
  EM.renderResult({
    winner: "e" + r.escenario, verdict: ver, tone: tone, bigNumber: r.neto, bigLabel: "netos de tu finiquito (estimado)", format: EM.eur,
    barsLabel: "Finiquito bruto",
    bars: [{ label: "Salario del mes", value: r.salMes, color: "a" }].concat(pg === 14 ? [{ label: "Pagas extra", value: r.pagasPend, color: "b" }] : []).concat([{ label: "Vacaciones", value: r.vacImporte, color: "a" }]),
    cols: ["Importe"],
    rows: [
      ["Salario diario de referencia", eur(r.salDia)],
      ["Salario del mes (" + Math.floor(d.dia) + " días de " + MESES[Math.floor(d.mes) - 1] + ")", eur(r.salMes)],
      ["Pagas extra proporcionales", eur(r.pagasPend)],
      ["Vacaciones devengadas hasta tu salida", dias(r.vacDev)],
      ["Vacaciones pendientes de disfrutar", dias(r.vacPend)],
      ["Vacaciones no disfrutadas (importe)", eur(r.vacImporte)],
      { label: "Finiquito bruto", values: [eur(r.brutoDev)], strong: true },
      ["Descuento por preaviso incumplido", eur(r.descAplicado)],
      ["Cotización del trabajador (" + EM.num(P.cotPct, 1) + " %)", eur(r.cot)],
      ["IRPF estimado (" + EM.num(d.tipo, 1) + " %)", eur(r.irpf)],
      { label: "Neto estimado", values: [eur(r.neto)], strong: true }
    ],
    note: extra
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
document.getElementById("mes").value = String(P.defMes);
EM.live(document.getElementById("f"), pintar);
