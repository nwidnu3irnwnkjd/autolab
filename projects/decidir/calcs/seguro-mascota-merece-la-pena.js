// Seguro de mascota: valor esperado con y sin seguro, probabilidad de equilibrio, peor escenario con carencia y hucha propia.
// Modelo: como mucho UN evento grave al ano, con probabilidad p. El seguro paga min(max(coste - franquicia, 0), limite) por evento.
// Hucha propia: guardas la prima cada mes (sin rentabilidad, prudente) en vez de pagarla. La prima se supone constante.
function calcular(d) {
  var p = d.prob / 100, H = Math.max(Math.round(d.horizonte), 1), M = Math.max(Math.round(d.carencia), 0);
  var cover = Math.min(Math.max(d.coste - d.franq, 0), d.limite), bolsillo = d.coste - cover, mes = M + 1;
  var sin = p * d.coste, con = d.prima + p * bolsillo, mensual = d.prima / 12;
  var r = {
    cobertura: cover, bolsillo: bolsillo, esperadoSin: sin, esperadoCon: con, ahorroEsperado: sin - con,
    esperadoSinTotal: sin * H, esperadoConTotal: con * H, ahorroTotal: (sin - con) * H,
    probEquilibrio: cover > 0 ? d.prima / cover * 100 : -1,
    anoConEventoSin: d.coste, anoConEventoCon: d.prima + bolsillo,
    mesesHucha: mensual > 0 ? d.coste / mensual : -1, huchaFinal: d.prima * H,
    golpeMes1Con: M > 0 ? d.coste : bolsillo, golpeMes1Hucha: Math.max(0, d.coste - mensual),
    mesCubierto: mes <= 12 ? mes : -1,
    golpeCubiertoCon: mes <= 12 ? bolsillo : -1, golpeCubiertoHucha: mes <= 12 ? Math.max(0, d.coste - mensual * mes) : -1,
    gastoAno1Con: mes <= 12 ? mensual * mes + bolsillo : d.coste,
    mejor: con < sin - 1 ? 0 : (sin < con - 1 ? 1 : 2)
  };
  return r;
}
function eur(x) { return EM.eur(x); }
var IDS = ["prima", "franq", "limite", "carencia", "prob", "coste", "horizonte"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.prima <= 0 || d.coste <= 0 || d.horizonte < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe una prima mayor que 0, un coste del evento grave mayor que 0 y al menos 1 año de horizonte.", tone: "warn",
      note: "<p>Sin prima o sin coste del evento no hay seguro que comparar.</p>" });
    return;
  }
  if (d.prob > 100 || d.horizonte > 30 || d.carencia > 60) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: la probabilidad no puede pasar del 100 %, el horizonte de 30 años ni la carencia de 60 meses.", tone: "warn",
      note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), H = Math.round(d.horizonte), w, verdict;
  var anos = EM.num(H, 0) + (H === 1 ? " año" : " años");
  if (r.cobertura <= 0) {
    w = "sin-seguro";
    verdict = "Con estos datos el seguro no pagaría nada: la franquicia (" + eur(d.franq) + ") alcanza el coste del evento (" + eur(d.coste) + ") o el límite de cobertura es 0, así que solo pagarías la prima.";
  } else if (r.mejor === 0) {
    w = "seguro";
    verdict = "Con estos datos el seguro compensa incluso en valor esperado: ahorra " + eur(r.ahorroEsperado) + " al año de media (" + eur(r.ahorroTotal) + " en " + anos + "), porque tu probabilidad del " + EM.num(d.prob, 1) + " % supera la de equilibrio del " + EM.num(r.probEquilibrio, 1) + " %.";
  } else if (r.mejor === 2) {
    w = "empate";
    verdict = "Con estos datos el seguro y no tenerlo cuestan lo mismo de media (" + eur(r.esperadoSin) + " al año): tu probabilidad coincide con la de equilibrio, " + EM.num(r.probEquilibrio, 1) + " %.";
  } else {
    w = "sin-seguro";
    verdict = "Con estos datos el seguro no compensa en valor esperado: cuesta " + eur(-r.ahorroEsperado) + " más al año de media (" + eur(-r.ahorroTotal) + " en " + anos + "); solo compensaría si la probabilidad anual de un evento grave superase el " + (r.probEquilibrio <= 100 ? EM.num(r.probEquilibrio, 1) + " %" : "100 % (nunca)") + ". Se paga por reducir la varianza: en un año con evento grave pagarías " + eur(r.anoConEventoCon) + " en vez de " + eur(r.anoConEventoSin) + ".";
  }
  var note = "<p><strong>Lectura:</strong> un seguro es una forma de reducir la varianza, no de esperar ganar. ";
  note += "Con tu probabilidad del " + EM.num(d.prob, 1) + " %, el coste medio es " + eur(r.esperadoCon, 2) + " al año con seguro y " + eur(r.esperadoSin, 2) + " sin él. ";
  if (r.probEquilibrio >= 0) note += "La probabilidad de equilibrio es " + (r.probEquilibrio <= 100 ? "del " + EM.num(r.probEquilibrio, 1) + " %" : "superior al 100 %: nunca compensa en valor esperado") + " (prima dividida por lo que paga el seguro en un evento, " + eur(r.cobertura) + "). ";
  note += "Un año sin evento cuesta " + eur(d.prima) + " con seguro y 0 sin él; un año con evento, " + eur(r.anoConEventoCon) + " con seguro y " + eur(r.anoConEventoSin) + " sin él. ";
  note += "Si en vez de pagar la prima la apartas cada mes, reunirías el coste de un evento en " + EM.num(r.mesesHucha, 0) + " meses y tendrías " + eur(r.huchaFinal) + " guardados en " + anos + ".</p>";
  note += "<p><strong>Peor escenario en el año 1:</strong> ";
  if (d.carencia > 0) note += "si el evento llega en el mes 1, dentro de la carencia de " + EM.num(d.carencia, 0) + (d.carencia === 1 ? " mes" : " meses") + ", el seguro no paga y desembolsas " + eur(r.golpeMes1Con) + ". ";
  else note += "sin carencia, si el evento llega en el mes 1 desembolsas " + eur(r.golpeMes1Con) + " con seguro y " + eur(d.coste) + " sin él. ";
  if (r.mesCubierto > 0) note += "Si llega en el primer mes cubierto (el mes " + EM.num(r.mesCubierto, 0) + "), desembolsas " + eur(r.golpeCubiertoCon) + " con seguro; en total, con las primas pagadas, " + eur(r.gastoAno1Con) + " frente a " + eur(d.coste) + " sin seguro. ";
  else note += "Con una carencia de 12 meses o más, un evento en el año 1 no está cubierto. ";
  note += "</p><p><strong>Límites:</strong> la probabilidad es una hipótesis tuya, no una estadística; los importes son ejemplos. Se supone como mucho un evento grave al año y una prima constante. No incluye las exclusiones concretas de ninguna póliza (preexistencias, razas, edad máxima), ni el coste de los gastos pequeños, ni la responsabilidad civil. No sustituye el consejo de tu veterinario.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: r.mejor === 0 && r.cobertura > 0 ? "ok" : "warn",
    bigNumber: r.esperadoCon, bigLabel: "coste esperado al año con seguro (prima incluida)", format: EM.eur,
    barsLabel: "Coste esperado en el horizonte",
    bars: [{ label: "Con seguro" + (r.mejor === 0 && r.cobertura > 0 ? " (más barato)" : ""), value: Math.max(r.esperadoConTotal, 0), color: "a" }, { label: "Sin seguro" + (w === "sin-seguro" ? " (más barato)" : ""), value: Math.max(r.esperadoSinTotal, 0), color: "b" }],
    cols: ["Con seguro", "Sin seguro o hucha"],
    rows: [
      ["Coste esperado al año", eur(r.esperadoCon, 2), eur(r.esperadoSin, 2)],
      ["Coste esperado en " + anos, eur(r.esperadoConTotal), eur(r.esperadoSinTotal)],
      ["Año sin evento grave", eur(d.prima), eur(0)],
      ["Año con evento grave", eur(r.anoConEventoCon), eur(r.anoConEventoSin)],
      ["De golpe si el evento llega en el mes 1", eur(r.golpeMes1Con), eur(d.coste) + " (con hucha, " + eur(r.golpeMes1Hucha) + ")"]
    ],
    note: note
  });
}
var sel = document.getElementById("perfil");
if (sel) sel.addEventListener("change", function () {
  if (sel.value !== "") { document.getElementById("prob").value = sel.value; pintar(); }
});
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
