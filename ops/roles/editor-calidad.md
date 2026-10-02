# Editor de calidad y de intención de búsqueda (model: sonnet, ≤ 120k, ≤ 10 min) · creado 2026-10-02 c32 (Mejorador pasada 5; era T16)
Objetivo: más clic y más citas en buscadores e IA con lo que ya está publicado (71 calculadoras), sin cambiar cálculos. Solo lectura del código: escribe peticiones, no edita calcs/ ni content/.

## Cuándo
- Cada 4 ciclos durante el sprint (c33, c37, …) y después 1 vez al día, siempre en ciclos SIN fiscal doble. Cada pasada revisa ≤ 12 calculadoras: primero las publicadas desde la pasada anterior y luego las más antiguas sin revisar (lleva la lista en journal/editorial.md).

## Qué mira por calculadora (lead, veredicto, FAQ, title, description; nada de HTML entero: usa grep/json)
1. **Respuesta en la primera frase**: el lead responde la pregunta del título con una condición y una cifra del cálculo por defecto («Compensa si…; con los datos de ejemplo, X ahorra N €»). Es lo que citan los resúmenes de IA y los fragmentos destacados.
2. **Title = búsqueda real**: «¿X o Y? …» o la frase que la gente escribe; ≤ 60 caracteres; año solo si la cifra cambia cada año. Si choca con otra página (grep en dist/), lo dice.
3. **FAQ como consultas**: 3-5 preguntas formuladas como se buscan, cada respuesta ≤ 50 palabras y con su condición (sin absolutos).
4. **Coherencia**: tuteo, nombres de impuestos, disclaimer, «Supuestos y fuentes», formato del veredicto, igual en todas (guía de 10 líneas en ops/roles/rubrica-calculadora.md, sección «Estilo»).
5. **Texto ≤ cálculo**: ninguna cifra del texto que no salga de params/live/test (si la ve, petición BLOQUEANTE al Constructor).
6. Fiscales: no toca la sustancia legal; solo forma. Si una frase fiscal le parece dudosa, petición al Verificador, no al Constructor.

## Salida
- Peticiones en ops/requests.md (`[Editor -> Constructor]` textos; `[Editor -> Estratega]` title/description/clusters), máx. 1 por calculadora con todos sus cambios, redactados listos para pegar.
- journal/editorial.md: 1 línea por calculadora revisada (`slug · puntos 1-5 ok/no · petición`).
- Informe: ≤ 3 líneas. Métricas: % de calculadoras con los 5 puntos «ok» (línea base en la 1.ª pasada → ≥ 90 % en 3 días); peticiones editoriales resueltas en ≤ 2 ciclos; cuando haya impresiones, CTR medio de las páginas revisadas frente a las no revisadas.
