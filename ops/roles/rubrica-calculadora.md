# Rúbrica de calidad de calculadora (v2, 2026-10-01T23:03Z c8; v1 2026-10-01; mantiene el Mejorador del equipo)
La usan el Constructor (autoevaluación, pegada en su informe final) y el QA (verificación). Cada punto 0/1/2.
**Se publica con ≥ 16/20 y ningún 0 en los puntos marcados con \*.** Métricas: retrabajo por calculadora (reintentos de QA) → 0; errores de texto hallados después del Constructor (c7: 2 en IRPF; día 1: Euríbor inventado en params) → 0.

| # | Criterio | 2 = cumple | 0 = bloquea |
|---|---|---|---|
| 1\* | Corrección | ≥ 3 casos en `calcs/<slug>.test.json` recalculados con Python independiente (no copiando la salida del JS); `ops/check.py` OK; un caso borde (0, máximo, empate) sin NaN/Infinity | algún test falla o los esperados salen del propio JS |
| 2\* | Cifras con origen | todo número del texto, FAQ y `veredicto` sale de `data/params.json`, de `data/live.json` o del cálculo; cada parámetro con fuente enlazada y fecha de consulta; **todo dato de mercado (Euríbor, carburantes, luz, IPC, tipos) sale de `live.json` vía `default_from: "live.…"` o, si no hay dato vivo, de una fuente oficial con fecha < 31 días anotada en params** | una cifra sin origen, o un dato de mercado escrito de memoria |
| 3\* | Fiscal/legal | si aplica: fuente oficial (BOE/AEAT/BdE/CNMC) + oráculo Python con barrido aleatorio + verificación de ops/roles/verificador-fiscal.md hecha | aplica y no está |
| 4 | Respuesta primero | la primera frase del `lead` es un veredicto condicionado («Conviene X si…»); `veredicto` relleno | describe en vez de decidir |
| 5 | Decisión, no dato | el resultado dice qué hacer y da el umbral/punto de equilibrio («a partir de N km/año…») | solo muestra importes |
| 6 | Entradas | ≤ 8 inputs, unidades en el label, `min`/`step`, defaults realistas tomados de params/live (no duplicados a mano); combinaciones que la ley no permite, bloqueadas o avisadas | defaults absurdos o duplicados sin anotar en requests |
| 7 | Componente | `EM.renderResult` + `EM.live`, `winner` pasado, formato `EM.eur`/`EM.num`, nada de HTML a mano | pinta HTML propio |
| 8 | SEO en página | title ≤ 60, description ≤ 155, `tema` en el JSON, 3–5 FAQ reales, keyword principal que no canibaliza otra página | falta title/description/tema |
| 9 | Enlazado y peso | 2–3 relacionadas en `data/clusters.json` (petición al Estratega si no puedes); página < 60 KB en dist | huérfana o > 80 KB |
| 10\* | Texto ≤ cálculo (nuevo v2) | cada afirmación general del lead, veredicto y FAQ («conviene cuando…», «siempre», «ahorras») está demostrada por el cálculo en los casos de test o por la norma citada; las condiciones van con su umbral calculado; los límites del modelo se dicen | una regla general que el cálculo no demuestra (c7: «conviene con sueldos desiguales») |

Formato del informe del Constructor: `Rúbrica <slug>: 1=2 2=2 3=n/a 4=2 5=1 6=2 7=2 8=2 9=1 10=2 → 18/20 (n/a cuenta como 2)`.
Prueba rápida del punto 10: para cada frase con «conviene/sale mejor/ahorras», señala el caso del test.json que la demuestra y otro que muestre su límite. Si no lo hay, reescribe la frase como condición con umbral o bórrala.

## Estilo (c32; lo aplica el Editor de calidad y el Constructor en calculadoras nuevas)
1. Tuteo siempre. 2. Lead: respuesta + condición + cifra del ejemplo en la 1.ª frase. 3. Veredicto: «Con tus datos, gana X por N € (al año / en N años)»; si la diferencia < 5 %, «empate práctico». 4. Impuestos con su nombre completo la primera vez (IRPF, IBI, ITP) y el artículo solo en «Supuestos y fuentes». 5. Sin absolutos sin condición. 6. «Supuestos y fuentes» con lo no modelado y su efecto. 7. Disclaimer estándar de build (no uno propio). 8. FAQ: 3-5, como consultas reales. 9. Cifras con coma decimal y punto de miles. 10. Title ≤ 60 caracteres, sin año salvo que la cifra sea anual.
