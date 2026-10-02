// Cuanto ahorrar para comprar casa (2026). Parametros generados desde data/params.json (vivienda_2026; fuentes y fechas alli).
// ccaa[].hab: rebajas de vivienda habitual sin requisitos personales {t nueva|usada, max valor|null, k tipo (nuevo tipo %)|bonif (% de la cuota), pct, txt}; solo se usan para el aviso cuantificado.
// ccaa[].itp / ajd: plano {pct} | escala {tramos [desde, %] progresivos} | bloque {tramos [valor superior a, %]: el tipo del tramo se aplica a todo el valor}.
var P = {"iva": 10, "gastos": 2500, "ccaa": {"andalucia": {"n": "Andalucía", "itp": {"tipo": "plano", "pct": 7}, "ajd": {"tipo": "plano", "pct": 1.2}, "orient": false, "red": "Esta comunidad tiene tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que aquí no se aplican.", "hab": [{"t": "usada", "max": 150000, "k": "tipo", "pct": 6, "txt": "en Andalucía la vivienda habitual de hasta 150.000 € tributa por ITP al 6 % en lugar del 7 % (art. 43.1.a de la Ley 5/2021)"}, {"t": "nueva", "max": 150000, "k": "tipo", "pct": 1, "txt": "en Andalucía la vivienda habitual de hasta 150.000 € tributa por AJD al 1 % en lugar del 1,2 % (art. 50.1.a de la Ley 5/2021)"}]}, "aragon": {"n": "Aragón", "itp": {"tipo": "escala", "tramos": [[0, 8], [400000, 8.5], [450000, 9], [500000, 9.5], [750000, 10]]}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "Esta comunidad tiene tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que aquí no se aplican."}, "asturias": {"n": "Asturias", "itp": {"tipo": "bloque", "tramos": [[0, 8], [300000, 9], [500000, 10]]}, "ajd": {"tipo": "plano", "pct": 1.2}, "orient": false, "red": "Esta comunidad tiene tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que aquí no se aplican."}, "baleares": {"n": "Illes Balears", "itp": {"tipo": "escala", "tramos": [[0, 8], [400000, 9], [600000, 10], [1000000, 12], [2000000, 13]]}, "ajd": {"tipo": "bloque", "tramos": [[0, 1.5], [999999.99, 2]]}, "orient": false, "red": "En Baleares el AJD baja al 1 % (0,5 % para menores de 36 años) en la primera vivienda habitual de hasta 270.151,20 € (art. 17 del DLeg 1/2014) y sube al 2 % si la vivienda vale 1.000.000 € o más (art. 17 bis); hay otros tipos reducidos por edad, familia numerosa, discapacidad o vivienda protegida que aquí no se aplican.", "hab": [{"t": "nueva", "max": 270151.2, "k": "tipo", "pct": 1, "txt": "en Baleares el AJD baja al 1 % en la primera vivienda habitual de hasta 270.151,20 € (art. 17 del DLeg 1/2014)"}]}, "cantabria": {"n": "Cantabria", "itp": {"tipo": "plano", "pct": 9}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "En Cantabria la vivienda habitual tributa por ITP al 7 % hasta 300.000 € (art. 9.2 del DLeg 62/2008), hay un 4 % de ITP para menores de 40 años (art. 9.3.c) y para familias numerosas, monoparentales o con discapacidad, y el AJD baja al 1 % en vivienda habitual (0,1 % para menores de 40 años y otros casos; art. 13.3 y 13.4).", "hab": [{"t": "usada", "max": 300000, "k": "tipo", "pct": 7, "txt": "en Cantabria la vivienda habitual de hasta 300.000 € tributa por ITP al 7 % en lugar del 9 % (art. 9.2 del DLeg 62/2008)"}, {"t": "nueva", "max": null, "k": "tipo", "pct": 1, "txt": "en Cantabria la vivienda habitual tributa por AJD al 1 % en lugar del 1,5 % (art. 13.3 del DLeg 62/2008)"}]}, "clm": {"n": "Castilla-La Mancha", "itp": {"tipo": "plano", "pct": 9}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "En Castilla-La Mancha, en la primera vivienda habitual de hasta 240.000 € financiada con hipoteca de más del 50 %, el AJD baja al 0,75 % (art. 21.2 de la Ley 8/2013, redacción de la Ley 1/2026) y el ITP al 6 % (art. 19.2)."}, "cyl": {"n": "Castilla y León", "itp": {"tipo": "escala", "tramos": [[0, 8], [250000, 10]]}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": true, "red": "En Castilla y León hay un 4 % de ITP en varios supuestos de vivienda habitual (art. 25.3 del DLeg 1/2013)."}, "cataluna": {"n": "Cataluña", "itp": {"tipo": "escala", "tramos": [[0, 10], [600000, 11], [900000, 12], [1500000, 13]]}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "Esta comunidad tiene tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que aquí no se aplican."}, "extremadura": {"n": "Extremadura", "itp": {"tipo": "escala", "tramos": [[0, 8], [360000, 10], [600000, 11]]}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "En Extremadura hay un 7 % para vivienda habitual de hasta 200.000 € con renta de hasta 30.000 € (55.000 € en conjunta), un 4 % para menores de 36 años y otros colectivos, y un 0,5 % de AJD en esos casos (arts. 40, 41 y 47 del DLeg 1/2018)."}, "galicia": {"n": "Galicia", "itp": {"tipo": "plano", "pct": 8}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "En Galicia hay un 7 % de ITP y un 1 % de AJD para vivienda habitual con requisitos (arts. 14 y 15 del DLeg 1/2011)."}, "madrid": {"n": "Comunidad de Madrid", "itp": {"tipo": "plano", "pct": 6}, "ajd": {"tipo": "bloque", "tramos": [[0, 0.4], [120000, 0.5], [180000, 0.75]]}, "orient": false, "red": "En Madrid hay una bonificación del 10 % del ITP y del AJD si es tu vivienda habitual y vale hasta 250.000 € (arts. 30 bis y 38 bis del DLeg 1/2010), y un 4 % de ITP para la vivienda habitual de una familia numerosa (art. 29).", "hab": [{"t": "usada", "max": 250000, "k": "bonif", "pct": 10, "txt": "en Madrid hay una bonificación del 10 % del ITP en la vivienda habitual de hasta 250.000 € (art. 30 bis del DLeg 1/2010)"}, {"t": "nueva", "max": 250000, "k": "bonif", "pct": 10, "txt": "en Madrid hay una bonificación del 10 % del AJD en la vivienda habitual de hasta 250.000 € (art. 38 bis del DLeg 1/2010)"}]}, "murcia": {"n": "Región de Murcia", "itp": {"tipo": "plano", "pct": 7.75}, "ajd": {"tipo": "plano", "pct": 1.5}, "orient": false, "red": "Esta comunidad tiene tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que aquí no se aplican."}, "rioja": {"n": "La Rioja", "itp": {"tipo": "plano", "pct": 7}, "ajd": {"tipo": "plano", "pct": 1.0}, "orient": false, "red": "En La Rioja hay un 5 % (o 3 % con requisitos) de ITP para la vivienda habitual de una familia numerosa (art. 45 de la Ley 10/2017)."}, "valencia": {"n": "Comunitat Valenciana", "itp": {"tipo": "bloque", "tramos": [[0, 9], [1000000, 11]]}, "ajd": {"tipo": "plano", "pct": 1.4}, "orient": false, "red": "En la Comunitat Valenciana la escritura de adquisición de vivienda habitual tributa por AJD al 0,1 % en lugar del 1,4 % (art. 14.Uno de la Ley 13/1997), y hay un 8 % de ITP para jóvenes y otros casos.", "hab": [{"t": "nueva", "max": null, "k": "tipo", "pct": 0.1, "txt": "en la Comunitat Valenciana la escritura de adquisición de vivienda habitual tributa por AJD al 0,1 % en lugar del 1,4 % (art. 14.Uno.a de la Ley 13/1997)"}]}}};
var PLAZO = 25;
function escala(v, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (v > tr[i][0]) s += (Math.min(v, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function bloque(v, tr) { var t = tr[0][1], i; for (i = 0; i < tr.length; i++) if (v > tr[i][0]) t = tr[i][1]; return t; }
function impuesto(v, t) {
  if (t.tipo === "plano") return v * t.pct / 100;
  if (t.tipo === "escala") return escala(v, t.tramos);
  return v * bloque(v, t.tramos) / 100;
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], v = d.precio, nueva = d.tipo === "nueva", iva = 0, aj = 0, itp = 0;
  if (nueva) { iva = v * P.iva / 100; aj = impuesto(v, cc.ajd); } else itp = impuesto(v, cc.itp);
  var imp = iva + aj + itp, ent = v * d.entrada / 100, hip = v - ent, total = ent + imp + d.gastos;
  var n = Math.round(d.anos * 12), i = Math.pow(1 + d.rentab / 100, 1 / 12) - 1;
  var ah = Math.abs(i) < 1e-12 ? total / n : total * i / (Math.pow(1 + i, n) - 1);
  var j = d.interes / 1200, m = PLAZO * 12;
  var cuota = Math.abs(j) < 1e-12 ? hip / m : hip * j / (1 - Math.pow(1 + j, -m));
  return {
    impuestos: imp, itp: itp, iva: iva, ajd: aj, entrada: ent, hipoteca: hip, totalNecesario: total, ahorroMensual: ah, cuotaHipoteca: cuota,
    costeTotal: v + imp + d.gastos, pctExtra: v > 0 ? 100 * (imp + d.gastos) / v : 0, tipoMedio: v > 0 ? 100 * imp / v : 0,
    ltv: v > 0 ? 100 * hip / v : 0, orientativo: cc.orient ? 1 : 0, ccaaNombre: cc.n, aportadoRentab: ah * n
  };
}
function ahorroHab(d, r) {
  var cc = P.ccaa[d.ccaa], nueva = d.tipo === "nueva", out = [], i, h, cuota, nuevo;
  (cc.hab || []).forEach(function (h) {
    if ((h.t === "nueva") !== nueva || (h.max !== null && d.precio > h.max)) return;
    cuota = nueva ? r.ajd : r.itp;
    nuevo = h.k === "tipo" ? d.precio * h.pct / 100 : cuota * (1 - h.pct / 100);
    if (cuota - nuevo > 0.5) out.push({ ahorro: cuota - nuevo, txt: h.txt });
  });
  return out;
}
function eur(x) { return EM.eur(x); }
var IDS = ["precio", "entrada", "gastos", "anos", "rentab", "interes"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.tipo = document.getElementById("tipo").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.precio <= 0 || d.entrada < 0 || d.entrada > 100 || d.anos < 1 || d.anos > 40 || d.gastos < 0 || d.interes < 0 || d.rentab <= -100) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Revisa los datos: el precio debe ser mayor que 0, la entrada estar entre 0 y 100 %, los años entre 1 y 40 y el tipo de interés no puede ser negativo.", note: "" });
    return;
  }
  var r = calcular(d), nueva = d.tipo === "nueva", pc = function (x, k) { return EM.num(x, k === undefined ? 1 : k) + " %"; };
  var verdict = "Para comprar una vivienda " + (nueva ? "nueva" : "usada") + " de " + eur(d.precio) + " en " + r.ccaaNombre + " necesitas tener ahorrados " + eur(r.totalNecesario) + ": " + eur(r.entrada) + " de entrada, " + eur(r.impuestos) + " de impuestos y " + eur(d.gastos) + " de gastos. Para llegar en " + d.anos + (d.anos === 1 ? " año" : " años") + " tendrías que ahorrar " + eur(r.ahorroMensual) + " al mes.";
  var note = "";
  if (r.orientativo) note += "<p><strong>Cifra orientativa:</strong> para " + r.ccaaNombre + " la norma de tipos consultada es un texto consolidado antiguo; contrasta el tipo con la Agencia Tributaria de tu comunidad.</p>";
  note += "<p><strong>Impuestos:</strong> " + (nueva
    ? "en vivienda nueva pagas IVA del " + pc(P.iva, 0) + " (" + eur(r.iva) + ") y el Impuesto de Actos Jurídicos Documentados (" + eur(r.ajd) + ", " + pc(100 * r.ajd / d.precio, 2) + " del precio sin IVA) con el tipo general de " + r.ccaaNombre + "; no pagas ITP"
    : "en vivienda usada pagas el Impuesto de Transmisiones Patrimoniales con el tipo general de " + r.ccaaNombre + " (" + eur(r.itp) + ", " + pc(r.tipoMedio, 2) + " del precio); no pagas IVA") + ". Con impuestos y gastos, la compra cuesta " + pc(r.pctExtra) + " más que el precio.</p>";
  ahorroHab(d, r).forEach(function (h) {
    note += "<p><strong>Posible ahorro si es tu vivienda habitual:</strong> " + h.txt + ". Con " + eur(d.precio) + " pagarías unos " + eur(h.ahorro) + " menos que la cifra de arriba, que usa el tipo general.</p>";
  });
  note += "<p><strong>Tipos reducidos:</strong> esta calculadora aplica solo el tipo general. " + cc_red(d.ccaa) + " Consulta tu comunidad: si cumples los requisitos puedes pagar menos.</p>";
  note += "<p><strong>Hipoteca implícita:</strong> con " + eur(r.entrada) + " de entrada, la hipoteca sería de " + eur(r.hipoteca) + " (" + pc(r.ltv, 0) + " del precio), con una cuota de unos " + eur(r.cuotaHipoteca) + " al mes a " + PLAZO + " años y un " + pc(d.interes, 2) + " de interés (Euríbor + 1 punto, hipótesis editable).";
  if (r.ltv > 80) note += " Los bancos suelen financiar hasta el 80 % del valor; con tan poca entrada es posible que no te concedan esta hipoteca.";
  note += "</p><p><strong>Qué no incluye:</strong> los gastos de notaría, registro, gestoría y tasación son una estimación tuya (por defecto " + eur(P.gastos) + "), no una cifra oficial: pide presupuestos. Tampoco incluye cuotas de comunidad, reformas, ajuar, seguros vinculados, comisiones ni el AJD de la hipoteca (lo paga el banco, art. 29 del texto refundido del ITP y AJD, RDL 17/2018). País Vasco, Navarra, Canarias (IGIC), Ceuta y Melilla no están cubiertos. Supone que el ahorro mensual se ingresa al final de cada mes y que partes de cero.</p>";
  EM.renderResult({
    winner: nueva ? "nueva" : "usada", verdict: verdict, tone: r.ltv > 80 ? "warn" : "ok",
    bigNumber: r.totalNecesario, bigLabel: "de ahorro para entrar a vivir (entrada, impuestos y gastos)", format: eur,
    barsLabel: "De dónde sale el dinero que necesitas",
    bars: [{ label: "Entrada (" + pc(d.entrada, 0) + ")", value: r.entrada, color: "a" }, { label: nueva ? "Impuestos (IVA y AJD)" : "Impuestos (ITP)", value: r.impuestos, color: "b" }, { label: "Notaría, registro, gestoría y tasación (estimación)", value: d.gastos, color: "c" }],
    cols: ["Importe"],
    rows: [
      ["Precio de la vivienda" + (nueva ? " (sin IVA)" : ""), eur(d.precio)],
      ["Entrada", eur(r.entrada)],
      [nueva ? "IVA + AJD" : "ITP", eur(r.impuestos)],
      ["Gastos (estimación tuya)", eur(d.gastos)],
      { label: "Ahorro necesario", values: [eur(r.totalNecesario)], strong: true },
      ["Ahorro mensual para llegar en " + d.anos + (d.anos === 1 ? " año" : " años"), eur(r.ahorroMensual)],
      ["Hipoteca (importe)", eur(r.hipoteca)],
      ["Cuota mensual estimada", eur(r.cuotaHipoteca)]
    ],
    note: note
  });
}
function cc_red(c) { return P.ccaa[c].red || ""; }
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
