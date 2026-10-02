# Verificación fiscal/legal · aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad · 2026-10-02 (Verificador Opus, v3.4)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 1 · N 1 · R 1 · S 1 (crítico) · otros 1 (absoluto) · cambio obligatorio en otras calculadoras: subsidio (solo texto); paro: ninguno.
Norma leída hoy (API BOE consolidado BOE-A-2015-11724): arts. 271 (vig. 4-2-2026), 272 (1-5-2025), 275, 280, 282 (23-5-2024), DA 59.ª (bloque da-35, única versión, vig. 1-11-2024); LISOS (BOE-A-2000-15060) arts. 25.4 y 47.1 (vig. 1-11-2024). RDL 26/2026 (BOE-A-2026-20266, vivienda): no cita la LGSS ni el desempleo (grep sobre el texto completo). Oráculo re-ejecutado: 25 fijos + 700 aleatorios, 0 discrepancias, estructura OK.

## Paso 0 · mi interpretación frente al bloque INTERPRETACION
- A (solo prestación), B paro (282.2: deducción proporcional, consume días), C (271.1.d/271.2 suspende sin consumir; ≥ 12 meses 272.1.c extingue), subsidio (282.3: tabla 80/75/70/60 … 20/15/10/5 por trimestre del subsidio y jornada ≥75 / 50-75 / <50, máx. 180 días que consumen subsidio, tope en días restantes): COINCIDE. Columnas y trimestres del oráculo = literal del 282.3. IPREM 600 € correcto.
- DIFIERE en dos puntos: (a) la DA 59.ª.4 no es un «límite» marginal sino que cambia la tabla del CAE del subsidio para quien agotó un paro > 12 meses reconocido desde 1-4-2025; (b) la opción A («no aceptar») no siempre existe sin coste: si la oferta llega del servicio público de empleo o de una agencia colaboradora, rechazarla es infracción grave.

## DA 59.ª: contenido exacto (respuesta al hallazgo del Constructor)
- 59.1: paro NACIDO desde 1-4-2025 con periodo reconocido > 12 meses, devengados 9 meses: compatible con trabajo a tiempo completo Y parcial «en la misma forma» que el CAE del subsidio (sustituye la deducción del 282.2 desde el 10.º mes; automática, con desistimiento en 15 días hábiles que suspende y cierra el 282.2). 59.2: nacido antes de 1-4-2025: solo tiempo completo y a solicitud. 59.3: tabla propia por mes (10.º-15.º 80/75/70/60; 16-18 60/50/45/40; 19-21 40/35/30/25; 22-24 30/25/20/15; duración 30/60/90/180 según mes de inicio). 59.5: incompatible si salario bruto > 375 % IPREM (2.250 €), «en la forma que se establezca reglamentariamente». 59.4: subsidio (274.1.a o 280) tras agotar un paro > 12 meses reconocido desde 1-4-2025: el CAE se calcula con la tabla del 282.3 tomando como referencia los meses transcurridos desde el 13.º mes de prestación.
- NO cambia la cuantía ni la duración del paro (270, 269) ni del subsidio (278, 277): solo la compatibilidad con trabajo. Bloqueo 5 de la calculadora: correcto y conservador (bloquea también paros anteriores a 1-4-2025 con parcial, que siguen en el 282.2: aceptable).

## Cambios obligatorios (esta calculadora)
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | S crítico | calcs .json/.js + content | Subsidio: añadir pregunta «¿tu subsidio viene de agotar un paro de más de 12 meses reconocido desde el 1-4-2025?» (o meses del paro agotado). Si sí: BLOQUEAR con mensaje (o modelar trimestre = min(5, ceil((P−12+m)/3))); hoy solo es una nota y el CAE sale hasta 4 veces mayor (480 € vs 120 € a jornada completa con paro de 24 meses) y puede cambiar el ganador | DA 59.ª.4. Afecta a una parte creciente de los subsidios de 2026 (los < 45 sin cargas necesitan ≥ 360 días de paro) |
| 2 | 8 | content (veredicto de A, FAQ 5, ejemplo sueldo 300 €) + JS texto del ganador A | Condicionar «no aceptar / seguir solo con el paro o subsidio»: solo sin coste si la oferta no llega del SEPE/servicio autonómico o agencia colaboradora como empleo adecuado; si llega así, rechazarla sin causa justificada es infracción grave con pérdida de la prestación (escala desde 3 meses) | LISOS 25.4.a y 47.1.b |
| 3 | otros (absoluto) | json .veredicto, FAQ 1, página «Cuándo la compatibilidad no existe» y lead | «A jornada completa no hay compatibilidad / el paro no se puede compatibilizar» → añadir «salvo un paro de más de 12 meses desde su 10.º mes (DA 59.ª)» | DA 59.ª.1-2 |
| 4 | R | content (párrafo DA 59.ª) y mensaje de bloqueo 5 | Precisar: se aplica a paros nacidos desde el 1-4-2025 (antes: solo jornada completa y a solicitud); desde el 10.º mes también el trabajo parcial pasa a CAE (no deducción proporcional), y es automático salvo desistimiento | DA 59.ª.1-2 |
| 5 | N | content «Supuestos» / nota | Declarar el tope de salario bruto del 375 % del IPREM (2.250 €/mes) para la compatibilidad del paro, pendiente de desarrollo reglamentario | DA 59.ª.5 |

## Supuestos S del preverif (revisados)
- El paro sigue consumiendo días al compatibilizar: DEFENDIBLE y confirmado por el SEPE («each day you receive is one day consumed», FAQ compatibilidad tiempo parcial). OK.
- Trabajo parcial sin pedir compatibilidad suspende: defendible (282.2 lo declara incompatible → 271.1.d). OK.
- Parcial ≥ 12 meses mantiene compatibilidad: defendible (282.2 admite solicitud hasta 12 meses tras el inicio, lo que presupone contratos largos) y avisado. OK.
- Deducción = % de jornada sobre el importe mensual: literal 282.2. OK.
## Otros controles
- T: DT 1.ª RDL 2/2024 agotada; ninguna transitoria vigente gradúa 271/272/282. (Nota menor del preverif: el RDL 3/2026 SUPRIME la 271.1.k, no la restituye; sin efecto aquí.)
- Citas muestreadas (282.2, 271.2, 272.1.c, 282.3 exclusiones): literales correctas.
- Bordes 75/74/50/49/100, 11/12 meses, tope 180 días y días restantes: el oráculo implementa la norma igual.

## Otras calculadoras (cambio obligatorio)
- subsidio-desempleo-cuanto-cobro-y-cuanto-dura: SOLO TEXTO. En «No incluye…» la frase «(80 % del IPREM el primer trimestre y menos después…; art. 282.3)» es absoluta: cambiar a «hasta el 80 % del IPREM el primer trimestre a jornada completa y menos después; menos desde el principio si vienes de agotar un paro de más de 12 meses reconocido desde el 1-4-2025, DA 59.ª.4». Cálculo de cuantía y duración: sin cambios.
- cuanto-cobro-de-paro-prestacion-desempleo: ningún cambio (DA 59.ª no toca 269/270; la página ya excluye la compatibilidad con trabajo).

## Casos nuevos para test.json
- subsidio, viene de paro > 12 meses desde 1-4-2025 = sí → bloqueo (o, si se modela, paro agotado 24 meses, jornada 100, mes 1 → CAE 120 €/mes).
- subsidio, viene de paro > 12 meses = no → resultado actual (CAE 480 € en T1 a jornada completa).
- textos: grep «no hay compatibilidad» sin «59.ª» en el mismo párrafo → falla; ganador A sin mención de «oferta de empleo adecuada» → falla.
