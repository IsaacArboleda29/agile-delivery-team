---
description: El Architect decide la estructura técnica y registra el porqué en ADRs.
argument-hint: "<carpeta del delivery, p. ej. deliveries/citasalud>"
---

# Arquitectura y ADRs

**Delivery:** `$ARGUMENTS`
Prerrequisito: `$ARGUMENTS/outputs/backlog.json` o `epics.md`.

Pasos:
1. Lanza el subagente **architect** (herramienta Task) para:
    - escribir `$ARGUMENTS/outputs/architecture.md` con un diagrama de componentes
      (Mermaid) y la justificación de valor/simplicidad;
    - escribir uno o más `$ARGUMENTS/outputs/adr/ADR-NNNN-<slug>.md` (formato MADR),
      cada uno citando la fuerza que lo motiva.
2. Resume al usuario las decisiones tomadas y, explícitamente, lo que se decidió
   **no** hacer todavía (open questions).