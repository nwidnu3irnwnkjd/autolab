// Gastos del alquiler de vivienda: quien paga y cuanto puede subir lo repercutido (LAU art. 20.1-3, 21.4, 17.6). Parametros y fuentes: data/params.json -> gastos_alquiler_2026.
var P = {"mult": 2, "aniosPf": 5, "aniosPj": 7};
// Pacto valido (art. 20.1): escrito Y con importe anual a la fecha del contrato (pacto "ok"). Si no, comunidad, IBI y basuras son del arrendador.
// Con pacto valido: la comunidad solo sube, dentro de los 5/7 primeros anos, hasta P.mult veces el % maximo de subida de la renta (art. 20.2); IBI y basuras (tributos) no tienen ese tope.
// Gestion inmobiliaria y formalizacion: del arrendador siempre (art. 20.1, vivienda): lo cobrado al inquilino es rechazable.
function calcular(d) {
  var valido = d.pacto === "ok";
  var tope = Math.max(0, P.mult * d.subidaRenta);
  var limitado = valido && d.tramo === "dentro";
  var sinAcuerdo = d.acuerdo === "no";   // art. 20.2: dentro de 5/7 anos la suma solo sube POR ACUERDO (una clausula de revision lo es por anticipado)
  var pct = valido ? (limitado ? (sinAcuerdo ? 0 : Math.min(d.subidaPedida, tope)) : d.subidaPedida) : 0;
  var comPed = d.comunidad * (1 + d.subidaPedida / 100);
  var comLey = valido ? d.comunidad * (1 + pct / 100) : 0;
  var ibiLey = valido ? d.ibi : 0, basLey = valido ? d.basuras : 0;
  var pedido = comPed + d.ibi + d.basuras + d.honorarios;
  var ley = comLey + ibiLey + basLey;
  return { topePct: tope, pctLegal: pct, limitado: limitado ? 1 : 0, comunidadPedida: comPed, comunidadLegal: comLey, excesoComunidad: comPed - comLey,
    ibiRechazable: d.ibi - ibiLey, basurasRechazable: d.basuras - basLey, honorariosRechazable: d.honorarios, pedido: pedido, tuCargo: ley, rechazable: pedido - ley };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["comunidad", "ibi", "subidaPedida", "subidaRenta", "honorarios"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.basuras = 0; d.acuerdo = document.getElementById("acuerdo").value; d.pacto = document.getElementById("pacto").value; d.tramo = document.getElementById("tramo").value; return d;
}
function pintar() {
  var d = leer();
  if (d.comunidad < 0 || d.ibi < 0 || d.subidaPedida < 0 || d.subidaRenta < 0 || d.honorarios < 0) return;
  var r = calcular(d), no = r.rechazable, valido = d.pacto === "ok";
  var piezas = [];
  if (!valido) {
    var g = r.excesoComunidad + r.ibiRechazable + r.basurasRechazable;
    if (g > 0.005) piezas.push(EM.eur(g) + " de comunidad, IBI y basuras, que sin pacto escrito con importe anual son del casero (art. 20.1)");
  } else if (r.excesoComunidad > 0.005) piezas.push(d.tramo === "dentro" && d.acuerdo === "no" ? EM.eur(r.excesoComunidad) + " de subida de la comunidad que no has aceptado ni prevé tu contrato (art. 20.2)" : EM.eur(r.excesoComunidad) + " de subida de la comunidad por encima del doble del % en que puede subir tu renta, " + EM.num(r.topePct, 2) + " % (art. 20.2)");
  if (r.honorariosRechazable > 0.005) piezas.push(EM.eur(r.honorariosRechazable) + " de honorarios de agencia (pago único), que son del casero (art. 20.1)");
  var verdict = no > 0.005
    ? 'Con tus datos, te repercuten ' + EM.eur(r.pedido) + ' este año y la ley te obliga a pagar ' + EM.eur(r.tuCargo) + ': puedes rechazar ' + EM.eur(no) + ' (' + piezas.join("; ") + ').'
    : 'Con tus datos, lo que te repercuten (' + EM.eur(r.pedido) + ' este año) es lo que la ley te obliga a pagar: no hay nada que rechazar por estas reglas.';
  var rows = [
    { label: "Comunidad (con la subida pedida)", values: [EM.eur(r.comunidadPedida), EM.eur(r.comunidadLegal), EM.eur(r.excesoComunidad)] },
    { label: "IBI y tasa de basuras", values: [EM.eur(d.ibi), EM.eur(valido ? d.ibi : 0), EM.eur(r.ibiRechazable)] },
    { label: "Honorarios de agencia y formalización (pago único)", values: [EM.eur(d.honorarios), EM.eur(0), EM.eur(r.honorariosRechazable)] },
    { label: "Total este año", values: [EM.eur(r.pedido), EM.eur(r.tuCargo), EM.eur(no)], strong: true }
  ];
  var note = '<p><strong>El pacto:</strong> ' + (valido
    ? 'tu contrato recoge por escrito el reparto con su importe anual, así que pagas comunidad, IBI y basuras (art. 20.1).'
    : (d.pacto === "sinimp" ? 'el pacto escrito sin el importe anual a la fecha del contrato no es válido: los gastos generales los paga el casero (art. 20.1).' : 'sin pacto escrito, los gastos generales los paga el casero (art. 20.1).')) + '</p>';
  if (valido) note += '<p><strong>Tu límite de subida:</strong> ' + (d.tramo === "dentro"
    ? 'la comunidad solo puede subir si lo acordáis (o lo prevé tu contrato) y nunca más del doble del % en que puede subir tu renta: ' + EM.num(r.topePct, 2) + ' % (el doble de ' + EM.num(d.subidaRenta, 2) + ' %)' + (d.acuerdo === "no" ? '. Como no lo has aceptado ni lo prevé tu contrato, no sube este año' : '') + '; los tributos (IBI y basuras) no tienen ese tope. Rige durante los ' + EM.num(P.aniosPf) + ' primeros años de vigencia, prórrogas incluidas (' + EM.num(P.aniosPj) + ' si el casero es persona jurídica, no un autónomo).'
    : 'pasados los ' + EM.num(P.aniosPf) + ' primeros años (' + EM.num(P.aniosPj) + ' con casero persona jurídica) el art. 20.2 ya no limita la subida: manda lo que pactasteis.') + '</p>';
  note += '<p><strong>Siempre tuyo:</strong> los suministros con contador (luz, agua, gas) y las pequeñas reparaciones por el uso ordinario (arts. 20.3 y 21.4). Las reparaciones necesarias para la habitabilidad son del casero sin subir la renta, salvo que el daño sea imputable al inquilino (art. 21.1).</p>';
  note += '<p><strong>Otros gastos:</strong> si el contrato te traslada por escrito y con importe otro gasto general que no sea un tributo (por ejemplo, el seguro), súmalo a la comunidad: el tope se aplica a la suma.</p>';
  note += '<p><strong>Lo que no calcula:</strong> contratos anteriores a 2019 o a mayo de 2023, uso distinto de vivienda, derramas extraordinarias, recibos de basuras que no sean un tributo, normativa foral o autonómica, y en zona tensionada (art. 17.6) que un contrato nuevo no puede añadir gastos que no estuvieran en el anterior.</p>';
  EM.renderResult({
    winner: (no > 0.005 ? "n" : "ok") + (valido ? "v" : "i") + (r.excesoComunidad > 0.005 ? "c" : "") + (r.honorariosRechazable > 0.005 ? "h" : ""), verdict: verdict, tone: no > 0.005 ? "warn" : "ok",
    bigNumber: no, bigLabel: "que puedes rechazar este año", format: EM.eur,
    barsLabel: "Lo que te repercuten frente a lo que la ley te obliga a pagar", bars: [{ label: "Te repercuten", value: r.pedido, color: "a" }, { label: "La ley te obliga", value: r.tuCargo, color: "b" }],
    cols: ["Te repercuten", "La ley te obliga", "Puedes rechazar"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
