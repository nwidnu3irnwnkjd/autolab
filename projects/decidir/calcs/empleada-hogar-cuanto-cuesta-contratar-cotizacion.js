// Empleada de hogar: coste real de contratar (2026). Parámetros desde data/params.json -> empleada_hogar_2026 (fuentes y fechas allí) y smi_2026 (SMI anual).
// Base = retribución mensual con prorrata de pagas -> escala de 8 tramos (Orden PJC/297/2026 art. 15); tipos del empleador con la reducción del 20 % (o 45 % de familia numerosa cuidadora) y la bonificación del 80 % de desempleo y Fogasa (RDL 16/2022 DA 1.ª).
var P = {"tramos": [[329.0, 306.0], [510.0, 436.0], [693.0, 602.0], [877.0, 785.0], [1061.0, 970.0], [1242.0, 1151.0], [1424.4, 1424.4]], "baseMax": 5101.2, "ccE": 23.6, "ccT": 4.7, "meiE": 0.75, "meiT": 0.15, "atep": 1.5, "desInd": [5.5, 1.55], "desTemp": [6.7, 1.6], "fog": 0.2, "red": 20, "famNum": 45, "bonDes": 80, "smiHora": 9.55, "jornada": 40, "semanas": 52, "smiAnual": 17094, "pagas": 14};
function redondea(x) { return Math.round(x * 100) / 100; }
function tramoDe(ret) {
  var i, r = redondea(ret);
  for (i = 0; i < P.tramos.length; i++) if (r <= P.tramos[i][0]) return { n: i + 1, base: P.tramos[i][1] };
  return { n: P.tramos.length + 1, base: Math.min(r, P.baseMax) };
}
function calcular(d) {
  var h = d.horas, imp = d.importe, meses = Math.round(d.meses);
  if (!(h > 0) || h > P.jornada) return { bloqueo: 1 };
  if (!(imp > 0)) return { bloqueo: 2 };
  if (!(meses >= 1) || meses > 12) return { bloqueo: 3 };
  var hm = h * P.semanas / 12, porHoras = d.modo === "horas", ret, minMes, minHora, cumple;
  if (porHoras) { ret = imp * hm; minHora = P.smiHora; minMes = minHora * hm; cumple = redondea(imp) >= P.smiHora; }
  else { ret = imp * (d.pagas === "14" ? P.pagas / 12 : 1); minMes = P.smiAnual / 12 * h / P.jornada; minHora = minMes / hm; cumple = redondea(ret) >= redondea(minMes); }
  var t = tramoDe(ret), b = Math.max(t.base, tramoDe(minMes).base), fam = d.fam === "si", des = d.tipo === "temporal" ? P.desTemp : P.desInd;
  var cc = b * P.ccE / 100, rcc = cc * (fam ? P.famNum : P.red) / 100, mei = b * P.meiE / 100, atep = b * P.atep / 100;
  var desE = b * des[0] / 100, fog = b * P.fog / 100, bdes = (desE + fog) * P.bonDes / 100;
  var emp = cc - rcc + mei + atep + desE + fog - bdes, sin = cc + mei + atep + desE + fog;
  var trab = b * (P.ccT + P.meiT + des[1]) / 100;
  var r = { bloqueo: 0, retMes: ret, base: b, tramo: t.n, cuotaEmp: emp, cuotaSin: sin, ahorroMes: sin - emp, cuotaTrab: trab, costeMes: ret + emp, costeTotal: (ret + emp) * meses,
    netoMes: ret - trab, minMes: minMes, minHora: minHora, cumple: cumple ? 1 : 0, horasMes: hm, costeHora: (ret + emp) / hm, difMin: ret - minMes, pctEmp: emp / b * 100, meses: meses, rcc: rcc, cc: cc, bdes: bdes, porHoras: porHoras ? 1 : 0, baseMinima: b > t.base ? 1 : 0 };
  if (t.n <= P.tramos.length - 1 && b === t.base) {
    var nb = P.tramos[t.n][1], k = (P.ccE * (1 - (fam ? P.famNum : P.red) / 100) + P.meiE + P.atep + (des[0] + P.fog) * (1 - P.bonDes / 100)) / 100;
    r.limite = P.tramos[t.n - 1][0]; r.baseSig = nb; r.saltoEmp = (nb - b) * k; r.saltoTrab = (nb - b) * (P.ccT + P.meiT + des[1]) / 100;
  }
  return r;
}
function eur(x) { return EM.eur(x, Math.abs(x - Math.round(x)) > 0.004 ? 2 : 0); }
function e0(x) { return EM.eur(x, 0); }
var IDS = ["horas", "importe", "meses"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.modo = document.getElementById("modo").value; d.pagas = document.getElementById("pagas").value; d.fam = document.getElementById("fam").value; d.tipo = document.getElementById("tipo").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function pintar() {
  var d = leer(), r = calcular(d);
  if (r.bloqueo === 1) { aviso("Indica entre 1 y " + P.jornada + " horas a la semana: " + P.jornada + " es la jornada ordinaria máxima (art. 9.1 del RD 1620/2011). Las horas de presencia y las extra se pactan aparte y esta herramienta no las modela."); return; }
  if (r.bloqueo === 2) { aviso("Indica una retribución mayor que cero: euros por hora si pagas por horas, o euros brutos al mes si pagas un sueldo mensual."); return; }
  if (r.bloqueo === 3) { aviso("Indica entre 1 y 12 meses de contrato: la herramienta calcula como máximo un año."); return; }
  var hora = r.porHoras === 1, fam = d.fam === "si", temp = d.tipo === "temporal";
  var minTxt = hora ? eur(P.smiHora) + " por hora trabajada, con todos los conceptos incluidos (art. 4.2 del RD 126/2026)" : eur(r.minMes) + " al mes con las pagas extra prorrateadas (el SMI de " + e0(P.smiAnual) + " al año, proporcional a tus " + EM.num(d.horas, 1) + " horas semanales)";
  var min = r.cumple === 1 ? "cumples el mínimo legal: " + minTxt : "no llegas al mínimo legal: " + minTxt + (hora ? "; te faltan " + eur(P.smiHora - d.importe) + " por hora, unos " + e0(r.minMes - r.retMes) + " al mes" : "; te faltan " + e0(r.minMes - r.retMes) + " al mes");
  var verdict = "Con tus datos, contratarla te cuesta " + eur(r.costeMes) + " al mes (sueldo bruto " + eur(r.retMes) + " más " + eur(r.cuotaEmp) + " de Seguridad Social a tu cargo), unos " + e0(r.costeTotal) + " en " + r.meses + (r.meses === 1 ? " mes" : " meses") + " de contrato, y " + min + ".";
  var ayuda = fam ? "la bonificación del " + P.famNum + " % de las cuotas de contingencias comunes por cuidadora de familia numerosa, en lugar de la reducción del " + P.red + " %" : "la reducción del " + P.red + " % en las contingencias comunes";
  var note = "<p><strong>Cómo sale:</strong> la retribución mensual (" + e0(r.retMes) + (hora ? ": " + eur(d.importe) + " por hora x " + EM.num(r.horasMes, 1) + " horas al mes" : (d.pagas === "14" ? ", con dos pagas extra prorrateadas" : "")) + ") cae en el tramo " + r.tramo + " de la escala de 2026, con base de cotización de " + eur(r.base) + (r.tramo > P.tramos.length ? " (la retribución real, hasta el tope)" : "") + (r.baseMinima === 1 ? ", elevada hasta la base mínima que corresponde al salario mínimo legal de tus horas (Orden PJC/297/2026, art. 15.2)" : "") + ". A la familia le suponen " + eur(r.cuotaEmp) + " al mes tras aplicar " + ayuda + " y la bonificación del " + P.bonDes + " % de desempleo y Fogasa; sin ayudas serían " + eur(r.cuotaSin) + " (te ahorras " + eur(r.ahorroMes) + " al mes). Contrato " + (temp ? "temporal" : "indefinido") + ".</p>";
  note += "<p><strong>Lo que paga ella:</strong> " + eur(r.cuotaTrab) + " al mes de cuota de la empleada, que tú descuentas de su sueldo al ingresar la cuota completa: cobra " + eur(r.netoMes) + " al mes antes del IRPF. Cada hora trabajada te cuesta " + eur(r.costeHora) + " con la Seguridad Social.</p>";
  if (r.limite) note += "<p><strong>Ojo al tramo:</strong> si la retribución supera " + eur(r.limite) + " al mes, la base sube a " + eur(r.baseSig) + " y la cuota que pagas sube " + eur(r.saltoEmp) + " al mes (y la de ella, " + eur(r.saltoTrab) + ").</p>";
  if (d.modo === "horas" && d.pagas === "14") note += "<p>Por horas el precio incluye ya las pagas y las vacaciones (art. 8.5 del RD 1620/2011): la opción de pagas no se aplica.</p>";
  note += "<p><strong>No incluye:</strong> el IRPF de la empleada, las horas de presencia y las extra, el alojamiento y la manutención, los convenios o pactos que mejoren el mínimo, la indemnización al terminar el contrato, las bajas (el empleador paga los días 4 a 8 de una baja por enfermedad común, art. 251 de la LGSS), la deducción por familia numerosa, las comunidades forales (País Vasco y Navarra), el alta del empleador y el reparto de bases entre varios empleadores (la calculadora calcula el coste de cada familia por separado). La bonificación de familia numerosa solo cubre a una persona dedicada exclusivamente a cuidar, y se calcula sobre contingencias comunes (supuesto propio). Información orientativa.</p>";
  var bars = [{ label: "Sueldo bruto", value: r.retMes, color: "a" }, { label: "Seguridad Social a tu cargo", value: r.cuotaEmp, color: "b" }];
  EM.renderResult({
    winner: r.cumple === 1 ? "cumple" : "nocumple", verdict: verdict, tone: r.cumple === 1 ? "ok" : "warn",
    bigNumber: r.costeMes, bigLabel: "al mes a la familia, con Seguridad Social", format: eur,
    barsLabel: "Dónde va el coste mensual", bars: bars, cols: ["Al mes", "En " + r.meses + (r.meses === 1 ? " mes" : " meses")],
    rows: [
      ["Sueldo bruto", eur(r.retMes), eur(r.retMes * r.meses)],
      ["Seguridad Social a tu cargo", eur(r.cuotaEmp), eur(r.cuotaEmp * r.meses)],
      ["Cuota de la empleada (sale de su sueldo)", eur(r.cuotaTrab), eur(r.cuotaTrab * r.meses)],
      { label: "Coste total para la familia: " + eur(r.costeMes) + " al mes", values: [eur(r.costeMes), eur(r.costeTotal)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
