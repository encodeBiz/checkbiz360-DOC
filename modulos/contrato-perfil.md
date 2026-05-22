# Módulo ContractProfile — Perfiles Laborales

> Estado: propuesta de ingeniería V1 en validación de arquitectura. Pendiente de aprobación por arquitectura jefe.
> Fuente canónica para backend, backoffice, app móvil y reporting contractual.

## Restricción de Diseño (no negociable)

> **Nada se elimina ni se modifica en el comportamiento existente.**
> El módulo se activa mediante un switch por empleado y sucursal (`contractProfilesByBranch[branchId].enabled`).
> Cuando el switch está desactivado (por defecto), todos los cálculos, estructuras de datos
> y respuestas de API funcionan exactamente igual que hoy.
> Los nuevos campos son siempre aditivos en los documentos Firestore y en las respuestas HTTP.

---

## 1. Contexto

El motor heurístico actual (`HeuristicCalculator`) calcula `costVariance` y `costTrend` usando `metadata.price` (tarifa/hora del empleado) como única referencia de coste. No sabe si las horas trabajadas son ordinarias, extraordinarias o nocturnas, ni si el empleado tiene un límite legal que se esté acercando.

Este módulo añade, opcionalmente, una capa de **contrato de referencia** que enriquece los cálculos existentes sin sustituirlos.

---

## 2. Nomenclatura UX — "Perfiles Laborales"

El menú y los textos de UI usan el término **"Perfiles laborales"** en lugar de "Plantillas contractuales".

**Por qué:** "Plantilla contractual" suena a departamento legal. "Perfil laboral" describe lo que el manager ve: un perfil con las condiciones de trabajo de un tipo de empleado. Es el mismo lenguaje que ya usa el sistema para `EmployeePattern`.

| Contexto | Texto UI |
|---|---|
| Menú de entidad | Perfiles laborales |
| Selector en sucursal | Perfil laboral por defecto |
| Selector en empleado | Perfil laboral asignado |
| Etiqueta del switch | Usar perfil laboral |
| Sección de campos editables | Condiciones específicas (ajustes sobre el perfil) |

---

## 3. Flujo UX — Tres Niveles

### Nivel Entidad — Gestión de plantillas

Nuevo menú **"Perfiles laborales"** en la configuración de entidad. Es el único lugar donde se crean, editan y eliminan los perfiles base. Nadie más puede modificar el perfil en sí.

```
Configuración de entidad
└── Perfiles laborales          ← NUEVO menú
    ├── [+ Nuevo perfil]
    ├── Jornada completa 40h    → editar / duplicar / eliminar
    ├── Turno noche almacén     → editar / duplicar / eliminar
    └── Parcial 20h ventas      → editar / duplicar / eliminar
```

**Regla de eliminación:** un perfil no se puede eliminar si está asignado a alguna sucursal o empleado. El sistema muestra cuántos lo usan antes de intentar borrar.

**Duplicar:** permite crear un perfil nuevo partiendo de uno existente, para ajustar solo lo que cambia (ej. mismo perfil pero con 32h en vez de 40h).

---

### Nivel Sucursal — Selector + autorelleno

En la ficha de configuración de la sucursal aparece una nueva sección **"Perfil laboral por defecto"**:

```
┌─────────────────────────────────────────────────┐
│  Perfil laboral por defecto                      │
│                                                  │
│  Perfil  [Jornada completa 40h        ▾]         │
│                                                  │
│  Al seleccionar un perfil, los campos se         │
│  rellenan automáticamente. Puedes ajustar        │
│  cualquier valor para esta sucursal.             │
│                                                  │
│  Horas semanales contratadas   [40]              │
│  Horas extras permitidas       [✓] Límite [80h]  │
│  Pago por hora extra           [1,25x]           │
│  Nocturnidad                   [✗]               │
│  ...                                             │
│                                                  │
│  Los cambios aquí solo afectan a esta sucursal.  │
│  Para modificar el perfil base: Perfiles         │
│  laborales en configuración de entidad.          │
└─────────────────────────────────────────────────┘
```

**Comportamiento del selector:**
1. El manager selecciona un perfil → los campos se rellenan con los valores del perfil.
2. Si modifica algún campo → ese campo queda marcado como "ajuste de sucursal" (badge visual).
3. Los campos no modificados siguen heredando del perfil base.
4. Si más tarde alguien edita el perfil base en entidad → los campos sin ajuste se actualizan automáticamente. Los campos con ajuste de sucursal no se tocan.

**Sin selector asignado:** la sucursal no tiene perfil por defecto. Los empleados de esa sucursal pueden heredar el perfil default de entidad solo si el switch empleado-sucursal está activo.

---

### Nivel Empleado — Selector + switch + autorelleno

En la ficha del empleado, nueva sección **"Perfil laboral"** (por debajo de los datos personales). El perfil se resuelve por sucursal/proyecto porque un empleado puede trabajar en varias sucursales con condiciones distintas.

```
┌─────────────────────────────────────────────────┐
│  Perfil laboral                                  │
│                                                  │
│  Usar perfil laboral    [  ●  ] Activo           │
│                                                  │
│  Perfil  [Heredado de sucursal: JC 40h  ▾]       │
│          [Jornada completa 40h          ]        │
│          [Turno noche almacén           ]        │
│          [Parcial 20h ventas            ]        │
│                                                  │
│  Horas semanales contratadas   [40]  ← sucursal  │
│  Horas extras permitidas       [✓]   ← sucursal  │
│  Límite anual horas extras     [80h] ← perfil    │
│  Pago por hora extra           [1,25x] ⚙ editado │
│  Nocturnidad                   [✗]   ← perfil    │
│  ...                                             │
└─────────────────────────────────────────────────┘
```

**Comportamiento:**
1. Si la sucursal tiene un perfil por defecto → el selector muestra "Heredado de sucursal: [nombre]" y los campos se rellenan con los valores ya resueltos (perfil + ajustes de sucursal).
2. El manager puede cambiar el perfil del empleado para esa sucursal concreta.
3. Puede editar campos individuales → quedan marcados como "ajuste de empleado en sucursal".
4. El switch activa/desactiva el uso del perfil para esa sucursal. Al desactivarlo, el sistema vuelve al comportamiento actual para ese empleado en esa sucursal.
5. Si el switch está desactivado, los campos del perfil se muestran en gris (referencia visual pero sin efecto).

**Badges de herencia en los campos:**

| Badge | Significado |
|---|---|
| `← perfil` | Valor viene del perfil base sin modificar |
| `← sucursal` | Valor ajustado a nivel de sucursal |
| `⚙ editado` | Valor ajustado para este empleado en esta sucursal |

---

## 4. Modelo de Datos

### `ContractProfile` (colección en entidad)

```typescript
interface ContractProfile {
  id: string;
  entityId: string;
  name: string;           // "Jornada completa 40h", "Turno noche almacén"
  isDefault: boolean;     // fallback cuando no hay perfil asignado en sucursal/empleado
  version: number;        // empieza en 1, incrementa en cada edición
  status: "active" | "archived";
  createdAt: Date;
  updatedAt: Date;

  // Jornada base
  contractType: "full_time" | "part_time" | "fixed_discontinuous";
  weeklyHoursContracted: number;       // 40, 20, 32...
  dailyHoursMax: number;              // 9 (ET default)
  minRestBetweenShiftsHours: number;  // 12 (mínimo legal ET)

  // Horas extraordinarias (full_time)
  overtime: {
    enabled: boolean;
    yearlyLimitHours: number;         // máx 80 (ET Art. 35)
    compensation: "pay" | "rest" | "both";
    payRate: number;                  // multiplicador, mín 1.0 (ET)
    restEquivalentHours: number;      // horas descanso por hora extra
    restMaxWeeks: number;             // plazo para compensar (ET: 16 semanas)
  };

  // Horas complementarias (part_time)
  complementaryHours: {
    enabled: boolean;
    limitPercent: number;             // máx 30 % (60 % con convenio) ET Art. 12
    noticeDays: number;               // mín 3 días ET
    payRate: number;
  };

  // Nocturnidad
  nightShift: {
    enabled: boolean;
    startTime: string;                // "22:00" (ET default)
    endTime: string;                  // "06:00" (ET default)
    dailyHoursMaxNight: number;       // 8 (ET Art. 36)
    overtimeAllowed: boolean;         // false para trabajadores nocturnos (ET Art. 36)
    supplementType: "percentage" | "fixed_per_hour" | "none";
    supplementValue: number;
  };

  // Festivos y domingos
  holidayWork: {
    enabled: boolean;
    supplementType: "percentage" | "fixed_per_hour" | "rest_day" | "none";
    supplementValue: number;
  };
  sundayWork: {
    enabled: boolean;
    supplementType: "percentage" | "fixed_per_hour" | "rest_day" | "none";
    supplementValue: number;
  };

  // Coste base (opcional — enriquece heurística)
  cost?: {
    hourlyRateBase: number;
    currency: "EUR";
  };
}
```

### Campos nuevos en `Branch` (aditivos)

```typescript
// Añadir al documento de sucursal existente
defaultContractProfileId?: string | null;
contractOverrides?: ContractFieldOverrides | null;
```

### Campos nuevos en `Employee` (aditivos)

```typescript
// Añadir al documento de empleado existente
contractProfilesByBranch?: Record<string, EmployeeBranchContractProfile>;
```

### `EmployeeBranchContractProfile`

```typescript
type EmployeeBranchContractProfile = {
  enabled: boolean;                       // switch ON/OFF por sucursal
  contractProfileId?: string | null;      // si null y enabled → hereda de sucursal o entidad
  contractOverrides?: ContractFieldOverrides | null;
  updatedAt: Date;
  updatedBy: string;                      // uid del actor
};
```

No se usa un contrato único global en empleado para V1. La unidad de resolución es siempre `employeeId + branchId`.

### `ContractFieldOverrides`

```typescript
// Dot-notation: solo se guardan los campos que el manager ha modificado
type ContractFieldOverrides = Partial<{
  weeklyHoursContracted: number;
  dailyHoursMax: number;
  "overtime.enabled": boolean;
  "overtime.yearlyLimitHours": number;
  "overtime.payRate": number;
  "overtime.compensation": "pay" | "rest" | "both";
  "overtime.restEquivalentHours": number;
  "overtime.restMaxWeeks": number;
  "complementaryHours.enabled": boolean;
  "nightShift.enabled": boolean;
  "nightShift.startTime": string;
  "nightShift.endTime": string;
  "nightShift.dailyHoursMaxNight": number;
  "nightShift.overtimeAllowed": boolean;
  "nightShift.supplementType": "percentage" | "fixed_per_hour" | "none";
  "nightShift.supplementValue": number;
  "complementaryHours.limitPercent": number;
  "complementaryHours.noticeDays": number;
  "complementaryHours.payRate": number;
  "holidayWork.enabled": boolean;
  "holidayWork.supplementType": "percentage" | "fixed_per_hour" | "rest_day" | "none";
  "holidayWork.supplementValue": number;
  "sundayWork.enabled": boolean;
  "sundayWork.supplementType": "percentage" | "fixed_per_hour" | "rest_day" | "none";
  "sundayWork.supplementValue": number;
}>;
```

Los overrides usan una allowlist explícita. La UI no puede enviar rutas arbitrarias aunque la representación sea dot-notation.

El coste se gestiona fuera de los overrides operativos:

```typescript
type ContractCostOverride = {
  hourlyRateBase: number;
  currency: "EUR";
  updatedAt: Date;
  updatedBy: string;
};
```

Solo owner/admin de entidad puede crear, ver o modificar `cost` y `ContractCostOverride`.

---

## 5. Paths de Firestore

```
entities/{entityId}/contractProfiles/{profileId}   ← plantillas (solo editable desde entidad)

// Campos aditivos en documentos existentes:
entities/{entityId}/branches/{branchId}
  + defaultContractProfileId?: string
  + contractOverrides?: ContractFieldOverrides

entities/{entityId}/employees/{employeeId}
  + contractProfilesByBranch?: {
      [branchId]: EmployeeBranchContractProfile
    }

entities/{entityId}/contractAggregates/{employeeId}_{year}
  + acumulados contractuales idempotentes por año

entities/{entityId}/contractAggregates/{employeeId}_{year}/processedChecklogs/{checkoutId}
  + contribución idempotente de cada checkout procesado
```

---

## 6. Algoritmo de Resolución

Solo se ejecuta cuando `employee.contractProfilesByBranch[branchId].enabled = true`.

El opt-in es deliberado: aunque exista perfil default de entidad o perfil por defecto de sucursal, el sistema no aplica cálculo contractual a un empleado/sucursal hasta que ese switch esté activo. Esto preserva el comportamiento histórico por defecto.

```
1. Determinar perfil base:
   a. employee.contractProfilesByBranch[branchId].contractProfileId → cargar ese perfil
   b. Si null → branch.defaultContractProfileId → cargar ese perfil
   c. Si null → perfil con isDefault:true de la entidad
   d. Si no hay ninguno → tratar como switch OFF (fallback seguro, sin error)

2. Aplicar branch.contractOverrides sobre el perfil base (deep-merge dot-notation)

3. Aplicar employee.contractProfilesByBranch[branchId].contractOverrides sobre el resultado del paso 2

4. Resultado: perfil efectivo listo para cálculos
```

La respuesta del endpoint `resolve` incluye `sources` por campo (igual que el calendario) para que el frontend pueda mostrar los badges de herencia.

### Invariantes de resolución

- Solo puede existir un `ContractProfile` con `isDefault = true` y `status = "active"` por entidad.
- Al marcar un perfil como default, el backend debe desmarcar el default anterior en la misma operación lógica.
- Un perfil `archived` no se puede asignar a nuevas sucursales o empleados.
- Si una sucursal o empleado-sucursal ya apuntaba a un perfil que luego pasa a `archived`, el resolve lo sigue usando para asignaciones existentes hasta que se reasigne manualmente. `archived` solo bloquea nuevas asignaciones.
- Si hay referencias rotas (`contractProfileId` inexistente), el resolve no falla el flujo de fichaje: registra warning técnico y actúa como switch OFF.

### Shape de respuesta `resolve`

```typescript
interface ResolvedContractProfile {
  enabled: boolean;
  profileId?: string;
  profileVersion?: number;
  effectiveTerms?: ContractEffectiveTermsSnapshot;
  cost?: { hourlyRateBase: number; currency: "EUR" }; // solo si el actor tiene permiso económico
  sources: Record<string, "profile" | "branch" | "employee">;
  chain: {
    profile?: Pick<ContractProfile, "id" | "name" | "version">;
    branchOverrides?: ContractFieldOverrides;
    employeeBranchOverrides?: ContractFieldOverrides;
  };
}
```

---

## 7. Integración con Capas Existentes (todo aditivo)

### Checklog — al cerrar turno (checkout)

Si `contractProfilesByBranch[branchId].enabled = true`, se añaden campos al documento del checklog **sin tocar los existentes**:

```typescript
overtimeMinutes?: number;           // horas que superan la jornada contratada del día
complementaryMinutes?: number;      // solo part_time, dentro del límite configurado
nightShiftMinutes?: number;         // minutos dentro de la franja nocturna configurada
isHolidayWork?: boolean;
isSundayWork?: boolean;
contractProfileSnapshot?: {
  profileId: string;
  profileVersion: number;
  profileName: string;
  resolvedAt: Date;
  effectiveTerms: ContractEffectiveTermsSnapshot;
  sources: Record<string, "profile" | "branch" | "employee">;
};                                  // snapshot mínimo para auditoría histórica
```

### `ContractEffectiveTermsSnapshot`

```typescript
type ContractEffectiveTermsSnapshot = Pick<
  ContractProfile,
  | "contractType"
  | "weeklyHoursContracted"
  | "dailyHoursMax"
  | "minRestBetweenShiftsHours"
  | "overtime"
  | "complementaryHours"
  | "nightShift"
  | "holidayWork"
  | "sundayWork"
>;
```

El snapshot no guarda `cost.hourlyRateBase`. El coste contractual se resuelve en reporting autorizado o se guarda en agregados restringidos, no en cada checklog.

### Reglas de cálculo V1

- El cálculo se ejecuta solo en checkout válido y solo si el empleado tiene `contractProfilesByBranch[branchId].enabled = true`.
- La jornada diaria de referencia sale de `contractedMinutesForDate({effectiveCalendar, effectiveTerms, dateLocal, branchId, timezone})`. Si no existe calendario resuelto, se usa `weeklyHoursContracted / 5` como fallback técnico y se marca `contractSummary.estimated = true`.
- `overtimeMinutes` en `full_time` son los minutos trabajados netos que superan la jornada diaria de referencia.
- `complementaryMinutes` en `part_time` se calculan contra el acumulado del periodo configurado, no solo contra una jornada aislada.
- V1 computa complementarias por branch. El límite semanal de cada branch se deriva de `weeklyHoursContracted * complementaryHours.limitPercent / 100` del perfil efectivo de ese `employeeId + branchId`.
- El control global multi-branch queda fuera de V1 y se documenta como V2.
- En `part_time`, los minutos por encima del límite complementario pasan a `overtimeMinutes`.
- `nightShiftMinutes` se calcula por intersección entre el intervalo trabajado real y la franja `nightShift.startTime/endTime`, usando la timezone efectiva del checklog.
- La intersección nocturna debe soportar franjas que cruzan medianoche y cambios DST.
- `isHolidayWork` se resuelve contra el calendario efectivo del día; `isSundayWork` se calcula desde la fecha local efectiva.
- Las pausas ya descontadas del neto del checklog no se vuelven a descontar.

### Agregados contractuales idempotentes

Las métricas acumuladas no se derivan incrementalmente solo desde el último evento. V1 mantiene un agregado anual por empleado:

```typescript
interface ContractAggregate {
  id: string; // `${employeeId}_${year}`
  entityId: string;
  employeeId: string;
  year: number;
  branchBreakdown: Record<string, {
    overtimeMinutesYTD: number;
    complementaryMinutesYTD: number;
    nightShiftMinutesYTD: number;
    holidayWorkMinutesYTD: number;
    sundayWorkMinutesYTD: number;
  }>;
  updatedAt: Date;
}

interface ContractProcessedChecklogContribution {
  checkoutId: string;
  branchId: string;
  employeeId: string;
  year: number;
  overtimeMinutes: number;
  complementaryMinutes: number;
  nightShiftMinutes: number;
  holidayWorkMinutes: number;
  sundayWorkMinutes: number;
  updatedAt: Date;
}
```

Cada checkout válido se aplica por `checkoutId`. Si el checkout cambia, se lee la contribución anterior en la subcolección `processedChecklogs/{checkoutId}`, se resta del agregado y se suma la nueva. Si se rechaza o deja de ser válido, se elimina su contribución. Esto evita duplicados por reintentos, triggers o reprocesos sin hacer crecer indefinidamente el documento anual.

La escritura del documento anual `contractAggregates/{employeeId}_{year}` y de `processedChecklogs/{checkoutId}` debe ejecutarse siempre en una transacción Firestore. No se permite actualizar el agregado y la contribución en escrituras separadas.

### Heurística — HeuristicCalculator

Añade bloque `contractMetrics` al `EmployeePattern` si el checklog tiene `contractProfileSnapshot`. Los campos actuales (`reliability`, `avgCostHour`, `avgCostEfficiency`, etc.) no se modifican.

```typescript
contractMetrics?: {
  overtimeHoursYTD: number;
  overtimeLimitPercent: number;       // % del límite anual consumido
  nightShiftHoursMonthly: number;
  avgOvertimeMinutesPerCycle: number; // EMA de extras por jornada
  contractualCostVariance?: number;   // coste real vs coste base contractual
};
```

`contractualCostVariance` solo se calcula en procesos autorizados que puedan leer coste contractual. No se calcula desde el snapshot del checklog porque el snapshot no contiene `cost`.

Alerta nueva (no reemplaza ninguna existente): cuando `overtimeLimitPercent >= 80` → notificación al manager.

### Daily reports

Añade `contractSummary?` al documento de reporte diario. La estructura existente no cambia.

### Panel de costes

Dos columnas nuevas en la tabla de empleados: horas extras (año) y % límite consumido. Solo visibles si hay al menos un empleado con el switch activo en esa sucursal.

### Informes

Nuevo informe disponible: desglose contractual mensual por empleado. Aparece en el selector de informes solo si la entidad tiene perfiles activos.

---

## 8. API HTTP

Todos los endpoints existentes permanecen sin cambio.

```
Handler base: `apiV100-firebaseEntryHttp-checkinbiz-contractProfilesHandler`

Headers: `Authorization: Bearer <sessionToken>`

Base path: `/contractProfiles`

POST   /contractProfiles
       body: { entityId, profile }

PUT    /contractProfiles/:id
       body: { entityId, profilePatch }

DELETE /contractProfiles/:id
       body: { entityId }
       → archivar perfil (bloquea nuevas asignaciones; conserva las existentes hasta reasignación)

GET    /contractProfiles?entityId=<entityId>&status=active|archived|all

GET    /contractProfiles/resolve?entityId=<entityId>&employeeId=<employeeId>&branchId=<branchId>

PATCH  /contractProfiles/branches/:branchId
       body: { entityId, defaultContractProfileId, contractOverrides }

PATCH  /contractProfiles/employees/:employeeId
       body: { entityId, branchId, enabled, contractProfileId, contractOverrides }

PATCH  /contractProfiles/:id/cost
       body: { entityId, cost }
```

Respuesta estándar exitosa:

```typescript
type ContractProfileResponse<T> = {
  code: string;
  data: T;
};
```

Respuesta de error:

```typescript
type ContractProfileError = {
  code: string;
  error: string;
  details?: string[];
};
```

El endpoint `resolve` devuelve el perfil final con `sources` por campo (para badges de herencia en UI) y `chain` con los overrides de cada nivel.

### Permisos V1

| Operación | Owner/Admin entidad | Owner operativo | Manager branch | Supervisor branch | Worker |
|---|:---:|:---:|:---:|:---:|:---:|
| Crear/editar/archivar perfiles base | sí | no | no | no | no |
| Duplicar perfil base | sí | no | no | no | no |
| Marcar perfil default de entidad | sí | no | no | no | no |
| Asignar perfil por defecto a sucursal | sí | sí | sí (misma sucursal) | no | no |
| Editar overrides de sucursal | sí | sí | sí (misma sucursal) | no | no |
| Activar switch en empleado | sí | sí (misma sucursal) | sí (misma sucursal) | no | no |
| Asignar perfil directo a empleado | sí | sí (misma sucursal) | sí (misma sucursal) | no | no |
| Editar overrides de empleado | sí | sí (misma sucursal) | sí (misma sucursal) | no | no |
| Consultar perfil efectivo propio | sí | sí | sí | sí | sí, solo propio |
| Consultar coste base contractual | sí | no | no | no | no |

El backend es la fuente de verdad. La UI solo oculta o muestra controles según estos permisos.

### Códigos de error V1

| Code | Status | Uso |
|---|---:|---|
| `contract_profile/bad_request` | 400 | Payload inválido |
| `contract_profile/not_found` | 404 | Perfil inexistente o fuera de entidad |
| `contract_profile/archived` | 409 | Intento de asignar perfil archivado |
| `contract_profile/default_conflict` | 409 | Conflicto al establecer default único |
| `contract_profile/assigned` | 409 | Operación incompatible con asignaciones activas |
| `contract_profile/invalid_override` | 400 | Override fuera de allowlist o tipo inválido |
| `contract_profile/unauthorized` | 403 | Actor sin permisos |
| `contract_profile/branch_required` | 400 | Operación de empleado sin `branchId` |

---

## 9. Casos de Uso

| Caso | Configuración |
|---|---|
| Empleado jornada completa 40h, sin extras | Perfil "JC 40h", `overtime.enabled: false`, switch ON |
| Igual pero con extras al 125% | `overtime.enabled: true`, `payRate: 1.25`, `compensation: "pay"` |
| Sucursal entera con nocturnidad al 30% | Perfil base sin nocturnidad + `contractOverrides` en sucursal con `nightShift.enabled: true, supplementValue: 30` |
| Empleado parcial 20h/semana | Perfil "Parcial 20h", `contractType: "part_time"`, `complementaryHours.enabled: true` |
| Empleado con mismo perfil de sucursal pero 32h | Selector hereda sucursal + override `weeklyHoursContracted: 32` en empleado |
| Manager que no quiere usar el módulo | Switch OFF (por defecto) → sistema funciona exactamente igual que hoy |

---

## 10. Presets de Sistema — España

Al crear una entidad, el sistema ofrece cargar automáticamente los presets de España como punto de partida. Son editables una vez creados; funcionan como cualquier otro perfil laboral de la entidad.

Los valores de cada preset se derivan directamente del **ET (RDL 2/2015)** y del **RDL 8/2019**. Donde la ley no fija un valor concreto (nocturnidad, festivos), se usa el rango habitual de convenio general. Ver referencias legales completas en la sección 11.

---

### Preset 1 — Jornada Completa Estándar (España)

Empleado a tiempo completo sin condiciones especiales. Configuración mínima legal.

```json
{
  "name": "Jornada completa estándar (España)",
  "isDefault": true,
  "contractType": "full_time",
  "weeklyHoursContracted": 40,
  "dailyHoursMax": 9,
  "minRestBetweenShiftsHours": 12,

  "overtime": {
    "enabled": true,
    "yearlyLimitHours": 80,
    "compensation": "pay",
    "payRate": 1.0,
    "restEquivalentHours": 1.0,
    "restMaxWeeks": 16
  },

  "complementaryHours": {
    "enabled": false,
    "limitPercent": 0,
    "noticeDays": 3,
    "payRate": 1.0
  },

  "nightShift": {
    "enabled": false,
    "startTime": "22:00",
    "endTime": "06:00",
    "dailyHoursMaxNight": 8,
    "overtimeAllowed": false,
    "supplementType": "none",
    "supplementValue": 0
  },

  "holidayWork": {
    "enabled": false,
    "supplementType": "none",
    "supplementValue": 0
  },

  "sundayWork": {
    "enabled": false,
    "supplementType": "none",
    "supplementValue": 0
  }
}
```

> `payRate: 1.0` es el mínimo legal (ET Art. 35.1: la hora extra se abona "en cuantía no inferior a la hora ordinaria"). Ajustar al alza según convenio colectivo aplicable.

---

### Preset 2 — Jornada Completa con Horas Extras Mejoradas (España)

Mismo régimen que el anterior pero con el plus habitual de convenio para horas extras (25 % sobre tarifa base) y compensación mixta (pago o descanso a elección).

```json
{
  "name": "Jornada completa + extras al 125% (España)",
  "isDefault": false,
  "contractType": "full_time",
  "weeklyHoursContracted": 40,
  "dailyHoursMax": 9,
  "minRestBetweenShiftsHours": 12,

  "overtime": {
    "enabled": true,
    "yearlyLimitHours": 80,
    "compensation": "both",
    "payRate": 1.25,
    "restEquivalentHours": 1.5,
    "restMaxWeeks": 16
  },

  "complementaryHours": { "enabled": false, "limitPercent": 0, "noticeDays": 3, "payRate": 1.0 },
  "nightShift": { "enabled": false, "startTime": "22:00", "endTime": "06:00",
                  "dailyHoursMaxNight": 8, "overtimeAllowed": false,
                  "supplementType": "none", "supplementValue": 0 },
  "holidayWork": { "enabled": true, "supplementType": "percentage", "supplementValue": 75 },
  "sundayWork":  { "enabled": true, "supplementType": "percentage", "supplementValue": 0 }
}
```

---

### Preset 3 — Turno Nocturno (España)

Para trabajadores nocturnos habituales. La ley prohíbe horas extras en este régimen (ET Art. 36.1). El complemento de nocturnidad es del 25 % (mínimo habitual de convenio general; ajustar por sector).

```json
{
  "name": "Turno nocturno (España)",
  "isDefault": false,
  "contractType": "full_time",
  "weeklyHoursContracted": 40,
  "dailyHoursMax": 8,
  "minRestBetweenShiftsHours": 12,

  "overtime": {
    "enabled": false,
    "yearlyLimitHours": 0,
    "compensation": "rest",
    "payRate": 1.0,
    "restEquivalentHours": 1.0,
    "restMaxWeeks": 16
  },

  "complementaryHours": { "enabled": false, "limitPercent": 0, "noticeDays": 3, "payRate": 1.0 },

  "nightShift": {
    "enabled": true,
    "startTime": "22:00",
    "endTime": "06:00",
    "dailyHoursMaxNight": 8,
    "overtimeAllowed": false,
    "supplementType": "percentage",
    "supplementValue": 25
  },

  "holidayWork": { "enabled": true, "supplementType": "percentage", "supplementValue": 75 },
  "sundayWork":  { "enabled": true, "supplementType": "percentage", "supplementValue": 25 }
}
```

> `overtimeAllowed: false` no es un ajuste de empresa — es un requisito legal (ET Art. 36.1). El motor de cálculo lo trata como valor no editable en la UI cuando `nightShift.enabled = true`.

---

### Preset 4 — Contrato a Tiempo Parcial 20h (España)

Para empleados con jornada reducida. Las horas que exceden las 20h contratadas son **horas complementarias** (no extraordinarias) hasta el límite del 30 % (ET Art. 12.5).

```json
{
  "name": "Tiempo parcial 20h/semana (España)",
  "isDefault": false,
  "contractType": "part_time",
  "weeklyHoursContracted": 20,
  "dailyHoursMax": 6,
  "minRestBetweenShiftsHours": 12,

  "overtime": {
    "enabled": false,
    "yearlyLimitHours": 0,
    "compensation": "pay",
    "payRate": 1.0,
    "restEquivalentHours": 1.0,
    "restMaxWeeks": 16
  },

  "complementaryHours": {
    "enabled": true,
    "limitPercent": 30,
    "noticeDays": 3,
    "payRate": 1.0
  },

  "nightShift": { "enabled": false, "startTime": "22:00", "endTime": "06:00",
                  "dailyHoursMaxNight": 8, "overtimeAllowed": false,
                  "supplementType": "none", "supplementValue": 0 },
  "holidayWork": { "enabled": false, "supplementType": "none", "supplementValue": 0 },
  "sundayWork":  { "enabled": false, "supplementType": "none", "supplementValue": 0 }
}
```

> El `limitPercent: 30` es el techo legal. Si el convenio colectivo lo eleva hasta 60 %, se edita este campo en el perfil desde el menú "Perfiles laborales" de la entidad.

---

### Campos bloqueados por ley en la UI

Algunos campos tienen un tope legal que la UI no debe permitir superar, independientemente de lo que el manager introduzca:

| Campo | Límite legal | Fuente | Comportamiento UI |
|---|---|---|---|
| `weeklyHoursContracted` | ≤ 40 h | ET Art. 34.1 | Warning si se supera; no bloquea (puede haber convenio que permita excepciones pactadas) |
| `overtime.yearlyLimitHours` | ≤ 80 h | ET Art. 35.2 | Warning si se supera |
| `minRestBetweenShiftsHours` | ≥ 12 h | ET Art. 34.3 | Bloqueo hard — no se permite guardar menos de 12 |
| `nightShift.dailyHoursMaxNight` | ≤ 8 h (media 15 días) | ET Art. 36.1 | Warning si se supera |
| `nightShift.overtimeAllowed` cuando `nightShift.enabled = true` | `false` por ley | ET Art. 36.1 | Campo deshabilitado en UI, tooltip explicativo |
| `complementaryHours.limitPercent` | ≤ 30 % (≤ 60 % con CT) | ET Art. 12.5 | Warning con mensaje "requiere convenio colectivo" si se supera 30 % |
| `complementaryHours.noticeDays` | ≥ 3 días | ET Art. 12.5 | Bloqueo hard — no se permite guardar menos de 3 |

---

## 11. Referencias Legales

Ver documento completo: [`DOCS/modulos/marco-legal-jornada.md`](./marco-legal-jornada.md)

| Norma | BOE | Artículos relevantes para este módulo |
|---|---|---|
| Real Decreto Legislativo 2/2015 — Estatuto de los Trabajadores | BOE-A-2015-11430 | Art. 12 (parcial y complementarias), Art. 34 (jornada), Art. 35 (horas extras), Art. 36 (nocturnidad), Art. 37 (descansos y festivos), Art. 38 (vacaciones) |
| Real Decreto-ley 8/2019 — Registro de jornada | BOE-A-2019-3481 | Art. 10 (modifica ET Art. 34.9): registro diario inicio/fin, conservación 4 años |
| Real Decreto Legislativo 5/2000 — LISOS | BOE-A-2000-15060 | Art. 7 y Art. 8; cuantías a verificar contra texto consolidado vigente antes de comunicar a cliente |
| Criterio Técnico ITSS 101/2019 | — | Criterios inspectores sobre registro de jornada |

**Nota de aplicación:** los valores de los presets cumplen los mínimos del ET. Cuando existe un convenio colectivo sectorial o de empresa, algunos valores (complemento de nocturnidad, plus de festivo, límite de horas complementarias) deben ajustarse al convenio aplicable editando el perfil desde "Perfiles laborales". El sistema no interpreta convenios automáticamente.

---

## 12. Rollout sin Riesgo

| Paso | Quién actúa | Efecto |
|---|---|---|
| 1. Deploy del módulo | Equipo técnico | Solo añade la colección y campos opcionales. Cero cambios en comportamiento. |
| 2. Crear perfiles en entidad | Manager desde nuevo menú "Perfiles laborales" | Sin efecto hasta asignar. |
| 3. Asignar perfil a sucursal | Manager en ficha de sucursal | Sin efecto hasta que empleados tengan switch ON. |
| 4. Activar switch en empleado | Manager en ficha del empleado | Solo afecta a ese empleado. El siguiente checklog ya usa el perfil. |
| 5. Nuevas métricas en heurística | Automático | Aparecen en el patrón del empleado tras el primer checkout con switch activo. |
