# Reverificación · pension-viudedad-cuanto-cobro · 2026-10-02 (Sonnet, solo lectura)
Cambios aplicados: 3/3. Problema pendiente: 1 (ejemplo obsoleto).
- C1 aplicado: JS usa el límite literal por edad (19.373,60 / 21.704,60 / 22.548,80) y avisa con el alternativo 27.034,40 (alt); content "Supuestos" y "70 %" citan «en función de la edad» con las 3 cifras; params limite_70_literal y nota presentes.
- C2 aplicado: nota `mant` del JS y "Supuestos" explican ingresos del año anterior, viudedad aún no cobrada y posible pérdida del 70 %; «no se sabe con certeza» eliminado.
- C3 aplicado: «mujeres con hijos y, en algunos casos, hombres» en NO_MODELA y content.
- Casos nuevos en test.json presentes (BR 1.200/66/1 hijo sin alt; BR 3.000/50/1 hijo con alt 1.931,03). Oráculo: 0 discrepancias (730). check.py: 6398/6398 OK.
- Sin absolutos ni cifras legales nuevas sin fuente (todas en params viudedad_2026).
## PENDIENTE
- content/pension-viudedad-cuanto-cobro.html, lista de ejemplos: «Base de 2.000 €, 45 años, 2 hijos y 6.000 € de ingresos: 70 %, 1.400 € al mes» ya NO coincide con la calculadora (con el límite literal da 52 %, 1.040 € al mes, más aviso de hasta 1.400 € con la lectura favorable). Corregir el ejemplo (el test.json ya espera 52 %). Aviso de 70 % reducido: el mismo caso BR 2.000 original del Opus (955,26) no sale como 70 % porque 52 % es mayor.
