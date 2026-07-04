#!/usr/bin/env python3
"""
dor-invest-gate.py — Quality gate del Agile Delivery Team.

Hook PreToolUse (matcher Write|Edit). Antes de que el equipo escriba las historias
refinadas (`stories.md`) o el plan del sprint (`sprint-plan.md`), este gate vuelve a
leer el `backlog.json` del MISMO delivery y verifica que cada historia cumpla
INVEST + Definition of Ready. Si algo no cumple, sale con código 2 y BLOQUEA la
escritura, devolviendo el motivo al agente.

Es la versión "delivery" de la idea de la Unidad 1: no confiamos en que el modelo
diga "ya está listo"; lo verificamos de forma independiente contra el dato
estructurado. Gobernanza ejecutable.

Verifica, por cada historia del backlog:
  - formato:      as_a / want / so_that no vacíos              (V + estructura)
  - testeable:    acceptance_criteria con >= 1 criterio        (T)
  - estimable:    estimate es entero > 0                        (E)
  - pequeña:      estimate <= DELIVERY_MAX_POINTS (def. 8)      (S)
  - independiente:dependencies apuntan a IDs existentes         (I + trazabilidad)
  - ready:        open_questions vacío                          (Definition of Ready)
  - no-vaga:      want/title sin términos vagos sin criterio    (T, anti-"sistema rápido")

Config por entorno:
  DELIVERY_MAX_POINTS   máximo de puntos para considerar una historia "pequeña" (8)

Salida:
  exit 0  → deja pasar (no es un archivo custodiado, o todo cumple)
  exit 2  → BLOQUEA (stderr lleva el motivo)
Silencio en stdout siempre (compatibilidad con Claude Code / portabilidad).
"""

import json
import os
import sys
import re

# Artefactos que este gate custodia (basename). Escribir otra cosa pasa libre.
GATED_FILES = {"stories.md", "sprint-plan.md"}

MAX_POINTS = int(os.environ.get("DELIVERY_MAX_POINTS", "8"))

# Términos de vaguedad que, sin un criterio de aceptación que los aterrice,
# vuelven una historia no testeable.
VAGUE_TERMS = [
    "rápido", "rapido", "lento", "intuitivo", "fácil de usar", "facil de usar",
    "amigable", "moderno", "óptimo", "optimo", "eficiente", "mejor", "bonito",
    "robusto", "escalable", "flexible", "sencillo de usar",
]


def read_event():
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def gated_path(event):
    """Devuelve la ruta del archivo si es uno custodiado; si no, None."""
    ti = event.get("tool_input", {}) or {}
    path = ti.get("file_path") or ti.get("path") or ti.get("absolute_path") or ""
    if not path:
        return None
    if os.path.basename(path) in GATED_FILES:
        return path
    return None


def find_backlog(file_path, event):
    """Deriva el backlog.json del mismo delivery a partir de la ruta del archivo.
    stories.md vive en <delivery>/outputs/ ; backlog.json también."""
    out_dir = os.path.dirname(os.path.abspath(file_path))
    candidate = os.path.join(out_dir, "backlog.json")
    if os.path.exists(candidate):
        return candidate
    # fallback: relativo al cwd del evento
    cwd = event.get("cwd", "")
    if cwd:
        candidate2 = os.path.join(cwd, out_dir, "backlog.json")
        if os.path.exists(candidate2):
            return candidate2
    return candidate  # devuelve la ruta esperada aunque no exista (se reporta)


def fail(reasons):
    msg = ["dor-invest-gate: BLOQUEADO — el backlog no está listo para el sprint.", ""]
    msg += [f"  ✗ {r}" for r in reasons]
    msg += [
        "",
        "Corrige las historias señaladas (no evadas el gate):",
        "  · formato Como/Quiero/Para completo",
        "  · al menos un criterio de aceptación verificable (testeable)",
        "  · una estimación en puntos > 0 (estimable)",
        f"  · tamaño <= {MAX_POINTS} pts; si es mayor, divídela (pequeña)",
        "  · sin preguntas abiertas bloqueantes (Definition of Ready)",
    ]
    sys.stderr.write("\n".join(msg) + "\n")
    sys.exit(2)


def main():
    event = read_event()
    file_path = gated_path(event)
    if not file_path:
        sys.exit(0)  # no es un archivo custodiado: pasa libre

    backlog_path = find_backlog(file_path, event)
    if not os.path.exists(backlog_path):
        fail([f"No existe backlog.json en el delivery ({backlog_path}). "
              "Corre /delivery:generate-epics primero."])

    try:
        with open(backlog_path, encoding="utf-8") as fh:
            backlog = json.load(fh)
    except (json.JSONDecodeError, ValueError) as e:
        fail([f"backlog.json no es JSON válido: {e}"])

    stories = backlog.get("stories", [])
    if not stories:
        fail(["El backlog no tiene historias. Nada que llevar al sprint."])

    ids = {s.get("id") for s in stories if s.get("id")}
    reasons = []

    for s in stories:
        sid = s.get("id", "(sin id)")

        # formato Como/Quiero/Para
        for field, label in [("as_a", "Como"), ("want", "quiero"), ("so_that", "para")]:
            if not str(s.get(field, "")).strip():
                reasons.append(f"{sid}: falta '{label}' (formato de historia incompleto).")

        # testeable
        ac = s.get("acceptance_criteria", [])
        if not isinstance(ac, list) or len([c for c in ac if str(c).strip()]) == 0:
            reasons.append(f"{sid}: sin criterios de aceptación (no es testeable).")

        # estimable + pequeña
        est = s.get("estimate", None)
        if not isinstance(est, int) or isinstance(est, bool) or est <= 0:
            reasons.append(f"{sid}: sin estimación válida en puntos (no es estimable).")
        elif est > MAX_POINTS:
            reasons.append(f"{sid}: {est} pts supera el máximo de {MAX_POINTS} (no es pequeña; divídela).")

        # independiente / trazabilidad de dependencias
        deps = s.get("dependencies", []) or []
        for d in deps:
            if d not in ids:
                reasons.append(f"{sid}: depende de '{d}', que no existe en el backlog.")

        # Definition of Ready: sin preguntas abiertas
        oq = s.get("open_questions", []) or []
        if len([q for q in oq if str(q).strip()]) > 0:
            reasons.append(f"{sid}: tiene preguntas abiertas sin resolver (no está 'ready').")

        # no-vaga: si el 'want' usa un término vago y no hay criterio que lo aterrice
        want = str(s.get("want", "")).lower()
        if any(t in want for t in VAGUE_TERMS):
            has_real_ac = isinstance(ac, list) and any(str(c).strip() for c in ac)
            if not has_real_ac:
                reasons.append(f"{sid}: usa un término vago ('{want}') sin criterio medible (no es testeable).")

    if reasons:
        fail(reasons)

    sys.exit(0)


if __name__ == "__main__":
    main()