---
description: Genera un reporte HTML visual del delivery (backlog por épica con estado INVEST y sprint plan), determinista desde los JSON.
argument-hint: "<carpeta del delivery, p. ej. deliveries/citasalud>"
---

# Reporte visual del delivery

**Delivery:** `$ARGUMENTS`
Prerrequisito: `$ARGUMENTS/outputs/backlog.json` (y opcionalmente `sprint-plan.json`).

Pasos:
1. Ejecuta el generador determinista (no inventes el HTML; lo produce el script):
   ```bash
   python3 .claude/scripts/build-report.py $ARGUMENTS
   ```
2. Confirma la ruta (`$ARGUMENTS/outputs/report.html`) y resume qué contiene:
   backlog por épica con el estado INVEST a color (verde = lista, morado = necesita
   refinamiento), prioridad, y el sprint plan.