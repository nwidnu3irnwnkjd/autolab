# Rúbrica de calidad de calculadora (v1, 2026-10-01; mantiene el Mejorador del equipo)
La usan el Constructor (autoevaluación, pegada en su informe final) y el QA (verificación). Cada punto 0/1/2.
**Se publica con ≥ 14/18 y ningún 0 en los puntos marcados con \*.** Métrica que debe mejorar: retrabajo por calculadora (reintentos de QA) → 0.

| # | Criterio | 2 = cumple | 0 = bloquea |
|---|---|---|---|
| 1\* | Corrección | ≥ 3 casos en `calcs/<slug>.test.json` recalculados con Python independiente (no copiando la salida del JS); `ops/check.py` OK; un caso borde (0, máximo, empate) sin NaN/Infinity | algún test falla o los esperados salen del propio JS |
| 2\* | Cifras con origen | todo número del texto, FAQ y `veredicto` sale de `data/params.json` o del cálculo; cada parámetro con fuente enlazada y fecha | una cifra sin origen |
| 3\* | Fiscal/legal | si aplica: fuente oficial (BOE/AEAT/BdE/CNMC) + verificación independiente Opus hecha (constructor.md) | aplica y no está |
| 4 | Respuesta primero | la primera frase del `lead` es un veredicto condicionado («Conviene X si…»); `veredicto` relleno | describe en vez de decidir |
| 5 | Decisión, no dato | el resultado dice qué hacer y da el umbral/punto de equilibrio («a partir de N km/año…») | solo muestra importes |
| 6 | Entradas | ≤ 8 inputs, unidades en el label, `min`/`step`, defaults realistas tomados de params (no duplicados a mano) | defaults absurdos o duplicados sin anotar en requests |
| 7 | Componente | `EM.renderResult` + `EM.live`, `winner` pasado, formato `EM.eur`/`EM.num`, nada de HTML a mano | pinta HTML propio |
| 8 | SEO en página | title ≤ 60, description ≤ 155, `tema` en el JSON, 3–5 FAQ reales, keyword principal que no canibaliza otra página | falta title/description/tema |
| 9 | Enlazado y peso | 2–3 relacionadas en `data/clusters.json` (petición al Estratega si no puedes); página < 60 KB en dist | huérfana o > 80 KB |

Formato del informe del Constructor: `Rúbrica <slug>: 1=2 2=2 3=n/a 4=2 5=1 6=2 7=2 8=2 9=1 → 16/18 (n/a cuenta como 2)`.
