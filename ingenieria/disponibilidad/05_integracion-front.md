# 05 — Integración: Front de administración

**Repo:** `encodebiz-front-saas`
**Rama del prototipo:** `feat/disponibilidad-horarios` (cortada de `develop`)
**Ubicación:** tercera pestaña de *Horarios y festivos* — `(main)/[entityId]/checkinbiz/calendar`

---

## Estado del prototipo

El tablero está implementado y funcionando, pero **contra el cruce local**. No se fusiona hasta
la Fase 3: la vista es la buena, la capa de datos no. Sirve mientras tanto como especificación
ejecutable de las reglas y como maqueta viva de la vista.

| Fichero | Fase 3 |
|---|---|
| `components/AvailabilityTab.tsx` | **Se conserva.** Cambia de dónde salen los datos |
| `components/AvailabilityDayDetail.tsx` | **Se conserva.** Pasa a pintar la respuesta del endpoint |
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

Por `/api/proxy/checkinbiz_calendar_handler`, que ya está registrado y ya acepta `GET`. Sin
variable de entorno nueva y sin redeploy en Vercel.

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

## Búsqueda de empleado

El buscador es un `Autocomplete` local sobre los nombres que vienen en la respuesta: no llama a
`searchIndex` ni al backend. Compara con `normalizarString` —igual que el resto de buscadores
del panel— para que funcione sin tildes, y por palabras sueltas, para que valga tanto
"jose acevedo" como "acevedo jose".

Nota de alcance: el buscador **filtra la rejilla**, no busca una persona. Escribir un nombre
deja las filas de sucursal y recalcula el número contando sólo a quien coincide. Si en algún
momento se quiere lo otro —una fila por empleado—, es una decisión de vista y no toca el
contrato.
