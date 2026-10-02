// Aceptar un trabajo cobrando paro o subsidio (2026). Parámetros desde data/params.json -> aceptar_trabajo_paro_2026 (fuentes y fechas allí).
// Paro (art. 282.2 LGSS): a tiempo parcial y pidiéndolo se descuenta la parte proporcional de la jornada; trabajo de menos de 12 meses sin compatibilidad: suspensión sin consumir meses (art. 271); con 12 o más, extinción (art. 272.1.c).
// Subsidio (art. 282.3): complemento de apoyo al empleo (CAE) = % del IPREM por trimestre del subsidio y jornada, hasta 180 días que se descuentan del subsidio.
var P = {"iprem": 600, "cae": [[80, 75, 70, 60], [60, 50, 45, 40], [40, 35, 30, 25], [30, 25, 20, 15], [20, 15, 10, 5]], "cae75": 75, "cae50": 50, "caeDias": 180, "mesesExt": 12, "paroDias": 720, "diasMes": 30, "trim": 3, "plazo": 15, "da59Mes": 10, "da59Mas": 12};
function colJ(j) { return j >= 100 ? 0 : j >= P.cae75 ? 1 : j >= P.cae50 ? 2 : 3; }
function calcular(d) {
  var j = Math.round(d.jornada), M = Math.round(d.meses), H = Math.round(d.duracion), s = Math.max(Math.round(d.inicio), 1), k, q;
  var paro = d.tipo === "paro", t = d.irpf / 100, jj = j / 100;
  if (d.tipo === "subsidio59") return { bloqueo: 6 };
  if (M < 1) return { bloqueo: 1 };
  if (H < 1) return { bloqueo: 2 };
  if (j < 1 || j > 100) return { bloqueo: 3 };
  if (paro && M > P.paroDias / P.diasMes) return { bloqueo: 4 };
  var cn = d.cuantia * (1 - t), nw = Math.min(H, M);
  if (paro && s - 1 + M > P.da59Mas && s + nw - 1 >= P.da59Mes) return { bloqueo: 5 };
  var r = { bloqueo: 0, cn: cn, H: H, M: M, nw: nw, totalA: cn * nw, restA: M - nw, ext: H >= P.mesesExt ? 1 : 0, nCae: 0, caeBruto: 0, cae1: 0, riesgo12: 0 };
  if (paro) {
    r.bOk = j < 100 ? 1 : 0; r.cOk = 1;
    r.mensualB = d.sueldo + cn * (1 - jj);
    r.totalB = r.bOk ? nw * r.mensualB + (H - nw) * d.sueldo : 0;
    r.restB = r.bOk ? M - nw : 0;
    r.totalC = d.sueldo * H; r.restC = r.ext ? 0 : M;
    r.umbralB = r.bOk ? cn * nw * jj / H : 0;
  } else {
    r.bOk = 1; r.cOk = 0;
    var n = Math.min(H, P.caeDias / P.diasMes, M), tot = 0;
    for (k = 0; k < n; k++) {
      q = Math.min(Math.ceil((s + k) / P.trim), P.cae.length);
      tot += P.iprem * P.cae[q - 1][colJ(j)] / 100;
      if (k === 0) r.cae1 = P.iprem * P.cae[q - 1][colJ(j)] / 100;
    }
    r.nCae = n; r.caeBruto = tot;
    r.mensualB = d.sueldo + r.cae1 * (1 - t);
    r.totalB = n * d.sueldo + tot * (1 - t) + (H - n) * d.sueldo;
    r.restB = M - n; r.totalC = 0; r.restC = 0;
    r.umbralB = Math.max((r.totalA - tot * (1 - t)) / H, 0);
    r.riesgo12 = H >= P.mesesExt ? 1 : 0;
  }
  r.umbralC = r.cOk ? r.totalA / H : 0;
  r.gananciaB = r.bOk ? r.totalB - r.totalA : 0;
  r.gananciaC = r.cOk ? r.totalC - r.totalA : 0;
  var o = [[1, r.totalA]];
  if (r.bOk) o.push([2, r.totalB]);
  if (r.cOk) o.push([3, r.totalC]);
  o.sort(function (a, b) { return (b[1] - a[1]) || (b[0] - a[0]); });
  r.winner = o[0][0]; r.second = o[1][0]; r.margen = o[0][1] - o[1][1];
  r.empate = r.margen < 0.05 * Math.abs(o[0][1]) ? 1 : 0;
  return r;
}
function eur(x) { return EM.eur(x, Math.abs(x - Math.round(x)) > 0.004 ? 2 : 0); }
function txtMeses(n) { return EM.num(n, 0) + (n === 1 ? " mes" : " meses"); }
var IDS = ["cuantia", "sueldo", "jornada", "meses", "duracion", "irpf", "inicio"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.tipo = document.getElementById("tipo").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function nombre(r, paro, c, jor) {
  if (c === 1) return paro ? "seguir cobrando solo el paro" : "seguir cobrando solo el subsidio";
  if (c === 2) return paro ? "trabajar a tiempo parcial y compatibilizar el paro" : "trabajar y cobrar el complemento de apoyo al empleo";
  return r.ext ? "aceptar el trabajo y perder el paro que te queda" : (jor >= 100 ? "trabajar a tiempo completo y suspender el paro" : "trabajar y suspender el paro sin pedir la compatibilidad");
}
function pintar() {
  var d = leer(), paro = d.tipo === "paro", tp = paro ? "paro" : "subsidio";
  if (d.cuantia < 0 || d.sueldo < 0 || d.meses < 0 || d.duracion < 0 || d.inicio < 0) { aviso("Revisa los datos: los importes y los meses no pueden ser negativos."); return; }
  if (d.irpf < 0 || d.irpf >= 100) { aviso("Revisa el tipo de IRPF: indica un porcentaje entre 0 y 99."); return; }
  var r = calcular(d);
  if (r.bloqueo === 6) { aviso("Si tu subsidio viene de agotar un paro de más de " + P.da59Mas + " meses reconocido desde el 1 de abril de 2025, el complemento de apoyo al empleo se cuenta como continuación de ese paro (disposición adicional 59.ª, apartado 4, de la LGSS) y puede ser mucho menor que el de un subsidio nuevo (por ejemplo, 120 € en vez de 480 € a jornada completa con un paro de 24 meses). Esta calculadora no lo modela, así que no te da una cifra que podría ser hasta cuatro veces mayor que la real: consulta al SEPE."); return; }
  if (r.bloqueo === 1) { aviso("Para comparar necesitas tener paro o subsidio pendiente de cobrar: indica al menos 1 mes restante. Sin prestación pendiente no hay compatibilidad que calcular."); return; }
  if (r.bloqueo === 2) { aviso("Indica al menos 1 mes de duración del contrato."); return; }
  if (r.bloqueo === 3) { aviso("La jornada del trabajo tiene que estar entre el 1 % y el 100 % (100 % es jornada completa)."); return; }
  if (r.bloqueo === 4) { aviso("El paro dura como máximo " + txtMeses(P.paroDias / P.diasMes) + " (" + P.paroDias + " días, art. 269.1 de la LGSS): revisa los meses que te quedan. Si cobras el subsidio, elige «Subsidio»."); return; }
  if (r.bloqueo === 5) { aviso("Con un paro de más de " + P.da59Mas + " meses (los " + txtMeses(Math.round(d.inicio) - 1 + Math.round(d.meses)) + " que resultan de tus datos) cuyo trabajo llega al mes " + P.da59Mes + " de paro se aplica otro régimen (disposición adicional 59.ª de la LGSS: complemento de apoyo al empleo en el paro, también a jornada completa, con tabla por mes y duración máxima de 30 a 180 días) que esta calculadora no modela. Se aplica a los paros nacidos desde el 1 de abril de 2025 (en los anteriores, solo a jornada completa y a solicitud); desde el mes " + P.da59Mes + " también el trabajo a tiempo parcial pasa a cobrarse con ese complemento en vez de con la deducción proporcional, salvo que desistas. Revisa el mes de inicio y los meses que te quedan, o consulta al SEPE."); return; }
  var jor = Math.round(d.jornada), H = r.H, M = r.M, w = r.winner, sg = r.second;
  var V;
  if (r.empate) V = "Con tus datos, hay empate práctico entre " + nombre(r, paro, w, jor) + " y " + nombre(r, paro, sg, jor) + ": " + eur(r.margen) + " de diferencia neta en " + txtMeses(H) + ".";
  else V = "Con tus datos, gana " + nombre(r, paro, w, jor) + " por " + eur(r.margen) + " netos en " + txtMeses(H) + " frente a " + nombre(r, paro, sg, jor) + ".";
  if (paro) {
    if (!r.bOk) V += " Con jornada completa no hay compatibilidad con el paro (art. 282.2), salvo desde el mes " + P.da59Mes + " de un paro de más de " + P.da59Mas + " meses (DA 59.ª): solo puedes suspenderlo.";
    else V += " La compatibilidad no existe si el contrato es a jornada completa (salvo desde el mes " + P.da59Mes + " de un paro de más de " + P.da59Mas + " meses, DA 59.ª), y hay que pedirla en los " + P.plazo + " días hábiles siguientes al inicio (art. 282.2).";
    V += r.ext ? " Con un contrato de " + P.mesesExt + " meses o más el paro se extingue (art. 272.1.c) y perderías los " + txtMeses(M) + " que te quedan." : " Si suspendes el paro (contrato de menos de " + P.mesesExt + " meses) conservas los " + txtMeses(M) + " que te quedan; si compatibilizas o no aceptas, te quedan " + txtMeses(r.restA) + " al acabar el contrato.";
  } else {
    V += " El complemento no existe si te contrata una empresa con expediente de regulación de empleo, en la que trabajaste en los últimos " + P.mesesExt + " meses o un familiar tuyo (art. 282.3). Lo cobrarías " + txtMeses(r.nCae) + " (máximo " + P.caeDias + " días, que se descuentan del subsidio) y te quedarían " + txtMeses(r.restB) + " de subsidio";
    V += r.riesgo12 ? ", pero con un contrato de " + P.mesesExt + " meses o más no está claro que los conserves (el art. 272.1.c extingue y el 282.3 habla de suspensión): confírmalo con el SEPE." : ", que se reanudan si cumples otra vez los requisitos.";
  }
  if (w === 1) V += " Rechazar una oferta de empleo adecuada del servicio público de empleo o de una agencia de colocación es una infracción grave que puede costarte la " + tp + " (LISOS, arts. 25.4.a y 47.1.b): no aceptar solo sale gratis si la oferta no llega por ese cauce.";
  var cols = ["Solo " + tp], rowM = ["Ingreso neto al mes (primer mes)", eur(r.cn)], rowT = ["Total neto en " + txtMeses(H), eur(r.totalA)], rowG = ["Diferencia con solo " + tp, "—"], rowR = ["Meses de " + tp + " que te quedan después", EM.num(r.restA, 0)];
  var bars = [{ label: "Solo " + tp, value: r.totalA, color: "a" }];
  if (r.bOk) {
    cols.push(paro ? "Compatibilizas (jornada parcial)" : "Trabajas con complemento (CAE)");
    rowM.push(eur(r.mensualB)); rowT.push(eur(r.totalB)); rowG.push(eur(r.gananciaB)); rowR.push(EM.num(r.restB, 0));
    bars.push({ label: paro ? "Compatibilizas" : "Con CAE", value: r.totalB, color: "b" });
  }
  if (r.cOk) {
    cols.push(r.ext ? "Aceptas y pierdes el paro" : "Suspendes el paro");
    rowM.push(eur(d.sueldo)); rowT.push(eur(r.totalC)); rowG.push(eur(r.gananciaC)); rowR.push(EM.num(r.restC, 0));
    bars.push({ label: r.ext ? "Aceptas y pierdes el paro" : "Suspendes", value: r.totalC, color: "c" });
  }
  var note = "<p><strong>Cómo sale:</strong> pasamos tu " + tp + " de " + eur(d.cuantia) + " brutos a " + eur(r.cn) + " netos con tu tipo de IRPF (" + EM.num(d.irpf, 0) + " %); el sueldo de " + eur(d.sueldo) + " ya lo das neto. Comparamos los " + txtMeses(H) + " del contrato.";
  if (paro) {
    if (r.bOk) note += " Con " + EM.num(jor, 0) + " % de jornada te descuentan el " + EM.num(jor, 0) + " % del paro (art. 282.2): cobras " + eur(r.cn * (1 - jor / 100)) + " netos de paro más el sueldo, y el paro sigue consumiéndose mes a mes. Compatibilizar supera a seguir solo con el paro si tu sueldo neto pasa de " + eur(r.umbralB) + " al mes.";
    if (r.cOk) note += " Suspender el paro supera a seguir solo con el paro si tu sueldo neto pasa de " + eur(r.umbralC) + " al mes durante el contrato.";
  } else {
    note += " El complemento de apoyo al empleo es un % del IPREM (" + eur(P.iprem) + ") según el trimestre del subsidio en que empiezas y tu jornada: " + eur(r.cae1) + " brutos el primer mes, y baja cada trimestre. Trabajar con el complemento supera a seguir solo con el subsidio si tu sueldo neto pasa de " + eur(r.umbralB) + " al mes.";
  }
  note += "</p>";
  note += paro ? "<p><strong>Plazos:</strong> la compatibilidad se pide ante el SEPE en los " + P.plazo + " días hábiles siguientes al inicio del contrato; si te pasas, se aplica desde la solicitud, siempre que la presentes antes de 12 meses (art. 282.2). Para reanudar un paro suspendido, solicítalo en los " + P.plazo + " días siguientes al fin del trabajo (art. 271.3.b).</p>" : "<p><strong>Plazos:</strong> si el trabajo acaba, comunícalo al SEPE en los " + P.plazo + " días hábiles siguientes; el subsidio se suspende y se puede reanudar si acreditas desempleo, inscripción y rentas o cargas familiares (art. 282.3).</p>";
  note += "<p><strong>No incluye:</strong> la retención real del IRPF ni el efecto de sumar el sueldo en tu declaración, la cotización a la Seguridad Social (el sueldo es neto), el nuevo paro que generarían tus cotizaciones y el derecho de opción (art. 269.3), la Renta Activa de Inserción, el Ingreso Mínimo Vital, los fijos discontinuos, los trabajadores agrarios, el trabajo por cuenta propia, la capitalización del paro, los programas de fomento del empleo y los territorios forales en lo que no es la prestación estatal.</p>";
  EM.renderResult({
    winner: ["", "solo", "compat", "suspende"][w], verdict: V, tone: "ok",
    bigNumber: r.margen, bigLabel: "de diferencia neta en " + txtMeses(H) + " con la mejor opción", format: eur,
    barsLabel: "Total neto en " + txtMeses(H), bars: bars, cols: cols,
    rows: [rowM, { label: rowT[0], values: rowT.slice(1), strong: true }, rowG, rowR],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
