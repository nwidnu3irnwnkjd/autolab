# Pre-verificación · fianza-y-garantias-adicionales-alquiler · 2026-10-02 (Constructor fiscal)
Interpretación en ops/verif/fianza-y-garantias-adicionales-alquiler_oraculo.py (bloque INTERPRETACION). Oráculo: 10 fijos + 800 aleatorios, 0 discrepancias. test.json: 9 casos (tol 1 €).
HALLAZGO: el encargo decía «gastos de gestión a cargo del arrendador cuando sea persona jurídica»; la tabla del Estratega y el art. 20.1 (Ley 12/2023) dicen SIEMPRE el arrendador, sin distinguir. Se modela la tabla (leído en la API del BOE el 2/10/2026). El interés legal del art. 36.4 no está en la tabla con cifra: NO se modela, se declara.
| # | Patrón | Estado / dónde |
|---|---|---|
| 1 | Absolutos | hecho: grep siempre/nunca/garantiza/cualquier en content y json = sin hits sin condición |
| 2 | Mecánica | modelado: 36.1 fianza, 36.5 garantía, 17.2 adelanto, 20.1 gestión. Declarado: 36.2 actualización en prórroga, 36.4 interés legal, DA 3.ª depósito, 36.6 exención de Administraciones (arrendatario público: no aplica a particulares) |
| 3 | Territorial | declarado en página y en «Lo que no calcula»: Cataluña, País Vasco, Navarra y otras CCAA; depósito autonómico |
| 4 | Redacción vigente / citas | consolidado LAU 2/10/2026 (RDL 26/2026 derogado, sin efecto 36.5 y 36.7 del RDL). Citas pegadas en S |
| 5 | Bordes | tests: 5 años pf (limita), 6 años pf (sin tope), 7 años pj (limita), 8 pj (sin tope), garantía en 2,0 y 2,5 meses |
| 6 | Defaults/omitidos | defaults = ejemplos editables en params.supuestos, declarados «no oficial»; nada «no verificado» |
| 7 | DT/DF | ver T |
| 8 | ¿Existe la opción? | ver 8 |
T · DT/DF que nombran el art. 36: DT 1.ª del RDL 7/2019 (contratos anteriores a 6-3-2019 conservan su régimen) → declarado: la calculadora aplica la ley vigente; contratos anteriores: «consulta tu contrato». RDL 26/2026 (36.5 y 36.7) sin efecto tras la derogación → no aplica. DT 4.ª Ley 12/2023 para el art. 20 (contratos anteriores a 26-5-2023 siguen su régimen): declarada, comisión puede no aplicar a contratos anteriores.
8 · Opción imposible: renta ≤ 0, duración ≤ 0 o importes negativos → pintar() no calcula (retorna). Uso distinto: art. 36.5/17.2/20.1 no aplican (vivienda) → «Sin tope legal»/«Pactable»; test caso 9 (uso distinto).
N · No modelado: 36.1 (fianza modelada), 36.2 (declarado: sube/baja la fianza en prórroga), 36.3 (declarado: fianza en la parte del plazo >5/7 años según pacto), 36.4 (declarado: devuelve más), 36.5 (modelado), 36.6 (exención AAPP: no aplica), 17.2 (modelado), 20.1 (modelado), DA 3.ª (declarado: depósito autonómico), 4.2 (declarado: >300 m² o >5,5 SMI).
R · RDL 26/2026: no toca arts. 36.1-36.4, 17.2, 20.1 en vigor (sus cambios a 36.5 y 36.7 quedaron sin efecto); se cita solo la derogación (BOE-A-2026-20526) como nota de vigencia. Sin PGE 2026.
S · Fianza 1 y 2 mensualidades · art. 36.1 LAU · «una mensualidad de renta en el arrendamiento de viviendas y de dos en el arrendamiento para uso distinto del de vivienda» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a36 · consultado 2026-10-02
S · Garantía adicional ≤ 2 mensualidades · art. 36.5 · «en contratos de hasta cinco años de duración, o de hasta siete años si el arrendador fuese persona jurídica, el valor de esta garantía adicional no podrá exceder de dos mensualidades de renta» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a36 · consultado 2026-10-02
S · Adelanto ≤ 1 mensualidad · art. 17.2 · «En ningún caso podrá el arrendador exigir el pago anticipado de más de una mensualidad de renta» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a17 · consultado 2026-10-02
S · Gestión y formalización del arrendador · art. 20.1 · «Los gastos de gestión inmobiliaria y los de formalización del contrato serán a cargo del arrendador» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a20 · consultado 2026-10-02
S · Devolución con interés legal · art. 36.4 · «devengará el interés legal, transcurrido un mes desde la entrega de las llaves» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a36 · consultado 2026-10-02
Supuestos no de ley: duración = pactada sin prórrogas (el art. 36.5 dice «duración»); fianza pedida por encima de la legal = no exigible (36.1 fija la cuantía); en uso distinto, garantía/adelanto/comisión pactables (art. 17, 20 y 36.5 son de vivienda); comisión de agencia contratada por el inquilino puede discutirse (declarado).
Verdicto: 5 escenarios probados con stub (conforme, sin tope, solo comisión, mixto, uso distinto): lista de conceptos suma el no exigible.
Rúbrica fianza-y-garantias-adicionales-alquiler: 1=2 2=2 3=0 (verificación Opus pendiente) 4=2 5=2 6=2 7=2 8=2 9=1 (clusters.json sin tocar: petición al Estratega; la guía de cláusulas debe añadir esta calc a `calcs`) 10=2 → 17/20 con punto 3 a 0 hasta verificar.
