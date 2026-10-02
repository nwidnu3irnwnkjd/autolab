// Reformar o mudarse: coste neto acumulado a N años y año de equilibrio.
// Reformar = presupuesto x (1 - % que recuperas al vender). Mudarse = valor x gastos de compraventa % + diferencia de precio + mudanza y adecuación + 12 x variación mensual x años.
// Todo son supuestos del usuario; sin descuento financiero. No incluye impuestos de compraventa por separado, plusvalía municipal, deducciones, hipoteca ni lo no monetizable.
function calcular(d) {
  var neto = d.reforma * (1 - d.recup / 100), fijo = d.valor * d.gastosPct / 100 + d.dif + d.extras;
  var cuota = 12 * d.mensual, mud = fijo + cuota * d.anios, dif = mud - neto, t = cuota !== 0 ? (neto - fijo) / cuota : 0;
  var eq = (cuota !== 0 && t > 0 && t <= 40) ? t : -1;
  return {
    costeReformar: neto, fijoMudarse: fijo, costeMudarse: mud, diferencia: dif, anioEq: eq,
    cruce: eq > 0 ? (cuota < 0 ? 1 : 0) : -1,
    reformaMax: d.recup < 100 ? mud / (1 - d.recup / 100) : -1,
    ganador: dif > 1 ? 0 : (dif < -1 ? 1 : 2)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["reforma", "recup", "valor", "gastosPct", "dif", "extras", "mensual", "anios"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0 && k !== "dif" && k !== "mensual") return;
  if (d.reforma <= 0 || d.valor <= 0 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un presupuesto de reforma y un valor de la vivienda mayores que 0, y al menos 1 año de horizonte.", tone: "warn", note: "<p>Sin esos datos no hay nada que comparar.</p>" });
    return;
  }
  if (d.anios > 40 || d.recup > 100 || d.gastosPct > 30 || Math.abs(d.mensual) > 2000) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 40 años, un 100 % de valor recuperado, un 30 % de gastos de compraventa y una variación mensual de hasta 2.000 € arriba o abajo.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), N = d.anios, g = r.ganador, abs = Math.abs(r.diferencia);
  var anos = EM.num(N, 0) + (N === 1 ? " año" : " años"), w, verdict, eqTxt = r.anioEq > 0 ? EM.num(r.anioEq, 1) + " años" : "";
  if (g === 2) {
    w = "empate";
    verdict = "Con estos datos reformar y mudarse cuestan lo mismo en " + anos + " (unos " + eur(r.costeReformar) + " netos): estás justo en el punto de equilibrio.";
  } else if (g === 0) {
    w = "reformar";
    verdict = "Con estos datos compensa reformar: te cuesta " + eur(abs) + " menos que mudarte en " + anos + " (" + eur(r.costeReformar) + " netos frente a " + eur(r.costeMudarse) + ")" +
      (r.cruce === 1 ? ", aunque a partir de unos " + eqTxt + " mudarse pasaría a costar menos por el ahorro mensual" : (r.cruce === 0 ? ", y la ventaja crece con los años" : "")) + ".";
  } else {
    w = "mudarse";
    verdict = "Con estos datos compensa mudarse: te cuesta " + eur(abs) + " menos que reformar en " + anos + " (" + eur(r.costeMudarse) + " frente a " + eur(r.costeReformar) + " netos)" +
      (r.cruce === 0 ? ", aunque a partir de unos " + eqTxt + " reformar pasaría a costar menos porque mudarte te sube los gastos mensuales" : "") + ".";
  }
  var note = "<p><strong>Lectura:</strong> ";
  if (r.anioEq > 0) note += "con tus datos, las dos opciones se igualan a los " + eqTxt + ": " + (r.cruce === 1 ? "a partir de ahí mudarse cuesta menos que reformar" : "a partir de ahí reformar cuesta menos que mudarse") + ". ";
  else note += "con tus datos no hay año de equilibrio dentro de los 40 años del modelo: " + (r.diferencia > 0 ? "reformar" : "mudarse") + " cuesta menos en todo ese plazo. ";
  if (r.reformaMax > 0) note += "Reformar sigue saliendo más barato mientras el presupuesto no supere " + eur(r.reformaMax) + " (con el " + EM.num(d.recup, 0) + " % de valor recuperado que has puesto). ";
  note += "Mudarte supone " + eur(r.fijoMudarse) + " de coste inicial (gastos de compraventa, diferencia de precio, mudanza y obras) y " + eur(12 * d.mensual) + " al año de variación en gastos.</p>";
  note += "<p>El % de valor recuperado es una hipótesis tuya, no un dato: consulta una tasación de tu vivienda. Es una estimación con supuestos tuyos: no incluye impuestos de compraventa por separado (consulta los de tu comunidad), plusvalía municipal, deducciones por reforma o eficiencia energética (dependen de requisitos: consúltalos), hipoteca ni lo no monetizable (barrio, colegio, trayecto, molestias de la obra). No descuenta el dinero en el tiempo.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: r.anioEq > 0 ? r.anioEq : abs, bigLabel: r.anioEq > 0 ? "años hasta que las dos opciones cuestan lo mismo" : "€ de diferencia entre las dos opciones", format: function (x) { return r.anioEq > 0 ? EM.num(x, 1) : EM.eur(x); },
    barsLabel: "Coste neto en " + anos,
    bars: [{ label: "Reformar" + (w === "reformar" ? " (gana)" : ""), value: Math.max(r.costeReformar, 0), color: "a" }, { label: "Mudarse" + (w === "mudarse" ? " (gana)" : ""), value: Math.max(r.costeMudarse, 0), color: "b" }],
    cols: ["Reformar", "Mudarse"],
    rows: [
      ["Coste neto en " + anos, eur(r.costeReformar), eur(r.costeMudarse)],
      ["Coste inicial", eur(d.reforma), eur(r.fijoMudarse)],
      ["Valor recuperado al vender", eur(d.reforma * d.recup / 100), "—"],
      ["Variación de gastos al año", "—", eur(12 * d.mensual)],
      { label: "Año de equilibrio", values: [r.anioEq > 0 ? EM.num(r.anioEq, 1) + " años" : "no hay", ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
