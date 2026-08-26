# Avisos y notificaciones de un add-on

> **Estado: diseñado, no implementado.** Se deja escrito ahora para que no se pierda; la
> implementación va al final, cuando el flujo esté probado. Lo que ya existe es el
> endpoint que alimenta todo esto: `GET /api/v1/{addonId}/pending/{entityId}`.

---

## 1. El problema que resuelve

Una integración deja cosas a medias por definición: gente sin correo, centros sin
geocerca, plazas sin tarifa, tareas de almacén sin repartir. Si eso vive sólo dentro de
una pantalla del add-on, **nadie entra a mirarlo** y el cliente descubre el problema el
día que alguien no puede fichar.

El objetivo no es avisar mucho, es avisar **lo justo, a quien puede arreglarlo y por
donde lo va a leer**.

## 2. Qué genera aviso

| Aviso | Por qué importa | Quién lo arregla |
|---|---|---|
| Persona sin correo | No tiene acceso: no puede fichar, y no se le factura | Administrador |
| Centro sin geocerca confirmada | Existe pero está inactivo: nadie puede fichar ahí | Administrador |
| Plaza sin tarifa | El coste de esa jornada sale a cero en los informes | Administrador |
| Tarea de almacén sin asignar | El material tiene fecha de salida y nadie tiene el encargo | Supervisor del almacén |
| Horas divergentes | Alguien editó en Rentman unas horas ya imputadas | Administrador |
| Jornadas rechazadas | Rentman no las acepta (solape con otras horas o una ausencia) | Administrador |
| Credencial inválida | La integración ha dejado de sincronizar | Administrador |

Todos salen del mismo sitio: la tabla `rentman_catalogue_item` con su motivo, y
`rentman_time_registration` para lo de horas. **Ningún aviso se calcula dos veces.**

## 3. Dónde se ve

**En el catálogo de add-ons.** La tarjeta de RentmanBiz muestra un indicador cuando
`pending.summary.total > 0`. En cero **no muestra nada**: un aviso permanente deja de
leerse en una semana.

**En la pantalla del add-on.** El listado de pendientes agrupado por tipo, cada línea con
su motivo y **enlace directo a la ficha** donde se arregla — la del empleado, la del
centro, la de la tarea. El add-on avisa y te lleva; se arregla en la pantalla del
producto, que es la que sabe validar.

**En el panel general**, si se quiere ir más lejos: un aviso al entrar cuando hay cosas
que ordenar. Decisión de producto, no del add-on.

## 4. A quién se le manda

- **Administradores de la entidad** — todo lo que es configuración: correos, geocercas,
  tarifas, credencial caída, divergencias.
- **Supervisores del almacén afectado** — sólo las tareas sin asignar de **su** centro.
  Al responsable del Eastern Warehouse no le importan las del Western.

Los destinatarios salen de las responsabilidades: quien tiene `manager` u `owner` en ese
centro. No hace falta una lista aparte que mantener.

## 5. Por dónde

Se reutiliza lo que ya existe en `@encodebiz/shared`, **sin inventar un canal propio**:

- **In-app**: `FirestoreAppNotificationsRepository` (colección `in_app_notifications`).
- **Push**: `CheckbizNotifier` / `CheckbizPushMessageFactory`, con los textos en
  `messages.ts` — ahí van los nuevos, no en el add-on.
- **Email**: `EmailService` con su plantilla, para el resumen.

Regla: **el add-on emite el hecho, la plataforma decide cómo se entrega.** Si mañana se
añade WhatsApp, lo gana también sin tocar la integración.

## 6. Cuándo (y cuándo no)

Esta es la parte que decide si el sistema es útil o se convierte en ruido:

- **Al cambiar de estado, no en cada pasada.** El sync corre cada 15 minutos; notificar
  cada vez las mismas 22 personas sin correo sería insoportable. Se avisa cuando **aparece
  algo nuevo**, comparando contra lo ya notificado.
- **Agrupado**: "22 personas sin correo", no 22 avisos.
- **Resumen por correo una vez al día**, no en tiempo real. Nada de esto es una urgencia:
  lo urgente es que alguien no pueda fichar, y eso se ve al intentarlo.
- **Excepción, sí inmediato**: la credencial dejó de funcionar. Ahí la sincronización está
  parada y cada hora cuenta.
- **Silencio si no hay nada.** Ningún "todo va bien" periódico.

## 7. Lo que falta decidir

1. Si el aviso llega también al **panel general** o se queda dentro del add-on.
2. Si el resumen diario por correo va a todos los administradores o a uno designado.
3. Si las tareas de almacén sin asignar avisan al supervisor **al crearse** o sólo si
   siguen sin repartir a X horas de la salida del material — esto último es más útil y
   bastante menos molesto.

## 8. Cómo se implementaría

1. Un `pendingSummary` por entidad ya existe. Se guarda **la última huella notificada**
   en la tabla del add-on: si el conjunto no cambió, no se vuelve a avisar.
2. Un paso al final de cada pasada de sync compara y, si hay novedad, emite.
3. Los textos, en `messages.ts` de shared, junto a los demás del producto.
4. Los destinatarios, resolviendo responsabilidades por centro.

Nada de esto necesita infraestructura nueva. Es pegamento entre lo que el add-on ya sabe y
lo que la plataforma ya sabe entregar.
