# Costes por ciclo
fecha-hora | 5h % | semanal % | extra EUR | nota
2026-10-01T20:41Z | 31 | 16 | 0.55 | ciclo 1 inicio (primera línea del día)
2026-10-01T21:20Z | ~33 | ~17 | 0.55+ | ciclo 1 cierre: Diseñador(opus,7min,134k tok) + Constructor(sonnet,1min,69k tok) + QA(haiku,1.6min,64k tok); 1 falso positivo de QA (sitemap) descartado
2026-10-01T21:08Z | 32 | 16 | 0.55 | ciclo 2 inicio (adelantado por Andoni)
2026-10-01T21:35Z | ~34 | ~17 | 0.55 | ciclo 2 cierre: Constructor(sonnet,2min,83k) + Diseñador(sonnet,2.7min,104k) + Estratega(opus,7.8min,141k) + QA(haiku,2.3min,66k); falso positivo QA (JSON-LD) descartado
2026-10-01T21:45Z | 35 | 17 | 0.55 | ciclo 3 inicio (adelantado por Andoni)
2026-10-01T22:10Z | ~37 | ~18 | 0.55 | ciclo 3 cierre: Diseñador(opus,14min,200k) + Constructor(sonnet,1.8min,79k) + Investigador(opus,5.4min,141k) + QA(haiku,1.4min,60k); cadencia acortada a 120 s por orden de Andoni
2026-10-01T21:40Z | 39 | 18 | 0.55 | ciclo 4 inicio
2026-10-01T21:54Z | ~44 | ~20 | 0.55 | ciclo 4 cierre: Constructor(sonnet,2.6min,94k)+Diseñador(sonnet,9.5min,190k)+Estratega(opus,9min,153k)+Mejorador(opus,5min,98k)+Verificador(sonnet,3min,80k)+QA(haiku,3.8min,97k); falso positivo QA (lineChart: ruido de consola de página de prueba borrada) descartado
2026-10-01T21:57Z | 44 | 18 | 0.55 | ciclo 5 inicio (refactor build.py T1 + lote de 2 calculadoras)
2026-10-01T22:06Z | ~48 | ~21 | 0.55 | ciclo 5 cierre: Diseñador(sonnet,refactor,72k,0.8min)+Constructor(sonnet,2 calcs+lineChart,105k,4.2min)+QA(haiku,94k,3.6min); build.py partido en ui.py/calcs_loader.py sin cambio de salida
2026-10-01T22:09Z | 45 | 19 | 0.55 | ciclo 6 inicio (Constructor lote 2 + Estratega frescura + Investigador fuentes fiscales); métricas SC: 0 indexadas/0 impresiones
2026-10-01T22:20Z | ~48 | ~20 | 0.55 | ciclo 6 cierre: Constructor(sonnet,113k)+Estratega(sonnet,113k)+Ingeniero sync(sonnet,116k)+Investigador(opus,en curso)+QA(haiku,94k); datos vivos: luz/carburantes/Euríbor/tiempo; defaults y Barómetro sincronizados con live.json
2026-10-01T22:26Z | 51 | 19 | 0.55 | ciclo 7 inicio (Constructor IRPF + IEH gas; Diseñador Pulso móvil)
2026-10-01T22:58Z | ~50 | ~20 | 0.55 | ciclo 7 cierre: Constructor IRPF(sonnet,210k)+fixes(sonnet,94k)+Diseñador Pulso(sonnet,97k)+Verificador IRPF Opus(231k+253k)+QA(haiku,93k); falso positivo QA (og.png, existe y 200 en producción)
2026-10-01T23:01Z | 3 | 20 | 0.55 | ciclo 8 inicio (Constructor pensiones+luz; Estratega frescura fase 2; Mejorador del equipo pasada 2)
2026-10-01T23:23Z | 10 | 21 | 0.55 | ciclo 8 cierre: Constructor lote fiscal(sonnet,219k)+Estratega frescura f2(sonnet,154k)+Mejorador pasada 2(opus,123k)+Diseñador R8.2(sonnet,92k)+Verificadores fiscales Opus pensiones(108k)+luz(117k)+fixes Sonnet(77k+91k)+re-verificación Sonnet(85k)+QA haiku(70k); 14 calculadoras; 6 errores reales cazados por verificadores (2 legales en pensiones, margen PVPC, avisos de ámbito)
2026-10-01T23:27Z | 10 | 21 | 0.55 | ciclo 9 inicio (T7 close_cycle.sh; Investigador T13; Constructor lote fiscal 3)
2026-10-02T00:14Z | 17 | 23 | 0.55 | ciclo 9 cierre: Ingeniero T7 sonnet 120k; Investigador sonnet 100k; Constructor lote fiscal sonnet 318k; Verificadores Opus autonomo 140k + casa 169k; fixes sonnet 81k+95k; re-verif sonnet 93k; QA haiku 94k; peticiones abiertas: 5; páginas: 31
2026-10-02T00:27Z | 20 | 23 | 0.55 | ciclo 10 cierre: Constructor sonnet 140k; Estratega sonnet 142k; Diseñador F14b sonnet 107k; QA haiku 92k; peticiones abiertas: 7; páginas: 35
2026-10-02T00:39Z | 22 | 23 | 0.55 | ciclo 11 cierre: Constructor sonnet 141k; Diseñador sonnet 84k; QA haiku 106k; peticiones abiertas: 3; páginas: 37
2026-10-02T00:58Z | 25 | 24 | 0.55 | ciclo 12 cierre: Estratega opus 173k; Constructor sonnet 160k; ingeniero tipo fija sonnet 128k; QA haiku 90k; peticiones abiertas: 7; páginas: 39
2026-10-02T01:22Z | 29 | 25 | 0.55 | ciclo 13 cierre: Constructor A sonnet 139k; Constructor B sonnet 162k + fixes 90k; Verificador Opus placas 115k; re-verif sonnet 82k; QA haiku 129k; peticiones abiertas: 8; páginas: 42
2026-10-02T01:51Z | 34 | 26 | 0.55 | ciclo 14 cierre: Estratega sonnet 143k; Investigador sonnet 97k; Constructor fiscal sonnet 196k + fixes 121k + textos 80k; Verificador Opus 132k + 163k; QA haiku 95k; peticiones abiertas: 6; páginas: 44
2026-10-02T02:15Z | 39 | 26 | 0.55 | ciclo 15 cierre: Constructor fiscal sonnet 154k + fixes 91k; Constructor no fiscal sonnet 145k; Diseñador sonnet 82k; Verificador Opus 103k; re-verif sonnet 83k; QA haiku 105k; peticiones abiertas: 7; páginas: 47
2026-10-02T02:29Z | 43 | 27 | 0.55 | ciclo 16 cierre: Mejorador opus 135k; Estratega opus 203k; Constructor sonnet 147k; QA haiku 62k; peticiones abiertas: 12; páginas: 51
2026-10-02T02:47Z | 47 | 28 | 0.55 | ciclo 17 cierre: Diseñador sonnet 78k; Constructor fiscal sonnet 176k + fixes 91k; Constructor no fiscal sonnet 149k; Verificador Opus 97k; QA haiku 108k; peticiones abiertas: 3; páginas: 54
2026-10-02T03:14Z | 53 | 29 | 0.55 | ciclo 18 cierre: Estratega sonnet 73k; Investigador sonnet 89k; Constructor fiscal sonnet 196k + fixes 119k + textos 61k; Constructor no fiscal sonnet 142k; Verificador Opus 118k + 154k; QA haiku 114k; peticiones abiertas: 5; páginas: 57
2026-10-02T03:39Z | 58 | 29 | 0.55 | ciclo 19 cierre: Constructor fiscal sonnet 205k + fixes 130k + textos 60k; Constructor no fiscal sonnet 148k; Verificador Opus 94k + 112k; QA haiku 96k; peticiones abiertas: 6; páginas: 60
2026-10-02T03:59Z | 5 | 30 | 0.55 | ciclo 20 cierre: Estratega sonnet 125k; Constructor fiscal sonnet 163k + fixes 83k; Constructor no fiscal sonnet 126k; Verificador Opus 109k; QA haiku 139k; peticiones abiertas: 7; páginas: 67
2026-10-02T04:32Z | 9 | 31 | 0.55 | ciclo 21 cierre: Diseñador sonnet 81k; Constructor fiscal sonnet 266k + fixes 76k; Constructor no fiscal sonnet 111k; Verificador Opus 115k; QA haiku 69k; peticiones abiertas: 7; páginas: 70
2026-10-02T04:48Z | 12 | 31 | 0.55 | ciclo 22 cierre: Estratega sonnet 125k; Investigador sonnet 77k; Constructor no fiscal sonnet 125k; QA haiku 144k; peticiones abiertas: 3; páginas: 73
2026-10-02T05:11Z | 16 | 32 | 0.55 | ciclo 23 cierre: Constructor fiscal sonnet 170k + fixes 79k; Constructor no fiscal sonnet 133k; Verificador Opus 97k; QA haiku 144k (1 falso positivo: coma decimal); peticiones abiertas: 3; páginas: 76
2026-10-02T05:28Z | 20 | 33 | 0.55 | ciclo 24 cierre: Mejorador opus 161k; Estratega opus 140k; Constructor no fiscal sonnet 124k; Diseñador sonnet 55k; QA haiku 51k; peticiones abiertas: 3; páginas: 79
2026-10-02T05:46Z | 22 | 34 | 0.6 | ciclo 25 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, QA; peticiones abiertas: 3; páginas: 82
2026-10-02T06:03Z | 26 | 34 | 0.55 | ciclo 26 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, Estratega Sonnet, QA; peticiones abiertas: 3; páginas: 85
2026-10-02T06:19Z | 28 | 34 | 0.55 | ciclo 27 cierre: Investigador, Constructor fiscal+Opus+reverif, Constructor no fiscal, QA; peticiones abiertas: 3; páginas: 88
2026-10-02T06:43Z | 33 | 35 | 0.55 | ciclo 28 cierre: Estratega Opus, Constructor fiscal+Opus+reverif, Constructor no fiscal, QA; peticiones abiertas: 1; páginas: 91
2026-10-02T06:56Z | 34 | 35 | 0.55 | ciclo 29 cierre: Constructor no fiscal, Disenador, Estratega ligero x2, QA x2; peticiones abiertas: 0; páginas: 93
2026-10-02T07:08Z | 36 | 35 | 0.55 | ciclo 30 cierre: Constructor no fiscal, Investigador, Estratega ligero, QA, metrics; peticiones abiertas: 0; páginas: 95
2026-10-02T07:22Z | 37 | 35 | 0.55 | ciclo 31 cierre: Constructor, Estratega ligero, QA; peticiones abiertas: 0; páginas: 97
2026-10-02T07:35Z | 39 | 36 | 0.55 | ciclo 32 cierre: Mejorador Opus, Estratega Opus, Investigador Opus, Constructor, QA; peticiones abiertas: 0; páginas: 100
2026-10-02T07:58Z | 43 | 36 | 0.55 | ciclo 33 cierre: 2 Constructores fiscales, 2 Opus, 2 reverif, Editor, Estratega ligero, QA; peticiones abiertas: 0; páginas: 102
2026-10-02T08:21Z | 48 | 37 | 0.55 | ciclo 34 cierre: 2 Constructores fiscales, 2 Opus, reverif, Editor, Estratega ligero, QA; peticiones abiertas: 0; páginas: 104
2026-10-02T08:45Z | 1 | 38 | 0.55 | ciclo 35 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, Estratega ligero x2, QA; peticiones abiertas: 0; páginas: 107
2026-10-02T09:16Z | 8 | 39 | 0.55 | ciclo 36 cierre: Estratega Opus, 2 Constructores fiscales, 3 pasadas Opus, Estratega ligero, QA; peticiones abiertas: 0; páginas: 114
2026-10-02T09:28Z | 10 | 39 | 0.55 | ciclo 37 cierre: Constructor fiscal (aparcado), Constructor no fiscal, Estratega ligero, QA; peticiones abiertas: 0; páginas: 116
2026-10-02T09:39Z | 12 | 40 | 0.55 | ciclo 38 cierre: Investigador fiscal Opus, Constructor no fiscal, Estratega ligero, QA; peticiones abiertas: 0; páginas: 118
2026-10-02T10:04Z | 17 | 40 | 0.55 | ciclo 39 cierre: 2 Constructores fiscales, 3 pasadas Opus, reverif, Estratega ligero, QA; peticiones abiertas: 2; páginas: 120
2026-10-02T10:35Z | 24 | 42 | 0.55 | ciclo 40 cierre: Mejorador Opus, Estratega Opus, 2 Constructores fiscales, 2 Opus, 2 reverif, Estratega ligero, QA; peticiones abiertas: 0; páginas: 123
2026-10-02T10:57Z | 32 | 43 | 0.55 | ciclo 41 cierre: Constructor fiscal+Opus, Editor, Ingeniero herramientas, Estratega ligero, QA; peticiones abiertas: 0; páginas: 124
2026-10-02T11:24Z | 37 | 44 | 0.55 | ciclo 42 cierre: Constructor fiscal+Opus+reverif, Estratega Sonnet (tablas), Editor, Estratega ligero, QA; peticiones abiertas: 0; páginas: 126
2026-10-02T11:53Z | 44 | 45 | 0.55 | ciclo 43 cierre: Constructor fiscal+Opus+reverif, Editor, Estratega ligero, QA; peticiones abiertas: 0; páginas: 127
2026-10-02T12:09Z | 47 | 46 | 0.55 | ciclo 44 cierre: Estratega Opus, Investigador Opus, QA; peticiones abiertas: 0; páginas: 128
2026-10-02T12:29Z | 51 | 46 | 0.55 | ciclo 45 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, comprobador BOE, Estratega ligero, QA; peticiones abiertas: 0; páginas: 131
2026-10-02T12:55Z | 55 | 47 | 0.55 | ciclo 46 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, comprobador BOE, Estratega ligero, QA; peticiones abiertas: 0; páginas: 133
2026-10-02T13:23Z | 59 | 48 | 0.55 | ciclo 47 cierre: Constructor fiscal+Opus+reverif, Constructor no fiscal, Estratega ligero, QA; peticiones abiertas: 0; páginas: 135
2026-10-02T13:52Z | 2 | 49 | 0.55 | ciclo 48 cierre: Mejorador Opus, Estratega Opus, Constructor fiscal+Opus+reverif, comprobador BOE, Estratega ligero, QA x2; peticiones abiertas: 4; páginas: 137
2026-10-02T14:12Z | 4 | 49 | 0.55 | ciclo 49 cierre: Vigilante, Constructor mejora, Editor, Ingeniero herramientas, QA; peticiones abiertas: 1; páginas: 137
2026-10-02T14:44Z | 7 | 50 | 0.55 | ciclo 50 cierre: Diseñador, Estratega x2, Escaparate, Ingeniero OG, QA; peticiones abiertas: 1; páginas: 138
2026-10-02T15:17Z | 10 | 50 | 0.55 | ciclo 51 cierre: Estratega+Diseñador, Constructor fiscal+Opus, Vigilante, QA; peticiones abiertas: 3; páginas: 140
2026-10-02T15:51Z | 13 | 51 | 0.55 | ciclo 52 cierre: Estratega Opus, Diseñador, ingeniero KPIs, QA; peticiones abiertas: 3; páginas: 142
2026-10-02T16:22Z | 17 | 51 | 0.55 | ciclo 53 cierre: Vigilante, 3 Constructores, Opus, Diseñador x2, QA; peticiones abiertas: 4; páginas: 245
2026-10-02T16:45Z | 24 | 53 | 0.55 | ciclo 54 cierre: Diseñador, Vigilante, QA; peticiones abiertas: 4; páginas: 246
2026-10-02T17:05Z | 29 | 54 | 0.55 | ciclo 55 cierre: Diseñador; peticiones abiertas: 4; páginas: 248
2026-10-02T17:30Z | 33 | 54 | 0.55 | ciclo 56 cierre: Mejorador Opus, Estratega Opus; peticiones abiertas: 4; páginas: 249
2026-10-02T19:50Z | 10 | 59 | 0.55 | ciclo 57 cierre: Estratega Opus, 2 Constructores, 2 Opus, Diseñador, QA; peticiones abiertas: 4; páginas: 254
2026-10-02T20:13:09Z | 10 | 59 | 0.55 | c58 inicio (contexto 9%)
2026-10-02T20:40Z | 15 | 60 | 0.55 | ciclo 58 cierre: Constructor x3, Opus x2, Investigador Opus, Vigilante, QA; peticiones abiertas: 4; páginas: 259
2026-10-02T21:29Z | 20 | 60 | 0.55 | ciclo 59 cierre: 2 Constructores, 3 Opus, Estratega Opus, QA; peticiones abiertas: 5; páginas: 264
2026-10-02T22:17Z | 26 | 61 | 0.55 | ciclo 60 cierre: 2 Constructores, 2 Opus, Diseñador, QA; peticiones abiertas: 4; páginas: 268
2026-10-03T15:01Z | 7 | 62 | 0.55 | ciclo 61 cierre: Constructor, Opus x2, Estratega Opus x2, Vigilante, QA; peticiones abiertas: 4; páginas: 272
2026-10-03T15:23Z | 9 | 63 | 0.55 | ciclo 62 cierre: Optimizador Opus, 2 Constructores, QA; peticiones abiertas: 11; páginas: 272
2026-10-03T16:02Z | 24 | 65 | 0.55 | ciclo 63 cierre: Constructores x5, Opus x2, Redactor, QA; peticiones abiertas: 11; páginas: 290
2026-10-03T17:30Z | 33 | 67 | 0.55 | ciclo 64 cierre: Vigilante, Opus x2, Constructores x3, Redactor, Director UX Opus, Disenador, QA x2; peticiones abiertas: 11; páginas: 293
2026-10-05T21:26Z | 11 | 71 | 0.55 | ciclo 65 cierre: Vigilante, Optimizador Opus, Redactor, Constructor, QA (usuario libre); peticiones abiertas: 18; páginas: 296
2026-10-05T22:07Z | 11 | 71 | 0.55 | ciclo 66 cierre: Constructor (usuario libre); peticiones abiertas: 16; páginas: 296
2026-10-06T06:02Z | 7 | 73 | 0.55 | ciclo 67 cierre: Vigilante, Redactor, Disenador x2, QA (usuario libre); peticiones abiertas: 15; páginas: 296
2026-10-06T06:39Z | 0 | 73 | 0.55 | ciclo 68 cierre: Vigilante, Redactor x2 (usuario libre); peticiones abiertas: 15; páginas: 297
2026-10-06T15:21Z | 5 | 0 | 0.55 | ciclo 70 cierre: Constructor, Redactor (usuario libre; semana nueva); peticiones abiertas: 15; páginas: 297
2026-10-07T06:28Z | 5 | 5 | 0.55 | ciclo 71 cierre: Vigilante/Redactor, Opus x4, Constructores x2, QA (usuario libre); peticiones abiertas: 18; páginas: 298
2026-10-07T12:44Z | 5 | 6 | 0.55 | ciclo 72 cierre: Redactor x2, Estratega (a peticion de Andoni); peticiones abiertas: 18; páginas: 302
2026-10-07T16:52Z | 5 | 8 | 0.55 | ciclo 73 cierre: Editor, Constructor, Vigilante, QA (modo continuo); peticiones abiertas: 18; páginas: 302
2026-10-07T17:17Z | 11 | 8 | 0.55 | ciclo 74 cierre: Constructor, Opus, QA propio (modo continuo); peticiones abiertas: 18; páginas: 302
2026-10-07T18:47Z | 15 | 9 | 0.55 | ciclo 75 cierre: Director UX Opus, Disenador x2, Constructor, revision propia; peticiones abiertas: 19; páginas: 302
2026-10-07T19:21Z | 15 | 10 | 0.55 | ciclo 76 cierre: Opus, Constructor, Editor, Redactor (modo continuo); peticiones abiertas: 19; páginas: 302
2026-10-07T19:51Z | 17 | 11 | 0.55 | ciclo 77 cierre: Opus, Constructor x2 (modo continuo); peticiones abiertas: 19; páginas: 302
2026-10-07T20:20Z | 17 | 12 | 0.55 | ciclo 78 cierre: Opus, Constructor, Estratega (modo continuo); peticiones abiertas: 18; páginas: 302
2026-10-07T20:58Z | 17 | 12 | 0.55 | ciclo 79 cierre: editor-calidad,verificador-fiscal,constructor,qa; peticiones abiertas: 18; páginas: 302
2026-10-07T21:23Z | 12 | 11 | 0.55 | ciclo 80 cierre: verificador-fiscal,constructor(barrido); peticiones abiertas: 18; páginas: 302
2026-10-07T21:46Z | 12 | 11 | 0.55 | ciclo 81 cierre: constructor,director-ux; peticiones abiertas: 18; páginas: 302
2026-10-07T22:13Z | 13 | 11 | 0.55 | ciclo 82 cierre: redactor,disenador,qa-propio; peticiones abiertas: 18; páginas: 303
2026-10-07T22:40Z | 14 | 11 | 0.55 | ciclo 83 cierre: disenador,editor-calidad,qa-propio; peticiones abiertas: 18; páginas: 303
2026-10-07T23:13Z | 15 | 11 | 0.55 | ciclo 84 cierre: constructor,verificador-legal,qa-propio; peticiones abiertas: 18; páginas: 303
2026-10-07T23:40Z | 16 | 12 | 0.55 | ciclo 85 cierre: disenador,estratega-seo,qa-propio; peticiones abiertas: 18; páginas: 303
2026-10-08T00:11Z | 1 | 12 | 0.55 | ciclo 86 cierre: verificador-fiscal,constructor,editor-calidad; peticiones abiertas: 18; páginas: 303
2026-10-08T00:35Z | 2 | 12 | 0.55 | ciclo 87 cierre: vigilante,constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T01:01Z | 3 | 12 | 0.55 | ciclo 88 cierre: constructor,estratega-seo; peticiones abiertas: 18; páginas: 303
2026-10-08T01:36Z | 4 | 12 | 0.55 | ciclo 89 cierre: verificador-fiscal,constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T02:19Z | 7 | 12 | 0.55 | ciclo 90 cierre: verificador-fiscal,director-ux,disenador,constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T03:01Z | 9 | 13 | 0.55 | ciclo 91 cierre: verificador-fiscal,constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T03:35Z | 10 | 13 | 0.55 | ciclo 92 cierre: constructor,disenador,qa-propio; peticiones abiertas: 18; páginas: 303
2026-10-08T04:05Z | 11 | 13 | 0.55 | ciclo 93 cierre: verificador-fiscal,constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T04:31Z | 12 | 14 | 0.55 | ciclo 94 cierre: constructor; peticiones abiertas: 18; páginas: 303
2026-10-08T05:15Z | 3 | 14 | 0.55 | ciclo 95 cierre: optimizador,constructor,estratega; peticiones abiertas: 23; páginas: 303
2026-10-08T05:34Z | 3 | 14 | 0.55 | ciclo 96 cierre: vigilante; peticiones abiertas: 23; páginas: 303
2026-10-08T06:39Z | 3 | 14 | 0.55 | ciclo 97 cierre: constructor; peticiones abiertas: 23; páginas: 303
2026-10-08T22:07Z | 4 | 21 | 0.55 | ciclo 98 cierre: redactor; peticiones abiertas: 23; páginas: 304
2026-10-09T05:39Z | 4 | 22 | 0.55 | ciclo 99 cierre: vigilante,redactor; peticiones abiertas: 23; páginas: 305
2026-10-09T14:57Z | 21 | 29 | 0.55 | ciclo 100 cierre: verificador-fiscal,constructor; peticiones abiertas: 23; páginas: 305
2026-10-09T15:33Z | 52 | 36 | 0.55 | ciclo 101 cierre: constructor; peticiones abiertas: 23; páginas: 305
2026-10-09T18:21Z | 2 | 36 | 0.55 | ciclo 103 cierre: editor-calidad,revisor; peticiones abiertas: 23; páginas: 305
2026-10-10T06:12Z | 2 | 38 | 0.55 | ciclo 104 cierre: vigilante; peticiones abiertas: 23; páginas: 305
