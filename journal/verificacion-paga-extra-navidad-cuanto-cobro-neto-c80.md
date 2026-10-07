# Re-verificación c80 · paga-extra-navidad-cuanto-cobro-neto · 2026-10-07 (Verificador fiscal, COLA ítem 8)
VEREDICTO: PUBLICABLE · T 0 · 8 0 · N 0 · R 0 · S 0 · otros 0 (0 cambios obligatorios; 2 recomendados, 1 con fecha de disparo 1-1-2027)

Por qué esta: es fiscal de alto tráfico y estacional (búsquedas de oct a dic), la última verificación es del 2-10 (c4) y no se había vuelto a verificar en c74-c78.

## Paso 0 · interpretación propia vs bloque INTERPRETACION del oráculo: coincide
- ET 31: dos pagas al año, una «con ocasión de las fiestas de Navidad». Su cuantía la fija el convenio, que también puede prorratearlas. La parte proporcional, el devengo y si cuenta días o meses no están en la ley: son inputs o supuestos declarados.
- LGSS 147.1: las percepciones que vencen con periodicidad superior a la mensual se prorratean en 12 meses, así que en el mes de la paga no se cotiza aparte. RIRPF 80.1.1.º + 86.1: a la paga se le aplica el tipo de la nómina; la regularización del art. 87 queda declarada como límite. ET 49.2: la parte proporcional va en el finiquito.

## Norma vigente: API consolidada del BOE, última `<version>` de cada bloque, consultada hoy
| Artículo | Última versión vigente desde | ¿Coincide con el texto que cita la página? |
|---|---|---|
| ET 31 (BOE-A-2015-11430) | 13-11-2015 (versión única) | sí, literal |
| ET 49.2 | 1-5-2025 (Ley 2/2025; el apdo. 2 no cambia) | sí, «propuesta del documento de liquidación de las cantidades adeudadas» |
| LGSS 147.1 (BOE-A-2015-11724) | 1-1-2023 | sí, «se prorratearán a lo largo de los doce meses del año» |
| RIRPF 80.1 (BOE-A-2007-6820) | 7-12-2023 | sí |
| RIRPF 86.1 | 26-1-2023 | sí, el tipo «se expresará con dos decimales» |
| RIRPF 87.3-4 | 21-10-2021 | sí (lo declara en «Qué no incluye») |
- RDL 25/2026 y RDL 28/29-2026, pendientes de convalidación: no tocan ET 31/49, LGSS 147 ni RIRPF 80/86/87 (journal/verificacion-rdl-25-2026.md y verificacion-rdl-28-29-2026.md; RDL 29 cambia la LIRPF, arts. 23, 24, 68.6, 85 y DA 55.ª, nada de retenciones del trabajo). El RDL 26/2026 aparece en params:4973+ como «derogado el 2-10-2026, no se cita»: correcto.
- Cotización del trabajador 2026: 6,5 % = CC 4,70 + desempleo indefinido 1,55 + FP 0,10 + MEI 0,15 (Orden PJC/297/2026, BOE-A-2026-7296; LGSS DT 43.ª: MEI 2026 0,90 = 0,75 + 0,15). Correcto.

## Oráculo y tests (re-ejecutados hoy)
- ops/verif/paga-extra-navidad-cuanto-cobro-neto_oraculo.py: 828 casos (800 aleatorios + 28 bordes), 0 discrepancias JS↔Python.
- calcs/…test.json: 25/25 casos pasan (incluye los 3 que pidió c4: baja 31-dic anual, alta 1-mar semestral, 365 días sin devengo).
- Ejemplo comprobado a mano: 1.500 × 122/184 = 994,57; retención 15 % = 149,19; neto 845,38; cotización 6,5 % = 64,65; neto real 780,73. Paga entera: 1.275. Coinciden en lead, veredicto, FAQ 1-2 y html:1, 4-6.
- Los 5 cambios obligatorios de c4 están aplicados: cita del art. 31 separada (lead/html:1), FAQ 5 y html:11 con «con ocasión de las fiestas de Navidad», «nóminas mensuales» en js escenario 1, art. 87 ampliado en html:15 y en la ayuda de `ret`, «el tipo, expresado con dos decimales» en html:5. Aplicado también el recomendado (d) de c4: frase del finiquito con baja + escenario 1 (js:46).

## Texto ≤ cálculo (muestreo de frases con contenido absoluto)
- Lead «la cobras entera si trabajaste todo su periodo»: demostrada sí; deja dicho que la baja o excedencia la decide el convenio (input diassin).
- «sin otra cotización aparte»: demostrada sí (147.1). «Neto real… aproximación al 6,5 %, sin tope»: demostrada sí y declarada como aproximación. El prorrateo de un alta a mitad de año depende del método de la empresa; el aviso de aproximación lo cubre.
- Ámbito: los forales, Ceuta y Melilla se resuelven con «pon el tipo de tu nómina» (html:16). Defendible.

## Cambios obligatorios
Ninguno.

## Recomendados (no bloquean)
| # | Archivo:línea | Actual → propuesto | Fuente |
|---|---|---|---|
| R1 | data/params.json:4540 (retencion_irpf_nomina_2026.cotizacion_trabajador_desglose) | «(Orden de cotización 2026 y RDL 3/2026; …)» → «(Orden PJC/297/2026, BOE-A-2026-7296, y LGSS DT 43.ª; …)», igual que params:41. Ya lo pidió c4 y sigue pendiente | Orden PJC/297/2026 |
| R2 | calcs/…js:3 (`"cot": 6.5`), js:37 («no existe en 2026»), html:6, :14, :22 y params:4973 (calendario_2026) | **Disparo 1-1-2027** (antes no: la paga de diciembre de 2026 es la que se busca ahora): crear paga_extra_navidad_2027 con cot 6,52 (MEI del trabajador 0,17 en 2027) y calendario 2027 (365/184; el día 182 sigue siendo el 1-jul) | LGSS DT 43.ª: «En el año 2027 … 0,17 al trabajador» |
| R3 | json sources, html:23, params «consulta» | «consultado el 2/10/2026» → «… y recontrastado el 7/10/2026 (API consolidada del BOE: sin versiones nuevas)» | este informe |

## Casos nuevos para test.json
No hacen falta: los bordes de fechas, el bloqueo de días inexistentes, las retenciones de 0 % y 47 %, el prorrateo y los días sin devengo ya están cubiertos. Si se aplica R2: un caso con cot 6,52 (1.500 € enteros → cotizada 97,80).
