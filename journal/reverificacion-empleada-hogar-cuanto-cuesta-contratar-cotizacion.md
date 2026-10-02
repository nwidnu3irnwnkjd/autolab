# Reverificación · empleada-hogar-cuanto-cuesta-contratar-cotizacion · 2026-10-02 (solo lectura)
RESULTADO: cambios aplicados 3/3 (uno con un resto menor en el HTML).

1. DA 3.ª bis «cuotas a cargo del empleador»: aplicado. Supuestos del content, FAQ 4, veredicto, sources/params (convenciones_propias c) y json lo dicen igual: 20 % a CC por literal, 45 % referido a cuotas del empleador y aplicado solo a CC (lectura prudente), ≈9 €/mes menos si se aplicara a más.
2. Familia numerosa: aplicado. Input «fam» opción «si», lead y veredicto exigen título, alta del pagador de cuotas y dedicación exclusiva a cuidar a la familia; el HTML añade el requisito de alta y título en el momento de contratar en Supuestos.
3. Salto de tramo: aplicado en el veredicto json («con contrato indefinido, la reducción del 20 % y 20 horas semanales o menos»). RESTO MENOR: en el content HTML, el ejemplo «El salto de tramo: con 9 horas semanales y un sueldo mensual de 877,00 € … 174,82 € / 216,02 €» no dice «contrato indefinido y reducción del 20 %». Recomendable añadirlo (no cambia cifras).
4. Varias familias: coherente. El HTML dice que cada una cotiza por su relación laboral (art. 15.1) y la calculadora sirve para cada una; calcula una relación, no suma ni promete lo no modelado. Matiz: la nota del JS y las sources aún listan «varias familias a la vez» como no incluido (compatible: no se modela la suma, pero conviene alinear la redacción).
5. Absolutos / cifras legales nuevas sin fuente: ninguno detectado; todas las cifras ya estaban en params.json con fuente.

Comandos: check.py decidir -> OK 9912/9912 comprobaciones (avisos ajenos: diesel, tipo_hipoteca_fija); qa_static --fiscal --changed -> 1 calculadora, sin avisos, 0 BLOQUEANTE, 0 AVISO.
