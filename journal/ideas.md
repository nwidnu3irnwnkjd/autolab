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

## Priorización de los siguientes 10 ciclos de construcción (2 calculadoras por ciclo)
Criterios: estacionalidad (hoy 2-oct), coste/riesgo (no fiscales primero; 1 fiscal en vuelo con pipeline T8), hueco de competencia, clústeres para enlazado interno. Ya hechas: 12 + guardería + seguro = 14.
| Ciclo | Construir | Motivo |
|---|---|---|
| 10 | cambiar-ventanas-aislamiento-merece-la-pena + cambiar-electrodomestico-antiguo-merece-la-pena | Estacional oct-feb; clúster energía con calefacción y luz ya publicadas |
| 11 | tren-avion-o-coche + reparar-o-comprar-electrodomestico | Puentes de diciembre y Black Friday (27-nov); ambas rápidas. Fiscal en paralelo: placas-solares-merece-la-pena (cadena T8, ciclo N) |
| 12 | coche-nuevo-o-seminuevo + cuanto-ahorrar-para-comprar-casa | Cierra clúster coche; hipoteca es el clúster con más citas AIO. Fiscal: verificación de placas |
| 13 | coche-propio-o-carsharing-o-vtc + bici-electrica-o-transporte-publico | Clúster movilidad completo → guía 1 |
| 14 | autonomo-o-asalariado (fiscal LISTA) + universidad-publica-o-privada-o-master | Enero: cuota de autónomos y búsquedas de cambio de empleo |
| 15 | rescate-plan-pensiones-capital-o-renta (fiscal LISTA) + guía «checklist casa» | Pensiones: complementa plan-pensiones-o-fondo-indexado; nov-dic hay búsqueda de rescate/aportación |
| 16 | Revisión de datos: params/live, ahorrar (fiscales) y Barómetro de noviembre; solo huecos y correcciones | Antes de enero se actualizan IRPF, cuotas y peajes |
| 17 | Preparar renta 2026: declaración conjunta ya publicada, actualizar mínimos autonómicos pendientes (7 CCAA) | Pico abril-junio; indexar en enero |
| 18 | Llamar al Investigador (cada 6 ciclos): 8 nuevas con datos de Search Console de los ciclos 1-12 | Reponer con evidencia real de impresiones, no estimaciones |
| 19 | Reforzar las 3 páginas con más impresiones (veredicto, escenarios, FAQ) en vez de nuevas | Con ≥ 20 calculadoras publicadas, mejorar manda sobre ampliar |
Regla: si el Verificador fiscal no cierra una fiscal a tiempo, se sustituye por la siguiente no fiscal de la lista; no se detiene el ciclo.
