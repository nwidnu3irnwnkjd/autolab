# Verificación independiente (Opus) · capitalizar-paro-o-cobrarlo · 2026-10-02
VEREDICTO: NO PUBLICAR (error de modelo que invierte el veredicto; corregible, requiere nueva pasada Opus corta porque cambia la interpretación legal)

## Fuentes consultadas hoy
BOE consolidado: Ley 20/2007 (LETA) arts. 33 y 34 (añadidos por art. 1.8 de la Ley 31/2015); RD 1044/1985 arts. 1-7 (autónomos suprimidos en 1992: confirmado); Ley 35/2006 art. 7.n (sin límite de importe, 5 años de actividad: confirmado). SEPE: cuantías 2026 (IPREM 600; mín. 560/749; máx. 1.225/1.400/1.575; interés legal 3,25 %: confirmado), hoja informativa del pago único (≥ 3 meses pendientes, 4 años, solicitud previa, documentación en 1 mes: confirmado) y FAQ «¿Cuándo me pagarán las cuotas?»: la subvención se mantiene «mientras continúes en la actividad... o hasta agotar el total de la cuantía de la prestación».

## Hallazgo 1 (patrón 2, modelo; OBLIGATORIO) · la subvención de cuotas no se pierde, se cobra hasta agotar el importe
El JS/oráculo paga la subvención solo durante msub = n·(1−X/V) meses (sub = msub × cuota) y da por perdida la diferencia. Según art. 34.1.2.ª Ley 20/2007 («calculada en días completos de prestación») y el SEPE, la cuota mensual consume días de prestación y se sigue abonando mientras sigas de alta hasta agotar el importe pendiente no capitalizado. Lo que se pierde frente a cobrar es solo el interés legal descontado (y el riesgo de cesar antes de agotarlo), no «la prestación menos la cuota».
Mis 4 escenarios (Python desde la norma; T y V coinciden con el JS < 1 €; capTotal NO):
| caso (n, BR, hijos, cobrados, inversión, cuota) | capTotal JS | capTotal norma | coste JS | coste norma |
| 12, 1.500, 0, 0, 6.000, 205,88 (defecto) | 7.181,72 | 11.596,37 | 4.518 | 104 |
| 18, 4.000, 2, 0, 20.000, 300 | 21.489,87 | 27.821,83 | 6.860 | 528 |
| 9, 900, 1, 4, 3.000, 205,88 | 4.016,98 | 6.699,82 | 2.724 | 41 |
| 24, 2.000, 0, 0, 0, 350 | 8.400,00 | 28.950,00 (en ~83 meses de alta) | 20.550 | 0 |
Oráculo del Constructor: 18 + 600, 0 discrepancias, pero comparte la misma interpretación errónea (no detecta el fallo).
Corrección: resto R = T − X·T/V (días no capitalizados) abonado como subvención fija de sm/mes durante R/sm meses mientras dure el alta; mostrar esa duración y avisar de que si cesas antes pierdes lo no cobrado. Si se descuenta o no el interés legal sobre la parte subvencionada: no lo fija la norma con claridad (SEPE: «en cualquier caso se descontará el interés legal»); declarar como supuesto (capTotal entre X+R y V).

## Hallazgo 2 (patrón 2/6, modelo; OBLIGATORIO) · «cobrar mes a mes» siendo autónomo solo es posible 270 días
Art. 33 Ley 20/2007: compatibilizar la prestación con el alta por cuenta propia «por un máximo de 270 días», pedido en 15 días. Fuera de eso, el alta como autónomo suspende (o extingue, según duración: LGSS arts. 271-272, a contrastar) la prestación. Comparar con cobrar los n meses enteros mientras ejerces la actividad no es una opción legal si n > 9. Corregir: la opción «cobrar» del que se hace autónomo = min(n, 9) mensualidades por compatibilidad (el resto, solo si cesa y reanuda), o reformular como «no hacerte autónomo todavía». El aviso actual no basta: los números del veredicto lo contradicen.

## Hallazgo 3 (patrón 4, cita legal; OBLIGATORIO)
El art. 34 (y el 33) son de la Ley 20/2007, del Estatuto del Trabajo Autónomo, añadidos por la Ley 31/2015; la Ley 31/2015 no tiene un art. 34 propio. Cambiar en content/capitalizar-paro-o-cobrarlo.html (2 citas «Ley 31/2015, art. 33/34» y su enlace a BOE-A-2007-13409 #a34/#a33), calcs/…json (fuentes) y data/params.json `capitalizar_paro_2026.fuente`/`url_ley_31_2015`.

## Cambios por archivo (todos obligatorios)
- calcs/capitalizar-paro-o-cobrarlo.js: subTotal = R (no msub×sm); mesesSub = R/sm; coste = T − X − R (± interés, según supuesto); opción cobrar con compatibilidad ≤ 9 meses; rehacer veredicto y nota («la parte que no capitalizas solo te paga la cuota... perderías» → «la parte no capitalizada se cobra como cuota mensual durante N meses mientras sigas de alta»).
- content/…html: lead, «Capitalizarlo», 4 ejemplos (7.182/11.700, 2.471 en 12 meses, 21.022/7.328), «Cómo decidir» punto 1 y supuestos: recalcular y quitar «solo te paga la cuota y capitalizar sale más caro» y «Si puedes financiar tú la inversión, cobrar mes a mes deja más dinero en total» (no demostrado tras la corrección); citas de la Ley 20/2007.
- ops/verif/capitalizar-paro-o-cobrarlo.py y calcs/…test.json: reescribir la subvención con la regla «hasta agotar»; añadir mis 4 casos (tabla) como tests (tolerancia 1 €; ajustar si se adopta el descuento de interés sobre la subvención); caso n = 12 para la opción cobrar con 270 días.
- params.json: corregir fuente/URL (hallazgo 3).

## Supuestos
Aceptables (declarados): descuento por interés simple k/12; X proporcional; subvención = cuota con suelo de la base mínima (205,88 €; regla 2.ª a); inversión incluye tributos y ≤ 15 % asesoramiento (regla 1.ª); IRPF no modelado y su sesgo; tarifa plana «no verificada/no modelada» (art. 38 ter remite a la LPGE: correcto); bloqueos sin actividad nueva y < 3 meses (RD art. 2: confirmado), ya+n > 24 (LGSS 269); inversión > V capada; exclusiones declaradas (negocio, cese de actividad, cuenta ajena, subsidio, discapacidad, bonificaciones, foral, sociedades). Añadir a «no incluye»: la cotización del desempleado que el SEPE descuenta de la prestación mensual (no verificado si se aplica al pago único).
Erróneos: subvención limitada a msub meses (H1); comparación con n meses cobrados siendo autónomo (H2).
Correctas: 70/60 % (art. 270.2), topes y mínimos 2026, IPREM 600, interés 3,25 %, 7.n sin límite + 5 años, plazo de 1 mes (RD 4.1/7), solicitud previa al alta (regla 3.ª), 24 meses sin compatibilizar (regla 4.ª), art. 5.2 RD.
Pre-verificación del Constructor: línea 1 (absolutos) OK; línea 2 falla (subvención y compatibilidad); 3 OK; 4 falla en la cita (Ley 20/2007); 5 bordes OK salvo los que dependen de H1; 6 omitidos: H2 no era un «límite declarable», cambia el ganador.

## Re-verificación (Opus, 2026-10-02, tras H1-H3)
VEREDICTO: PUBLICABLE CON CAMBIOS (2 retoques de texto menores; no requieren otra pasada Opus, basta Sonnet releyendo las 2 frases)
- Escenarios (osascript contra el JS actual, tolerancia 1 €): mis 4 + 2 bordes (n = 6 sin inversión: empate 5.040; n = 9 con inversión > V: −118) → 0 discrepancias en T, V, subvención, total capitalizado y total con compatibilidad. Ejemplos del HTML recalculados (defecto 11.596/9.000; 12.000 € → 11.501; sin inversión ~57 meses; 2 hijos 27.822/14.175, 38 meses; n = 9 → 8.920 vs 9.000): coinciden.
- H1 bien aplicada: R = T − X·T/V se cobra como subvención fija = max(cuota, 205,88) durante R/cuota meses mientras dure el alta (art. 34.1.2.ª Ley 20/2007 + FAQ SEPE «hasta agotar»); se quitó el tope por prestación media (correcto: la cuota consume días, el total no cambia). El supuesto del interés sobre la parte subvencionada está declarado con su rango (V … capTotal).
- H2 bien aplicada: cobrar siendo autónomo = min(n, 9) mensualidades (art. 33); el resto, declarado como no modelado (suspensión/extinción, consultar al SEPE).
- «Con n ≤ 9 gana cobrar por el interés legal»: cierta. Con n ≤ 9, Tc = T y capTotal = T − X·(T/V − 1) ≤ T; la diferencia es exactamente el interés del pago único. Si no hay pago único (X = 0) es empate, no «cobrar gana». Con n > 9 la diferencia siempre favorece a capitalizar (≥ 3 mensualidades frente al interés). No sesga, con dos matices que el texto debe condicionar (abajo).
- Citas: 0 apariciones de «Ley 31/2015, art.» en HTML y JS; enlaces a BOE-A-2007-13409 #a33/#a34; en el .json, «Ley 20/2007 … añadidos por la Ley 31/2015» (correcto).
Cambios (texto, content/capitalizar-paro-o-cobrarlo.html):
1. Lead y «Cómo decidir», punto 1: «capitalizarlo te deja más dinero en total» → añadir la condición «si sigues de alta hasta agotar la subvención (en el ejemplo, unos 27 meses; sin inversión, casi 5 años)» y que la subvención llega repartida en ese tiempo. Hoy la condición solo aparece después; la frase principal es un absoluto sin condición (patrón 1).
2. «Con 9 meses o menos pendientes, cobrar mes a mes te deja algo más (el interés legal)» (lead y «Cómo decidir») → «… si capitalizas algo; sin pago único, recibes lo mismo».
Opcional: «Supuestos» repite «la reanudación de la prestación» dos veces.
