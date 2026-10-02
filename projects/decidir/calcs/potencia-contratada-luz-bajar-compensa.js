// Bajar la potencia contratada de la luz (2.0TD): ahorro anual del termino de potencia frente al riesgo de que salte el ICP y al coste del cambio.
// Ahorro = (kW actuales - kW nuevos) x EUR/kW y ano, mas Impuesto Electrico (5,11269632 % sobre el termino de potencia) e IVA 21 %.
// pico: la mayor potencia que usas a la vez (kW; dato tuyo). Si pico > kW nuevos, bajar a esa potencia puede hacer saltar el ICP.
// estado: 0 compensa, 1 riesgo (pico > kW nuevos), 2 el coste del cambio no se recupera en el horizonte, 3 no es una bajada. ganador: 0 bajar, 1 mantener, 2 empate.
var L = { iee: 0.0511269632, iva: 0.21 };
function conImp(x) { return x * (1 + L.iee) * (1 + L.iva); }
function calcular(d) {
  var f = conImp(1), baja = d.kwActual - d.kwNuevo, ahorro = baja > 0 ? baja * d.eurKw * f : 0;
  var neto = ahorro * d.anos - d.costeCambio, minimo = d.pico, ahorroMin = Math.max(d.kwActual - d.pico, 0) * d.eurKw * f;
  var estado, ganador;
  if (ahorro <= 0) { estado = 3; ganador = 1; }
  else if (d.pico > d.kwNuevo) { estado = 1; ganador = 1; }
  else if (Math.abs(neto) < 1) { estado = 2; ganador = 2; }
  else if (neto < 0) { estado = 2; ganador = 1; }
  else { estado = 0; ganador = 0; }
  var anios = d.costeCambio <= 0 ? (ahorro > 0 ? 0 : -1) : (ahorro > 0 ? d.costeCambio / ahorro : -1);
  return { costeActual: conImp(d.kwActual * d.eurKw), costeNuevo: conImp(d.kwNuevo * d.eurKw), ahorroAnual: ahorro, ahorroNeto: neto,
    aniosAmort: anios, margen: d.kwNuevo - d.pico, ahorroMinimo: ahorroMin, pctBaja: d.kwActual > 0 ? Math.max(baja, 0) / d.kwActual * 100 : 0,
    estado: estado, ganador: ganador };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["kwActual", "kwNuevo", "pico", "eurKw", "costeCambio", "anos"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.kwActual <= 0 || d.kwNuevo <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica la potencia que tienes ahora y la que quieres contratar (mayores que 0 kW).", tone: "warn", note: "<p>Los kW contratados figuran en tu factura, en «potencia contratada».</p>" });
    return;
  }
  if (d.anos < 1 || d.anos > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica un horizonte de entre 1 y 30 años.", tone: "warn", note: "<p>Es el tiempo durante el que repartes el coste del cambio.</p>" });
    return;
  }
  var r = calcular(d), an = EM.num(d.anos, d.anos % 1 ? 1 : 0) + (d.anos === 1 ? " año" : " años"), v, w, tone = "ok";
  if (r.estado === 3) {
    w = "mantener"; tone = "warn";
    v = "Con estos datos no hay ahorro (de " + EM.num(d.kwActual, 2) + " a " + EM.num(d.kwNuevo, 2) + " kW), así que no hay ahorro que calcular: pon en «kW nuevos» un valor menor que los actuales y un precio mayor que 0.";
  } else if (r.estado === 1) {
    w = "riesgo"; tone = "warn";
    v = "Con tu pico de " + EM.num(d.pico, 2) + " kW no compensa bajar a " + EM.num(d.kwNuevo, 2) + " kW: ahorrarías " + EM.eur(r.ahorroAnual) + " al año, pero tu consumo simultáneo supera la potencia nueva y el ICP puede saltar. Bajar solo hasta " + EM.num(d.pico, 2) + " kW (si ese pico es real) ahorraría " + EM.eur(r.ahorroMinimo) + " al año.";
  } else if (r.ganador === 2) {
    w = "empate"; tone = "warn";
    v = "Con estos datos bajar a " + EM.num(d.kwNuevo, 2) + " kW queda en tablas: el ahorro de " + an + " (" + EM.eur(r.ahorroAnual * d.anos) + ") iguala el coste del cambio (" + EM.eur(d.costeCambio) + ").";
  } else if (r.estado === 2) {
    w = "mantener"; tone = "warn";
    v = "Con estos datos no compensa bajar a " + EM.num(d.kwNuevo, 2) + " kW en " + an + ": ahorras " + EM.eur(r.ahorroAnual) + " al año y el cambio cuesta " + EM.eur(d.costeCambio) + ", se recupera en " + EM.num(r.aniosAmort, 1) + " años.";
  } else {
    w = "bajar";
    v = "Con estos datos compensa bajar a " + EM.num(d.kwNuevo, 2) + " kW: ahorras " + EM.eur(r.ahorroAnual) + " al año con impuestos" + (d.costeCambio > 0 ? " y, descontado el coste del cambio, " + EM.eur(r.ahorroNeto) + " en " + an : "") + ", si tu pico real de " + EM.num(d.pico, 2) + " kW es cierto.";
  }
  var note = "<p><strong>Lectura:</strong> el término de potencia con impuestos pasa de " + EM.eur(r.costeActual) + " al año con " + EM.num(d.kwActual, 2) + " kW a " + EM.eur(r.costeNuevo) + " con " + EM.num(d.kwNuevo, 2) + " kW" + (r.ahorroAnual > 0 ? " (un " + EM.num(r.pctBaja, 0) + " % menos de potencia)" : "") + ". ";
  if (d.pico <= d.kwNuevo && r.ahorroAnual > 0) note += "Tu margen sobre el pico es de " + EM.num(r.margen, 2) + " kW" + (r.margen < 0.5 ? ": es estrecho, y encender a la vez horno, placa y calefacción puede pasarlo" : "") + ". ";
  if (r.aniosAmort > 0 && d.costeCambio > 0) note += "El coste del cambio se recupera en <strong>" + EM.num(r.aniosAmort, 1) + " años</strong>. ";
  note += "</p><p><strong>Cómo sacar el pico:</strong> mira en la web o app de tu distribuidora el maxímetro o la curva de carga (te lo da quien lee tu contador) y pon la mayor potencia que usaste a la vez; si no lo tienes, suma la potencia de lo que encenderías a la vez en tu peor momento. El valor por defecto es un ejemplo, no un dato tuyo.</p>" +
    "<p><strong>No incluye:</strong> el margen del término de potencia de tu comercializadora (el precio por defecto es solo la parte regulada de peajes y cargos: suma el de tu factura), las potencias normalizadas que ofrece tu distribuidora, los derechos y gastos de tramitación (pon en «coste del cambio» lo que te diga la distribuidora; el 0 por defecto no es un dato) ni que subir de nuevo la potencia después puede costar más. Se supone la misma potencia en los dos periodos de potencia de la 2.0TD y el IEE sin su mínimo por kWh. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: tone,
    bigNumber: r.ahorroAnual, bigLabel: "al año con impuestos si bajas a " + EM.num(d.kwNuevo, 2) + " kW", format: EM.eur,
    barsLabel: "Término de potencia al año (con impuestos)",
    bars: [{ label: "Con " + EM.num(d.kwActual, 2) + " kW", value: r.costeActual, color: "a" }, { label: "Con " + EM.num(d.kwNuevo, 2) + " kW", value: r.costeNuevo, color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Ahorro anual", EM.eur(r.ahorroAnual)],
      ["Ahorro en " + an, EM.eur(r.ahorroAnual * d.anos)],
      ["Coste del cambio", EM.eur(d.costeCambio)],
      { label: "Ahorro neto en " + an, values: [EM.eur(r.ahorroNeto)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
