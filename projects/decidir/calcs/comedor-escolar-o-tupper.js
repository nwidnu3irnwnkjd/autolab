// Comedor escolar o tupper/comer en casa: coste por curso (dinero y tiempo) para N hijos.
// Comedor = hijos x dias x menu x (1 - descuento). Tupper = dias x (hijos x compra por comida + minutos/60 x valor de la hora) + material por curso.
// Con valor de la hora 0 el tiempo no cuenta en euros, pero se muestran las horas. Empate si la diferencia < 5 %.
// ganador: 0 comedor, 1 tupper, 2 empate. menuEq: precio maximo del menu al que el comedor iguala al tupper (-1 si no existe).
function calcular(d) {
  var desc = d.desc / 100, comedor = d.hijos * d.dias * d.menu * (1 - desc);
  var horas = d.dias * d.minutos / 60, tiempo = horas * d.valorHora;
  var compra = d.dias * d.hijos * d.compra, tupper = compra + tiempo + d.material, dif = comedor - tupper;
  var m = Math.min(comedor, tupper), g = Math.abs(dif) < 0.05 * m || Math.abs(dif) < 1e-9 ? 2 : (dif > 0 ? 1 : 0);
  var den = d.hijos * d.dias * (1 - desc), menuEq = den > 0 ? tupper / den : -1;
  return { comedor: comedor, comedorDia: d.hijos * d.menu * (1 - desc), tupper: tupper, tupperDia: d.dias > 0 ? tupper / d.dias : 0,
    compra: compra, tiempo: tiempo, horas: horas, diferencia: dif, menuEq: menuEq, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["menu", "dias", "desc", "hijos", "compra", "minutos", "valorHora", "material"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.menu <= 0 || d.dias < 1 || d.hijos < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Indica el precio del menú (mayor que 0 €), al menos 1 día de comedor y al menos 1 hijo.", tone: "warn", note: "<p>Sin esos datos no hay coste que comparar.</p>" });
    return;
  }
  if (d.dias > 366 || d.desc > 100 || d.hijos > 10 || d.minutos > 240) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: hasta 366 días, un descuento de 0 a 100 %, hasta 10 hijos y 240 minutos de preparación al día.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, ab = Math.abs(r.diferencia), w, verdict, tone = "ok";
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con tus datos hay empate práctico: el comedor (" + eur(r.comedor) + ") y el tupper (" + eur(r.tupper) + ") cuestan casi lo mismo por curso, con menos de un 5 % de diferencia.";
  } else if (g === 0) {
    w = "comedor";
    verdict = "Con tus datos, gana el comedor por " + eur(ab) + " al curso: " + eur(r.comedor) + " frente a " + eur(r.tupper) + " del tupper" + (d.valorHora > 0 ? " (contando tu tiempo a " + eur(d.valorHora, 2) + " la hora)" : "") + ".";
  } else {
    w = "tupper";
    verdict = "Con tus datos, gana el tupper por " + eur(ab) + " al curso: " + eur(r.tupper) + " frente a " + eur(r.comedor) + " del comedor" + (d.valorHora > 0 ? " (contando tu tiempo a " + eur(d.valorHora, 2) + " la hora)" : "") + (r.menuEq > 0 ? ". El comedor igualaría si el menú costara " + eur(r.menuEq, 2) + " o menos." : ".");
  }
  var note = "<p><strong>Lectura:</strong> el comedor cuesta " + eur(r.comedorDia, 2) + " al día y el tupper " + eur(r.tupperDia, 2) + " al día de media (con material). Prepararlo te lleva " + EM.num(r.horas, 0) + " horas al curso" + (d.valorHora > 0 ? ", que suman " + eur(r.tiempo) + " con el valor de la hora que has puesto" : " (no cuentan en euros porque has puesto 0 € la hora)") + ". ";
  if (g === 1 && r.menuEq > 0) note += "El punto de equilibrio del comedor, con el resto igual, es un menú de <strong>" + eur(r.menuEq, 2) + "</strong>. ";
  note += "</p><p><strong>Descuentos y ayudas:</strong> el porcentaje de descuento o beca lo pones tú; consulta tu centro y tu administración educativa para saber si te corresponde alguno y cuánto cubre. No se modelan ayudas fijas en euros ni requisitos de acceso.</p>";
  note += "<p><strong>No incluye:</strong> cuotas de cuidado en el horario del mediodía si el centro las cobra aparte, la comodidad, la organización de tu semana ni lo que prefiera cada niño. Esto compara costes, no recomienda ninguna forma de comer. Se supone el mismo precio de menú y de compra todo el curso.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia al curso" : (g === 0 ? "menos con el comedor al curso" : "menos con el tupper al curso"), format: EM.eur,
    barsLabel: "Coste por curso",
    bars: [{ label: "Comedor" + (w === "comedor" ? " (gana)" : ""), value: r.comedor, color: "a" }, { label: "Tupper" + (w === "tupper" ? " (gana)" : ""), value: r.tupper, color: "b" }],
    cols: ["Comedor", "Tupper"],
    rows: [
      ["Comida (menú o compra)", eur(r.comedor), eur(r.compra)],
      ["Material (envases, neveras)", eur(0), eur(d.material)],
      ["Tu tiempo (" + EM.num(r.horas, 0) + " h)", "—", eur(r.tiempo)],
      { label: "Total por curso", values: [eur(r.comedor), eur(r.tupper)], strong: true },
      ["Coste medio por día de colegio", eur(r.comedorDia, 2), eur(r.tupperDia, 2)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
