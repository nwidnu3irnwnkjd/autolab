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
        frase=f"Con estos supuestos, si el Euríbor se queda, de forma estable, por encima del {pct(r['euriborEquilibrio'])} durante los {num(r['anosRestantes'], 0) if r['anosRestantes'] == int(r['anosRestantes']) else num(r['anosRestantes'], 1)} años siguientes al primero, la fija sale más barata en intereses; si se mantiene en {pct(i['euribor'], 3)}, la fija ahorra {eur(abs(r['diferencia']))}, y si queda estable por debajo, la variable pagaría menos. Si el Euríbor sube o baja con el tiempo el resultado cambia y los primeros años pesan más: con el Euríbor subiendo del 1 % al 2,95 % la variable ahorraría 7.200 € y bajando del 2,95 % al 1 % costaría 12.372 € más (ambas sendas con la misma media, 1,975 %, por encima del umbral; cifras comprobadas con ops/verif/hipoteca-fija-o-variable.py).")

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
    "hipoteca-fija-o-variable": (ej_fija_variable, {"capital": 150000, "anos": 25, "fijo": 2.76, "dif": 0.8, "euribor": 3.247, "escenario": 0}),
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

def hj(n):
    n = int(n); return f"{n} hijo" + ("" if n == 1 else "s")
def ej_autonomo(i, r):
    return (f"{eur(i['bruto'])} brutos como asalariado frente a {eur(i['factura'])} facturados sin IVA y {eur(i['gastos'])} de gastos como autónomo, Madrid, {hj(i['hijos'])}",
            f"como asalariado quedarían {eur(r['netoAsalariado'])} netos al año y como autónomo {eur(r['netoAutonomo'])} (cuota de autónomos de {eur(r['cuotaReta'])}); para igualar el neto de asalariado tendrías que facturar unos {eur(r['facturaIgual'])}.")
def ej_ofertas(i, r):
    return (f"oferta A de {eur(i['brutoA'])} brutos y B de {eur(i['brutoB'])}, {i['pagas']} pagas, Madrid, desplazamiento de {eur(i['desplA'])} al año en A y {eur(i['desplB'])} en B",
            f"neto al año {eur(r['netoA'])} (A) y {eur(r['netoB'])} (B); descontado el desplazamiento, {eur(r['netoTrasA'])} frente a {eur(r['netoTrasB'])}: " + ("gana B" if r["dif"] > 0 else "gana A") + f" por {eur(abs(r['dif']))} al año.")
def ej_casa(i, r):
    tipo = "nueva" if i["tipo"] == "nueva" else "usada"
    return (f"vivienda {tipo} de {eur(i['precio'])} en {r['ccaaNombre']}, entrada del {pct(i['entrada'], 0)}, {eur(i['gastos'])} de otros gastos, {i['anos']} años para ahorrar, hipoteca al {pct(i['interes'], 1)}",
            f"necesitarías {eur(r['totalNecesario'])} ahorrados ({eur(r['entrada'])} de entrada, {eur(r['impuestos'])} de impuestos y otros gastos), unos {eur(r['ahorroMensual'])} al mes; cuota de {eur(r['cuotaHipoteca'], 2)}/mes.")
def ej_subsidio(i, r):
    s = "paro agotado" if i["situ"] == "agotado" else "cotización insuficiente para el paro"
    return (f"{s}, {i['dias']} días cotizados, {i['edad']} años, {hj(i['hijos'])} a cargo, sin rentas propias",
            f"el subsidio sería de {eur(r['m1'])} al mes los primeros {r['dias1']} días" + (f", {eur(r['m2'])} los {r['dias2']} siguientes y {eur(r['m3'])} el resto" if r["dias2"] else "") + f": {eur(r['total'])} en {r['meses']} meses.")
def ej_permiso(i, r):
    if i["mono"] == "si":
        return (f"familia monoparental con sueldo de {eur(i['sueldoA'])}/mes, permiso de {r['maxA']} semanas",
                f"la prestación sería de {eur(r['prestA'])} en total ({eur(r['semanalA'], 2)} por semana).")
    return (f"dos progenitores con sueldos de {eur(i['sueldoA'])} y {eur(i['sueldoB'])} al mes, 19 semanas cada uno",
            f"la prestación sería de {eur(r['prestA'])} y {eur(r['prestB'])}: {eur(r['prest'])} entre los dos.")
def ej_hogar(i, r):
    m = {"horas": f"{num(i['horas'])} h al mes a {eur(i['importe'], 2)}/h", "mensual": f"{eur(i['importe'])} al mes en {'14' if i['pagas'] == '14' else '12'} pagas", "interna": f"interna con {eur(i['importe'])} al mes"}[i["modo"]]
    return (f"empleada de hogar, {m}, contrato {'indefinido' if i['tipo'] == 'indef' else 'temporal'}",
            f"la cuota de la familia empleadora sería de {eur(r['cuotaEmp'], 2)}/mes (la de la trabajadora, {eur(r['cuotaTrab'], 2)}); coste total de {eur(r['costeMes'], 2)}/mes, {eur(r['costeTotal'])} en {r['meses']} meses.")
def ej_plan(i, r):
    return (f"{eur(i['aportacion'])} al año durante {i['anos']} años, renta de {eur(i['renta'])}, Madrid, rentabilidad del {pct(i['rentab'], 0)}, comisiones del {pct(i['comPlan'], 1)} y {pct(i['comFondo'], 1)}, rescate en un solo pago",
            f"el plan ahorra {eur(r['ahorroFiscalAnual'])} al año de IRPF (límite de aportación {eur(r['limite'])}) y deja {eur(r['patrimonioPlan'])} netos frente a {eur(r['patrimonioFondo'])} del fondo: " + ("gana el fondo" if r["diferencia"] < 0 else "gana el plan") + f" por {eur(abs(r['diferencia']))}.")
def ej_donativos(i, r):
    return (f"donativo de {eur(i['donado'])}" + (" recurrente" if i["recurrente"] == "1" else "") + f", base liquidable de {eur(i['bl'])}, comunidad de régimen común",
            f"deducirías {eur(r['deduccion'])} en la renta y te costaría {eur(r['costeNeto'])} netos ({pct(r['pctEfectivo'], 0)} de desgravación efectiva).")
def ej_obligado(i, r):
    pg = f"{eur(i['t1'])} del primer pagador y {eur(i['t2'])} del segundo"
    if r["estado"] == 1:
        return (pg, f"sumas {eur(r['totalTrabajo'])} y, al superar el segundo pagador los 1.500 €, el límite baja a {eur(r['limite'])}: lo superas en {eur(r['exceso'])} y estarías obligado a declarar.")
    return (pg, f"sumas {eur(r['totalTrabajo'])}, por debajo del límite de {eur(r['limiteTrabajo'])} (margen de {eur(r['margen'])}): por este supuesto no estarías obligado a declarar.")
def ej_maternidad(i, r):
    p = f"{i['n3']} hijos menores de 3 años" if i["n3"] != "1" else "1 hijo menor de 3 años"
    f = "" if i["fam"] == "no" else f", familia numerosa general con {i['hijosFam']} hijos"
    g = f", {eur(i['guarGasto'])} de guardería en {i['guarMeses']} meses" if i["guarGasto"] else ""
    return (f"{p}, {i['mesesMat']} meses con derecho{f}{g}",
            f"la deducción anual sería de {eur(r['deduccion'])} (maternidad {eur(r['mat'])}, guardería {eur(r['guar'])}, familia numerosa {eur(r['fam'])}); cobrándola por adelantado, {eur(r['anticipoMes'])} al mes.")

CCAA_N = {"madrid": "Madrid", "cataluna": "Cataluña", "galicia": "Galicia"}
def ej_sueldo(i, r):
    pg = "14 pagas" if int(i["pagas"]) == 14 else "12 pagas"
    h = f", {hj(i['hijos'])}" if i["hijos"] else ""
    return (f"{eur(i['bruto'])} brutos al año, {pg}, {CCAA_N.get(i['ccaa'], i['ccaa'])}, contrato indefinido{h}",
            f"cobrarías {eur(r['neto'])} netos al año tras {eur(r['ss'])} de Seguridad Social y {eur(r['ret'])} de retención de IRPF (tipo del {pct(r['tipo'], 1)}): {eur(r['netoMes12'], 2)} al mes si te prorratean las pagas" + (f", o {eur(r['netoMesNormal14'], 2)} los meses normales y {eur(r['netoMesExtra14'], 2)} los de paga extra." if int(i["pagas"]) == 14 else "."))
def ej_luz(i, r):
    g = "la tarifa fija" if r["diferencia"] < 0 else "el PVPC"
    return (f"{num(i['consumo'])} kWh al año, {num(i['potencia'], 2)} kW de potencia, {i['pctPunta']} % del consumo en punta y {i['pctLlano']} % en llano, tarifa fija a {num(i['precioFijo'], 3)} €/kWh frente a PVPC a {num(i['pvpc'], 3)} €/kWh",
            f"la tarifa fija costaría {eur(r['costeFija'])} al año y el PVPC {eur(r['costePvpc'])}: con estos supuestos sale mejor {g} por {eur(abs(r['diferencia']))} al año.")
def ej_placas(i, r):
    sub = f", {eur(i['subv'])} de subvención" if i["subv"] else ""
    return (f"instalación de {num(i['potencia'])} kW por {eur(i['coste'])}{sub}, consumo de {num(i['consumo'])} kWh al año, {i['pctAuto']} % de autoconsumo, {num(i['prod'])} kWh producidos por kW, energía a {num(i['precio'], 3)} €/kWh y excedentes a {num(i['comp'], 3)} €/kWh",
            f"ahorrarías unos {eur(r['ahorro1'])} el primer año en factura y cobrarías {eur(r['comp1'])} por excedentes; la inversión de {eur(r['neto'])} se recuperaría en {num(r['anosAmort'], 1)} años y el ahorro neto acumulado en la vida de la instalación sería de {eur(r['ahorroNeto'])}.")
def ej_salud(i, r):
    emp = f", con {eur(i['empresa'])} al mes pagados por la empresa" if i["empresa"] else ""
    sin = r["sinSeguro"] < r["conSeguro"]
    return (f"prima de {eur(i['prima'])} al año{emp}, {i['actos']} consultas o pruebas al año a {eur(i['coste'])} cada una en privado, copago de {eur(i['copago'])}, a {i['horizonte']} años",
            f"con seguro gastarías {eur(r['conSeguro'])} y pagando cada acto sin seguro {eur(r['sinSeguro'])}: " + ("sale más barato no tener seguro" if sin else "sale más barato el seguro") + f" por {eur(abs(r['diferencia']))}; el seguro compensaría con unos {num(r['actosEq'], 1)} actos al año.")
def ej_coche_ns(i, r):
    nuevo = r["tcoNuevo"] < r["tcoSemi"]
    fin = f", financiado al {pct(i['tin'], 1)}" if i["tin"] else ""
    return (f"coche nuevo de {eur(i['pnuevo'])} o seminuevo de {eur(i['psemi'])} con {i['edad']} años, {i['anos']} años de uso{fin}",
            f"el coste real del nuevo sería {eur(r['tcoNuevo'])} y el del seminuevo {eur(r['tcoSemi'])}: sale más barato el {'nuevo' if nuevo else 'seminuevo'} por {eur(abs(r['diferencia']))}" + (f"; el nuevo solo compensaría si costara {eur(r['precioEquilibrio'])} o menos." if not nuevo else "."))
def ej_tren(i, r):
    m = {0: "el coche", 1: "el tren", 2: "el avión"}[r["barato"]]
    return (f"{num(i['dist'])} km, {i['viaj']} " + ("viajero" if i["viaj"] == 1 else "viajeros") + f", tren a {eur(i['tren'])} y avión a {eur(i['avion'])} por persona y trayecto, {num(i['htren'], 1)} h en tren y {num(i['havion'], 1)} h en avión, coche a {num(i['kmcoche'], 2)} €/km",
            f"el coste del trayecto es de {eur(r['costeCoche'])} en coche, {eur(r['costeTren'])} en tren y {eur(r['costeAvion'])} en avión (en total para el grupo): lo más barato es {m}; en coche tardarías {num(r['tiempoCoche'], 1)} h.")
def ej_tele(i, r):
    v = f", valorando tu hora a {eur(i['valorHora'])}" if i["valorHora"] else ""
    return (f"{i['dias']} días de teletrabajo a la semana, {eur(i['desp'])} de desplazamiento y {i['min']} minutos de trayecto al día, comida de {eur(i['comida'])} fuera, {eur(i['casa'])} de gasto extra en casa por día, {eur(i['comp'])} de compensación al mes y {eur(i['equip'])} de equipamiento{v}",
            f"el balance anual es de {eur(r['netoAnual'])} ({eur(r['ahorroDesplazamiento'])} de desplazamiento y {eur(r['ahorroComida'])} de comida ahorrados, {eur(r['costeCasa'])} de gasto en casa y {eur(r['equipamientoAnual'])} de equipamiento) y ganarías {num(r['horasAhorradas'])} horas al año de trayecto.")
def ej_cocinar(i, r):
    v = f", valorando tu hora a {eur(i['vh'])}" if i["vh"] else ""
    return (f"{i['fuera']} " + ("comida" if i["fuera"] == 1 else "comidas") + f" fuera a la semana a {eur(i['precio'])}, cocinando en casa por {eur(i['racion'])} la ración, {i['minCook']} minutos de cocina y {i['minDesp']} de desplazamiento, {i['dias']} días al año{v}",
            f"comer fuera te cuesta {eur(r['gastoFuera'])} al año y cocinar las mismas comidas en casa {eur(r['gastoCasaMismas'])}: ahorras {eur(r['ahorroDinero'])} al año a cambio de {num(r['horasExtra'])} horas más de cocina" + (f"; con tu hora a {eur(i['vh'])}, " + ("sigue ganando cocinar." if r["ganador"] == 0 else "ya compensa más comer fuera.") if i["vh"] else f", y cocinar deja de compensar si tu hora vale más de {eur(r['vhEq'])}."))
def ej_fondo(i, r):
    return (f"gastos esenciales de {eur(i['gastos'])} al mes, {eur(i['ahorro'])} ahorrados y {eur(i['aport'])} al mes de aportación" + (", perfil de mayor riesgo (empleo e ingresos)" if i["empleo"] or i["ingresos"] else ""),
            f"te convendría un fondo de {num(r['meses'], 1)} meses de gastos, es decir {eur(r['objetivo'])}: " + (f"te faltan {eur(r['falta'])} y lo alcanzarías en {r['mesesAlcanzar']} meses." if r["falta"] > 0 else "ya lo tienes cubierto."))
def ej_reformar(i, r):
    ref = r["diferencia"] > 0
    return (f"reforma de {eur(i['reforma'])} que recuperas un {pct(i['recup'], 0)} al vender, vivienda de {eur(i['valor'])}, gastos de mudanza y compraventa del {pct(i['gastosPct'], 0)} y {eur(i['extras'])} extra, a {i['anios']} " + ("año" if i["anios"] == 1 else "años"),
            f"reformar costaría {eur(r['costeReformar'])} y mudarse {eur(r['costeMudarse'])}: sale más barato " + ("reformar" if ref else "mudarse") + f" por {eur(abs(r['diferencia']))}.")

# ---------- Casos típicos, tanda 3: las entradas salen de calcs/<slug>.test.json (mismos casos que verifica ops/check.py) ----------
def T(slug, *idx):
    t = json.load(open(os.path.join(PDIR, "calcs", slug + ".test.json"), encoding="utf-8"))["cases"]
    return [t[k]["in"] for k in idx]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fm(t): return f"{MESES[int(t) % 12]} de {int(t) // 12}"
def ej_viudedad(i, r):
    ing = f", otros ingresos de {eur(i['ingresos'])} al año" if i["ingresos"] else ""
    h = f", {hj(i['hijos'])} a cargo" if i["hijos"] else ""
    return (f"pensión del fallecido con base reguladora de {eur(i['br'])}, viudo o viuda de {i['edad']} años{h}{ing}",
            f"la pensión sería del {pct(r['pct'], 0)} de la base reguladora: {eur(r['mes'], 2)} al mes ({eur(r['anual'])} al año en 14 pagas)" + (f"; queda {eur(r['falta'], 2)} por debajo de la pensión mínima de referencia ({eur(r['minimo'], 2)}/mes)." if r["falta"] > 0 else "."))
def ej_motor(i, r):
    n = ["diésel", "gasolina", "híbrido", "eléctrico"]
    cs = [("diésel", r["costeDiesel"]), ("gasolina", r["costeGasolina"]), ("híbrido", r["costeHibrido"]), ("eléctrico", r["costeElectrico"])]
    return (f"{num(i['km'])} km al año durante {i['anos']} años, {i['pctCasa']} % de la recarga en casa",
            "coste total de " + ", ".join(f"{eur(v)} ({k})" for k, v in cs) + f": sale más barato " + ("la" if r["ganador"] == 1 else "el") + f" {n[r['ganador']]} ({num(r['costeKmX'], 2)} €/km, {eur(r['mesDiesel' if r['ganador'] == 0 else 'mesGasolina' if r['ganador'] == 1 else 'mesHibrido' if r['ganador'] == 2 else 'mesElectrico'])} al mes) por {eur(r['diferencia'])} sobre el siguiente.")
def ej_potencia(i, r):
    pic = f"; tu pico de consumo ({num(i['pico'], 2)} kW) supera la potencia nueva y habría cortes, así que no compensa" if i["pico"] > i["kwNuevo"] else ""
    cam = f", con {eur(i['costeCambio'])} de coste del cambio" if i["costeCambio"] else ""
    rec = f"; se recuperaría en {num(r['aniosAmort'], 1)} años" if r["aniosAmort"] > 0 else ""
    return (f"bajar de {num(i['kwActual'], 2)} a {num(i['kwNuevo'], 2)} kW con un pico de {num(i['pico'], 2)} kW{cam}, a {i['anos']} años",
            f"la parte de potencia pasaría de {eur(r['costeActual'], 2)} a {eur(r['costeNuevo'], 2)} al año: {eur(r['ahorroAnual'], 2)} menos al año; " + (f"en {i['anos']} años ahorrarías {eur(r['ahorroNeto'], 2)} netos" if r["ahorroNeto"] >= 0 else f"en {i['anos']} años el cambio te costaría {eur(-r['ahorroNeto'], 2)} más de lo que ahorras") + f"{rec}{pic}.")
def ej_jub2627(i, r):
    return (f"nacido en {MESES[i['nac_m'] - 1]} de {i['nac_a']}, {i['cot_a']} años y {i['cot_m']} meses cotizados, base reguladora de {eur(r['a26_br'], 2)}",
            f"jubilándote en {fm(r['a26_t'])} cobrarías {eur(r['a26_pension'], 2)} al mes ({pct(r['a26_pct'], 2)} de la base) y en {fm(r['a27_t'])} {eur(r['a27_pension'], 2)} ({pct(r['a27_pct'], 2)}); la de 2026 revalorizada en enero de 2027 sería de {eur(r['a26_pension_ene27'], 2)}: " + ("esperar a 2027 no sube la pensión." if r["dif"] <= 0 else "esperar a 2027 la sube."))
def ej_guarderia(i, r):
    return (f"guardería de {eur(i['guarderia'])}/mes" + (f" con {eur(i['ayuda'])} de ayuda" if i["ayuda"] else "") + f", cuidadora de {eur(i['cuidadora'])}/mes o reducir jornada un {i['reduccion']} % con {eur(i['salario'])} de salario, durante {i['meses']} meses",
            f"coste de {eur(r['totalGuarderia'])} la guardería, {eur(r['totalCuidadora'])} la cuidadora y {eur(r['totalReducir'])} reducir jornada ({eur(r['costeMesGuarderia'], 2)}, {eur(r['costeMesCuidadora'], 2)} y {eur(r['costeMesReducir'], 2)} al mes): sale más barata {'la ' if r['ganador'] != 'reducir jornada' else ''}{r['ganador']} por {eur(r['ahorroVsSiguiente'])} sobre la siguiente.")
def ej_conjunta(i, r):
    h = i["hijosMenores"] + i["hijosMayores"]
    sit = "matrimonio" if i["tipo"] == "mat" else "familia monoparental"
    seg = f" y {eur(i['b2'])}" if i["b2"] else ""
    return (f"{sit} con rendimientos de {eur(i['b1'])}{seg}, {hj(h)}, {r['ccaaNombre']}",
            f"la cuota sería de {eur(r['cuotaIndividual'])} en individual y {eur(r['cuotaConjunta'])} en conjunta: " + ("conviene la conjunta" if r["ganador"] == "conjunta" else "conviene la individual" if r["ganador"] == "individual" else "da igual") + (f" por {eur(abs(r['diferencia']))}." if r["ganador"] != "empate" else " (no hay cuota en ninguna)."))
def ej_nomina27(i, r):
    return (f"{eur(i['bruto'])} brutos al año, contrato {i['contrato']}",
            f"la cotización del trabajador pasaría de {eur(r['mes26'], 2)} a {eur(r['mes27'], 2)} al mes ({eur(r['anual26'], 2)} a {eur(r['anual27'], 2)} al año): {eur(r['sube'], 2)} más al año, de los que {eur(r['dMei'], 2)} son del MEI" + (f" y {eur(r['dSol'], 2)} de la cuota de solidaridad." if r["dSol"] > 0 else "; sin cuota de solidaridad por estar por debajo de la base máxima."))
def ej_bebe(i, r):
    ay = f", con {eur(i['ayudas'])} de ayudas" if i["ayudas"] else ""
    return (f"equipamiento de {eur(i['equip'])}, pañales y alimentación de {eur(i['panalim'])}/mes, ropa de {eur(i['ropa'])} y {eur(i['cuidado'])}/mes de cuidado durante {i['mesesC']} meses{ay}",
            f"el primer año costaría {eur(r['bruto'])} (" + (f"{eur(r['total'])} tras ayudas, " if i["ayudas"] else "") + f"unos {eur(r['mensualMedio'], 2)} al mes); lo recomendable sería ahorrar {eur(r['ahorroPrevio'], 2)} antes del nacimiento.")
def ej_venta(i, r):
    sit = {"hab": "vivienda habitual", "hab65": "vivienda habitual de mayor de 65 años", "nohab": "vivienda no habitual"}[i["sit"]]
    reinv = f", reinvirtiendo {eur(i['reinv'])}" if i["reinv"] else ""
    return (f"{sit} vendida por {eur(i['venta'])}, comprada por {eur(i['adq'])}, {eur(i['hipoteca'])} de hipoteca pendiente{reinv}",
            f"la ganancia patrimonial es de {eur(r['ganancia'])}" + (f"; exenta por reinversión {eur(r['exenta'])}, tributa {eur(r['base'])} con una cuota de {eur(r['cuota'])} y te quedan {eur(r['neto'])} netos tras cancelar la hipoteca." if r["cuota"] > 0 and r["exenta"] > 0 else f"; queda totalmente exenta y te quedan {eur(r['neto'])} netos tras cancelar la hipoteca (sin la exención serían {eur(r['cuotaSin'])} de IRPF)." if r["exenta"] >= r["ganancia"] and r["ganancia"] > 0 else f"; sin exención la cuota es de {eur(r['cuota'])} y te quedan {eur(r['neto'])} netos tras cancelar la hipoteca."))
def ej_cuota_aut(i, r):
    if r["escenario"] == 1:
        f = f"pagaste {eur(r['pagado'], 2)} de cuota provisional y la definitiva sería de {eur(r['definitiva'], 2)}: tendrías que pagar {eur(r['regul'], 2)} más al regularizar."
    elif r["escenario"] == 2:
        f = f"pagaste {eur(r['pagado'], 2)} y la definitiva sería de {eur(r['definitiva'], 2)}: te devolverían {eur(-r['regul'], 2)} al regularizar."
    else:
        f = f"pagas {eur(r['pagado'], 2)} y la definitiva es la misma: no hay regularización."
    return (f"rendimiento previsto de {eur(i['prev'], 2)}/mes, real de {eur(i['real'], 2)}/mes y base elegida de {eur(i['base'], 2)}/mes durante {i['meses']} meses", f)

# ---------- Casos típicos, tanda 4 (hogar, ahorro, coche, trabajo) ----------
def ej_amortizar(i, r):
    c = f", con {pct(i['comision'], 1)} de comisión" if i["comision"] else ""
    return (f"hipoteca de {eur(i['capital'])} al {pct(i['tipo'], 1)} a {i['meses'] // 12} años y {eur(i['extra'])} de amortización anticipada{c}",
            f"reduciendo la cuota bajaría de {eur(r['cuota0'], 2)} a {eur(r['cuotaA'], 2)} al mes y ahorrarías {eur(r['ahorroA'])} en intereses; reduciendo el plazo mantienes {eur(r['cuotaB'], 2)}, terminas {r['mesesMenos']} meses antes y ahorras {eur(r['ahorroB'])}: " + ("reducir plazo ahorra más intereses." if r["ahorroB"] > r["ahorroA"] else "reducir cuota ahorra más intereses."))
def ej_gimnasio(i, r):
    w = {0: "el gimnasio", 1: "entrenar en casa"}.get(r["ganador"])
    return (f"gimnasio de {eur(i['cuota'])} al mes con {eur(i['matricula'])} de matrícula y {eur(i['desp'], 2)} de desplazamiento por sesión, {i['sg']} sesiones a la semana en el gimnasio o {i['sc']} en casa, equipo de {eur(i['equipo'])} que revenderías por {eur(i['reventa'])}, a {i['meses']} meses",
            f"el gimnasio costaría {eur(r['costeGim'])} ({eur(r['cpsGim'], 2)} por sesión) y entrenar en casa {eur(r['costeCasa'])} ({eur(r['cpsCasa'], 2)} por sesión)" + (f": sale más barato por sesión {w}." if w else "."))
def ej_coche_propio(i, r):
    n = ["el coche propio", "el carsharing", "el taxi/VTC"][r["barato"]]
    return (f"{i['viajes']} viajes al mes de {i['kmviaje']} km, {eur(i['fijos'])} de gastos fijos y {eur(i['deprec'])} de depreciación anuales del coche, {eur(i['kmcoche'], 2)}/km de coste variable, carsharing a {eur(i['cskm'], 2)}/km con {eur(i['cscuota'])} de cuota mensual y taxi/VTC a {eur(i['vtckm'], 2)}/km",
            f"para {num(r['km'])} km al año, el coche propio costaría {eur(r['propio'])}, el carsharing {eur(r['carsharing'])} y el taxi/VTC {eur(r['vtc'])}: lo más barato es {n}.")
def ej_caldera(i, r):
    w = {0: "reparar", 1: "cambiar la caldera"}.get(r["ganador"], "cualquiera de las dos")
    return (f"reparación de {eur(i['repar'])} o caldera nueva de {eur(i['nueva'])}, {num(i['consumo'])} kWh de gas al año, rendimientos del {pct(i['rendAct'] * 100, 0)} y el {pct(i['rendNueva'] * 100, 0)}, {i['vida']} años de vida útil",
            f"reparar costaría {eur(r['anualReparar'])} al año y cambiar {eur(r['anualCambiar'])}: sale más barato {w}" + (f" por {eur(abs(r['diferencia']))} al año; cambiar compensaría desde unos {eur(r['equilibrio'])} de reparación." if r["ganador"] == 1 else f" por {eur(abs(r['diferencia']))} al año." if r["ganador"] == 0 else "."))
def ej_secadora(i, r):
    v = f", valorando tu hora a {eur(i['valorHora'])}" if i["valorHora"] else ", sin valorar tu tiempo"
    return (f"{i['coladas']} coladas a la semana durante {i['semanas']} semanas, secadora de {eur(i['compra'])} que dura {i['vida']} años y gasta {num(i['kwh'], 1)} kWh por ciclo a {eur(i['precio'], 2)}/kWh, {i['minutos']} minutos de tendido por colada{v}",
            f"la secadora costaría {eur(r['totalSecadora'])} al año y el tendedero {eur(r['totalTendedero'])}: sale más barato " + ("el tendedero" if r["ganador"] == 1 else "la secadora" if r["ganador"] == 0 else "tendedero, casi igual") + f" por {eur(abs(r['diferencia']))} al año; la secadora compensaría si tu hora vale más de {eur(r['valorEq'], 2)}.")
def ej_suscrip(i, r):
    return (f"tres suscripciones de {eur(i['p1'])}, {eur(i['p2'])} y {eur(i['p3'])} al mes con {i['h1']}, {i['h2']} y {i['h3']} horas de uso, {pct(i['dto'], 0)} de descuento por pago anual y cancelables tras {i['meses']} meses",
            f"gastas {eur(r['gastoAnual'])} al año ({eur(r['mediaHora'], 2)} por hora de uso de media); la menos aprovechada es la nº {r['mayorCoste'] + 1}, y si cancelas las poco usadas y pagas el resto al año ahorrarías {eur(r['ahorroTotal'])} y quedarías en {eur(r['gastoTras'])}.")
def ej_hip_entrada(i, r):
    w = ["aportar más entrada", "conservar los ahorros", "cualquiera de las dos"][r["tipo"]]
    return (f"hipoteca de {eur(i['capital'])} al {pct(i['tin'], 2)} a {i['plazo']} años, {eur(i['extra'])} de ahorros que podrías aportar de entrada, rentabilidad del {pct(i['rent'], 1)} y horizonte de {i['anos']} años",
            f"con la entrada extra la cuota sería de {eur(r['cuotaA'], 2)} y sin ella {eur(r['cuotaB'], 2)}; a {i['anos']} años conviene {w}" + (f" por {eur(abs(r['dif']))}" if r["tipo"] != 2 else "") + f", y ambas se igualan con una rentabilidad del {pct(r['rentEq'], 1)}.")
def ej_excedencia(i, r):
    g = r["ganador"]
    return (f"neto de {eur(i['neto'])} al mes, reducción de jornada del {i['red']} % (pierdes un {i['perdida'] or i['red']} % del neto), {eur(i['cuidados'])} al mes de cuidados que te ahorras y {i['dur']} " + ("mes" if i["dur"] == 1 else "meses"),
            f"la reducción te costaría {eur(r['costeMesRed'])} al mes ({eur(r['costeTotalRed'])} en total) y la excedencia {eur(r['costeMesExc'])} al mes ({eur(r['costeTotalExc'])} en total): " + ("la reducción de jornada sale mucho más barata." if r["costeTotalRed"] < r["costeTotalExc"] else "la excedencia sale más barata."))
def ej_movil(i, r):
    n = "el nuevo" if r["mejor"] == 0 else "el reacondicionado"
    return (f"móvil nuevo de {eur(i['pnuevo'])} que dura {i['vidaN']} años o reacondicionado de {eur(i['prec'])} que dura {i['vidaR']}, {i['prob']} % de probabilidad de avería con {eur(i['rep'])} de reparación y {i['reventa']} % de reventa",
            f"el nuevo cuesta {eur(r['anoNuevo'], 2)} al año y el reacondicionado {eur(r['anoReac'], 2)}: sale más barato {n} por {eur(abs(r['diferenciaAno']), 2)} al año" + (f"; el nuevo solo compensaría si costara {eur(r['precioEquilibrio'])} o menos." if r["mejor"] == 1 else "."))
def ej_deposito(i, r):
    n = {"dep": "el depósito", "letras": "comprar Letras del Tesoro", "fondo": "el fondo monetario"}.get(r["ganador"], "ninguno claramente")
    return (f"{eur(i['importe'])} a {i['plazo']} meses: depósito al {pct(i['tin'], 2)}, Letras al {pct(i['letras'], 3)} y fondo monetario con {pct(i['rentFondo'], 1)} de rentabilidad y {pct(i['comFondo'], 1)} de comisión, " + (f"con {eur(i['otras'])} de otras rentas" if i["otras"] else "sin otras rentas"),
            f"netos de impuestos, el depósito te dejaría {eur(r['netoDep'], 2)}, las Letras {eur(r['netoLet'], 2)} y el fondo {eur(r['netoFon'], 2)}: sale mejor {n}" + (f" por {eur(r['diferencia'], 2)} sobre la segunda opción." if r["ganador"] != "empate" else "."))


# ---------- Casos típicos, tanda 5 (alquiler, trabajo, energía, hogar, coche): entradas de calcs/<slug>.test.json ----------
def fdate(x):
    a, m, d = x.split("-"); return f"{int(d)}/{int(m)}/{a}"
def ej_irav(i, r):
    ind = {"ipc": "cláusula con IPC", "igc": "cláusula sin índice", "none": "sin cláusula", "otro": "otro índice pactado"}[i["indice"]]
    ven = "dentro del periodo con tope del 2 %" if r["ventana"] else "fuera del periodo con tope del 2 %"
    if r["subidaMes"] == 0:
        f = f"la renta se queda en {eur(r['nueva'], 2)} al mes: no hay subida."
    else:
        f = f"la renta pasaría de {eur(i['renta'], 2)} a {eur(r['nueva'], 2)} al mes ({pct(r['pct'])}, {eur(r['subidaMes'], 2)} más al mes y {eur(r['subidaAnio'], 2)} más al año)" + (f"; sin tope serían {eur(r['nuevaSinTope'], 2)}." if abs(r["nuevaSinTope"] - r["nueva"]) > 0.005 else ".")
    return (f"renta de {eur(i['renta'], 2)} al mes, contrato posterior a mayo de 2023, {ind}, IRAV del {pct(i['irav'])}, IPC del {pct(i['ipc'])} y aniversario el {fdate(i['aniv'])} ({ven})", f)
def ej_incap(i, r):
    g = {"total": "total", "absoluta": "absoluta", "gran": "con gran incapacidad"}[i["grado"]]
    ex = " La pensión de incapacidad absoluta y gran incapacidad está exenta de IRPF." if r["exenta"] else ""
    cp = f", suma de {eur(r['pen_final'], 2)} de pensión y {eur(r['comp'], 2)} de complemento por gran incapacidad" if r["comp"] else ""
    return (f"incapacidad permanente {g}, por enfermedad común, base de cotización de {eur(i['base'])}, {i['edad']} años y {num(i['anos'])} años cotizados, sin trabajar",
            f"con una base reguladora de {eur(r['br'], 2)}, cobrarías {eur(r['pagado'], 2)} al mes en 14 pagas, {eur(r['anual'])} al año{cp}.{ex}")
def ej_irpf_alq(i, r):
    c = {"b50": "reducción del 50 %", "a60": "reducción del 60 % (contrato anterior a mayo de 2023)", "b70": "reducción del 70 %", "b90": "reducción del 90 % (zona tensionada)"}[i["contrato"]]
    return (f"alquiler de {eur(i['renta'])} al mes durante {i['meses']} meses, {eur(i['otros'])} de gastos, {eur(i['interep'])} de intereses, tipo marginal del {pct(i['tipo'], 0)} y {c}",
            f"ingresas {eur(r['ingresos'])} y el rendimiento previo es de {eur(r['previo'])}; con la reducción del {pct(r['pct'], 0)} tributas por {eur(r['reducido'])}, pagas {eur(r['cuota'])} de IRPF y te quedan {eur(r['neto'])} netos tras gastos e impuesto.")
def ej_valle(i, r):
    fr = {0: "el llano", 1: "la punta", 2: "la punta y el llano a partes iguales"}[i["franja"]]
    base = f"lavadora de {num(i['kwhUso'], 1)} kWh por uso y {i['usosSem']} usos a la semana, termo de {num(i['kwhTermo'])} kWh a la semana, {i['pctDesp']} % desplazable al valle, precios de {num(i['precioPunta'], 4)}/{num(i['precioLlano'], 4)}/{num(i['precioValle'], 4)} €/kWh (punta/llano/valle) y uso actual en {fr}"
    if r["estado"] == 2: f = f"el valle es más caro que tu franja actual: pasarías de {eur(r['costeHoy'], 2)} a {eur(r['costeValle'], 2)} al año en ese consumo y pagarías {eur(abs(r['ahorroAnual']), 2)} más; no compensa mover."
    else: f = f"moverlo al valle bajaría ese consumo de {eur(r['costeHoy'], 2)} a {eur(r['costeValle'], 2)} al año: ahorrarías {eur(r['ahorroAnual'], 2)} al año ({eur(r['ahorroMes'], 2)} al mes)."
    return (base, f)
def ej_aire(i, r):
    n = "el ventilador" if r["esVentilador"] else "la alternativa"
    if r["ganador"] == 0: f = f"el inverter costaría {eur(r['costeInv'], 2)} al año de luz y {n} {eur(r['costeAlt'], 2)}; con la compra repartida en {i['vida']} años, el inverter sale {eur(abs(r['diferencia']))} más barato."
    else: f = f"el inverter costaría {eur(r['costeInv'], 2)} al año de luz y {n} {eur(r['costeAlt'], 2)}; con la compra repartida en {i['vida']} años, {n} sale {eur(abs(r['diferencia']))} más barato."
    if r["horasEq"] > 0 and r["ganador"] == 0: f += f" El inverter compensa a partir de {num(r['horasEq'], 1)} horas al día."
    return (f"inverter de {num(i['kwInv'], 1)} kW (compra de {eur(i['compraInv'])}) frente a una alternativa de {num(i['kwAlt'], 2)} kW (compra de {eur(i['compraAlt'])}), {num(i['horas'])} {'hora' if i['horas'] == 1 else 'horas'} al día durante {i['dias']} días, {eur(i['precio'], 2)}/kWh y {i['vida']} años de vida", f)
def ej_freidora(i, r):
    alt = ["el horno eléctrico tradicional", "el horno eléctrico ventilado", "el microondas", "el horno de gas"][i["alt"]]
    altf = alt.replace("el ", "al ", 1)
    w = "la freidora" if r["ganador"] == 0 else "la alternativa" if r["ganador"] == 1 else "ninguna claramente"
    f = f"la freidora costaría {eur(r['anualFr'], 2)} al año de energía ({eur(r['totalFr'], 2)} con la compra repartida) y {alt} {eur(r['anualAlt'], 2)}: sale más barato {w}" + (f" por {eur(abs(r['diferencia']), 2)} al año." if r["ganador"] != 2 else " (diferencia de menos del 5 %).")
    return (f"freidora de aire de {num(i['kwFr'], 1)} kW (compra de {eur(i['compra'])}) frente {altf}, {i['usos']} usos a la semana, {i['minFr']} minutos de cocción con la freidora frente a {i['minAlt']} con la otra opción", f)
def ej_paro_aut(i, r):
    return (f"base de cotización de {eur(i['base'])}/mes, {i['m48']} meses cotizados por cese en 48 meses, {i['hijos']} hijos a cargo, cese por motivos económicos y {i['edad']} años",
            f"cobrarías {eur(r['prest'], 2)} al mes durante {r['dur']} meses: {eur(r['total'], 2)} en total" + (f"; el tope legal de {eur(r['tope'])}/mes limita la cuantía (el 70 % de tu base serían {eur(r['raw'], 2)})." if r["ap"] == 1 else "."))
def ej_aceptar(i, r):
    w = {1: "seguir solo con el paro", 2: "compatibilizar el trabajo con el paro", 3: "trabajar renunciando al paro"}[r["winner"]]
    return (f"paro de {eur(i['cuantia'])} brutos al mes con {i['meses']} meses por cobrar, trabajo de {eur(i['sueldo'])} netos al mes al {i['jornada']} % de jornada durante {i['duracion']} meses e IRPF del {pct(i['irpf'], 0)}",
            f"seguir solo con el paro daría {eur(r['totalA'])}; compatibilizar " + (f"daría {eur(r['totalB'])}" if r["bOk"] else "no es posible a jornada completa") + f" y trabajar renunciando al paro {eur(r['totalC'])}: sale mejor {w} por {eur(r['margen'])} sobre la segunda opción.")
def ej_seg_hogar(i, r):
    w = "la póliza con franquicia" if r["mejor"] == 0 else "la póliza sin franquicia"
    return (f"póliza sin franquicia de {eur(i['primaSin'])} al año frente a {eur(i['primaCon'])} con franquicia de {eur(i['franq'])}, {num(i['frec'], 2)} siniestros pequeños al año de {eur(i['coste'])} de media y horizonte de {i['horizonte']} años",
            f"con franquicia ahorras {eur(r['ahorroAnual'])} al año de prima y pagas de tu bolsillo {eur(r['perdidaAnual'], 2)} al año en siniestros: " + (f"a {i['horizonte']} años quedas {eur(r['netoTotal'])} a favor" if r["netoTotal"] >= 0 else f"a {i['horizonte']} años pierdes {eur(abs(r['netoTotal']))}") + f", así que sale mejor {w}; se igualan con unos {num(r['frecEquilibrio'], 2)} siniestros al año.")
def ej_mudanza(i, r):
    t = {1: "la empresa sale más barata", 2: "la furgoneta ahorra algo, pero la reserva por daños se lo come", 3: "la furgoneta sale más barata"}[r["tipo"]]
    return (f"mudanza de {i['vol']} m3 a {i['dist']} km, empresa a {eur(i['empresa'])}, furgoneta a {eur(i['alqdia'])} al día, {i['nayud']} ayudantes a {eur(i['eurayud'])} la hora y {eur(i['extras'])} de extras",
            f"la furgoneta costaría {eur(r['costeFurgo'], 2)} ({eur(r['costeFurgoConReserva'], 2)} con reserva de daños) en {r['viajes']} {'viaje' if r['viajes'] == 1 else 'viajes'} y {r['dias']} {'día' if r['dias'] == 1 else 'días'} de alquiler, con unas {num(r['horasTuyas'], 1)} horas tuyas, frente a {eur(r['costeEmpresa'])} de la empresa: {t}.")
def ej_gasolinera(i, r):
    f = f"ahorras {eur(r['bruto'], 2)} en el depósito y gastas {eur(r['combustible'], 2)} de combustible en el desvío: " + (f"te quedan {eur(r['neto'], 2)} netos; compensa hasta {num(r['kmEquilibrio'], 1)} km de desvío." if r["neto"] > 0 else f"pierdes {eur(abs(r['neto']), 2)}; solo compensaría hasta {num(r['kmEquilibrio'], 1)} km de desvío.")
    t = f"{i['litros']} litros con {eur(i['dif'], 2)}/l de diferencia, {i['km']} km de desvío entre ida y vuelta, consumo de {num(i['cons'], 1)} l/100 km y gasolina a {eur(i['precio'], 3)}/l" + (f", contando tu tiempo a {eur(i['valorHora'])}/h" if i["valorHora"] else "")
    return (t, f)
def ej_km_dietas(i, r):
    if r["tribTotal"] == 0: f = f"todo queda exento ({eur(r['exentoTotal'], 2)}) y no tributa nada"
    else: f = f"quedan exentos {eur(r['exentoTotal'], 2)} y tributan {eur(r['tribTotal'], 2)}, con {eur(r['cargaExtra'], 2)} de impuestos y cotización extra"
    k = f"; el coche te cuesta {eur(r['costeCoche'])} y te deja {eur(r['netoCoche'], 2)} netos" if i["km"] else ""
    return (f"{num(i['km'])} km a {eur(i['pagokm'], 2)}/km con un coche de {eur(i['costekm'], 2)}/km, {eur(i['peajes'])} de peajes, {i['diasSin']} días de dieta sin pernocta y {i['diasCon']} con pernocta a {eur(i['dieta'], 2)} y tipo del {pct(i['tipo'], 0)}",
            f + (k.replace("te deja -", "te hace perder ").replace("te deja", "te deja") if r["netoCoche"] >= 0 else f"; el coche te cuesta {eur(r['costeCoche'])} y te hace perder {eur(abs(r['netoCoche']), 2)} netos" if i["km"] else "") + ".")

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
    "autonomo-o-asalariado": (ej_autonomo, [
        {"bruto": 30000, "factura": 45000, "gastos": 3000, "ccaa": "madrid", "hijos": "0", "contrato": "indef"},
        {"bruto": 24000, "factura": 30000, "gastos": 2000, "ccaa": "madrid", "hijos": "1", "contrato": "indef"}]),
    "comparar-ofertas-de-trabajo-neto-real": (ej_ofertas, [
        {"brutoA": 32000, "brutoB": 36000, "ccaa": "madrid", "pagas": "14", "desplA": 600, "desplB": 1800, "horasA": 40, "horasB": 40},
        {"brutoA": 28000, "brutoB": 30000, "ccaa": "madrid", "pagas": "12", "desplA": 0, "desplB": 1200, "horasA": 40, "horasB": 40}]),
    "cuanto-ahorrar-para-comprar-casa": (ej_casa, [
        {"precio": 250000, "ccaa": "madrid", "tipo": "usada", "entrada": 20, "gastos": 2500, "anos": 5, "rentab": 0, "interes": 3.0},
        {"precio": 180000, "ccaa": "andalucia", "tipo": "nueva", "entrada": 20, "gastos": 2500, "anos": 4, "rentab": 0, "interes": 3.0}]),
    "subsidio-desempleo-cuanto-cobro-y-cuanto-dura": (ej_subsidio, [
        {"situ": "agotado", "dias": 360, "edad": 40, "hijos": 1, "conyuge": "no", "renta": 0, "rentaOtros": 0, "jub": "no"},
        {"situ": "insuf", "dias": 200, "edad": 35, "hijos": 0, "conyuge": "no", "renta": 0, "rentaOtros": 0, "jub": "no"}]),
    "permiso-nacimiento-cuanto-cobro-y-como-repartir": (ej_permiso, [
        {"sueldoA": 3200, "sueldoB": 2400, "mono": "no", "amp": 0, "semA": 19, "semB": 19, "complA": 0, "complB": 0},
        {"sueldoA": 2000, "sueldoB": 2400, "mono": "si", "amp": 0, "semA": 19, "semB": 19, "complA": 0, "complB": 0}]),
    "empleada-hogar-cuanto-cuesta-contratar-cotizacion": (ej_hogar, [
        {"modo": "horas", "horas": 20, "importe": 10, "pagas": "prorr", "fam": "no", "meses": 12, "tipo": "indef"},
        {"modo": "mensual", "horas": 20, "importe": 900, "pagas": "14", "fam": "no", "meses": 12, "tipo": "indef"}]),
    "plan-pensiones-o-fondo-indexado": (ej_plan, [
        {"aportacion": 1500, "anos": 25, "renta": 35000, "ccaa": "madrid", "rescate": "1", "rentab": 4, "comPlan": 1.0, "comFondo": 0.2},
        {"aportacion": 3000, "anos": 15, "renta": 50000, "ccaa": "madrid", "rescate": "1", "rentab": 4, "comPlan": 1.0, "comFondo": 0.2}]),
    "donativos-irpf-cuanto-desgrava-y-cuanto-donar": (ej_donativos, [
        {"donado": 100, "recurrente": "1", "bl": 25000, "adicional": 0, "ambito": "comun"},
        {"donado": 300, "recurrente": "0", "bl": 25000, "adicional": 0, "ambito": "comun"},
        {"donado": 1000, "recurrente": "0", "bl": 30000, "adicional": 0, "ambito": "comun"}]),
    "obligado-a-declarar-renta-dos-pagadores": (ej_obligado, [
        {"t1": 18000, "t2": 2000, "t3": 0, "noRet": "0", "capRet": 0, "inmo": 0, "esp": "0", "obl": "0", "reg": "comun"},
        {"t1": 14000, "t2": 1500, "t3": 0, "noRet": "0", "capRet": 0, "inmo": 0, "esp": "0", "obl": "0", "reg": "comun"}]),
    "deduccion-maternidad-familia-numerosa": (ej_maternidad, [
        {"n3": "1", "mesesMat": 12, "guarMeses": 10, "guarGasto": 3000, "fam": "general", "hijosFam": 3, "mesesFam": 12, "cotiz": 3500},
        {"n3": "2", "mesesMat": 12, "guarMeses": 0, "guarGasto": 0, "fam": "no", "hijosFam": 3, "mesesFam": 12, "cotiz": 3500}]),
    "sueldo-bruto-a-neto-2026": (ej_sueldo, [
        {"bruto": 25200, "pagas": 14, "contrato": "indef", "ccaa": "madrid", "hijos": 0, "menores3": 0, "meses": 6},
        {"bruto": 35000, "pagas": 14, "contrato": "indef", "ccaa": "cataluna", "hijos": 0, "menores3": 0, "meses": 6},
        {"bruto": 40000, "pagas": 14, "contrato": "indef", "ccaa": "galicia", "hijos": 3, "menores3": 1, "meses": 6}]),
    "luz-fija-o-indexada": (ej_luz, [
        {"consumo": 3000, "potencia": 4.6, "pctPunta": 30, "pctLlano": 30, "precioFijo": 0.15, "potFija": 0.0779, "pvpc": 0.184, "hip": 0},
        {"consumo": 4200, "potencia": 5.5, "pctPunta": 30, "pctLlano": 30, "precioFijo": 0.1, "potFija": 0.0779, "pvpc": 0.21339, "hip": 10},
        {"consumo": 2500, "potencia": 3.45, "pctPunta": 10, "pctLlano": 10, "precioFijo": 0.22, "potFija": 0.0902, "pvpc": 0.12, "hip": -10}]),
    "placas-solares-merece-la-pena": (ej_placas, [
        {"potencia": 4, "coste": 6000, "subv": 0, "consumo": 4000, "pctAuto": 40, "prod": 1610, "precio": 0.18, "comp": 0.07},
        {"potencia": 6, "coste": 12000, "subv": 1500, "consumo": 3000, "pctAuto": 30, "prod": 1280, "precio": 0.25, "comp": 0.1},
        {"potencia": 4, "coste": 9000, "subv": 0, "consumo": 4000, "pctAuto": 30, "prod": 1165, "precio": 0.13, "comp": 0.07}]),
    "seguro-salud-privado-merece-la-pena": (ej_salud, [
        {"prima": 900, "empresa": 0, "subidaPrima": 4, "actos": 8, "coste": 60, "copago": 8, "subidaPrecios": 2, "horizonte": 10},
        {"prima": 900, "empresa": 0, "subidaPrima": 4, "actos": 25, "coste": 60, "copago": 8, "subidaPrecios": 2, "horizonte": 10},
        {"prima": 900, "empresa": 50, "subidaPrima": 0, "actos": 8, "coste": 60, "copago": 8, "subidaPrecios": 0, "horizonte": 10}]),
    "coche-nuevo-o-seminuevo": (ej_coche_ns, [
        {"pnuevo": 25000, "psemi": 17500, "edad": 3, "anos": 5, "dep1": 18, "gastos": 1000, "extra": 300, "tin": 0},
        {"pnuevo": 25000, "psemi": 17500, "edad": 3, "anos": 5, "dep1": 18, "gastos": 1000, "extra": 300, "tin": 6.5}]),
    "tren-avion-o-coche": (ej_tren, [
        {"dist": 620, "viaj": 2, "tren": 60, "avion": 110, "htren": 3.5, "havion": 4.5, "kmcoche": 0.2, "extras": 40},
        {"dist": 620, "viaj": 4, "tren": 60, "avion": 110, "htren": 3.5, "havion": 4.5, "kmcoche": 0.2, "extras": 40},
        {"dist": 620, "viaj": 1, "tren": 150, "avion": 110, "htren": 8, "havion": 4.5, "kmcoche": 0.2, "extras": 40}]),
    "teletrabajo-o-oficina-coste-real": (ej_tele, [
        {"dias": 2, "desp": 6, "min": 60, "valorHora": 0, "casa": 0.7, "comida": 5, "comp": 0, "equip": 300},
        {"dias": 2, "desp": 2, "min": 60, "valorHora": 0, "casa": 5, "comida": 1, "comp": 20, "equip": 0},
        {"dias": 5, "desp": 1, "min": 60, "valorHora": 15, "casa": 0.5, "comida": 0, "comp": 0, "equip": 900}]),
    "cocinar-en-casa-o-comer-fuera": (ej_cocinar, [
        {"fuera": 3, "precio": 13, "racion": 4, "minCook": 30, "minDesp": 15, "vh": 0, "sust": 3, "dias": 220},
        {"fuera": 3, "precio": 13, "racion": 4, "minCook": 30, "minDesp": 15, "vh": 40, "sust": 3, "dias": 220},
        {"fuera": 3, "precio": 13, "racion": 4, "minCook": 30, "minDesp": 15, "vh": 10, "sust": 3, "dias": 220}]),
    "fondo-de-emergencia-cuantos-meses-necesito": (ej_fondo, [
        {"gastos": 1500, "empleo": 0, "ingresos": 0, "dep": 1, "otro": 0, "ahorro": 3000, "aport": 200},
        {"gastos": 1500, "empleo": 2, "ingresos": 1, "dep": 2, "otro": 0, "ahorro": 3000, "aport": 200},
        {"gastos": 1500, "empleo": 0, "ingresos": 0, "dep": 1, "otro": 0, "ahorro": 6000, "aport": 200}]),
    "reformar-o-mudarse": (ej_reformar, [
        {"reforma": 20000, "recup": 50, "valor": 250000, "gastosPct": 10, "dif": 0, "extras": 3000, "mensual": -50, "anios": 10},
        {"reforma": 20000, "recup": 50, "valor": 250000, "gastosPct": 10, "dif": 0, "extras": 3000, "mensual": -50, "anios": 1},
        {"reforma": 60000, "recup": 30, "valor": 250000, "gastosPct": 3, "dif": 0, "extras": 500, "mensual": 80, "anios": 10}]),
    "pension-viudedad-cuanto-cobro": (ej_viudedad, T("pension-viudedad-cuanto-cobro", 0, 1, 3)),
    "diesel-gasolina-hibrido-electrico": (ej_motor, T("diesel-gasolina-hibrido-electrico", 0, 1, 2)),
    "potencia-contratada-luz-bajar-compensa": (ej_potencia, T("potencia-contratada-luz-bajar-compensa", 0, 2, 3)),
    "jubilarse-en-2026-o-en-2027-edad-y-pension": (ej_jub2627, T("jubilarse-en-2026-o-en-2027-edad-y-pension", 0, 2)),
    "guarderia-cuidadora-o-reducir-jornada": (ej_guarderia, T("guarderia-cuidadora-o-reducir-jornada", 0, 1)),
    "declaracion-conjunta-o-individual": (ej_conjunta, T("declaracion-conjunta-o-individual", 0, 1, 7)),
    "nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad": (ej_nomina27, T("nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad", 0, 1, 7)),
    "cuanto-cuesta-un-bebe-el-primer-ano": (ej_bebe, T("cuanto-cuesta-un-bebe-el-primer-ano", 0, 2, 4)),
    "venta-vivienda-plusvalia-irpf-exencion": (ej_venta, T("venta-vivienda-plusvalia-irpf-exencion", 0, 3, 5)),
    "cuota-autonomos-ingresos-reales-regularizacion": (ej_cuota_aut, T("cuota-autonomos-ingresos-reales-regularizacion", 0, 1, 2)),
    "amortizar-plazo-o-cuota": (ej_amortizar, T("amortizar-plazo-o-cuota", 0)),
    "gimnasio-o-entrenar-en-casa": (ej_gimnasio, T("gimnasio-o-entrenar-en-casa", 0, 1)),
    "coche-propio-o-carsharing-o-vtc": (ej_coche_propio, T("coche-propio-o-carsharing-o-vtc", 0, 1)),
    "caldera-reparar-o-cambiar": (ej_caldera, T("caldera-reparar-o-cambiar", 0, 1, 2)),
    "secadora-o-tendedero-coste-por-lavado": (ej_secadora, T("secadora-o-tendedero-coste-por-lavado", 0, 1)),
    "suscripciones-cuanto-gasto-al-ano": (ej_suscrip, T("suscripciones-cuanto-gasto-al-ano", 0, 2)),
    "hipoteca-mas-entrada-o-conservar-ahorros": (ej_hip_entrada, T("hipoteca-mas-entrada-o-conservar-ahorros", 0, 1)),
    "excedencia-o-reduccion-jornada": (ej_excedencia, T("excedencia-o-reduccion-jornada", 0, 1)),
    "movil-reacondicionado-o-nuevo": (ej_movil, T("movil-reacondicionado-o-nuevo", 0, 1)),
    "deposito-letras-o-fondo-monetario": (ej_deposito, T("deposito-letras-o-fondo-monetario", 0, 3)),
    "actualizacion-renta-alquiler-irav-ipc": (ej_irav, T("actualizacion-renta-alquiler-irav-ipc", 1, 4, 11)),
    "incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar": (ej_incap, T("incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar", 0, 1, 2)),
    "irpf-alquilar-vivienda-rendimiento-neto": (ej_irpf_alq, T("irpf-alquilar-vivienda-rendimiento-neto", 0, 2, 3)),
    "horas-valle-luz-lavadora-termo-cuanto-ahorro": (ej_valle, T("horas-valle-luz-lavadora-termo-cuanto-ahorro", 0, 1, 4)),
    "aire-acondicionado-inverter-o-ventilador-coste-verano": (ej_aire, T("aire-acondicionado-inverter-o-ventilador-coste-verano", 0, 1, 2)),
    "freidora-de-aire-u-horno-cuanto-gasta": (ej_freidora, T("freidora-de-aire-u-horno-cuanto-gasta", 0, 2, 3)),
    "paro-autonomos-cese-actividad-cuanto-cobro": (ej_paro_aut, T("paro-autonomos-cese-actividad-cuanto-cobro", 0, 1, 4)),
    "aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad": (ej_aceptar, T("aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad", 0, 1, 2)),
    "seguro-hogar-con-o-sin-franquicia": (ej_seg_hogar, T("seguro-hogar-con-o-sin-franquicia", 0, 1)),
    "mudanza-empresa-o-furgoneta": (ej_mudanza, T("mudanza-empresa-o-furgoneta", 0, 1, 3)),
    "gasolinera-low-cost-compensa-desviarse": (ej_gasolinera, T("gasolinera-low-cost-compensa-desviarse", 0, 1, 4)),
    "kilometraje-y-dietas-exentas-irpf": (ej_km_dietas, T("kilometraje-y-dietas-exentas-irpf", 0, 2, 3)),
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
