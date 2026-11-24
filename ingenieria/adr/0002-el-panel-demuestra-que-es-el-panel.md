# ADR-0002 — El panel demuestra que es el panel; todo lo demás es la app

**Estado:** aceptada · 2026-11-11 (decidida con Jose el 2026-11-06)
**Sustituye a:** la heurística por `User-Agent` de `resolveClientChannel` (#258, #259)
**Complementa:** [ADR-004 de documental](../documental-service/adr/ADR-004-auth-solo-firebase-token.md) — la identidad sigue siendo solo el Firebase ID token
**Diseño:** [canal-app-panel/TDR-001](../canal-app-panel/TDR-001-prueba-de-panel.md) · **Roadmap:** [canal-app-panel/README](../canal-app-panel/README.md)

---

## Contexto

Una misma persona puede ser propietaria o administradora y, además, tener ficha de empleada.
En el panel es administración; en la app es una empleada más («la app es solo para
empleados»). Desde el 06-nov, `documents` —y desde el 08-nov también `tasks`— deciden qué
enseñar según **desde dónde** llega la llamada, y lo deducen del `User-Agent`:

- la app lo sustituye por la huella del dispositivo;
- el panel llega con `Mozilla/…` o, casi siempre, con `node` desde su servidor en Vercel.

El `User-Agent` lo escribe quien llama. Y una lista de cadenas se queda corta: el 06-nov el
hotfix #258 no reconocía `node` y la gestión documental del panel salió **vacía 25 minutos**
a todos los owner y admin; lo vio un cliente.

## Decisión

**El canal deja de deducirse y pasa a demostrarse.** Quien tiene que demostrar algo es el
**servidor del panel**: firma cada llamada con un código de un solo uso, estilo 2FA,
derivado de un secreto que solo conocen él y la API. Código válido → `panel`. **Cualquier
otra cosa → `app`**, que es el lado estricto.

- La identidad no cambia: la da el Firebase ID token (ADR-004). La prueba de panel no
  autentica a nadie; solo dice por qué puerta ha entrado una identidad ya autenticada.
- La app no tiene que demostrar nada.
- Las llamadas servicio a servicio y la puerta delegada del asistente siguen como están
  (deciden su canal en su propio código, no por cabecera).

## Por qué así

- **Falla hacia el lado seguro.** Sin prueba, menos acceso, nunca más. Un `curl`, una sonda o
  un `node` falsificado ven lo que vería una empleada.
- **No depende de nada que el atacante controle.** El `User-Agent` sí.
- **Barato.** Un secreto, una cabecera en el único punto de salida del panel
  (`serverBackendProxy.ts`) y una función en `shared`. Sin pantallas ni cambios en la app.
- **Rotatorio y no fijo**: si el código aparece en un log o una traza, caduca en un minuto.

## Descartado

- *Dispositivo de confianza del 2FA del empleado* como prueba de «app»: obliga a la app a
  demostrar, y una empresa sin 2FA no tiene dispositivos registrados. Con esta decisión ya
  no hace falta.
- *Custom claims de Firebase*: son por usuario, no por sesión; la misma persona usa panel y
  app con el mismo usuario.
- *Cabecera de cliente sin firmar* (`X-CheckBiz-Client: panel`): igual de falsificable que el
  `User-Agent`.
- *Secreto fijo en una cabecera*: funciona, pero una copia del valor vale para siempre.

## Consecuencias

- Toda ruta que distinga app y panel usa `resolveClientChannel` de `@encodebiz/shared`. Nadie
  vuelve a mirar el `User-Agent` para esto.
- El panel necesita la variable `PANEL_CHANNEL_SECRET` en Vercel (solo servidor, nunca
  `NEXT_PUBLIC_`). Sin ella, en modo estricto, el panel se ve como la app: **la variable va
  antes que el modo estricto**, siempre.
- Cualquier otro cliente Node que hoy llame con el token de una persona (QA, scripts,
  sondas) pasa a verse como app cuando se active el modo estricto. Es lo correcto, pero hay
  que inventariarlo antes (TDR-001, «Riesgos»).
- El secreto se rota sin cortar el panel: la API acepta el actual y el anterior.
