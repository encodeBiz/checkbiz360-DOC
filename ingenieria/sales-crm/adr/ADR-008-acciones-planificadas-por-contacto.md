# ADR-008 — Acciones planificadas por contacto

**Fecha:** 2026-10-15
**Estado:** Aceptado
**Decisionario:** Jose Acevedo («investiga cómo podemos saber las actividades programadas… se han enviado InMail y hay pendientes por enviar, ¿cómo lo detectamos fácilmente?»)

---

## Contexto

La etapa es de la empresa y marca lo más avanzado que ha pasado en ella: Serlimar está
`contacted` porque se escribió a su director general, aunque al de operaciones (a quien toca
escribir el martes) no le ha llegado nada. Eso es correcto y se mantiene. El hueco es otro:
cada cuenta tiene **una** «próxima acción» de texto libre, así que «InMail a David Álvarez el
martes» vive en una nota. Ni el pipeline, ni la agenda, ni la lista de contactos lo ven.

## Decisión

1. **Entidad nueva: la acción planificada** (`sales_planned_actions`): cuenta, contacto
   (opcional), tipo de actividad, título, borrador del mensaje, fecha y estado
   (`pending` → `done` | `skipped`).
2. **Completarla registra la actividad** en la misma transacción, con las mismas reglas y los
   mismos efectos de etapa que `LogActivity`. Descartarla exige motivo.
3. **Las reglas se comprueban al planificar**, no solo al registrar: sin perfil vigente,
   contacto con oposición o email no permitido (06 §D5) se rechazan al planificar, para
   enterarse el lunes y no el martes al ir a enviar. Se vuelven a comprobar al completar.
4. **Estado de contacto derivado**, aparte de la etapa: `untouched`, `pending`, `overdue`,
   `contacted`, `replied`. Se calcula, no se guarda.
5. La cuenta muestra cuántas acciones tiene pendientes y vencidas, y la próxima fecha. La
   agenda (correo y `crm_next_actions`) lista las acciones por persona y canal.
6. **Nada se envía solo** (ADR-006): la acción es un recordatorio con el texto listo.

## Alternativas descartadas

- **Etapa por contacto:** duplicaría el embudo y rompería los recuentos por empresa, que es
  la unidad (ADR-002).
- **Varias «próximas acciones» de texto en la cuenta:** no tendrían persona, ni borrador, ni
  estado, ni se cerrarían al enviar.

## Consecuencias

- La «próxima acción» manual de la cuenta se conserva (sirve para lo que no es un mensaje a
  alguien: «revisar el pliego»), y la agenda junta las dos.
- El agente pasa de «redactar y olvidar» a planificar con borrador y marcar como hecho cuando
  la persona confirma el envío.
