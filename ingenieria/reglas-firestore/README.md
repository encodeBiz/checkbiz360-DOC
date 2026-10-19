# Reglas de Firestore: cerrar la lectura anónima y aislar por entidad — Documento de Ingeniería

**Proyecto:** encodebiz-api (`firestore.rules`) · encodebiz-front-saas (panel) · checkbiz360 (app)
**Dominio:** reglas de seguridad de Firestore en `dev-encodebiz` y `encodebiz-services`
**Fecha de inicio:** 2026-10-16
**Prioridad:** 🔴 **ALERTA MÁXIMA.** El paso 1 se ejecuta el **17 o el 18 de octubre de 2026**, antes que cualquier otra cosa pendiente.
**Estado:** paso 1 en producción desde el 2026-10-17; **paso 2a** (aislar `entities/{e}`) y Storage cerrado al cliente en producción desde el 2026-10-19, ver [paso-2a.md](paso-2a.md); paso 2b (raíces) pendiente
**Autor:** Jose Acevedo

---

## Por qué es alerta máxima

Hoy, en desarrollo y en producción, **cualquiera lee todo Firestore sin iniciar sesión**. La
regla vigente (`encodebiz-api/firestore.rules`) dice:

```
match /{collection}/{document=**} {
  allow read: if !cerrada(collection, document);
  allow write: if conSesion() && !cerrada(collection, document) && ...;
}
match /{path=**}/{sub}/{document} {
  allow read: if !soloServidor(sub);
}
```

`cerrada()` sólo tapa lo del módulo de firma, los cuadrantes, el conector de asistentes, los
días generados y los lotes de importación. Todo lo demás está abierto a lectura para quien
tenga la configuración pública del proyecto, que va dentro del bundle del panel y de la app:

- `entities/{e}/employees`: nombre, correo, teléfono y DNI de toda la plantilla de todos los clientes.
- `entities/{e}/checklogs`: fichajes con geolocalización.
- `entities/{e}/documents`, `tasks`, `branches`, `calendar`, `subscriptions`.
- `users`, `user_entity_roles`, `searchIndex`, `issues`, `in_app_notifications`.

Y una consulta de grupo (`collectionGroup`) recorre todas las entidades de una vez: no hace
falta conocer ningún identificador.

La escritura pide sesión, pero **cualquier sesión**: una cuenta gratuita recién creada puede
escribir en la entidad de cualquier otro cliente.

Se sabe desde la auditoría de mayo ([BE-05](../../Security-Audit/README.md), con el
`allow read: if request.auth != null` ya propuesto en el
[plan de remediación §5](../../Security-Audit/2026-05-25/REMEDIATION-PLAN.md)), se confirmó
leyendo el ruleset de dev el 2026-09-11 y el de producción el 2026-10-11. No se cerró porque el
panel y la app leen y escriben Firestore directamente y nadie había inventariado qué rompería.
Ese inventario está hecho (abajo). Lo que lo convierte en urgente es que estamos abriendo una
negociación con una empresa de mil empleados y la primera revisión de su responsable de datos
lo encuentra en una hora.

## Principio de diseño

> **Nadie lee sin sesión, y cada sesión lee y escribe sólo las entidades a las que pertenece.
> El catálogo es público. Lo del servidor sólo lo toca el servidor.**

Son dos cierres distintos y van en dos pasos: el primero es un cambio de una línea y se puede
desplegar en un día; el segundo necesita reglas por colección, un cambio en el login de la app
y cuatro arreglos en el panel.

---

## Lo comprobado el 2026-10-16

Inventario de todo lo que lee o escribe Firestore desde fuera del servidor. Rutas relativas a
cada repo.

| Cliente | Cómo se autentica | Lee sin sesión |
|---|---|---|
| **Panel** (encodebiz-front-saas) | Firebase Auth: correo, Google y custom token (`lib/firebase/authentication/login.ts:14,31,36`). Una sola instancia de la app de Firebase; sin REST a Firestore; el servidor de Next sólo usa Admin Auth, nunca Firestore. | Sólo `/tools/checking`, el fichaje web antiguo, que ya está **redirigido a `maintenance`** por `src/proxy.ts:127-133`. Login, registro, recuperación, 2FA y todo `/main/**` leen después de la sesión. |
| **App** (checkbiz360, Flutter) | Firebase Auth: correo, Google y Apple (`auth_provider.dart:829-905`). Mantiene la sesión de Firebase mientras la persona está dentro; sólo hace `signOut` al cerrar sesión, al abortar el login o con `rememberMe=false` al arrancar. | Sólo la **versión mínima** en `app_config/global` desde el splash (`app_config_firestore_datasource.dart:14`, `splash_page.dart:66-113`), antes de `initializeAuthFlow`. Si la lectura falla, el `try/catch` la trata como «no hace falta actualizar» y sigue. |
| **Landing** (CheckBiz360-Landing) | — | No usa Firestore: sólo HTTP a `sales` (`src/lib/leads.ts:13`). |
| **Backoffice** | — | No toca Firestore (todo por su API). |
| **Servicios y Functions** | Admin SDK | No pasan por reglas. |
| **QA** (`qa/`) | Cuenta de servicio | No pasa por reglas. |

Conclusión: **exigir sesión para leer no rompe nada que esté en uso**, con una excepción
pública para `app_config`.

Efecto secundario esperado: al cerrar sesión, algunos listeners siguen vivos un instante después
del `signOut` y soltarán `permission-denied` en consola. En el panel: el documento de la
entidad, `subscriptions`, `issues` y el documento de Merlin (`entityContext.tsx:262-264`,
`merlin.service.ts:111`). En la app: el stream de responsabilidades
(`auth_provider.dart:1016`, sin `onError`). Hay que comprobar que no rompe nada visible, no
que no aparezca el error.

---

## Paso 1 — Sesión obligatoria para leer (17/18-oct-2026)

### El cambio

Una función nueva y dos condiciones en los comodines de `firestore.rules`:

```
// Catálogo público: lo lee la app en el splash, antes de tener sesión (versión mínima y
// enlaces a las tiendas). Sólo lectura: lo escribe el servidor. Un valor mal puesto aquí
// deja a toda la plantilla sin fichar, así que el navegador no lo toca.
function publica(collection) {
  return collection == 'app_config';
}

match /{collection}/{document=**} {
  allow read: if (conSesion() || publica(collection)) && !cerrada(collection, document);
  allow write: if conSesion() && !cerrada(collection, document) && !publica(collection)
    && (collection != 'notification_tokens' || noTocaSigningKey());
}

match /{path=**}/{sub}/{document} {
  allow read: if conSesion() && !soloServidor(sub);
}
```

Dos cosas que no son opcionales:

- La excepción va **dentro del comodín**, no en un `match` aparte: las reglas se combinan con
  OR y un `match` nuevo que abra algo abre para siempre.
- La regla de consultas de grupo tiene que seguir empezando por `{path=**}`: fue el incidente
  del 2026-10-14 (presets de calendario con 403).

### Qué compra y qué no

Pasamos de «cualquiera en internet» a «cualquiera con una cuenta». Como el registro es libre
(freemium), alguien con intención puede crear una cuenta y seguir leyendo los datos de todos.
Deja de ser anónimo, deja de ser trivial y queda rastro de quién lee, pero **no es el
arreglo**: es el torniquete. El arreglo es el paso 2.

### Plan de ejecución

Casillas por rellenar con hora, quién y resultado, como en los registros de
[deployment-prod](../../deployment-prod/).

- [ ] **Rama** desde `develop` en encodebiz-api (nombre: Jose). Cambio en `firestore.rules`
      tal cual el bloque de arriba.
- [ ] **Emulador**: con el `firebase emulators:start --only firestore --project dev-encodebiz`
      y un script de pruebas que compruebe, para anónimo y para una sesión cualquiera:
      - `entities/{e}/employees/{id}` → anónimo denegado, sesión permitido.
      - `collectionGroup('employees')` y `collectionGroup('calendar')` → anónimo denegado,
        sesión permitido.
      - `app_config/global` → anónimo permitido en lectura, **denegado en escritura** incluso
        con sesión.
      - `signing_keys`, `calendar_days`, `staff_imports`, `assistant_*` → denegado para todos.
- [ ] **Dev**: guardar el ruleset vivo (`firebase firestore:rules:get` o la API de
      firebaserules con `x-goog-user-project`) en
      `DOCS/deployment-prod/<fecha>-firestore-rules-dev-antes.rules`; después
      `firebase deploy --only firestore:rules --project dev-encodebiz`.
- [ ] **Verificar en dev por REST**, sin SDK, que es lo que haría un atacante:

      ```bash
      # Anónimo, consulta de grupo: tiene que ser 403 PERMISSION_DENIED
      curl -s -X POST "https://firestore.googleapis.com/v1/projects/dev-encodebiz/databases/(default)/documents:runQuery" \
        -H 'Content-Type: application/json' \
        -d '{"structuredQuery":{"from":[{"collectionId":"employees","allDescendants":true}],"limit":1}}'
      # Con ID token de un trabajador: 200
      curl -s -X POST "…:runQuery" -H "Authorization: Bearer $ID_TOKEN" -H 'Content-Type: application/json' -d '…'
      # app_config anónimo: 200
      curl -s "https://firestore.googleapis.com/v1/projects/dev-encodebiz/databases/(default)/documents/app_config/global"
      ```
- [ ] **QA en dev**: suite de Playwright entera (`qa/`), fuera de la ventana de medianoche de
      Madrid. A mano en el panel: login, aceptar una invitación, 2FA, presets de calendario,
      cerrar sesión. En la app (flavor `development`): splash con y sin sesión guardada,
      login, fichaje, cerrar sesión.
- [ ] **Staging**: el mismo fichero sirve a los dos entornos; fundir la rama en `develop` y
      `staging` como siempre.
- [ ] **Producción**, sólo con autorización expresa de Jose, paso a paso:
      1. Guardar el ruleset vivo de prod con la API de firebaserules
         (`gcloud auth print-access-token` + cabecera `x-goog-user-project: encodebiz-services`),
         como el 14-oct, en `DOCS/deployment-prod/<fecha>-firestore-rules-prod-antes.rules`.
      2. `firebase deploy --only firestore:rules --project encodebiz-services` desde la rama
         (igual que el 14-oct: `main` sigue sin el fichero, ver
         [proximo-pase-back §5](../../deployment-prod/proximo-pase-back.md)).
      3. Las tres comprobaciones por REST de arriba contra `encodebiz-services`.
      4. Media hora mirando panel y app con un cliente real: fichaje, lista de empleados,
         presets de calendario.
      5. Anotar en [proximo-pase-back §6](../../deployment-prod/proximo-pase-back.md) con hora,
         quién y lo que se vio.
- [ ] **Vuelta atrás**: `firebase deploy --only firestore:rules --project <proyecto>` con el
      fichero guardado en el punto 1. Menos de un minuto.

### Trampas conocidas

- `firebase deploy` **siempre** con `--only firestore:rules` y `--project` explícito: un deploy
  completo desde encodebiz-api desplegaría también functions y podaría los índices.
- El hook `block-prod.sh` **no está registrado**; el candado es la regla de CLAUDE.md.
- Un `firebase.json` sin `firestore.indexes` es a propósito; no añadirlo.

---

## Paso 2 — Cada sesión ve sólo lo suyo (diseño; 2-3 semanas)

Aplica a **lectura y escritura**. El modelo de datos ayuda: casi todo cuelga de
`entities/{e}/…`, y lo que está en la raíz lleva `entityId` como campo.

### Cómo se decide la pertenencia

```
function miembro(e) {
  return conSesion() && (
    // Propietario o administrador: el rol se guarda con id `uid_entidad`
    // (shared: auth/entityRole.ts:18-19, auth/canWrite.ts:17). Una lectura por evaluación,
    // cacheada dentro de la petición.
    exists(/databases/$(database)/documents/user_entity_roles/$(request.auth.uid + '_' + e))
    // Empleado: la ficha NO lleva el uid como id (se busca por collectionGroup con `uid`),
    // así que va por claim del token, puesto en el login.
    || (('ent' in request.auth.token) && (e in request.auth.token.ent))
  );
}
```

- **Rol de entidad**: comprobar también que el rol está activo (`get(...).data.status` o
  `isActive`, el campo exacto se decide en el TDR; hoy el panel escribe `isActive` en
  `saveStateCurrentEntity` y `status: active` en `updateAuth`).
- **Claim del empleado**: `loginEmployee.controller.ts:21-23` ya pone `employee: true`; se
  añade `ent: { <entityId>: true, … }` con las entidades que ya resuelve por
  `collectionGroup("employees").where("uid", "==", uid)`. Límite de claims: 1000 bytes
  (unas 25 entidades por persona, de sobra). La app fuerza `getIdToken(true)` tras el login
  para no esperar la renovación horaria; las versiones antiguas de la app reciben el claim en
  la siguiente renovación automática (como máximo una hora).
- **Relleno inicial**: script que ponga el claim a todos los empleados existentes
  (recorrido tipo `firebase_sdk/src/maintenance/census.ts`), para que nadie tenga que volver a
  entrar.

### Matriz por colección

| Ruta | Lectura | Escritura | Notas |
|---|---|---|---|
| `entities/{e}` | `miembro(e)` | servidor | El panel hoy actualiza la entidad por Functions (`updateEntity`); confirmar que no escribe directo. |
| `entities/{e}/{sub=**}` | `miembro(e)` y no cerrada | `miembro(e)` y no cerrada | `calendar_days`, `cuadrante_lotes`, `import_batches`, `staff_imports`, `subscriptions` y `reports` sólo servidor. |
| `{path=**}/employees/{id}` (grupo) | `resource.data.uid == request.auth.uid` o `miembro(resource.data.entityId)` | — | La app lista sus entidades así (`entity_firestore_datasource.dart:71`); la consulta ya filtra por `uid`. Confirmar que la ficha lleva `entityId`. |
| `{path=**}/calendar/{id}` (grupo, presets) | `miembro(resource.data.entityId)` | — | `calendar.service.ts:66` ya filtra por `entityId`. |
| `user_entity_roles/{id}` | `resource.data.uid == uid` o `miembro(resource.data.entityId)` | **ninguna desde el cliente** | Pasar al backend `saveStateCurrentEntity` e `updateAuth` del panel (pendiente ya en baja de colaboradores). |
| `users/{uid}` | propio, o `miembro` de una entidad común | propio | `users.service.ts:12` lee **toda** la colección: hay que acotarla. |
| `searchIndex` | `miembro(resource.data.entityId)` | servidor | Lo escribe shared por Admin SDK. |
| `issues`, `issues/{id}/responses` | `miembro(resource.data.entityId)` | `miembro(resource.data.entityId)` | El listener del panel sobre **toda** la colección (`employee.service.ts:761`) tiene que filtrar por entidad. |
| `in_app_notifications` | `miembro(resource.data.entityId)` | `isRead` y borrado, mismo criterio | La app ya filtra por `employeeId` y `entityId`. |
| `notification_tokens/{employeeId}/devices/{d}` | sesión | sesión y `noTocaSigningKey()` | **Por decidir**: el id es el del empleado, no el uid; atarlo exige que el documento lleve `uid` o `entityId`. En la primera versión del paso 2 se queda como hoy. |
| `campaigns`, `campaigns/{id}/openBy/{uid}` | sesión | sólo `openBy/{uid}` propio | |
| `service`, `service/{id}/plan`, `addons`, `app_config` | **pública** | servidor | Catálogo. |
| `checkbiz_branch_patterns`, `checkbiz_employee_patterns`, `checkbiz_heuristic_indicators_v2`, `ai-analizer` | `miembro(resource.data.entityId)` | servidor | Confirmar que cada documento lleva `entityId` (`stats.service.ts:31,66,83`, `merlin.service.ts:97,111`). |
| `emails_template`, `engine_rules`, `backoffice_users`, `pendingEmails`, `invoice_emails`, `checkbiz_daily_report`, `daily_report`, `pattern_history`, `checkbiz_employee_planifiers` | servidor | servidor | Entran en `cerradas()`. |

### Cambios fuera de las reglas

**Panel (encodebiz-front-saas)**

- `users.service.ts:12`: deja de leer todos los usuarios.
- `entity.service.ts:215,227`: deja de leer todas las entidades.
- `employee.service.ts:761`: el listener de incidencias filtra por entidad.
- `media.service.ts:85`: lee `ENTITIES` con `getAllWithLimit`; parece un error y hay que mirarlo.
- Escrituras en `user_entity_roles` → backend.
- Tras aceptar una invitación o cambiar de entidad, `getIdToken(true)`.

**App (checkbiz360)**

- `getIdToken(true)` después de `loginEmployee`/`validateEmployee`.
- Nada más: todas sus lecturas ya van filtradas por `entityId`, `employeeId` o `uid`.

**Backend (encodebiz-api)**

- Claim `ent` en `loginEmployee.controller.ts`.
- Script de relleno inicial de claims.
- Pruebas de reglas con el emulador (`@firebase/rules-unit-testing`) en el repo, con la matriz
  anónimo / empleado de A / propietario de A / propietario de B contra los datos de A. Es
  barato y es lo único que impide que esto vuelva a abrirse en un cambio futuro.

### Orden de despliegue

Las reglas deniegan lo que los clientes antiguos hacen, así que **primero los clientes, después
las reglas**: panel y backend con sus cambios en producción, script de claims ejecutado, y sólo
entonces las reglas, con la misma ceremonia que el paso 1 (copia del ruleset, deploy con
`--project`, verificación por REST con sesiones de dos entidades distintas, vuelta atrás a
mano).

---

## Decisiones abiertas (Jose)

1. ¿El registro sigue abierto (freemium)? Condiciona cuánto compra el paso 1 por sí solo.
2. `notification_tokens`: ¿se ata al uid en el paso 2 o en una fase posterior?
3. ¿El panel puede seguir escribiendo el documento de la entidad directamente, o pasa al backend?

## Referencias

- [Security-Audit 2026-05-25](../../Security-Audit/README.md): BE-04, BE-05 y plan de remediación §5-6.
- [deployment-prod/proximo-pase-back.md](../../deployment-prod/proximo-pase-back.md) §5 (un solo despliegue de reglas) y §6 (este paso 1).
- Rulesets guardados: `deployment-prod/2026-10-11-firestore-rules-prod-antes.rules`, `2026-10-14-…`, `2026-10-16-firestore-rules-dev-antes.rules`.
- [firma/README.md](../firma/README.md) §Reglas de Firestore: por qué la condición va dentro del comodín.
- Incidente de las consultas de grupo del 2026-10-14: registro §12 de [2026-10-inventario-firma-back.md](../../deployment-prod/2026-10-inventario-firma-back.md).
