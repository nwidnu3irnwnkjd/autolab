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
- [x] D1 (opus): rediseñar templates/base.html y el CSS global según estos principios: header con logo, hero de home con una frase y las calculadoras como tarjetas con icono SVG y micro-descripción; footer limpio.
- [x] D2 (sonnet): componente de resultado reutilizable (veredicto + cifra grande + gráfico de barras SVG + tabla) y actualizar las 3 calculadoras existentes para usarlo con cálculo en vivo.
- [x] D3 (sonnet): página /decidir/ como catálogo filtrable por tema (hipoteca, coche, impuestos, energía, ahorro) y buscador instantáneo en cliente.
- [x] D4 (haiku): favicon SVG, og:image estática por defecto, meta theme-color, 404 bonita.
- [x] D5 (sonnet): revisión de accesibilidad y de la vista a 375 px en todas las páginas; corregir.

## Fase 2: ilustración y movimiento
Sistema propio de ilustración en SVG (sin librerías ni fotos). Tokens de color `--i1` (acento), `--i2` (cálido), `--i3` (verde azulado), `--i1s` (acento suave), `--ib` (fondo), `--is` (superficie), `--il` (trazo) en `:root`, redefinidos en oscuro. Sprite en `assets/illustrations.svg` (`<symbol>` con viewBox 0 0 160 120: hipoteca, coche, impuestos, energia, ahorro, perdido, vacio), usado con `<use>` mediante `ill(sym, cls, w, h)` en build.py (versión `?v=` automática). Todo el movimiento va dentro de `@media (prefers-reduced-motion:no-preference)`; el estado sin animación es el final y completo.
- [x] F1 Hero de la home: ilustración inline «entre muchos caminos, uno te conviene» (bifurcación con 4 rutas punteadas hacia monedas, casa, coche y balanza; la ruta elegida, en acento, se dibuja hasta el check). Entrada escalonada (dibujo de trazo + pop con muelle), flotación continua, pulso en inicio y meta, punto que recorre la ruta (SMIL, se pausa fuera de pantalla), parallax leve con el ratón (solo pointer:fine) y malla de degradado animada (transform, 24 s). CSS del hero inline en home.html para no pesar en el resto.
- [x] F2 Ilustración por tema: pequeña (88×66) en tarjetas y grande (220×165; 104×78 en móvil) en la cabecera `.ph` de cada calculadora (kicker con el tema que enlaza a `/decidir/#tema`, h1 y lead; tinte por tema). Tamaños reservados: sin layout shift.
- [x] F3 Microinteracciones: tarjetas con elevación + brillo (barrido) al pasar o enfocar y la ilustración se inclina; revelado al hacer scroll (IntersectionObserver, una vez, solo elementos bajo el pliegue); destello en el veredicto cuando cambia el ganador (`o.winner` o texto del veredicto sin cifras); barras con easing y escalonado; inputs con transición de foco y label en acento; botón con escala al pulsar y onda; nav con `aria-current`.
- [x] F4 404 con ilustración «perdido» (poste con flechas) y estados vacíos (catálogo y home) con «vacio».
- [x] F5 «Guías» en la navegación y en el footer; estilos de `ul.guides`, `article.guide .byline` y tablas de guías; `EM.num(x, d)` y `EM.eur(x, d)` con agrupación siempre («1.143 €»); `EM.renderResult` los usa por defecto.
- [x] F6 og:image nuevo 1200×630 con texto (Inter, rasterizado en canvas del navegador) y la ilustración del hero.
- [x] F7 Verificado en navegador: home, catálogo (+ vacío), 2 calculadoras, guía y 404, a 375 y 1280 px, claro y oscuro, sin animaciones; sin errores de consola ni scroll horizontal.
- [ ] F8 Minificar app.css/app.js en build (dist) o separar CSS de guías: la página más pesada (diésel) está en 63 KB en bruto (18 KB gzip) porque su HTML ocupa 26 KB.
- [ ] F9 Ilustraciones propias para impuestos/energía/ahorro en uso real cuando existan calculadoras de esos temas (ya están en el sprite; revisar a 375 px).
- [ ] F10 Variante del hero para móvil más compacta (horizontal) si el CLS/LCP de campo lo pide; medir con Search Console/CrUX.
- [ ] F11 og:image por calculadora (ilustración del tema + h1) generado igual que el general.
- [ ] F12 Gráfico de evolución en el tiempo (línea SVG animada) para calculadoras con horizonte (alquilar o comprar, amortizar o invertir).
