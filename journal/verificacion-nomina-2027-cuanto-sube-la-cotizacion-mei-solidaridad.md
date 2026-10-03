# Verificación fiscal · nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad (Opus, 2026-10-03)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 3 · 8 1 · N 0 · R 0 · S 1 (no crítico) · otros 1 (patrón 6, default de base máxima)
Paso 0: mi interpretación coincide con el bloque INTERPRETACION (base = bruto/12 con prorrata; CC+MEI+desempleo+FP hasta B; solidaridad por tramos del exceso B·1,1 / B·1,5; reparto 4,70/28,30). Sin diferencia de modelo. Oráculo re-ejecutado: 800 casos, 0 discrepancias; mis 6 casos (ops/verif/<slug>.py): 0 discrepancias.

## Lectura propia del BOE (API, versión de fecha_vigencia más alta; 3/10/2026)
- DT 43.ª (dt-14, vig. 2023-04-01): «En el año 2027, será de 1 punto porcentual, del que el 0,83 corresponderá a la empresa y el 0,17 al trabajador»; 2026: 0,90 con 0,15 del trabajador. Orden PJC/297/2026 art. 16: 0,90 %, 0,15 % trabajador. **Punto 1 confirmado.**
- DT 42.ª (dt-13, vig. 2023-04-01): 2027 = 1,38 / 1,5 / 1,75; reparto: «mantendrá la misma proporción que la distribución del tipo general [...] por contingencias comunes». Art. 19 bis (a1-4, vig. 2025-01-01): tramos B→B+10 %, 10 %→50 %, >50 %; misma regla de reparto. Orden art. 17: 0,19/0,21/0,24 del trabajador (= 1,15/1,25/1,46 × 4,70/28,30 redondeado a 2 decimales); tramos 5.101,21-5.611,32 y 5.611,33-7.651,80 (= B·1,1 y B·1,5: bordes del modelo correctos).
- Orden art. 4 (CC 28,30; 4,70 trabajador), art. 2 (5.101,20 €/mes), art. 1.1 regla 2.ª (prorrata de pagas): citas correctas (muestreo de 3 citas: art. 1, art. 16, art. 17: correctas).
- DT 38.ª (dt-9): «Desde el año 2024 hasta el año 2050 [...] fijarán el tope máximo [...] se le sumará una cuantía fija anual de 1,2 puntos porcentuales». La base máxima sube por ley todos los años.

## Respuestas a los puntos críticos
1. MEI 0,17 (2027) / 0,15 (2026): literal en DT 43.ª y Orden art. 16. OK.
2. Solidaridad del trabajador 2027 (0,23/0,25/0,29): el **reparto sí está en la ley** (art. 19 bis y DT 42.ª, literal); solo el **redondeo a 2 decimales** no lo está (lo fija cada Orden; la de 2026 redondeó así, y 1,38/1,5/1,75 × 4,70/28,30 = 0,229/0,249/0,291). Es S no crítico (efecto ≤ 0,006 pp sobre el exceso: ≤ 1,3 €/año con 300.000 €) y ya está declarado en página y sources. Solo matizar el lead (cambio T3).
3. «Demás tipos 2027 = 2026»: defendible (CC 28,30/4,70 sin cambios desde hace años; además se cancelan en la diferencia) y declarado. **Base máxima 2027 = 2026: no engaña en el detalle (sección «Qué no incluye» da el +5 %: 215,52 € con 90.000 €), pero sí en el titular**: la DT 38.ª obliga a subirla cada año (revalorización + 1,2 puntos), así que para sueldos > 61.214,40 € la cifra del lead (23,64 €) es un mínimo, no la estimación central: la parte de base máxima pesa ~9 veces más. Cambio obligatorio (otros/patrón 6).
4. Bordes 12·B, 12·B+0,01, 12·1,1·B, 12·1,5·B: correctos y en test.json; añado temporal en 1,1·B y 1,5·B.
5. Absolutos: sin «siempre/nunca». IRPF declarado («el neto baja algo menos»; correcto: la cotización del trabajador es gasto deducible, art. 19.2.a LIRPF). FAQ «una sexta parte» = 4,70/28,30 = 0,166: OK. Cifras de lead/FAQ recalculadas (6,00; 23,64 = 12,24 + 11,40; 53,40; 336,52 → 338,49): OK.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | otros (patrón 6) | calcs/<slug>.json (lead, veredicto) y content (1.er párrafo) | Tras la cifra de 90.000 €, decir en el lead que la base máxima sube por ley cada año (DT 38.ª: revalorización + 1,2 puntos) y que, si sube un 5 %, con 90.000 € la subida sería 215,52 € al año (casi todo por la base, no por el MEI): la cifra con la base de 2026 es la subida mínima por encima de la base | El default es un escenario que la DT 38.ª descarta; hoy el aviso solo está en «Qué no incluye» |
| 2 | T | calcs/<slug>.js, pintar() | Si r.dBase ≠ 0: el veredicto debe nombrar la parte de base («y X por la base máxima que supones»), y la frase «solidaridad, que pasa de sol26 a sol27» no cuadra con dSol (90.000 y B27 5.356,26: «pasa de 59,28 a 63,00» pero dSol = 10,20). Usar la misma referencia (o quitar «pasa de… a…» cuando dBase ≠ 0). bigLabel «más al año en 2027 por MEI y solidaridad» → «más al año en 2027» (o condicional), y si sube < 0 «menos al año» | Texto ≤ cálculo: 12,96 + 10,20 ≠ 215,52 en el veredicto; con base 4.800 el número grande es −201,48 con etiqueta «más» |
| 3 | T | calcs/<slug>.json lead | «Estos son los tipos que la ley ya fija para 2027» → «La ley ya fija para 2027 el MEI y los tipos totales de solidaridad; la parte del trabajador en la solidaridad (0,23/0,25/0,29 %) es nuestro cálculo con la proporción legal, a falta de la orden de 2027» | La ley fija total y proporción, no el redondeo |
| 4 | T | content (escenario 1, JS) | En escenario 1 con dBase ≠ 0 (62.000 €, base 5.356,26: sube 61,92 de los que 49,56 por base) el veredicto atribuye todo al MEI («el MEI pasa… (12,36 más)») sin la parte de base | mismo motivo que 2 |
| 5 | 8 | calcs/<slug>.js | base27 < 5.101,20: avisar (no bloquear) que la DT 38.ª prevé subirla, no bajarla; el cálculo sigue | Combinación no prevista por la norma (patrón 8) |

## Casos nuevos para test.json (valores del oráculo; ops/verif/<slug>.py los ejecuta)
- 90.000 indef., base27 5.356,26: sube 215,52 · dMei 12,96 · dSol 10,20 · dBase 192,36 · sol26 59,28 · sol27 63,00 (ya existe el caso; añadir comprobación de texto del #2).
- 62.000 indef., base27 5.356,26: escenario 1 · sube 61,92 · dMei 12,36 · dSol 0 · dBase 49,56 · sol26 1,44.
- 90.000 indef., base27 4.800: sube −201,48 · dMei 11,52 · dSol 13,32 · dBase −226,32 (aviso #5).
- 91.821,60 temporal, base27 5.101,20: mes26 339,39 · mes27 341,42 · sube 24,36 · dSol 12,12.
- 67.335,84 temporal, base27 5.101,20: mes26 335,10 · mes27 336,32 · sube 14,64 · dSol 2,40.
- 1.000.000 indef., base27 5.101,20: sube 478,44 · dMei 12,24 · dSol 466,20 · solMes27 225,75.

## Re-verificación (Sonnet, sin navegar)
Ejecutar ops/verif/<slug>_oraculo.py y ops/verif/<slug>.py; releer lead, veredicto, bigLabel y las dos frases de pintar() de los cambios 1-4. Opus no hace falta: no cambia la interpretación legal.
