// Mudanza: empresa o furgoneta de alquiler. Coste directo de la furgoneta (alquiler por dias + combustible + extras + ayudantes), reserva de danos (hipotesis) y tu tiempo.
// Supuestos fijos declarados: capacidad 20 m3 por viaje, 600 km por dia de alquiler, 80 km/h, 0,6 horas-persona por m3 (carga y descarga), reserva de danos 5 EUR/m3, la furgoneta se devuelve en origen (ida y vuelta).
var CAP = 20, KMDIA = 600, VEL = 80, HM3 = 0.6, DANO = 5, MAXKM = 3000;
function furgo(d, dist) {
  var viajes = Math.ceil(d.vol / CAP), km = viajes * 2 * dist, dias = Math.max(1, Math.ceil(km / KMDIA));
  var hCarga = d.vol * HM3 / (1 + d.nayud);
  var directo = dias * d.alqdia + km * d.kmfurgo + d.extras + d.nayud * d.eurayud * hCarga;
  return { viajes: viajes, km: km, dias: dias, hCarga: hCarga, hUser: hCarga + km / VEL, directo: directo };
}
function calcular(d) {
  var f = furgo(d, d.dist), reserva = DANO * d.vol, d1 = d.empresa - f.directo, d2 = d1 - reserva, tipo, vEq = 0, dist, kmEq;
  if (d1 <= 0) tipo = 1; else if (d2 <= 0) tipo = 2; else { tipo = 3; vEq = d2 / f.hUser; }
  kmEq = -1;
  for (dist = 0; dist <= MAXKM; dist++) { if (furgo(d, dist).directo < d.empresa) kmEq = dist; else break; }
  return {
    costeFurgo: f.directo, reserva: reserva, costeFurgoConReserva: f.directo + reserva, costeEmpresa: d.empresa,
    m3Furgo: f.directo / d.vol, m3Empresa: d.empresa / d.vol, viajes: f.viajes, dias: f.dias, km: f.km,
    horasTuyas: f.hUser, horasCarga: f.hCarga, diferencia: d1, tipo: tipo, horaEq: vEq, kmEq: kmEq,
    presupuestoEq: f.directo + reserva
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["vol", "dist", "empresa", "alqdia", "kmfurgo", "extras", "nayud", "eurayud"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.vol <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un volumen mayor que 0 m³.", tone: "warn", note: "<p>Sin volumen que mover no hay mudanza que comparar.</p>" });
    return;
  }
  if (d.vol > 80 || d.dist > 3000 || d.nayud > 8 || Math.floor(d.nayud) !== d.nayud) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 80 m³, 3.000 km y 8 ayudantes (número entero).", tone: "warn", note: "<p>Fuera de esos valores el modelo de una furgoneta no tendría sentido práctico: consulta presupuestos.</p>" });
    return;
  }
  var r = calcular(d), t = r.tipo, w = t === 3 ? "furgoneta" : "empresa", verdict, abs = Math.abs(r.diferencia);
  var h = function (x) { return EM.num(x, 1) + " h"; };
  if (t === 1) verdict = "Con estos datos compensa la empresa: su presupuesto (" + eur(d.empresa) + ") es " + (abs < 1 ? "igual" : eur(abs) + " menor") + " que el gasto directo de la furgoneta (" + eur(r.costeFurgo) + "), y además te ahorras " + h(r.horasTuyas) + " de tu tiempo.";
  else if (t === 2) verdict = "Con estos datos la furgoneta sale " + eur(r.diferencia) + " más barata en gasto directo, pero la reserva de daños de la hipótesis (" + eur(r.reserva) + ") deja la empresa como mejor opción incluso sin valorar tu tiempo.";
  else verdict = "Con estos datos compensa la furgoneta si tu hora vale menos de " + eur(r.horaEq) + ": cuesta " + eur(r.costeFurgo) + " frente a " + eur(d.empresa) + " de la empresa, y con la reserva de daños y tus " + h(r.horasTuyas) + " de trabajo la empresa pasaría a ganar si tu hora vale más.";
  var note = "<p><strong>Lectura:</strong> el coste por m³ es " + eur(r.m3Furgo, 2) + " con la furgoneta (sin reserva ni tu tiempo) y " + eur(r.m3Empresa, 2) + " con la empresa. La furgoneta necesita " + r.viajes + (r.viajes === 1 ? " viaje" : " viajes") + " (" + EM.num(r.km, 0) + " km en total, ida y vuelta) y " + r.dias + (r.dias === 1 ? " día" : " días") + " de alquiler; tú trabajarías unas " + h(r.horasTuyas) + " entre carga, descarga y conducción. ";
  if (r.kmEq >= 0 && r.kmEq < 3000) note += "Con tu presupuesto de empresa, el gasto directo de la furgoneta se mantiene por debajo de él hasta unos <strong>" + EM.num(r.kmEq, 0) + " km</strong>. ";
  else if (r.kmEq < 0) note += "Con tu presupuesto de empresa, la furgoneta no queda por debajo ni sin distancia. ";
  else note += "Con tu presupuesto de empresa, la furgoneta sale por debajo hasta los 3.000 km del modelo. ";
  note += "La empresa compensaría con cualquier presupuesto por debajo de " + eur(r.presupuestoEq) + " (furgoneta más reserva de daños, sin tu tiempo).</p>";
  note += "<p><strong>Ojo:</strong> la reserva de daños (" + eur(DANO) + " por m³) es una hipótesis, no una estadística: si la empresa asegura tus muebles y tu furgoneta no, puede pesar más. Supuestos fijos: furgoneta de " + CAP + " m³ por viaje, " + KMDIA + " km por día de alquiler, " + VEL + " km/h, " + EM.num(HM3, 1) + " horas por m³ y persona, y se devuelve en origen. No incluye aparcamiento ni permisos municipales, ascensor o montacargas, seguros específicos de la mudanza ni impuestos: consulta con tu ayuntamiento, tu aseguradora y la empresa.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: "ok",
    bigNumber: t === 3 ? r.costeFurgo : d.empresa, bigLabel: t === 1 ? "€ de la empresa, menos que el gasto directo de la furgoneta" : t === 2 ? "€ de la empresa, menos que la furgoneta con reserva de daños" : "€ de gasto directo de la furgoneta, sin reserva ni tu tiempo", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste de la mudanza",
    bars: [{ label: "Empresa" + (w === "empresa" ? " (gana)" : ""), value: r.costeEmpresa, color: "a" }, { label: "Furgoneta, gasto directo" + (w === "furgoneta" ? " (gana)" : ""), value: r.costeFurgo, color: "b" }, { label: "Furgoneta con reserva de daños", value: r.costeFurgoConReserva, color: "b" }],
    cols: ["Empresa", "Furgoneta"],
    rows: [
      ["Coste directo", eur(r.costeEmpresa), eur(r.costeFurgo)],
      ["Con reserva de daños (hipótesis)", eur(r.costeEmpresa), eur(r.costeFurgoConReserva)],
      ["Coste por m³", eur(r.m3Empresa, 2), eur(r.m3Furgo, 2)],
      ["Tu tiempo de trabajo", "—", h(r.horasTuyas)],
      ["Valor de tu hora de equilibrio", "—", t === 3 ? eur(r.horaEq) : "no compensa"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
