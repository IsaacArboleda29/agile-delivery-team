# ADR-0001 · Canal de notificación al cliente: WhatsApp primero, SMS como fallback
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

El requisito no funcional **R-09** exige que la notificación al cliente llegue
"por un canal que el cliente ya use habitualmente, sin obligarlo a instalar
una app nueva". La evidencia (`personas.md` · técnico, `inbox/mvp-canvas.md`)
confirma que la coordinación actual del negocio ya pasa por WhatsApp
("Me mandan la dirección por WhatsApp la noche anterior", técnico) y por
llamadas que no escalan. La historia **US-03** (épica E-01) es la que dispara
el envío automático; su criterio de aceptación dice literalmente "recibo un
mensaje con la hora estimada de llegada por un canal que ya uso (WhatsApp o
SMS)". El PO dejó la elección del canal como `open_question` delegada al
Architect (ver `epics.md`, sección "Open questions declaradas por el PO").

La fuerza que obliga a decidir es doble:

1. **R-09 + US-03** — el canal debe ser uno que el cliente ya use, y
   `user-stories.md` lo acota explícitamente a WhatsApp o SMS.
2. **R-12** — la notificación debe llegar en "pocos minutos"; la elección del
   canal afecta la latencia y la tasa de entrega, sobre todo en zonas con red
   inestable (riesgo (c) del MVP canvas).

## Decisión

Se adopta **WhatsApp como canal primario de notificación al cliente** y
**SMS como fallback automático** cuando (a) el trabajo no tiene número de
WhatsApp del cliente cargado, o (b) el envío por WhatsApp falla
(rechazo, número inválido, timeout del proveedor).

El envío se hace a través de una capa de notificación (`NotificationChannel`)
con dos implementaciones: `WhatsAppChannel` y `SmsChannel`, y un selector
basado en (i) el dato de contacto del trabajo y (ii) el resultado del intento
primario. La plantilla del mensaje es la misma para ambos canales (nombre del
técnico, hora estimada, nombre del negocio) y se versiona como pide la nota
de refinamiento de US-03 en `stories.md`.

## Alternativas consideradas

- **Solo SMS** — más simple operacionalmente (un solo proveedor, una sola API)
  pero choca con la evidencia: la coordinación ya ocurre por WhatsApp y el
  cliente ya está acostumbrado a abrir mensajes de WhatsApp del negocio.
  Adoptar solo SMS reintroduce el problema de "canal que el cliente debe
  aprender" y baja la tasa de apertura (riesgo (a) del MVP canvas: alto).
- **Solo WhatsApp** — más alineado con la evidencia pero deja sin canal a
  clientes sin WhatsApp o con número mal cargado. US-03 exige fallar con
  "error claro dirigido al gerente" (nota de refinamiento), no silenciosamente;
  sin fallback, ese error se vuelve regla y el gerente termina llamando a
  esos clientes, exactamente el dolor que la métrica de éxito busca mover.
- **App push propia** — descartada por el mvp-canvas ("fuera de alcance:
  notificaciones push dentro de una app propia") y por R-09 ("sin obligarlo
  a instalar una app nueva").

## Consecuencias

- **Ganamos:** un único canal primario que coincide con el hábito actual del
  cliente (R-09) y un fallback que evita la falla silenciosa. La latencia de
  "pocos minutos" de R-12 se cumple para ambos canales porque el envío es
  asíncrono y el proveedor externo es responsable de la entrega.
- **Costo que aceptamos:** dos integraciones en lugar de una, y un selector
  simple de canal. Es costo pequeño comparado con el riesgo de perder
  trabajos por falta de aviso (pain `cliente-cancela-por-demora`,
  `perdida-clientes`).
- **Decisión deliberadamente diferida (no es parte de este ADR):** la
  elección del proveedor concreto de WhatsApp Business API (Meta Cloud API
  vs. BSP tipo Twilio) se declara como `open_question` porque el
  descubrimiento no la respalda y no es bloqueante para la historia US-03.
