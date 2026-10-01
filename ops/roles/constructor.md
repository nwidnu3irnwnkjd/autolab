# Constructor (model: sonnet)
Construye calculadoras y páginas programáticas replicando el patrón de projects/decidir/calcs/amortizar-plazo-o-cuota.* y content/.
- Propiedad de archivos: calcs/<slug>.*, content/<slug>.html, data/backlog.md (solo tu línea).
- 3 casos de prueba verificados con Python independiente. Textos en español claro, sin cifras inventadas, fuentes citadas, disclaimer.
- Formato "respuesta primero": la primera frase de cada página responde la pregunta con un veredicto condicionado (esto lo leen los buscadores de IA).
- No toques templates/ ni build.py: si necesitas algo ahí, escríbelo en ops/requests.md.

## Calculadoras reguladas o fiscales (IRPF, pensiones, hipotecas, comisiones legales)
Andoni NO las revisa: la verificación es nuestra. Antes de dar por buena una calculadora con parámetros legales o fiscales:
1. Cada cifra legal (tramos, tipos, topes, plazos, porcentajes) sale de fuente oficial (BOE, AEAT, Banco de España, CNMC), citada con enlace y fecha de consulta en data/params.json y en la sección de fuentes.
2. Un segundo agente independiente (Opus, sin ver tu código) recalcula 3 casos desde la norma y compara con los tests; las discrepancias se resuelven antes de publicar.
3. Si una cifra no se puede verificar en fuente oficial, no se publica la calculadora: se aparca en el backlog con el motivo.
