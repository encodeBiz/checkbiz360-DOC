# Modulo Reporting y Analitica — Agregados Diarios y Reportes Masivos

> Estado: Ingenieria aprobada para robustez operativa.
> Alcance: CheckBiz — estadisticas, dashboards, reportes masivos y cumplimiento.
> Motivacion: soportar clientes medianos/grandes sin procesar checklogs crudos en requests HTTP.

## 1. Resumen

Los reportes masivos y la analitica no deben depender de leer y procesar todos los `checklogs` crudos bajo demanda.

La arquitectura objetivo es consolidar automaticamente la actividad diaria y construir dashboards/reportes desde historicos agregados.

```txt
checklogs crudos
  -> agregador diario automatico
  -> historico diario normalizado
  -> dashboards / analitica / reportes masivos
  -> archivo generado en background
```

Esta decision reduce riesgo de timeout, consumo de memoria, coste impredecible y degradacion de la operativa cuando una entidad tiene cientos de trabajadores.

## 2. Problema

Con clientes de volumen medio/alto, por ejemplo 800 empleados:

- 800 empleados x 2 marcajes diarios x 30 dias = ~48.000 checklogs mensuales minimos.
- Con pausas, incidencias, errores, ediciones y jornadas manuales, el volumen real puede ser bastante mayor.
- Un reporte mensual construido en una request HTTP puede tener que leer, agrupar, enriquecer y renderizar decenas de miles de eventos.
- Si varios responsables generan informes o abren dashboards a la vez, el coste y la latencia se multiplican.

El riesgo no esta en el check-in individual, sino en los procesos analiticos amplios sobre rangos grandes.

## 3. Decision Arquitectonica

### ADR-001: Los reportes masivos se construyen desde agregados diarios

**Decision:** los reportes masivos deben consumir historicos diarios preconsolidados, no `checklogs` crudos.

Los `checklogs` crudos quedan como fuente de verdad para:

- auditoria,
- detalle de jornada,
- resolucion de incidencias,
- recalculo puntual,
- trazabilidad legal.

Los dashboards y reportes de rango deben consumir:

- agregado diario por entidad,
- agregado diario por sucursal/proyecto,
- agregado diario por empleado cuando aplique.

### ADR-002: La consolidacion diaria debe ser automatica

**Decision:** cada dia debe ejecutarse un proceso automatico que consolide la actividad del dia anterior.

El proceso debe calcular y persistir metricas como:

- horas trabajadas,
- numero de checkins/checkouts,
- jornadas incompletas,
- ausencias,
- retrasos,
- salidas anticipadas,
- horas extra,
- coste estimado,
- cumplimiento horario,
- cumplimiento geografico,
- marcajes sospechosos,
- incidencias,
- registros manuales pendientes/aprobados/rechazados.

### ADR-003: Los reportes grandes deben ser asincronos

**Decision:** los reportes de rango amplio o volumen alto no deben bloquear una llamada HTTP.

Flujo esperado:

1. Front solicita generar reporte.
2. Backend crea un `report_job`.
3. Worker/proceso background genera el archivo.
4. Archivo final se guarda en Storage privado.
5. Front consulta estado o recibe notificacion cuando este listo.
6. Usuario descarga mediante URL firmada temporal.

### ADR-004: Los dashboards deben evitar recalculo duplicado

**Decision:** el endpoint de dashboard debe favorecer respuestas compuestas o cacheables.

No es deseable que cada widget ejecute la misma carga base de datos/rango/empleados por separado.

Estrategias aceptadas:

- endpoint que devuelva varias metricas en una sola llamada,
- cache corto por `entityId + branchId + from + to + metricSet`,
- reutilizacion interna de la misma carga base para multiples metricas,
- limites maximos de rango segun granularidad.

## 4. Modelo de Datos Objetivo

### Coleccion diaria por sucursal

```txt
checkbiz_daily_report/{entityId}_{branchId}_{yyyyMMdd}
```

Campos orientativos:

```json
{
  "entityId": "entity_001",
  "branchId": "branch_001",
  "date": "2026-05-20T00:00:00.000Z",
  "employeesCount": 42,
  "workedHours": 318.5,
  "expectedHours": 336,
  "extraHours": 12.25,
  "absences": 3,
  "lateCheckins": 7,
  "earlyCheckouts": 2,
  "validChecklogs": 81,
  "failedChecklogs": 5,
  "manualApproved": 1,
  "manualPending": 2,
  "manualRejected": 0,
  "geoComplianceRate": 0.97,
  "scheduleComplianceRate": 0.91,
  "totalCost": 4120.75,
  "employees": []
}
```

### Agregado diario por empleado

Para reportes masivos por empleado conviene persistir tambien una unidad diaria por empleado.

```txt
checkbiz_daily_employee_report/{entityId}_{branchId}_{employeeId}_{yyyyMMdd}
```

Campos orientativos:

```json
{
  "entityId": "entity_001",
  "branchId": "branch_001",
  "employeeId": "employee_001",
  "date": "2026-05-20T00:00:00.000Z",
  "workedHours": 7.9,
  "expectedHours": 8,
  "extraHours": 0,
  "absence": false,
  "late": true,
  "earlyCheckout": false,
  "remoteWork": false,
  "geoValid": true,
  "status": "complete",
  "cost": 96.4,
  "checklogIds": []
}
```

## 5. TDRs

### TDR-001: El agregado diario debe ser idempotente

El proceso diario debe poder reejecutarse sin duplicar datos.

La clave del documento debe ser deterministica:

```txt
entityId + branchId + date
entityId + branchId + employeeId + date
```

### TDR-002: Recalculo puntual por rango limitado

Debe existir un mecanismo interno para recalcular un dia, sucursal o empleado cuando se corrige un checklog historico.

No se debe recalcular una entidad completa si el cambio afecta a un empleado/dia concreto.

### TDR-003: Los checklogs crudos no desaparecen

Los agregados no sustituyen la trazabilidad. Los `checklogs` siguen siendo fuente de auditoria y detalle legal.

Los agregados son una vista materializada para lectura eficiente.

### TDR-004: Reportes masivos con job persistente

Un reporte masivo debe tener estado persistente:

```txt
pending -> processing -> ready | failed
```

Campos minimos:

- `id`,
- `entityId`,
- `requestedBy`,
- `type`,
- `filters`,
- `status`,
- `storagePath`,
- `error`,
- `createdAt`,
- `startedAt`,
- `finishedAt`.

### TDR-005: Limites por rango y granularidad

Los endpoints HTTP deben aplicar limites.

Ejemplos:

- dashboard diario: maximo 90 dias,
- dashboard mensual: maximo 24 meses,
- reporte sincronico: solo rangos pequenos,
- reporte masivo: siempre job asincrono.

### TDR-006: Indices Firestore requeridos

Indices minimos:

```txt
checkbiz_daily_report:
- entityId ASC, date DESC
- entityId ASC, branchId ASC, date DESC

checkbiz_daily_employee_report:
- entityId ASC, date DESC
- entityId ASC, branchId ASC, date DESC
- entityId ASC, employeeId ASC, date DESC
- entityId ASC, branchId ASC, employeeId ASC, date DESC

report_jobs:
- entityId ASC, status ASC, createdAt DESC
- entityId ASC, requestedBy ASC, createdAt DESC
```

## 6. Flujo de Reporte Masivo

```txt
Backoffice
  -> POST /reports/jobs
  -> report_job pending
  -> worker procesa agregados diarios
  -> genera PDF/CSV/XLSX si aplica
  -> sube a Storage privado
  -> report_job ready
  -> notificacion al solicitante
  -> GET /reports/jobs/:id/download
```

## 7. Flujo de Dashboard

```txt
Backoffice abre dashboard
  -> solicita metricSet
  -> backend lee agregados diarios del rango
  -> calcula KPIs en memoria sobre datos ya compactados
  -> responde dataset compuesto
```

El dashboard no debe consultar checklogs crudos salvo para drill-down de detalle.

## 8. Criterios de Escalabilidad

Antes de aceptar clientes con cientos de empleados, validar:

- 800 empleados marcando en ventana de 5, 10 y 20 minutos.
- dashboard con 30, 60 y 90 dias.
- 5-10 responsables consultando estadisticas a la vez.
- reporte mensual completo de entidad.
- reporte mensual por sucursal.
- reporte por empleado con drill-down de checklogs.

Metricas objetivo:

- sin timeouts HTTP,
- memoria estable,
- coste Firestore predecible,
- p95 de dashboard razonable,
- reportes masivos generados por job y no por request bloqueante.

## 9. Estado Actual y Brecha

El sistema ya dispone de una base de agregados diarios para estadisticas (`checkbiz_daily_report`) y un controlador de estadisticas que consume esos agregados.

La brecha principal es que los reportes PDF de rango amplio todavia pueden depender de checklogs crudos y ejecutarse en una request HTTP. Para clientes medianos/grandes, esa parte debe migrar a jobs asincronos sobre agregados diarios.

## 10. Roadmap Recomendado

### Fase 1 — Blindaje de agregados diarios

- validar estructura actual de `checkbiz_daily_report`,
- asegurar idempotencia,
- documentar campos canonicos,
- crear indices necesarios,
- crear recalculo manual por dia/sucursal.

### Fase 2 — Agregado diario por empleado

- crear `checkbiz_daily_employee_report`,
- poblar por schedule diario,
- soportar recalculo puntual,
- usarlo para reportes por empleado y entidad.

### Fase 3 — Report jobs asincronos

- crear `report_jobs`,
- mover reportes masivos a background,
- guardar salida en Storage,
- exponer estado y descarga.

### Fase 4 — Dashboard compuesto/cacheado

- endpoint de metricas compuestas,
- cache corto por rango,
- limites por granularidad,
- evitar recarga duplicada por widget.

### Fase 5 — QA de carga

- dataset sintetico de 800 empleados,
- pruebas de concurrencia,
- pruebas de coste Firestore,
- pruebas de reportes mensuales.
