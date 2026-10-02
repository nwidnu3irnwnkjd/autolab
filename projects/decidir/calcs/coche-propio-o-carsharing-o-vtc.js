// Coche propio, carsharing o taxi/VTC: coste anual de cada opcion, coste por km y puntos de equilibrio en km/anio.
// km/anio = viajes/mes x 12 x km por viaje. Propio = fijos + depreciacion + km x coste variable (combustible + mantenimiento).
// Carsharing = 12 x cuota mensual + km x tarifa por km (todo incluido). VTC/taxi = km x precio por km (bajada de bandera repartida). Empate: propio, carsharing, VTC.
// Equilibrio de A frente a B (coste = F + v x km): tipo 0 = A siempre es igual o mas barato; 1 = A nunca es mas barato; 2 = A gana a partir de km; 3 = A gana por debajo de km.
function equilibrio(Fa, va, Fb, vb) {
  var x;
  if (va === vb) return { tipo: Fa <= Fb ? 0 : 1, km: 0 };
  x = (Fa - Fb) / (vb - va);
  if (vb > va) return Fa <= Fb ? { tipo: 0, km: 0 } : { tipo: 2, km: x };
  return Fa >= Fb ? { tipo: 1, km: 0 } : { tipo: 3, km: x };
}
function calcular(d) {
  var km = d.viajes * 12 * d.kmviaje, F = d.fijos + d.deprec, kv = d.kmviaje * 12;
  var propio = F + km * d.kmcoche, cs = 12 * d.cscuota + km * d.cskm, vtc = km * d.vtckm;
  var cs3 = [propio, cs, vtc], b = 0, k, eC = equilibrio(F, d.kmcoche, 12 * d.cscuota, d.cskm), eV = equilibrio(F, d.kmcoche, 0, d.vtckm);
  for (k = 1; k < 3; k++) if (cs3[k] < cs3[b]) b = k;
  return {
    km: km, propio: propio, carsharing: cs, vtc: vtc,
    propioKm: km > 0 ? propio / km : 0, carsharingKm: km > 0 ? cs / km : 0, vtcKm: km > 0 ? vtc / km : 0, barato: b,
    tipoCS: eC.tipo, kmCS: eC.km, tipoVTC: eV.tipo, kmVTC: eV.km,
    viajesCS: kv > 0 ? eC.km / kv : 0, viajesVTC: kv > 0 ? eV.km / kv : 0
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["viajes", "kmviaje", "fijos", "deprec", "kmcoche", "cskm", "cscuota", "vtckm"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
// Frase de equilibrio del coche propio frente a otra opcion, con km/anio y viajes/mes.
function umbral(nombre, tipo, km, viajes) {
  var u = "unos " + EM.num(Math.round(km)) + " km al año (unos " + EM.num(Math.round(viajes)) + " viajes al mes de ese tamaño)";
  if (tipo === 0) return "el coche propio no sale más caro que " + nombre + " a ningún kilometraje";
  if (tipo === 1) return "el coche propio no sale más barato que " + nombre + " a ningún kilometraje";
  if (tipo === 2) return "el coche propio sale más barato que " + nombre + " a partir de " + u;
  return "el coche propio solo sale más barato que " + nombre + " por debajo de " + u;
}
function pintar() {
  var d = leer(), r, b, nombres = ["el coche propio", "el carsharing", "el taxi/VTC"], cs, v, note;
  if (d.viajes < 0 || d.kmviaje < 0 || d.fijos < 0 || d.deprec < 0 || d.kmcoche < 0 || d.cskm < 0 || d.cscuota < 0 || d.vtckm < 0) return;
  if (d.viajes > 150 || d.kmviaje > 300) { aviso("Revisa los viajes: hasta 150 al mes y 300 km por viaje.", "Por encima de eso, el carsharing y el taxi/VTC dejan de ser una alternativa realista para estos desplazamientos (viajes largos: mira <a href=\"/decidir/tren-avion-o-coche/\">tren, avión o coche</a>)."); return; }
  if (d.kmviaje <= 0 && d.viajes > 0) { aviso("Escribe los km medios de cada viaje (mayor que 0) o pon 0 viajes al mes.", "Sin distancia por viaje no hay kilómetros que comparar."); return; }
  r = calcular(d); b = r.barato; cs = [r.propio, r.carsharing, r.vtc];
  if (r.km === 0) v = "Con 0 km al año no hay desplazamientos que comparar: el coche propio sigue costando " + EM.eur(r.propio) + " al año en costes fijos y depreciación, y el carsharing solo su cuota (" + EM.eur(r.carsharing) + ").";
  else v = "Con estos datos, lo más barato al año es " + nombres[b] + " (" + EM.eur(cs[b]) + " al año, " + EM.eur(cs[b] / r.km, 2) + " por km) para " + EM.num(Math.round(r.km)) + " km al año.";
  note = "<p><strong>Lectura:</strong> " + umbral("el carsharing", r.tipoCS, r.kmCS, r.viajesCS) + "; " + umbral("el taxi/VTC", r.tipoVTC, r.kmVTC, r.viajesVTC) + ". Tú haces " + EM.num(Math.round(r.km)) + " km al año con estos viajes.</p>";
  note += "<p><strong>Supuestos:</strong> las tres opciones cubren los mismos km al año. El coste fijo y la depreciación del coche propio, la tarifa del carsharing y el precio del taxi/VTC los pones tú: los valores de la página son ejemplos, no tarifas de ninguna empresa ni cifras de mercado. El coste por km del coche propio sale por defecto de la gasolina 95 de hoy más un mantenimiento supuesto. Con depreciación 0 no cuentas lo que pierde de valor el coche, y si ya lo tienes pagado el coste de oportunidad del dinero no está incluido.</p>";
  note += "<p><strong>No incluido:</strong> tu tiempo, la disponibilidad (en el carsharing y el VTC depende de la zona y la hora), el aparcamiento ni las zonas de bajas emisiones, ni los viajes que solo puedes hacer con coche propio. Mira también <a href=\"/decidir/comprar-coche-o-renting/\">comprar coche o renting</a> y <a href=\"/decidir/bici-electrica-o-transporte-publico/\">bici eléctrica o transporte público</a>.</p>";
  EM.renderResult({
    winner: ["propio", "carsharing", "vtc"][b], verdict: v, tone: r.km === 0 ? "warn" : "ok",
    bigNumber: cs[b], bigLabel: "al año con " + nombres[b], format: EM.eur,
    barsLabel: "Coste anual de cada opción",
    bars: [{ label: "Coche propio" + (b === 0 ? " (más barato)" : ""), value: r.propio, color: "a" }, { label: "Carsharing" + (b === 1 ? " (más barato)" : ""), value: r.carsharing, color: "b" }, { label: "Taxi/VTC" + (b === 2 ? " (más barato)" : ""), value: r.vtc, color: "a" }],
    cols: ["Coche propio", "Carsharing", "Taxi/VTC"],
    rows: [
      { label: "Coste al año", values: [EM.eur(r.propio), EM.eur(r.carsharing), EM.eur(r.vtc)], strong: true },
      ["Coste al mes", EM.eur(r.propio / 12), EM.eur(r.carsharing / 12), EM.eur(r.vtc / 12)],
      ["Coste por km", r.km > 0 ? EM.eur(r.propioKm, 2) : "—", r.km > 0 ? EM.eur(r.carsharingKm, 2) : "—", r.km > 0 ? EM.eur(r.vtcKm, 2) : "—"],
      ["Km al año desde los que el coche propio es más barato", "—", r.tipoCS === 2 ? EM.num(Math.round(r.kmCS)) + " km" : (r.tipoCS === 0 ? "siempre" : (r.tipoCS === 1 ? "nunca" : "solo por debajo de " + EM.num(Math.round(r.kmCS)) + " km")), r.tipoVTC === 2 ? EM.num(Math.round(r.kmVTC)) + " km" : (r.tipoVTC === 0 ? "siempre" : (r.tipoVTC === 1 ? "nunca" : "solo por debajo de " + EM.num(Math.round(r.kmVTC)) + " km"))]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
