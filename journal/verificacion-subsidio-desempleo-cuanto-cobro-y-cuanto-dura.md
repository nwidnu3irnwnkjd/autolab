# Verificación fiscal/legal · subsidio-desempleo-cuanto-cobro-y-cuanto-dura · 2026-10-02 (Verificador Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 1 · N 3 (1 crítico) · R 0 · S 0 · otros 2

## Paso 0: norma leída hoy (API BOE consolidado BOE-A-2015-11724, última versión de 274, 275, 277, 278 y 280 = RDL 2/2024, vigencia 23-5-2024)
- 274.1.a/b, 274.2 (rentas propias O responsabilidades familiares), 275.1-3 (75 % SMI sin pagas; suma unidad / miembros), 277.1 (tabla con rowspan: «No» <45 ≥360 d y >45 ≥120 d -> ambas 6 meses; «Sí» indiferente ≥120 -> 24, ≥180 -> 30), 277.2 (90/120/150/180 -> 3/4/5/6 o 21), 278 (95/90/80 por días 1-180/181-360/361+), 280.1-2-4-6 (≥52 cumplidos, jubilación salvo edad, 6 años por desempleo, solo renta propia, 80 % IPREM, extinción 272.d): coinciden con el bloque INTERPRETACION del oráculo. Sin diferencia de interpretación.
- Cifras: 600 x 0,95/0,90/0,80 = 570/540/480; 1.221 x 0,75 = 915,75; x3 = 2.747,25; 30 meses = 3.420 + 3.240 + 540 x 16 = 15.300; 6 meses = 3.420; 21 meses = 10.980; 3 meses = 1.710; 55 años: 120-144 meses, 57.600-69.120. Todo correcto.
- IPREM 600 y SMI 1.221 (RD 126/2026) ya verificados en fiscal-fuentes.md (< 30 días): sin cambios. RDL 26/2026 (vivienda): 0 menciones a desempleo/subsidio/IPREM/8/2015 en el texto: correcto no citarlo. T: DT 1.ª RDL 2/2024 agotada; ninguna DT gradúa 274-280 en 2026.
- Citas por muestreo (274.1.a, 277.1, 278, 280.4, 275.1): literales correctos.
- Supuestos S: mes de 30 días (defendible, declarado); 45 exactos como «>45» (la tabla tiene hueco en 45; 274.1.a solo exige 360 d al «menor de 45»: defendible); cota 65-67 (205.1.a; en 2026 la DT 7.ª da 66 a 10 m / 38 a 3 m, que cae dentro de la cota): correcto; cargas con al menos otro miembro (275.2-3): correcto. Sin cambios.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / artículo |
|---|---|---|---|---|
| 1 | N **crítico** | calcs/…json input `renta` (label) + content (Requisito de renta y Supuestos) + nota «Cómo sale» del JS | Añadir: «No cuentes el sueldo ni el paro que ya no cobras el día de la solicitud: las rentas del trabajo y las prestaciones públicas que no se mantienen en esa fecha no computan (art. 275.5.e)». | 275.5.e: «Las rentas del trabajo y las prestaciones públicas percibidas por la persona solicitante que no se mantengan en la fecha de la solicitud» no son renta. Hoy el label pide «trabajo, prestaciones» del mes anterior: quien acaba de agotar el paro (p. ej. 1.100 € el mes anterior) lo mete y ve «la opción no existe». Cambia el veredicto del usuario principal. |
| 2 | 8 | JS (verdict y bigNumber cuando d52) + content (Ejemplo mayor de 52) | Con `d52`, no presentar 570 € «durante 6 meses» y además 480 € como si se sumaran: decir que son subsidios alternativos (no se cobran a la vez) y que, si cumples el art. 280, el subsidio que corresponde es el de mayores de 52 (art. 274.3); la cifra grande debe ser 480 €. | 274.3 y 280.1: quien cumple los requisitos del 280 es beneficiario de ese subsidio; hoy la cifra principal (570) puede no existir para él. |
| 3 | N | calcs/…json input `dias` (label) + FAQ 4 | Para cotización insuficiente: «días cotizados que no hayas usado ya para una prestación o subsidio anterior (el informe de vida laboral no los descuenta)». | 269.2 (por remisión del 274.1.b) y 277.2 párr. 2: cotizaciones ya computadas no sirven; mismo hallazgo que en la calculadora del paro. |
| 4 | N | calcs/…json input `jub` (label) + FAQ 5 | «por ejemplo, 15 años cotizados, 2 de ellos en los últimos 15 años». | 280.1 remite a todos los requisitos de jubilación salvo la edad: 205.1.b exige los 2 años dentro de los 15 últimos. |
| 5 | otros (redacción) | calcs/…json `veredicto` | «con más de 52 años» -> «con 52 años o más». | 280.1: «tengan cumplida dicha edad»; el JS usa edad ≥ 52 (bien). |
| 6 | otros (redacción) | content (Requisito de renta) y FAQ 3 | «cónyuge o pareja e hijos a cargo» -> «cónyuge o pareja, o hijos a cargo (basta uno)». | 275.2-3: la unidad con solo cónyuge cuenta; el JS ya lo modela así (miembros > 1); el texto sugiere que hacen falta ambos. |

## Casos nuevos para test.json
- agotado, 360 d, 40 años, 0 hijos, cónyuge no, renta 0 (paro de 1.100 € del mes anterior ya no se cobra) -> derecho 6 meses, 3.420 € (el caso documenta el cambio 1 en el label; el cálculo no cambia).
- agotado, 360 d, 55 años, jub sí, renta 0, 0 hijos -> winner derecho52, bigNumber 480 (cambio 2).
- agotado, 360 d, 40 años, 0 hijos, cónyuge sí, renta 1.500, rentaOtros 0 -> derecho por cargas (750 €/persona), 30 meses, 15.300 € (cambio 6).

## Re-verificación (Sonnet)
Sin cambio de interpretación ni de fórmula: releer solo las frases de los cambios 1-6 y comprobar que el JS con d52 muestra 480 como cifra principal; ejecutar el oráculo del Constructor (adaptar el caso d52 si cambia el winner/bigNumber).
