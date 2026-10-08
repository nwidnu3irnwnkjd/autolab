# Vías adicionales y gratuitas para enlaces/descubrimiento (8-oct-2026)

Investigación con web pública, SIN ejecutar nada. Complementa `PEDIR-A-ANDONI-ENLACES.md`. Orden: retorno/riesgo. «dofollow» = probabilidad de que el enlace sea seguible (no garantiza que Google lo valore). Los datos de requisitos proceden de las páginas citadas; lo marcado (verificar) no lo he podido confirmar.

Contexto ya cubierto (no repetir): IndexNow/Bing Webmaster, dataset CC BY 4.0 + `/inserta/` + README GitHub (E6 de OPTIMIZACION.md), enlaces desde webs de Andoni, 8 directorios.

## 1. Catálogo de Aplicaciones de datos.gob.es
- URL: https://datos.gob.es/es/aplicaciones (formulario «Añadir una nueva aplicación», sección Comunidad/Interactúa).
- Requisito: persona física o jurídica describe la solución; la revisa el equipo; debe ser una solución que reutilice datos públicos y la información debe coincidir con la URL. Encaja: usamos datos oficiales (BOE, INE, BdE, REE, tablas fiscales) con fuente enlazada.
- Esfuerzo: bajo (formulario + 3 capturas/descripción). Riesgo: bajo. Necesita de Andoni: cuenta en datos.gob.es (registro, probablemente con email) y que figure su nombre o el del proyecto como reutilizador. Dofollow: media (ficha de aplicación en dominio .gob.es; sin confirmar el atributo rel) (verificar).
- Cautela: indicar solo los datasets públicos que realmente reutilizamos; no exagerar.

## 2. Finanzas para Todos (CNMV + Banco de España + Ministerio) — sugerencia de recurso
- URL: https://www.finanzasparatodos.es/ (tienen sección propia de herramientas; contacto por el formulario del portal) (verificar existencia de canal de sugerencias).
- Requisito: ninguno formal; escribir un correo breve ofreciendo la calculadora como recurso complementario (hipoteca fija/variable, jubilación) con fuentes oficiales. Probabilidad de respuesta baja, pero el techo de valor es el más alto de la lista.
- Esfuerzo: bajo (1 correo, borrador mío). Riesgo: bajo. Necesita de Andoni: enviarlo desde su correo (yo solo dejo el borrador). Dofollow: baja-media (si lo añaden, sería enlace institucional; probabilidad total de que lo hagan ~5 %).

## 3. Zenodo (CERN/OpenAIRE): depósito de los datasets con DOI
- URL: https://zenodo.org (guía: https://help.zenodo.org/docs/deposit/create-new-upload/).
- Requisito: cuenta gratuita (ORCID o GitHub); subir CSV de Barómetro/Tablas 2026/euríbor con licencia CC BY 4.0 y metadatos; el campo «Related identifiers» admite URLs, así que enlaza a /datos/ y /tablas-2026/. Zenodo indexa en Google Dataset Search y OpenAIRE, buena señal de descubrimiento y de cita (GEO).
- Esfuerzo: medio (script de empaquetado + ficha; versionado nuevo por actualización). Riesgo: bajo (contenido original, no spam). Necesita de Andoni: cuenta (identidad de persona o de proyecto; mejor cuenta «Entre Muchos» vinculada a GitHub del proyecto). Dofollow: media-baja para el enlace; el valor real es el DOI citable y el rastreo frecuente de zenodo.org.

## 4. Catálogo de datasets de datos.gob.es (publicador no oficial)
- URL: https://datos.gob.es/en/conocimiento/how-publish-data-datosgobes-catalogue
- Requisito: la cuenta con rol «organismo» exige aprobación del responsable RISP de una Administración; un particular normalmente NO puede publicar en el catálogo (solo en Aplicaciones, vía 1). Descartado como publicación directa. Variante realista: que los datasets propios se mencionen en la ficha de la aplicación (vía 1).
- Estado: DESCARTADA como vía independiente (no aplica a no-organismos); se resuelve con la vía 1.

## 5. Google Dataset Search + schema Dataset (sin cuenta)
- URL: https://datasetsearch.research.google.com/ (indexa marcado schema.org/Dataset; ya lo tenemos en Barómetro y Tablas).
- Requisito: ya cumplido; falta comprobar que cada /datos/* lleva `Dataset` con `distribution` CSV y `license`, y que está en el sitemap. Es señal de descubrimiento, no enlace.
- Esfuerzo: bajo (auditoría interna del Estratega). Riesgo: nulo. Necesita de Andoni: nada. Dofollow: no aplica.

## 6. Listas «awesome» y repos de recursos en GitHub (España/datos abiertos)
- URLs: https://github.com/GeiserX/awesome-spain (solo software open source) y https://github.com/AlonsoAlviraa/spain-open-data (directorio de recursos de datos abiertos).
- Requisito: pull request con una línea. awesome-spain exige software open source: solo vale si publicamos el código de las calculadoras con licencia libre (decisión de Andoni). spain-open-data: solo si lo aceptan por ser reutilizador de datos (verificar criterios en su README).
- Esfuerzo: bajo (PR). Riesgo: bajo si el encaje es real; medio si se fuerza (cierran el PR, sin penalización). Necesita de Andoni: la cuenta GitHub del proyecto (ya prevista en E6). Dofollow: los enlaces dentro de README en GitHub llevan nofollow; valor = descubrimiento (github.com se rastrea a diario), no autoridad. Probabilidad dofollow: muy baja (~0 %).

## 7. Guías de recursos de bibliotecas universitarias (LibGuides)
- URLs de ejemplo: https://unizar.libguides.com/recursoseconomiaempresafecemBUZ (Economía y Empresa, Universidad de Zaragoza); hay equivalentes en otras universidades.
- Requisito: escribir al bibliotecario responsable de la guía proponiendo un recurso gratuito y sin registro, con fuentes oficiales. Solo aceptan recursos de calidad académica: nuestra baza es /tablas-2026/ y /datos/ (datos fechados con método), no las calculadoras.
- Esfuerzo: medio (localizar 10 guías, correo personalizado a cada una). Riesgo: bajo (petición individual y legítima; no envío masivo). Necesita de Andoni: firma/identidad real y que él envíe los correos (yo dejo borradores). Dofollow: alta si lo incluyen (enlaces .edu/.es de bibliotecas suelen ir sin nofollow); probabilidad de que lo incluyan ~10 %.

## 8. Prensa local y especializada: nota con dato propio (no nota de prensa genérica)
- Vía: enviar a redacciones (economía/consumo de medios regionales, newsletters de finanzas) un dato propio del Barómetro/Tablas con CSV y método. Sin pago.
- Requisito: dato nuevo y verificable; los periodistas citan si pueden copiar la cifra y la fuente. Sin plataformas de pago.
- Esfuerzo: alto (redactar, seleccionar contactos). Riesgo: bajo; el único riesgo es el reputacional si el dato falla (YMYL). Necesita de Andoni: identidad como contacto y envío de los correos. Dofollow: media-alta (la prensa online suele enlazar sin nofollow en artículos editoriales); probabilidad de cobertura ~3-5 % por envío en frío.

## 9. OCU / FACUA / asociaciones de consumidores
- URLs: https://www.ocu.org/ y https://www.facua.org/ (solo su contacto público).
- Requisito: no he encontrado un canal público de «sugerencias de herramientas»; son entidades que venden/compiten con comparadores propios (OCU). Sin canal público documentado = no insistir. Por la regla de la tarea (solo si aceptan sugerencias públicas): DESCARTADAS.

## 10. Show HN (Hacker News) — solo si hay algo notable
- URL: https://news.ycombinator.com/showhn.html
- Requisito: gratis, sin registro de pago; pide un producto que se pueda probar y que no sea marketing. Enlaces nofollow. Audiencia anglófona y técnica; nuestro público es hispano y poco técnico: encaje malo salvo para un ángulo técnico (Python puro sin dependencias, build estático, 88 calculadoras verificadas con tests).
- Esfuerzo: bajo. Riesgo: medio (a HN le molesta la autopromoción; una sola vez). Necesita de Andoni: cuenta HN (identidad suya). Dofollow: no (nofollow). Valor: señal de descubrimiento y copia por scrapers/LLM. Última prioridad; no es una red social convencional pero roza la regla de «sin redes sociales»: decisión de Andoni.

## 11. Directorios de lanzamientos (Product Hunt y alternativas gratuitas)
- URLs: https://www.producthunt.com y listas como https://github.com/DirectorySurf/awesome-producthunt-alternatives.
- Requisito: cuentas, texto en inglés. Muchos dan nofollow en el plan gratuito y dofollow solo de pago (p. ej. Smol Launch). Audiencia fuera de España.
- Riesgo: medio-alto de caer en «directorios de baja calidad» que Google ignora o ve como patrón de enlaces artificial si se envía a 20 a la vez. Probabilidad dofollow gratis: baja. DESCARTADA como vía recomendada.

## Descartadas (resumen)
- Wikidata/OpenStreetMap: excluidas por el encargo. Wikipedia: enlaces externos nofollow y política contra autopromoción.
- Directorios españoles genéricos de calculadoras (calculadoraonline.es, cubotica, etc.): son competidores, no listas que acepten sugerencias; no he visto formulario de alta.
- Intercambio de enlaces, guest posts de pago, comentarios y redes: fuera de política.

## Recomendación de orden de acción (cuando Andoni lo autorice)
1. Vía 1 (datos.gob.es Aplicaciones) y vía 3 (Zenodo): una tarde, riesgo bajo, mejor retorno realista.
2. Vía 5 (auditoría Dataset schema): la puedo hacer yo ahora sin pedir nada.
3. Vía 2 y 7: borradores de correo para que Andoni los envíe (cautela: nunca envío yo).
4. Vía 6 solo si se publica el código con licencia libre; vías 8 y 10 cuando haya un dato propio sólido.

Nota honesta: ninguna de estas vías garantiza dofollow; con 0 enlaces externos y 1 URL indexada, las más probables son Zenodo/datos.gob.es (descubrimiento y señal de entidad) y los enlaces editoriales desde webs propias de Andoni.
