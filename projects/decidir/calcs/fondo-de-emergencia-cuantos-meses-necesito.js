// Fondo de emergencia: meses de gastos recomendados (HIPOTESIS propia, no una ley), importe objetivo y meses para alcanzarlo.
// Base: indefinido/funcionario 3, temporal 6, autonomo 6; +1 si ingresos variables; +0,5 por persona a cargo (maximo +2); -1 si otra persona del hogar tiene ingresos estables; entre 3 y 12.
// empleo: 0 indefinido, 1 temporal, 2 autonomo; ingresos: 0 estables, 1 variables; otro: 0 no, 1 si.
// ganador (estado): 0 ya cubierto, 1 se alcanza en 12 meses o menos, 2 en mas de 12, 3 no se alcanza sin aportacion.
var BASE = [3, 6, 6], MIN_M = 3, MAX_M = 12;
function calcular(d) {
  var m = BASE[d.empleo] + (d.ingresos === 1 ? 1 : 0) + Math.min(d.dep * 0.5, 2) - (d.otro === 1 ? 1 : 0);
  m = Math.min(Math.max(m, MIN_M), MAX_M);
  var obj = m * d.gastos, falta = Math.max(obj - d.ahorro, 0), falta1 = Math.max(d.gastos - d.ahorro, 0);
  var cob = d.gastos > 0 ? d.ahorro / d.gastos : 0;
  var alc = falta === 0 ? 0 : (d.aport > 0 ? Math.ceil(falta / d.aport) : -1);
  var h1 = falta1 === 0 ? 0 : (d.aport > 0 ? Math.ceil(falta1 / d.aport) : -1);
  var g = falta === 0 ? 0 : (alc < 0 ? 3 : (alc <= 12 ? 1 : 2));
  return { meses: m, objetivo: obj, falta: falta, cobertura: cob, mesesAlcanzar: alc, mesesHito1: h1, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
function plazo(n) {
  var a = Math.floor(n / 12), m = n % 12, s = EM.num(n, 0) + (n === 1 ? " mes" : " meses");
  if (a >= 1) s += " (" + a + (a === 1 ? " año" : " años") + (m ? " y " + m + (m === 1 ? " mes" : " meses") : "") + ")";
  return s;
}
var IDS = ["gastos", "empleo", "ingresos", "dep", "otro", "ahorro", "aport"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.gastos <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica tus gastos mensuales imprescindibles (mayores que 0 €).", tone: "warn", note: "<p>Cuenta lo que pagarías cada mes aunque te quedaras sin ingresos: vivienda, comida, suministros, seguros y cuotas.</p>" });
    return;
  }
  if (d.dep > 10 || d.dep % 1 !== 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica el número de personas a tu cargo como un entero de 0 a 10.", tone: "warn", note: "<p>Cuenta solo a quienes dependen de tus ingresos.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ms = EM.num(r.meses, r.meses % 1 ? 1 : 0), w, verdict, tone = "ok";
  var base = "Con estos criterios (una hipótesis, no una ley) conviene tener unos " + ms + " meses de gastos ahorrados, " + EM.eur(r.objetivo) + ". ";
  if (g === 0) {
    w = "cubierto";
    verdict = base + "Ya los tienes: tu ahorro de " + EM.eur(d.ahorro) + " cubre " + EM.num(r.cobertura, 1) + " meses.";
  } else if (g === 1) {
    w = "en-camino";
    verdict = base + "Te faltan " + EM.eur(r.falta) + " y con " + EM.eur(d.aport) + " al mes los alcanzas en " + plazo(r.mesesAlcanzar) + ".";
  } else if (g === 2) {
    w = "largo-plazo"; tone = "warn";
    verdict = base + "Te faltan " + EM.eur(r.falta) + " y con " + EM.eur(d.aport) + " al mes tardarías " + plazo(r.mesesAlcanzar) + ": plantéate subir la aportación o ir por hitos.";
  } else {
    w = "sin-aportacion"; tone = "warn";
    verdict = base + "Te faltan " + EM.eur(r.falta) + " y, sin aportación mensual, el fondo no crece: fija una cantidad al mes, aunque sea pequeña.";
  }
  var note = "<p><strong>Lectura:</strong> hoy tu ahorro cubre " + EM.num(r.cobertura, 1) + " meses de gastos. ";
  if (g !== 0 && r.mesesHito1 > 0) note += "Un primer hito razonable es juntar 1 mes de gastos (" + EM.eur(d.gastos) + "): lo tendrías en " + plazo(r.mesesHito1) + ". ";
  else if (g !== 0 && r.mesesHito1 < 0) note += "Sin aportación no llegas ni a un primer mes de gastos. ";
  note += "El fondo cubre gastos imprescindibles, no el nivel de vida actual: si recortas en una crisis, necesitas menos.</p>";
  note += "<p><strong>Criterio usado (hipótesis propia, no una norma ni una regla oficial):</strong> 3 meses para un asalariado indefinido o funcionario, 6 si el empleo es temporal o autónomo; +1 mes si los ingresos son variables; +0,5 por persona a cargo (hasta +2); -1 si otra persona del hogar tiene ingresos estables; con un mínimo de 3 y un máximo de 12. Es una guía para empezar, no un resultado exacto.</p>";
  note += "<p><strong>Dónde guardarlo:</strong> lo importante es que puedas disponer del dinero cuando lo necesites sin perder capital: una cuenta corriente o de ahorro de acceso inmediato o un producto con liquidez y sin riesgo de pérdida. Evita inmovilizarlo o ponerlo en inversiones cuyo valor puede bajar justo cuando lo necesites, y mira si tu entidad está cubierta por el Fondo de Garantía de Depósitos. No es asesoramiento financiero ni recomendación de ningún producto.</p>";
  note += "<p><strong>No incluye:</strong> el paro que podrías cobrar, deudas con cuotas altas, gastos extraordinarios previsibles (coche, salud, reformas), una segunda fuente de ingresos distinta de la que marcas ni la inflación. Si cobras prestación o tienes seguros que cubren parte del riesgo, necesitarás menos.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: r.meses, bigLabel: "meses de gastos recomendados (hipótesis)", format: function (x) { return EM.num(x, x % 1 ? 1 : 0); },
    barsLabel: "Tu ahorro frente al objetivo",
    bars: [{ label: "Ahorro actual", value: d.ahorro, color: "a" }, { label: "Objetivo" + (w === "cubierto" ? " (cubierto)" : ""), value: r.objetivo, color: "b" }],
    cols: ["Tú"],
    rows: [
      ["Meses de gastos recomendados", ms],
      ["Importe objetivo", EM.eur(r.objetivo)],
      ["Meses de gastos que cubre tu ahorro", EM.num(r.cobertura, 1)],
      { label: "Importe que te falta", values: [EM.eur(r.falta)], strong: true },
      ["Tiempo para alcanzarlo", g === 0 ? "ya lo tienes" : (r.mesesAlcanzar < 0 ? "sin aportación, no se alcanza" : plazo(r.mesesAlcanzar))]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
