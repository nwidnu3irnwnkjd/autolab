# Verificación fiscal · loteria-navidad-premio-neto-hacienda · 2026-10-02 (Verificador Opus, v3.5)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 1 · R 0 · S 1 · otros 1 · críticos 0 (ninguno cambia cifra ni veredicto)
Fuente leída: LIRPF consolidada, API BOE (bloque datrigesimatercera, versión vigente desde 05-07-2018, Ley 6/2018 art. 67.1) + texto completo (búsqueda de «trigésima tercera»).

## Paso 0: interpretación propia (coincide con INTERPRETACION del oráculo)
- Gravamen especial por décimo, fracción o cupón (apdo. 1, último párrafo). Exento hasta 40.000 € inclusive («igual o inferior»); tributa el exceso (apdo. 2). Tipo 20 % (apdo. 4); retención o ingreso a cuenta 20 % sobre la base (apdo. 6), que practica el pagador (arts. 99 y 105 LIRPF; lo ingresa con su modelo 230). El premiado solo autoliquida (modelo 136) si no hubo retención (apdo. 7), p. ej. premios de entidades UE/EEE. No integra la base del IRPF; la retención no minora la cuota líquida ni da devolución (apdo. 8).
- Titularidad compartida: prorrateo de la cuantía exenta (apdo. 2, párr. 3) y de la base (apdo. 3, párr. 3) «en función de la cuota». LITERAL de la ley, no criterio administrativo: compartir no multiplica los 40.000 €. Correcto en JS, oráculo y página.
- Lo que NO es literal: que si cobra uno solo sin acreditar cotitularidad el gravamen recae íntegro en él y la entrega posterior es donación (ISD). Es criterio de la AEAT/DGT (prueba de la cotitularidad al cobro); defendible, pero hay que atribuirlo.
- Importe vigente 2026: 40.000 € (sin PGE 2026; RDL 26/2026 no toca la DA 33.ª). Tablas 2.º-5.º premio: no usadas.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | otros (absoluto, patrón 1) | calcs/...js, nota np>1 | «si cobra uno solo y reparte, el reparto es una donación» → «puede ser una donación sujeta al ISD de tu comunidad» | Contradice la página («puede ser») y no lo demuestra la norma (depende de la prueba de cotitularidad y de la normativa autonómica) |
| 2 | S | content + json (lead, veredicto, bloque «Si cobra uno solo») y JS esc 4 | Atribuir: «según el criterio de la Agencia Tributaria, si no se acredita la cotitularidad al cobrar, el gravamen recae sobre quien cobra…» | No está en la DA 33.ª; es criterio administrativo |
| 3 | N | content «Qué premios entran» y NO_MODELA/«otros organizadores» | Añadir apdo. 1.b: premios de organismos públicos o entidades sin ánimo de lucro de otros Estados UE/EEE con fines idénticos también tributan por este gravamen (sin retención española: autoliquidación, modelo 136). «Otros organizadores» → «organizadores privados o de fuera de la UE/EEE (tributan en el IRPF general)» | Hoy la página da a entender que solo entran los de 1.a |
| 4 | T | data/params.json (consolidados) y preverif línea T | «importe exento de 40.000 €, desde 2019» → «desde 2020»; existe la DT 35.ª LIRPF (10.000 € en 2018 tras el 05-07-2018, 20.000 € en 2019), que el grep de preverif no detectó | Sin efecto en 2026; corrige la fuente |

## Puntos verificados sin cambio
- Gordo 2025: 4.000.000 € por serie (10 décimos de 20 €) = 400.000 €/décimo; estructura estable del sorteo; presentado correctamente como ejemplo editable, no dato 2026. Confianza B aceptable.
- Bordes 40.000,00 exento / 40.000,01 sujeto 0,01 (retención 0,002 → 0,00): correctos.
- Forales PV/Navarra: solo aviso (bien). Ceuta/Melilla: art. 68.4 no afecta al gravamen especial. No residentes: aviso IRNR (bien). ISD: aviso (bien).
- Absolutos «definitivo», «no se retiene nada», «no se declara en la renta»: demostrados por apdos. 2, 7 y 8.
- Citas por muestreo (apdos. 1, 4, 8): coinciden con el texto.
- Ámbito 8: bloqueos premio ≤ 0, 0 décimos, 0 personas, negativos: correctos.

## Tests nuevos
Ninguno de cifra. Re-verificación Sonnet: releer solo las frases de los cambios 1-3 y el campo de params del cambio 4.
