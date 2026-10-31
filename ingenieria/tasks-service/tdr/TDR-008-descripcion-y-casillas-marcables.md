# TDR-008 — Descripción de la tarea con casillas que marca el trabajador

**Fecha:** 2026-10-30
**Estado:** Diseño aprobado; servidor en `feat/descripcion-casillas` (encodebiz-api)
**Componente:** `encodebiz-api` — `tasks` (+ `descriptionChecklist` y repositorio en
`@encodebiz/shared`), app móvil, panel

---

## Resumen

La descripción de una tarea admite listas de casillas en Markdown (`- [ ] Revisar cámaras`).
Hasta ahora eran **solo texto**: la app las pintaba sin poder pulsarlas y el manual decía que
«no son un estado guardado» ([06 §7](../06_integracion-app-movil.md#7-formato-de-taskdescription-markdown)).
El trabajador no podía dejar constancia de qué puntos del guion había hecho.

Se abre un endpoint propio para la descripción, `PATCH /:taskId/description`. La marca vive
**en el propio texto** (`[ ]` → `[x]`): no hay un estado aparte que mantener en paralelo. Lo que
evita que una edición pise a otra es el **historial**: cada cambio de la descripción queda en
la actividad de la tarea con quién, cuándo, el texto anterior, el nuevo y **qué casilla
cambió**.

El endpoint es de la descripción y no de las casillas a propósito: si mañana el trabajador
necesita tocar otra cosa del texto, se amplía la regla del servidor y el endpoint es el mismo.

---

## 1. Lo que hay

- `task.description` es un `string` con Markdown (CommonMark + task lists de GFM).
- Solo se cambia por `PATCH /:taskId`, con `canManageTask` (gestor). Ese PATCH apunta en la
  actividad `updated` con la lista de campos tocados, sin el antes ni el después.
- La app renderiza las casillas no interactivas.

## 2. Decisiones

### D1. La marca va en el texto, el historial la respalda

Marcar reescribe la línea de la casilla en `description`. No se guarda un mapa de casillas
aparte: con dos fuentes, cada edición del gestor obligaría a reconciliarlas. El riesgo de que
dos cambios se pisen se cubre con el historial (D4) y con la comprobación de base (D3).

Consecuencia aceptada: la lista es **una por tarea**. Si hay varias personas asignadas, lo que
marca una lo ven las demás.

### D2. Un endpoint, dos alcances según quién

`PATCH /:taskId/description` con la descripción completa. El servidor decide qué acepta:

| Quién | Qué puede cambiar |
|---|---|
| Gestor (`canManageTask`) | Cualquier cosa del texto, como en el PATCH general |
| Asignado o supervisor (`canOperateAssignedTask`) | **Solo** el estado de las casillas |
| Resto | Nada (`403 task/unauthorized`) |

«Solo casillas» se comprueba comparando el texto guardado y el nuevo con las marcas
enmascaradas: mismas líneas, en el mismo orden, y en cada casilla solo puede cambiar el
carácter entre corchetes (` `, `x`, `X`). Si cambia cualquier otra cosa →
`403 task/description_checklist_only`.

Para quien no es gestor, además, la tarea tiene que estar abierta: en `completed`, `validated`
o `cancelled` la lista ya es el registro de lo entregado y no se toca →
`409 task/description_locked`. Un gestor sí puede corregirla (queda en el historial).

### D3. Se edita sobre lo que se vio: `baseDescription`

El cuerpo lleva también `baseDescription`, el texto que el cliente tenía en pantalla. Si no
coincide con el guardado → `409 task/description_conflict`, con la descripción actual en la
respuesta para que el cliente recargue y repita el gesto.

Por qué no basta la regla de D2: dos trabajadores con la misma tarea abierta. A marca la 1; B,
con la versión vieja, marca la 2 y manda el texto con la 1 sin marcar. Para D2 eso «solo cambia
casillas» y se aceptaría, desmarcando en silencio la de A. Con la base, B recibe el 409.

La comparación y la escritura van en **una transacción** sobre el documento de la tarea, con
la actividad dentro: o queda el cambio con su rastro, o no queda nada.

Comparación: se normalizan los finales de línea (`\r\n` → `\n`) y se recorta el texto, igual
que ya hace el PATCH general al guardar.

### D4. Todo cambio de la descripción deja rastro, con la casilla

Actividad nueva `description_updated` con:

```jsonc
{
  "type": "description_updated",
  "actorId": "…", "actorRole": "worker", "createdAt": "…",
  "metadata": {
    "checklistOnly": true,              // solo cambiaron casillas
    "changes": [                        // una entrada por casilla que cambió
      {"index": 2, "line": 3, "text": "Contar caja", "from": false, "to": true}
    ],
    "before": "## Apertura\n- [ ] Revisar cámaras\n- [ ] Contar caja",
    "after":  "## Apertura\n- [ ] Revisar cámaras\n- [x] Contar caja"
  }
}
```

- `index` es el número de la casilla en la lista (1 = la primera), `line` la línea del texto
  (1 = la primera); `text`, lo que dice la casilla sin la marca. Con eso el historial dice
  «Ana marcó *Contar caja*» sin que nadie tenga que comparar textos.
- Si el gestor cambió además el texto (`checklistOnly: false`), `changes` recoge las casillas
  que siguen existiendo con el mismo texto y cambiaron de estado; el resto del cambio se lee en
  `before`/`after`, que permiten reconstruir cualquier versión.
- El PATCH general también deja este rastro cuando cambia `description`, además del `updated`
  de siempre. Así el historial está completo venga el cambio de donde venga.

### D5. Avisos

- Marcar casillas **no** manda push a los asignados: sería un aviso por casilla.
- Si cambia el texto (lo hace un gestor), se avisa como en el PATCH general.
- El evento `task.updated` sale en los dos casos con `changed_fields: ["description"]`.

## 3. Contrato

`PATCH /:taskId/description`

```jsonc
// body
{"entityId": "…", "baseDescription": "texto que tenía el cliente", "description": "texto nuevo"}
```

| Respuesta | Cuándo |
|---|---|
| `200` la tarea (`Task`) | Guardado, o sin cambios (no se escribe ni se apunta nada) |
| `400 task/bad_request` | Falta `entityId`, o `description` / `baseDescription` no son texto |
| `403 task/unauthorized` | No es gestor ni puede operar la tarea |
| `403 task/description_checklist_only` | No es gestor y cambió algo más que casillas |
| `404` | La tarea no existe |
| `409 task/description_conflict` | `baseDescription` ≠ guardada; trae `description` actual |
| `409 task/description_locked` | No es gestor y la tarea está cerrada |

## 4. Clientes

**App (lo que da sentido a esto).** Las casillas pasan a ser pulsables. Al pulsar, la app
cambia `[ ]`↔`[x]` en esa línea del texto que está enseñando y manda
`{baseDescription: lo enseñado, description: lo nuevo}`. Pinta el cambio al momento; si llega
`409 task/description_conflict`, pone la `description` de la respuesta y avisa de que la lista
había cambiado; con otro error, deshace. Con la tarea cerrada, casillas sin pulsar. Ver
[06 §7](../06_integracion-app-movil.md#7-formato-de-taskdescription-markdown).

**Panel.** El historial de la tarea enseña `description_updated`: «marcó / desmarcó
*texto*» por cada entrada de `changes`, y «editó la descripción» cuando `checklistOnly` es
falso. La edición de la descripción puede seguir por el PATCH general (deja el mismo rastro).

**Historial: el mismo en los dos.** La app enseña a la trabajadora el mismo historial que el
panel a la gestora, entrada por entrada: mismos tipos (ciclo de vida, pausas, intentos
rechazados fuera del lugar de trabajo y `description_updated`), mismos títulos y las mismas
notas (motivo de pausa, «Pausa de X», motivo de validación o cancelación, una línea por
casilla). Si se toca uno, se toca el otro. Tras marcar, la app vuelve a traer la actividad
para que la entrada salga sin salir de la ficha.

**Manual.** La nota «las casillas no son un estado guardado» de *Crear una tarea* (ES/EN/PT)
se cambia **cuando la app que las marca esté publicada**; antes sería falsa.

## 5. Fuera de alcance

- Casillas por persona (cada asignado su lista).
- Que marcar todas las casillas sea condición para completar la tarea.
- Editar desde la app algo de la descripción que no sean casillas.
