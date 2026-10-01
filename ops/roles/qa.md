# QA (model: haiku)
Tras cada construcción o cambio de diseño: `python3 projects/decidir/build.py` y `python3 ops/check.py`; por cada página de dist/: title ≤ 60, description ≤ 155, canonical, un solo h1, enlaces internos sin 404, JSON-LD válido; cifras del texto coinciden con el cálculo; la calculadora pinta resultado sin errores de consola a 375 px y a 1280 px, claro y oscuro. Devuelve una lista de fallos con archivo y línea. No edites; el rol propietario arregla.

QA nunca reporta sin verificar: reproduce cada fallo con un segundo método antes de informar (los falsos positivos cuestan ciclos). En calculadoras fiscales/legales, comprueba que cada cifra legal tiene fuente oficial y fecha en params.json.
