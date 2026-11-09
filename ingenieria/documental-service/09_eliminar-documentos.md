# 09 · Eliminar documentos (y liberar el espacio)

**Abierto:** 2026-11-07 · **Estado:** construido y EN STAGING el 07-nov (API `bd3388a`, panel `e893995d`); prod pendiente, pase §46.
**De dónde sale:** Jose, 07-nov: «nosotros cobramos por espacio pero no dejamos a los clientes
liberar; hay que poder eliminar documentos con sus avisos correspondientes».

## El hueco

La papelera del documental solo **archiva** (`DELETE /documents/:id` → `status: "archived"`): el
documento sale de la vista, pero el fichero sigue en el bucket y sigue contando en el
almacenamiento que se cobra por encima de 2 GB (almacenamiento, ADR-002). El contador ya resta
solo cuando un objeto desaparece del bucket (`storageUsageDeleted`); lo que falta es que el
documental lo saque. El diseño del almacenamiento ya decía «lo que sube un administrador lo borra
un administrador», pero nunca se construyó.

## Decisiones de Jose (2026-11-07)

1. **Dos acciones.** *Archivar* se queda como está: lo quita de la vista y conserva el fichero.
   *Eliminar* es nueva: borra los ficheros y libera el espacio en el acto.
2. **Se borra todo**: el fichero, el original si se firmó dentro del PDF, el PDF firmado y la
   evidencia de cada acuse, y **el acta de firma**.
3. **El registro se queda.** El documento sigue en Firestore con `status: "deleted"`, quién,
   cuándo y por qué, más su nombre, tipo, tamaño y huella (SHA-256); los acuses y la actividad
   tampoco se borran. «Así si nos reclaman tenemos pruebas»: de que existió, de qué contenido era
   (la huella casa con cualquier copia que conserve la empresa), de quién lo recibió o lo firmó y
   cuándo, y de quién lo eliminó.
4. **Avisos según lo que se borra** (avisar, no impedir):
   - normal: «Se eliminará para siempre y liberarás 3,2 MB»;
   - con acuse o firma, o la hoja informativa: en rojo, con quién lo firmó y cuándo, y que solo
     quedará el registro, sin documento ni acta; hay que marcar una casilla para seguir;
   - nóminas y contratos: en rojo, que la ley puede obligar a conservarlos. Tampoco se bloquea.
5. **Solo owner y admin.** Los gestores siguen archivando.
6. **Varios a la vez** desde la lista (selección), para liberar espacio de una vez.

## Lo que se borra y lo que se queda

| Se borra del bucket | Se queda en Firestore |
|---|---|
| `storagePath` (el fichero, o el firmado si se firmó dentro) | el documento con `status: "deleted"`, `deletedAt`, `deletedBy`, `deleteReason`, `deletedFiles` (cuántos) y `freedBytes` |
| `signed.originalStoragePath` | `filename`, `type`, `sizeBytes`, `contentSha256`, `signed` (sin fichero) |
| de cada acuse, `signedFile.path` y `signature.evidence.path` | los acuses: quién, cuándo, cómo, versión, huellas |
| el acta de cada firma (`checkbiz/reports/entities/{e}/actas/…/acta_{challengeId}.pdf`) | la actividad, con una entrada `deleted` |

Un fichero que no existe ya no es un error: se cuenta como borrado. Si alguno falla, el
documento **no** pasa a `deleted` y la respuesta lo dice: se puede reintentar, y lo ya borrado
no se cuenta dos veces (el contador es idempotente por objeto). El bucket conserva lo borrado 7
días (borrado blando de Google): es nuestra red ante un error, no se ofrece al cliente.

## Cómo se comporta un documento eliminado

- **Owner y admin** lo ven en la lista (ya ven todos los estados) con la etiqueta «Eliminado», y
  su ficha enseña el registro: sin descarga, sin editar, sin archivar.
- **El trabajador** no lo ve: la app solo recibe documentos activos.
- **Descargar** responde 410 (`documents/deleted`); acusar o firmar, 409.
- **Hoja informativa:** si el eliminado es la hoja que tiene la ficha del empleado, se quita el
  resumen (`dataProtectionNotice`); la alerta `notice_unsigned` vuelve a contarle, porque ya no
  hay prueba.
- **Inventario y cartera:** un documento eliminado deja de contar como cualquier archivado (se
  revisan los filtros `!== "archived"`, que lo darían por vigente).
- **Índice de búsqueda:** fuera, como al archivar.
- **Evento** `document.deleted` en el catálogo de eventos, como `document.archived`.

## API

- `POST /documents/:documentId/delete` `{entityId, reason?}` → `{ok, freedBytes, deletedFiles}`.
  404 si no existe, 403 si no es owner/admin, 409 si ya está eliminado.
- `POST /documents/delete` `{entityId, documentIds[≤50], reason?}` → por documento, `deleted` o
  el motivo por el que no; uno que falla no para a los demás.
- `GET /documents/:documentId/delete-preview?entityId` → lo que necesita el aviso: tamaño total
  de lo que se borra, quién acusó o firmó y cuándo, y si el tipo es de los que la ley puede pedir
  conservar. Así el panel no cruza acuses.

`DELETE /documents/:id` sigue siendo archivar: cambiarle el sentido rompería la app.

## Panel

- En la ficha del documento, junto a *Archivar*, **Eliminar** (solo owner/admin), con el modal de
  avisos de arriba y un motivo opcional.
- En la lista, selección múltiple y *Eliminar seleccionados*, con un modal que resume cuántos,
  cuánto espacio se libera y cuántos tienen firma o son nóminas o contratos.
- Estado «Eliminado» en el filtro y en la etiqueta.

## Fuera de alcance

Restaurar un eliminado; caducidad automática de documentos; borrar adjuntos de tareas (ya tienen
su propio borrado con recuento de referencias).
