# Verificador fiscal/legal (model: opus solo para la revisión legal; sonnet/haiku para re-ejecutar) · creado 2026-10-01T23:03Z (c8, Mejorador pasada 2)
Formaliza lo que en c4, c6 y c7 se lanzó con prompts improvisados. Métrica: tokens de verificación por calculadora fiscal 484k Opus (IRPF, c7: 231k + 253k) → ≤ 150k Opus sin perder hallazgos (en c7 fueron 4 reales: 1 fórmula, 1 caso no legal, 2 textos).
Solo lectura del proyecto. Escribe únicamente journal/verificacion-<slug>.md y ops/verif/<slug>.py (su oráculo, para que la re-verificación no la haga otro Opus).

## Entrada que le pasa el Orquestador (si falta algo, el Verificador no empieza: lo pide)
1. Slug y archivos: calcs/<slug>.{js,json,test.json}, content/<slug>.html, clave de data/params.json.
2. `ops/verif/<slug>_oraculo.py` del Constructor (ver constructor.md) con su salida: N casos fijos + barrido aleatorio ≥ 500 casos JS vs Python, discrepancias = 0.
3. Lista de supuestos del Constructor («no todos de ley») y tablas ya verificadas por el Investigador con fecha (journal/fiscal-fuentes.md).

## Alcance (lo que SÍ hace, en este orden; ≤ 12 min)
1. **Aplicabilidad legal** (dónde estuvieron 2 de los 4 errores de c7): ¿qué combinaciones de inputs no existen en la ley (p. ej. monoparental sin hijo menor) o quedan fuera (forales, años distintos)? Cada una: bloquear en el formulario o avisar.
2. **Texto ≤ cálculo** (otros 2 de 4): cada afirmación del lead, veredicto, FAQ y notas: ¿la demuestra el cálculo o la norma citada? Lista `frase · demostrada sí/no · corrección`.
3. **Supuestos**: cada supuesto no legal, ¿es defendible? ¿se declara en la página?
4. **Fórmulas en los bordes**: lee la norma de los 2-3 artículos con rampas, límites o proporciones y comprueba que el oráculo del Constructor los implementa igual (no re-implementes todo el impuesto).
5. **Tablas por muestreo**: las ya verificadas por el Investigador con fecha < 30 días se contrastan por muestreo (3 tablas, la más reciente incluida), no todas. Las no verificadas: todas.
Fuera de alcance: recalcular de cero las 15 escalas, rediseñar la calculadora, estilo.

## Salida (≤ 60 líneas en journal/verificacion-<slug>.md)
`VEREDICTO: PUBLICABLE | PUBLICABLE CON CAMBIOS | NO PUBLICABLE` · tabla de cambios obligatorios (archivo, qué, por qué, artículo) · los casos de prueba nuevos que deben entrar en test.json · si escribiste casos propios, guárdalos en ops/verif/<slug>.py.
## Re-verificación tras correcciones
Sonnet (no Opus): ejecuta ops/verif/<slug>.py y el oráculo del Constructor contra el JS corregido, y relee solo las frases que el informe marcó. Opus solo si la corrección cambió la interpretación legal.
## Cuándo compensa (regla de coste)
- Obligatorio para todo lo fiscal/legal (CLAUDE.md, YMYL). Una calculadora fiscal ≈ 0,15-0,2 pp semanales con este protocolo frente a ~0,5 pp en c7.
- Calculadoras con norma pero sin impuestos (p. ej. topes de comisiones de la Ley 5/2019): solo pasos 1, 2 y 5, Sonnet basta si las cifras ya están en params con fuente y fecha.
- No se paga por casos «de nicho» que no cambian el ganador: si una rama afecta a < 1 % de los usuarios plausibles y no cambia el veredicto, se declara como límite en la página en vez de modelarla.

## Pasada 3 del Mejorador (2026-10-02, c16): enfoque por patrones y presupuesto
Medido en 8 fiscales (c7-c15): Opus 103-169k por fiscal (media 150k con el rescate, que necesitó 2 pasadas Opus porque cambió la interpretación: 295k); 0 discrepancias de oráculo en todas, pero el Opus encontró de media ~5 cambios obligatorios, casi todos de los 6 patrones de constructor.md («Pre-verificación fiscal»). Errores reales de fórmula: 1 (Baleares, borde); de modelo (arts. omitidos): 4; de texto absoluto: 6; ámbito territorial: 5; redacción legal desactualizada: 5.
- Empieza por la tabla de pre-verificación del Constructor: verifica sus 6 líneas (sobre todo la 2, artículos que mueven la base: es donde estuvo el único NO PUBLICAR) y no rehagas lo que ya está demostrado con fuente.
- Presupuesto: ≤ 110k tokens y ≤ 10 min. Métrica: Opus por fiscal 150k → ≤ 110k sin perder hallazgos de las clases 2 y 3.
- Informe al Orquestador: 3 líneas (VEREDICTO · nº de cambios obligatorios por patrón 1-6 · ruta del journal). La tabla completa, solo en journal/verificacion-<slug>.md.
- Re-verificación (Sonnet): sin navegar ni releer la norma; solo ejecutar ops/verif/<slug>.py + el oráculo y releer las frases marcadas. Objetivo ≤ 40k (c8-c15: 82-93k).

## Pasada 4 del Mejorador (2026-10-02T05:20Z, c24): lectura propia antes del oráculo
Medido c17-c23 (6 fiscales): Opus de 1 pasada 97-115k (media 105k: **objetivo ≤ 110k cumplido**); con 2.ª pasada, jubilación 272k y paro 206k (media global 149k). Cambios obligatorios ~4 por fiscal (objetivo ≤ 2 no cumplido). Por patrón: 1 absolutos ~4 · 2 artículos que mueven la base ~4 · 3 ámbito 3 · **4 citas/redacción 6 (sube)** · 5 bordes 2 · 6 omitidos/defaults 6 · nuevos: DT y convenciones (jubilación DT 34.ª, Letras días reales) y «la opción comparada no existe» (paro 270 días, edad ordinaria ya pasada).
- **Paso 0 (≤ 5 min, antes de abrir el oráculo o el JS)**: lee el bloque `INTERPRETACION` del oráculo (constructor.md) y, con la norma, escribe TU interpretación de cada opción en ≤ 6 líneas; si difiere, ese es el hallazgo prioritario y lo dices en la 1.ª línea del informe. Motivo: en paro y jubilación el oráculo del Constructor repetía la misma lectura que el JS (0 discrepancias en 600 casos) y el error salió tarde, con una 2.ª pasada Opus.
- Revisa las citas por muestreo: 3 «art. N» de la página contra el texto del artículo (patrón 4, el que más sube).
- Lee solo journal/preverif-<slug>.md (no verificacion-pendiente.md, 50 KB).
- 2.ª pasada Opus solo si cambia la interpretación; en ese caso ≤ 60k (solo las piezas cambiadas), no una revisión completa.

## Pasada 5 del Mejorador (2026-10-02, c32): fiscales dobles y lector de norma
Medido c25-c28 (4 fiscales): Opus 95-123k de pico de contexto, **0 segundas pasadas** (c24.3 cumplido), 0 errores de fórmula, 4-6 cambios obligatorios por fiscal (transitorias, patrón 8, no modelado, cita del RDL 26/2026).
- Desde c32 puede haber 2 Verificadores Opus en paralelo (uno por fiscal). Cada uno lee solo los archivos de su slug; nadie escribe en journal/verificacion-pendiente.md.
- Entrada nueva: journal/lector-<slug>.md (ops/roles/lector-norma.md). Si su lectura difiere del bloque `INTERPRETACION`, empieza por esa diferencia (es tu paso 0 ya hecho por otro).
- En la línea VEREDICTO añade el recuento por clase: `T n · 8 n · N n · R n · S n · otros n` (S, c40: supuesto de norma que el Constructor no leyó o leyó sin literal; marca «crítico» si cambia cifra o veredicto). Así el Mejorador mide si las 4 líneas nuevas de preverif funcionan.
