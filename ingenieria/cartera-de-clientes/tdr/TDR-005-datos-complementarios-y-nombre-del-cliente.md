# TDR-005 — «Datos complementarios» en la app y el nombre del cliente, solo con autorización

**Fecha:** 2026-11-07
**Estado:** decidido por Jose el 2026-11-07 («encajo con todo lo que me dices»). API en staging el mismo día (`ca2d144`; develop `fe3c62b0`, staging `a8fa6c74`), panel `38228381` en `feat/cartera-de-clientes`, app `7c0f94a` en `checkbiz360` `feat/datos-complementarios`, sin push. Pase en §48.
**Componente:** `packages/shared` (`taskCustomerSnapshot`), `services/tasks`, `services/customers`; panel (ficha y formulario del cliente, detalle de la tarea); app `checkbiz360` (detalle de la tarea)
**Sustituye en parte:** [TDR-002](TDR-002-el-cliente-en-la-tarea.md) §la copia para la app, y la hoja «Ver datos del cliente» de la Fase 4 ([TDR-003](TDR-003-documentos-del-cliente.md))

---

## 1. Lo que Jose ha visto en la QA de la app

- **Un botón que nadie pulsa.** Hoy la trabajadora tiene que tocar «Ver datos del cliente» para ver
  las indicaciones, los contactos y los documentos. En limpieza y SAD eso es complicar: lo quiere
  como **una tarjeta más** del detalle de la tarea.
- **El nombre del cliente es un dato sensible.** En una subcontrata, el nombre del cliente más el
  teléfono de su contacto es entregarle el cliente a quien lo puede robar. Que la tarea enseñe el
  nombre tiene que ser **una autorización expresa en el cliente, apagada por defecto**. «Es un fallo
  que se muestre por defecto». Se habla de la app; el panel es de quien gestiona y lo sigue viendo.

## 2. Lo decidido

### La tarjeta «Datos complementarios»

- En el detalle de la tarea de la app, una tarjeta **encima de «Equipo»**, titulada «Datos
  complementarios»: notas de campo, contactos visibles (con llamar) y documentos para trabajadores
  (con abrir).
- **Carga perezosa**: pide `GET /customers/for-task/:taskId` solo cuando la tarjeta entra en
  pantalla, no al abrir la tarea. Una tarea sin cliente no pide nada.
- **Si no hay nada que enseñar, no aparece**: sin notas, sin contactos visibles y sin documentos
  para trabajadores, ni tarjeta ni hueco.
- Desaparece el botón «Ver datos del cliente» y su hoja inferior.

### «Mostrar el nombre del cliente a la plantilla»

- Campo nuevo en el cliente, `showNameToWorkers: boolean`, **`false` por defecto** y `false` para
  todo cliente que no lo tenga. Se marca en el formulario del cliente (panel), con la ayuda: «Si no
  lo marcas, la plantilla ve las indicaciones, los contactos visibles y los documentos para
  trabajadores, pero no el nombre del cliente. Ojo: el título de la tarea se ve siempre».
- **Apagado, la plantilla ve los datos complementarios sin el nombre** (opción recomendada y
  aceptada). La alternativa estricta —sin autorización no se ve nada del cliente— se descartó: cada
  dato de la tarjeta ya se marcó a propósito como visible para la trabajadora, y sin indicaciones el
  trabajo se resiente.
- Encendido, la tarjeta lleva el nombre del cliente arriba, como hoy «Cliente: …».

### Lo corta el servidor, no la app

La app no recibe el nombre si no está autorizado. Que no lo pinte no basta:

- **La copia en la tarea** (`task.customer`, `taskCustomerSnapshot`) se construye **sin `name`**
  cuando el cliente no tiene `showNameToWorkers`. Así no está ni en lo que sirve el servicio de
  tareas ni en el documento de Firestore, que hoy cualquier miembro puede leer con el SDK (reglas
  2b pendientes). La copia gana `nameVisible: boolean` para que nadie confunda «sin nombre» con
  «cliente sin nombre».
- **`for-task`** devuelve `customer.name` solo con `showNameToWorkers`.
- **El panel** deja de leer el nombre de la copia: el detalle de la tarea lo resuelve por
  `customerId` contra `customers` (quien gestiona sí puede), igual que el selector del formulario.
- **Cambiar la casilla o el nombre del cliente** rehace la copia de sus tareas abiertas (no
  terminadas ni canceladas) en el mismo PATCH del cliente. Hoy la copia solo se refresca en la
  siguiente edición de la tarea; con un dato sensible no vale esperar: quitar la autorización tiene
  que quitar el nombre ya.
- Revisar al implementar que **ningún aviso a la plantilla** (push, correo de tarea) lleve
  `customer.name`.

### Contactos: el aviso junto a «visible para trabajadores»

Un contacto visible puede delatar al cliente tanto como el nombre («Jefe de compras de …»). Junto
a la casilla del contacto, el panel avisa: «La plantilla verá su nombre, su cargo y su teléfono».

### Lo que no se puede controlar

El **título de la tarea** se ve siempre. Si se titula «Limpieza Mercadona», el nombre está ahí. Se
dice en la ayuda de la casilla; no se intenta detectar.

## 3. Datos existentes

- **Producción**: la cartera aún no está (pase §33–§35), así que no hay copias que corregir: todos
  los clientes nacerán con la casilla apagada.
- **Staging**: las tareas con cliente ya creadas llevan el nombre en la copia. Un script que simula
  por defecto (`--apply` para actuar) rehace la copia de las tareas abiertas con la regla nueva.

## 4. Piezas y orden

1. `shared`: `showNameToWorkers` en `Customer`; `taskCustomerSnapshot` sin `name` si no está
   autorizado, con `nameVisible`.
2. `customers`: el campo en alta y edición (validación booleana); `for-task` sin nombre; el PATCH
   rehace las copias de las tareas abiertas cuando cambia la casilla o el nombre; script de staging.
3. `tasks`: nada propio más allá de usar el `taskCustomerSnapshot` nuevo (alta, edición, copia).
4. Panel: casilla y ayuda en el formulario del cliente, aviso en los contactos, el detalle de la
   tarea resuelve el nombre por `customerId`.
5. App: la tarjeta «Datos complementarios» encima de «Equipo», perezosa y oculta si no hay datos;
   fuera el botón y la hoja.

API y panel juntos; la app después, que sin la casilla encendida simplemente deja de ver el nombre.

## 5. Pruebas

- Cliente sin autorizar: la app no ve el nombre en la tarea ni en la tarjeta; ve notas, contactos
  visibles y la ficha. El documento de la tarea en Firestore no lleva `name`.
- Marcar la casilla: sus tareas abiertas pasan a enseñar el nombre sin editarlas. Desmarcarla: lo
  pierden.
- Tarea de un cliente sin notas, sin contactos visibles y sin documentos para trabajadores: no
  aparece tarjeta. Tarea sin cliente: no se hace la petición.
- Panel: el detalle de la tarea sigue mostrando el nombre y el enlace al cliente.
