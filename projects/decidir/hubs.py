"""Hubs temáticos (dueño: Estratega SEO/GEO). Una página-mapa por tema, en orden de decisión, con datos vivos fechados.
Reutilizable: añade una entrada a HUBS (y nada más) cuando el tema cumpla el disparador: >= MIN_PAGES páginas propias
(calculadoras del tema + guías que enlazan a ellas). build.main llama a hubs.eligible()/page() sin conocer el tema.
Texto: solo cifras de data/live.json (marcadores {{...}}), del Barómetro o de la propia calculadora; nunca de memoria."""
import json, os, html
import seo, calcs_loader

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_PAGES = 6
AUTHOR = seo.AUTHOR

HUBS = {
    "hipoteca": {
        "path": "/hipoteca/",
        "tema": "hipoteca",
        "title": "Calculadoras de hipoteca: decide con tus números",
        "h1": "Hipotecas: decide con tus números",
        "description": "Del ahorro a la amortización: las calculadoras de hipoteca en orden de decisión, con el Euríbor y el tipo fijo medio del BCE de este mes.",
        "kicker": "Tema · Hipoteca y vivienda",
        "nav": "Hipotecas",
        "all_title": "Todas las calculadoras de hipoteca",
        "baro": ("/barometro/#hipoteca", 0, "Cifras propias de cada mes con su fecha: Euríbor de equilibrio, coste por km y rentabilidad para invertir antes que amortizar."),
        "fechas": ["fecha_tipo_fijo", "fecha_euribor"],
        "disclaimer": "Información orientativa, no constituye asesoramiento financiero ni legal. Los datos de mercado proceden del Banco Central Europeo y se actualizan con cada dato nuevo; las condiciones de tu hipoteca están en tu escritura.",
        "lead": ("<strong>Respuesta corta:</strong> una hipoteca se decide en seis pasos y el orden importa: cuánto ahorrar, alquilar o comprar, fija o variable, "
                 "cambiarla de banco, amortizar plazo o cuota y amortizar o invertir. Hoy el Euríbor a 12 meses está en el {{euribor_12m}} % "
                 "(media de {{periodo_euribor_es}}) y las hipotecas fijas nuevas a más de 10 años se firman de media al {{tipo_fijo}} % ({{periodo_tipo_fijo_es}}); fuente: BCE."),
        "groups": [
            ("Antes de firmar", ["cuanto-ahorrar-para-comprar-casa", "alquilar-o-comprar", "hipoteca-mas-entrada-o-conservar-ahorros", "hipoteca-20-25-o-30-anos-cuota-vs-intereses", "hipoteca-fija-o-variable", "hipoteca-bonificada-o-sin-vinculaciones", "seguro-vida-hipoteca-banco-o-externo"]),
            ("Con la hipoteca ya firmada", ["subrogar-hipoteca-merece-la-pena", "amortizar-plazo-o-cuota", "amortizar-o-invertir"]),
            ("Si ya vives en tu casa", ["reformar-o-mudarse"]),
        ],
        "steps": {
            "hipoteca-20-25-o-30-anos-cuota-vs-intereses": {
                "name": "Plazo: 20, 25 o 30 años",
                "text": "Un plazo más corto paga menos intereses pero sube la cuota. El que te conviene es el más corto cuya cuota, sumada a tus otras deudas, quepa en el tope de esfuerzo que fijes; la calculadora lo elige y, si no cabe ninguno, te da el plazo mínimo.",
            },
            "hipoteca-mas-entrada-o-conservar-ahorros": {
                "name": "Más entrada o conservar ahorros",
                "text": "Aportar más entrada baja la hipoteca y los intereses, pero deja el dinero atado al piso. La calculadora compara el patrimonio a N años de cada opción y la rentabilidad de equilibrio, y avisa si te quedas sin liquidez.",
            },
            "hipoteca-bonificada-o-sin-vinculaciones": {
                "name": "Bonificada o sin vinculaciones",
                "text": "La bonificada baja el tipo a cambio de contratar nómina, seguros u otros productos. Solo compensa si esa rebaja supera la bonificación mínima que sale de tu capital, plazo, tipo, comisiones y coste de las vinculaciones; la calculadora te da ese umbral.",
            },
            "seguro-vida-hipoteca-banco-o-externo": {
                "name": "Seguro de vida: el del banco o uno externo",
                "text": "Con una póliza externa de coberturas equivalentes, el seguro del banco solo compensa si la bonificación del tipo supera la mínima que sale de tu capital, plazo, tipo y primas. La calculadora te da ese umbral.",
            },
            "cuanto-ahorrar-para-comprar-casa": {
                "name": "Cuánto dinero necesitas",
                "text": "Antes de mirar pisos, calcula el efectivo que hace falta de verdad: la entrada, los impuestos (ITP en vivienda usada; IVA y AJD en nueva) y los gastos de notaría, registro, gestoría y tasación. Es la cifra que te dice si puedes empezar ya o te conviene esperar.",
            },
            "alquilar-o-comprar": {
                "name": "Alquilar o comprar",
                "text": "Comprar no gana siempre: depende de cuántos años te vas a quedar, de cuánto suba la vivienda y de lo que harías con el dinero de la entrada. La calculadora compara el patrimonio de cada opción y dice en qué año compensa comprar.",
            },
            "hipoteca-fija-o-variable": {
                "name": "Fija o variable",
                "text": "La variable paga Euríbor más un diferencial; la fija protege la cuota a cambio de un tipo inicial mayor. La clave es el Euríbor medio a partir del cual la fija te sale más barata.",
                "datos": "{{baro}}",
                "fecha": ("fecha_euribor", "Euríbor"),
                "guia": "euribor-hipoteca",
            },
            "subrogar-hipoteca-merece-la-pena": {
                "name": "Cambiar la hipoteca de banco o a fija",
                "text": "Si ya tienes hipoteca, compara su tipo con lo que se ofrece hoy: el tipo fijo medio de las hipotecas nuevas es del {{tipo_fijo}} % ({{periodo_tipo_fijo_es}}, BCE). Cambiar compensa si el ahorro supera la comisión y los gastos del cambio antes de que acabes el préstamo.",
            },
            "amortizar-plazo-o-cuota": {
                "name": "Amortizar: plazo o cuota",
                "text": "Con la misma cantidad, reducir plazo ahorra más intereses; reducir cuota solo compensa si necesitas respirar cada mes. Antes de pagar, mira qué comisión máxima te puede cobrar el banco.",
                "guia": "amortizacion-anticipada-comisiones",
            },
            "reformar-o-mudarse": {
                "name": "Reformar o mudarte",
                "text": "Reformar compensa frente a mudarte mientras el coste neto de la obra sea menor que el de cambiar de casa. La calculadora da el año de equilibrio y el presupuesto máximo con el que reformar sigue ganando; el valor que recuperas al vender es una hipótesis tuya.",
            },
            "amortizar-o-invertir": {
                "name": "Amortizar o invertir",
                "text": "Amortizar equivale a invertir sin riesgo al tipo de tu hipoteca. Solo compensa invertir si esperas una rentabilidad neta claramente mayor y aceptas que no llegue.",
            },
        },
    },
    "coche": {
        "path": "/coche/",
        "tema": "coche",
        "title": "Calculadoras de coche: cuánto cuesta y qué te conviene",
        "h1": "Coche: decide con tus números",
        "description": "Si necesitas coche, cuál, con qué motor, comprar o renting y qué seguro: las calculadoras en orden, con el precio de los carburantes de hoy (MITECO).",
        "kicker": "Tema · Coche y movilidad",
        "nav": "Coche",
        "all_title": "Todas las calculadoras de coche y movilidad",
        "baro": ("/barometro/#coche", 1, "Cada mes, el coste por km de diésel, gasolina, híbrido y eléctrico con los precios del día y su fecha."),
        "fechas": ["fecha_carburantes"],
        "disclaimer": "Información orientativa, no constituye asesoramiento financiero. Los precios de los carburantes son una media simple de las gasolineras de Península y Baleares publicada por el Ministerio para la Transición Ecológica (MITECO); tu gasolinera, tu consumo y las condiciones de tu oferta mandan.",
        "lead": ("<strong>Respuesta corta:</strong> el coche se decide de lo general a lo concreto: primero si lo necesitas para tus trayectos, después cuál (nuevo o seminuevo, y con qué motor), "
                 "cómo pagarlo (comprar o renting) y qué seguro. El combustible es solo una parte del coste: la depreciación, el seguro y la financiación pesan aunque el coche esté parado. "
                 "Hoy la gasolina 95 cuesta {{gasolina}} €/l y el diésel {{diesel}} €/l de media ({{fecha_carburantes_es}}; fuente: MITECO)."),
        "groups": [
            ("¿Necesitas coche?", ["coche-propio-o-carsharing-o-vtc", "bici-electrica-o-transporte-publico", "tren-avion-o-coche", "equipaje-y-asiento-avion-coste-real"]),
            ("Si vas a tener coche", ["coche-nuevo-o-seminuevo", "diesel-gasolina-hibrido-electrico", "coche-segunda-mano-particular-o-concesionario", "comprar-coche-o-renting", "seguro-todo-riesgo-o-terceros", "gasolinera-low-cost-compensa-desviarse"]),
        ],
        "steps": {
            "coche-propio-o-carsharing-o-vtc": {
                "name": "Coche propio, carsharing o taxi/VTC",
                "text": "Tener coche tiene costes fijos que pagas aunque no lo uses. La calculadora te da los kilómetros al año a partir de los cuales compensa tenerlo; por debajo, sale más barato el carsharing o el taxi/VTC con tus tarifas.",
            },
            "bici-electrica-o-transporte-publico": {
                "name": "Para ir a trabajar: bici eléctrica, abono o coche",
                "text": "Para los trayectos diarios, compara el coste anual de la bici eléctrica, el abono de transporte y el coche, y en cuántos años se amortiza la bici con tus kilómetros.",
            },
            "tren-avion-o-coche": {
                "name": "Para viajar: tren, avión o coche",
                "text": "En un viaje largo el coche cuesta lo mismo vayas solo o acompañado, y los billetes se multiplican por viajero. La calculadora te dice con cuántos viajeros gana el coche y cuánto tiene que valer tu hora para que compense ir más rápido.",
            },
            "equipaje-y-asiento-avion-coste-real": {
                "name": "Avión: equipaje y asiento",
                "text": "La tarifa low cost solo es la más barata hasta que sumas maleta, asiento y embarque prioritario. La calculadora compara el coste real por viaje con las tarifas que tú introduces y te dice cuándo compensa la tarifa completa.",
            },
            "coche-nuevo-o-seminuevo": {
                "name": "Nuevo o seminuevo",
                "text": "La diferencia la marca la pérdida de valor de los primeros años frente a la garantía y las averías del seminuevo. La calculadora te da el año en que se igualan y el precio máximo del seminuevo que compensa.",
                "guia": "cuanto-cuesta-tener-coche",
            },
            "diesel-gasolina-hibrido-electrico": {
                "name": "Diésel, gasolina, híbrido o eléctrico",
                "text": "Cuantos más kilómetros haces, más pesa el coste por kilómetro frente al precio de compra. La calculadora usa el precio medio del día del diésel y la gasolina y te dice desde qué kilometraje cambia el orden.",
                "datos": "{{baro}} Precios de hoy: gasolina 95 a {{gasolina}} €/l y diésel a {{diesel}} €/l (MITECO).",
                "fecha": ("fecha_carburantes", "Carburantes"),
            },
            "coche-segunda-mano-particular-o-concesionario": {
                "name": "Segunda mano: particular o concesionario",
                "text": "El particular suele ser más barato, pero sin garantía ni revisión. La calculadora pone precio a ese riesgo y te dice cuánto más puedes pagar al concesionario antes de que deje de compensar.",
            },
            "comprar-coche-o-renting": {
                "name": "Comprar o renting",
                "text": "Compara el coste real de comprar (préstamo, seguro, mantenimiento y lo que recuperas al venderlo) con la cuota del renting, que lo incluye casi todo. La calculadora da la cuota de renting de equilibrio.",
            },
            "gasolinera-low-cost-compensa-desviarse": {
                "name": "Repostar: gasolinera low cost",
                "text": "Ahorrar unos céntimos por litro no compensa si el desvío te cuesta más en combustible. La calculadora te dice cuántos kilómetros de desvío puedes hacer antes de perder el ahorro.",
            },
            "seguro-todo-riesgo-o-terceros": {
                "name": "Seguro: todo riesgo o terceros",
                "text": "El todo riesgo compensa mientras el coche valga bastante más que la diferencia de prima; al depreciarse, deja de hacerlo. La calculadora te dice desde qué año, con tus primas y tu franquicia.",
            },
        },
    },
    "energia": {
        "path": "/energia/",
        "tema": "energia",
        "title": "Calculadoras de energía en casa: luz, calefacción y placas",
        "h1": "Energía en casa: decide con tus números",
        "description": "De la tarifa de luz a las placas solares: las decisiones de energía de tu casa en orden, con el PVPC de hoy (Red Eléctrica) y la tarifa del gas (BOE).",
        "kicker": "Tema · Energía en casa",
        "nav": "Energía",
        "all_title": "Todas las calculadoras de energía",
        "baro": None,
        "fechas": ["fecha_pvpc", "fecha_gas"],
        "disclaimer": "Información orientativa, no constituye asesoramiento. El precio del PVPC es el de la energía publicado por Red Eléctrica (sin peajes, cargos ni impuestos) y la tarifa del gas, la TUR publicada en el BOE; tu factura y tu contrato mandan. No prometemos ahorros: dependen de tu vivienda, tu zona y tu consumo.",
        "lead": ("<strong>Respuesta corta:</strong> en energía, decide primero lo que no cuesta dinero y después lo que exige obra: la tarifa de luz, el sistema de calefacción, las ventanas y el aislamiento, "
                 "las placas solares y, al final, los electrodomésticos. Hoy la energía del PVPC cuesta {{pvpc_hoy}} €/kWh de media ({{fecha_pvpc_es}}, sin peajes ni impuestos; fuente: Red Eléctrica) "
                 "y el gas con la tarifa regulada TUR.2 sale a {{gas_kwh}} €/kWh con impuestos ({{periodo_gas_es}}; fuente: BOE)."),
        "groups": [
            ("Sin obra: lo primero", ["luz-fija-o-indexada", "potencia-contratada-luz-bajar-compensa", "horas-valle-luz-lavadora-termo-cuanto-ahorro", "calefaccion-gas-aerotermia-electrica"]),
            ("Con inversión: cuándo se amortiza", ["caldera-reparar-o-cambiar", "termo-electrico-o-calentador-gas-o-aerotermia-agua", "cambiar-ventanas-aislamiento-merece-la-pena", "placas-solares-merece-la-pena", "punto-de-carga-casa-con-o-sin-placas", "cambiar-electrodomestico-antiguo-merece-la-pena", "reparar-o-comprar-electrodomestico", "aire-acondicionado-inverter-o-ventilador-coste-verano"]),
        ],
        "steps": {
            "luz-fija-o-indexada": {
                "name": "Tarifa de luz: fija o PVPC",
                "text": "No requiere obra y se revisa en una tarde. La tarifa fija compensa si el precio de su energía queda por debajo del punto de equilibrio con el PVPC, que depende de cuándo consumes.",
                "datos": "Precio medio de la energía del PVPC: {{pvpc_hoy}} €/kWh (media de las 24 horas, sin peajes, cargos ni impuestos; Red Eléctrica).",
                "fecha": ("fecha_pvpc", "PVPC"),
                "guia": "checklist-casa-antes-del-invierno",
            },
            "potencia-contratada-luz-bajar-compensa": {
                "name": "Potencia contratada: bajarla o no",
                "text": "Bajar los kW contratados reduce el término fijo de la factura sin obra. La calculadora estima el ahorro anual y los años que tarda en recuperarse el coste del cambio; el límite lo marca tu pico real de uso.",
                "guia": "ahorrar-factura-luz-potencia-horas-valle-tarifa",
            },
            "horas-valle-luz-lavadora-termo-cuanto-ahorro": {
                "name": "Horas valle: lavadora, lavavajillas y termo",
                "text": "Mover consumos a la franja valle solo ahorra si tu tarifa tiene discriminación horaria. La calculadora da el ahorro anual con tus kWh y tus precios por periodo.",
                "guia": "ahorrar-factura-luz-potencia-horas-valle-tarifa",
            },
            "calefaccion-gas-aerotermia-electrica": {
                "name": "Calefacción: gas, aerotermia o eléctrica",
                "text": "La aerotermia suele ser la más barata de usar, pero su instalación es más cara: solo compensa si la casa gasta bastante calefacción y la usas varios años. La calculadora compara el coste total con tu zona y tu aislamiento.",
                "datos": "Gas con la tarifa regulada TUR.2: {{gas_kwh}} €/kWh con impuestos en {{periodo_gas_es}} (BOE).",
                "fecha": ("fecha_gas", "Tarifa del gas"),
            },
            "caldera-reparar-o-cambiar": {
                "name": "Reparar o cambiar la caldera",
                "text": "Cambiarla sale más barato que repararla cuando el presupuesto de la reparación supera el punto de equilibrio que sale de tu consumo de gas, tu rendimiento actual y el precio de la nueva. Es una estimación económica; el diagnóstico lo hace un técnico autorizado.",
            },
            "termo-electrico-o-calentador-gas-o-aerotermia-agua": {
                "name": "Agua caliente: termo, gas o aerotermia",
                "text": "El agua caliente es una parte fija de la factura: la calculadora compara el coste total a varios años del termo eléctrico, el calentador de gas y la aerotermia con tu consumo, y da el punto en el que la opción más cara de instalar se amortiza.",
            },
            "cambiar-ventanas-aislamiento-merece-la-pena": {
                "name": "Ventanas y aislamiento",
                "text": "El ahorro real depende de la vivienda y no se puede prometer, así que la calculadora da el porcentaje mínimo de ahorro que necesitas para recuperar la obra con tu gasto en calefacción.",
            },
            "placas-solares-merece-la-pena": {
                "name": "Placas solares",
                "text": "Se amortizan antes cuanto más energía consumes en el momento en que la produces. La calculadora estima los años de amortización con tu consumo, tu producción y los excedentes.",
            },
            "punto-de-carga-casa-con-o-sin-placas": {
                "name": "Punto de carga en casa (coche eléctrico)",
                "text": "Un punto de carga en casa compensa si haces más kilómetros al año de los que lo amortizan y el kWh de casa sale más barato que el de la carga pública. La calculadora da el ahorro, los años de amortización y el efecto de tener placas.",
            },
            "cambiar-electrodomestico-antiguo-merece-la-pena": {
                "name": "Cambiar un electrodoméstico que funciona",
                "text": "Cambiar uno que funciona por uno de clase A compensa solo si el ahorro de luz cubre su precio en los años que cuentas: la calculadora te da los kWh al año que tendrías que ahorrar.",
            },
            "aire-acondicionado-inverter-o-ventilador-coste-verano": {
                "name": "Aire inverter, no inverter o ventilador",
                "text": "El inverter compensa frente a uno no inverter cuando el ahorro de energía en su vida útil supera la diferencia de precio, y eso depende de tus horas de uso. Frente a un ventilador la comparación es solo de coste: el ventilador no enfría.",
            },
            "reparar-o-comprar-electrodomestico": {
                "name": "Si se estropea: reparar o comprar",
                "text": "Cuando el aparato falla, la decisión cambia: la calculadora da el presupuesto máximo de reparación que compensa con su vida útil, el riesgo de otra avería y el consumo extra del viejo.",
            },
        },
    },
    "impuestos": {
        "path": "/impuestos/",
        "tema": "impuestos",
        "title": "Calculadoras de IRPF: renta, donativos y plan de pensiones",
        "h1": "IRPF: decide con tus números (ejercicio 2026)",
        "description": "Declaración conjunta o individual, donativos, plan de pensiones y rescate: las decisiones de IRPF del ejercicio 2026 en orden, con la normativa del BOE.",
        "kicker": "Tema · Impuestos (IRPF)",
        "nav": "Impuestos",
        "all_title": "Todas las calculadoras de impuestos",
        "baro": None,
        "fechas": [],
        "disclaimer": "Información orientativa, no constituye asesoramiento fiscal. Las cifras son las del IRPF del ejercicio 2026 (declaración de 2027) según la Ley 35/2006 y la Ley 49/2002 consultadas en el BOE el 2 de octubre de 2026, y pueden cambiar; no cubren País Vasco ni Navarra (régimen foral). Para tu caso concreto, consulta a un asesor fiscal o a la Agencia Tributaria.",
        "lead": ("<strong>Respuesta corta:</strong> en el IRPF del ejercicio 2026 (la declaración que presentarás en 2027), las decisiones que dependen de ti son pocas y conviene mirarlas en este orden: "
                 "si te conviene ser autónomo o asalariado, cuánto aportar a un plan de pensiones y cuánto donar (ambas solo cuentan para 2026 si las haces antes del 31 de diciembre de 2026), "
                 "cómo cobrar un plan en el futuro y, al presentar, si declaras en conjunta o por separado. Cada paso lleva a una calculadora con tus datos; ninguna cifra de esta página es un resultado para tu caso."),
        "groups": [
            ("Antes de dar el paso", ["autonomo-o-asalariado", "autonomo-o-sociedad-limitada", "comparar-ofertas-de-trabajo-neto-real"]),
            ("Si ya eres autónomo", ["cuota-autonomos-ingresos-reales-regularizacion"]),
            ("Si alquilas o vendes una vivienda", ["irpf-alquilar-vivienda-rendimiento-neto", "venta-vivienda-plusvalia-irpf-exencion"]),
            ("Antes del 31 de diciembre de 2026", ["plan-pensiones-o-fondo-indexado", "donativos-irpf-cuanto-desgrava-y-cuanto-donar", "compensar-perdidas-ganancias-irpf-antes-fin-de-ano", "retribucion-flexible-me-conviene"]),
            ("Si usas tu coche para trabajar", ["kilometraje-y-dietas-exentas-irpf"]),
            ("Al presentar la declaración y en el futuro", ["retencion-irpf-nomina-subir-o-no", "obligado-a-declarar-renta-dos-pagadores", "declaracion-conjunta-o-individual", "deduccion-maternidad-familia-numerosa", "traspasar-fondo-o-reembolsar-irpf", "rescate-plan-pensiones-capital-o-renta"]),
            ("Si cambia tu situación laboral", ["indemnizacion-despido-objetivo-o-improcedente-neto", "cuanto-cobro-de-paro-prestacion-desempleo", "subsidio-desempleo-cuanto-cobro-y-cuanto-dura", "capitalizar-paro-o-cobrarlo", "jubilacion-anticipada-o-demorada", "finiquito-baja-voluntaria-vacaciones-preaviso"]),
        ],
        "steps": {
            "autonomo-o-asalariado": {
                "name": "Autónomo o asalariado",
                "text": "Para cobrar lo mismo, un autónomo tiene que facturar más que el sueldo bruto de un asalariado. La calculadora da cuánto, con tu comunidad, tus gastos y las cuotas de 2026.",
            },
            "autonomo-o-sociedad-limitada": {
                "name": "Autónomo o sociedad limitada",
                "text": "Depende de tu beneficio, de la retribución que te pagues y de cuánto repartas en dividendos. La calculadora compara lo que te queda en mano como autónomo y con una SL, con el IRPF, el Impuesto sobre Sociedades y las cuotas de 2026.",
            },
            "cuota-autonomos-ingresos-reales-regularizacion": {
                "name": "Cuota de autónomo por ingresos reales",
                "text": "Cotizas por el rendimiento neto que prevés y, al cierre del año, la Seguridad Social regulariza la diferencia con el real: te devuelve o te pide. La calculadora da tu tramo y cuánto te regularizarán.",
            },
            "finiquito-baja-voluntaria-vacaciones-preaviso": {
                "name": "Finiquito al dejar un trabajo",
                "text": "Al irte cobras el sueldo del mes, las pagas pendientes y las vacaciones sin disfrutar, y si no das el preaviso del convenio te descuentan días. La calculadora da el finiquito bruto y neto con tus fechas.",
            },
            "retribucion-flexible-me-conviene": {
                "name": "Retribución flexible",
                "text": "Seguro médico, comida, transporte y guardería pagados desde la nómina dentro de los límites del artículo 42 de la Ley del IRPF te ahorran IRPF, no cotización. La calculadora da cuánto ahorras con tu tipo marginal.",
            },
            "comparar-ofertas-de-trabajo-neto-real": {
                "name": "Comparar dos ofertas de trabajo",
                "text": "Conviene la oferta que deja más neto al año después de Seguridad Social, IRPF y desplazamientos, no la de más bruto. La calculadora da la diferencia, el neto por hora y el bruto que iguala a la mejor.",
            },
            "irpf-alquilar-vivienda-rendimiento-neto": {
                "name": "IRPF por alquilar una vivienda",
                "text": "Lo que tributa es el rendimiento neto: ingresos menos gastos deducibles y, si cumples los requisitos, la reducción del 50 al 90 % del artículo 23.2 de la Ley del IRPF. La calculadora da el rendimiento neto, la base y la cuota con tus datos.",
            },
            "venta-vivienda-plusvalia-irpf-exencion": {
                "name": "Vender tu vivienda: IRPF y exención",
                "text": "La ganancia (venta menos compra, gastos y mejoras) tributa en la base del ahorro; si es tu vivienda habitual puede quedar excluida reinvirtiendo en otra o, con 65 años o más, sin reinvertir. La calculadora da la ganancia, la parte exenta y la cuota con tus datos.",
            },
            "retencion-irpf-nomina-subir-o-no": {
                "name": "Retención de IRPF en la nómina: ¿subirla o no?",
                "text": "La retención es un anticipo, no el impuesto final: si es menor que tu cuota saldrá a pagar y si es mayor te devolverán la diferencia. La calculadora compara tu retención con tu cuota estimada y te dice si te conviene pedir que te la cambien.",
            },
            "kilometraje-y-dietas-exentas-irpf": {
                "name": "Kilometraje y dietas exentas de IRPF",
                "text": "La empresa puede pagarte sin IRPF hasta 0,26 € por km y las dietas dentro de los límites del Reglamento; el exceso tributa. La calculadora compara lo que te pagan con lo que te cuesta el coche por km y da el exceso sujeto a IRPF.",
            },
            "obligado-a-declarar-renta-dos-pagadores": {
                "name": "¿Estás obligado a declarar? (dos pagadores)",
                "text": "Con dos pagadores el límite de rendimientos del trabajo que obliga a declarar es más bajo que con uno, si el segundo y siguientes superan un importe mínimo. La calculadora te dice si estás obligado con tus cifras (territorio común).",
            },
            "deduccion-maternidad-familia-numerosa": {
                "name": "Deducción por maternidad y familia numerosa",
                "text": "Con hijos menores de 3 años o familia numerosa, estas deducciones las abona Hacienda aunque superen tu cuota, y parte se puede cobrar por adelantado cada mes. La calculadora da cuánto te corresponde con tus cotizaciones y tu situación.",
            },
            "cuanto-cobro-de-paro-prestacion-desempleo": {
                "name": "Cuánto cobrarás de paro",
                "text": "La prestación es el 70 % de tu base reguladora los primeros 180 días y el 60 % después, con un máximo y un mínimo que dependen de tus hijos a cargo. La calculadora da tu cuantía mensual y el total con tus datos.",
            },
            "subsidio-desempleo-cuanto-cobro-y-cuanto-dura": {
                "name": "Subsidio por desempleo",
                "text": "Cuando se agota el paro o no llegas a cotizar lo suficiente, el subsidio puede darte un importe fijo durante un tiempo que depende de tus cotizaciones y cargas familiares. La calculadora estima cuánto cobrarías y cuánto duraría con tus datos.",
            },
            "indemnizacion-despido-objetivo-o-improcedente-neto": {
                "name": "Despido: indemnización neta",
                "text": "Tras un despido, la indemnización legal está exenta de IRPF hasta un límite y el exceso tributa. La calculadora compara aceptar la oferta con reclamar la improcedente y da el neto de cada una con tus datos.",
                "guia": "me-han-despedido-indemnizacion-paro-plazos",
            },
            "capitalizar-paro-o-cobrarlo": {
                "name": "Capitalizar el paro o cobrarlo",
                "text": "Si vas a hacerte autónomo, puedes cobrar la prestación mes a mes durante un máximo de 270 días o capitalizarla en un pago único. La calculadora compara ambas con tus meses restantes y tu inversión.",
            },
            "jubilacion-anticipada-o-demorada": {
                "name": "Jubilación anticipada o demorada",
                "text": "La edad de equilibrio depende de cuánto cobres y de cuántos años coticen. La calculadora compara tu pensión anticipada, ordinaria o demorada y la edad a partir de la cual compensa esperar.",
            },
            "plan-pensiones-o-fondo-indexado": {
                "name": "Aportar a un plan de pensiones",
                "text": "La aportación reduce la base liquidable del año, dentro de un límite, pero el plan tributa al rescatarlo: compensa si tributarás menos entonces que ahora. La calculadora lo compara con un fondo indexado.",
                "guia": "base-liquidable-tramos-irpf-2026",
            },
            "compensar-perdidas-ganancias-irpf-antes-fin-de-ano": {
                "name": "Vender con pérdidas antes de fin de año",
                "text": "Las pérdidas de ventas de acciones o fondos compensan ganancias del mismo año en la base del ahorro, pero recomprar pronto puede bloquear la pérdida. La calculadora da cuánto IRPF ahorras en 2026 con tus datos.",
            },
            "donativos-irpf-cuanto-desgrava-y-cuanto-donar": {
                "name": "Donativos",
                "text": "La deducción estatal es del 80 % de los primeros 250 € y del 40 % del resto, con un tope del 10 % de la base liquidable, y siempre te cuesta algo de dinero. La calculadora da lo que te cuesta de verdad donar.",
            },
            "declaracion-conjunta-o-individual": {
                "name": "Declaración conjunta o individual",
                "text": "La conjunta suele compensar cuando uno de los dos ingresa muy poco o nada; con dos sueldos normales suele salir mejor la individual. La calculadora compara la cuota de cada una con tus datos.",
                "guia": "renta-2027-ejercicio-2026-paso-a-paso",
            },
            "traspasar-fondo-o-reembolsar-irpf": {
                "name": "Traspasar o reembolsar un fondo",
                "text": "Traspasar un fondo de inversión a otro no tributa hasta que reembolsas, mientras que reembolsar liquida el IRPF de la ganancia ya. La calculadora da cuánto IRPF difieres y si la ventaja compensa.",
            },
            "rescate-plan-pensiones-capital-o-renta": {
                "name": "Rescatar un plan de pensiones",
                "text": "Cobrar en renta suele pagar menos IRPF que rescatar de golpe cuando el saldo es grande frente a tus otras rentas, pero no siempre. La calculadora compara capital, renta y mixto.",
            },
        },
    },
    "ahorro": {
        "path": "/ahorro/",
        "tema": "ahorro",
        "title": "Calculadoras para ahorrar: suscripciones, seguros y compras",
        "h1": "Ahorro y gastos del día a día: decide con tus números",
        "description": "Suscripciones, telefonía, seguros, compras, cuidados y estudios: las decisiones de gasto de casa en orden, con la regla de cada una y tu calculadora.",
        "kicker": "Tema · Ahorro y consumo",
        "nav": "Ahorro",
        "all_title": "Todas las calculadoras de ahorro e inversión",
        "baro": None,
        "fechas": [],
        "disclaimer": "Información orientativa, no constituye asesoramiento financiero ni de seguros. Cada regla de esta página es la que aplica su calculadora con los datos que tú introduces; ninguna cifra es un resultado para tu caso ni una recomendación de contratar o cancelar un producto concreto.",
        "lead": ("<strong>Respuesta corta:</strong> para gastar menos sin dejar de hacer lo que haces, el orden que más rinde es este: "
                 "primero los gastos que se repiten cada mes (suscripciones, fibra y móvil, seguros), porque se revisan una vez y ahorran todo el año; "
                 "después cada compra o gasto grande antes de hacerlo (cuánto puedes gastar, contado o financiar, nuevo o reacondicionado, reparar o cambiar, comprar o alquilar); "
                 "luego dónde guardar lo que ahorras y, por último, las decisiones de familia, trabajo y estudios que mueven más dinero al año. "
                 "Cada paso lleva a una calculadora con tus datos y te da el punto en el que cambia la decisión."),
        "groups": [
            ("Gastos que se repiten cada mes (revísalos una vez al año)", ["suscripciones-cuanto-gasto-al-ano", "fibra-y-movil-juntos-o-por-separado", "cambiar-de-operadora-compensa-permanencia", "marca-blanca-o-marca-ahorro-anual", "cocinar-en-casa-o-comer-fuera", "comedor-escolar-o-tupper", "gimnasio-o-entrenar-en-casa", "seguro-hogar-con-o-sin-franquicia", "seguro-salud-privado-merece-la-pena", "seguro-mascota-merece-la-pena", "adoptar-o-comprar-perro-coste-anual"]),
            ("Antes de una compra o un gasto grande", ["navidad-cuanto-gastar-sin-endeudarte", "contado-o-financiar", "portatil-o-movil-comprar-renting-o-financiar", "movil-reacondicionado-o-nuevo", "reparar-o-comprar-electrodomestico", "comprar-o-alquilar-herramienta", "impresora-tinta-o-laser-coste-por-pagina", "pc-sobremesa-o-portatil-coste-a-5-anos", "comprar-o-alquilar-trastero", "garaje-comprar-alquilar-o-aparcar-en-la-calle", "mudanza-empresa-o-furgoneta", "hotel-o-apartamento-viaje-en-grupo"]),
            ("Tu colchón y dónde guardarlo", ["fondo-de-emergencia-cuantos-meses-necesito", "deposito-letras-o-fondo-monetario"]),
            ("Familia, trabajo y estudios", ["permiso-nacimiento-cuanto-cobro-y-como-repartir", "guarderia-cuidadora-o-reducir-jornada", "excedencia-o-reduccion-jornada", "teletrabajo-o-oficina-coste-real", "vivir-cerca-del-trabajo-o-mas-barato-lejos", "residencia-o-cuidador-a-domicilio", "pension-viudedad-cuanto-cobro", "jubilacion-activa-o-dejar-de-trabajar", "universidad-publica-o-privada-o-master", "academia-idiomas-presencial-online-o-intensivo", "curso-online-bootcamp-o-fp-coste-y-retorno"]),
        ],
        "steps": {
            "vivir-cerca-del-trabajo-o-mas-barato-lejos": {
                "name": "Vivir cerca del trabajo o más barato lejos",
                "text": "Vivir lejos solo compensa si lo que ahorras en alquiler o cuota supera el desplazamiento anual y el valor de tu tiempo. La calculadora da la distancia que lo equilibra con tus datos.",
            },
            "cambiar-de-operadora-compensa-permanencia": {
                "name": "Cambiar de operadora y permanencia",
                "text": "Cambiar compensa si el ahorro mensual de la nueva oferta, multiplicado por los meses que te quedan, supera la penalización por permanencia. La calculadora te da los meses de equilibrio con tus datos.",
            },
            "impresora-tinta-o-laser-coste-por-pagina": {
                "name": "Impresora: tinta o láser",
                "text": "La que sale más barata es la de menor coste total según las páginas que imprimes al año: precio de la impresora más consumibles. La calculadora compara el coste por página de cada tecnología con tu volumen.",
            },
            "mudanza-empresa-o-furgoneta": {
                "name": "Mudanza: empresa o furgoneta",
                "text": "Con poco volumen y ayuda propia suele ganar la furgoneta; con mucho volumen, escaleras o distancia, la empresa. La calculadora compara el coste real según tus metros cúbicos, la distancia y la ayuda con la que cuentas.",
            },
            "suscripciones-cuanto-gasto-al-ano": {
                "name": "Suscripciones",
                "text": "Las candidatas a rotar o cancelar son las que te cuestan más por hora de uso que la media de las tuyas; el plan anual solo compensa con descuento y si la usas todo el año. La calculadora suma tu gasto anual y lo que ahorras rotando.",
            },
            "fibra-y-movil-juntos-o-por-separado": {
                "name": "Fibra y móvil: pack o por separado",
                "text": "El pack sale más barato mientras dura la promoción y su precio posterior no supere lo que pagarías por separado. La calculadora te da el mes en que se agota la ventaja y el riesgo de la permanencia.",
            },
            "marca-blanca-o-marca-ahorro-anual": {
                "name": "Marca blanca o de fabricante",
                "text": "Cambiar compensa si el ahorro al año (la parte de la compra que cambiarías por la diferencia de precio) supera el mínimo que te merece el cambio. La calculadora da la diferencia de precio mínima con la que compensa.",
            },
            "comedor-escolar-o-tupper": {
                "name": "Comedor escolar o tupper",
                "text": "El comedor compensa si su precio por día supera lo que cuesta preparar el tupper contando tu tiempo; si es menor, gana el comedor. La calculadora da el coste anual de cada opción con tus días lectivos y tu precio.",
            },
            "pc-sobremesa-o-portatil-coste-a-5-anos": {
                "name": "PC de sobremesa o portátil: coste a 5 años",
                "text": "Sale más barato el equipo de menor coste total a 5 años: precio inicial, consumo eléctrico y reposición o reparación. La calculadora compara sobremesa y portátil con tu uso y te da el ahorro total.",
            },
            "cocinar-en-casa-o-comer-fuera": {
                "name": "Cocinar en casa o comer fuera",
                "text": "Cocinar compensa mientras el valor que das a tu hora sea menor que el ahorro por comida dividido entre el tiempo extra que te cuesta. La calculadora da ese valor de equilibrio.",
            },
            "gimnasio-o-entrenar-en-casa": {
                "name": "Gimnasio o entrenar en casa",
                "text": "El gimnasio compensa solo si su coste por sesión que de verdad haces (cuota, matrícula y desplazamiento) es menor que el del equipo de casa menos su reventa. La calculadora da las sesiones por semana de equilibrio.",
            },
            "seguro-hogar-con-o-sin-franquicia": {
                "name": "Seguro de hogar con o sin franquicia",
                "text": "La franquicia compensa si la prima que ahorras al año supera lo que esperas pagar en siniestros pequeños; si tu colchón no cubre la franquicia, pesa más el riesgo que la media. La calculadora da la frecuencia de equilibrio.",
            },
            "seguro-salud-privado-merece-la-pena": {
                "name": "Seguro de salud privado",
                "text": "En coste compensa solo si esperas más consultas y pruebas al año que el equilibrio que sale de tu prima y tu copago; por debajo, pagar aparte cuesta menos, y la decisión también es de cobertura y acceso.",
            },
            "seguro-mascota-merece-la-pena": {
                "name": "Seguro de mascota",
                "text": "Compensa en valor esperado solo si la probabilidad de un gasto veterinario grave supera la prima dividida entre lo que cubre el seguro. La calculadora te da ese umbral y el peor escenario con carencia.",
            },
            "adoptar-o-comprar-perro-coste-anual": {
                "name": "Adoptar o comprar un perro: coste anual",
                "text": "Un perro es un gasto fijo durante años, más allá del precio de adquisición: la calculadora compara adoptar y comprar sumando lo que cuesta cada año (comida, veterinario, seguro) y te da el total a tu horizonte.",
            },
            "navidad-cuanto-gastar-sin-endeudarte": {
                "name": "Cuánto puedes gastar en Navidad y Black Friday",
                "text": "Lo que puedes gastar sin crédito es tu margen mensual libre por los meses que faltan, sin tocar el fondo de emergencia. La calculadora te da esa cifra y lo que cuesta financiar el exceso.",
                "guia": "black-friday-y-navidad-sin-deudas",
            },
            "contado-o-financiar": {
                "name": "Pagar al contado o financiar",
                "text": "Financiar solo compensa si tu dinero rinde, tras impuestos, más que la TAE real del préstamo con comisiones y seguros, y no pierdes un descuento por pagar al contado.",
            },
            "portatil-o-movil-comprar-renting-o-financiar": {
                "name": "Portátil o móvil: comprar, financiar o renting",
                "text": "Al contado cuesta menos salvo financiación sin intereses ni comisión; el renting compensa solo si su cuota es menor que el coste neto de comprar repartido entre los meses de uso. La calculadora da esa cuota de equilibrio.",
            },
            "movil-reacondicionado-o-nuevo": {
                "name": "Móvil reacondicionado o nuevo",
                "text": "El reacondicionado compensa mientras su precio quede por debajo del precio de equilibrio que sale de los años que lo usarás, la garantía y la reventa.",
            },
            "reparar-o-comprar-electrodomestico": {
                "name": "Reparar o cambiar un electrodoméstico",
                "text": "Reparar compensa mientras el presupuesto quede por debajo del importe de equilibrio que sale del precio del nuevo, la vida que le queda, el riesgo de otra avería y el consumo del viejo.",
            },
            "comprar-o-alquilar-herramienta": {
                "name": "Comprar o alquilar una herramienta",
                "text": "Comprar compensa cuando la usas más veces al año que el punto de equilibrio entre su coste total (con reventa y mantenimiento) y lo que cuesta cada alquiler.",
            },
            "comprar-o-alquilar-trastero": {
                "name": "Comprar o alquilar un trastero",
                "text": "Comprar compensa cuando el alquiler de uno equivalente supera el alquiler de equilibrio que sale del precio, los gastos anuales y el valor que tendrá al venderlo.",
            },
            "garaje-comprar-alquilar-o-aparcar-en-la-calle": {
                "name": "Garaje: comprar, alquilar o aparcar en la calle",
                "text": "Comprar plaza compensa cuando el alquiler y el aparcamiento en la calle que evitas superan el coste anual de tenerla; la calculadora da el punto de equilibrio con tus cifras.",
            },
            "hotel-o-apartamento-viaje-en-grupo": {
                "name": "Hotel o apartamento para un viaje en grupo",
                "text": "El apartamento gana cuando su noche más la comida cocinada cuesta menos que las habitaciones más comer fuera; con pocas personas o pocas noches puede ganar el hotel. La calculadora da el coste por persona y noche.",
            },
            "fondo-de-emergencia-cuantos-meses-necesito": {
                "name": "Fondo de emergencia: cuántos meses",
                "text": "Antes de invertir, el colchón: los meses de gastos recomendados suben con la inestabilidad del empleo, los ingresos variables y las personas a cargo. Es una hipótesis de trabajo, no una ley; la calculadora da la cifra y cuánto tardas en reunirla.",
            },
            "deposito-letras-o-fondo-monetario": {
                "name": "Depósito, Letras del Tesoro o fondo monetario",
                "text": "Las tres tributan igual en la base del ahorro, así que deja más neto la de mayor rendimiento a tu plazo; el fondo tiene que rendir más para compensar que no garantiza el capital. La calculadora da el neto de cada una.",
            },
            "permiso-nacimiento-cuanto-cobro-y-como-repartir": {
                "name": "Permiso por nacimiento",
                "text": "Las 19 semanas se cobran al 100 % de tu base reguladora y la prestación está exenta de IRPF. La calculadora reparte las semanas entre los dos progenitores y da lo que cobras con tus bases.",
            },
            "guarderia-cuidadora-o-reducir-jornada": {
                "name": "Guardería, cuidadora o reducir jornada",
                "text": "Reducir jornada solo compensa si el sueldo neto que pierdes es menor que lo que costaría la guardería o la cuidadora. La calculadora da el salario y el precio de equilibrio.",
            },
            "excedencia-o-reduccion-jornada": {
                "name": "Excedencia o reducción de jornada",
                "text": "Cada opción cuesta lo que dejas de cobrar menos las ayudas y los cuidados que evitas. La calculadora da el coste neto por mes y en total con tus datos.",
            },
            "teletrabajo-o-oficina-coste-real": {
                "name": "Teletrabajo u oficina",
                "text": "Teletrabajar ahorra si lo que evitas cada día en desplazamiento y comida supera el gasto extra en casa. La calculadora da el ahorro anual y la compensación mínima de la empresa.",
            },
            "jubilacion-activa-o-dejar-de-trabajar": {
                "name": "Jubilación activa: seguir trabajando y cobrar pensión",
                "text": "Con la jubilación activa cobras una parte de la pensión (45 % al inicio, hasta el 75 % según los años de demora) mientras sigues trabajando. La calculadora compara el neto de seguir trabajando con el de jubilarte del todo.",
            },
            "pension-viudedad-cuanto-cobro": {
                "name": "Pensión de viudedad",
                "text": "El porcentaje de la base reguladora (52, 60 o 70 %) depende de tu edad, tus hijos y tus ingresos, y se compara con el mínimo. La calculadora te da cuánto cobrarías con tus datos.",
            },
            "residencia-o-cuidador-a-domicilio": {
                "name": "Residencia o cuidador a domicilio",
                "text": "El cuidado en casa cuesta menos que la residencia mientras las horas diarias de cuidador queden por debajo del equilibrio que sale de tus datos. Es una comparación de coste, no una recomendación sobre el cuidado.",
            },
            "universidad-publica-o-privada-o-master": {
                "name": "Universidad pública o privada",
                "text": "La privada compensa en dinero solo si la mejora de sueldo que esperas supera su sobrecoste repartido entre tus años de trabajo; es una hipótesis, no una promesa.",
            },
            "academia-idiomas-presencial-online-o-intensivo": {
                "name": "Idiomas: academia, online o inmersión",
                "text": "Lo más barato para llegar a tu nivel depende del precio por hora y de cuánto rinde cada formato. La calculadora da el coste total y la eficacia mínima con la que compensa el online.",
            },
            "curso-online-bootcamp-o-fp-coste-y-retorno": {
                "name": "Curso, bootcamp o FP: coste y retorno",
                "text": "Formarte compensa en dinero si la mejora de sueldo que esperas recupera lo que cuesta (matrícula más ingresos que dejas de ganar) en pocos años; es una hipótesis, no una promesa.",
            },
        },
    },
}


def _n(v, dec): return f"{v:.{dec}f}".replace(".", ",")

def markers(params, live, baro_text=""):
    """Marcadores {{...}} del hub: mismos datos vivos que las guías (euribor_12m, periodo_euribor_es) + tipo fijo del BCE."""
    pm = calcs_loader.merge_market(params)
    m = {"euribor_12m": _n(pm["euribor_12m"], 3) if isinstance(pm.get("euribor_12m"), (int, float)) else "", "baro": baro_text}
    m["periodo_euribor_es"] = seo._mes(pm["periodo_euribor"]) if pm.get("periodo_euribor") else ""
    d = (live.get("datos") or {}).get("tipo_hipoteca_fija")
    if d and d.get("ok") and isinstance(d.get("valor"), (int, float)):
        m["tipo_fijo"] = _n(d["valor"], 2); m["periodo_tipo_fijo_es"] = seo._mes(d["extra"]["periodo"]); m["fecha_tipo_fijo"] = d["fecha_dato"]
    else:  # respaldo declarado en params (periodo y fuente fechados)
        m["tipo_fijo"] = _n(params["tipo_hipoteca_fija_medio"], 2); m["periodo_tipo_fijo_es"] = seo._mes(params["tipo_hipoteca_fija_periodo"]); m["fecha_tipo_fijo"] = params.get("fecha", "")
    m["fecha_euribor"] = pm.get("fecha_euribor", "")
    # coche: carburantes del día (MITECO, live.json; respaldo params con su fecha)
    def lv(i):
        x = (live.get("datos") or {}).get(i) or {}
        return x if x.get("ok") and isinstance(x.get("valor"), (int, float)) else None
    g, dsl = lv("gasolina95"), lv("diesel")
    m["gasolina"] = _n(g["valor"] if g else params["gasolina_eur_l"], 3)
    m["diesel"] = _n(dsl["valor"] if dsl else params["diesel_eur_l"], 3)
    m["fecha_carburantes"] = max([x["fecha_dato"] for x in (g, dsl) if x] or [params.get("fecha_combustibles", "")])
    m["fecha_carburantes_es"] = seo.fecha_es(m["fecha_carburantes"]) if m["fecha_carburantes"] else ""
    # energía: PVPC del día (REE, live.json) y gas TUR.2 con impuestos (params, verificado en BOE con su fecha)
    lz = lv("luz_pvpc")
    if lz: m["pvpc_hoy"] = _n(lz["valor"], 3); m["fecha_pvpc"] = lz["fecha_dato"]; m["fecha_pvpc_es"] = seo.fecha_es(lz["fecha_dato"])
    else: m["pvpc_hoy"] = _n(params["luz_2026"]["pvpc_media_ref"]["valor"], 3); m["fecha_pvpc"] = params["luz_2026"]["fecha"]; m["fecha_pvpc_es"] = "media de " + seo._mes(params["luz_2026"]["pvpc_media_ref"]["periodo"])
    m["gas_kwh"] = _n(params["gas_eur_kwh"], 3); m["fecha_gas"] = params.get("fecha_calefaccion", ""); m["periodo_gas_es"] = seo._mes(m["fecha_gas"][:7]) if m["fecha_gas"] else ""
    return m

def _fill(s, m):
    for k, v in m.items(): s = s.replace("{{" + k + "}}", v)
    return s

def themes_calcs(spec, calcs):
    return [c for c in calcs if c.get("tema") == spec["tema"]]

def guides_of(spec, guides, calcs):
    slugs = {c["slug"] for c in themes_calcs(spec, calcs)}
    return [g for g in guides if slugs & set(g.get("calcs", []))]

def eligible(calcs, guides):
    """Hubs que cumplen el disparador (>= MIN_PAGES páginas del tema entre calculadoras y guías)."""
    return {k: s for k, s in HUBS.items() if len(themes_calcs(s, calcs)) + len(guides_of(s, guides, calcs)) >= MIN_PAGES}

def page(key, spec, calcs, guides, params, live, card, base, baro_texts=(), tablas_items=()):
    """-> (body_html, jsonld, lastmod). Pasos en orden de decisión, 1-2 frases, dato vivo con fecha, calculadora y guía de cada paso."""
    baro = spec.get("baro")  # (ancla, índice de la frase de barometro.answers_text, descripción) o None
    baro_text = baro_texts[baro[1]] if baro and len(baro_texts) > baro[1] else ""
    m = markers(params, live, baro_text); by = {c["slug"]: c for c in calcs}; gb = {g["slug"]: g for g in guides}
    n = 0; secs = []; items = []
    for gname, slugs in spec["groups"]:
        secs.append(f"<h2>{html.escape(gname)}</h2>")
        for s in slugs:
            if s not in by: continue
            n += 1; st = spec["steps"][s]; c = by[s]
            datos = st.get("datos")
            dtxt = ""
            if datos:
                fk, flab = st.get("fecha", ("fecha_euribor", "Euríbor"))
                fch = f'<time datetime="{m[fk]}">{seo.fecha_es(m[fk])}</time>' if m.get(fk) else ""
                dtxt = f'<p class="note">{_fill(datos, m)}' + (f" {flab}: dato del {fch}." if fch else "") + "</p>"
            g = gb.get(st.get("guia"))
            glink = f' <a href="/guias/{g["slug"]}/">Guía: {html.escape(g["h1"])}</a>' if g else ""
            secs.append(f'<section class="box" id="paso-{n}"><h3>Paso {n}: {html.escape(st["name"])}</h3><p>{_fill(st["text"], m)}</p>{dtxt}'
                        f'<p><a class="btn2" href="/decidir/{s}/">{html.escape(c["h1"])}</a>{glink}</p></section>')
            items.append((st["name"], f'/decidir/{s}/'))
    for g in guides_of(spec, guides, calcs): items.append((g["h1"], f'/guias/{g["slug"]}/'))
    if baro: items.append(("Barómetro Entre Muchos", "/barometro/"))
    for p, h1, _ in tablas_items: items.append((h1, p))  # c36: tablas oficiales 2026 (tablas.hub_items)
    mod = seo.lastmod("hubs.py", extra=[m.get(k, "") for k in spec.get("fechas", [])] + [g["modified"] for g in guides_of(spec, guides, calcs)])
    pub = seo.published("hubs.py")
    gl = "".join(f'<li><a href="/guias/{g["slug"]}/">{g["h1"]}</a> <span class="note">{g["description"]}</span></li>' for g in guides_of(spec, guides, calcs))
    bl = f'<li><a href="{baro[0]}">Barómetro Entre Muchos</a> <span class="note">{baro[2]}</span></li>' if baro else ""
    bl += "".join(f'<li><a href="{p}">{html.escape(h1)}</a> <span class="note">{html.escape(d)}</span></li>' for p, h1, d in tablas_items)
    body = f"""<article class="guide hub">
<p class="kicker">{spec["kicker"]}</p>
<h1>{spec["h1"]}</h1>
<p class="byline note">Por {AUTHOR} · Publicado el <time datetime="{pub}">{seo.fecha_es(pub)}</time> · Actualizado el <time datetime="{mod}">{seo.fecha_es(mod)}</time></p>
<p class="lead">{_fill(spec["lead"], m)}</p>
{"".join(secs)}
<h2>Guías y datos propios</h2>
<ul class="guides">{gl}{bl}</ul>
<h2>{spec["all_title"]}</h2>
<ul class="cards">{"".join(card(c) for c in themes_calcs(spec, calcs))}</ul>
<p class="disclaimer">{spec["disclaimer"]} Lee cómo trabajamos en <a href="/como-funciona/">Cómo funciona</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""
    url = base + spec["path"]
    org = seo.org(base)
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": spec["h1"], "description": spec["description"], "url": url,
           "inLanguage": "es-ES", "datePublished": pub, "dateModified": mod, "isPartOf": {"@id": base + "/#website"},
           "author": {"@type": "Organization", "name": AUTHOR, "url": base + "/como-funciona/"}, "publisher": org,
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListOrder": "https://schema.org/ItemListOrderAscending",
                          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": nm, "url": base + p} for i, (nm, p) in enumerate(items)]}},
          seo.breadcrumbs(base, [("Inicio", "/"), (spec["h1"], None)])]
    return body, ld, mod

# ---------- enlaces desde otras páginas ----------
def calc_link(slug, calcs, active):
    """Párrafo «forma parte del mapa de …» para calculadoras del hub."""
    for k, s in active.items():
        if any(slug in sl for _, sl in s["groups"]):
            return f'<p class="note hub-link">Esta decisión es un paso del mapa <a href="{s["path"]}">{html.escape(s["h1"])}</a>, en orden.</p>'
    return ""

def guide_link(g, calcs, guides, active):
    for k, s in active.items():
        if g in guides_of(s, guides, calcs):
            return f'<p class="note hub-link">Más sobre el tema: <a href="{s["path"]}">{html.escape(s["h1"])}</a> (calculadoras y guías en orden de decisión).</p>'
    return ""

def home_link(active):
    if len(active) == 1:
        s = next(iter(active.values()))
        return f'<p class="note hub-link"><strong>Temas:</strong> <a href="{s["path"]}">{html.escape(s["h1"])}</a> · {html.escape(s["description"])}</p>'
    return ('<p class="note hub-link"><strong>Mapas por tema, en orden de decisión:</strong> '
            + " · ".join(f'<a href="{s["path"]}">{html.escape(s["nav"])}</a>' for s in active.values()) + "</p>") if active else ""

def footer_links(active, skip=("hipoteca",)):
    """Enlaces del pie para hubs que aún no están en templates/base.html (el de hipoteca ya lo está)."""
    return "".join(f'<a href="{s["path"]}">{html.escape(s["nav"])}</a>' for k, s in active.items() if k not in skip)

def llms_lines(active, base):
    return [f"- [{s['h1']}]({base}{s['path']}): {s['description']}" for s in active.values()]
