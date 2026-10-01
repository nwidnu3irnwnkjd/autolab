# Verificación fiscal independiente · plan-pensiones-o-fondo-indexado · 2026-10-02 (Opus)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (cálculo correcto: 0 discrepancias en 11 escenarios + 500 aleatorios; 3 cambios de texto/aviso obligatorios por norma, ninguno cambia fórmulas).
Fuentes leídas por mí hoy (curl boe.es, consolidado): Ley 35/2006 arts. 17.2.a.3.ª, 51.6-8, 52.1-2, 56, 63.1, 66.1, 76, 94.1.a, DT 12.ª; RDL 1/2002 arts. 5.3, 8.8, 36.5; DLeg 1/2010 Madrid art. 1. Oráculo propio: ops/verif/plan-pensiones-o-fondo-indexado.py (escalas estatal y ahorro transcritas del BOE, no de params).

## 1. Tablas (muestreo)
- Escala estatal art. 63.1 (9,5/12/15/18,5/22,5/24,5; 12.450/20.200/35.200/60.000/300.000): coincide con params y JS.
- Ahorro arts. 66.1 + 76 (cada mitad 9,5/10,5/11,5/13,5/15; 6.000/50.000/200.000/300.000 → 19-30 %): coincide.
- Madrid art. 1 DLeg 1/2010 (8,5/10,7/12,8/17,4/20,5; 13.362,22/19.004,63/35.425,68/57.320,40): coincide. pensiones_2026 (1.500 €, 30 %, 8.500, 4.250, 10 años): coincide con art. 52.1 y TRLPFP 5.3/8.8.

## 2. Escenarios (JS vs oráculo, tol. 1 € / 0,02 pp; todos OK)
| # | Escenario | Aport. efect. | Ahorro IRPF/año | Plan (1 vez) | Fondo | Dif. | Dif. 10 pagos | T. eq. |
|---|---|---|---|---|---|---|---|---|
| 1 | Defecto Madrid 35.000, 25 a | 1.500 | 417,00 | 49.491,28 | 57.862,54 | −8.371,26 | −5.824,57 | 25,09 % |
| 2 | Aporta 5.000 (> 1.500), 45.000 | 1.500 | 538,50 | 53.283,97 | 57.862,54 | −4.578,57 | −1.561,11 | 33,13 % |
| 3 | Límite 30 %: renta 3.000, aporta 2.000, rescate ×2 | 900 | 0,00 | 8.412,78 | 10.711,23 | −2.298,45 | −2.103,35 | −0,79 % |
| 4 | Autónomo plan simplificado 5.750, Valencia 40.000 | 1.500 | 532,50 | 51.165,91 | 57.862,54 | −6.696,63 | −2.431,37 | 32,73 % |
| 5 | Rescate ×0,5, 60.000, com. 0,5/0,5, 20 a | 1.500 | 585,00 | 47.583,40 | 45.268,02 | +2.315,38 | +7.311,42 | 42,67 % |
| 6 | Horizonte 1 año, CyL 45.000 | 1.500 | 555,00 | 1.528,35 | 1.546,17 | −17,82 | −17,82 | 35,85 % |
| 7 | Rescate ×2, Cataluña 60.000, 30 a | 1.500 | 600,00 | 68.385,39 | 76.296,01 | −7.910,62 | −7.725,58 | 36,49 % |
| 8 | Extremadura 20.000, rescate ×0,5, 30 a | 1.500 | 326,25 | 62.113,38 | 76.296,01 | −14.182,63 | −1.519,64 | 18,18 % |
| 9 | La Rioja 150.000, 6 %/0,3/0,1, 15 a | 1.500 | 742,50 | 34.224,67 | 33.832,85 | +391,82 | +391,82 | 50,59 % |
| 10 | Rentab. −2 %, Galicia 30.000, 10 a | 1.500 | 448,50 | 12.465,80 | 13.299,68 | −833,88 | −306,44 | 27,49 % |
| 11 | Renta 8.000, rescate ×0,5 (b0 = 4.000 < mínimo) | 1.500 | 270,00 | 95.111,70 | 104.744,24 | −9.632,54 | +14.303,39 | 28,47 % |
Barrido 500 casos aleatorios (15 CCAA, 1-45 años, rentab. −3/9 %): 0 discrepancias.

## 3. Discrepancias con la norma
D1 (caso 2, legal): aportar > 1.500 € a un plan individual **no está permitido** (TRLPFP art. 5.3.a); el exceso se sanciona con multa del 50 % salvo que se retire antes del 30 de junio del año siguiente (art. 36.5). El aviso del JS y el HTML dicen solo «el exceso no desgrava/no reduce tu base este año»: engañoso.
D2 (caso 3): el exceso por el límite del 30 % (o por insuficiencia de base) se puede reducir en los **5 ejercicios siguientes** (art. 52.2); el exceso sobre 1.500 € no. El texto no lo dice.
D3 (FAQ 2 y HTML «Límite de aportación»): los incrementos no se suman sin más: entre 8.500 € (empresa o aportaciones del trabajador al mismo plan de empleo, con el cuadro de coeficientes) y 4.250 € (autónomos) el **incremento conjunto máximo es 8.500 €** (art. 52.1, último párrafo) → tope total 10.000 €, y siempre con el 30 %. La FAQ «se suman hasta 8.500 € más … y 4.250 € más» sugiere 12.750 €.
D4 (caso 11, nicho < 1 %): si la renta del año de reembolso (renta × factor) es menor que el mínimo personal, el sobrante del mínimo reduce la base del ahorro (art. 56.2); el JS no lo aplica y sobrevalora el impuesto del fondo (333 € en el caso 11). No cambia ganador. Declarar como límite.
D5 (art. 94.1.a): el diferimiento por traspaso NO aplica a fondos cotizados (ETF). «Los traspasos entre fondos no tributan» debe matizarlo.

## 4. Cambios requeridos (obligatorios: 1-4; recomendados: 5-7)
1. calcs/plan-pensiones-o-fondo-indexado.js, nota `r.excede`: distinguir (a) aportación > límite del 30 % pero ≤ 1.500 €: «el exceso no reduce la base este año, pero puedes reducirlo en los 5 años siguientes (art. 52.2)»; (b) aportación > 1.500 €: «la ley no permite aportar más de 1.500 € al año a planes individuales (art. 5.3 TRLPFP); el exceso debe retirarse antes del 30 de junio del año siguiente o se multa con el 50 % (art. 36.5); solo con aportaciones de empresa o planes de autónomos el límite sube (no modelado)». Alternativa válida: max = 1.500 en el input y quitar la rama (b).
2. content/…html, «Límite de aportación deducible»: sustituir «el exceso no desgrava este año» por el texto de 1 (arrastre 5 años y prohibición > 1.500 €); y «incrementos de hasta 8.500 € y 4.250 €» por «incremento de hasta 8.500 € (empresa) o 4.250 € (autónomos), como máximo 8.500 € entre los dos (10.000 € en total) y siempre con el tope del 30 %».
3. calcs/…json, FAQ 2: mismo matiz que 2 (tope conjunto 8.500 €, total 10.000 €; los 8.500 € incluyen aportaciones del propio trabajador al plan de empleo según el cuadro del art. 52.1.1.º) + frase del arrastre 5 años. Campo `sources`: añadir «art. 52.2 (arrastre) y art. 5.3 y 36.5 TRLPFP».
4. calcs/…json FAQ 5 y content/…html «Qué estás comparando»: «Los traspasos entre fondos de inversión no tributan (salvo ETF/fondos cotizados, art. 94.1.a)».
5. content/…html «Supuestos»: añadir «Si tus rentas del año de reembolso fueran inferiores al mínimo personal, el sobrante reduce el impuesto del fondo (art. 56.2); no se modela» y «El límite del 30 % se calcula sobre la cifra que introduces; la ley lo calcula sobre rendimientos netos antes de la reducción del art. 20, que no se modela (afecta a rentas < 19.747,5 €)».
6. calcs/…json FAQ 3: la reducción del 40 % (DT 12.ª) exige además cobrar el capital en el año de la contingencia o en los dos siguientes (apdo. 4).
7. content/…html «Valora la liquidez»: «o jubilación» → «o al llegar una contingencia (jubilación, incapacidad, dependencia o fallecimiento)»; el supuesto de 10 años en planes de empleo solo si lo prevén sus especificaciones (art. 8.8).
Casos nuevos para test.json: escenarios 4 (aport. 5.750 → efectiva 1.500, dif −6.696,63), 8 (dif −14.182,63, dif10 −1.519,64) y 9 (dif +391,82; tipoEquilibrio 50,59).

## 5. Supuestos
Aceptables y declarados: aportación a principio de año; devolución al cierre y reinvertida en el fondo (declarado, con «llega meses después»); rentab. neta = bruta − comisión; otras rentas del rescate = renta × {0,5, 1, 2}; 10 pagos sin rentabilidad en el cobro (conservador para el plan); solo mínimo personal; escalas 2026 constantes; tipo de equilibrio como tipo MEDIO (el texto lo llama siempre «tipo medio»); comparar solo la parte deducible; hipótesis por defecto no oficiales. Rescate como rendimiento del trabajo en base general en el año del cobro, capital o renta: correcto (art. 17.2.a.3.ª). Reducción en base general (arts. 50-51): correcta.
Erróneos/engañosos: solo el tratamiento textual de la aportación > 1.500 € (D1) y la suma de incrementos (D3). Texto ≤ cálculo: lead, veredicto y FAQ 1/3 respaldados (con comisiones 1/0,2 el rescate de una vez pierde en los 6 combos renta×factor probados; con comisiones iguales y rentas menores al rescatar gana el plan, coherente con «depende»). Liquidez, comisiones y «hipótesis, no previsión» presentes; no se prometen rentabilidades.
Re-verificación (Sonnet): `python3 ops/verif/plan-pensiones-o-fondo-indexado.py` (sale 0) y releer solo los textos de los cambios 1-4.
