# Verificación R58.3 · porcentaje del paro desde el día 181 · 2026-10-02 (Verificador fiscal, Opus)
VEREDICTO: FALSA ALARMA · el 60 % es el vigente; NO hay que corregir ninguna calculadora, página, test ni guía. Cerrar R58.3 como «no procede».

## Qué dice la norma hoy
- LGSS art. 270.2, texto consolidado del BOE (https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a270), leído el 2/10/2026: «el 70 por ciento durante los ciento ochenta primeros días y el 60 por ciento a partir del día ciento ochenta y uno».
- Nota del BOE en el artículo: «Se modifica el apartado 2 por la disposición final 25.8 de la Ley 31/2022, de 23 de diciembre» (BOE-A-2022-22128). Redacción vigente: publicada el 24/12/2022, en vigor desde el 01/01/2023. Es la última actualización del artículo: ninguna norma posterior lo ha tocado.
- El «50 por ciento» es el **texto original** (publicado el 31/10/2015, en vigor el 02/01/2016), derogado desde el 1/1/2023.
- RDL 26/2026 (BOE-A-2026-20266, derogado el 2/10/2026 por BOE-A-2026-20526): según params.cuanto_cobro_paro_2026.rdl_26_2026 no toca los arts. 147, 269 ni 270, y la ficha del a270 no lo menciona. En el BOE no hay ninguna reforma del 270.2 publicada después de la Ley 31/2022. Un proyecto no publicado no es norma, así que no se modela.

## Por qué salió el error (lección para el Constructor y el Lector de norma)
La API de legislación consolidada (…/texto/bloque/a270) devuelve **todas las versiones** del bloque, de la más antigua a la más reciente:
`<version id_norma="BOE-A-2015-11724" fecha_vigencia="20160102">` (50 %) y luego `<version id_norma="BOE-A-2022-22128" fecha_vigencia="20230101">` (60 %).
El Constructor de pagas se quedó con la primera. Regla: tomar siempre la `<version>` con la `fecha_vigencia` más alta que no pase de hoy, o leer la página act.php («Última actualización … en vigor a partir de …»). Propuesta al Mejorador: añadir esta regla a constructor.md y a lector-norma.md.

## Archivos que usan 70/60: correctos, NO tocar (lista para que nadie los «corrija»)
| Archivo | Líneas | Valor |
|---|---|---|
| projects/decidir/data/params.json | 3554-3555 y 4163-4164 (cuanto_cobro_paro_2026 y capitalizar_paro_2026: pct_primeros_180_dias 70, pct_despues 60) | correcto |
| calcs/cuanto-cobro-de-paro-prestacion-desempleo.js | 3 (pctAlto 70, pctBajo 60), 16, 59 | correcto |
| calcs/cuanto-cobro-de-paro-prestacion-desempleo.json | 7, 64, 76 (cita art. 270.2), 80 | correcto |
| content/cuanto-cobro-de-paro-prestacion-desempleo.html | 5 (cita art. 270.2), 14, 16, 17, 22 | correcto |
| calcs/capitalizar-paro-o-cobrarlo.js | 3 (pctBajo 60), 12 | correcto |
| calcs/capitalizar-paro-o-cobrarlo.json | 25, 37, 106 | correcto |
| content/capitalizar-paro-o-cobrarlo.html | 4, 30 | correcto |
| content/guias/me-han-despedido-indemnizacion-paro-plazos.html | 11 | correcto |
| ops/verif/cuanto-cobro-de-paro-prestacion-desempleo.py | 7 · capitalizar-paro-o-cobrarlo.py 4, 87 · capitalizar-paro-o-cobrarlo-verificador.py 7 | correcto |
Los demás «50 %» / «60 %» del grep (cese parcial de autónomos, tabla del CAE en aceptar-trabajo, jornada parcial del 50 %, IT del 60 % del día 4 al 20) son otras normas: no tienen que ver con el 270.2.
Grep «50 por ciento a partir | 70/50 | 50 % desde/después» en todo autolab (sin dist/): solo salen journal/preverif-pagas-extra-prorrateadas-o-14-pagas.md (líneas 16 «prestación (70 %/50 %…)» y 31) y ops/requests.md:164. Ninguna página publicada usa el 50 %.

## Qué sí hay que cambiar (solo texto interno, no público)
1. ops/requests.md:164 R58.3 → marcar [x] con «no procede: 270.2 vigente = 60 % desde 1/1/2023 (Ley 31/2022 DF 25.8); el 50 % era el texto original; ver journal/verificacion-paro-pct-r58-3.md».
2. journal/preverif-pagas-extra-prorrateadas-o-14-pagas.md:16 «(70 %/50 %, …)» → «(70 %/60 %, …)», y la línea 31 tacharla con referencia a este informe (lo hace el Constructor o el Orquestador; yo no edito journals ajenos).
