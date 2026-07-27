# Merlin — IA de Interpretación Operativa

> Servicio: `encodebiz-api/services/merlin` | Puerto: 3001  
> Última actualización: 2026-07-03

---

## Qué es Merlin

Merlin es la IA de encodeBiz. Traduce los datos heurísticos de una sucursal o empleado en un análisis ejecutivo accionable para el gestor. No es un chatbot — es un **analista operativo** que recibe señales numéricas (patrón de comportamiento, indicadores V2, señales de tareas) y genera un diagnóstico estructurado con causas raíz y acciones concretas.

---

## Arquitectura

```
merlin/src/
├── domain/
│   └── index.ts              → InterpretationRequest, InterpretationResult, PromptBuilder, Renderer
├── application/
│   └── interpret.usecase.ts  → InterpretUseCase: orquesta builder → renderer
├── infrastructure/
│   ├── openai.renderer.ts    → llama a OpenAI Responses API, extrae JSON
│   ├── interpretation.factory.ts → composition root: selecciona builder por modo/target/audience
│   └── promptBuilders/
│       ├── branchInterpret.builder.ts      → análisis de sucursal (modo más desarrollado)
│       ├── employeeAdminInterpret.builder.ts → análisis empleado para admin
│       ├── employeeFeedback.builder.ts     → feedback empleado para vista empleado
│       ├── branchCompare.builder.ts        → comparativa entre sucursales
│       └── employeeCompare.builder.ts      → comparativa entre empleados
├── modules/
│   ├── application/
│   │   ├── getOrCreateBranchAnalysis.ts    → orquesta interpretación de sucursal(es)
│   │   └── interpretEmployees.ts           → orquesta interpretación de empleado
│   ├── domain/
│   │   └── analysis.ts                     → BranchAnalysis entity, cache keys
│   └── infrastructure/
│       └── FirestoreAnalysisRepository.ts  → cache de análisis en Firestore
└── interfaces/
    └── merlin.router.ts      → POST /api/v1/gpt/interpret
```

---

## Endpoint

```
POST /api/v1/gpt/interpret
Authorization: Bearer <Firebase JWT>

body: {
  request: {
    entityId: string           // obligatorio
    branchIds?: string[]       // para target=branch
    employeeId?: string        // para target=employee
    branchId?: string          // contexto del empleado
    mode?: "interpret"|"compare"   // default: interpret
    target?: "branch"|"employee"   // default: branch
    audience?: "admin"|"employee"  // default: admin
    lang?: "es"|"en"               // default: es
    locale?: "es"|"en"|"pt"        // default: es
  }
}

response 200: { code: "ai/cache_hit", result: InterpretationResult }
response 202: { code: "ai/analysing", result: InterpretationResult }
response 404: { code: "pattern/not_found" }
```

---

## Modos y builders

| mode | target | audience | Builder |
|---|---|---|---|
| `interpret` | `branch` | `admin` | `BranchInterpretPromptBuilder` |
| `interpret` | `employee` | `admin` | `EmployeeAdminInterpretPromptBuilder` |
| `interpret` | `employee` | `employee` | `EmployeeFeedbackPromptBuilder` |
| `compare` | `branch` | `admin` | `BranchComparePromptBuilder` |
| `compare` | `employee` | `admin` | `EmployeeComparePromptBuilder` |

---

## Schema de respuesta (JSON Schema estructurado)

```typescript
{
  headline: string      // ≤ 12 palabras, debe incluir número si dataQuality > 50%
  summary: string       // 2-3 frases: diagnóstico de causa raíz con valores específicos
  body: string          // ≤ 3 frases: el "por qué", conexión de señales, nota positiva
  actions: string[]     // ≤ 3 acciones, imperativas, acotadas en tiempo y específicas
  confidenceNote: string // ≤ 35 palabras: nivel de confianza por dataQuality
}
```

---

## Datos que recibe Merlin (branchInterpret)

El builder extrae del patrón:
- **Timing**: `avgStartHour`, `avgEndHour`, `stdStartHour`, `stdEndHour` → formateados como HH:MM
- **Dispersión por día**: `stdStartByDay[7]` → tabla día/desviación
- **Horas semanales**: `weeklyWorkAvg[7]` → resumen Dom-Sáb
- **Señales de tarea**: `taskSignals.branchOnTimeRate`, `branchRejectionRate`, `branchAvgRating`, `taskCount`
- **Calidad de datos**: `dataMaturity`, `dataQuality`, `dataPoints`
- **Perfil**: `profileType` → guía el tono del análisis

---

## Perfiles y guía por tipo

| profileType | Instrucción a Merlin |
|---|---|
| `elite` | Consolida y replica lo que funciona. No sobre-ingeniería. |
| `data-weak` | Solo recomendar mejorar captura de datos. NO diagnosticar operaciones. |
| `discipline-gap` | Asistencia ok, calidad de tareas baja. Foco en ejecución y rechazos. |
| `understaffed` | Horas cortas + tareas tardías → plantilla o turnos. |
| `multi-shift-stable` | Dispersión global ESTRUCTURAL (múltiples turnos). NO alertar sobre ella. |
| `anchor` | Empleado fiable. Refuerza. |
| `at-risk` | Fiabilidad < 50% o tareas fuera de plazo. Acción inmediata. |
| `maverick` | Horario irregular pero quality ok. Gestión flexible. |

---

## Problemas conocidos (pendiente de mejora)

| Problema | Estado |
|---|---|
| `EmployeeAdminInterpretPromptBuilder` vuelca JSON crudo — no extrae valores como branch | ⚠️ Pendiente reescritura |
| `EmployeeFeedbackPromptBuilder` referencia campos inexistentes (`promotionScore`, `skillLevel`) | ⚠️ Pendiente reescritura |
| Merlin no recibe contexto histórico (TrendAnalysis) | ⏳ Fase 4 pipeline |
| Acciones genéricas sin números específicos en builder de empleado | ⚠️ Pendiente |

---

## Próximos pasos (Fase 4)

Cuando `analytics` tenga `pattern_snapshots` de ≥ 14 días, Merlin recibirá `TrendAnalysis` en el prompt:

```
TENDENCIAS (últimos 30 días):
- Fiabilidad: improving (+8% en 14 días, de 0.71 a 0.79)
- Puntualidad entrada: declining (-12%)
- Valoración tareas: improving (+0.3★)
- Señal: ✅ Recovery signal activa (mejora en últimos 7 días)
```

Esto permite diagnósticos como: *"La fiabilidad mejora pero la puntualidad empeora — posible cambio de turno no reflejado en el horario planificado"*.

---

## Deploy

```bash
# Prod (via docker compose en servidor)
docker compose up --build merlin

# Dev local
npm run dev:merlin
```

El `merlinIa` de Firebase Functions actúa como proxy hasta completar la migración:
```typescript
// Firebase Functions → merlin:3001
fetch(`${ENCODEBIZ_API_URL}/api/v1/gpt/interpret`, { method: "POST", ... })
```
