# Verificación · actualizacion-renta-alquiler-irav-ipc · 2026-10-02 (Verificador fiscal/legal, Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 1 · R 0 · S 1 (crítico) · otros 1 (absoluto)

## Paso 0: interpretación propia (norma leída hoy) vs bloque INTERPRETACION del oráculo: coincide
- LAU art. 18.1 (consolidado BOE-A-1994-26003, «Se deja sin efecto la modificación del apartado 1» del RDL 26/2026 por BOE-A-2026-20526): actualización solo en el aniversario «en los términos pactados»; «En defecto de pacto expreso, no se aplicará actualización»; pacto sin índice → variación anual del IGC; «En todo caso» el incremento no puede exceder la variación del IPC del último índice publicado. OK.
- Art. 18.2: exigible «a partir del mes siguiente» a la notificación escrita con el porcentaje (vale nota en el recibo precedente; certificado INE si lo pide el inquilino). No hay preaviso de un mes. OK.
- DA 11.ª (literal): el índice del INE «se fijará como límite de referencia a los efectos del artículo 18»; añadida por DF 1.5 Ley 12/2023, en vigor 26/05/2023, con remisión a la DT 4.ª para contratos anteriores. DT 4.ª original (diario BOE-A-2023-12203, leída): los anteriores «continuarán rigiéndose por lo establecido en el régimen jurídico que les era de aplicación». INEbase: contratos posteriores al 26/5/2023 «se revisarán en base al IRAV». La formulación de confianza B («límite según la DA 11.ª y el INE») es correcta; «desde el 26/5/2023» es correcto (entrada en vigor). Efectos IRAV 1/1/2025 (Res. INE BOE-A-2024-26685).
- Negativos: el art. 18 solo limita el incremento; la actualización la puede hacer «el arrendador o el arrendatario» en los términos pactados → con IPC pactado negativo la renta puede bajar a instancia del inquilino (no modelado; ver N).

## Datos con fuente
- IRAV agosto 2026 = 2,47 %, «Publicado: 15/09/2026»: CONFIRMADO en INEbase IRAV (https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177110&idp=1254735976607&menu=ultiDatos).
- IPC 4,9 %: existe, pero es el AVANCE (indicador adelantado) de septiembre 2026, publicado 29/09/2026 (INEbase IPC, «Base 2025 - Avance. Septiembre 2026»). El último IPC DEFINITIVO publicado es AGOSTO 2026 = 4,3 % (API INE tabla 76134, serie «Nacional. Índice general. Variación anual», dato tipo definitivo; julio 3,6 %). Es falso lo de preverif «el definitivo de agosto no figuraba».

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | S crítico | data/params.json renta_alquiler_2026 (ipc_pct, ipc_periodo, fuente, nota); calcs/…json (label/ayuda del input ipc, lead, veredicto, sources); content/…html; test.json (caso pre ipc) | Default IPC = 4,3 % (agosto 2026, definitivo, INE) en vez de 4,9 % (avance de septiembre). Si se quiere mencionar el avance, solo como aviso: «el avance de septiembre (4,9 %) no es el índice definitivo; el de septiembre sale a mediados de octubre». | Art. 18.1: «último índice que estuviera publicado»; el avance es una estimación sin índice definitivo (el INE certifica con índices definitivos). Cambia cifra en contratos 6/3/2019-25/5/2023: 800 € → máx. 834,40 € (no 839,20 €). Ejemplo «post» no cambia (min = IRAV 2,47 %). |
| 2 | otros (absoluto) | calcs/…json veredicto | «Si el IPC o el IRAV no son positivos, no hay subida» → «Si el índice que limita tu subida (IPC; desde el 26/5/2023, el menor entre IPC e IRAV) no es positivo, no hay subida». | En contratos «pre» el IRAV no cuenta: con IRAV ≤ 0 e IPC > 0 sí hay subida. |
| 3 | N | content (Qué no incluye) y escenario 5 del JS (texto, cuando se corrija) | Añadir: «Si tu cláusula es el IPC y es negativo, la actualización pactada puede bajar la renta: también puedes aplicarla tú (art. 18.1)». | Art. 18.1 «por el arrendador o el arrendatario … en los términos pactados». |
| 4 | T | content (Vigencia) y nota del JS | Añadir: «Si la subida se notificó el 1 o 2 de octubre de 2026, con el RDL 26/2026 en vigor, consulta a un profesional». | Derogación no retroactiva (fiscal-fuentes regla 6); el default es mes = octubre. |

## Comprobado sin cambios
- 8: firma «ant» bloquea; «none» ignora índices; mes fuera de 1-12 no calcula. Zona tensionada/gran tenedor solo informan: correcto (17.6-7 y 10.2-3 afectan a renta inicial y prórroga, no al art. 18). VPO, uso distinto de vivienda, forales/autonómicas: declarados fuera.
- R: RDL 26/2026 y 27/2026 derogados (BOE-A-2026-20526/20527); art. 18 vuelve a la redacción RDL 7/2019. Topes art. 46 RDL 6/2022 agotados 31/12/2024: correcto.
- Citas por muestreo (3): art. 18.1, 18.2, DA 11.ª: literales correctos.
- Opcional (no obligatorio): DT 4.ª.2 Ley 12/2023: un contrato anterior adaptado por acuerdo al nuevo régimen se trataría como «post»; una línea en la ayuda del selector.
