# ADR-0002 · Tipo de aplicación: una sola web app responsive con tres vistas (técnico / cliente / gerente)
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

Tres fuerzas empujan en direcciones aparentemente opuestas:

- **R-08 / R-10** (US-01, US-02): el técnico está en campo, con manos
  ocupadas; necesita una pantalla de **un toque** que se vea bien en celular.
- **R-09** (US-04, US-06): el cliente no debe instalar app, y el gerente
  (o quien le ayude) debe ver la agenda desde celular **y** computador.
- **Fuera de alcance del MVP** (`mvp-canvas.md`): "App móvil nativa para el
  cliente", "Notificaciones push dentro de una app propia". Esto cierra la
  opción de app nativa propia para el cliente y para el técnico.

La US-06 refuerza explícitamente la decisión: "vista web responsive, no app
nativa" (nota de refinamiento de US-06, `stories.md`).

## Decisión

Se construye **una única aplicación web responsive** (HTML + CSS + JS
servidos por el mismo backend) con tres rutas/ vistas diferenciadas:

1. **`/tecnico`** — vista móvil con dos botones grandes ("voy en camino" y
   "se demoró, nueva hora") y, debajo, el "siguiente trabajo" de la agenda.
   Optimizada para pantalla de celular, dedo pulgar, manos ocupadas.
2. **`/cliente/<token>`** — vista pública sin login (token de un solo uso
   en URL, ver ADR-0004) que muestra el estado actual del trabajo y el
   historial del día. Carga rápido en el enlace que llega en el WhatsApp.
3. **`/gerente`** — vista de panel con la agenda del día y el estado de
   cada trabajo; usable desde celular y computador.

Una sola base de código reduce la superficie a mantener y garantiza que las
tres vistas compartan el mismo modelo de estado del trabajo. La
"responsive" cubre R-09 (sin app nueva) y R-10 (un toque en celular del
técnico).

## Alternativas consideradas

- **Frontend separado para técnico (móvil) vs. cliente (enlace web) vs.
  gerente (panel web)** — duplica el modelo de estado, los despliegues y
  los mecanismos de autenticación para tres audiencias que, en el MVP, son
  un solo negocio pequeño. El gerente y el técnico son la misma persona o
  un equipo de ≤ 2 (ver `open_question` sobre multi-técnico). El costo de
  mantener tres frontends no se justifica con 6 historias y 24 pts.
- **PWA instalable** — ofrece "icono en pantalla" sin tienda de apps y
  podría cachear la cola offline que pide la nota de refinamiento de US-01.
  Sin embargo, la nota de refinamiento de US-01 ya dice "el cliente del
  técnico debe encolar la acción localmente y reintentar", lo cual se
  resuelve con `localStorage` o `IndexedDB` desde la web responsive sin
  necesitar el shell de PWA. PWA es una mejora, no un prerequisito; se
  declara como `open_question` (mejora post-MVP) en lugar de inflar el MVP.
- **Nativa para el técnico** — descartada por "fuera de alcance: app móvil
  nativa" del mvp-canvas. Además, una app nativa introduce el problema
  de "el técnico debe instalar y mantener la app" en un usuario con manos
  ocupadas.

## Consecuencias

- **Ganamos:** una sola base de código, un solo modelo de estado, un solo
  despliegue. Las tres audiencias comparten la agenda (US-05) y el evento
  de estado (US-01/02) sin duplicación. R-08, R-09 y R-10 se cumplen con
  la misma aplicación.
- **Costo que aceptamos:** la vista del técnico en `/tecnico` no tendrá el
  mismo "feel" de una app nativa (sin haptic feedback, sin icono dedicado
  en el launcher). Se mitiga con un buen responsive y un acceso directo
  en la pantalla de inicio (atajo del navegador, no PWA completa) si
  surge como necesidad real.
- **Decisión deliberadamente diferida:** convertir la web en PWA
  instalable se trata como `open_question` (mejora) — no es ADR aceptado.
