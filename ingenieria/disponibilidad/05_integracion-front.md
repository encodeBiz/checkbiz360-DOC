# 05 — Integración: Front de administración

**Repo:** `encodebiz-front-saas`
**Rama del prototipo:** `feat/disponibilidad-horarios` (cortada de `develop`)
**Ubicación:** tercera pestaña de *Horarios y festivos* — `(main)/[entityId]/checkinbiz/calendar`

---

---

## Qué hay que hacer, en concreto

El backend está **desplegado y verificado en dev** (2026-09-02). Esta sección es autocontenida:
con lo de aquí se puede hacer el cutover sin volver a leer el resto.

### 1. Repuntar el calendario al contenedor

Las escrituras de calendario ya no viven en la Cloud Function. Es **una variable**, sin tocar
`serverBackendProxy.ts`: el router del contenedor replica el mismo despacho por `action` y
`scope` en el cuerpo, así que ni una sola llamada del panel cambia.

```
NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_HANDLER
  dev  → http://141.95.47.135:8080/api/v1/checkinbiz/calendar
  prod → https://api.checkbiz360.com/api/v1/checkinbiz/calendar
```

Verificado en dev de punta a punta: alta y borrado de festivo en los tres scopes, ausencia con
rango, solapamiento rechazado, validaciones y 404 en borrado inexistente.

**Prod no se mueve** hasta que el panel esté probado contra dev. El rollback es reponer la URL
de la Cloud Function.

### 2. Dar de alta el handler de disponibilidad

Estas rutas son nuevas, así que sí necesitan entrada en la allowlist. En
`src/lib/http/serverBackendProxy.ts`:

```ts
// ── CheckinBiz — Disponibilidad (path-forwarding handler) ─────────────────
// La base es una raíz con subrutas, así que lleva `subPathPattern`: sin él, el
// navegador alcanzaría todo lo que cuelgue de ella a través de un proxy que ya
// pone el token.
checkinbiz_calendar_availability: {
  envKeys: [
    'NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY',
    'BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY',
    'NEXT_PUBLIC_BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY',
  ],
  methods: ['GET'],
  requiresAuth: true,
  subPathPattern: /^(\/day)?$/,
},
```

```
NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY
  dev  → http://141.95.47.135:8080/api/v1/checkinbiz/calendar/availability
  prod → https://api.checkbiz360.com/api/v1/checkinbiz/calendar/availability
```

Queda `/api/proxy/checkinbiz_calendar_availability` y
`/api/proxy/checkinbiz_calendar_availability/day`.

### 3. Las dos llamadas

```
GET .../availability      ?entityId&from&to[&branchId][&includeUnassigned]
GET .../availability/day  ?entityId&date&groupId
```

`from` y `to` en `YYYY-MM-DD`, inclusive, máximo 62 días. `groupId` es el id de sucursal o
`__unassigned__`. Formas exactas de la respuesta en [03](./03_contratos-api.md) — está al día con
lo desplegado, incluido `warnings.discardedHolidays` en la rejilla.

### 4. Lo que se borra

`services/checkinbiz/availability.service.ts` entero, y de `lib/common/availability.ts` la parte
que decide: `mergeSchedule`, `normalizeDay`, `buildDefaultSchedule`, `evaluateMemberDay`,
`buildBoard`, `buildDayDetail`. Sobrevive lo que es presentación (§Qué se queda).

### 5. Cómo probarlo contra dev

Entidad `Wl8ZCvpdmIXzEE0mhT7W`, sucursal `Dr1iEnNrbHS3HWXgXJiy`, un empleado.
Owner: `rpTBdSC6YUhf7uEba26thWSYFM03` — **no** el uid admin habitual, que da `403` porque no es
dueño de esa entidad.

Casos que ya se sabe que responden bien, y que sirven de contraste al pintar:

| Día | Qué debe verse |
|---|---|
| 2026-11-11 (mié) | **Rojo** — la plantilla de vacaciones, agujero de cobertura |
| 2026-11-14 (sáb) | **Gris** — fin de semana, aunque además esté marcado como vacaciones |
| 2026-11-17 (mar) | **Verde** |
| 2026-09-16 (mié) | **Gris** — festivo de sucursal |
| 2026-09-24 (jue) | **Gris** — festivo de entidad |

Si el 11 sale gris, el `source` no está llegando y el tablero está mintiendo hacia arriba.

---

## Estado del prototipo

El tablero está implementado y funcionando, pero **contra el cruce local**. No se fusiona hasta
la Fase 3: la vista es la buena, la capa de datos no. Sirve mientras tanto como especificación
ejecutable de las reglas y como maqueta viva de la vista.

| Fichero | Fase 3 |
|---|---|
| `components/AvailabilityTab.tsx` | **Se conserva.** Cambia de dónde salen los datos |
| `components/AvailabilityDayDetail.tsx` | **Se conserva y crece.** Pinta la respuesta del endpoint y gana los gestos de escritura del ADR-003 |
| `domain/features/checkinbiz/IAvailability.ts` | **Se conserva**, alineando nombres con el contrato |
| `services/checkinbiz/availability.service.ts` | **Se vacía.** Una llamada donde había N+B+2 lecturas |
| `lib/common/availability.ts` | **Se poda.** Se va la resolución; se queda la presentación |

## Qué se borra de `lib/common/availability.ts`

Todo lo que decide, que pasa a ser del servidor:

- `mergeSchedule`, `normalizeDay`, `buildDefaultSchedule` — la herencia entidad → sucursal →
  empleado. Es la tercera copia de una regla que ya vive en `ResolveEffectiveCalendarUseCase`.
- `evaluateMemberDay` — la precedencia del motivo.
- `buildBoard`, `buildDayDetail` — la agregación y el desglose.

## Qué se queda

Todo lo que es presentación:

- `buildPeriodDays` y `startOfWeek` — qué días pinta el mes o la semana. El servidor devuelve un
  rango; el front decide cómo lo trocea en pantalla.
- `coverageLevel` y los umbrales `COVERAGE_OK` / `COVERAGE_WARNING` — el verde, el ámbar y el
  rojo son lectura visual sobre `available` y `total`, no dato.
- `formatTime` — el formato de hora depende del locale.
- `initialsOf` — cosmética del avatar.

## Cómo queda el servicio

```ts
export const fetchAvailabilityBoard = async (params: {
  entityId: string;
  from: string;          // YYYY-MM-DD
  to: string;
  branchId?: string;
  token: string;
  locale?: string;
}): Promise<AvailabilityBoardResponse> => { /* una llamada al proxy */ };

export const fetchAvailabilityDay = async (params: {
  entityId: string;
  date: string;
  groupId: string;
  token: string;
  locale?: string;
}): Promise<AvailabilityDayResponse> => { /* ídem */ };
```

Por `/api/proxy/checkinbiz_calendar_availability[/day]`, que **hay que dar de alta**: las rutas
viven en el contenedor, no en la Cloud Function a la que apunta `checkinbiz_calendar_handler`.

Son dos cosas, y las dos son trabajo del front:

1. Una entrada en `BACKEND_PROXY_TARGETS` de `src/lib/http/serverBackendProxy.ts`, con
   `methods: ['GET']`, `requiresAuth: true` y un `subPathPattern` que sólo permita la raíz y
   `/day` — la base es una raíz de API, así que sin patrón el navegador alcanzaría todo lo que
   cuelgue de ella a través de un proxy que ya pone el token.
2. `NEXT_BACKEND_URI_CHECKINBIZ_CALENDAR_AVAILABILITY` por entorno, y su despliegue en Vercel.

## Cuándo se llama

- **Al abrir la pestaña:** una llamada con el mes visible.
- **Al cambiar de mes o de semana:** sólo si el nuevo periodo se sale del rango ya pedido. La
  vista semanal cae dentro del mes que ya está en memoria, así que no dispara nada.
- **Al pinchar una celda:** una llamada al desglose de ese día y ese grupo.
- **Al filtrar por sucursal o buscar un empleado:** ninguna. El filtro de sucursal recorta la
  rejilla que ya está, y el buscador trabaja sobre los nombres que ya vinieron.

## Errores que hay que tratar de verdad

| `code` | Qué hace el front |
|---|---|
| `calendar/headcount_too_large` | No pinta rejilla vacía: pide elegir sucursal, con el número de plantilla en el mensaje |
| `calendar/forbidden` | Oculta la pestaña entera; un `worker` no debería llegar a verla |
| `calendar/range_too_long` | No debería ocurrir —el front nunca pide más de un mes—; si ocurre, es un bug del front |
| Cualquier otro | Mensaje de error y rejilla vacía. **Nunca un número** |

El último punto es la lección del prototipo: el cruce local trataba cualquier fallo de lectura
como "sin ausencias", y eso convertía un permiso denegado en un empleado disponible. Un tablero
de cobertura que se equivoca callando es peor que uno que no carga.

## El desglose escribe: arrastre y botón

Ver [ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md). Se puede implementar
**antes** que el resto de fases sobre el cruce local del prototipo: la escritura reusa
`upsertCalendar` y `deleteCalendarItem`, que ya existen.

Lo que sí depende del backend es la **lectura**: tras el cutover de la Fase 3, saber qué fila es
reversible deja de calcularse en el navegador y pasa a venir en la respuesta —`reason`,
`reasonSource`, `absenceId` y `paid`—. Y esos campos sólo se pueden rellenar con el `source` de
la Fase 1.

| Gesto | Qué abre | Qué escribe |
|---|---|---|
| *Disponible* → *No disponible* (arrastrar, o flecha →) | `HolidayModal` en scope empleado, con la fecha y la persona puestas | `PATCH` con `holiday` |
| *No disponible* → *Disponible* (arrastrar, o flecha ←) | Modal con las **ausencias propias** de esa persona | `DELETE` con `kind: 'holiday'` |

Reglas que la vista tiene que respetar:

- **Sólo `reason: 'absence'` es reversible.** Festivo de entidad o sucursal, `noShift` y
  `employeeStatus` no se arrastran y llevan la flecha deshabilitada, con tooltip explicando por
  qué y enlace al sitio correcto cuando lo hay.
- **Soltar no escribe:** siempre media un modal que hay que confirmar. Un arrastre accidental
  cuesta un *Cancelar*.
- **El botón no es el plan B.** En tablet es el camino principal; el arrastre es el atajo de
  ratón. Ambos hacen exactamente lo mismo.
- **Tras escribir se vuelve a pedir el dato**, no se parchea en memoria. Misma regla que el
  resto del tablero: ningún número que el front se haya inventado.
- **Retribuida** (`paid`) es una casilla del modal, sólo en scope empleado. Sin valor es *no
  consta* y se pinta distinto de *no* — [ADR-004](./adr/ADR-004-ausencias-retribuidas.md).

Sobre la librería de arrastre: el ADR-003 proponía `@dnd-kit/core` por su recorrido de teclado.
Al llevar cada fila su propio botón, el teclado y el táctil ya están cubiertos por el botón, así
que la implementación usa **arrastre HTML5 nativo y ninguna dependencia nueva**. El día que el
arrastre tenga que hacer algo más fino que dos columnas, la librería sigue siendo la respuesta.

## Búsqueda de empleado

El buscador es un `Autocomplete` local sobre los nombres que vienen en la respuesta: no llama a
`searchIndex` ni al backend. Compara con `normalizarString` —igual que el resto de buscadores
del panel— para que funcione sin tildes, y por palabras sueltas, para que valga tanto
"jose acevedo" como "acevedo jose".

Nota de alcance: el buscador **filtra la rejilla**, no busca una persona. Escribir un nombre
deja las filas de sucursal y recalcula el número contando sólo a quien coincide. Si en algún
momento se quiere lo otro —una fila por empleado—, es una decisión de vista y no toca el
contrato.
