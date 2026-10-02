// Comparar ofertas de trabajo en neto real (2026). Parametros generados desde data/params.json (irpf_2026, autonomo_2026 y comparar_ofertas_2026; fuentes y fechas alli).
// Enfoque de arts. 19-20 y DA 61.a copiado de autonomo-o-asalariado (verificado). est: escala estatal general; ccaa: escala general y minimo del contribuyente (min null = estatal); sol: cotizacion de solidaridad [desde, hasta, % empresa, % trabajador] (mensual).
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": 5790, "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": 6105, "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": 5550, "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": 5606, "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": 5789, "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": 5956.65, "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": 6105, "orient": false}}, "sol": [[5101.2, 5611.32, 0.96, 0.19], [5611.32, 7651.8, 1.04, 0.21], [7651.8, null, 1.22, 0.24]], "w": 6.5};
var BMAX = 5101.20, MINIMO_E = 5550, SEM = 365 / 7 - 30 / 7 - 14 / 5;
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function cuotaBase(bg, cc) {
  var m = cc.min === null ? MINIMO_E : cc.min;
  return Math.max(0, escala(bg, P.est) - escala(MINIMO_E, P.est)) + Math.max(0, escala(bg, cc.esc) - escala(m, cc.esc));
}
function red20(n) {
  if (n >= 19747.5) return 0;
  if (n <= 14852) return 7302;
  if (n <= 17673.52) return 7302 - 1.75 * (n - 14852);
  return Math.max(0, 2364.34 - 1.14 * (n - 17673.52));
}
function da61(b) {
  if (b >= 20048.45) return 0;
  return b <= 17094 ? 590.89 : 590.89 - 0.2 * (b - 17094);
}
// Cotizacion del trabajador al ano: tipo sobre la base (tope BMAX/mes) mas solidaridad sobre el exceso mensual.
function ssTrab(bruto) {
  var r = bruto / 12, base = Math.min(r, BMAX), s = 0, i, t, x;
  for (i = 0; i < P.sol.length; i++) {
    t = P.sol[i]; x = Math.max(0, Math.min(r, t[1] === null ? Infinity : t[1]) - t[0]); s += x * t[3] / 100;
  }
  return 12 * (base * P.w / 100 + s);
}
function irpfTrab(bruto, cc) {
  var neto = bruto - ssTrab(bruto), otros = Math.min(2000, Math.max(neto, 0)), rn = Math.max(0, neto - otros - red20(neto));
  var ci = cuotaBase(rn, cc);
  return Math.max(0, ci - Math.min(da61(bruto), ci));
}
function netoDe(bruto, cc) { return bruto - ssTrab(bruto) - irpfTrab(bruto, cc); }
// Bruto minimo cuyo neto alcanza T (el neto no baja al subir el bruto): se sube y se afina por biseccion.
function brutoPara(T, cc) {
  var lo = 0, hi = 100, m, j;
  if (netoDe(0, cc) >= T) return 0;
  while (netoDe(hi, cc) < T && hi < 1e9) { lo = hi; hi = hi < 1e5 ? hi + 100 : hi * 1.5; }
  for (j = 0; j < 80; j++) { m = (lo + hi) / 2; if (netoDe(m, cc) >= T) hi = m; else lo = m; }
  return hi;
}
function pos(x) { return Math.max(+x || 0, 0); }
function calcular(d) {
  var cc = P.ccaa[d.ccaa], pagas = +d.pagas === 12 ? 12 : 14, r = {};
  ["A", "B"].forEach(function (k) {
    var b = pos(d["bruto" + k]), n = netoDe(b, cc), t = n - pos(d["despl" + k]), h = pos(d["horas" + k]) * SEM;
    r["ss" + k] = ssTrab(b); r["irpf" + k] = irpfTrab(b, cc); r["neto" + k] = n; r["netoTras" + k] = t;
    r["netoMes" + k] = n / 12; r["netoPaga" + k] = n / pagas; r["hora" + k] = h > 0 ? t / h : null; r["horasAno" + k] = h;
  });
  r.dif = r.netoTrasB - r.netoTrasA;
  r.ganador = Math.abs(r.dif) < 1 ? "empate" : (r.dif > 0 ? "b" : "a");
  r.ganNum = r.ganador === "empate" ? 0 : (r.ganador === "a" ? 1 : 2);
  r.brutoIgual = null; r.subidaIgual = null;
  r.unaCero = (pos(d.brutoA) === 0) !== (pos(d.brutoB) === 0) ? 1 : 0;
  if (r.ganador !== "empate" && !r.unaCero) {
    var peor = r.ganador === "b" ? "A" : "B", mejor = r.ganador === "b" ? "B" : "A";
    r.brutoIgual = brutoPara(r["netoTras" + mejor] + pos(d["despl" + peor]), cc);
    r.subidaIgual = r.brutoIgual - pos(d["bruto" + peor]);
  }
  r.ganadorHora = (r.horaA === null || r.horaB === null || Math.abs(r.horaB - r.horaA) < 0.005) ? "" : (r.horaB > r.horaA ? "b" : "a");
  r.orientativo = cc.orient ? 1 : 0; r.ccaaNombre = cc.n; r.pagas = pagas; r.semanas = SEM;
  return r;
}
function eur(x) { return EM.eur(x); }
function eurh(x) { return x === null ? "–" : EM.eur(x, 2) + "/h"; }
var IDS = ["brutoA", "brutoB", "desplA", "desplB", "horasA", "horasB", "pagas"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; return d;
}
function pintar() {
  var d = leer(), r = calcular(d);
  var nom = { a: "la oferta A", b: "la oferta B" }, verdict, note = "";
  if (d.brutoA <= 0 && d.brutoB <= 0) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Escribe el bruto anual de al menos una de las dos ofertas.", note: "<p>La calculadora compara dos sueldos brutos anuales (incluye el variable que esperas cobrar) en neto, después de Seguridad Social, IRPF y desplazamientos.</p>" });
    return;
  }
  if (r.unaCero) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Escribe el bruto anual de las dos ofertas: con una en blanco o a 0 € no hay comparación con sentido.", note: "<p>La calculadora compara dos sueldos brutos anuales (incluye el variable que esperas cobrar) en neto, después de Seguridad Social, IRPF y desplazamientos. Si una de las dos no tiene sueldo, ni el veredicto ni el bruto que igualaría a la otra serían fiables.</p>" });
    return;
  }
  if (r.ganador === "empate") verdict = "Con estos datos las dos ofertas te dejan lo mismo al año tras Seguridad Social, IRPF y desplazamientos (" + eur(r.netoTrasA) + "): decide por lo que esta comparación no mide (estabilidad, promoción, horario).";
  else {
    var g = r.ganador, o = g === "a" ? "b" : "a";
    verdict = "Con estos datos, " + nom[g] + " te deja " + eur(Math.abs(r.dif)) + " más al año en neto tras desplazamientos (" + eur(r["netoTras" + g.toUpperCase()]) + " frente a " + eur(r["netoTras" + o.toUpperCase()]) + "): para igualarla, " + nom[o] + " tendría que subir a " + eur(r.brutoIgual) + " brutos al año (" + eur(r.subidaIgual) + " más)." + (r.ganadorHora && r.ganadorHora !== g ? " Por hora trabajada sale mejor " + nom[r.ganadorHora] + ", porque las horas semanales no son las mismas." : "");
  }
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  if ((d.brutoA > 0 && d.brutoA < 17094) || (d.brutoB > 0 && d.brutoB < 17094)) note += "<p><strong>Atención:</strong> por debajo de 17.094 € brutos al año (salario mínimo de 2026 en 14 pagas) rigen bases mínimas de cotización por grupo que esta calculadora no modela: el resultado es solo orientativo.</p>";
  if (d.brutoA / 12 > BMAX || d.brutoB / 12 > BMAX) note += "<p>Una de las ofertas supera la base máxima de cotización (" + eur(BMAX) + " al mes): el exceso solo paga la cotización adicional de solidaridad, ya incluida.</p>";
  if (d.horasA <= 0 || d.horasB <= 0) note += "<p>Escribe las horas semanales de las dos ofertas para ver el neto por hora.</p>";
  else note += "<p>El neto por hora supone " + EM.num(r.semanas, 1) + " semanas de trabajo al año (365 días menos 30 de vacaciones y 14 fiestas, el mínimo y el máximo del Estatuto de los Trabajadores): " + EM.num(r.horasAnoA, 0) + " h al año en A y " + EM.num(r.horasAnoB, 0) + " h en B. Más vacaciones suben el neto por hora; si en tu calendario caen menos de 14 fiestas entre semana, trabajas más horas y baja.</p>";
  note += "<p><strong>No incluye:</strong> hijos y situación familiar (solo el mínimo personal; con descendientes el neto sería mayor), deducciones, retribución en especie y flexible, contratos temporales (cotizan al 6,55 %), indemnizaciones, cambios de convenio, estabilidad, promoción, el valor de tu tiempo (salvo el neto por hora), los 2.000 € adicionales si estabas en paro inscrito y aceptas un empleo que te obliga a mudarte de municipio (ese año y el siguiente, art. 19.2.f LIRPF) ni la del 30 % del art. 18 para el variable generado en más de dos años. Es el IRPF final del año, no la retención de la nómina, y supone un año completo en cada oferta y que no tienes otras rentas de más de 6.500 €. El variable y los incentivos van incluidos en el bruto.</p>";
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.ganador === "empate" ? "warn" : "ok",
    bigNumber: r.ganador === "empate" ? undefined : Math.abs(r.dif), bigLabel: r.ganador === "empate" ? "" : "al año más en neto tras desplazamientos con " + nom[r.ganador], format: eur,
    barsLabel: "Neto anual después de Seguridad Social, IRPF y desplazamientos",
    bars: [{ label: "Oferta A" + (r.ganador === "a" ? " (gana)" : ""), value: Math.max(r.netoTrasA, 0), color: "a" }, { label: "Oferta B" + (r.ganador === "b" ? " (gana)" : ""), value: Math.max(r.netoTrasB, 0), color: "b" }],
    cols: ["Oferta A", "Oferta B"],
    rows: [
      ["Bruto anual", eur(d.brutoA), eur(d.brutoB)],
      ["Seguridad Social a tu cargo", eur(r.ssA), eur(r.ssB)],
      ["IRPF", eur(r.irpfA), eur(r.irpfB)],
      ["Neto anual", eur(r.netoA), eur(r.netoB)],
      ["Neto al mes (÷ 12)", eur(r.netoMesA), eur(r.netoMesB)],
      ["Neto por paga (reparto igual en " + r.pagas + ")", eur(r.netoPagaA), eur(r.netoPagaB)],
      ["Desplazamientos al año", eur(d.desplA), eur(d.desplB)],
      { label: "Neto anual tras desplazamientos", values: [eur(r.netoTrasA), eur(r.netoTrasB)], strong: true },
      ["Neto por hora trabajada", eurh(r.horaA), eurh(r.horaB)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
