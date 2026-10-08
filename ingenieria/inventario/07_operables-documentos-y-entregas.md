# 07 — Operables con papeles: documentos, revisiones y entregas a personas

**Fecha:** 2026-10-07 (corregido el 2026-10-08) · **Estado:** diseño, sin código · **Decisionario:** Jose Acevedo

> Jose, 2026-10-07: «Necesitamos poder relacionarles documentos como propiedad, la inspección
> de prevención de riesgos, etc. Y poder demostrar mediante el sistema que a un trabajador se
> le entregaron sus EPIs o que la máquina con la que trabaja ha pasado sus revisiones
> obligatorias te cubre legalmente ante cualquier inspección.» Y después: «dentro de
> inventario, como una funcionalidad nueva, ya que esto es estricto contra operables».

## 1. Para qué

Hoy el operable sabe dónde vive, en qué tareas está y cuándo está libre. No sabe **de quién
es, qué papeles tiene ni en manos de quién está**. Y eso es justo lo que pide una inspección de
trabajo:

- **Equipos de trabajo** (RD 1215/1997): que la máquina tiene su documentación (propiedad,
  declaración CE, manual) y que ha pasado las revisiones periódicas obligatorias, con fecha,
  resultado y quién las hizo.
- **EPIs** (RD 773/1997): que a cada trabajador se le entregó su equipo, cuándo, y que se le
  informó de su uso; con constancia del trabajador.

La frase que este módulo puede decir y un ERP de almacén no:

> *El arnés AR-07 es de la empresa desde el 3 de marzo, pasó su revisión el 12 de junio
> (apta, próxima en junio del año que viene), se le entregó a Juan el 15 de junio y Juan lo
> confirmó desde su móvil ese día a las 8:40.*

## 2. Alcance

**Estricto a operables** (decisión de Jose). Lo que se documenta, se revisa y se entrega es un
**ejemplar** (`item_units`): una máquina, un vehículo, un arnés. Un EPI que se entrega es un
ejemplar, con identificador si lo tiene (arnés, casco con número) y sin él si no (un par de
guantes anticorte es un ejemplar sin identificador: lo que importa es el registro de entrega, no
distinguir un par de otro).

**Dentro del add-on de inventario**, como funcionalidad nueva, no como add-on aparte.

**Fuera, por decisión:** la entrega de **consumibles** a personas (una caja de mascarillas) no
entra en esta fase. Queda anotado en [06 §D9](./06_decisiones-abiertas.md) por si un cliente lo
pide; el modelo lo admitiría como un movimiento más del libro.

## 3. Lo que ya existe y se reutiliza

- **El servicio documental** (`documents:3007`) ya tiene el documento con tipo, caducidad
  (`expiresAt`), visibilidad por rol y **acuse de recibo** del empleado (`requiresAcknowledgement`,
  `DocumentWithAckStatus`). Hoy cuelga de la empresa, de una sucursal o de un empleado.
- **El inventario** ya tiene el ejemplar con su almacén base, su estado (`unavailable` con
  motivo) y su agenda; el libro de movimientos; el espejo a Postgres; y los avisos sobre el
  framework de notificaciones de `shared`.
- **La app** ya identifica al trabajador y ya le enseña documentos para confirmar.

No se inventa un segundo documento ni un segundo acuse: **el papel del ejemplar es el documento
de siempre, colgado de un sitio nuevo; la entrega es una asignación del ejemplar a una persona,
con el mismo acuse que un documento** ([ADR-007](./adr/ADR-007-entrega-es-asignacion-con-acuse.md)).

## 4. Modelo

### 4.1 Documentos del ejemplar y del artículo

El servicio documental admite dos ámbitos nuevos:

| `scope` | Cuelga de | Para qué |
|---|---|---|
| `item` | el artículo (`itemId`) | lo común a todos los ejemplares del modelo: declaración CE, manual, ficha técnica |
| `unit` | el ejemplar (`unitId`) | lo propio de ese ejemplar: factura o propiedad, seguro, ITV, revisiones, inspección PRL |

Tipos nuevos en el catálogo de `DocumentType`:

| Tipo | Qué es | Caduca |
|---|---|---|
| `ownership` | factura, contrato de compra o renting, propiedad | no (renting: sí, fin de contrato) |
| `ce_declaration` | declaración CE de conformidad | no |
| `manual` | manual de instrucciones | no |
| `insurance` | seguro del equipo o vehículo | sí |
| `mandatory_inspection` | revisión periódica obligatoria: OCA, ITV, inspección reglamentaria | **sí: la próxima revisión** |
| `maintenance_check` | revisión o mantenimiento interno | sí, si se quiere avisar |
| `risk_assessment` | evaluación o inspección de prevención de riesgos del equipo | sí, según el plan de prevención |

Los campos ya existentes bastan: `expiresAt` es la validez (o la próxima revisión), `metadata`
lleva `result` (`apto` | `no_apto` | `con_reservas`), `performedBy` (organismo o persona) y
`externalRef` (número de certificado). **Un documento con resultado `no_apto` vale como
caducado**: el ejemplar no está en regla.

### 4.2 Qué le pasa al ejemplar

- **Aviso antes de caducar**: `unit_document_expiring`, N días antes (por defecto 30, por
  empresa), a supervisores y responsables de las sucursales del almacén base, por el mismo
  camino que `stock_below_minimum`.
- **Caducado o no apto: no se bloquea.** Jose, 2026-10-08: «no puedes bloquear el uso de
  maquinaria arbitrariamente, pero sí marcarlo en rojo como precaución y mostrarlo
  fehacientemente con un warning». El ejemplar se pinta **en rojo** en todos los sitios donde
  aparece —Existencias, su ficha, el calendario, el selector de material del planificador y la
  app— con el hecho escrito: «Revisión obligatoria caducada el {fecha}» o «Revisión del {fecha}:
  no apto». Y al asignarlo a una tarea o entregarlo a una persona sale un aviso que hay que
  pasar a propósito («¿Asignar de todas formas?»); si se pasa, la reserva o la entrega guardan
  qué avisos se aceptaron y quién los aceptó. Se avisa `unit_document_expired` a los
  responsables. Retirarlo del servicio sigue siendo una decisión de una persona: lo pone en
  `unavailable` a mano, como hoy. **Nombrar lo observado**: el rojo dice el hecho, no una
  interpretación.
- **Caducado, si el tipo no es obligatorio** (`insurance`, `maintenance_check`,
  `risk_assessment`): marca ámbar y aviso de caducidad; sin pregunta al asignar.

No se añade ningún campo al ejemplar: lo que está en regla se calcula de sus documentos cada
vez que se enseña, igual que la posición se deriva de la reserva (ADR-006: lo que se deriva no
se guarda). El job nocturno de `inventory` solo **avisa** de lo que va a caducar y de lo que ha
caducado; no cambia estados.

### 4.3 La entrega: `unit_assignments`

```ts
export type AssignmentStatus = "active" | "returned";
export type AcknowledgementStatus = "pending" | "acknowledged" | "declined";

export interface UnitAssignment {
  id?: string;
  entityId: string;
  unitId: string;
  itemId: string;
  employeeId: string;
  /** Quién la registra, desde el panel o desde la app. */
  assignedBy: string;
  assignedAt: Date;
  note?: string;
  acknowledgement: {
    status: AcknowledgementStatus;
    /** El texto que el trabajador confirma: «He recibido … y la información sobre su uso». */
    text: string;
    at?: Date;
    /** El uid autenticado que confirmó, y desde qué dispositivo (modelo, SO, versión de la app). */
    by?: string;
    device?: { id: string; model?: string; os?: string; appVersion?: string };
    /**
     * Cómo se confirmó, de más a menos fuerte (ver §4.5): firma con la clave del chip seguro
     * desbloqueada por huella o cara; PIN o patrón del móvil; contraseña de la cuenta.
     */
    method?: "biometric_signature" | "device_credential" | "password";
    /** Solo con `biometric_signature`: el reto que el servidor emitió, la firma y la clave. */
    challenge?: string;
    signature?: string;
    publicKeyId?: string;
    /** `true` solo cuando el servidor comprobó la firma con la clave pública registrada. */
    verified: boolean;
    declinedReason?: string;
  };
  status: AssignmentStatus;
  returnedAt?: Date;
  returnedBy?: string;
  returnCondition?: "ok" | "damaged" | "lost";
  returnNote?: string;
  updatedAt: Date;
}
```

Reglas:

- **Un ejemplar tiene como mucho una asignación activa.** Mientras la tiene, no se ofrece a las
  tareas (está en manos de alguien) y el calendario lo pinta «con {persona}». Su almacén base
  no cambia: es a donde vuelve.
- **La asignación no es consumo ni salida** ([ADR-004](./adr/ADR-004-asignar-no-es-consumir.md)):
  no toca saldos. Queda en el libro como `assignment` y `assignment_returned`, con `unitId` y
  `employeeId`, para que el informe y el CSV la vean.
- **El acuse es del trabajador, no de quien entrega.** Un responsable puede registrar la
  entrega; el acuse solo lo puede dar el uid del empleado, desde la app. Hasta entonces queda
  `pending` y se le avisa (`unit_assignment_pending`), igual que con un documento sin confirmar.
- **Rechazar es posible** (`declined` con motivo): «no es mi talla», «llegó roto». Queda
  registrado y el responsable lo ve.
- **La devolución** cierra la asignación con estado del ejemplar; `damaged` o `lost` llevan al
  ejemplar a `unavailable` o `retired` según decida quien recibe.
- **Espejo**: `unit_assignments_raw` en Postgres, mismo patrón que `unit_reservations_raw`.

### 4.5 Cómo confirma el trabajador: biometría, con escalera de alternativas

Jose, 2026-10-08: «lo de la firma quiero hacerlo mediante biometría; creo que Flutter lo tiene,
y en su defecto, o sea que el móvil no lo tenga, necesito una alternativa». Sin firma dibujada.

**Es una capacidad de otro módulo.** Jose, 2026-10-08: «esto es otro módulo»: la misma firma
vale para el recibí de una nómina o el enterado de una amonestación, así que se construye una
vez, en el módulo de [firma](../firma/README.md), y el inventario la consume. Lo que sigue
describe cómo la usa la entrega; las claves por móvil, el reto y la comprobación viven allí.

Hay dos cosas que se parecen y no son lo mismo:

- **`local_auth`** (ya en la app) pide huella, cara, o el PIN del móvil, y devuelve al móvil un
  «sí». El servidor solo sabe que la app dice que pasó. Vale como gesto, no como prueba
  comprobable.
- **Una clave en el chip seguro del móvil** (Secure Enclave en iOS, Keystore/StrongBox en
  Android), creada una vez y que solo se puede usar tras la huella o la cara. Con ella la app
  **firma** lo que confirma, y el servidor **comprueba la firma** con la clave pública que
  registró al activarla. Eso sí es fehaciente: nadie puede fabricar esa firma sin ese móvil y
  ese dedo, y el reto del servidor impide reutilizarla. En Flutter lo hace `biometric_signature`
  (ECDSA, hardware-backed, Android e iOS; a probar en 6c con móviles reales, también de gama baja).

La escalera, de más a menos fuerte; la app usa el peldaño más alto que el móvil permita y el
servidor guarda cuál fue:

| Nivel | Cuándo | Qué hace | `method` | `verified` |
|---|---|---|---|---|
| 1 | el móvil tiene huella o cara | activación una vez: la app crea la clave en el chip seguro y registra la pública (`POST /employees/me/devices`); al confirmar pide un reto al servidor, lo firma con la huella y lo envía | `biometric_signature` | sí |
| 2 | sin biometría, pero con bloqueo de pantalla | `local_auth` con el PIN o patrón del móvil, y el acuse viaja por la sesión autenticada | `device_credential` | no |
| 3 | sin bloqueo de pantalla | vuelve a pedir la contraseña de la cuenta justo antes de confirmar (reautenticación de Firebase; con proveedor externo, la suya) | `password` | no |

En los tres casos quedan el uid, la hora del servidor, el texto confirmado y el dispositivo. El
registro de entrega dice cómo se confirmó: «confirmado con huella, firma verificada», «con el
PIN del móvil» o «con su contraseña». La empresa puede exigir el nivel 1 (ajuste en la
entidad): entonces un móvil sin biometría no puede confirmar y el trabajador lo hace desde
otro, o la entrega queda pendiente. Por defecto, se acepta el mejor peldaño disponible.

La clave es por dispositivo y por empleado; cambiar de móvil es activar otra vez. La baja del
empleado deja las claves inservibles porque el uid ya no entra.

### 4.4 Lo que ve cada uno

- **El trabajador** (app): «Mi material»: lo que tiene a su nombre, con fecha de entrega, y lo
  pendiente de confirmar arriba. Confirmar es leer el texto y poner la huella (o la cara, o el
  PIN del móvil, o su contraseña: §4.5). Nada más.
- **El responsable** (panel): desde la fila de un operable en Existencias, «Entregar» (elige
  ejemplar y persona); desde la **ficha del ejemplar** (nueva ruta, hoy el ejemplar solo es una
  fila de la ficha del artículo), sus documentos, sus revisiones con semáforo, su asignación
  actual y su historial de entregas; desde la **ficha del empleado**, una sección «Material a
  su nombre».
- **La inspección**: **un informe más en el apartado de Informes**, no una descarga desde la
  ficha (Jose, 2026-10-08). «Equipos y EPIs» (nombre por decidir), con dos vistas: **por
  trabajador**, el registro de entrega: qué, cuándo, quién entregó, cuándo lo confirmó y desde
  dónde, firma si la hay; **por ejemplar**, el dossier: propiedad, documentos vigentes y
  caducados, revisiones con resultado y quién las hizo, y a quién ha estado asignado. PDF y CSV,
  generados en `reports` como el resto. **Se lista siempre**: si la empresa no tiene el
  inventario habilitado, la entrada aparece **en rojo**, y al pulsarla sale primero «Tienes que
  habilitar el inventario» con el enlace para contratarlo, y debajo qué es este informe, qué
  hace y de qué te protege. Ese patrón —el informe que depende de un add-on se ve, en rojo, y
  se explica— vale para cualquier otro informe que dependa de un add-on.

## 5. Contratos (boceto)

**Documental** (`/api/v1/documents`): `POST /documents` admite `scope=item|unit` con `itemId` |
`unitId`; `GET /documents?scope=unit&unitId=…`; los tipos nuevos en el catálogo; el acuse no
aplica a estos ámbitos (el que acusa es la asignación, no el papel).

**Inventario** (`/api/v1/inventory`):

| Ruta | Quién | Qué |
|---|---|---|
| `POST /units/:unitId/assign` | gestiona catálogo o supervisor del almacén | `{ employeeId, note?, acknowledgementText?, acceptWarnings? }` → `201 UnitAssignment` con `warnings` (`409 unit_already_assigned`, `409 unit_not_available`). Una revisión caducada **no es un 409**: va en `warnings` y, si se acepta, queda guardado |
| `POST /assignments/:id/acknowledge` | **solo el empleado asignado** | `{ accepted: true, method, challenge?, signature?, publicKeyId?, device }` o `{ accepted: false, reason }`; con `method=biometric_signature` la firma la comprueba el módulo de [firma](../firma/README.md), que es también quien emite el reto y guarda las claves por móvil |
| `POST /assignments/:id/return` | gestiona catálogo o supervisor | `{ condition, note? }` |
| `GET /units/:unitId/assignments` | ve el almacén | historial del ejemplar |
| `GET /employees/:employeeId/assignments?status=active\|all` | el propio empleado o quien gestiona | «Mi material» y la ficha del empleado |
| `GET /units/:unitId/compliance` | ve el almacén | `{ level: ok\|amber\|red, documents: [{ type, expiresAt, result, status: valid\|expiring\|expired\|missing }] }`; es lo que pinta el rojo en cada sitio |

`POST /tasks/:taskId/units` (reservar a tarea) devuelve también `warnings` y admite
`acceptWarnings`, con la misma regla: nunca un 409 por una revisión caducada.

**Informes** (`/api/reports/inventory/compliance`, servicio `reports`): `?entityId&view=employees\|units&employeeId?&unitId?&format=json\|pdf\|csv`. Con el inventario sin habilitar
responde `402 inventory/not_subscribed`, que es lo que el panel convierte en la entrada en rojo
con su explicación.

Avisos nuevos en `messages.ts`: `unit_document_expiring`, `unit_document_expired`,
`unit_assignment_pending`, `unit_assignment_declined`.

## 6. Orden de entrega, por uso

**6a — Entrega con acuse.** Lo que toca a cada trabajador, cada vez que entra o cambia de equipo.
API (`unit_assignments`, libro, espejo, avisos), app («Mi material» y el acuse), panel
(«Entregar» desde Existencias, ficha del ejemplar con su asignación, sección en la ficha del
empleado) y el informe «Equipos y EPIs» en Informes con su vista por trabajador, en rojo sin el
add-on.

**6b — Documentos y revisiones del ejemplar.** Ámbitos `item`/`unit` en el documental, tipos
nuevos, el rojo y el ámbar en cada sitio donde sale el ejemplar, el aviso al asignar, los avisos
de caducidad, y la vista por ejemplar del informe.

**6c — La firma verificable (nivel 1 de §4.5)**: depende del módulo de [firma](../firma/README.md).
En 6a el acuse nace ya con los niveles 2 y 3, que no necesitan nada nuevo en el móvil.

## 7. Lo que exige cada entorno

Colección `unit_assignments` (Firestore, sin índice compuesto si las consultas son por
`unitId` o por `employeeId` con un solo `where`); migración `024` para `unit_assignments_raw`;
los tipos nuevos en el catálogo del documental; cuatro claves de aviso; la ruta del informe en
`reports`, en nginx y en el allowlist del proxy del panel. Nada en Vercel.

## 8. Decisiones y preguntas

- **Decidido (Jose):** estricto a operables; dentro del add-on de inventario.
- **Decidido (Jose, 2026-10-08):** una revisión caducada **no bloquea** la maquinaria: rojo en
  todos los sitios y aviso fehaciente al asignar, que se puede pasar y queda registrado.
- **Decidido (Jose, 2026-10-08):** la prueba para la inspección es **un informe del apartado de
  Informes**; se ve siempre, en rojo si el inventario no está habilitado, y al pulsarlo explica
  que hay que habilitarlo, qué es, qué hace y de qué protege.
- **Decidido (Jose, 2026-10-08):** el acuse se confirma **con biometría**, y si el móvil no la
  tiene, con el PIN del móvil o con la contraseña de la cuenta (§4.5, [06 §D8](./06_decisiones-abiertas.md)).
  Sin firma dibujada. La versión verificable por el servidor es la de la clave en el chip
  seguro; las otras dos quedan registradas como lo que son.
- **Fuera por decisión:** EPIs consumibles ([06 §D9](./06_decisiones-abiertas.md)).
- **Lo que no se promete:** el sistema produce la prueba que una inspección pide (entrega
  confirmada, información sobre el uso, revisiones con fecha y resultado). Que un inspector la
  dé por buena depende del contenido del registro y de la normativa aplicable a cada equipo,
  no de la herramienta. El texto del acuse lo escribe la empresa.
