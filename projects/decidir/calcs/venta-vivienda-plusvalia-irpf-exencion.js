// Venta de vivienda: ganancia patrimonial, exencion (art. 33.4.b y 38 LIRPF) y cuota por la escala del ahorro (ejercicio 2026). Parametros: data/params.json -> venta_vivienda_2026 e irpf_2026.escala_ahorro_mitad (fuentes y fechas alli).
// Escala de UNA mitad (art. 66.1 estatal; la autonomica del art. 76 es igual): [desde, cuota integra acumulada, tipo %]; el total es el doble.
var P = { tab: [[0, 0, 9.5], [6000, 570, 10.5], [50000, 5190, 11.5], [200000, 22440, 13.5], [300000, 35940, 15]] };
function escala(x) {
  if (x <= 0) return 0;
  for (var i = P.tab.length - 1; i >= 0; i--) if (x > P.tab[i][0]) return 2 * (P.tab[i][1] + (x - P.tab[i][0]) * P.tab[i][2] / 100);
  return 0;
}
// Cuota de la ganancia no exenta `b` sobre otras rentas del ahorro `o`: escala(o + b) - escala(o).
function cuotaDe(o, b) { return escala(o + b) - escala(o); }
function calcular(d) {
  var cero = { invalido: 1, transmision: 0, adquisicion: 0, ganancia: 0, exenta: 0, base: 0, cuota: 0, neto: 0, necesaria: 0, cuotaSin: 0, cuotaTotal: 0, ratio: 0, tipoMedio: 0 };
  var trans = d.venta - d.gventa, adq = d.adq + d.gcomp, g = trans - adq, obt = trans - d.hipoteca;
  if (d.hipoteca > trans || d.venta < 0 || d.adq < 0 || d.gventa < 0 || d.hipoteca < 0 || d.reinv < 0 || d.otras < 0) return cero;
  var pos = Math.max(g, 0), ex = 0, ratio = 0;
  if (pos > 0 && d.sit === "hab65") { ex = pos; ratio = 1; }
  else if (pos > 0 && d.sit === "hab") { ratio = obt <= 0 ? 1 : Math.min(1, d.reinv / obt); ex = pos * ratio; }
  var base = pos - ex, cuota = cuotaDe(d.otras, base), cuotaSin = cuotaDe(d.otras, pos);
  return { invalido: 0, transmision: trans, adquisicion: adq, ganancia: g, exenta: ex, base: base, cuota: cuota, neto: d.venta - d.gventa - d.hipoteca - cuota,
    necesaria: d.sit === "hab" && pos > 0 ? Math.max(obt, 0) : 0, cuotaSin: cuotaSin, cuotaTotal: 0, ratio: ratio, tipoMedio: base > 0 ? cuota / base * 100 : 0 };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["venta", "adq", "gcomp", "gventa", "hipoteca", "reinv", "otras"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.sit = document.getElementById("sit").value; return d;
}
function pintar() {
  var d = leer();
  var r = calcular(d);
  if (r.invalido) {
    EM.renderResult({ winner: "inv", tone: "warn", verdict: "Estos datos no encajan: la hipoteca pendiente no puede superar lo que te queda de la venta (precio menos gastos de venta) y ningún importe puede ser negativo (solo los gastos de compra y mejoras, menos amortizaciones, admiten un signo menos).",
      note: "<p><strong>Qué hacer:</strong> revisa el principal pendiente de la hipoteca de esa vivienda y los gastos de venta.</p>" });
    return;
  }
  var verdict, winner, tone = "ok";
  if (r.ganancia <= 0) {
    winner = r.ganancia < 0 ? "perdida" : "cero"; tone = "ok";
    verdict = r.ganancia < 0
      ? "Con estos datos vendes con una pérdida patrimonial de " + eur(-r.ganancia) + ": no pagas IRPF por esta venta (esta herramienta no calcula la compensación de la pérdida con otras ganancias del ahorro) y te quedan " + eur(r.neto) + " tras gastos y cancelar la hipoteca."
      : "Con estos datos la venta no deja ganancia ni pérdida: no pagas IRPF y te quedan " + eur(r.neto) + " tras gastos y cancelar la hipoteca.";
  } else if (d.sit === "hab65") {
    winner = "exenta65"; verdict = "Con estos datos la ganancia de " + eur(r.ganancia) + " queda exenta por transmitir tu vivienda habitual con 65 años o más (o con dependencia severa o gran dependencia): no pagas IRPF y te quedan " + eur(r.neto) + " tras gastos y cancelar la hipoteca, sin necesidad de reinvertir.";
  } else if (d.sit === "nohab") {
    winner = "tributa"; tone = "warn"; verdict = "Con estos datos la vivienda no era tu habitual (ni lo fue en los dos años anteriores a vender), así que no hay exención por reinversión: la ganancia de " + eur(r.ganancia) + " tributa en la base del ahorro y pagas unos " + eur(r.cuota) + " de IRPF (tipo medio del " + EM.num(r.tipoMedio, 1) + " %); te quedan " + eur(r.neto) + " tras gastos, hipoteca e impuesto.";
  } else if (r.base <= 0.005) {
    winner = "total"; verdict = "Con estos datos, si reinviertes " + eur(r.necesaria) + " o más en tu nueva vivienda habitual dentro del plazo, la ganancia de " + eur(r.ganancia) + " queda excluida de gravamen: no pagas IRPF y te quedan " + eur(r.neto) + " tras gastos y cancelar la hipoteca (sin reinvertir, pagarías unos " + eur(r.cuotaSin) + ").";
  } else if (d.reinv > 0) {
    winner = "parcial"; tone = "warn"; verdict = "Con estos datos, reinvertir " + eur(d.reinv) + " excluye solo " + EM.num(r.ratio * 100, 1) + " % de la ganancia (" + eur(r.exenta) + "): tributan " + eur(r.base) + " y pagas unos " + eur(r.cuota) + " de IRPF; para no pagar nada tendrías que reinvertir " + eur(r.necesaria) + " o más. Te quedan " + eur(r.neto) + " tras gastos, hipoteca e impuesto.";
  } else {
    winner = "tributa"; tone = "warn"; verdict = "Con estos datos y sin reinvertir en otra vivienda habitual pagas unos " + eur(r.cuota) + " de IRPF por la ganancia de " + eur(r.ganancia) + " (tipo medio del " + EM.num(r.tipoMedio, 1) + " %); si reinviertes " + eur(r.necesaria) + " o más en los dos años siguientes (o los dos anteriores) no pagas nada. Te quedan " + eur(r.neto) + " tras gastos, hipoteca e impuesto.";
  }
  var pos = Math.max(r.ganancia, 0), rows = [
    { label: "Ganancia patrimonial (venta menos gastos de venta, menos compra, gastos y mejoras)", values: [eur(r.ganancia), "—", "—"] },
    { label: "Sin exención", values: [eur(pos), eur(r.cuotaSin), eur(d.venta - d.gventa - d.hipoteca - r.cuotaSin)] },
    { label: "Con tu situación" + (d.sit === "hab" ? " (reinversión de " + eur(d.reinv) + ")" : ""), values: [eur(r.base), eur(r.cuota), eur(r.neto)], strong: true }
  ];
  if (d.sit === "hab" && pos > 0) rows.push({ label: "Reinvirtiendo todo (" + eur(r.necesaria) + ")", values: [eur(0), eur(0), eur(d.venta - d.gventa - d.hipoteca)] });
  var note = '<p><strong>Reinversión:</strong> ' + (d.sit === "hab" && pos > 0
    ? 'para excluir toda la ganancia hay que reinvertir al menos <strong>' + eur(r.necesaria) + '</strong> (precio de venta menos gastos de venta y menos el principal pendiente de la hipoteca de esa vivienda); cada 10.000 € reinvertidos excluyen ' + eur(pos * 10000 / r.necesaria) + ' de ganancia. Plazo: dos años desde la venta, o dentro de los dos años anteriores. Si no lo reinviertes todo, solo se excluye la parte proporcional.'
    : 'solo aplica si vendes tu vivienda habitual (cuenta lo que pagas por la nueva aunque la financies con hipoteca); con 65 años o más (o dependencia severa) la ganancia de la vivienda habitual está exenta sin reinvertir.') + '</p>';
  note += '<p><strong>Límites:</strong> el cálculo usa la escala del ahorro (19 % a 30 %, estatal más autonómica) sobre la ganancia no exenta y tus otras rentas del ahorro, y supone que tu base general absorbe el mínimo personal y familiar (si tienes pocas rentas, pagarías algo menos). Si compraste antes del 31/12/1994 y la ganancia no está exenta, la disposición transitoria 9.ª puede reducir la parte generada hasta el 19/1/2006 (coeficientes de abatimiento): no se calcula, así que el impuesto real sería igual o menor. No incluye la plusvalía municipal (IIVTNU) salvo que la pagaste tú y la metas en los gastos de venta, no residentes (tributan por el IRNR), deducción del 60 % de Ceuta y Melilla (art. 68.4), venta de vivienda desocupada a entes públicos (DA 65.ª, RDL 26/2026, pendiente de convalidación), renta vitalicia de mayores de 65 años (art. 38.3, máximo 240.000 €), subrogación de hipoteca, herencias o donaciones, vivienda ganancial en pareja, ni País Vasco y Navarra.</p>';
  EM.renderResult({
    winner: winner, verdict: verdict, tone: tone,
    bigNumber: r.cuota, bigLabel: "de IRPF estimado por la venta", format: EM.eur,
    barsLabel: "De la ganancia a lo que tributa", bars: [{ label: "Ganancia exenta", value: r.exenta, color: "a" }, { label: "Ganancia que tributa", value: r.base, color: "b" }],
    cols: ["Ganancia que tributa", "IRPF estimado", "Neto en mano"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
