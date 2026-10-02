# Verificación fiscal · traspasar-fondo-o-reembolsar-irpf (Verificador Opus, 2026-10-02)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 0 · R 0 · otros 5 · crítico: 1 (art. 49.1.b, modelo de pérdidas)
Fuente leída (API BOE consolidado BOE-A-2006-20764, 2/10/2026): art. 94 (versión Ley 11/2021), 95 ter (versión BOE-A-2026-20266, vigencia 1/10/2026), 101.6, DT 36.ª. Escala del ahorro contrastada con fiscal-fuentes 1.2 (A): 19/21/23/27/30, tramos 6.000/50.000/200.000/300.000; params coincide.

## Paso 0: interpretación propia
- Traspasar: 94.1.a 2.º párr.: no se computa ganancia ni pérdida y se conserva valor y fecha; solo 1.º reembolsos de fondos de inversión y 2.º transmisión de acciones de IIC societarias con >500 socios y sin >5 % del capital en ningún momento de los 12 meses previos; excluido si el importe se pone a disposición o si origen o destino es ETF/sociedad del mismo tipo (art. 79 RD 1082/2012). Extranjeras: 94.2.a (UCITS UE inscrita en CNMV, comercializador inscrito, 500/5 % por compartimento, no análogas a ETF) con la excepción DT 36.ª.
- Reembolsar: ganancia en base del ahorro, gasto de venta minora (35), pérdida: 49.1.b (primero con ganancias patrimoniales del ahorro sin límite, después 25 % de rendimientos del capital, resto 4 años).
- Coincide con el JS salvo la compensación de pérdidas (ver C1). Ejemplo recalculado a mano: 6.180 / 8.932 / 16.833 / 87.994 / 91.224: correctos.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| C1 | otros (crítico, patrón 2) | calcs .json (ayuda de «otras»), content (sección pérdidas, «Qué no incluye»), FAQ 4 | La ayuda define «otras» como «dividendos, intereses y otras ganancias» y el modelo limita la pérdida al 25 % de todo ello. Por ley, la pérdida patrimonial compensa SIN límite con otras ganancias patrimoniales del año y solo el saldo negativo restante compensa el 25 % de los rendimientos del capital (dividendos, intereses). Mínimo sin tocar calcs/: restringir la ayuda a «rendimientos del capital mobiliario (dividendos, intereses)» y decir en página y FAQ 4: «si además tienes otras ganancias patrimoniales este año, la pérdida las compensa enteras: reembolsar te ahorra más de lo que muestra». Ideal (Constructor): input separado de ganancias patrimoniales. | art. 49.1.b LIRPF |
| C2 | T (patrón 1) | FAQ 1, content «Qué no puede traspasarse», ayuda de «vehiculo», lead y veredicto («traspasar no existe») | Absoluto «No» / «no existe» para ETF sin la excepción: ETF extranjeros adquiridos antes del 1/1/2022 y no cotizados en bolsa española pueden traspasarse si el destino no es otro ETF. Añadir esa condición (sin modelarla) o «salvo ETF extranjeros comprados antes de 2022, ver DT 36.ª». | DT 36.ª y 94.2.a.3.º |
| C3 | otros (patrón 1) | json description y primera frase del lead | «Traspasar un fondo no tributa hasta reembolsar» y «no te cuesta IRPF hoy» van antes de la condición. Reescribir: «Traspasar un fondo de inversión a otro (no ETF), sin que el dinero pase por tu cuenta, no tributa hasta reembolsar». | 94.1.a párr. 3.º y 4.º |
| C4 | otros (patrón 4) | lead y opción «sicav» del select | «tienes el 5 % o menos del capital» no recoge el plazo: la ley exige no haber superado el 5 % en ningún momento de los 12 meses anteriores (FAQ 2 y content ya lo dicen bien). | 94.1.a 2.º |
| C5 | otros (patrón 3) | FAQ 2 y content «Qué puede traspasarse» | Para extranjeras faltan los 500 socios / 5 % por compartimento (la mayoría de los «fondos» extranjeros son SICAV con subfondos) y que el destino tampoco sea análogo a un ETF. | 94.2.a.2.º y 3.º |
| C6 | otros (patrón 4) | FAQ 4 y content pérdidas | «Si reinviertes en el mismo fondo en el plazo de 1 año, no se computa»: la norma dice homogéneos adquiridos en el año anterior o posterior, y la pérdida no se pierde, se integra al transmitir esos valores. Reescribir: «si compras participaciones del mismo fondo en el año anterior o posterior, la pérdida se aplaza hasta que las vendas». | art. 33.5.g y último párrafo del 33.5 |

## Comprobado sin cambios
- 94.1.a texto y redacción vigente (Ley 11/2021, efectos 2022), FIFO (94.1.a y 37.2), 101.6 (19 %, sin retención en traspaso), 95 ter.6 (excluye 94.1.a dentro de la Cuenta Financia Europa; RDL 26/2026 en vigor 1/10/2026, sin convalidar: bien citado como B y no modelado). Recomendable cambiar «La futura Cuenta» por «La Cuenta (en vigor desde el 1/10/2026, pendiente de convalidar)».
- Modelo: comparación correcta (reembolsar: impuesto hoy, reinversión con nuevo coste; traspasar: coste original y pago al final). Sesgo declarado del arrastre de 4 años (favorece a traspasar con pérdida): correcto, pero C1 añade un segundo sesgo en el mismo sentido que hay que declarar si no se modela.
- Umbral del 5 %: declarado como «criterio de esta calculadora» en «Cómo usar»; recomendable (no obligatorio) repetirlo en lead y veredicto junto a «empate práctico».
- Opción imposible (8): ETF/acción y SICAV que no cumple bloquean traspasar: correcto (salvo C2).

## Casos nuevos para test.json
1. valor 40.000, coste 50.000, otras = solo rendimientos 10.000: ahorro 525 € (se mantiene, ya en test).
2. Tras C1 con input de ganancias: pérdida 10.000, otras ganancias patrimoniales 10.000, rendimientos 0: ahorro de reembolsar 2.040 € (6.000×19 % + 4.000×21 %), no 0.
