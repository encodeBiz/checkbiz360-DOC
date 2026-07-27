# Módulo ContractProfile — Perfiles Laborales

> Estado: propuesta de ingeniería V1 en validación de arquitectura. Pendiente de aprobación por arquitectura jefe.
> Fuente canónica para backend, backoffice, app móvil y reporting contractual.

## Restricción de Diseño (no negociable)

> **Nada se elimina ni se modifica en el comportamiento existente.**
> El módulo se activa mediante un switch por empleado y sucursal (`contractProfilesByBranch[branchId].enabled`).
> Cuando el switch está desactivado (por defecto), todos los cálculos, estructuras de datos
> y respuestas de API funcionan exactamente igual que hoy.
> Los nuevos campos son siempre aditivos en los documentos Firestore y en las respuestas HTTP.

## Principio de Producto — Plantillas Orientativas, No Enforcement Legal

Los perfiles laborales son **plantillas configurables**, no un motor de cumplimiento legal que impone una única interpretación normativa.

V1 incluye plantillas detalladas para España porque es la jurisdicción documentada actualmente. Para cualquier entidad fuera de España, el sistema debe ofrecer al menos una plantilla básica neutra, sin asumir límites legales locales que no estén documentados. Cuando en el futuro se añadan plantillas por país/estado/sector, cada plantilla deberá declarar su jurisdicción, fuente y fecha de revisión.

Las reglas basadas en marco legal generan `warnings` visibles y auditables, pero no bloquean la edición ni el guardado de una plantilla. La responsabilidad final de configurar condiciones laborales compatibles con contratos, acuerdos, convenios y normativa aplicable recae en el administrador de la entidad. CheckBiz360 no debe presentarse como asesor jurídico ni como sustituto de revisión legal profesional.

**Excepción:** el backend sí puede rechazar datos técnicamente inválidos o corruptos (`dailyHoursMax <= 0`, porcentajes negativos, tipos incorrectos, referencias fuera de entidad, payloads fuera de allowlist). Eso es validación de integridad del sistema, no enforcement legal.

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
  jurisdiction: "generic" | "ES" | string; // plantilla normativa declarada; "generic" no aplica reglas legales locales
  name: string;           // "Jornada completa 40h", "Turno noche almacén"
  isDefault: boolean;     // fallback cuando no hay perfil asignado en sucursal/empleado
  version: number;        // empieza en 1, incrementa en cada edición
  status: "active" | "archived";
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;  // uid del creador
  updatedBy: string;  // uid del último editor de campos contractuales

  // Jornada base
  contractType: "full_time" | "part_time";
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
    restMaxMonths: number;            // plazo para compensar (ET: 4 meses calendario)
  };

  // Horas complementarias (part_time)
  complementaryHours: {
    enabled: boolean;
    pactLimitPercent: number;         // pactadas: máx 30 % (60 % con convenio)
    voluntaryEnabled: boolean;        // voluntarias adicionales
    voluntaryLimitPercent: number;    // máx 15 % adicional (30 % con convenio)
    noticeDays: number;               // mín 3 días ET
    payRate: number;
  };

  // Nocturnidad
  nightShift: {
    enabled: boolean;
    startTime: string;                // "22:00" (ET default)
    endTime: string;                  // "06:00" (ET default)
    dailyHoursMaxNight: number;       // 8 (ET Art. 36)
    overtimeAllowed: boolean;         // si contradice la plantilla legal, genera warning
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
    currency: string;  // ISO 4217; default desde la moneda configurada en la entidad
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
  "overtime.restMaxMonths": number;
  "complementaryHours.enabled": boolean;
  "nightShift.enabled": boolean;
  "nightShift.startTime": string;
  "nightShift.endTime": string;
  "nightShift.dailyHoursMaxNight": number;
  "nightShift.overtimeAllowed": boolean;
  "nightShift.supplementType": "percentage" | "fixed_per_hour" | "none";
  "nightShift.supplementValue": number;
  "complementaryHours.pactLimitPercent": number;
  "complementaryHours.voluntaryEnabled": boolean;
  "complementaryHours.voluntaryLimitPercent": number;
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

`contractType` no es overrideable por diseño. Si una sucursal o empleado cambia de jornada completa a tiempo parcial, debe asignarse un perfil base distinto con `contractType` correcto. El backend debe validar que el perfil asignado sea compatible con la configuración laboral esperada; no se permite convertir un perfil `full_time` en `part_time` mediante overrides.

`nightShift.overtimeAllowed` es editable porque las plantillas son configurables por el cliente. Si la plantilla de España detecta `nightShift.enabled = true` y `nightShift.overtimeAllowed = true`, el backend debe devolver un warning legal auditable, no rechazar el guardado.

`fixed_discontinuous` queda fuera de V1. Se reserva para V2 porque requiere reglas propias de llamamiento, periodos de actividad/inactividad y cómputo de jornada de referencia.

El coste se gestiona fuera de los overrides operativos:

```typescript
type ContractCostOverride = {
  hourlyRateBase: number;
  currency: string; // ISO 4217
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

entities/{entityId}/contractAggregates/{employeeId}#{year}
  + acumulados contractuales idempotentes por año

entities/{entityId}/contractAggregates/{employeeId}#{year}/processedChecklogs/{checkoutId}
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
- Al marcar un perfil como default, el backend debe desmarcar el default anterior en una única transacción Firestore. No se permiten dos escrituras secuenciales independientes.
- Un perfil `archived` no se puede asignar a nuevas sucursales o empleados.
- Si una sucursal o empleado-sucursal ya apuntaba a un perfil que luego pasa a `archived`, el resolve lo sigue usando para asignaciones existentes hasta que se reasigne manualmente. `archived` solo bloquea nuevas asignaciones.
- Si hay referencias rotas (`contractProfileId` inexistente), el resolve no falla el flujo de fichaje: registra warning técnico y actúa como switch OFF.
- Cada responsabilidad activa `employeeId + branchId` debe tener una decisión contractual auditable: switch ON con perfil heredado/asignado, o switch OFF explícito. La ausencia de entrada en `contractProfilesByBranch[branchId]` se trata como OFF por compatibilidad, pero debe aparecer como gap de configuración en backoffice.
- `version` empieza en 1 y se incrementa solo cuando cambian campos de contenido contractual del perfil base. Cambios de `name`, `status`, `isDefault` o asignaciones externas no modifican la versión contractual. El archivado no incrementa `version`; solo cambia `status`.
- Al activar el switch `enabled` en un `EmployeeBranchContractProfile`, el perfil se resuelve en el momento del **checkout**, no del checkin. Si el empleado ya tiene un turno abierto cuando el manager activa el switch, ese turno en curso se calcula con el perfil activo en el momento del cierre. No hay retroactividad al checkin. La UI debe mostrar el aviso: *"El siguiente cierre de turno usará el nuevo perfil laboral."* La misma regla aplica al desactivar el switch: el turno en curso se cierra con el perfil que estaba activo al momento del checkout.

### Shape de respuesta `resolve`

```typescript
interface ResolvedContractProfile {
  enabled: boolean;
  profileId?: string;
  profileVersion?: number;
  effectiveTerms?: ContractEffectiveTermsSnapshot;
  cost?: { hourlyRateBase: number; currency: string }; // solo si el actor tiene permiso económico
  warnings?: ContractProfileWarning[];
  sources: Record<string, "profile" | "branch" | "employee">;
  chain: {
    profile?: Pick<ContractProfile, "id" | "name" | "version">;
    branchOverrides?: ContractFieldOverrides;
    employeeBranchOverrides?: ContractFieldOverrides;
  };
}
```

```typescript
type ContractProfileWarning = {
  code: string;
  severity: "info" | "warning" | "critical";
  field?: string;
  jurisdiction?: string; // ej. "ES"
  message: string;
  source: "template" | "resolve" | "checkout" | "reporting";
};
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

`effectiveTerms` contiene siempre los valores ya resueltos tras aplicar perfil base, overrides de sucursal y overrides de empleado-sucursal. No se guarda el perfil raw.

Si un checklog ya tiene `contractProfileSnapshot`, cualquier reproceso ordinario debe usar ese snapshot como fuente contractual. Solo una migración o recálculo forense autorizado puede resolver de nuevo contra perfiles actuales.

### Reglas de cálculo V1

- El cálculo se ejecuta solo en checkout válido y solo si el empleado tiene `contractProfilesByBranch[branchId].enabled = true`.
- La jornada diaria de referencia sale de `contractedMinutesForDate({effectiveCalendar, effectiveTerms, dateLocal, branchId, timezone})`. Si no existe calendario resuelto, se usa `weeklyHoursContracted / 5` como fallback técnico y se marca `contractSummary.estimated = true`.
- `overtimeMinutes` en `full_time` son los minutos trabajados netos que superan la jornada diaria de referencia.
- `complementaryMinutes` en `part_time` se calculan contra el acumulado del periodo configurado, no solo contra una jornada aislada.
- V1 computa complementarias por branch. El límite semanal de cada branch se deriva de `weeklyHoursContracted * (complementaryHours.pactLimitPercent + voluntaryLimitPercentAplicable) / 100` del perfil efectivo de ese `employeeId + branchId`.
- El control global multi-branch queda fuera de V1 y se documenta como deuda V2 obligatoria: `CONTRACTS-V2-GLOBAL-COMPLEMENTARY-HOURS`. V1 no debe comunicarse como cumplimiento legal global para empleados multi-branch; solo alerta por sucursal.
- En `part_time`, los minutos por encima del límite complementario pasan a `overtimeMinutes` para clasificación legal y alertas aunque `overtime.enabled = false`. En ese caso `overtime.enabled = false` significa "no permitido/planificado", no "sin coste"; la compensación usa `overtime.payRate` con mínimo 1.0 salvo configuración más protectora.
- `nightShiftMinutes` se calcula por intersección entre el intervalo trabajado real y la franja `nightShift.startTime/endTime`, usando la timezone efectiva del checklog.
- La intersección nocturna debe soportar franjas que cruzan medianoche y cambios DST. Estrategia V1: el checklog se almacena como instantes UTC; el cálculo proyecta el intervalo a la timezone IANA efectiva del branch/checklog, divide por días locales y calcula la intersección contra ventanas locales. En horas ambiguas por cambio DST, se cuenta el tiempo real transcurrido entre instantes, no la diferencia textual de reloj.
- `isHolidayWork` se resuelve contra el calendario efectivo del día; `isSundayWork` se calcula desde la fecha local efectiva.
- `holidayWorkMinutesYTD` acumula los minutos netos trabajados en checklogs cuyo día local efectivo sea festivo según calendario efectivo. `sundayWorkMinutesYTD` acumula los minutos netos trabajados en domingo local. V1 no parte turnos por tramos parciales de festivo salvo cruce de día local; si un turno cruza medianoche, se divide por día local antes de acumular.
- Las pausas ya descontadas del neto del checklog no se vuelven a descontar.
- Si no existe calendario resuelto, el fallback `weeklyHoursContracted / 5` asume semana laboral de cinco días y debe marcar `estimatedReason = "missing_effective_calendar"`. Este fallback no es válido para cumplimiento legal estricto en jornadas de 4, 6 o 7 días.
- **Clasificación como trabajador nocturno habitual (ET Art. 36):** el sistema no clasifica automáticamente a un empleado como "trabajador nocturno" al superar el umbral legal (≥ 3 h/noche de forma habitual o ≥ 1/3 de jornada anual en franja nocturna). Esta funcionalidad queda como deuda V2: `CONTRACTS-V2-NOCTURNAL-WORKER-CLASSIFICATION`.
- **Menores de 18 años:** el ET prohíbe absolutamente horas extraordinarias y trabajo nocturno para menores. El sistema no valida la edad del empleado contra la configuración del perfil. Es responsabilidad del manager asignar perfiles compatibles. V2 debe añadir validación de `employeeBirthDate` contra `overtime.enabled` y `nightShift.enabled`.
- **Pausa mínima legal (ET Art. 34.4):** si la jornada efectiva supera 6 h continuas, el trabajador tiene derecho a 15 min de pausa (infracción grave LISOS Art. 7 si no se respeta). V1 no valida ni alerta sobre ausencia de pausa en turnos largos. Queda como deuda V2: `CONTRACTS-V2-BREAK-VALIDATION`.

### Agregados contractuales idempotentes

Las métricas acumuladas no se derivan incrementalmente solo desde el último evento. V1 mantiene un agregado anual por empleado:

```typescript
interface ContractAggregate {
  id: string; // `${employeeId}#${year}`
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
  // Nota de tamaño: branchBreakdown crece un entry por branchId activo en el año.
  // Para empleados con alta rotación de sucursales, monitorizar tamaño del documento.
  // Si supera ~200 entradas, migrar a subcolección por branch (deuda V2: CONTRACTS-V2-AGGREGATE-SHARDING).
  updatedAt: Date;
}

interface ContractProcessedChecklogContribution {
  checkoutId: string;
  entityId: string;
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

La escritura del documento anual `contractAggregates/{employeeId}#{year}` y de `processedChecklogs/{checkoutId}` debe ejecutarse siempre en una transacción Firestore. No se permite actualizar el agregado y la contribución en escrituras separadas.

### Heurística — HeuristicCalculator

Añade bloque `contractMetrics` al `EmployeePattern` si el checklog tiene `contractProfileSnapshot`. Los campos actuales (`reliability`, `avgCostHour`, `avgCostEfficiency`, etc.) no se modifican.

```typescript
contractMetrics?: {
  overtimeHoursYTD: number;
  overtimeLimitPercent: number;              // % del límite anual consumido
  nightShiftHoursMonthly: number;            // horas nocturnas del mes natural en curso
                                             // = (nightShiftMinutesYTD_hoy
                                             //    - _nightShiftMinutesAtStartOfMonth) / 60
                                             // HeuristicCalculator persiste _nightShiftMinutesAtStartOfMonth
                                             // en EmployeePattern al inicio de cada mes natural.
  avgOvertimeMinutesPerCycle: number;        // EMA de extras por jornada
  contractualCostVariance?: number;          // coste real vs coste base contractual
};
```

`contractualCostVariance` solo se calcula en procesos autorizados que puedan leer coste contractual. No se calcula desde el snapshot del checklog porque el snapshot no contiene `cost`.

Alerta nueva (no reemplaza ninguna existente): cuando `overtimeLimitPercent >= 80` → notificación al manager. El umbral del 80 % está fijo en V1 por diseño. Configurarlo por perfil o entidad queda registrado como deuda V2: `CONTRACTS-V2-OVERTIME-ALERT-THRESHOLD`.

### Daily reports

Añade `contractSummary?` al documento de reporte diario. La estructura existente no cambia.

```typescript
interface ContractDailySummary {
  profileId: string;
  profileVersion: number;
  contractType: "full_time" | "part_time";
  overtimeMinutes: number;
  complementaryMinutes: number;
  nightShiftMinutes: number;
  isHolidayWork: boolean;
  isSundayWork: boolean;
  estimated: boolean;         // true si se usó el fallback weeklyHoursContracted/5
  estimatedReason?: string;   // ej. "missing_effective_calendar"
}
```

### Panel de costes

Dos columnas nuevas en la tabla de empleados: horas extras (año) y % límite consumido. Solo visibles si hay al menos un empleado con el switch activo en esa sucursal.

### Informes

Nuevo informe disponible: desglose contractual mensual por empleado. Aparece en el selector de informes solo si la entidad tiene perfiles activos.

Estructura mínima V1:

| Columna | Descripción | Visibilidad |
|---|---|---|
| Empleado | Nombre y employeeId | roles con acceso a reportes |
| Sucursal | branchId/nombre | roles con acceso a la sucursal |
| Perfil laboral | nombre + version snapshot dominante del periodo | roles con acceso a reportes |
| Horas ordinarias | minutos netos no clasificados como extra/complementaria | roles con acceso a reportes |
| Horas complementarias | `complementaryMinutes` | roles con acceso a reportes |
| Horas extraordinarias | `overtimeMinutes` | roles con acceso a reportes |
| Nocturnidad | `nightShiftMinutes` | roles con acceso a reportes |
| Festivo/domingo | `holidayWorkMinutes` / `sundayWorkMinutes` | roles con acceso a reportes |
| Coste contractual estimado | calculado con coste contractual | solo owner/admin |

Filtros: `entityId`, rango mensual, `branchId?`, `employeeId?`, `contractProfileId?`. Exportación CSV/XLSX con las mismas reglas de visibilidad que la API.

---

## 8. API HTTP

Todos los endpoints existentes permanecen sin cambio.

```
Handler base: `apiV100-firebaseEntryHttp-checkinbiz-contractProfilesHandler`

Headers: `Authorization: Bearer <sessionToken>`

Base path: `/contractProfiles`

POST   /contractProfiles
       body: { entityId, profile }

PATCH  /contractProfiles/:id
       body: { entityId, profilePatch }
       // Semántica merge-partial: solo los campos presentes en profilePatch se actualizan.
       // Campos ausentes no se modifican. No se acepta reemplazo total del objeto.

POST   /contractProfiles/:id/archive
       body: { entityId }
       → archivar perfil (bloquea nuevas asignaciones; conserva las existentes hasta reasignación)

GET    /contractProfiles?entityId=<entityId>&status=active|archived|all&limit=<n>&cursor=<lastProfileId>
       // limit: número máximo de resultados por página (default 50, máx 200).
       // cursor: id del último perfil recibido; omitir para la primera página.

GET    /contractProfiles/resolve?entityId=<entityId>&employeeId=<employeeId>&branchId=<branchId>

PATCH  /contractProfiles/branches/:branchId
       body: { entityId, defaultContractProfileId, contractOverrides }
       // defaultContractProfileId: null  → elimina la asignación del perfil por defecto.
       // defaultContractProfileId omitido → no modifica el valor actual.
       // contractOverrides: null         → elimina todos los overrides de la sucursal.
       // El backend distingue null (borrar) de campo ausente (no tocar).

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
  warnings?: ContractProfileWarning[];
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
| `contract_profile/invalid_technical_value` | 400 | Payload técnicamente inválido o corrupto (tipo incorrecto, valor negativo imposible, referencia fuera de entidad) |
| `contract_profile/unauthorized` | 403 | Actor sin permisos |
| `contract_profile/branch_required` | 400 | Operación de empleado sin `branchId` |

Las discrepancias contra una plantilla legal no devuelven error 4xx. Se devuelven como `warnings` en la respuesta y quedan disponibles para auditoría/reporting.

### Firestore Rules mínimas V1

- `contractProfiles`: lectura para owner/admin y responsables autorizados de la entidad; escritura solo owner/admin. El campo `cost` no debe exponerse a roles no económicos.
- `branches.defaultContractProfileId` y `branches.contractOverrides`: escritura owner/admin y roles operativos autorizados sobre la misma sucursal según la tabla de permisos; validación backend obligatoria.
- `employees.contractProfilesByBranch`: escritura solo sobre branches donde el actor tenga permiso operativo; worker no puede modificarlo.
- `contractAggregates` y `processedChecklogs`: lectura restringida a owner/admin y reporting autorizado; escritura solo backend/Cloud Functions.
- Reglas deny-by-default; la UI no es control de seguridad.
- Las Firestore Rules validan permisos, pertenencia a entidad, allowlist de campos y tipos básicos. No deben bloquear configuraciones por criterio legal de una plantilla; esos casos se gestionan como warnings de aplicación.

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

## 10. Presets de Sistema

Al crear una entidad, el sistema ofrece siempre una plantilla básica neutra. Si la entidad selecciona España como jurisdicción operativa, puede cargar además los presets de España como punto de partida. Son editables una vez creados; funcionan como cualquier otro perfil laboral de la entidad.

Solo puede quedar un perfil `isDefault = true` por entidad. Si se cargan la plantilla básica y presets de España en el mismo onboarding, el asistente debe pedir cuál queda como default o aplicar el default según la jurisdicción elegida.

Los valores de los presets de España se derivan del **ET (RDL 2/2015)** y del **RDL 8/2019**. Donde la ley no fija un valor concreto (nocturnidad, festivos), se usa el rango habitual de convenio general. Ver referencias legales completas en la sección 11. Estos presets son orientación configurable, no enforcement legal.

---

### Preset 0 — Perfil Básico Internacional

Plantilla mínima para entidades sin jurisdicción detallada configurada. No intenta interpretar normativa local.

```json
{
  "name": "Perfil laboral básico",
  "isDefault": true,
  "jurisdiction": "generic",
  "contractType": "full_time",
  "weeklyHoursContracted": 40,
  "dailyHoursMax": 8,
  "minRestBetweenShiftsHours": 0,

  "overtime": {
    "enabled": false,
    "yearlyLimitHours": 0,
    "compensation": "pay",
    "payRate": 1.0,
    "restEquivalentHours": 1.0,
    "restMaxMonths": 1
  },

  "complementaryHours": {
    "enabled": false,
    "pactLimitPercent": 0,
    "voluntaryEnabled": false,
    "voluntaryLimitPercent": 0,
    "noticeDays": 0,
    "payRate": 1.0
  },

  "nightShift": {
    "enabled": false,
    "startTime": "22:00",
    "endTime": "06:00",
    "dailyHoursMaxNight": 8,
    "overtimeAllowed": true,
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

> Este preset no genera warnings legales específicos porque no declara jurisdicción normativa. Solo aplica validaciones técnicas de integridad.

---

### Preset 1 — Jornada Completa Estándar (España)

Empleado a tiempo completo sin condiciones especiales. Configuración mínima legal.

```json
{
  "name": "Jornada completa estándar (España)",
  "isDefault": true,
  "jurisdiction": "ES",
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
    "restMaxMonths": 4
  },

  "complementaryHours": {
    "enabled": false,
    "pactLimitPercent": 0,
    "voluntaryEnabled": false,
    "voluntaryLimitPercent": 0,
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
  "jurisdiction": "ES",
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
    "restMaxMonths": 4
  },

  "complementaryHours": { "enabled": false, "pactLimitPercent": 0, "voluntaryEnabled": false, "voluntaryLimitPercent": 0, "noticeDays": 3, "payRate": 1.0 },
  "nightShift": { "enabled": false, "startTime": "22:00", "endTime": "06:00",
                  "dailyHoursMaxNight": 8, "overtimeAllowed": false,
                  "supplementType": "none", "supplementValue": 0 },
  "holidayWork": { "enabled": true, "supplementType": "percentage", "supplementValue": 75 },
  "sundayWork":  { "enabled": true, "supplementType": "percentage", "supplementValue": 0 }
}
```

> `sundayWork.enabled: true` con `supplementValue: 0` significa track-only: el sistema separa minutos trabajados en domingo para reporting, pero no aplica plus económico por defecto. Si el convenio exige plus dominical, debe ajustarse el `supplementValue`.

---

### Preset 3 — Turno Nocturno (España)

Para trabajadores nocturnos habituales. La ley prohíbe horas extras en este régimen (ET Art. 36.1). El complemento de nocturnidad es del 25 % (mínimo habitual de convenio general; ajustar por sector).

```json
{
  "name": "Turno nocturno (España)",
  "isDefault": false,
  "jurisdiction": "ES",
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
    "restMaxMonths": 4
  },

  "complementaryHours": { "enabled": false, "pactLimitPercent": 0, "voluntaryEnabled": false, "voluntaryLimitPercent": 0, "noticeDays": 3, "payRate": 1.0 },

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

> `overtimeAllowed: false` es el valor recomendado por la plantilla española según ET Art. 36.1. Si el administrador lo cambia, el sistema debe conservar el cambio y mostrar warning legal auditable.

---

### Preset 4 — Contrato a Tiempo Parcial 20h (España)

Para empleados con jornada reducida. Las horas que exceden las 20h contratadas son **horas complementarias** (no extraordinarias) hasta el límite del 30 % (ET Art. 12.5).

```json
{
  "name": "Tiempo parcial 20h/semana (España)",
  "isDefault": false,
  "jurisdiction": "ES",
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
    "restMaxMonths": 4
  },

  "complementaryHours": {
    "enabled": true,
    "pactLimitPercent": 30,
    "voluntaryEnabled": false,
    "voluntaryLimitPercent": 0,
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

> `pactLimitPercent: 30` es el techo legal ordinario para horas complementarias pactadas. Si el convenio colectivo lo eleva hasta 60 %, se edita este campo en el perfil desde el menú "Perfiles laborales" de la entidad. Las horas complementarias voluntarias se modelan por separado con `voluntaryEnabled` y `voluntaryLimitPercent`.

---

### Warnings legales y validaciones técnicas

Algunos campos tienen una referencia legal según la plantilla española. La UI debe avisar antes de guardar y el backend debe devolver `warnings`, pero no bloquear el guardado por criterio legal. Solo se bloquean valores técnicamente inválidos o corruptos.

| Campo | Referencia plantilla España | Fuente | Comportamiento |
|---|---|---|---|
| `weeklyHoursContracted` | ≤ 40 h | ET Art. 34.1 | Warning si se supera; permitir guardar |
| `dailyHoursMax` | > 0 h como integridad técnica; referencia España ≤ 9 h ordinarias | ET Art. 34.3 | Bloquear solo `<= 0`; warning si supera referencia legal |
| `overtime.yearlyLimitHours` | ≤ 80 h | ET Art. 35.2 | Warning si se supera; permitir guardar |
| `overtime.restMaxMonths` | > 0 como integridad técnica; referencia España ≤ 4 meses | ET Art. 35.1 | Bloquear solo `<= 0`; warning si supera referencia legal |
| `minRestBetweenShiftsHours` | ≥ 12 h | ET Art. 34.3 | Warning si baja de 12; permitir guardar |
| `nightShift.dailyHoursMaxNight` | ≤ 8 h (media 15 días) | ET Art. 36.1 | Warning si se supera; permitir guardar |
| `nightShift.overtimeAllowed` cuando `nightShift.enabled = true` | `false` recomendado por plantilla España | ET Art. 36.1 | Warning si es `true`; permitir guardar |
| `complementaryHours.pactLimitPercent` | ≤ 30 % (≤ 60 % con CT) | ET Art. 12.5 | Warning con mensaje "requiere convenio colectivo/acuerdo aplicable" si se supera 30 % |
| `complementaryHours.voluntaryLimitPercent` | ≤ 15 % adicional (≤ 30 % con CT) | ET Art. 12.5 | Warning con mensaje "requiere convenio colectivo/acuerdo aplicable" si se supera 15 % |
| `complementaryHours.noticeDays` | ≥ 3 días | ET Art. 12.5 | Warning si baja de 3; permitir guardar |

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
| 4. Activar switch en empleado | Manager en ficha del empleado | Solo afecta a ese empleado. El perfil se aplica en el próximo **checkout** (no al checkin en curso). Si el empleado está fichado en ese momento, la UI muestra el aviso: *"El siguiente cierre de turno usará el nuevo perfil laboral."* |
| 5. Nuevas métricas en heurística | Automático | Aparecen en el patrón del empleado tras el primer checkout con switch activo. |
