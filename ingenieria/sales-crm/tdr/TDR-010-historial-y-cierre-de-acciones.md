# TDR-010 — Historial y cierre de acciones

**Fecha:** 2026-10-28
**Estado:** En implementación (rama `fix/crm-historial-acciones`)
**Origen:** issue #201 «mejorar crm», de la responsable de marketing (21-oct)
**Toca:** [ADR-008](../adr/ADR-008-acciones-planificadas-por-contacto.md), [TDR-006](./TDR-006-acciones-planificadas.md)

---

## El problema, tal como se vio

Quien lleva el CRM marca «Hecho» y la acción se va de Pendientes sin que nada diga que se ha
guardado. Si repite, el servidor contesta «la acción ya está hecha» en amarillo: parece un
fallo justo cuando funcionó. Lo hecho existe, pero la cuenta solo enseña las 20 últimas
actividades, y si al cerrar escribe un comentario, ese comentario **sustituye** al mensaje
enviado. La «Próxima acción» de la empresa es un texto libre que nadie cierra, y se queda en
rojo con la acción ya hecha. Un mensaje privado planificado como «Nota» no mueve la etapa, y
una vez planificado no se le puede cambiar el canal. La respuesta en el momento es solo una
etiqueta en la actividad saliente: no hay registro de la respuesta, y «Ha respondido» deja la
cuenta en `contacted`.

Lo que se espera: completar → queda en el historial → la respuesta, si la hubo, queda aparte
y enlazada → la etapa se mueve si toca → se ve el siguiente paso y su fecha. Nada se borra
ni se sobrescribe.

## Decisiones

### 1. «Hecho» es idempotente y confirma

`POST /actions/:id/complete` sobre una acción **ya hecha** devuelve `200` con lo que se
registró (`activityId`, etapa actual) y `alreadyDone: true`, en vez de `409 action_closed`.
Así un reintento —porque la respuesta se perdió o porque no quedó claro— no duplica nada ni
asusta. Sobre una **descartada** sigue siendo `409`: eso sí es otra cosa. El panel confirma
con un aviso («Registrado en el historial», y la etapa nueva si cambió).

### 2. Lo enviado no se pisa

El resumen de la actividad es siempre el título y el borrador de la acción; el comentario de
quien la cierra se **añade** detrás, no los sustituye. Si no cabe en 4000 caracteres, se
recorta el borrador, nunca el comentario.

### 3. La respuesta en el momento es una actividad propia

Al cerrar, «¿hubo respuesta?» deja de ser una etiqueta de la saliente:

- `no_answer` se queda en la actividad saliente, como hasta ahora.
- Cualquier respuesta (`replied`, `interested`, `not_interested`, `booked`, `opted_out`)
  crea **una segunda actividad**, `direction: inbound`, mismo canal y contacto, con
  `in_reply_to` apuntando a la saliente y, si se escribe, el texto de lo que respondió
  (`replySummary`). Sin texto, el resumen dice qué respuesta fue.
- Las dos pasan por `LogActivity` en la misma transacción, así que la etapa sale sola:
  la saliente lleva a `contacted`; la respuesta, a `conversation` (o `demo` si agenda).
  `sales_lead_qualified` se emite como siempre al entrar en conversación.
- Una tarea interna (`note`) no tiene respuesta: conserva el comportamiento de antes.

Columna nueva `sales_activities.in_reply_to` (FK a la misma tabla, nula). Vale también para
el futuro: una respuesta que llega días después podrá enlazarse igual.

### 4. Cinco canales, y el canal se puede corregir

Tipos de actividad y de acción: se añade `comment` (**comentario público**, en LinkedIn u
otra red). En pantalla quedan: Comentario público, Mensaje directo (`linkedin`), Email,
Llamada, Reunión, Demo y Nota interna (`note`). Todos salvo la nota son contacto saliente:
exigen perfil vigente (ADR-003) y llevan la cuenta a `contacted`. Un comentario público
cuenta como contacto porque es un toque intencionado y visible a esa persona, y porque si no
cuenta, el CRM no lo ve al decidir el siguiente mensaje y se repite.

`PATCH /actions/:id` acepta `type` mientras la acción esté pendiente; si el canal nuevo es
saliente, se comprueban otra vez las reglas de contacto.

### 5. La próxima acción sale de las acciones planificadas

Se retira el texto libre `next_action` / `next_action_at` de la cuenta. La próxima acción de
una empresa es **su acción pendiente más cercana**; si no tiene, «Sin próxima acción» y un
botón para planificar. Lo que antes se escribía ahí («revisar el pliego») es una acción de
tipo nota interna.

- Lecturas: `AccountSummary.nextAction` / `nextActionAt` se calculan con la acción pendiente
  más cercana; desaparece `nextPlannedAt`, que era lo mismo. La agenda diaria y
  `crm_next_actions` quedan bien sin tocarlas.
- Escrituras: `crm_create_account` / `crm_update_account` y la API siguen aceptando
  `nextAction` / `nextActionAt` (el plugin de Cowork ya instalado los usa), pero ahora
  **crean una acción planificada de tipo nota** en la misma transacción. Nunca se guardan en
  la cuenta.
- Migración `045`: cada cuenta abierta con texto o fecha en `next_action` gana una acción
  `note` pendiente con ese texto (fecha: la que tenía, o la de la migración). Idempotente
  (`created_by = 'migracion:045'`). Las columnas se quedan, sin leerse, hasta el pase
  siguiente; se borran después en otra migración.

### 6. Historial completo y paginado

`GET /accounts/:id/activities?contactId&limit&cursorAt&cursorId`: la cronología entera,
paginada por servidor con cursor (`occurred_at`, `id`). La cuenta sigue trayendo las 20
últimas para pintar rápido; «Ver más» pide el resto, y el filtro por contacto se hace en el
servidor, no sobre esas 20. Cada línea: fecha, canal, dirección, contacto, resultado,
responsable y el texto; la respuesta va debajo de su mensaje. Herramienta MCP nueva
`crm_list_activities` para que el asistente planificador lea la historia antes de proponer.

Las acciones descartadas no son actividad (no pasó nada), y siguen sin entrar en la
cronología.

### 7. Etapas: registrar no se bloquea y la etapa se corrige a mano

Segunda queja de la misma persona (28-oct): «Cambiar etapa solo me deja ponerla en perdida, y
no funciona bien». Lo que pasaba: lo contactado sin investigar no se podía registrar (ADR-003),
la empresa se quedaba en `signal`, y desde `signal` a mano solo se permitía `lost`. Prueba y
Cliente pedían un id interno de entidad que nadie tiene a mano.

- **Perfil al planificar, no al registrar** (revisión de ADR-003, aprobada por Jose).
  `LogActivity` y `CompleteAction` ya no exigen perfil; `PlanAction` y el cambio de canal de
  una pendiente, sí. La oposición y la regla del email (06 §D5) se mantienen al registrar: son
  ley. La respuesta dice `withoutProfile: true` y el panel marca en rojo «Contactada sin
  investigar» mientras la cuenta pase de `researched` sin perfil vigente.
- **Cambio manual a cualquier etapa**, hacia delante o hacia atrás, incluida reabrir una
  perdida, con **motivo obligatorio** (`note`) que queda en la cronología. `lost` sigue
  pidiendo `lostReason`. Las etapas automáticas siguen moviéndose solas; esto es para corregir.
  Un cambio manual no emite `sales_lead_qualified`: la conversión la da una respuesta real.
- **Prueba y Cliente sin id de entidad obligatorio.** Se puede dar; si no, la cuenta se marca
  en rojo «Sin vincular a la plataforma». El id solo se guarda: nada lo consume hoy.
- **Desde la ficha de contacto** también se cambia la etapa de su empresa.

## Fuera

- Enlazar a mano una respuesta que llega días después a su mensaje (la columna ya lo permite;
  la pantalla, todavía no).
- Borrar las columnas `next_action*` (pase siguiente).

## Verificación

Tests de `sales`: «Hecho» repetido no duplica; comentario + borrador conservados; respuesta
crea inbound enlazada y mueve a `conversation`; `comment` lleva a `contacted`; cambio de
canal revalida; próxima acción derivada; `nextAction` al crear/editar crea nota; paginación
por cursor. En dev: migración en `encodebiz_staging` y prueba del flujo en el backoffice.
