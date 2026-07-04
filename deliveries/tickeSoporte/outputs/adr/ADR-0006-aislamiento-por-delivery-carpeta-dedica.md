# ADR-0006 · Aislamiento por delivery: cada delivery vive en su propia carpeta, sin compartir base ni archivos en runtime
**Estado:** aceptado
**Fecha:** 2026-07-01

## Contexto y fuerza

La constitución del proyecto (`CLAUDE.md`, regla 5) establece: "Aislamiento.
Cada delivery vive en su carpeta bajo `deliveries/<nombre>/`. Nunca mezcles
datos entre deliveries." El delivery actual es `deliveries/tickeSoporte/`.

Esta restricción no es una decisión técnica del **producto** que se
construye, sino una decisión técnica del **proyecto** que lo contiene.
Aun así, tiene implicaciones arquitectónicas para el MVP (dónde vive la
base de datos, qué nombres de variables de entorno se usan, qué puertos).

La fuerza que obliga a decidir es: si el MVP se lleva a producción o se
despliega en un entorno compartido, ¿cómo se evita contaminar otros
deliveries del mismo repositorio (o un futuro segundo cliente)?

## Decisión

Se aplican las siguientes reglas de aislamiento, en línea con la
constitución:

1. **Ruta dedicada:** todo el código, configuración y datos del MVP
   vive bajo `deliveries/tickeSoporte/`. La raíz del repositorio no
   contiene código de aplicación que no sea el andamiaje del equipo
   (`/.claude/`, `CLAUDE.md`, `scripts/`).
2. **Prefijo de nombres:** los recursos nombrados (tabla, bucket, cola,
   variable de entorno, subdominio) llevan el prefijo `tickesoporte-`
   (kebab-case del nombre del delivery). Esto evita colisiones si en
   el futuro se monta un segundo delivery en el mismo entorno.
3. **Base de datos propia:** el MVP usa su propia base de datos (o su
   propio schema dedicado). No se comparte una base con otros
   deliveries.
4. **Sin código compartido entre deliveries:** si una pieza (p. ej. la
   clase `NotificationChannel` de ADR-0001) fuera útil para un
   segundo delivery, se promueve a `lib/` o a un paquete del
   repositorio **después** de que aparezca la segunda necesidad. En
   el MVP, todo vive dentro de `deliveries/tickeSoporte/` aunque sea
   código duplicable.

## Alternativas consideradas

- **Reutilización preventiva (extraer a `lib/` desde el día 1)** —
  sobre-diseño. El equipo no tiene un segundo delivery; extraer
  "por si acaso" viola la regla "maximiza el trabajo no hecho" del
  Architect. Se prefiere duplicar y promover cuando haya evidencia
  de la segunda necesidad.
- **Monorepo con un solo `package.json` raíz** — tentador para
  compartir dependencias, pero confunde el aislamiento por
  delivery y complica el gate (`dor-invest-gate.py`) que valida
  artefactos por carpeta. No aporta valor al MVP.

## Consecuencias

- **Ganamos:** cero acoplamiento accidental entre deliveries. La
  regla 5 de la constitución se aplica de forma automática por
  convención de carpetas y prefijos, no por disciplina. Si el
  equipo monta un segundo delivery, no hay riesgo de pisar datos.
- **Costo que aceptamos:** si en el futuro hay un segundo
  delivery con código similar, habrá una refactorización
  explícita para extraer la parte común. Es un costo
  **futuro** y opt-in, no presente.
- **No bloquea el MVP:** ninguna decisión de US-01…US-06 depende
  de cómo se organice el código entre deliveries; el aislamiento
  es transversal.
