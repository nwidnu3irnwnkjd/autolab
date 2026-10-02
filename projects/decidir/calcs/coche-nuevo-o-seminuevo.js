// Coche nuevo o seminuevo: coste total de propiedad a N anios = perdida de valor + intereses + seguro y mantenimiento + averias esperadas.
// Supuestos del modelo (estimaciones propias, no oficiales; documentados en data/params.json > coche_nuevo_seminuevo):
// entrada 20 %, depreciacion 10 %/anio (nuevo desde el 2.o anio; seminuevo desde el 1.o), garantia del nuevo 3 anios (al seminuevo le quedan 3 - edad),
// averia fuera de garantia: prob. = min(0,6; 0,04 + 0,03 x edad del coche ese anio) x 1.000 EUR. Prestamo frances a N anios.
var ENT = 0.20, DEP = 0.10, GAR = 3, A_BASE = 0.04, A_EDAD = 0.03, A_TOPE = 0.6, A_COSTE = 1000;
function interesesAcum(precio, tin, N) { // cumulativo por anio, indice 0..N
  var L = precio * (1 - ENT), i = tin / 1200, n = 12 * N, out = [0], m, bal = L, cuota, ac = 0, k, it;
  if (tin <= 0 || L <= 0) { for (k = 1; k <= N; k++) out.push(0); return out; }
  cuota = L * i / (1 - Math.pow(1 + i, -n));
  for (m = 1; m <= n; m++) { it = bal * i; ac += it; bal -= cuota - it; if (m % 12 === 0) out.push(ac); }
  return out;
}
function averia(edad0, garantia, t) { return t <= garantia ? 0 : Math.min(A_TOPE, A_BASE + A_EDAD * (edad0 + t - 1)) * A_COSTE; }
function opcion(precio, valor, gasto, edad0, garantia, tin, N) {
  var ints = interesesAcum(precio, tin, N), av = 0, acum = [], t;
  for (t = 1; t <= N; t++) { av += averia(edad0, garantia, t); acum.push(precio - valor(t) + ints[t] + gasto * t + av); }
  return { acum: acum, total: acum[N - 1], perdida: precio - valor(N), intereses: ints[N], gastos: gasto * N, averias: av, residual: valor(N) };
}
function semi(d, precio, N) { return opcion(precio, function (t) { return precio * Math.pow(1 - DEP, t); }, d.gastos + d.extra, d.edad, Math.max(0, GAR - d.edad), d.tin, N); }
function calcular(d) {
  var N = d.anos, n, s, dif, s1, cruce = 0, t, a, b, pend;
  n = opcion(d.pnuevo, function (t) { return t === 0 ? d.pnuevo : d.pnuevo * (1 - d.dep1 / 100) * Math.pow(1 - DEP, t - 1); }, d.gastos, 0, GAR, d.tin, N);
  s = semi(d, d.psemi, N);
  dif = n.total - s.total;
  s1 = (n.acum[0] - s.acum[0]) > 0;
  for (t = 2; t <= N; t++) if (((n.acum[t - 1] - s.acum[t - 1]) > 0) !== s1) { cruce = t; break; }
  a = s.total; b = semi(d, d.psemi + 1000, N).total; pend = (b - a) / 1000;
  return {
    tcoNuevo: n.total, tcoSemi: s.total, perdidaNuevo: n.perdida, perdidaSemi: s.perdida, interesesNuevo: n.intereses, interesesSemi: s.intereses,
    gastosNuevo: n.gastos, gastosSemi: s.gastos, averiasNuevo: n.averias, averiasSemi: s.averias, residualNuevo: n.residual, residualSemi: s.residual,
    diferencia: dif, ganador: dif > 0.5 ? 0 : (dif < -0.5 ? 1 : 2), cruce: cruce, precioEquilibrio: d.psemi + dif / pend,
    acumNuevo: n.acum, acumSemi: s.acum
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["pnuevo", "psemi", "edad", "anos", "dep1", "gastos", "extra", "tin"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pintar() {
  var d = leer(), r, g, abs, v, note, N, an = " años";
  if (d.pnuevo < 0 || d.psemi < 0 || d.edad < 0 || d.anos < 0 || d.dep1 < 0 || d.gastos < 0 || d.extra < 0 || d.tin < 0) return;
  if (d.pnuevo <= 0 || d.psemi <= 0) { aviso("Escribe el precio del nuevo y el del seminuevo, mayores que 0.", "Sin precios no hay coste que comparar."); return; }
  if (d.psemi >= d.pnuevo) { aviso("El seminuevo debe costar menos que el nuevo equivalente.", "Si el seminuevo cuesta igual o más que el nuevo, elige el nuevo: la ventaja de un seminuevo es pagar menos por haber saltado los primeros años de pérdida de valor."); return; }
  if (Math.floor(d.anos) !== d.anos || d.anos < 1 || d.anos > 10) { aviso("El horizonte debe ser un número entero de años entre 1 y 10.", "Más allá de 10 años las estimaciones de pérdida de valor y averías del modelo dejan de ser razonables."); return; }
  if (d.edad > 10 || d.dep1 > 60 || d.tin > 25) { aviso("Revisa los datos: la edad del seminuevo va de 0 a 10 años, la pérdida del primer año hasta el 60 % y el TIN hasta el 25 %.", "Fuera de esos rangos el modelo no es fiable."); return; }
  N = d.anos; an = N === 1 ? " año" : " años"; r = calcular(d); g = r.ganador; abs = Math.abs(r.diferencia);
  if (g === 2) v = "Con estos datos, nuevo y seminuevo cuestan prácticamente lo mismo en " + N + an + " (" + EM.eur(r.tcoNuevo) + " frente a " + EM.eur(r.tcoSemi) + ").";
  else v = "Con estos datos, " + (g === 0 ? "el seminuevo" : "el nuevo") + " sale " + EM.eur(abs) + " más barato en " + N + an + " (coste total " + EM.eur(g === 0 ? r.tcoSemi : r.tcoNuevo) + " frente a " + EM.eur(g === 0 ? r.tcoNuevo : r.tcoSemi) + ").";
  note = "<p><strong>Lectura:</strong> la diferencia la marca sobre todo la pérdida de valor de los primeros años (" + EM.eur(r.perdidaNuevo) + " el nuevo, " + EM.eur(r.perdidaSemi) + " el seminuevo) y tu horizonte. ";
  if (r.cruce > 0) note += "Las curvas de coste se cruzan en el año <strong>" + r.cruce + "</strong>: a partir de ahí va por delante " + (g === 0 ? "el seminuevo" : "el nuevo") + ". ";
  else if (N > 1) note += "En tus " + N + " años no se cruzan: va por delante " + (r.acumSemi[0] < r.acumNuevo[0] ? "el seminuevo" : "el nuevo") + " todo el periodo. ";
  if (r.precioEquilibrio > 0) note += "El seminuevo compensa mientras cueste menos de <strong>" + EM.eur(r.precioEquilibrio) + "</strong> (con tus demás datos); ahora cuesta " + EM.eur(d.psemi) + ". ";
  else note += "Con tus demás datos el seminuevo no compensaría ni siquiera regalado. ";
  note += "</p><p><strong>Ojo:</strong> pérdida de valor, garantía y averías son <strong>estimaciones propias del modelo, no estadísticas ni cifras oficiales</strong>: entrada del 20 % si financias, depreciación del 10 % anual (en el nuevo, tu porcentaje el primer año), garantía de 3 años para el nuevo (al seminuevo le quedan " + Math.max(0, 3 - d.edad) + "), averías fuera de garantía con probabilidad creciente con la edad y 1.000 € por avería. No incluye impuestos de matriculación ni circulación, combustible, el interés que ganaría el dinero que no inviertes, ni diferencias de consumo o equipamiento. Mira también <a href=\"/decidir/comprar-coche-o-renting/\">comprar o renting</a>.</p>";
  EM.renderResult({
    winner: g === 0 ? "seminuevo" : (g === 1 ? "nuevo" : "empate"), verdict: v, tone: g === 2 ? "warn" : "ok",
    bigNumber: abs, bigLabel: g === 2 ? "de diferencia" : "menos con " + (g === 0 ? "el seminuevo" : "el nuevo") + " en " + N + an, format: EM.eur,
    barsLabel: "Coste total a " + N + an + " (ya descontado el valor residual)",
    bars: [{ label: "Nuevo" + (g === 1 ? " (más barato)" : ""), value: r.tcoNuevo, color: "a" }, { label: "Seminuevo" + (g === 0 ? " (más barato)" : ""), value: r.tcoSemi, color: "b" }],
    cols: ["Nuevo", "Seminuevo"],
    rows: [
      { label: "Coste total a " + N + an, values: [EM.eur(r.tcoNuevo), EM.eur(r.tcoSemi)], strong: true },
      ["Coste medio al año", EM.eur(r.tcoNuevo / N), EM.eur(r.tcoSemi / N)],
      ["Pérdida de valor", EM.eur(r.perdidaNuevo), EM.eur(r.perdidaSemi)],
      ["Intereses de la financiación", EM.eur(r.interesesNuevo), EM.eur(r.interesesSemi)],
      ["Seguro y mantenimiento", EM.eur(r.gastosNuevo), EM.eur(r.gastosSemi)],
      ["Averías esperadas fuera de garantía", EM.eur(r.averiasNuevo), EM.eur(r.averiasSemi)],
      ["Valor del coche al final", EM.eur(r.residualNuevo), EM.eur(r.residualSemi)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
