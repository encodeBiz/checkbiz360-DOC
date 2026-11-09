# TDR-002 — El cierre del periodo

**Fecha:** 2026-10-26
**Estado:** Diseño propuesto
**Componente:** `services/a3nomina` — `PrepararCierre`, `AjustarCierre`, `AprobarYEnviar`
**Decisiones de referencia:** [ADR-002](../adr/ADR-002-se-envia-el-cierre-aprobado.md),
[ADR-003](../adr/ADR-003-unidades-no-euros.md),
[ADR-004](../adr/ADR-004-la-hora-extra-la-decide-una-persona.md),
[ADR-005](../adr/ADR-005-cada-linea-sabe-de-donde-sale.md)

---

## 1. El ciclo

```
preparar ──► borrador ──(ajustar)──► aprobar ──► enviado
                │                                   │
                └── se puede volver a preparar      └── líneas rechazadas o transitorias
                    mientras sea borrador               a la vista; se reintentan las transitorias
```

- **Preparar** mide el periodo (§3) y escribe un `a3nomina_cierre` en `borrador` con sus
  líneas. Preparar otra vez un borrador lo reemplaza entero: no se mezclan dos mediciones.
- **Ajustar** solo existe en borrador (§4).
- **Aprobar** congela el cierre y lo envía por el puerto. Lo puede hacer quien tenga
  `owner` o `admin` en la entidad.
- **Enviado** no se edita nunca. Para corregir, se prepara el siguiente (§6).

## 2. Los conceptos de CheckBiz (lista cerrada en v1)

| Concepto | Unidad | De dónde sale |
|---|---|---|
| `horas_ordinarias` | horas | Neto trabajado − horas extra confirmadas |
| `horas_nocturnas` | horas | Tramo de cada ciclo entre 22:00 y 06:00, hora local del centro |
| `horas_festivo` | horas | Neto trabajado en días que son festivo en su calendario (entidad, sucursal o persona) |
| `horas_extra` | horas | Exceso confirmado por quien aprueba (ADR-004) |
| `vacaciones` | días | Ausencias aprobadas de tipo `vacation` |
| `permiso_retribuido` | días | Ausencias aprobadas con `paid: true`, de tipo distinto de `vacation` |
| `permiso_no_retribuido` | días | Ausencias aprobadas con `paid: false` |

Fuera de v1:

- **Bajas (IT):** A3 ya las recibe por los partes de la Seguridad Social, y mandarlas
  podría duplicarlas. *A confirmar con la cuenta*. Mientras tanto, se enseñan en la vista
  previa como información y no se envían.
- **Dietas, kilometraje y pluses:** fase 3; CheckBiz hoy no los registra.

Los conceptos no se excluyen entre sí: una hora nocturna en festivo cuenta en
`horas_nocturnas` y en `horas_festivo`. Cada concepto es una cantidad que A3 valora según su
configuración, como hacen los recargos.

## 3. Medición

**Fuente de horas: `employee_daily_reports`.** Es la tabla que construye `reports`
(`BuildEmployeeDailyReports.ts`, 02:30 UTC) y la que lee el informe legal de jornada
(`GenerateReportPDF.ts`). La nómina y el informe legal tienen que dar la misma cifra. Si
algún día divergen, el error es de este servicio. Se usan `total_net_minutes` y `cycles`
(con entrada, salida y descanso de cada ciclo).

Por persona y día del periodo:

1. **Neto trabajado:** `total_net_minutes`.
2. **Nocturnas:** para cada ciclo, la intersección de `[entrada, salida]` con 22:00–06:00
   en la zona horaria del centro (`branch_meta`). Se descuenta el descanso de forma
   proporcional cuando cae dentro del tramo. Es una regla aproximada y queda escrita como tal
   en el origen de la línea.
3. **Festivo:** el día es festivo si figura en los `holidays` del calendario resuelto de esa
   persona (entidad + sucursal + persona) en `dim_calendars`.
4. **Previsto:** según el modo de la persona ese día. *Semana tipo* usa la semana tipo;
   *Por turnos* usa los turnos cargados (sin turno, el día libra); *Por tareas* usa la suma
   de sus tareas. Se toma de `checklogs_raw.schedule_applied` cuando la jornada lo trae, y
   del calendario resuelto cuando no.
5. **Exceso:** `max(0, neto − previsto)` cuando hay previsto. Sin previsto, no hay exceso
   medible, y la línea lo dice.

Los días de una ausencia aprobada que caen dentro del periodo cuentan en días naturales o
laborables según la correspondencia del concepto. *A confirmar con la cuenta*: qué espera A3.

**Bloqueos por persona** (ADR-002): la persona queda fuera, con su motivo, si tiene

- alguna jornada del periodo en `pending-employee-validation` o sin salida
  (`incomplete_workday`);
- ausencias con `paid: null`;
- falta de asociación con un empleado de A3.

Un concepto sin correspondencia no excluye a la persona: se excluye esa línea.

**Antes de preparar se comprueba que los diarios del periodo están construidos.** Si
falta algún día en `employee_daily_reports`, se avisa y no se prepara: no se mide a medias.

## 4. Vista previa y ajustes

La pantalla enseña:

- **Por persona:** cada concepto con su cantidad, desplegable hasta los días y jornadas de
  los que sale.
- **Arriba, lo que falta:** personas bloqueadas y conceptos sin asociar, cada uno con un
  enlace a donde se arregla. La gestión no obliga a salir de la pantalla.

Ajustes posibles, todos con motivo obligatorio y guardados en `a3nomina_ajuste`:

- **Horas extra:** por defecto se propone todo el exceso. Quien aprueba puede bajarlas (por
  ejemplo, si se compensan con descanso) pero nunca subirlas por encima del exceso medido.
  Lo que deja de ser extra pasa a `horas_ordinarias`.
- **Excluir a una persona del envío.**

No se puede editar una cantidad medida (neto, nocturnas, festivo). Si está mal, se corrige
la jornada en CheckBiz y se vuelve a preparar. La cifra de la nómina tiene que seguir siendo
la del registro.

## 5. Envío

`AprobarYEnviar`:

1. Pasa el cierre a `aprobado` con autor y hora.
2. Traduce cada línea incluida a su concepto de A3 y su empleado externo (TDR-003).
3. Envía por `NominaExterna.enviarPeriodo`.
4. Guarda la respuesta línea a línea:
   - `aceptada`;
   - `rechazada`, con el motivo que da A3;
   - `transitoria`, que se reintenta por S2S con presupuesto.
5. El cierre queda en `enviado` si todo se aceptó, o en `con_errores` con el detalle a la
   vista.

La huella de cada línea evita mandar dos veces lo mismo en un reintento.

## 6. Correcciones después de enviar

Una jornada corregida en CheckBiz después de enviar el cierre no se pierde. Al preparar el
**siguiente** cierre, también se vuelve a medir el periodo anterior. Lo que haya cambiado
sale en un bloque aparte, *diferencias del periodo anterior*, con la cantidad enviada y la
nueva.

Qué se hace con esa diferencia (mandarla como atraso, reescribir el periodo anterior si A3
lo admite, o solo avisar) **está a confirmar con la cuenta**. En v1, si A3 no da una vía
clara, solo se avisa, y quien hace la nómina decide en A3.

## 7. Abierto

- **Periodo:** ¿siempre mes natural, o el periodo de nómina que tenga cada cliente
  (quincenal en algunos sectores)? Propuesta: mes natural en v1 y el periodo como
  configuración del add-on después.
- **Nocturnas:** 22:00–06:00 es el mínimo del Estatuto, pero un convenio puede fijar otro
  tramo. Propuesta: el tramo, configurable por entidad, con el del Estatuto por defecto.
