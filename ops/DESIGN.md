# Sistema de diseño — Entre Muchos

Objetivo: que la gente diga "qué bien hecho está esto". Claridad primero, belleza después, y ambas sin peso.

## Principios
1. La respuesta se entiende en 2 segundos: veredicto grande, color semántico (verde = conviene, ámbar = depende), cifra clave enorme.
2. Una calculadora es una conversación: inputs con unidades visibles, ayudas cortas, valores por defecto sensatos, resultado en vivo al cambiar (debounce), sin botón obligatorio (el botón queda como refuerzo).
3. Móvil primero: todo usable con el pulgar a 375 px. Inputs grandes (≥ 44 px), teclado numérico.
4. Gráfico siempre: una comparación visual (barras SVG inline, dos colores) de las dos opciones. Sin librerías.
5. Transiciones suaves (150–250 ms) en aparición del resultado y en las barras. Respetar prefers-reduced-motion.
6. Tipografía: Inter (Google Fonts, display=swap, solo pesos 400/600/800) para texto; cifras con font-variant-numeric: tabular-nums. Escala: 15/17/20/26/36/48.
7. Color: tokens en :root; modo oscuro impecable (no gris sucio). Acento azul eléctrico, éxito verde, aviso ámbar; fondos con superficie elevada sutil (sombra suave en claro, borde en oscuro).
8. Accesibilidad: contraste AA, foco visible, labels asociados, aria-live en el resultado, tablas con scope.
9. Rendimiento: < 60 KB HTML+CSS+JS por página, sin fuentes bloqueantes, sin imágenes pesadas. Lighthouse ≥ 95 en móvil.
10. Marca: logotipo tipográfico "entre muchos" con las dos palabras en pesos distintos; favicon SVG inline; tono cercano, sin tecnicismos gratuitos.

## Tareas de diseño
- [ ] D1 (opus): rediseñar templates/base.html y el CSS global según estos principios: header con logo, hero de home con una frase y las calculadoras como tarjetas con icono SVG y micro-descripción; footer limpio.
- [ ] D2 (sonnet): componente de resultado reutilizable (veredicto + cifra grande + gráfico de barras SVG + tabla) y actualizar las 3 calculadoras existentes para usarlo con cálculo en vivo.
- [ ] D3 (sonnet): página /decidir/ como catálogo filtrable por tema (hipoteca, coche, impuestos, energía, ahorro) y buscador instantáneo en cliente.
- [ ] D4 (haiku): favicon SVG, og:image estática por defecto, meta theme-color, 404 bonita.
- [ ] D5 (sonnet): revisión de accesibilidad y de la vista a 375 px en todas las páginas; corregir.
