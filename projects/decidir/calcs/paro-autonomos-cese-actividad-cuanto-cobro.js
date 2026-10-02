// Paro de autonomos (prestacion por cese de actividad): derecho, cuantia mensual y duracion (2026). Parametros generados desde data/params.json -> paro_autonomos_cese_2026 (fuentes y fechas alli).
// tope/minimo: IPREM 600 + 1/6 = 700, x 175/200/225 % y 80/107 % segun hijos a cargo (0, 1, 2 o mas). escala: [meses cotizados por cese en 48 meses, meses de prestacion]. Cese parcial, sociedades de capital, cooperativas, Mar y agrarios: fuera del modelo.
var P = {"tope": [1225, 1400, 1575], "minimo": [560, 749, 749], "pct": 70, "escala": [[48, 24], [43, 16], [36, 12], [30, 10], [24, 8], [18, 6], [12, 4]], "carencia": 12, "ventana": 48, "entre": 18, "edadDudosa": 65, "edadTope": 67};
var ADM = { eco: 1, fuerza: 1, licencia: 1, violencia: 1, divorcio: 1, trade: 1 };
function duracion(m48) {
  for (var i = 0; i < P.escala.length; i++) if (m48 >= P.escala[i][0]) return P.escala[i][1];
  return 0;
}
function calcular(d) {
  var m48 = Math.min(Math.floor(d.m48), P.ventana), m24 = Math.floor(d.m24);
  var h = Math.min(Math.max(Math.round(d.hijos), 0), 2);
  var r = { bloqueo: 0, prest: 0, raw: 0, tope: P.tope[h], minimo: P.minimo[h], ap: 0, dur: 0, total: 0, condTrabajo: 0, condEdad: 0, hijos: h, m48: m48, m24: m24 };
  if (m24 > m48) { r.bloqueo = 7; return r; }
  if (d.causa === "fuera") { r.bloqueo = 2; return r; }
  if (!ADM[d.causa]) { r.bloqueo = 1; return r; }
  if (d.anterior === "reciente") { r.bloqueo = 5; return r; }
  if (d.edad >= P.edadTope) { r.bloqueo = 3; return r; }
  if (m48 < P.carencia || m24 < P.carencia) { r.bloqueo = 6; return r; }
  r.raw = d.base * P.pct / 100;
  r.prest = Math.min(Math.max(r.raw, r.minimo), r.tope);
  r.ap = r.raw > r.tope ? 1 : (r.raw < r.minimo ? -1 : 0);
  r.dur = duracion(m48);
  r.total = r.prest * r.dur;
  r.condTrabajo = d.trabaja === "si" ? 1 : 0;
  r.condEdad = d.edad >= P.edadDudosa ? 1 : 0;
  return r;
}
function eur(x) { return EM.eur(x); }
var IDS = ["base", "m48", "m24", "hijos", "edad"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  ["causa", "trabaja", "anterior"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function sinDerecho(w, txt) { EM.renderResult({ winner: "sin-" + w, tone: "warn", verdict: txt }); }
function txtMeses(n) { return EM.num(n, 0) + (n === 1 ? " mes" : " meses"); }
var MSG = {
  1: "Con ese motivo, el derecho no existe: dejar la actividad por decisión propia no es situación legal de cese de actividad (art. 331.2.a de la LGSS), salvo el TRADE que rompe con su cliente por incumplimiento grave de este (art. 333.1.b). Solo cuentan los motivos económicos, técnicos, productivos u organizativos, la fuerza mayor, la pérdida de la licencia, la violencia de género o sexual, el divorcio cuando ayudabas en el negocio de tu excónyuge y, si eres autónomo económicamente dependiente, el fin del contrato con tu cliente. Si tu cierre encaja en alguno, cambia el motivo.",
  2: "Esta herramienta no calcula esa situación: el cese parcial (reducción del 60 % de la jornada de la plantilla, deudas superiores al 150 % de los ingresos o fuerza mayor parcial) se paga al 50 % y sin máximo ni mínimo, y los socios de sociedades de capital, las cooperativas, el Régimen del Mar y los agrarios tienen requisitos propios. Pregunta a tu mutua o al SEPE.",
  3: "Con esa edad el derecho no existe si el cese es definitivo: la prestación exige no haber cumplido la edad ordinaria de jubilación (art. 330.1.d de la LGSS), que en 2026 es de 65 años con 38 años y 3 meses cotizados o de 66 años y 10 meses si no, y con 67 años ya la has superado. La excepción es no tener cotizados los 15 años que exige la pensión de jubilación; esta herramienta no calcula ese caso.",
  5: "Todavía no puedes volver a cobrar: el art. 338.3 de la LGSS exige que hayan pasado 18 meses desde que te reconocieron la prestación anterior, y las cotizaciones que ya usaste no cuentan para la nueva (art. 338.4). Cuando pasen, introduce solo los meses cotizados desde entonces.",
  6: "Con esos meses cotizados el derecho no existe: hacen falta al menos 12 meses cotizados por cese de actividad en los 48 anteriores al cese y, de ellos, al menos 12 en los 24 inmediatamente anteriores (art. 338.1 de la LGSS). Cuenta solo las cotizaciones por cese que no hayas usado en una prestación anterior.",
  7: "Revisa los meses: los cotizados en los últimos 24 meses no pueden ser más que los cotizados en los últimos 48."
};
function pintar() {
  var d = leer();
  if (d.base <= 0 || d.m48 < 0 || d.m24 < 0 || d.hijos < 0 || d.edad < 1) { aviso("Revisa los datos: la base debe ser mayor que 0, los meses y los hijos no pueden ser negativos y indica tu edad."); return; }
  var r = calcular(d);
  if (r.bloqueo === 7) { aviso(MSG[7]); return; }
  if (r.bloqueo > 0) { sinDerecho(r.bloqueo, MSG[r.bloqueo]); return; }
  var cond = [];
  if (r.condTrabajo) cond.push("mientras trabajes por cuenta propia o ajena no cobras la prestación, se suspende (arts. 340.1.c y 342.1): la cifra es la que cobrarías si dejas toda actividad");
  if (r.condEdad) cond.push("con " + EM.num(d.edad, 0) + " años puede que ya hayas cumplido la edad ordinaria de jubilación según tus años cotizados (65 años con 38 años y 3 meses cotizados, 66 años y 10 meses si no), y entonces el derecho no existe si el cese es definitivo (art. 330.1.d)");
  var verdict = "Con tus datos, tendrías derecho a " + eur(r.prest) + " al mes durante " + txtMeses(r.dur) + ": " + eur(r.total) + " brutos en total" +
    (r.ap === 1 ? " (limitada por el máximo de " + eur(r.tope) + ")" : (r.ap === -1 ? " (subida al mínimo de " + eur(r.minimo) + ")" : "")) +
    ", si tu cese está acreditado como situación legal, estás al corriente de cuotas y solicitas la prestación a tiempo." +
    (cond.length ? " Ojo: " + cond.join("; y ") + "." : "");
  var note = "<p><strong>Cómo sale:</strong> el " + P.pct + " % de tu base reguladora (" + eur(d.base) + " al mes, la media de tus bases de los últimos 12 meses) son " + eur(r.raw) + " al mes, dentro de un máximo de " + eur(r.tope) + " y un mínimo de " + eur(r.minimo) + " con " + (r.hijos === 0 ? "ningún hijo" : (r.hijos === 1 ? "1 hijo" : "2 o más hijos")) + " a cargo (art. 339). La duración sale de tus " + txtMeses(r.m48) + " cotizados por cese en los 48 anteriores (art. 338.1).</p>" +
    "<p><strong>La cuota:</strong> mientras cobras, el órgano gestor se hace cargo de tu cuota a la Seguridad Social si pides la prestación en plazo; si te retrasas, desde el mes siguiente a la solicitud (arts. 329.1.b y 337.6); esta herramienta no calcula su importe. Para cobrar tienes que estar de baja en el RETA si el cese es definitivo y pedirlo a tu mutua (o al SEPE) hasta el último día del mes siguiente al cese: si te retrasas, se descuentan esos días de la prestación (art. 337.4-5).</p>" +
    "<p><strong>No incluye:</strong> la retención del IRPF (ni la foral), el cese parcial, las sociedades de capital, las cooperativas, el Régimen del Mar y los agrarios, la baja por incapacidad temporal o nacimiento durante la prestación, los requisitos de estar al corriente de cuotas y de activa disponibilidad para trabajar, ni las sanciones.</p>";
  EM.renderResult({
    winner: r.condTrabajo || r.condEdad ? "condicionado" : "derecho", verdict: verdict, tone: r.condTrabajo || r.condEdad ? "warn" : "info",
    bigNumber: r.prest, bigLabel: "al mes durante " + txtMeses(r.dur) + " (bruto)", format: eur,
    barsLabel: "Prestación mensual bruta: tu cuantía frente al mínimo y el máximo",
    bars: [{ label: "Mínimo", value: r.minimo, color: "b" }, { label: "Tu prestación", value: r.prest, color: "a" }, { label: "Máximo", value: r.tope, color: "b" }],
    cols: ["Con tus datos"],
    rows: [
      ["70 % de la base reguladora", eur(r.raw)],
      ["Máximo / mínimo mensual", eur(r.tope) + " / " + eur(r.minimo)],
      ["Límite aplicado", r.ap === 1 ? "máximo" : (r.ap === -1 ? "mínimo" : "ninguno")],
      ["Prestación mensual", eur(r.prest)],
      ["Duración", txtMeses(r.dur)],
      { label: "Total estimado (bruto)", values: [eur(r.total)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
