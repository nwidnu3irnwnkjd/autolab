// Formacion para cambiar de trabajo (curso online, bootcamp o FP): coste total, meses para recuperarlo y valor a N años.
// Coste = matricula x (1 - beca %) + sueldo mensual x % que dejas de cobrar x meses de formacion.
// Beneficio = subida neta mensual x meses cobrando la subida (horizonte - formacion - busqueda). Sin descuento ni impuestos.
function calcular(d) {
  var coste = d.matricula * (1 - d.beca / 100) + d.sueldo * (d.renuncia / 100) * d.meses;
  var mesesGana = Math.max(12 * d.anios - d.meses - d.busqueda, 0);
  var valor = d.subida * mesesGana - coste, tol = 0.05 * coste;
  return {
    costeMatricula: d.matricula * (1 - d.beca / 100), costeTiempo: d.sueldo * (d.renuncia / 100) * d.meses, costeTotal: coste,
    mesesRecuperar: d.subida > 0 ? coste / d.subida : -1,
    mesesDesdeInicio: d.subida > 0 ? d.meses + d.busqueda + coste / d.subida : -1,
    mesesGana: mesesGana, valor: valor,
    subidaMin: mesesGana > 0 ? coste / mesesGana : -1,
    ganador: Math.abs(valor) <= tol ? 2 : (valor > 0 ? 0 : 1)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["matricula", "beca", "meses", "sueldo", "renuncia", "busqueda", "subida", "anios"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function mes(m) { return m < 0 ? "no se recupera" : EM.num(m, 1) + " meses"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.meses < 1 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe al menos 1 mes de duración y 1 año de horizonte.", tone: "warn", note: "<p>Sin duración u horizonte no hay nada que calcular.</p>" });
    return;
  }
  if (d.meses > 60 || d.anios > 30 || d.beca > 100 || d.renuncia > 100 || d.busqueda > 36) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: hasta 60 meses de formación, 30 años de horizonte, 36 meses de búsqueda, y becas y renuncia de sueldo de como máximo 100 %.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, N = d.anios, anos = EM.num(N, 0) + (N === 1 ? " año" : " años"), w, verdict;
  var umbral = r.subidaMin >= 0 ? " La formación compensa en " + anos + " solo si la subida neta supera " + eur(r.subidaMin) + " al mes (tú supones " + eur(d.subida) + ")." : " Con ese horizonte, la formación y la búsqueda ocupan todo el plazo: no da tiempo a cobrar la subida.";
  if (g === 2) {
    w = "empate";
    verdict = "Con estos datos hay empate práctico: a " + anos + " la formación recupera casi justo lo que cuesta (" + eur(r.costeTotal) + ")." + umbral;
  } else if (g === 0) {
    w = "compensa";
    verdict = "Con estos datos, la formación compensa: a " + anos + " te deja " + eur(r.valor) + " más de lo que cuesta (" + eur(r.costeTotal) + "), y lo recuperas " + (r.mesesRecuperar >= 0 ? "en " + EM.num(r.mesesRecuperar, 1) + " meses desde que empiezas a cobrar la subida" : "sin necesidad de subida, porque no tiene coste") + "." + umbral + " La subida es una hipótesis tuya, no una promesa.";
  } else {
    w = "no compensa";
    verdict = "Con estos datos, la formación no compensa en " + anos + ": cuesta " + eur(r.costeTotal) + " y te deja " + eur(r.valor) + " frente a no hacerla. " + (r.mesesRecuperar >= 0 ? "Recuperarías la inversión a los " + EM.num(r.mesesRecuperar, 1) + " meses de cobrar la subida, más allá del horizonte." : "Con una subida de 0 € no se recupera.") + umbral;
  }
  var note = "<p><strong>Lectura:</strong> el coste son " + eur(r.costeMatricula) + " de matrícula (tras la beca o gratuidad que indiques) y " + eur(r.costeTiempo) + " de sueldo que dejas de cobrar durante " + EM.num(d.meses, 0) + " meses. ";
  note += "Empiezas a cobrar la subida tras " + EM.num(d.meses + d.busqueda, 0) + " meses (formación más búsqueda) y la cobras durante " + EM.num(r.mesesGana, 0) + " meses del horizonte. ";
  note += r.mesesRecuperar >= 0 ? "Contando desde el inicio de la formación, la inversión se recupera a los " + EM.num(r.mesesDesdeInicio, 1) + " meses.</p>" : "Sin subida no hay recuperación.</p>";
  note += "<p><strong>Límites:</strong> la subida de sueldo y los meses de búsqueda son hipótesis tuyas: esta página no promete empleo ni cifra salarios del mercado. Las becas y la gratuidad de la FP dependen de tu comunidad y de tu situación: consulta tu comunidad e indica el porcentaje que te cubran. No incluye impuestos (usa la subida neta), descuento del dinero en el tiempo, material, desplazamientos, ni que la formación pueda cambiar tu trayectoria más allá del horizonte. Para comparar curso online, bootcamp y FP, calcula cada uno por separado con sus datos.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 0 ? "ok" : "warn",
    bigNumber: r.valor, bigLabel: "€ de valor neto a " + anos + " (beneficio de la subida menos el coste)", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste frente a beneficio de la subida a " + anos,
    bars: [{ label: "Coste total", value: Math.max(r.costeTotal, 0), color: "a" }, { label: "Beneficio de la subida", value: Math.max(d.subida * r.mesesGana, 0), color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Matrícula tras becas", eur(r.costeMatricula)],
      ["Sueldo que dejas de cobrar", eur(r.costeTiempo)],
      ["Coste total", eur(r.costeTotal)],
      ["Meses para recuperarlo desde que cobras la subida", mes(r.mesesRecuperar)],
      ["Subida neta mínima al mes para compensar a " + anos, r.subidaMin >= 0 ? eur(r.subidaMin) : "no da tiempo"],
      { label: "Valor neto a " + anos, values: [eur(r.valor)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
