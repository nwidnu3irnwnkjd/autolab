// Suscripciones: gasto anual, coste por hora de uso y ahorro si rotas o cancelas las de menor uso.
// Tres grupos (precio mensual de la suma del grupo, horas de uso al mes). Hipotesis: las horas anuales no cambian si rotas
// (concentras el uso en los m meses en que pagas). Candidatas: coste por hora del grupo > media ponderada (precio total / horas totales).
// Candidata con horas: paga lo menor entre rotar (m x precio) y plan anual (12 x precio x (1 - descuento)). Sin horas: se cancela.
// Las no candidatas se quedan, con plan anual si hay descuento.
function calcular(d) {
  var P = [d.p1, d.p2, d.p3], H = [d.h1, d.h2, d.h3], i, sp = 0, sh = 0;
  for (i = 0; i < 3; i++) { sp += P[i]; sh += H[i]; }
  var dto = d.dto / 100, m = d.meses, gasto = 12 * sp, anual = 12 * sp * (1 - dto);
  var ahCand = 0, ahMant = 0, nCand = 0, ch = [], mayor = -1, mayorV = -1;
  for (i = 0; i < 3; i++) {
    ch.push(H[i] > 0 ? P[i] / H[i] : -1);
    if (H[i] > 0 && P[i] / H[i] > mayorV) { mayorV = P[i] / H[i]; mayor = i; }
    if (P[i] <= 0) continue;
    var cand = H[i] <= 0 || P[i] * sh > H[i] * sp;
    if (cand) {
      nCand++;
      ahCand += H[i] <= 0 ? 12 * P[i] : 12 * P[i] - Math.min(m * P[i], 12 * P[i] * (1 - dto));
    } else ahMant += 12 * P[i] * dto;
  }
  return { gastoAnual: gasto, gastoPagoAnual: anual, horasMes: sh, mediaHora: sh > 0 ? sp / sh : -1,
    horaG1: ch[0], horaG2: ch[1], horaG3: ch[2], mayorCoste: mayor, nCandidatas: nCand,
    ahorroCandidatas: ahCand, ahorroMantenidas: ahMant, ahorroTotal: ahCand + ahMant, gastoTras: gasto - ahCand - ahMant,
    descuentoAnual: gasto - anual };
}
function eur(x) { return EM.eur(x); }
var IDS = ["p1", "h1", "p2", "h2", "p3", "h3", "dto", "meses"];
var NOM = ["vídeo en streaming", "música y apps", "otras (prensa, gimnasio…)"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.p1 < 0 || d.p2 < 0 || d.p3 < 0 || d.h1 < 0 || d.h2 < 0 || d.h3 < 0 || d.dto < 0) return;
  if (d.p1 + d.p2 + d.p3 <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe el gasto mensual de al menos un grupo de suscripciones.", tone: "warn",
      note: "<p>Sin ningún gasto mensual no hay nada que calcular.</p>" });
    return;
  }
  if (d.dto >= 100 || d.meses < 0 || d.meses > 12) {
    EM.renderResult({ winner: "invalido", verdict: "El descuento por pago anual debe ser menor que 100 % y los meses con suscripción activa, de 0 a 12.", tone: "warn",
      note: "<p>Revisa esos dos datos.</p>" });
    return;
  }
  var r = calcular(d), P = [d.p1, d.p2, d.p3], H = [d.h1, d.h2, d.h3], i;
  var verdict = "Gastas " + EM.eur(r.gastoAnual) + " al año en suscripciones. ";
  if (r.nCandidatas === 0) verdict += "Ningún grupo cuesta por hora de uso más que tu media" + (r.mediaHora >= 0 ? " (" + EM.eur(r.mediaHora, 2) + " por hora)" : "") + ": no hay una candidata clara a cancelar" + (r.ahorroMantenidas > 0 ? "; solo el plan anual te ahorraría " + EM.eur(r.ahorroMantenidas) + " al año." : ".");
  else if (r.ahorroTotal < 1) verdict += "Hay grupos que cuestan más que la media por hora de uso, pero con esos meses y ese descuento rotar o cancelar no te ahorra nada.";
  else if (r.mediaHora < 0) verdict += "Con 0 horas de uso en total, todas son candidatas a cancelar: ahorrarías " + EM.eur(r.ahorroTotal) + " al año.";
  else verdict += "Las que cuestan más de " + EM.eur(r.mediaHora, 2) + " por hora de uso (la media de tus suscripciones) son las candidatas a rotar o cancelar: con ellas, y con plan anual en las demás si hay descuento, ahorrarías " + EM.eur(r.ahorroTotal) + " al año y gastarías " + EM.eur(r.gastoTras) + ".";
  var rows = [], nom = ["Streaming", "Música y apps", "Otras"];
  for (i = 0; i < 3; i++) {
    var ch = H[i] > 0 && P[i] > 0 ? P[i] / H[i] : null;
    rows.push([nom[i], EM.eur(12 * P[i]), H[i] > 0 ? EM.num(12 * H[i], 0) + " h" : "sin uso", ch === null ? (P[i] > 0 ? "sin uso" : "—") : EM.eur(ch, 2)]);
  }
  var note = "<p><strong>Lectura:</strong> el coste por hora es el precio mensual entre las horas de uso al mes. ";
  if (r.descuentoAnual > 0) note += "Pagar todo por adelantado con tu descuento ahorraría " + EM.eur(r.descuentoAnual) + " al año, pero solo tiene sentido en lo que vas a usar todo el año. ";
  note += "Al rotar se supone que concentras las mismas horas de uso en los " + EM.num(d.meses, d.meses % 1 ? 1 : 0) + " meses en que pagas.</p>";
  note += "<p><strong>Límites:</strong> cada fila suma varias suscripciones del mismo tipo; los precios y horas son tuyos o ejemplos, no tarifas de plataformas concretas. No se valoran el catálogo, la calidad ni los contratos con permanencia, y los precios pueden cambiar.</p>";
  EM.renderResult({
    winner: r.ahorroTotal < 1 ? "mantener" : "recortar", verdict: verdict, tone: r.ahorroTotal < 1 ? "warn" : "ok",
    bigNumber: r.ahorroTotal, bigLabel: "de ahorro anual posible", format: EM.eur,
    barsLabel: "Gasto anual por grupo",
    bars: [{ label: "Streaming", value: 12 * d.p1, color: "a" }, { label: "Música y apps", value: 12 * d.p2, color: "b" }, { label: "Otras", value: 12 * d.p3, color: "a" }],
    cols: ["Gasto al año", "Uso al año", "€ por hora"],
    rows: rows,
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
