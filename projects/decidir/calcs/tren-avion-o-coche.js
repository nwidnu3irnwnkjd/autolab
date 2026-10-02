// Tren, avion o coche: coste total del grupo, tiempo puerta a puerta y puntos de equilibrio. Precios y tiempos de tren/avion los pone el usuario.
// Coche: dist x coste por km (combustible + desgaste) + peajes/extras; no depende del nº de viajeros. Tren/avion: billete x viajeros.
// Tiempo del coche = dist / VEL (supuesto fijo, con paradas). Empate de coste/tiempo: gana el primero en el orden coche, tren, avion.
var VEL = 85, NOMBRES = ["coche", "tren", "avión"];
function argmin(v) { var k = 0, i; for (i = 1; i < v.length; i++) if (v[i] < v[k]) k = i; return k; }
// A frente a B: tipo 0 = A siempre mejor (mas barato y no mas lento); 1 = nunca; 2 = A compensa si la hora vale >= h; 3 = A (mas barato pero mas lento) compensa si la hora vale <= h.
function equilibrio(cA, tA, cB, tB, n) {
  var dc = cA - cB, dt = tB - tA;
  if (dc <= 0 && dt >= 0) return { tipo: 0, h: 0 };
  if (dc > 0 && dt <= 0) return { tipo: 1, h: 0 };
  return { tipo: dc > 0 ? 2 : 3, h: dc / (n * dt) };
}
function minViajeros(cCoche, billete) { return billete > 0 ? Math.floor(cCoche / billete) + 1 : -1; }
function calcular(d) {
  var cCoche = d.dist * d.kmcoche + d.extras, cTren = d.tren * d.viaj, cAvion = d.avion * d.viaj;
  var tCoche = d.dist / VEL, costes = [cCoche, cTren, cAvion], tiempos = [tCoche, d.htren, d.havion];
  var eTC = equilibrio(cTren, d.htren, cCoche, tCoche, d.viaj), eAC = equilibrio(cAvion, d.havion, cCoche, tCoche, d.viaj), eAT = equilibrio(cAvion, d.havion, cTren, d.htren, d.viaj);
  return {
    costeCoche: cCoche, costeTren: cTren, costeAvion: cAvion, porPersonaCoche: cCoche / d.viaj, tiempoCoche: tCoche,
    barato: argmin(costes), rapido: argmin(tiempos),
    minViajerosTren: minViajeros(cCoche, d.tren), minViajerosAvion: minViajeros(cCoche, d.avion),
    tipoTrenCoche: eTC.tipo, horaTrenCoche: eTC.h, tipoAvionCoche: eAC.tipo, horaAvionCoche: eAC.h, tipoAvionTren: eAT.tipo, horaAvionTren: eAT.h
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["dist", "viaj", "tren", "avion", "htren", "havion", "kmcoche", "extras"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function horas(x) { var m = Math.round(x * 60); return Math.floor(m / 60) + " h " + (m % 60 < 10 ? "0" : "") + (m % 60) + " min"; }
function frase(nombre, tipo, h, ref) {
  return frase0(nombre, tipo, h, ref).replace(/ a el /g, " al ");
}
function frase0(nombre, tipo, h, ref) {
  if (tipo === 0) return "el " + nombre + " es más barato y no más lento que " + ref + ": compensa a cualquier valor de tu hora";
  if (tipo === 1) return "el " + nombre + " cuesta más y no ahorra tiempo frente a " + ref + ": no compensa a ningún valor de tu hora";
  if (tipo === 2) return "el " + nombre + " compensa frente a " + ref + " si tu hora vale más de " + EM.eur(h) + " por persona";
  return "el " + nombre + " es más barato pero más lento que " + ref + ": compensa solo si tu hora vale menos de " + EM.eur(h) + " por persona";
}
function pintar() {
  var d = leer();
  if (d.dist < 0 || d.viaj < 0 || d.tren < 0 || d.avion < 0 || d.htren < 0 || d.havion < 0 || d.kmcoche < 0 || d.extras < 0) return;
  if (d.dist <= 0 || d.viaj < 1 || d.htren <= 0 || d.havion <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe una distancia mayor que 0, al menos 1 viajero y un tiempo mayor que 0 para tren y avión.", tone: "warn",
      note: "<p>Sin distancia, viajeros o tiempos no hay viaje que comparar.</p>" });
    return;
  }
  if (d.viaj > 5 || Math.floor(d.viaj) !== d.viaj) {
    EM.renderResult({ winner: "invalido", verdict: "La comparación supone un solo coche: el número de viajeros debe ser un entero entre 1 y 5.", tone: "warn",
      note: "<p>Para más de 5 personas haría falta otro vehículo y el coste del coche no sería el mismo. Divide el grupo o calcula cada coche por separado.</p>" });
    return;
  }
  var r = calcular(d), cs = [r.costeCoche, r.costeTren, r.costeAvion], ts = [r.tiempoCoche, d.htren, d.havion], b = r.barato, f = r.rapido;
  var verdict = b === f ? "Con estos datos, el " + NOMBRES[b] + " es a la vez el más barato (" + EM.eur(cs[b]) + ") y el más rápido (" + horas(ts[b]) + ")."
    : "Con estos datos, el más barato es el " + NOMBRES[b] + " (" + EM.eur(cs[b]) + " para " + d.viaj + (d.viaj === 1 ? " viajero" : " viajeros") + ") y el más rápido es el " + NOMBRES[f] + " (" + horas(ts[f]) + ").";
  var note = "<p><strong>Lectura:</strong> el coche cuesta " + EM.eur(r.costeCoche) + " en total aunque vayas solo o acompañado, mientras tren y avión se pagan por persona. ";
  note += r.minViajerosTren > 0 ? "El coche sale más barato que el tren a partir de <strong>" + r.minViajerosTren + "</strong> viajeros" : "El tren no tiene precio (0 €)";
  note += r.minViajerosAvion > 0 ? " y que el avión a partir de <strong>" + r.minViajerosAvion + "</strong>" : " y el avión no tiene precio (0 €)";
  note += ((r.minViajerosTren > 5 || r.minViajerosTren < 0) && (r.minViajerosAvion > 5 || r.minViajerosAvion < 0)) ? " (con los 5 plazas de un coche, no llega a ganar a ninguno por coste)" : "";
  note += ". Valor de tu hora: " + frase("tren", r.tipoTrenCoche, r.horaTrenCoche, "el coche") + "; " + frase("avión", r.tipoAvionCoche, r.horaAvionCoche, "el coche") + ". Entre avión y tren: " + frase("avión", r.tipoAvionTren, r.horaAvionTren, "el tren") + ".</p>";
  note += "<p><strong>Ojo:</strong> los billetes, los peajes y los tiempos de tren y avión (con traslados y esperas) los pones tú: los valores de la página son un ejemplo, no cotizaciones. El tiempo del coche es la distancia entre " + VEL + " km/h de media con paradas. No incluye CO2, comodidad, seguro, alquiler de coche en destino ni aparcamiento si no lo sumas en «peajes y extras». El precio de los billetes cambia con la antelación y la fecha.</p>";
  EM.renderResult({
    winner: NOMBRES[b], verdict: verdict, tone: "ok",
    bigNumber: cs[b], bigLabel: "coste total del modo más barato (" + NOMBRES[b] + ") para " + d.viaj + (d.viaj === 1 ? " viajero" : " viajeros"), format: EM.eur,
    barsLabel: "Coste total del viaje para el grupo",
    bars: [{ label: "Coche" + (b === 0 ? " (más barato)" : ""), value: r.costeCoche, color: "a" }, { label: "Tren" + (b === 1 ? " (más barato)" : ""), value: r.costeTren, color: "b" }, { label: "Avión" + (b === 2 ? " (más barato)" : ""), value: r.costeAvion, color: "a" }],
    cols: ["Coche", "Tren", "Avión"],
    rows: [
      ["Coste total del grupo", EM.eur(cs[0]), EM.eur(cs[1]), EM.eur(cs[2])],
      ["Coste por persona", EM.eur(cs[0] / d.viaj), EM.eur(cs[1] / d.viaj), EM.eur(cs[2] / d.viaj)],
      ["Tiempo puerta a puerta", horas(ts[0]), horas(ts[1]), horas(ts[2])],
      ["Viajeros desde los que el coche es más barato", "—", r.minViajerosTren < 0 ? "nunca" : String(r.minViajerosTren), r.minViajerosAvion < 0 ? "nunca" : String(r.minViajerosAvion)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
