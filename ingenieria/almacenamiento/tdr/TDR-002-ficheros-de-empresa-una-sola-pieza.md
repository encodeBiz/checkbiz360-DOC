# TDR-002 — Ficheros de empresa con una sola pieza: cifrado y enlaces cortos para tareas, firmas y quiosco

**Fecha:** 2026-11-14
**Estado:** Propuesta, pendiente de revisión de Jose ([ADR-004](../adr/ADR-004-ficheros-de-empresa-con-una-sola-pieza-en-shared.md)) · sin código
**Parte de:** [TDR-001](TDR-001-cifrado-de-documentos.md), que sigue igual: lo de hoy no se toca
**Componentes:** `packages/shared` (pieza nueva `secureFiles`), `services/documents` (la cede a
`shared` y sigue sirviendo la descarga), `services/tasks`, `services/inventory`,
`services/reports`, `services/customers`, `services/checkinbiz` (última fase), app `checkbiz360`,
panel `encodebiz-front-saas`, compose de staging y producción

---

## 1. Qué problema resuelve

Dos problemas, del más grave al menos grave:

1. **Enlaces eternos sin sesión en las tareas.** `services/tasks/src/core/shared/firebase/storage.ts:24`
   firma cada subida con `expires: "2050-01-01"`. El enlace se guarda en `resources/{id}.url` y lo
   usan:
   - la app, que lee la subcolección `resources` directamente de Firestore
     (`task_firestore_datasource.dart:256`);
   - el panel, igual (`task.service.ts:144`);
   - el evento `task.resource_uploaded`, en el campo `url` (`services/tasks/src/events/task.ts:150`).

   Quien tenga el enlace (un correo reenviado, una captura, el historial de un navegador) descarga
   el fichero hasta 2050.
2. **Ficheros de empresa en claro fuera del documental.** Las evidencias, los adjuntos (PDF de
   hasta 20 MB), las incidencias y las fotos de valoración de las tareas; la evidencia JSON de las
   firmas; las actas; las fotos del quiosco.

Y una cuestión de diseño, que es lo que pidió Jose: que un cambio de seguridad de los ficheros se
haga **una vez, en `shared`**.

## 2. Qué se cubre, por fases

| Fase | Prefijo | Quién lo escribe | Quién lo lee | Por qué en este orden |
|---|---|---|---|---|
| 0 | — | — | — | Sacar el mecanismo de `documents` a `shared` sin cambiar nada visible |
| 1 | `media/entities/{e}/checkinbiz/tasks/…` (evidencias, `adjuntos/`, `incidencia-…`, `ratings/`) | `tasks` | app, panel, `reports` (fotos del parte), `customers` (ticket → justificante) | Enlaces de 2050 y ficheros que puede subir cualquier empleado |
| 2 | `signatures/evidence/{e}/…` | `shared/signature`, desde `documents` e `inventory` | `reports` (`GET /reports/signatures/evidence`) | Datos personales, pero ya se sirven con sesión |
| 3 | `checkbiz/reports/entities/{e}/…` (actas, exportaciones) | `reports` | panel | Por revisar: no lo he inventariado |
| 4 | `kiosk/…` (bucket del sistema) | `checkinbiz` | panel | Ya usa enlaces de 5 minutos (`shared/storage/privateFiles.ts`); falta el cifrado |

**Fuera:** la marca de la empresa (`media/entities/{e}/{tipo}/…` fuera de `checkinbiz/`), las
campañas y el CRM. Son públicos por naturaleza o no son de ninguna empresa (tabla de
`almacenamiento/README.md`).

## 3. La pieza `secureFiles` en `shared`

Sale de `services/documents/src/application/services/document/`, **sin cambiar el formato
`CBZE v1` ni el token**: lo cifrado hoy se sigue abriendo igual.

| Función | Hace | Hoy está en |
|---|---|---|
| `loadKeyRing()` | carga la llave de `/run/secrets/documents_kek` (`DOCUMENTS_KEK_FILE`) | `DocumentCrypto.loadKeyRing` |
| `writeSecureFile({path, contentType, buffer})` | cifra (si la escritura cifrada está activa) y sube; devuelve `{sizeBytes, sha256}` del contenido en claro | `DocumentStorageService.writeDocumentFile` |
| `readSecureFile(path)` | baja y descifra; un fichero en claro se devuelve tal cual (transición) | `DocumentStorageService.readDocumentFile` |
| `secureFileUrl({entityId, path, filename, minutes})` | emite el enlace corto propio (`/api/v1/documents/files/<token>`) | token de `DocumentCrypto` |
| `verifySecureFileToken(token)` | comprueba firma, caducidad y que la ruta casa con la empresa | idem |
| `recordDownload(…)` | anota quién descargó qué (nuevo) | — |

**El prefijo permitido** deja de ser solo `documents/entities/{e}/`. Pasa a una lista en la propia
pieza, con la misma forma que `RULES` de `storageUsage.ts`: **la empresa siempre en la ruta**, y la
ruta del token tiene que casar con la empresa del token.

**Las variables** se renombran sin romper lo de hoy: `SECURE_FILES_ENCRYPT_WRITES`, con
`DOCUMENTS_ENCRYPT_WRITES` como alias mientras convivan. La llave sigue en el mismo fichero de
secreto y con el mismo `kekId`. **No hay llave nueva.**

**El script** `encrypt-existing` pasa a `shared` o queda en `documents` con un `--prefix` por fase.
Sigue con `--inventory`, simulación por defecto y `--apply` / `--reverse`. En staging se lanza
**solo en las empresas de prueba** (SaludStart, Cuidama, Encodebiz y Fonteluz) salvo que Jose diga
otra cosa.

**Cabecera del módulo:** *«Si cambias esto, redespliega todos los servicios que lo usan: hoy
documents, tasks, inventory y reports. Un formato nuevo se despliega primero para leer y después
para escribir.»*

## 4. La descarga: una sola puerta

La ruta pública sigue siendo la de `documents`: `GET /api/v1/documents/files/<token>`.

- Cada módulo **comprueba sus permisos** y luego llama a `secureFileUrl(…)`. `documents` no sabe
  de tareas: solo verifica el token, descifra y entrega.
- Caducidad: la de hoy para documentos. Para fotos que se ven en una lista (miniaturas), un poco
  más larga, para no pedir un enlace por cada desplazamiento. **A decidir** (§8).
- Cabeceras: `Cache-Control: private, no-store`, como hoy.

## 5. Fase 1, tareas

**Servidor (`tasks`):**

- `uploadTaskFile` deja de firmar a 2050. Guarda con `writeSecureFile` y no escribe ningún `url`
  nuevo en `resources`. Mientras haya apps viejas, `url` se rellena con un enlace propio
  **largo**, pero caducable y revocable. Se decide en §8.
- Ruta nueva: `GET /tasks/:taskId/resources/:resourceId/url` → `{url}`, con los mismos permisos que
  ver la tarea (`canOperateAssignedTask` o gestor de la sucursal). Opcional: devolver el enlace ya
  dentro del detalle de la tarea, si la app lo pide por API.
- Igual para incidencias (`taskIncident.controller.ts:127`) y valoraciones
  (`rateTaskWorker.controller.ts:53`).
- El evento `task.resource_uploaded` lleva `resource_id`, no `url`. Antes hay que mirar quién lo
  consume: los webhooks de clientes, Rentman y el motor de eventos.
- **Los duplicados de tarea** comparten el fichero de `adjuntos/` (TDR-007): el enlace se pide por
  el recurso de cada tarea, así que no cambia nada.

**Otros lectores:**

- `reports`, `TaskEvidencePhotos.ts` (fotos en el parte del cliente): lee con `readSecureFile`, ya
  tiene la llave.
- `customers`, `FirestoreExpenseReceipts.copyFile` (ticket → justificante): hoy baja el ticket
  «en claro» del bucket (comentario de la línea 31). Pasa a `readSecureFile`. Si `customers` no
  tiene la llave, se lo pide a `documents`, como ya hace con el justificante.

**App y panel:** al abrir un recurso, piden el enlace a la API en vez de usar `resource.url`. Con
caché en memoria hasta que caduque.

**Orden, sin romper móviles con la versión vieja:**

1. Servidor: la ruta nueva y la lectura con `readSecureFile`, **sin cifrar todavía**. La
   escritura sigue en claro.
2. Panel y app usan la ruta nueva. Se publica la app.
3. La versión nueva pasa a obligatoria (`app_config/global`).
4. Se cifra lo nuevo (`ENCRYPT_WRITES` en `tasks`).
5. Se cifra lo existente con el script, empresa por empresa. **Aquí mueren los enlaces de 2050.**

Si se cifra antes del paso 3, las fotos dejan de verse en las apps viejas.

## 6. Fase 2, evidencia de las firmas

`SignatureEvidence.ts:44` escribe `signatures/evidence/{e}/{purpose}/{challengeId}.json` desde el
proceso que verifica (`documents` para documentos, `inventory` para EPI). Pasa a `writeSecureFile`.
`reports` la lee con `readSecureFile` para el perito.

`inventory` necesita la llave montada.

## 7. Fases 3 y 4, actas y quiosco

- **Actas y exportaciones (`reports`):** por inventariar antes de diseñar.
- **Quiosco (`checkinbiz`):** ya sirve con enlaces de 5 minutos (`privateFiles.ts`), y las fotos
  caducan por las reglas de retención. Cifrar es poner `writeSecureFile` y `readSecureFile` en el
  mismo flujo. Está en otro bucket (el del sistema): la lista de prefijos de la pieza tiene que
  admitir el bucket.

## 8. A decidir en la revisión

1. **El `url` de las apps viejas** durante la transición de la fase 1:
   - **a)** seguir firmando a 2050 hasta que la versión nueva sea obligatoria, y entonces cortar;
   - **b)** enlace propio de 30 días desde ya;
   - **c)** dejar `url` vacío y aceptar que en la app vieja no se vean.

   Recomiendo **a)**: no rompe nada y el corte llega en el paso 5 igualmente.
2. **La caducidad de las miniaturas.** Recomiendo 1 hora para fotos de tareas en lista y la de hoy
   para descargas.
3. **`customers` y `merlin`:** que sigan pidiéndoselo a `documents` (como hoy) o pasen a la pieza con
   la llave montada. Recomiendo dejarlos como están: funcionan y no ganan nada.
4. **Registro de descargas:** dónde se guarda (Postgres, como el resto del espejo) y cuánto tiempo.

## 9. Pruebas

- **Unitarias:** las de TDR-001 §9 pasan con la pieza en `shared` sin tocar los resultados; prefijos
  nuevos permitidos y rechazados; token con ruta de otra empresa → rechazo.
- **Staging, solo en las empresas de prueba:**
  - subir foto, PDF, incidencia y valoración: en el bucket empiezan por `CBZE`;
  - verlos en panel y app nueva;
  - la app vieja sigue viéndolos mientras no se cifre lo existente;
  - el parte del cliente sale con fotos;
  - el ticket pasa a justificante;
  - un enlace de 2050 anterior descarga algo ilegible después del script.
- **QA:** `55-tareas-adjuntos.spec.ts` y las de incidencia y valoración, adaptadas como FIR-04-04
  (la URL ya no es de Google).

## 10. Antes de producción

- La fase 0 no necesita nada: es mover código.
- La fase 1 depende de que la app nueva esté publicada y obligatoria.
- La llave de producción es la misma de TDR-001 (`prod2026a`). Se monta como secreto en `tasks`,
  `inventory` y `reports`, con el mismo `touch` previo del fichero (TDR-001 §11, pase §71).
- Va después del pase §71 (documentos en prod), no antes: primero se prueba en producción el
  mecanismo con un solo servicio.
