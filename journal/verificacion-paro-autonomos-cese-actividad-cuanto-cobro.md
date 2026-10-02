# Verificación fiscal · paro-autonomos-cese-actividad-cuanto-cobro (Opus, 2/10/2026)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 4 · 8 0 · N 0 · R 0 · S 1 · otros 0 · críticos (cambian cifra) 0
Leído desde la norma: API BOE consolidado BOE-A-2015-11724, última versión de los arts. 327, 329, 330 (vig. 2/3/2023), 331, 333, 337, 338, 339, 340, 341, 342 (vig. 1/1/2023). RDL 26/2026 (BOE-A-2026-20266): su análisis no modifica BOE-A-2015-11724 ni el IPREM (confirmado). IPREM 600 €/mes, sin PGE 2026.

## Paso 0: interpretación propia (coincide con el JS y el oráculo)
- Cuantía = 70 % de BR (339.2), máximo 175 % del IPREM mensual + 1/6 (700 €) sin hijos; «uno o más hijos ... respectivamente 200 o 225 %»: «uno» → 200, «más» → 225. Es la lectura directa de «respectivamente», no un supuesto débil (se puede quitar «es una lectura nuestra» o dejarlo). Mínimo 80 % / 107 % (sin / con hijos). 1.225/1.400/1.575 y 560/749/749: correctos.
- Duración 338.1: escala 12-17→4, 18-23→6, 24-29→8, 30-35→10, 36-42→12, 43-47→16, ≥48→24, dentro de 48 meses con ≥ 12 «comprendidos en los veinticuatro meses inmediatamente anteriores» (RDL 13/2022; ya no «continuados»). JS idéntico. BR sí es «doce meses continuados e inmediatamente anteriores» (339.1): bien.
- 338.3: 18 meses desde el **reconocimiento** del último derecho (no desde el último cobro). JS (select «me la reconocieron») bien; texto no (cambio 3).
- 50 % y sin límites solo en 331.1.a.4.º-5.º y fuerza mayor parcial (339.2-3): bloqueado y declarado. Bien.
- Cuota (329.1.b): el órgano gestor se hace cargo; 50 % en 4.º/5.º; sin obligación de cotizar en violencia (331.1.d); y 337.6: solo si se solicita en plazo, si no desde el mes siguiente a la solicitud (cambio 4).
- Edad (330.1.d): sin derecho en cese definitivo tras la edad ordinaria «salvo que no tuviera acreditado el período de cotización»; DT 7.ª 2026: 65 (38 a 3 m) / 66 a 10 m. Bloqueo ≥ 67 y aviso 65-66: correcto y declarado.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | T | json lead, veredicto, faq 3; html lead | «El derecho no existe ... si sigues trabajando mientras cobras» / «y no sigues trabajando» / «o trabajas mientras cobras» → «y la prestación se suspende mientras trabajes (se extingue si trabajas 12 meses o más)» | Art. 340.1.c: es suspensión, no inexistencia; la propia calculadora calcula con aviso (texto contradice al cálculo) |
| 2 | T | json veredicto, faq 3 | «el derecho no existe si ya has cumplido la edad ordinaria de jubilación» → añadir «salvo que no tengas la cotización exigida para la pensión» | Art. 330.1.d (excepción literal); la página sí la dice en «Cuándo existe» |
| 3 | S | json veredicto («no has cobrado otra prestación en los 18 meses anteriores»), faq 3 («cobraste otra prestación hace menos de 18 meses») | → «han pasado 18 meses desde que te reconocieron la anterior» | Art. 338.3 cuenta desde el reconocimiento, no desde el cobro: con la redacción actual quien terminó de cobrar hace < 18 meses pero se la reconocieron hace ≥ 18 se cree sin derecho |
| 4 | T | json veredicto y faq 4; html bullet «La cuota»; js note «La cuota» (Constructor) | «la paga el órgano gestor mientras cobras» → añadir «si la pides en plazo (art. 337.6); si te retrasas, desde el mes siguiente a la solicitud» | Art. 337.6 condiciona el pago de la cuota al plazo del 337.4 |
| 5 | T | html lead y bullet «Cese voluntario»; js MSG 1 (Constructor) | «el derecho no existe si dejas la actividad por decisión propia» → añadir «(salvo el TRADE que rompe con su cliente por incumplimiento grave de este, art. 333.1.b)» o remitir a la opción TRADE | Art. 331.2.a: «salvo en el supuesto previsto en el artículo 333.1.b)» |

Recomendado (no obligatorio): html «Si tienes un establecimiento abierto al público, hay que cerrarlo o traspasarlo» → «en los motivos económicos» (exigencia del 331.1.a, no de todas las causas). En el cese por violencia no hay obligación de cotizar (329.1.b último párrafo): la frase de la cuota no es falsa, se puede matizar.

## Citas por muestreo (patrón 4)
art. 339.3 (máx./mín.) ✓ · art. 338.1 (escala y 12 en 24) ✓ · art. 337.4-5 (plazo y descuento) ✓ · art. 331.2.b (TRADE, 1 año desde que se extinguió la prestación) ✓ · DT 7.ª 2026 ✓.

## Casos de prueba
Ninguno nuevo de cálculo (fórmula, escala, topes y bloqueos coinciden con la norma). Re-verificación Sonnet: solo releer las frases de los cambios 1-5; no cambia interpretación ni cifras.
