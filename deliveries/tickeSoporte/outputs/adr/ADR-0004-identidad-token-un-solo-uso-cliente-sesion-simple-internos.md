# ADR-0004 · Identidad y autenticación: token de un solo uso en URL para el cliente; sesión simple (email + password) para técnico y gerente
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

- **US-04** exige "vista de estado del trabajo para el cliente, vía
  enlace, sin app nueva obligatoria". Su nota de refinamiento precisa:
  "acceso por token de un solo uso enviado en el mismo mensaje de US-03,
  sin login ni contraseña. El token caduca al finalizar el trabajo."
- **US-06** exige que el gerente (y quien le ayude a contestar) vea la
  agenda y el estado de cada trabajo. R-09 dice "canal que el cliente
  ya usa", que para el gerente se traduce en "celular y computador".
- **Fuera de alcance del MVP** ("multi-técnico simultáneo") implica que el
  número de usuarios internos del sistema es muy pequeño: 1–2 personas.
- **R-08 / R-10** aplican al técnico: en el MVP, el técnico es el gerente
  mismo o un técnico secuencial; la fricción de un login con password
  tecleado en campo es tolerable solo si es la **mínima posible**.

La fuerza que obliga a decidir es: cómo se identifica a cada actor sin
convertir la autenticación en un subproducto del MVP.

## Decisión

Se establecen **dos mecanismos de identidad, distintos por audiencia**:

1. **Cliente (`/cliente/<token>`)** — **token de un solo uso incluido en
   la URL**. El token se genera cuando el técnico marca "voy en camino"
   (US-01) o cuando se agenda el trabajo, y se incrusta en el enlace que
   el WhatsApp envía al cliente (US-03). Características:
   - Longitud: 32 caracteres alfanuméricos (suficiente para no ser
     adivinable por el espacio de búsqueda de un solo trabajo).
   - Caducidad: cuando el trabajo pasa a `finalizado` (estado terminal
     definido en la nota de refinamiento de US-04) o, como máximo, 24 h
     después de la hora estimada inicial (lo que ocurra primero).
   - Un solo uso **lógico** (no rotado por GET): si el cliente abre el
     enlace varias veces, sigue funcionando hasta la caducidad, porque
     "ver el estado" es idempotente. La nota de refinamiento de US-04
     dice "sin login ni contraseña", que es lo que esto implementa.
   - Se transmite por HTTPS y nunca se loggea en claro fuera del
     registro del trabajo.

2. **Técnico y gerente (`/tecnico`, `/gerente`)** — **sesión por email +
   password**, administrada por el backend (cookie de sesión httpOnly).
   - En el MVP, las cuentas son creadas por el gerente (dueño) antes de
     habilitar al técnico; no hay self-service de registro público.
   - Password con hash (bcrypt/argon2, decisión de implementación, no
     arquitectónica).
   - Sesión con expiración de 12 h (cubre el horario laboral de R-11
     sin renovaciones constantes) y logout explícito.

## Alternativas consideradas

- **Token de un solo uso también para el técnico** — la nota de
  refinamiento de US-01 pide que el técnico pulse con manos ocupadas;
  un enlace con token en URL cada vez sería inviable en campo. La sesión
  persistente (login una vez al día) es el mínimo fricción.
- **OAuth / login social para el cliente** — introduce un proveedor
  externo y rompe R-09 ("sin obligarlo a instalar una app nueva" se
  interpreta como "sin pedirle un paso de login nuevo"). Un token en
  el enlace del WhatsApp es la fricción mínima.
- **Magic link por email para técnico/gerente** — más simple
  operacionalmente (sin password que guardar), pero requiere acceso a
  email en campo. La evidencia dice que el técnico coordina por
  WhatsApp, no por email; reintroducir email en el flujo diario es
  fricción evitable.
- **Sin autenticación para el gerente** — descartado porque US-06 dice
  "el panel debe ser accesible... desde el celular del gerente y desde
  un computador de quien le ayude a contestar mensajes". Sin auth,
  cualquiera con la URL ve la agenda, lo que expone datos del cliente
  (dirección, hora estimada) y choca con el sentido común de
  confidencialidad comercial (no está explícito en el inbox, pero es
  defecto de la industria y se alinea con R-11 de "disponibilidad
  robusta").

## Consecuencias

- **Ganamos:** el cliente entra al estado de su trabajo con cero
  fricción (un toque en el enlace del WhatsApp). El técnico y el
  gerente mantienen sesión todo el día y solo pulsan, que es
  exactamente lo que R-08 / R-10 exigen. La confidencialidad básica
  de la agenda queda cubierta con email + password.
- **Costo que aceptamos:** dos mecanismos de identidad que mantener.
  Es un costo bajo: el del cliente es un campo más en la tabla de
  trabajos y un endpoint de validación de token; el de internos es
  un módulo estándar de auth.
- **Decisión deliberadamente diferida:** rotación de token por GET,
  revocación inmediata, y rate limiting por IP son detalles de
  implementación, no de arquitectura; se documentan en la
  historia US-04 y se refinana en el sprint planning. Se declara
  como `open_question` solo lo que dependa de un proveedor externo
  (p. ej. enviar el magic link de recuperación de password para el
  gerente — el MVP asume que el gerente puede pedir un reset al
  operador del sistema).
