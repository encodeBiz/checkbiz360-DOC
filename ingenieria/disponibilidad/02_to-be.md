# 02 — Arquitectura objetivo (To-Be)

## Dónde vive

En el módulo `calendar` que ya existe, como dos acciones nuevas de solo lectura sobre el mismo
handler:

```
GET calendarHandler?action=availability      → la rejilla agregada
GET calendarHandler?action=availabilityDay   → el desglose de un día
```

No es un servicio nuevo ni una colección nueva. La disponibilidad no tiene datos propios: es
una lectura derivada de datos que el módulo `calendar` ya posee, resuelta con la regla de
herencia que el módulo ya implementa. El razonamiento completo, y las tres alternativas
descartadas, en [ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md).

Reusar el handler existente tiene además una consecuencia práctica que no es menor: el front ya
llega a él por el proxy de Next (`/api/proxy/checkinbiz_calendar_handler`), así que **no hay
variable de entorno nueva, ni entrada nueva en la allowlist del proxy, ni redeploy en Vercel**.

## Plan de lectura en el servidor

El coste sigue siendo lineal con la plantilla, pero se paga **una vez, dentro del mismo
datacenter que Firestore, y no en el navegador de cada usuario**:

| Paso | Lectura |
|---|---|
| 1 | `entities/{e}/calendar/config` — 1 doc |
| 2 | `entities/{e}/branches` — 1 query (filtrada a activas) |
| 3 | `entities/{e}/employees` — 1 query (filtrada por estado computable) |
| 4 | Configs de sucursal — 1 `getAll` de B referencias |
| 5 | **Configs de empleado — 1 query `collectionGroup('calendar')`** filtrada por `entityId` y `type != 'preset'` |

El paso 5 es el que convierte N idas y vueltas en una. Requiere que los documentos
`calendar/config` lleven dentro el campo `entityId`, que hoy sólo está garantizado en los
presets: ver [ADR-002](./adr/ADR-002-entityid-en-los-documentos-de-calendario.md). Mientras no
esté, el Admin SDK puede usar `getAll()` con las N referencias, que es un único round trip aun
siendo N lecturas facturadas — ya suficiente para quitar el problema de latencia.

## Frontera: quién decide qué

| Decisión | Dónde vive | Por qué |
|---|---|---|
| Herencia entidad → sucursal → empleado | **Backend** | Ya está resuelta una vez en `ResolveEffectiveCalendarUseCase` |
| Qué estados de empleado cuentan como plantilla | **Backend** | Cambia el denominador; tiene que ser el mismo para todos los clientes |
| Precedencia del motivo de no disponibilidad | **Backend** | De ella depende `closed`, que es dato, no estilo |
| Qué día se considera "cerrado" (descanso) | **Backend** | Ídem |
| Umbrales de color (≥70% verde, ≥55% ámbar) | **Front** | Es lectura visual, no dato. La API devuelve `available` y `total` |
| Agrupación visible, orden, búsqueda, export | **Front** | Presentación sobre una rejilla ya calculada |
| Navegación de mes/semana | **Front** | Sobre el rango ya pedido; sólo vuelve a llamar si sale del rango |

## Lo que deja de existir

En el front se borran el cruce y la duplicación de la regla:

- `src/services/checkinbiz/availability.service.ts` — el cruce contra Firestore, entero.
- De `src/lib/common/availability.ts`, la parte de resolución: `mergeSchedule`, `normalizeDay`,
  `buildDefaultSchedule`, `evaluateMemberDay`, `buildBoard`, `buildDayDetail`.

Sobrevive lo que es presentación: construcción del periodo, formato de horas, umbrales de
color, iniciales. Detalle en [05](./05_integracion-front.md).

## Lo que el prototipo deja hecho

La semántica está fijada y probada contra la vista, así que el backend no parte de una hoja en
blanco: `lib/common/availability.ts` es, literalmente, la especificación ejecutable de las
reglas —precedencia del motivo, definición de día cerrado, qué cuenta como turno—. El
[TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) las recoge una por una.

## Permisos

El handler de calendario hoy no discrimina por nivel de responsabilidad. La disponibilidad sí
tiene que hacerlo, porque devuelve nombres de toda la plantilla:

| Nivel | Qué ve |
|---|---|
| `owner`, `manager` | Todas las sucursales de la entidad |
| `supervisor` | Sólo las sucursales donde tiene responsabilidad |
| `worker` | Nada — `403` |

Es la primera vez que el módulo `calendar` necesita esta distinción, y es trabajo nuevo, no un
port. Se resuelve como en `tasks`, con el nivel del actor
(`worker < supervisor < manager < owner`).

## Cutover

Sin bandera ni doble camino: el tablero no está publicado todavía, así que la Fase 3 sustituye
la implementación del servicio del front y ya. No hay usuarios a los que migrar, ni periodo de
convivencia que sostener. Ver [04](./04_fases.md).
