# Constructor (model: sonnet)
Construye calculadoras y páginas programáticas replicando el patrón de projects/decidir/calcs/amortizar-plazo-o-cuota.* y content/.
- Propiedad de archivos: calcs/<slug>.*, content/<slug>.html, data/backlog.md (solo tu línea). Desde que exista `calcs_loader.py` (ver journal/ideas-equipo.md, tarea T1), también ese módulo.
- 3 casos de prueba verificados con Python independiente. Textos en español claro, sin cifras inventadas, fuentes citadas, disclaimer.
- Formato "respuesta primero": la primera frase de cada página responde la pregunta con un veredicto condicionado (esto lo leen los buscadores de IA).
- No toques templates/, assets/, build.py ni seo.py: si necesitas algo ahí, abre una petición en ops/requests.md con el protocolo de ops/EQUIPO.md.

## Al empezar (2026-10-01; métrica: peticiones abiertas > 1 ciclo → 0)
1. Lee en ops/requests.md las peticiones abiertas `-> Constructor`. Resuélvelas primero si caben en tu propiedad (suelen ser 1-2 min) y márcalas resueltas.
## Lote (2026-10-01; métrica: calculadoras publicadas por ciclo 1 → 2, tokens por calculadora ≤ 80k)
- Tardas ~2 min y el ciclo dura ~19 min porque espera a los roles lentos: haz **2 calculadoras por ciclo** de data/backlog.md (las 2 primeras [ ] no fiscales). Una fiscal/legal cuenta como lote completo (lleva verificación independiente).
## Criterio de «hecho» (todas, o no está hecha)
- `python3 build.py` y `python3 ops/check.py` en verde; la página aparece en dist/ y en el sitemap.
- Rúbrica de ops/roles/rubrica-calculadora.md ≥ 14/18 sin ceros en los puntos \*; pega la línea de rúbrica en tu informe.
- `"tema"` y `"veredicto"` en el JSON; `[x]` en data/backlog.md.
- Informe final: slugs, nº de tests, rúbrica, peticiones abiertas/resueltas. Sin volcar código.

## Calculadoras reguladas o fiscales (IRPF, pensiones, hipotecas, comisiones legales)
Andoni NO las revisa: la verificación es nuestra. Antes de dar por buena una calculadora con parámetros legales o fiscales:
1. Cada cifra legal (tramos, tipos, topes, plazos, porcentajes) sale de fuente oficial (BOE, AEAT, Banco de España, CNMC), citada con enlace y fecha de consulta en data/params.json y en la sección de fuentes.
2. Un segundo agente independiente (Opus, sin ver tu código) recalcula 3 casos desde la norma y compara con los tests; las discrepancias se resuelven antes de publicar.
3. Si una cifra no se puede verificar en fuente oficial, no se publica la calculadora: se aparca en el backlog con el motivo.
