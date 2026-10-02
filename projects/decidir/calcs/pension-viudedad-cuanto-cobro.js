// Pension de viudedad: cuanto cobrare (2026). Parametros generados desde data/params.json -> viudedad_2026 (fuentes y fechas alli).
// pct: 52 % base, 60 % mejora (65+, sin otra pension ni trabajo), 70 % con cargas familiares. Minimos y limites en euros/ano (14 pagas).
var P = {"pctBase": 52, "pctMejora": 60, "pctCargas": 70, "edadMejora": 65, "limIng": 9442, "minCargas": 17592.4, "min65": 13106.8, "min6064": 12262.6, "minMenor60": 9931.6, "maxMes": 3359.6, "pagas": 14, "umbralMiembro": 10989, "pctMinPension": 50, "convPareja": 5, "anosMatrimonio": 1, "mesesTemporal": 24};
function calcular(d) {
  var br = d.br, ing = d.ingresos, edad = d.edad, h = Math.max(Math.round(d.hijos), 0), otra = d.otra;
  if (d.causante === "nocumple") return { bloqueo: 1 };
  var temporal = 0;
  if (d.union === "matrimonio") {
    if (d.causante !== "accidente" && d.anos < P.anosMatrimonio && h === 0) temporal = 1;
  } else {
    if (!(h > 0 || d.anos >= P.convPareja)) return { bloqueo: 2 };
    if (d.union === "pareja_corta") temporal = 1;
  }
  var n = 1 + h, rend = ing + otra * P.pagas, limAmplio = P.limIng + P.minCargas;
  var p52 = br * P.pctBase / 100 * P.pagas, p60 = br * P.pctMejora / 100 * P.pagas, p70 = br * P.pctCargas / 100 * P.pagas;
  var cEstricta = h >= 1 && rend / n <= P.umbralMiembro;
  var minEdad = edad >= 65 ? P.min65 : (edad >= 60 ? P.min6064 : P.minMenor60), limLit = P.limIng + minEdad;
  function pen70(carg, lim) {
    if (!carg || rend > lim) return null;
    var pe = Math.min(p70, lim - rend);
    if (pe <= 0 || pe / (pe + rend) < P.pctMinPension / 100) return null;
    return pe;
  }
  var pct = P.pctBase, anual = p52, pe = pen70(cEstricta, limLit);
  if (edad >= P.edadMejora && otra === 0 && ing === 0) { pct = P.pctMejora; anual = p60; }
  if (pe !== null && pe > p52 && pe > anual) { pct = P.pctCargas; anual = pe; }
  var pos = (edad >= P.edadMejora && otra === 0 && ing > 0 && ing <= P.limIng && pct < P.pctMejora) ? P.pctMejora : 0;
  var mant = (pct === P.pctCargas && (rend + anual) / n > P.umbralMiembro) ? 1 : 0;
  var mesPre = anual / P.pagas, cap = Math.max(P.maxMes - otra, 0), mes = Math.min(mesPre, cap);
  var pw = pen70(cEstricta, limAmplio), alt = 0;
  if (pw !== null && pw > p52 && pw > anual + 0.005 && !(pct === P.pctMejora && p60 >= pw)) { var am = Math.min(pw / P.pagas, cap); if (am > mes + 0.005) alt = am; }
  var minimo = (cEstricta ? P.minCargas : minEdad) / P.pagas;
  return { bloqueo: 0, temporal: temporal, pct: pct, mes_pre: mesPre, mes: mes, anual: mes * P.pagas, capado: mesPre > cap + 1e-9 ? 1 : 0,
    minimo: minimo, falta: Math.max(minimo - mes, 0), pos: pos, alt: alt, mant: mant, limite: limLit, cargas: cEstricta ? 1 : 0, rend: rend, br: br, cap: cap };
}
function eur(x) { return EM.eur(x); }
var IDS = ["br", "ingresos", "edad", "hijos", "anos", "otra"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.causante = document.getElementById("causante").value; d.union = document.getElementById("union").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
var NO_MODELA = "<p><strong>No incluye:</strong> la retención del IRPF (lo que ingresas en la cuenta es menos que el bruto), el complemento por brecha de género por hijo (36,90 € al mes por hijo, hasta 4, para mujeres con hijos y, en algunos casos, hombres), la pensión de orfandad ni el reparto entre viudedad y orfandad, la viudedad de separados y divorciados, los regímenes forales, de mutualistas y de Clases Pasivas, la extinción por nuevo matrimonio o pareja de hecho, ni el cálculo de la base reguladora (la pones tú: la Seguridad Social te la comunica en la resolución).</p>";
function pintar() {
  var d = leer();
  if (d.br <= 0 || d.ingresos < 0 || d.otra < 0 || d.hijos < 0 || d.anos < 0) { aviso("Revisa los datos: la base reguladora debe ser mayor que 0 y ingresos, otra pensión, hijos y años no pueden ser negativos."); return; }
  if (d.edad < 16 || d.edad > 110) { aviso("Revisa la edad: indica la edad del superviviente (entre 16 y 110 años)."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Si el fallecido estaba en alta, necesitas que hubiera cotizado 500 días en los 5 años anteriores (o 15 años en total si no estaba en alta), salvo que la muerte fuera por accidente o enfermedad profesional (art. 219.1 de la LGSS). Con tus datos no hay pensión de viudedad. Comprueba su vida laboral: consúltalo en la Seguridad Social."); return; }
  if (r.bloqueo === 2) { aviso("Como pareja de hecho necesitas una convivencia estable de al menos 5 años acreditada con el empadronamiento, salvo que tengáis hijos en común (art. 221.2 de la LGSS). Con tus datos no hay pensión de viudedad. Consúltalo en la Seguridad Social."); return; }
  var tiene = r.temporal ? "prestación temporal de viudedad, durante " + P.mesesTemporal + " meses" : "pensión de viudedad vitalicia";
  var porque = r.pct === 70 ? "tienes cargas familiares, la pensión es tu principal fuente de ingresos y tus ingresos no superan el límite" : (r.pct === 60 ? "tienes 65 años o más, no cobras otra pensión pública ni trabajas" : "es el porcentaje general");
  var verdict = "Con tus datos tendrías una " + tiene + " del " + r.pct + " % de la base reguladora (" + porque + "): unos " + eur(r.mes) + " brutos al mes en 14 pagas (" + eur(r.anual) + " al año)" +
    (r.mes >= r.minimo ? ", por encima del mínimo de " + eur(r.minimo) + " al mes." : ", por debajo del mínimo de " + eur(r.minimo) + " al mes.");
  var note = "<p><strong>Cómo sale:</strong> base reguladora " + eur(d.br) + " × " + r.pct + " % = " + eur(r.mes_pre) + " al mes" + (r.capado ? "; el límite de 3.359,60 € al mes para el conjunto de pensiones lo reduce a " + eur(r.mes) : "") + ".</p>";
  if (r.pos === 60) note += "<p>Tus ingresos no son cero. Si no proceden del trabajo sino de capital (alquileres, intereses) y no superan " + eur(P.limIng) + " al año, podrías tener el 60 %: " + eur(d.br * 0.6) + " al mes. Si trabajas, se queda el 52 %.</p>";
  if (r.alt > 0) note += "<p><strong>Aviso sobre el límite del 70 %:</strong> el art. 31.2 fija el límite de rendimientos en 9.442 € más la pensión mínima de viudedad \"en función de la edad\": con tu edad, " + eur(r.limite) + " al año, y es el que usamos. Si la Seguridad Social aplicara el mínimo con cargas familiares (27.034,40 € al año), cobrarías hasta " + eur(r.alt) + " al mes. No está confirmado: pregúntalo al pedir la pensión.</p>";
  if (r.mant === 1) note += "<p>Al reconocer la pensión se miran tus ingresos del año anterior, cuando aún no cobrabas la viudedad. En los años siguientes sí cuenta la propia pensión en los rendimientos de tu unidad familiar, y si superan el 75 % del salario mínimo por miembro (10.989 €), el 70 % puede perderse y volverías al 52 %.</p>";
  if (r.temporal) note += "<p>Es temporal porque el matrimonio o la pareja de hecho no cumple el tiempo mínimo (1 año de matrimonio sin hijos, o inscripción de la pareja con 2 años de antelación): se paga la misma cuantía durante 24 meses (art. 222). Si la enfermedad que causó la muerte apareció después de casaros, o si sumando la convivencia previa llegáis a 2 años, sí hay pensión vitalicia (art. 219.2): consúltalo.</p>";
  else note += "<p>Es vitalicia mientras no te cases ni constituyas otra pareja de hecho (art. 223.2) y es compatible con el trabajo (art. 223.1).</p>";
  if (!r.temporal && r.falta > 0.005) note += "<p><strong>Comparación con el mínimo:</strong> el mínimo de tu situación es " + eur(r.minimo) + " al mes y tu pensión queda " + eur(r.falta) + " por debajo. Si tus ingresos sin esta pensión no superan " + eur(P.limIng) + " al año, puedes pedir el complemento por mínimos; no lo calculamos porque tiene límites propios (otras pensiones, cónyuge a cargo, tope de la pensión no contributiva).</p>";
  note += NO_MODELA;
  EM.renderResult({
    winner: r.pct === 70 ? "70" : (r.pct === 60 ? "60" : "52"), verdict: verdict, tone: "info",
    bigNumber: r.mes, bigLabel: "al mes en 14 pagas (bruto)", format: eur,
    barsLabel: "Pensión mensual bruta",
    bars: [{ label: "Tu pensión", value: r.mes, color: "a" }, { label: "Mínimo de tu situación", value: r.minimo, color: "b" }],
    cols: ["Dato"],
    rows: [
      ["Porcentaje aplicable", EM.num(r.pct, 0) + " %"],
      ["Pensión mensual bruta (14 pagas)", eur(r.mes)],
      ["Pensión anual bruta", eur(r.anual)],
      ["Mínimo mensual de tu situación", eur(r.minimo)],
      ["Tipo", r.temporal ? "temporal, 24 meses" : "vitalicia"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
