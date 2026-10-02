// Fianza y garantias adicionales del alquiler (LAU art. 36, 17.2 y 20.1). Parametros: data/params.json -> fianza_alquiler_2026 (fuentes y fechas alli).
var P = {"fianzaViv": 1, "fianzaUso": 2, "garMax": 2, "aniosPf": 5, "aniosPj": 7, "adelMax": 1};
// Todo en euros. El exceso de fianza sobre la legal cuenta como garantia adicional y suma en su tope.
// Vivienda: fianza P.fianzaViv, garantia <= P.garMax mensualidades si la duracion pactada <= 5 (7 si arrendador persona juridica), 1 mensualidad adelantada, gestion a cargo del arrendador.
// Uso distinto: fianza P.fianzaUso; la ley no pone tope a la garantia, al adelanto ni a la comision en esta calculadora (se admite lo pedido).
function calcular(d) {
  var R = d.renta, viv = d.tipo === "viv";
  var lim = d.arr === "pj" ? P.aniosPj : P.aniosPf;
  var fl = (viv ? P.fianzaViv : P.fianzaUso) * R;
  var sin = (viv && d.duracion <= lim) ? 0 : 1;
  var extraF = Math.max(0, d.fianza * R - fl);   // fianza pedida por encima de la legal = garantia adicional en metalico (art. 36.5)
  var pideG = d.garantia * R + extraF, gm = sin ? pideG : P.garMax * R;
  var adm = viv ? P.adelMax * R : d.adelanto * R;
  var cm = viv ? 0 : d.comision;
  var exF = 0, exG = Math.max(0, pideG - gm), exA = Math.max(0, d.adelanto * R - adm), exC = Math.max(0, d.comision - cm);
  var ped = (d.fianza + d.garantia + d.adelanto) * R + d.comision, no = exF + exG + exA + exC;
  return { fianzaLegal: fl, garantiaMax: gm, sinTope: sin, limiteAnios: lim, maxLegal: fl + gm + adm + cm, pedido: ped, exigible: ped - no, noExigible: no,
    exFianza: exF, pedidoG: pideG, exGarantia: exG, exAdelanto: exA, exComision: exC };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["renta", "duracion", "fianza", "garantia", "adelanto", "comision"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.tipo = document.getElementById("tipo").value; d.arr = document.getElementById("arr").value; return d;
}
function pintar() {
  var d = leer();
  if (d.renta <= 0 || d.duracion <= 0 || d.fianza < 0 || d.garantia < 0 || d.adelanto < 0 || d.comision < 0) return;
  var r = calcular(d), viv = d.tipo === "viv", no = r.noExigible;
  var piezas = [];
  if (r.exGarantia > 0) piezas.push(EM.eur(r.exGarantia) + " de garantía adicional (incluida la fianza que pase de la legal) por encima de " + EM.num(P.garMax) + " mensualidades (art. 36.5)");
  if (r.exAdelanto > 0) piezas.push(EM.eur(r.exAdelanto) + " de renta adelantada por encima de " + EM.num(P.adelMax) + " mensualidad (art. 17.2)");
  if (r.exComision > 0) piezas.push(EM.eur(r.exComision) + " de comisión de agencia o formalización (art. 20.1)");
  var verdict = no > 0.005
    ? 'Con tus datos, te piden ' + EM.eur(r.pedido) + ' al firmar y la ley solo permite exigirte ' + EM.eur(r.exigible) + ': puedes negarte a pagar ' + EM.eur(no) + ' (' + piezas.join("; ") + ').'
    : 'Con tus datos, lo que te piden (' + EM.eur(r.pedido) + ') cabe dentro de lo que la ley permite exigir al firmar' + (r.sinTope && viv && d.garantia > 0 ? ', y en tu caso la ley no pone tope a la garantía adicional' : '') + ': no hay nada que puedas negarte a pagar por estas reglas.';
  var rows = [
    { label: "Fianza en metálico", values: [EM.eur(Math.min(d.fianza * d.renta, r.fianzaLegal)), EM.eur(r.fianzaLegal), EM.eur(0)] },
    { label: "Garantía adicional (aval, depósito, seguro; incluye la fianza que pase de la legal)", values: [EM.eur(r.pedidoG), r.sinTope ? "Sin tope legal" : EM.eur(r.garantiaMax), EM.eur(r.exGarantia)] },
    { label: "Renta por adelantado", values: [EM.eur(d.adelanto * d.renta), viv ? EM.eur(P.adelMax * d.renta) : "Sin tope legal", EM.eur(r.exAdelanto)] },
    { label: "Comisión de agencia o formalización", values: [EM.eur(d.comision), viv ? EM.eur(0) : "Pactable", EM.eur(r.exComision)] },
    { label: "Total al firmar", values: [EM.eur(r.pedido), EM.eur(r.exigible), EM.eur(no)], strong: true }
  ];
  var note = '<p><strong>Tu límite:</strong> ' + (viv
    ? 'en vivienda la garantía adicional queda limitada a ' + EM.num(P.garMax) + ' mensualidades (' + EM.eur(P.garMax * d.renta) + ') si el contrato dura hasta ' + EM.num(r.limiteAnios) + ' años' + (d.arr === "pj" ? ' (casero persona jurídica)' : ' (casero persona física; serían ' + EM.num(P.aniosPj) + ' si fuese persona jurídica)') + '; tu contrato dura ' + EM.num(d.duracion, 1) + (r.sinTope ? ' años, así que la ley no pone tope a la garantía.' : ' años, así que el tope se aplica.')
    : 'en arrendamientos para uso distinto de vivienda la fianza es de ' + EM.num(P.fianzaUso) + ' mensualidades y esta calculadora no aplica otros topes (garantía, adelanto y comisión se pactan).') + '</p>';
  note += '<p><strong>Lo que no calcula:</strong> el depósito de la fianza en el organismo de tu comunidad (disposición adicional 3.ª; cuantía y plazo varían), el interés legal si te devuelven la fianza pasado un mes desde la entrega de llaves (art. 36.4), la actualización de la fianza en cada prórroga (art. 36.2), las reglas de contratos anteriores a 2019 o a mayo de 2023, ni temporada, habitaciones, subarriendos o alquiler social.</p>';
  EM.renderResult({
    winner: (no > 0.005 ? "n" : "ok") + (r.exGarantia > 0 ? "g" : "") + (r.exAdelanto > 0 ? "a" : "") + (r.exComision > 0 ? "c" : ""), verdict: verdict, tone: no > 0.005 ? "warn" : "ok",
    bigNumber: no, bigLabel: "que no te pueden exigir al firmar", format: EM.eur,
    barsLabel: "Lo que te piden frente a lo exigible", bars: [{ label: "Te piden", value: r.pedido, color: "a" }, { label: "La ley permite exigir", value: r.exigible, color: "b" }],
    cols: ["Te piden", "La ley permite exigir", "Puedes negarte a pagar"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
