// Donativos y IRPF 2026. Parametros: data/params.json -> donativos_2026 (Ley 49/2002 art. 19; Ley 35/2006 art. 69.1; fuentes y fechas alli).
var P = {"tramo": 250, "p1": 80, "p2": 40, "p2r": 45, "lim": 10};
function deducir(x, rec, lim) {
  var base = Math.min(Math.max(x, 0), lim), a = Math.min(base, P.tramo), r = Math.max(0, base - P.tramo);
  return a * P.p1 / 100 + r * (rec ? P.p2r : P.p2) / 100;
}
function calcular(d) {
  var don = Math.max(+d.donado || 0, 0), adi = Math.max(+d.adicional || 0, 0), bl = Math.max(+d.bl || 0, 0), rec = +d.recurrente === 1;
  if (d.ambito !== "comun" && d.ambito !== "ceutamelilla") return { invalido: 1, ambito: d.ambito, limite: 0, baseDeduccion: 0, exceso: 0, deduccion: 0, costeNeto: 0, importeTramo80: 0, deduccionTotal: 0, deduccionAdicional: 0, costeNetoAdicional: 0, costeEuroResto: 0, pctEfectivo: 0, avisoBase: 0 };
  var lim = bl * P.lim / 100, ded = deducir(don, rec, lim), tot = deducir(don + adi, rec, lim), pr = rec ? P.p2r : P.p2;
  return {
    invalido: 0, limite: lim, baseDeduccion: Math.min(don, lim), exceso: Math.max(don - lim, 0),
    deduccion: ded, costeNeto: don - ded, importeTramo80: Math.min(P.tramo, lim), pctEfectivo: don > 0 ? ded / don * 100 : 0,
    costeEuroResto: 1 - pr / 100, deduccionTotal: tot, deduccionAdicional: tot - ded, costeNetoAdicional: adi - (tot - ded),
    hayTramoResto: lim > P.tramo ? 1 : 0, avisoBase: bl < 5550 ? 2 : (bl < 15000 ? 1 : 0)
  };
}
function eur(x) { return EM.eur(x); }
function e(x) { return Math.abs(x - Math.round(x)) < 0.005 ? EM.eur(x) : EM.eur(x, 2); }
function leer() {
  var d = {}; ["donado", "bl", "adicional", "recurrente"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ambito = document.getElementById("ambito").value;
  return d;
}
function pintar() {
  var d = leer(), r = calcular(d);
  if (d.donado < 0 || d.bl < 0 || d.adicional < 0) return;
  var avisoCm = d.ambito === "ceutamelilla" ? '<p><strong>Ceuta y Melilla:</strong> la deducción por donativos es la misma que en el resto de España; el 60 % de la cuota del art. 68.4 de la Ley del IRPF reduce la cuota sobre la que se aplica, así que el límite por cuota puede cortar antes. Revisa tu cuota.</p>' : '';
  var aviso = avisoCm + '<p><strong>Comunidad autónoma:</strong> varias comunidades tienen deducciones propias por donativos que se suman a la estatal y no están en este cálculo; consulta la tuya en el Manual práctico de Renta de la Agencia Tributaria.</p>';
  if (r.invalido) {
    EM.renderResult({ winner: "invalido", verdict: "Esta calculadora no cubre tu territorio: haciendas forales.", tone: "warn",
      note: "<p>El País Vasco y Navarra tienen su propio régimen foral de donativos, con porcentajes y límites distintos de la Ley 49/2002 estatal. Consulta la normativa de tu administración tributaria.</p>" });
    return;
  }
  if (d.donado <= 0) {
    EM.renderResult({ winner: "nada", verdict: "Escribe el importe que has donado o piensas donar este año para ver cuánto desgrava.", tone: "info", note: aviso });
    return;
  }
  var pr = Math.round(r.costeEuroResto * 100) / 100;
  var verdict, tone = "ok", partes = [];
  if (r.limite <= 0) {
    verdict = "Con una base liquidable de 0 € no puedes deducir nada por donar: el límite del 10 % de la base liquidable es 0 €.";
    tone = "warn";
  } else {
    verdict = "Donar " + e(d.donado) + " te desgrava " + (r.avisoBase === 2 ? "como máximo " : "") + e(r.deduccion) + " en la cuota del IRPF 2026, pero te cuesta " + (r.avisoBase === 2 ? "como mínimo " : "") + e(r.costeNeto) + " netos: desgrava, no es un negocio.";
    if (r.avisoBase === 2) { verdict += " Atención: con esa base liquidable tu cuota íntegra probablemente es 0 € (mínimo personal de 5.550 €, art. 57 de la Ley del IRPF) y la deducción solo se aplica hasta tu cuota: es probable que no te desgrave nada; comprueba las casillas 0545 y 0546."; tone = "warn"; }
    if (r.exceso > 0) { verdict += " Pasas el límite del 10 % de tu base liquidable (" + e(r.limite) + "): " + e(r.exceso) + " no desgravan."; tone = "warn"; }
  }
  var warnBase = r.avisoBase >= 1 && r.limite > 0 ? '<p><strong>Ojo con tu cuota:</strong> con una base liquidable menor de 15.000 € la cuota íntegra puede ser pequeña (con menos de 5.550 € es 0 € por el mínimo personal, art. 57 de la Ley del IRPF) y la deducción no puede pasar de ella: comprueba las casillas 0545 y 0546 de tu renta.</p>' : '';
  var note = warnBase + (r.limite <= 0 ? '<p><strong>Cuánto donar:</strong> con base liquidable 0 € el límite es 0 €, así que ninguna cantidad desgrava este año; si tu base liquidable es mayor, el tope es el 10 %.</p>' : '<p><strong>Cuánto donar:</strong> el tramo del ' + P.p1 + ' % cubre solo los primeros ' + e(P.tramo) + (r.limite < P.tramo ? ', y con tu base liquidable el límite del 10 % lo reduce a ' + e(r.importeTramo80) : '') + ': ahí cada euro donado te cuesta ' + e(1 - P.p1 / 100) + ' netos. ');
  if (r.limite > P.tramo) note += 'Por encima de ' + e(P.tramo) + ' desgrava el ' + (+d.recurrente === 1 ? P.p2r : P.p2) + ' %, es decir, cada euro más te cuesta ' + e(pr) + ' netos. ';
  if (r.limite > 0) note += 'Hasta ' + e(r.limite) + ' (10 % de tu base liquidable) se deduce; por encima de ese tope cada euro cuesta el euro entero, y en el IRPF la norma no prevé arrastrar el exceso a otros años. ';
  if (r.limite > 0) note += 'Con la deducción estatal, cualquier importe te cuesta dinero: donar es una decisión solidaria, no un ahorro fiscal (alguna deducción autonómica, p. ej. la valenciana del 20 % de los primeros 250 €, puede dejar ese tramo a coste 0, nunca en ganancia).</p>';
  if (d.adicional > 0 && r.limite > 0) note += r.deduccionAdicional < 0.005 ? '<p><strong>Si donas además ' + e(d.adicional) + ':</strong> esa cantidad extra no desgrava nada: ya estás en el tope del 10 %, así que te cuesta ' + e(d.adicional) + ' enteros.</p>' : '<p><strong>Si donas además ' + e(d.adicional) + ':</strong> la deducción sube de ' + e(r.deduccion) + ' a ' + e(r.deduccionTotal) + ' (' + e(r.deduccionAdicional) + ' más) y esa parte extra te cuesta ' + e(r.costeNetoAdicional) + ' netos.</p>';
  note += '<p><strong>Requisitos:</strong> el donativo debe ser irrevocable y a una entidad acogida a la Ley 49/2002, y la entidad debe darte un certificado (con tu NIF, fecha e importe); sin certificado no hay deducción. Se dona antes del 31 de diciembre para aplicarlo en este ejercicio. </p><p><strong>Importante: esta calculadora no limita la deducción por tu cuota.</strong> La deducción se resta de la cuota íntegra (estatal y autonómica a partes iguales) y no puede dejarla por debajo de 0 €: si tu cuota es baja, la deducción real es menor que la que ves aquí.</p>' + aviso;
  EM.renderResult({
    winner: r.limite <= 0 ? "nada" : (r.exceso > 0 ? "limite" : "desgrava"), verdict: verdict, tone: tone,
    bigNumber: r.deduccion, bigLabel: "de deducción en la cuota", format: EM.eur,
    barsLabel: "Lo que donas y lo que te cuesta de verdad",
    bars: [{ label: "Donado", value: d.donado, color: "a" }, { label: "Deducción", value: r.deduccion, color: "b" }, { label: "Coste neto", value: r.costeNeto, color: "a" }],
    cols: ["Importe"],
    rows: [
      ["Donado este año", e(d.donado)],
      ["Tope de base deducible (10 % de la base liquidable)", e(r.limite)],
      ["Base que desgrava", e(r.baseDeduccion)],
      ["Parte que no desgrava", e(r.exceso)],
      ["Deducción en la cuota", e(r.deduccion)],
      { label: "Coste neto de donar", values: [e(r.costeNeto)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
