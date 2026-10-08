# ADR-007 — La entrega de un ejemplar a una persona es una asignación con acuse; su papel es el documento de siempre

**Fecha:** 2026-10-07 (corregido el 2026-10-08)
**Estado:** Propuesto (D8 decidida el 2026-10-08: acuse con biometría y escalera de alternativas)
**Decisionario:** Jose Acevedo

---

## Contexto

Jose pide que un operable pueda llevar sus documentos (propiedad, inspección de prevención de
riesgos, revisiones obligatorias) y que el sistema demuestre que a un trabajador se le entregó
su EPI, para una inspección de trabajo. Estricto a operables y dentro del add-on de inventario.

Se valoraron tres formas de modelarlo:

**A — Campos en el ejemplar.** `insuranceExpiresAt`, `lastInspectionAt`, `assignedTo`… Rápido
y pobre: cada tipo de papel es un campo nuevo, no hay fichero, no hay historial, y el acuse
habría que inventarlo.

**B — Un subsistema propio de inventario.** Colección de «papeles del ejemplar» con su fichero
y su acuse, aparte del servicio documental. Duplica lo que ya existe: almacenamiento,
visibilidad por rol, caducidad y acuse de recibo.

**C — Reutilizar el documental y añadir la asignación.** El documento de siempre, colgado del
ejemplar o del artículo (ámbitos nuevos `unit` e `item`, tipos nuevos). Y una entidad nueva,
`unit_assignments`, que es «este ejemplar está en manos de esta persona desde esta fecha», con
el acuse del trabajador dentro, igual que confirma un documento.

## Decisión

**Opción C.**

- **El papel del ejemplar es el documento de siempre.** Tipo, fichero, caducidad y visibilidad
  ya existen; solo cambia de dónde cuelga. Un operable no gana campos: lo que está en regla se
  deriva de sus documentos (como la posición se deriva de la reserva, ADR-006).
- **La entrega es una asignación, no un movimiento de saldo.** Asignar no es consumir
  (ADR-004): el ejemplar sigue siendo de la empresa y vuelve a su almacén base. Queda en el
  libro para que informes y CSV la vean, pero no toca cantidades.
- **El acuse lo da el trabajador, desde la app, con su uid y la hora del servidor.** Quien
  entrega registra; quien recibe confirma o rechaza. Es el mismo gesto con el que ya confirma
  un documento, así que el trabajador no aprende nada nuevo.
- **Se confirma con biometría** (Jose, 2026-10-08): la huella desbloquea una clave del chip
  seguro del móvil que firma un reto del servidor, y el servidor comprueba la firma. Si el
  móvil no tiene biometría, el PIN del móvil; si no tiene bloqueo, la contraseña de la cuenta.
  El registro dice cuál de los tres fue. Sin firma dibujada.
- **Un ejemplar asignado no se ofrece a las tareas.** Está en manos de alguien; su agenda lo
  pinta así.
- **Una revisión caducada no bloquea.** Jose, 2026-10-08: «no puedes bloquear el uso de
  maquinaria arbitrariamente». El ejemplar se pinta en rojo con el hecho escrito y asignarlo
  pide confirmación, que queda registrada. Retirarlo es decisión de una persona.

## Consecuencias

- El servicio documental gana dos ámbitos y siete tipos; el inventario, una colección, su
  espejo, cuatro avisos y un job nocturno que solo avisa de caducidades (no cambia estados).
- La prueba para la inspección es un informe del apartado de Informes, servido por `reports`,
  visible siempre y en rojo cuando el inventario no está habilitado, con la explicación de qué
  es y cómo habilitarlo. El patrón sirve para cualquier informe que dependa de un add-on.
- El ejemplar necesita **ficha propia** en el panel (hoy es una fila de la ficha del artículo):
  documentos con semáforo, asignación actual, historial.
- La prueba para una inspección sale de dos registros, no de uno: el documento (qué papel, de
  cuándo a cuándo, con qué resultado) y la asignación (a quién, cuándo, confirmado cuándo y
  desde dónde). El sistema da la constancia; el valor legal del formato lo pone la normativa de
  cada equipo, no la herramienta.
