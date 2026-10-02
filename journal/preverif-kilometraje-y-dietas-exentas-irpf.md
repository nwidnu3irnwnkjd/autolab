# Pre-verificación · kilometraje-y-dietas-exentas-irpf · 2026-10-02 (Constructor fiscal)
HALLAZGO PRIORITARIO: el backlog citaba «RIRPF art. 9.A.1.a / 9.A.2.a». Correcto: locomoción = art. 9.A.2.b. El texto consolidado del Reglamento sigue diciendo 0,19 €/km; el 0,26 sale de la Orden HFP/792/2023 (art. único.1, BOE-A-2023-16461, vigente desde 17-7-2023), que el análisis del BOE lista como norma «en relación». La AEAT (Manual Renta 2025) aplica 0,26. Sin revisión posterior. Se declara en la página.
Oráculo: ops/verif/kilometraje-y-dietas-exentas-irpf_oraculo.py (INTERPRETACION + 17 fijos + 800 aleatorios, 0 discrepancias; `--contenido` 0 fallos). Tests: 10 casos con valores del oráculo (a mano: caso 1 = 720 €, caso 0,40 €/km = 413,04 €).
| # | Patrón | Estado / dónde |
|---|---|---|
| 1 | Absolutos | hecho: grep siempre/nunca/garantiza/solo tiene sentido/en todos los casos/cualquier = 0 en content, json y js (contenido() lo comprueba) |
| 2 | Mecánica que mueve la base | modelado: 9.A.2.b, 9.A.3.a.1.º/2.º, 9.A.6, LIRPF 17.1.d, 19.2.a (cotización deducible), LGSS 147.2.b (exceso cotiza). Declarado: art. 20 y DA 61.ª (dentro del tipo marginal que pone el usuario), base máxima/solidaridad (LGSS 19 bis), dietas y comedor misma jornada (RIRPF 45), 9.B (relaciones especiales) |
| 3 | Territorial | forales declarados; Canarias/Ceuta-Melilla: misma norma de Reglamento estatal; deducciones autonómicas no afectan |
| 4 | Redacción vigente | a9 RIRPF (versiones 2007, 2008, 2023; API 30-9-2026); a147 LGSS (v. 1-1-2023); LIRPF a17, a19 leídos. Citas: 9.A.2.b «0,19 euros por kilómetro recorrido, siempre que se justifique la realidad del desplazamiento, más los gastos de peaje y aparcamiento que se justifiquen»; Orden «multiplicar 0,26 euros por el número de kilómetros recorridos»; 9.A.3.a.2.º «26,67 ó 48,08 euros diarios»; 19.2 «exclusivamente los siguientes» |
| 5 | Bordes | tests en 0,26=0,26 (empate), dieta 26,67/26,68, 53,35, tipo 47, días 365+, sin datos |
| 6 | Defaults | km/peajes/días/dieta/tipo = ejemplos editables (params supuestos); coste/km = live.gasolina95 x 0,065 + 0,05 como coche-propio-o-carsharing-o-vtc |
| 7 | DT/DF | RIRPF art. 9: ninguna DT lo nombra; LGSS 147: DA 38.ª (músicos) no aplica; DF del Reglamento 2008 (RD 1804/2008) tocó 9.A.3 con efectos 2008, sin efecto en 2026 |
| 8 | Opción imposible | días con+sin > 365 -> bloqueo 2 (test); sin km ni días -> bloqueo 1 (test); sin km con dietas -> escenario 5 (test); tipo > 47 se acota |
T · 9.A sin DT; LGSS 147 sin DT en 2026 · 8 · ver fila 8 · N · no modelado en «Supuestos» con efecto: extranjero (sube lo exento), >9 meses (baja lo exento), estancia (exenta), transporte carretera y vuelo (importes propios), base máxima (baja ligeramente el coste de cotizar), comedor el mismo día (RIRPF 45: los días con dieta exenta no cuentan para la fórmula de comida) · R · RDL 26/2026: no toca arts. 9 RIRPF, 17/19 LIRPF ni 147 LGSS; no se cita; no hay PGE 2026.
S · km exento 0,26 · Orden HFP/792/2023 art. único.1 · «se excluirá la cantidad que resulte de multiplicar 0,26 euros por el número de kilómetros recorridos» · https://www.boe.es/eli/es/o/2023/07/12/hfp792 · consultado 2026-10-02
S · manutención 26,67/53,34 · RIRPF 9.A.3.a · «53,34 euros diarios» / «26,67 ó 48,08 euros diarios» · https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a9 · consultado 2026-10-02
S · exceso tributa · RIRPF 9.A.6 · «estarán sujetas a gravamen» · idem · consultado 2026-10-02
S · exceso cotiza · LGSS 147.2.b · «en la cuantía y con el alcance previstos en la normativa estatal reguladora del Impuesto sobre la Renta» · https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a147 · consultado 2026-10-02
S · cotización deducible · LIRPF 19.2.a · «Las cotizaciones a la Seguridad Social» · https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764 · consultado 2026-10-02
S · cotización 6,5 % · Orden PJC/297/2026 (ya verificada en autonomo_2026) · consultado 2026-10-02
SUPUESTOS PROPIOS (declarados): tipo marginal del usuario; dieta igual en ambos tipos de día; peajes reembolsados (neto 0); coste del coche solo variable; sin base máxima.
Supuesto de interpretación a validar por el Verificador: «kilometraje pagado por debajo de 0,26 nunca tributa» y que el exceso de manutención cotiza (147.2.b).
Rúbrica kilometraje-y-dietas-exentas-irpf: 1=2 2=2 3=0 (verificación Opus pendiente) 4=2 5=2 6=2 7=2 8=2 9=1 (clusters sin tocar: petición al Estratega) 10=2 → 17/20 con punto 3 a 0 hasta verificar.

Verificación Opus aplicada (3 cambios): lead/veredicto con centro habitual y «en general»; 9.A.3 vs kilometraje en «Ten los justificantes»; tipo marginal = base liquidable 20.200-35.200 (bruto ~24.000-40.000). S/R del Verificador: sin líneas nuevas (RDL 26/2026 no toca 9 RIRPF, 17/19 LIRPF, 147 LGSS; transportistas 15/25 € declarados como excluidos).

R · RDL 26/2026 derogado el 2-10-2026 · BOE-A-2026-20526 · revisado c53
