# Verificación fiscal · compensar-perdidas-ganancias-irpf-antes-fin-de-ano · 2026-10-02 (Verificador Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 1 · N 1 · R 1 · otros 1 (orden de compensación: fórmula)
Norma leída: BOE-A-2006-20764 consolidado (API, 30/09/2026): arts. 33.5.e-g y último párrafo, 37.2, 46, 48, 49 (v. 1/1/2015), 66.1 y 76 (v. 22/12/2024), DA 12.ª, DA 39.ª, DT 7.ª; RDL 26/2026 (BOE-A-2026-20266) art. 6; AEAT Manual Renta 2025 cap. 12 (base del ahorro, Fase 1.ª/2.ª).

## Paso 0: interpretación propia vs bloque INTERPRETACION
- Coincide: dos cajones (49.1.a/b), 25 % fijo (la DA 12.ª fijó 10/15/20 % solo para 2015-2017; nada para 2026), arrastre 4 años, 2022 caduca tras 2026, 33.5.f/g y diferimiento, FIFO 37.2, escala 19/21/23/27/30 % con cuotas 0/570/5.190/22.440/35.940 por mitad (correcta; el 28 % es la escala anterior a 2025).
- DIFIERE (punto 2 del oráculo): el orden. AEAT, Manual 2025: «Fase 1.ª» compensa el ejercicio (incluido el 25 % entre cajones del saldo negativo del año) y solo después, «Fase 2.ª», los saldos de ejercicios anteriores contra el saldo positivo «una vez minorado» y con el 25 % «conjuntamente» y «antes de compensaciones». JS y oráculo aplican primero el saldo antiguo (supuesto atribuido al art. 49.2, que no fija ese orden).
  - Caso A (rcm 8.000, saldo 2022 2.000, vende 6.000): cuota igual, pero el JS da arrastre 6.000 y 0 caducado; correcto: arrastre 4.000 y **2.000 € del saldo de 2022 caducan**. El veredicto omite justo el aviso que la página promete («un saldo de 2022 caduca»).
  - Caso B (gp 1.000, otras −1.000, saldo 2023 500): base JS 375 €; correcta 250 € (cuota 71,25 → 47,50).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | otros (fórmula) | calcs/*.js + oráculo del Constructor | En `liquidar`: 1.º nuevo saldo negativo de b contra 25 % de a, y saldo negativo de a contra 25 % de b (ejercicio); 2.º saldo antiguo contra b restante y luego contra el 25 % restante de a (límite conjunto sobre a antes de compensaciones) | Art. 49.1 («obtenido en el mismo período» primero; los anteriores «en el mismo orden») + AEAT Manual 2025 Fase 1.ª/2.ª. Referencia: ops/verif/<slug>.py |
| 2 | otros (texto) | content «Supuestos» + json/preverif | Cambiar «se compensa primero con las ganancias del año … empezando por el más antiguo» por el orden AEAT: primero lo del año, después saldos anteriores con lo que quede | Igual que 1 |
| 3 | 8 | content «Qué no incluye» o FAQ 2 + ayuda del input `perdida` | Fondos de inversión: el traspaso entre fondos no genera la pérdida (art. 94.1.a); solo el reembolso. Fondos no cotizados: plazo de recompra 1 año (33.5.g); ETF cotizados: 2 meses | Si no, la opción «vender» no existe para quien piensa hacerlo por traspaso |
| 4 | R | content «Qué no incluye» + sources/params | Añadir: activos dentro de una Cuenta de Ahorro e Inversión Financia Europa (art. 95 ter LIRPF, RDL 26/2026, sin convalidar y aún no comercializada): sus pérdidas no se integran hasta la disposición. Matizar «el RDL 26/2026 no toca estos artículos» → «no modifica los arts. 33, 37, 46, 49, 66 y 76; añade el art. 95 ter» | Art. 6 RDL 26/2026, art. 95 ter.3 y 95 ter.5 |
| 5 | T | content «Qué no incluye» + sources | DA 39.ª: decir que no aplica en 2026 (rentas anteriores a 2015 + 4 años: caducadas); quitar la idea de que «puede permitir compensar más» (preverif) | DA 39.ª.1, plazo de 4 años |

## Recomendado (no bloquea)
- N: recompra parcial: solo deja de computar la parte de la pérdida correspondiente a los valores homogéneos recomprados (criterio DGT); el input sí/no es todo o nada: avisarlo en la ayuda de `recompra`.
- Citar la DA 12.ª al decir «25 % fijo» (hubo calendario 2015-2017).

## Comprobado sin cambios
Lead, veredicto y FAQs: cifras del ejemplo (2.610 → 1.560 €, 1.050 €, 10.750 €; 1.560 → 1.140 €, 420 €, 4.000 €) recalculadas a mano. Citas muestreadas: 33.5.f (2 meses), 37.2 (FIFO), 49.1 (25 % y 4 años): literales correctos. Mínimo personal sobre el ahorro y forales: declarados.

## Casos nuevos para test.json (ya en ops/verif/compensar-perdidas-ganancias-irpf-antes-fin-de-ano.py, hoy FALLAN: 3/3)
1. gp 0, perd 0, rcm 8.000, otras 0, prev 2.000, anio 2022, no, perdida 6.000 → baseCon 6.000, ahorro 0, arrastreCon 4.000, caducaCon 2.000.
2. gp 1.000, perd 0, rcm 0, otras −1.000, prev 500, anio 2023, no, perdida 0 → baseSin 250, cuotaSin 47,50.
Re-verificación: Sonnet (no cambia la interpretación de la ley, solo el orden ya documentado por la AEAT): ejecutar ops/verif/<slug>.py + oráculo corregido y releer las frases de los cambios 2-5.
