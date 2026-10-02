// Seguro de salud privado: coste esperado con seguro (prima + copagos) frente a pagar cada acto sin seguro.
// Modelo: "actos" = consultas, pruebas y urgencias que esperas al ano (todas al mismo coste medio). Con seguro pagas tu parte de la prima
// (la empresa paga un % si es de grupo) mas el copago por acto; sin seguro, el precio privado del acto. La prima sube sp % al ano y los precios sc % al ano.
function calcular(d) {
  var H = Math.max(Math.round(d.horizonte), 1), sp = d.subidaPrima / 100, sc = d.subidaPrecios / 100, tuParte = 1 - Math.min(Math.max(d.empresa, 0), 100) / 100;
  var con = 0, sin = 0, primas = 0, copagos = 0, ahorroActos = 0, y, fp, fc, con1 = 0, sin1 = 0;
  for (y = 0; y < H; y++) {
    fp = Math.pow(1 + sp, y); fc = Math.pow(1 + sc, y);
    var pr = d.prima * tuParte * fp, cp = d.actos * d.copago * fc, sn = d.actos * d.coste * fc;
    primas += pr; copagos += cp; con += pr + cp; sin += sn; ahorroActos += d.actos * (d.coste - d.copago) * fc;
    if (y === 0) { con1 = pr + cp; sin1 = sn; }
  }
  var sumFc = 0; for (y = 0; y < H; y++) sumFc += Math.pow(1 + sc, y);
  var unit = d.coste - d.copago, eqH = unit > 0 ? primas / (unit * sumFc) : -1, eq1 = unit > 0 ? d.prima * tuParte / unit : -1;
  return {
    H: H, conSeguro: con, sinSeguro: sin, primas: primas, copagos: copagos, diferencia: sin - con, conAno1: con1, sinAno1: sin1,
    primaAno1: d.prima * tuParte, primaUltimo: d.prima * tuParte * Math.pow(1 + sp, H - 1), actosEq: eqH, actosEq1: eq1,
    ahorroPorActo: unit, mejor: con < sin - 1 ? 0 : (sin < con - 1 ? 1 : 2)
  };
}
function eur(x) { return EM.eur(x); }
function n1(x) { return EM.num(x, 1).replace(/,0$/, ""); }
var IDS = ["prima", "empresa", "subidaPrima", "actos", "coste", "copago", "subidaPrecios", "horizonte"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.prima <= 0 || d.horizonte < 1) { aviso("Escribe una prima anual mayor que 0 y al menos 1 año de horizonte.", "Sin prima o sin horizonte no hay seguro que comparar."); return; }
  if (d.empresa > 100 || d.horizonte > 40 || d.subidaPrima > 20 || d.subidaPrecios > 20 || d.actos > 200) { aviso("Revisa los límites: la parte de la empresa no puede pasar del 100 %, el horizonte de 40 años, las subidas del 20 % anual ni los actos de 200 al año.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), anos = EM.num(r.H, 0) + (r.H === 1 ? " año" : " años"), w, v;
  var eq = r.actosEq < 0 ? null : n1(r.actosEq);
  if (r.ahorroPorActo <= 0) {
    w = "sin-seguro";
    v = "Con estos datos, el seguro no te ahorra nada por acto (el copago de " + eur(d.copago) + " alcanza el coste de pagar el acto, " + eur(d.coste) + "): solo pagarías la prima, " + eur(r.conSeguro) + " en " + anos + " frente a " + eur(r.sinSeguro) + " sin seguro.";
  } else if (r.mejor === 0) {
    w = "seguro";
    v = "Con estos datos, el seguro cuesta " + eur(r.diferencia) + " menos en " + anos + " que pagar cada acto por tu cuenta, porque esperas " + n1(d.actos) + " actos al año y el equilibrio está en " + eq + ". Es una decisión de cobertura y acceso, no solo de coste.";
  } else if (r.mejor === 2) {
    w = "empate";
    v = "Con estos datos, con seguro y sin él cuestas lo mismo en " + anos + " (unos " + eur(r.sinSeguro) + "): tus " + n1(d.actos) + " actos al año coinciden con el equilibrio. Es una decisión de cobertura y acceso, no solo de coste.";
  } else {
    w = "sin-seguro";
    v = "Con estos datos, pagar cada acto por tu cuenta cuesta " + eur(-r.diferencia) + " menos en " + anos + " que el seguro; solo compensaría en coste con unos " + eq + " actos al año o más (esperas " + n1(d.actos) + "). Es una decisión de cobertura y acceso, no solo de coste.";
  }
  var note = "<p><strong>Lectura:</strong> con seguro pagas " + eur(r.conAno1) + " el primer año (tu parte de la prima, " + eur(r.primaAno1) + ", más copagos) y sin seguro " + eur(r.sinAno1) + ". ";
  if (d.subidaPrima > 0 && r.H > 1) note += "Con la subida de la prima del " + n1(d.subidaPrima) + " % anual, tu parte llega a " + eur(r.primaUltimo) + " el año " + EM.num(r.H, 0) + ". ";
  if (r.actosEq >= 0) note += "El equilibrio está en " + n1(r.actosEq) + " actos al año de media en el horizonte (" + n1(r.actosEq1) + " el primer año), con un ahorro de " + eur(r.ahorroPorActo) + " por acto frente a pagarlo por tu cuenta. ";
  note += "</p><p><strong>Lo que el coste no mide:</strong> las listas de espera, la libre elección de médico y la tranquilidad de tener cobertura no tienen precio en esta calculadora; para muchas personas pesan más que el dinero. Tampoco incluye urgencias graves u hospitalizaciones (que podrían costar mucho más que lo que pones aquí), preexistencias, carencias, exclusiones de la póliza ni el efecto fiscal de un seguro de empresa. Los importes son ejemplos tuyos, no tarifas. No es una recomendación sanitaria ni asesoramiento: ante cualquier duda de salud, consulta a un profesional.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: r.mejor === 0 && r.ahorroPorActo > 0 ? "ok" : "warn",
    bigNumber: Math.abs(r.diferencia), bigLabel: r.mejor === 0 ? "menos con seguro en " + anos : (r.mejor === 1 ? "menos sin seguro en " + anos : "de diferencia en " + anos), format: EM.eur,
    barsLabel: "Coste esperado en " + anos,
    bars: [{ label: "Con seguro" + (r.mejor === 0 ? " (menos coste)" : ""), value: r.conSeguro, color: "a" }, { label: "Sin seguro" + (r.mejor === 1 ? " (menos coste)" : ""), value: r.sinSeguro, color: "b" }],
    cols: ["Con seguro", "Sin seguro"],
    rows: [
      ["Primer año", eur(r.conAno1), eur(r.sinAno1)],
      ["Primas (tu parte) en " + anos, eur(r.primas), eur(0)],
      ["Copagos o pago de cada acto en " + anos, eur(r.copagos), eur(r.sinSeguro)],
      { label: "Coste esperado en " + anos, values: [eur(r.conSeguro), eur(r.sinSeguro)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
