# Reverificación · cuanto-cobro-de-paro-prestacion-desempleo · 2026-10-02
VEREDICTO: LOS 3 CAMBIOS APLICADOS · SMI 1.221 € CORRECTO · 1 PENDIENTE MENOR (fuente en params)

## Cambios críticos (solo lectura)
1. Ámbito País Vasco/Navarra: aplicado. calcs/…js (nota «No incluye») dice «la retención del IRPF (tampoco la foral)»; en el html ya no figura «País Vasco/Navarra».
2. Hijo a cargo: aplicado. calcs/…json input `hijos` tiene `ayuda` (menores de 26, mayores con discapacidad, menores acogidos, conviven o dependen, rentas ≤ SMI 1.221 €, sin pagas extra) y el html («Supuestos», línea 31) lo repite.
3. Días cotizados: aplicado. Label del input `dias` = «…que no hayas usado ya para una prestación o subsidio anterior»; la ayuda dice que la vida laboral no descuenta (art. 269.2); html línea 30 igual.

## SMI 2026
Confirmado: 1.221 €/mes en 14 pagas (40,70 €/día) = 17.094 €/año. Real Decreto 126/2026, de 18 de febrero, BOE 19/02/2026, BOE-A-2026-3815. URL: https://www.boe.es/boe/dias/2026/02/19/pdfs/BOE-A-2026-3815.pdf (ELI: https://www.boe.es/eli/es/rd/2026/02/18). Sin pagas extra, la cifra es 1.221 € (17.094 / 14).

## data/params.json
La cifra existe: autonomo_2026.general.smi_anual = 17094 (línea 1221). NO tiene fuente propia: no se cita el RD 126/2026 en ningún sitio del params, y el bloque cuanto_cobro_paro_2026 no incluye el SMI (1.221 € está solo escrito a mano en el json y el html de la calculadora). Recomendable (no bloqueante): añadir smi_mensual_14_pagas 1221 + fuente RD 126/2026 + URL arriba en params.cuanto_cobro_paro_2026 y referenciarlo.
