// Obligacion de declarar el IRPF (art. 96 Ley 35/2006, texto consolidado; fuentes y fecha en data/params.json -> obligado_declarar_2026).
var P = { gen: 22000, multi: 15876, resto: 1500, cap: 1600, inm: 1000, tot: 1000 };
function calcular(d) {
  var pag = [+d.t1 || 0, +d.t2 || 0, +d.t3 || 0].filter(function (x) { return x > 0; }).sort(function (a, b) { return b - a; });
  var cap = Math.max(0, +d.capRet || 0), inm = Math.max(0, +d.inmo || 0), esp = +d.esp || 0, obl = +d.obl || 0, noret = +d.noRet === 1, i, total = 0, resto = 0;
  if (d.reg === "foral") return { estado: 3, supuesto: 0, limiteTrabajo: 0, totalTrabajo: 0, resto: 0, exceso: 0, limite: 0, nMotivos: 0, margen: 0, motivos: [], causas: [] };
  for (i = 0; i < pag.length; i++) { total += pag[i]; if (i > 0) resto += pag[i]; }
  var causas = [];
  if (pag.length >= 2 && resto > P.resto && esp !== 7) causas.push(2);
  if (esp === 1) causas.push(3);
  if (noret && pag.length) causas.push(4);
  if (esp === 2) causas.push(5);
  var lim = causas.length ? P.multi : P.gen, mot = [];
  if (obl === 3) mot.push({ s: 10, ex: 0, li: 0 });
  if (obl === 4) mot.push({ s: 11, ex: 0, li: 0 });
  if (obl === 6) mot.push({ s: 12, ex: 0, li: 0 });
  if (total > lim) mot.push({ s: causas.length ? causas[0] : 1, ex: total - lim, li: lim });
  if (cap > P.cap) mot.push({ s: 6, ex: cap - P.cap, li: P.cap });
  if (inm > P.inm) mot.push({ s: 7, ex: inm - P.inm, li: P.inm });
  var todo = total + cap + inm;
  if (esp === 5 && todo > P.tot) mot.push({ s: 13, ex: todo - P.tot, li: P.tot });
  var r = { limiteTrabajo: lim, totalTrabajo: total, resto: resto, nMotivos: mot.length, margen: Math.max(0, lim - total), causas: causas, todo: todo,
    motivos: mot.map(function (m) { return m.s; }) };
  if (mot.length) { r.estado = 1; r.supuesto = mot[0].s; r.exceso = mot[0].ex; r.limite = mot[0].li; }
  else if (esp === 5) { r.estado = 2; r.supuesto = 14; r.exceso = 0; r.limite = P.tot; }
  else { r.estado = 0; r.supuesto = 0; r.exceso = 0; r.limite = 0; }
  return r;
}
function eur(x) { return EM.eur(x); }
var SUP = {
  1: "tus rendimientos del trabajo de un solo pagador (o con el segundo y siguientes sin pasar de 1.500 €) superan el límite de 22.000 €",
  2: "cobras de más de un pagador y el segundo y siguientes suman más de 1.500 €, así que el límite baja a 15.876 € y lo superas",
  3: "cobras pensión compensatoria del cónyuge o anualidades por alimentos no exentas, así que el límite baja a 15.876 € y lo superas",
  4: "algún pagador no está obligado a retener, así que el límite baja a 15.876 € y lo superas",
  5: "tus rendimientos del trabajo van a un tipo fijo de retención, así que el límite baja a 15.876 € y lo superas",
  6: "tus rendimientos del capital mobiliario y ganancias con retención superan el límite conjunto de 1.600 €",
  7: "tus rentas inmobiliarias imputadas, Letras del Tesoro y ayudas a vivienda protegida u otras ayudas públicas superan el límite conjunto de 1.000 €",
  10: "has estado de alta en el RETA (autónomos) o en el Régimen del Mar en algún momento del año",
  11: "si quieres aplicar la reducción por aportaciones a planes de pensiones o similares, o la deducción por doble imposición internacional, la ley te obliga a declarar (art. 96.4 de la Ley y art. 61.1 del Reglamento)",
  12: "eres titular o miembro de la unidad de convivencia de un ingreso mínimo vital",
  13: "tienes otras rentas distintas de las listadas y el total de tus rentas supera 1.000 €"
};
function leer() {
  var d = {}; ["t1", "t2", "t3", "capRet", "inmo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["noRet", "esp", "obl", "reg"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer(), r = calcular(d), i, nota = "";
  var avisoDeclarar = '<p><strong>Aunque no estés obligado, puede convenirte declarar:</strong> si te han retenido de más o tienes deducciones, solo recuperas el dinero presentando la declaración; con dos cónyuges, compara también la <a href="/decidir/declaracion-conjunta-o-individual/">declaración conjunta o individual</a>.</p>';
  var excl = '<p><strong>No incluye:</strong> mínimo por descendientes (no cambia la obligación), rentas exentas, no residentes, retenciones distintas de las habituales, cambios de situación familiar durante el año, ni la tributación conjunta (los límites se aplican a la unidad familiar). Los límites son los del ejercicio 2026 según el texto consolidado actual; no hay cifras 2027. Información orientativa, no asesoramiento fiscal.</p>';
  if (r.estado === 3) {
    EM.renderResult({ winner: "foral", verdict: "Esta calculadora no cubre el País Vasco ni Navarra: tienen su propia norma foral y límites distintos.", tone: "warn",
      note: '<p>Consulta la Hacienda Foral de tu territorio. Los límites del art. 96 de la Ley 35/2006 que usa esta página son los del régimen común.</p>' });
    return;
  }
  var v, tone, big, bigL, extra = "";
  if (r.estado === 1) {
    var s = r.supuesto;
    v = "Con estos datos estás obligado a declarar (territorio común): " + SUP[s] + (r.exceso > 0 ? " (te pasas en " + EM.eur(r.exceso) + ")" : "") + ".";
    tone = "warn"; big = r.exceso > 0 ? r.exceso : undefined; bigL = r.exceso > 0 ? "por encima del límite aplicable" : "";
    if (r.nMotivos > 1) { var otros = []; for (i = 1; i < r.motivos.length; i++) otros.push("<li>" + SUP[r.motivos[i]] + "</li>"); extra = "<p>Además se cumple a la vez:</p><ul>" + otros.join("") + "</ul>"; }
  } else if (r.estado === 2) {
    v = "Depende: con tus cifras listadas no llegas a ningún límite, pero al tener otras rentas distintas, estás obligado si el total de todas tus rentas supera 1.000 €.";
    tone = "info";
  } else {
    v = "Con estos datos no estarías obligado a declarar (territorio común)" + (r.totalTrabajo > 0 ? ": tu trabajo (" + EM.eur(r.totalTrabajo) + ") queda dentro del límite de " + EM.eur(r.limiteTrabajo) + "" : "") + ", pero revisa si te conviene hacerlo.";
    tone = "ok"; big = r.margen; bigL = "de margen hasta el límite del trabajo";
  }
  var cond = [];
  if (r.causas.indexOf(2) >= 0) cond.push("varios pagadores con el 2.º y siguientes por encima de 1.500 € (suman " + EM.eur(r.resto) + ")");
  if (r.causas.indexOf(3) >= 0) cond.push("pensión compensatoria o alimentos");
  if (r.causas.indexOf(4) >= 0) cond.push("pagador no obligado a retener");
  if (r.causas.indexOf(5) >= 0) cond.push("tipo fijo de retención");
  nota = '<p><strong>Límite del trabajo aplicado:</strong> ' + EM.eur(r.limiteTrabajo) + (cond.length ? " por " + cond.join(", ") : (r.resto > 0 ? " (hay más de un pagador, pero el segundo y siguientes suman " + EM.eur(r.resto) + ", sin pasar de 1.500 €, o solo cobras pensiones con procedimiento especial)" : "")) + '. El límite se cumple si lo superas: con la cifra justo en el límite no estás obligado por ese concepto.</p>' + extra + avisoDeclarar +
    '<p>Los límites del art. 96.3 de la Ley 35/2006 son 15.876 €; el reglamento (art. 61 RIRPF) aún dice 15.000 €, pero la ley es posterior y la AEAT aplica 15.876 €.</p>' + excl;
  EM.renderResult({
    winner: r.estado + "-" + r.supuesto, verdict: v, tone: tone, bigNumber: big, bigLabel: bigL, format: EM.eur,
    barsLabel: "Rendimientos del trabajo frente a tu límite",
    bars: [{ label: "Tus rendimientos del trabajo", value: r.totalTrabajo, color: "a" }, { label: "Límite que te aplica", value: r.limiteTrabajo, color: "b" }],
    cols: ["Tu cifra", "Límite", "¿Obliga?"],
    rows: [
      ["Rendimientos del trabajo", EM.eur(r.totalTrabajo), EM.eur(r.limiteTrabajo), r.totalTrabajo > r.limiteTrabajo ? "Sí" : "No"],
      ["Capital mobiliario y ganancias con retención", EM.eur(d.capRet), EM.eur(P.cap), d.capRet > P.cap ? "Sí" : "No"],
      ["Rentas inmobiliarias, Letras y ayudas", EM.eur(d.inmo), EM.eur(P.inm), d.inmo > P.inm ? "Sí" : "No"],
      { label: "Resultado", values: ["", "", r.estado === 1 ? "Obligado" : (r.estado === 2 ? "Depende" : "No obligado")], strong: true }
    ],
    note: nota
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
