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

# Ciclo 10b · 2026-10-02 — 12 calculadoras nuevas (Investigador, Sonnet con web)
**Honestidad:** WebSearch desde EE. UU.; sin Keyword Planner. Evidencia = SERP de hoy en 5 consultas (capitalizar paro, caldera, punto de carga, franquicia hogar, autónomo vs SL); las demás por señal estacional y revisión previa: validar con Search Console a 28 días. Vol. A/M/B. F = fiscal/regulada (cadena Constructor + Verificador Opus). Todas en `backlog.md`.

| # | Slug | Keyword | Vol. | Evidencia / competencia | Por qué ganaríamos | Datos (origen) | YMYL | Publicar |
|---|---|---|---|---|---|---|---|---|
| 1 | caldera-reparar-o-cambiar | reparar o cambiar caldera | A (oct-feb) | Ecoinventos, Manairsat, Huelvaya, JAG Alcaide, Selectra: «regla 40-50 %», condensación 20-30 % menos consumo; ninguna calculadora | Años de amortización con tu factura de gas, edad y presupuesto de reparación; enlaza calefaccion-gas-aerotermia | Inputs; precio gas fechado de params | Bajo | Ya (oct) |
| 2 | punto-de-carga-casa-con-o-sin-placas | punto de carga en casa coste placas | M-A | Autosolar (800-1.600 € vivienda, 1.600-2.200 € garaje comunitario), Toyota, cargaencasa, ritest (calculadora EV vs gasolina); nadie combina carga + placas con luz fechada | €/100 km cargando en valle, con placas o en pública; años de amortizar el cargador | luz_pvpc live.json; precios = input | Bajo | Nov |
| 3 | navidad-cuanto-gastar-sin-endeudarte | cuánto gastar en Navidad presupuesto | A (nov-dic) | No buscado hoy; señal estacional (revisión ciclo 9: Black Friday) | Presupuesto con tus ingresos, regalos, cenas y viaje; coste de financiar a plazos | Inputs | Medio (deuda) | Antes 15-nov |
| 4 | hotel-o-apartamento-viaje-en-grupo | hotel o apartamento turístico cuál sale más barato | M-A | No buscado hoy: validar | Coste por persona con desayuno, limpieza, comisiones y cocina | Inputs | Bajo | Nov y feb |
| 5 | comprar-o-alquilar-trastero | alquilar trastero cuánto cuesta | B-M | Evidencia débil, no buscado | Punto de corte meses/m² frente a comprar | Inputs | Bajo | Feb; sustituible |
| 6 | reformar-o-mudarse | reformar o mudarse | M-A | No buscado hoy | Coste total (obra, ITP, agencia, mudanza, hipoteca nueva) vs reforma; enlaza clúster hipoteca | Inputs; ITP de cuanto-ahorrar-para-comprar-casa | Bajo-medio | Ene |
| 7 | academia-idiomas-presencial-online-o-intensivo | cuánto cuesta aprender inglés | A (sep, ene) | No buscado hoy | Coste por hora y por nivel, no por mes | Inputs | Bajo | Dic |
| 8 | seguro-hogar-con-o-sin-franquicia | seguro de hogar con franquicia merece la pena | M | Pelayo, Santalucía, turboseguros, seguros.insure: «15-40 % menos de prima»; ninguna calculadora. **Viable** solo con primas del usuario (descartamos cotizador) | Prima ahorrada acumulada vs siniestros pequeños esperados a N años (frecuencia editable) | Inputs | Medio | Dic |
| 9 | capitalizar-paro-o-cobrarlo | capitalizar el paro | A | 9 resultados (taxfix, holded, declarando, calculadoralaboral, palenciaasesores, gestoria247): calculan importe (descuento interés legal 3,25 % en 2026); ninguna decide | Capitalizar vs cobrar: neto, cuota, colchón en meses, tarifa plana | Normativa SEPE/LGSS; interés legal: verificar | Medio | Ene |
| 10 | autonomo-o-sociedad-limitada | autónomo o SL a partir de cuánto | M-A | Billeo, Fube, calculaespana, Anfico, Holded (umbral 40-50 k€): 5 calculadoras ya | Umbral con retribución del administrador, cuota 2026 y reparto de dividendos; neutral | IS, IRPF, cuotas (BOE) | Medio | Dic-ene |
| 11 | excedencia-o-reduccion-jornada | excedencia o reducción de jornada | M | Mucho texto legal (revisión previa) | Neto perdido y cotización protegida; pareja de guarderia-cuidadora | ET, LGSS, IRPF | Medio | Ene |
| 12 | comparar-ofertas-de-trabajo-neto-real | comparar ofertas de trabajo bruto neto | A | Netos: saturado en bruto→neto; falta comparar dos ofertas | Dos ofertas en neto + variable + trayecto + teletrabajo | IRPF/SS 2026 (BOE) | Medio | Ene |

**Descartadas:** loterías/juegos (YMYL/ludopatía); seguro de hogar como cotizador; deducción alquiler (reserva, tabla CCAA sin verificar); maternidad/familia numerosa (reserva).

## Revisión de competencia (2026-10-02)
Sin cambios nuevos fuera de lo registrado en competencia.md (Calcuribor/Bankinter en fija-variable). IRPF: autónomo vs SL ya tiene 5 calculadoras; capitalizar paro 6 calculadoras de importe sin decisión. Coche: ritest y ahorrove, todos EV vs gasolina. No verificadas hoy hipotecas y IRPF conjunta.

## Tres guías de apoyo
1. **Navidad y Black Friday sin deudas** (publicar antes del 15-nov): presupuesto, contado o financiar, reparar o comprar, portátil/móvil, navidad-cuanto-gastar.
2. **Declaración de la renta 2027 paso a paso con enlaces** (indexar en enero; campaña abr-jun): enlaces a AEAT/Renta WEB, conjunta o individual, donativos, planes, depósito/Letras, alquiler; cada cifra con año fiscal y fuente.
3. **Cuánto cuesta realmente tener hijos, mascota o coche** (hub citable con cifra fechada): guardería, universidad, seguro mascota, coche; enlaza 8-10 calculadoras.

## Priorización de los siguientes 8 ciclos (11-18; 2 calculadoras por ciclo)
Estado: ya publicadas (marcadas [x]) donativos, portátil/móvil, fibra+móvil, seguro vida hipoteca, teletrabajo, depósito/Letras, seguro salud y mascota. Pendientes: jubilacion (en construcción), herramienta y las 12 de c10b. F = fiscal/regulada: Constructor deja parámetros y 3 casos; Verificador Opus verifica norma y casos antes de publicar; si no cierra, se sustituye por una NF y el ciclo sigue.
| Ciclo | Construir | Motivo |
|---|---|---|
| 11 | caldera-reparar-o-cambiar (NF) + navidad-cuanto-gastar-sin-endeudarte (NF) | Estacional ya; publicar antes del 15-nov; guía 1 |
| 12 | punto-de-carga-casa-con-o-sin-placas (NF) + hotel-o-apartamento-viaje-en-grupo (NF) | Energía; viajes de Navidad |
| 13 | jubilacion-anticipada-o-demorada (F, YMYL alto: doble verificación) + seguro-hogar-con-o-sin-franquicia (NF) | Pensiones dic-ene |
| 14 | capitalizar-paro-o-cobrarlo (F) + academia-idiomas-presencial-online-o-intensivo (NF) | Enero |
| 15 | excedencia-o-reduccion-jornada (F) + reformar-o-mudarse (NF) | Enero; clúster familia/hipoteca |
| 16 | comparar-ofertas-de-trabajo-neto-real (F) + actualización params 2027; llamar al Investigador | Parámetros 2027 |
| 17 | autonomo-o-sociedad-limitada (F) + deduccion-alquiler-vivienda-por-comunidad (F; solo con tabla BOE verificada, si no comprar-o-alquilar-trastero); guía 2 Renta | Pico abr-jun |
| 18 | comprar-o-alquilar-trastero o herramienta (NF, validar con Search Console) + ciclo de refuerzo con datos reales | Reponer con impresiones |

# Ciclo 11 · 2026-10-02 — 14 calculadoras nuevas (Investigador, Sonnet con web)
Volumen = estimación cualitativa (sin Keyword Planner); «evidencia» = lo visto en SERP hoy. Validar con Search Console a 28 días.
Deduplicado contra calcs/*.json y backlog: se descartó «coche de segunda mano vs renting» (solapa con comprar-coche-o-renting y coche-nuevo-o-seminuevo) y «cambiar de operadora» (solapa con fibra-y-movil).

## No fiscales (8)
| Slug | Keyword | Volumen / evidencia | Por qué ganaríamos | Datos y fuente | YMYL | Publicar |
|---|---|---|---|---|---|---|
| suscripciones-cuanto-gasto-al-ano | cuánto gasto en suscripciones al año | Medio-alto (estimación). Hoy: costomas.com, Sharingful (lanzó «primera calculadora» de ahorro por compartir, abr-2026), webtech360; dato: 286 €/hogar/año en audiovisual (EFE/Crónica Global, abr-2026) | Lista precargada de precios por plataforma con fecha, % de uso real y «coste por hora»; competencia es suma simple o vende compartir cuentas | Precios públicos de plataformas (fechar); resto = entrada | Bajo | dic-ene |
| gimnasio-o-entrenar-en-casa | gimnasio o entrenar en casa | Alto estacional enero (estimación). SERP: Infobae (abr-2026), Pulzo, vivemasvidas, blogs fitness; tarifa media 49,10 €/mes citada sin fuente clara | Coste por visita real según asistencia y años de amortización del equipo; todo son artículos | Cuota y equipo = entrada; media orientativa a verificar | Bajo | antes del 15-dic |
| cocinar-en-casa-o-comer-fuera | cuánto ahorro cocinando en casa | Medio (estimación, sin evidencia SERP revisada) | Coste por ración con tiempo valorado y menú del día; veredicto por frecuencia | Entrada del usuario; IPC alimentos INE como referencia | Bajo | ene |
| movil-reacondicionado-o-nuevo | móvil reacondicionado merece la pena | Alto en Black Friday (estimación). Enlaza con portatil-o-movil-comprar-renting-o-financiar | Coste por año de vida útil y garantía (3 años legal en nuevo vs 1 año mínimo... verificar plazos en TRLGDCU art. 120 antes de afirmar) | Precios = entrada; garantía: TRLGDCU | Bajo | nov |
| equipaje-y-asiento-avion-coste-real | equipaje de mano precio low cost / cuánto cuesta facturar | Alto en picos (Navidad, verano) (estimación) | Suma tarifa + maleta + asiento + embarque vs tarifa completa; la tarifa de cada aerolínea es dato volátil, va como entrada con ejemplos fechados | Entrada; no precargar tarifas | Bajo | dic y may |
| marca-blanca-o-marca-ahorro-anual | marca blanca o marca ahorro | Medio (estimación). OCU publica comparativas | Ahorro anual con tu cesta y % de categorías donde compensa; sin calculadora conocida | Entrada; OCU como contexto | Bajo | ene |
| residencia-o-cuidador-a-domicilio | residencia o cuidador a domicilio coste | Medio-alto y creciente (estimación) | Coste mensual y a N años, incluyendo cotización del cuidador y copago; veredicto sin sesgo comercial | Precios = entrada; ayudas de dependencia por CCAA no cifrar sin fuente | Medio: no recomendar cuidado, solo coste; aviso | feb |
| mudanza-empresa-o-furgoneta | cuánto cuesta una mudanza | Alto (estimación). SERP: N26, Cetelem, Habitissimo, Iberfurgo, Sirelo, Calculy: empresa 500-900 € local vs furgoneta 120-250 € (cifras de terceros sin metodología común) | Incluye tu tiempo, ayudantes, combustible, seguro y riesgo de daños; veredicto por m³ y distancia | Entrada; rangos solo como referencia | Bajo | may (pico jun-sep) |

## Fiscales / reguladas (6). Cadena: Constructor deja parámetros + 3 casos; Verificador Opus valida norma
| Slug | Keyword | Volumen / evidencia | Por qué ganaríamos | Datos y fuente | YMYL | Publicar |
|---|---|---|---|---|---|---|
| obligado-a-declarar-renta-dos-pagadores | quién está obligado a declarar la renta / dos pagadores | Muy alto en abr-jun (estimación, es el clásico de campaña) | Resultado sí/no con límites 22.000/15.000 € ya verificados (art. 96 LIRPF) y casos de excepción | LIRPF art. 96; verificado | Medio | indexar en enero |
| irpf-alquilar-vivienda-rendimiento-neto | tributación alquiler vivienda IRPF | Alto (estimación) | Reducción **vigente 2026** según AEAT cuadro art. 23.2: 50 % general; 60 % rehabilitada en 2 años previos; 70 % zona tensionada + joven 18-35 o vivienda social; 90 % zona tensionada con rebaja de renta > 5 %; contratos desde 26-may-2023. Calculadora con gastos deducibles y amortización 3 % | AEAT cuadro-resumen reducciones (sede.agenciatributaria.gob.es, manual IRPF 2024); verificar zonas tensionadas por CCAA como entrada | Medio-alto | dic-ene |
| deduccion-maternidad-familia-numerosa | deducción por maternidad / familia numerosa renta | Alto (estimación) | Reúne maternidad (art. 81), familia numerosa y mínimo por descendientes en un solo resultado | LIRPF arts. 58, 81 y 81 bis; **verificar importes 2026 en BOE**; autonómicas fuera | Medio | dic-ene |
| venta-vivienda-plusvalia-irpf-exencion | vender vivienda IRPF plusvalía exención | Alto (estimación) | Ganancia patrimonial neta (gastos, mejoras), exención por reinversión en vivienda habitual y por mayores de 65 (arts. 33, 38 LIRPF); competencia son artículos | LIRPF y reglamento; confirmar tramos del ahorro | Alto | feb-mar |
| autonomo-estimacion-directa-o-modulos | estimación directa o módulos autónomo | Medio-alto (estimación) | Cuota IRPF trimestral por modelo; módulos solo si la Orden de módulos vigente es verificable | Orden anual de módulos (BOE); **no publicar si no se verifica** | Medio-alto | ene (params 2027) |
| deduccion-alquiler-vivienda-habitual-comunidad | deducción alquiler vivienda habitual comunidad | Muy alto en campaña (estimación) | Estatal ya no existe para contratos nuevos (solo régimen transitorio pre-2015); es autonómica. Sin tabla BOE verificada de 15 CCAA: calculadora genérica (% y límite del usuario) | Leyes autonómicas: **sin tabla verificada hoy** | Medio-alto | feb |
Herencia/donación: no se incluye (sin fuente verificable del conjunto de CCAA); queda en reserva.

## Dos guías de apoyo
1. **Renta 2027: cómo ordenar tus papeles** (borrador de datos fiscales, certificados de retenciones, alquileres, hijos, donativos, plan de pensiones; enlaza a obligado-a-declarar, conjunta-o-individual, donativos, deducción de alquiler). Publicar en enero. Aviso: no es asesoramiento fiscal.
2. **Coste real de tener un hijo / mascota / coche** (tres bloques con cifras de las calculadoras guardería, seguro mascota, comprar-coche y coche propio vs carsharing; cada cifra con fecha y entrada del usuario). Publicar en nov.

## Revisión de competencia (c11)
Sin Keyword Planner y con una sola ronda de búsqueda hoy, no se re-consultaron hipotecas, coche, IRPF ni luz: no hay evidencia nueva. Último estado conocido (c10): Calcuribor y Bankinter se acercan al euríbor de equilibrio en fija/variable; en luz nadie con veredicto personalizado sobre histórico real. Pendiente: reconsultar al llamar de nuevo (c16).

## Priorización de los siguientes 8 ciclos (11-18; 2 por ciclo; F = fiscal, máx. 1 por ciclo; F pasa por Constructor + Verificador Opus; si no cierra, se sustituye por una NF)
| Ciclo | Construir | Motivo |
|---|---|---|
| 11 | academia-idiomas-presencial-online-o-intensivo (NF) + seguro-hogar-con-o-sin-franquicia (NF) | En construcción; pico sep y ene |
| 12 | suscripciones-cuanto-gasto-al-ano (NF) + obligado-a-declarar-renta-dos-pagadores (F, límites ya verificados) | Dic-ene; indexar para Renta 2027 |
| 13 | gimnasio-o-entrenar-en-casa (NF) + deduccion-maternidad-familia-numerosa (F) | Antes del 15-dic; verificar importes 2026 |
| 14 | cocinar-en-casa-o-comer-fuera (NF) + irpf-alquilar-vivienda-rendimiento-neto (F) | Enero; reducciones ya localizadas en AEAT |
| 15 | movil-reacondicionado-o-nuevo (NF) + venta-vivienda-plusvalia-irpf-exencion (F, doble verificación) | Black Friday si el calendario lo permite; si no, ene |
| 16 | equipaje-y-asiento-avion-coste-real (NF) + autonomo-estimacion-directa-o-modulos (F) + params 2027; llamar al Investigador | Parámetros 2027 |
| 17 | residencia-o-cuidador-a-domicilio (NF) + deduccion-alquiler-vivienda-habitual-comunidad (F; si no hay tabla, versión genérica) | Pico abr-jun |
| 18 | marca-blanca-o-marca-ahorro-anual (NF) + mudanza-empresa-o-furgoneta (NF) + refuerzo con datos de Search Console | Reponer con impresiones |

## Ciclo 17 (Investigador, 2026-10-02)
12 propuestas no fiscales añadidas al final de backlog.md (sin búsqueda web; criterio: demanda evergreen en ES y ausencia en las 59 calcs). Prioridad SEO/GEO: aire acondicionado, fondo de emergencia, coche segunda mano, gasolinera low cost, impresora, cambio de operadora. Reparto hubs: energía 2, coche 3, ahorro 7, hipoteca 1 (garaje). Ventaja común: cálculo con los números del usuario (competidores solo dan medias).
