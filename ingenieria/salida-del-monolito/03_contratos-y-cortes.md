# 03 — Contratos y cortes

## 1. Por qué esto merece un documento

«Ya está portado» y «ya se puede cortar» no son lo mismo, y confundirlos cuesta una tarde de
502 en el peor momento. El panel llama a las funciones de Firebase con una forma muy concreta,
heredada de cómo se escribieron: **una URL fija por operación y todo lo demás en el cuerpo**.

```ts
// src/services/checkinbiz/employee.service.ts
new HttpClient({ baseURL: '/api/proxy/checkinbiz_update_employee' }).post('', { ...data });
new HttpClient({ baseURL: '/api/proxy/checkinbiz_delete_employee' }).delete('', { employeeId, entityId });
```

No hay path, no hay verbo semántico y el identificador viaja dentro del JSON. El proxy de Next
resuelve el handler contra una variable de entorno y reenvía tal cual. Nuestros routers, en
cambio, se escribieron en REST: `PATCH /employees/:employeeId`, `DELETE /employees/:employeeId`.

Son dos contratos distintos para la misma operación. Apuntar la variable sin más devuelve un
404, no un error de datos: el corte parece hecho y no lo está.

## 2. La decisión

**El contenedor imita el contrato viejo y el panel no se toca para cortar.** Se añade un alias
por operación —con la forma que el panel ya manda— que resuelve al mismo caso de uso que la
ruta REST. La ruta REST se queda: es la que usarán la app y los integradores. Ver
[ADR-002](./adr/ADR-002-el-contrato-viejo-se-imita.md).

Cuesta diez líneas por operación y compra tres cosas: el corte vuelve a ser una variable de
entorno, el rollback vuelve a ser esa misma variable, y el panel no entra en la ventana de
riesgo —que es lo que hizo que los fichajes salieran bien—.

## 3. Estado por operación

**Corta con una variable, sin tocar código:**

| Handler del panel | Ruta destino |
|---|---|
| `checkinbiz_create_employee` | `POST /api/v1/employees` (servicio `employees`) |
| `checkinbiz_validate_employee` | `POST /api/v1/employees/validate` (servicio `employees`) |
| `checkinbiz_stats_panel` | `POST /api/analytics/panel/stats` |
| `checkinbiz_enable2af_employee` | `POST /api/v1/checkinbiz/auth/2fa/enable` |
| `checkinbiz_verify2af_employee` | `POST /api/v1/checkinbiz/auth/2fa/verify` |
| `status2fa_user` | `GET /api/v1/checkinbiz/auth/2fa/user/status` |
| `enable2fa_user` | `POST /api/v1/checkinbiz/auth/2fa/user/enable` |
| `verify2fa_user` | `POST /api/v1/checkinbiz/auth/2fa/user/verify` |
| `checkinbiz_stats` (heurística) | `POST /api/analytics/heuristic` |
| `checkinbiz_responsability_handler` | `/api/v1/employees/responsibilities` (POST, PATCH, DELETE) |
| `upload_media` | `POST /api/v1/media` |
| `delete_media` | `DELETE /api/v1/media` |
| `assing_user` | `POST /api/v1/entities/collaborators` |

**Necesita alias antes de cortar:**

| Handler del panel | Lo que manda | Alias a añadir |
|---|---|---|
| `checkinbiz_update_employee` | `POST` con `employeeId` en el cuerpo | `POST /employees/update` |
| `checkinbiz_delete_employee` | `DELETE` con `employeeId` y `entityId` en el cuerpo | `DELETE /employees` |
| `checkinbiz_create_sucursal` | `POST` con el centro entero | `POST /branches` |
| `checkinbiz_update_sucursal` | `POST` con `branchId` en el cuerpo | `POST /branches/update` |
| `checkinbiz_delete_sucursal` | `DELETE` con `branchId` y `entityId` en el cuerpo | `DELETE /branches` |
| `create_entity` | `POST` con la entidad | `POST /entities` |
| `update_entity` | `POST` con `entityId` en el cuerpo | `POST /entities/update` |
| `update_brandng_entity` | `POST` con el branding | `POST /entities/branding` |
| `delete_entity` | `DELETE` con el cuerpo | `DELETE /entities` |

Cada alias cuelga del prefijo de su servicio: `/api/v1/employees`, `/api/v1/branches` y
`/api/v1/entities`. Ver [02 §2](./02_to-be.md).

Es el mismo patrón que ya se usó con los fichajes: `POST /checklogs/update` en vez de un
`PATCH /checklogs/:id`, y por el mismo motivo.

## 4. Dos cosas que hay que averiguar, no suponer

**`employeesExportHandler` no aparece en la allowlist del panel ni tiene variable en el
entorno de desarrollo, y nadie en `src/` lo llama.** Está desplegado y portado, pero no consta
quién lo usa. Antes de contarlo como cerrado hay que encontrar al consumidor —o confirmar que
no lo hay y retirarlo—.

**Las variables de producción las manda Vercel, no el repositorio.** El fichero de entorno de
producción no viaja en el repo y además queda fuera de lo que se toca desde el entorno de
trabajo. Todo lo que dice este documento sobre «dónde apunta hoy» está leído del entorno de
**desarrollo**, que es el que va por delante: si algo apunta a Firebase en desarrollo, en
producción también. Al revés no se puede afirmar, y cada corte en producción se comprueba en
el panel de Vercel antes de darlo por hecho.

## 5. El orden de un corte

Siempre el mismo, y siempre con el rollback probado antes de empezar:

1. La ruta responde en el contenedor de desarrollo, con su alias si lo necesita.
2. Se reproduce contra ella cada fila de la tabla de errores de la operación: mismo HTTP,
   mismo `code`. Un 200 no basta; lo que rompe al panel son los errores.
3. Se apunta la variable en desarrollo y se hace la operación de punta a punta desde la
   pantalla real, mirando en Firestore que el documento queda igual.
4. Se deja correr. Cuando lleve tiempo sin incidencias, se apuntan las variables de producción.
5. La función de Firebase **se queda viva** hasta la Fase 6. No estorba y es el rollback.
