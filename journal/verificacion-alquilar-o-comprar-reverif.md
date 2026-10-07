# Re-verificación alquilar-o-comprar (tarea 8, alto tráfico) · Verificador Opus · 2026-10-07
Oráculo propio: ops/verif/alquilar-o-comprar.py (saldo por fórmula cerrada, carteras mes a mes, sensibilidades fiscales). Exit 0.
**VEREDICTO: PUBLICABLE CON CAMBIOS (cálculo correcto; 1 texto que contradice al cálculo en un borde, 2 supuestos por declarar).** T 2 · 8 0 · N 2 · R 1 · S 0 · otros 0 · ninguno crítico para el ejemplo por defecto.

## Resultados del oráculo
- JS vs oráculo: 9 casos fijos + 3 de test.json + 600 aleatorios (precio 60-900k, tipo 0-7 %, plazo 5-40, horizonte 1-40, revalorización −3/7, rentab −2/9) → **0 discrepancias** (> 0,01 €).
- (1) Ejemplo resuelto: comprar 204.271,93 · alquilar 171.500,41 · **+32.771,52 €** · cuota 843,21 · coste 1.143,21 · **cruce año 9** (año 8: −3.376; año 9: +1.105). Coincide con ejemplos.json, description y test.json. «Si vendes antes, gana alquilar»: cierto.
- Supuestos implícitos (2) cuantificados sobre el ejemplo: impuestos del ahorro (art. 66/76 LIRPF) sobre las carteras → +48.156, año 8 (omitirlos favorece a alquilar: conservador, declarado). IBI+comunidad +2 %/año → +29.714, año 9 (declarado). **Deducción estatal del 10 % del alquiler (RDL 29/2026, LIRPF 68.6; máx. 1.163 €; BI < 33.007,20 €; pendiente de convalidación) → +9.401, año 13**: cambia mucho el ejemplo para un inquilino con derecho y hoy solo se cubre con «desgravaciones». Deducción por vivienda habitual (suprimida para compras desde 1-1-2013): bien no modelada. Gastos de venta: sí (3 %). Plusvalía municipal (IIVTNU) e IRPF de la venta: no modelados; la FAQ dice «posible plusvalía de la venta» (ambiguo).
- (4) Subida del alquiler: default 2 %, editable, constante 15 años. Defendible: coincide con el tope de la DF 6.ª RDL 29/2026 (actualización anual máx. 2 % hasta 31-12-2027, pendiente de convalidación) y con la revalorización por defecto (2 %). Pero el tope solo rige dentro del contrato y hasta 2027; al renovar manda el mercado. Sensibilidad: 1 % → +17.142, año 11; 3 % → +49.749, año 8. Falta decirlo en la ayuda.
- Borde (texto ≤ cálculo): 5/600 aleatorios y casos plausibles con rentab ≫ revalorización y horizonte largo tienen 2 cruces. Ej.: defecto + revalorización 3 %, rentab 6,5 %, horizonte 40 → veredicto «alquilar te deja 178.986 € más» y a la vez la nota «comprar empieza a superar a alquilar a partir del año 10: si vas a vivir ahí menos tiempo, alquilar sale mejor» (comprar gana solo de los años 10 a 26). Contradicción visible.
- (3) Absolutos: lead/veredicto/FAQ usan «suele» y «con estos supuestos»: OK. H1 con «N años» literal (se publica tal cual en dist): parece un marcador sin rellenar.

## Cambios
| # | Clase | Archivo · línea | Qué | Por qué |
|---|---|---|---|---|
| 1 | T | calcs/alquilar-o-comprar.js:56-57 | Calcular también el último año con comprar > alquilar; si `diferencia <= 0` y `anosEquilibrio > 0`: «comprar supera a alquilar entre los años X e Y, pero al final del horizonte vuelve a ganar alquilar e invertir». En la rama eq = 0 cambiar «necesitaría más años, más revalorización…» por «necesitaría más revalorización, menos rentabilidad o, según el caso, más años» (con rentab 7 % la diferencia empeora con los años). | Nota contradice al veredicto (borde de 2 cruces); «más años» no siempre lo demuestra el cálculo. |
| 2 | T | calcs/alquilar-o-comprar.json:5 | H1 «¿qué sale mejor a N años?» → «¿qué sale mejor según los años que te quedes?» (o «a 10, 15 o 20 años»). | «N» literal en el H1 publicado. |
| 3 | N | calcs/alquilar-o-comprar.json:128 (FAQ «Qué no incluye») | Añadir: «Tampoco la deducción estatal del 10 % del alquiler de vivienda habitual (RDL 29/2026, pendiente de convalidación; máx. 1.163 €/año, base imponible < 33.007,20 €): si tienes derecho, resta ese importe del alquiler; en el ejemplo, comprar pasaría a ganar por unos 9.400 € y desde el año 13». Y «posible plusvalía de la venta» → «plusvalía municipal ni IRPF de la ganancia al vender». | Supuesto que cambia el año de cruce del ejemplo (9→13) para un perfil amplio. No modelar hasta la convalidación (~18-nov). |
| 4 | N | calcs/alquilar-o-comprar.json:131 (sources) | Añadir «no existe deducción por compra de vivienda habitual para compras desde 2013; el alquiler sube cada año el % indicado durante todo el horizonte». | Declarar hipótesis implícitas. |
| 5 | R | calcs/alquilar-o-comprar.json:82 (ayuda de «Subida anual del alquiler») | «Hasta el 31-12-2027 la actualización anual dentro del contrato no puede superar el 2 % (RDL 29/2026, DF 6.ª, pendiente de convalidación); al renovar o cambiar de piso el alquiler sigue al mercado: prueba también 3 %.» | Default 2 % defendible, pero el tope es temporal y solo intra-contrato. |
| — | opcional | content/alquilar-o-comprar.html:12 | «Mira el año de equilibrio… si con tus datos hay dos cruces, mira también desde qué año vuelve a ganar alquilar». | Coherencia con el cambio 1. |

## Casos nuevos para test.json (valores del oráculo, tol 1)
1. defecto + horizonte 8 → diferencia −3.375,98 · anosEquilibrio 0 (borde: un año antes del cruce).
2. defecto + horizonte 9 → diferencia 1.104,73 · anosEquilibrio 9 · patrimonioComprar 132.302,28.
3. defecto + revaloriza 3, rentab 6,5, horizonte 40 → comprar 1.003.695,77 · alquilar 1.182.682,20 · diferencia −178.986,44 · anosEquilibrio 10 (doble cruce; tras el cambio 1, la nota debe decir «entre los años 10 y 26»).
4. defecto + subida 1 → diferencia 17.142,34 · anosEquilibrio 11.
5. defecto + interes 0, entrada 0 → diferencia 156.315,90 · anosEquilibrio 3.
Re-verificación tras el cambio 1 (Sonnet): `python3 ops/verif/alquilar-o-comprar.py` (exit 0) y releer la nota del caso 3.
