// Actualizacion de la renta del alquiler de vivienda (LAU art. 18.1-2 en la redaccion del RDL 29/2026, art. 3 y DF 6.a; DA 11.a y DT 4.a Ley 12/2023). Parametros y fuentes: data/params.json -> renta_alquiler_2026 (IRAV, IPC, tope y fechas). RDL 29/2026: en vigor desde el 8-10-2026, pendiente de convalidacion.
var P = {"tope": 2, "ini": "2026-10-08", "fin": "2027-12-31"};
var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
// firma: post (desde 26-5-2023), pre (6-3-2019 a 25-5-2023), ant (antes de 6-3-2019: orientativo). indice: none | ipc | igc (sin indice: IRAV) | otro.
// aniv: fecha ISO de inicio del tramo de aniversario elegido ("2000-01-01" = hasta el 7-10-2026). sup: no | si | nls (renta sobre el indice estatal de referencia).
// pct = subida maxima en %: IRAV como tope en todo caso (art. 18.1) y, con aniversario entre P.ini y P.fin, ninguna subida si la renta supera el indice o, si no, maximo P.tope % sin nuevo pacto (DF 6.a).
function calcular(d) {
  var r = d.renta, o = { noModelado: 0, exacto: 1, pct: 0, escenario: 0, ventana: 0 };
  var base = 0;
  if (d.indice === "ipc") base = Math.min(d.ipc, d.irav);
  else if (d.indice !== "none") base = d.irav;
  base = Math.max(base, 0);
  if (d.indice === "otro" || d.firma === "ant") o.exacto = 0;
  var vent = d.aniv !== "2000-01-01" && d.aniv >= P.ini && d.aniv <= P.fin;
  var pct = base;
  if (d.indice !== "none" && vent) {
    if (d.sup === "si") pct = 0;
    else { pct = Math.min(base, P.tope); if (d.sup === "nls") o.exacto = 0; }
  }
  var nueva = Math.round(r * (1 + pct / 100) * 100) / 100;
  var sm = Math.round((nueva - r) * 100) / 100;
  var ex = d.pide > 0 ? Math.max(0, d.pide - nueva) : 0;
  o.pct = pct; o.nueva = nueva; o.subidaMes = sm; o.subidaAnio = Math.round(sm * 12 * 100) / 100;
  o.ventana = vent ? 1 : 0;
  o.nuevaSinTope = Math.round(r * (1 + base / 100) * 100) / 100;
  o.mesCobro = d.aniv === "2000-01-01" ? 0 : parseInt(d.aniv.substr(5, 2), 10) % 12 + 1;
  o.excesoMes = Math.round(ex * 100) / 100; o.excesoAnio = Math.round(ex * 12 * 100) / 100;
  if (d.indice === "none") o.escenario = 1;
  else if (vent && d.sup === "si") o.escenario = 6;
  else if (pct <= 0) o.escenario = 5;
  else if (!(d.pide > 0)) o.escenario = 4;
  else if (d.pide <= nueva + 0.005) o.escenario = 2;
  else o.escenario = 3;
  return o;
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["renta", "irav", "ipc", "pide"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["firma", "indice", "aniv", "sup"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.renta <= 0) return;
  var r = calcular(d), v, tone = "ok", rows = [], note = "", big, bigLbl;
  var cobro = r.mesCobro ? "el recibo de " + MESES[r.mesCobro - 1] : "el recibo del mes siguiente a la notificación";
  var notif = r.mesCobro ? " en " + MESES[(r.mesCobro + 10) % 12] : "";
  var salv = "en vigor desde el 8/10/2026 (Real Decreto-ley 29/2026), pendiente de convalidación";
  var topeTxt = d.indice === "ipc" ? "el menor entre el IPC y el IRAV" : "el IRAV";
  var limita2 = r.ventana && d.sup !== "si" && d.indice !== "none" && r.nueva < r.nuevaSinTope;
  if (r.escenario === 1) {
    v = "Con tus datos, tu casero no puede subirte la renta: sin cláusula de actualización en el contrato no hay actualización (art. 18.1 LAU), y seguirías pagando " + EM.eur(d.renta) + " al mes.";
    if (d.pide > d.renta) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera tu renta actual en " + EM.eur(r.excesoMes) + " al mes; solo podría subir si lo acordáis por escrito.";
  } else if (r.escenario === 6) {
    v = "Con tus datos, tu casero no puede subirte la renta en este aniversario: la renta supera el límite del índice estatal de precios de referencia y, con aniversario entre el 8/10/2026 y el 31/12/2027, no se admite ningún incremento (" + salv + "). Seguirías pagando " + EM.eur(d.renta) + " al mes. Si el RDL 29/2026 se derogara antes de tu aniversario, el máximo sería " + EM.eur(r.nuevaSinTope) + " al mes (" + EM.num(Math.max(0, d.indice === "ipc" ? Math.min(d.ipc, d.irav) : d.irav), 2) + " %).";
    if (d.pide > d.renta) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera tu renta en " + EM.eur(r.excesoMes) + " al mes.";
  } else if (r.escenario === 5) {
    v = "Con tus datos, la variación del índice que limita la subida no es positiva, así que el casero no puede exigirte una subida: la renta máxima sigue siendo " + EM.eur(d.renta) + " al mes (si tu cláusula es el IPC, el inquilino puede pedir que se aplique la variación negativa; esta calculadora no la calcula).";
    if (d.pide > d.renta) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera tu renta actual: solo sería válido si lo acordáis por escrito.";
  } else {
    var exacta = r.exacto ? "puede exigirte como máximo" : "puede exigirte, como máximo y según lo que diga tu cláusula,";
    v = "Con tus datos, tu casero " + exacta + " una subida del " + EM.num(r.pct, 2) + " %: de " + EM.eur(d.renta) + " a " + EM.eur(r.nueva) + " al mes (" + EM.eur(r.subidaMes) + " más al mes, " + EM.eur(r.subidaAnio) + " al año), desde " + cobro + " si te lo notifica por escrito" + notif + ".";
    if (limita2) v += " El límite es el 2 % de la disposición final 6.ª del Real Decreto-ley 29/2026 (" + salv + "): sin él, el máximo sería " + EM.eur(r.nuevaSinTope) + " al mes. Un nuevo pacto por escrito podría fijar otra cifra, pero seguiría limitado por el IRAV «en todo caso» (art. 18.1; interpretación nuestra) y no cabe si la renta supera el índice.";
    else if (r.ventana) v += " Tu aniversario está en el periodo del 2 % del Real Decreto-ley 29/2026 (" + salv + "), pero el tope de tu cláusula ya es menor.";
    if (r.escenario === 3) { v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) supera ese máximo en " + EM.eur(r.excesoMes) + " al mes (" + EM.eur(r.excesoAnio) + " al año): esa parte no puedes tener que pagarla por la actualización."; tone = "warn"; }
    else if (r.escenario === 2) v += " Lo que te piden (" + EM.eur(d.pide) + " al mes) está dentro de ese máximo.";
    else v += " Si te piden más que " + EM.eur(r.nueva) + " al mes, el exceso no es una actualización válida.";
  }
  big = r.nueva; bigLbl = "renta mensual máxima tras la actualización";
  rows.push(["Renta actual", EM.eur(d.renta), EM.eur(d.renta * 12)]);
  rows.push({ label: "Renta máxima actualizada", values: [EM.eur(r.nueva), EM.eur(r.nueva * 12)], strong: true });
  rows.push(["Subida máxima", EM.eur(r.subidaMes), EM.eur(r.subidaAnio)]);
  if (r.ventana && d.indice !== "none") rows.push(["Máximo sin el RDL 29/2026 (si se derogara antes del aniversario)", EM.eur(r.nuevaSinTope), EM.eur(r.nuevaSinTope * 12)]);
  if (d.pide > 0) {
    rows.push(["Lo que te piden", EM.eur(d.pide), EM.eur(d.pide * 12)]);
    rows.push(["Exceso sobre el máximo", EM.eur(r.excesoMes), EM.eur(r.excesoAnio)]);
  }
  note += "<p><strong>Qué regla rige:</strong> ";
  if (d.indice === "none") note += "sin cláusula de actualización, la renta no se actualiza (art. 18.1 LAU).</p>";
  else {
    note += "la actualización solo puede hacerse en cada aniversario del contrato, con tope en " + topeTxt + " «en todo caso» (art. 18.1 LAU, redacción del Real Decreto-ley 29/2026; la disposición transitoria 4.ª.1 de la Ley 12/2023, en la redacción del art. 4.Dos del RDL 29/2026, lo extiende a los contratos anteriores al 26/5/2023). ";
    if (d.indice === "igc") note += "Si la cláusula no dice el índice, se actualiza con el IRAV (antes, con el IGC). ";
    if (d.indice === "otro") note += "Si pactasteis otro índice, la subida real puede ser menor que este máximo. ";
    if (d.firma === "ant") note += "Con un contrato entre el 1/1/1995 y el 5/3/2019 el resultado es orientativo: revisa tu cláusula. ";
    note += "Con IRAV " + EM.num(d.irav, 2) + " % e IPC " + EM.num(d.ipc, 2) + " %, el tope del contrato es " + EM.num(Math.max(0, d.indice === "ipc" ? Math.min(d.ipc, d.irav) : d.irav), 2) + " %.</p>";
  }
  if (r.ventana && d.indice !== "none") {
    note += "<p><strong>Tope del 2 % (RDL 29/2026, DF 6.ª):</strong> para contratos de vivienda sujetos a la LAU, sea cual sea su fecha de firma, con aniversario entre el 8/10/2026 y el 31/12/2027: si la renta supera el límite del índice estatal de precios de referencia no hay incremento; si no, lo que fije un nuevo pacto y, sin él, como máximo el 2 %. Por lo general, ese índice solo existe para zonas tensionadas declaradas: si no sabes si tu renta lo supera, mira el índice de tu zona antes de aceptar la subida.</p>";
    if (d.sup === "nls") note += "<p><strong>Has marcado «no lo sé»:</strong> se calcula como si la renta no superara el índice; si lo supera, la subida es cero.</p>";
  }
  note += "<p><strong>Cuándo se cobra:</strong> desde el mes siguiente a la notificación escrita del porcentaje aplicado; vale una nota en el recibo anterior (art. 18.2). No hay un preaviso legal de un mes." + (r.mesCobro ? " Se supone que la notificas en el mes del aniversario." : "") + "</p>";
  if (r.escenario === 5 && (d.indice === "ipc" || d.indice === "igc")) note += "<p><strong>Índice negativo:</strong> la subida máxima es cero, pero con el IPC pactado o con una cláusula sin índice (IRAV) y un índice negativo, la actualización puede bajar la renta y también puedes pedirla tú como inquilino (art. 18.1). No se calcula la bajada.</p>";
  note += "<p><strong>Vigencia (7/10/2026):</strong> el Real Decreto-ley 29/2026 (BOE-A-2026-20823) está " + salv + ". Si se derogara (los Reales Decretos-ley 26/2026 y 27/2026, casi idénticos, se derogaron el 2/10/2026), en principio no habría efecto retroactivo: las actualizaciones con aniversario entre el 8/10/2026 y la derogación quedarían con el tope del 2 %. Si tu aniversario es anterior al 8/10/2026, este tope no te afecta. El IRAV y el IPC son editables: usa el último publicado a la fecha de actualización.</p>";
  note += "<p><strong>No incluye:</strong> uso distinto de vivienda, vivienda de protección oficial, contratos anteriores al 1/1/1995 (renta antigua, DT 1.ª y 2.ª LAU), normas autonómicas adicionales (Cataluña, País Vasco, Navarra…: no se modelan), prórrogas extraordinarias, reducción de renta en zona tensionada, la excepción de rentas altas, actualizaciones atrasadas no reclamadas y bajadas de renta.</p>";
  EM.renderResult({ winner: "e" + r.escenario + d.firma + d.indice + r.ventana, tone: tone, verdict: v, bigNumber: big, bigLabel: bigLbl, format: EM.eur, cols: ["Al mes", "Al año"], rows: rows, note: note });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
