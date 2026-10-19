# Paso 2a — Cada sesión ve sólo las entidades de las que es miembro

**Proyecto:** encodebiz-api (`firestore.rules`, `firebase_sdk`, `shared`)
**Fecha:** 2026-10-19
**Estado:** **en producción desde el 2026-10-19** (Firestore 17:05, Storage 17:07 UTC); registro en [proximo-pase-back §10](../../deployment-prod/proximo-pase-back.md). `main` aún sin los ficheros
**Antecede:** [README.md](README.md), paso 1 (en producción desde el 2026-10-17) y diseño del paso 2
**Autor:** Jose Acevedo

---

## Por qué va antes que el resto del paso 2

El paso 1 cerró la lectura sin sesión, pero **cualquier sesión lee y escribe cualquier
entidad**, y el registro del panel gratuito está abierto: darse de alta y leer la plantilla,
los DNI y los fichajes de todos los clientes son dos minutos. Casi todo lo sensible cuelga de
`entities/{e}/…`, así que aislar ese árbol cubre la mayor parte del riesgo con una fracción del
trabajo del paso 2 completo. Las colecciones de la raíz quedan para el 2b.

## Qué cambia con respecto al diseño del paso 2

El diseño original resolvía al empleado con un claim `ent` en el token. **Se descarta.** La app
(1.7.0 y 1.8.0, mismo código de Firestore) pide el token con `getIdToken(true)` *antes* de
`/auth/login` y no lo refresca después. Un claim puesto en el login no llega a Firestore hasta
la renovación horaria: un empleado recién dado de alta, o el primer día tras el despliegue,
estaría hasta una hora sin poder leer su ficha ni fichar. Arreglarlo exige publicar app.

En su lugar, una **colección espejo de pertenencia** que lee la regla con `exists()`:

```
entity_members/{uid}_{entityId}   { uid, entityId, employeeIds: [...], updatedAt }
```

- Existe si y sólo si hay en `entities/{entityId}/employees` al menos una ficha con ese `uid` y
  `status != 'fired'`.
- La mantiene un trigger nuevo, `onWriteEmployeeMember` en el código y `onEmpMember` en GCP (`onDocumentWritten` sobre
  `entities/{entityId}/employees/{employeeId}`). En cada escritura **recalcula desde la fuente**
  (consulta las fichas de ese `uid` en esa entidad) para el `uid` de antes y el de después. No
  suma ni resta: recalcular es idempotente y aguanta reintentos, desórdenes y fichas duplicadas
  (una recontratación deja una ficha `fired` y otra activa con el mismo `uid`).
- Sólo servidor: entra en `cerradas()`.
- **Por qué un trigger y no el repositorio de `shared`:** las fichas se escriben por muchos
  caminos (alta de `shared`, `onCreateEmployee`, importaciones, sembrado de Merlin, la app
  escribiendo `language`, la consola). Un espejo que se salta un camino deja a una persona sin
  fichar, en silencio. ADR-006 reserva `firebase_sdk` a escrituras de Firestore que el
  contenedor no ve; aquí el índice deriva del estado de Firestore, venga de donde venga.
- **Reconciliación:** script `reconcile-entity-members` (simula por defecto, `--apply` para
  escribir) que recorre las fichas con `uid` y deja el espejo exacto: crea lo que falta y borra
  lo que sobra. Es el relleno inicial y la red si el trigger falla.

Propietarios y administradores **no** van por el espejo: su asiento ya tiene el id
`{userId}_{entityId}` (`checkinbiz/FirestoreEntityMembershipRepository`, mismo formato que las
Cloud Functions de siempre), y la regla lo lee directamente. Así el dueño que acaba de crear su
empresa la ve al instante, sin esperar a un trigger.

## Las reglas

```
function miembro(e) {
  return conSesion() && (
    exists(/databases/$(database)/documents/entity_members/$(request.auth.uid + '_' + e))
    || asientoVigente(e)
  );
}

// `invited` cuenta: el panel lee la entidad para enseñar la invitación antes de aceptarla.
// Un asiento sin `status` es anterior al campo y era activo (mismo criterio que canWrite).
function asientoVigente(e) {
  let ruta = /databases/$(database)/documents/user_entity_roles/$(request.auth.uid + '_' + e);
  return exists(ruta) && get(ruta).data.get('status', 'active') != 'disabled';
}
```

- **Comodín general:** si la raíz es `entities`, leer y escribir piden además
  `miembro(<primer tramo de la ruta>)`. El resto de raíces sigue como en el paso 1.
- **Consultas de grupo:** la regla genérica `/{path=**}/{sub}/{document}` se **sustituye** por
  dos con nombre. No es estilo: las reglas se suman con OR y la genérica también casa con las
  lecturas directas (`entities/B/employees/x` casa con `path = entities/B`), así que dejarla
  anularía el aislamiento entero.
  - `{path=**}/employees/{id}`: `resource.data.uid == request.auth.uid ||
    miembro(resource.data.entityId)`. Es la consulta de la app (`where uid == uid`).
  - `{path=**}/calendar/{id}`: `miembro(resource.data.entityId)`. Es la de presets del panel
    (`where type == preset && entityId == e`).
  Ninguna otra consulta de grupo existe en panel, app ni quiosco (inventario del 2026-10-19).
- **`user_entity_roles`:** hoy cualquier sesión puede crear `miuid_entidadAjena`, y con este
  paso eso sería la llave de la entidad. Desde el cliente: ni crear ni borrar; actualizar sólo el
  propio asiento (`resource.data.userId == uid`), sólo `status`, `isActive` y `updatedAt`, y
  `status` sólo se queda igual o pasa de `invited` a `active`. Es exactamente lo que hacen
  `updateAuth` y `saveStateCurrentEntity` del panel; las altas, bajas y cambios de rol ya van
  por el backend. La lectura de la colección queda para el 2b.

Coste: hasta dos lecturas de documento por evaluación (el espejo y el asiento), cacheadas dentro
de la petición. En una consulta de lista se evalúa una vez, no por documento.

## Qué no cubre (2b)

Siguen abiertas a cualquier sesión las raíces: `users`, `issues` (el panel tiene un listener
sobre la colección entera), `searchIndex`, `in_app_notifications`, `notification_tokens`,
patrones, `ai-analizer` y la lectura de `user_entity_roles`. Las del panel que leen todo
(`fetchAllEntities`, `fetchUsers`, `fetchAllMediaPaginated`) son código muerto: no rompen.

Dentro de una misma entidad no se distingue por rol: un empleado lee lo que lee hoy de su
entidad (la app ya filtra en cliente por sucursal y tarea). Afinar eso es otro trabajo.

## Lo que se comprobó antes de diseñar (2026-10-19)

- **Panel:** todo lo de `entities/{e}/…` va por la entidad en curso; el `{e}` sale de
  `currentEntity` o de la ruta, o del propio documento (`addUpdateRequest`, informes), que es
  de la misma entidad. Única consulta de grupo viva: `listCalendarPresets`. Escribe en
  `entities/{e}` (`language`, `config`), sus subcolecciones y en `user_entity_roles` sólo
  `status`/`isActive`. Sin superadmin. `/tools/checking` (sin sesión) está en mantenimiento.
- **App:** lee y escribe su ficha (`language` en cada login), su entidad, sucursales, fichajes,
  tareas y responsabilidades de su entidad; una consulta de grupo `employees where uid ==`.
  Todo con la entidad del login. La ficha lleva `uid` y `entityId` (el modelo exige `entityId`).
- **Quiosco** (`checkbiz360-quiosco`, rama `feat/quiosco`, sin publicar): mismas fuentes de
  datos que la app. **Cuando salga, la sesión del dispositivo tendrá que ser miembro** (por
  asiento o por espejo); se anota como dependencia de su diseño.
- **Backend y backoffice:** Admin SDK, no pasan por reglas.

## Riesgos y cómo se cubren

| Riesgo | Efecto | Cobertura |
|---|---|---|
| Ficha con `uid` sin espejo (trigger caído, ficha antigua) | Esa persona no lee nada: no ficha | Reconciliación antes de las reglas y comprobación de cero diferencias; métrica de errores del trigger |
| Asiento con id distinto de `{userId}_{entityId}` | Ese dueño o admin no ve su empresa | Recuento en dev y prod antes del despliegue: asientos cuyo id no casa |
| Ficha sin `entityId` | Falla la consulta de grupo de la app para esa persona | Recuento de fichas con `uid` y sin `entityId` |
| Preset de calendario sin `entityId` | No sale en la lista | La consulta ya filtra por `entityId`: hoy tampoco sale |
| Consulta de grupo no prevista | 403 | Inventario de los tres clientes; QA entera en staging |

## Orden y prueba en staging

1. **Código** en `feat/reglas-paso-2a`: reglas, trigger, script, pruebas del emulador con la
   matriz anónimo / empleado de A / dueño de A / admin desactivado de A / dueño de B / sesión sin
   nada, contra datos de A, incluidas consultas de grupo y listas.
2. **Dev, antes de las reglas:** desplegar el trigger (`desplegar.mjs --project dev-encodebiz
   --solo onEmpMember --con-reintentos`), reconciliación simulada → `--apply` → simulada otra
   vez con cero diferencias. Recuentos de asientos y fichas raros.
3. **Dev, reglas:** guardar el ruleset vivo, `firebase deploy --only firestore:rules --project
   dev-encodebiz`, verificación por REST con sesiones de dos entidades.
4. **QA en staging:** suite de Playwright entera fuera de la ventana de medianoche de Madrid; a
   mano en el panel (login, cambio de empresa, invitación, presets, empleados, fichajes,
   informes, tareas) y en la app de desarrollo (login, multiempresa, fichaje, tareas, avisos).
   Un alta nueva de empleado y su primer login en menos de un minuto.
5. **Prod**, otro día y con autorización expresa: el mismo orden (trigger, reconciliación con
   cero diferencias, copia del ruleset, reglas), y media hora mirando con un cliente real.

## Storage

Las reglas de Storage vivían en `encodeBiz-SAAS/storage.rules` (retirado) y dejaban a cualquier
sesión leer, listar y subir en todo el bucket salvo `documents/`. Comprobado en dev el
2026-10-19 con la sesión de un dueño cualquiera: metadatos, descarga, listado de `checkbiz/` y
subida, todo **200**, sobre informes de otra empresa.

Inventario del mismo día: **ningún cliente usa el SDK de Storage.** El panel tiene un
`fileManager.ts` sin importadores (el último uso, el avatar `user-avatar/`, se quitó el 2-sep);
la app y el quiosco declaran `firebase_storage` pero no lo importan. Todo se sube por la API
(multipart en tareas y documentos, base64 en la foto del quiosco) y se muestra con la URL que
devuelve la API: firmada por el backend o, en lo antiguo, con token de descarga. Ninguna de las
dos pasa por las reglas.

Así que `encodebiz-api/storage.rules` cierra el cliente entero (`allow read, write: if false`),
declarado en el `firebase.json` de la raíz junto a Firestore. En dev el 2026-10-19, con copia
previa en `deployment-prod/2026-10-19-storage-rules-dev-antes.rules`: con sesión, todo 403; la
URL con token (In-App Messaging) y la URL firmada, 200.

- **No volver a desplegar Storage desde `encodeBiz-SAAS`**: su `firebase.json` lo declara y
  reabriría el bucket.
- Las URLs firmadas del backend caducan en **2050** (`media`, `tasks`, campañas): quien tenga una
  la tiene para siempre. No es de las reglas, pero es la siguiente fuga del mismo tipo.
- El bucket europeo de los ficheros de trabajadores (CLAUDE.md, almacenamiento) no tiene reglas
  publicadas en dev porque no existe allí; en prod hay que mirar qué buckets tienen release.

## Lo que salió al implementarlo

- `string(document).split('/')[0]` no da la entidad: la regla fallaba para todo el mundo. Y
  `document[0]` vale al leer un documento pero no al listar («Variable is not bound in path
  template»). `entities` va en su propio `match /entities/{e}/{resto=**}` y el comodín general
  la excluye.
- El nombre de la función en GCP no puede pasar de 62 caracteres: se exporta como
  `onEmpMember`. Con `retry: true`, el primer despliegue pide `--force`; `desplegar.mjs` lo
  pasa con `--con-reintentos`, sólo junto a `--solo`.
- La QA de Playwright no prueba las reglas: lee y escribe con Admin SDK. Lo que las prueba es
  el emulador (`qa/reglas/probar-reglas.sh`, 96 casos), las sondas por REST con sesiones reales
  y el panel y la app de desarrollo.

**Vuelta atrás:** redesplegar el ruleset guardado (menos de un minuto). El trigger y el espejo
pueden quedarse: sin la regla nadie los lee.
