// Luz 2.0TD: tarifa fija o PVPC. Parametros (data/params.json -> luz_2026; fuentes y fechas alli).
// pot: peaje + cargo de potencia (EUR/kW y ano); iee e ieeMin: Impuesto Especial sobre la Electricidad; iva: tipo general;
// ccf: margen de comercializacion fijo del PVPC (EUR/kW y ano; Orden ETU/1948/2016, anexo II); MAXKW: el PVPC solo existe hasta 10 kW.
// perfil: precio medio de punta/llano/valle del PVPC dividido por la media de todas las horas (REData, oct 2025-sep 2026); media12: media de 12 meses (EUR/kWh).
var L = { pot: 28.429836, iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, perfil: [1.4366, 0.9336, 0.8374], media12: 0.1425, ccf: 3.113 };
var MAXKW = 10;
// Total de la factura anual: base (potencia + energia) + impuesto electrico (con minimo por kWh) + IVA.
function conImpuestos(base, kwh) { return (base + Math.max(base * L.iee, kwh * L.ieeMin)) * (1 + L.iva); }
function costeFija(d, pf) { return conImpuestos(d.potencia * d.potFija * 365 + d.consumo * pf, d.consumo); }
function precioEfectivo(d, media) {
  var v = 100 - d.pctPunta - d.pctLlano;
  return media * (d.pctPunta * L.perfil[0] + d.pctLlano * L.perfil[1] + v * L.perfil[2]) / 100;
}
function costePvpc(d, media) { return conImpuestos(d.potencia * (L.pot + L.ccf) + d.consumo * precioEfectivo(d, media), d.consumo); }
function calcular(d) {
  if (d.pctPunta + d.pctLlano > 100) return { invalido: 1, costeFija: 0, costePvpc: 0, diferencia: 0, ganador: "invalido" };
  var media = d.pvpc * (1 + d.hip / 100), cf = costeFija(d, d.precioFijo), cp = costePvpc(d, media), dif = cf - cp;
  // precio fijo de equilibrio (EUR/kWh de energia) con tu termino de potencia: biseccion sobre el coste total
  var eq = null;
  if (d.consumo > 0 && costeFija(d, 0) <= cp && costeFija(d, 5) >= cp) {
    var lo = 0, hi = 5, j;
    for (j = 0; j < 100; j++) { var m = (lo + hi) / 2; if (costeFija(d, m) < cp) lo = m; else hi = m; }
    eq = (lo + hi) / 2;
  }
  var sens = [-10, 0, 10].map(function (h) {
    var mm = d.pvpc * (1 + h / 100), c = costePvpc(d, mm); return { media: mm, pvpc: c, dif: cf - c };
  });
  var c12 = costePvpc(d, L.media12), desv12 = media / L.media12 - 1;
  return {
    costeFija: cf, costePvpc: cp, diferencia: dif, ahorroPvpc: Math.max(dif, 0), ahorroFija: Math.max(-dif, 0),
    ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "pvpc" : "fija"),
    precioMedioPvpc: media, precioEfectivoPvpc: precioEfectivo(d, media), precioEquilibrio: eq, equilibrioMwh: eq === null ? -1 : eq * 1000,
    difMenos10: sens[0].dif, difIgual: sens[1].dif, difMas10: sens[2].dif, costeMenos10: sens[0].pvpc, costeMas10: sens[2].pvpc,
    costeMedia12: c12, desv12: desv12, difMedia12: cf - c12, hayEquilibrio: eq === null ? 0 : 1
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["consumo", "potencia", "pctPunta", "pctLlano", "precioFijo", "potFija", "pvpc", "hip"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.consumo < 0 || d.potencia <= 0 || d.pctPunta < 0 || d.pctLlano < 0 || d.precioFijo < 0 || d.potFija < 0 || d.pvpc <= 0) return;
  if (d.potencia > MAXKW) {
    EM.renderResult({ winner: "empate", verdict: "El PVPC solo existe para potencias contratadas de hasta 10 kW.", tone: "warn",
      note: "<p>Con " + EM.num(d.potencia, 1) + " kW no puedes contratar el PVPC (RD 216/2014): tendrías que elegir una tarifa de mercado libre. Esta calculadora compara únicamente con el PVPC, así que baja la potencia a 10 kW o menos si tu contrato lo permite.</p>" });
    return;
  }
  var r = calcular(d);
  if (r.invalido) {
    EM.renderResult({ winner: "empate", verdict: "Los porcentajes de punta y llano suman más de 100 %.", tone: "warn",
      note: "<p>El consumo en horas valle es lo que queda tras restar punta y llano, así que punta + llano no puede superar el 100 %. Corrige los porcentajes.</p>" });
    return;
  }
  var abs = Math.abs(r.diferencia), pv = r.ganador === "pvpc", valle = 100 - d.pctPunta - d.pctLlano;
  var verdict = r.ganador === "empate" ? "Con estos supuestos, la tarifa fija y el PVPC te cuestan lo mismo al año."
    : "Con estos supuestos, " + (pv ? "el PVPC te sale " : "tu tarifa fija te sale ") + EM.eur(abs) + (pv ? " más barato" : " más barata") + " al año" + (pv ? " que la tarifa fija." : " que el PVPC.");
  var note = "<p><strong>Lectura:</strong> ";
  if (d.consumo <= 0) note += "con consumo cero solo comparas el término de potencia. ";
  else if (r.hayEquilibrio) note += "tu oferta fija compensa mientras el precio de la energía sea inferior a <strong>" + EM.num(r.precioEquilibrio, 3) + " €/kWh</strong> (sin impuestos, con tu término de potencia); por encima, el PVPC con estos supuestos sale mejor. ";
  else note += "con ese término de potencia no existe un precio de energía que iguale el coste del PVPC. ";
  var d12 = r.difMedia12, g12 = Math.abs(d12) < 1 ? "empate" : (d12 > 0 ? "pvpc" : "fija");
  note += "Para comparar con tu tarifa fija (" + EM.eur(r.costeFija) + " al año): con el PVPC un 10 % más barato costaría " + EM.eur(r.costeMenos10) + "; un 10 % más caro, " + EM.eur(r.costeMas10) + "; y con la media de los últimos 12 meses (" + EM.num(L.media12, 4) + " €/kWh), " + EM.eur(r.costeMedia12) + ". ";
  note += g12 === "empate" ? "Con esa media de 12 meses, la tarifa fija y el PVPC cuestan lo mismo.</p>"
    : "Con esa media de 12 meses " + (g12 === "pvpc" ? "saldría mejor el PVPC, por " : "seguiría ganando la tarifa fija, por ") + EM.eur(Math.abs(d12)) + (Math.abs(d12) < 30 ? " (casi un empate)" : "") + (g12 !== r.ganador && r.ganador !== "empate" ? ": el resultado cambia de signo respecto a tu precio medio" : "") + ".</p>";
  if (Math.abs(r.desv12) >= 0.1) note += "<p><strong>Ojo con el precio de partida:</strong> el PVPC medio que usas (" + EM.num(r.precioMedioPvpc, 3) + " €/kWh) está un " + EM.num(Math.abs(r.desv12) * 100, 0) + " % " + (r.desv12 > 0 ? "por encima" : "por debajo") + " de la media de 12 meses" + (r.desv12 > 0 ? "; septiembre es el mes más caro del último año y eso favorece a la tarifa fija" : "") + ". Además, la forma por periodos (punta/llano/valle) es la de 12 meses aunque el precio sea de un mes, lo que puede mover el resultado unos 20-30 € según tu perfil.</p>";
  note += "<p><strong>Ojo:</strong> el PVPC cambia cada hora y no se puede fijar; esto es una estimación con un perfil de consumo (" + EM.num(d.pctPunta) + " % punta, " + EM.num(d.pctLlano) + " % llano, " + EM.num(valle) + " % valle) y con la forma de precios por periodo de los últimos 12 meses, que no tiene por qué repetirse (en verano, de junio a septiembre de 2026, el valle ha salido igual o más caro que el llano). Incluye el margen de comercialización fijo del PVPC (3,113 €/kW·año), el impuesto eléctrico (5,11269632 %) y el IVA del 21 %, vigentes en octubre de 2026; en noviembre y diciembre pueden bajar (IVA 10 % solo con potencia de hasta 10 kW) si el IPC de la electricidad sube más de un 15 % (el de septiembre decide noviembre y el de octubre, diciembre), y entonces la diferencia absoluta sería menor. Solo vale para Península y Baleares: Canarias (IGIC), Ceuta y Melilla (IPSI) tienen otros impuestos, y el precio de Red Eléctrica usado es el peninsular. No incluye alquiler del contador, bono social, financiación del bono social (unos 7 €/año, también la cobran casi todas las fijas) ni potencias distintas en punta y valle.</p>";
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: abs < Math.max(r.costeFija, r.costePvpc, 1) * 0.03 ? "warn" : "ok",
    bigNumber: abs, bigLabel: r.ganador === "empate" ? "de diferencia" : "menos al año con " + (pv ? "el PVPC" : "la tarifa fija"), format: EM.eur,
    barsLabel: "Coste anual estimado con impuestos",
    bars: [{ label: "Tarifa fija" + (r.ganador === "fija" ? " (gana)" : ""), value: r.costeFija, color: "a" }, { label: "PVPC" + (pv ? " (gana)" : ""), value: r.costePvpc, color: "b" }],
    cols: ["Fija", "PVPC"],
    rows: [
      ["Coste anual con impuestos", EM.eur(r.costeFija), EM.eur(r.costePvpc)],
      ["Precio medio de la energía, sin impuestos (€/kWh)", EM.num(d.precioFijo, 3), EM.num(r.precioEfectivoPvpc, 3)],
      ["Con el PVPC un 10 % más barato", EM.eur(r.costeFija), EM.eur(r.costeMenos10)],
      ["Con el PVPC un 10 % más caro", EM.eur(r.costeFija), EM.eur(r.costeMas10)],
      ["Con el PVPC igual a la media de 12 meses", EM.eur(r.costeFija), EM.eur(r.costeMedia12)],
      { label: "Diferencia anual con tus supuestos (positivo = más barato el PVPC)", values: ["", EM.eur(r.diferencia)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
