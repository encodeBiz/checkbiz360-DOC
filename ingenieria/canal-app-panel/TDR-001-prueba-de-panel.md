# TDR-001 — Prueba de panel: código rotatorio en `X-CheckBiz-Panel`

**Fecha:** 2026-11-11
**Estado:** Diseño aprobado (ADR-0002) · implementación en `feat/canal-panel-firmado` (API y panel)
**Componentes:** `packages/shared` (`checkbiz/auth/clientChannel.ts`), `services/documents`,
`services/tasks`, panel `src/lib/http/serverBackendProxy.ts`

---

## 1. El secreto

- `PANEL_CHANNEL_SECRET`: 32 bytes aleatorios en **base64** (`openssl rand -base64 32`).
- Dónde: Vercel (solo servidor; **nunca** `NEXT_PUBLIC_`) y el `.env` del stack de la API
  (`.env.staging` / `.env.production`, que leen todos los servicios). Un valor por entorno;
  staging y producción **no** comparten secreto.
- Nunca en un repositorio, ni en un log, ni en un mensaje de error.
- `PANEL_CHANNEL_SECRET_PREVIOUS` (opcional, solo API): el secreto anterior durante una
  rotación. Ver §6.

Un secreto que no decodifica a ≥32 bytes se trata como **ausente** y se avisa una vez en el
log al arrancar (`[clientChannel] PANEL_CHANNEL_SECRET inválido: se ignora`).

## 2. El código

```
ventana = floor(unix_segundos / 30)
código  = hex( HMAC-SHA256( secreto_en_bytes, "checkbiz-panel:v1:" + ventana ) )
cabecera: X-CheckBiz-Panel: v1.<ventana>.<código>
```

- La ventana va **en claro** en la cabecera: así el servidor sabe qué ventana comprobar y,
  al depurar, se ve de un vistazo si el problema es de reloj.
- `v1` permite cambiar el formato sin ambigüedad.
- *Precisión sobre lo apuntado el 06-nov* (TDR-002 de documental, «Fase 2»): allí la cabecera
  llevaba solo el código. Llevar versión y ventana no cambia la seguridad (la ventana no es
  secreta) y quita adivinanzas al verificar.

**Vector de prueba** (el mismo en los tests de la API y del panel, para que los dos lados
calculen igual):

| Secreto (base64) | `unix` | Ventana | Cabecera |
|---|---|---|---|
| `BwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwcHBwc=` (32 bytes `0x07`) | `1770000000` | `59000000` | `v1.59000000.c40e2e35acec8903167d367f3c21a3d8203f7c2359c4fa587d737204f49249af` |
| ídem | `1770000030` | `59000001` | `v1.59000001.f81d23cc2498d0a123d3054e5dab95cc136bc960a756d3401644569e890baa2a` |

## 3. La verificación (API, `@encodebiz/shared`)

`resolveClientChannel(headers, ahora?)` sustituye a `resolveClientChannel(userAgent)`:

1. Si la API **no tiene secreto** → heurística del `User-Agent` de hoy (`PANEL_USER_AGENT`).
   Es el comportamiento actual, sin cambios.
2. Si llega `X-CheckBiz-Panel`:
   - formato `v1.<entero>.<64 hex>`, ventana a **±1** de la actual (tolera 30 s de
     desfase en cualquier sentido), y HMAC igual al calculado con el secreto actual **o** el
     anterior, comparado con `crypto.timingSafeEqual` → **`panel`**;
   - cualquier otra cosa (mal formada, caducada, firmada con otro secreto) → **`app`**.
     **Nunca** se cae al `User-Agent` cuando la cabecera está y no vale: si no, bastaría con
     mandar basura y un `User-Agent: node`.
3. Si **no** llega la cabecera:
   - `PANEL_CHANNEL_STRICT` distinto de `true` → heurística del `User-Agent` (transición);
   - `PANEL_CHANNEL_STRICT=true` → **`app`**.

Cuando el resultado sale de la heurística del `User-Agent` con secreto configurado, se
escribe como mucho **una línea por minuto** y servicio:
`[clientChannel] panel sin prueba por User-Agent "<ua recortado a 40>"`. Es la señal para
saber si alguien —el panel u otro cliente— sigue entrando sin firmar antes de pasar a
estricto. Nunca se escribe la cabecera ni el secreto.

*Precisión sobre lo apuntado el 06-nov:* allí el paso C era «quitar el `User-Agent` del
código». Aquí es una **variable** (`PANEL_CHANNEL_STRICT`), por dos razones: se vuelve atrás
sin desplegar si algo sale mal (lección de #258 → #259), y se prueba en staging el mismo día.
El código de la heurística se borra en una limpieza posterior, cuando producción lleve una
semana en estricto sin líneas de aviso.

`resolveClientChannelFromUserAgent(ua)` queda exportada solo para esa transición y para los
tests; ningún servicio la llama directamente.

**Consumidores que cambian** (los únicos hoy, 11-nov; buscar de nuevo antes de fusionar):

- `services/documents/src/interfaces/http/document/document.helpers.ts`
- `services/tasks/src/interfaces/http/task/task.helpers.ts`

Las llamadas servicio a servicio (`sendNoticeInternal…`, `channel: "panel"` fijo) y la puerta
delegada del asistente (`delegatedUid`, cuenta como panel) **no** pasan por aquí y no cambian.

### 3.1 Precisiones de la implementación (11-nov)

Donde el texto de arriba dejaba margen, la implementación decidió así (revisado contra el TDR):

- El aviso «panel sin prueba» sale **solo cuando la heurística concede `panel`**. La app nunca
  firma: si también avisara cuando da `app`, llenaría el cupo de una línea por minuto y taparía
  la señal útil. Los caracteres no imprimibles del `User-Agent` se cambian por `?`.
- Con `PANEL_CHANNEL_SECRET_PREVIOUS` configurado pero **sin** `PANEL_CHANNEL_SECRET`, se trata
  como «sin secreto» (heurística). Es un estado de configuración a medias, no de rotación.
- Una cabecera **repetida** (llega como lista) o **vacía** cuenta como presente e inválida:
  `app`.
- Formato aceptado: `^v1\.(\d{1,15})\.([0-9a-f]{64})$`, sin distinguir mayúsculas.
- Las variables se leen en cada llamada (y una vez al cargar el módulo, para que el aviso de
  secreto inválido salga al arrancar). `PANEL_CHANNEL_STRICT` solo vale con el texto `true`.

**Verificado de punta a punta**: la cabecera que genera el helper del panel la acepta la
verificación de `shared` con el reloj real; firmada hace 30 s o con el reloj del panel 25 s
adelantado → panel; hace 70 s, otro secreto o basura (con `User-Agent: node`) → app; estricto
sin cabecera → app; rotación con el secreto anterior → panel.

## 4. La firma (panel)

En `src/lib/http/serverBackendProxy.ts`, en el `fetch` hacia la API, se añade la cabecera si
y solo si existe `process.env.PANEL_CHANNEL_SECRET`. Se calcula **en cada llamada** (no se
cachea entre peticiones) con `node:crypto`. Un helper puro y probado con el vector de §2
(`src/lib/http/panelChannelProof.ts` o donde encaje con el estilo del repo). Antes de tocar el
proxy, buscar cualquier otro `fetch` de servidor que llame a la API sin pasar por él y
firmarlo también, o anotarlo.

La cabecera **no** se reenvía desde el navegador: el proxy la escribe; si el navegador manda
una `X-CheckBiz-Panel`, se descarta.

## 5. Despliegue (sin ventana de panel vacío)

| Paso | Qué | Cómo se sabe que está bien |
|---|---|---|
| A | API con el código nuevo y el secreto en el `.env`; `PANEL_CHANNEL_STRICT` sin poner | Todo igual que antes; aparecen líneas `[clientChannel] panel sin prueba` por las llamadas `node` del panel |
| B | Panel con la variable y la cabecera | Las líneas de aviso dejan de salir para el panel; sonda: con cabecera → panel |
| C | `PANEL_CHANNEL_STRICT=true` + reiniciar `documents` y `tasks` | Sonda: `User-Agent: node` sin cabecera → app; el panel sigue viendo todo |
| Vuelta atrás | Quitar `PANEL_CHANNEL_STRICT` (o el secreto) y reiniciar | Comportamiento del 06-nov |

**Orden obligatorio:** A antes que B (una cabecera que nadie verifica es inocua); B antes que
C (estricto sin panel firmando = panel vacío). Nunca C en el mismo despliegue que A.

## 6. Rotación del secreto

1. API: `PANEL_CHANNEL_SECRET_PREVIOUS=<actual>` y `PANEL_CHANNEL_SECRET=<nuevo>`; reiniciar.
2. Vercel: `PANEL_CHANNEL_SECRET=<nuevo>`; redesplegar.
3. Al día siguiente, quitar `PANEL_CHANNEL_SECRET_PREVIOUS` de la API.

## 7. Pruebas de aceptación

**Unitarias (`shared`)**: vector de §2; ventanas −1, 0 y +1 aceptadas, ±2 rechazadas;
secreto anterior aceptado; cabecera mal formada, de 63 hex, con ventana no numérica o firmada
con otro secreto → `app` aunque el `User-Agent` sea `node`; sin cabecera → heurística o `app`
según `PANEL_CHANNEL_STRICT`; sin secreto → heurística siempre; secreto de menos de 32 bytes →
ausente. Las pruebas de `documents` y `tasks` siguen pasando.

**Unitarias (panel)**: el helper produce exactamente la cabecera del vector con el reloj fijado.

**En staging** (sonda del contenedor `tasks`, como en §38 del pase; owner de una empresa de
staging con documentos personales de otra persona):

| Llamada | Esperado tras A | Tras B | Tras C |
|---|---|---|---|
| Panel real (Vercel local) | ve todo | ve todo | ve todo |
| `User-Agent: node`, sin cabecera | ve todo | ve todo | **como app** |
| Cabecera válida | ve todo | ve todo | ve todo |
| Cabecera de hace 2 min / basura | **como app** | como app | como app |
| Huella de dispositivo (app) | como app | como app | como app |
| Worker, cualquier canal | lo suyo | lo suyo | lo suyo |

## 8. Riesgos y qué se mira antes de C

- **Otros clientes Node con token de persona**: la suite QA (`qa/`), scripts y sondas. En
  estricto se ven como app. Antes de C: revisar las líneas de aviso de una semana y la suite
  QA; si la QA necesita ver como panel, se le da el secreto **de staging** por su `.env`.
- **`services/events/scripts/probe-events.js`** llama a `tasks` con el token del owner desde Node
  sin `User-Agent` propio: hoy cuenta como panel y **en estricto será app**. Es una sonda de
  pruebas; antes de C, o se le da el secreto de su entorno o se acepta que vea como app.
- **La suite QA ya es app hoy** (`User-Agent: encodebiz-qa/1.0 (playwright)`, `qa/src/entorno.ts`):
  el modo estricto no le cambia nada.
- **El navegador llama directo a `assistant`** (`assistantConnections.service.ts`, conexiones
  del conector) sin pasar por el proxy. Hoy `assistant` no distingue canal; si algún día lo
  hace, esas llamadas tienen que ir por el proxy para poder firmarse.
- **Reloj del servidor**: ±30 s. Los dos lados usan NTP; si alguna vez falla, la ventana en
  claro de la cabecera lo enseña en el acto.
- **Repetición dentro de la ventana**: quien copie una cabecera válida puede reutilizarla
  hasta un minuto, y además necesitaría un ID token válido. Aceptado.
- **El staging del panel es el portátil** (no Vercel): el secreto de staging va en su
  `.env.local`, no en Vercel.
