# Re-verificación periódica (Opus) · cuanto-cobro-de-paro-prestacion-desempleo · 2026-10-07
VEREDICTO: SIGUE CORRECTA, sin cambios obligatorios · T 0 · 8 0 · N 0 · R 0 · S 0 · otros 0 (2 opcionales) · 0 errores de fórmula

## Norma leída hoy (API BOE consolidada, BOE-A-2015-11724; índice actualizado a 03/10/2026)
- Art. 270 (última versión, fecha_vigencia 01/01/2023, DF 25.8 Ley 31/2022): BR = promedio de la base por desempleo de los últimos 180 días sin horas extra (270.1); 70 % días 1-180 y 60 % desde el 181 (270.2); máx. 175/200/225 % y mín. 80/107 % del IPREM mensual «incrementado en una sexta parte», con tiempo parcial según el promedio de horas de los 180 días (270.3). Coincide con JS, params y oráculo.
- Art. 269 (versión vigente: BOE-A-2024-10235, RDL 2/2024, en vigor 23/05/2024). Trampa de versiones: la de fecha_vigencia más alta (01/06/2024) es la del RDL 7/2023, que el Congreso derogó (BOE-A-2024-664); solo cambia el 269.3. Escala 269.1 (360-539:120 … 2.160+:720) idéntica a `P.escala`; 269.2 (cotizaciones no computadas antes) declarado en label y supuestos.
- Arts. 262-282 con cambios en 2025-2026: solo el 271 (suspensión, letra k del 271.1 suprimida por RDL 3/2026, tras la derogación del RDL 16/2025). No afecta a la cuantía ni a la duración. El 147 no cambia desde 2022. Los cambios de 03/10/2026 (Ley 4/2026, BOE-A-2026-20528) tocan los arts. 190 y 363, no el desempleo.
- RDL 25/2026 (BOE-A-2026-20265), RDL 26/2026 (BOE-A-2026-20266, derogado BOE-A-2026-20526), RDL 28/2026 (BOE-A-2026-20822) y RDL 29/2026 (BOE-A-2026-20823): 0 menciones del IPREM, el art. 269/270 ni la prestación por desempleo (el RDL 28 solo cita el RDL 2/2024 en la exposición). RDL 3/2026 (BOE-A-2026-2548): toca el IRPF de los perceptores (obligación de declarar), no la cuantía; la página no habla de esa obligación.

## IPREM y SMI
- IPREM 2026 = 600 €/mes (20 €/día, 7.200 €/año): DA 90.ª de la Ley 31/2022 (PGE 2023, consolidado, sin modificar), prorrogada por falta de PGE; ninguna norma de 2026 lo cambia (comprobado en los RDL anteriores). 600 x 7/6 = 700 → 1.225/1.400/1.575 y 560/749: correcto.
- SEPE, «Cuantías anuales» (consultada hoy): SMI 1.221 € (RD 126/2026), IPREM 600 € (Ley 31/2022), mínimo 560/749, máximo 1.225/1.400/1.575. Coincide.
- IPREM/SMI 2027: no hay norma publicada; Cortes disueltas por el RD 806/2026 (BOE-A-2026-20742), así que no puede haber PGE 2027 antes de enero. La página dice «cuantías de 2026 … se suponen constantes; la ley puede cambiar»: correcto, no da cifras de 2027.

## Ejecución
- Oráculo `ops/verif/cuanto-cobro-de-paro-prestacion-desempleo.py`: 600 aleatorios + 20 fijos, 0 discrepancias con el JS.
- `ops/check.py`: 13.623/13.623 OK; casos típicos 19/19 y tablas de respuesta 4/4 coinciden con la calculadora.

## Recalculado a mano
- Tabla `#nomina-1800`: 1.800 x 70 % = 1.260 > 1.225, así que sin hijos 1.225; 60 % = 1.080. Con 1 hijo: 1.260 < 1.400 y 1.080 ≥ 749 → 1.260 · 1.080. Coincide.
- `#nomina-1000`: 700 · 600 sin hijos; con hijo, mínimo de 749 en los dos tramos → 749 · 749. `#nomina-2200`: 1.540 y 1.320 → 1.225 · 1.225 sin hijos; con hijo 1.400 · 1.320. Coincide.
- Casos típicos: 1.200/720 d → 180 x 28 + 60 x 24 = 6.480 €; 2.500/1.080 d → 360 x 40,83 = 14.700 €; 1.800/2 hijos/1.440 d → 480 días, 180 x 42 + 300 x 36 = 18.360 €. Coinciden.
- Texto (ejemplos, umbrales 1.750/2.000/2.250, 2.041,67/2.333,33/2.625, 800/933,33/1.070/1.248,33, 612,50, 37.800, −14,3 %): siguen correctos.

## Opcionales (no bloquean)
| archivo | qué | por qué |
|---|---|---|
| data/tablas_respuesta.json (tabla-paro, h3) | Añadir «(base con pagas prorrateadas)» al título o a la columna «Nómina» | Quien cobra 1.800 € en 14 pagas tiene base de 2.100 € (sin hijos, 1.225 · 1.225, no 1.225 · 1.080). Las condiciones lo dicen, pero el h3 no. |
| data/params.json cuanto_cobro_paro_2026 | Actualizar `consulta`/`consolidados` a 07/10/2026 y añadir el SMI 1.221 € con fuente RD 126/2026 | Sigue pendiente de la reverificación del 2/10; las cifras no cambian. |
Próxima revisión con contenido: cuando se publique un IPREM o un SMI de 2027, o si una norma modifica los arts. 269-270.
