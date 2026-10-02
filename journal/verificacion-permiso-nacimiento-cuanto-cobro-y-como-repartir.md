# Verificación fiscal · permiso-nacimiento-cuanto-cobro-y-como-repartir (Verificador Opus, 2/10/2026)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 1 · R 0 · otros 4
Normas leídas hoy en el consolidado del BOE (API, última versión): ET art. 48 (vigente 31-7-2025) y su versión anterior (1-5-2025); LGSS 177, 178 (31-7-2025), 179 (1-1-2023), 180, 181, 182 (31-7-2025), 248.1.b (1-4-2025); LIRPF art. 7.h (versión 1-10-2026, RDL 26/2026: h sin cambios); RDL 9/2025, DT única (texto en el BOE); Orden PJC/297/2026 art. 2.1 (5.101,20 €).

## Paso 0: interpretación propia frente al bloque INTERPRETACION del oráculo
1. 19 semanas por progenitor (6 + 11 + 2), 32 monoparental (6 + 22 + 4); +1 por progenitor por hijo adicional y por discapacidad, ampliación completa (+2) con un solo progenitor (48.6). COINCIDE. Mono con parto doble = 34: correcto.
2. 179.1: 100 % de la base de cotización por CC del mes inmediatamente anterior al mes previo al del hecho causante, /30 si retribución mensual y alta todo el mes; con tope de la base máxima. COINCIDE (la página dice bien «mes anterior al previo»; journal/fiscal-fuentes.md c38 dice «mes anterior»: corregir allí).
3. Reparto: derecho individual e intransferible; el «reparto de menor pérdida» solo mueve semanas dentro de [6, máx] de cada uno, sin transferir: CORRECTO como modelo (el que gana más renuncia a semanas propias y el otro usa más de las suyas). Solo falla la redacción (ver otros 3).
4. DIFIERE: la DT única del RDL 9/2025 solo retrotrae al 2-8-2024 las 2 (4) semanas de la letra c). La 11.ª semana de la letra b) no es retroactiva: antes del 31-7-2025 el art. 48.4 daba 16 semanas (versión 1-5-2025). Nacimientos del 2-8-2024 al 30-7-2025 = 16 + 2 = 18, no 19; y a 2-10-2026 su ventana de 12 meses ya está cerrada, así que solo les quedan las 2 (4) semanas hasta los 8 años. El oráculo y la preverificación dicen «las 19 semanas valen para esos nacimientos»: no es así.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | T (crítico) | content html (Supuestos «No incluye» y «Derecho individual»), json (lead/FAQ 4), JS NO_MODELA | Cambiar «nacimientos anteriores al 2-8-2024 (16 semanas)» por: «la herramienta vale para nacimientos desde el 31-7-2025. Si nació entre el 2-8-2024 y el 30-7-2025 tenías 16 semanas (6 + 10) más las 2 (4 monoparental) hasta los 8 años, y hoy solo puedes pedir esas 2 (4); antes del 2-8-2024, 16 semanas». Ningún texto debe decir que las 19 valen desde el 2-8-2024 | ET 48.4 versión 1-5-2025 (16 semanas) frente a la de 31-7-2025; RDL 9/2025 DT única (solo «la adición de las dos semanas») |
| 2 | N | html Supuestos + JS NO_MODELA | Añadir «contratos a tiempo parcial: la base es la suma de las bases de los 12 meses anteriores al mes previo, entre 365» | LGSS 248.1.b: otra fórmula, cambia el importe |
| 3 | otros (absoluto) | json FAQ 2 | «Podéis cogerlas a la vez o una detrás de otra» → añadir «las 6 obligatorias de los dos coinciden, inmediatamente después del parto; las voluntarias, a la vez o una detrás de otra» | ET 48.4.a |
| 4 | otros (absoluto) | json veredicto y FAQ 2, html «Derecho individual» | «el derecho no se puede transferir» → añadir «salvo fallecimiento de un progenitor, en que el otro puede usar lo que reste» | ET 48.4, párrafo 6 |
| 5 | otros (redacción) | html «Cuántas semanas toma cada uno» | «y las demás las toma el otro» sugiere transferencia → «y el otro toma más de sus propias semanas, si no las usaba todas» | ET 48.4 (intransferible) |
| 6 | otros (redacción) | JS NO_MODELA | «la prestación de cuidado del menor de 8 semanas hasta los 8 años (sin retribución)» → «el permiso parental de 8 semanas hasta los 8 años (art. 48 bis ET, no retribuido)» | no es una prestación |

## Comprobado sin cambios
- Fórmulas: semanal = min(sueldo, 5.101,20) × 7/30; cifras de la página recalculadas (14.186,67; 1.190,28; 3.098,01; 978,32; 3.319,68 / 2.881,67 con 90 % a 6.500 €; mono 23.893,33 y 25.386,67): correctas.
- Tope 5.101,20 €/mes desde 1-1-2026 (Orden PJC/297/2026 art. 2.1, RDL 3/2026): correcto.
- 7.h: exenta la prestación del Cap. VI Tít. II LGSS; complemento de empresa tributa: correcto. El «tope de la prestación máxima» de fiscal-fuentes solo aplica a mutualidades/funcionarios: no está en la página, bien.
- Carencia 178.1, alta 178.4 (añadido por RDL 9/2025), 180 trabajo durante el descanso, 182 no contributiva (IPREM o base menor, 6 semanas + 14 días en 4 supuestos): citas correctas.
- RDL 26/2026: no toca ET 48, LGSS 177-182 ni la letra h del 7 LIRPF. R 0.
- Bloqueos (1-5 semanas, > máximo, 0 total, sueldo 0): correctos.

## Casos nuevos para test.json
- Ninguno de fórmula. Si se añade un input «fecha de nacimiento» (opcional), caso: nacimiento 15-3-2025, dos progenitores → máximo 2 semanas cada uno (aviso), no 19.
