# Verificación fiscal · finiquito-baja-voluntaria-vacaciones-preaviso (Opus, 2026-10-02)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 1 · R 0 · S 3 (1 crítico) · otros 5 (absolutos 3, cita 1, cifra de texto 1)

## Paso 0 (interpretación propia desde la norma, antes del oráculo)
Coincide con el bloque INTERPRETACION en vacaciones (ET 38.1 + LGSS 147.1), preaviso (ET 49.1.d: plazo por convenio/costumbre; la consecuencia no está en el ET), pagas (ET 31 no fija devengo) e IRPF (RIRPF 80.1). **Difiere en la cotización**: RGC (RD 2064/1995, BOE-A-1996-1579) art. 23.1.A «Las percepciones de vencimiento superior al mensual se prorratearán a lo largo de los doce meses del año»: la parte pendiente de las pagas YA cotizó mes a mes por prorrata; en el finiquito solo cotiza la prorrata del mes de salida, no toda la paga pendiente. El modelo cotiza la paga pendiente entera (sobrecotización).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | S **crítico** | calcs .js + oráculo + json/html (cifras) | Base de cotización del mes = salMes + prorrata de pagas del mes (14 pagas: 2·(bruto/14)·dia/365, o (2·m/12)·dia/díasMes) con tope; vacaciones aparte como ahora. NO cotizar `pagasPend` entera. IRPF sigue sobre todo lo cobrado. | RGC art. 23.1.A. Ejemplo: cotización 143 → 87 €, neto 1.726 → 1.782 € (+56); el 30-jun (paga completa) el error ronda +100 €. Cambia el lead, veredicto, FAQ 1 y 740 € del preaviso (→ 796 €). Con 12 pagas no cambia. |
| 2 | otros (cita) | json sources, params.fuente, html, FAQ 2 | Convenio 132 OIT art. 11 confirmado en BOE: **BOE-A-1974-1055** (BOE núm. 160, 5-7-1974, https://www.boe.es/diario_boe/txt.php?id=BOE-A-1974-1055): «derecho, al terminarse la relación de trabajo, a vacaciones pagadas proporcionales… o a una indemnización compensatoria». Es tratado ratificado y vigente (art. 96 CE), no solo «doctrina»: redactar «lo establece el art. 11 del Convenio 132 de la OIT, ratificado por España, lo aplica el Tribunal Supremo y lo presupone el art. 147.1 LGSS». Opcional: Directiva 2003/88/CE art. 7.2. | Patrón 4 |
| 3 | otros (absoluto) | html «Baja voluntaria o despido» + js l.52 | «no hay indemnización ni paro, salvo que renuncies por una causa del art. 50» es incompleto e impreciso: también dan paro y 20 días/año la rescisión por traslado (ET 40.1) y por modificación sustancial (ET 41.3), y paro la del 49.1.m (LGSS 267.1.a.5.º); el art. 50 no es «renunciar», exige pedir la extinción al juez. | ET 40, 41.3, 50; LGSS 267.1.a.5.º |
| 4 | otros (absoluto) | html + js l.52 «Si fuera un despido» | «se suma la indemnización de 20 o 33 días» → «en un despido objetivo (20) o improcedente (33); el disciplinario procedente no tiene indemnización». | ET 53.1.b, 56.1, 55.7 |
| 5 | otros (absoluto) | html «¿Disfrutarlas antes o cobrarlas?» | «retrasa la fecha de salida» → «si no caben dentro del preaviso, retrasa la salida» (el js ya condiciona). | ET 38.2 (fecha por acuerdo) |
| 6 | S | html IRPF + label del input | Matiz: es el tipo único (general) de retención del trabajador, no un marginal; al extinguirse el contrato la empresa suele regularizarlo con las retribuciones reales del año (RIRPF 86.1 y 87.2.3.º «variaciones en la cuantía de las retribuciones»), así que el del finiquito puede ser menor (o mayor) que el de la última nómina. | RIRPF 80.1, 86.1, 87.2.3.º |
| 7 | S | html «Qué no incluye»/supuestos | Devengo semestral es defendible (ET 31 no lo fija) pero declarar el efecto: con verano de 1-jul a 30-jun y Navidad por año natural (convenios frecuentes), en el ejemplo las pagas pendientes serían ~1.855 € en vez de 997 €. | ET 31 (convenio) |
| 8 | N / cifra | html, params.convenciones (c), js | «hasta un 14 % menor» → «hasta un 13 % menor» (1 − 365/420 = 13,1 %). Y matizar que el TS/TJUE exigen pagar las vacaciones con la retribución ordinaria (no solo salario base). | Texto ≤ cálculo |

## Confirmado sin cambios
ET 38.1 (≥ 30 días naturales, literal), proporción por días/365, día = bruto/365 (S defendible y declarado), ET 49.1.d y descuento por días incumplidos solo si convenio/contrato lo prevé (S correcto: el ET no fija la consecuencia), impuestos antes del descuento (declarado, conservador), ET 49.2 y 59.1, LGSS 147.1 (vacaciones aparte, sin prorrateo, tope del mes/meses), 6,5 % (4,70+1,55+0,10+0,15 MEI 2026) y tope 5.101,20 (fiscal-fuentes), LGSS 267.1.a.5.º. T: sin transitorias aplicables (de acuerdo). 8: bloqueos correctos; Convenio 132 art. 5 (periodo mínimo) no exigido en España. R: aceptado lo comprobado por el Constructor.

## Casos nuevos para test.json (tras el cambio 1; esperados a recalcular con el oráculo corregido)
- defecto (24.000, 14, 15-oct, 30/18, 0, 15 %): cot ≈ 87,3; neto ≈ 1.782.
- 14 pagas 30-jun (21.000, 30/10, 12 %): la cot no debe incluir la paga de verano entera.
- 12 pagas: cifras idénticas a las actuales (control de no regresión).
