# ADR-001 — PostgreSQL privado como Data Warehouse analítico

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

encodeBiz procesa checklogs en tiempo real y los almacena en Firestore bajo la ruta `entities/{entityId}/checklogs/{checklogId}`. Cuando un administrador solicita un reporte de asistencia para un rango de fechas (ej: último mes, 200 empleados), el sistema ejecuta una query de Firestore que devuelve potencialmente miles de documentos. Firestore cobra **por lectura de documento individual**, no por query, lo que hace que este modelo sea inviable a escala.

Las alternativas evaluadas para crear una capa analítica fueron:

| Opción | Costo | Control | SQL | Latencia | Datos sensibles |
|--------|-------|---------|-----|----------|-----------------|
| Firestore (actual) | Alto a escala | Total | No | Alta | Cumple |
| BigQuery (Google) | Por query/TB | Parcial | Sí | Media | Tercero |
| Supabase cloud | Mensual fijo | Parcial | Sí | Baja | Tercero |
| PlanetScale / Neon | Mensual fijo | Parcial | Sí | Baja | Tercero |
| PostgreSQL privado | Costo servidor | Total | Sí | Baja | Total |

---

## Decisión

Se elige **PostgreSQL 15+ en servidor privado propiedad de encodeBiz** como capa analítica.

---

## Justificación detallada

**1. Los datos de asistencia son altamente sensibles.**  
Checklogs contienen coordenadas GPS, horarios de entrada/salida y patrones de comportamiento de empleados de empresas clientes. Almacenarlos en infraestructura de terceros (Supabase, PlanetScale) introduce riesgo legal y contractual que no existe con PostgreSQL en servidor propio.

**2. El volumen estimado no justifica BigQuery.**  
BigQuery es eficiente a partir de terabytes. Con la estimación de ~7.2M checklogs a 12 meses y 100 empresas, estamos en el orden de gigabytes. Un servidor PostgreSQL bien indexado maneja este volumen sin estrés y sin el costo de BigQuery por query.

**3. SQL nativo habilita análisis que Firestore no puede hacer.**  
Joins entre checklogs y task ratings, percentiles de puntualidad, media móvil de patrones, agrupación multi-dimensión: todo esto requiere SQL. No existe alternativa razonable en Firestore para este tipo de consultas.

**4. Firebase NO se reemplaza.**  
Firebase sigue siendo la fuente operacional y el backend del app en tiempo real. PostgreSQL es exclusivamente la capa analítica. No hay migración de frontend.

---

## Consecuencias

**Positivas:**
- Costo de lectura de datos analíticos: cero (solo costo del servidor)
- Queries SQL complejas sin restricciones
- Control total sobre retención, backup y acceso
- Datos sensibles permanecen en infraestructura propia

**Negativas / Compromisos aceptados:**
- Requiere mantener un servidor privado (ops, actualizaciones, backup)
- Doble escritura: Firebase operacional + PostgreSQL analítico añade complejidad
- Sin la HA gestionada de un cloud managed DB (requiere configurar replicación si se necesita)

**Riesgos mitigados:**
- El servidor privado puede caer sin afectar el app (ver ADR-002 sobre fire-and-forget)
- PostgreSQL puede fallar y los datos siguen estando en Firestore como respaldo para re-sync

---

## Revisión futura

Si encodeBiz supera las 1.000 empresas activas y el volumen de datos alcanza los 100GB+, evaluar migración a un managed PostgreSQL (RDS, Cloud SQL) manteniendo el principio de servidor privado o single-tenant.
