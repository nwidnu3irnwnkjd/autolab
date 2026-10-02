# Verificación independiente · placas-solares-merece-la-pena · 2026-10-02 (Verificador fiscal, Opus)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (el JS hace lo que dice, pero valora la compensación sin impuestos cuando la norma la descuenta antes de impuestos; tope más laxo de lo declarado; texto de la DA 62.ª incompleto; faltan ámbitos: forales y Canarias).
Oráculo del Constructor: 609 casos, 0 discrepancias ✔. Modelo propio en Python (escrito de cero) contra el JS por osascript, 9 escenarios: 0 discrepancias (< 0,01 €) en neto, ahorro1, comp1, tope, amortización simple/descontada y ahorro neto a 25 años. La tabla del HTML (9,0/10.484; 11,8/6.288; 13,7/4.619; 12,1/8.484) y el caso de FAQ 1 (12.000 €, Bilbao: −2.340 €) coinciden.

## 1. Norma (leída hoy en el BOE consolidado)
- RD 244/2019 art. 4.2.a: renovable, ≤ 100 kW, contrato único **solo si hacen falta servicios auxiliares**, contrato de compensación, sin régimen retributivo ✔ (página correcta; bloqueo > 100 kWp correcto). Art. 4.3: autoconsumo colectivo con reparto: no modelado ni declarado.
- Art. 14.3 ✔ comercializadora libre = precio pactado; PVPC = Pmh − CDSVh; tope = valor de la energía horaria consumida de la red en el periodo de facturación (≤ 1 mes). **Matiz que falta**: con PVPC esa energía de la red se valora al **TCUh** (coste de la energía del RD 216/2014 art. 7, **sin peajes ni cargos**), no al precio total sin impuestos que usa el JS → el tope real es más estricto por dos vías (mensual/horario y base sin peajes/cargos). Estimación con el perfil mensual PVGIS de Madrid (caso por defecto): tope anual JS 203 €, mensual 174 €, mensual con TCU ≈ 0,09 € → 128 €.
- **Art. 14.6.ii-iv (PVPC)**: la compensación se descuenta «sobre las cantidades a facturar antes de impuestos» y «una vez obtenida la cuantía final, se le aplicarán los correspondientes impuestos». **Ley 38/1992 art. 94.9**: exenta del IEE la energía objeto de compensación. → Cada € compensado ahorra también IEE e IVA: valor para el usuario = min(exc·comp, tope) × 1,0511269632 × 1,21. El JS (y la respuesta del Constructor a su punto 3) lo cuenta sin impuestos: **infravalora la compensación un 27 %**. Efecto: caso por defecto 9,0 → 8,3 años; 10 % autoconsumo 11,8 → 9,7; todo a red 13,7 → 10,7 (ahorro 25 a: 4.619 → 7.506 €). Con libre: misma práctica de facturación (IEE por art. 94.9 seguro; IVA sobre el neto no verificado en DGT).
- Ahorro por autoconsumo con IEE + IVA ✔: art. 94.5 Ley 38/1992 exime el consumo de los titulares de instalaciones renovables (≤ 50 MW) y no hay entrega sujeta a IVA. El mínimo de 1 €/MWh (art. 99.2.b) es irrelevante (actúa solo si la cuota cae por debajo de 0,001 €/kWh) ✔.
- DA 62.ª LIRPF (texto vigente, añadida por RDL 7/2026 art. 36.3; apdo. 6 modificado por RDL 26/2026 de 29/9, solo orden de aplicación): 10 % (vivienda propia) / 20 % (propietarios de viviendas en edificio de uso predominante residencial donde se instala) de lo pagado del 1/1 al 31/12/2026, **base máx. 5.000 €/año (deducción máx. 500 € / 1.000 €)**, instalación finalizada no después de 2026, sin efectivo, descontando subvenciones, con CIE, no afecta a actividad económica, incompatible con DA 50.ª para la misma instalación ✔ en lo esencial. Fallos de redacción: «10 % de hasta 5.000 €» se lee como deducción de 5.000 €; «20 % en edificios residenciales» es impreciso; falta que la DA 50.ª.2 (40 %, base 7.500 €, si el certificado acredita −30 % de energía primaria no renovable o clase A/B, pagos hasta 31/12/2026) es la alternativa posible y a veces mejor; falta que es IRPF **estatal** (País Vasco y Navarra tienen IRPF foral: no aplica).
- ICIO: tipo máximo 4 % (TRLRHL art. 102.3) y es un **coste** si el presupuesto no lo incluye; bonificaciones potestativas (arts. 74.5 y 103.2) ✔ declaradas como no verificadas.

## 2. PVGIS (API v5_3/PVcalc hoy, SARAH3, 1 kWp, 30°, sur, 14 %)
Madrid 1.610,5 ✔ · Sevilla 1.666,9 ✔ · Bilbao 1.164,8 ✔ · Santiago 1.289,4 (tabla 1.280; −0,7 %, punto distinto, aceptable). Sensibilidad Madrid: 15° → 1.528 (−5 %); SE/SO 45° → 1.509 (−6 %); este/oeste → 1.305 (−19 %). La página dice que depende de orientación, inclinación y sombras ✔; conviene dar la cifra (este/oeste ≈ −20 %).

## 3. Texto ≤ cálculo
| Frase | ¿Demostrada? | Corrección |
|---|---|---|
| Lead/FAQ 1/FAQ 3/tabla: «unos 9 años con 40 %, 12 con 10 %, 14 todo a red» | Sí con el JS actual; no tras corregir impuestos | Regenerar cifras tras el cambio C1 |
| Lead: «se amortizan antes cuanta más energía consumes directamente» | Solo si el kWh evitado vale más que el compensado (casi siempre; el veredicto lo dice, el lead no) | Añadir la condición al lead |
| FAQ 2/HTML: «el real puede ser más estricto» (tope) | Sí, pero subestima: falta la base TCU sin peajes/cargos con PVPC | Ver C2 |
| FAQ 4/HTML: deducción «10 % de hasta 5.000 €», «20 % en edificios residenciales» | Ambigua | Ver C3 |
| Ejemplos (6.000 €, 40 %, 0,07 €/kWh) presentados como editables | Sí ✔ | — |
| Precio evitado = media 12 m × 1,2718 | Defendible y declarado (horas de sol pueden valer otro precio) ✔; ×1,21 no vale en Canarias (IGIC) ni Ceuta/Melilla, y Las Palmas está en la tabla | Ver C4 |
| «Sin sesgo»: autoconsumo como hipótesis dominante | Sí ✔ (FAQ 3 + sensibilidad −10 puntos) | — |
| Sources: «compensación ... con tope en el valor de la energía ... sin impuestos» | Sí (describe el JS), pero norma mal resumida | Ajustar con C1-C2 |

## 4. Cambios obligatorios
- **C1** calcs/placas-solares-merece-la-pena.js `flujos`: `comp = Math.min(e*d.comp, tope) * (1+S.iee)*(1+S.iva)` (RD 244/2019 art. 14.6.iv; Ley 38/1992 art. 94.9); mismo cambio en ops/verif/placas-solares-merece-la-pena.py; label del input `comp`: «€/kWh sin impuestos, como figura en tu contrato o en el PVPC»; nota «Qué incluye» y sources: «la compensación se descuenta antes de impuestos, así que ahorras también IEE e IVA sobre ella». Regenerar test.json, tabla del HTML, lead, FAQ 1 y FAQ 3.
- **C2** JS nota del tope + FAQ 2 + HTML «Qué se calcula»: añadir «con PVPC el tope se calcula solo con el coste de la energía, sin peajes ni cargos (RD 244/2019 art. 14.3.ii.a), así que puede ser bastante menor; en el ejemplo, alrededor de un tercio menos». Si se prefiere no declararlo, modelarlo; no basta el aviso actual.
- **C3** FAQ 4 + HTML «Ayudas»: «10 % de lo pagado, con una base máxima de 5.000 € al año (hasta 500 €); 20 % (hasta 1.000 €) si eres propietario en un edificio de viviendas donde se instala para la comunidad; instalación terminada en 2026, sin pagos en efectivo, descontando subvenciones y con CIE. Es incompatible con la deducción por eficiencia energética (DA 50.ª), que puede ser mayor (40 %, base 7.500 €) si un certificado energético acredita la mejora. Es IRPF estatal: no se aplica en País Vasco ni Navarra». Si terminas en 2027, hoy no hay deducción.
- **C4** HTML supuestos + label `precio`: «En Canarias, Ceuta y Melilla no hay IVA del 21 % (IGIC/IPSI): escribe tu precio con tus impuestos».
- **C5** HTML «No incluye» + JS nota: añadir autoconsumo colectivo, «batería virtual» (oferta comercial, no regulada) e ICIO/licencia como coste («hasta el 4 % del presupuesto si no está incluido»); label `coste`: «llave en mano, con legalización».

## 5. Supuestos
Aceptables (declarados): 25 años, 0,5 %/año, euros constantes con sensibilidad +3 %, descuento 3 %, mantenimiento 0 (declarado; cambio de inversor fuera), % autoconsumo constante, PVGIS por capital, precio evitado PVPC × 1,2718 en península y Baleares, bloqueo > 100 kWp, IEE mínimo ignorado.
Erróneos: compensación sin IEE/IVA (C1); tope descrito solo como «anual vs mensual» cuando con PVPC además excluye peajes y cargos (C2).

## 6. Casos nuevos para test.json (JS actual → tras C1, tol 1 €)
- 8 kWp, 9.000 €, 3.000 kWh, 20 %, 1.667, 0,20, 0,10 (tope activo): comp1 52,33 → 66,56; años 15,47 → 15,00; neto25 5.480 → 6.000.
- 5 kWp, 5.000 €, subv 6.000, 2.000 kWh, 80 %, 1.600, 0,18, 0,06 (subv > coste; autoconsumo limitado al consumo): neto 0, años 0, comp1 0, neto25 9.000 (igual tras C1).
- 4 kWp, 6.000 €, 4.000 kWh, 0 %, 1.610, 0,18, 0,07: comp1 450,80 → 573,36; años 13,74 → 10,72.
Re-verificación: Sonnet basta (C1 es fórmula ya fijada aquí; C2-C5 son texto).
