# ADR-003 — Firestore permanece como fuente de datos del frontend

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

Con la introducción de PostgreSQL como capa analítica, surge la pregunta natural: ¿debe el frontend leer los reportes directamente de PostgreSQL en lugar de Firestore?

Sería más "puro" arquitectónicamente que el frontend leyera del mismo lugar donde se generan los datos: el servidor privado con PostgreSQL.

Las opciones:

**Opción A — Frontend lee de Firestore (actual + propuesto):**
- El batch diario escribe en PostgreSQL Y en Firestore `checkbiz_daily_report`
- El frontend lee de Firestore como siempre
- Zero cambio en el frontend

**Opción B — Frontend lee de PostgreSQL vía API del servidor privado:**
- El frontend llama al servidor privado para obtener reportes
- Firestore solo almacena datos operacionales (checklogs, empleados, etc.)
- Requiere autenticación propia en el servidor privado, CORS, gestión de tokens

---

## Decisión

Se elige **Opción A**: Firestore permanece como fuente de datos del frontend. El servidor privado escribe en PostgreSQL Y devuelve el resultado al Cloud Function, que lo persiste en Firestore.

---

## Justificación

**El frontend ya funciona y no debe romperse.**  
El frontend de encodeBiz tiene queries, subscripciones en tiempo real y lógica de cache construidas sobre Firestore. Migrar esa capa es un proyecto separado de semanas, con riesgo de regresión, sin beneficio funcional inmediato para el usuario final.

**Firestore tiene ventajas que PostgreSQL no puede ofrecer al frontend:**
- Subscripciones en tiempo real (onSnapshot)
- Autenticación integrada con Firebase Auth y reglas de seguridad
- SDK disponible en iOS, Android, Web sin configuración adicional
- Funciona offline con cache local

**El servidor privado no debe ser accesible públicamente desde el frontend.**  
El servidor privado es infraestructura interna con datos analíticos. Exponerlo al frontend requeriría:
- Autenticación propia (JWT o API keys por usuario)
- CORS configurado correctamente
- Rate limiting por cliente
- Certificado SSL gestionado

Esto duplica la carga de seguridad sin añadir valor al usuario.

**El doble-write es el compromiso correcto:**
```
Servidor privado → PostgreSQL (fuente analítica)
                → retorna resultado al Cloud Function
                     → Cloud Function → Firestore (fuente frontend)
```

Este flujo mantiene Firestore actualizado con datos enriquecidos (task ratings, métricas mejoradas) sin cambiar cómo el frontend los consume.

---

## Consecuencias

**Positivas:**
- Zero cambios en el frontend para Fase 1, 2, 3 y 4
- Los reportes enriquecidos aparecen en el frontend automáticamente
- Seguridad perimetral: el servidor privado nunca expuesto a internet público

**Negativas / Compromisos aceptados:**
- Los datos en Firestore son una copia derivada (no la fuente analítica)
- Si el servidor privado falla durante el batch, Firestore podría tener reportes del día anterior mientras PostgreSQL no
- Costo de Firestore por las escrituras de `checkbiz_daily_report` (bajo pero real)

**Invariante que esta decisión protege:**
> *Ningún cambio en el pipeline analítico puede requerir un deploy del frontend.*
