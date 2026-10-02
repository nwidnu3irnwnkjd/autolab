// Prorrogar o firmar contrato nuevo de alquiler (reduccion IRPF del casero). Parametros: data/params.json -> alquiler_irpf_2026 (fuentes y fechas alli).
var P = {"antes": 60, "general": 50, "rehab": 60, "tensionada": 90, "rebajaMin": 5, "holguraRehab": 10};
// Resultado anual despues de IRPF con renta mensual R, gastos g (incluida amortizacion), reduccion p (%) y tipo t (%).
function liquidar(R, g, p, t) {
  var ing = 12 * R, prev = ing - g, red = prev > 0 ? prev * (1 - p / 100) : prev, cuota = Math.max(red, 0) * t / 100;
  return { ing: ing, prev: prev, cuota: cuota, res: ing - g - cuota };
}
// Renta mensual con la que, con la reduccion p, el resultado iguala a T (despeje exacto por tramos).
function rentaEq(T, g, p, t) {
  var k = t / 100 * (1 - p / 100), x = T > 0 ? T / (1 - k) : T;
  return Math.max(0, (x + g) / 12);
}
function calcular(d) {
  var R0 = d.renta0, R1 = d.renta1, g = d.gastos, t = d.tipo, tens = d.tensionada === "si", exc = d.excepcion176, reh = exc === "rehab";
  var pA = d.fecha === "antes" ? P.antes : d.fecha === "reconduccion" ? P.general : Number(d.pctActual);
  var limite = R0 * (exc !== "ninguna" ? 1 + P.holguraRehab / 100 : 1);
  var incumple = tens && R1 - limite > 1e-9;
  var rebajaOk = tens && (R0 - R1) * 100 - P.rebajaMin * R0 > 1e-9;
  var pB = incumple ? 0 : rebajaOk ? P.tensionada : reh ? P.rehab : P.general;
  var a = liquidar(R0, g, pA, t), b = liquidar(R1, g, pB, t), dif = b.res - a.res, gran = Math.max(Math.abs(a.res), Math.abs(b.res));
  var gana = gran === 0 || Math.abs(dif) - gran * 0.05 < -1e-9 ? 0 : dif > 0 ? 2 : 1;
  var r90 = rentaEq(a.res, g, P.tensionada, t);
  return { noModelado: 0, pctA: pA, pctB: pB, prevA: a.prev, prevB: b.prev, cuotaA: a.cuota, cuotaB: b.cuota, resA: a.res, resB: b.res, dif: dif, gana: gana,
    incumple: incumple ? 1 : 0, rebajaOk: rebajaOk ? 1 : 0, limite176: tens ? limite : -1, rentaEq: rentaEq(a.res, g, pB, t), r90: r90,
    rebajaMax90: R0 > 0 ? Math.max(0, (1 - r90 / R0) * 100) : 0 };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["renta0", "renta1", "gastos", "tipo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["fecha", "pctActual", "tensionada", "excepcion176"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.renta0 <= 0 || d.renta1 < 0 || d.gastos < 0 || d.tipo < 0 || d.tipo > 100) return;
  var r = calcular(d), antes = d.fecha === "antes", recon = d.fecha === "reconduccion", verdict;
  var pa = EM.num(r.pctA) + " %", pb = EM.num(r.pctB) + " %";
  if (r.incumple) {
    verdict = 'Con estos datos, en zona tensionada la renta del contrato nuevo (' + EM.eur(d.renta1) + ' al mes) supera el límite de ' + EM.eur(r.limite176) + ' del art. 17.6 de la Ley de Arrendamientos Urbanos' + (d.excepcion176 === 'ninguna' ? ': ese contrato incumple, salvo que acredites una de las excepciones del art. 17.6 (rehabilitación, eficiencia energética, accesibilidad o contrato de 10 años o más), y además pierdes toda reducción en el IRPF (art. 23.2).' : ' (la última renta más el 10 % de tu excepción): ese contrato incumple y pierdes toda reducción en el IRPF (art. 23.2).') + ' Con una renta de hasta ' + EM.eur(r.limite176) + ' al mes, firmarlo te dejaría la reducción que corresponda; prorrogar te deja ' + EM.eur(r.resA) + ' al año después de IRPF.';
  } else if (r.gana === 0) {
    verdict = 'Con tus datos, empate práctico: prorrogar (reducción del ' + pa + ') te deja ' + EM.eur(r.resA) + ' al año después de IRPF y firmar uno nuevo (' + pb + '), ' + EM.eur(r.resB) + ', una diferencia de ' + EM.eur(Math.abs(r.dif)) + '.';
  } else if (r.gana === 1) {
    verdict = 'Con tus datos, gana prorrogar por ' + EM.eur(-r.dif) + ' al año: te quedan ' + EM.eur(r.resA) + ' con la reducción del ' + pa + ' frente a ' + EM.eur(r.resB) + ' con un contrato nuevo (' + pb + ').';
  } else {
    verdict = 'Con tus datos, gana firmar el contrato nuevo por ' + EM.eur(r.dif) + ' al año: te quedan ' + EM.eur(r.resB) + ' con la reducción del ' + pb + ' frente a ' + EM.eur(r.resA) + ' si prorrogas (' + pa + ').';
  }
  var rows = [
    { label: "Prorrogar el contrato (reducción del " + pa + ")", values: [EM.eur(r.prevA), EM.eur(r.cuotaA), EM.eur(r.resA)], strong: r.gana === 1 },
    { label: "Firmar contrato nuevo (reducción del " + pb + ")", values: [EM.eur(r.prevB), EM.eur(r.cuotaB), EM.eur(r.resB)], strong: r.gana === 2 }
  ];
  var note = '';
  if (!r.incumple) note += '<p><strong>Umbral:</strong> con la reducción del contrato nuevo (' + pb + '), firmarlo compensa a partir de una renta de <strong>' + EM.eur(r.rentaEq) + ' al mes</strong> (' + (d.renta1 >= r.rentaEq ? 'tu renta nueva la supera' : 'tu renta nueva no llega') + ').</p>';
  if (d.tensionada === "si") note += '<p><strong>Zona tensionada:</strong> el límite de renta del contrato nuevo es ' + EM.eur(r.limite176) + ' al mes (art. 17.6 de la Ley de Arrendamientos Urbanos). Para el 90 % la renta inicial tiene que bajar más del 5 % respecto a la última; con esa reducción compensa bajar hasta un <strong>' + EM.num(r.rebajaMax90, 1) + ' %</strong> (renta mínima ' + EM.eur(r.r90) + ' al mes) frente a prorrogar.</p>';
  note += '<p><strong>Supuesto propio (confianza media):</strong> ' + (antes ? 'el 60 % de un contrato anterior al 26/5/2023 vale solo para la prórroga de los arts. 9 y 10 de la Ley de Arrendamientos Urbanos (incluida la extraordinaria del art. 10.2), porque es el mismo contrato y la disposición transitoria 38.ª se refiere a los contratos celebrados antes de esa fecha; no hay consulta de la Dirección General de Tributos que lo confirme. Si ya agotaste esas prórrogas y sigues por tácita reconducción (art. 1566 del Código Civil), o firmas un documento nuevo, puede aplicarse el 50 %: elige esa opción en la fecha del contrato.' : recon ? 'con tácita reconducción (art. 1566 del Código Civil) o un documento nuevo se considera un contrato nuevo y se aplica el 50 %; el 60 % de los contratos anteriores al 26/5/2023 vale solo para la prórroga de los arts. 9 y 10 de la Ley de Arrendamientos Urbanos.' : 'prorrogar (arts. 9 y 10 de la Ley de Arrendamientos Urbanos) conserva la reducción de tu contrato actual: los requisitos se miran al celebrarlo y la reducción sigue mientras se cumplan (art. 23.2).') + ' Un contrato nuevo con el mismo inquilino cuenta como contrato nuevo. Mientras dure la prórroga obligatoria, firmar uno nuevo exige el acuerdo del inquilino (arts. 9.1 y 10.1).</p>';
  note += '<p><strong>Límites:</strong> la vivienda ya está alquilada, así que el 70 % de «primera vez» a un joven no está disponible; no se modelan el 70 % de alquiler social o programa público (si te aplica, el contrato nuevo sube a ese 70 %) ni al gran tenedor, y el gasto incluye la amortización (que no sale de tu cuenta). Hay 12 meses de renta, sin actualización ni vacíos.</p>';
  EM.renderResult({
    winner: r.incumple ? "incumple" : r.gana === 1 ? "prorrogar" : r.gana === 2 ? "nuevo" : "empate", verdict: verdict, tone: r.incumple ? "warn" : "ok",
    bigNumber: Math.abs(r.dif), bigLabel: r.gana === 0 ? "de diferencia al año" : r.gana === 1 ? "al año más si prorrogas" : "al año más si firmas nuevo", format: EM.eur,
    barsLabel: "Resultado al año después de IRPF", bars: [{ label: "Prorrogar", value: Math.max(r.resA, 0), color: "a" }, { label: "Contrato nuevo", value: Math.max(r.resB, 0), color: "b" }],
    cols: ["Rendimiento neto", "IRPF", "Te queda al año"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
