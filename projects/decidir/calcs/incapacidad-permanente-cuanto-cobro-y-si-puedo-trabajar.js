// Incapacidad permanente: cuanto cobro y si puedo trabajar (2026). Parametros desde data/params.json -> incapacidad_permanente_2026 (fuentes y fechas alli).
// Grados: parcial (tanto alzado), total 55 % (75 % cualificada), absoluta 100 %, gran incapacidad 100 % + complemento. Cuantias en euros/mes (14 pagas); minimos en euros/ano.
var P = {"pctTotal": 55, "pctIncr": 20, "pctAbs": 100, "edadIncr": 55, "mensParcial": 24, "brMeses": 96, "brDiv": 112, "brMesesAcc": 24, "brDivAcc": 28, "pctBase": 50, "mesesBase": 180, "t1Meses": 49, "t1Pct": 0.21, "t2Meses": 209, "t2Pct": 0.19, "edadCorta": 65, "edadLargaMeses": 802, "umbralCot": 459, "carParcialDias": 1800, "carMenor": 31, "carDesdeMenor": 16, "carFracMenor": 3, "carDesdeMayor": 20, "carFracMayor": 4, "carMinAnos": 5, "jubMinAnos": 15, "granBase": 45, "granUlt": 30, "granMinPen": 45, "baseMin": 1424.4, "baseMax": 5101.2, "maxMes": 3359.6, "pagas": 14, "limIng": 9442, "minGran": 19660.2, "minAbs": 13106.8, "minT65": 13106.8, "minT60": 12262.6, "minTC": 9662.8, "sueloTC": 9580.2, "edad65": 65, "edad60": 60, "edadMinModelo": 18, "edadMaxModelo": 80};
function eordMeses(anos) { return anos * 12 >= P.umbralCot ? P.edadCorta * 12 : P.edadLargaMeses; }
function pctAnos(m) {
  if (m < P.mesesBase) return P.pctBase;
  var a = Math.min(m - P.mesesBase, P.t1Meses), b = Math.min(Math.max(m - P.mesesBase - P.t1Meses, 0), P.t2Meses);
  return Math.min(P.pctBase + a * P.t1Pct + b * P.t2Pct, 100);
}
function calcular(d) {
  var g = d.grado, o = d.origen, base = d.base, edad = d.edad, anos = d.anos, trab = d.trabajo !== "no", sal = d.salario;
  var comun = o !== "profesional", em = eordMeses(anos);
  if (comun && edad * 12 >= em) return { bloqueo: anos >= P.jubMinAnos ? 1 : 4 };
  if (o === "comun" && g !== "parcial") {
    var req = edad < P.carMenor ? (edad - P.carDesdeMenor) / P.carFracMenor : Math.max((edad - P.carDesdeMayor) / P.carFracMayor, P.carMinAnos);
    if (anos + 1e-9 < req) return { bloqueo: 2 };
  }
  if (o === "comun" && g === "parcial" && anos * 365 < P.carParcialDias) return { bloqueo: 2 };
  if ((g === "absoluta" || g === "gran") && trab && edad * 12 >= em) return { bloqueo: 3 };
  var resto = Math.max(em - edad * 12, 0), tot = Math.floor(anos * 12 + resto + 1e-9);
  var pa = o === "comun" ? pctAnos(tot) : 0, br;
  if (o === "comun") br = base * P.brMeses / P.brDiv * pa / 100;
  else if (o === "accidente") br = base * P.brMesesAcc / P.brDivAcc;
  else br = base;
  var r = { bloqueo: 0, br: br, pct_anos: pa, pen: 0, capado: 0, comp: 0, minimo: 0, topup: 0, pen_final: 0, cual: 0, tanto: 0, pagado: 0, total_mes: 0, exenta: 0, anual: 0, rest: resto, tot: tot };
  var ing = trab ? sal * 12 : 0;
  r.exenta = (g === "absoluta" || g === "gran") ? 1 : 0;
  if (g === "parcial") { r.tanto = P.mensParcial * base; r.total_mes = trab ? sal : 0; return r; }
  var pct = g === "total" ? P.pctTotal : P.pctAbs, pre = br * pct / 100, pen = Math.min(pre, P.maxMes), suelo = (g === "total" && o === "comun") ? P.sueloTC / P.pagas : 0;
  pen = Math.max(pen, suelo);
  r.capado = pre > P.maxMes + 1e-9 ? 1 : 0; r.pen = pen;
  if (g === "gran") r.comp = Math.max(P.granBase / 100 * P.baseMin + P.granUlt / 100 * Math.min(base, P.baseMax), P.granMinPen / 100 * pen);
  var ma;
  if (g === "gran") ma = P.minGran;
  else if (g === "absoluta") ma = P.minAbs;
  else ma = edad >= P.edad65 ? P.minT65 : (edad >= P.edad60 ? P.minT60 : (o === "comun" ? P.minTC : 0));
  var m = ma / P.pagas, pY = (pen + r.comp) * P.pagas;
  function compMin(ingr) { return ma ? Math.max(Math.min(ma - pY, P.limIng + ma - ingr - pY), 0) / P.pagas : 0; }
  var top = compMin(0);
  r.minimo = m; r.topup = top; r.suelo = suelo; r.pen_final = pen + top; r.anual = (pen + top + r.comp) * P.pagas;
  if (g === "total" && edad >= P.edadIncr) { var p75 = Math.max(Math.min(br * (P.pctTotal + P.pctIncr) / 100, P.maxMes), suelo), q75 = p75 * P.pagas; r.cual = p75 + (ma ? Math.max(Math.min(ma - q75, P.limIng + ma - q75), 0) / P.pagas : 0); }
  if (!trab) r.pagado = r.pen_final + r.comp;
  else if (g === "total") r.pagado = d.trabajo === "mismas" ? 0 : pen + compMin(ing);
  else if (g === "absoluta") r.pagado = 0;
  else r.pagado = r.comp;
  r.total_mes = r.pagado + (trab ? sal : 0);
  return r;
}
function eur(x) { return EM.eur(x, 2); }
var IDS = ["base", "edad", "anos", "salario"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.grado = document.getElementById("grado").value; d.origen = document.getElementById("origen").value; d.trabajo = document.getElementById("trabajo").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
var NOMBRE = { parcial: "parcial", total: "total", absoluta: "absoluta", gran: "gran incapacidad" };
var NO_MODELA = "<p><strong>No incluye:</strong> el cálculo detallado de la base reguladora con tus bases reales (actualización con el IPC, lagunas de cotización: si tienes meses sin cotizar, tu base real puede ser menor), la retención del IRPF en la total y la parcial, el recargo de prestaciones por falta de medidas de seguridad, las mejoras de convenio o de seguros, la revisión por mejoría o agravación, el derecho a la pensión sin estar en alta, la sustitución de la total por una indemnización a tanto alzado antes de los 60 años, los autónomos y otros regímenes especiales (aplican en lo esencial las mismas reglas, art. 318 de la LGSS, con sus propias bases), los regímenes forales (País Vasco y Navarra siguen la misma Seguridad Social, pero tienen su propio IRPF), los mutualistas, la pensión no contributiva y Clases Pasivas. La calificación del grado la hace el INSS: aquí eliges tú el grado para ver cuánto supondría.</p>";
function pintar() {
  var d = leer();
  if (d.base <= 0 || d.anos < 0 || d.salario < 0) { aviso("Revisa los datos: la base debe ser mayor que 0 y los años cotizados y el salario no pueden ser negativos."); return; }
  if (d.edad < P.edadMinModelo || d.edad > P.edadMaxModelo) { aviso("Revisa la edad: indica tus años cumplidos (entre " + P.edadMinModelo + " y " + P.edadMaxModelo + ")."); return; }
  if (d.trabajo !== "no" && d.salario <= 0) { aviso("Has indicado que trabajas: escribe también cuánto cobras al mes (bruto) para calcular la compatibilidad."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Con tu edad y tus años cotizados ya tienes la edad ordinaria de jubilación y has cotizado 15 años o más: la Seguridad Social no reconoce una incapacidad permanente por enfermedad común o accidente no laboral en ese caso (art. 195.1 de la LGSS). Lo que correspondería es la pensión de jubilación; la incapacidad por accidente de trabajo o enfermedad profesional sí se puede reconocer. Mira la calculadora de jubilación."); return; }
  if (r.bloqueo === 2) { aviso("Con tus años cotizados no llegas al período mínimo que exige la enfermedad común para esta incapacidad (art. 195 de la LGSS): para la parcial, 1.800 días; para el resto, un tercio del tiempo desde los 16 años si tienes menos de 31, o un cuarto desde los 20 con un mínimo de 5 años. Si la causa es un accidente (laboral o no) o una enfermedad profesional, no se pide cotización previa: elige ese origen. Con estos datos no se calcula pensión."); return; }
  if (r.bloqueo === 3) { aviso("Si cobras una incapacidad absoluta o una gran incapacidad y has llegado a la edad de jubilación, trabajar con alta en la Seguridad Social se rige por las reglas de la jubilación activa (art. 198.3 de la LGSS, remite al art. 213.1). Esa combinación no se calcula aquí: mira la calculadora de jubilación activa."); return; }
  if (r.bloqueo === 4) { aviso("Con la edad ordinaria cumplida y menos de 15 años cotizados, la pensión de incapacidad se calcula con una regla especial (art. 196.5 de la LGSS) que esta herramienta no modela. Consulta tu caso en el INSS."); return; }
  var g = d.grado, ng = NOMBRE[g], verdict, bigNumber, bigLabel, note = "", comparaMin = "";
  var pctG = g === "total" ? P.pctTotal : P.pctAbs;
  if (g === "parcial") {
    verdict = "Con tus datos, una incapacidad permanente parcial no da pensión mensual: es un pago único de unos " + eur(r.tanto) + " brutos (" + P.mensParcial + " mensualidades de tu base), que tributa en el IRPF como rendimiento del trabajo. Eso solo ocurre si el INSS reconoce una pérdida de rendimiento de al menos el 33 % en tu profesión habitual sin impedirte sus tareas fundamentales.";
    bigNumber = r.tanto; bigLabel = "pago único bruto";
  } else {
    var base_txt = g === "gran" ? " más un complemento de " + eur(r.comp) + " para pagar a quien te atiende, en total " + eur(r.pen_final + r.comp) : "";
    verdict = "Con tus datos, " + (g === "gran" ? "una gran incapacidad" : "una incapacidad permanente " + ng) + " daría unos " + eur(r.pen_final) + " brutos al mes en 14 pagas (" + eur(r.pen_final * P.pagas) + " al año)" + base_txt + ", " + (r.exenta ? "exentos de IRPF." : "que tributan en el IRPF como rendimiento del trabajo.");
    bigNumber = r.pen_final + r.comp; bigLabel = "al mes en 14 pagas (bruto)";
  }
  var trab = d.trabajo !== "no";
  if (trab) {
    if (g === "parcial") verdict += " Es un pago único: no se descuenta de tu sueldo.";
    else if (g === "total" && d.trabajo === "distintas") verdict += " Como tu trabajo es de funciones distintas, puedes seguir cobrando la pensión y el sueldo: unos " + eur(r.total_mes) + " al mes entre los dos.";
    else if (g === "total") verdict += " Pero con las mismas funciones el trabajo no es compatible con la pensión (art. 198.1): no la cobrarías mientras lo hagas.";
    else if (g === "absoluta") verdict += " Pero trabajar con alta en la Seguridad Social hace que el INSS te suspenda la pensión (art. 198.2): solo cobrarías el sueldo, unos " + eur(r.total_mes) + " al mes.";
    else verdict += " Si trabajas con alta, el INSS suspende la pensión pero mantiene el complemento: cobrarías " + eur(r.comp) + " de complemento más el sueldo, unos " + eur(r.total_mes) + " al mes.";
  }
  if (g === "parcial") {
    note += "<p><strong>Cómo sale:</strong> " + P.mensParcial + " mensualidades × " + eur(d.base) + " = " + eur(r.tanto) + ". La ley usa la base reguladora de la incapacidad temporal de la que deriva; aquí usamos la base que has escrito.</p>";
  } else {
    var orig = d.origen === "comun" ? "la media de tus bases (" + eur(d.base) + ") × " + P.brMeses + " / " + P.brDiv + " × " + EM.num(r.pct_anos, 2) + " % por años cotizados (con " + EM.num(r.tot / 12, 1) + " años contando los que faltan hasta la edad ordinaria)" : (d.origen === "accidente" ? eur(d.base) + " × " + P.brMesesAcc + " / " + P.brDivAcc : "la base reguladora que has escrito (" + eur(d.base) + ")");
    note += "<p><strong>Cómo sale:</strong> base reguladora = " + orig + " = " + eur(r.br) + " al mes. Pensión = " + pctG + " % de la base reguladora = " + eur(r.br * pctG / 100) + " al mes" + (r.capado ? "; el límite de " + eur(P.maxMes) + " al mes para la pensión inicial la reduce a " + eur(r.pen) : "") + ".</p>";
    if (g === "gran") note += "<p><strong>Complemento de gran incapacidad:</strong> " + P.granBase + " % de la base mínima de cotización (" + eur(P.baseMin) + ") más " + P.granUlt + " % de tu última base (" + eur(Math.min(d.base, P.baseMax)) + "), con un mínimo del " + P.granMinPen + " % de la pensión sin complemento: " + eur(r.comp) + " al mes. No se suspende si trabajas.</p>";
    if (r.topup > 0.005) note += "<p><strong>Mínimo:</strong> tu pensión queda por debajo del mínimo de tu situación (" + eur(r.minimo) + " al mes) y se completaría con " + eur(r.topup) + " al mes (complemento por mínimos): se reconoce la diferencia hasta el mínimo mientras la suma de tus otros ingresos y la pensión no supere " + eur(P.limIng) + " al año más el mínimo.</p>";
    else if (r.minimo > 0) note += "<p><strong>Mínimo:</strong> tu pensión supera el mínimo de tu situación (" + eur(r.minimo) + " al mes), así que no hay complemento por mínimos.</p>";
    else note += "<p><strong>Mínimo:</strong> para tu edad y origen la tabla de mínimos de 2026 no fija una pensión mínima.</p>";
    if (g === "total" && d.edad >= P.edadIncr) note += "<p><strong>Incremento del " + P.pctIncr + " %:</strong> a partir de los " + P.edadIncr + " años, si el INSS considera que te será difícil encontrar otro empleo por tu edad, falta de preparación o circunstancias del lugar donde vives, la total sube al " + (P.pctTotal + P.pctIncr) + " % de la base reguladora: " + eur(r.cual) + " al mes. Ese incremento queda en suspenso mientras trabajes (Decreto 1646/1972, art. 6).</p>";
    if (g === "total" && trab && d.trabajo === "distintas" && r.topup > 0.005 && r.pagado - r.pen < r.topup - 0.005) note += "<p>Con ese sueldo el complemento por mínimos baja de " + eur(r.topup) + " a " + eur(Math.max(r.pagado - r.pen, 0)) + " al mes.</p>";
    if (r.suelo > 0.005 && r.suelo > r.br * pctG / 100) note += "<p><strong>Suelo de la total por enfermedad común:</strong> la pensión no puede ser inferior a " + eur(r.suelo) + " al mes (9.580,20 € al año; art. 196.2 de la LGSS), con cualquier sueldo.</p>";
  }
  if (!trab && g !== "parcial") note += "<p><strong>Trabajar:</strong> " + (g === "total" ? "la total es compatible con un sueldo si las funciones son distintas a las de tu profesión habitual (art. 198.1); con las mismas funciones no. " : (g === "absoluta" ? "la absoluta no impide actividades compatibles con tu estado, pero un trabajo que dé alta en la Seguridad Social suspende la pensión (art. 198.2). " : "en la gran incapacidad, un trabajo con alta suspende la pensión pero no el complemento (art. 198.2). ")) + "Cámbialo en «Trabajo» para ver el efecto.</p>";
  note += NO_MODELA;
  var rows = [], grados = ["parcial", "total", "absoluta", "gran"];
  grados.forEach(function (x) {
    var dd = {}; for (var k in d) dd[k] = d[k]; dd.grado = x; dd.trabajo = "no"; dd.salario = 0;
    var q = calcular(dd);
    if (q.bloqueo) { rows.push([NOMBRE[x], "no calculable con tus datos", "—", "—"]); return; }
    if (x === "parcial") rows.push([NOMBRE[x], "pago único de " + eur(q.tanto), "—", "sí"]);
    else rows.push([NOMBRE[x], eur(q.pen_final + q.comp) + " al mes (" + eur(q.anual) + " al año)", eur(q.minimo || 0), q.exenta ? "no, exenta" : "sí"]);
  });
  var bars = g === "parcial" ? [] : [{ label: "Tu pensión", value: r.pen_final + r.comp, color: "a" }, { label: "Mínimo de tu situación", value: r.minimo, color: "b" }, { label: "Máximo de la pensión inicial", value: P.maxMes, color: "b" }];
  var res = {
    winner: g, verdict: verdict, tone: "info",
    bigNumber: bigNumber, bigLabel: bigLabel, format: eur,
    cols: ["Grado", "Importe bruto", "Mínimo mensual", "Tributa en el IRPF"], rows: rows,
    note: note
  };
  if (bars.length) { res.barsLabel = "Pensión mensual bruta (14 pagas)"; res.bars = bars; }
  EM.renderResult(res);
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
