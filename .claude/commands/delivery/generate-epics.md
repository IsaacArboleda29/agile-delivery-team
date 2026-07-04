---
description: El Product Owner descompone el MVP del Discovery Agent en épicas y un backlog priorizado por valor.
argument-hint: "<carpeta del delivery, p. ej. deliveries/citasalud>"
---

# Generar épicas y backlog

**Delivery:** `$ARGUMENTS`
Si está vacío, pregunta cuál delivery antes de continuar.

Prerrequisito: `$ARGUMENTS/inbox/` debe contener las salidas del Discovery Agent
(`mvp-canvas.md`, `user-stories.md`, `requisitos.md`, `personas.md`,
`evidence-map.json`). Si está vacío, pide al usuario que las copie ahí.

Pasos:
1. Lanza el subagente **product-owner** (herramienta Task) con la instrucción de
   leer `$ARGUMENTS/inbox/` y producir:
    - `$ARGUMENTS/outputs/epics.md` — épicas legibles + diagrama Mermaid del backlog.
    - `$ARGUMENTS/outputs/backlog.json` — estructurado, según el esquema de la skill.
2. Verifica que cada épica e historia tenga su `origin` trazando al inbox.
3. Resume al usuario: cuántas épicas, cuántas historias candidatas, y el orden de
   prioridad con una línea de justificación por épica.

No escribas `stories.md` aquí (eso es de `generate-stories` y pasa por el gate).