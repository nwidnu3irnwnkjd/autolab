# Verificación fiscal/legal · pension-viudedad-cuanto-cobro · 2026-10-02 (Verificador Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 2 · R 0 · otros 1 · errores de fórmula 0
Norma leída hoy (BOE): Decreto 3158/1966 art. 31.2-3 (consolidado), RD 900/2018 arts. 2, 3 y 7, RD 241/2026 (BOE-A-2026-6977) art. 3 y anexo I, LGSS arts. 219-223 (consolidado). No hay journal/lector-<slug>.md.

## Paso 0: mi lectura frente a INTERPRETACION del oráculo
- 52 % (31.1), 60 % (RD 900/2018 art. 2 a-d: 65+, sin derecho a otra pensión pública española o extranjera, sin ingresos de trabajo, capital/act. económicas/ganancias ≤ límite de mínimos = 9.442 € en 2026) y no acumulación con el 70 % (art. 7): COINCIDE.
- 70 %, límite de rendimientos (31.2 párr. 2): el texto dice «pensión mínima de viudedad **en función de la edad** del pensionista». El Constructor usa el mínimo con cargas (17.592,40 → 27.034,40). La lectura literal da 9.442 + 9.931,60 = 19.373,60 (< 60), 21.704,60 (60-64), 22.548,80 (65+). La redacción es de 2003, anterior a la fila «con cargas» del anexo; fuentes secundarias divergen. Lectura del Constructor defendible pero NO demostrada y es la más favorable: DIFIERE (hallazgo prioritario, N).
- Cargas (31.2 párr. 3-4): renta de la unidad familiar incluido el pensionista / miembros ≤ 75 % SMI sin extras (10.989 €); «rendimientos computables… de naturaleza prestacional»; se toman los del **ejercicio anterior**, excluidos los dejados de percibir por el hecho causante. Consecuencia: en el reconocimiento inicial la viudedad no se cobró el año anterior (no cuenta); en años posteriores sí cuenta. La página dice «no se sabe con certeza»: la norma sí lo aclara en parte (N, texto).
- 50 % «como mínimo» incluyendo el complemento a mínimos: JS usa ≥ 0,5 sin complemento (más estricto, declarado): OK.
- 31.3 (reducción hasta el límite): OK. Tope 3.359,60 €/mes (RD 241/2026 art. 3) y 9.442 € y mínimos 17.592,40 / 13.106,80 / 12.262,60 / 9.931,60 (anexo I): cifras verificadas literalmente.
- LGSS 219.1 (500 días/5 años, 15 años sin alta, accidente sin período), 219.2 (1 año o hijos; enfermedad sobrevenida y suma de convivencia: avisado), 221.2 (5 años salvo hijos; registro 2 años), 222 (temporal 2 años para cónyuge y pareja con registro < 2 años), 223.1 («compatible con cualesquiera rentas de trabajo»), 223.2: citas correctas (3 de 3 por muestreo: 221.2, 222, 223.1).

## Puntos del encargo
1. 52/60/70: correctos; 9.442 € vigente 2026 (RD 241/2026). 70 %: ver cambio 1.
2. Tope y mínimos 2026: correctos (mensual = anual/14).
3. Requisitos: modelados matrimonio, pareja (5 años/hijos, registro 2 años → temporal), cotización (bloqueo). Sin dependencia económica para pareja (suprimida por Ley 21/2021): correcto.
4. Trabajo: viudedad compatible (223.1); el 60 % sí exige no trabajar (RD 900/2018 art. 2.c). Bloquear el 60 % con ingresos > 0 es correcto si son de trabajo; con capital ≤ 9.442 € la herramienta avisa (pos = 60): correcto.
5. Propia pensión en la renta familiar: ver cambio 2.
6. T: DT 13.ª, DA 40.ª, DT 1.ª RD 900/2018: no aplican en 2026 (correcto, declarado). 8: opciones imposibles bloqueadas (causante sin período, pareja sin 5 años ni hijos). N: mínimos, brecha, orfandad/art. 229, IRPF, separados declarados. R: RDL 26/2026 no toca viudedad, no se cita: correcto.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | N | calcs/…js + content/…html | Mantener 27.034,40 si se quiere, pero cuando el 70 % o su importe dependa del límite, avisar con el límite literal por edad (19.373,60 / 21.704,60 / 22.548,80 €) y el importe resultante; en «Supuestos» citar la frase «en función de la edad» y dar las 3 cifras | Decreto 3158/1966 art. 31.2 párr. 2; lectura favorable no confirmada (YMYL: no prometer el importe alto) |
| 2 | N | content + nota pos=70 del JS | Sustituir «no se sabe con certeza si cuenta la propia pensión» por: se computan los rendimientos del año anterior; al reconocer la pensión, la viudedad aún no se cobraba (no cuenta); al mantener el 70 % en años siguientes sí cuenta (rendimientos «de naturaleza prestacional»), y el 70 % puede perderse. Indicar que «ingresos» = los del año anterior | art. 31.2 párr. 4 |
| 3 | otros (texto) | content + NO_MODELA del JS | Brecha de género: «para mujeres con hijos» → «para mujeres con hijos y, en algunos casos, hombres» | LGSS art. 60.1 |

## Casos nuevos para test.json
- BR 2.000, 45 años, 2 hijos, 6.000 € de ingresos: 70 % 1.400 € con 27.034,40; con límite literal (< 60) 955,26 €/mes → debe salir el aviso del cambio 1.
- BR 1.200, 66 años, 1 hijo, 0 ingresos: límite literal 65+ 22.548,80 no limita (11.760 €): sin aviso.
- BR 3.000, 50 años, 1 hijo, 0 ingresos: p70 29.400 > 19.373,60 literal y > 27.034,40 → reducido a 1.931,03 €/mes (27.034,40) o 1.383,83 (literal): aviso.
Re-verificación: Sonnet, solo cambios 1-3 y estos casos (no cambia la interpretación del resto).
