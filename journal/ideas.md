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
