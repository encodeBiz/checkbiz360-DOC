# 07 — Portal del cliente (fase dos, add-on)

**Fecha:** 2026-11-03
**Estado:** **PENDIENTE, aplazado** (Jose, 2026-11-03: «la fase dos déjala como pendiente, concéntrate en la fase 1»). Boceto aprobado en conversación; se detalla en TDR cuando se retome. Depende
de las Fases 2 (cliente en la tarea), 3 (horas e informe) y 4 (documentos del cliente).

---

## Qué es

Un acceso para **el cliente de nuestro cliente**: la presidenta de la comunidad que limpia
Neteges, la hija de Juana, el jefe de obra de la promotora, la agencia que contrató el
montaje. Gente que no es empleada de nadie en la plataforma, que no va a instalar la app y
que no tiene cuenta. Entra por un enlace que la empresa le manda, desde el móvil, y ve **lo
suyo**: cuándo vienen, qué hicieron, qué tiene que firmar, qué puede pedir.

Es el quiosco con otro público ([ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md)):
el quiosco resuelve «tiene que fichar y no tiene app»; el portal resuelve «tiene que ver,
firmar y pedir, y no tiene app».

## Por qué cierra el círculo

Hoy la cadena termina en la empresa: planifica, la trabajadora ficha y deja evidencia, el
informe sale. El cliente final recibe, si acaso, un PDF por correo. Con el portal la cadena
sigue un paso más: **el cliente confirma y firma**, y la firma vuelve al informe. En SAD es
la clienta o su familia firmando el parte de la visita, lo que aplazamos en el TDR-007 de
tasks. En limpieza es la comunidad firmando el parte mensual con las fotos. En construcción
es el jefe de obra firmando el parte de horas que después va a la certificación. En eventos
es la agencia firmando el acta de montaje. Nadie en nuestros nichos junta las cuatro puntas:
fichaje, tarea con evidencia, cliente que firma, informe con todo detrás.

## Lo que copiamos de otros, y de quién

Se miraron el 2026-11-03 los portales de cliente de los productos de referencia en cada
sector. Lo que vale la pena copiar, con su origen, y lo que se deja fuera a propósito:

| Idea | De quién | Qué hacemos |
|---|---|---|
| **Entrar por enlace, sin contraseña.** El cliente recibe un enlace por correo o SMS; pasado un tiempo sin enlace nuevo, confirma el correo o los últimos dígitos del teléfono | Jobber (Client Hub) | Igual. Enlace con código, caducidad, reconfirmación suave. Nada de cuentas |
| **Acceso que se apaga solo.** Si el cliente deja de estar activo, el portal deja de abrir | Birdie (Family App) | Igual: desactivar al cliente o al contacto corta el acceso en el acto |
| **Solo lectura por defecto, y la comunicación con la empresa, no con la trabajadora** | Birdie | Igual. El cliente escribe al gestor, no a la auxiliar. La relación la lleva la empresa |
| **Próximas visitas con quién viene**, nombre y foto; la empresa decide si enseña la hora exacta o solo el día | Jobber | Igual: calendario de sus lugares, nombre y foto de quien viene, hora o solo día por ajuste de la empresa |
| **Quién está ahora en mi edificio** | Janitorial Manager | Igual, por lugar, opcional por empresa: nombre y desde qué hora. Sale del fichaje y de la tarea iniciada |
| **Solicitudes con foto y seguimiento**: pedir un trabajo extra, avisar de una incidencia, pedir material, agradecer; ver en qué estado está | Janitorial Manager, BigChange, Jobber | Igual. La solicitud llega al gestor de la sucursal, puede convertirse en tarea con un clic, y el cliente ve el estado |
| **Documentos por carpetas**: contratos, certificados, fichas de seguridad | Janitorial Manager | Igual, desde el documental del cliente (Fase 4): la empresa marca qué documento se comparte al portal |
| **Aprobar con firma y registro de qué vio y cuándo** | Jobber (presupuestos), Buildertrend (órdenes de cambio) | Igual para **partes y presupuestos**: el cliente firma en el portal y queda sellado con la firma electrónica que ya tenemos |
| **Parte de trabajo firmado por el cliente con fotos** | STEL Order | Es nuestro parte de servicio (tarea con evidencias) y nuestro parte del mes (informe por cliente), firmables |
| **Resultados de inspección con fotos y puntuación por zona, exportables** | Janitorial Manager, CleanTelligent | Más adelante: hoy la validación de la tarea con puntuación es del supervisor; enseñarla al cliente es una casilla, no un módulo |
| **Valoración tras la visita, encuestas de satisfacción** | AlayaCare, Gesad | Igual, sencillo: una valoración por visita o por mes, visible para la empresa |
| **Aviso «vamos de camino» / hora estimada** | Housecall Pro, BigChange | Más adelante, y solo si se pide: exige la posición del trabajador en tiempo real, que hoy no guardamos |
| **Contrato por centro con frecuencia, SLA de incidencias y hoja mensual de servicio** | ES Servicios Limpieza (Odoo) | Para el **core**, no para el portal: confirma la [D4 del 06](./06_decisiones-abiertas.md) (frecuencia en el contrato) y el informe mensual por cliente |

**Lo que se deja fuera a propósito**, aunque lo tengan todos: **pagar facturas** en el portal,
cartera de tarjetas, **reservar cita** desde el portal, **recomendar a un amigo**. Lo primero
es facturación ([ADR-004](./adr/ADR-004-la-tarifa-valora-no-factura.md)); lo segundo no
encaja en servicios con contrato; lo tercero es marketing del cliente, no nuestro.

## Qué ve el cliente

Una web para móvil, sin instalar nada, con pestañas. Todo filtrado a **sus lugares**: un
cliente con tres edificios ve los tres, nunca lo de otro cliente.

**Calendario.** Las próximas visitas en sus lugares (tareas con su cliente, y jornadas en
sucursales dedicadas), con quién viene, nombre y foto. La empresa decide por cliente si
enseña la hora o solo el día. Las pasadas, con lo que se hizo y las evidencias que la empresa
haya marcado como compartibles.

**Hoy.** Quién está ahora en su lugar y desde cuándo. Opcional por empresa.

**Documentación.** Lo que la empresa le comparte desde el documental del cliente: contratos,
certificados, seguros, fichas de seguridad, el parte del mes. Cada documento con su estado:
*para leer*, *pendiente de firma*, *firmado el …*. Firmar es un gesto en el móvil; lo que se
sella es el PDF, con la evidencia de quién, cuándo y desde dónde.

**Partes.** El parte de servicio de cada visita (la tarea: qué se hizo, quién, cuánto, fotos
compartibles) y el **parte del mes** (el informe por cliente de la Fase 3, en su versión para
el cliente, sin tarifas ni desvíos salvo que la empresa quiera enseñarlos). Los dos
firmables.

**Solicitudes.** Pedir un trabajo extra, avisar de una incidencia con foto, pedir material,
dar las gracias a alguien. Cada una con su estado: *recibida*, *en curso*, *hecha*, y la
respuesta del gestor. Si el gestor la convierte en tarea, el cliente ve la visita en el
calendario.

**Contacto.** Teléfono, correo y horario de la empresa, y un hilo de mensajes con el gestor
de su sucursal. Nunca con la trabajadora directamente.

**Valoración.** Una nota y un comentario tras cada visita o cada mes, a elección de la
empresa. La empresa la ve en la ficha del cliente y, agregada, en el panel operativo.

## Qué controla la empresa

Todo desde la ficha del cliente, pestaña **Portal**:

- Qué contactos tienen acceso; mandar o revocar el enlace.
- Qué se enseña: hora exacta o solo día; quién está ahora sí o no; valoración sí o no.
- Qué documento se comparte al portal (casilla en el documental, por documento) y cuál pide
  firma.
- Qué evidencias de cada tarea se comparten (casilla por recurso, `shareWithCustomer`; por
  defecto ninguna: la foto de la trabajadora en casa de Juana no sale sin que alguien lo
  decida).
- Si el parte del mes lleva importe o solo horas.
- Lo pendiente del cliente: firmas que faltan, solicitudes sin responder, valoraciones
  recientes.

## Cómo entra el cliente

1. La empresa marca a un contacto del cliente con acceso al portal. `customers` genera un
   enlace con un token de un solo uso y se lo manda por correo (o lo da para copiar y mandar
   por WhatsApp, que es como se habla con una presidenta de comunidad).
2. El enlace abre el portal y deja una sesión larga en ese navegador. Pasados N días sin
   enlace nuevo, el portal pide confirmar el correo o los últimos cuatro dígitos del
   teléfono del contacto antes de volver a entrar.
3. Desactivar al contacto, al cliente o la suscripción del portal corta todas las sesiones.
4. Cada entrada, cada apertura de documento y cada firma quedan registradas con fecha,
   dirección y dispositivo. Es lo que da valor legal a la firma y lo que la empresa enseña si
   hay una discusión.

No hay cuenta de Firebase Auth para el cliente: no es un usuario de la empresa, no entra en
`users` ni en las reglas de Firestore. El portal habla con `customers` por HTTP con su
sesión, y `customers` lee lo que haga falta.

## La firma

Es la **firma electrónica que ya tenemos en el servidor** (PAdES, sellado por la plataforma)
con el firmante identificado por el acceso al portal: contacto, enlace usado, momento,
dirección y dispositivo. No se pide certificado al cliente; la evidencia es la cadena de
acceso, igual que Jobber y Buildertrend sellan «qué vio y cuándo aprobó». Para el parte de
servicio de SAD y el parte mensual de limpieza es más que suficiente; si un cliente de
construcción necesita firma cualificada para una certificación, esa es otra conversación y
otro proveedor.

Lo que se firma es siempre un PDF del documental del cliente: el parte lo genera `reports`
y lo deposita como documento del cliente con `requiresAcknowledgement`; el portal lo enseña
*pendiente de firma*; la firma lo sella y sustituye el fichero, como hace hoy el documental
con los empleados.

## Dónde vive

Dentro de `customers`, bajo `/api/v1/customers/portal/*`, con autenticación propia (sesión
de portal) y `requirePortalSubscription` delante. Colecciones nuevas, todas del cliente:
`customer_portal_access` (contacto, token, caducidad, último acceso, estado),
`customer_requests` (solicitudes con estado, fotos y respuesta), `customer_messages` (hilo
con el gestor), `customer_ratings`. Y dos casillas fuera: `shareWithCustomer` en el recurso
de la tarea y `sharedToPortal` en el documento del cliente. Espejo a Postgres de solicitudes
y valoraciones, para el panel operativo y Merlin.

El front del portal: una web pequeña y aparte, para móvil, servida por `customers` o por el
panel bajo su propia ruta pública. **No es el panel** y no comparte sesión con él.

## Fases dentro de la Fase 6

- **6a — Entrar, ver y firmar.** Acceso por enlace, Calendario, Documentación con firma,
  Partes. Es lo que cierra el círculo y lo que se vende primero.
- **6b — Pedir y hablar.** Solicitudes con conversión a tarea, Contacto con hilo, Hoy (quién
  está).
- **6c — Valorar y aprobar.** Valoración por visita o mes; aprobar presupuestos con firma.

## Decisiones que quedan para el TDR

- Si el portal se cobra por plantilla o por contacto con acceso activo ([06 §D1](./06_decisiones-abiertas.md)).
- Cuánto dura la sesión larga y cada cuánto se reconfirma.
- Si el parte de servicio se firma por visita (SAD) o solo el del mes (limpieza), o la
  empresa elige por cliente. Probablemente lo tercero.
- Idioma del portal: el del contacto, si no el de la empresa, si no inglés
  (`feedback-idioma-ultimo-ingles`).

## Fuentes consultadas (2026-11-03)

- Jobber Client Hub: [qué ve el cliente](https://help.getjobber.com/en/articles/what-do-your-clients-see-in-client-hub/), [aprobación de presupuestos con firma](https://help.getjobber.com/es/articles/quote-approvals/)
- Birdie Family App: [producto](https://www.birdie.care/product-tour/family-app), [ayuda](https://help.birdie.care/en/articles/6006503-the-care-circle-birdie-app-for-family-friends)
- Janitorial Manager: [Client Portal](https://www.janitorialmanager.com/?p=53716), [inspecciones](https://www.janitorialmanager.com/work-management-system/janitorial-inspections-app/)
- CleanTelligent / Otuvy: [FAQ](https://cleantelligent.com/about-us/frequently-asked-questions/)
- Housecall Pro: [portal del cliente](https://www.housecallpro.com/features/customer-portal/), [notificaciones](https://help.housecallpro.com/notifications/what-job-notifications-will-my-customers-receive)
- BigChange: [portal del cliente](https://www.internationalrentalnews.com/news/bigchange-launches-customer-portal/8031456.article)
- AlayaCare Family Portal: [producto](https://alayacare.com/family-portal/), [folleto](https://alayacare.com/wp-content/uploads/2023/06/family-portal.pdf)
- Gesad (Trevenque), SAD en España: [balance 2021](https://www.trevenque.es/wp-content/uploads/2021/11/gesad-balance-noviembre.pdf); Urgatzi Familias: [App Store](https://apps.apple.com/us/app/id1605146899)
- Buildertrend: [portal del cliente](https://buildertrend.com/communication/construction-client-portal/)
- STEL Order: [partes de trabajo](https://www.stelorder.com/partes-de-trabajo/), [funcionalidades](https://www.stelorder.com/funcionalidades/)
- ES Servicios Limpieza (Odoo): [módulo](https://apps.odoo.com/apps/modules/19.0/es_limpieza_servicios)
- Rentman vs Current RMS (eventos, aprobación de presupuesto por enlace): [comparativa](https://rentman.io/rentman-vs-current-rms)

Casi todo es material del propio fabricante; se copia la idea, no la afirmación de que
funcione bien.
