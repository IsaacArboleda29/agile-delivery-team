# ADR-0003 · Persistencia y propagación de eventos: backend HTTP con persistencia relacional y polling corto (sin WebSocket/SSE en MVP)
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

- **R-12** exige que "el cambio de estado del técnico y la notificación al
  cliente se propaguen en pocos minutos". US-02 lo trae a sus criterios y
  US-04 dice "cuando refresco, el nuevo estado aparece en pocos minutos".
- La nota de refinamiento de **US-06** dice: "La actualización del panel
  debe ser por push o polling en ≤ 60 s para cumplir la latencia de 'pocos
  minutos' de R-12; el equipo decide el mecanismo (WebSocket/SSE/poll) en
  el sprint planning." — el Architect debe decidir ese mecanismo.
- **US-01** nota de refinamiento: "el evento se persiste en ≤ 30 s aunque
  la red del cliente sea mala; si no hay conectividad, el cliente del
  técnico debe encolar la acción localmente y reintentar."
- **R-11** exige disponibilidad en horario laboral completo, sin caídas en
  horas pico.

La fuerza que obliga a decidir es: ¿cómo lleva el backend el evento
`tecnico.en_camino` (US-01) hasta el panel del gerente (US-06) y la vista
del cliente (US-04) en "pocos minutos" sin sobre-diseñar?

## Decisión

Se adopta una **arquitectura HTTP request/response clásica** con los
siguientes componentes:

- **API REST** del backend recibe `POST /eventos` desde la vista del técnico
  (`/tecnico`) y registra el evento en una **base de datos relacional** con
  un único reloj del servidor (timestamp del servidor, no del cliente, como
  pide la nota de refinamiento de US-01).
- Un **worker de envíos asíncronos** (proceso en segundo plano del mismo
  backend, sin cola externa) consume los eventos nuevos y dispara
  `WhatsAppChannel` o `SmsChannel` (ver ADR-0001). Esto satisface US-03 sin
  bloquear la respuesta HTTP al técnico (R-12).
- La vista del cliente (`/cliente/<token>`, US-04) y el panel del gerente
  (`/gerente`, US-06) **leen del backend con polling** cada **30 s** cuando
  la pestaña está activa. El cliente también puede refrescar manualmente.
  Un polling de 30 s cumple el "pocos minutos" de R-12 con margen (el peor
  caso es un cambio que se ve a los 30 s, dentro del SLA).
- **Cola local en el cliente del técnico** (US-01): si no hay red, el
  frontend encola en `localStorage` y reintenta; el backend acepta eventos
  con timestamp del cliente como sugerencia, pero siempre sobrescribe con
  su propio reloj al persistir.

No se usan WebSocket ni SSE en el MVP. No se usa una cola externa
(RabbitMQ, SQS, Redis Streams). No se usa un cache distribuido.

## Alternativas consideradas

- **WebSocket bidireccional** — menor latencia percibida (cambio
  instantáneo en la vista del cliente), pero introduce: (a) un servidor
  con estado de conexiones, (b) lógica de reconexión y (c) pruebas más
  costosas. R-12 pide "pocos minutos", no segundos. El "casi instantáneo"
  no mueve la métrica de éxito (umbral ≥ 70 % de trabajos con un aviso
  recibido antes de la llegada) y sí añade complejidad operativa en un
  MVP de 24 pts.
- **SSE (Server-Sent Events)** — más simple que WebSocket y suficiente para
 推送 unidireccional servidor→cliente, pero añade un endpoint de larga
  duración que complica el deploy y los proxies típicos. Polling cada
  30 s da una experiencia equivalente para el caso de uso (el cliente
  refresca o espera; el gerente ve la lista).
- **Cola externa (SQS / Pub/Sub)** — robusto y escalable, pero es
  sobre-diseño: el volumen del MVP es de decenas de eventos/día (un negocio
  con handful de técnicos y ≤ 20 trabajos/día). Un worker en proceso basta
  y elimina un proveedor más en la cuenta.
- **Sin backend (cliente → cliente directo)** — imposible: la notificación
  al cliente se hace por WhatsApp/SMS, que requiere un originador
  (proveedor externo), no un peer-to-peer entre celulares.

## Consecuencias

- **Ganamos:** un solo proceso backend por rol (API + worker), una sola
  base de datos, cero infraestructura de cola/conexiones. La latencia de
  30 s cumple R-12 con margen y US-01/US-02/US-04/US-06 quedan
  cubiertas con el mismo mecanismo. Las pruebas son HTTP puras, fáciles
  de escribir y de gatear.
- **Costo que aceptamos:** la vista del cliente puede mostrar un estado
  con hasta 30 s de retraso. Aceptable porque (a) R-12 habla de "pocos
  minutos", no de segundos, y (b) el aviso principal al cliente es el
  WhatsApp (US-03), que se dispara por el worker asíncrono y llega
  típicamente en < 1 min, no por el polling de la vista web.
- **Decisión deliberadamente diferida:** si la métrica de éxito se mueve
  pero el feedback del negocio exige "cambio casi instantáneo en la vista
  del cliente", evaluar SSE o WebSocket como evolución post-MVP. Se
  declara como `open_question`.
