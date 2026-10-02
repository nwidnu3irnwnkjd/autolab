// Residencia o cuidador a domicilio: coste mensual de cada opcion y horas diarias de equilibrio.
// Domicilio = horas x coste/hora x (1 + cotizacion) x 365/12 + adaptacion/(anios x 12) + valor del cuidado familiar - ayudas; residencia = cuota - ayudas.
// Las ayudas (input) se restan a ambas opciones. ganador: 0 domicilio, 1 residencia, 2 empate.
function calcular(d) {
  var tarifa = d.costeh * (1 + d.cotiz / 100) * 365 / 12;
  var cuid = d.horas * tarifa, adapt = d.adapt / (d.anios * 12);
  var resi = d.resi - d.ayudas, dom = cuid + adapt + d.fam - d.ayudas, domEf = cuid + adapt - d.ayudas;
  var eq = tarifa > 0 ? Math.max(0, (d.resi - adapt - d.fam) / tarifa) : -1;
  var g = dom < resi - 0.005 ? 0 : (dom > resi + 0.005 ? 1 : 2);
  return { cuidadorMes: cuid, adaptMes: adapt, costeResi: resi, costeDom: dom, costeDomEfectivo: domEf,
    diferencia: resi - dom, horasEquilibrio: eq, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["resi", "horas", "costeh", "cotiz", "adapt", "anios", "fam", "ayudas"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.horas > 24) {
    EM.renderResult({ winner: "invalido", verdict: "Un día solo tiene 24 horas: revisa las horas diarias de cuidado.", tone: "warn", note: "<p>Si necesita atención continua, consulta con los servicios sociales cómo se organiza un cuidado de 24 horas.</p>" });
    return;
  }
  if (d.anios < 1 || d.anios > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica entre 1 y 30 años para repartir el gasto de adaptación.", tone: "warn", note: "<p>Usa el tiempo que prevés vivir en la vivienda adaptada.</p>" });
    return;
  }
  if (d.cotiz > 100) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el porcentaje de cotización: no puede pasar de 100.", tone: "warn", note: "<p>Consulta el porcentaje que corresponde a tu caso en la Seguridad Social.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, w, verdict, tone = "ok", dif = Math.abs(r.diferencia);
  if (g === 0) {
    w = "domicilio";
    verdict = "Con estos datos el cuidado a domicilio cuesta " + eur(r.costeDom) + " al mes frente a " + eur(r.costeResi) + " de la residencia, " + eur(dif) + " menos. Esto cambiaría si necesitaras más de " + EM.num(r.horasEquilibrio, 1) + " horas de cuidador al día.";
  } else if (g === 1) {
    w = "residencia";
    verdict = "Con estos datos la residencia cuesta " + eur(r.costeResi) + " al mes frente a " + eur(r.costeDom) + " del cuidado a domicilio, " + eur(dif) + " menos. " + (r.horasEquilibrio > 0 ? "El domicilio saldría más barato por debajo de " + EM.num(r.horasEquilibrio, 1) + " horas de cuidador al día." : "El domicilio no saldría más barato ni con cero horas de cuidador, por el coste de adaptación y del cuidado familiar.");
  } else {
    w = "empate"; tone = "warn";
    verdict = "Con estos datos las dos opciones cuestan lo mismo al mes (" + eur(r.costeResi) + ").";
  }
  var note = "<p><strong>Solo coste, no recomendación:</strong> esta comparación mide dinero, no la atención, la seguridad ni el bienestar de la persona, que son lo principal en esta decisión. ";
  if (r.horasEquilibrio >= 0) note += "El equilibrio está en <strong>" + EM.num(r.horasEquilibrio, 1) + " horas de cuidador al día</strong>. ";
  note += "El coste de oportunidad del cuidado familiar (" + eur(d.fam) + " al mes) es un valor que pones tú; sin contarlo, el domicilio cuesta " + eur(r.costeDomEfectivo) + " al mes en dinero efectivo.</p>";
  note += "<p><strong>No incluye:</strong> la Ley de Dependencia ni ninguna prestación o ayuda concreta (las ayudas que pongas se restan por igual de las dos opciones; consulta qué corresponde a tu caso en los servicios sociales de tu comunidad), cifras legales de cotización (consulta a la Seguridad Social o a un gestor), sustitución por vacaciones o bajas, ni consejo sanitario o legal.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: r.horasEquilibrio >= 0 ? r.horasEquilibrio : undefined, bigLabel: "horas de cuidador al día en las que ambas opciones igualan su coste", format: function (x) { return EM.num(x, 1); },
    barsLabel: "Coste mensual",
    bars: [{ label: "Cuidador a domicilio" + (w === "domicilio" ? " (menor)" : ""), value: Math.max(r.costeDom, 0), color: "a" }, { label: "Residencia" + (w === "residencia" ? " (menor)" : ""), value: Math.max(r.costeResi, 0), color: "b" }],
    cols: ["A domicilio", "Residencia"],
    rows: [
      ["Cuidador con cotización", eur(r.cuidadorMes), "—"],
      ["Adaptación de la vivienda (repartida)", eur(r.adaptMes), "—"],
      ["Cuidado familiar (coste de oportunidad)", eur(d.fam), "—"],
      ["Ayudas que restas", eur(-d.ayudas), eur(-d.ayudas)],
      { label: "Coste mensual", values: [eur(r.costeDom), eur(r.costeResi)], strong: true },
      ["Coste mensual en dinero efectivo", eur(r.costeDomEfectivo), eur(r.costeResi)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
