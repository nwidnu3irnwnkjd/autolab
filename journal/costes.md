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
