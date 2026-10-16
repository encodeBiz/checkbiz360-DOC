# Alta de plantilla y sucursales por Excel — Documento de Ingeniería

**Proyecto:** encodebiz-api · encodebiz-front-saas
**Dominio:** `services/employees` (la importación) · `services/branches` (puerta delegada) · panel, listas de empleados y sucursales
**Fecha de inicio:** 2026-10-16
**Estado:** Fase 1 (plantilla y panel) y fase 2 (el asistente) hechas el 2026-10-16; API en staging, panel en develop
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Montar un cliente es la parte donde más se cae la gente: hay que crear sus sucursales y su
plantilla una a una, con su dirección, su correo y su responsabilidad en cada centro. Hoy eso
son horas, o una llamada en la que alguien de encodeBiz pasa a mano el Excel que mandó la
gestoría ([puesta en marcha](../puesta-en-marcha/README.md)). El seed de la puesta en marcha ya
sabe hacerlo, pero sólo lo usa nuestro equipo.

Lo que se decide aquí es que **el propio cliente** dé de alta sus sucursales y su gente de una
vez con una plantilla Excel, como ya hace con el material de un almacén
([inventario TDR-007](../inventario/tdr/TDR-007-importacion-masiva-por-plantilla.md)) y con el
cuadrante de una sucursal ([cuadrantes TDR-001](../cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md)).
Y que después el conector de asistentes entre por el mismo lote
([conector-asistente](../conector-asistente/README.md)): el cliente le pasa a su IA el Excel de la
gestoría, con sus columnas y su desorden, y la IA lo propone en las filas de la plantilla.

## Principio de diseño

> **Subir no escribe nada: primero enseña, después aplica. Y cada fila pasa por las mismas
> reglas que el alta a mano en el panel, sin camino especial.**

## Decisiones

**D1. Un solo fichero con dos pestañas: Sucursales y Empleados.** Las sucursales van primero
porque las personas se asignan a ellas; una persona puede ir a una sucursal del propio fichero
o a una que ya existe. Se baja y se sube igual desde la lista de empleados que desde la de
sucursales.

**D2. Cada fila por las reglas del alta a mano.** La sucursal se crea por la ruta de
`branches`, con su validación, su índice y su evento, a través de la puerta delegada
(conector-asistente ADR-005). La persona y su responsabilidad, por las mismas funciones que
usan las rutas de `employees`, que se sacan de los controladores a la capa de aplicación para
que la importación las comparta.

**D3. La bienvenida no se manda al importar** (Jose, 2026-10-16: se tomó la recomendación). La
persona nace activa, con su acceso creado, pero sin correo. El resultado de la importación
ofrece **«Enviar bienvenidas»** a las personas que se acaban de crear, y el cliente lo pulsa
cuando ha revisado que todo está bien. Así no salen doscientos correos con contraseña a mitad
del montaje (puesta en marcha 07, problema 1).

**D4. No hay cupo** (Jose, 2026-10-16: «no hay cupo»). El plan nunca para una operación; si
el cliente se pasa, se le cobra. La importación no calcula plazas ni deja filas fuera. Y como
cada fila pasa por las reglas del alta a mano (D2), **el alta a mano tampoco bloquea ya por
cupo**: `canCreateEmployee` y `canCreateBranch` sólo exigen que la empresa tenga suscripción,
que no es un cupo. Era la pieza pendiente de la regla general (sin `409`/`403` por cupo). El
tope de diez empleados que el panel aplica en el plan gratuito es del panel y se decide aparte.

**D5. La factura se dice antes del botón.** Las personas nuevas nacen activas y cuentan en la
facturación por uso. La propuesta dice cuántas personas se añaden.

**D6. Nada se duplica: se reconoce por clave natural.** La sucursal, por su nombre normalizado
(el `normalizeText` del buscador); la persona, por su correo. Una sucursal que ya existe se usa
tal cual y no se modifica. Una persona que ya existe tampoco se modifica, pero **se le añaden las
sucursales nuevas** del fichero: es lo que hace falta para «Marta ahora también trabaja en
Getafe». Una persona dada de baja con ese correo es un error de su fila: se reactiva desde su
ficha.

**D7. La dirección se geocodifica al proponer y se enseña la precisión.** Una dirección que
sólo se resuelve a una ciudad o a medias es un error de la fila, como en el seed: la valla del
fichaje quedaría en mitad de un polígono. Lo resuelto se guarda en el lote y no se vuelve a
geocodificar al aplicar.

**D8. Sólo propietario y administración.** Es el mismo permiso que el alta a mano (`canWrite`).

## Fases

1. **La plantilla y el panel** ([TDR-001](./tdr/TDR-001-plantilla-lote-y-panel.md)). Bajar, subir,
   propuesta, confirmar en segundo plano, resultado y «Enviar bienvenidas». Botón «Importar» en
   las listas de empleados y de sucursales.
2. **El asistente.** Las mismas filas por el conector: el lote desde filas, como el cuadrante
   (conector-asistente ADR-004), con las herramientas de proponer, ver, confirmar y enviar
   bienvenidas. **Hecha el 2026-10-16** a petición de Jose («era la guinda del pastel»):
   `POST /import/rows` y `GET /import/:id/excel` en `employees` (también por la puerta delegada) y
   las herramientas `proponer_alta_masiva`, `ver_alta_masiva`, `confirmar_alta_masiva`,
   `descartar_alta_masiva` y `enviar_bienvenidas`. Además, altas sueltas: `crear_empleado` y
   `crear_sucursal`. QA ALT-06 contra staging.
3. **Editar y cambiar estados por el asistente.** Editar a una persona, cambiar su estado,
   despedirla —que es una baja blanda y deja huérfanas sus tareas futuras: la vista previa las
   lista y ofrece reasignarlas—, y vacaciones o bajas como ausencias del calendario.
4. **El manual del cliente**, en sus idiomas.

## Fuera de la primera versión

- Actualizar los datos de una persona o una sucursal que ya existe (correo, teléfono, dirección).
- Reactivar personas dadas de baja.
- Equipos y responsabilidades distintas de trabajador, supervisor y gerente.
- El horario de cada sucursal: va por su calendario o por el cuadrante.
