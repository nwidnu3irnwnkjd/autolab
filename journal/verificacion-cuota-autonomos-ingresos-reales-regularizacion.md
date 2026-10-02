# Verificación fiscal · cuota-autonomos-ingresos-reales-regularizacion (Verificador Opus, 2/10/2026)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 1 · R 2 · otros 1 · fórmula 0 · críticos 0 (ninguno cambia cifras)
Método: norma leída en la API consolidada del BOE hoy (LGSS arts. 308 y 327; RGC arts. 45, 43 bis y 46; RDL 13/2022 DT 1.ª; RDL 3/2026 art. 3 [BOE-A-2026-2548]; Resolución de convalidación BOE-A-2026-4668; Orden PJC/297/2026 art. 18). Oráculo del Constructor re-ejecutado: 1.500 casos, 0 discrepancias.

## Paso 0: interpretación propia vs INTERPRETACION del oráculo
Coincide en todo: tramo con rendimiento × 0,93 (LGSS 308.1.c.2.ª); base elegible entre la mínima del tramo previsto y 5.101,20 (DT 1.ª.2 RDL 13/2022, prorrogada por RDL 3/2026 art. 3.4); regularización por PROMEDIO mensual de bases provisionales frente a mín./máx. del tramo real (RGC 46.2 reglas 2.ª, 3.ª y 5.ª: confirmado que se compara la media, no mes a mes); tipo 31,5 % (Orden art. 18.2: CC 28,30, CP 1,30, MEI 0,90; cese 0,90 y FP 0,10).

## Puntos críticos pedidos
1. Tabla 2026: cotejada línea a línea con Orden art. 18.1 (= params). RDL 3/2026 art. 3.4: tabla de 2025 de la DT 1.ª RDL 13/2022 «hasta la aprobación de la Ley de PGE», solo la base máxima de tramos 11-12 sube al tope de 5.101,20 (art. 3.1). Convalidado (Resolución 26/2/2026, BOE-A-2026-4668). OK.
2. Tipo total 31,50 % y cuota = base × 31,5 %: OK. Reducción pluriactividad 0,055 × cuota CC (Orden 18.2.a): OK.
3. Plazos: NO hay discrepancia ley/reglamento. El «31 de mayo» era la redacción original del RDL 13/2022; la DF 10.1 del RDL 14/2022 (BOE-A-2022-12925, vigente desde 1/1/2023) la cambió: hoy el art. 308.1.c.4.ª LGSS dice «antes del 30 de abril del ejercicio siguiente», igual que RGC 46.2.5.ª.c. Rige el 30 de abril. Ingreso: hasta el último día del mes siguiente a la notificación, sin recargo ni interés si se paga en ese plazo.
4. Seis cambios al año: correcto en contenido y fechas, pero el art. 43 bis RGC está DEROGADO (RDL 13/2022, disp. derog. única.d, efectos 1/1/2023). La regla está en el art. 45.1 RGC (redacción RDL 13/2022 art. 5.1).
5. Cese obligatorio: LGSS 327.1 «es de carácter obligatorio». OK, va dentro del 31,5 %.
6. T/8/N/R: opción de base fuera de límites bloqueada (OK); societarios, colaboradores, pluriactividad, tarifa plana, agrario, venta ambulante, forales declarados. RDL 26/2026 no toca LGSS 308 ni Orden art. 18: bien no citarlo. Alta de oficio (308.1.a.5.ª, sin regularización) no declarada: nicho < 1 %, opcional.
7. Absolutos: 1 frase sin condición (abajo).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | R | content/…html (Plazos), calcs/…json (l. 96 «Duda abierta»), params.autonomo_regularizacion_2026.confianza_nota | Quitar «el art. 308.1.c.4.ª LGSS habla del 31 de mayo… debe confirmarla tu notificación» y la «duda abierta». Texto: «antes del 30 de abril del año siguiente a aquel en que la Agencia Tributaria comunica los rendimientos (art. 308.1.c.4.ª LGSS y art. 46.2.5.ª.c RGC)». | LGSS 308.1.c.4.ª en redacción del RDL 14/2022 DF 10.1 |
| 2 | R | content/…html («Cambia la base…»), calcs/…json (l. 96), params.autonomo_regularizacion_2026.fuente | «art. 43 bis» → «art. 45.1 del Reglamento General de Cotización»; en json/params quitar «Real decreto 504/2022» como fuente de esa regla (es RDL 13/2022 art. 5.1). | 43 bis derogado desde 1/1/2023 |
| 3 | N | content/…html (Supuestos, tarifa plana) | «con tarifa plana, los primeros 12 meses no se regularizan nunca; la prórroga de otros 12 meses, tampoco salvo que el rendimiento del año supere el salario mínimo (art. 46.1 RGC)». | RGC 46.1: el período del art. 38 ter.1 Ley 20/2007 no se regulariza; el «salvo… SMI» solo afecta al del 38 ter.2 |
| 4 | otros (absoluto) | content/…html («No es una multa…») | «…hasta el último día del mes siguiente a la notificación, sin recargo ni intereses si pagas en ese plazo». | LGSS 308.1.c.4.ª: «de abonarse en ese plazo» |

Opcional: en «meses con prestación… no se regularizan» añadir «ni las bases usadas para calcular una prestación ya reconocida» (RGC 46.1, párr. 4.º).
Casos nuevos para test.json: ninguno (no cambia el cálculo). Re-verificación: Sonnet, solo releer las 4 frases (sin oráculo propio: el del Constructor basta).
