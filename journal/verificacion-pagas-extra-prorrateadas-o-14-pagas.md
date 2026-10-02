# Verificación fiscal · pagas-extra-prorrateadas-o-14-pagas · 2026-10-02 (Verificador, Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 0 · R 0 · S 1 (no crítico) · otros 2 (ninguno cambia el neto ni el veredicto)

## Paso 0 · interpretación propia vs bloque INTERPRETACION: coincide, con un matiz en la IT
Normas leídas hoy en el BOE consolidado:
- ET 31 (literal): 2 gratificaciones, una en Navidad; la cuantía la fija el convenio; «podrá acordarse en convenio colectivo» el prorrateo en 12. Las 3 o 4 pagas, las fechas y el devengo son del convenio, no de la ley: así lo trata la página.
- LGSS 147.1 (vigente desde 1/1/2023): «Las percepciones de vencimiento superior al mensual se prorratearán a lo largo de los doce meses del año». La base es B/12 en las dos formas, el mes de la paga no cotiza aparte y las pagas pendientes del finiquito tampoco: ya cotizaron. Correcto.
- RIRPF 80.1, 83.2 regla 1.ª y 86.1: un solo tipo anual sobre todo lo que «vaya normalmente a percibir» en el año. Mismo tipo y misma retención anual. Correcto. Art. 87 declarado.
- LGSS 270.1: promedio de la base cotizada en los últimos 180 días = 6 × B/12 / 180 = B/360 en las dos formas (66,67 €). Correcto.
- Decreto 1646/1972 art. 13 (lo cito porque la página lo cita). Apdo. 1: la base del mes anterior va «excluidos … los conceptos remuneratorios comprendidos en el número cuatro». Apdo. 4: las pagas extra entran por el «promedio de la base de cotización correspondiente a tales conceptos durante los doce meses». La IT **no** es base/30 tal cual: es sueldo sin pagas/30 + promedio de las pagas. Si el promedio se divide entre 365 (lo habitual en nómina), el ejemplo da 1.714,29/30 + 3.428,57/365 = **66,54 €**; si es el promedio mensual entre 30, da 66,67 €. En las dos formas sale **igual**, porque el art. 13.4 se aplica a las pagas extraordinarias estén o no prorrateadas. Se mantiene «la misma en los dos casos», pero la cifra de 66,67 € solo está demostrada para el paro (cambio 1).
- Oráculo re-ejecutado: 933 casos, 0 discrepancias; máx. |dif neto anual| 0,00. El máximo de 89,68 € de dif. devengado sale con brutos altos (escala con B): la página da 16,67 € condicionado a «con 24.000 € y 4 pagas», así que está bien.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | S (no crítico: no cambia el ganador) | json lead («la base de la baja médica y del paro es la misma … (66,67 € al día en el ejemplo)»), json veredicto («La base de la baja médica y del paro no cambia (66,67 € al día)»), json faq[3], html «Baja médica y paro» («la de un día de baja o de paro también: 66,67 €»), js filas «Base diaria para baja médica y paro» (escenarios 1 y 2) | Dar la cifra solo para el paro y decir que la IT es igual en las dos formas sin dar su cifra. Por ejemplo: «La base del paro es la misma (66,67 € al día en el ejemplo, art. 270.1 LGSS) y la de la baja médica también es igual en las dos formas, porque las pagas extra entran por su promedio de 12 meses (art. 13.4 del Decreto 1646/1972), estén o no prorrateadas». Fila del JS: «Base diaria del paro (la de la baja es igual en las dos formas)» | Art. 13.1 y 13.4: la base de IT excluye las pagas de la base mensual y las suma por su promedio anual, así que no es base/30 (66,54 € con el promedio entre 365) |
| 2 | otros (absoluto, patrón 1) | html lead «El prorrateo solo existe si lo prevé tu convenio colectivo»; json lead «El prorrateo solo existe si tu convenio colectivo lo prevé»; js nota «el prorrateo solo existe si lo prevé tu convenio colectivo» | → «La ley prevé el prorrateo cuando lo acuerda el convenio colectivo (art. 31 ET): mira el tuyo antes de pedirlo» | El literal es «podrá acordarse en convenio colectivo». «Solo existe» afirma algo sobre la práctica (pactos individuales) que ni la página ni la norma citada demuestran |
| 3 | otros (absoluto, patrón 1) | html «Qué no incluye», línea «El IRPF final»: «es el mismo en las dos formas porque lo cobrado en el año es el mismo» | → «si trabajas todo el año es el mismo en las dos formas, porque lo cobrado en el año es el mismo; si te vas a mitad de año, lo devengado difiere unos euros (ver arriba)» | Con baja, el propio cálculo da una diferencia de devengado de hasta 16,67 € (24.000 €, 4 pagas) y de 89,68 € en el barrido |

## Texto ≤ cálculo (lo demás está demostrado)
Lead/FAQ 1 (18.840 = 18.840; 3.600; 1.560; 1.570 frente a 1.327,14; 242,86) · sí, con la condición «si trabajas todo el año» · — | Cotización igual y «el mes de la paga no cotiza aparte» · sí (147.1) | Retención anual igual · sí (83.2 regla 1.ª + 80.1) | Finiquito: 1.145,96 € brutos y 974,07 € netos, «123 de 184 días» · sí (supuesto de devengo declarado; neto sin cotización por 147.1) | «casi igual, no idéntico» en lo devengado · sí | Territorial (forales, Ceuta y Melilla: pon tu tipo) · sí | Supuestos de calendario y devengo · declarados en «Qué no incluye» y en la nota del resultado.
Citas por muestreo, todas literales correctas: art. 31 ET; 147.1 LGSS; 270.1 LGSS; 83.2 regla 1.ª, 86.1 («se expresará con dos decimales», del tipo) y 80.1 RIRPF; Decreto 1646/1972 art. 13 (con el alcance que corrige el cambio 1). Las redacciones vigentes coinciden con las de la pre-verificación (a147 en vigor desde 1/1/2023; a270 desde 1/1/2023).
T: no hay transitorias que toquen los arts. centrales. 8: los bloqueos (bruto 0, 29-feb, 31-abr, n ∉ {2,3,4}) están en el JS y en los tests. R: el RDL 26/2026 está derogado y no se cita. Bien.

## Hallazgo ajeno de la pre-verificación (R58.3): falso
El 270.2 vigente dice 60 % desde el día 181 (Ley 31/2022 DF 25.8, en vigor desde 1/1/2023). El 50 % es el texto original, que la API devuelve como primera `<version>`. Detalle en journal/verificacion-paro-pct-r58-3.md. La línea 16 de journal/preverif-pagas-extra-prorrateadas-o-14-pagas.md («70 %/50 %») debe decir 70 %/60 %.

## Casos nuevos para test.json
- 15 pagas, baja 30-abr: la paga de abril (periodo de ene a abr, que cierra en el mes de la baja) va entera al finiquito (pendiente14 = pagaExtra en el periodo 1 + 0 en los demás).
- 14 pagas, bruto 61.214,40, baja 31-dic: cotización topada y pendiente = paga de Navidad entera.

Re-verificación (Sonnet): ejecutar ops/verif/pagas-extra-prorrateadas-o-14-pagas_oraculo.py y releer solo las frases de los cambios 1 a 3. Opus no hace falta: las cifras no cambian (el cambio 1 es de texto o de etiqueta).
