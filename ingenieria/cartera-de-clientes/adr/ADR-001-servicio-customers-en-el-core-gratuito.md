# ADR-001 — Servicio `customers` dedicado, parte del core de checkinbiz y gratuito; el portal es lo que se cobra

**Fecha:** 2026-10-29 · **revisado el 2026-11-03**
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

La primera versión de este ADR (29-oct) hacía de la cartera un add-on de pago calcado del
inventario: servicio propio con puerta de suscripción delante, precio en Stripe, factura
aparte. El 3-nov Jose lo giró con una razón de producto:

> El módulo será *free* en una primera versión, y después surge la fase dos: un apartado como
> el quiosco pero para los clientes de nuestros clientes, donde pueden recibir documentación
> para firmar, contactar, revisar el calendario y demás. El básico es desde el panel. Es
> necesario para cerrar el círculo del core para nuestros nichos principales.

Lo que cambia no es dónde vive el código, sino **qué es**. El cliente no es un extra sobre el
producto: es la pieza que le falta al producto para que funcione en limpieza, ayuda a
domicilio, eventos y construcción. Sin él, el horario por tareas de Neteges no cierra, la
tarea de SAD no sabe a quién va y la obra no sabe de quién es. Cobrar por eso sería cobrar
por terminar lo que ya venden.

## Decisión

1. **La cartera básica es parte de checkinbiz y es gratuita.** Toda empresa con checkinbiz ve
   «Clientes» en el panel. No hay puerta de suscripción, no hay alta en `billing`, no hay
   precio en Stripe. Lo que cubre: clientes con contactos, lugares y sucursales asignadas; el
   cliente en la tarea; horas e informe por cliente; documentos y contratos del cliente;
   tarifas y presupuestos.
2. **El portal del cliente es el add-on**, como el quiosco: un acceso para el cliente de
   nuestro cliente, con su puerta, su precio y su factura aparte
   ([ADR-005](./ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md), [07](../07_portal-del-cliente.md)).
3. **El código sigue en un servicio propio, `customers:3018`.** Sin puerta, pero propio.

## Justificación

**Gratis porque cierra el círculo.** La plataforma vende quién, dónde, cuándo, con qué y con
qué foto. El «para quién» completa la frase; no es una frase nueva. Y es lo que convierte el
horario por tareas en algo que Neteges puede usar sin 134 sucursales falsas.

**Se cobra donde hay valor nuevo para alguien nuevo.** El portal le da algo a una persona que
hoy no toca la plataforma: la presidenta de la comunidad, la hija de Juana, el jefe de obra
de la promotora. Ver cuándo vienen, firmar el parte, pedir algo, leer el informe con las
fotos. Eso ningún competidor de nuestros nichos lo junta con el fichaje y la tarea, y eso sí
se paga. Es el mismo razonamiento que el quiosco: la pantalla para quien no tiene app.

**Servicio propio aunque sea gratis.** Tres razones que sobreviven a quitar la puerta:

- El portal se engancha a él, y el portal sí lleva puerta, autenticación propia (el cliente
  no es un usuario de la empresa) y ritmo propio (enlaces que caducan, firmas, avisos). Eso
  no puede vivir dentro de `tasks`.
- `tasks` ya es grande, y la dirección del acoplamiento sería la equivocada: el núcleo
  pasaría a depender del cliente. Con servicio propio, `tasks` guarda tres campos opacos como
  guarda `workSite`.
- La imputación diaria de horas, el reintento del espejo y el rojo de los contratos son jobs
  que no pintan nada en el camino HTTP de una tarea.

**Si un día hay que cobrar el básico**, la puerta se añade delante del servicio en una
tarde, exactamente como la tiene inventario. Lo contrario, sacar una puerta que ya está
repartida por `tasks`, `documents` y `reports`, costaría semanas. Empezar sin puerta en un
proceso propio deja las dos puertas abiertas.

## Consecuencias

- Puerto **3018**. Bloque en los dos compose, upstream y location en los dos nginx. **Sin**
  `requireCustomersSubscription`, **sin** `GET /access`, **sin** `"customers"` en `SERVICES`
  ni en `PLATFORM_SERVICES`. Las rutas exigen la credencial de checkinbiz como las de `tasks`.
- El panel enseña «Clientes» a toda empresa con checkinbiz. El selector de cliente en la
  tarea aparece en cuanto la sucursal tiene algún cliente asignado; sin clientes, el
  formulario de siempre.
- `reports` añade la columna «Cliente» al informe de tareas y el informe «Por cliente» cuando
  la empresa tiene algún cliente; sin clientes, los informes de siempre.
- `customers` es dueño de su dato. `tasks` guarda `customerId`, `customerSiteId` y un
  snapshot `customer` **sin conocerlos**; el espejo señala los que no resuelven.
- Lo único que toca fuera de su casa: tres campos opcionales en `Task`, un valor en
  `DocumentScope`, dos columnas en `tasks_raw`, y los dos cambios en `reports`.
- **Nombre en código `customers`**, no `clients`: `client` ya es el cliente OAuth del
  asistente y el cliente HTTP de media docena de módulos. En pantalla, «Clientes».
- El portal, cuando llegue, entra como servicio cobrable con su propio valor en `SERVICES`
  (`customer_portal`), su plan, su precio y su plantilla de correo, calcado del quiosco. El
  precio se decide entonces ([06 §D1](../06_decisiones-abiertas.md)).
