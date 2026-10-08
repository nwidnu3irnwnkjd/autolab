# Re-verificación fiscal c90 · cuota-autonomos-ingresos-reales-regularizacion (Verificador Opus, 8/10/2026)
Elegida por tráfico potencial: es la única calculadora de cuota RETA 2026 en calcs/ (las otras de autónomos son comparativas: módulos, SL, asalariado, paro).
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 0 · R 0 · S 1 (no crítico: no cambia ningún ejemplo publicado) · otros 1 (texto no demostrado) · fórmula 0
Pruebas: oráculo del Constructor 1.500 casos, 0 discrepancias; test.json 46 casos / 345 comprobaciones, 0 fallos; ejemplos de lead, veredicto, FAQ y tabla recalculados con el JS (282 / 4.536 / 4.818 / 899 / 5.435 / −126 / 4.410 / −3.150 / 5.481 / 703 €): todos cuadran.

## Norma contrastada hoy (API consolidada del BOE, última versión válida de cada bloque)
- Trampa de versiones: en el RGC (BOE-A-1996-1579), arts. 43 bis y 45 tienen DOS versiones con fecha_vigencia 20230101. La válida es la de publicación posterior (RDL 13/2022, 27/7/2022) frente a la del RD 504/2022 (28/6/2022): art. 43 bis DEROGADO (RDL 13/2022, disp. derog. única.d) y art. 45 = «Cambios posteriores de base» (hasta 6 veces; efectos 1-mar/may/jul/sep/nov/1-ene). Tomar max(fecha_vigencia) a secas da el 43 bis vigente (error). La página cita bien el art. 45.1.
- Tabla 2026: RDL 3/2026 art. 3.4 (tabla 2025 de la DT 1.ª.2 RDL 13/2022, tramos 11-12 con máx. 5.101,20), convalidado (BOE-A-2026-4668); Orden PJC/297/2026 art. 18.1 idéntica a params. DT 1.ª.3: calendario posterior sin fijar → no hay tabla 2027 (la página lo dice). OK.
- Tipos: CC 28,30 · CP 1,30 · MEI 0,90 (RDL 3/2026 art. 3.2; Orden 18.2.c) · cese 0,90 · FP 0,10 (Orden) = 31,50 %. Cese obligatorio (LGSS 327.1). Pluriactividad −0,055 × cuota CC (Orden 18.2.a) y reintegro 50 % > 17.323,68 € (RDL 3/2026 art. 3.5). OK.
- Rendimiento: LGSS 308.1.c.2.ª: 7 % general; el 3 % es para societarios y art. 305.2.b/e (NO para módulos, como decía el encargo); la página lo dice bien. RIRPF art. 30.2: 5 % difícil justificación con tope 2.000 €.
- Regularización: LGSS 308.1.c.3.ª-4.ª (redacción RDL 14/2022): ingreso hasta el último día del mes siguiente a la notificación sin recargo; devolución de oficio sin intereses antes del 30 de abril del año siguiente a la comunicación de la AEAT; RGC 46.2 (RD 665/2024) compara el PROMEDIO de bases. Modelado igual. OK.
- Tarifa plana: LETA art. 38 ter (12 meses + 12 si rendimiento < SMI); RGC 46.1: periodo del 38 ter.1 no se regulariza; el del 38 ter.2 solo si rendimiento > SMI. Página correcta (excluida y declarada).
- RDL 24, 25, 26, 27, 28 y 29/2026 (BOE-A-2026-20264/20265/20266/20385/20822/20823): ninguno toca LGSS 308, RGC 45-46, LETA 38 ter ni la Orden art. 18 (0 menciones de RETA/cuenta propia/bases de cotización). No hay que citarlos.

## Cambios obligatorios
| # | Clase | Archivo · línea | Texto actual → propuesto | Fuente |
|---|---|---|---|---|
| 1 | S | calcs/cuota-autonomos-ingresos-reales-regularizacion.js l. 35 (verdict bloqueo 3) | «Con rendimiento real de 0 € (o sin ingresos declarados en la Renta) la Seguridad Social no regulariza por tramos: aplica…» → «Si no presentas la Renta, o la presentas sin declarar ingresos en estimación directa, la base definitiva es la mínima del grupo de cotización 7 (1.424,40 € al mes, art. 308.1.c.5.ª de la Ley General de la Seguridad Social). Si tuviste ingresos y tu rendimiento neto fue 0 o negativo, tu tramo real es Reducida 1 (hasta 670 €): indica 1 € para calcularlo.» | LGSS 308.1.c.5.ª exige no presentar IRPF o no declarar ingresos; un rendimiento neto ≤ 0 con ingresos cae en el tramo 1 reducido (≤ 670). Cifra 1.424,40: Orden PJC/297/2026 art. 3 (grupo 7) |
| 1b | S | content/…html l. 57 | «Si no declaras ingresos (rendimiento real de 0 €) la calculadora no calcula la regularización: aplica la base mínima del grupo 7.» → «Si no presentas la Renta o no declaras ingresos (estimación directa), se aplica la base mínima del grupo 7 y la calculadora no lo calcula; si tuviste ingresos con rendimiento 0 o negativo, tu tramo es Reducida 1 (pon 1 €).» | ídem |
| 2 | otros (texto no demostrado) | calcs/…js l. 62 (nota pluriactividad) | «…esa opción afecta a la cobertura de contingencias profesionales y no está calculada.» → «…no cubrirla es voluntario si ya la tienes por tu trabajo por cuenta ajena (art. 315 de la Ley General de la Seguridad Social) y esa rebaja no está restada en el cálculo.» | LGSS 316.1: contingencias profesionales «obligatoria»; Orden 18.2.a solo rebaja CC |

Alternativa al 1 (mejor, opcional, para el Constructor): JS l. 16 `if (real <= 0)` → no bloquear y calcular con tramo Reducida 1 (tramoDe(0) ya devuelve 0); oráculo l. 38 igual; añadir a test.json `{prev:1800, real:0, base:1200, meses:12}` → tramoReal 1, regul −N·(1200−718,94)·0,315 = −1.818,41. Mantener el aviso del grupo 7 en la nota.

## Recomendados (no bloquean)
- calcs/…js l. 36 (bloqueo 4): «la nueva base tiene que estar entre 653,59 y 5.101,20 €» → «…entre la mínima del tramo de la nueva previsión que declaras con el cambio (art. 45.2 RGC; desde 653,59 €) y 5.101,20 €». Hoy el motor exige la mínima del tramo previsto a la base inicial pero no al cambio.
- calcs/…json l. 77 (FAQ 1): «La tabla de 2026 es la de 2025, prorrogada por el Real decreto-ley 3/2026.» → «…, salvo la base máxima de General 11 y 12, que sube a 5.101,20 € (art. 3.4).»
- content/…html l. 53: tras «el 5 % de difícil justificación» añadir «(máximo 2.000 € al año, art. 30.2 del Reglamento del IRPF)».
- ops/verif/…_oraculo.py l. 4 y 7 (solo comentario): «RGC 43 bis» → «RGC art. 45.1 (redacción RDL 13/2022, art. 5.1; el 43 bis está derogado)».
Re-verificación: Sonnet, releer las 3 frases (1, 1b, 2); si se toma la alternativa al 1, re-ejecutar oráculo + test.json.
