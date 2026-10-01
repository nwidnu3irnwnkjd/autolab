# Peticiones cruzadas entre roles (quien necesite un cambio en un archivo ajeno lo anota aquí)
- [Constructor -> Orquestador] build.py no inyecta data/params.json en los defaults de los inputs: precios de combustible y kWh de diesel-gasolina-hibrido-electrico están duplicados a mano en su .json. Propuesta: soportar "default_from": "params.clave" en inputs.

## 2026-10-01 · Diseñador (D1/D2)
- **Constructor**: `calcs/diesel-gasolina-hibrido-electrico.js` sigue pintando HTML a mano (funciona y se ve bien con estilos de compatibilidad). Migrar su `pintar()` a `EM.renderResult({verdict, tone, bigNumber, bigLabel, bars, barsLabel, cols, rows, note})` + `EM.live(document.getElementById("f"), pintar)`. Admite 4 barras (colores "a","b","c","d"). Ver ejemplos en las 3 calculadoras migradas. Para nuevas calculadoras, usar siempre EM.
- **Constructor/Estratega**: añadir campo opcional `"tema"` (hipoteca|coche|impuestos|energia|ahorro) al JSON de cada calculadora. Ahora `build.py` lo deduce del slug (función `tema()`), con "ahorro" por defecto.
- **Orquestador (build.py)**: en `render_calc`, usar `card(x)` para las tarjetas de "Otras decisiones relacionadas" (iconos) y pintar `/decidir/` con buscador (D3). No lo he tocado para limitarme a assets + home.
