# TDR-004 — Los contratos del cliente y su rentabilidad

**Fecha:** 2026-11-04
**Estado:** API en `develop` `0a9c1cf` y `staging` `768b052` (`[skip ci]`), desplegada a mano en el VPS de dev y probada el 2026-11-05; panel commiteado en `feat/cartera-de-clientes` (`1a094562`, `c6647d05`), sin push, probado por su proxy en local. Pase en `DOCS/deployment-prod/proximo-pase-back.md` §35.
**Componente:** `packages/shared` (entidad y repositorio), `services/customers` (contratos, rentabilidad, cierre, previsión), `services/tasks` (`contractId`), `services/merlin` (lectura del PDF), migración `051`; panel (ficha del cliente y tarea).
**Decisiones de base:** [ADR-006](../adr/ADR-006-el-contrato-es-el-montaje.md) (el contrato es el montaje), 06 §D11 (el recorte del MVP), 03 §El contrato, §La rentabilidad, §La previsión y §El histórico.
**Lo que ya existe y se usa:** la migración `050` (`checklogs_raw.task_id`, `dim_responsibilities.job_price`, `responsibility_events`, `task_events_raw`), `item_movements_raw` + `dim_items.unit_cost`, el documento `customer_contract` del TDR-003, la lectura de PDF con disposición y el borde que tacha nombres de `merlin` (cuadrantes).

---

## 0. Lo que cambia respecto a ADR-006

ADR-006 decía que el contrato se vinculaba a **una sucursal o una tarea** (el montaje). Jose lo
corrigió el 2026-11-05: *«un cliente puede tener varios contratos a la vez; un contrato no puede
colgarse de la sucursal sino del cliente, como un documento más»*. Y sobre a cuál va cada tarea
aceptó la recomendación: **la tarea dice de qué contrato es**, y solo lo pide cuando el cliente
tiene más de uno vigente. Además (06 §D11 bis) la rentabilidad es **core**: el add-on es el portal.

Se mantiene de la ADR: solo se pide el PDF; lo real sale solo y **en bruto**; la primera estimación
se congela; la previsión viene del histórico y con pocos cierres no enseña ninguna cifra.
`customer_hours_daily` no se construye: el coste sale del crudo que ya hay (§4).

## 1. El modelo

### `CustomerContract` (`shared`, colección plana `entities/{e}/customerContracts/{id}`)

Plana para leerla por id desde la tarea sin saber el cliente. Importe en céntimos.

```ts
export interface ContractTerms {
  amount?: number;            // céntimos, el precio cerrado con el cliente
  currency?: "EUR";
  estimatedHours?: number;    // horas de trabajo, no días de calendario
  complexity?: 1 | 2 | 3 | 4 | 5;
}

export interface CustomerContract extends ContractTerms {
  id?: string; entityId: string; customerId: string; title: string;
  documentId?: string;        // el PDF en el documental (customer_contract); opcional
  startsAt: Date; endsAt?: Date; notes?: string;
  extraction?: ContractExtraction;                    // lo que leyó la IA, con citas; no se reescribe
  initialEstimate?: ContractTerms & { savedAt: Date }; // solo lectura: de aquí aprende la previsión
  closedAt?: Date; closedBy?: string; status: "active" | "closed";
  createdBy: string; createdAt: Date; updatedAt: Date;
}
```

El **vencimiento en rojo** sigue siendo del documento (`expiresAt`, TDR-003): al crear un contrato
desde un documento, `endsAt` toma su `expiresAt` si no se dice otra cosa.

### El contrato en la tarea (`Task.contractId`)

La regla vive en `shared` (`resolveTaskContract`) y la aplica `tasks` al crear, al cargar el
cuadrante, al editar y al duplicar:

- `contractId: null` lo quita; un id tiene que ser un contrato **activo de ese cliente**
  (`task/contract_not_found`, `task/contract_not_of_customer`, `task/contract_closed`, 400). Fuera
  de su vigencia se acepta: la empresa sabe por qué sigue yendo.
- Sin decir nada: el **único vigente** en la fecha de la tarea (inicio previsto o, si no,
  vencimiento) se pone solo. Con varios o ninguno, sin contrato. **Nunca se bloquea** una tarea.
- Cambiar el cliente de la tarea vuelve a resolver el contrato; quitar el cliente lo quita.
- Una tarea es de un solo contrato, así que el total del cliente no cuenta nada dos veces.
- Borrar un contrato con tareas: 409 `customers/contract_has_tasks`. Antes se cambian o se quitan.
- `initialEstimate` se congela la primera vez que el contrato tiene horas o complejidad.

## 2. La lectura del PDF (en `merlin`, no en `customers`)

El contrato lleva el nombre del cliente, direcciones, firmantes y a veces DNI. Por la regla de la
casa (nombres nunca a OpenAI; borde `PERSONA_n`, 04-nov), la lectura va por donde ya va la de
cuadrantes: **`merlin`**, que tiene el lector de PDF con disposición, el borde que tacha, el
modelo y la disciplina de «propuesta con evidencia, nada se guarda». `customers` no habla con
OpenAI ni carga pdfjs.

`POST /api/v1/gpt/contratos/leer` — `requireFirebaseAuth` + `requireEntityWriter`, como
cuadrantes. Cuerpo: `{ entityId, documentId }`.

1. Lee `entities/{e}/documents/{documentId}`; exige `scope: "customer"` y `status: "active"`;
   404 si no. Descarga `storagePath` del bucket (misma cuenta de servicio que el documental).
2. `aTexto` (PDF, hoja o texto, por contenido). Si el PDF es una imagen escaneada sin capa de
   texto, el texto sale vacío: responde `unreadable` y el panel enseña el formulario vacío con
   la frase «no se ha podido leer el PDF; rellena los datos a mano». Sin OCR en esta versión.
3. **Sombra**: se tachan nombres, direcciones, teléfonos, correos y DNI con `Seudonimos`;
   importes, fechas, horas, porcentajes y palabras de contrato quedan intactos. Es una sombra
   de texto corrido, no de rejilla: función nueva `sombraDeTexto` junto a `sombraDeCuadrante`,
   con el mismo diccionario y la misma restauración.
4. Modelo (`gpt-5-mini`, JSON estricto): importe total **sin IVA si el documento lo distingue**
   (y lo dice en `notes`), moneda, fecha de inicio, de fin, horas estimadas de trabajo (solo si
   el documento las dice o se deducen de «N operarios × M jornadas»; si no, vacío), complejidad
   1–5 **solo si el documento la justifica** (número de ubicaciones, alturas, permisos, plazos),
   y por cada dato la cita literal. Avisos en lenguaje de persona, nunca de campos.
5. Se restauran las citas (lo tachado vuelve a su valor) y se devuelve la propuesta. **No se
   guarda nada**: el panel se la lleva al formulario y, al guardar en `customers`, viaja como
   `extraction` para quedar de evidencia.

### La anonimización (RGPD, Jose 2026-11-05: «todo documento debe ir anonimizado cuando se usan modelos»)

`sombraDeContrato` aplica tres pasadas, en este orden. Primero lo **conocido** de Firestore: el
cliente, sus contactos, la empresa y su plantilla. Después lo que tiene **forma** de identidad:
DNI, NIE, CIF, IBAN, correos, teléfonos, lo que sigue a un tratamiento, direcciones y códigos
postales. Por último, **todo tramo de palabras con mayúscula** que no sea vocabulario seguro de
contrato. La última pasada es la que cierra la puerta: falla tachando de más, como la lista
blanca de los cuadrantes. El panel lo dice al lado de «Leer el PDF» (`AiPrivacyNotice`). Lo que
la sombra no puede reconocer es texto en minúscula que identifique a alguien, como un
diagnóstico: por eso el aviso pide no subir datos de salud.

## 3. La API de `customers`

Bajo `/api/v1/customers`, con la cadena actual (credencial → entidad → actor). Permisos en §6.

| Ruta | Qué hace |
|---|---|
| `GET /:customerId/contracts` | Los contratos del cliente con su rentabilidad y el total (el total, solo owner/admin) |
| `GET /:customerId/contracts/options?at=` | Para el selector de la tarea: contratos activos, cuáles vigentes en esa fecha y cuántos; sin dinero |
| `POST /:customerId/contracts` | Crea: `title`, `documentId?`, `startsAt`, `endsAt?`, términos, `extraction?`, `notes?` |
| `GET /contracts/:id` | El contrato con su rentabilidad, la previsión y sus eventos |
| `PATCH /contracts/:id` | Términos, fechas, título, notas (`null` quita). Cada término cambiado deja `terms_changed` |
| `POST /contracts/:id/close` · `/reopen` | Cierra (escribe `contract_outcomes`, puntúa previsiones) o deshace el cierre |
| `DELETE /contracts/:id` | Borra el contrato, no el documento; 409 si tiene tareas |

## 4. La rentabilidad: la suma de las tareas del contrato

Se calcula al leer. `customers` busca en Firestore las tareas con ese `contractId` y lee Postgres
con el `pool` de `shared`:

- **Tareas con fichajes** (`checklogs_raw.task_id`, horario por tareas): se emparejan con
  `buildWorkSessions` y se valoran con el `employee_price` del fichaje. Fiable.
- **Tareas sin fichajes**: su reloj (`startedAt → completedAt − pausedMs`) por cada asignada,
  valorado con `dim_responsibilities.job_price`. Se avisa con `task_clock`.
- **Material**: `item_movements_raw` de tipo `consumption` de esas tareas × `dim_items.unit_cost`;
  sin coste unitario, cantidad sí e importe no.
- `labour.source`: `checklogs`, `task_clock`, `mixed` o `none`. Avisos: `no_tasks`, `no_rate`,
  `unpriced_material`, `untracked_sessions`, `task_clock`.

Todo en céntimos y en bruto. **Nunca un cero que parezca un dato**: sin tarifa, `costCents: null`.

## 5. Cierre y previsión

- `close` escribe `contract_outcomes`: `initialEstimate`, términos finales, minutos reales,
  coste, material, personas, días, importe, complejidad. Una fila por contrato; `reopen` la
  borra.
- **Sesgo**: mediana de `actual_hours / initial_estimated_hours` sobre los cerrados de la
  empresa con la misma complejidad (mínimo 5); si no los hay, sobre todos los cerrados (mínimo
  5). Horquilla: percentiles 25 y 75. Por debajo del mínimo, `insufficient_history` y **ninguna
  cifra**.
- **Antes de empezar**: `estimatedHours × sesgo × coste medio/hora de los parecidos` → horquilla
  de horas, coste y margen. **Durante**: consumido + `(estimatedHours × sesgo − horas reales) ×
  coste/hora de este montaje`; si cruza el importe, `overBudgetAt` al ritmo de los últimos 7
  días.
- **Cada previsión que se enseña se guarda** en `contract_forecasts` (`model_version:
  "median-bias-v1"`) y se puntúa al cerrar (`hours_error_pct`, `within_range`). Es lo que deja
  medir si el modelo acierta antes de cambiarlo.

## 6. Permisos

El coste es salario. Quien hoy ve coste en la plataforma (panel de dirección, `ver_costes`) es
owner y admin. Aquí igual: **contratos, importes, coste y margen: owner y admin**
(`seesEverything`). El gestor y el supervisor ven en la ficha del cliente que hay un contrato
vinculado a su montaje y sus horas, pero ni importe ni coste ni margen (la respuesta se
recorta por rol, no se bloquea la ruta). Trabajador: nada, como el resto de la cartera. La
lectura del PDF, `requireEntityWriter`: también owner/admin.

## 7. Postgres (migración `051_contratos_montaje.sql`, a mano por SSH)

`customer_contracts` (espejo del contrato, para análisis y para unir con el resto),
`contract_events` (cada decisión humana: `extracted`, `terms_set`, `terms_changed`, `closed`,
`reopened`, `deleted`; con `actor_id`, `field`, `previous_value`, `new_value`,
`source`), `contract_outcomes` y `contract_forecasts` (03 §El histórico, tal cual). El espejo
y los eventos los escribe `customers` en la misma petición, a mejor esfuerzo, como `tasks_raw`.
La `049` sigue reservada para las dimensiones de la cartera (Fase 3, aplazada).

## 8. Panel (`encodebiz-front-saas`)

- **Hecho (05-nov, `1a094562`):** contrato y presupuesto del cliente son documentación
  administrativa. Al subirlos, «visible para» pasa a gestores; marcar supervisores o trabajadores
  se puede, con aviso en rojo (06 §D18).
- **Hecho (05-nov, `c6647d05`)** todo lo que sigue. Variable nueva del proxy:
  `NEXT_BACKEND_URI_CONTRATOS_LEER` (handler `contratos_leer_handler`).
- **Ficha del cliente**, bloque **Contratos**: lista con su tarjeta y el total; «Nuevo contrato»
  desde un documento del cliente o sin PDF; «Leer el PDF» rellena el formulario con cada dato y su
  cita al lado; lo no encontrado, vacío.
- **Tarjeta**: importe, horas y su fuente, coste de RRHH, material, margen, etiqueta **«en bruto»**,
  cobertura de tarifa; **en rojo** cuando el coste pasa del importe. Previsión como horquilla con
  «sobre N contratos cerrados de complejidad X»; sin histórico, la frase y nada más. Cerrar y reabrir.
- **Tarea**: tras elegir cliente, «Contrato» solo si tiene más de uno vigente, sin preseleccionar;
  con uno, nada que elegir. En el detalle, el nombre del contrato.

**App:** nada.

## 9. Core

Cerrado por Jose el 05-nov: la rentabilidad es core. Sin puerta.

## 10. Fuera de este TDR

Presupuestos por líneas; coste de empresa y cotizaciones; repartir un contrato entre varios
montajes; previsión por equipo; OCR de PDF escaneado; Merlin narrando desviaciones (D8);
avisos por correo de contrato que vence o presupuesto superado (alertas por correo, fase 3 de
ese módulo); `customer_hours_daily` y el informe por cliente (Fase 3).

## 11. Pruebas

Hechas en staging el 05-nov (§35 del pase), y la lectura de un PDF inventado por el proxy del
panel (importe, fechas, 96 h y complejidad, cada uno con su frase): estimación congelada; un vigente se pone solo; dos
vigentes dejan la tarea sin contrato; id explícito, inexistente (400) y `null`; total sin doble
cuenta; 409 al borrar con tareas; cerrar y reabrir. Pendiente: un PDF real de cliente, uno escaneado, tareas
con fichajes reales y la vista del gestor (horas sin dinero).

## 12. Pase a producción

`DOCS/deployment-prod/proximo-pase-back.md` §35. Depende de §33 y §34.

