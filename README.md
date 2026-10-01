# autolab

Laboratorio de webs de utilidad operadas por agentes. Ver `CLAUDE.md` (reglas), `REGISTRY.md` (proyectos),
`ops/loop-prompt.md` (ciclo autónomo) y `journal/` (diario).

## Operar
- Construir un proyecto: `cd projects/decidir && python3 build.py`
- Servir en local: `bash ops/serve.sh decidir` → http://localhost:8787
- Ciclo autónomo: en Claude Code, `/loop` con el contenido de `ops/loop-prompt.md`.
