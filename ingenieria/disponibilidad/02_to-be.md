# 02 — Arquitectura objetivo (To-Be)

## Dónde vive

En el módulo `calendar` **del contenedor**, como dos rutas nuevas de solo lectura sobre el
router que ya sirve el calendario efectivo:

```
GET /api/v1/checkinbiz/calendar/availability       → la rejilla agregada
GET /api/v1/checkinbiz/calendar/availability/day   → el desglose de un día
```

Los casos de uso viven en `@encodebiz/shared`, al lado de
`ResolveEffectiveCalendarUseCase`, que es la regla que reusan. Los controladores, en
`services/checkinbiz/src/interfaces/http/calendar/`, colgando del `calendarRouter` que ya está
montado detrás de `requireFirebaseAuth` en `app.ts`.

No es un servicio nuevo ni una colección nueva. La disponibilidad no tiene datos propios: es una
lectura derivada de datos que el módulo `calendar` ya posee, resuelta con la regla que el módulo
ya implementa. El razonamiento completo, y las tres alternativas descartadas, en
[ADR-001](./adr/ADR-001-la-disponibilidad-la-agrega-el-modulo-calendario.md).

### Por qué el contenedor y no la Cloud Function

Porque la regla de herencia buena está en `shared` y el `calendarHandler` de Firebase trabaja
sobre **una copia** que está en retirada. Escribir la agregación allí sería crear la cuarta
implementación de la misma cascada en el repo del que el dominio se está yendo.

Cuesta lo siguiente, y conviene tenerlo escrito porque la primera versión de este diseño lo daba
por cero:

- Una entrada nueva en la allowlist del proxy de Next (`BACKEND_PROXY_TARGETS`), con
  `methods: ['GET']` y un `subPathPattern` que sólo permita la raíz y `/day`.
- Una variable de entorno por entorno, y su despliegue en Vercel.

Es código en el front más un deploy. Barato comparado con la alternativa.

## Plan de lectura en el servidor

El coste sigue siendo lineal con la plantilla, pero se paga **una vez, en el servidor, y no en el
navegador de cada usuario**. Cinco round trips, independientemente del tamaño de la plantilla —
detalle en [TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) §1.

Ojo con una corrección importante: el contenedor está en OVH y Firestore en GCP, así que **no
comparten datacenter**. Lo que hay que minimizar son las idas y vueltas, no las lecturas
facturadas. De ahí que el paso caro se resuelva con un solo `getAll` y nunca con `getDoc` en
bucle.

## Frontera: quién decide qué

| Decisión | Dónde vive | Por qué |
|---|---|---|
| Herencia entidad → sucursal → empleado | **Backend** | Ya está resuelta una vez en `ResolveEffectiveCalendarUseCase` |
| Qué estados de empleado cuentan como plantilla | **Backend** | Cambia el denominador; tiene que ser el mismo para todos |
| Qué día se considera cerrado | **Backend** | Depende del `source` de los festivos, que el cliente no tiene |
| El motivo de cada ausencia, y si es reversible | **Backend** | Es lo que habilita o bloquea el gesto de escritura del ADR-003 |
| Umbrales de color (≥70% verde, ≥55% ámbar) | **Front** | Es lectura visual. La API devuelve `available` y `total` |
| Agrupación visible, orden, búsqueda, export | **Front** | Presentación sobre una rejilla ya calculada |
| Navegación de mes/semana | **Front** | Sobre el rango ya pedido; sólo vuelve a llamar si sale de él |

## El desglose no es solo lectura

El desglose de un día da de alta y borra ausencias
([ADR-003](./adr/ADR-003-el-desglose-del-dia-escribe-ausencias.md)), reusando las escrituras de
calendario que ya existen. Eso condiciona la frontera: el backend tiene que decir, por cada
persona ausente, **qué la deja fuera y si eso se puede deshacer desde aquí**.

De ahí que la respuesta lleve `reason`, `reasonSource`, `absenceId` y `paid`, y de ahí que el
`source` de los festivos (Fase 1) sea prerrequisito y no adorno: es lo que separa el festivo de
la empresa —que no se toca desde el tablero— de la ausencia propia, que sí.

## Lo que deja de existir

En el front se borran el cruce y la duplicación de la regla:

- `src/services/checkinbiz/availability.service.ts` — el cruce contra Firestore, entero.
- De `src/lib/common/availability.ts`, la parte de resolución: `mergeSchedule`, `normalizeDay`,
  `buildDefaultSchedule`, `evaluateMemberDay`, `buildBoard`, `buildDayDetail`.

Sobrevive lo que es presentación: construcción del periodo, formato de horas, umbrales de color,
iniciales. Detalle en [05](./05_integracion-front.md).

## Lo que el prototipo deja hecho

La semántica está fijada y probada contra la vista, así que el backend no parte de una hoja en
blanco: `lib/common/availability.ts` es la especificación ejecutable de las reglas. El
[TDR-001](./tdr/TDR-001-calculo-de-disponibilidad.md) recoge las que sobreviven a la
simplificación.

## Permisos

El handler de calendario hoy no discrimina por nivel de responsabilidad. La disponibilidad sí
tiene que hacerlo, porque devuelve nombres de toda la plantilla: `owner` y `manager` ven la
entidad, `supervisor` sólo sus sucursales, `worker` recibe `403`.

No es trabajo desde cero: `resolveActorByUid` de `tasks` ya hace esta resolución con piezas que
están en `shared`. Se sube y se llama.

## Cutover

Sin bandera ni doble camino: el tablero no está publicado todavía, así que la Fase 3 sustituye la
implementación del servicio del front y ya. No hay usuarios a los que migrar. Ver
[04](./04_fases.md).
