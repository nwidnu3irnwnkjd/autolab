// Retribucion flexible: me conviene? (2026). Parametros generados desde data/params.json (irpf_2026, autonomo_2026 y retribucion_flexible_2026; fuentes y fechas alli).
// Enfoque de arts. 19-20 y DA 61.a copiado de comparar-ofertas-de-trabajo-neto-real (verificado). est: escala estatal general; ccaa: escala general y minimo del contribuyente (min null = estatal); sol: cotizacion de solidaridad [desde, hasta, % empresa, % trabajador] (mensual).
var P = {"est":[[0,9.5],[12450,12],[20200,15],[35200,18.5],[60000,22.5],[300000,24.5]],"ccaa":{"andalucia":{"esc":[[0,9.5],[13000,12],[21100,15],[35200,18.5],[60000,22.5]],"min":5790},"aragon":{"esc":[[0,9.5],[13072.5,12],[21210,15],[36960,18.5],[52500,20.5],[60000,23],[80000,24],[90000,25],[130000,25.5]],"min":null},"asturias":{"esc":[[0,9],[12450,12],[17707.2,14],[33007.2,19.2],[53407.2,21.5],[70000,22.5],[90000,25],[175000,26]],"min":6105},"baleares":{"esc":[[0,9],[10000,11.25],[18000,14.25],[30000,17.5],[48000,19],[70000,21.75],[90000,22.75],[120000,23.75],[175000,24.75]],"min":5550},"canarias":{"esc":[[0,9],[13748,11.5],[19422,14],[35924,18.5],[57566,23.5],[93268,25],[123745,26]],"min":5606},"cantabria":{"esc":[[0,8.5],[13000,11],[21000,14.5],[35200,18],[60000,22.5],[90000,24.5]],"min":null},"clm":{"esc":[[0,9.5],[12450,12],[20200,15],[35200,18.5],[60000,22.5]],"min":null},"cyl":{"esc":[[0,9],[12450,12],[20200,14],[35200,18.5],[53407.2,21.5]],"min":null},"cataluna":{"esc":[[0,9.5],[12500,12.5],[22000,16],[33000,19],[53000,21.5],[90000,23.5],[120000,24.5],[175000,25.5]],"min":null},"extremadura":{"esc":[[0,7.75],[12450,9.75],[20200,16],[24200,17.5],[35200,21],[60000,23.5],[80200,24],[99200,24.5],[120200,25]],"min":null},"galicia":{"esc":[[0,9],[12985.35,11.65],[21068.6,14.9],[35200,18.4],[60000,22.5]],"min":5789},"madrid":{"esc":[[0,8.5],[13362.22,10.7],[19004.63,12.8],[35425.68,17.4],[57320.4,20.5]],"min":5956.65},"murcia":{"esc":[[0,9.5],[12450,11.2],[20200,13.3],[34000,17.9],[60000,22.5]],"min":null},"rioja":{"esc":[[0,8],[12450,10.6],[20200,13.6],[35200,17.8],[40000,18.3],[50000,19],[60000,24.5],[120000,27]],"min":null},"valencia":{"esc":[[0,8.8],[12000,11.7],[22000,14.6],[32000,17],[42000,19.4],[52000,21.9],[62000,24.4],[72000,26.1],[100000,27.35],[150000,28.35],[200000,29.35]],"min":6105}},"sol":[[5101.2,5611.32,0.96,0.19],[5611.32,7651.8,1.04,0.21],[7651.8,null,1.22,0.24]],"w":6.5};
var BMAX = 5101.20, MINIMO_E = 5550, SMI = 17094;
var T = { seg: 500, segD: 1500, dia: 11, tra: 1500, esp: 0.30, umbral: 0.05, mat: 1000 };
var PROD = { seguro: "seguro de salud", comida: "tarjeta restaurante", transporte: "transporte público", guarderia: "guardería", otro: "ese producto" };
var ART = { seguro: "el seguro de salud", comida: "la tarjeta restaurante", transporte: "el transporte público", guarderia: "la guardería", otro: "ese producto" };
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function cuotaBase(bg, cc) {
  var m = cc.min === null ? MINIMO_E : cc.min;
  return Math.max(0, escala(bg, P.est) - escala(MINIMO_E, P.est)) + Math.max(0, escala(bg, cc.esc) - escala(m, cc.esc));
}
function red20(n) {
  if (n >= 19747.5) return 0;
  if (n <= 14852) return 7302;
  if (n <= 17673.52) return 7302 - 1.75 * (n - 14852);
  return Math.max(0, 2364.34 - 1.14 * (n - 17673.52));
}
function da61(b) {
  if (b >= 20048.45) return 0;
  return b <= 17094 ? 590.89 : 590.89 - 0.2 * (b - 17094);
}
// Cotizacion del trabajador al ano: tipo sobre la base (tope BMAX/mes) mas solidaridad sobre el exceso mensual. La base incluye la retribucion en especie (LGSS art. 147.1).
function ssTrab(bruto) {
  var r = bruto / 12, base = Math.min(r, BMAX), s = 0, i, t, x;
  for (i = 0; i < P.sol.length; i++) {
    t = P.sol[i]; x = Math.max(0, Math.min(r, t[1] === null ? Infinity : t[1]) - t[0]); s += x * t[3] / 100;
  }
  return 12 * (base * P.w / 100 + s);
}
// IRPF final del ano: ingresos = rendimientos integros del trabajo (sin lo exento); cot = cotizacion deducible.
function irpfDe(ingresos, cot, cc) {
  var neto = ingresos - cot, otros = Math.min(2000, Math.max(neto, 0)), rn = Math.max(0, neto - otros - red20(neto));
  var ci = cuotaBase(rn, cc);
  return Math.max(0, ci - Math.min(da61(ingresos), ci));
}
function netoDe(bruto, cc) { var c = ssTrab(bruto); return bruto - c - irpfDe(bruto, c, cc); }
// Bruto extra cuyo neto adicional alcanza T (se sube y se afina por biseccion).
function brutoExtra(S, T0, cc) {
  var base = netoDe(S, cc), lo = 0, hi = 100, m, j;
  if (T0 <= 0) return 0;
  while (netoDe(S + hi, cc) - base < T0 && hi < 1e9) { lo = hi; hi = hi < 1e5 ? hi + 100 : hi * 1.5; }
  for (j = 0; j < 80; j++) { m = (lo + hi) / 2; if (netoDe(S + m, cc) - base >= T0) hi = m; else lo = m; }
  return hi;
}
function pos(x) { return Math.max(+x || 0, 0); }
function calcular(d) {
  var r = { bloqueado: 0, escenario: 0, exento: 0, cap: 0, maxX: 0, permitido: 0, ss: 0, irpfA: 0, irpfB: 0, ahorroIRPF: 0, netoA: 0, netoB: 0, ahorroNeto: 0, brutoEq: 0, tipoEf: 0, perdidaMat: 0, ahorroTrasMat: 0, ahorroAlt: 0, ganNum: 0 };
  var S = pos(d.bruto), C = pos(d.coste), X = pos(d.sustituir), prod = d.producto;
  var n = Math.floor(Math.max(1, Math.min(8, pos(d.personas) || 1))), m = Math.floor(Math.max(0, Math.min(n, pos(d.discap)))), D = Math.max(0, Math.min(260, pos(d.dias)));
  var cc = P.ccaa[d.ccaa], cap, gan;
  if (!cc || S <= 0 || X <= 0) { r.bloqueado = 1; return r; }
  if (prod === "seguro") cap = T.seg * (n - m) + T.segD * m;
  else if (prod === "comida") cap = T.dia * D;
  else if (prod === "transporte") cap = T.tra;
  else if (prod === "guarderia") cap = Infinity;
  else cap = 0;
  r.cap = cap === Infinity ? -1 : cap;
  r.exento = Math.min(X, cap);
  r.maxX = Math.max(0, Math.min(T.esp * S, S - SMI));
  r.permitido = X <= r.maxX + 1e-9 ? 1 : 0;
  r.ss = ssTrab(S);
  r.irpfA = irpfDe(S, r.ss, cc); r.irpfB = irpfDe(S - r.exento, r.ss, cc);
  r.ahorroIRPF = r.irpfA - r.irpfB;
  r.netoA = S - r.ss - r.irpfA - C; r.netoB = S - X - r.ss - r.irpfB;
  r.ahorroNeto = r.netoB - r.netoA;
  r.brutoEq = brutoExtra(S, C, cc);
  r.tipoEf = r.exento > 0 ? r.ahorroIRPF / r.exento * 100 : 0;
  r.perdidaMat = prod === "guarderia" ? Math.min(T.mat, C) - Math.min(T.mat, Math.max(0, C - r.exento)) : 0;
  r.ahorroTrasMat = r.ahorroNeto - r.perdidaMat;
  r.ahorroAlt = prod === "guarderia" && C > T.mat ? r.irpfA - irpfDe(S - (C - T.mat), r.ss, cc) : 0;
  gan = r.ahorroNeto >= T.umbral * C && r.ahorroNeto > 0 ? 1 : (r.ahorroNeto <= -T.umbral * C && r.ahorroNeto < 0 ? 2 : 0);
  r.ganNum = gan;
  r.escenario = !r.permitido ? 4 : (gan === 1 ? (r.exento <= 0 ? 5 : (r.exento >= X - 1e-9 ? 1 : 2)) : 3);
  return r;
}
function eur(x) { return EM.eur(x); }
function pct(x) { return EM.num(x, 1) + " %"; }
var IDS = ["bruto", "coste", "sustituir", "personas", "discap", "dias"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.producto = document.getElementById("producto").value; return d;
}
function pintar() {
  var d = leer(), r = calcular(d), nom = PROD[d.producto], verdict, tone = "ok", note = "", sin;
  if (d.ccaa === "foral") {
    EM.renderResult({ winner: "foral", tone: "warn", verdict: "País Vasco y Navarra tienen su propio IRPF y esta calculadora no lo cubre.", note: "<p>Las rentas en especie exentas pueden tener topes y requisitos distintos en los regímenes forales. Consulta la normativa de tu Hacienda foral.</p>" });
    return;
  }
  if (d.bruto <= 0 || d.sustituir <= 0) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Escribe tu salario bruto anual y el importe del bruto que cambiarías por el producto.", note: "<p>La calculadora compara cobrar todo el sueldo en dinero y pagar tú el producto con cobrar menos en dinero y recibirlo de tu empresa en especie.</p>" });
    return;
  }
  sin = r.cap === 0 || r.exento <= 0;
  if (!r.permitido) {
    tone = "warn";
    verdict = "Con tus datos, no puedes cambiar " + eur(d.sustituir) + " de sueldo por " + ART[d.producto] + ": el salario en especie no puede pasar del 30 % de tus percepciones salariales ni dejar tu sueldo en dinero por debajo del salario mínimo, así que el máximo es " + eur(r.maxX) + " al año.";
  } else if (r.ganNum === 1 && sin) {
    verdict = "Con tus datos, la retribución flexible te deja " + eur(r.ahorroNeto) + " más al año, pero no por IRPF (la exención no existe para ese importe o producto): solo porque tu empresa te da " + ART[d.producto] + " por " + eur(d.sustituir) + " de tu bruto y por tu cuenta te costaría " + eur(d.coste) + ".";
  } else if (r.ganNum === 1) {
    verdict = "Con tus datos, la retribución flexible te deja " + eur(r.ahorroNeto) + " más al año: " + (r.escenario === 1 ? "los " + eur(d.sustituir) + " de " + nom + " están exentos de IRPF y te ahorras el " + pct(r.tipoEf) + " de ellos" : "solo " + eur(r.exento) + " de los " + eur(d.sustituir) + " están exentos de IRPF (el resto tributa como sueldo) y te ahorras el " + pct(r.tipoEf) + " de esa parte") + "; no cambia lo que pagas de Seguridad Social.";
  } else if (r.ganNum === 2) {
    tone = "warn";
    verdict = "Con tus datos, pagar " + ART[d.producto] + " por tu cuenta sale mejor por " + eur(-r.ahorroNeto) + " al año: " + (sin ? "la exención no existe para ese importe o producto y cambias " + eur(d.sustituir) + " de sueldo por algo que te cuesta " + eur(d.coste) + "." : "el ahorro de IRPF de " + eur(r.ahorroIRPF) + " no compensa que cedas " + eur(d.sustituir) + " de sueldo por algo que te cuesta " + eur(d.coste) + " por tu cuenta.");
  } else {
    tone = "warn";
    verdict = "Con tus datos, es un empate práctico (diferencia de " + eur(Math.abs(r.ahorroNeto)) + " al año)" + (sin ? ": la exención no existe para ese importe o producto, así que solo ganarías si tu empresa te lo ofrece más barato que tu precio." : ": el ahorro de IRPF de " + eur(r.ahorroIRPF) + " queda en nada frente a lo que cedes de sueldo.");
  }
  if (r.permitido && d.producto !== "otro" && !sin && r.exento < d.sustituir) note += "<p><strong>La exención no cubre todo el importe:</strong> el tope para " + nom + " es " + (r.cap < 0 ? "ilimitado" : eur(r.cap)) + " y los " + eur(d.sustituir - r.exento) + " de más tributan igual que el sueldo.</p>";
  if (d.producto === "otro") note += "<p><strong>Para ese producto no hay exención</strong> (gimnasio, móvil, ordenador, cursos que eliges tú, etc.): se valora como retribución en especie y tributa como sueldo.</p>";
  if (d.producto === "comida" && d.dias <= 0) note += "<p>Indica los días de trabajo al año en que usarás la tarjeta: sin días no hay importe exento.</p>";
  if (d.producto === "comida") note += "<p>Pon como coste lo que ya ibas a gastar en comidas: si no, no es un ahorro. El máximo es 11 € por día de trabajo, sin dietas exentas ese día ni acumular lo no gastado.</p>";
  var cond = d.producto === "guarderia" && r.permitido && r.perdidaMat > 0;
  if (cond) {
    tone = "warn";
    verdict = "Con tus datos, la guardería deja hasta " + eur(r.ahorroNeto) + " al año si no tienes derecho al incremento de la deducción por maternidad (art. 81.2), y unos " + eur(r.ahorroTrasMat) + " si lo tienes, porque pierdes " + eur(r.perdidaMat) + (r.ahorroTrasMat < 0 ? " (no conviene)" : "") + (r.ahorroAlt > 0 ? ". Cediendo " + eur(d.coste - T.mat) + " (el resto lo pagas tú) conservas el incremento y ahorras " + eur(r.ahorroAlt) + "." : ".");
  }
  if (d.producto === "transporte") note += "<p>Solo cuenta el transporte público colectivo; la gasolina o el aparcamiento no están exentos.</p>";
  if (d.producto === "seguro") note += "<p>El seguro puede cubrirte a ti, a tu cónyuge y a tus hijos. Se supone la prima repartida a partes iguales entre las " + EM.num(Math.max(1, Math.min(8, Math.floor(d.personas) || 1)), 0) + " persona(s) cubiertas.</p>";
  note += "<p><strong>Seguridad Social:</strong> la base de cotización cuenta la remuneración total, en dinero o en especie, y solo excluye una lista cerrada de conceptos que no incluye estos productos: tu cotización (" + eur(r.ss) + " al año) y tus prestaciones (paro, baja, pensión) no cambian.</p>";
  note += "<p><strong>Pagarlo tú:</strong> " + eur(d.coste) + " netos al año equivalen a unos " + eur(r.brutoEq) + " brutos más de sueldo.</p>";
  note += "<p><strong>No incluye:</strong> País Vasco y Navarra, vehículos, vivienda, préstamos a empleados, planes de pensiones de empleo, acciones ni directivos; tampoco la retención de la nómina ni comisiones de gestión. Se supone contrato indefinido a jornada completa, un año completo, que la empresa paga el producto y lo valora por el sueldo que cedes. Normalmente se pacta contigo. El límite del 30 % cuenta también la especie que ya cobres.</p>";
  if (d.bruto < SMI + 1) note += "<p><strong>Atención:</strong> con un sueldo igual o inferior al salario mínimo (" + eur(SMI) + " en 14 pagas) no se puede ceder nada en especie.</p>";
  EM.renderResult({
    winner: r.escenario, verdict: verdict, tone: tone,
    bigNumber: r.permitido && !cond ? r.ahorroNeto : undefined, bigLabel: r.permitido && !cond ? "al año " + (r.ahorroNeto >= 0 ? "a favor" : "en contra") + " de la retribución flexible" : "", format: eur,
    barsLabel: "Neto anual después de Seguridad Social, IRPF y del producto",
    bars: [{ label: "Pagándolo tú", value: Math.max(r.netoA, 0), color: "a" }, { label: "Con retribución flexible", value: Math.max(r.netoB, 0), color: "b" }],
    cols: ["Pagándolo tú", "Con retribución flexible"],
    rows: [
      ["Sueldo bruto en dinero", eur(d.bruto), eur(d.bruto - d.sustituir)],
      ["Producto en especie (cedido del bruto)", eur(0), eur(d.sustituir)],
      ["Parte exenta de IRPF", "–", eur(r.exento)],
      ["Seguridad Social a tu cargo (misma base)", eur(r.ss), eur(r.ss)],
      ["IRPF del año", eur(r.irpfA), eur(r.irpfB)],
      ["Pagas tú el producto", eur(d.coste), eur(0)],
      { label: "Neto anual tras el producto", values: [eur(r.netoA), eur(r.netoB)], strong: true },
      ["Bruto extra que necesitarías para pagarlo tú", eur(r.brutoEq), "–"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
