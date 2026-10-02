# Verificación fiscal · baja-medica-cuanto-cobro-incapacidad-temporal (Verificador Opus, 2/10/2026)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 2 · N 0 · R 0 · S 2 · otros 1 · críticos 0
Normas leídas hoy en el BOE: LGSS 169, 171, 172, 173 (Ley 6/2024, vigor 3-3-2025), 174 (vigor 1-5-2025), 102 (API consolidado); RD 53/1980 art. único (doc.php); Decreto 3158/1966 art. 2.1 (doc.php + referencias posteriores: solo lo modifica el RD 53/1980); Orden 13-10-1967 arts. 2 y 8 (art. 8.a no derogado: solo 8.d, RD 1251/2001); **Decreto 1646/1972 art. 13 (BOE-A-1972-944, act.php)**. Orden PJC/297/2026 (5.101,20 €): por muestreo, ya verificada en permiso-nacimiento. Oráculo re-ejecutado: 20 fijos + 800 aleatorios, 0 discrepancias.

## Paso 0: interpretación propia frente a INTERPRETACION del oráculo
1. Común: 0 € días 1-3, 60 % BR días 4-20 (RD 53/1980 literal: «hasta el veinteavo día, inclusive ... sesenta por ciento»), 75 % desde el 21 (Decreto 3158/1966 art. 2.1, que el RD 53/1980 solo modifica para 4-20); días 4-15 a cargo de la empresa (173.1). COINCIDE.
2. AT/EP: salario íntegro el día de la baja a cargo de la empresa y 75 % desde el día siguiente (173.1 literal; no es supuesto). Sin carencia (172.b). COINCIDE.
3. BR = base de cotización de la contingencia del mes anterior / días a que se refiere; /30 si retribución mensual y alta todo el mes: **literal en Decreto 1646/1972 art. 13.1-2** (13.4: conceptos de devengo superior al mes, promedio 12 meses). COINCIDE con el JS; la página dice que no hay artículo: falso (ver S1).
4. Duración: 365 + 180 (169.1.a), extinción a 545 (174.1). DIFIERE en el texto: 174.5 da «prolongación de efectos económicos» tras el día 545 hasta la resolución de IP (174.2: hasta 730 días con demora de calificación, sin cotizar). La cuantía no cambia ≤ 545; el bloqueo de 546 es aceptable como «fuera del modelo» pero no como «se extingue y no cobras».

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | S | content/*.html (Cómo se calcula + Supuestos), params baja_medica_2026.fuente, calcs json fuente | Sustituir «no hemos encontrado un artículo consolidado... supuesto propio» por «Decreto 1646/1972, art. 13.1 y 13.2» (enlace https://www.boe.es/buscar/act.php?id=BOE-A-1972-944) y subir a confianza A; el mes de 30 días con sueldo mensual también es literal (13.2), no convención | El artículo existe y lo dice literalmente |
| 2 | S | lead/html, json (lead, FAQ), js nota y tabla (Constructor) | «desde el 16 lo paga la Seguridad Social o la mutua» → «desde el 16 está a cargo de la Seguridad Social o la mutua (normalmente te lo sigue abonando la empresa en la nómina, pago delegado)» | 173.1 fija a cargo de quién, no quién abona; con pago delegado lo paga la empresa |
| 3 | 8 | json ayuda de «dias», html Duración, mensaje de bloqueo de 546 | Sustituir «Más de 545 días el derecho se extingue» por: «a los 545 días se extingue la IT, pero sigues cobrando la misma prestación (prolongación de efectos, art. 174.5) hasta que se resuelva la incapacidad permanente; la herramienta no calcula más allá del día 545» | 174.5 y 174.2 |
| 4 | 8 | json/html: aviso junto al resultado en «común» | Una línea visible (no solo en Supuestos): «En enfermedad común necesitas 180 días cotizados en los 5 años anteriores (art. 172.a); si no los tienes, no cobras subsidio» | La opción calculada puede no existir para el usuario |
| 5 | otros | json (Duración/FAQ) | «en un plazo máximo de tres meses» → «90 días naturales» | 174.2 literal |

## Supuestos S revisados (prioridad del preverif)
- Mejora del convenio con el mismo % todos los días: no legal, defendible y declarado en página y ayuda. OK.
- Día de la baja en AT a salario íntegro: literal 173.1 (reclasificar como ley, no supuesto). OK.
- Orden 1967 art. 8.a (7 días mínimos): texto confirmado y sin derogación expresa; no modelarlo siguiendo 173.1 LGSS (rango y fecha posteriores) es defendible y está declarado. OK.
- 60 %/75 %: literal confirmado (ver Paso 0). Base máxima 5.101,20: OK.
## Transitorias, RDL 26/2026, absolutos
T: Ley 6/2024 en vigor desde 3-3-2025, situaciones especiales declaradas como no modeladas; sin DT activa. R: el RDL 26/2026 no toca LGSS 169-176, RD 53/1980 ni Decreto 1646/1972; la página no lo cita. Absolutos: «Los 3 primeros días no se cobra prestación» queda salvado por la exclusión declarada de las situaciones especiales; sin más hits.
## Tests nuevos para test.json: ninguno (los bordes 3/4, 15/16, 20/21, 545/546 y base máxima ya están).
