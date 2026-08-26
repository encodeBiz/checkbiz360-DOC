# Contrato de activación de un add-on

Cómo se publica un add-on en el catálogo y qué pasa exactamente cuando un cliente lo
activa. Lo fija Rentman por ser el primero, y lo siguen todos: **FleetBiz · Glovo** es el
segundo.

> **Un add-on no es un servicio.** No cuelga de `subscriptions`, no crea planes y —mientras
> estén en **beta**— **no se cobra por activarlo**. Si algún día se cobran, la facturación
> se añade aparte; este contrato no cambia.

---

## 1. Las dos piezas

| | Dónde | Quién escribe | Quién lee |
|---|---|---|---|
| **Catálogo** — qué existe y qué hace | `addons/{addonId}` (raíz) | El propio módulo, con su script de siembra | El front, directo de Firestore |
| **Activación** — quién lo tiene puesto | `entities/{entityId}/addons/{addonId}` | **Solo** el microservicio del add-on | El microservicio y el front |

El mismo `addonId` en los tres sitios: el documento del catálogo, el de activación y el
prefijo de las rutas HTTP (`/api/v1/{addonId}/…`). El nuestro es `rentmanbiz`, siguiendo el patrón Biz del resto de productos
(checkinbiz, passinbiz); el de Glovo sería `fleetbiz-glovo`. Ojo: el **id del add-on** es
nuestro producto; el **vendor** es el tercero (`{ name: "Rentman" }`), y no son lo mismo.

## 2. Catálogo — `addons/{addonId}`

Todos los textos son bilingües en cinco idiomas: `{ es, en, fr, pt, de }`.

```ts
interface AddonCatalogueEntry {
  id: string;                      // "rentmanbiz" · "fleetbiz-glovo" — patrón Biz
  name: string;
  order: number;                   // orden en el catálogo
  active: boolean;                 // false = ni siquiera se lista
  status: "active" | "beta" | "coming_soon";
  requires: string[];              // servicios necesarios, p.ej. ["checkinbiz"]
  vendor: { name: string; url: string };

  description: I18n;               // una línea, bajo el nombre en la tarjeta
  about: I18n;                     // el párrafo: qué es y por qué importa
  featuredList: I18nList;          // funcionalidades, en bullets
  target: I18nBlocks;              // el valor, en bloques {title, description}
  steps: I18nBlocks;               // asistente de conexión, paso a paso

  connection: {
    type: "api_token" | "oauth" | "basic_auth";
    encrypted: true;               // siempre
    fields: Array<{
      key: string;                 // "token", "apiKey", "clientSecret"…
      type: "password" | "text";
      required: boolean;
      label: I18n;
      help: I18n;                  // dónde consigue el cliente ese dato
    }>;
    endpoints: { save: string; test: string; status: string };
  };

  capabilities: Array<{
    id: string;
    status: "available" | "coming_soon";
    direction: "checkbiz_to_external" | "external_to_checkbiz"
             | "bidirectional" | "checkbiz_authority";
    name: I18n;
    description: I18n;
  }>;

  createdAt: string;               // ISO
  updatedAt: string;               // ISO
}

type I18n       = { es: string; en: string; fr: string; pt: string; de: string };
type I18nList   = { [lang: string]: string[] };
type I18nBlocks = { [lang: string]: Array<{ title: string; description: string }> };
```

**Cómo se publica:** el contenido vive en el repo del módulo como dato puro
(`src/domain/addonCatalogue.ts` en Rentman) y lo escribe un script idempotente
(`scripts/seed-addon-catalogue.ts`). Así el copy que lee el cliente se revisa en el mismo
PR que el código que lo cumple, y relanzarlo no rompe nada.

**Por qué `capabilities`:** el front pinta las `available` con check y las `coming_soon`
en gris. Es lo que permite sacar un add-on en beta enseñando la hoja de ruta sin mentir.

## 3. Activación — `entities/{entityId}/addons/{addonId}`

**Activar y conectar no son el mismo gesto**, y separarlos importa: el cliente pasa un
rato en el estado intermedio —dado de alta, aún sin credencial— y es justo donde hay que
poder ayudarle.

```ts
interface AddonActivation {
  addonId: string;
  entityId: string;

  active: boolean;                        // paso 1: el add-on está dado de alta
  status: "disconnected" | "connected" | "error";   // paso 2: la conexión

  // Secreto del tercero, SIEMPRE cifrado (AES-256-GCM con ENC_KEY). Null hasta conectar.
  // El nombre del campo lo elige el add-on; que esté cifrado, no.
  tokenEncrypted: string | null;
  // Referencia enmascarada del secreto en uso: "*****Jy7Pts". Es lo ÚNICO que puede
  // volver al cliente, para que reconozca cuál de sus tokens está puesto.
  tokenRef: string | null;

  lastError?: string | null;
  activatedAt: Timestamp;
  connectedAt?: Timestamp | null;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

### Los cuatro verbos

| Verbo | Endpoint | Qué hace |
|---|---|---|
| **Activar** | `POST /api/v1/{addonId}/activate` | Crea el documento en `disconnected`. Comprueba antes que el servicio del que cuelga esté contratado |
| **Conectar** | `POST /api/v1/{addonId}/connect` | Recibe el secreto, **lo valida contra el tercero**, lo cifra y pasa a `connected` |
| **Desconectar** | `POST /api/v1/{addonId}/disconnect` | Retira la credencial. Sigue de alta, listo para reconectar |
| **Apagar/encender** | `POST /api/v1/{addonId}/active` | Para la sincronización sin borrar nada |

Y para leer el estado: `GET /api/v1/{addonId}/connection/{entityId}` → devuelve
`{active, status, tokenRef, lastError, activatedAt, connectedAt}`. Sin secreto.

### Reglas que no se negocian

1. **El front nunca escribe este documento.** Cifrar es cosa del servidor.
2. **El secreto no se devuelve jamás**, ni enmascarado a medias. Solo `tokenRef`, que es
   una cola insuficiente para reconstruirlo. Para cambiarlo, se manda uno nuevo.
3. **Se valida antes de guardar.** Un secreto inválido en reposo no sirve a nadie y
   enturbia el diagnóstico del día siguiente. Si el tercero lo rechaza, no se persiste.
4. **Apagar no es desinstalar**: `active: false` y nada se borra. Al encender, sigue.
5. **Sin `active` y `connected`, el add-on no trabaja.** Una sola puerta para el sync.

## 4. La puerta: sin servicio contratado no hay add-on

Un add-on no se sostiene solo. RentmanBiz sincroniza jornadas: sin **checkbiz** activo no
hay jornadas, y activarlo sería vender humo. Por eso el alta comprueba primero:

```
entities/{entityId}/subscriptions/{serviceId}  →  { serviceId, plan, status: "active" }
```

Si no está activo, `POST /activate` responde **409** `{ error: "service_not_active",
requiredService: "checkinbiz" }`, y el catálogo debe mostrar el add-on bloqueado
explicando por qué. El campo `requires` de la ficha declara de qué servicios depende.

Es **lectura pura del core**: el adaptador consulta las suscripciones, no las escribe ni
les añade campos.

> En beta **no se cobra por activar** un add-on. La suscripción que se comprueba es la
> del servicio base, no la del add-on.

## 4bis. El flujo completo, de punta a punta

1. El cliente pulsa el interruptor del catálogo → `POST /activate`. Si le falta el
   servicio base, se le dice ahí mismo y no se crea nada.
2. El documento existe en `disconnected`. El catálogo ya puede mostrar *Activado, sin
   conectar* y abrir el asistente.
3. Pega su credencial → `POST /connect`. Se prueba contra el tercero **antes** de
   guardarla; si falla, se le enseña el motivo y no se persiste nada.
4. Estado `connected` y `tokenRef` visible. A partir de ahí el add-on trabaja solo.
5. Los emparejamientos que necesite (en RentmanBiz, empleado ↔ crew member).

## 5. Dónde van los datos del add-on

Fuera del documento de activación, cada add-on guarda lo suyo **con prefijo propio**:

- **PostgreSQL**: tablas `{addonId}_*` (`rentman_employee_mapping`, `rentman_sync_log`…),
  en una migración propia numerada.
- **Firestore**: colecciones raíz `{addon}_*` (`fleetbiz_glovo_rider`, …) o subcolecciones
  del propio documento de activación.

Y la regla de oro, que aplica a todos: **el adaptador absorbe todo; checkbiz360 no se
modifica para cumplir con el sistema externo.** Del core se lee, no se le añaden campos
"porque el tercero los pide". Si mañana se retira el add-on, basta apagar su servicio y
borrar sus tablas.

## 6. Checklist para un add-on nuevo

1. Microservicio propio en `encodebiz-api/services/{addonId}` con su puerto y su ruta de
   nginx. **Nada en el SaaS.**
2. `POST /credentials`, `GET /test-connection/:entityId` y `GET /status` con Firebase auth.
3. Disparo S2S en **su propio prefijo** (`/api/v1/{addonId}/sync/…`) con `x-encodebiz-key`:
   montar el middleware sobre la raíz del servicio exigiría las dos credenciales a la vez.
4. Ficha de catálogo como dato puro + script de siembra idempotente.
5. Tablas/colecciones con prefijo y migración propia (se aplican **a mano** por SSH).
6. Sincronización por sondeo, idempotente por huella del contenido, con presupuesto de
   llamadas por pasada y distinguiendo el "no" definitivo (4xx) del fallo transitorio.
7. Documentación: ficha en `integraciones/` y capítulo de cliente en `Clients/`.
