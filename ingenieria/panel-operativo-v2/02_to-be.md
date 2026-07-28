# 02 — Diseño objetivo (To-Be)

**Fecha:** 2026-07-28
**Estado:** Diseño para aprobación

---

## 1. Principio rector

> El mercado de control horario mide **actividad**: quién fichó, cuántas horas, cuánto costó.
> CheckBiz puede medir **entorno y capacidad**: si el sitio funciona, si la gente crece ahí, de
> quién depende la operación y qué va a pasar.

De ahí salen tres reglas que gobiernan todo el diseño:

1. **La unidad no es la persona, es la jornada.** Un equipo de 2 que cubre sus 2 posiciones está
   tan operativo como uno de 4 que cubre las suyas. Nada se divide por plantilla; todo sale en
   proporción. Así una sucursal de 5 y una de 40 se comparan de verdad.
2. **Nada se compara contra una escala universal.** Se compara contra la propia historia, contra
   la cohorte de mismo puesto y responsabilidad, o contra los demás centros del mismo cliente.
3. **Ausencia de evidencia nunca es evidencia negativa.** Sin datos suficientes se dice
   "acumulando datos", nunca `at-risk`.

---

## 2. La espina dorsal: tres ideas, tres niveles

El fallo de arrastrar métricas distintas por nivel es que produce tres dashboards pegados. Aquí
los tres niveles comparten los **mismos tres conceptos**, leídos a distinta altura. Eso es lo que
permite navegar de la organización al centro y del centro a la persona sin cambiar de idioma.

| Concepto | Nivel entidad | Nivel sucursal | Nivel empleado |
|---|---|---|---|
| **Fiabilidad** | Fiabilidad media de la organización y su dispersión | Fiabilidad del centro | Fiabilidad de la persona, normalizada por madurez (TDR-003) |
| **Efecto entorno** | Cuánta diferencia hay entre el mejor y el peor entorno | **Cuánto suma o resta el centro a quien pasa por él** (TDR-001) | Cuánto le está afectando su centro actual |
| **Fragilidad** | Cuántos centros están en riesgo por dependencia | Concentración de la operación en pocas manos (TDR-002) | Cuánto depende el centro de esta persona |

Recorrido natural del usuario: entra arriba → ve qué centro tiene peor efecto entorno → baja a ese
centro → ve quién lo sostiene y quién se degrada → baja a la persona.

---

## 3. Los cuatro diferenciales

Ninguno de estos cuatro existe hoy en el mercado de control horario, y los cuatro salen de datos
que ya se están guardando.

### 3.1 Efecto centro — ¿el problema es la persona o el sitio? ⭐

El diferencial principal. Para cada trabajador se compara su rendimiento **en ese centro** contra
su propio rendimiento **global**; el promedio de esos deltas entre todos los que pasan por allí es
el efecto que el centro ejerce sobre las personas, ya limpio del talento individual.

Habilitado por la granularidad dual de `pattern_snapshots` (203 registros por sucursal + 204
globales). Detalle en **TDR-001**.

**Por qué nadie lo tiene:** requiere patrón individual, el mismo patrón desagregado por centro, y
la historia diaria de ambos. Un competidor que copiara la idea mañana necesitaría años de
acumulación para replicarla.

**Por qué es el sitio correcto para empezar:** compara a cada persona **consigo misma**, así que
esquiva por completo el sesgo de arranque descrito en ADR-005.

### 3.2 Fragilidad del centro — ¿de cuántas manos depende esto?

Qué parte de la operación recae en una sola persona. Si el trabajador más presente cubre el 60 %
de las jornadas, el centro es una bomba de relojería. Detalle en **TDR-002**.

### 3.3 Redundancia por puesto — ¿quién cubre si mañana falta?

Cuántas personas hay realmente capacitadas para cada puesto en cada centro, usando
`experienceByJob`. Responde la pregunta que un jefe de zona se hace cada mañana.

### 3.4 Capacidad de formación — ¿este centro forma o quema?

Cuánto tarda un novato en alcanzar rendimiento pleno *en ese centro* frente a los demás centros
del cliente. Convierte la rotación de queja en causa localizada.

> **Dependencia:** 3.3 y 3.4 ganan mucha precisión con `taskSignals`, hoy presente en 46 de 406
> snapshots. Se entregan con el estado de madurez que corresponda (ADR-004), no se posponen.

---

## 4. Estructura de la pantalla

Una sola vista. Desaparecen las pestañas por tema (Costes / Salarios / Cumplimiento), que agrupan
por origen del dato — una preocupación interna, no del cliente.

**Cabecera — los tres índices de la espina dorsal** al nivel en el que estés, cada uno con su
variación respecto al periodo anterior y su estado de madurez.

**Cuerpo — dónde mirar.** Los centros ordenados por necesidad de atención (no por tamaño ni por
coste), con su efecto entorno y su fragilidad. Al abrir un centro: quién lo sostiene, quién se
está degradando, qué puestos no tienen relevo.

**Línea de tiempo — qué ha cambiado.** Hechos fechados: cambios de arquetipo, rachas, saltos
significativos. Alimentada por `pattern_snapshots` de empleado (que sí tienen recorrido desde
enero), no por los de sucursal.

**Detalle — bajo demanda.** Las series actuales, colapsadas. No desaparecen; dejan de competir por
la primera pantalla.

---

## 5. Qué se retira

| Métrica actual | Destino |
|---|---|
| `cost_vs_budget` | Se elimina (ya comentada; exige presupuestos que nadie introduce) |
| `salary_estimate` (pestaña propia) | Se elimina como pestaña; es coste con otro nombre |
| `top_employees` (por coste) | Se elimina: ordena por quién cobra más, no informa |
| `distance_avg` | Se integra en geocumplimiento |
| `cost_by_branch` + `cost_distribution` + `cost_per_hour` | Se fusionan en una vista de coste |
| Resto de métricas operativas | Pasan a ser ingredientes de los índices, no tarjetas |

El coste deja de presidir el panel: no es una medida de operatividad, es una consecuencia. Su
sitio es dentro del perfil —coste por jornada cubierta, comparado con la cohorte del mismo
puesto— y siempre acompañado de su cobertura de configuración (ADR-004).

---

## 6. Fuente de datos

**Postgres como fuente única.** Cero lecturas de Firestore desde el panel (ADR-001). Requiere
crear las tablas de dimensión `dim_branches` y `dim_employees` mantenidas por el sync.

---

## 7. Orden de entrega

1. Documentación (este bloque) — **aprobación previa**
2. Tablas de dimensión + normalización de fiabilidad por madurez (TDR-003)
3. Efecto centro (TDR-001) — el diferencial
4. Fragilidad y redundancia (TDR-002)
5. Contrato de API unificado (TDR-004)
6. Reestructuración completa del panel en el front

---

## 8. Riesgos asumidos

| Riesgo | Mitigación |
|---|---|
| Solo 5 empleados en varias sucursales → efecto centro con pocos casos cruzados limpios | El delta por-sucursal vs global se calcula para los 27 con perfil; el estado de madurez lo acompaña. Crece solo con la movilidad |
| Sesgo de arranque en los arquetipos | TDR-003 y ADR-005: separar madurez de calidad antes de publicar ninguna etiqueta |
| `incomplete_workday` sin interpretación confirmada | Bloquea la capa de ejecución hasta confirmación de negocio (ver 01_as-is §4) |
| Reliability de sucursal plana en 0,5 | El diseño se apoya en snapshots de **empleado**, que sí tienen señal, y en el efecto centro, que es un delta relativo |
