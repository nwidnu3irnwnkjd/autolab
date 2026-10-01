# Equipo de agentes (mantiene el Mejorador del equipo)

| Rol | Modelo | Frecuencia | Propiedad |
|---|---|---|---|
| Orquestador / Eficiencia | Sonnet 5.5 (sesión) | cada 20 min | ops/loop-prompt.md, costes, integración |
| Constructor | Sonnet | cada ciclo | calcs/, content/<slug> |
| Diseñador UI/UX | Sonnet (Opus en D1) | cada ciclo hasta terminar DESIGN.md | templates/, assets/ |
| Estratega SEO/GEO | Opus estrategia, Sonnet ejecución | ciclos pares | build.py (SEO), content/guias, static/, ops/SEO-GEO.md |
| Investigador | Opus + web | cada 3 ciclos | journal/ideas.md, competencia.md |
| QA | Haiku | cada ciclo | solo lectura |
| Mejorador del equipo | Opus | cada 4 ciclos | ops/roles/*, EQUIPO.md |

## Registro de cambios
- 2026-10-01: equipo v1 creado (6 roles + Estratega SEO/GEO + Mejorador del equipo). Cadencia 20 min, tope 400 EUR extra y 100 EUR/día.
