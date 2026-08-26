# Prompt para el backoffice — Paso 1: activar y conectar un add-on

> Alcance deliberadamente corto: **solo el alta y la conexión**. Los emparejamientos y el
> panel de datos vienen después, en `prompt-agente-front.md`. Copia lo de abajo tal cual.

---

## PROMPT

Vas a implementar en el backoffice la sección **Integraciones**, pero solo la parte de
**activar y conectar** un add-on. El primero es **RentmanBiz** (`addonId: "rentmanbiz"`),
que conecta CheckBiz360 con Rentman. Habrá más: **no cablees nada específico de Rentman**,
todo sale del catálogo.

### El concepto que hay que entender antes de maquetar

Activar y conectar **no son lo mismo**, y la interfaz tiene que reflejarlo:

- **Activar** da de alta el add-on en la entidad. Queda en `disconnected`: existe, pero
  todavía no habla con el sistema externo.
- **Conectar** entrega la credencial del cliente. Solo entonces pasa a `connected` y
  empieza a trabajar.

El cliente va a pasar un rato en ese estado intermedio. No es un error: es donde hay que
acompañarle.

### De dónde salen los datos

**El catálogo — Firestore, colección `addons`** (léela directo, como ya lees `service`).
Un documento por add-on, todo el texto bilingüe en cinco idiomas (`es`, `en`, `fr`, `pt`,
`de`): `name`, `description` (una línea), `about` (el párrafo), `featuredList` (bullets),
`target` (bloques de valor), `steps` (los pasos del asistente), `connection` (qué
credencial pide y con qué ayuda), `capabilities` (qué sabe hacer, con `available` o
`coming_soon`), `status` (`active` · `beta` · `coming_soon`) y `requires` (de qué
servicios depende).

**Nada de copy en el código**: si un texto no está en el documento, no se pinta.

**El estado por entidad — la API**, `/api/v1/{addonId}`, con Firebase ID token:

| Llamada | Devuelve |
|---|---|
| `GET /connection/{entityId}` | `{ok, connection}` o `connection: null` si no está activado |
| `POST /activate` `{entityId}` | `{ok, connection}` · **409** `service_not_active` |
| `POST /connect` `{entityId, token}` | `{ok, connection}` · **400** `invalid_credentials` · **409** `addon_not_active` |
| `POST /disconnect` `{entityId}` | `{ok, connection}` |
| `POST /active` `{entityId, active}` | `{ok, connection}` |

Y `connection` siempre tiene esta forma:

```json
{
  "addonId": "rentmanbiz",
  "entityId": "…",
  "active": true,
  "status": "disconnected | connected | error",
  "tokenRef": "*****Jy7Pts",
  "lastError": null,
  "activatedAt": "2026-08-19T12:00:00.000Z",
  "connectedAt": null
}
```

`tokenRef` es lo **único** que vuelve del secreto: una cola enmascarada para que el
cliente reconozca cuál de sus tokens está puesto. El secreto completo no sale del
servidor jamás, así que no intentes mostrarlo ni guardarlo en el cliente.

### Los cinco estados de una tarjeta

Combinando el catálogo con `connection`:

| Estado | Cuándo | Qué muestra |
|---|---|---|
| **Bloqueado** | `requires` incluye un servicio que la entidad no tiene activo | Interruptor deshabilitado y el motivo: *"Necesitas CheckBiz activo"* |
| **Sin activar** | `connection` es `null` | Interruptor apagado |
| **Activado, sin conectar** | `active: true`, `status: "disconnected"` | Aviso ámbar *"Falta conectar"* y botón **Conectar** |
| **Conectado** | `status: "connected"` | Verde, con `tokenRef` y la fecha de conexión |
| **Con error** | `status: "error"` | Rojo con `lastError` y botón **Reconectar** |

Un add-on con `status: "coming_soon"` en el catálogo se lista en gris y sin interruptor.
Con `status: "beta"`, etiqueta *Beta* junto al nombre.

### El flujo

1. **Encender el interruptor** → `POST /activate`. Si responde **409**
   `service_not_active`, no lo trates como fallo: explica que hace falta el servicio que
   viene en `requiredService` y deja la tarjeta bloqueada.
2. Con el add-on activado, **abre el asistente** con los pasos de `steps`.
3. **Campo del secreto**: constrúyelo desde `connection.fields` del catálogo (`key`,
   `type`, `label`, `help`). Tipo password, sin autocompletado, sin pegarlo en ningún log
   ni en analítica. La ayuda dice dónde consigue el cliente ese dato.
4. **Conectar** → `POST /connect`. El servidor lo valida contra el sistema externo antes
   de guardarlo, así que un **400** `invalid_credentials` significa que la credencial es
   mala de verdad: enseña `detail` y deja reintentar sin salir del asistente.
5. **Conectado**: cierra el asistente, muestra `tokenRef` y la fecha.
6. **Sincroniza al momento**: llama a `POST /{addonId}/hours/sync-now` `{entityId}` y
   enseña el resultado. Sin esto, el cliente recién conectado tendría que esperar al ciclo
   de 15 minutos para ver la primera señal de vida, que es una pésima primera impresión.

   Ese mismo botón va también en la pantalla del add-on, como *Sincronizar ahora*.
   Responde **429** `sync_in_progress` con `retryAfterSeconds` cuando ya hay una pasada en
   curso o cuando se pulsa dos veces seguidas: deshabilita el botón ese rato y dilo con
   naturalidad ("sincronizando…"), no como error. Y ojo con el resultado en cero: si el
   cliente aún no ha emparejado a nadie o no hay jornadas cerradas, `pushed` será 0 y eso
   **no es un fallo** — explícalo en vez de pintar un error rojo.

### Cambiar o retirar la credencial

- **Cambiar**: se pega una nueva y se llama otra vez a `POST /connect`. No hay edición
  parcial ni "ver token".
- **Retirar**: `POST /disconnect`. Explica que el add-on sigue activado y que dejará de
  sincronizar hasta que se conecte otra vez.
- **Apagar**: `POST /active` con `active: false`. Confirma explicando que **no se borra
  nada** —credencial, emparejamientos e histórico siguen— y que al encender continúa
  donde se quedó. Apagar no es desinstalar.

### Detalles que marcan la diferencia

- **Nunca escribas en Firestore el documento de activación.** Es del servidor: el front
  solo llama a los endpoints. Cifrar no es cosa del navegador.
- **El secreto no se guarda en el cliente**: ni en estado global, ni en localStorage, ni
  en la URL. Se manda y se olvida.
- **Enseña el error real** que devuelve la API, no un genérico. En este flujo el error
  *es* la información útil.
- **Esqueletos mientras carga**, no ceros ni estados falsos: "sin conectar" es una
  afirmación, y si aún no sabes el estado, no la hagas.
- **Idioma del usuario** con `es` de reserva.
- **En beta no se cobra** por activar. No metas pasos de pago ni de plan en este flujo.

### Lo que NO entra en este paso

Emparejar trabajadores, tiles de métricas, divergencias y el panel de eventos y tareas.
Todo eso va en la siguiente entrega y tiene su propio prompt. Si el diseño ya los enseña,
déjalos como bloques vacíos con su título: no inventes datos.
