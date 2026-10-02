// Baja médica (incapacidad temporal) 2026: cuánto cobro cada día. Parámetros: data/params.json -> baja_medica_2026 (fuentes y fechas allí).
// Enfermedad común: días 1-3 sin subsidio, 60 % de la base reguladora del día 4 al 20, 75 % desde el 21 (días 4-15 los paga la empresa). Accidente de trabajo o enfermedad profesional: salario íntegro el día de la baja y 75 % desde el día siguiente.
var P = {"pct60": 60, "pct75": 75, "dSin": 3, "dEmp": 15, "dTramo": 20, "dMes": 30, "dMax": 545, "dOrd": 365, "dProrroga": 180, "baseMax": 5101.2, "pagas": 14};
function calcular(d) {
  var dias = Math.round(d.dias), r = { bloqueo: 0, esc: 0 };
  if (!(d.sueldo > 0)) { r.bloqueo = 3; return r; }
  if (dias < 1) { r.bloqueo = 2; return r; }
  if (dias > P.dMax) { r.bloqueo = 1; return r; }
  var prof = d.cont === "prof";
  var mensual = d.pagas === "14" ? d.sueldo * P.pagas / 12 : d.sueldo;
  var br = Math.min(mensual, P.baseMax) / P.dMes, sal = mensual / P.dMes;
  var m = Math.min(Math.max(d.mejora, 0), 100) / 100, t = Math.min(Math.max(d.tipo, 0), 100) / 100;
  var s60 = br * P.pct60 / 100, s75 = br * P.pct75 / 100, ms = m * sal;
  function perdidaDia(sub) { return sal - Math.max(sub, ms); }
  var n0 = 0, n60 = 0, n75 = 0, nFull = 0;
  if (prof) { nFull = 1; n75 = dias - 1; }
  else { n0 = Math.min(dias, P.dSin); n60 = Math.max(0, Math.min(dias, P.dTramo) - P.dSin); n75 = Math.max(0, dias - P.dTramo); }
  var emp = Math.max(0, Math.min(dias, P.dEmp) - P.dSin);
  r.brDia = br; r.salDia = sal; r.s60 = s60; r.s75 = s75;
  r.n0 = n0; r.n60 = n60; r.n75 = n75; r.nFull = nFull;
  r.prest60 = n60 * s60; r.prest75 = n75 * s75; r.prest = r.prest60 + r.prest75;
  r.compl0 = n0 * ms; r.compl60 = n60 * Math.max(0, ms - s60); r.compl75 = n75 * Math.max(0, ms - s75);
  r.compl = r.compl0 + r.compl60 + r.compl75;
  r.salFull = nFull * sal;
  r.ingreso = r.prest + r.compl + r.salFull;
  r.habitual = dias * sal;
  r.perdida = r.habitual - r.ingreso;
  r.perdidaNeta = r.perdida * (1 - t);
  r.perdida3 = prof ? Math.max(0, Math.min(dias, P.dSin) - 1) * perdidaDia(s75) : Math.min(dias, P.dSin) * perdidaDia(0);
  r.perdida75 = perdidaDia(s75); r.perdida60 = perdidaDia(s60); r.perdida0 = perdidaDia(0);
  r.perdidaMes = r.perdida75 * P.dMes;
  var empSub = prof ? 0 : emp * s60;
  r.empSub = empSub; r.empresa = empSub + r.compl + r.salFull; r.entidad = r.prest - empSub;
  r.tope = mensual > P.baseMax ? 1 : 0;
  r.esc = r.perdida < 0.5 ? 1 : (r.prest === 0 ? 2 : (m === 0 ? 3 : 4));
  return r;
}
function eur(x) { return EM.eur(x); }
var IDS = ["sueldo", "dias", "mejora", "tipo"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.pagas = document.getElementById("pagas").value; d.cont = document.getElementById("cont").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
var NO_MODELA = "<p><strong>No incluye:</strong> los autónomos (su base y su cese tienen reglas propias), los desempleados con prestación, los contratos a tiempo parcial y los fijos discontinuos (la base reguladora se calcula con las bases de los últimos meses), los funcionarios con MUFACE y otros regímenes especiales, la cotización y el IRPF de la prestación (la prestación tributa como rendimiento del trabajo; el tipo marginal opcional solo da una cifra aproximada), los regímenes forales de País Vasco y Navarra, las situaciones especiales de la Ley 6/2024 (menstruación incapacitante secundaria, interrupción del embarazo, semana 39 de gestación y donación de órganos, con reglas propias desde el día 1 o el 2), las horas extraordinarias en accidente de trabajo (su media sube la base reguladora, así que la prestación real puede ser mayor), la carencia de 180 días cotizados en enfermedad común, las recaídas, la huelga y el cierre patronal, y el abono por pago delegado o directo.</p>";
function pintar() {
  var d = leer();
  if (d.dias < 0 || d.mejora < 0 || d.tipo < 0) { aviso("Revisa los datos: los días, la mejora del convenio y el tipo marginal no pueden ser negativos."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("La herramienta calcula hasta " + EM.num(P.dMax, 0) + " días naturales (" + EM.num(P.dOrd, 0) + " días más una prórroga de " + EM.num(P.dProrroga, 0) + "). A los " + EM.num(P.dMax, 0) + " días se extingue la incapacidad temporal, pero sigues cobrando la misma prestación (prolongación de efectos económicos, art. 174.5 de la LGSS) hasta que se resuelva la incapacidad permanente, y eso no lo calculamos."); return; }
  if (r.bloqueo === 2) { aviso("Indica al menos 1 día de baja."); return; }
  if (r.bloqueo === 3) { aviso("Indica tu sueldo bruto mensual (mayor que 0): sin él no se puede calcular la base reguladora."); return; }
  var dias = Math.round(d.dias), prof = d.cont === "prof", verdict;
  var ref = "Con tus datos (" + EM.num(dias, 0) + " días de baja por " + (prof ? "accidente de trabajo o enfermedad profesional" : "enfermedad común o accidente no laboral") + "), ";
  if (r.esc === 1) verdict = ref + "cobras " + eur(r.ingreso) + " brutos y no pierdes dinero frente a tu sueldo habitual de esos días (" + eur(r.habitual) + "), porque " + (r.compl > 0 ? "la mejora de tu convenio completa lo que no paga la Seguridad Social" : "el único día que cuenta lo paga la empresa íntegro") + ".";
  else if (r.esc === 2) verdict = ref + "no hay subsidio de la Seguridad Social, porque en enfermedad común solo se cobra desde el cuarto día: pierdes " + eur(r.perdida) + " brutos frente a tu sueldo (" + eur(r.habitual) + ")" + (r.compl > 0 ? ", después de la mejora de tu convenio" : ", salvo que tu convenio o tu empresa mejoren esos días") + ".";
  else if (r.esc === 3) verdict = ref + "cobras " + eur(r.ingreso) + " brutos de " + eur(r.habitual) + " y pierdes " + eur(r.perdida) + " frente a tu sueldo" + (r.perdida3 > 0.5 ? ", de los que " + eur(r.perdida3) + " son de los 3 primeros días" : "") + ". Si tu convenio mejora la prestación, esa pérdida baja; sin mejora, cada día del tramo del " + EM.num(P.pct75, 0) + " % te cuesta " + eur(r.perdida75) + ".";
  else verdict = ref + "cobras " + eur(r.ingreso) + " brutos, incluida una mejora de " + eur(r.compl) + ", y aun así pierdes " + eur(r.perdida) + " frente a tu sueldo habitual (" + eur(r.habitual) + "): la mejora que has indicado (" + EM.num(Math.min(Math.max(d.mejora, 0), 100), 0) + " % del sueldo) no cubre toda la diferencia" + (r.tope ? " o tu sueldo supera la base máxima de cotización" : "") + ".";
  var tn = Math.min(Math.max(d.tipo, 0), 100);
  var note = "<p><strong>Cómo sale:</strong> la base reguladora es tu base de cotización del mes anterior dividida entre " + EM.num(P.dMes, 0) + " días" + (r.tope ? ", limitada a la base máxima de " + eur(P.baseMax) + " al mes (tu sueldo con pagas prorrateadas la supera)" : "") + ": " + eur(r.brDia) + " al día. " + (prof ? "En accidente de trabajo o enfermedad profesional la empresa paga el salario íntegro del día de la baja y la Seguridad Social el " + EM.num(P.pct75, 0) + " % desde el día siguiente, sin días de espera." : "En enfermedad común no se cobra nada los 3 primeros días, el " + EM.num(P.pct60, 0) + " % del día 4 al " + EM.num(P.dTramo, 0) + " y el " + EM.num(P.pct75, 0) + " % desde el día " + EM.num(P.dTramo + 1, 0) + "; del día 4 al " + EM.num(P.dEmp, 0) + " lo paga la empresa y desde el " + EM.num(P.dEmp + 1, 0) + " está a cargo de la Seguridad Social o la mutua (con pago delegado, normalmente te lo sigue abonando la empresa en la nómina).") + "</p>";
  note += "<p><strong>Cuánto te falta por día:</strong> " + (prof ? "" : eur(r.perdida0) + " en los 3 primeros días, " + eur(r.perdida60) + " del día 4 al " + P.dTramo + ", y ") + eur(r.perdida75) + " en el tramo del " + EM.num(P.pct75, 0) + " %, es decir, " + eur(r.perdidaMes) + " brutos por cada " + EM.num(P.dMes, 0) + " días en ese tramo.</p>";
  if (tn > 0) note += "<p><strong>Tras impuestos (aproximado):</strong> con un tipo marginal del " + EM.num(tn, 0) + " %, la pérdida sería de unos " + eur(r.perdidaNeta) + ". La prestación y la mejora tributan como el sueldo; no calculamos tu retención ni tus cotizaciones.</p>";
  if (dias > P.dOrd) note += "<p>Pasados los " + EM.num(P.dOrd, 0) + " días, solo el INSS puede dar el alta o reconocer la prórroga de " + EM.num(P.dProrroga, 0) + " días.</p>";
  if (!prof) note += "<p><strong>Requisito:</strong> en enfermedad común necesitas 180 días cotizados en los 5 años anteriores a la baja (art. 172.a de la LGSS); si no los tienes, no cobras subsidio y estas cifras no te valen.</p>";
  note += "<p>La mejora del convenio no es de ley: se aplica como el porcentaje de tu sueldo hasta el que la empresa completa cada día de baja, incluidos los 3 primeros de enfermedad común. Comprueba en tu convenio desde qué día y hasta cuándo se paga.</p>";
  note += NO_MODELA;
  var rows = [];
  if (!prof) rows.push(["Días 1 a 3 (sin subsidio)", EM.num(r.n0, 0), "0 %", eur(0), "Nadie (salvo mejora)"]);
  if (prof) rows.push(["Día de la baja (salario íntegro)", EM.num(r.nFull, 0), "100 %", eur(r.salFull), "Empresa"]);
  if (!prof) rows.push(["Días 4 a " + P.dTramo + " (" + P.pct60 + " %)", EM.num(r.n60, 0), P.pct60 + " %", eur(r.prest60), r.n60 > 0 ? (Math.min(dias, P.dEmp) > P.dSin ? "Empresa hasta el día " + P.dEmp + (dias > P.dEmp ? ", después Seguridad Social" : "") : "") : ""]);
  rows.push([prof ? "Desde el día 2 (" + P.pct75 + " %)" : "Desde el día " + (P.dTramo + 1) + " (" + P.pct75 + " %)", EM.num(r.n75, 0), P.pct75 + " %", eur(r.prest75), "A cargo de la Seguridad Social o la mutua"]);
  rows.push(["Mejora del convenio", EM.num(dias, 0), EM.num(Math.min(Math.max(d.mejora, 0), 100), 0) + " % del sueldo", eur(r.compl), "Empresa"]);
  rows.push(["Total que cobras", EM.num(dias, 0), "", eur(r.ingreso), "Empresa " + eur(r.empresa) + " · Seg. Social " + eur(r.entidad)]);
  rows.push(["Sueldo habitual de esos días", EM.num(dias, 0), "100 %", eur(r.habitual), ""]);
  rows.push(["Pérdida frente al sueldo", "", "", eur(r.perdida), "3 primeros días: " + eur(r.perdida3)]);
  EM.renderResult({
    winner: "esc" + r.esc, verdict: verdict, tone: r.esc === 1 ? "ok" : "info",
    bigNumber: r.ingreso, bigLabel: "que cobras en " + EM.num(dias, 0) + " días de baja (bruto)", format: eur,
    barsLabel: "Quién te paga",
    bars: [{ label: "Empresa", value: r.empresa, color: "a" }, { label: "A cargo de la Seguridad Social o la mutua", value: r.entidad, color: "b" }],
    cols: ["Tramo", "Días", "Porcentaje", "Importe", "Quién paga"],
    rows: rows,
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
