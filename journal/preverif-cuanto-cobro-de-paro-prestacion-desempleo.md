# Pre-verificación · cuanto-cobro-de-paro-prestacion-desempleo · 2026-10-02 (Constructor Sonnet)
Fuente: BOE consolidado LGSS (BOE-A-2015-11724) leído hoy: art. 269 (apdo. 3 RDL 2/2024, sin efecto en la escala), 270 (apdo. 2 Ley 31/2022; vigente 1/1/2023), 147.1. Nota: el art. 271 es «Suspensión del derecho», no cuantía; la cuantía está solo en 269-270. IPREM 2026 600 € (SEPE, cuantías 2026; Ley 31/2022 prorrogada). Reutiliza lo verificado en journal/verificacion-paro.md (70/60 %, 175/200/225 %, 80/107 %, +1/6, 560/749, 1.225/1.400/1.575).
Oráculo: ops/verif/cuanto-cobro-de-paro-prestacion-desempleo.py (INTERPRETACION en cabecera; 20 fijos + 600 aleatorios contra el JS real, 0 discrepancias).
1. Absolutos: grep sin hits en content y json. Hecho.
2. Mecánica no modelada: horas extra (excluidas de la BR, art. 270.1: declarado), 270.4 dos contratos parciales (declarado), 270.5 desempleo parcial (declarado), 270.6 reducción de jornada por cuidado (declarado; sube la BR), retención IRPF y cotización del trabajador (declarado: el neto es menor), carencia de rentas/subsidios (declarado).
3. Territorial: forales declarados; Canarias/Ceuta/Melilla no cambian la prestación.
4. Redacción vigente: ver arriba. Citas: 270.1 «promedio de la base ... últimos ciento ochenta días»; 270.2 «70 por ciento ... 60 por ciento»; 270.3 «175... 200... 225 %; mínima 107 u 80 %; IPREM calculado en función del promedio de las horas trabajadas; IPREM incrementado en una sexta parte»; 269.1 escala; 147.1 «percepciones de vencimiento superior al mensual se prorratearán».
5. Bordes: tests en 1.750 (tope tramo 1), 800 (mínimo tramo 1), 1.070 con 1 hijo (749 = 0,7 x 1.070), 359/360/539/2.160 días.
6. Defaults: 1.500 €, 0 hijos, 100 %, 720 días (hipótesis editables, sin dato de mercado).
7. Convenciones: mes = 30 días (prestación diaria x 30, convención del SEPE; no verificada en la norma, declarada). Jornada parcial: promedio ponderado de horas; el modelo usa el % medio introducido (declarado).
T · Transitorias: RDL 2/2024 (art. 269.3, reapertura; no afecta a la cuantía ni a la escala): no aplica en 2026. Ninguna DT activa sobre 269/270 (grep «artículo 270» en el consolidado: solo referencias de cese de actividad, art. 331). Declarada.
8 · Opción imposible: < 360 días cotizados -> bloqueo (caso test «dias 359»); jornada fuera de 1-100 y hijos negativos -> aviso. Sin alternativas comparadas.
N · No modelado: ver «Supuestos del cálculo» en la página (IRPF y cotización: el neto baja; subsidios; compatibilidad; forales; fijos discontinuos; dos parciales; sanciones; reducción de jornada).
R · RDL 26/2026 (BOE-A-2026-20266): no toca arts. 147, 269 ni 270 (sin menciones a desempleo ni IPREM en el texto); no se cita en la página. No hay PGE 2026: IPREM prorrogado.
Supuestos no todos de ley: mes de 30 días; 14/12 para pagas no prorrateadas; % medio de jornada; «hijos a cargo» por criterios del SEPE (sin modelar requisitos).
