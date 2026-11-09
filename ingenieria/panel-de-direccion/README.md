# Panel de dirección — Documento de Ingeniería

**Proyecto:** encodebiz-api
**Dominio:** `services/backoffice` (módulo `direccion`) y `services/assistant` (registro de uso)
**Fecha:** 2026-10-28
**Estado:** en `develop`, sin desplegar. Migración 044 aplicada en la base de desarrollo.
**Autor:** Jose Acevedo (pedido) · diseño y código con Claude

## Por qué

Las estadísticas del backoffice (`/stats`) cuentan la plataforma entera: cuántos fichajes,
cuántos leads, cuántas conversiones medidas en GA4. Sirven para vigilar la medición, no para
dirigir. Jose, el 2026-10-28: «no me dicen nada, son un montón de datos inservibles; necesito
medir evolución, uso, qué herramientas se usan más, el uso de los MCP; necesitamos hacer que
los clientes usen la plataforma, si no estamos perdidos».

Lo que un responsable de ventas pregunta un lunes es otra cosa: **cuántos clientes la usan de
verdad, si más o menos que el mes pasado, qué partes usan, quién se está enfriando y a quién
llamo hoy**. Y del conector de IA, que es la apuesta: quién lo usa, qué pide y cuánto acaba
escribiendo en la plataforma.

## Lo que había y lo que faltaba

| Pregunta | Antes | Ahora |
|---|---|---|
| ¿Qué clientes están activos? | Un total de entidades | Activos / reales, con el tramo anterior |
| ¿Quién se está enfriando? | Nada | Estado por cliente y lista ordenada por urgencia |
| ¿Qué módulo se usa? | Nada | Empresas por módulo, % sobre activas, diferencia con el tramo anterior |
| ¿Se usa el asistente (MCP)? | Sólo `lastUsedAt` de la conexión | Cada llamada apuntada: herramienta, asistente, empresa, error, escritura confirmada |
| ¿Las altas arrancan? | Nada | Embudo a 90 días: alta → plantilla → primer fichaje → repite → paga |

## Decisiones

1. **Se mide a los clientes, no a nosotros.** Las empresas internas y de pruebas (QA, demo,
   encodeBiz, CheckBiz360, y los ids de `BACKOFFICE_ENTIDADES_INTERNAS`) quedan fuera de
   todos los totales. Se dice cuántas se excluyen.
2. **Cada número lleva su tramo anterior.** Siempre el inmediatamente anterior del mismo
   tamaño. La evolución va a 12 semanas fijas, elija el periodo que elija quien mira.
3. **Un estado por cliente y una frase.** `activo` (actividad en 14 días), `enfriandose`
   (de 14 a 30), `dormido` (más de 30), `sin_arrancar` (nunca, alta de más de 14 días), `nuevo`,
   `baja`. La sugerencia nombra lo observado («18 personas dadas de alta y nadie ha fichado»),
   nunca la causa.
4. **El registro del conector es una tabla, no Firestore.** Una fila por llamada en
   `assistant_tool_calls` (migración 044): crece sin fin, se agrega con SQL, y no lleva
   argumentos ni respuesta (nombres de empleados). Se escribe sin esperar: la herramienta
   responde igual si la base no está.
5. **Se calcula en el servidor y se cachea 5 minutos.** Una docena de consultas agregadas
   por empresa y la lectura entera de `entities`, `subscriptions` (grupo) y
   `assistant_connections`. `?fresh=1` recalcula.

## Fuentes

Postgres: `checklogs_raw` (actividad y canal quiosco por `user_agent`), `tasks_raw`,
`item_movements_raw`, `webhook_delivery`, `task_ratings_raw`, `dim_calendars`
(`schedule_mode`: `calendar` = turnos, `tasks` = por tareas), `dim_employees`,
`operational_daily` (jornadas previstas con fichaje), `assistant_tool_calls`.
Firestore: `entities`, `entities/*/subscriptions`, `assistant_connections`.
Cuota estimada con `shared/platform/pricing` sobre la plantilla activa; Stripe tiene la real.

## Lo que falta

- **Accesos al panel**: Firebase Auth guarda `lastSignInTime`; recorrer las cuentas en la
  cosecha nocturna daría «administradores que entran al panel cada semana».
- **Firma y documentos** por empresa: subcolecciones de Firestore, sin agregado en Postgres.
- **Merlin**: cuántas empresas piden análisis; hoy no se apunta.
- Índice `checklogs_raw (entity_id, timestamp)` (ya pendiente en análisis-a-escala): la
  historia por empresa hace un recorrido completo de la tabla; con la caché no duele hoy.
