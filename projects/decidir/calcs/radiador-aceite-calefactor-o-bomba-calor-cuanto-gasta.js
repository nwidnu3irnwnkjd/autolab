// Calentar una estancia con electricidad: radiador de aceite, calefactor, convector o estufa (resistencia) frente a bomba de calor (aire acondicionado con bomba de calor).
// Potencia electrica media en funcionamiento (kW) x factor de aislamiento (hipotesis) = kW de la resistencia; la bomba da el mismo calor con kW / COP (COP = hipotesis editable).
// Precio efectivo = energia + impuesto electrico (con minimo por kWh) + IVA (Ley 38/1992 art. 99, Ley 37/1992). Coste marginal: sin termino de potencia ni alquiler de contador.
// Total = compra extra de la bomba + vida x coste anual (sin descontar ni inflacion). ganador: 0 resistencia, 1 bomba de calor, 2 empate practico (< 5 %).
// diasEq: dias de uso al ano a partir de los cuales la bomba compensa la compra extra en la vida util (-1 si no hay).
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, mes: 30, empate: 0.05 };
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precio), kwR = d.potencia * d.aisl, kwB = kwR / d.cop;
  var hR = kwR * pe, hB = kwB * pe, dR = hR * d.horas, dB = hB * d.horas;
  var mR = dR * L.mes, mB = dB * L.mes, aR = dR * d.dias, aB = dB * d.dias;
  var kwhAnoR = kwR * d.horas * d.dias, kwhAnoB = kwB * d.horas * d.dias;
  var ahorro = aR - aB, tR = d.vida * aR, tB = d.compraExtra + d.vida * aB, dif = tR - tB;
  var anios = d.compraExtra <= 0 ? (ahorro >= 0 ? 0 : -1) : (ahorro > 0 ? d.compraExtra / ahorro : -1);
  var diasEq = (d.compraExtra > 0 && d.cop > 1 && d.vida > 0 && d.horas > 0 && kwR > 0 && pe > 0) ? d.compraExtra / (d.vida * pe * kwR * d.horas * (1 - 1 / d.cop)) : -1;
  var g = Math.abs(dif) < Math.max(1, L.empate * Math.max(tR, tB)) ? 2 : (dif > 0 ? 1 : 0);
  return { precioEf: pe, kwR: kwR, kwB: kwB, horaR: hR, horaB: hB, diaR: dR, diaB: dB, mesR: mR, mesB: mB, anoR: aR, anoB: aB,
    kwhAnoR: kwhAnoR, kwhAnoB: kwhAnoB, ahorroAnual: ahorro, totalR: tR, totalB: tB, diferencia: dif, aniosAmort: anios, diasEq: diasEq, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["potencia", "aisl", "horas", "dias", "precio", "cop", "compraExtra", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.potencia <= 0 || d.aisl <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica la potencia eléctrica media del radiador o calefactor en marcha (mayor que 0 kW).", tone: "warn", note: "<p>Sin potencia no hay consumo que comparar. Piensa en la media con el termostato, no en la potencia máxima de la placa.</p>" });
    return;
  }
  if (d.cop < 1 || d.cop > 8) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el COP de la bomba de calor: debe estar entre 1 y 8.", tone: "warn", note: "<p>El COP es los kWh de calor que da la bomba por cada kWh de electricidad; con 1 sería como una resistencia. Es una hipótesis tuya: mira la ficha del equipo.</p>" });
    return;
  }
  if (d.horas > 24 || d.dias > 366) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el uso: no puede haber más de 24 horas al día ni de 366 días al año.", tone: "warn", note: "<p>Cuenta solo las horas en que la calefacción está funcionando de verdad.</p>" });
    return;
  }
  if (d.vida < 1 || d.vida > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica una vida útil de entre 1 y 30 años.", tone: "warn", note: "<p>Es el periodo en que repartes la compra extra; no es una garantía del fabricante.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), vid = EM.num(d.vida, d.vida % 1 ? 1 : 0) + (d.vida === 1 ? " año" : " años"), w, verdict, tone = "ok";
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con tus datos, empate práctico: la resistencia y la bomba de calor cuestan casi lo mismo en " + vid + " (compra extra más energía; diferencia de " + EM.eur(ab) + ").";
  } else if (g === 1) {
    w = "bomba";
    verdict = "Con tus datos, gana la bomba de calor por " + EM.eur(ab) + " en " + vid + " (compra extra más energía), si el confort que da es suficiente para tu estancia.";
  } else {
    w = "resistencia";
    verdict = "Con tus datos, gana la resistencia (radiador, calefactor, convector o estufa) por " + EM.eur(ab) + " en " + vid + ": el ahorro de energía de la bomba no cubre su compra extra" + (r.diasEq > 0 && r.diasEq <= 366 ? ", salvo que la uses más de " + EM.num(r.diasEq, 0) + " días al año" : "") + ".";
  }
  var note = "<p><strong>Lectura:</strong> con un precio de " + EM.num(r.precioEf, 3) + " €/kWh con impuestos, una hora cuesta " + EM.eur(r.horaR, 2) + " con la resistencia y " + EM.eur(r.horaB, 2) + " con la bomba (COP " + EM.num(d.cop, 1) + "); un día de " + EM.num(d.horas, 1) + " horas, " + EM.eur(r.diaR, 2) + " y " + EM.eur(r.diaB, 2) + "; un mes de " + L.mes + " días de uso, " + EM.eur(r.mesR) + " y " + EM.eur(r.mesB) + ". ";
  if (r.aniosAmort > 0) note += "La compra extra de la bomba (" + EM.eur(d.compraExtra) + ") se recupera con el ahorro de energía en <strong>" + EM.num(r.aniosAmort, 1) + " años</strong>" + (r.aniosAmort > d.vida ? ", más que la vida útil que has puesto" : "") + ". ";
  else if (r.aniosAmort === 0) note += "La bomba no cuesta más de comprar y gasta menos energía, así que no hay nada que amortizar. ";
  else if (d.compraExtra > 0) note += "Con estos datos la bomba no ahorra energía suficiente para recuperar su compra extra. ";
  if (r.diasEq > 0) note += "El punto de equilibrio con tus horas y tu vida útil está en <strong>" + EM.num(r.diasEq, 0) + " días de uso al año</strong>" + (r.diasEq > 366 ? " (más de un año: no se alcanza)" : "") + ". ";
  note += "</p><p><strong>Confort no equivalente:</strong> la resistencia calienta rápido y de forma local, y un radiador de aceite sigue emitiendo calor un rato al apagarse; la bomba de calor reparte el calor con aire, tarda más en notarse, hace ruido y puede perder rendimiento con mucho frío. Esta cifra compara cuánto cuesta el mismo calor, no la sensación de confort. En un radiador de aceite, un calefactor, un convector o una estufa eléctrica, cada kWh de luz se convierte en un kWh de calor, así que el modelo los trata igual y la diferencia entre ellos está en cómo reparten el calor, no en el coste de energía.</p>";
  note += "<p><strong>No incluye:</strong> el término de potencia ni el alquiler del contador, un aumento de potencia contratada, el mantenimiento, la inflación del precio de la luz ni descuentos financieros. El factor de aislamiento y el COP son hipótesis, no medidas de tu casa. Se usa la media de todas las horas del PVPC: de noche, en horas valle, el kWh suele ser más barato, y si calientas por la tarde-noche, más caro. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia en " + vid : (g === 1 ? "menos con la bomba de calor en " + vid : "menos con la resistencia en " + vid), format: EM.eur,
    barsLabel: "Coste total en " + vid + " (compra extra más energía)",
    bars: [{ label: "Resistencia" + (w === "resistencia" ? " (gana)" : ""), value: r.totalR, color: "a" }, { label: "Bomba de calor" + (w === "bomba" ? " (gana)" : ""), value: r.totalB, color: "b" }],
    cols: ["Radiador, calefactor, convector o estufa", "Bomba de calor"],
    rows: [
      ["Potencia eléctrica media (kW)", EM.num(r.kwR, 2), EM.num(r.kwB, 2)],
      ["Coste por hora", EM.eur(r.horaR, 2), EM.eur(r.horaB, 2)],
      ["Coste por día de uso", EM.eur(r.diaR, 2), EM.eur(r.diaB, 2)],
      ["Coste por mes de " + L.mes + " días de uso", EM.eur(r.mesR), EM.eur(r.mesB)],
      ["Coste de energía al año", EM.eur(r.anoR), EM.eur(r.anoB)],
      { label: "Total en " + vid + " con la compra extra", values: [EM.eur(r.totalR), EM.eur(r.totalB)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
