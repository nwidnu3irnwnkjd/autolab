// Deduccion por maternidad (art. 81) y por familia numerosa (art. 81 bis) de la Ley del IRPF, ejercicio 2026. Parametros: data/params.json -> maternidad_familia_2026 (fuentes y fechas alli).
var P = { mat: 1200, guar: 1000, famBase: 1200, famExtra: 600, minGen: 3, minEsp: 5, antHijo: 100, antFam: 100, antExtra: 50 };
function calcular(d) {
  var n3 = +d.n3 || 0, mm = +d.mesesMat || 0, mf = +d.mesesFam || 0, gm = +d.guarMeses || 0, gasto = +d.guarGasto || 0, h = +d.hijosFam || 0, cot = +d.cotiz || 0, fam = String(d.fam), t = /x2$/.test(fam) ? 2 : 1;
  fam = fam.replace(/x2$/, "");
  var cero = { invalido: 0, mat: 0, guar: 0, fam: 0, especial: 0, exceso: 0, deduccion: 0, recorte: 0, anticipoMes: 0, anticipoAnual: 0, resto: 0, hijosExtra: 0 };
  var mal = mm < 0 || mm > 12 || mf < 0 || mf > 12 ||
    (fam === "general" && (h < 3 || n3 > h)) || (fam === "especial" && (h < 4 || n3 > h)) || (fam === "mono2" && n3 > 2);
  if (mal) { cero.invalido = 1; return cero; }
  var fm = mm / 12, ff = mf / 12, o = cero;
  o.mat = n3 * P.mat * fm;
  o.guar = n3 * Math.min(P.guar * Math.min(gm, mm) / 12, Math.max(gasto, 0));
  var anFam = 0;
  if (fam !== "no") {
    var base = P.famBase * ff / t;
    o.fam = Math.min(base, Math.max(cot, 0));
    o.recorte = base - o.fam;
    anFam = P.antFam / t;
    if (fam === "especial") { o.especial = P.famBase * ff / t; anFam += P.antFam / t; }
    if (fam !== "mono2") {
      o.hijosExtra = Math.max(0, h - (fam === "general" ? P.minGen : P.minEsp));
      o.exceso = P.famExtra * o.hijosExtra * ff / t;
      anFam += P.antExtra * o.hijosExtra / t;
    }
  }
  o.deduccion = o.mat + o.guar + o.fam + o.especial + o.exceso;
  o.anticipoMes = P.antHijo * n3 + anFam;
  o.anticipoAnual = P.antHijo * n3 * mm + anFam * mf;
  o.resto = o.deduccion - o.anticipoAnual;
  return o;
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["mesesMat", "mesesFam", "guarMeses", "guarGasto", "hijosFam", "cotiz"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["n3", "fam"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.mesesMat < 0 || d.mesesMat > 12 || d.mesesFam < 0 || d.mesesFam > 12 || d.guarMeses < 0 || d.guarGasto < 0 || d.cotiz < 0 || d.hijosFam < 0) return;
  var r = calcular(d), n3 = +d.n3;
  if (r.invalido) {
    EM.renderResult({ winner: "inv", tone: "warn", verdict: "Estos datos no encajan con la ley: una familia numerosa general necesita 3 hijos o más, la especial 4 o más (con 4, solo si cumple el supuesto de la Ley 40/2003) y los hijos menores de 3 años no pueden ser más que los hijos de la familia (o 2 si eres un ascendiente separado con dos hijos).",
      note: "<p><strong>Qué hacer:</strong> corrige el número de hijos o la categoría. Las familias con 2 hijos que la ley equipara a numerosas (con un hijo con discapacidad, ascendientes con discapacidad, huérfanos y similares, art. 2.2 de la Ley 40/2003) y las demás equiparaciones no se calculan aquí.</p>" });
    return;
  }
  var partes = [];
  if (r.mat + r.guar > 0) partes.push("maternidad " + eur(r.mat + r.guar) + (r.guar > 0 ? " (de ellos " + eur(r.guar) + " por guardería)" : ""));
  if (r.fam + r.especial + r.exceso > 0) partes.push("familia numerosa " + eur(r.fam + r.especial + r.exceso));
  var verdict;
  if (r.deduccion <= 0) {
    verdict = n3 === 0 && d.fam === "no"
      ? "Con estos datos no te corresponde la deducción por maternidad ni la de familia numerosa: la primera necesita al menos un hijo menor de 3 años y la segunda el título de familia numerosa (o ser un ascendiente separado con dos hijos), y en ambos casos haber cobrado paro al nacer el hijo o haber estado de alta con 30 días cotizados (familia numerosa: alta, paro o pensión en el mes)."
      : "Con estos datos la deducción sale en 0 €: " + (d.mesesMat === 0 && d.mesesFam === 0 ? "sin meses con derecho no se genera ninguna parte." : "con cotizaciones de 0 € se pierde la parte básica de 1.200 € de familia numerosa (si cobras paro o pensión no hay tope: escribe 1.200 € o más) y no hay hijos menores de 3 años ni categoría especial que sumen otra.");
  } else {
    verdict = "Con estos datos Hacienda te devuelve " + eur(r.deduccion) + " al año (" + partes.join(" y ") + "), aunque no pagues IRPF, porque minora la cuota diferencial.";
    if (r.recorte > 0.005) verdict += " Las cotizaciones indicadas (" + eur(+d.cotiz) + ") limitan la parte básica de familia numerosa y pierdes " + eur(r.recorte) + ".";
  }
  var rows = [];
  rows.push({ label: "Maternidad (1.200 € por hijo menor de 3 años)", values: [eur(r.mat), n3 > 0 ? eur(P.antHijo * n3) : "—"] });
  rows.push({ label: "Incremento por guardería autorizada (hasta 1.000 € por hijo)", values: [eur(r.guar), "No se anticipa"] });
  if (d.fam !== "no") {
    var bm = r.fam > 0 || r.recorte > 0 ? P.antFam / ((/x2$/.test(d.fam) ? 2 : 1)) : 0;
    rows.push({ label: "Familia numerosa o ascendiente separado con 2 hijos (1.200 €, con tope de cotizaciones)", values: [eur(r.fam), eur(bm)] });
    if (/^especial/.test(d.fam)) rows.push({ label: "Incremento por categoría especial (otros 1.200 €)", values: [eur(r.especial), eur(P.antFam / ((/x2$/.test(d.fam) ? 2 : 1)))] });
    if (d.fam !== "mono2") rows.push({ label: "Incremento por hijos sobre el mínimo (600 € cada uno: " + EM.num(r.hijosExtra) + ")", values: [eur(r.exceso), eur(P.antExtra * r.hijosExtra / ((/x2$/.test(d.fam) ? 2 : 1)))] });
  }
  rows.push({ label: "Total de la deducción", values: [eur(r.deduccion), eur(r.anticipoMes)], strong: true });
  var note = '<p><strong>Abono anticipado:</strong> si lo solicitas (modelo 140 para maternidad, modelo 143 para familia numerosa), la Agencia Tributaria te ingresa unos <strong>' + eur(r.anticipoMes) + ' al mes</strong> durante los meses con derecho (' + eur(r.anticipoAnual) + ' en el año).';
  if (r.resto >= 0.005) note += ' El resto, ' + eur(r.resto) + ', lo recibes al presentar la declaración.';
  else if (r.resto <= -0.005) note += ' Como el anticipo supera la deducción real en ' + eur(-r.resto) + ', tendrías que regularizarlo en la declaración (sin intereses de demora si no es por tu culpa).';
  else note += ' No queda nada pendiente para la declaración.';
  note += ' Lo anticipado no se vuelve a restar de la cuota diferencial, así que el total anual es el mismo; la parte de guardería no se anticipa.</p>';
  note += '<p><strong>Límites:</strong> la maternidad no tiene tope de cotizaciones; la parte básica de familia numerosa sí (cotizaciones y cuotas de la Seguridad Social del año), pero no los incrementos de categoría especial ni por hijos adicionales. Es una deducción reembolsable: no depende de tu cuota de IRPF, por eso la calculadora no la pide. ' +
    'No incluye deducciones autonómicas (hay comunidades con importes propios para hijos, guardería o familia numerosa), el complemento de ayuda para la infancia (los meses en que se cobra no dan maternidad), el aumento de 150 € del mes en que se cumplen 30 días cotizados, personas con discapacidad a cargo, tutela o acogimiento, los meses de guardería posteriores a los 3 años, ni el País Vasco y Navarra. Si el otro progenitor también tiene derecho a la deducción de familia numerosa, el importe se reparte a partes iguales (opciones «dos titulares»). Para la maternidad no hace falta seguir de alta: basta haberlo estado (o cobrar paro) al nacer el hijo o después, y tener derecho al mínimo por descendientes.</p>';
  EM.renderResult({
    winner: r.deduccion > 0 ? "hay" : "cero", verdict: verdict, tone: r.deduccion > 0 ? "ok" : "warn",
    bigNumber: r.deduccion, bigLabel: "de deducción al año (reembolsable)", format: EM.eur,
    barsLabel: "De dónde sale", bars: [{ label: "Maternidad y guardería", value: r.mat + r.guar, color: "a" }, { label: "Familia numerosa", value: r.fam + r.especial + r.exceso, color: "b" }],
    cols: ["Importe al año", "Al mes si lo anticipas"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
