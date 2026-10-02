# Verificación fiscal independiente (Opus) · obligado-a-declarar-renta-dos-pagadores · 2026-10-02
VEREDICTO: PUBLICABLE CON CAMBIOS (5 cambios obligatorios, todos de texto/etiqueta; 0 errores de fórmula)

## Fuentes leídas hoy (BOE consolidado, API XML)
- LIRPF art. 96 (última versión BOE-A-2025-1136, 23/1/2025): 2.a 22.000; 2.b 1.600 conjunto; 2.c 1.000 conjunto; párrafo «en ningún caso» 1.000 + pérdidas < 500; RETA/Mar «en cualquier caso»; 3.a-d 15.876; 4 planes/patrimonios protegidos/doble imposición. Historial del 96.3: 15.000 (BOE-A-2022-22128) → 15.876 por BOE-A-2024-12944 (RDL 4/2024, vigencia 28/6/2024); RDL 9/2024 y su derogación no cambian la cifra. El RDL publicado el 30/9/2026 no toca el art. 96.
- RIRPF art. 61 (última mod. BOE-A-2023-24841): sigue diciendo 15.000 €; 61.1 «cuando ejerciten tal derecho»; 61.3.A.2.º.d cita solo 80.1.3.º y 4.º; 61.4 se refiere a quien ESTÁ obligado.
- Ley 19/2021 IMV art. 36.1.f (titular) y 36.2.c (integrantes de la unidad de convivencia): «Presentar anualmente declaración correspondiente al IRPF». Confirmado en la ley (no solo en el Manual).
- LIRPF art. 103.1: la devolución se practica sobre la «cuota resultante de la autoliquidación».

## Interpretaciones dudosas del Constructor
1. a/b/c independientes: CORRECTA (cada letra con su propio límite, «exclusivamente de las siguientes fuentes»; 22.000 + 1.600 + 1.000 no obliga). Las excepciones del 96.3.a (1.º ≤ 1.500; 2.º pasivas con procedimiento especial) solo quitan la causa «varios pagadores»; b/c/d se acumulan y bajan el límite por sí solas: así está implementado.
2. «Con el límite de X»: X exacto no obliga. CORRECTA.
3. 1.000 conjunto con «otras rentas» (obligado si > 1.000; «depende» si ≤ 1.000): CORRECTA y prudente.
4. Pagador no obligado a retener, input único: CORRECTA (ley: «el pagador»; RIRPF art. 76).
5. Pasivas con procedimiento especial (89.A) sin verificar requisitos: ACEPTABLE (lo elige el usuario; declarado).
6. Planes como obligado directo: ACEPTABLE, pero falta «si quieres aplicar la reducción» (61.1 «cuando ejerciten tal derecho") → cambio 4.
7. Tipo fijo = 80.1.3.º y 4.º: CORRECTA (61.3.A.2.º.d).
8. Pensión compensatoria sin comprobar exención: ACEPTABLE (la compensatoria nunca está en el art. 7.k; los alimentos de los padres sí); pero la pensión es rendimiento del trabajo (art. 17.2.f) y debe sumarse → cambio 3.
9. Conjunta no modelada: ACEPTABLE (declarado).
10. Ejercicio 2026 con texto vigente: ACEPTABLE.
11. Exclusiones (descendientes, exentas, no residentes, pérdidas ≥ 500, IIC 96.2.b 2.º, forales bloqueados con estado 3): ACEPTABLES y declaradas; ninguna invierte el veredicto salvo pérdidas ≥ 500 e IIC, que se declaran.
IMV: lectura CORRECTA (art. 36 Ley 19/2021), mal citada → cambio 2.

## Cambios obligatorios (archivo · qué · por qué)
1. calcs/obligado-a-declarar-renta-dos-pagadores.json faqs[2] (y si se cita en JS avisoDeclarar): sustituir «(art. 61.4 del Reglamento)» por «(art. 103.1 de la Ley del IRPF: la devolución se calcula sobre la autoliquidación)». El 61.4 RIRPF habla de quien sí está obligado; no demuestra la frase para el no obligado. [patrón 4: cita legal]
2. content/…html (lista «Qué obliga… sea cual sea el importe») + json faqs[3] + sources: citar «Ley 19/2021, art. 36.1.f y 36.2.c» en vez de «Ley 19/2021, según el Manual». [patrón 4]
3. json inputs t1/t2/t3 (o nota bajo la opción esp=1) + html «Cómo usar»: «Si cobras pensión compensatoria o alimentos no exentos, inclúyelos como un pagador más (son rendimientos del trabajo, art. 17.2.f LIRPF); si te los paga un particular, marca también “pagador no obligado a retener”». Sin esto, 15.000 de sueldo + 1.000 de compensatoria sin introducir da «no obligado» cuando sí lo está (16.000 > 15.876). [patrón 6: omitido que invierte el veredicto]
4. json inputs[6] (select único «esp»): añadir en la etiqueta o una nota «Si te aplica más de una, elige primero alta en autónomos, ingreso mínimo vital o plan de pensiones (obligan siempre)»; mejor aún, convertir RETA/IMV/planes en casillas aparte. Hoy, quien tiene compensatoria + plan de pensiones y elige la compensatoria puede obtener «no obligado». En la opción y SUP 11: «…si quieres aplicar la reducción o la deducción (art. 61.1 RIRPF)». [patrón 6 / 1]
5. json lead y veredicto: añadir el ámbito «(en territorio común; País Vasco y Navarra tienen sus propias normas)» a la primera frase, que hoy afirma «Estás obligado…» sin condición territorial. [patrón 3]
Recomendado (no bloquea): SUP 7 y etiqueta «inmo»: «ayudas VPO» → «ayudas a vivienda protegida y demás ganancias derivadas de ayudas públicas» (96.2.c literal).

## Texto ≤ cálculo (frases revisadas)
- Lead/veredicto 22.000 / 15.876 / 1.500; 18.000+2.000 obligado, 18.500+1.500 no, 18.500+1.501 sí: demostradas (norma y JS) · sí.
- FAQ 1, 2, 5 (RDL 4/2024, RDL 9/2024 sin efecto): demostradas · sí. FAQ 3: frase cierta, cita errónea → cambio 1. FAQ 4: sí, salvo cita IMV → cambio 2.
- «Aunque no estés obligado, puede convenirte declarar»: bien condicionado («si te han retenido de más o tienes deducciones»); no induce a no declarar. Sin absolutos sin condición.
- Nota JS 15.876 vs 15.000: correcta (ley posterior y de rango superior; AEAT aplica 15.876).

## Ejecución
- Oráculo del Constructor: 16 fijos + 700 aleatorios, 0 discrepancias. ops/check.py decidir: OK 3922/3922.
- 14 escenarios propios desde la norma (Python independiente, scratchpad, vs JS por osascript): 22.000/22.001; 15.000+876+1 (resto 877 → 22.000); 10.000+5.000+1.000 (exceso 124); 22.000+1.600+1.000 (no obligado); otras rentas 1.100 (obligado); compensatoria 15.000 / 16.000 con no-retención (exceso 124); 1.500+1.500; foral; 0 pagadores; 15.877+1.501; pasivas especiales 24.000; RETA. Veredicto exacto y cifras ±1 €: 0 discrepancias.
- Casos nuevos para test.json: {t1:15000,t2:1000,esp:1,noRet:1}→estado 1, exceso 124; {t1:22000,capRet:1600,inmo:1000}→estado 0; {t1:15000,t2:876,t3:1}→estado 0.
