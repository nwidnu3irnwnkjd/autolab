// Gastos del alquiler de vivienda: quien paga y cuanto puede subir lo repercutido (LAU art. 20, 21.4, 17.6; RDL 29/2026, en vigor desde el 8-10-2026, pendiente de convalidacion). Parametros y fuentes: data/params.json -> gastos_alquiler_2026.
var P = {"mult": 2, "aniosPf": 5, "aniosPj": 7};
// Pacto valido (art. 20.1): escrito Y con importe anual a la fecha del contrato (pacto "ok"). Si no, comunidad, IBI y basuras son del arrendador.
// Con pacto valido: la comunidad solo sube, dentro de los 5/7 primeros anos, hasta P.mult veces el % maximo de subida de la renta (art. 20.2); IBI y basuras (tributos) no tienen ese tope.
// Gestion inmobiliaria y formalizacion: del arrendador siempre (art. 20.1, vivienda): lo cobrado al inquilino es rechazable.
// Contrato firmado desde el 8-10-2026 (d.firma === "despues"; supuesto S, confianza B, sin transitoria expresa: CC art. 2.3; la lectura contraria aplicaria el art. 20 a los recibos posteriores al 8-10 de contratos anteriores): el IBI no se puede repercutir al inquilino (art. 20.1 nuevo, salvo que sea el obligado tributario). La tasa de basuras suele tener como contribuyente al ocupante (TRLRHL 23.1.b y 23.2.a): se trata como repercutible; el input ibi solo recoge IBI y tasas cuyo obligado tributario es el propietario. La comunidad sigue con pacto valido y tope (art. 20.3 nuevo).
function calcular(d) {
  var valido = d.pacto === "ok";
  var nuevo = d.firma === "despues";
  var tope = Math.max(0, P.mult * d.subidaRenta);
  var limitado = valido && d.tramo === "dentro";
  var sinAcuerdo = d.acuerdo === "no";   // art. 20.2: dentro de 5/7 anos la suma solo sube POR ACUERDO (una clausula de revision lo es por anticipado)
  var pct = valido ? (limitado ? (sinAcuerdo ? 0 : Math.min(d.subidaPedida, tope)) : d.subidaPedida) : 0;
  var comPed = d.comunidad * (1 + d.subidaPedida / 100);
  var comLey = valido ? d.comunidad * (1 + pct / 100) : 0;
  var ibiLey = valido && !nuevo ? d.ibi : 0, basLey = valido ? d.basuras : 0;
  var pedido = comPed + d.ibi + d.basuras + d.honorarios;
  var ley = comLey + ibiLey + basLey;
  return { topePct: tope, pctLegal: pct, limitado: limitado ? 1 : 0, comunidadPedida: comPed, comunidadLegal: comLey, excesoComunidad: comPed - comLey,
    ibiRechazable: d.ibi - ibiLey, basurasRechazable: d.basuras - basLey, honorariosRechazable: d.honorarios, pedido: pedido, tuCargo: ley, rechazable: pedido - ley };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["comunidad", "ibi", "subidaPedida", "subidaRenta", "honorarios"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  var t = document.getElementById("tramo").value;   // fusiona 'años de contrato' y 'acuerdo de subida': dentro-si | dentro-no | fuera
  d.basuras = 0; d.pacto = document.getElementById("pacto").value; d.firma = document.getElementById("firma").value;
  d.tramo = t === "fuera" ? "fuera" : "dentro"; d.acuerdo = t === "dentro-no" ? "no" : "si"; return d;
}
function pintar() {
  var d = leer();
  if (d.comunidad < 0 || d.ibi < 0 || d.subidaPedida < 0 || d.subidaRenta < 0 || d.honorarios < 0) return;
  var r = calcular(d), no = r.rechazable, valido = d.pacto === "ok", nuevo = d.firma === "despues";
  var n20 = nuevo ? "20.3" : "20.2", nGest = nuevo ? "20.2" : "20.1";
  var piezas = [];
  if (!valido) {
    var g = r.excesoComunidad + r.ibiRechazable + r.basurasRechazable;
    if (g > 0.005) piezas.push(EM.eur(g) + (nuevo ? " de comunidad, IBI y tasas, que no puedes pagar: sin pacto escrito con importe anual la comunidad es del casero y, en contratos desde el 8-10-2026, el IBI (y las tasas de las que el obligado es el propietario) tampoco se repercute (art. 20)" : " de comunidad, IBI y basuras, que sin pacto escrito con importe anual son del casero (art. 20.1)"));
  } else if (r.excesoComunidad > 0.005) piezas.push(d.tramo === "dentro" && d.acuerdo === "no" ? EM.eur(r.excesoComunidad) + " de subida de la comunidad que no has aceptado ni prevé tu contrato (art. " + n20 + ")" : EM.eur(r.excesoComunidad) + " de subida de la comunidad por encima del doble del % en que puede subir tu renta, " + EM.num(r.topePct, 2) + " % (art. " + n20 + ")");
  if (valido && nuevo && r.ibiRechazable > 0.005) piezas.push(EM.eur(r.ibiRechazable) + " de IBI y tasas con el propietario como obligado tributario, que en contratos firmados desde el 8-10-2026 el casero no puede repercutirte (art. 20.1)");
  if (r.honorariosRechazable > 0.005) piezas.push(EM.eur(r.honorariosRechazable) + " de honorarios de agencia (pago único), que son del casero (art. " + nGest + ")");
  var verdict = no > 0.005
    ? 'Con tus datos, te repercuten ' + EM.eur(r.pedido) + ' este año y la ley te obliga a pagar ' + EM.eur(r.tuCargo) + ': puedes rechazar ' + EM.eur(no) + ' (' + piezas.join("; ") + ').' + (nuevo ? ' Regla vigente desde el 8-10-2026, pendiente de convalidación.' : '')
    : 'Con tus datos, lo que te repercuten (' + EM.eur(r.pedido) + ' este año) es lo que la ley te obliga a pagar: no hay nada que rechazar por estas reglas.';
  var rows = [
    { label: "Comunidad (con la subida pedida)", values: [EM.eur(r.comunidadPedida), EM.eur(r.comunidadLegal), EM.eur(r.excesoComunidad)] },
    { label: "IBI y tasas (obligado: el propietario)", values: [EM.eur(d.ibi), EM.eur(d.ibi - r.ibiRechazable), EM.eur(r.ibiRechazable)] },
    { label: "Honorarios de agencia y formalización (pago único)", values: [EM.eur(d.honorarios), EM.eur(0), EM.eur(r.honorariosRechazable)] },
    { label: "Total este año", values: [EM.eur(r.pedido), EM.eur(r.tuCargo), EM.eur(no)], strong: true }
  ];
  var note = '';
  if (nuevo) note += '<p><strong>Contrato firmado desde el 8-10-2026:</strong> el IBI no se puede repercutir al inquilino, salvo que sea él el obligado tributario (art. 20.1 nuevo, RDL 29/2026). La tasa de basuras suele tener como contribuyente al ocupante (TRLRHL, art. 23.1.b y 23.2.a): si es tu caso, es tuya; en el campo de IBI y tasas pon solo las tasas cuyo obligado es el propietario (depende de la ordenanza de tu ayuntamiento). La ley no trae transición expresa para este artículo; leemos que rige para los contratos firmados desde esa fecha (interpretación nuestra, confianza B, art. 2.3 del Código Civil); la lectura contraria lo aplicaría también a los recibos posteriores al 8-10 de contratos anteriores. Está <em>en vigor desde el 8-10-2026, pendiente de convalidación</em> por el Congreso: si se deroga, volvería la regla anterior para los contratos que se firmen después de la derogación. Si el edificio no está en propiedad horizontal tampoco se repercute comunidad (no se calcula), y el seguro de impago no se puede exigir al inquilino (art. 36.5).</p>';
  else note += '<p><strong>Contrato firmado antes del 8-10-2026:</strong> sigue la regla anterior (el IBI y las tasas sí pueden repercutirse con pacto válido). El RDL 29/2026 solo lo cambia, en nuestra lectura, para contratos firmados desde esa fecha (en vigor desde el 8-10-2026, pendiente de convalidación); la lectura contraria lo aplicaría a los recibos posteriores al 8-10. Para ti el tope de comunidad es el del art. 20.2 de la redacción vigente al firmar (art. 20.3 con la numeración actual).</p>';
  note += '<p><strong>El pacto:</strong> ' + (valido
    ? (nuevo ? 'tu contrato recoge por escrito el reparto con su importe anual, así que pagas la comunidad; el IBI, en un contrato desde el 8-10-2026, no (y las tasas, solo las de las que seas el obligado tributario).' : 'tu contrato recoge por escrito el reparto con su importe anual, así que pagas comunidad, IBI y basuras (art. 20.1).')
    : (d.pacto === "sinimp" ? 'el pacto escrito sin el importe anual a la fecha del contrato no es válido: los gastos generales los paga el casero (art. 20.1).' : 'sin pacto escrito, los gastos generales los paga el casero (art. 20.1).')) + '</p>';
  if (valido) note += '<p><strong>Tu límite de subida:</strong> ' + (d.tramo === "dentro"
    ? 'la comunidad solo puede subir si lo acordáis (o lo prevé tu contrato) y nunca más del doble del % en que puede subir tu renta: ' + EM.num(r.topePct, 2) + ' % (el doble de ' + EM.num(d.subidaRenta, 2) + ' %, art. ' + n20 + ')' + (d.acuerdo === "no" ? '. Como no lo has aceptado ni lo prevé tu contrato, no sube este año' : '') + (nuevo ? '.' : '; los tributos (IBI y basuras) no tienen ese tope.') + (' Hasta el 31-12-2027, sin nuevo pacto, la renta no puede subir más del 2 % (DF 6.ª del RDL 29/2026, pendiente de convalidación), así que lo prudente es poner 2 en «subida máxima de tu renta» (tope de comunidad 4 %); con el IRAV de 2,47 % sin esa regla sería el 4,94 %.') + ' Rige durante los ' + EM.num(P.aniosPf) + ' primeros años de vigencia, prórrogas incluidas (' + EM.num(P.aniosPj) + ' si el casero es persona jurídica, no un autónomo).'
    : 'pasados los ' + EM.num(P.aniosPf) + ' primeros años (' + EM.num(P.aniosPj) + ' con casero persona jurídica) el art. 20.2 ya no limita la subida: manda lo que pactasteis.') + '</p>';
  note += '<p><strong>Siempre tuyo:</strong> los suministros con contador (luz, agua, gas) y las pequeñas reparaciones por el uso ordinario (arts. ' + (nuevo ? '20.4' : '20.3') + ' y 21.4). Las reparaciones necesarias para la habitabilidad son del casero sin subir la renta, salvo que el daño sea imputable al inquilino (art. 21.1).</p>';
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
