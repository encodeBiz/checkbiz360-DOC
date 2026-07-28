# Panel Operativo v2 — de reporte de actividad a inteligencia de operación

**Estado:** Documentación para aprobación
**Fecha:** 2026-07-28
**Responsable:** Jose Acevedo

---

## El problema

Los clientes reportan que el panel no es útil: no da valores históricos ni evolución, no muestra
KPIs que ayuden a decidir, y la información es mejorable. La capa de estadística y gestión de
datos no es productiva.

El levantamiento (ver `01_as-is.md`, con datos medidos en producción) confirma que la causa no es
cómo se dibuja, sino **qué se eligió medir**:

- No existe ventana de comparación en ningún punto de la cadena: es imposible por diseño decir si
  algo mejora o empeora
- Dos de las tres pestañas se apoyan en el coste, que deriva de una tarifa que entra como `0` si
  el cliente no la configuró — un dato sesgado sin ninguna marca
- Las sucursales se comparan por valores absolutos, así que se compara tamaño disfrazado de
  rendimiento
- El activo más diferencial del producto —el perfil de trabajador con trayectoria histórica y
  granularidad por centro— no aparece en pantalla

---

## La tesis

> El mercado de control horario mide **actividad**. CheckBiz puede medir **entorno y capacidad**.

Ningún competidor del nicho puede responder si un centro mejora o degrada a la gente que pasa por
él, de cuántas manos depende una operación, o quién puede cubrir un puesto mañana. CheckBiz sí,
porque guarda el patrón de cada persona **con granularidad dual**: cómo rinde en general y cómo
rinde en cada centro.

Verificado en producción: 203 snapshots de empleado por sucursal, 204 globales, serie diaria desde
enero de 2026.

---

## Índice

| Documento | Contenido |
|---|---|
| [01_as-is.md](01_as-is.md) | Estado actual con volúmenes reales de producción y señales rotas |
| [02_to-be.md](02_to-be.md) | Dashboard de tres niveles, espina dorsal y los cuatro diferenciales |

### Decisiones de producto (ADR)

| ADR | Decisión |
|---|---|
| [ADR-001](adr/ADR-001-postgres-fuente-unica-del-panel.md) | PostgreSQL como fuente única; tablas de dimensión propias. Cero Firestore desde el panel |
| [ADR-002](adr/ADR-002-espina-dorsal-tres-niveles.md) | Tres índices leídos en tres niveles, en vez de métricas distintas por nivel |
| [ADR-003](adr/ADR-003-efecto-centro-valor-diferencial.md) | El efecto centro como métrica insignia y valor diferencial |
| [ADR-004](adr/ADR-004-madurez-del-dato-explicita.md) | La madurez del dato viaja en el contrato y se comunica en el front |
| [ADR-005](adr/ADR-005-ausencia-de-evidencia-no-es-evidencia-negativa.md) | Separar madurez de calidad: nunca etiquetar de `at-risk` a quien solo lleva poco observado |

### Decisiones técnicas (TDR)

| TDR | Contenido |
|---|---|
| [TDR-001](tdr/TDR-001-efecto-centro.md) | Algoritmo del efecto centro |
| [TDR-002](tdr/TDR-002-fragilidad-y-redundancia.md) | Concentración de cobertura (bus factor) y relevo por puesto |
| [TDR-003](tdr/TDR-003-fiabilidad-normalizada-por-madurez.md) | Separación de `dataQuality` y `dataMaturity`; detección de señal muerta |
| [TDR-004](tdr/TDR-004-contrato-api-panel.md) | Contrato del API: una llamada por vista, comparación y madurez incluidas |

---

## Hallazgos críticos del levantamiento

Tres cosas que hay que resolver y que no eran visibles antes de medir producción:

**El sesgo de arranque invalida los arquetipos.** De 44 perfiles: 17 `at-risk`, 18 `ghost`, 9
`neutral`, y **cero** `anchor`, `high-potential`, `specialist` o `maverick`. La experiencia
registrada está en semanas, así que el sistema mide antigüedad en la plataforma, no calidad del
trabajador. Publicar eso tal cual acusaría a 35 de 44 personas sin fundamento, con implicaciones
laborales reales. → ADR-005, TDR-003

**La fiabilidad de sucursal está muerta.** Constante en 0,5 en toda la serie, por el bug conocido
de `consistencyScore`. Cero varianza, cero rachas, cero cambios detectados. Además infla el modelo
de sobrecoste operativo, donde entra en tres de sus cinco penalizaciones. El diseño se apoya en
snapshots de **empleado**, que sí tienen señal. → TDR-003

**Faltan las tablas de dimensión.** No hay `branches` ni `employees` en Postgres; los nombres se
rescatan de un JSONB de `employee_daily_reports`, que solo cubre 28 de 36 empleados y 6 de 8
sucursales. → ADR-001

---

## Cuestión abierta que bloquea

`incomplete_workday` representa el 31 % de los fichajes. **Falta confirmar con negocio si significa
"jornada mal cerrada" o "jornada todavía abierta".** De ello depende que el indicador de ejecución
denuncie un problema real o acuse en falso. Ninguna métrica basada en ese estado se publica hasta
que quede resuelto.

---

## Orden de trabajo

1. **Documentación** (este bloque) — aprobación previa a cualquier implementación
2. Tablas de dimensión + fiabilidad normalizada (ADR-001, TDR-003)
3. Efecto centro (TDR-001) — el diferencial
4. Fragilidad y redundancia (TDR-002)
5. Contrato unificado `GET /panel/overview` (TDR-004)
6. **Reestructuración completa del panel en el front** — última fase

---

## Qué ya está hecho

El módulo de estadísticas (`FetchCheckbizStats`, 19 métricas) fue portado de Cloud Functions a
`encodebiz-api/services/analytics` el 2026-07-28, con paridad de cálculo verificada (cero
diferencias en el cuerpo de cálculo) y sin tocar una línea de Firebase. Se mantiene como puente
durante la migración del front.
