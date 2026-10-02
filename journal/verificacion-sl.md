# Verificación fiscal independiente (Opus) · autonomo-o-sociedad-limitada · 2026-10-02
VEREDICTO: PUBLICABLE CON CAMBIOS (3 obligatorios, ninguno cambia fórmulas ni cifras; 0 discrepancias numéricas)

## Norma leída hoy (BOE, API de legislación consolidada / diario)
LIS art. 29.1 (vers. Ley 7/2024, vig. 22/12/2024: 25 %; micro 17/20 % régimen final; 15 % nueva creación 1.er periodo con BI positiva y siguiente; exclusiones a) actividad transmitida por vinculadas, b) ejercida el año anterior por persona física con > 50 %; grupo; patrimoniales excluidas del 15/17/20 %) · LIS DT 44.ª ap. 2 (2026: micro < 1 M€ 19 % hasta 50.000 y 21 %; art. 101: 23 %) · LIRPF art. 20 (RDL 4/2024: 19.747,5 / 14.852 / 17.673,52 / 7.302 / 1,75 / 2.364,34 / 1,14; «rentas distintas del trabajo superiores a 6.500») · LIRPF art. 27.1 párr. 2.º · LGSS art. 308 (vers. RDL 13/2022, vig. 1/1/2023): 1.a regla 4.ª (305.2.b no puede elegir base < base mínima CC grupo 7), 1.c regla 1.ª (305.2.b: totalidad de rendimientos íntegros por participación en fondos propios con ≥ 33 % o administrador con ≥ 25 %, más los de trabajo en la entidad), regla 2.ª (deducción 3 %) · Orden PJC/297/2026 art. 3 (grupo 7: 1.424,40 €/mes) y art. 18 (MEI 0,90; tabla) · LSC arts. 4 (1 €; < 3.000 €: 20 % a reserva y responsabilidad solidaria hasta 3.000), 4 bis suprimido (ya no hay límite del 20 % a retribuciones), 274 (10 % hasta 20 % del capital).

## Cálculo
Oráculo del Constructor: 12 fijos + 560 aleatorios, 0 discrepancias > 1 €. Mío (Python escrito desde la norma, tablas IRPF/RETA tomadas de P; JS ejecutado con osascript), tolerancia 1 €, 6 escenarios, todos OK (incluido equilibrio por bisección propia con paso 50 €):
| caso (benef, sueldo, %div, CCAA, tipo, costes) | aut | SL | cuota SL | umbral |
|---|---|---|---|---|
| 60.000, 24.000, 50, Madrid, micro, 1.800 (defecto) | 40.486,79 | 27.505,59 | 5.435,30 | no se alcanza ≤ 400.000 |
| 100.000, 30.000, 100, Cataluña, nueva, 1.500 | 61.848,11 | 65.316,04 | 7.288,22 | 65.281,60 |
| 200.000, 0, 100, Valencia, reducida, 2.500 | 110.934,58 | 112.037,81 | 7.288,22 | 189.120,06 |
| 40.000, 15.000, 30, Andalucía, micro, 1.200 | 27.666,31 | 15.318,01 | 5.384,23 | no se alcanza |
| 90.000, 58.200, 100, Madrid, micro, 1.800 | 57.688,11 | 58.174,91 | 7.288,22 | 83.035,71 |
| 150.000, 40.000, 100, Asturias, micro, 1.800 | 88.122,02 | 94.235,02 | 7.288,22 | 76.177,99 |
Cifras del texto comprobadas: 135.281 (100 %), 79.419 (15 %), 83.036 (58.200 €), 99.621 (Cataluña), 40.487/27.506/13.851, 37.588, IS 6.498, cuotas 5.384 (1.424,40×31,5 %×12), 5.435, 6.547, 2.471. Verdicto en 4 escenarios (defecto, 100 %, 15 %, retribución > resultado): signo y textos coherentes. Desglose a mano del defecto (IS, cuota, IRPF general + ahorro con mínimos) cuadra al céntimo.

## Interpretaciones dudosas del Constructor
1. Base del socio = (retribución + dividendos íntegros del año) × 0,97, tramo general, mínima del tramo y ≥ 1.424,40: CORRECTA. La propia LGSS 308.1.c regla 1.ª dice «la totalidad de los rendimientos íntegros... derivados de la participación en los fondos propios» (por tanto también los de reservas de años anteriores, en el año en que se perciben, con el criterio del IRPF). Base mínima del tramo: es la opción legal más barata (sin regularización si está dentro del tramo). Aceptable declarada.
2. Solo RETA, sin cuota de empresa ni desempleo: CORRECTA (art. 305.2.b; queda fuera del RG).
3. Cuota RETA como gasto 19.2.a del sueldo, pagada por el socio, suelo 0: CORRECTA (criterio DGT reiterado); sin sueldo la cuota no se deduce: conservador y declarado.
4. Dividendos > 6.500 € anulan la reducción del art. 20: CORRECTA (capital mobiliario es renta distinta del trabajo; se computa el neto, aquí = íntegro).
5. DA 61.ª no aplica al administrador: CORRECTA.
6. Retribución deducible si está en estatutos (art. 217 LSC; art. 15.e LIS): ACEPTABLE DECLARADA.
7. Mínimo no absorbido a la base del ahorro, escala del ahorro única: CORRECTA (arts. 56.2, 66, 76).
8. Tipo IS a elección del usuario: ACEPTABLE pero el TEXTO sobrevende el 15 % (cambio 1).
9. Sin reserva legal ni retenciones: ACEPTABLE DECLARADA (con capital < 3.000 € la reserva del 20 % se agota en ≤ 3.000 € una vez; no invierte veredictos; la retención es pago a cuenta).
10-11. Autónomo con el modelo ya verificado; socio único, sin hijos ni otras rentas: ACEPTABLES DECLARADAS.
12. Umbral = último cruce (no monótono): CORRECTO y declarado («y ya no baja de ahí»); p. ej. sueldo 0, costes 0 cruza en 334.044.
Casos límite: beneficio 0/pérdida (bloqueado con aviso / tope de retribución sin pérdidas: correcto); retribución 0 permitida (cargo gratuito, art. 217) y se cotiza igual en RETA: aceptable para el socio único que trabaja en la sociedad; forales y Ceuta/Melilla fuera del selector: correcto.

## Cambios obligatorios
1. [patrón 1/3 · aplicabilidad del 15 %] calcs/…json `lead`, `veredicto`, `faqs[0][1]` y content/…html («Cómo decidir»): cada vez que se da 79.419 € añadir la condición: «solo si la actividad es nueva: si ya la ejercías tú como autónomo el año anterior y tienes más del 50 % de la SL, no se aplica (Ley 27/2014, art. 29.1.b), y dura dos periodos». Es justo el usuario objetivo de la página (autónomo que se plantea pasar a SL). En `inputs[4].options[1].t`: «Nueva creación con actividad nueva (no si la ejercías tú el año anterior): 15 %».
2. [patrón 2 · artículo omitido] LIRPF art. 27.1 párr. 2.º: si la SL presta servicios profesionales (Sección 2.ª de las tarifas del IAE) y el socio está en el RETA, lo que cobra por esos servicios es rendimiento de actividad económica, no del trabajo (sin los 2.000 € del 19.2.f ni la reducción del art. 20), y debe pagarse a valor de mercado (operación vinculada, art. 18 LIS). Declararlo en content/…html (Supuestos), `faqs[4][1]` («no incluye») y `sources`; efecto estimado de cientos de euros, no invierte el veredicto por defecto (≈ 450 € frente a 12.981 € de diferencia).
3. [patrón 5/6 · temporalidad] calcs/…js `pintar()`: si `d.tipo === "nueva"`, añadir a la nota: «El 15 % solo se aplica en el primer periodo con base imponible positiva y en el siguiente; después rige la escala de microempresa y el umbral sube (calcúlalo con esa opción).»
## Recomendados (no bloquean)
- `faqs[2][1]` y Supuestos del HTML: sustituir «el detalle reglamentario de qué dividendos cuentan no lo hemos contrastado» por la cita de LGSS 308.1.c regla 1.ª (cuentan todos los dividendos percibidos de la SL en el año) y mencionar el requisito de 90 días de alta para el 3 % y la base del grupo 7.
- `bigLabel` (JS): «…con tus datos de sueldo, dividendos, costes, tipo del IS y comunidad».
## Tests nuevos para test.json
Los 6 escenarios de la tabla (tol 1 €), sobre todo Cataluña/nueva/100 % (umbral 65.281,60), Valencia/reducida/sueldo 0 (189.120,06) y Asturias (76.177,99).
Re-verificación: Sonnet; solo releer las frases de los cambios 1-3 (no cambian el cálculo).
