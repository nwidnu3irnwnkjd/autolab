# Reverificación · traspasar-fondo-o-reembolsar-irpf · 2026-10-02 (Sonnet, solo lectura)
Cambios aplicados: 6/6. Problemas pendientes: ninguno bloqueante.
- C1: ayuda de «otras» restringida a dividendos/intereses; content, FAQ 4, veredicto y «Qué no incluye» dicen que otras ganancias patrimoniales no se modelan y que reembolsar ahorra más (art. 49.1.b). Input separado no creado (opcional, Constructor); sesgo declarado.
- C2: «salvo ETF extranjeros comprados antes de 2022… DT 36.ª, no modelado» en lead, veredicto, FAQ 1, ayuda de vehiculo, content y JS.
- C3: description y primera frase condicionadas (sin que el dinero pase por tu cuenta / destino no ETF).
- C4: lead y opción sicav con «ningún momento de los 12 meses anteriores».
- C5: FAQ 2 y content con 500 socios/5 % por compartimento y destino no análogo a ETF.
- C6: homogéneos del año anterior o posterior, pérdida aplazada (art. 33.5.g).
- Extra: «La Cuenta… en vigor desde el 1/10/2026 y pendiente de convalidar» aplicado.
- Cifras ejemplo (6.180 / 91.224 / 87.994 / 3.229) coherentes con oráculo; oráculo: 0 discrepancias (816). check.py: 6398/6398 OK. Sin cifras legales nuevas sin fuente.
- Nota menor: caso de test nuevo de pérdida con otras ganancias (2.040 €) no existe porque el input no se modeló; no procede.
