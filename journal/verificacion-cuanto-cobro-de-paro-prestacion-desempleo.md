# Verificación independiente (Opus) · cuanto-cobro-de-paro-prestacion-desempleo · 2026-10-02
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 1 · N 1 · R 0 · otros 1 (ámbito) · 0 errores de fórmula · re-verificación: Sonnet (solo texto, no cambia la interpretación)

## Paso 0: mi lectura de la norma frente a la INTERPRETACION del oráculo
Leído hoy el BOE consolidado (BOE-A-2015-11724) de los arts. 269 y 270: coinciden con el bloque INTERPRETACION. BR = promedio de la base por desempleo de los últimos 180 días sin horas extra (270.1); 70 % los 180 primeros días y 60 % desde el 181 (270.2, en la redacción de la DF 25.8 de la Ley 31/2022, en vigor desde el 1/1/2023); máximo 175/200/225 % y mínimo 80/107 % del IPREM mensual «incrementado en una sexta parte» (270.3); con jornada parcial, IPREM según el promedio de horas de los 180 días (270.3, párrafo 3): x jornada/100 es correcto con jornada constante y está declarado; escala 360-539:120 … 2.160+:720 (269.1): exacta. IPREM 2026 = 600 €/mes: es el vigente (DA 90.ª de la Ley 31/2022, prorrogada; sin PGE 2026; la página de cuantías del SEPE sigue con 600 y 560/749 y 1.225/1.400/1.575). 700 x 1,75/2/2,25 = 1.225/1.400/1.575; 700 x 0,80/1,07 = 560/749: correcto. Ejemplos y umbrales de la página recalculados a mano (8.100; 14.700; 37.800; 560; 420/360; 612,50; 1.750/2.041,67/933,33/1.070/1.248,33; −14,3 %): todos correctos.

## Cambios obligatorios
| # | clase | archivo | qué | por qué |
|---|---|---|---|---|
| 1 | otros (ámbito, patrón 3) | calcs/…js (nota «No incluye») y content/…html («Supuestos», último punto de exclusiones) | Quitar «el País Vasco y Navarra» de lo no incluido | La prestación contributiva es estatal (la gestiona el SEPE en todo el territorio, arts. 269-270 LGSS); en los forales solo cambia la retención del IRPF, que ya no se modela. Decirle a un vasco o navarro que no le aplica es falso y le hace abandonar la herramienta. Si se quiere, «la retención del IRPF (tampoco la foral)». |
| 2 | 8 (opción que puede no existir) | calcs/…json, input `hijos` (añadir `ayuda`) y content/…html (punto «Supuestos» de hijos) | Definir hijo a cargo: menor de 26 años, o mayor con discapacidad, o menor acogido, que conviva o dependa económicamente de ti y no tenga rentas mensuales superiores al SMI (1.221 € en 2026), excluidas pagas extra (SEPE) | Hoy solo dice «los que cumplen los requisitos del SEPE»: quien tenga un hijo de 27 años o con ingresos marcaría 1 y vería un máximo de 1.400 o un mínimo de 749 que no le corresponde. |
| 3 | N (art. omitido en el input, 269.2) | calcs/…json, input `dias` (label/ayuda) y FAQ 3 | «Días cotizados en los últimos 6 años que no hayas usado ya para una prestación o subsidio anterior»; la ayuda debe decir que el informe de vida laboral no los descuenta | Art. 269.2: solo cuentan las cotizaciones «que no hayan sido computadas para el reconocimiento de un derecho anterior». Está en «Supuestos», pero el label manda al informe de vida laboral, que da el total: quien ya cobró paro sobrestima la duración (p. ej. 720 → 240 días cuando quizá le corresponden 120 o ninguno). |

## Opcionales (no bloquean)
- `dias` > 2.191 no es posible en 6 años: aviso o tope (la duración no cambia: 720).
- FAQ 3 «anteriores al despido» → «anteriores a la situación legal de desempleo» (art. 269.1; incluye fin de contrato).
- Nota JS: mismo cambio 1 en el texto de «No incluye».

## Supuestos (todos defendibles y declarados)
Mes de 30 días (los topes del SEPE son mensuales de 30 días; el total por días es exacto) · 14/12 si la base no incluye pagas (aritmético; art. 147.1 citado bien) · % medio de jornada (declarado que la ley pondera por empleo) · IRPF y cotización del trabajador no modelados, declarados como neto menor · subsidios, compatibilidad, fijos discontinuos, 270.4, 270.5, 270.6 declarados. Bloqueo < 360 días correcto.

## T / 8 / N / R
T: ninguna DT vigente sobre 269-270 (la DT 1.ª del RDL 2/2024 sobre 269.3 se agotó el 31/10/2024; el paso 50→60 % rige desde 1/1/2023 y ya no hay derechos vivos anteriores). 8: hallazgo 2. N: hallazgo 3 (el resto de lo no modelado está declarado). R: RDL 26/2026 (vivienda, sin convalidar) no toca 147, 269, 270 ni el IPREM: correcto no citarlo.
Citas por muestreo (patrón 4): 270.1, 270.2, 270.3, 269.1 y 147.1 contra el texto consolidado: correctas.

## Tests nuevos (test.json)
Ninguno de fórmula. Si se aplica el opcional de días > 2.191, un caso de aviso.
