# Reverificación deduccion-maternidad-familia-numerosa (Sonnet, 2026-10-02)
Cambios obligatorios aplicados: 5/5 (con 1 resto menor en el cambio 2). check.py decidir: OK 4578/4578.

| # | Estado | Evidencia |
|---|---|---|
| 1 | OK | mesesMat y mesesFam separados en .json/.js; mat, guardería (min(gm, mm)) y anticipoAnual de hijos usan mesesMat; fam, especial, exceso y anticipo 143 usan mesesFam. |
| 2 | OK con resto | lead, veredicto, ayuda de n3 y .html reformulados («no hace falta seguir de alta»). RESTO: en el .js, veredicto del caso 0 € con n3=0 y fam=no dice «en ambos casos estar de alta en la Seguridad Social» sin matizar (maternidad: paro o alta al nacer o después; familia: alta, paro o pensión). |
| 3 | OK (vía ayuda) | ayuda de cotiz: «si cobras paro o pensión no hay tope: escribe 1.200 € o más»; el veredicto del 0 € lo repite. No hay opción propia (el informe permitía el mínimo). |
| 4 | OK por construcción | No existe opción mono2 con dos titulares (el sufijo x2 solo está en general/especial), así que no es alcanzable. No hay bloqueo explícito en calcular(). |
| 5 | OK | mensaje de inválido y bloque «fuera del cálculo» del .html y ayuda de fam citan los casos equiparados (discapacidad, ascendientes, viudo/a, huérfanos; art. 2.2 Ley 40/2003). |

## Casos de prueba en test.json
- A (mesesMat 12, mesesFam 6, cotiz 2000): presente, 2.633,33 correcto.
- B: presente pero con cotiz 1200 en vez de cotiz 0 (el informe pedía 0 con sin recorte; la calculadora con 0 recorta, por eso se adaptó a la ayuda). Valor 1.200 coincide. Desviación aceptable, no equivalente.
- C (mesesFam 0, guardería 12 m 5.000 €): presente, 2.200 correcto.
- D (mono2, titulares 2): AUSENTE. Existe «mono2 un solo titular» (1.200), que es la alternativa del informe, pero no el caso inválido; innecesario si no hay opción de dos titulares.

## Absolutos y cifras nuevas
Sin cifras legales nuevas sin fuente (1.200, 1.000, 600, 100/50 € ya en params.json con fuente BOE y RDL 26/2026 comprobado). Sin absolutos del tipo «siempre/nunca» detectados.

## Pendientes
1. Matizar la frase de alta en el veredicto 0 € del .js (cambio 2).
2. Opcional: caso B con cotiz 0 solo si se añade opción paro/pensión; caso D irrelevante hoy.
