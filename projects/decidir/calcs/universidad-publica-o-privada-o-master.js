// Universidad publica o privada (grado o master): sobrecoste de la privada y diferencia de salario necesaria para amortizarlo.
// Sobrecoste anual c = matricula privada - publica + coste de vida adicional - ayudas adicionales, pagado al inicio de cada anio de estudio.
// Diferencia de salario (privada - publica): HIPOTESIS del usuario, cobrada al final de cada anio de trabajo, tras estudiar. Tasa 0 = sin descontar.
// VAN = valor actual del salario extra - valor actual del sobrecoste. Empate (VAN = 0): publica.
function calcular(d) {
  var a = Math.round(d.anos), n = Math.round(d.ntrab), r = d.tasa / 100, c = d.matpriv - d.matpub + d.vida - d.ayuda;
  var pvc = 0, fac = 0, t, k, van, A, pay;
  for (t = 0; t < a; t++) pvc += c / Math.pow(1 + r, t);
  for (k = 1; k <= n; k++) fac += 1 / Math.pow(1 + r, a + k);
  van = d.dsal * fac - pvc;
  if (pvc <= 0) pay = 0;
  else if (d.dsal <= 0) pay = -1;
  else {
    A = pvc * Math.pow(1 + r, a) / d.dsal;
    if (r === 0) pay = A;
    else if (A * r >= 1) pay = -1;
    else pay = -Math.log(1 - A * r) / Math.log(1 + r);
  }
  return {
    matPub: a * d.matpub, matPriv: a * d.matpriv, extra: a * (d.vida - d.ayuda), sobrecoste: a * c,
    pvSobrecoste: pvc, van: van, dsalMin: pvc / fac, anosAmortizar: pay, mejor: van > 0 ? 1 : 0, gananciaBruta: d.dsal * n
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["anos", "matpub", "matpriv", "vida", "ayuda", "dsal", "ntrab", "tasa"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function anosTxt(x) { return EM.num(Math.round(x * 10) / 10, 1) + " años"; }
function pintar() {
  var d = leer(), r, v, note, mej, hay, cuando;
  if (d.matpub < 0 || d.matpriv < 0 || d.tasa < 0) return;
  if (d.anos < 1 || d.anos > 8 || Math.round(d.anos) !== d.anos) { aviso("La duración de los estudios debe ser un número entero de 1 a 8 años.", "Un grado suele durar 4 años y un máster 1 o 2: escribe la duración de la opción que comparas."); return; }
  if (d.ntrab < 1 || d.ntrab > 45 || Math.round(d.ntrab) !== d.ntrab) { aviso("Los años de trabajo considerados deben ser un número entero de 1 a 45.", "Es el horizonte en el que cuentas la diferencia de salario que esperas."); return; }
  if (d.tasa > 20) { aviso("La tasa de descuento debe estar entre 0 y 20 %.", "Déjala en 0 si no quieres descontar el dinero futuro."); return; }
  r = calcular(d); mej = r.mejor; hay = r.pvSobrecoste > 0;
  if (!hay) {
    v = "Con estos datos la privada no cuesta más que la pública (" + (r.sobrecoste < 0 ? "cuesta " + EM.eur(-r.sobrecoste) + " menos" : "mismo coste") + "): " + (mej ? "con la diferencia de salario que esperas sale a cuenta" : "con la diferencia de salario que esperas (" + EM.eur(d.dsal) + " al año) la pública sale mejor") + ".";
  } else if (mej) {
    v = "Con tus hipótesis, el sobrecoste de la privada (" + EM.eur(r.sobrecoste) + ") se recupera en " + anosTxt(r.anosAmortizar) + " de trabajo, dentro de los " + d.ntrab + (d.ntrab === 1 ? " año" : " años") + " que consideras; necesitas una diferencia de salario de al menos " + EM.eur(r.dsalMin) + " al año y esperas " + EM.eur(d.dsal) + ".";
  } else {
    v = "Con tus hipótesis, la privada no recupera su sobrecoste (" + EM.eur(r.sobrecoste) + ") en " + d.ntrab + (d.ntrab === 1 ? " año" : " años") + " de trabajo: necesitarías una diferencia de salario de al menos " + EM.eur(r.dsalMin) + " al año y esperas " + EM.eur(d.dsal) + ".";
  }
  cuando = hay ? (r.anosAmortizar >= 0 ? anosTxt(r.anosAmortizar) + " de trabajo" : "no se amortiza con esa diferencia de salario") : "sin sobrecoste";
  note = "<p><strong>Lectura:</strong> " + (hay ? "para que la privada compense en dinero en " + d.ntrab + (d.ntrab === 1 ? " año" : " años") + " de trabajo, la diferencia de salario anual entre las dos opciones debe ser de al menos <strong>" + EM.eur(r.dsalMin) + "</strong>; con " + EM.eur(d.dsal) + " al año el resultado neto es de " + EM.eur(r.van) + (d.tasa > 0 ? " (en valor actual, con descuento del " + EM.num(d.tasa, 1) + " %)" : " (sin descontar)") + "." : "como la privada no cuesta más, basta con que no te dé un salario menor para que no pierdas dinero.") + "</p>";
  note += "<p><strong>Esto no es una predicción:</strong> la diferencia de salario es una hipótesis que escribes tú, no un dato ni una promesa. El retorno real depende del sector, de la nota, de la red de contactos y del mercado de trabajo, y puede ser menor, mayor o nulo. Las matrículas son ejemplos declarados, no cifras oficiales: las públicas varían por comunidad autónoma, universidad, titulación y créditos (consulta tu universidad) y las privadas fijan su precio.</p>";
  note += "<p><strong>No incluido:</strong> lo que no se mide en dinero (vocación, calidad de la enseñanza, prácticas, ambiente, cercanía a casa), los ingresos que dejas de ganar mientras estudias, los impuestos, las becas que no sean de ese importe anual y los costes de vida que son iguales en las dos opciones. Calcula con tus datos y decide con más información que esta.</p>";
  EM.renderResult({
    winner: mej ? "privada" : "publica", verdict: v, tone: "info",
    bigNumber: hay ? r.dsalMin : r.van, bigLabel: hay ? "diferencia de salario mínima al año para amortizar la privada en " + d.ntrab + (d.ntrab === 1 ? " año" : " años") : "resultado neto de la privada frente a la pública", format: EM.eur,
    barsLabel: "Coste de estudiar en cada opción",
    bars: [{ label: "Pública (matrícula)", value: r.matPub, color: "b" }, { label: "Privada (matrícula + vida extra − ayudas)", value: Math.max(0, r.matPriv + r.extra), color: "a" }],
    cols: ["Pública", "Privada"],
    rows: [
      ["Matrícula total (" + d.anos + (d.anos === 1 ? " año)" : " años)"), EM.eur(r.matPub), EM.eur(r.matPriv)],
      ["Coste de vida adicional menos ayudas (total)", "—", EM.eur(r.extra)],
      { label: "Sobrecoste total de la privada", values: ["—", EM.eur(r.sobrecoste)], strong: true },
      ["Diferencia de salario mínima necesaria al año", "—", hay ? EM.eur(r.dsalMin) : "—"],
      ["Años de trabajo para amortizar el sobrecoste", "—", cuando]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
