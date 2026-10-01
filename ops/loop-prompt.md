Trabaja en el laboratorio `autolab` (lee CLAUDE.md, REGISTRY.md y el último journal). En este ciclo:
1. Elige la acción con mayor impacto esperado en tráfico orgánico entre: (a) añadir una calculadora nueva del backlog
   en `projects/decidir/data/backlog.md` con sus 3 casos de prueba; (b) mejorar una página existente (claridad, FAQs,
   enlaces internos, schema); (c) revisar métricas si hay analítica conectada y ajustar el backlog; (d) arrancar el
   siguiente proyecto del REGISTRY si decidir ya tiene ≥10 calculadoras.
2. Usa subagentes con modelo eficiente (haiku) para redactar y verificar; tú revisas y decides.
3. Verifica: `python3 build.py` y `python3 ops/check.py`. Si falla, arréglalo antes de seguir.
4. Haz commit y, si hay remoto configurado, push. Escribe la entrada del journal con: qué hiciste, por qué, qué medir.
5. Si necesitas algo que solo Andoni puede hacer (dominio, cuenta, dinero), anótalo en `journal/PENDIENTE-ANDONI.md` y sigue con otra cosa.
No preguntes; decide. Un ciclo = un cambio pequeño y verificado. Espacia los ciclos ~45–60 min.
