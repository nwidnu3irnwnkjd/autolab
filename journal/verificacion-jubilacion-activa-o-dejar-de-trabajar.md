# Verificación fiscal/legal · jubilacion-activa-o-dejar-de-trabajar · 2026-10-02 (Verificador Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 1 · N 0 · R 0 · otros 3 (1 crítico: arts. 152/311 omitidos, patrón 2)
Norma leída hoy (API BOE consolidado BOE-A-2015-11724, versión vigente de cada bloque): arts. 152, 153, 205, 210, 214, 310, 311, DT 7.ª; Orden PJC/297/2026 art. 32 (BOE-A-2026-7296); RDL 5/2013 DA 1.ª (BOE-A-2013-2874); RDL 26/2026 (BOE-A-2026-20266).

## Paso 0: interpretación propia frente a INTERPRETACION del oráculo
- Activa (214.1-3): coincide. 45/55/65/80/100 % por años COMPLETOS de demora (1/2/3/4/5+), +5 puntos cada 12 meses ininterrumpidos (desde el mes siguiente), tope 100 %; 75 % del autónomo con indefinido de 18 meses o nuevo (sin vínculo 2 años) solo con demora de 1 a 3 años y luego la escala; base = importe del art. 210 incluido el complemento de demora y brecha/maternidad, sin mínimos (214.2, 214.6). 15 años a la EO y ≥ 1 año hasta el HC, sin bonificaciones ni anticipos. Confirmado.
- Solidaridad: 9 % (153: 7 empresa + 2 trabajador; 310.1: 9 % autónomo sobre su base de CC), no computable para prestaciones. Confirmado.
- 210.2.a: 4 % por año completo cotizado; desde el 2.º año completo, periodos > 6 meses = 2 %; tope art. 57 y exceso como cantidad anual con tope de la base máxima anual; b) tanto alzado y c) combinación; compatible con 214 sin que crezca durante la activa. Confirmado (oráculo y JS iguales).
- **DIFERENCIA 1 (crítica, patrón 2)**: «demorar» (opción C) se calcula con cotización ordinaria (6,5 % trabajador; 31,5 % RETA). Pero el art. 152.1-2 LGSS (Ley 21/2021) exime a empresa y trabajador de cotizar por contingencias comunes (salvo IT), desempleo, FOGASA y FP «una vez hayan alcanzado la edad» del 205.1.a), y el art. 311 exime al autónomo salvo IT y CP. Orden PJC/297/2026 art. 32.1: IT del 152 = 1,55 % (0,25 % trabajador); IT del 311 = 1,56 %. Los periodos exentos cuentan como cotizados (152.4), así que la demora de C sigue sumando 4 puntos.
- **DIFERENCIA 2 (T)**: la EO usa el calendario de 2027+ (38a6m / 67). La DT 7.ª aplica por el año en que se cumple la edad: 2024 38a/66a6m; 2025 38a3m/66a8m; 2026 38a3m/66a10m. Quien puede estar en activa en 2026-2027 cumplió la EO en 2024-2026: la demora sale 2-6 meses menor y puede bajar un año completo (p. ej. 67a9m con 35 cotizados que cumplió 66a8m en 2025: demora real 13 meses → 45 %; la herramienta dice «todavía no puedes»). Cambia escalón del 214 (−10 puntos o niega la activa) y del 210.2 (−4 puntos).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | otros (patrón 2), crítico | calcs .js/.json, oráculo, content | En C, neto = sueldo − 0,25 % de la base (ajena) o − (1,56 % IT + tipo CP del RETA) × base (autónomo); quitar «6,5 %» y «cuota completa del RETA» de la página (sección «Demorar») y del json (l. 151, 162); recalcular el ejemplo «1.870 € … recupera a los 84 años». Opcional: en la activa añadir el 0,25 % de IT del trabajador (art. 153 «únicamente por IT y CP»). | arts. 152 y 311 LGSS; Orden PJC/297/2026 art. 32.1.a-b |
| 2 | T | .js/.json/content/FAQ l. 147 | Pedir el año del hecho causante (o de nacimiento) y aplicar la DT 7.ª por el año en que se cumple la EO (params jubilacion_2026.edad_ordinaria ya tiene 2026; añadir 2024 [456,798] y 2025 [459,800]). Si no se modela: bloquear HC con EO anterior a 2027 o avisar, y corregir el texto «65 con 38a6m, 67 si no» como solo de 2027 en adelante. | DT 7.ª LGSS |
| 3 | 8 | .js estado 2, FAQ l. 147 | El aviso «no hay jubilación activa» es falso: si los 15 años se reúnen después de la EO, el año mínimo se cuenta desde esa fecha (214.1, última frase). Lo que no hay es complemento de demora (210.2). Cambiar el mensaje (la herramienta no lo calcula) y la FAQ. | art. 214.1 in fine; 210.2 |
| 4 | otros (cita) | content «Demorar» | «4 puntos más de base reguladora» → «4 puntos más de porcentaje sobre la base reguladora». | art. 210.2.a |
| 5 | otros (texto) | content «No incluye» | El requisito de no haber hecho despidos improcedentes está derogado (DA 1.ª RDL 5/2013, derogada por el RDL 8/2015 desde el 2/1/2016): decirlo así o quitarlo de «No incluye». | RDL 8/2015 DD única.26 |

## Comprobado sin cambios
- Params jubilacion_activa_2026: escala, 75, 5, 12 meses, 15 años, 9/7/2 %, máxima 3.359,60, mínima 13.106,80, base máxima 5.101,20 (fuentes ya verificadas en jubilacion_2026). Tope anual 61.214,40 = 12 × 5.101,20.
- Citas por muestreo (214.1, 214.3, 153): textuales.
- R: el RDL 26/2026 no menciona jubilación ni los arts. 152/153/205/210/214/310/311; no se cita. Sin DT en el RDL 11/2024 para la activa (solo relevo): correcto.
- Absolutos: «Solo compensa si vas a cobrar la pensión durante muchos años» es condicional y defendible; resto sin absolutos.
- N: IRPF, IT/CP, mínimos, brecha, MEI, tanto alzado, forales y sector público (214.9) declarados.

## Casos nuevos para test.json
1. Ajena, 67a, 40 cot, pensión 2.000, sueldo 2.000, N 3: netoDemora = 1.995 (2.000 − 0,25 %), no 1.870; eq (edad de recuperación) recalculada.
2. Autónomo 2.500 de rendimiento (base 1.274,51): netoDemora = 2.500 − (1,56 % + CP RETA) × 1.274,51, no 2.500 − 31,5 %.
3. HC 2026 a 67a9m, 35 cot (EO 66a8m en 2025): demora 13 meses, activa 45 %.
4. HC 2027 a 67a10m, 30 cot (EO 66a10m en 2026): demora 12 meses, activa 45 % (hoy: «todavía no»).
5. 67a con 14 cot a la EO y 16 al HC a 69a: aviso sin «no hay jubilación activa».
Re-verificación: cambia la interpretación (C y EO) → Opus ≤ 60k solo sobre las piezas 1-3; el resto, Sonnet.

## 2.ª pasada Opus (2026-10-02, solo piezas con interpretación cambiada)
VEREDICTO: PUBLICABLE CON CAMBIOS MENORES (2 textos, sin cálculo) · T 0 · 8 0 · N 0 · R 0 · otros 2
- (a) Demorar: netos() aplica 0,25 % (art. 152; Orden PJC/297/2026 art. 32.1.a) y 1,56 % IT + 1,30 % CP (art. 311; Orden art. 32.1.b y tipo CP RETA 1,30 %, comprobado en la Orden); la activa suma 2 %/9 % de solidaridad sobre lo anterior (153/310 «únicamente por IT y CP»). Recalculado a mano el caso 1 (67a, 2027, 40 cot): EO 65a3m (cumple 65 en 2025 con 38a, llega a 38a3m a los 65a3m), demora 21 m → 2.080 €; C: 57 m → 16 + 2 = 18 puntos → 2.360 €; neto 1.995 / 1.955; TA 114.060, TB 87.360, dif 26.700; recuperación 80,78 = 80 años y 9 meses. Correcto. RETA 2.500: base 1.274,51 → 2.463,55 / 2.348,84. Correcto.
- (b) DT 7.ª: cuadro 2013-2026 de dt7 coincide con el BOE en sus 14 filas; el año de cada edad candidata se calcula desde el HC (julio), que es la lectura del INSS por año de cumplimiento. Casos 67a9m/2026/35 → EO 800 (66a8m, 2025), demora 13, 45 %; 67a10m/2027/30 → EO 802, demora 12; 70a/2027/14 → EO 796 (2023). Correctos. DT 9.ª por año del HC (2023-2026: 49 m al 0,21 + 0,19; 2027+: 248 al 0,19 + 0,18; tope 100) y C con y+n: correcto. Lo de tomar julio está declarado en la etiqueta.
- (c) Estado 3 (15 años reunidos tras la EO): mensaje fiel al 214.1 in fine y al 210.2; estado 2 solo si no hay 15 años ni al HC. Correcto.
- (d) Select tipo (ajena / propia / propia_contrata): el 75 % solo con propia_contrata y dY 1-3, luego la escala. Correcto.
- Oráculo actualizado: 716 casos, 0 discrepancias (ejecutado hoy).
Cambios restantes (texto, no bloquean el cálculo):
1. content l. 34 (Supuestos): «4 puntos de base reguladora» → «4 puntos de porcentaje sobre la base reguladora» (210.2.a; la l. 6 ya está corregida).
2. json tipo (etiqueta y opción propia_contrata): añadir «sin vínculo laboral contigo en los 2 años anteriores» al trabajador nuevo (214.3).
Re-verificación: Sonnet, solo releer esas 2 frases.
