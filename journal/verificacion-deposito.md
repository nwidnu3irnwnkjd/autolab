# Verificación fiscal independiente (Opus): deposito-letras-o-fondo-monetario · 2026-10-02
Nota: journal/verificacion-pendiente.md no tenía aún la sección del slug; se verificó con calcs/*.{js,json}, content/*.html, params.deposito_letras_2026 y ops/verif/deposito-letras-o-fondo-monetario.py.

VEREDICTO: PUBLICABLE CON CAMBIOS (5 obligatorios: patrón 1 ×1, 2 ×1, 3 ×1, 6 ×2; ninguno toca la escala ni las fórmulas fiscales)

## Comprobado con fuente propia (BOE consolidado descargado el 2/10/2026; Tesoro, resultados de subastas)
- Escala del ahorro 2026 (arts. 66.1 y 76 LIRPF): 9,5/10,5/11,5/13,5/15 % por mitad, tramos 6.000/50.000/200.000/300.000 → 19/21/23/27/30 %. VIGENTE. La autonómica la fija el art. 76 (las CCAA no la cambian): «no te pedimos la comunidad» es correcto.
- Retención 19 %: art. 101.4 (capital mobiliario) y 101.6 (reembolso de IIC; sin retención en traspasos). Pago a cuenta: correcto.
- Letras: art. 75.3.b RIRPF, sin retención en rendimientos de Letras, salvo las cuentas de entidades basadas en operaciones sobre Letras. Rendimiento = capital mobiliario (art. 25.2). CORRECTO.
- Fondo: art. 94.1.a, ganancia/pérdida al reembolso, traspaso diferido; integración en el ahorro (arts. 46, 49.1.b). CORRECTO.
- Art. 56.2: el mínimo sobrante reduce la base del ahorro; como el neto es monótono en el bruto (tipo marginal < 100 %), no cambia el orden. Bien declarado.
- FGD: art. 10.1 RDL 16/2011 y anexo del RD 2606/1996 (100.000 € por depositante y entidad). CORRECTO. Pero el art. 7 bis del RD 2606/1996 cubre aparte hasta 100.000 € en valores confiados a la entidad (ver cambio 4).
- Tesoro, subasta del 8/9/2026, 9 meses: precio medio 97,990, tipo medio 2,776 % (cuadra). P = 100/(1+i·d/360) → d = 266 días, no 273,75 (ver cambio 1).
- Oráculo del constructor: 618 casos, 0 discrepancias. Mis 4 escenarios (Python desde la norma, scratchpad): base 20.000/9 m; 150.000/12 m con otras 48.000 (cruza 50.000); 10.000/3 m con fondo −1 %; 500.000/6 m con otras 299.000 (cruza 300.000): 0 fallos > 1 €; los ganadores son letras/fondo/letras/depósito, así que «depende de los tipos y de tu tramo» es coherente. Forales → invalido 1; Ceuta/Melilla calcula; plazo 18 → se limita a 12 en calcular() (la página no pinta nada; aceptable porque el input tiene max=12).

## Cambios obligatorios
| # | Patrón | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | 6 (default sesgado) / 1 (fórmula) | calcs/*.js (g.Let), *.json (lead, veredicto, FAQ 1), content/*.html («Cuándo gana», supuestos) | Las Letras usan d = 365·m/12 días; las reales tienen otro plazo: la de 9 m del 8/9/2026 dura 266 días → 410,25 € brutos (≈ 332,30 € netos), no 422,18/341,97 €; el TIN de equilibrio es ≈ 2,735 %, no 2,815 %. Añadir el input «días hasta el vencimiento de la Letra» (default 266 con el ejemplo del 8/9/2026) y recalcular las cifras del ejemplo, o, como mínimo, declarar el supuesto y quitar las cifras presentadas como exactas. | Tesoro: tipo simple con los días reales, base 360. A 12 m (371 días) el error va en sentido contrario. En casos ajustados cambia el ganador. |
| 2 | 2 (mecánica que mueve la base) | *.json lead, veredicto, FAQ 1 y 5; content h2 «Por qué el impuesto no cambia el ganador»; nota del JS | Condicionar «el IRPF no cambia el orden»: «…salvo que tengas pérdidas patrimoniales (del año o pendientes de los 4 anteriores): compensan al 100 % la ganancia del fondo y solo hasta el 25 % los intereses del depósito y de las Letras, lo que favorece al fondo». | Art. 49.1.a y b LIRPF. |
| 3 | 3 (territorial) | nota del JS («Límites»), *.json FAQ 5 y sources, content «Qué no incluye» | Ceuta/Melilla: la deducción del 60 % solo afecta a las rentas obtenidas allí (p. ej., intereses de capitales invertidos en esas ciudades); en general no a las Letras, y no a los fondos (las IIC quedan excluidas para no residentes salvo que inviertan todo allí). Puede cambiar el orden: decirlo y no afirmar ahí que el impuesto no cambia el ganador. | Art. 68.4.1.º, 2.º y 3.º.f LIRPF. |
| 4 | 1 (absoluto) | *.json FAQ 4; content «Qué cubre cada una» | «no entra en ese fondo» → «el FGD no cubre el riesgo del Estado como emisor; si las tienes depositadas en un banco, el FGD de inversores cubre aparte hasta 100.000 € si la entidad no te las devuelve (art. 7 bis del RD 2606/1996)». | Art. 7 bis del RD 2606/1996. |
| 5 | 6 (redacción) | nota del JS («Con esa rentabilidad el fondo pierde dinero») | «tampoco lo recuperas en impuestos» es falso: la pérdida compensa otras ganancias, o hasta el 25 % de los rendimientos, y se arrastra 4 años. Cambiar por «la calculadora no compensa la pérdida con otras rentas (art. 49), lo que te devolvería parte en impuestos». El orden no cambia: el fondo sigue con neto negativo. | Art. 49.1.b LIRPF. |

## Recomendados (no bloquean)
- content, tabla de retención: «Ninguna si las compras en el Tesoro» → «Ninguna (art. 75.3.b RIRPF), también a través de un banco, salvo en cuentas basadas en operaciones sobre Letras»: tal como está, sugiere que por banco sí hay retención.
- Supuestos: «persona física residente en España»; precisar que las «otras rentas» son las del año del vencimiento o reembolso (imputación por exigibilidad).
- test.json: añadir un caso con días reales de la Letra (20.000 €, 2,776 %, 266 días → 410,25 € brutos) cuando entre el cambio 1.

## Supuestos
Aceptables: intereses al vencimiento; todo imputado en un ejercicio; comisión dentro del valor liquidativo (art. 26.1.a, no deducible aparte); retención solo informativa; mínimo 56.2 excluido (no cambia el orden); sin custodia; País Vasco y Navarra bloqueados; plazo de 1 a 12 meses.
Erróneos: duración de la Letra = 365·m/12 presentada con cifras exactas (cambio 1); «no recuperas en impuestos» (cambio 5).
Lo fiscal está bien: escala, tipos, retenciones y fórmulas del depósito y del fondo coinciden con la norma.
