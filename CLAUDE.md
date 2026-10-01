# AUTOLAB — reglas para cualquier sesión o agente que trabaje aquí

Laboratorio de proyectos web de utilidad, pasivos, operados por agentes. Objetivo: ver si Andoni + Claude
consiguen algo monetizable. Fase actual: **informal, sin monetizar, buscando tracción y tráfico**.

## Principios
1. Capa de decisión, no de datos: cada página responde "¿qué hago?", no "¿cuánto es?".
2. Cada página aporta algo único (cálculo, herramienta o dato). Nada de relleno: Google penaliza contenido escalado vacío.
3. Cifras del texto = cifras del cálculo. El texto nunca inventa números.
4. Web estática, rápida (<2 s), HTML completo para Googlebot, canónicas limpias, sitemap actualizado.
5. Español primero. Inglés solo cuando un proyecto demuestre tracción.
6. Cumplimiento desde el día 1: aviso legal, privacidad, cookies, disclaimer "no es asesoramiento", política de IA visible.
7. Riesgo bajo: nada de cobros, nada de datos personales de usuarios, nada de trámites administrativos ni contenido YMYL sin disclaimer.

## Cómo se trabaja
- Cada proyecto vive en `projects/<slug>/` y se construye con `python3 build.py` → `dist/`. Sin Node, sin dependencias.
- Antes de tocar nada: leer `REGISTRY.md` (estado de proyectos) y las últimas entradas de `journal/`.
- Cada ciclo de trabajo termina con: build OK, commit con mensaje claro, entrada en `journal/YYYY-MM-DD.md`.
- Cambios reversibles (contenido, calculadoras, SEO): hacerlos sin preguntar. Cambios con coste o irreversibles
  (dominios, cuentas, dinero, borrar un proyecto): proponerlos en el journal y esperar a Andoni.
- Modelos: orquestación con el modelo principal; tareas repetitivas (generar páginas, verificar cifras) con modelos eficientes (Haiku/Sonnet).
- Prueba y error: medir (Search Console, analítica), decidir, iterar. Lo que no gana tráfico en 60–90 días se congela.

## Verificación mínima por ciclo
- `python3 build.py` sin errores y `dist/` con sitemap y robots.
- Cada calculadora nueva: 3 casos de prueba con resultado esperado en `calcs/<slug>.test.json` y pasados por `python3 ops/check.py`.
- Ninguna página sin título, descripción, canónica y enlaces internos.
