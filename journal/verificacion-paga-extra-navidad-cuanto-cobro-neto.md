# Verificación fiscal · paga-extra-navidad-cuanto-cobro-neto · 2026-10-02 (Verificador, Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 1 · R 0 · S 1 · otros 3 (ninguno crítico: no cambian cifras ni veredicto)

## Paso 0 · interpretación propia vs bloque INTERPRETACION: coincide
- ET 31 (literal, 2 párrafos, vigente 13-11-2015): 2 gratificaciones, una «con ocasión de las fiestas de Navidad»; cuantía por convenio; prorrateo en 12 por convenio. Proporcionalidad, devengo y forma de contar NO están en la ley → supuesto/input, bien tratado.
- LGSS 147.1 (vig. 1-1-2023): percepciones de vencimiento superior al mensual se prorratean en 12 meses → sin cotización extra en el mes de la paga. Correcto. 19 bis (vig. 1-1-2025) solo afecta por encima de base máxima: declarado.
- RIRPF 80.1.1.º (vig. 7-12-2023) + 83.2.1.ª (cuantía total = todo lo que «vaya normalmente a percibir … en el año natural», pagas incluidas) + 86.1: un único tipo anual que se aplica también a la paga. No hay procedimiento propio para pagas. Lo único que mueve el neto es la regularización del art. 87 (apdos. 3 y 4: el nuevo tipo se aplica desde la variación a los pagos que quedan, y la diferencia se reparte entre menos pagos). Está declarado, pero corto (cambio 4).
- Oráculo re-ejecutado: 828 casos, 0 discrepancias. Bordes de fechas (1-jul, 2-jul, 30-jun, 31-dic, 1-ene, 29-feb, 31-abr, alta antes del periodo, baja antes del periodo = 0) correctos en JS y oráculo; cifras del ejemplo comprobadas a mano (122/184 → 994,57; 149,19; 845,38; 64,65 → 780,73).

## (a) Cotización 6,5 %: verificada hoy en la Orden PJC/297/2026 (BOE-A-2026-7296)
art. 4.a CC 4,70 · art. 33.2.a.1.º desempleo indefinido 1,55 (temporal 1,60) · MEI 0,15 · FP 0,10 (fiscal-fuentes 5.3) = 6,50 %. Bien. La pre-verificación dice «temporal 6,6 %, −0,1 pt»: es 6,55 % (−0,05 pt); en la página no aparece, no hay que cambiar nada. Recomendado (no obligatorio): en params retencion_irpf_nomina_2026 citar «Orden PJC/297/2026» en vez de «Orden de cotización 2026 y RDL 3/2026».
## (b) Días naturales y devengo como supuestos del convenio: bien declarados (lead, «Cómo se calcula», «Qué fija el convenio», nota del resultado, labels «según convenio»; el día de entrada o de salida se cuenta como trabajado). Falta solo el cambio 2.
## (d) Bordes: correctos. Recomendado: baja el 31-dic da escenario 1 («cobras la paga entera»), sin decir que va en el finiquito; añadir la frase del escenario 5 cuando situacion=baja.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | otros (cita, patrón 4) | content .html lead; json veredicto | La cita «(art. 31 ET)» va detrás de una frase que incluye la parte proporcional y el neto sin cotización. Repartir: «la cuantía y el devengo los fija el convenio (art. 31 ET); sin cotización aparte (art. 147.1 LGSS)», y presentar la parte proporcional como criterio del convenio, no del art. 31 | El art. 31 no recoge la proporcionalidad ni el neto |
| 2 | S (no crítico) | html «Qué fija el convenio»; json faq5 | «El mes de cobro … tampoco están en la ley» y la FAQ 5 «El convenio (art. 31 ET): la cuantía, el mes de cobro y el periodo de devengo» → «La ley dice que una se paga con ocasión de las fiestas de Navidad y deja al convenio su cuantía (art. 31); la fecha exacta y el periodo de devengo los fija el convenio, no el art. 31» | Literal del art. 31: Navidad está en la ley; el convenio fija el mes solo de la *otra* paga. El devengo no aparece en el art. 31 |
| 3 | otros (absoluto, patrón 1) | json lead («ya se cotizó repartida en las doce nóminas»); js escenario 1 («repartida en las doce nóminas del año») | → «repartida en tus nóminas mensuales» (como ya dice el html) | Con alta el 1-jul y devengo semestral la paga es entera pero solo hay 6 nóminas (test «alta 1-jul = entera») |
| 4 | N (no crítico) | html «Qué no incluye» (línea del art. 87); json input ret (ayuda) | Sustituir «si tu pagador la cambia antes de diciembre, el tipo de la paga será el nuevo» por: «si tu pagador regulariza el tipo (art. 87: subida de sueldo, cambio de hijos…), el nuevo tipo se aplica desde ese momento a lo que queda por cobrar, también a la nómina de diciembre con la paga, y como el ajuste se reparte entre menos pagos puede subir o bajar bastante». Ayuda del input: «pon el de la nómina del mes en que cobras la paga, si ya lo sabes» | RIRPF 87.3 y 87.4 (literal: «se aplicarán a partir de la fecha en que se produzcan las variaciones»). Es lo único que hace que el tipo de la paga no sea el de la nómina anterior |
| 5 | otros (cita, patrón 4) | html «Retención de IRPF» | «con dos decimales (art. 86.1)» → «el tipo, expresado con dos decimales (art. 86.1)» | El 86.1 habla del tipo, no del importe retenido |

## Texto ≤ cálculo (lo demás está demostrado)
Ejemplo del lead/FAQ 1-2 (122/184, 66,3 %, 994,57/845,38, 1.275) · sí · — | FAQ 2 «el tipo del año se fija con todas tus retribuciones previstas» · sí (RIRPF 83.2.1.ª; añadir la cita es opcional) | FAQ 3 · sí (147.1) | FAQ 4 «normalmente en el finiquito, según convenio» + 49.2 · sí (literal comprobado; art. 49 vigente desde 1-5-2025 por la Ley 2/2025, apdo. 2 sin cambios: la pre-verificación pone 13-11-2015) | «aproximación al 6,5 % … sin tope» · sí, declarado | territorial (forales, Ceuta y Melilla: pon tu tipo) · sí.
Citas por muestreo: art. 31, 147.1, 86.1, 80.1, 49.2, 87, 19 bis: literales coinciden (salvo el alcance de los cambios 1, 2 y 5).

## Casos nuevos para test.json
- baja 31-dic, devengo anual → escenario 1, 365/365 (y escenario 5 si se aplica el cambio recomendado de (d)).
- alta 1-mar, devengo semestral → entera 184/184 (alta antes del periodo semestral).
- todo el periodo, anual, diassin 365 → escenario 4, 0 días.

Re-verificación (Sonnet): ejecutar ops/verif/paga-extra-navidad-cuanto-cobro-neto_oraculo.py y releer solo las frases de los cambios 1 a 5. Opus no hace falta: no cambia la interpretación.
