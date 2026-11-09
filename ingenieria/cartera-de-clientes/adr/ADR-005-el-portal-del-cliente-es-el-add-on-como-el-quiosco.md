# ADR-005 — El portal del cliente es el add-on, como el quiosco

**Fecha:** 2026-11-03
**Estado:** Aceptado (boceto del portal en [07](../07_portal-del-cliente.md); se detalla al arrancar la fase)
**Decisionario:** Jose Acevedo

---

## Contexto

La cartera básica es gratuita y vive en el panel ([ADR-001](./ADR-001-servicio-customers-en-el-core-gratuito.md)).
La fase dos es un espacio para **el cliente de nuestro cliente**: la presidenta de la
comunidad, la familia de Juana, el jefe de obra de la promotora, la agencia que contrató el
montaje. Personas que no son empleados de nadie en la plataforma, que no van a instalar la
app y que no tienen cuenta.

Ya existe un precedente de «acceso para quien no tiene app ni cuenta»: el **quiosco**, una
pantalla en el centro de trabajo para fichar, servicio aparte (`kiosk` en `SERVICES`),
cobrado aparte.

## Decisión

El portal del cliente es **un add-on de pago sobre checkinbiz, con la mecánica del quiosco**:
servicio cobrable con su valor en `SERVICES` (`customer_portal`), puerta de suscripción
delante de todas sus rutas, precio en Stripe, factura aparte, plantilla de correo de alta.

Vive **dentro del servicio `customers`**, bajo `/api/v1/customers/portal/…`, con
**autenticación propia**: el cliente entra por un enlace que la empresa le manda a su
contacto, no por Firebase Auth de la empresa.

## Justificación

**Se cobra donde hay valor para alguien nuevo.** El portal da a una persona que hoy no toca
la plataforma la posibilidad de ver cuándo vienen, firmar el parte, pedir algo y leer el
informe con las fotos. Eso se paga, y la empresa lo repercute o lo usa para vender.

**Es el quiosco con otro público.** El quiosco resuelve «esta persona tiene que usar la
plataforma y no tiene app ni cuenta». El portal resuelve lo mismo para el cliente. Misma
puerta, mismo alta en billing, misma lógica de «con add-on todo, sin add-on nada».

**Dentro de `customers`, no servicio aparte.** El portal no tiene datos propios que no sean
del cliente: lee sus lugares, sus tareas, sus documentos, su informe. Separarlo en otro
proceso obligaría a llamadas S2S para todo. Lo que sí separa es la **autenticación** (sesión
de portal, no credencial de empresa) y la **puerta** (solo sobre `/portal`).

**Autenticación propia porque el cliente no es un usuario.** Un contacto del cliente no
tiene correo corporativo de la empresa, no tiene roles, no aparece en la plantilla. Darle
una cuenta de Firebase Auth de la empresa sería meterlo en `users` y en las reglas de
Firestore. El enlace con código y caducidad es lo que hacen los portales de referencia
([07 §Lo que copiamos](../07_portal-del-cliente.md)) y lo que la empresa entiende: «le mando
el acceso».

## Consecuencias

- `customer_portal` en `SERVICES` y en `PLATFORM_SERVICES`; plan `standard`; precio en
  Stripe (tramos sobre la plantilla como inventario, o por cliente con portal activo:
  [06 §D1](../06_decisiones-abiertas.md)); 15 días de prueba; plantilla de correo.
- `requirePortalSubscription` delante de `/api/v1/customers/portal/*` **y** delante de las
  rutas del panel que gestionan el portal (dar acceso a un contacto, compartir un documento
  al portal). Lo demás de `customers` sigue sin puerta.
- Sesión de portal: `customer_portal_access` con el contacto, un token de enlace con
  caducidad, el último acceso y el estado. Desactivar al cliente o al contacto apaga el acceso
  en el acto.
- El panel gana, en la ficha del cliente, la pestaña **Portal**: quién tiene acceso, qué se
  comparte, qué está pendiente de firma, qué ha pedido el cliente.
- Darse de baja del portal apaga los enlaces y la pestaña; **no borra** nada: mensajes,
  solicitudes y firmas quedan en el cliente, que es del core.
