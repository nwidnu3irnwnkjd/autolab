# Verificación plan-pensiones-o-fondo-indexado · c106 · 2026-10-10 (COLA ítem 8)
VEREDICTO: PUBLICABLE CON CAMBIOS (3 obligatorios, solo texto; ninguna cifra ni veredicto cambia) · T 2 · 8 0 · N 0 · R 1 · S 0 · otros 0 · recomendados 2 (T 1, N 1)

## Pruebas
- ops/verif/plan-pensiones-o-fondo-indexado.py: 11 casos fijos OK + barrido 500 JS vs Python, 0 discrepancias.
- calcs/plan-pensiones-o-fondo-indexado.test.json (arnés de ops/check.py, solo este slug): 16 casos, 75 aserciones, 0 fallos.
- Guía: 417 € (1.500 × 27,8 %, Madrid 35.000: estatal 15 + autonómica 12,8), 49.491 / 57.863 / 8.371 € coinciden con el caso 1 de test.json.

## Norma leída (API consolidada BOE, versión con fecha_vigencia más alta de cada bloque; LIRPF actualizada 07-10-2026, TRLPFP 18-09-2026)
- LIRPF art. 52.1 (Ley 31/2022, vig. 1-1-2023): menor de 30 % de rend. netos trabajo+actividades o 1.500 €; +8.500 € contribuciones empresariales o aportaciones del trabajador al mismo instrumento según cuadro (×2,5 / 1.250+0,25 / ×1; ×1 si >60.000 € de esa empresa); +4.250 € autónomos (sectoriales, simplificados, promotor-partícipe); máx. 8.500 € de incrementos. 52.2: arrastre 5 años por insuficiencia de base o límite del 30 %. Sin cambios posteriores (ni Ley 12/2023, que es de vivienda, ni PGE: no hay PGE 2024-2026 que lo modifiquen).
- Ojo con la numeración del encargo: el límite NO es el art. 51 sino el 52.1; el cónyuge (1.000 €, cónyuge con rend. < 8.000 €) es el art. 51.7 (Ley 11/2020); el 51.5 es seguros de dependencia; los planes de empleo y sus incrementos están en 52.1.1.º-2.º y TRLPFP art. 5.3. La página cita bien (52, 52.1, 52.2): sin cambio.
- LIRPF art. 17.2.a.3.ª (vig. 2020): prestaciones de planes = rendimiento del trabajo; también lo cobrado por liquidez del 8.8. Arts. 63 (vig. 2021), 66 y 76 (Ley 7/2024, vig. 22-12-2024), 74: sin cambios; escalas del oráculo correctas.
- TRLPFP art. 5.3.a (vig. 2023): 1.500 € máx. a planes; art. 36.5: retirar exceso antes del 30-6 del año siguiente o multa del 50 %; art. 8.8 (vig. 26-9-2022): liquidez por desempleo de larga duración, enfermedad grave y aportaciones con al menos 10 años (individual/asociado: por ley; empleo: «si así lo permite el compromiso y lo prevén las especificaciones»).
- RDL 25/2026 (BOE-A-2026-20265) y RDL 28/2026 (-20822): no citan la Ley 35/2006 ni el RDL 1/2002. RDL 29/2026 (-20823, XML del BOE): en la LIRPF toca arts. 7.ñ, 23.2, 67.1, 68.6 (nueva deducción por alquiler), sección 8.ª tít. X (Cuenta Financia Europa), DA 5.ª.4, 26.ª (PALP), 50.ª.6, 55.ª, 58.ª.5, 62.ª.6, 65.ª y 66.ª nuevas, DT 15.ª.3 y 38.ª; desde 2027 arts. 24 y 85. Confirmado: no toca arts. 17.2.a, 51, 52, 63, 66 ni 76 ni el TRLPFP. Los bloques a51/a52 del consolidado del 07-10 siguen con su versión de 2022/2023.

## Cambios obligatorios (archivo · línea · actual → propuesto · fuente)
| # | Archivo:línea | Actual → propuesto | Fuente | Clase |
|---|---|---|---|---|
| 1 | calcs/plan-pensiones-o-fondo-indexado.json:152 (FAQ «¿Cuánto puedo aportar…?») | «Con aportaciones de empresa sube a 8.500 €.» → «Con contribuciones de la empresa a un plan de empleo el límite sube hasta 8.500 € más (10.000 € en total, siempre con el tope del 30 %).» | LIRPF 52.1.1.º | T |
| 2 | calcs/plan-pensiones-o-fondo-indexado.js:64 (nota >1.500 €) | «Solo con aportaciones de la empresa o con planes de autónomos sube ese límite, y la calculadora no lo modela» → «Ese tope del plan individual no sube nunca; el límite conjunto solo crece con contribuciones de la empresa a un plan de empleo o con planes de empleo de autónomos, y la calculadora no lo modela» | TRLPFP 5.3.a; LIRPF 52.1 | T |
| 3 | calcs/plan-pensiones-o-fondo-indexado.js:73 y content/plan-pensiones-o-fondo-indexado.html:13 | js: «o, si sus especificaciones lo prevén, aportaciones con al menos diez años de antigüedad» → «o aportaciones con al menos diez años de antigüedad (en planes individuales, por ley; en los de empleo, si lo prevén sus especificaciones)»; html: «o, si sus especificaciones lo prevén, aportaciones de más de diez años de antigüedad» → mismo texto, con «al menos diez años» | TRLPFP 8.8 párr. 2 | R |

## Recomendados (no bloquean)
| 4 | content/guias/antes-fin-de-ano-dinero-plan-pensiones-perdidas-donativos.html:1 (FAQ meta) | «(hasta 1.500 € o el 30 % de tus rendimientos)» → «(hasta el menor de 1.500 € o el 30 % de tus rendimientos)» | LIRPF 52.1 | T |
| 5 | content/plan-pensiones-o-fondo-indexado.html:27 (Supuestos, antes de «No incluye la reducción del 40 %») | añadir «<li>No incluye la reducción por aportaciones al plan de tu cónyuge si gana menos de 8.000 € al año (hasta 1.000 €, art. 51.7 de la Ley del IRPF).</li>» | LIRPF 51.7 | N |

## Resto revisado sin hallazgos
Rescate como rendimiento del trabajo en base general, capital o renta (17.2.a.3.ª) · DT 12.ª fuera de modelo y declarada · arrastre 5 años (52.2) · art. 36.5 · traspasos art. 94.1.a · ahorro fiscal = diferencia de cuota estatal+autonómica con mínimo personal, tipo marginal = suma de tramos (JS = oráculo) · guía: arts. 51 y 52, 1.500/30 %, retirada antes del 30-6, rescate en escala general: correctos.

## Casos nuevos para test.json
Ninguno: los cambios son de texto. Re-verificación: Sonnet, releer solo las 3 frases (+2 si se aceptan) y re-ejecutar ops/verif/plan-pensiones-o-fondo-indexado.py y ops/check.py decidir.
