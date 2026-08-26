# Integraciones (add-ons)

Cómo se construye, se conecta y se cobra una integración en checkbiz360. RentmanBiz es la
primera, y este apartado fija el modelo para las que vengan.

---

## 1. Qué es un add-on, y qué no

Un add-on es un **módulo activable y de pago** que conecta checkbiz con un sistema de
terceros. No es una funcionalidad del producto: el cliente que no lo contrata no debe
notar que existe, ni en su interfaz ni en su factura ni en su modelo de datos.

De ahí la **regla de oro**, que aplica a todas:

> El adaptador absorbe todo. checkbiz360 no se modifica para cumplir con el sistema externo.

En la práctica: el código vive en `services/<integración>/` dentro de **encodebiz-api**;
sus tablas llevan prefijo propio (`rentman_*`); las tablas y colecciones del core
(`checklogs_raw`, la configuración de centro en Firestore) se leen en **solo lectura**;
y las peculiaridades del tercero —campos obligatorios, unidades raras, formatos de
referencia— se traducen dentro del adaptador, nunca aguas arriba.

Dos corolarios que conviene tener presentes:

- **No se contamina el SaaS.** Nada del add-on entra en `encodeBiz-SAAS` ni en sus Cloud
  Functions. Si un add-on necesita exponer algo, lo expone su propio microservicio.
- **Si mañana se retira la integración**, basta con apagar el servicio y borrar sus
  tablas. No quedan cicatrices en el producto.

## 2. El catálogo: colección `addons`

Antes no existía. La creó Rentman y por eso su documento fija la forma. La colección es
**plana**, un documento por add-on, con el id del add-on como id del documento:

```
addons/{addonId}
```

La estructura calca la del catálogo de servicios (`service/{id}`) para que el front
reutilice lo que ya sabe pintar, y añade lo que un add-on tiene y un servicio no.

| Campo | Para qué |
|---|---|
| `id`, `name`, `order`, `active` | Identidad y orden en el catálogo |
| `status` | `active` · `beta` · `coming_soon` — gobierna si se puede activar |
| `requires` | De qué producto cuelga (Rentman: `["checkinbiz"]`) |
| `vendor` | Nombre y web del tercero |
| `description` | Una línea: la que va bajo el nombre en la tarjeta |
| `about` | **El párrafo**: qué es y por qué importa. Lo que se lee antes de activar |
| `featuredList` | Lista de funcionalidades, en bullets |
| `target` | El valor en bloques `{title, description}` |
| `steps` | Asistente de conexión, paso a paso |
| `connection` | Qué credencial pide, con qué endpoints se guarda y se prueba |
| `capabilities` | Qué sabe hacer, cada una con su `status` y su `direction` |

Todos los textos son bilingües `{es, en}`.

**Quién lo escribe:** cada módulo siembra su propia ficha. En Rentman, el contenido vive
en `services/rentman/src/domain/addonCatalogue.ts` (dato puro, sin dependencias) y lo
publica `scripts/seed-addon-catalogue.ts`, que es idempotente. Así el copy del catálogo
se revisa en el mismo PR que el código que lo cumple.

**Quién lo lee:** el front, directamente de Firestore, igual que ya lee `service`. No
hace falta endpoint intermedio, y así el catálogo no obliga a tocar el SaaS.

## 3. La conexión: dónde vive la credencial

El token del tercero es **por entidad** y se guarda cifrado:

```
entities/{entityId}/addons/{addonId}          ← mismo nombre que el catálogo
  ├── active           el add-on está dado de alta en la entidad (paso 1)
  ├── status           disconnected | connected | error            (paso 2)
  ├── tokenEncrypted   AES-256-GCM con ENC_KEY (solo en el servidor)
  ├── tokenRef         "*****Jy7Pts" — referencia visible, para reconocerlo
  └── activatedAt · connectedAt · updatedAt
```

Detalle completo, con los cuatro verbos del ciclo de vida, en
[`contrato-activacion.md`](contrato-activacion.md).

Nunca se guarda en claro, no está en ningún `.env` y solo se descifra en memoria para
construir el cliente de la API. `ENC_KEY` es **común a todos los add-ons** — se llamaba
`RENTMAN_ENC_KEY` y se renombró justo por eso.

El flujo desde el front es siempre el mismo: **activar** (alta, sin credencial) →
**conectar** (la credencial se valida contra el tercero y se cifra) → emparejar lo que
haya que emparejar → listo. Activar y conectar son dos gestos distintos a propósito.

## 4. Autenticación de los endpoints

Cada microservicio de integración expone tres familias de rutas:

- **Gestión** (`/api/v1/<addon>/…`) — Firebase ID token. Es lo que llama el front.
- **S2S** (`/api/v1/<addon>/sync/…`) — cabecera `x-encodebiz-key`. Disparo manual y
  operación. Va en su **propio prefijo**: montar el middleware sobre la raíz del servicio
  se lo aplicaría a todo y exigiría las dos credenciales a la vez.
- **Público**, si lo hubiera (webhooks) — verificado por secreto del tenant.

## 5. Sincronización: sondeo, no webhooks

Decisión tomada en Rentman y buena por defecto para las demás (ver
`rentman-integration/adr/0001`): se sincroniza **por sondeo** desde el propio servicio.
Un webhook perdido se pierde para siempre; una pasada fallida la retoma la siguiente.

Tres cosas que toda sincronización debe traer de serie:

1. **Idempotencia por huella del contenido**, no por marca de tiempo. Lo mismo no se
   envía dos veces; lo corregido se reenvía solo.
2. **Presupuesto de llamadas por pasada** y sin solape entre pasadas, que el techo de la
   API del tercero rara vez está documentado.
3. **Distinguir el "no" definitivo del fallo transitorio.** Un 400 no mejora
   reintentándolo; un 429 o un 5xx sí.

## 6. Monetización

Un add-on se cobra como se cobran checkbiz y passbiz: servicio + planes en Firestore,
reutilizando el motor de facturación existente. **Pendiente** para Rentman: crear el
servicio y sus planes y fijar tarifa. El catálogo (`addons`) es el escaparate; la
facturación es otra cosa y no debe mezclarse con él.

## 7. Integraciones actuales

| Add-on | Estado | Detalle |
|---|---|---|
| [RentmanBiz](rentman.md) | beta — capa de horas en producción de código, catálogo sembrado en dev | `rentman-integration/` |

---

- Diseño completo de Rentman: `../rentman-integration/` (as-is, to-be, decisiones, fases, ADRs).
- **Front — contrato y prompt completos**: [`prompt-front-rentmanbiz.md`](prompt-front-rentmanbiz.md).
- Prompt anterior, sólo del panel: [`prompt-agente-front.md`](prompt-agente-front.md).
- Avisos y notificaciones (diseñado, pendiente de implementar): [`avisos-y-notificaciones.md`](avisos-y-notificaciones.md).
