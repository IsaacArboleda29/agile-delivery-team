---
description: El Scrum Master arma el Sprint Plan con las historias que cumplen la Definition of Ready, respetando la capacidad. Pasa por el gate.
argument-hint: "<carpeta del delivery> [capacidad en puntos, p. ej. 20]"
---

# Sprint Plan

**Delivery:** `$ARGUMENTS`
Prerrequisito: `$ARGUMENTS/outputs/backlog.json` con historias refinadas
(de `/delivery:generate-stories`, ya pasadas por el gate).

Pasos:
1. Lanza el subagente **scrum-master** (herramienta Task) para:
    - definir un **Sprint Goal** claro en una frase;
    - seleccionar, en orden de prioridad, solo historias que cumplan la DoR, hasta
      la capacidad indicada (por defecto 20 pts);
    - escribir `$ARGUMENTS/outputs/sprint-plan.md` y `sprint-plan.json`.
2. Al escribir se ejecuta el hook **dor-invest-gate** (también custodia el sprint
   plan): si una historia incluida no está lista, bloquea. Corrige y reintenta.
3. Resume: Sprint Goal, historias comprometidas y puntos (comprometido ≤ capacidad).