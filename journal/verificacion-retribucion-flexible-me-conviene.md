# Verificación fiscal · retribucion-flexible-me-conviene (Verificador Opus, 2026-10-02)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 2 (1 crítico) · R 0 · S 0 · otros 2

Norma leída hoy (API de consolidados del BOE, última versión de cada bloque): LIRPF art. 42 (versión de 1-1-2023), 43.1.1.º.d, 81 (1-1-2023); RIRPF arts. 44, 45 (1-1-2018), 46 (2017), 46 bis (2015); LGSS art. 147 (1-1-2023); ET art. 26 (2015). Ninguno tiene una versión posterior: el RDL 26/2026 no los toca (confirmado).

## Paso 0: interpretación propia frente al bloque INTERPRETACION del oráculo
Coincide en los puntos 1 a 5 y 7. Topes: 42.3.c, 500 € por persona y 1.500 € con discapacidad (el 1.500 € viene de la Ley 48/2015, con efectos en 2016, no de «2022» como pone la preverificación; la página no lo cita, así que no hay que tocarla). 42.3.e: 1.500 €. RIRPF 46 bis: 136,36 €/mes. RIRPF 45.2: 11 €/día solo en días hábiles y sin dietas exentas; el comedor directo no tiene tope. 42.3.b: guardería sin tope. Formación: 42.2.a no es renta solo si la exige el puesto (RIRPF 44); la página lo condiciona bien («que eliges tú»). La jornada partida no es requisito legal y la página no lo afirma. El «1.652,86 €» no aparece en el art. 42 vigente.
SS: el art. 147.2 empieza con «Únicamente» y ninguno de los 4 productos está en la lista: correcto que no baja. ET 26.1: máximo del 30 % y SMI en dinero (17.094 €, RD 126/2026): correcto.
Diferencia (punto 6): la fórmula de pérdida del art. 81.2 está bien, pero la pérdida no entra en el veredicto. Ver el cambio 1.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / artículo |
|---|---|---|---|---|
| 1 | N crítico | json (FAQ 1), html (tabla de ejemplos), js (veredicto de guardería) | «Guardería de 3.000 €: ahorras 834 €» se da sin condición. Una madre con derecho al art. 81 pierde hasta 1.000 € del incremento, así que el resultado neto queda en unos −166 € y el veredicto se invierte. El público típico de la guardería (hijo menor de 3 años, madre de alta) es justo el que tiene ese derecho. | Art. 81.2 LIRPF: no cuentan los gastos exentos por el 42.3.b. Hay dos opciones: añadir el input «¿aplicas la deducción por maternidad por este hijo?» y usar ahorroTrasMat en el veredicto, o condicionar la frase en FAQ, tabla y veredicto. Consejo que sí demuestra el cálculo: ceder C − 1.000 € mantiene el incremento (con 3.000 € ahorras unos 556 €). |
| 2 | N | html Supuestos y nota del js | El 30 % del ET 26.1 incluye todo el salario en especie que ya cobras (otros productos, coche), no solo este producto. | ET 26.1, «el salario en especie». Hay que decirlo en los supuestos. |
| 3 | otros (absoluto) | json FAQ 3 («la empresa no puede imponértelo»), nota del js («Hace falta tu acuerdo») | La frase es absoluta y la norma citada no la demuestra: el sistema de remuneración puede cambiarse por la vía de la modificación sustancial (ET art. 41.1.d) o por el convenio. | Cambiar por «normalmente es voluntario y se pacta contigo». |
| 4 | otros (texto) | js, nota de comida | Hay una frase rota: «si no, no es un ahorro.  como comida en días de trabajo…» (falta el sujeto). | Hay que completarla, por ejemplo «Solo puede usarse como comida…». |

## Supuestos (S)
- Valoración por el sueldo cedido: defendible. El art. 43.1.1.º.d valora estas rentas por el coste para el pagador, y la página lo declara.
- Criterio de la DGT sobre la sustitución de sueldo: la página lo declara como no contrastado, lo cual es aceptable (la ley no lo excluye).
- Tipo marginal: el cálculo usa la diferencia real de IRPF, no un tipo nominal, y la página lo explica.
- Prima repartida a partes iguales: declarado.

## Casos nuevos para test.json
- Guardería, 30.000 €, Madrid, C = X = 3.000: perdidaMat = 1.000 y ahorroTrasMat ≈ −166. Si se aplica el cambio 1, el veredicto con maternidad debe ser 3.
- Guardería, C = 3.000, X = 2.000: perdidaMat = 0.
