// Indemnizacion por despido objetivo o improcedente, neta de IRPF. Parametros generados desde data/params.json -> indemnizacion_despido_2026 (fuentes y fechas alli).
var P = {"dObj": 20, "mObj": 12, "dImp": 33, "mImp": 24, "dPre": 45, "topePre": 720, "mPre": 42, "mens": 30, "anio": 365, "exMax": 180000, "redPct": 30, "redBase": 300000, "red0": 700000, "red1": 1000000, "redAnios": 2, "igual": 1, "margMax": 55};
function reduccionBase(t) { return Math.min(t, Math.max(0, P.redBase - Math.max(0, t - P.red0))); }
function neto(cobrado, legal, M, marg) {
  var ex = Math.min(cobrado, legal, P.exMax), trib = cobrado - ex, red = M > P.redAnios * 12 ? P.redPct / 100 * reduccionBase(trib) : 0, irpf = (trib - red) * marg / 100;
  return { exento: ex, trib: trib, red: red, irpf: irpf, neto: cobrado - irpf };
}
function calcular(d) {
  var bruto = +d.bruto || 0, a = Math.floor(+d.anios || 0), m = Math.floor(+d.meses || 0), antes = Math.floor(+d.antes || 0), oferta = +d.oferta || 0, marg = +d.marginal || 0, M = a * 12 + m;
  var z = { bloqueado: 1, escenario: 0, M: 0, salDia: 0, diasObj: 0, legalObj: 0, diasImp: 0, legalImp: 0, legal: 0, exento: 0, trib: 0, red: 0, irpf: 0, neto: 0, netoLegal: 0, netoObj: 0, netoImp: 0, difBruta: 0, difNeta: 0, impMenosObj: 0, topeObj: 0, topeImp: 0, reduccionAplica: 0, motivo: "" };
  if (bruto <= 0 || M <= 0 || a < 0 || m < 0 || m > 11 || antes < 0 || antes > M || marg < 0 || marg > P.margMax || oferta < 0) { z.motivo = antes > M ? "antes" : "datos"; return z; }
  var sal = bruto / P.anio, rawObj = P.dObj * M / 12, diasObj = Math.min(rawObj, P.mObj * P.mens), rawImp, cap;
  if (antes === 0) { rawImp = P.dImp * M / 12; cap = P.mImp * P.mens; }
  else { var r45 = P.dPre * antes / 12; rawImp = r45 + P.dImp * (M - antes) / 12; cap = r45 > P.topePre ? Math.min(r45, P.mPre * P.mens) : P.topePre; }
  var diasImp = Math.min(rawImp, cap), legalObj = diasObj * sal, legalImp = diasImp * sal, objetivo = d.tipo === "objetivo", legal = objetivo ? legalObj : legalImp;
  var hay = oferta > 0, cobrado = hay ? oferta : legal, lim = objetivo && d.causa !== "otra" ? legalImp : legal, n = neto(cobrado, lim, M, marg), nObj = neto(legalObj, legalObj, M, marg), nImp = neto(legalImp, legalImp, M, marg), nLegal = objetivo ? nObj : nImp, dif = cobrado - legal;
  var esc = !hay ? 4 : dif < -P.igual ? 1 : dif <= P.igual ? 2 : 3;
  return { bloqueado: 0, escenario: esc, M: M, salDia: sal, diasObj: diasObj, legalObj: legalObj, diasImp: diasImp, legalImp: legalImp, legal: legal, exento: n.exento, trib: n.trib, red: n.red, irpf: n.irpf, neto: n.neto,
    netoLegal: nLegal.neto, netoObj: nObj.neto, netoImp: nImp.neto, difBruta: dif, difNeta: n.neto - nLegal.neto, impMenosObj: legalImp - legalObj, topeObj: rawObj > P.mObj * P.mens ? 1 : 0, topeImp: rawImp > cap ? 1 : 0, reduccionAplica: M > P.redAnios * 12 ? 1 : 0, motivo: "" };
}
function eur(x) { return EM.eur(x); }
function dias(x) { return EM.num(x, 1) + " días"; }
function leer() {
  var d = {}; ["bruto", "anios", "meses", "antes", "oferta", "marginal"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.tipo = document.getElementById("tipo").value; d.causa = document.getElementById("causa").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.bruto <= 0) return;
  var r = calcular(d);
  if (r.bloqueado) {
    EM.renderResult({ winner: "bloqueado", verdict: r.motivo === "antes" ? "Los meses trabajados antes del 12-2-2012 no pueden superar tu antigüedad total." : "Revisa los datos: hace falta un salario positivo, al menos un mes de antigüedad, meses entre 0 y 11 y un tipo marginal entre 0 y " + P.margMax + " %.", tone: "warn",
      note: "<p>La calculadora no puede dar una cifra con estos datos.</p>" });
    return;
  }
  var obj = d.tipo === "objetivo", pre = Math.floor(d.antes) > 0, nombre = obj ? "despido objetivo (" + P.dObj + " días por año)" : "despido improcedente (" + (pre ? P.dPre + " días por año hasta el 11-2-2012 y " + P.dImp + " después" : P.dImp + " días por año") + ")";
  var legal = r.legal, ver, tone, extra = "", partes = "";
  if (r.escenario === 4) {
    ver = "Con estos datos, la indemnización legal de un " + nombre + " es de " + eur(legal) + " brutos (" + dias(obj ? r.diasObj : r.diasImp) + " de salario) y te quedarían unos " + eur(r.neto) + " netos de IRPF." + (obj ? " Si un juez lo declarase improcedente serían " + eur(r.legalImp) + " (" + eur(r.impMenosObj) + " más)." : "");
    tone = "info";
  } else if (r.escenario === 1) {
    ver = "Con estos datos, la oferta de " + eur(d.oferta) + " queda " + eur(-r.difBruta) + " por debajo de la indemnización legal de un " + nombre + " (" + eur(legal) + "): puedes reclamar la diferencia, pero el plazo para demandar es de 20 días hábiles desde el despido (art. 59.3 del Estatuto de los Trabajadores).";
    tone = "warn";
  } else if (r.escenario === 2) {
    ver = "Con estos datos, la oferta de " + eur(d.oferta) + " coincide con la indemnización legal de un " + nombre + " (" + eur(legal) + "), exenta de IRPF hasta " + eur(P.exMax) + "." + (obj ? " Lo que queda por decidir es si el despido es procedente: si un juez lo declarase improcedente serían " + eur(r.legalImp) + " (" + eur(r.impMenosObj) + " más), pero eso depende de que haya motivos y no es seguro." : "");
    tone = "ok";
  } else {
    ver = "Con estos datos, la oferta de " + eur(d.oferta) + " supera en " + eur(r.difBruta) + " la indemnización legal de un " + nombre + " (" + eur(legal) + "): " + (r.trib > P.igual ? "la parte exenta (" + eur(r.exento) + ") no tributa y el resto sí" : "toda la oferta está exenta de IRPF por ser un despido objetivo por causas económicas, técnicas, organizativas o de producción y no superar la indemnización del improcedente") + ", de modo que te quedarían unos " + eur(r.neto) + " netos, " + eur(r.difNeta) + " más que con la legal.";
    tone = "ok";
  }
  if (!obj) extra += "<p><strong>Condición de la exención:</strong> la indemnización del improcedente solo queda exenta si la improcedencia se reconoce en conciliación ante el servicio administrativo (art. 63 de la Ley reguladora de la jurisdicción social) o en sentencia; lo pagado por un pacto privado es un pacto y tributa.</p>";
  if (obj) extra += "<p><strong>¿Aceptar los " + P.dObj + " días o reclamar los " + P.dImp + "?</strong> Si el despido objetivo se declara procedente cobras la indemnización de " + P.dObj + " días (" + eur(r.legalObj) + "); si se declara improcedente y la empresa opta por indemnizar, " + (pre ? "con tu contrato anterior a 2012 salen " + dias(r.diasImp) : "salen " + dias(r.diasImp)) + " (" + eur(r.legalImp) + ", " + eur(r.impMenosObj) + " más brutos). Cuál es más probable lo decide un juez según la causa alegada: la calculadora solo mide lo que está en juego.</p>";
  else extra += "<p><strong>Si fuera un despido objetivo procedente</strong> cobrarías " + dias(r.diasObj) + " (" + eur(r.legalObj) + "), " + eur(r.impMenosObj) + " menos que en el improcedente.</p>";
  if (r.topeObj) partes += "Se aplica el tope de " + P.mObj + " mensualidades en el despido objetivo. ";
  if (r.topeImp) partes += "Se aplica el tope del despido improcedente (" + (pre && r.diasImp > P.topePre ? "hasta " + P.mPre + " mensualidades por el tramo anterior a 2012" : P.mImp + " mensualidades") + "). ";
  if (partes) extra += "<p>" + partes + "</p>";
  if (r.trib > 0) extra += "<p><strong>Tributación:</strong> " + eur(r.exento) + " exentos (art. 7.e de la Ley del IRPF" + (r.exento >= P.exMax ? ", con el límite de " + eur(P.exMax) + "" : "") + ") y " + eur(r.trib) + " tributan como rendimiento del trabajo" + (r.reduccionAplica ? ", con la reducción del " + P.redPct + " % por superar " + P.redAnios + " años de servicio (art. 18.2): " + eur(r.red) + " menos de base" : ", sin reducción porque tu antigüedad no supera " + P.redAnios + " años") + ". IRPF estimado: " + eur(r.irpf) + " con un tipo marginal del " + EM.num(d.marginal, 1) + " %; si la parte tributable es grande te sube de tramo y el tipo real sería mayor.</p>";
  else extra += "<p><strong>Tributación:</strong> toda la cantidad está exenta de IRPF (art. 7.e) mientras no supere " + (obj && d.causa !== "otra" ? "la indemnización del improcedente (" + eur(r.legalImp) + ", despido objetivo por causas económicas, técnicas, organizativas o de producción)" : "la indemnización legal") + " ni " + eur(P.exMax) + ".</p>";
  extra += "<p><strong>Paro:</strong> el despido es situación legal de desempleo y puedes pedir la prestación en los 15 días siguientes (arts. 267 y 268 de la Ley General de la Seguridad Social); su importe sale de tus cotizaciones, no de la indemnización. <a href=\"/decidir/cuanto-cobro-de-paro-prestacion-desempleo/\">Calcula cuánto cobrarías</a>. Para el subsidio, la indemnización legal no cuenta como renta pero el exceso pactado sí (art. 275.5.b).</p>";
  extra += "<p><strong>Límites del cálculo:</strong> contrato ordinario, despido individual, territorio común. No incluye despido colectivo, nulo ni disciplinario procedente (sin indemnización), alta dirección, indemnizaciones mayores por convenio o contrato, FOGASA, salarios de tramitación ni costes del proceso. La exención exige desvinculación real de la empresa (art. 1 del Reglamento del IRPF). El tipo marginal es una aproximación y no sustituye a la declaración.</p>";
  EM.renderResult({
    winner: "e" + r.escenario, verdict: ver, tone: tone, bigNumber: r.neto, bigLabel: r.escenario === 4 ? "netos de la indemnización legal (estimado)" : "netos de lo que te ofrecen (estimado)", format: EM.eur,
    barsLabel: "Indemnización bruta",
    bars: [{ label: "Objetivo (" + P.dObj + " días)", value: r.legalObj, color: "a" }, { label: "Improcedente" + (pre ? " (45 + 33 días)" : " (" + P.dImp + " días)"), value: r.legalImp, color: "b" }].concat(r.escenario === 4 ? [] : [{ label: "Oferta de la empresa", value: d.oferta, color: "a" }]),
    cols: ["Importe"],
    rows: [
      ["Salario diario de referencia", eur(r.salDia)],
      ["Antigüedad", Math.floor(r.M / 12) + " años y " + (r.M % 12) + " meses"],
      ["Legal objetivo: " + dias(r.diasObj), eur(r.legalObj)],
      ["Legal improcedente: " + dias(r.diasImp), eur(r.legalImp)],
      ["Parte exenta de IRPF", eur(r.exento)],
      ["Parte tributable (antes de la reducción)", eur(r.trib)],
      ["IRPF estimado", eur(r.irpf)],
      { label: "Neto estimado", values: [eur(r.neto)], strong: true }
    ].concat(r.escenario === 4 ? [] : [["Oferta menos legal (bruto)", eur(r.difBruta)]]),
    note: extra
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
