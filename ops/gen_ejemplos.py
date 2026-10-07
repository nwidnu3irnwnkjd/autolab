#!/usr/bin/env python3
"""Genera projects/decidir/data/ejemplos.json: el «Ejemplo resuelto» de las 9 calculadoras insignia (acción #2 de OPTIMIZACION.md).
Ejecuta la función REAL calcular() de cada calcs/<slug>.js con JavaScriptCore (osascript, como ops/check.py) con entradas
EXPLÍCITAS y fijas (abajo). Los datos vivos que son defaults de la calculadora (tipo medio de las hipotecas fijas, Euríbor) se
fijan aquí con su fecha; así el ejemplo no cambia solo cuando cambia live.json. Para actualizarlo: editar las entradas y volver a lanzar.
El build (projects/decidir/ejemplos.py, también en GitHub Actions) solo LEE el JSON: no necesita osascript.
Uso:  python3 ops/gen_ejemplos.py          escribe data/ejemplos.json
      python3 ops/gen_ejemplos.py --check  recalcula y exige que el JSON vigente coincida (lo llama ops/check.py); sin osascript, se salta
Solo stdlib. Sin red. Sin cifras legales nuevas: solo las entradas por defecto de cada calculadora."""
import datetime, json, math, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "projects", "decidir")
OUT = os.path.join(PDIR, "data", "ejemplos.json")

# ---------- formato es-ES (agrupa miles siempre, como EM.eur de assets/em.js) ----------
def _r(x, d=0):
    q = 10 ** d
    return math.floor(abs(x) * q + 0.5) / q * (1 if x >= 0 else -1)
def num(x, d=0):
    s = f"{abs(_r(x, d)):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if _r(x, d) < 0 else "") + s
def eur(x, d=0): return num(x, d) + " €"
def pct(x, d=2): return num(x, d) + " %"

# ---------- los 9 ejemplos: entradas fijas, filas de la tabla y frase condicionada ----------
def ej_alquilar(i, r):
    comp = r["diferencia"] > 0
    return dict(
        entradas=f"vivienda de {eur(i['precio'])}, entrada del {pct(i['entrada'], 0)}, hipoteca al {pct(i['interes'])} a {i['plazo']} años, alquiler equivalente de {eur(i['alquiler'])} al mes, revalorización del {pct(i['revaloriza'], 0)} anual, rentabilidad de invertir del {pct(i['rentab'], 0)} anual y horizonte de {i['horizonte']} años",
        filas=[("Patrimonio al comprar", eur(r["patrimonioComprar"])), ("Patrimonio al alquilar e invertir", eur(r["patrimonioAlquilar"])),
               ("Diferencia a favor de " + ("comprar" if comp else "alquilar"), eur(abs(r["diferencia"]))),
               ("Cuota de la hipoteca", eur(r["cuotaHipoteca"], 2) + "/mes"), ("Coste mensual de comprar (cuota, IBI, comunidad y mantenimiento)", eur(r["costeMensualCompra"], 2) + "/mes"),
               ("Año en que comprar empieza a ganar", str(r["anosEquilibrio"]))],
        frase=f"Con estos supuestos, a {i['horizonte']} años comprar deja {eur(abs(r['diferencia']))} " + ("más" if comp else "menos") + f" de patrimonio que alquilar e invertir la entrada y empieza a ganar en el año {r['anosEquilibrio']}: si vendes antes, con estos números gana alquilar.")

def ej_amortizar(i, r):
    inv = r["diferencia"] > 0
    return dict(
        entradas=f"hipoteca de {eur(i['capital'])} al {pct(i['tipo'])} a {i['anos']} años, {eur(i['importe'])} disponibles, reduciendo el plazo, rentabilidad de invertir del {pct(i['rentab'], 0)} anual e impuesto sobre ganancias del {pct(i['impuesto'], 0)}",
        filas=[("Patrimonio al amortizar", eur(r["patrimonioAmortizar"])), ("Patrimonio al invertir", eur(r["patrimonioInvertir"])),
               ("Diferencia a favor de " + ("invertir" if inv else "amortizar"), eur(abs(r["diferencia"]))),
               ("Intereses ahorrados al amortizar", eur(r["interesesAhorrados"])), ("Cuota actual", eur(r["cuotaActual"], 2) + "/mes"),
               ("Rentabilidad anual de equilibrio", pct(r["rentabilidadDeEquilibrio"]))],
        frase=f"Con estos supuestos (inversión al {pct(i['rentab'], 0)} anual), invertir deja {eur(abs(r['diferencia']))} " + ("más" if inv else "menos") + f" que amortizar; invertir solo sale mejor si rinde más de un {pct(r['rentabilidadDeEquilibrio'])} anual (antes de impuestos sobre ganancias), y esa rentabilidad no está garantizada: por debajo, amortizar sale mejor.")

def ej_coche(i, r):
    comp = r["diferencia"] > 0
    return dict(
        entradas=f"coche de {eur(i['precio'])} durante {i['anos']} años, valor de reventa del {pct(i['reventa'], 0)}, seguro de {eur(i['seguro'])} al año, mantenimiento de {eur(i['mantenimiento'])} al año, impuesto de {eur(i['impuesto'])} al año, sin financiar, frente a un renting de {eur(i['cuota'])} al mes con todo incluido",
        filas=[("Coste total de comprar", eur(r["costeCompra"])), ("Coste total del renting", eur(r["costeRenting"])),
               ("Diferencia a favor de " + ("comprar" if comp else "el renting"), eur(abs(r["diferencia"]))),
               ("Coste mensual de comprar", eur(r["mesCompra"], 2)), ("Cuota mensual del renting", eur(r["mesRenting"], 2)),
               ("Cuota de renting de equilibrio", eur(r["cuotaEquilibrio"], 2) + "/mes")],
        frase=f"Con estos supuestos, " + ("comprar" if comp else "el renting") + f" sale {eur(abs(r['diferencia']))} más barato en {i['anos']} años; el renting solo compensaría si su cuota, con todo incluido, bajara de {eur(r['cuotaEquilibrio'], 2)} al mes.")

def ej_contado(i, r):
    cont = r["ventajaFinanciar"] < 0
    return dict(
        entradas=f"compra de {eur(i['precio'])} con {eur(i['entrada'])} de entrada, préstamo al {pct(i['tin'], 0)} TIN con {pct(i['comision'], 0)} de comisión a {i['plazo']} meses, sin descuento por pagar al contado, y tu dinero rindiendo un {pct(i['rentab'], 0)} anual con un {pct(i['impuesto'], 0)} de impuestos",
        filas=[("Coste de financiar (intereses y comisión)", eur(r["costeFinanciar"])), ("Rendimiento neto de tu dinero si financias", eur(r["rendimientoNeto"])),
               ("Ventaja de financiar", eur(r["ventajaFinanciar"])), ("Cuota mensual", eur(r["cuota"], 2)), ("TAE real del préstamo", pct(r["tae"])),
               ("Rentabilidad anual de equilibrio", pct(r["rentabilidadDeEquilibrio"]))],
        frase=("Con estos supuestos, pagar al contado ahorra " + eur(abs(r["ventajaFinanciar"])) if cont else f"Con estos supuestos, financiar ahorra {eur(r['ventajaFinanciar'])}") + f"; financiar solo compensaría si tu dinero rindiera más de un {pct(r['rentabilidadDeEquilibrio'])} anual antes de impuestos (la TAE real es del {pct(r['tae'])}) o si te hicieran descuento por pagar al contado.")

def ej_plazos(i, r):
    return dict(
        entradas=f"hipoteca de {eur(i['capital'])} al {pct(i['tin'])} (tipo medio de las nuevas hipotecas fijas, BCE, agosto de 2026), ingresos netos de {eur(i['ingresos'])} al mes, sin otras deudas y tope de esfuerzo del {pct(i['tope'], 0)}",
        filas=[(f"A {y} años: cuota e intereses totales", f"{eur(r['cuota' + str(y)], 2)}/mes · {eur(r['int' + str(y)])}") for y in (20, 25, 30)] +
              [("Cuota máxima con ese tope", eur(r["cuotaMax"], 2) + "/mes"), ("Intereses extra de 30 años frente a 20", eur(r["extra30"]))],
        frase=f"Con estos supuestos, el plazo más corto de los tres que cabe en el {pct(i['tope'], 0)} de tus ingresos es {r['elegido']} años; alargar a 30 años baja la cuota {eur(r['alivio30'], 2)} al mes pero paga {eur(r['extra30'])} más de intereses.")

def ej_bonificada(i, r):
    bon = r["diferencia"] > 0
    return dict(
        entradas=f"hipoteca de {eur(i['capital'])} a {i['plazo']} años al {pct(i['tin'])} con bonificación (tipo medio de las nuevas hipotecas fijas, BCE, agosto de 2026), {num(i['bonif'], 2)} puntos más sin vinculaciones, y vinculaciones de {eur(i['vinc'])} al año, a {i['horizonte']} años",
        filas=[("Coste total de la bonificada (intereses y vinculaciones)", eur(r["costeBon"])), ("Coste total de la de sin vinculaciones", eur(r["costeSin"])),
               ("Diferencia a favor de " + ("la bonificada" if bon else "la de sin vinculaciones"), eur(abs(r["diferencia"]))),
               ("Cuota de la bonificada", eur(r["cuotaBon"], 2) + "/mes"), ("Cuota de la de sin vinculaciones", eur(r["cuotaSin"], 2) + "/mes"),
               ("Bonificación mínima para compensar", num(r["bonifMin"], 2) + " puntos")],
        frase=f"Con estos supuestos, la bonificada ahorra {eur(r['diferencia'])} en {i['horizonte']} años y compensa mientras la rebaja del tipo supere {num(r['bonifMin'], 2)} puntos o las vinculaciones cuesten menos de {eur(r['vincMax'])} al año; por debajo de ese umbral sale más barata la de sin vinculaciones." if bon else f"Con estos supuestos, la de sin vinculaciones sale {eur(abs(r['diferencia']))} más barata en {i['horizonte']} años; la bonificada solo compensaría con una rebaja del tipo de más de {num(r['bonifMin'], 2)} puntos.")

def ej_seguro(i, r):
    return dict(
        entradas=f"coche de {eur(i['valor'])} que se deprecia un {pct(i['deprec'], 0)} al año, prima de {eur(i['primaTR'])} a todo riesgo frente a {eur(i['primaTerceros'])} a terceros, franquicia de {eur(i['franquicia'])}, probabilidad de siniestro del {pct(i['prob'], 0)} al año y reparación media de {eur(i['coste'])}, a {i['anos']} años",
        filas=[("Sobreprima del todo riesgo al año", eur(r["primaExtraAnual"])), (f"Sobreprima acumulada en {i['anos']} años", eur(r["difPrimaAcum"])),
               ("Pérdida esperada que te cubre en ese plazo", eur(r["cubiertoEsperado"])), ("Saldo del todo riesgo (cubierto menos sobreprima)", eur(r["saldoTodoRiesgo"])),
               ("Valor estimado del coche al final", eur(r["valorFinal"]))],
        frase=f"Con estos supuestos, el todo riesgo te cubre {eur(r['cubiertoEsperado'])} esperados a cambio de {eur(r['difPrimaAcum'])} de sobreprima en {i['anos']} años (saldo de {eur(r['saldoTodoRiesgo'])}): " + ("no compensa" if r["saldoTodoRiesgo"] < 0 else "compensa") + "; el resultado cambia si tu probabilidad de siniestro o el coste medio de reparar son mayores.")

def ej_subrogar(i, r):
    return dict(
        entradas=f"hipoteca de {eur(i['capital'])} con {i['anos']} años por delante, al {pct(i['tipoActual'])} actual y al {pct(i['tipoNuevo'])} la nueva (tipo medio de las nuevas hipotecas fijas, BCE, agosto de 2026), comisión del {pct(i['comision'])}, gastos de {eur(i['gastos'])}, vinculaciones de {eur(i['vinculacion'])} al año y horizonte de {i['horizonte']} años",
        filas=[("Cuota actual", eur(r["cuotaActual"], 2) + "/mes"), ("Cuota nueva", eur(r["cuotaNueva"], 2) + "/mes"), ("Ahorro de cuota con vinculaciones", eur(r["ahorroCuota"], 2) + "/mes"),
               ("Coste del cambio (comisión y gastos)", eur(r["costeCambio"])), ("Ahorro neto a " + str(i["horizonte"]) + " años", eur(r["ahorroNetoHorizonte"])),
               ("Meses para recuperar el coste", str(r["mesesEquilibrio"]))],
        frase=f"Con estos supuestos, cambiar de hipoteca recupera su coste en {r['mesesEquilibrio']} meses y ahorra {eur(r['ahorroNetoHorizonte'])} netos a {i['horizonte']} años; compensa si el tipo nuevo queda por debajo del {pct(r['tipoEquilibrio'])} y no vendes ni cancelas antes de esos {r['mesesEquilibrio']} meses.")

def ej_fija_variable(i, r):
    return dict(
        entradas=f"hipoteca de {eur(i['capital'])} a {i['anos']} años, fija al {pct(i['fijo'])} frente a Euríbor + {num(i['dif'], 2)} puntos con el Euríbor en {pct(i['euribor'], 3)} (media de septiembre de 2026, BCE) y sin variación del Euríbor después del primer año",
        filas=[("Cuota de la fija", eur(r["cuotaFija"], 2) + "/mes"), ("Cuota de la variable el primer año", eur(r["cuotaVar1"], 2) + "/mes"),
               ("Intereses totales de la fija", eur(r["intFija"])), ("Intereses totales de la variable", eur(r["intVar"])),
               ("Intereses menos con la " + ("fija" if r["diferencia"] > 0 else "variable"), eur(abs(r["diferencia"]))),
               ("Euríbor medio de equilibrio", pct(r["euriborEquilibrio"]))],
        frase=f"Con estos supuestos, la fija sale más barata en intereses si el Euríbor medio de los {r['anosRestantes']} años siguientes al primero supera el {pct(r['euriborEquilibrio'])}; si se mantiene en {pct(i['euribor'], 3)}, la fija ahorra {eur(abs(r['diferencia']))}, y si queda por debajo del {pct(r['euriborEquilibrio'])}, la variable pagaría menos.")

DATOS_FIJOS = "tipo medio de las nuevas hipotecas fijas 2,76 % (BCE, media de agosto de 2026) y Euríbor 12 meses 3,247 % (BCE, media de septiembre de 2026), tal como estaban en data/live.json el 3-oct-2026; se fijan aquí y no cambian solos"
EJEMPLOS = {
    "alquilar-o-comprar": (ej_alquilar, {"precio": 250000, "entrada": 20, "interes": 3.0, "plazo": 30, "gastos": 10, "ibi": 400, "comunidad": 700, "mant": 1, "revaloriza": 2, "alquiler": 900, "subida": 2, "rentab": 4, "venta": 3, "horizonte": 15}),
    "amortizar-o-invertir": (ej_amortizar, {"capital": 150000, "tipo": 3.0, "anos": 20, "importe": 30000, "aporte": 0, "rentab": 4, "impuesto": 19, "comision": 0, "modo": 1}),
    "comprar-coche-o-renting": (ej_coche, {"precio": 25000, "anos": 4, "reventa": 45, "seguro": 600, "mantenimiento": 500, "impuesto": 80, "tipo": 0, "cuota": 450, "entrada": 0}),
    "contado-o-financiar": (ej_contado, {"precio": 20000, "entrada": 2000, "tin": 7, "comision": 1, "plazo": 48, "seguro": 0, "rentab": 3, "impuesto": 19, "descuento": 0}),
    "hipoteca-20-25-o-30-anos-cuota-vs-intereses": (ej_plazos, {"capital": 150000, "tin": 2.76, "ingresos": 3500, "otras": 0, "tope": 35}),
    "hipoteca-bonificada-o-sin-vinculaciones": (ej_bonificada, {"capital": 150000, "plazo": 25, "tin": 2.76, "bonif": 0.5, "vinc": 300, "aperturaBon": 0, "aperturaSin": 0, "horizonte": 25}),
    "seguro-todo-riesgo-o-terceros": (ej_seguro, {"valor": 18000, "deprec": 12, "primaTerceros": 380, "primaTR": 720, "franquicia": 300, "prob": 10, "coste": 3000, "anos": 5}),
    "subrogar-hipoteca-merece-la-pena": (ej_subrogar, {"capital": 150000, "tipoActual": 3.5, "anos": 20, "tipoNuevo": 2.76, "comision": 0.05, "gastos": 1500, "vinculacion": 300, "horizonte": 10}),
    "hipoteca-fija-o-variable": (ej_fija_variable, {"capital": 150000, "anos": 25, "fijo": 2.8, "dif": 0.8, "euribor": 3.247, "escenario": 0}),
}
VIVOS = {"hipoteca-20-25-o-30-anos-cuota-vs-intereses", "hipoteca-bonificada-o-sin-vinculaciones", "subrogar-hipoteca-merece-la-pena", "hipoteca-fija-o-variable"}

# ---------- «Casos típicos» (tarea 4 de COLA-TRABAJO): 2-3 casos por calculadora NO insignia, misma calcular() real ----------
def ej_paro(i, r):
    tope = f"; el máximo legal ({eur(r['tope'])}/mes con {r['hijos']} hijos a cargo) limita la cuantía" if r["ap1"] else ""
    return (f"Base de {eur(i['base'])} y {num(i['dias'])} días cotizados, {i['hijos']} hijos a cargo",
            f"cobrarías {eur(r['m1'])} al mes los primeros {r['d1']} días y {eur(r['m2'])} al mes los {r['d2']} siguientes: {eur(r['total'])} en {r['dur']} días ({num(r['meses'], 0)} meses){tope}.")
def ej_capitalizar(i, r):
    return (f"{i['meses']} meses por cobrar, base de {eur(i['br'])}, inversión de {eur(i['inversion'])}, cuota de autónomo de {eur(i['cuota'], 2)}/mes",
            f"capitalizando cobrarías {eur(r['pagoUnico'])} de golpe y unos {eur(r['subTotal'])} más como ayuda a la cuota ({eur(r['capTotal'])} en total); cobrando mes a mes con la actividad solo se admiten {r['mesesCob']} meses ({eur(r['totalCob'])}), así que capitalizar da {eur(abs(r['dif']))} " + ("más" if r["dif"] >= 0 else "menos") + " en esas condiciones.")
def ej_finiquito(i, r):
    d = f"; el preaviso incumplido ({i['incumple']} días) resta {eur(r['descAplicado'])}" if r["descuento"] > 0 else ""
    return (f"{eur(i['bruto'])} brutos al año en {i['pagas']} pagas, baja el {i['dia']}/{i['mes']}, {i['vacDisf']} de {i['vacAnual']} días de vacaciones disfrutados, IRPF del {pct(i['tipo'], 0)}",
            f"finiquito bruto de {eur(r['brutoDev'])} (mes {eur(r['salMes'])}, pagas {eur(r['pagasPend'])}, vacaciones {eur(r['vacImporte'])}) y unos {eur(r['neto'])} netos tras {eur(r['cot'])} de cotización y {eur(r['irpf'])} de IRPF estimado{d}.")
def ej_despido(i, r):
    obj = i["tipo"] == "objetivo"
    base = f"{eur(i['bruto'])} brutos al año, {i['anios']} años de antigüedad, despido {'objetivo' if obj else 'improcedente'}"
    if i["oferta"] > 0:
        base += f", oferta de {eur(i['oferta'])}"
        if r["difBruta"] < 0:
            f = f"la legal serían {eur(r['legal'])}: la oferta queda {eur(abs(r['difBruta']))} por debajo y te quedarían {eur(r['neto'])} netos."
        else:
            f = f"la legal (improcedente) serían {eur(r['legal'])} y la oferta la supera en {eur(r['difBruta'])}: te quedarían {eur(r['neto'])} netos tras {eur(r['irpf'])} de IRPF estimado al {pct(i['marginal'], 0)}."
    else:
        f = f"la indemnización legal sería de {eur(r['legal'])} brutos ({eur(r['neto'])} netos); si un juez lo declarase improcedente serían {eur(r['legalImp'])}." if obj else f"la indemnización legal sería de {eur(r['legal'])} brutos ({eur(r['neto'])} netos); si el despido fuera objetivo serían {eur(r['legalObj'])}."
    return (base, f)
def ej_navidad(i, r):
    sit = {"todo": "todo el periodo trabajado", "alta": f"alta el {i['dia']}/{i['mes']}", "baja": f"baja el {i['dia']}/{i['mes']}"}[i["situacion"]]
    return (f"Paga de {eur(i['importe'])}, devengo {i['devengo']}, {sit}, retención del {pct(i['ret'], 0)}",
            f"corresponden {r['dias']} de {r['diasPeriodo']} días: {eur(r['bruta'], 2)} brutos y {eur(r['neto'], 2)} netos tras {eur(r['retencion'], 2)} de retención (si además descuentas la cotización, {eur(r['netoReal'], 2)}).")
def ej_loteria(i, r):
    com = f", repartido entre {i['personas']} personas" if i["personas"] > 1 else ""
    if r["sujeto"] == 0:
        f = f"el premio queda exento ({eur(r['exento'])}) y cobras el 100 %: {eur(r['netoTotal'])}."
    else:
        pp = f" ({eur(r['netoPersona'])} por persona)" if i["personas"] > 1 else ""
        f = f"quedan exentos {eur(r['exento'])}, tributa el exceso de {eur(r['sujeto'])} y la retención es de {eur(r['retencion'])}: cobras {eur(r['netoTotal'])}{pp}."
    return (f"Premio de {eur(i['premio'])} por décimo{com}", f)
def ej_baja(i, r):
    tipo = "accidente de trabajo" if i["cont"] == "prof" else "enfermedad común"
    return (f"{eur(i['sueldo'])} de sueldo mensual ({'14 pagas' if i['pagas'] == '14' else 'pagas prorrateadas'}), {tipo}, {i['dias']} días de baja, sin mejora de convenio",
            f"cobrarías {eur(r['ingreso'])} en esos {i['dias']} días frente a {eur(r['habitual'])} de sueldo habitual, es decir {eur(r['perdida'])} menos; la empresa adelanta {eur(r['empSub'])} y el resto lo paga la entidad gestora.")
def ej_extras(i, r):
    return (f"{eur(i['bruto'])} brutos al año, {i['extras']} pagas extra, retención del {pct(i['ret'], 0)}",
            f"con 14 pagas el mes normal es de {eur(r['mensual14'])} brutos ({eur(r['netoMes14'], 2)} netos) y los meses con paga {eur(r['netoMesPaga14'], 2)} netos; prorrateadas cobrarías {eur(r['mensual12'])} brutos ({eur(r['netoMes12'], 2)} netos) cada mes. Neto anual: {eur(r['netoAnual14'])} frente a {eur(r['netoAnual12'])}" + (", igual en ambos casos." if r["difAnual"] == 0 else "."))
def ej_retencion(i, r):
    a = r["resultado"]
    return (f"{eur(i['bruto'])} brutos al año, un pagador, Comunidad de Madrid, sin hijos, retención del {pct(i['ret'], 0)}",
            f"el IRPF de ese año sería de {eur(r['cuota'])} y te retienen {eur(r['retenido'])}: " + (f"saldrías a pagar {eur(a)} en la renta" if a > 0 else f"te devolverían {eur(-a)}") + f"; la retención que dejaría el resultado en 0 sería del {pct(r['tipo0'])} y la mínima legal estimada del {pct(r['tipoLegal'])}.")
def ej_jubilacion(i, r):
    ant = r["mesesDiff"] < 0
    return (f"{i['edad']} años, {i['cot']} años cotizados, base reguladora de {eur(i['br'])}, jubilación a los {i['eleg_a']} años, cobrando hasta los {i['fin']}",
            f"a la edad ordinaria que te corresponde ({num(r['ordRealM'] / 12, 0)} años) cobrarías {eur(r['pensionOrdinaria'])} al mes y jubilándote {abs(r['mesesDiff'])} meses " + ("antes" if ant else "después") + f" {eur(r['pensionElegida'])} ({'reducción del ' + pct(r['coefPct'], 0) if ant else 'incremento del ' + pct(r['extraPct'], 0)}); hasta los {i['fin']} acumularías {eur(abs(r['diferencia']))} " + ("más" if r["diferencia"] >= 0 else "menos") + f", y la opción de jubilarte más tarde supera en acumulado a la otra solo si cobras más allá de los {num(r['equilibrioEdad'], 1)} años.")

CASOS = {
    "cuanto-cobro-de-paro-prestacion-desempleo": (ej_paro, [
        {"base": 1200, "extras": "si", "hijos": 0, "jornada": 100, "dias": 720},
        {"base": 2500, "extras": "si", "hijos": 0, "jornada": 100, "dias": 1080},
        {"base": 1800, "extras": "si", "hijos": 2, "jornada": 100, "dias": 1440}]),
    "capitalizar-paro-o-cobrarlo": (ej_capitalizar, [
        {"meses": 12, "br": 1500, "hijos": 0, "cobrados": 0, "actividad": "si", "inversion": 6000, "cuota": 205.88, "arranque": 6},
        {"meses": 18, "br": 2000, "hijos": 0, "cobrados": 6, "actividad": "si", "inversion": 15000, "cuota": 205.88, "arranque": 12}]),
    "finiquito-baja-voluntaria-vacaciones-preaviso": (ej_finiquito, [
        {"bruto": 24000, "pagas": 14, "mes": 10, "dia": 15, "vacAnual": 30, "vacDisf": 10, "incumple": 0, "tipo": 12},
        {"bruto": 30000, "pagas": 12, "mes": 6, "dia": 30, "vacAnual": 30, "vacDisf": 5, "incumple": 15, "tipo": 15},
        {"bruto": 18000, "pagas": 14, "mes": 3, "dia": 31, "vacAnual": 30, "vacDisf": 0, "incumple": 0, "tipo": 8}]),
    "indemnizacion-despido-objetivo-o-improcedente-neto": (ej_despido, [
        {"bruto": 24000, "anios": 3, "meses": 0, "antes": 0, "oferta": 0, "marginal": 24, "tipo": "objetivo", "causa": "eco"},
        {"bruto": 30000, "anios": 8, "meses": 0, "antes": 0, "oferta": 10000, "marginal": 30, "tipo": "objetivo", "causa": "eco"},
        {"bruto": 30000, "anios": 8, "meses": 0, "antes": 0, "oferta": 30000, "marginal": 30, "tipo": "improcedente", "causa": "otra"}]),
    "paga-extra-navidad-cuanto-cobro-neto": (ej_navidad, [
        {"importe": 1500, "devengo": "semestral", "situacion": "todo", "mes": 9, "dia": 1, "diassin": 0, "ret": 15, "forma": "14"},
        {"importe": 2000, "devengo": "anual", "situacion": "alta", "mes": 4, "dia": 1, "diassin": 0, "ret": 18, "forma": "14"},
        {"importe": 1800, "devengo": "semestral", "situacion": "baja", "mes": 10, "dia": 31, "diassin": 0, "ret": 12, "forma": "14"}]),
    "loteria-navidad-premio-neto-hacienda": (ej_loteria, [
        {"premio": 400000, "decimos": 1, "personas": 1, "cobro": "uno"},
        {"premio": 40000, "decimos": 1, "personas": 1, "cobro": "uno"},
        {"premio": 400000, "decimos": 1, "personas": 4, "cobro": "cotitulares"}]),
    "baja-medica-cuanto-cobro-incapacidad-temporal": (ej_baja, [
        {"sueldo": 1800, "pagas": "prorr", "cont": "comun", "dias": 30, "mejora": 0, "tipo": 0},
        {"sueldo": 2200, "pagas": "14", "cont": "comun", "dias": 60, "mejora": 0, "tipo": 0},
        {"sueldo": 1800, "pagas": "prorr", "cont": "prof", "dias": 30, "mejora": 0, "tipo": 0}]),
    "pagas-extra-prorrateadas-o-14-pagas": (ej_extras, [
        {"bruto": 24000, "extras": 2, "contrato": "indef", "ret": 15, "situacion": "todo", "mes": 10, "dia": 31},
        {"bruto": 36000, "extras": 2, "contrato": "indef", "ret": 18, "situacion": "todo", "mes": 10, "dia": 31}]),
    "retencion-irpf-nomina-subir-o-no": (ej_retencion, [
        {"bruto": 24000, "ret": 10, "hijos": 0, "menores3": 0, "reparto": "entero", "pagador2": 0, "ccaa": "madrid", "euribor": 3.247},
        {"bruto": 30000, "ret": 12, "hijos": 0, "menores3": 0, "reparto": "entero", "pagador2": 0, "ccaa": "madrid", "euribor": 3.247},
        {"bruto": 45000, "ret": 20, "hijos": 0, "menores3": 0, "reparto": "entero", "pagador2": 0, "ccaa": "madrid", "euribor": 3.247}]),
    "jubilacion-anticipada-o-demorada": (ej_jubilacion, [
        {"edad": 62, "cot": 38, "br": 2000, "eleg_a": 63, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 2.7},
        {"edad": 64, "cot": 38, "br": 2000, "eleg_a": 67, "eleg_m": 0, "fin": 85, "irpf": 0, "ipc": 2.7}]),
}

def generar_casos(fecha):
    out = {}
    for slug, (fn, lista) in CASOS.items():
        cs = []
        for inp in lista:
            r = ejecutar(slug, inp); t, f = fn(inp, r)
            cs.append({"inputs": inp, "resultado": r, "titulo": t, "texto": f})
        out[slug] = {"fecha": fecha, "casos": cs}
    return out

def ejecutar(slug, inputs):
    """calcular() real del .js (funciones puras antes de 'function eur(', igual que ops/check.py)."""
    js = open(os.path.join(PDIR, "calcs", slug + ".js"), encoding="utf-8").read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + f"\nJSON.stringify(calcular({json.dumps(inputs)}));"], capture_output=True, text=True)
    if o.returncode != 0: raise RuntimeError(f"{slug}: error JS: {o.stderr.strip()}")
    r = json.loads(o.stdout.strip())
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if isinstance(v, (int, float, str, bool)) or v is None}

def generar(fecha):
    out = {}
    for slug, (fn, inputs) in EJEMPLOS.items():
        r = ejecutar(slug, inputs); e = fn(inputs, r)
        out[slug] = {"inputs": inputs, "resultado": r, "entradas_texto": e["entradas"], "filas": e["filas"], "veredicto_texto": e["frase"], "fecha": fecha,
                     "datos_fijados": DATOS_FIJOS if slug in VIVOS else ""}
    return out

def main():
    check = "--check" in sys.argv
    if not shutil.which("osascript"):
        print("gen_ejemplos: sin osascript (no es macOS): se salta"); return 0
    if check:
        try: cur = json.load(open(OUT, encoding="utf-8"))
        except Exception: print("✗ ejemplos: falta data/ejemplos.json (python3 ops/gen_ejemplos.py)"); return 1
        malos = 0
        for slug, nuevo in json.loads(json.dumps(generar("x"))).items():
            v = cur.get(slug)
            if not v or any(v.get(k) != nuevo[k] for k in ("inputs", "resultado", "entradas_texto", "filas", "veredicto_texto")):
                print(f"✗ ejemplos: {slug} no coincide con la calculadora (regenera con python3 ops/gen_ejemplos.py)"); malos += 1
        cc = cur.get("_casos", {}); tot = len(EJEMPLOS) + len(CASOS)
        for slug, nuevo in generar_casos("x").items():
            v = cc.get(slug)
            if not v or v["casos"] != nuevo["casos"]:
                print(f"✗ casos típicos: {slug} no coincide con la calculadora (regenera con python3 ops/gen_ejemplos.py)"); malos += 1
        print(f"{'OK' if not malos else 'FALLOS'}: ejemplos y casos típicos {tot - malos}/{tot} coinciden con la calculadora"); return 1 if malos else 0
    hoy = datetime.date.today().isoformat()
    out = generar(hoy); out["_casos"] = generar_casos(hoy)
    try: old = json.load(open(OUT, encoding="utf-8"))
    except Exception: old = {}
    for k, v in out.items():  # conserva la fecha de lo que no ha cambiado
        o = old.get(k)
        if k == "_casos":
            for sl, vv in v.items():
                oo = (o or {}).get(sl)
                if oo and oo["casos"] == vv["casos"]: vv["fecha"] = oo["fecha"]
        elif o and all(o.get(x) == v[x] for x in ("inputs", "resultado", "entradas_texto", "filas", "veredicto_texto")): v["fecha"] = o["fecha"]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(OUT, "a").write("\n")
    for s, v in out.items():
        if s != "_casos": print(f"{s}: {v['veredicto_texto']}")
    for s, v in out["_casos"].items():
        for c in v["casos"]: print(f"[casos] {s}: {c['titulo']}: {c['texto']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
