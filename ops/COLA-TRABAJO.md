# COLA DE TRABAJO CONTINUO (7-oct, orden de Andoni: trabajo continuo y periódico, sin esperas por consumo)
El Orquestador toma de aquí en cada ciclo (≥ 2 agentes por ciclo, en paralelo), sin esperar a hechos nuevos. Respeta el congelado del Optimizador: NO páginas nuevas (calculadoras, guías, tablas, planes) hasta ≥ 30 URL rastreadas; sí mejorar páginas existentes y noticias.
1. [Vigilante+Redactor] Noticias del día (BOE de cada mañana ~07:40 local, REE ~20:30Z, jueves Boletín Petrolero, 14-oct IPC/IRAV, 20-oct modelos 3T, 29-oct BCE, 31-oct base autónomos): al menos 2 piezas con valor/día; resumen del día; semana el lunes.
2. [Sonnet barrido] Vigencia de TODAS las calculadoras/guías YMYL frente a la última semana (RDL 25/28/29, consolidados): buscar frases desactualizadas («no rige», «derogado», cifras 2026 caducadas) y listar/corregir texto; si cambia una cifra → Constructor + Opus.
3. [Editor de calidad] Pasada sobre las calculadoras sin Editor 5/5 (journal/editorial.md): titular, lead con respuesta, FAQ, fuentes, tono.
4. [Constructor] «Casos típicos» (3 ejemplos resueltos extra con cifras reales, estáticos como ops/gen_ejemplos.py) en las 20 calculadoras con más potencial de búsqueda; cifras citables para IA.
5. [Diseñador/Constructor] Enlazado interno: páginas con menos inlinks (ops/seo_audit.py) → enlaces contextuales; bloque «Relacionado» en noticias.
6. [Director UX] Pasada 2 (cada 4 ciclos) y experimentos E-UX1/E-UX2; velocidad móvil.
7. [Optimizador Opus] Pasada 3 el 12-oct (o antes si inspect_all llega a 10 rastreadas).
8. [Verificador Opus] Re-verificación periódica (1/día) de la calculadora fiscal más antigua o de mayor tráfico frente a la norma vigente y sus cifras 2026-2027.
9. [Orquestador, 0 tokens] inspect_all + kpis cada ciclo de mañana; refresh de datos; convalidación RDL 25/28/29.
