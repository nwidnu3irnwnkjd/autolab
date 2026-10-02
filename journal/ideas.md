# Ideas e innovación — Investigador
Fecha: 2026-10-01. Fuentes en `journal/competencia.md`. Volumen = estimación cualitativa por señales de SERP y estacionalidad (sin Keyword Planner); validar con Search Console a 28 días.

## 1. Doce calculadoras nuevas (priorizadas)
Criterio: decisión con números del usuario + dato que podamos precargar y fechar + competencia sin veredicto. Ninguna repite el backlog actual.

| # | Slug | Keyword principal | Tema | Intención | Dificultad | Por qué ganaríamos |
|---|---|---|---|---|---|---|
| 1 | calefaccion-gas-aerotermia-electrica | qué calefacción sale más barata | energía | decidir sistema / coste anual | Media | **Estacional ahora (oct-feb).** SERP de instaladores y comercializadoras con cifras dispares (Infobae, Repsol, preciogas). Nadie cruza m², zona climática, precio gas/luz fechado y coste de instalación con años de amortización |
| 2 | subrogar-hipoteca-merece-la-pena | subrogar hipoteca merece la pena / cambiar hipoteca variable a fija | hipoteca | decidir cambio | Media | iAhorro/HelpMyCash/Gibobs captan leads. Ganamos con meses para recuperar gastos (comisión 0,05 % Ley 5/2019) y veredicto neutral. Enlaza con fija-o-variable |
| 3 | cuanto-ahorrar-para-comprar-casa | cuánto dinero necesito para comprar una casa | hipoteca | planificar | Media | Competencia (Selectra, Fotocasa, iAhorro) usa "30-35 %" genérico. Ganamos con ITP/IVA+AJD **por comunidad** precargado y años para llegar con tu ahorro mensual. Ya propuesta como guía en SEO-GEO |
| 4 | rescate-plan-pensiones-capital-o-renta | rescatar plan de pensiones capital o renta | impuestos | decidir forma de rescate | Media | Fundación Mapfre/Santalucía tienen simulador; casi todo lo demás son artículos. Ganamos con reducción 40 % pre-2007 + tramos IRPF + reparto óptimo en años |
| 5 | seguro-todo-riesgo-o-terceros | seguro todo riesgo o terceros | coche | decidir cobertura | Baja-media | Solo aseguradoras y corredores (Prima, Rastreator, Motor16). Regla del 10 % del valor venal muy calculable: valor por antigüedad + prima + franquicia → veredicto |
| 6 | placas-solares-merece-la-pena | placas solares merece la pena | energía | decidir inversión | Alta | SERP lleno de instaladores. Ganamos con neutralidad + deducción IRPF + IBI + compensación de excedentes, pero con más esfuerzo |
| 7 | guarderia-cuidadora-o-reducir-jornada | guardería o reducir jornada qué sale más barato | familia | decidir cuidado | Baja | Hay calculadoras de "cuánto pierdo con reducción" (datosfiscales, jornadareducida.es) pero **nadie compara las tres opciones** con deducción 1.000 € por guardería y cotización protegida 2 años |
| 8 | autonomo-o-asalariado | cuánto tengo que facturar como autónomo para cobrar lo mismo | trabajo | decidir empleo | Media-alta | netocalc, fiscaliza, billeo, Fube ya existen. Ganamos con "facturación equivalente" como respuesta directa y cuota por tramos 2026 |
| 9 | coche-nuevo-o-seminuevo | coche nuevo o seminuevo | coche | decidir compra | Media | Mayoría de resultados de Latinoamérica o vendedores (Autohero). Depreciación + garantía + financiación en coste total español |
| 10 | capitalizar-paro-o-cobrarlo | capitalizar el paro merece la pena | trabajo | decidir | Media | Gestorías y asesorías. Riesgo: roza "trámite"; enfocar solo en la decisión económica |
| 11 | autonomo-o-sociedad-limitada | autónomo o SL a partir de cuánto | trabajo | decidir forma jurídica | Alta | Muchas gestorías; cifra umbral 40-60 k€ repetida sin cálculo. Esfuerzo fiscal alto |
| 12 | excedencia-o-reduccion-jornada | excedencia o reducción de jornada | familia | decidir | Baja-media | Pareja natural de #7; pocas calculadoras, mucho texto legal |

**Añadidas al backlog (8):** 1, 2, 3, 4, 5, 7, 6, 8. Orden recomendado de construcción: 1 (estacional ya), 2 y 3 (clúster hipoteca, el más citado por AIO), 7, 5, 4, 8, 6. `declaracion-conjunta-o-individual` debe estar publicada antes de marzo 2027 (pico abril-junio).

## 2. Innovación: tres formatos que una IA generalista no replica
| Idea | Qué es | Por qué no lo replica una IA | Esfuerzo | Impacto |
|---|---|---|---|---|
| **A. Barómetro mensual "Entre Muchos"** (`/barometro/2026-10/`) | Cada mes, un informe automático con dato propio: euríbor de equilibrio fija/variable, años de equilibrio alquilar/comprar por capital, €/100 km por motorización, coste de calefacción por sistema. Mismo motor que las calculadoras con los parámetros del mes; serie histórica enlazable y gráfico | Es un dato **nuevo y fechado** que no existe en ningún otro sitio: la IA solo puede citarlo. Las AIO citan datos específicos, recientes y con fuente | Medio (1 script + plantilla; parámetros ya en `params.json`) | Alto (citas IA, enlaces de prensa/blogs, frescura) |
| **B. "Plan completo" encadenado** | Un recorrido de 3-4 pasos que reutiliza resultados: ¿cuánto ahorrar? → ¿fija o variable? → ¿amortizo o invierto? (o coche: motor → compra/renting → seguro). Resultado final: resumen de decisiones con cifras y enlace compartible (estado en la URL, sin datos personales en servidor) | La IA responde una pregunta suelta; no mantiene un modelo numérico coherente entre decisiones con tus cifras | Medio-alto (estado compartido en `app.js`, sin backend) | Alto en engagement y páginas/sesión; medio en SEO |
| **C. Informe personal descargable (PDF/imprimible)** | Botón "Descargar mi informe": tabla de escenarios, supuestos, fuentes y fecha; generado en el navegador (`window.print` con CSS de impresión) | Documento auditable con tus números para llevar al banco/asesor; la IA no te da un entregable con supuestos trazables | Bajo (CSS print + plantilla) | Medio ahora; base de la monetización futura (informe premium 3-5 € del brief) |

Prioridad: **C** (barato, mejora todas las calculadoras ya), **A** (palanca GEO principal, coincide con la palanca 4 de SEO-GEO), **B** cuando haya 8+ calculadoras en un clúster.

## 3. Proyecto 2 — evaluación y recomendación
Sin volúmenes exactos (pendiente Keyword Planner). Evaluación por señales reales del SERP del 2026-10-01.

| Candidato | Demanda (señal) | Competencia ES | Riesgo YMYL | Monetización | Datos | Veredicto |
|---|---|---|---|---|---|---|
| **Alimentos** (cuánto dura / se puede congelar) | Alta y diaria, evergreen, cola larga alimento × estado (crudo/cocinado/abierto/congelado) | **Fragmentada**: medios y blogs con un artículo por alimento; tablas únicas de ~20-25 alimentos (OCU 2024, meskeia); nadie con base de datos por alimento | Medio (seguridad alimentaria) → mitigable citando AESAN/USDA y regla "en caso de duda, tirar" | Baja (CPC bajo; publi + menaje/congeladores) | **USDA FoodKeeper con versión en español (JSON)** + AESAN: dato estructurado gratis | **Recomendado** |
| Mascotas (puede comer mi perro X) | Alta | Alta: Rover, Purina, Hill's, Wamiz, Wakyma, clínicas | Alto (toxicidad, urgencias veterinarias) | Media-alta (seguros de mascota) | ASPCA (EN), AVEPA (parcial); sin dataset abierto en ES | Segundo; más riesgo y competencia |
| Clima por mes | Alta | **Saturada**: WeatherSpark ES, Avionero, climate-data, ViajaTiempo, hikersbay | Bajo | Media (afiliación viajes) | Open-Meteo (atribución, uso comercial de pago) | Descartar como proyecto solo |
| Festivos/puentes | Muy alta y estacional (oct-ene) | Alta: calendariosnacionales (por municipio), misfestivos, calendario-laboral.org, cazadores de puentes | Bajo | Media | BOE + boletines; 8.000 municipios a mantener cada año | Descartar ahora; quizá como herramienta "optimizador de puentes" dentro de otro sitio |

**Recomendación: alimentos** (slug sugerido `alimentos`). Encaja con el principio "capa de decisión": cada página responde "¿me lo como, lo guardo o lo tiro?" con una herramienta propia (calculadora "lo cociné el día X → seguro hasta el día Y", estado de la nevera, corte de luz).

### Plan de arranque de 5 días
1. **Día 1 — datos:** bajar FoodKeeper ES/EN a mano (el script recibe 403) y la tabla AESAN; normalizar a `data/alimentos.json` (alimento, categoría, estado, nevera, congelador, despensa, fuente, nota de seguridad). Revisar 30 entradas a mano contra AESAN. Andoni: decidir dominio (cambio con coste → PENDIENTE-ANDONI).
2. **Día 2 — plantilla:** reutilizar el generador de `decidir` (Python puro): página por alimento con respuesta en la primera frase, tabla nevera/congelador/despensa, herramienta "¿hasta cuándo?", señales de deterioro, fuentes, disclaimer sanitario. Schema Article + FAQ por entendimiento.
3. **Día 3 — 20 páginas + 2 hubs** (lista abajo), `check.py` adaptado: cada cifra de la página = cifra del JSON.
4. **Día 4 — herramientas transversales:** "se fue la luz: ¿qué tiro?" (AESAN: <4 h no hace falta tirar) y "¿se puede volver a congelar?". Legales, robots, sitemap, llms.txt, IndexNow.
5. **Día 5 — publicación y medición:** deploy, Search Console + Bing, enlazado interno por categoría, línea base de métricas; plan para escalar a 150 páginas solo si hay impresiones a 28 días.

### Primeras 20 páginas
1. cuánto dura el pollo cocinado en la nevera
2. cuánto dura la carne picada en la nevera
3. cuánto duran los huevos (y prueba del agua)
4. cuánto dura el arroz cocido en la nevera
5. cuánto dura el pescado fresco en la nevera
6. cuánto dura el jamón cocido / fiambre abierto
7. cuánto dura la leche abierta
8. yogur caducado: ¿se puede comer?
9. cuánto dura el queso abierto (curado vs fresco)
10. ¿se puede congelar el queso?
11. ¿se puede congelar la nata / la leche?
12. ¿se puede congelar el pan?
13. cuánto dura la tortilla de patatas en la nevera
14. cuánto dura un guiso / lentejas en la nevera y congelador
15. cuánto dura el marisco cocido (gambas, mejillones)
16. ¿se puede volver a congelar la carne descongelada?
17. cuánto aguanta la comida congelada si se va la luz
18. consumir preferentemente vs fecha de caducidad
19. cuánto dura la salsa de tomate / tomate frito abierto
20. cuánto dura la fruta cortada (aguacate, manzana)
Hubs: `/carnes/`, `/lacteos/` (y un índice general con buscador).

---
# Ciclo 9 · 2026-10-02 — 8 calculadoras NO fiscales (Investigador, Sonnet con web)
**Honestidad sobre volúmenes:** sin Keyword Planner ni acceso a autocompletar. «Evidencia» = nº de resultados/competidores y titulares reales de la SERP del 2026-10-02 (desde EE. UU.). Volumen cualitativo (A alto / M medio / B bajo) por esa señal; validar con Search Console a 28 días. Todas ya añadidas al final de `projects/decidir/data/backlog.md`. Ninguna depende de tablas legales: lo pone el usuario o sale de `live.json` (gasolina95, diesel, luz_pvpc, euribor12m).

| # | Slug | Keyword principal | Vol. | Tema | Evidencia | Por qué ganaríamos | Datos (origen) | YMYL |
|---|---|---|---|---|---|---|---|---|
| 1 | reparar-o-comprar-electrodomestico | reparar o comprar lavadora nueva | A | hogar | 9 resultados: OCU, Infobae, NerdWallet, reparadores; todos «regla del 50 %», ninguna calculadora | Veredicto con presupuesto de reparación, edad, precio nuevo, riesgo de 2.ª avería y consumo extra; coste por año de vida restante | Inputs usuario (presupuesto, edad, precio nuevo, kWh etiqueta); luz_pvpc para el consumo | Bajo |
| 2 | cambiar-electrodomestico-antiguo-merece-la-pena | cambiar electrodomésticos antiguos por clase A merece la pena | A | energía | eldiario.es, elEconomista, Fintonic, Telecinco (jun-2026 «hasta 300 €/año»), mielectro; cifras dispares, sin calculadora | Años de amortización = (precio nuevo − valor actual) / (Δ kWh × €/kWh del día); cifra propia frente a titulares inflados | kWh/año de la etiqueta (usuario), luz_pvpc (live.json), vida útil (param) | Bajo |
| 3 | coche-nuevo-o-seminuevo | coche nuevo o de segunda mano cuál compensa | A | coche | Autohero, Clicars, Autokey, State Farm (EE. UU.) + calculadoras de depreciación sueltas; ninguna da coste total a N años | Coste total a N años: depreciación (curva editable), garantía, mantenimiento, financiación, seguro; año de equilibrio. Enlaza con comprar-coche-o-renting | Inputs usuario; seguro y mantenimiento como supuestos fechados en params | Bajo |
| 4 | tren-avion-o-coche | tren avión o coche qué sale más barato | A (estacional: puentes, Navidad, verano) | viajes | Omio, lostraveleros, mundukos: tablas por ruta (Madrid-Barcelona bus 51, tren 59, coche 102, avión 117 €, sin fecha) | Tu coste real de coche (consumo × gasolina95 de live.json + peajes + desgaste), nº de viajeros que divide el coche, extras de avión (equipaje, traslado) y tiempo puerta a puerta | Precios de billete y peajes: inputs; carburante: live.json; km: input | Bajo |
| 5 | bici-electrica-o-transporte-publico | bici eléctrica o transporte público cuánto se ahorra | M-A | ahorro | rodarelectric (vendedor), Rankia, urbancitymove, SALAMANCArtv (sep-2026); datos «abono 21,80 € Madrid» en artículos | Años para amortizar la bici frente a abono o coche, con carga, mantenimiento, seguro, robo; 3 comparaciones en una | Abono y precio bici: inputs (con ejemplos por ciudad); luz_pvpc para carga | Bajo |
| 6 | coche-propio-o-carsharing-o-vtc | tener coche o carsharing cuánto cuesta al mes | M | coche | Avancar, adslzone, elespanol 2018, LinkedIn; datos obsoletos (car2go/emov) | Punto de corte en km/mes y salidas/mes a partir del cual el coche propio gana; coste fijo real del coche (seguro, ITV, parking, depreciación) | Todo input; carburante: live.json | Bajo |
| 7 | cambiar-ventanas-aislamiento-merece-la-pena | cambiar ventanas merece la pena ahorro | M-A (estacional oct-feb) | hogar | Leroy Merlin, OCU, certificadosenergeticos, humedades.com: «amortiza en 5-10 años» sin cálculo | Amortización con TU factura de calefacción y TU % de ahorro (rango pesimista/base/optimista), ayudas como entrada para no fijar normativa | Factura calefacción y presupuesto: inputs; precio kWh de calefaccion-gas-aerotermia (params) | Bajo-medio (ahorro prometido: usar rangos) |
| 8 | universidad-publica-o-privada-o-master | universidad pública o privada cuánto cuesta | A (pico jun-sep) | familia | Infobae (ene-2025), Bankinter, OCU, yaq, dineo, cuentasclaras: tablas €/crédito por CCAA, sin herramienta de decisión | Coste total del grado/máster + vivir fuera vs en casa + beca opcional + año de equilibrio frente a salario esperado (input); no promete sueldos | €/crédito, alojamiento, salario: inputs; medias públicas como ejemplo fechado | Medio (decisión familiar; sin cifras de empleabilidad inventadas) |

**Descartadas con motivo:** bombillas LED (amortiza en meses, decisión trivial y SERP de vendedores; mejor como bloque dentro de #2), aire acondicionado vs ventilador (informativa, consumo; posible bloque estacional), seguro de hogar y fibra vs móvil (precio depende de cotizadores propietarios: sin dato vivo ni dato del usuario fiable), lavavajillas (sub-caso de #1/#2).

## Tres formatos de contenido de apoyo (guías que enlazan a varias calculadoras)
1. **«Cuánto cuesta de verdad tener coche en España» (guía-hub, ~1.500 palabras + tabla €/km):** enlaza a diesel-gasolina-hibrido-electrico, comprar-coche-o-renting, seguro-todo-riesgo-o-terceros, coche-nuevo-o-seminuevo, coche-propio-o-carsharing-o-vtc, bici-electrica-o-transporte-publico. Cifra citable por AIO: coste anual medio con fecha (del Barómetro).
2. **«Checklist de tu casa antes del invierno» (estacional oct-nov):** ventanas/aislamiento, calefacción gas-aerotermia-eléctrica, luz fija o indexada, placas solares, cambiar electrodomésticos. Una tabla «qué hacer primero» ordenada por años de amortización con tus datos (enlaza 5 calculadoras).
3. **«Plan de compra de vivienda en 4 pasos» (formato B de la sección 2):** cuánto ahorrar → alquilar o comprar → fija o variable → amortizar plazo/cuota → amortizar o invertir. Hub de mayor valor y mejor encaje con AIO (hipotecas: comparadores 43 % de citas). Alternativa ligera: «Black Friday sin arrepentirse» (nov: reparar o comprar, cambiar electrodoméstico, contado o financiar).

# Ciclo 10 · 2026-10-02 — reposición del backlog (Investigador, Sonnet con web)
**Honestidad:** WebSearch desde EE. UU.; sin Keyword Planner ni autocompletar. «Evidencia» = nº de resultados y titulares reales de la SERP de hoy. Volumen cualitativo A/M/B; validar con Search Console a 28 días. Las 10 ya están al final de `projects/decidir/data/backlog.md`. Todas son inputs del usuario salvo lo indicado; los parámetros fiscales pasan por `journal/fiscal-fuentes.md` + Verificador Opus.

| # | Slug | Keyword principal | Vol. | Tema | Evidencia SERP 2026-10-02 | Por qué ganaríamos | Datos (origen) | YMYL | Estacionalidad / publicar |
|---|---|---|---|---|---|---|---|---|---|
| 1 | donativos-irpf-cuanto-desgrava-y-cuanto-donar | cuánto desgravan las donaciones | M-A (pico dic y abr-jun) | impuestos (F) | Idealista (1-may-2026), Taxdown, Cienvidas, AEAT manual, andabogados: todo artículos con el ejemplo 300 € → 220 € | Calculadora con escala 80 %/40 %/45 % recurrencia, límite 10 % base liquidable y coste neto real de donar X; no hay veredicto de «cuánto donar para optimizar» | Arts. 68.3 LIRPF y 19-20 Ley 49/2002 (AEAT manual IRPF 2025); autonómicas = fuera de v1 | Medio | Publicar antes del 15-nov (se dona antes del 31-dic); repunta en Renta |
| 2 | jubilacion-anticipada-o-demorada | jubilación anticipada o demorada qué compensa | A | jubilación (F/regulada) | javilinares, calculadoralaboral, VidaCaixa, calculates, laboria, calculadora-jubilacion.com (demorada +4 %/año): calculan penalización o pensión, no comparan ambas con años para recuperar | Veredicto: pensión neta acumulada hasta los 90-95 años por escenario, edad de equilibrio y escenarios de longevidad; coeficientes 3,26-21 % (reforma 2023) | Coeficientes y edades LGSS (arts. 208, 210; verificar BOE), base reguladora = entrada del usuario | **Alto** | Evergreen; pico ene y sep-oct; publicar antes de dic |
| 3 | deposito-letras-o-fondo-monetario | depósito o letras del Tesoro o fondo dónde meter ahorros | A | ahorro (F) | Rankia, Raisin, finanzasdigitales, mundoofertas, ahorrainversion (calculadora solo Letras), cuantomecuesta: Letras 12 m 2,57-2,65 %, depósitos hasta 3,2 % TAE | Neto tras IRPF ahorro (19-30 %) a N meses; cuenta de comisión de custodia bancaria vs Tesoro Directo y diferimiento en fondos; comparador a 3 con fechas | Tipos = entrada del usuario con fecha; Tesoro (subastas); escala ahorro art. 66 LIRPF | Medio-alto | Pico ene (nuevo año) y tras cada bajada de tipos; publicar dic |
| 4 | teletrabajo-o-oficina-coste-real | cuánto ahorro teletrabajando | A | trabajo | OCU vía Genbeta (264 €/mes coche >45 km), Xataka (47 % ahorra >100 €/mes), Xataka (7 % menos salario) | Ahorro neto anual con TU trayecto, comida, luz/calefacción en casa (luz_pvpc) y desplazamiento; contrapone pérdida de plus/salario | Todo input; precio luz y gasolina de live.json | Bajo | Evergreen; pico sep-oct y ene |
| 5 | seguro-salud-privado-merece-la-pena | merece la pena un seguro de salud privado | A | seguros | Kelisto, Acierto, Generali, polizamedica (35-55 €/mes jóvenes, 90-150 € >60 años), adeslas, Periodista Digital | Prima acumulada hasta los 65 años (con subida por tramo) vs gasto equivalente en pago por uso; sin vender pólizas | Prima = entrada; escalado edad = hipótesis editable fechada | **Medio-alto** (salud): no recomienda cancelar cobertura | Pico ene y sep-oct; publicar dic |
| 6 | seguro-mascota-merece-la-pena | cuánto cuesta un perro al año / seguro mascota merece la pena | A | mascotas | Línea Directa, Santévet, Aon, Finhabits (RC 35-50 €; seguros 150-500 €) | Coste anual por raza/edad + probabilidad de gasto grande vs prima; fondo propio de emergencia como alternativa | Inputs; RC obligatoria en perros PPP según normativa (verificar) | Medio | Evergreen; Navidad y verano |
| 7 | fibra-y-movil-juntos-o-por-separado | fibra y móvil juntos o por separado qué sale más barato | A | telefonía | xatakamovil, comparaiso, Multioferta, Selectra, quecomparo (ahorro «20-30 %», «hasta 17 €/mes»), mundoofertas | Coste a 24 meses con permanencia, subida de precio tras promoción, líneas extra y penalización; **todo con precios que mete el usuario** | Inputs (sin scraping de tarifas) | Bajo | Pico sep-nov y Black Friday; publicar antes del 15-nov |
| 8 | portatil-o-movil-comprar-renting-o-financiar | comprar o renting de ordenador/móvil | M-A | compras | declarando.es, rentingpc, alfacomputer, tecfys, emendu (vendedores); nadie con coste total a N años | TCO a 2-4 años con valor residual, mantenimiento y (autónomo) IVA/IRPF deducible como opción; neutral frente a vendedores | Inputs; deducibilidad = nota genérica sin cifras | Bajo (con aviso autónomo) | Pico Black Friday (27-nov) y vuelta al cole |
| 9 | comprar-o-alquilar-herramienta | comprar o alquilar herramienta (taladro, hormigonera…) | B-M | hogar/bricolaje | Sin resultados sólidos en la búsqueda de hoy: **evidencia débil**, validar con SC antes de construir; sustituible por seguro-mascota si hay duda | Número de usos a partir del cual compensa comprar; el coste de oportunidad y el trastero | Inputs | Bajo | Primavera y otoño (obras); publicar feb |
| 10 | seguro-vida-hipoteca-banco-o-externo | seguro de vida de la hipoteca banco o externo cuánto ahorro | A | hipoteca | (no re-buscado hoy) tema ligado al clúster hipoteca; Ley 5/2019 permite póliza externa: **verificar competencia antes de construir** | Ahorro a 25 años de póliza externa vs vinculada (bonificación del tipo perdida) con veredicto de punto de equilibrio | Bonificación = entrada; Ley 5/2019 art. 14 | Medio | Evergreen; encaja tras subrogar y fija-variable |

**Descartadas/reserva:** deducciones por alquiler por comunidad (volumen A en abr-jun: 14 CCAA con porcentajes distintos, p. ej. Madrid 30 % hasta 1.237,20 € y Cataluña 10 % hasta 500 €, según Rankia/Xataka; **no hay verificación oficial** de las 14 normas → entra en c17 solo con Verificador Opus; slug reservado `deduccion-alquiler-vivienda-por-comunidad`); familia numerosa/hijos (estatal ya en declaracion-conjunta); herencias/donaciones por CCAA (17 normas sin fuente verificada: descartar hasta tener tabla BOE); seguro de hogar (cotizador propietario); coche de alquiler vs transporte (cubierto por tren-avion-o-coche y coche-propio-o-carsharing). Ya presentes en la sección 1 y aún no en backlog: capitalizar-paro-o-cobrarlo, autonomo-o-sociedad-limitada, excedencia-o-reduccion-jornada.

## Tres guías de apoyo estacionales (otoño-invierno)
1. **«Tu casa en invierno: calefacción, luz y aislamiento» (publicar antes del 15-oct, hub oct-feb):** tabla «qué hacer primero» por años de amortización. Enlaza calefaccion-gas-aerotermia-electrica, luz-fija-o-indexada, cambiar-ventanas-aislamiento-merece-la-pena, cambiar-electrodomestico-antiguo-merece-la-pena, placas-solares-merece-la-pena, teletrabajo-o-oficina-coste-real.
2. **«Black Friday y rebajas sin arrepentirte» (publicar antes del 15-nov; BF 27-nov-2026; rebajas enero):** checklist de decisión comprar/reparar/financiar. Enlaza reparar-o-comprar-electrodomestico, cambiar-electrodomestico-antiguo, contado-o-financiar, portatil-o-movil-comprar-renting-o-financiar, fibra-y-movil-juntos-o-por-separado, coche-nuevo-o-seminuevo.
3. **«Campaña de la Renta 2027: qué decidir antes de abril» (indexar en enero; la campaña es abr-jun):** calendario de decisiones (conjunta o individual, aportar o rescatar, donar antes del 31-dic, autónomo, alquiler). Enlaza declaracion-conjunta-o-individual, donativos-irpf-cuanto-desgrava-y-cuanto-donar, plan-pensiones-o-fondo-indexado, rescate-plan-pensiones-capital-o-renta, deposito-letras-o-fondo-monetario, autonomo-o-asalariado, jubilacion-anticipada-o-demorada. Cada cifra con año fiscal y fuente (YMYL).

## Priorización de los siguientes 8 ciclos (11-18; 2 calculadoras por ciclo)
Supuesto: rescate-plan-pensiones-capital-o-renta se cierra en el ciclo 10. F = fiscal/regulada con cadena Constructor + Verificador Opus (Constructor deja parámetros y 3 casos; Opus verifica norma y casos antes de publicar; si no cierra, se sustituye por la siguiente no fiscal y no se detiene el ciclo). NF = no fiscal.
| Ciclo | Construir | Motivo / fecha límite |
|---|---|---|
| 11 | donativos-irpf-cuanto-desgrava-y-cuanto-donar (F) + portatil-o-movil-comprar-renting-o-financiar (NF) | Donaciones se hacen antes del 31-dic; Black Friday 27-nov. Guía 2 |
| 12 | fibra-y-movil-juntos-o-por-separado (NF) + seguro-vida-hipoteca-banco-o-externo (NF; buscar competencia antes) | Ofertas de otoño y clúster hipoteca; guía 1 ya publicada |
| 13 | jubilacion-anticipada-o-demorada (F, YMYL alto: 2 verificadores o revisión doble de coeficientes) + teletrabajo-o-oficina-coste-real (NF) | Búsqueda de pensión sube en dic-ene; vuelta a oficina |
| 14 | deposito-letras-o-fondo-monetario (F) + seguro-salud-privado-merece-la-pena (NF) | «Dónde meter ahorros 2027» y altas de seguros en enero; actualizar tipos |
| 15 | seguro-mascota-merece-la-pena (NF) + capitalizar-paro-o-cobrarlo (F; si el verificador no cierra, comprar-o-alquilar-herramienta) | Enero; roza trámite: solo decisión económica |
| 16 | excedencia-o-reduccion-jornada (F-ligera) + revisión de datos: params/live, IRPF, cuotas autónomos, peajes | Antes de enero actualizar parámetros 2027 |
| 17 | deduccion-alquiler-vivienda-por-comunidad (F; solo con tabla BOE verificada de las CCAA incluidas, el resto «consulta tu comunidad») + guía 3 (Renta 2027) y mínimos autonómicos pendientes | Pico abril-junio; indexar en enero-febrero |
| 18 | autonomo-o-sociedad-limitada (F) + llamada al Investigador (cada 6 ciclos) con datos de Search Console | Trimestre fiscal y Renta; reponer con impresiones reales |
Regla: con ≥ 30 calculadoras y datos de SC, un ciclo de refuerzo (veredicto, escenarios, FAQ en las 3 con más impresiones) puede sustituir a uno de nuevas. Backlog tras c18: 0 pendientes; llamar al Investigador en c16.
