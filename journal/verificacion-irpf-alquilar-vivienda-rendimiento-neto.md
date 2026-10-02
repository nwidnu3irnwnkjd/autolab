# Verificación fiscal · irpf-alquilar-vivienda-rendimiento-neto · 2026-10-02 (Verificador Opus, v3.2)
VEREDICTO: PUBLICABLE CON CAMBIOS (4 obligatorios, 4 recomendados). Interpretación del Constructor = la mía (sin 2.ª pasada Opus).

## Paso 0 · interpretación propia (desde la norma)
- RDL 26/2026, de 29/9 (BOE-A-2026-20266, BOE n.º 241 de 30/9/2026) EXISTE. DF 11.ª: vigor al día siguiente de publicación = 1/10/2026. Art. 6.Segundo.Dos reescribe el art. 23.2 (100/95/90/85/70 con rebaja > 5 %; 50 sin subida; 40/30/25/20/15 con subida; 1.ª vez 100/95/90/85/50; 70 social; 60 rehabilitación; 80 prórroga tácita; exclusión gran tenedor). Art. 6.Segundo.Catorce reescribe la DT 38.ª: contrato anterior a la entrada en vigor de la Ley 12/2023 (26/5/2023) → art. 23.2 a 31/12/2021 (60 %); entre 26/5/2023 y 1/12/2026 → art. 23.2 a 31/12/2025 (90/70/60/50, verificado en la versión consolidada de 1/1/2024). Fechas y porcentajes del Constructor: correctos.
- Si NO se convalida: la DT 38.ª anterior (consolidada, 1/1/2024) da el mismo 60 % a contratos < 26/5/2023 y el art. 23.2 de 2024 al resto → las ramas modeladas no cambian. Correcto.
- Art. 22.2, 23.1.a.1.º (límite intereses+reparación = íntegros, exceso 4 años), 23.1.b y RIRPF 14.2.a (3 % del mayor coste/catastral sin suelo): JS correcto (`fin = min(interep, ing)`, reducción solo si neto > 0).
- Fuera de plazo: el art. 23.2 (todas las versiones desde Ley 11/2021) solo exige autoliquidación antes del inicio de verificación/comprobación limitada/inspección; la página lo dice bien.
- Tipo marginal: el de entrada se aplica al neto reducido; tipos de ejemplo 30/37/45 % coherentes con irpf_2026 (estatal+autonómica, p. ej. 15+15, 18,5+18,5, 22,5+22,5).

## Cambios obligatorios
| # | Patrón | Archivo | Qué cambiar | Por qué / norma |
|---|---|---|---|---|
| 1 | 8 ¿opción existe? | calcs/…js (note «Rebaja de renta que compensa») y content/…html («Cómo usar») | Añadir: «el 90 % del texto de 2025 solo vale si el nuevo contrato se firma como tarde el 1/12/2026; los posteriores siguen el texto nuevo del RDL 26/2026 (si se convalida), con otros porcentajes». | DT 38.ª.2 (RDL 26/2026 art. 6.Segundo.Catorce). La columna sugiere firmar un contrato nuevo y quedan 2 meses. |
| 2 | 6 defaults/omitidos | calcs/…json (ayuda de `adq`) y content (Amortización) | Ayuda: «si no conoces el valor del suelo, multiplica el coste total de compra por el % de construcción del recibo del IBI (valor catastral construcción / total)». Añadir a límites: muebles y enseres cedidos (amortización aparte, RIRPF 14.2.b) no incluidos. | RIRPF art. 14.2.a, 2.º inciso: el suelo se calcula prorrateando el coste por los valores catastrales. Sin ayuda, el usuario mete el precio total y sobreestima la amortización. |
| 3 | 4 citas | calcs/…json `sources`, data/params.json `alquiler_irpf_2026.fuente` y `confianza` | No decir «texto consolidado con el RDL 26/2026» ni «art. 23 última versión 1/10/2026»: a 2/10/2026 el consolidado del BOE sigue mostrando art. 23 y DT 38.ª en la versión de 1/1/2024. Citar RDL 26/2026 art. 6.Segundo.Dos (art. 23.2) y .Catorce (DT 38.ª), url diario_boe/txt.php?id=BOE-A-2026-20266. `confianza`: B para lo que depende del RDL (regla de fiscal-fuentes) y añadir en la página: «si el Congreso no lo convalida, los porcentajes calculados no cambian y los contratos posteriores al 1/12/2026 seguirían con el texto de 2024-2025». | API consolidada a23/dt-6 consultada hoy; fiscal-fuentes §0.1. |
| 4 | 7 DT | content + note de límites del JS; preverif fila 7 | Añadir a límites: reducción del 80 % por prórroga tácita (art. 10.1 LAU) cuando el plazo mínimo de 5 años termina después del 1/12/2026, cualquiera que sea la fecha del contrato (renta ≤ índice de referencia, no gran tenedor): no calculada; puede afectar ya a rentas de diciembre de 2026. La afirmación «no aplica a 2026» es inexacta. | DT 38.ª párrafo final y art. 23.2 último párrafo (RDL 26/2026). |

## Recomendados (no bloquean)
5. Supuesto de amortización por meses: no es solo «criterio prudente», es el criterio de la AEAT (proporcional a días arrendados, Manual Renta, conf. C); cambiar la frase.
6. `tipo` máx. 60 → 54: el marginal general máximo 2026 es 24,5 + 29,35 (C. Valenciana) = 53,85 %.
7. Opción b70: si hay varios inquilinos, el 70 % solo se aplica a la parte de los que tienen 18-35 años (art. 23.2.b.1.º, texto 2025): añadir a la ayuda.
8. Límites: rentas distintas del trabajo > 6.500 € quitan la reducción del art. 20 y la deducción de la DA 61.ª (afecta a sueldos < 19.747,5 €); declarar fuera de plazo mantiene la reducción pero genera recargo del art. 27 LGT.

## Comprobado sin cambios
Ejemplo 800 €/30 %: 2.600 → 1.300, cuota 390, neto 5.810; 90 % → 6.122; rebaja que compensa 3,35 % (< 5 %, no da derecho al 90 %: lead correcto). 1.500 €/37 %: 9,39 %. Citas muestreadas: art. 22.2, 23.1.a.1.º, 23.1.b, RIRPF 14.2.a, 23.2 (inciso autoliquidación): literales correctos.

## Casos nuevos para test.json
- b70 con `tipo` 54 (borde superior tras el cambio 6).
- `adq` = 0 y `cat` > 0 ya cubierto; añadir `meses` 12 con `interep` = ingresos exactos (fin = ing, sin exceso).
