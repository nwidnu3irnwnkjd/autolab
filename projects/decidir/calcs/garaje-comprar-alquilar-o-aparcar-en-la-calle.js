// Plaza de garaje: comprar, alquilar o aparcar en la calle (zona regulada), coste a N años en euros de hoy.
// Comprar = precio x (1 + gastos %) + costes anuales x A - precio x v^N (se vende al precio de compra, precios constantes).
// Alquilar = 12 x cuota x A. Calle = (12 x tarifa + multas esperadas) x A. A = suma de v^t (t = 1..N), v = 1 / (1 + coste de oportunidad).
// Todo son supuestos del usuario: sin impuestos de compra por separado (el usuario mete el % total), sin revalorizacion ni gastos de venta.
function calcular(d) {
  var r = d.tasa / 100, v = 1 / (1 + r), N = d.anios, MAXT = 40;
  function A(T) { return r === 0 ? T : (1 - Math.pow(v, T)) / r; }
  function compra(T) { return d.precio * (1 + d.gastosPct / 100) + d.costes * A(T) - d.precio * Math.pow(v, T); }
  var fAlq = 12 * d.alq, fCalle = 12 * d.calle + d.multas, fAlt = Math.min(fAlq, fCalle);
  var c = [compra(N), fAlq * A(N), fCalle * A(N)];
  var mejor = 0, i;
  for (i = 1; i < 3; i++) if (c[i] < c[mejor]) mejor = i;
  var resto = [];
  for (i = 0; i < 3; i++) if (i !== mejor) resto.push(c[i]);
  var ahorro = Math.min(resto[0], resto[1]) - c[mejor], segundo = Math.min(resto[0], resto[1]);
  var eq = -1, T;
  for (T = MAXT; T >= 1; T--) { if (fAlt * A(T) - compra(T) < 0) { eq = T < MAXT ? T + 1 : -1; break; } }
  if (T < 1) eq = 1;
  return {
    costeCompra: c[0], costeAlquiler: c[1], costeCalle: c[2], desembolso: d.precio * (1 + d.gastosPct / 100),
    mejor: mejor, ahorro: ahorro, minimo: c[mejor], anioEq: eq,
    alqEq: c[0] / (12 * A(N)), calleEq: (c[0] / A(N) - d.multas) / 12,
    ganador: ahorro <= 0.05 * segundo ? 3 : mejor
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["precio", "gastosPct", "costes", "alq", "calle", "multas", "anios", "tasa"];
var NOM = ["comprar la plaza", "alquilar la plaza", "aparcar en la calle"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.precio <= 0 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un precio de compra mayor que 0 y al menos 1 año de horizonte.", tone: "warn", note: "<p>Sin precio de compra o sin años no hay nada que comparar.</p>" });
    return;
  }
  if (d.anios > 40 || d.tasa > 30 || d.gastosPct > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 40 años, 30 % de gastos de compra y 30 % de coste de oportunidad.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), N = d.anios, g = r.ganador;
  var anos = EM.num(N, 0) + (N === 1 ? " año" : " años"), w, verdict;
  var otros = ["comprar", "alquilar", "calle"];
  if (g === 3) {
    w = "empate";
    verdict = "Con estos datos hay empate práctico: la opción más barata (" + NOM[r.mejor] + ") sale solo " + eur(r.ahorro) + " mejor que la siguiente en " + anos + ", menos del 5 %. Decide por comodidad y seguridad.";
  } else {
    w = otros[g];
    verdict = "Con estos datos, lo más barato es " + NOM[g] + ": " + eur(r.minimo) + " en " + anos + " (euros de hoy), " + eur(r.ahorro) + " menos que la siguiente opción. ";
    if (g === 0) verdict += "Comprar compensa mientras el alquiler de una plaza equivalente supere " + eur(Math.max(r.alqEq, 0)) + " al mes y la calle te cueste más de " + eur(Math.max(r.calleEq, 0)) + " al mes (tarifa, sin contar multas)" + (r.anioEq > 0 && r.anioEq <= N ? "; comprar empieza a costar menos desde el año " + r.anioEq : "") + ".";
    else if (g === 1) verdict += "Alquilar gana frente a comprar mientras el alquiler no supere " + eur(Math.max(r.alqEq, 0)) + " al mes (el tuyo es de " + eur(d.alq) + ").";
    else verdict += "La calle gana frente a comprar mientras la tarifa mensual no supere " + eur(Math.max(r.calleEq, 0)) + " (la tuya es de " + eur(d.calle) + ") con tus multas esperadas de " + eur(d.multas) + " al año.";
  }
  var note = "<p><strong>Lectura:</strong> comprar la plaza exige " + eur(r.desembolso) + " el primer día (precio más gastos) y supone que la vendes al final por lo que pagaste. ";
  note += "El alquiler mensual que iguala comprar a " + anos + " es " + eur(Math.max(r.alqEq, 0)) + " y la tarifa mensual de calle que lo iguala, " + eur(Math.max(r.calleEq, 0)) + " (descontadas tus multas esperadas). ";
  note += r.anioEq > 0 ? "Frente a la alternativa más barata, comprar empieza a costar menos desde el año " + r.anioEq + " y se mantiene así hasta los 40 años del modelo.</p>" : "Frente a la alternativa más barata, comprar no llega a costar menos en 40 años con estos datos.</p>";
  note += "<p><strong>Límites:</strong> el porcentaje de gastos de compra lo pones tú con el total de tu comunidad (consulta los gastos de tu comunidad). Los importes se expresan en euros de hoy con tu coste de oportunidad del " + EM.num(d.tasa, 1) + " % (hipótesis editable, no una rentabilidad garantizada). No incluye revalorización ni gastos de venta de la plaza (si se revaloriza, comprar sale mejor; los gastos de venta lo empeoran), subidas del alquiler ni de la tarifa (si suben, alquilar y la calle salen peor), hipoteca, tiempo buscando aparcamiento, seguridad ni disponibilidad de plazas.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 3 ? "warn" : "ok",
    bigNumber: r.minimo, bigLabel: "€ de coste total de la opción más barata en " + anos, format: function (x) { return EM.eur(x); },
    barsLabel: "Coste total en " + anos + " (euros de hoy)",
    bars: [{ label: "Comprar" + (w === "comprar" ? " (gana)" : ""), value: Math.max(r.costeCompra, 0), color: "a" },
      { label: "Alquilar" + (w === "alquilar" ? " (gana)" : ""), value: Math.max(r.costeAlquiler, 0), color: "b" },
      { label: "Calle" + (w === "calle" ? " (gana)" : ""), value: Math.max(r.costeCalle, 0), color: "c" }],
    cols: ["Comprar", "Alquilar", "Calle"],
    rows: [
      ["Coste total en " + anos, eur(r.costeCompra), eur(r.costeAlquiler), eur(r.costeCalle)],
      ["Desembolso el primer día", eur(r.desembolso), "—", "—"],
      ["Cuota mensual de equilibrio frente a comprar", "—", eur(Math.max(r.alqEq, 0)), eur(Math.max(r.calleEq, 0))],
      { label: "Año desde el que comprar cuesta menos que la alternativa más barata", values: [r.anioEq > 0 ? EM.num(r.anioEq, 0) : "no llega", "", ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
