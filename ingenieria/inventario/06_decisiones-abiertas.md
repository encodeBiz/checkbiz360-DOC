# 06 — Decisiones abiertas y aplazadas

Lo que falta por responder, y lo que se ha aplazado con su boceto para no discutirlo desde
cero. Ninguna bloquea la Fase 0.

---

## D1 — Qué cuentan exactamente los dos clientes que lo piden

**Bloquea:** el orden entre las Fases 2 y 3.
**Estado:** sin respuesta.

El modelo cubre los dos tipos; lo que depende de esto es **el orden**. Si los dos son de
limpieza y lo que les duele es el consumible, la Fase 3 puede esperar; si uno es de construcción
y quiere cuadrar maquinaria, la Fase 3 sube antes que los informes.

Hace falta lo que pidieron **con sus palabras**, no una interpretación.

---

## D2 — Precio del add-on

**Bloquea:** nada.
**Estado:** **decidida el 2026-09-29** por Jose.

**29 € al mes hasta 50 empleados, y 0,75 € por cada empleado a partir del 51.** El precio
escala con la envergadura de la empresa y la envergadura la dan los empleados: 10 empleados,
29 €; 50, 29 €; 51, 29,75 €; 100, 66,50 €; 120, 81,50 €; 200, 141,50 €. Servicio y factura
**aparte**, suscripción propia en Stripe. Sin tope de ejemplares ni ningún otro límite: **un
límite de plan nunca para el servicio; si se pasa, se cobra**. Nunca por movimiento. Los mismos **15 días de prueba** de la plataforma (`BILLING_TRIAL_DAYS=15`; el 45
es solo el valor por defecto del código).

**No se elige plan: el precio es reactivo.** Hay un único plan, `standard`; la cantidad es la
plantilla y el tramo lo aplica Stripe, así que el precio sube y baja solo con la empresa. Y
**los importes los controláis vosotros en cada momento**: viven en el precio de Stripe, no en
el código, y se cambian allí sin desplegar nada.

**Cómo se cobra sin código nuevo:** un precio en Stripe con tramos **graduados**
(`tiers_mode: graduated`): tramo 1, hasta 50, `flat_amount` 29 € y unidad 0; tramo 2, desde 51
hasta infinito, 0,75 € por unidad. La cantidad sigue siendo el número de empleados, así que
`getCount`, el recuento al fin de prueba y `syncQuantity` funcionan tal cual. `inventory` es
otro `serviceId` con la misma forma de plan.

Graduado y no por volumen a propósito: por volumen, a 51 empleados todo pasaría a 0,75 y la
factura saltaría de 29 a 38,25 €; graduado, el empleado 51 cuesta 0,75 € y ya.

**Por qué este modelo:** el 29 € fijo le dice al cliente que esto es un módulo, no una función
—y es lo que compra el esfuerzo de cargar el catálogo en la puesta en marcha—; el 0,75 por
cabeza a partir de 50 hace que las cuentas grandes paguen en proporción sin que el precio se
vuelva invisible. Referencias: Bronze está a 5 € de lista y 2 € en la tarifa 2026; las
herramientas de inventario sueltas para pyme (Sortly, EZOfficeInventory, el módulo de Odoo) se
mueven, de memoria y **a confirmar antes de publicarlo**, entre 25 y 50 € al mes o 25 € por
usuario, y ninguna sabe qué tarea gastó qué.

**Lo que se descartó por el camino:** 1 €/empleado lineal (justo, pero se lee peor en una
factura aparte); tramos 19/29/49 € (escalones y un tramo alto que salía más barato que el
anterior); 0,50 €/empleado lineal (simple, pero a 15 € al mes el cliente no invierte en
cargarlo).

**Lo que cede:** una empresa de 10 personas en la tarifa 2026 paga 29 € por el add-on y 20 €
por el plan base. Es una decisión consciente: el módulo vale eso, y una empresa de 10 con
almacenes es rara.

**Antes de fiarse:** confirmar que el webhook pasa la suscripción local de `pending` a
`trialing` al arrancar la prueba —la puerta acepta `active` o `trialing`— o el cliente
contrata y ve el módulo cerrado quince días. Y que el alta empuje a crear el primer almacén y
los primeros artículos en la misma sesión: quince días con el catálogo vacío no enseñan nada.

---

## D3 — Sin conexión: aplazado, con boceto

**Bloquea:** nada en v1.
**Estado:** verificado que la app no escribe en Firestore ni tiene cola local; **fuera de v1**
por decisión del 2026-09-28. Todo va por API.

Cuando se retome, la forma acordada:

- **Copia local** de la petición en el almacenamiento del dispositivo, solo cuando no hay red o
  la API falla. Se avisa al operario de que se guardará y se enviará después.
- **Reenvío idempotente** al recuperar cobertura: el `movementId` lo genera la app, así que el
  reenvío es el mismo apunte, tarde lo que tarde.
- **La hora del hecho, no la de la sincronización.** La app manda `occurredAt`; la API ya lo
  acepta desde la v1. Sin eso, una cola de tres horas diría que todo se gastó a las cinco.
- **Un apunte que llega tarde entra igual**, aunque la tarea ya esté validada y el sobrante
  cuadrado. No se rechaza —sería borrar un gasto que ocurrió—: se registra, se marca como
  llegado tras el cierre y se enseña como discrepancia.
- **Caché de lectura** de la pantalla de material, además de la cola de escritura: el operario
  también tiene que ver «lo que lleva» sin señal.

Es trabajo de app de verdad, con su liberación manual, y se presupuesta como fase propia.

---

## D4 — Respaldo de Postgres

**Bloquea:** el pase a producción.
**Estado:** en el repo no hay nada programado; solo un `pg_dump` comentado en
`docker-compose.yml`.

Con el libro espejado en Postgres, la copia consultable de la trazabilidad vive ahí. Hay que
confirmar si existe respaldo a nivel de máquina en OVH y, si no, programarlo antes de
producción.

---

## D5 — Alta del servicio en `billing`

**Bloquea:** el cobro real.
**Estado:** definido; sin código.

No hay ningún trigger que portar: `onActivateCheckbiz` ya está en este repo y solo crea la
sucursal inicial, y la suscripción la escribe `billing`. Lo que hace falta es `inventory` en el
tipo `SERVICES` (`packages/shared/src/platform/Service.ts`), en `OUR_SERVICES` de
`StripeWebhookHandler.ts`, los planes en `service/inventory/plan/*` y el precio en Stripe.

---

## D6 — Tiempo mínimo entre asignaciones de un operable

**Bloquea:** nada en v1.
**Estado:** aplazado a después de la Fase 3.

Dos tareas seguidas con la misma fregadora en obras distintas no chocan en el calendario pero
son imposibles en la carretera. Y un animal necesita descanso obligatorio entre jornadas. Es el
mismo campo para los dos casos; su hermano natural es un máximo de uso diario.

---

## D8 — Cómo confirma el trabajador la entrega de un EPI — DECIDIDO (2026-10-08)

Fase 6 ([07 §4.5](./07_operables-documentos-y-entregas.md)). Se propuso firma dibujada opcional.
Jose: «lo de la firma quiero hacerlo mediante biometría; creo que Flutter lo tiene, y en su
defecto, o sea que el móvil no lo tenga, necesito una alternativa».

**Decidido:** biometría, con escalera: (1) huella o cara que desbloquea una clave del chip
seguro del móvil y **firma** un reto del servidor, que la comprueba (`biometric_signature`;
`local_auth` ya está en la app pero solo devuelve sí/no); (2) sin biometría, el PIN o patrón
del móvil; (3) sin bloqueo de pantalla, la contraseña de la cuenta. El servidor guarda qué nivel
fue y si la firma se verificó. Sin firma dibujada. Queda por probar en 6c el paquete en
móviles reales de gama baja.

## D9 — EPIs consumibles: fuera de la Fase 6 por decisión

Jose, 2026-10-07: «esto es estricto contra operables». Un EPI que se entrega es un ejemplar,
con identificador o sin él. La entrega de **cantidades** a una persona (una caja de mascarillas,
veinte pares de guantes desechables) no entra. Si un cliente lo pide, el modelo lo admite como un
movimiento más del libro (`delivery`, de almacén a persona, con acuse) sin tocar lo de la Fase 6.

## D7 — ¿Entran artículos y almacenes en `searchIndex`?

**Bloquea:** Fase 1.
**Estado:** sin decidir.

Si se buscan desde el panel, entran — y su borrado tiene que acordarse de retirar la entrada.
