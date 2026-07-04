# Requisitos candidatos — tickeSoporte

> Discovery: `discoveries/tickeSoporte`
> Evidencia: `discoveries/tickeSoporte/interviews/`
> Numero correlativo (R-NN). Cada requisito cita la fuente que lo respalda.

## Funcionales

- **[R-01]** El técnico debe poder indicar con una sola acción que va "en camino" al siguiente cliente.
  - Tipo: funcional
  - Origen: `tecnico.md` · Técnico de campo
  - Evidencia: "Me gustaría tener algo donde yo toco un botón y el cliente sabe que voy en camino o que me demoré, sin tener que llamar yo".

- **[R-02]** Cuando el técnico marque "en camino", el cliente debe recibir una notificación automática con la hora estimada de llegada.
  - Tipo: funcional
  - Origen: `cliente.md` · Cliente residencial
  - Evidencia: "Si alguien me mandara un mensaje cuando el técnico salió hacia mi casa, o me avisara si se va a demorar, ese ya tiene mi preferencia".

- **[R-03]** Cuando el técnico sufra un retraso, debe poder actualizar la hora estimada con un cambio mínimo (un toque) y el cliente debe recibir el nuevo aviso sin que el técnico tenga que redactar ni llamar.
  - Tipo: funcional
  - Origen: `tecnico.md`, `cliente.md` · Técnico de campo, Cliente residencial
  - Evidencia: "no sé qué herramienta existe para eso" (técnico); "si me dijeran 'mire, el técnico se retrasó, llega a las cinco' yo puedo planificar" (cliente).

- **[R-04]** El cliente debe poder ver el estado actual del trabajo asignado (asignado / en camino / en sitio / finalizado) sin tener que llamar a la empresa.
  - Tipo: funcional
  - Origen: `cliente.md` · Cliente residencial
  - Evidencia: "es como cuando uno pide un domicilio y puede ver dónde está el repartidor, ¿por qué con los técnicos no existe algo así?".

- **[R-05]** El sistema debe permitir registrar la agenda del día (orden de trabajos, dirección y hora estimada inicial) de forma rápida, sin escribir a mano como en la agenda en papel.
  - Tipo: funcional
  - Origen: `gerente_general.md` · Gerente general
  - Evidencia: "Hemos probado con agenda en papel, con el calendario del teléfono, pero igual toca escribir todo a mano y cuando hay tres trabajos en el día ya se complica".

- **[R-06]** La lista de trabajos del día debe ser visible para quien ayude a contestar mensajes, para que cualquiera en el negocio sepa el estado de cada visita.
  - Tipo: funcional
  - Origen: `gerente_general.md` · Gerente general
  - Evidencia: "A veces alguien me ayuda contestando mensajes pero tampoco sabe en qué estado está cada trabajo".

- **[R-07]** El sistema debe notificar al cliente el evento "técnico en camino" y el evento "técnico demorado, nueva hora" sin requerir que el técnico redacte mensajes.
  - Tipo: funcional
  - Origen: `tecnico.md` · Técnico de campo
  - Evidencia: "sin tener que llamar yo, porque cuando estoy trabajando no puedo estar con el teléfono en la mano".

## No funcionales

- **[R-08]** La acción del técnico para actualizar el estado debe poder hacerse en un solo toque, sin tipear ni desbloquear múltiples pantallas.
  - Tipo: no funcional (usabilidad)
  - Origen: `tecnico.md` · Técnico de campo
  - Evidencia: "Me gustaría tener algo donde yo toco un botón".

- **[R-09]** La notificación al cliente debe llegar por un canal que el cliente ya use habitualmente, sin obligarlo a instalar una app nueva para cada visita.
  - Tipo: no funcional (canal de comunicación)
  - Origen: `tecnico.md`, `gerente_general.md` · Técnico de campo, Gerente general
  - Evidencia: la coordinación actual ya se apoya en WhatsApp ("Me mandan la dirección por WhatsApp la noche anterior", técnico) y en llamadas que no escalan ("no tengo cómo avisarle que me retrasé, a menos que me acuerde de llamar", gerente).

- **[R-10]** El sistema debe funcionar mientras el técnico tiene las manos ocupadas y no puede sostener el teléfono (interacción mínima,看一眼-y-toque, sin tipeo).
  - Tipo: no funcional (usabilidad / contexto de uso)
  - Origen: `tecnico.md` · Técnico de campo
  - Evidencia: "cuando estoy trabajando no puedo estar con el teléfono en la mano".

- **[R-11]** La disponibilidad del sistema debe cubrir el horario laboral completo del negocio, sin caídas en horas pico (final de la mañana, tarde).
  - Tipo: no funcional (disponibilidad)
  - Origen: `gerente_general.md` · Gerente general
  - Evidencia: "recibimos llamadas durante todo el día" y la coordinación ocurre en una franja amplia ("entre las tres y las cinco").

- **[R-12]** El cambio de estado del técnico y la notificación al cliente deben propagarse en pocos minutos, para que la información no llegue cuando el cliente ya se fue.
  - Tipo: no funcional (latencia)
  - Origen: `cliente.md` · Cliente residencial
  - Evidencia: "Una vez estuve esperando desde las tres y llegó a las seis y media sin avisar nada".
