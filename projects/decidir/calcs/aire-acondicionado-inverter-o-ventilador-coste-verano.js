// Aire inverter frente a una alternativa (ventilador o aire no inverter): coste de energia de la temporada, total en la vida util y equilibrio.
// Energia = potencia media (kW) x horas/dia x dias x precio efectivo; precio efectivo = energia + impuesto electrico (con minimo por kWh) + IVA (Ley 38/1992 art. 99, Ley 37/1992).
// Coste marginal: no incluye termino de potencia ni alquiler de contador. Total = compra + vida x coste anual de energia (sin descontar ni inflacion).
// ganador: 0 inverter, 1 alternativa, 2 empate. horasEq: horas/dia a partir de las cuales el inverter compensa (-1 si no hay).
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, ratioVent: 0.2 };
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precio), h = d.horas * d.dias;
  var kwhI = d.kwInv * h, kwhA = d.kwAlt * h, cI = kwhI * pe, cA = kwhA * pe;
  var ahorro = cA - cI, extra = d.compraInv - d.compraAlt;
  var totI = d.compraInv + d.vida * cI, totA = d.compraAlt + d.vida * cA, dif = totA - totI;
  var anios = extra <= 0 ? (ahorro >= 0 ? 0 : -1) : (ahorro > 0 ? extra / ahorro : -1);
  var eq = (d.kwAlt > d.kwInv && extra > 0 && d.dias > 0 && d.vida > 0 && pe > 0) ? extra / (d.vida * d.dias * pe * (d.kwAlt - d.kwInv)) : -1;
  return { precioEf: pe, kwhInv: kwhI, kwhAlt: kwhA, costeInv: cI, costeAlt: cA, ahorroAnual: ahorro, extraCompra: extra,
    totalInv: totI, totalAlt: totA, diferencia: dif, aniosAmort: anios, horasEq: eq,
    esVentilador: d.kwAlt < L.ratioVent * d.kwInv ? 1 : 0, ganador: Math.abs(dif) < 1 ? 2 : (dif > 0 ? 0 : 1) };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["kwInv", "kwAlt", "horas", "dias", "precio", "compraInv", "compraAlt", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.kwInv <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica la potencia eléctrica media del aire inverter (mayor que 0 kW).", tone: "warn", note: "<p>Sin potencia no hay consumo que comparar.</p>" });
    return;
  }
  if (d.horas > 24 || d.dias > 366) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el uso: no puede haber más de 24 horas al día ni de 366 días.", tone: "warn", note: "<p>Cuenta solo las horas en que el equipo está funcionando de verdad.</p>" });
    return;
  }
  if (d.vida < 1 || d.vida > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Indica una vida útil de entre 1 y 30 años.", tone: "warn", note: "<p>Es el periodo en que repartes la compra; no es una garantía del fabricante.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), vent = r.esVentilador === 1, vid = EM.num(d.vida, d.vida % 1 ? 1 : 0) + (d.vida === 1 ? " año" : " años");
  var alt = vent ? "el ventilador" : "la alternativa", w, verdict, tone = "ok";
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con estos datos el aire inverter y " + alt + " cuestan lo mismo en " + vid + " (compra más energía).";
  } else if (g === 0) {
    w = "inverter";
    verdict = "Con estos datos el aire inverter sale " + EM.eur(ab) + " más barato que " + alt + " en " + vid + " (compra más energía)" + (vent ? ", aunque un ventilador no enfría el aire y por eso no son equivalentes" : "") + ".";
  } else if (vent) {
    w = "alternativa";
    verdict = "El ventilador cuesta " + EM.eur(ab) + " menos que el aire inverter en " + vid + " (compra más energía), pero no enfría el aire: mueve el aire y alivia la sensación, así que esto es una comparación de coste, no de confort.";
  } else {
    w = "alternativa";
    verdict = "Con estos datos la alternativa sale " + EM.eur(ab) + " más barata que el aire inverter en " + vid + " (compra más energía)." +
      (r.horasEq > 0 && r.horasEq <= 24 ? " El inverter compensaría con más de " + EM.num(r.horasEq, 1) + " horas al día de uso." : (r.horasEq > 24 ? " El inverter no compensaría ni usándolo las 24 horas del día." : ""));
  }
  var note = "<p><strong>Lectura:</strong> la energía de la temporada (" + EM.num(d.horas * d.dias, 0) + " horas) cuesta " + EM.eur(r.costeInv) + " con el aire inverter (" + EM.num(r.kwhInv, 0) + " kWh) y " + EM.eur(r.costeAlt) + " con " + alt + " (" + EM.num(r.kwhAlt, 0) + " kWh), con el precio de " + EM.num(r.precioEf, 3) + " €/kWh con impuestos. ";
  if (r.aniosAmort > 0) note += "La diferencia de compra (" + EM.eur(r.extraCompra) + ") se recupera con el ahorro de energía en <strong>" + EM.num(r.aniosAmort, 1) + " años</strong>" + (r.aniosAmort > d.vida ? ", más que la vida útil que has puesto" : "") + ". ";
  else if (r.aniosAmort === 0) note += "El aire inverter no cuesta más que la alternativa y gasta menos energía, así que no hay nada que amortizar. ";
  else if (r.ahorroAnual <= 0) note += "El aire inverter gasta más energía que la alternativa con estos datos, así que la diferencia de compra no se recupera. ";
  if (r.horasEq > 0 && !vent && r.horasEq <= 24) note += "El punto de equilibrio con tus días y tu vida útil está en <strong>" + EM.num(r.horasEq, 1) + " horas al día</strong>. ";
  note += "</p>";
  if (vent) note += "<p><strong>Confort no equivalente:</strong> un ventilador no baja la temperatura ni deshumidifica; solo mueve el aire. Por eso la cifra compara cuánto cuesta cada opción, no si cumplen la misma función. Aquí se considera ventilador una alternativa con menos de un 20 % de la potencia del inverter.</p>";
  note += "<p><strong>No incluye:</strong> el término de potencia ni el alquiler del contador (el coste es solo el de la energía adicional), el aumento de potencia contratada si lo necesitas, el mantenimiento, la inflación del precio de la luz ni descuentos financieros. Se usa la media de todas las horas del PVPC sin discriminar por horas, y la tarde-noche, cuando más se usa el aire, suele ser más cara que esa media: si lo usas sobre todo entonces, sube el precio. La potencia es una potencia media en funcionamiento (el inverter modula y el no inverter alterna parado y en marcha), no la de la placa. Península y Baleares: otros territorios tienen otros impuestos.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia en " + vid : (g === 0 ? "menos con el aire inverter en " + vid : "menos con " + alt + " en " + vid), format: EM.eur,
    barsLabel: "Coste total en " + vid + " (compra más energía)",
    bars: [{ label: "Aire inverter" + (w === "inverter" ? " (gana)" : ""), value: r.totalInv, color: "a" }, { label: (vent ? "Ventilador" : "Alternativa") + (w === "alternativa" ? " (gana)" : ""), value: r.totalAlt, color: "b" }],
    cols: ["Aire inverter", vent ? "Ventilador" : "Alternativa"],
    rows: [
      ["Energía de la temporada (kWh)", EM.num(r.kwhInv, 0), EM.num(r.kwhAlt, 0)],
      ["Coste de energía por temporada", EM.eur(r.costeInv), EM.eur(r.costeAlt)],
      ["Compra e instalación", EM.eur(d.compraInv), EM.eur(d.compraAlt)],
      { label: "Total en " + vid, values: [EM.eur(r.totalInv), EM.eur(r.totalAlt)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
