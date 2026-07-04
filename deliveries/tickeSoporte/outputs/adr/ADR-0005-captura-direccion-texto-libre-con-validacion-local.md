# ADR-0005 · Captura de dirección del trabajo (US-05): texto libre con validación local, sin geocodificación externa en el MVP
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

- **US-05** dice: "registrar la agenda del día (orden de trabajos,
  dirección y hora estimada inicial) desde un solo lugar". Su nota de
  refinamiento precisa: "La captura de dirección puede ser texto libre,
  autocompletado, o pegado desde WhatsApp — el requisito R-05 no precisa
  mecanismo; la decisión de UX/geocodificación queda al Architect."
- **R-05** exige "sin escribir a mano como en la agenda en papel" (es
  decir, sin re-tipear lo que el gerente ya tiene en un mensaje de
  WhatsApp la noche anterior), pero **no** exige geocodificación ni
  validación de dirección.
- El PO delegó explícitamente esta decisión al Architect
  (`epics.md` · open questions: "Cómo se captura la dirección del
  trabajo en US-05 (texto libre, geocodificación, autocompletado)").

La fuerza que obliga a decidir es: ¿se añade una dependencia externa
(API de geocodificación) para validar o normalizar la dirección, o se
mantiene texto libre?

## Decisión

Se adopta **texto libre con validación local** en el formulario de la
agenda (`/gerente`, US-05):

- Un campo de texto donde el gerente pega la dirección tal cual la
  recibe por WhatsApp, o la escribe una vez. Sin integración con
  Google Maps / OpenStreetMap / Nominatim en el MVP.
- **Validación local mínima:** no vacío, longitud máxima (p. ej. 200
  caracteres), trimming de espacios. La dirección tal cual se guarda
  en la base de datos y se muestra al técnico (US-05) y, si la historia
  lo pidiera, al cliente. Como US-04 no incluye la dirección en la
  vista del cliente, **no hay geocodificación ni reverse-geocoding
  necesarios para servir la vista pública**.
- **Reuso desde WhatsApp** soportado por UX (botón "pegar" en móvil),
  que es lo que pedía la nota de refinamiento de US-05 ("pegado desde
  WhatsApp") y satisface el "sin escribir a mano" de R-05 sin
  añadir proveedor externo.

## Alternativas consideradas

- **Autocompletado con Google Places / Mapbox** — reduce errores de
  tipeo y normaliza la dirección, pero (a) añade un proveedor externo
  con costo por request, (b) requiere API key y conectividad del
  gerente al cargar la agenda, (c) la dirección del técnico no se
  usa para navegar en el MVP (no hay integración con Google Maps del
  técnico — eso está fuera de alcance). Beneficio marginal para 6
  historias y 24 pts.
- **Geocodificación silenciosa al guardar** — útil solo si la vista
  del cliente o el técnico necesitaran coordenadas, lo cual no ocurre
  en el MVP. Añade latencia y un punto de falla por cada trabajo
  cargado. La nota de refinamiento de US-05 ya advierte: "la
  persistencia histórica y la consulta de días anteriores NO entran
  en esta historia".
- **Validación contra un catálogo de ciudades/localidades** — útil
  en negocios que cubren una zona amplia, pero la evidencia muestra
  un solo negocio local con direcciones residenciales; un campo
  de texto libre con UX de "pegar" es suficiente.

## Consecuencias

- **Ganamos:** cero dependencias externas nuevas. La agenda se carga
  rápido, offline-tolerant, y el gerente usa el texto que ya tiene
  en WhatsApp. R-05 se cumple sin proveedor extra. La dirección
  almacenada es exactamente la que el cliente conoce, lo que reduce
  fricción cuando el técnico la lee en campo.
- **Costo que aceptamos:** la dirección puede tener erratas, abreviaturas
  locales o variantes ("Calle 50 # 30-20" vs "Cl 50 30 20"). Esto es
  aceptable porque la dirección no se usa para navegación en el MVP
  y porque el técnico ya trabaja en la zona y reconoce la dirección.
- **Decisión deliberadamente diferida:** añadir autocompletado o
  geocodificación se trata como `open_question` (mejora post-MVP)
  por si el negocio crece a una zona donde las erratas empiezan a
  costar llegadas tarde. No es ADR aceptado en el MVP.
