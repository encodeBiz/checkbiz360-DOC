# 07 · El seed — del borrador a la plataforma

Lo mecánico. El borrador ya está aprobado; esto lo ejecuta. Simula por defecto, escribe sólo
con `--apply`, es idempotente por clave natural y trae su deshacer desde el primer día.

Pero «mecánico» no quiere decir sencillo: al preparar este documento aparecieron tres cosas
que cambian lo que se puede hacer, y dos de ellas cuestan dinero.

---

## Lo que escribe, y en qué orden

```
entidad → sucursales → (esperar patrón) → empleados → responsabilidades → calendario
```

**Entidad.** Si la puesta en marcha arranca desde una entidad ya creada en el back office
—que es el caso normal—, no se crea nada: se completan los huecos.

**Sucursales.** Antes de escribir, **geocodificar** cada dirección y guardar la precisión que
devuelve el geocodificador. Con radios de cientos de metros, la diferencia entre `rooftop` y
`approximate` es poner la valla en la nave o en mitad del polígono, y eso hay que enseñarlo
en la simulación, no descubrirlo después.

**Esperar al patrón.** La Cloud Function `onCreateBranch` crea el documento de
`checkbiz_branch_patterns` al crear la sucursal. El seed **no lo crea** —competiría con el
trigger por el mismo documento— pero **espera a que aparezca y se detiene si no aparece**:
sin él, el trigger de fichajes no acumula nada y el cliente ficha un mes sin generar un solo
dato ([ADR-002](./adr/ADR-002-la-puesta-en-marcha-siembra-patron-y-coste.md)).

**Empleados.** Aquí está el problema gordo. Ver abajo.

**Responsabilidades.** Una por persona y centro. `createResponsibility` rellena además
`Employee.branchId[]` con `arrayUnion`, así que las dos cosas son la misma operación y no hay
que escribir el array aparte.

**Calendario.** Los tres niveles. Ver abajo: hoy Merlin no puede escribirlo.

---

## Problema 1 — el alta manda el correo de bienvenida, siempre

`createEmployee` de `shared` crea el usuario de Auth, escribe la ficha, la indexa en el
buscador **y manda la bienvenida**. Sin forma de callarlo: `updateEmployee` acepta
`{sendWelcome}`, pero `createEmployee` no.

Sembrar doscientas personas con eso son doscientos correos con contraseña a la plantilla de
un cliente en mitad del montaje, cuando todavía se está decidiendo si los centros están bien.

Y no vale con esquivar la función y escribir la ficha a mano: hay un disparador de Firestore
(`onCreateEmployee`) que manda la bienvenida por su cuenta. Se aparta en dos casos, y sólo en
dos: **si la ficha trae `uid`** o **si nace en `pending`**.

**Lo que hay que hacer:** dar a `createEmployee` la misma opción que ya tiene
`updateEmployee`. Es un parámetro, no un diseño nuevo.

---

## Problema 2 — a quién se factura, y desde cuándo

`countByEntity`, que es de donde sale la factura, cuenta a todo el mundo **salvo `fired` y
`pending`**.

Así que sembrar la plantilla como `active` empieza a facturarla en ese momento: gente que
todavía no ha recibido su acceso —la contraseña va en la bienvenida— y que por tanto no puede
entrar ni fichar. Se cobra por una plantilla que no existe todavía.

Sembrar como `pending` no factura, y además hace que el disparador se aparte solo. El estado
está documentado como «una ficha a medio hacer que todavía no puede fichar, y no se factura»,
que es exactamente la situación. Su ejemplo canónico es otro —falta el correo—, pero el caso
general es el mismo.

**Propuesta:** sembrar en `pending`, y que **invitar sea un paso aparte y explícito** que
pasa a `active` y manda las bienvenidas cuando el cliente dice que sí. Es también lo que
pide el relato: las invitaciones apagadas hasta el final.

---

## Problema 3 — Merlin no puede escribir el calendario

`FirestoreCalendarRepository` vive en `checkinbiz`, y sus rutas HTTP están detrás de
`requireFirebaseAuth`: no hay puerta de servicio a servicio. Merlin no puede llamarlas ni
tiene el repositorio.

Tres salidas, y sólo una es buena:

- **Abrir una puerta S2S en checkinbiz.** Le añade superficie al servicio que registra los
  fichajes, que es justo lo que no queremos.
- **Que Merlin escriba los documentos por su cuenta.** Duplica dominio, que es lo que la
  regla de `shared` prohíbe.
- **Mover el repositorio a `shared`.** Es donde dice la regla que va: los tipos del
  calendario ya están allí, y lo necesitan dos servicios —`checkinbiz` lo resuelve contra
  Firestore y `analytics` contra Postgres—. Toca la línea de importación de ocho
  controladores y **deja checkinbiz más pequeño, no más grande.**

---

## Idempotencia y deshacer

**Por clave natural** —nombre de centro, correo de empleado—, nunca por id generado. La
entidad puede tener cosas creadas de antes: es lo único que evita duplicarle un centro a
alguien que ya empezó por su cuenta.

**El deshacer se escribe a la vez que el seed**, no después, porque volver atrás no es gratis:
`deleteEmployee` es borrado blando y deja la ficha en `fired`, la entrada del `searchIndex`
hay que retirarla aparte, el usuario de Auth sobrevive y los patrones acumulados no se restan.

---

## Lo que no bloquea

`GOOGLE_MAPS_API_KEY` está puesta en desarrollo, así que la geocodificación funciona. Se
comprobó el 2026-09-06.
