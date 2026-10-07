# Re-verificación periódica · hipoteca-fija-o-variable · 2026-10-07 (Verificador, tarea 8)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 2 · 8 0 · N 1 · R 1 · S 0 · otros 2 (dato vivo/fallback, borde) · ninguno crítico (no cambia ninguna cifra publicada)

## Comprobado
- Oráculo nuevo independiente (mes a mes, revisión anual con recálculo de cuota): `ops/verif/hipoteca-fija-o-variable.py` → 2 fijos + 600 aleatorios JS vs Python, 0 discrepancias. `ops/check.py decidir` 13623/13623 OK (barómetro 141/141); `gen_ejemplos.py --check` 19/19 OK.
- A mano: (1) 150.000 €, 25 a, fija 2,80 %: cuota 695,81 €, intereses 58.744 €; variable 3,247+0,80 = 4,047 %: cuota 795,65 €, intereses 88.696 € → la fija ahorra 29.952 €, equilibrio 1,9018 % (= Ejemplo resuelto). (2) 200.000 €, 30 a, fija 3 %, Eur 2,10 +1, escenario +2: 103.554,90 vs 185.824,44 € (= test.json).
- Euríbor 3,247 % (sept. 2026): coincide con el BdE en BOE-A-2026-20519 (Euríbor 1 año 3,247 %). BOE-A-2026-20586 es el rendimiento de deuda 2-6 años (2,983 %): no afecta a esta calculadora. Sin novedades de Ley 5/2019 que toquen la página (no la cita; solo menciona bonificaciones en FAQ, correcto).
- live.json hoy: euribor12m ok=true, fecha_dato 2026-09-30, max_edad 45, fuente BCE; tipo_hipoteca_fija 2,76 % (ago.) ok=true. El fallo del bot de esta mañana ya se recuperó.
- Con ok=false: `calcs_loader._fresh` descarta el dato aunque esté dentro de max_edad y usa `params.euribor_12m` (3,247, igual hoy → sin efecto ahora). No usa datos obsoletos del live, pero ver cambio O1.

## Cambios
| # | Clase | Archivo · línea | Qué | Por qué |
|---|---|---|---|---|
| 1 | T | ops/gen_ejemplos.py:~101-104 (frase del veredicto, hipoteca-fija-o-variable) | «si el Euríbor medio de los 24 años siguientes al primero supera el 1,90 %» → «si el Euríbor se queda, de forma estable, por encima del 1,90 % durante los 24 años siguientes (con subidas y bajadas pesan más los primeros años)» | El umbral es para un Euríbor constante. Con media aritmética 1,975 % (> 1,90 %): una senda 1 %→2,95 % hace que la variable ahorre 8.123 €, y la inversa hace que cueste 11.449 € más (oráculo). La frase absoluta no se cumple. |
| 2 | T | calcs/…js (nota de `pintar`, «Euríbor medio de los próximos N años») · content/…html párr. 3 · json FAQ 1 | Mismo matiz: «Euríbor medio» → «Euríbor estable (medio)… los primeros años pesan más» | Lo mismo que el 1. Lo cambia el Constructor (no edito calcs/content). |
| 3 | N | calcs/…json input `fijo` (default 2.8 literal) / gen_ejemplos | La página muestra dos umbrales: 1,90 % (ejemplo, fija 2,80 %) y 1,86 % (bloque de datos, fija 2,76 % BCE). Pon `default_from: live.tipo_hipoteca_fija` con fallback params, o ejemplo con fijo 2,76 | El usuario ve dos «umbrales» distintos en la misma página y no se explica por qué. Además, DATOS_FIJOS de gen_ejemplos cita 2,76 %, que este ejemplo no usa. |
| 4 | R | calcs/…json `sources` | «valores oficiales publicados por el Banco de España… (BCE…)» → «Euríbor 12 meses, media mensual (BCE; el mismo valor oficial publica el Banco de España en el BOE)» | Mezcla dos atribuciones en una sola frase. Las cifras son correctas (BOE-A-2026-20519 = 3,247). |
| O1 | otros | projects/decidir/calcs_loader.py:32 `_fresh` | Aceptar ok=false si fecha_dato está dentro de max_edad_dias (como datos.py `_live`). El fallback a params no tiene control de edad ni de fecha: si el BCE falla más de 45 días, se mostraría un valor de params sin fecha («Parámetros actualizados» usa params.fecha) | Hoy, con un timeout, la calculadora y /datos/euribor-hoy/ podrían mostrar Euríbor de fuentes distintas. Con un fallo largo, el default quedaría obsoleto sin aviso. |
| O2 | otros (borde) | calcs/…js `euriborEquilibrio`/`pintar` | Con fijo = 0 (o variable siempre más cara), la bisección devuelve −5 y se muestra «equilibrio −5,00 %». Si eq ≤ −dif o eq ≥ 29,9, mostrar «la fija/variable gana con cualquier Euríbor». Además, `anosRestantes = anos − 1` no está redondeado (plazo 24,5 → «23,5 años») | Texto sin sentido en un borde poco frecuente. No cambia el veredicto. |

Casos para test.json (Constructor): {fijo 0 → eq −5 (hasta que se corrija O2)}; el ejemplo 3,247 % (diferencia 29.952,41, eq 1,9018).
Matemática correcta: cuota francesa, revisión anual única, tipo con suelo en 0 %, bisección en [−5, 30] sobre el Euríbor de los años 2 en adelante.
