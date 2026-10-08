# Re-verificación sueldo-bruto-a-neto-2026 (c89, Verificador fiscal Opus, 2026-10-08)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (solo texto; ninguna cifra publicada es falsa) · T 1 · 8 0 · N 1 · R 0 · S 1 (no crítico para la nómina; sí para el consejo «no declares» de los inquilinos) · otros 1
Paso 0: mi lectura coincide con el bloque INTERPRETACION del oráculo (SS, base de retención, 81/83.2/85.3/86.2, art. 20, DA 61.ª, 96.2.a, temporal < 1 año). Lo único nuevo es el art. 68.6 LIRPF (RDL 29/2026): cambia la cuota estatal de la Renta, no la retención.

## Norma releída hoy (API consolidada BOE; versión de fecha_vigencia más alta, comprobando id_norma)
- LIRPF: a19 (BOE-A-2014-12327), a20 (BOE-A-2024-12944, vig. 28-6-2024), a57/58/59/61 (2014), a63 (BOE-A-2020-17339), a74, a96 (BOE-A-2025-1136: 96.2.a 22.000 €), a101 (2023), DA 61.ª = bloque `da-15` (BOE-A-2026-3810, vig. 20-2-2026: 590,89 / 17.094 / 20.048,45). **Ninguno con versión nueva** tras RDL 25/28/29.
- RIRPF a80-a88: últimas 2014-2024 (a81 y a83 RD 142/2024; a85 2022; a86 2023). **Sin versión nueva.** La DF 3.ª del RDL 29 (XML BOE-A-2026-20823, leído íntegro) solo toca RIRPF 41 bis.3, 69.3, 75.3-4, 76.2.h, 93.7, 94.3 y DA 8.ª ⇒ la retención no cambia.
- **Trampa de versiones**: a67 y a68 tienen 3 versiones de 2026: BOE-A-2026-20266 (RDL 26, derogado el 2-oct), BOE-A-2026-20526 (2-oct) y **BOE-A-2026-20823 (RDL 29, vig. 8-10-2026) = la válida**. Su 68.6: deducción del 10 % del alquiler de vivienda habitual, BI < 33.007,20 €, base máx. 11.630 € (rampa −1,163 × (BI − 23.007,20)), sin otra vivienda a < 50 km; 67.1.a la resta íntegra de la cuota estatal. Efectos «desde la entrada en vigor» (art. 6.Segundo); si cubre el alquiler pagado antes del 8-oct en el IRPF 2026: no resuelto (ya marcado S en verificacion-rdl-28-29-2026.md). RDL 29 pendiente de convalidación (art. 86.2 CE).
- RDL 25/2026 (energía) y RDL 28/2026 (LAU): no tocan IRPF del trabajo ni cotización.
- Orden PJC/297/2026 (txt BOE-A-2026-7296, releída por muestreo): art. 2 tope 5.101,20 €; CC 4,70; MEI 0,15; desempleo 1,55 indefinido / 1,60 duración determinada; FP 0,10; solidaridad 0,19 sobre 5.101,21-5.611,32 €. = JS (`bmax`, `w` 6,50/6,55, `sol`).
- Tablas autonómicas (15 de régimen común modeladas; País Vasco y Navarra bloqueados con aviso, motivo 2; Ceuta y Melilla fuera con aviso en supuestos, sources y nota de límites): muestreo BOE hoy de las 2 más recientes, Extremadura (DLeg 1/2018 art. 1, BOE-A-2026-17839, efectos 1-1-2026) y C. Valenciana (Ley 13/1997 art. 2, BOE-A-2026-19331; la escala 2027 de la DT 3.ª no aplica a 2026): idénticas al JS. Madrid: verificada el 3-oct (< 30 días). Andalucía: la API no devuelve el bloque (404), no re-leída.

## Ejecución
- Oráculo `ops/verif/sueldo-bruto-a-neto-2026_oraculo.py`: **724 casos, 0 discrepancias** JS vs Python.
- `ops/verif/sueldo-bruto-a-neto-2026.py`: todo OK (20 casos; añadidos hoy 4 de impacto del art. 68.6, ver abajo).
- `ops/check.py decidir`: 13.680/13.680 OK (incluye sueldo-bruto-a-neto-2026.test.json, 34 casos). `ops/gen_tabla_sueldo.py --check`: 23 filas OK.
- Lead, veredicto, 5 FAQ, ejemplo de la tabla (1.800 € → 1.478 / 1.408 / 2.952) y filas 1.500 / 2.000: coinciden con el motor (1.407,90 / 2.952,30 / 1.477,80; 14,20 %; 3.578 €; 19.984 €; 5,07 %; 10,36 %; 1.537 / 3.225 / 1.600; 1.229 / 2.572 / 1.326).

## Impacto del art. 68.6 (no modelado; cifras del script)
- 21.000 € (1.500 × 14), Madrid, sin hijos, alquiler 9.000 €/año: cuota estatal 1.262,31; deducción 900 ⇒ la diferencia pasa de −132,35 («no obligado: si no presentas, no pagas») a **+767,65 a devolver**. Hoy la página empuja a no declarar a quien perdería ~770 €.
- 25.200 € Madrid, alquiler 9.000: a devolver 228,05 → **1.128,05**. Afecta a casi toda la tabla (BI < 33.007,20 ≈ hasta ~37.000 € brutos).

## Cambios obligatorios (no edito la calculadora)
| # | Cl. | Archivo:línea | Texto actual → propuesto | Fuente |
|---|---|---|---|---|
| 1 | N/S | calcs/sueldo-bruto-a-neto-2026.js:93 (nota `noObligado`) | «…si no presentas la Renta, no pagas esa diferencia y tu neto es el de la nómina (X). Si la presentas por otro motivo, se liquidaría.» → añadir al final: « Pero si vives de alquiler, la nueva deducción estatal del 10 % del alquiler (art. 68.6 de la Ley del IRPF, Real Decreto-ley 29/2026, pendiente de convalidación) puede hacer que te salga a devolver: compruébalo antes de decidir no declarar.» | LIRPF 68.6 y 67.1.a (BOE-A-2026-20823, versión vig. 8-10-2026) |
| 2 | N | calcs/…js:100 (Límites) y content/sueldo-bruto-a-neto-2026.html:32 | «no incluye ascendientes, discapacidad, pensión compensatoria, deducciones, …» → «…, deducciones (tampoco la nueva deducción estatal del 10 % del alquiler de tu vivienda habitual, art. 68.6 de la Ley del IRPF, para bases imponibles de menos de 33.007,20 €: hasta 1.163 € menos de IRPF en la Renta, sin cambiar la retención de la nómina; está pendiente de convalidación y no está claro si cubre el alquiler pagado antes del 8 de octubre de 2026), planes de pensiones, …» | ídem; RIRPF 80-88 sin cambios |
| 3 | T | content/…html:6 | «…lo compara con lo retenido: la diferencia es lo que te devuelven o pagas al hacer la declaración.» → «…la diferencia es una estimación de lo que te devolverían o pagarías al declarar, sin deducciones (por ejemplo, la del alquiler, art. 68.6 de la Ley del IRPF).» | 68.6; texto ≤ cálculo |
| 4 | otros | content/…html:24 y calcs/sueldo-bruto-a-neto-2026.json:167 (sources, frase «la diferencia con el IRPF final no se paga si no presentas la Renta») | añadir: «; si pagas alquiler de tu vivienda habitual, declarar puede salirte a devolver por la deducción del art. 68.6» y en sources «ni deducciones» → «ni deducciones, incluida la estatal del 10 % del alquiler del art. 68.6 (RDL 29/2026)»; «Ley 35/2006 del IRPF, consolidada a 30/09/2026» → «consolidada a 8/10/2026» | 96.2.a + 68.6 |
Opcional (no bloquea): cuando se convalide el RDL 29 y se aclare 2026, añadir input «alquiler anual de tu vivienda» que reste min(10 % × min(alquiler, base máx.), cuota estatal) solo del IRPF final; el script ya trae `ded_alquiler()` como oráculo.

## Casos nuevos para test.json
Ninguno numérico (el motor no cambia). En ops/verif/sueldo-bruto-a-neto-2026.py: 68.6 cuota estatal 21.000 = 1.262,31; deducción 900; difRenta con deducción 767,65; 25.200 = 1.128,05 (lectura nuestra: la deducción no puede superar la cuota estatal tras la DA 61.ª).
Re-verificación: Sonnet releyendo las 4 frases + ambos scripts. Vigilar: convalidación del RDL 29 (si decae, quitar las menciones al 68.6).
