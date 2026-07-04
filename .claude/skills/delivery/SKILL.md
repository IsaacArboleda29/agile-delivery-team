---
name: delivery
description: Formatos y reglas para planificar el delivery ágil — épicas, historias INVEST, backlog estructurado, ADRs, sprint plan, Definition of Ready. Cárgala al generar cualquier artefacto de delivery.
user-invocable: false
---

# Skill · Delivery ágil

Formatos canónicos del equipo. Toda salida los respeta para que los gates y el
reporte puedan auditarla.

## 1. Épica

Una épica agrupa historias hacia un resultado de valor. En `epics.md`:

```
## E-01 · <título de la épica>
**Valor (outcome):** <qué comportamiento cambia / qué número se mueve>
**Origen:** <ítems del mvp-canvas.md / requisitos que la motivan>
**Prioridad:** 1 (más alta) … N
**Historias:** US-01, US-02, …
```

## 2. Historia de usuario (formato INVEST)

En `stories.md`, una historia refinada se ve así:

```
### US-01 · <título corto>   ·   épica E-01   ·   3 pts
**Como** <rol>, **quiero** <acción>, **para** <beneficio>.

Criterios de aceptación (Gherkin):
- Dado <contexto>, cuando <acción>, entonces <resultado verificable>.
- Dado … cuando … entonces …

Origen: <user story / requisito del inbox>
```

Una historia es **INVEST**:
- **I**ndependiente — entregable sin depender de otra (o con dependencias resueltas).
- **N**egociable — no es un contrato cerrado.
- **V**aliosa — el "para" expresa un beneficio real (outcome).
- **E**stimable — tiene una estimación en puntos.
- **S**mall (pequeña) — cabe holgada en un sprint (≤ 8 pts por defecto).
- **T**esteable — tiene criterios de aceptación verificables.

## 3. `backlog.json` (estructurado — lo lee el gate y el reporte)

El PO lo escribe en `generate-epics`. Esquema:

```json
{
  "epics": [
    { "id": "E-01", "title": "Reserva en línea", "value": "...", "priority": 1, "origin": ["mvp:reserva-online"] }
  ],
  "stories": [
    {
      "id": "US-01",
      "epic": "E-01",
      "as_a": "paciente recurrente",
      "want": "reservar una cita en línea",
      "so_that": "no tener que llamar en horario de oficina",
      "acceptance_criteria": [
        "Dado un horario libre, cuando el paciente reserva, entonces la cita queda registrada y recibe confirmación."
      ],
      "estimate": 3,
      "dependencies": [],
      "open_questions": [],
      "priority": 1,
      "origin": ["us:reserva-online"]
    }
  ]
}
```

Reglas de campos (las verifica el gate):
- `as_a`, `want`, `so_that` — no vacíos (formato y valor).
- `acceptance_criteria` — lista con ≥ 1 criterio (testeable).
- `estimate` — número entero > 0 (estimable).
- `estimate` ≤ `DELIVERY_MAX_POINTS` (pequeña; por defecto 8).
- `dependencies` — si hay, deben apuntar a IDs existentes (independiente/trazable).
- `open_questions` — vacío para estar "ready" (Definition of Ready).

## 4. Definition of Ready (DoR)

Una historia entra al sprint solo si: cumple INVEST + tiene criterios de aceptación
+ tiene estimación + no tiene preguntas abiertas bloqueantes. El gate la exige
  antes de escribir `stories.md` y `sprint-plan.md`.

## 5. ADR — Architecture Decision Record (formato MADR breve)

Un ADR por decisión, en `adr/ADR-NNNN-<slug>.md`:

```
# ADR-0001 · <decisión>
**Estado:** aceptado | propuesto | reemplazado por ADR-XXXX
**Fecha:** AAAA-MM-DD

## Contexto y fuerza
<qué problema/fuerza obliga a decidir; cita el origen en el inbox o en una épica>

## Decisión
<lo que se decide>

## Alternativas consideradas
- <alternativa> — <por qué no>

## Consecuencias
<lo que ganamos y el costo que aceptamos>
```

## 6. Sprint Plan

En `sprint-plan.md` y `sprint-plan.json`:

```
# Sprint 1 — <Sprint Goal en una frase>
**Capacidad:** <pts> · **Comprometido:** <pts>
| Historia | Pts | Épica | Prioridad |
|----------|-----|-------|-----------|
| US-01    | 3   | E-01  | 1         |
```

`sprint-plan.json`: `{ "sprint_goal": "...", "capacity": 20, "stories": ["US-01", ...] }`.
Solo entran historias que cumplen la DoR.

## 7. Color y diagramas (Unidad 2: teal + morado)

Codifica por significado, consistente con las diapositivas de la unidad:
- **Estado de historia:** lista (verde) · necesita refinamiento (morado).
- **Prioridad/épica:** teal como color base.
- En `epics.md`, incluye un diagrama Mermaid del backlog (épicas → historias) con
  `classDef` en teal/morado. En `architecture.md`, un diagrama de componentes.

Tras generar los artefactos, `/delivery:report <delivery>` produce
`outputs/report.html`: un dashboard determinista (lo genera `build-report.py`, no el
modelo) que muestra el backlog por épica con el estado INVEST a color y el sprint
plan.