// Actualizacion de la renta del alquiler de vivienda (LAU art. 18 + DA 11.a). Parametros y fuentes: data/params.json -> renta_alquiler_2026 (IRAV, IPC, fechas).
var P = {};
var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
// Regla que rige. firma: post (desde 26-5-2023), pre (6-3-2019 a 25-5-2023), ant (antes: no se modela). indice: none | ipc | igc | otro.
// pct = subida maxima en % (tope IPC; desde 26-5-2023 ademas tope IRAV); exacto=0 si el indice pactado (IGC, otro) puede dar menos que el tope.
function calcular(d) {
  var r = d.renta, o = { noModelado: 0, exacto: 1, pct: 0, escenario: 0 };
  if (d.firma === "ant") { o.noModelado = 1; o.exacto = 0; return o; }
  var pct = 0;
  if (d.indice !== "none") {
    pct = d.firma === "pre" ? d.ipc : Math.min(d.ipc, d.irav);
    pct = Math.max(pct, 0);
    if (d.indice === "igc" || d.indice === "otro") o.exacto = 0;
  }
  var nueva = Math.round(r * (1 + pct / 100) * 100) / 100;
  var sm = Math.round((nueva - r) * 100) / 100;
  var ex = d.pide > 0 ? Math.max(0, d.pide - nueva) : 0;
  o.pct = pct; o.nueva = nueva; o.subidaMes = sm; o.subidaAnio = Math.round(sm * 12 * 100) / 100;
  o.mesCobro = d.mes % 12 + 1;
  o.excesoMes = Math.round(ex * 100) / 100; o.excesoAnio = Math.round(ex * 12 * 100) / 100;
  if (d.indice === "none") o.escenario = 1;
  else if (pct <= 0) o.escenario = 5;
  else if (!(d.pide > 0)) o.escenario = 4;
  else if (d.pide <= nueva + 0.005) o.escenario = 2;
  else o.escenario = 3;
  return o;
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["renta", "mes", "irav", "ipc", "pide"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["firma", "indice", "zona"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.renta <= 0 || d.mes < 1 || d.mes > 12) return;
  var r = calcular(d), v, tone = "ok", rows = [], note = "", big, bigLbl;
  var cobro = MESES[r.mesCobro - 1];
  if (r.noModelado) {
    EM.renderResult({ winner: "ant", tone: "warn", verdict: "Con un contrato firmado antes del 6 de marzo de 2019 la actualización depende de tu cláusula y de la ley vigente cuando lo firmaste: esta calculadora no lo calcula. Revisa la cláusula de actualización o consulta a un profesional.", note: "<p>Para contratos posteriores calculamos la subida máxima con la regla que rige. No es asesoramiento.</p>" });
    return;
  }
  var tope = d.firma === "pre" ? "el IPC" : "el menor entre el IPC y el IRAV";
  if (r.escenario === 1) {
    v = "Con tus datos, tu casero no puede subirte la renta: sin cláusula de actualización en el contrato no hay actualización (art. 18.1 LAU), y seguirías pagando " + EM.eur(d.renta) + " al mes.";
    if (d.pide > d.renta) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera tu renta actual en " + EM.eur(r.excesoMes) + " al mes; solo podría subir si lo acordáis por escrito.";
  } else if (r.escenario === 5) {
    v = "Con tus datos, la variación del índice que limita la subida no es positiva (" + EM.num(Math.min(d.ipc, d.firma === "pre" ? d.ipc : d.irav), 2) + " %), así que el casero no puede exigirte una subida: la renta máxima sigue siendo " + EM.eur(d.renta) + " al mes (si tu cláusula es el IPC, el inquilino puede pedir que se aplique la variación negativa; esta calculadora no la calcula).";
    if (d.pide > d.renta) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera tu renta actual: solo sería válido si lo acordáis por escrito.";
  } else {
    var exacta = r.exacto ? "puede exigirte como máximo" : "puede exigirte, como máximo y según lo que diga tu cláusula,";
    v = "Con tus datos, tu casero " + exacta + " una subida del " + EM.num(r.pct, 2) + " %: de " + EM.eur(d.renta) + " a " + EM.eur(r.nueva) + " al mes (" + EM.eur(r.subidaMes) + " más al mes, " + EM.eur(r.subidaAnio) + " al año), desde el recibo de " + cobro + " si te lo notifica por escrito en " + MESES[d.mes - 1] + ".";
    if (r.escenario === 3) { v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera ese máximo en " + EM.eur(r.excesoMes) + " al mes (" + EM.eur(r.excesoAnio) + " al año): esa parte no puedes tener que pagarla por la actualización."; tone = "warn"; }
    else if (r.escenario === 2) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) está dentro de ese máximo.";
    else v += " Si te piden más que " + EM.eur(r.nueva) + " al mes, el exceso no es una actualización válida.";
  }
  big = r.nueva; bigLbl = "renta mensual máxima tras la actualización";
  rows.push(["Renta actual", EM.eur(d.renta), EM.eur(d.renta * 12)]);
  rows.push({ label: "Renta máxima actualizada", values: [EM.eur(r.nueva), EM.eur(r.nueva * 12)], strong: true });
  rows.push(["Subida máxima", EM.eur(r.subidaMes), EM.eur(r.subidaAnio)]);
  if (d.pide > 0) {
    rows.push(["Lo que te piden", EM.eur(d.pide), EM.eur(d.pide * 12)]);
    rows.push(["Exceso sobre el máximo", EM.eur(r.excesoMes), EM.eur(r.excesoAnio)]);
  }
  note += "<p><strong>Qué regla rige:</strong> ";
  if (d.indice === "none") note += "sin cláusula de actualización, la renta no se actualiza (art. 18.1 LAU).</p>";
  else note += "la actualización solo puede hacerse en cada aniversario del contrato y con tope en " + tope + (d.firma === "pre" ? " (contrato firmado antes del 26/5/2023: rige el art. 18 vigente al firmarlo)" : " (contrato firmado desde el 26/5/2023: el IRAV es el límite de referencia según la DA 11.ª; confianza media, el art. 18 todavía menciona el IPC)") + ". Con IRAV " + EM.num(d.irav, 2) + " % e IPC " + EM.num(d.ipc, 2) + " %, el tope es " + EM.num(r.pct, 2) + " %." + (r.exacto ? "" : " Si tu cláusula no dice índice se aplica el IGC (art. 18.1) y, si es otro índice, el que pactasteis: la subida real puede ser menor que este máximo.") + "</p>";
  note += "<p><strong>Cuándo se cobra:</strong> desde el mes siguiente a la notificación escrita del porcentaje aplicado; vale una nota en el recibo anterior (art. 18.2). No hay un preaviso legal de un mes.</p>";
  if (r.escenario === 5 && d.indice === "ipc") note += "<p><strong>Índice negativo:</strong> la subida máxima es cero, pero con el IPC pactado y negativo la actualización puede bajar la renta y también puedes pedirla tú como inquilino (art. 18.1). No se calcula la bajada.</p>";
  if (d.zona === "zt") note += "<p><strong>Zona tensionada:</strong> esta calculadora no la modela. Puede afectar a la renta inicial de un contrato nuevo y a la prórroga (arts. 17.6 y 10.2-3), no a este cálculo.</p>";
  if (d.zona === "gt") note += "<p><strong>Gran tenedor:</strong> esta calculadora no lo modela; algunas reglas de renta inicial y prórroga son distintas para ti, no este cálculo de actualización.</p>";
  note += "<p><strong>Vigencia (2/10/2026):</strong> el tope del 2 % del Real Decreto-ley 26/2026 existió del 1 al 2 de octubre de 2026 y no rige (derogado, BOE-A-2026-20526). Si la subida se notificó el 1 o el 2 de octubre de 2026, con ese decreto-ley en vigor, consulta a un profesional. El IRAV y el IPC son editables: usa el último publicado a la fecha de actualización.</p>";
  note += "<p><strong>No incluye:</strong> uso distinto de vivienda, vivienda de protección oficial, normativa autonómica (Cataluña, País Vasco, Navarra…), prórrogas extraordinarias, reducción de renta en zona tensionada, actualizaciones atrasadas no reclamadas y bajadas de renta.</p>";
  EM.renderResult({ winner: "e" + r.escenario + d.firma + d.indice, tone: tone, verdict: v, bigNumber: big, bigLabel: bigLbl, format: EM.eur, cols: ["Al mes", "Al año"], rows: rows, note: note });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
