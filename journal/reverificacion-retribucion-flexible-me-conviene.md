# Reverificación · retribucion-flexible-me-conviene (2026-10-02, solo lectura)
RESULTADO: cambios aplicados 2/4 completos, 2 parciales. check.py decidir: OK 8420/8420.

| # | Cambio | Estado | Detalle |
|---|---|---|---|
| 1 | Guardería con pérdida art. 81.2 y ceder C − 1.000 € | APLICADO | js: veredicto añade pérdida, resultado (−166) y alternativa (ahorroAlt 556); json FAQ 1 y html (tabla y "Cómo decidir") condicionados; params.json recoge art. 81.2 y maternidad_guarderia_max 1000. Matiz: el titular/cifra grande sigue mostrando +834 y el "Ojo" va añadido al final (ganNum sigue 1, no pasa a 3). |
| 2 | 30 % ET 26.1 en supuestos | PARCIAL | Está en la nota del js y en la FAQ 3 del json, pero NO en la sección "Supuestos del cálculo" del html. |
| 3 | Absoluto condicionado | PARCIAL | js ("Normalmente se pacta contigo") y json FAQ 3 arreglados. En el html sigue "Y necesitas estar de acuerdo." en el punto "Que la ley te deja cederlo". |
| 4 | Frase de comida | APLICADO | "Pon como coste lo que ya ibas a gastar en comidas: si no, no es un ahorro. El máximo es 11 € ..." ya tiene sujeto. |

Tests nuevos: presentes (20 casos). "guardería 3.000 € con deducción por maternidad" (perdidaMat 1000, ahorroTrasMat −166, ahorroAlt 556) y "ceder 2.000 € de 3.000 €" (perdidaMat 0) coinciden con el informe. El informe pedía "veredicto con maternidad = 3", el test lleva ganNum 1 porque el código no lo cambia (ver matiz del 1).

Cifras/fuentes: 556 y −166 son derivadas del propio cálculo. Pendiente: el json cita "ET art. 41" y el html/sources no lo incluyen entre las fuentes (solo ET 26.1).

Pendientes: (a) añadir el 30 % con la especie ya cobrada a Supuestos del html; (b) quitar o suavizar "Y necesitas estar de acuerdo" en el html; (c) añadir ET art. 41 a sources o quitar la cita; (d) opcional: que el veredicto pase a 3 con maternidad.
