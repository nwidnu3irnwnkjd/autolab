# Verificación fiscal · empleada-hogar-cuanto-cuesta-contratar-cotizacion · 2026-10-02 (Verificador Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 1 · N 0 · R 0 · S 1 · otros 1 (absoluto) · críticos 0 (ninguno cambia cifras ni veredicto)
Normas leídas hoy en el BOE: Orden PJC/297/2026 arts. 2.1, 15, 16, 35 y 37 (Diario); LGSS DA 61.ª (CNAE 97 0,80+0,70=1,50); RDL 16/2022 DA 1.ª y DT 3.ª (consolidado, redacción RDL 2/2024); RDL 1/2023 DA 3.ª bis (añadida por RDL 2/2024); RD 126/2026 arts. 1 y 4; RD 1620/2011 art. 8.

## Paso 0: mi interpretación frente a INTERPRETACION del oráculo: coincide
- Escala de 8 tramos, límites y bases (329/306 … 1.424,40/1.424,40; 8.º desde 1.424,41 = retribución, tope 5.101,20) literal del art. 15.1; prorrata de pagas (art. 147.1 LGSS) y base mínima por SMI equivalente (art. 15.2.a-c): OK, igual que el JS.
- Tipos 2026: CC 23,60/4,70 (15.3); MEI 0,75/0,15 (16); AT/EP 1,50 empleador (15.4 + DA 61.ª); desempleo 5,50/1,55 indefinido y 6,70/1,60 temporal, Fogasa 0,20 (art. 35): sí, el empleador paga desempleo en 2026. Sin FP: el art. 35 no la incluye y el art. 37 no la extiende al hogar. OK.
- 20 % de CC + 80 % de desempleo y Fogasa (DA 1.ª.1): OK. 45/30 % por renta (DA 1.ª.2): «en los términos y condiciones que se fijen reglamentariamente», sin reglamento: bien no modelado.
- 45 % familia numerosa: solo cuidadora exclusiva (DA 3.ª bis.2), una sola persona, sustituye al 20 % y no excluye el 80 % (DT 3.ª solo excluye el «párrafo primero» y el apartado 2): corrección del Constructor confirmada. «Bonificación por conciliación»: no existe en estas normas; la página no la menciona. OK.
- SMI: 1.221 €/mes (RD 126/2026 art. 1) → 17.094 €/año; 9,55 €/h por horas externa con todo incluido (art. 4.2 en relación con art. 8.5 RD 1620/2011); prorrata de jornada (art. 8.1); pagas: cuantía pactada que garantice el SMI anual (art. 8.4). OK.
- Cifras de la página recalculadas a mano (base 785: 174,82 / 247,67 / 128,50; 1.424,50: 317,24; mínimo 20 h mensual 712,25): coinciden.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | S | content (Supuestos, 2.º punto) y json (FAQ 4, veredicto) | El 2.º supuesto justifica aplicar el 45 % solo a CC porque «el texto habla de la aportación empresarial por contingencias comunes»: eso vale para el 20 % (DA 1.ª.1), no para el 45 %. La DA 3.ª bis.1 dice «bonificación del 45 por ciento de las cuotas a la Seguridad Social a cargo del empleador». Redactar: «el 20 % se aplica a las contingencias comunes, como dice la norma; el 45 % la norma lo refiere a las cuotas a cargo del empleador y la calculadora lo aplica solo a contingencias comunes (lectura prudente): si la Seguridad Social lo aplica a más cuotas, tu coste es algo menor (≈ 9 €/mes en el ejemplo)». La FAQ 4 («45 % de las cuotas») y el veredicto («reducción … del 45 %») deben decir lo mismo que el cálculo (sobre contingencias comunes, supuesto propio). | RDL 1/2023 DA 3.ª bis.1-2 |
| 2 | 8 | json (input fam, opción «si») y lead | La bonificación exige además que quien paga las cuotas esté «en situación de alta, o en situación asimilada a la de alta, con obligación de ingreso de cuotas» y tenga el título «en el momento de la contratación». La opción solo pide título y cuidado: añadir «y tú (quien paga las cuotas) estás de alta en la Seguridad Social». Cambiar «solo cuida de personas» (lead) y «solo cuida de personas de la familia» por «se dedica exclusivamente a cuidar a los miembros de la familia o a quienes conviven en casa». | DA 3.ª bis.1 y 2 |
| 3 | otros (absoluto) | json (veredicto, última frase) | «con 20 horas semanales o menos, un sueldo de 877,01 € … sube de 174,82 € a 216,02 €»: las cifras son solo con contrato indefinido y la reducción del 20 %. Añadir «con contrato indefinido y la reducción del 20 %». | cálculo |

## Recomendado (no obligatorio)
- N: la página excluye «a quien trabaja para varias familias», pero la escala se aplica «por cada relación laboral» (art. 15.1): cada familia cotiza por su propia relación y la calculadora sirve para cada una. Puede decirse así en vez de excluirlo.

## Supuestos S (por prioridad)
- horas/mes = semanales × 52/12: defendible y declarado. Pagas = una mensualidad: defendible (art. 8.4) y declarado. MEI sin reducir: correcto (art. 16 lo separa de CC). 20 % solo a CC: literal. 45 % solo a CC: ver cambio 1. Base elevada al tramo del SMI cuando se paga menos: literal art. 15.2 y aviso en el resultado. Las 13 líneas S con literal comprobadas por muestreo (15.1, 15.2, 15.3, 16, 35, DA 61.ª, DA 1.ª.1, DT 3.ª, DA 3.ª bis, RD 126 arts. 1 y 4, RD 1620 art. 8): todas coinciden.

## T/8/N/R
- T: DT 8.ª RDL 8/2023 (bases 2026 sin LPGE) citada en el propio art. 15.1: OK. DT 3.ª RDL 16/2022 (bonificaciones de art. 9 Ley 40/2003 vigentes el 1-4-2024): se mantienen con igual incompatibilidad; sin efecto en la cifra.
- 8: interna por horas no existe (art. 8.5 solo externa): bien, no es opción. Más de 40 h efectivas: bloqueo correcto (art. 9.1). Familia numerosa: cambio 2.
- N: todo lo no modelado tiene frase y sentido del efecto. R: RDL 26/2026 no toca estas normas: OK.

## Casos nuevos para test.json
Ninguno obligatorio (los cambios son de texto). Opcional: fam=si con temporal (comprueba que el 80 % se mantiene con el 45 %): horas 20, 10 €/h, temporal → base 785, cuota empleador = 101,89 + 5,89 + 11,78 + (52,60+1,57)×0,2 = 130,38.
