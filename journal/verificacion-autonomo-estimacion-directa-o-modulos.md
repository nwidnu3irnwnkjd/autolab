# Verificación fiscal · autonomo-estimacion-directa-o-modulos (Verificador Opus, 2/10/2026)
VEREDICTO: PUBLICABLE CON CAMBIOS · 6 cambios obligatorios (2 críticos), 0 errores de fórmula.
Norma leída hoy (API BOE consolidada): LIRPF arts. 30.2.4.ª, 31.1.3.ª, 32.2 y DT 32.ª; RIRPF arts. 30, 33, 35, 36; RIVA art. 33.2; LIVA art. 122; LGSS art. 308.1.c; Orden HAC/1425/2025 arts. 3, 5, DA 1.ª, anexo II. AEAT sede (act. 28/9/2026) + nota AEAT 1/4/2026 con criterio DGT (vía prensa profesional, confianza C).

## Paso 0: interpretación propia = la del oráculo
Directa simplificada: I − G − cuota RETA − 5 % (máx. 2.000, art. 30.2.ª RIRPF / 30.2.4.ª LIRPF) → 32.2.3.º → escala. Módulos: neto de módulos × 0,95 (DA 1.ª) → 32.2.3.º; sin restar cuota ni gastos. RETA: directa = neto + cuotas; EO = rendimiento neto previo (308.1.c LGSS), −7 %. Coincide con JS y oráculo.

## Puntos pedidos
1. Límite 2026. Letra de la ley: 150.000/75.000/150.000 € (DT 32.ª consolidada solo hasta 2024; RDL 9/2024, 16/2025 y 2/2026 derogados: BOE-A-2025-1136, A-2026-2024, A-2026-4667). Orden art. 3 remite «al previsto para 2026» sin cifra. Pero la AEAT, con criterio de la DGT (nota 1/4/2026), aplica 250.000/125.000/250.000 € en 2026 y da por válidas las renuncias hechas con los RDL vigentes. Decisión: para 2026 rige en la práctica 250.000 €; bloqueo > 250.000 + aviso 150.000-250.000 es correcto, con los cambios 2 y 3. La página de la sede AEAT («2016 hasta 2026») arrastra el texto del RDL 2/2026: citar la nota de 1/4/2026, no solo la sede.
2. Correcto: 5 % con tope 2.000 € (RIRPF 30.2.ª, cita bien); 32.2.3.º se aplica también en módulos (el 2.º.a exige directa, así que EO cae siempre en el 3.º); bordes 8.000/12.000 y «inferiores a 12.000» bien en JS. 600.000 € (RIRPF 28.1) irrelevante por el bloqueo a 250.000.
3. Correcto: la cuota RETA no se deduce en EO; 130 = 20 % (110.1.a); 131 = 2/3/4 % (110.1.b y anexo II.4) y DA 1.ª.3 aplicada; plazos (RIRPF 33.1.a/b, 33.3, Orden art. 5) bien citados.
4. Patrón 8: ver cambios 1, 3 y 4.
5. RDL 26/2026 no toca LIRPF 28-32, DT 32.ª ni RIRPF 28-37/109-110 (toca arts. 7, 23, 24, 67, 68, 85, 95 bis/ter y DA vivienda; RIRPF 41 bis, 69, 75-76, 93-94). Sin efecto. DA 64.ª LIRPF (Ceuta, RDL 22/2026) no modelada: ver cambio 6.

## Cambios obligatorios
| # | Patrón | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 CRÍTICO | 4/8 | content (Cómo decidir, Plazo de renuncia) y js `note` «No incluye» | Quitar «el régimen simplificado y su renuncia se deciden aparte» y «se tramitan por separado». Poner: «Renunciar a módulos supone renunciar también al régimen simplificado del IVA, y al revés (art. 33.2 del Reglamento del IVA y art. 36 del Reglamento del IRPF): en directa pasas al IVA general, cuyo efecto no se calcula.» | RIVA 33.2: «La renuncia al régimen de estimación objetiva del IRPF supondrá la renuncia» al simplificado; RIRPF 36.1-2 a la inversa. Afirmación falsa que cambia la decisión |
| 2 CRÍTICO | 7 | content (Límites) y js aviso150 | La página decide 2027 (renuncia en diciembre de 2026), pero el límite solo se explica para 2026. Añadir: «Para 2027 la ley fija 150.000 € (75.000 € a empresas) y aún no hay prórroga ni Orden de 2027: si facturaste más de 150.000 € en 2026, puede que en 2027 no puedas estar en módulos.» Citar la nota AEAT/DGT de 1/4/2026 como base de los 250.000 € de 2026 | DT 32.ª no cubre 2026 ni 2027; el criterio administrativo es solo para 2026 |
| 3 | 8 | js `aviso150` y content | El límite de facturas a empresas (125.000 € AEAT / 75.000 € ley, art. 31.1.3.ª.b LIRPF) no avisa entre 125.000 y 150.000 €: activar el aviso con ingresos > 125.000 € (y mencionarlo en «léelo si facturas más de…») | Usuario B2B de 125-150k excluido sin aviso |
| 4 | 1/8 | js nota exento130 | El aviso del art. 109.2 (70 % con retención) solo vale para actividades profesionales y la herramienta supone actividad empresarial (las de módulos lo son): quitarlo o decir «no aplica a actividades empresariales» | Texto no aplicable al ámbito |
| 5 | 4 | js bloqueo 3 | «Con más de 250.000 € de ingresos al año» → «Si en el año anterior tus ingresos superaron 250.000 €» | El límite se mide con el año inmediato anterior (31.1.3.ª.b, RIRPF 33.3) |
| 6 | 3 | content «No incluye» y js note | Añadir Ceuta y Melilla (DA 64.ª LIRPF: 10 % de difícil justificación y reducción de módulos del 10 % en Ceuta en 2026; deducción del 60 %, art. 68.4) y Canarias (IGIC: la renuncia también arrastra, art. 36.3-4 RIRPF) | Ámbito territorial |

## Casos nuevos para test.json
- ingresos 130.000 → aviso150 (o el nuevo aviso) = 1; ingresos 125.000 → 0.
- texto: grep «se deciden aparte|por separado» = 0 hits en content y js; grep «36 del Reglamento del IRPF» ≥ 1.
- bloqueo 3 con ingresos 250.001: verdict contiene «año anterior».
Re-verificación: Sonnet (no cambia la interpretación de las fórmulas).
