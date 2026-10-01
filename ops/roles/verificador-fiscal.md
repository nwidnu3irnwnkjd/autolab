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
