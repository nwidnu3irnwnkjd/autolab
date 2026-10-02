// Cambiar de operadora con permanencia: quedarse, cambiar ya pagando la penalizacion o esperar a que acabe la permanencia.
// Coste en el horizonte: quedarse = H x cuota actual; cambiar ya = penalizacion + alta + cuotas nuevas (promo N meses y luego cuota completa);
// esperar = cuota actual durante la permanencia, luego alta + cuotas nuevas. Sin permanencia la penalizacion no se aplica. Todo son datos del usuario.
function calcular(d) {
  var H = d.horiz, W = d.perm, pen = W > 0 ? d.penal : 0;
  function nuevo(n) {
    var m = Math.min(n, d.promoM);
    return m * d.promo + (n - m) * d.nueva;
  }
  var q = H * d.act, c = pen + d.alta + nuevo(H), e = H <= W ? q : W * d.act + d.alta + nuevo(H - W), t, eq = -1;
  for (t = 120; t >= 1; t--) {
    if (t * d.act - pen - d.alta - nuevo(t) >= -1e-9) eq = t; else break;
  }
  var best = Math.min(c, e);
  return {
    costeQuedarse: q, costeCambiar: c, costeEsperar: e, ahorroCambiar: q - c, ahorroEsperar: q - e, mesEq: eq,
    penalMax: q - d.alta - nuevo(H), penalMaxEsperar: e - d.alta - nuevo(H),
    ganador: q - best <= 1 ? 2 : (c <= e ? 0 : 1)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["act", "nueva", "promoM", "promo", "perm", "penal", "alta", "horiz"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.act <= 0 || d.horiz < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe tu cuota actual (más de 0) y un horizonte de al menos 1 mes.", tone: "warn", note: "<p>Sin cuota actual ni horizonte no hay nada que comparar.</p>" });
    return;
  }
  if (d.horiz > 120 || d.perm > 60 || d.promoM > 60 || d.act > 1000 || d.nueva > 1000 || d.promo > 1000 || d.penal > 5000 || d.alta > 1000) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 120 meses de horizonte, 60 de permanencia o de promoción, 1.000 € de cuota y 5.000 € de penalización.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), H = d.horiz, g = r.ganador, w = ["cambiar", "esperar", "quedarse"][g], verdict;
  var meses = EM.num(H, 0) + (H === 1 ? " mes" : " meses");
  if (g === 2) {
    verdict = "Con estos datos no compensa cambiar en " + meses + ": quedarte cuesta " + eur(r.costeQuedarse) + " y la mejor alternativa no baja de " + eur(r.costeQuedarse - Math.max(r.ahorroCambiar, r.ahorroEsperar)) + ", así que no ahorras con el cambio. La promoción expira: lo que cuenta es la cuota completa.";
  } else if (g === 0) {
    verdict = "Con estos datos compensa cambiar ya aun pagando la penalización: ahorras " + eur(r.ahorroCambiar) + " en " + meses + (r.mesEq > 0 ? " y recuperas lo pagado (penalización y alta) en el mes " + r.mesEq : "") + ". Las promociones expiran: comprueba la cuota completa.";
  } else {
    verdict = "Con estos datos compensa cambiar, pero esperando a que acabe la permanencia: ahorras " + eur(r.ahorroEsperar) + " en " + meses + ", más que cambiando ya (" + eur(r.ahorroCambiar) + "). Cambiar ya solo compensaría con una penalización menor de " + eur(Math.max(r.penalMaxEsperar, 0)) + ". Las promociones expiran: comprueba la cuota completa.";
  }
  var note = "<p><strong>Lectura:</strong> ";
  note += "la penalización máxima con la que cambiar ya sigue ahorrando frente a quedarte es " + eur(Math.max(r.penalMax, 0)) + " (la tuya es " + eur(d.perm > 0 ? d.penal : 0) + "). ";
  if (d.perm > 0 && d.perm < H) note += "Frente a esperar " + EM.num(d.perm, 0) + " meses, cambiar ya compensa si la penalización es menor de " + eur(Math.max(r.penalMaxEsperar, 0)) + ". ";
  if (d.perm >= H) note += "Tu permanencia dura todo el horizonte: esperar equivale a quedarte. ";
  if (d.perm <= 0) note += "Sin permanencia no se aplica penalización y cambiar ya equivale a esperar. ";
  if (d.promoM > 0 && d.promo < d.nueva) note += "Tras los " + EM.num(d.promoM, 0) + " meses de promoción la cuota pasa a " + eur(d.nueva) + (d.nueva >= d.act ? ", igual o más que tu cuota actual: desde entonces el cambio no ahorra." : ". ");
  note += "</p><p>Es una estimación con supuestos tuyos: la penalización, la cuota completa y las condiciones de la promoción están en tu contrato y tu oferta (consulta tu contrato). No incluye diferencias de servicio, cobertura, velocidad o datos, subidas de precio posteriores, ni descuentos por llevar varios servicios; supone que la cuota actual no cambia y que el cambio se hace sin periodos sin servicio.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: Math.max(r.ahorroCambiar, r.ahorroEsperar, 0), bigLabel: "€ de ahorro en " + meses + " con la mejor alternativa a quedarte (0 si no compensa)", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste total en " + meses,
    bars: [{ label: "Quedarte" + (w === "quedarse" ? " (gana)" : ""), value: r.costeQuedarse, color: "a" }, { label: "Cambiar ya" + (w === "cambiar" ? " (gana)" : ""), value: r.costeCambiar, color: "b" }, { label: "Esperar y cambiar" + (w === "esperar" ? " (gana)" : ""), value: r.costeEsperar, color: "c" }],
    cols: ["Quedarte", "Cambiar ya", "Esperar"],
    rows: [
      ["Coste total en " + meses, eur(r.costeQuedarse), eur(r.costeCambiar), eur(r.costeEsperar)],
      ["Ahorro frente a quedarte", "—", eur(r.ahorroCambiar), eur(r.ahorroEsperar)],
      { label: "Mes en que cambiar ya recupera la penalización y el alta", values: [r.mesEq > 0 ? EM.num(r.mesEq, 0) : "no llega", "", ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
