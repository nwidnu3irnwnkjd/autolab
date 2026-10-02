# Verificación fiscal independiente: autonomo-o-asalariado (Opus, 2026-10-02)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (cifras y fórmulas correctas; 6 cambios de texto obligatorios, 0 de cálculo).

## 1. Normativa (leída hoy en el BOE consolidado)
- Orden PJC/297/2026 (BOE-A-2026-7296): art. 18.1, tabla de 15 tramos (3 reducida + 12 general), bases mín./máx. y límites (< 1.166,70 / ≥ 1.166,70): **coinciden** con params y JS. Art. 18.2: 28,30 + 1,30 (+0,10 si no cubre AT, no aplica) y 0,90 MEI; art. 37.5-6 (cese 0,90; FP 0,10) → **31,50 % correcto**. RG art. 4.a, 33.2, 16: trabajador 6,50 / 6,55, empresa 30,65 / 31,85 **correctos**; art. 2.1 base máx. 5.101,20 ✓; art. 3 grupos 4-7 1.424,40 ✓; art. 17 solidaridad 1,15/1,25/1,46 con reparto 0,96-0,19 / 1,04-0,21 / 1,22-0,24 ✓.
- LGSS art. 308.1.c.1.ª (estimación directa: rendimiento computable = rendimiento neto + cuotas) y 2.ª (−7 % genéricos; 3 % solo societarios 305.2.b/e) ✓. Reglas 3.ª-4.ª: solo se regulariza si la base queda fuera de [mín, máx] del tramo real → **«cuota = base mínima del tramo» es la cuota mínima legal**: supuesto aceptable y bien declarado. Cálculo del tramo con el 5 % de difícil justificación dentro del rendimiento neto (RIRPF 30.2.ª: «5 % sobre el rendimiento neto, excluido este concepto») ✓. Punto fijo: la aplicación tramo→tramo es monótona, siempre existe; el menor es el legalmente alcanzable (quien cotiza por la base menor queda en ese tramo sin regularización) ✓.
- RIRPF 30.2.ª 5 %, máx. 2.000 € y LIRPF 30.2.4.ª ✓; la DA 56.ª (7 %) era solo 2023 y la DA 64.ª (2026) solo Ceuta (fuera del selector) ✓. LIRPF 32.2.3.º 1.620 € / −0,405 × (rentas − 8.000), rentas < 12.000 ✓; art. 20 (7.302 / 14.852 / 17.673,52 / 19.747,5) ✓; DA 61.ª (590,89; 17.094–20.048,45; RDL 5/2026) ✓; arts. 57-58 (5.550; 2.400/2.700/4.000/4.500) ✓. Muestreo de escala autonómica: Madrid (DLeg 1/2010 arts. 1-2) ✓.
- Tarifa plana: está en la **Ley 20/2007 (LETA) art. 38 ter**, no en la LGSS como dice la nota del Constructor (cuota reducida 12 meses, ampliable 12 más si rendimientos < SMI; cuantía en la LPGE, no leída hoy). No modelarla es aceptable si se declara mejor (cambio 2).
- **Omisión legal relevante:** LIRPF art. 32.2.1.º-2.º: autónomo con un único cliente no vinculado (o TRADE), gastos ≤ 30 %, ≥ 70 % de ingresos con retención y sin rendimientos del trabajo: −2.000 € y, si el rendimiento < 19.747,5 €, hasta −6.498 € adicionales, incompatible con el 5 %. Es justo el caso «mi empresa me ofrece pasar a autónomo». Efecto estimado: −250 € de facturación de equivalencia con 30.000 € y ~−500 € con 20.000 €. No cambia el sentido, pero hay que declararlo (cambios 3 y 4).
- Art. 32.3 (20 %): aplica al **primer período con rendimiento positivo y al siguiente**; el texto dice «primer año» (cambio 5).

## 2. Casos engañosos
- **No monotonía real (cambio 1, el único importante):** el neto cae en cada salto de tramo, así que hay franjas por DEBAJO de la facturación de equivalencia en que el autónomo ya gana. Ej. Madrid, 40.000 € brutos, 3.000 € gastos: equivalencia 46.213 €, pero con 46.000 € el JS dice «tendrías que facturar al menos 46.213 €… Con 46.000 € ganarías 63 € más». Contradicción visible. En una rejilla de 498 casos (17.094–100.000 €, 3 CCAA, G 0/3.000): 36 con franja previa > 5 €, máx. ~690 € (sueldos 18-19 mil). La definición («a partir de la cual ya no baja») es correcta; lo engañoso es «al menos» y «si es menor… cobrarías menos».
- Bruto < SMI bloqueado ✓; factura 0 o gastos > factura → cuota mínima de tabla reducida (2.470,57 €) y aviso ✓; grupos 1-3 declarados ✓; hijos «a cargo exclusivo» declarado (en pareja el mínimo se prorratea; afecta a ambos escenarios, efecto pequeño: aceptable).
- «Cada euro de gastos se factura además»: exacto en el modelo (todo depende de I − G; comprobado con G = 0/3.000/8.000/15.000: equivalencia − G = 33.402,19 € constante) ✓.

## 3. Texto ≤ cálculo
| Frase | ¿Demostrada? | Corrección |
|---|---|---|
| Lead/veredicto «Un autónomo tiene que facturar más que el bruto» | Sí en el modelo (mín. +2.541 € con G = 0, 17.094–150.000 €, 3 CCAA, 0/3 hijos); **no** con tarifa plana el 1.er año | Añadir «sin tarifa plana» en la primera frase del lead y del veredicto |
| Tabla HTML 20/30/40/60 mil (neto, coste, equivalencia) | Sí, recalculada por mí: 16.829/26.130/26.690; 23.452/39.195/36.402; 30.196/52.260/46.213; 42.184/78.390/65.647 | — |
| «33 % … 9 %», «unos 3.030 €/mes», FAQ 1 y 3 (26.700/36.400/65.600; 26.100/39.200) | Sí | — |
| «Con sueldos bajos puede superar el coste de la empresa» | Sí (con 3.000 € de gastos, hasta ~20.500 €) | — |
| FAQ 2 (31,50 %, desglose, 653,59 → 206 €/mes, 1.928,10, 5.101,20, art. 308) | Sí | — |
| FAQ 5 «el autónomo resta… 5 %… 1.620 €» | Incompleta (falta 32.2.1.º) | Cambio 4 |
| HTML «si es menor que la cifra de equivalencia, cobrarías menos» | No siempre | Cambio 1 |
| HTML «la cuota de autónomos es fija aunque un mes no factures» | Parcial (se regulariza con los rendimientos anuales, 308.1.c) | Cambio 6 |
| «reducción del 20 % del primer año» (FAQ 4, HTML, nota JS) | No exacta (art. 32.3: dos períodos) | Cambio 5 |
No hay promesas de ventaja; los supuestos (bruto/12, sin AT/EP, base mínima del tramo, EDS, año completo, sin IVA) están declarados en HTML y nota.

## 4. Cambios obligatorios
1. calcs/autonomo-o-asalariado.js (verdict): si `d.factura < r.facturaIgual` y `r.ganador === "autonomo"`, no decir «al menos»: p. ej. «A partir de X siempre cobras más como autónomo; con tu facturación (Y) también, porque estás justo antes de un cambio de tramo de la cuota: si facturas algo más, la cuota sube y podrías quedar por debajo». Cambiar «tendrías que facturar al menos X» por «a partir de X € al año sin IVA cobras siempre lo mismo o más». content/…html «Cómo decidir»: añadir «salvo franjas estrechas (de hasta unos cientos de euros) justo antes de un cambio de tramo de la cuota».
2. calcs/…json (lead, veredicto) y content/…html: «Sin contar la tarifa plana del primer año, un autónomo…»; sustituir «La tarifa plana no se modela porque no está verificada» por «La tarifa plana (Ley 20/2007, art. 38 ter: cuota reducida los 12 primeros meses, ampliable 12 más si tus rendimientos no llegan al SMI) abarata mucho esos meses; el resultado es el de un año sin ella». No dar la cuantía (80 €) sin leer la norma que la fija.
3. content/…html (Supuestos) y nota JS «No incluye»: «Si trabajas para un único cliente no vinculado y cumples los requisitos del art. 32.2 de la Ley del IRPF (gastos ≤ 30 %, ≥ 70 % de ingresos con retención…), tienes una reducción mayor que el 5 % (2.000 € y hasta 6.498 € más con rendimientos bajos) y la facturación necesaria sería algo menor».
4. calcs/…json FAQ 5: tras «1.620 € de reducción» → «(hasta 1.620 € si sus rentas no llegan a 12.000 €; si trabaja para un único cliente y cumple los requisitos del art. 32.2.1.º, en lugar del 5 % resta 2.000 € y hasta 6.498 € más)».
5. calcs/…json FAQ 4, content/…html, nota JS: «reducción del 20 % del primer año…» → «reducción del 20 % del IRPF del primer año con beneficios y del siguiente (art. 32.3)».
6. content/…html: «la cuota de autónomos es fija aunque un mes no factures» → «la cuota se paga cada mes aunque ese mes no factures (al año siguiente se regulariza con tus rendimientos reales)».
Opcional: fiscal-fuentes §5.2 y verificacion-pendiente: corregir «art. 38 ter LGSS» → «Ley 20/2007 art. 38 ter».

## 5. Ejecución
- Oráculo del Constructor: 9 fijos + 520 aleatorios, 0 discrepancias > 1 € (28 s).
- Mi modelo propio (Python desde la norma, tramo por tramo eligiendo el menor consistente; equivalencia con rejilla de 1 € + bisección; en scratchpad, no en el proyecto) vs JS en 7 escenarios: Madrid 20k (tabla), SMI Andalucía temporal 1 hijo, Cataluña 55k 3 hijos tramo 11, Valencia en el borde reducida 3/general 1, Madrid 40k (franja no monótona), Galicia 60k temporal 2 hijos 15.000 € de gastos, Madrid 60k (tabla): **0 discrepancias > 1 €** en neto asalariado, coste, cuota, IRPF autónomo, neto autónomo y equivalencia.
- Casos nuevos para test.json: {bruto 40000, factura 46000, gastos 3000, madrid, 0, indef} → netoAutonomo 30258,72; ganador «autonomo»; facturaIgual 46213,16 (guarda el texto del cambio 1). {bruto 25000, factura 17060, gastos 2000, valencia, 0, indef} → cuotaReta 3211,75 (tabla reducida, tramo 3); facturaIgual 30509,74.
Re-verificación: Sonnet (solo textos 1-6 y los 2 casos nuevos); no cambia la interpretación legal.
