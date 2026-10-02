# Reverificación · irpf-alquilar-vivienda-rendimiento-neto · 2026-10-02 (solo lectura)
Resultado: 7/8 aplicados plenamente, 1 parcial (cambio 5).

| # | Estado | Evidencia |
|---|---|---|
| 1 | OK | Aviso del 90 % solo hasta 1/12/2026 en note del JS y en "Cómo usar" del HTML. |
| 2 | OK | Ayuda de `adq` con prorrateo por IBI (RIRPF 14.2.a); muebles (14.2.b) en límites del JS, HTML y FAQ. |
| 3 | OK | `sources` y params.fuente citan RDL 26/2026 art. 6.Segundo.Dos y .Catorce con url BOE-A-2026-20266; confianza B; frase de no convalidación en HTML, FAQ y sources. Sin "consolidado con el RDL". |
| 4 | OK | Prórroga tácita 80 % en límites (JS, HTML, FAQ); ya no dice "no aplica a 2026"; preverif fila 7 actualizada. |
| 5 | PARCIAL | HTML corregido ("criterio de la Agencia Tributaria"). Pero la FAQ 2 del .json aún dice "un criterio prudente porque el reglamento habla de «cada año»". Falta cambiarla. |
| 6 | OK | JS `tipo > 54`; ayuda "unos 54 %"; test.json con caso tipo 54. |
| 7 | OK | Ayuda de `contrato` (70 % joven solo a la parte de quienes cumplen la edad). |
| 8 | OK | Límites con 6.500 € (art. 20 y DA 61.ª) y recargo art. 27 LGT en JS y HTML. |

## Absolutos / cifras nuevas
- Sin absolutos nuevos. 54 % respaldado por escalas de params.json (24,5 + 29,35 = 53,85); 6.500 € está en params (otras_rentas_max).
- Cifras legales sin fuente en `sources` ni params: art. 27 LGT (recargo), art. 10.1 LAU (prórroga tácita, solo en texto; params cita url_lau pero para art. 17.6) y RIRPF 14.2.b. Menor: añadir a `sources`/params.fuente (LGT art. 27) o aceptar que están cubiertas por el informe Opus.

## Pendiente
1. FAQ 2 del .json: sustituir "criterio prudente" por criterio AEAT (cambio 5).
2. Opcional: citar LGT art. 27 en sources.
