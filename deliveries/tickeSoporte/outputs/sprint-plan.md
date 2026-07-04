# Sprint 1 — Entregar al cliente el aviso automático de que el técnico va en camino, con la hora estimada, sin que el técnico tenga que llamar.
**Capacidad:** 20 · **Comprometido:** 16

| Historia | Pts | Épica | Prioridad |
|----------|-----|-------|-----------|
| US-01    | 3   | E-01  | 1         |
| US-02    | 3   | E-01  | 2         |
| US-03    | 5   | E-01  | 3         |
| US-04    | 5   | E-02  | 4         |

## Sprint Goal (justificación)
Cuando el técnico termina un trabajo y pulsa "voy en camino" (o "se demoró, nueva hora"), el cliente del siguiente trabajo recibe un mensaje automático por WhatsApp con la hora estimada de llegada, y desde un enlace puede ver el estado actual del trabajo sin tener que llamar a la empresa. Esto mueve la métrica de éxito del MVP (tasa de trabajos del día en los que el cliente recibió al menos un aviso automático antes de la llegada, umbral ≥ 70 % medido durante 4 semanas; `mvp:metrica-exito`) atacando el dolor compartido declarado en las entrevistas: el cliente no sabe nada mientras el técnico está en el trabajo anterior (`mvp:propuesta-valor`).

El sprint entrega el camino crítico de la propuesta de valor (`mvp-canvas:cobertura-historia-dolor` marca US-01…US-04 como críticos) y cubre los requisitos R-01, R-02, R-03, R-04, R-07, R-08, R-09, R-10 y R-12 del inbox, todos ya anclados a las historias refinadas en `stories.md`. US-03 implementa el envío por el canal que el cliente ya usa (R-09); US-04 materializa la vista de estado sin app (R-09, `mvp:funcionalidad-4`); US-01 y US-02 eliminan el tipeo y la llamada del técnico (R-01, R-08, R-10).

## Historias NO comprometidas
- **US-05 · Agenda del día en un solo lugar (5 pts, prioridad 5)** — queda fuera por capacidad. Es habilitadora para el técnico (sin agenda no hay "siguiente trabajo" que marcar) y para el panel del gerente (US-06), pero el sprint 1 puede operar contra una agenda precargada por el gerente a mano mientras se construye la herramienta, y el botón de US-01 muestra un tooltip claro si no hay "siguiente trabajo" agendado.
- **US-06 · Panel compartido del estado de cada trabajo (3 pts, prioridad 6)** — queda fuera por dependencia de US-05 y por capacidad. El gerente puede consultar el estado pidiendo al técnico o mirando el evento en el log; no bloquea la métrica de éxito del MVP, que se mide del lado del cliente.

## Riesgos y supuestos
- **Capacidad sub-utilizada (16 / 20 pts).** 4 pts de holgura se reservan para imprevistos y para absorber trabajo de refactor de las 4 historias comprometidas (especialmente idempotencia del envío en US-03 y la latencia de propagación en US-04). No se sube el compromiso: la capacidad no se infla.
- **Riesgo de la métrica por dejar US-05 fuera.** El camino crítico US-01/US-02/US-03/US-04 entrega el aviso automático, pero depende de que el gerente cargue los trabajos del día por otro medio (papel/WhatsApp). Si el gerente no carga nada, US-01 queda sin "siguiente trabajo" y el botón no se habilita. Mitigación: durante el sprint el equipo de soporte ayuda al gerente a precargar la agenda del día de lanzamiento desde un canal temporal (hoja de cálculo o mensaje) hasta que US-05 entre al siguiente sprint.
- **Riesgo técnico de US-04 (latencia "pocos minutos").** El criterio de aceptación exige que el cambio de estado aparezca en la vista del cliente en pocos minutos; el Developer nota que esto depende del mecanismo de actualización (WebSocket/SSE/poll). Si la decisión del Architect (ADR) favorece polling, se debe respetar el intervalo acordado para no degradar la experiencia.
- **Supuesto sobre WhatsApp.** US-03 asume que el cliente tiene WhatsApp activo y abre el mensaje. El mvp-canvas marca esto como riesgo alto (`mvp:riesgos-b`); no se mitiga en este sprint, se acepta como hipótesis para validar post-lanzamiento.
- **No hay preguntas abiertas bloqueantes en DoR:** las 6 historias refinadas tienen `open_questions` vacío, formato INVEST completo y estimaciones ≤ 8 pts. El gate `dor-invest-gate.py` no debe bloquear la escritura de este plan.
