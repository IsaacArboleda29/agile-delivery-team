#!/usr/bin/env python3
"""
build-report.py — Reporte HTML visual de un delivery, determinista y sin dependencias.

Lee backlog.json (+ sprint-plan.json si existe) y produce outputs/report.html: un
dashboard con el backlog por épica, el estado INVEST de cada historia codificado por
color, y el sprint plan. Paleta de la Unidad 2: teal + morado.

Es determinista (mismo input → mismo output); no depende del modelo. Misma filosofía
que el gate: lógica en código.

USO:
    python3 .claude/scripts/build-report.py <carpeta-del-delivery>
    python3 .claude/scripts/build-report.py deliveries/citasalud
"""

import json
import os
import sys
import html
from datetime import date

# Paleta Unidad 2
TEAL = "#0F766E"; TEAL_DEEP = "#0A5750"; TEAL_TINT = "#DCEEEB"; TEAL_MID = "#3E9B8C"
PLUM = "#8B5DA8"; PLUM_INK = "#6A3D86"; PLUM_SOFT = "#EADCF3"
INK = "#0E1A26"; PAPER = "#F3F4F1"
GREEN = "#2E7D52"; GREEN_BG = "#E3F1E8"
RED = "#B3402F"; RED_BG = "#F6E2DD"

MAX_POINTS = int(os.environ.get("DELIVERY_MAX_POINTS", "8"))


def esc(x):
    return html.escape(str(x), quote=True)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def story_status(s):
    """Devuelve (ready: bool, motivos: list[str]) replicando la lógica del gate."""
    reasons = []
    for f, lab in [("as_a", "Como"), ("want", "quiero"), ("so_that", "para")]:
        if not str(s.get(f, "")).strip():
            reasons.append(f"falta '{lab}'")
    ac = s.get("acceptance_criteria", [])
    if not isinstance(ac, list) or not [c for c in ac if str(c).strip()]:
        reasons.append("sin criterios")
    est = s.get("estimate", None)
    if not isinstance(est, int) or isinstance(est, bool) or est <= 0:
        reasons.append("sin estimación")
    elif est > MAX_POINTS:
        reasons.append(f"{est} pts (muy grande)")
    if [q for q in (s.get("open_questions") or []) if str(q).strip()]:
        reasons.append("preguntas abiertas")
    return (len(reasons) == 0, reasons)


def chip(text, fg, bg):
    return (f'<span style="display:inline-block;padding:2px 9px;border-radius:999px;'
            f'font:600 11px/1.6 ui-monospace,Menlo,monospace;color:{fg};'
            f'background:{bg};white-space:nowrap">{esc(text)}</span>')


def build(delivery_dir):
    name = os.path.basename(os.path.normpath(delivery_dir))
    out_dir = os.path.join(delivery_dir, "outputs")
    backlog = load_json(os.path.join(out_dir, "backlog.json")) or {}
    sprint = load_json(os.path.join(out_dir, "sprint-plan.json"))

    epics = backlog.get("epics", [])
    stories = backlog.get("stories", [])
    by_epic = {}
    for s in stories:
        by_epic.setdefault(s.get("epic", "(sin épica)"), []).append(s)

    ready_count = sum(1 for s in stories if story_status(s)[0])
    total_pts = sum(s.get("estimate") or 0 for s in stories if isinstance(s.get("estimate"), int))

    P = []
    A = P.append
    A(f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Delivery — {esc(name)}</title>
<style>
  *{{box-sizing:border-box}}
  body{{margin:0;background:{PAPER};color:{INK};
    font-family:'IBM Plex Sans',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;line-height:1.5}}
  .wrap{{max-width:1000px;margin:0 auto;padding:32px 24px 80px}}
  .eyebrow{{font:600 12px/1.6 ui-monospace,Menlo,monospace;letter-spacing:.12em;
    text-transform:uppercase;color:{TEAL}}}
  h1{{font-size:34px;margin:.1em 0}}
  h2{{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:{TEAL};
    border-bottom:2px solid {TEAL};padding-bottom:6px;margin:38px 0 16px;font-family:ui-monospace,Menlo,monospace}}
  h3{{font-size:16px;margin:0}}
  .sub{{color:#3C4A57}}
  .counts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}}
  .stat{{background:#fff;border:1px solid #D7DCE2;border-radius:12px;padding:10px 16px;min-width:92px}}
  .stat b{{display:block;font-size:24px;line-height:1.1}}
  .stat span{{font-size:12px;color:#3C4A57}}
  .legend{{display:flex;flex-wrap:wrap;gap:18px;background:#fff;border:1px solid #D7DCE2;
    border-radius:12px;padding:12px 16px;margin-top:16px;font-size:13px}}
  .legend div{{display:flex;align-items:center;gap:7px}}
  .dot{{width:12px;height:12px;border-radius:3px;display:inline-block}}
  .epic{{background:#fff;border:1px solid #D7DCE2;border-left:5px solid {TEAL};border-radius:14px;padding:16px 18px;margin-bottom:16px}}
  .epic .head{{display:flex;justify-content:space-between;align-items:start;gap:10px;flex-wrap:wrap}}
  .epic .val{{color:#3C4A57;font-size:14px;margin-top:4px}}
  .story{{border:1px solid #E7EAEE;border-left:4px solid {GREEN};border-radius:10px;padding:10px 14px;margin-top:10px;background:#FBFCFA}}
  .story.refine{{border-left-color:{PLUM}}}
  .story .t{{display:flex;justify-content:space-between;gap:10px;align-items:start;flex-wrap:wrap}}
  .story .desc{{font-size:13.5px;margin-top:4px}}
  .story .meta{{font-size:11.5px;color:#3C4A57;margin-top:4px;font-family:ui-monospace,Menlo,monospace}}
  .sprint{{background:{TEAL_TINT};border:1px solid {TEAL};border-radius:14px;padding:18px 20px}}
  table{{border-collapse:collapse;width:100%;background:#fff;border-radius:10px;overflow:hidden;font-size:14px;margin-top:10px}}
  th,td{{text-align:left;padding:9px 13px;border-bottom:1px solid #E7EAEE}}
  th{{background:{PLUM_SOFT};font:600 11px/1.6 ui-monospace,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase;color:{PLUM_INK}}}
  tr:last-child td{{border-bottom:none}}
  .foot{{margin-top:44px;font-size:12px;color:#6A7682}}
  .mono{{font-family:ui-monospace,Menlo,monospace}}
</style></head><body><div class="wrap">""")

    A(f'<div class="eyebrow">Agile Delivery Team · reporte visual</div>')
    A(f'<h1>{esc(name)}</h1>')
    A(f'<div class="sub">Plan de entrega — generado {date.today().isoformat()}.</div>')
    A('<div class="counts">')
    for v, l in [(len(epics), "épicas"), (len(stories), "historias"),
                 (f"{ready_count}/{len(stories)}", "listas (DoR)"), (total_pts, "puntos")]:
        A(f'<div class="stat"><b>{v}</b><span>{l}</span></div>')
    A('</div>')

    A('<div class="legend">')
    A(f'<div><span class="dot" style="background:{GREEN}"></span>historia lista (cumple INVEST + DoR)</div>')
    A(f'<div><span class="dot" style="background:{PLUM}"></span>necesita refinamiento</div>')
    A('</div>')

    # Backlog por épica
    A('<h2>Backlog por épica (priorizado por valor)</h2>')
    for e in sorted(epics, key=lambda x: x.get("priority", 99)):
        A('<div class="epic">')
        A(f'<div class="head"><h3>{esc(e.get("id",""))} · {esc(e.get("title",""))}</h3>'
          f'{chip("prioridad " + str(e.get("priority","?")), TEAL_DEEP, TEAL_TINT)}</div>')
        A(f'<div class="val">{esc(e.get("value",""))}</div>')
        for s in by_epic.get(e.get("id"), []):
            ready, reasons = story_status(s)
            cls = "story" if ready else "story refine"
            badge = chip(f'{s.get("estimate","?")} pts', PLUM_INK, PLUM_SOFT) if ready \
                    else chip("refinar: " + ", ".join(reasons), RED, RED_BG)
            A(f'<div class="{cls}"><div class="t"><b>{esc(s.get("id",""))} · {esc(s.get("want",""))}</b>{badge}</div>')
            A(f'<div class="desc">Como <b>{esc(s.get("as_a",""))}</b>, quiero {esc(s.get("want",""))}, para {esc(s.get("so_that",""))}.</div>')
            ac = s.get("acceptance_criteria") or []
            if ac:
                A(f'<div class="meta">{len(ac)} criterio(s) de aceptación · origen: {esc(", ".join(s.get("origin",[])))}</div>')
            A('</div>')
        A('</div>')

    # Sprint plan
    if sprint:
        A('<h2>Sprint Plan</h2>')
        A('<div class="sprint">')
        A(f'<h3>{esc(sprint.get("sprint_goal",""))}</h3>')
        A(f'<div class="sub mono" style="margin-top:6px">capacidad {sprint.get("capacity","?")} pts · comprometido {sprint.get("committed","?")} pts</div>')
        sel = sprint.get("stories", [])
        smap = {s.get("id"): s for s in stories}
        A('<table><thead><tr><th>Historia</th><th>Pts</th><th>Épica</th></tr></thead><tbody>')
        for sid in sel:
            s = smap.get(sid, {})
            A(f'<tr><td>{esc(sid)} · {esc(s.get("want",""))}</td><td>{esc(s.get("estimate","?"))}</td><td>{esc(s.get("epic",""))}</td></tr>')
        A('</tbody></table></div>')

    A(f'<div class="foot">Generado por <span class="mono">build-report.py</span> desde '
      f'<span class="mono">backlog.json</span>'
      f'{" y sprint-plan.json" if sprint else ""}. '
      f'El detalle en prosa (historias, ADRs) está en los .md de '
      f'<span class="mono">{esc(name)}/outputs/</span>.</div>')
    A('</div></body></html>')

    report_path = os.path.join(out_dir, "report.html")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("".join(P))
    return report_path


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 build-report.py <carpeta-del-delivery>", file=sys.stderr)
        sys.exit(1)
    d = sys.argv[1]
    if not os.path.isdir(os.path.join(d, "outputs")):
        print(f"No existe {d}/outputs. ¿Corriste generate-epics primero?", file=sys.stderr)
        sys.exit(1)
    print(f"✓ Reporte generado: {build(d)}")


if __name__ == "__main__":
    main()