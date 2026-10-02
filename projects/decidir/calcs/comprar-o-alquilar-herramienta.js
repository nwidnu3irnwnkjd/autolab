// Comprar o alquilar una herramienta: coste total y por uso en N años, usos de equilibrio y años para amortizar.
// Compra = precio + (mantenimiento + almacenamiento) por año - reventa al final; alquiler = usos al año x coste por uso.
// Con coste de oportunidad > 0 se descuentan los flujos anuales (euros de hoy); con 0 es la suma simple. Todo son supuestos del usuario (ejemplos declarados en la página).
function calcular(d) {
  var r = d.tasa / 100, v = 1 / (1 + r), N = d.anios;
  var A = r === 0 ? N : (1 - Math.pow(v, N)) / r;
  var reventa = d.reventa / 100 * d.precio, vN = Math.pow(v, N);
  var pvc = d.precio + (d.mant + d.alm) * A - reventa * vN, pva = d.usos * d.alq * A, dif = pva - pvc;
  var s = d.usos * d.alq - d.mant - d.alm, pay;
  function f(T) { var AT = r === 0 ? T : (1 - Math.pow(v, T)) / r; return s * AT + reventa * Math.pow(v, T) - d.precio; }
  if (d.precio - reventa <= 0) pay = 0;
  else if (f(100) < 0) pay = -1;
  else { var lo = 0, hi = 100, i; for (i = 0; i < 100; i++) { var mid = (lo + hi) / 2; if (f(mid) < 0) lo = mid; else hi = mid; } pay = hi; }
  return {
    pvCompra: pvc, pvAlquiler: pva, diferencia: dif, reventaEur: reventa,
    costeUsoCompra: d.usos > 0 ? pvc / (d.usos * A) : 0,
    usosEqAnio: d.alq > 0 ? pvc / (d.alq * A) : -1, usosEqTotal: d.alq > 0 ? pvc / (d.alq * A) * N : -1,
    payback: pay, ahorroAnualNeto: s, ganador: dif > 1 ? 0 : (dif < -1 ? 1 : 2)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["precio", "alq", "usos", "anios", "reventa", "mant", "alm", "tasa"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.precio <= 0 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un precio de compra mayor que 0 y al menos 1 año de uso.", tone: "warn", note: "<p>Sin precio de compra o sin años de uso no hay nada que comparar.</p>" });
    return;
  }
  if (d.reventa > 100 || d.anios > 40 || d.tasa > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: la reventa no puede pasar del 100 % del precio, los años de uso de 40 ni el coste de oportunidad del 30 %.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), N = d.anios, g = r.ganador, abs = Math.abs(r.diferencia);
  var anos = EM.num(N, N % 1 ? 1 : 0) + (N === 1 ? " año" : " años");
  var eq = r.usosEqAnio, w, verdict;
  if (d.alq <= 0) {
    w = "alquilar";
    verdict = "Si alquilar no te cuesta nada por uso, comprar no puede compensar: solo suma el precio y los costes anuales (" + eur(r.pvCompra) + " en " + anos + ").";
  } else if (d.usos <= 0) {
    w = "alquilar";
    verdict = "Sin usos previstos, comprar solo suma costes (" + eur(r.pvCompra) + " en " + anos + "): no hay nada que alquilar ni que amortizar.";
  } else if (g === 2) {
    w = "empate";
    verdict = "Con estos datos comprar y alquilar cuestan lo mismo en " + anos + " (unos " + eur(r.pvCompra) + "): estás justo en el punto de equilibrio, " + EM.num(eq, 1) + " usos al año.";
  } else if (g === 0) {
    w = "comprar";
    verdict = "Con estos datos compensa comprar: te sale " + eur(abs) + " más barato que alquilar en " + anos + " (" + eur(r.costeUsoCompra, 2) + " por uso frente a " + eur(d.alq, 2) + "). Compensa a partir de " + EM.num(eq, 1) + " usos al año y esperas " + EM.num(d.usos, 1) + ".";
  } else {
    w = "alquilar";
    verdict = "Con estos datos compensa alquilar: te sale " + eur(abs) + " más barato que comprar en " + anos + " (" + eur(d.alq, 2) + " por uso frente a " + eur(r.costeUsoCompra, 2) + " si compras). Comprar compensaría a partir de " + EM.num(eq, 1) + " usos al año y esperas " + EM.num(d.usos, 1) + ".";
  }
  var note = "<p><strong>Lectura:</strong> ";
  if (d.alq > 0) {
    note += "el punto de equilibrio son <strong>" + EM.num(eq, 1) + " usos al año</strong> (" + EM.num(r.usosEqTotal, 1) + " usos en " + anos + "): por debajo conviene alquilar y por encima, comprar, con los demás datos iguales. ";
  }
  if (d.usos > 0 && d.alq > 0) {
    if (r.payback === 0) note += "Con tu reventa, la compra no tiene coste neto inicial. ";
    else if (r.payback < 0) note += "Con " + EM.num(d.usos, 1) + " usos al año, lo que te ahorras de alquiler no llega a cubrir el coste de comprar ni en 100 años. ";
    else note += "Con " + EM.num(d.usos, 1) + " usos al año, lo que te ahorras de alquiler cubre el coste de comprar en " + EM.num(r.payback, 1) + " años" + (r.payback <= N ? ", dentro de tu horizonte de " + anos + ". " : ", más allá de tu horizonte de " + anos + ". ");
  }
  note += "La reventa que has supuesto (" + EM.num(d.reventa, 0) + " %) equivale a " + eur(r.reventaEur) + " al final";
  note += d.tasa > 0 ? "; con un coste de oportunidad del " + EM.num(d.tasa, 1) + " % los importes se expresan en euros de hoy.</p>" : ".</p>";
  note += "<p>Es una estimación con supuestos tuyos: no incluye precios de ninguna tienda ni de ningún alquilador, la fianza o el seguro del alquiler (suma lo que no recuperes al coste por uso), el valor de tener la herramienta a mano ni el tiempo de ir a recogerla y devolverla. Se supone que la herramienta dura " + anos + " y que el uso es parecido cada año; si te la puedes prestar o compartir con vecinos, el coste de comprar baja.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: d.alq > 0 ? eq : undefined, bigLabel: "usos al año a partir de los cuales compensa comprar", format: function (x) { return EM.num(x, 1); },
    barsLabel: "Coste total en " + anos + (d.tasa > 0 ? " (euros de hoy)" : ""),
    bars: [{ label: "Comprar" + (w === "comprar" ? " (gana)" : ""), value: Math.max(r.pvCompra, 0), color: "a" }, { label: "Alquilar" + (w === "alquilar" ? " (gana)" : ""), value: Math.max(r.pvAlquiler, 0), color: "b" }],
    cols: ["Comprar", "Alquilar"],
    rows: [
      ["Coste total en " + anos, eur(r.pvCompra), eur(r.pvAlquiler)],
      ["Coste por uso", d.usos > 0 ? eur(r.costeUsoCompra, 2) : "—", eur(d.alq, 2)],
      ["Reventa al final", eur(r.reventaEur), "—"],
      ["Usos de equilibrio al año", d.alq > 0 ? EM.num(eq, 1) : "—", ""],
      { label: "Años para que el alquiler evitado cubra la compra", values: [r.payback < 0 ? "no llega" : EM.num(r.payback, 1), ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
