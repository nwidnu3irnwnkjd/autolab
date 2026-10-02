// Prestacion por nacimiento y cuidado de menor (2026): cuanto cobro y como repartir las semanas. Parametros: data/params.json -> permiso_nacimiento_2026 (fuentes y fechas alli).
// Cada progenitor: 19 semanas individuales e intransferibles (32 si es monoparental); 100 % de la base de cotizacion (tope 5.101,20 EUR/mes) / 30 por dia natural.
var P = {"tope": 5101.2, "dias": 7, "mes": 30, "obl": 6, "total": 19, "mono": 32};
function calcular(d) {
  var mono = d.mono === "si", amp = Math.max(Math.round(d.amp), 0);
  var mx = mono ? P.mono + 2 * amp : P.total + amp;
  var a = Math.round(d.semA), b = mono ? 0 : Math.round(d.semB);
  var r = { bloqueo: 0, esc: 0, maxA: mx, maxB: mono ? 0 : mx };
  if (a < 0 || b < 0 || a > mx || b > mx) { r.bloqueo = 1; return r; }
  if ((a > 0 && a < P.obl) || (b > 0 && b < P.obl)) { r.bloqueo = 2; return r; }
  if (a + b === 0) { r.bloqueo = 3; return r; }
  if ((a > 0 && d.sueldoA <= 0) || (b > 0 && d.sueldoB <= 0)) { r.bloqueo = 4; return r; }
  function persona(sueldo, pct) {
    var p = Math.min(Math.max(pct, 0), 100);
    var base = Math.min(sueldo, P.tope), sem = base * P.dias / P.mes;
    var cs = Math.max(0, p / 100 * sueldo * P.dias / P.mes - sem);
    return { sem: sem, cs: cs, rate: sueldo * P.dias / P.mes - sem - cs };
  }
  var pa = persona(d.sueldoA, d.complA);
  var pb = b > 0 ? persona(d.sueldoB, d.complB) : { sem: 0, cs: 0, rate: 0 };
  r.semanalA = pa.sem; r.semanalB = pb.sem;
  r.prestA = pa.sem * a; r.prestB = pb.sem * b;
  r.complA = pa.cs * a; r.complB = pb.cs * b;
  r.totalA = r.prestA + r.complA; r.totalB = r.prestB + r.complB;
  r.dejadoA = d.sueldoA * P.dias / P.mes * a; r.dejadoB = b > 0 ? d.sueldoB * P.dias / P.mes * b : 0;
  r.perdidaA = pa.rate * a; r.perdidaB = pb.rate * b;
  r.prest = r.prestA + r.prestB; r.compl = r.complA + r.complB; r.total = r.totalA + r.totalB; r.perdida = r.perdidaA + r.perdidaB;
  r.rateA = pa.rate; r.rateB = b > 0 ? pb.rate : 0;
  var dos = !mono && a >= P.obl && b >= P.obl;
  r.optA = a; r.optB = b; r.perdidaOpt = r.perdida; r.ahorro = 0;
  if (!dos) { r.esc = 4; return r; }
  var T = a + b, best = null;
  for (var x = P.obl; x <= mx; x++) {
    var y = T - x;
    if (y < P.obl || y > mx) continue;
    var c = x * pa.rate + y * pb.rate, dist = Math.abs(x - a);
    if (best === null || c < best.c - 1e-9 || (Math.abs(c - best.c) <= 1e-9 && dist < best.dist)) best = { x: x, y: y, c: c, dist: dist };
  }
  r.optA = best.x; r.optB = best.y; r.perdidaOpt = best.c; r.ahorro = Math.max(0, r.perdida - best.c);
  r.esc = r.perdida < 0.5 ? 1 : (r.ahorro >= 1 ? 3 : 2);
  return r;
}
function eur(x) { return EM.eur(x); }
var IDS = ["sueldoA", "sueldoB", "amp", "semA", "semB", "complA", "complB"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.mono = document.getElementById("mono").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
var NO_MODELA = "<p><strong>No incluye:</strong> el neto (la prestación está exenta de IRPF, pero el complemento de la empresa y tu sueldo no, y no calculamos tu retención ni tus cotizaciones); los autónomos, las empleadas de hogar, los desempleados y la prestación no contributiva de quien no llega a la carencia; la adopción y el acogimiento; los funcionarios con permiso retribuido; los regímenes forales; los nacimientos anteriores al 31-7-2025 (si el hijo nació entre el 2-8-2024 y el 30-7-2025, tenías 16 semanas más 2 hasta los 8 años, y hoy solo puedes pedir esas 2; antes del 2-8-2024, 16 semanas); los contratos a tiempo parcial (la base es la suma de las bases de los 12 meses anteriores al mes previo, entre 365: art. 248.1.b de la LGSS); la jornada parcial de las semanas voluntarias; el permiso parental de 8 semanas hasta los 8 años (art. 48 bis del Estatuto de los Trabajadores, no retribuido); el aumento de semanas por hospitalización del recién nacido; ni cuántos de tus días entran en las semanas (si el sueldo cambia, la base también).</p>";
function pintar() {
  var d = leer();
  if (d.sueldoA < 0 || d.sueldoB < 0 || d.amp < 0 || d.complA < 0 || d.complB < 0) { aviso("Revisa los datos: sueldos, ampliaciones y complementos no pueden ser negativos."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Cada progenitor tiene como máximo " + EM.num(r.maxA, 0) + " semanas con tus datos (19 por progenitor, 32 si es monoparental, más 1 por cada hijo adicional o por discapacidad del hijo; con un solo progenitor, 2 por cada una) y no puede tener semanas negativas. Revisa las semanas indicadas (art. 48.4 y 48.6 del Estatuto de los Trabajadores)."); return; }
  if (r.bloqueo === 2) { aviso("Quien disfruta del permiso tiene que tomar al menos las 6 semanas obligatorias inmediatamente posteriores al parto, a jornada completa (art. 48.4.a del Estatuto de los Trabajadores): pon 0 si ese progenitor no lo disfruta, o 6 o más."); return; }
  if (r.bloqueo === 3) { aviso("Indica las semanas que disfruta al menos uno de los dos progenitores (6 o más) para calcular la prestación."); return; }
  if (r.bloqueo === 4) { aviso("Indica el sueldo bruto mensual de cada progenitor que disfruta semanas (mayor que 0): sin él no se puede calcular la base."); return; }
  var mono = d.mono === "si", a = Math.round(d.semA), b = mono ? 0 : Math.round(d.semB), dos = r.esc !== 4;
  var verdict;
  var total = eur(r.total) + " en total" + (b > 0 ? " (" + eur(r.totalA) + " al progenitor A y " + eur(r.totalB) + " al B)" : "");
  if (r.esc === 1) verdict = "Con tus datos, la Seguridad Social os paga " + eur(r.prest) + (r.compl > 0 ? " más " + eur(r.compl) + " de complemento de empresa" : "") + ": " + total + ", el 100 % de la base de cotización, y no pierdes ingresos brutos frente al sueldo. Repartir las semanas de otra forma no cambia la pérdida, que ya es cero.";
  else if (r.esc === 2) verdict = "Con tus datos, cobráis " + total + " y perdéis " + eur(r.perdida) + " brutos frente al sueldo, porque la prestación tiene como tope la base máxima de " + eur(P.tope) + " al mes. Vuestro reparto (" + a + " y " + b + " semanas) ya es el que menos pierde: otro reparto con las mismas semanas totales no mejora el dinero.";
  else if (r.esc === 3) verdict = "Con tus datos, cobráis " + total + " y perdéis " + eur(r.perdida) + " brutos frente al sueldo, porque la prestación tiene como tope la base máxima de " + eur(P.tope) + " al mes. Si repartís las mismas semanas totales como " + r.optA + " para A y " + r.optB + " para B, la pérdida baja a " + eur(r.perdidaOpt) + " (" + eur(r.ahorro) + " menos).";
  else verdict = "Con tus datos, " + (mono ? "como familia monoparental " : "") + "cobras " + total + " por " + a + (b > 0 ? " y " + b : "") + " semanas" + (r.perdida >= 0.5 ? ", y pierdes " + eur(r.perdida) + " brutos frente al sueldo por el tope de la base máxima de " + eur(P.tope) + " al mes o por tu complemento" : ", sin perder ingresos brutos frente al sueldo") + (mono ? "." : ". Con un solo progenitor que disfruta no hay reparto que optimizar.");
  var note = "<p><strong>Ámbito:</strong> La herramienta vale para nacimientos desde el 31-7-2025. Si el hijo nació entre el 2-8-2024 y el 30-7-2025, tenías 16 semanas (6 + 10) más las 2 (4 si eres monoparental) hasta los 8 años, y hoy solo puedes pedir esas 2 (4); antes del 2-8-2024, 16 semanas.</p>" +
    "<p><strong>Cómo sale:</strong> la prestación es el 100 % de la base de cotización por contingencias comunes (tu sueldo bruto mensual con pagas prorrateadas, con el tope de " + eur(P.tope) + "), dividida entre 30 y cobrada por cada día natural: " + eur(r.semanalA) + " por semana el progenitor A" + (b > 0 ? " y " + eur(r.semanalB) + " el B" : "") + ". Cada progenitor tiene su derecho individual: las semanas que uno no use no pasan al otro (salvo fallecimiento de un progenitor, en que el otro puede usar lo que reste).</p>";
  if (r.perdida >= 0.5) note += "<p><strong>Dónde está la pérdida:</strong> solo cobras menos que tu sueldo si este supera " + eur(P.tope) + " al mes (la base máxima) y la empresa no completa la diferencia. Cada semana que tome el progenitor A cuesta " + eur(r.rateA) + " brutos" + (b > 0 ? " y cada semana del B, " + eur(r.rateB) : "") + ".</p>";
  if (dos) note += "<p><strong>Simultáneo o sucesivo:</strong> da lo mismo en dinero, porque cada progenitor cobra sus semanas por separado. Cambia otra cosa: las 6 semanas obligatorias van seguidas tras el parto, las demás se reparten a vuestro gusto hasta los 12 meses del hijo (y 2 de ellas, hasta los 8 años), y la empresa puede limitar el disfrute simultáneo si trabajáis en la misma.</p>";
  if (mono && d.semB > 0) note += "<p>Como familia monoparental solo cuenta el progenitor A: se ignoran las semanas del B.</p>";
  note += "<p>La prestación está exenta de IRPF (art. 7.h de la Ley del IRPF); el complemento de la empresa, no. El importe es bruto frente a bruto: en neto la comparación depende de tu retención y tus cotizaciones, y no la calculamos.</p>";
  note += NO_MODELA;
  var rows = [
    ["Semanas disfrutadas", EM.num(a, 0), EM.num(b, 0), EM.num(a + b, 0)],
    ["Prestación de la Seguridad Social", eur(r.prestA), eur(r.prestB), eur(r.prest)],
    ["Complemento de la empresa", eur(r.complA), eur(r.complB), eur(r.compl)],
    ["Total que cobráis", eur(r.totalA), eur(r.totalB), eur(r.total)],
    ["Sueldo bruto de esas semanas", eur(r.dejadoA), eur(r.dejadoB), eur(r.dejadoA + r.dejadoB)],
    ["Pérdida bruta frente al sueldo", eur(r.perdidaA), eur(r.perdidaB), eur(r.perdida)]
  ];
  if (dos) rows.push(["Reparto que menos pierde (mismas semanas totales)", EM.num(r.optA, 0) + " semanas", EM.num(r.optB, 0) + " semanas", eur(r.perdidaOpt) + " de pérdida"]);
  EM.renderResult({
    winner: "esc" + r.esc, verdict: verdict, tone: r.esc === 1 ? "ok" : "info",
    bigNumber: r.total, bigLabel: "en total en " + EM.num(a + b, 0) + " semanas (bruto, exento de IRPF)", format: eur,
    barsLabel: "Prestación total",
    bars: [{ label: "Progenitor A", value: r.totalA, color: "a" }, { label: "Progenitor B", value: r.totalB, color: "b" }],
    cols: ["Progenitor A", "Progenitor B", "Familia"],
    rows: rows,
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
