# User Stories — tickeSoporte

> Discovery: `discoveries/tickeSoporte`
> Evidencia: `discoveries/tickeSoporte/interviews/`
> Regla: cero invención. Cada historia INVEST cita el archivo de entrevista que la respalda y se vincula a uno o más requisitos de `requisitos.md`.

## Mapa historia ↔ requisito ↔ dolor

| Historia | Requisitos | Dolores que ataca |
|---|---|---|
| US-01 | R-01, R-08, R-10 | cliente-sin-actualizacion, no-poder-atender-telefono |
| US-02 | R-03, R-07, R-12 | retraso-sin-aviso, espera-sin-informacion |
| US-03 | R-02, R-04, R-09 | espera-sin-informacion, ventana-tiempo-amplia |
| US-04 | R-04, R-09 | ventana-tiempo-amplia, no-poder-planificar |
| US-05 | R-05, R-06 | imposible-coordenar-desde-campo, doble-rol-atencion |
| US-06 | R-06, R-09 | doble-rol-atencion |

## Historias

### Núcleo del MVP (lo que se construye primero)

- **[US-01]** Como **técnico de campo**, quiero pulsar un único botón "voy en camino" al terminar el trabajo anterior, para que el cliente del siguiente reciba el aviso sin tener yo que llamar ni redactar nada.
  - Criterios de aceptación:
    - Dado que estoy en un trabajo y el siguiente está agendado, cuando pulso "voy en camino", entonces el sistema registra el evento con la hora actual sin pedirme texto adicional.
    - Dado que pulso "voy en camino", cuando suelto el botón, entonces la confirmación visual cabe en una sola pantalla sin tecleo adicional (un toque o dos como máximo).
    - Dado que estoy con las manos ocupadas, cuando quiero actualizar el estado, entonces no necesito escribir ni desbloquear más de una pantalla.
  - Fuente: `tecnico.md` · Técnico de campo
  - Requisitos: R-01, R-08, R-10

- **[US-02]** Como **técnico de campo**, quiero poder actualizar la hora estimada del siguiente trabajo con un toque cuando me retrase, para avisar al cliente sin tener que llamar yo.
  - Criterios de aceptación:
    - Dado que estoy en un trabajo y me retraso, cuando pulso "se demoró, nueva hora", entonces el sistema permite sumar 30/60/90 minutos a la hora estimada sin tipear.
    - Dado que actualizo la hora estimada, cuando confirmo, entonces el cambio queda registrado y se propaga al cliente en pocos minutos.
  - Fuente: `tecnico.md` · Técnico de campo
  - Requisitos: R-03, R-07, R-12

- **[US-03]** Como **cliente residencial**, quiero recibir un mensaje automático cuando el técnico salga hacia mi casa, para saber que el servicio está en curso y a qué hora estimada llega.
  - Criterios de aceptación:
    - Dado que tengo un trabajo agendado, cuando el técnico pulsa "voy en camino", entonces recibo un mensaje con la hora estimada de llegada por un canal que ya uso (WhatsApp o SMS).
    - Dado que recibo el mensaje, cuando lo abro, entonces dice al menos: nombre del técnico, hora estimada de llegada y nombre del negocio.
  - Fuente: `cliente.md` · Cliente residencial
  - Requisitos: R-02, R-04, R-09

- **[US-04]** Como **cliente residencial**, quiero ver el estado actual de mi trabajo (asignado / en camino / en sitio / finalizado) sin tener que llamar a la empresa, para poder planificar mi día.
  - Criterios de aceptación:
    - Dado que tengo un trabajo agendado, cuando abro el enlace o la vista de estado, entonces veo el estado actual del técnico y la hora estimada de llegada.
    - Dado que el técnico actualiza el estado, cuando refresco, entonces el nuevo estado aparece en pocos minutos sin que yo tenga que llamar.
  - Fuente: `cliente.md` · Cliente residencial
  - Requisitos: R-04, R-09

### Soporte mínimo (sin esto el núcleo no se puede operar)

- **[US-05]** Como **gerente general**, quiero registrar la agenda del día (orden de trabajos, dirección y hora estimada inicial) desde un solo lugar, para no escribir a mano y para que cualquiera que mire vea lo mismo que yo.
  - Criterios de aceptación:
    - Dado que es el inicio del día, cuando cargo los trabajos del día, entonces quedan en una lista con orden, dirección y hora estimada inicial visible para mí y para quien ayude a contestar.
    - Dado que tengo la lista cargada, cuando entro a la herramienta, entonces veo la agenda completa del día en una sola vista.
  - Fuente: `gerente_general.md` · Gerente general
  - Requisitos: R-05, R-06

- **[US-06]** Como **gerente general**, quiero que quien me ayuda a contestar mensajes vea el estado de cada trabajo del día, para no depender solo de mí para contestar.
  - Criterios de aceptación:
    - Dado que hay trabajos cargados en el día, cuando entro al panel, entonces la lista muestra el estado actual de cada trabajo (asignado, en camino, en sitio, finalizado) y se actualiza cuando el técnico lo cambia.
  - Fuente: `gerente_general.md` · Gerente general
  - Requisitos: R-06, R-09

## No funcionales como criterios verificables

Estos NF ya están en `requisitos.md` y se verifican dentro de las historias anteriores; no se duplican como historias separadas para no inflar el MVP.

- **R-08 / R-10** (un toque / manos ocupadas) — se verifica en los criterios de US-01 y US-02.
- **R-09** (canal habitual, sin app nueva obligatoria) — se verifica en el criterio de US-03 y US-06.
- **R-11** (disponibilidad en horario laboral) — se verifica operativamente: el MVP debe estar disponible durante todo el horario del negocio.
- **R-12** (latencia de pocos minutos) — se verifica en los criterios de US-02 y US-04.
