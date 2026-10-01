# Verificación independiente pendiente (Opus, sin ver el código del Constructor)

## declaracion-conjunta-o-individual: pendiente de verificación independiente Opus (2026-10-02)
Archivos: projects/decidir/calcs/declaracion-conjunta-o-individual.{js,json,test.json}, projects/decidir/content/declaracion-conjunta-o-individual.html, projects/decidir/data/params.json (clave `irpf_2026`, con fuente BOE/AEAT, enlace y fecha por tabla).
Qué debe recalcular el verificador desde la norma (Ley 35/2006 consolidada, BOE-A-2006-20764) y las leyes autonómicas, y comparar con el test.json (22 casos):
- Escala estatal general (art. 63.1) y escala del ahorro (arts. 66.1/76, mitad estatal + mitad autonómica).
- Escalas autonómicas 2026 de las 15 CCAA de régimen común (params `irpf_2026.ccaa.*.escala_general`; Castilla y León, Murcia y La Rioja = confianza B, aviso «cifras autonómicas orientativas»).
- Mínimos autonómicos propios releídos en el BOE consolidado: Madrid, C. Valenciana, Galicia, Andalucía, Asturias, Canarias, Baleares (+10 % del 2.º al 4.º descendiente). Resto: se aplican los estatales (no hay artículo propio en el consolidado). Comprobar si falta alguna comunidad con mínimos propios.
- Mínimo estatal (arts. 57, 58, 61.1.ª: reparto 50/50 en individual; entero en conjunta; un solo mínimo del contribuyente en conjunta, art. 84.2.2.º).
- Reducción conjunta: 3.400 € (modalidad 1) y 2.150 € (modalidad 2), a la base general y el resto al ahorro (art. 84.2.3.º y 4.º).
- Art. 19.2.f (2.000 €) y art. 20 (reducción 7.302 € y rampas 1,75 / 1,14, tope 19.747,5 €; no aplica si rentas distintas del trabajo > 6.500 €).
- DA 61.ª (590,89 €, rampa 0,2 hasta 20.048,45 €; límite proporcional a la cuota). Simplificación: ratio = rendimiento neto reducido / (base general + ahorro).
Supuestos a validar (no todos de ley): en conjunta los 2.000 € y la reducción del art. 20 se aplican UNA vez sobre la suma (confirmado en Manual de Renta 2025 de la AEAT, enlace en params); cotización a la SS repartida en proporción al sueldo; ahorro a partes iguales; DA 61.ª sobre la suma en conjunta (NO confirmado en AEAT); hijos de 3-24 años ocupan los primeros lugares del orden y los menores de 3 los últimos.
Corrección al Investigador: journal/fiscal-fuentes.md §1.7 dice que los 2.000 € «se aplican a cada perceptor» en conjunta; la AEAT dice que se aplican por unidad familiar (una vez). La calculadora usa lo de la AEAT.
Estado: NO publicable como definitiva hasta que el verificador cierre las discrepancias.

## declaracion-conjunta-o-individual: correcciones aplicadas, pendiente de re-verificación (2026-10-02)
Aplicados los cambios de journal/verificacion-irpf.md §6: límite DA 61.ª en conjunta = ci·big/(big+bia); monoparental sin hijo menor de 18 bloqueada (nuevo input «18 a 24 años», `hijosAdultos`; «3 a 17» = `hijosMayores`); textos (mínimo personal no se recupera, umbral del segundo sueldo 2.300-7.300 €, sin «firman los dos» en monoparental); avisos de supuestos; params CyL/Cataluña/Murcia/La Rioja (A−). Test.json: 26 casos (22 previos sin cambios + 4 nuevos). Pendiente de re-verificación por Opus.
- [x] verificacion-irpf: APTA PARA PUBLICAR tras re-verificación (0/12 y 0/1000 fallos); horquilla del texto corregida a 2.000-10.000 €. 2026-10-02
