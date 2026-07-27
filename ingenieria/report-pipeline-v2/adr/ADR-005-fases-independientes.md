# ADR-005 — Implementación en fases independientes, no big bang

**Fecha:** 2026-06-02  
**Estado:** Aceptado  
**Decisionario:** Jose Acevedo

---

## Contexto

La transición completa implica: crear el servidor privado, sincronizar checklogs, integrar task ratings, generar daily reports enriquecidos, acumular pattern snapshots y mejorar la IA. Todo esto son entre 6 y 9 días de desarrollo.

La pregunta es si hacer todo de una vez (big bang) o en fases desplegables.

**Opción A — Big bang:**
- Todo se desarrolla en una rama `feature/pipeline-v2`
- Se despliega cuando todo está completo y probado
- 6-9 días sin cambios en producción
- Si hay un problema crítico → rollback de todo el conjunto

**Opción B — Fases independientes:**
- Cada fase tiene su propio entregable y su criterio de éxito
- Se puede desplegar y validar cada fase antes de empezar la siguiente
- Si una fase falla → solo se revierte esa fase, el resto del sistema no se toca

---

## Decisión

Se elige **Opción B: fases independientes** con el orden establecido en [04_fases.md](../04_fases.md).

---

## Justificación

**El riesgo se acumula con la complejidad.**  
Una migración de 9 días de desarrollo que se despliega toda de golpe concentra 9 días de riesgo en un único momento. Si el deploy tiene un problema, la superficie de debug es enorme.

**Cada fase tiene valor por sí sola.**  
- Fase 1 (raw sync) ya tiene valor: tenemos el warehouse listo para análisis futuros
- Fase 2 (daily enriquecido) ya tiene valor: los reportes son más ricos sin cambio en el frontend
- Fase 3 (pattern history) ya tiene valor: los patrones dejan de disolverse
- Fase 4 (IA histórica) es el destino final, pero no necesita estar lista el día 1

**El rollback granular es más seguro que el rollback total.**  
Si la Fase 2 tiene un bug que afecta los reportes de una noche, se revierte `dailyCollectorDataController` a 5 líneas de código. El servidor privado, la Fase 1 y los datos ya acumulados no se ven afectados.

**Permite aprender del sistema real entre fases.**  
Después de desplegar Fase 1, se pueden observar los datos en PostgreSQL durante varios días, validar que el sync es correcto y ajustar el schema antes de construir Fase 2 sobre esa base.

---

## Orden estricto de dependencias

```
Fase 1 (sync raw)
  ↓ prerequisito
Fase 2 (daily enriquecido)
  ↓ prerequisito  
Fase 3 (pattern snapshots)
  ↓ prerequisito (mínimo 7 días activa)
Fase 4 (IA histórica)
```

Este orden no es arbitrario:
- Fase 2 necesita datos en `checklogs_raw` → depende de Fase 1
- Fase 3 es parte del proceso de Fase 2 → depende de Fase 2
- Fase 4 necesita historial acumulado → depende de Fase 3 con N días de datos

**No se puede saltear fases.** Si se intenta Fase 3 sin Fase 2, no hay proceso que capture los snapshots. Si se intenta Fase 4 sin 7+ días de Fase 3, los algoritmos de tendencia no tienen datos suficientes.

---

## Consecuencias

**Positivas:**
- Riesgo máximo de un deploy = el riesgo de esa fase específica
- Feedback real del sistema antes de continuar
- Se puede pausar en cualquier fase si hay prioridades cambiantes

**Negativas / Compromisos aceptados:**
- Tiempo total mayor que big bang (hay overhead de deploy y validación por fase)
- Durante la transición, el sistema tiene comportamiento mixto (parcialmente enriquecido)
- Documentar el estado actual del sistema en cada punto del tiempo es más complejo
