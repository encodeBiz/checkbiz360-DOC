# Medicion de conversiones: Google Ads, GA4 y modulo sales

Fecha: 2026-10-12. Version: v1.
Estado: diagnostico verificado + especificacion para implementar en Claude Code. No autoriza desplegar ni publicar GTM sin revision.
Cuenta: CheckBiz360 (Google Ads). Campana: `Leads-Search-CHECKBIZ`. GA4: propiedad CheckBiz360, flujo web `G-WEYR0DSWBP`. GTM: `GTM-MRQR78CK`.
Principio: **la API de sales es la fuente de verdad** de leads y contactos.

## 1. Estado verificado (2026-10-12)

### Flujo actual

1. La landing guarda en `sessionStorage` (`cb360:visit`) los parametros `gclid`, `gbraid`, `wbraid` y `utm_*` de la URL de entrada.
2. El formulario hace `POST https://api.checkbiz360.com/api/v1/sales/leads` con esos parametros. `gaClientId` (valor crudo de la cookie `_ga`) y `gaSessionId` solo se envian si hay consentimiento de marketing.
3. El clic en WhatsApp va por beacon a `POST /api/v1/sales/conversions`.
4. La API envia a GA4 por Measurement Protocol `sales_lead_accepted` y `sales_whatsapp_click`.
5. Google Ads importa ambos eventos desde GA4.

### Evidencias

| Hallazgo | Evidencia |
|---|---|
| No hay etiqueta de Google Ads en la web | GTM-MRQR78CK solo carga `G-WEYR0DSWBP`; con `?gclid=` de prueba no se crea `_gcl_aw` |
| Conversiones mejoradas sin datos | Ads > Conversiones > Diagnostico: "Urgente. No hay datos recientes". La configuracion dice "se gestiona a traves de la etiqueta de Google", que no esta |
| Habia etiqueta de Ads antes | `localStorage._gcl_ls.last_convs` conserva una conversion con label `dULrCKGtmNwcELyw6rRE` (finales de agosto). Deduccion, no confirmado |
| Fuente offline con aviso | Ads > Diagnostico > Conversion sin conexion, "Conexion directa": "Requiere atencion". Sin revisar el detalle |
| Pipeline API -> GA4 consistente | GA4, 28 dias: `landing_generate_lead_browser` 2 = `sales_lead_accepted` 2; `landing_whatsapp_click` 11 = `sales_whatsapp_click` 11 |
| Ads ve menos | Ads, 30 dias: 1 lead y 5 WhatsApp atribuidos |
| Fuga en el formulario sin explicar | GA4, 28 dias: `landing_form_submit_attempt` 18 (11 usuarios) frente a 2 leads. Los eventos `landing_form_validation_error`, `landing_form_turnstile_pending` y `landing_form_submit_failed` existen en el bundle pero no llegan a GA4 |
| Trafico de baja calidad | Ads, 7 dias: partners de busqueda 96,3 % de clics y 90,2 % del coste. Ads 30 dias: 165 clics; GA4 28 dias: 86 sesiones |
| Gasto | 30 dias (12 sept - 11 oct): 267,14 EUR, 165 clics, 1 conversion. Grupo Eventos: 104,96 EUR, 0 conversiones |

### Acciones de conversion activas

| Accion | Origen | Uso | Ventana |
|---|---|---|---|
| `checkbiz360.com (web) sales_lead_accepted` | GA4 | Principal (objetivo Envio de formularios) | 90 dias |
| `checkbiz360.com (web) sales_whatsapp_click` | GA4 | Secundaria (objetivo Contactos) | 90 dias |
| Formulario de contacto - Enviar | Formulario alojado en Google | Secundaria | 1 dia |

## 2. Cambios aplicados en Google Ads (2026-10-12, autorizados por el usuario)

- Objetivos de la campana: queda solo **Envio de formularios para clientes potenciales**. Se quito Contactos (no tenia accion principal; Ads lo marcaba "Configuracion erronea"). WhatsApp se sigue midiendo como secundaria.
- 60 palabras clave negativas a nivel de campana, concordancia de frase: busquedas de contratar eventos, software de eventos/entradas, gestores de tareas/proyectos e intencion informativa o gratuita. Reversible desde Historial de cambios.

Pendiente de decision del usuario (no aplicado): desactivar partners de busqueda; pausar la campana hasta cerrar la medicion.

## 3. Trabajo para Claude Code

Repos necesarios: backend con el servicio `sales` y la landing de checkbiz360.com. No estan en este repo de documentacion.

### 3.1 Backend sales: subir conversiones a Google Ads (prioridad 1)

> **Hecho y en produccion (2026-10-12), pero por la Data Manager API, no por `UploadClickConversions`.** Google cerro esa via a integraciones nuevas. Ver seccion 9.

Objetivo: que Google Ads reciba el lead desde la fuente de verdad, sin depender de GA4 ni de la cookie de GA.

- Google Ads API, `ConversionUploadService.UploadClickConversions`.
- Crear en Ads una accion de conversion de tipo importacion de clics, p. ej. `sales_lead_accepted (API)`. Arranca como **secundaria** en paralelo con la importacion de GA4; pasa a principal cuando cuadre 2-4 semanas con `sales_leads`.
- Por lead aceptado enviar: `gclid` o `gbraid`/`wbraid`, `conversion_date_time` con zona horaria, `order_id` = id del lead (deduplicacion), valor y moneda segun `SALES_GA4_LEAD_VALUE`/`SALES_GA4_LEAD_CURRENCY`.
- Conversiones mejoradas para leads: `user_identifiers` con email y telefono normalizados y SHA-256. Solo con consentimiento.
- Consentimiento UE: informar `consent.ad_user_data` (y `ad_personalization`) a partir de `marketingConsent` del lead. Sin consentimiento, no subir o subir marcado como denegado; decidir y documentar.
- Leads sin click id: no se suben por clic; quedan solo en sales.
- Reutilizar los controles existentes de `SALES_CONVERSION_*` (dedupe, limites) y el patron `SALES_GA4_APPLY` (solo escribe en produccion).
- Credenciales (developer token con acceso Basic, OAuth, customer id) en Secret Manager, nunca en el repo.
- Registrar resultado por lead (`uploaded`, `rejected` con motivo, `skipped_no_click_id`, `skipped_no_consent`) para poder reconciliar.
- Fase 2: acciones adicionales `lead_cualificado` y `demo_celebrada` cuando ventas registre esos estados. Secundarias hasta tener volumen.

### 3.2 Backend sales: comprobaciones del envio a GA4 (prioridad 2)

> **Comprobado (2026-10-12): ya estaba todo hecho.** Produccion registra en `G-WEYR0DSWBP`; el `client_id` se recorta de la cookie `_ga`; `session_id` se envia; el bloque `consent` va en cada evento.

- `SALES_GA4_MEASUREMENT_ID` en produccion = `G-WEYR0DSWBP` (la app SaaS usa otra propiedad, `G-1RKB5RT7NG`).
- El `client_id` de Measurement Protocol debe quitar el prefijo `GA1.1.` del valor de `_ga` que manda la landing.
- Enviar `session_id` cuando llegue `gaSessionId`.
- Confirmar que se envian los campos de consentimiento de Measurement Protocol.

### 3.3 Landing (prioridad 2)

- Persistir `gclid`/`gbraid`/`wbraid` mas alla de la pestana (almacenamiento propio con caducidad de 90 dias) **solo con consentimiento de marketing**. Hoy se pierde al cerrar la pestana.
- `vp()` toma el primer cookie que empieza por `_ga_`; si conviven varias propiedades puede leer la equivocada. Leer `_ga_WEYR0DSWBP`.

### 3.4 GTM (prioridad 2, requiere aprobacion antes de publicar)

- Reenviar a GA4 `landing_form_validation_error`, `landing_form_turnstile_pending` y `landing_form_submit_failed` para explicar la fuga 18 intentos / 2 leads.
- Etiqueta de Google Ads + vinculador de conversiones: solo si se decide medir tambien en navegador. Si la subida desde sales queda como unica fuente, ajustar en Ads la opcion de conversiones mejoradas que hoy apunta a la etiqueta de Google.

## 4. Criterios de aceptacion

1. Para un periodo dado, leads en `sales_leads` con click id = conversiones subidas aceptadas por Ads (diferencias justificadas en el registro de subida).
2. Ads > Diagnostico sin avisos urgentes de conversiones mejoradas.
3. La campana optimiza a una sola accion principal que sale de sales.
4. Cada intento de envio del formulario termina en GA4 como lead o con un motivo de fallo.

## 5. Preguntas abiertas

- Detalle del aviso de la fuente offline "Conexion directa" en Ads.
- Que hacer con los partners de busqueda y si se pausa la campana mientras se implementa.
- Si se quiere pujar por competidores de fichaje (Skello, Factorial, Sesame); hoy no estan en negativas.

## 6. Exploraciones GA4 (creadas 2026-10-12)

En GA4 > Explorar, propiedad CheckBiz360. Datos de los ultimos 28 dias en la fecha de creacion.

| Exploracion | Pregunta | Lectura inicial |
|---|---|---|
| 01 Embudo hasta lead | En que paso se pierde la gente (landing, CTA, formulario visto, empieza, intenta enviar, lead), por dispositivo | 47 usuarios ven la landing, 16 pulsan CTA, 12 ven el formulario, 5 empiezan, 2 intentan enviar, 1 lead. En movil 3 empiezan a rellenar y 0 llegan a enviar |
| 02 Que CTA funciona | Que boton o WhatsApp se pulsa, movil frente a escritorio | Los CTA del hero concentran los clics; los sticky y WhatsApp aportan pocos |
| 03 Lectura por secciones | Que secciones se ven y en cuales se detienen | En la landing de campo, analisis, precio, costes y adopcion se ven pero casi nadie se detiene (13/11/10/10 usuarios ven, 2 se detienen) |
| 04 Trafico que actua | Que fuente y campana trae gente que pulsa, abre formulario, intenta enviar o escribe | google / cpc: 22 usuarios pulsan CTA, 20 ven formulario, 9 intentan enviar, 5 WhatsApp, 1 lead |

Dimensiones nuevas registradas: Failure Reason, Error Fields, Section Name, Page Type, Close Reason, Source CTA ID. Cuentan desde el 2026-10-12. Failure Reason y Error Fields seguiran vacias hasta que GTM reenvie `landing_form_submit_failed` y `landing_form_validation_error` (seccion 3.4).

Trafico interno visible en 04 (ads.google.com y encodebiz.com como referral): conviene definir trafico interno en GA4 para excluirlo.

## 7. Auditoria del formulario de demo (2026-10-12)

### Resultado
El formulario funciona. Prueba real del usuario con cookies rechazadas y `utm_source=qa_test`: envio correcto en escritorio, Safari iOS y Chrome Android. En el navegador integrado de Claude, Cloudflare devuelve `600010` (reto fallido, deteccion de automatizacion): no es representativo de usuarios reales.

### Que explica los intentos sin lead
- `landing_form_submit_attempt` se dispara al pulsar, antes de validar (`DemoForm.tsx:263`). No equivale a un envio al servidor.
- En GA4 (1 sep - 12 oct): 20 intentos, 3 `landing_generate_lead_browser`, 0 eventos de fallo. GTM no reenvia `landing_form_validation_error`, `landing_form_turnstile_pending` ni `landing_form_submit_failed`.
- Intentos separados 1-3 s (Valdemoro 113,5/116,6/117,9 s; Alicante 36,3/38,8 y 104,1/106,4/107,4 s). La espera de Turnstile (10 s, `useTurnstile.ts:22`) y el timeout de red (20 s) quedan descartados: son fallos inmediatos, casi seguro errores de validacion.
- Sin filas en `sales_leads` esos dias: el envio no llego al servidor.
- Conclusion: problema de conversion (gente que recibe un error de campo y abandona), no fallo tecnico. El campo exacto no es recuperable para fechas pasadas.

### Cambios propuestos para Claude Code (por prioridad)
1. GTM: reenviar a GA4 `landing_form_validation_error` (`error_fields`), `landing_form_turnstile_pending` y `landing_form_submit_failed` (`reason`), y `required_fields_completed` en el intento. Sin esto no se sabe que campo frena.
2. `DemoForm.tsx:297-306` + `content.*.ts` (`errors.verification`): cuando el reto espera un clic, el mensaje debe pedir marcar la casilla de Cloudflare. Hoy dice "Vuelve a intentarlo" y el boton muestra "Enviando..." durante 10 s sin explicar nada.
3. `useTurnstile.ts:92-103`: tras `error-callback` el envio sale sin token. Si `TURNSTILE_ENFORCE` no es `0` en produccion, el servidor lo guarda como `bot`, no avisa a ventas y responde `ok`: el visitante ve "enviado" y el lead se pierde. Decidir: o el servidor acepta sin token y marca para revision, o el cliente muestra error con salida por correo/WhatsApp. Verificar el valor en produccion.
4. Layout shift: el widget de Turnstile aparece al abrir el modal y desplaza el boton unos 44 px. Reservar altura al contenedor (`DemoForm.module.css`, `.turnstile`).
5. `leads.ts:359`: sustituir `AbortSignal.timeout` (Safari 16+) por `AbortController` + `setTimeout`.
6. Backend `PostgresLeadRepository.hasRecentDuplicate`: misma IP + `message` nulo en 10 min cuenta como duplicado. En la portada no hay campo mensaje, asi que dos personas tras la misma IP (oficina, CGNAT movil) se descartan en silencio. Ajustar a email o a IP + email.

### Datos de prueba creados
Leads con nombre `TEST AUDITORIA no contactar`, emails `qa-test-*@encodebiz.com`, `utm_source=qa_test`. Sin consentimiento de marketing: no se envian a GA4/Ads. Borrar o marcar en `sales_leads` cuando se revisen.

## 8. Ajuste a la subida por API tras el despliegue (2026-10-12)

> **Aplicado y despues superado.** El developer token se quito (PR #145), pero la primera validacion real mostro que `UploadClickConversions` no se abre a integraciones nuevas. Ver seccion 9.

Google retiro los developer tokens el 2026-09-09: el nivel de acceso ahora pertenece al proyecto de Google Cloud dueno del cliente OAuth y el token es opcional e ignorado. Fuente: developers.google.com/google-ads/api/docs/first-call/dev-token (actualizada 2026-10-07).

Cambio para Claude Code en `services/sales/src/application/ads/`:
- `config.ts` `missingSettings()`: quitar `SALES_ADS_API_DEVELOPER_TOKEN` de los obligatorios. Hoy sin token la integracion queda desactivada y ya no se puede obtener uno.
- `googleAdsApi.ts:132`: enviar la cabecera `developer-token` solo si la variable existe.
- README §Puesta en marcha paso 2: sustituir "developer token Basic" por "proyecto de Cloud con Google Ads API habilitada y acceso Explorer" (automatico, 2.880 operaciones/dia en cuentas reales, suficiente para estos volumenes). Sin MCC.

## 9. Estado de la implementacion (2026-10-12)

### Subida de leads a Google Ads: en produccion, subiendo de verdad

- **Via: Data Manager API** (`POST datamanager.googleapis.com/v1/events:ingest`). La primera validacion contra `UploadClickConversions` devolvio `CUSTOMER_NOT_ALLOWLISTED_FOR_THIS_FEATURE`: Google la reserva a quien ya la usaba y manda las integraciones nuevas a Data Manager. OAuth, proyecto, cuenta y accion si respondieron bien.
- **Destino:** accion `sales_lead_accepted (API)`, id `7840297411`, cuenta `161-619-3145`, **secundaria**. Sin MCC y sin developer token.
- **Credenciales:** cliente OAuth y refresh token con scope `https://www.googleapis.com/auth/datamanager` en el `.env.production` del servidor (no en Secret Manager: aqui los secretos van en ese fichero). Un token de scope `adwords` no sirve.
- **Activado** con `SALES_ADS_API_APPLY=1` el 2026-10-12. Primer envio real: lead 30 (24-sep), requestId `cf50b905-5e7c-4d41-9376-b3190a85a352`.
- **Como funciona:** un barrido en el contenedor sube cada 15 min los leads aceptados de mas de 30 min y de los ultimos 7 dias, **uno por peticion** (Data Manager rechaza la peticion entera si un evento esta mal). Google contesta en dos tiempos: `uploaded` con un requestId al recibirlo, y `confirmed` o `rejected` cuando el barrido pregunta por ese id, a partir de los 30 min.
- **Por lead se envia:** `transactionId` = id del lead (repetirlo actualiza, no suma), fecha del lead, `gclid`/`gbraid`/`wbraid`, consentimiento y, con consentimiento, email y telefono en SHA-256 (Gmail sin puntos).
- **Consentimiento, decidido:** sin senal explicita de marketing el lead **no se sube** (`skipped_no_consent`). Es el mismo criterio que GA4 y se cambia con `SALES_ADS_API_CONSENT_MODE`. Los datos cifrados nunca salen sin consentimiento.
- **Leads sin click id:** `skipped_no_click_id`, se quedan en sales.
- **Historico:** el barrido no lo sube solo. Script `subir-conversiones-ads` con `--days N` (simula sin `--apply`).

### Como cuadrarlo (criterio de aceptacion 1)

```sql
SELECT ads_status, count(*) FROM sales_leads
 WHERE status = 'accepted' AND created_at > NOW() - interval '30 days' GROUP BY 1;
```

o `GET /api/v1/sales/ads/status?days=30` (S2S). Estados: `pending`, `validated`, `uploaded`, `confirmed`, `rejected` (motivo en `ads_error`), `failed`, `skipped_no_click_id`, `skipped_no_consent`.

### Tres canales hacia Ads, y no hay que confundirlos

| Canal | En Ads aparece como |
|---|---|
| CSV `/exports/google-ads-leads.csv` (ya existia, agosto) | fuente offline "Conexion directa" de Data Manager. Es casi seguro la fuente con aviso "Requiere atencion" de la seccion 1 |
| GA4 `sales_lead_accepted` | accion importada de GA4 (la principal hoy) |
| Data Manager API (nuevo) | `sales_lead_accepted (API)`, secundaria |

### Pendiente

1. Lead 30: Google lo recibio y a la hora lo rechazo con `DESTINATION_TOO_RECENTLY_CREATED` (la accion se creo ese mismo dia y Google no acepta nada en ella durante unas horas). No es culpa del lead. Arreglo en develop (`e078f3b`): ese motivo devuelve el lead a la cola en vez de rechazarlo. Reenviar el lead 30 cuando la accion tenga unas horas.
2. Pasar `sales_lead_accepted (API)` a principal tras 2-4 semanas cuadrando con `sales_leads`. Decision del usuario.
3. Dar valor al lead: `SALES_GA4_LEAD_VALUE` esta vacio y Ads usa 1 EUR.
4. Activar en Ads las conversiones mejoradas para leads por API (hoy dicen "se gestiona a traves de la etiqueta de Google").
5. Seccion 7, punto 1 (GTM): instrucciones dadas al usuario; se hace en la interfaz de GTM. Ojo: `error_fields` llega como array y el parametro es `failure_reason`, no `reason`.
6. El primer despliegue del PR #146 fallo por timeout SSH del runner de GitHub contra produccion; al relanzarlo paso. Posible ban de fail2ban a IPs de Azure.

Codigo: `encodebiz-api`, `services/sales/src/application/ads/`, migraciones `029` y `030`, PRs #144, #145 y #146. Detalle tecnico en `services/sales/README.md`.

## 9. Cambios en la campana (2026-10-12, tarde, autorizados por el usuario)

- Motivo: 29 clics hoy, 100 % partners de busqueda, CTR 21,3 %, 29,90 € gastados, 0 conversiones; en GA4 las sesiones google/cpc con 0 % de interaccion. La estrategia estaba en aprendizaje tras quitar el objetivo Contactos.
- Partners de busqueda desactivados: la campana sale solo en la Red de Busqueda de Google.
- Puja: de Maximizar conversiones a Maximizar clics con limite de CPC de 3,00 €. Volver a Maximizar conversiones cuando haya conversiones suficientes (orientativo: 15-30 en 30 dias).
- Accion `sales_lead_accepted (API)` creada: id 7840297411, cuenta 161-619-3145, importacion de clics, secundaria, una conversion, 90 dias, valor por defecto 1 €. Alimentada por la Data Manager API desde sales (`SALES_ADS_API_APPLY=1` en produccion).

## 10. Revision y cambios (2026-10-13, autorizados por el usuario)

- 12 oct: 29 clics, 100 % partners, 0 conversiones. 13 oct (a media jornada): 18 clics, 100 % Busqueda de Google, CTR 14,4 %, CPC medio 1,40 €, 25,27 €, 0 conversiones; 1 `sales_whatsapp_click` en GA4.
- 14 de 18 clics del 13 oct venian de 4 palabras clave amplias con busquedas de RRHH/informativas y marcas de competencia.
- Pausadas (amplia): control de fichajes, gestion de personal, sistema de fichaje (Construccion); registro de horas (General).
- Anadidas (frase): "control de fichajes", "gestion de personal", "sistema de fichaje" (Construccion); "registro de horas" (General).
- 10 negativas de campana (frase): evaluar, evaluacion, evaluación, desempeño, rendimiento, relaciones, plantilla, contador, cómo, como. Total negativas: 196.
- Aplicacion automatica de recomendaciones: desactivadas "Quita las palabras clave redundantes" (aplico 1 cambio el 12 oct) y "Quita las palabras clave negativas en conflicto" (quito 1 negativa de frase el 13 oct a las 3:59). Siguen activas: rotacion optimizada, atribucion basada en datos, Maximizar clics.
