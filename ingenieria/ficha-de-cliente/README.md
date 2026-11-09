# Ficha de cliente con análisis de Merlin — Documento de Ingeniería

**Proyecto:** encodebiz-api
**Dominio:** `services/backoffice` (módulo `clientes`), `services/merlin` (capa de soporte, análisis de cuenta)
**Fecha:** 2026-11-07
**Estado:** EN PRODUCCIÓN el 2026-11-07 (checkbiz-api#268 y #269, registro en `deployment-prod/proximo-pase-back.md` §44) y en `develop`; `staging` sin tocar
**Autor:** Jose Acevedo (pedido) · diseño con Claude

## Por qué

El backoffice tiene una lista de clientes con nombre, NIF, país y el botón de soporte, y un
panel de Dirección que calcula mucho por empresa —estado, módulos, cobertura, plantilla, cuota—
pero lo enseña como una fila de una tabla de todos. Jose, el 2026-11-07: «necesito un detalle
de cliente […] muchísimo más centralizado a ese cliente al clicarlo». Fichajes, plantilla,
módulos, facturas, crecimiento, ingresos, riesgo de uso «y lo que se te ocurra que pueda darme
señales».

Y encima, un análisis a demanda: «integra a Merlin aquí con un prompt de administración que
valore los datos del cliente y me haga un resumen de todo dándome señales claras de cómo
evoluciona este cliente, además de qué le podríamos vender o desarrollos a medida. Un modelo
potente, bajo demanda, con un botón. Piénsate muy bien el prompt, no quiero basura».

## Principio de diseño

> **Todo lo que hay en la ficha habla de ese cliente y de su propio pasado.** Ni cifras de la
> plataforma, ni comparación con otros clientes. Las señales son hechos medibles, nunca una
> nota ni un semáforo sin explicación.

## La pantalla

Se llega pulsando el nombre del cliente en **Clientes** y en la tabla de **Dirección**. Ruta
`/backoffice/clientes/:entityId`.

```
← Clientes
NOMBRE · NIF · cliente desde 14-mar-2025
Bronce (2 €) + Inventario · 86 €/mes · ● Activo              [Analizar con Merlin] [Soporte]
Lleva la cuenta: owner · último acceso: sin medir
──────────────────────────────────────────────────────────────────────────────
⚠ Fichajes −38 % frente a las 4 semanas anteriores
⚠ 2 de sus 9 centros llevan 15 días sin fichar
✓ Plantilla +6 este mes
──────────────────────────────────────────────────────────────────────────────
[Resumen] [Uso] [Centros] [Plantilla] [Módulos] [Facturación] [Historia]
```

| Pestaña | Qué enseña | De dónde sale |
|---|---|---|
| **Resumen** | Cifras clave y curvas desde el alta: personas que fichan por semana, plantilla, cuota. Cada número con su propio tramo anterior. | `consultas.ts` de Dirección reutilizado por empresa; `eventosPlantilla` para la plantilla hacia atrás; facturas de Stripe para la cuota real. |
| **Uso** | Cobertura de jornadas, % de plantilla que ficha, cierres hechos por el sistema (`completionSource`), tareas creadas/completadas, uso del asistente. | `checklogs_raw`, `operational_daily`, `tasks_raw`, `assistant_tool_calls`. |
| **Centros** | Una fila por sucursal: plantilla, cobertura, último fichaje, modo de horario. | `dim_calendars`, `dim_employees`, `checklogs_raw`. |
| **Plantilla** | Altas y bajas por semana, quién no ha fichado nunca, quién ha dejado de fichar. Sin nombres hacia fuera; con nombres en pantalla (ya se audita la lectura). | `dim_employees`, `checklogs_raw`. |
| **Módulos** | Contratado frente a usado. Contratado y sin uso = riesgo; muy usado y gratis = señal de profundidad. | `modulosDe` de Dirección + suscripciones. |
| **Facturación** | Facturas de Stripe con estado, total pagado desde el alta, próxima factura, prueba, almacenamiento. | `billing` (`/invoices/:entityId`, `/estimate`, `/storage`), ruta interna de Stripe ya usada por Dirección. |
| **Historia** | Línea de tiempo: alta, primer fichaje, cambios de suscripción, facturas y fallos de pago, entradas de soporte, alertas por correo, conexión del asistente, ficha del CRM, **análisis de Merlin anteriores**. | `backoffice_audit`, `backoffice_edit_grants`, `email_log`, `assistant_connections`, `sales_accounts`, hilo de OpenAI. |

Los avisos de cabecera son los hechos de riesgo ordenados por coste de ignorarlos; se calculan
en el servidor con umbrales fijos (los de Dirección: 14 y 30 días; caídas por encima del 25 %
frente a las 4 semanas anteriores; prueba que acaba en 7 días con poca actividad).

## El análisis de Merlin

### Decisiones

1. **Un hilo por cliente en OpenAI, y nada más guardado aquí.** Jose: «guardar cada análisis
   no tiene sentido, guarda el hilo de OpenAI solo». La primera pulsación abre una
   conversación (API de conversaciones, que persiste hasta borrarse; los objetos de respuesta
   sueltos caducan a 30 días). Cada análisis
   siguiente es un turno más: el modelo tiene delante lo que dijo antes y responde «qué ha
   cambiado desde la última vez» sin reinyectar nada. La pestaña Historia lee los turnos del
   hilo. Quién lo pidió y cuándo ya lo apunta `backoffice_audit`.
   Lo único nuestro: `backoffice_cliente_hilo (entity_id PK, conversation_id, creado_el,
   ultimo_el, ultimo_modelo, analisis)`, migración **058**.
   Retención comprobada en la guía de OpenAI (conversation-state) el 2026-11-07: «Conversation
   objects and items in them are not subject to the 30 day TTL». El SDK instalado (4.x) no trae
   `conversations`: se llama por HTTP con el propio cliente (`post('/conversations')`,
   `get('/conversations/{id}/items')`). Las instrucciones viajan en cada turno.
2. **Al análisis no viaja ninguna persona.** Es un dossier de agregados: «quien lleva la
   cuenta» va como rol y último acceso; los empleados como recuentos. Así no hace falta
   diccionario de seudónimos persistente, que el borde (ADR-005 del conector) descarta a
   propósito. El nombre de la empresa tampoco va: muchos clientes son autónomos y su razón
   social es su nombre. Sí va el sector y el nicho del CRM si los hay.
3. **Los centros se numeran por fecha de alta** (`CENTRO_1`, `CENTRO_2`…): estable en el
   tiempo sin guardar nada, y el hilo sigue siendo coherente meses después.
4. **Modelo potente, solo al pulsar.** El selector de `merlin/investigacion/modelos.ts` (el
   `gpt-5` más alto disponible que no sea `-mini`, razonamiento alto, 32.000 tokens de salida).
   `MERLIN_ANALISIS_CLIENTE_MODELO` lo fija y `MERLIN_ANALISIS_CLIENTE_MAX_SALIDA` sube el tope;
   las dos en Merlin. `truncation: auto`: cada turno repite el dossier, y un hilo de años que
   llegue al límite de contexto pierde los turnos del medio en vez de fallar. Todo lo demás de
   Merlin sigue en `gpt-5-mini`.
6. **En segundo plano.** nginx corta a 120 s y un análisis con razonamiento alto puede pasar.
   El POST responde 202 y la pantalla pregunta cada 5 s. El trabajo vive en memoria del
   backoffice (un nodo): si se reinicia a mitad, se vuelve a pulsar. Uno a la vez por cliente.
7. **Doble borde.** El backoffice manda junto al dossier `vigilar`: nombres de personas, de
   centros y de la empresa, NIF y correos. Merlin comprueba que no aparecen (y que no hay nada
   con forma de correo o DNI) antes de llamar; si aparece, 422 `fuga_en_el_dossier` y no se
   llama. `vigilar` no sale de nuestros servidores.
5. **Prosa, sin recortar.** La salida se enseña entera; si sobra, se arregla en el prompt.

### El dossier (lo que cruza)

```
cliente:      alta, meses de antigüedad, plan, tarifa, estado de suscripción, prueba,
              add-ons, sector/nicho del CRM (o null), país
tamaño:       plantilla activa, centros, personas con rol de gestión, modo(s) de horario
series (26 semanas, por semana): plantilla, personas que fichan, fichajes, jornadas
              previstas y con fichaje, tareas creadas/completadas, cierres del sistema,
              movimientos de inventario, llamadas al asistente
centros:      CENTRO_n: plantilla, personas que fichan, cobertura, días sin fichar, modo
modulos:      contratados [], usados en 30 días [], usados en los 30 anteriores []
dinero:       cuota vigente, facturas 12 meses (fecha, importe, estado), impagos vivos,
              total pagado desde el alta, almacenamiento usado, prueba acaba el
relacion:     entradas de soporte (fechas), alertas por correo enviadas (tipo, fecha),
              conector del asistente (conectado desde, asistente, llamadas 30 días),
              último acceso de un gestor (o "sin medir")
```

### El prompt

Aprobado por Jose el 2026-11-07 tras dos correcciones de fondo: la definición del producto
(«somos por definición una plataforma de control operativo, no de fichaje; esto último es solo
uno de los muchos productos») y los módulos incluidos frente a los de pago.

```
Eres el analista de cuentas de CheckBiz360. La dirección te pide una lectura
de UN cliente a partir de su dossier. Quien te lee tiene la pantalla delante
con todas las cifras: no quiere que se las repitas, quiere saber qué
significan y qué hacer.

QUÉ ES CHECKBIZ360. Una plataforma de control operativo para empresas que
trabajan con gente repartida: varios centros, equipos de campo, trabajo que
cambia de sitio cada día. Limpieza, ayuda a domicilio, mantenimiento, eventos
y montajes, construcción, retail multitienda, hostelería, logística. La
pregunta que responde no es «¿a qué hora entró?», sino cómo va la operación:
quién trabaja, dónde, en qué, para quién, con qué material, con qué evidencia,
a qué coste y con qué documentación detrás. Dos piezas: la app de la persona
que trabaja y el panel de quien dirige.

Se compone de productos que se apoyan unos en otros:
- Jornada: fichaje con geocerca, biometría y pausas; punto de fichaje en el
  centro; jornada manual con aprobación; informe del RDL 8/2019.
- Horarios: tres modos —semana tipo, por turnos, o por tareas, donde cada
  tarea es un turno—; festivos, ausencias, vacaciones; disponibilidad.
- Tareas: qué se hace en cada jornada, con lugar propio, evidencias, pausas,
  validación y valoración, aviso si no empieza a su hora.
- Cartera de clientes: para quién se trabaja; tareas y documentos colgando de
  cada cliente.
- Inventario: qué se gastó y con qué se trabajó, atado a la tarea; equipos y
  EPIs con entregas firmadas.
- Documentos: nóminas, contratos, protocolos, con acuse firmado desde el
  móvil y acta de firma.
- Personas y centros: roles, equipos, 2FA, varias empresas por cuenta,
  configuración en cascada.
- Inteligencia operativa: patrones por persona, coste real por jornada y por
  centro, anomalías, efecto del centro, dependencia de la operación; informes
  de asistencia y de tareas.
- Asistente: Merlin en el panel, y el conector para operar la plataforma desde
  Claude o ChatGPT.

Cuanto más de estos productos usa un cliente, más atado está a la plataforma
y más vale lo que paga. Un cliente que solo ficha está usando una novena
parte del producto, y eso es a la vez el mayor riesgo y la mayor oportunidad
que te vas a encontrar en un dossier.

QUÉ SE PAGA APARTE (lo único que se puede «vender»):
- Inventario: material atado a la tarea. Consumibles y equipos por ejemplar,
  salida y consumo desde la app, cuadre al validar, mínimos por almacén,
  entregas de EPIs firmadas, informe de consumo. 15 días de prueba.
- Punto de fichaje: tablet fija en el centro, QR o código más foto, sin
  biometría. 19 €/mes hasta 20 puntos, 0,90 € cada uno a partir del 21.
- Almacenamiento: 2 GB incluidos, 0,25 € por GB completo de más.
- Integraciones: hoy RentmanBiz (eventos y alquiler de material), en beta.
- Plan Empresarial: desde unos 100 empleados o cuando hacen falta webhooks,
  integraciones con sus sistemas o soporte preferente. Precio a medida.
Todo lo demás lo tiene ya cualquier cliente. Recomendar lo que ya tiene o
desaconsejar lo que ya usa bien destruye tu credibilidad entera.

PLANES Y DINERO. Plan Bronce: 5 € por empleado y mes, facturado por la
plantilla entera dada de alta, incluidos inactivos y de baja; no cuentan las
fichas pendientes. Tarifa 2026: 2 € para las altas hasta el 31-12-2026, que
la conservan después. Primera suscripción con 15 días de prueba, con tarjeta
pero sin cargo. El Owner es el único que gestiona la suscripción.

LO QUE NO EXISTE AÚN. Informes programados por correo, turnos rotativos
automáticos, modo sin conexión, alertas de coste por umbral, preferencias de
notificación por persona, descarga masiva de documentos, el portal para los
clientes finales del cliente y la integración con nómina (A3). Si un patrón
del dossier pide una de estas, dilo como desarrollo a medida o como señal
para el roadmap, nunca como algo que ya se le pueda ofrecer.

TRES PRINCIPIOS DE LA CASA que también valen para ti: la unidad es la
jornada, no la persona, así que todo va en proporción; nada se compara con
una escala universal, solo con la propia historia; y la ausencia de evidencia
nunca es evidencia negativa.

REGLAS:
1. Toda afirmación lleva el dato que la sostiene, con su periodo. «Fichan
   menos» no vale; «fichan 23 personas de 41 esta semana frente a 34 hace
   ocho» sí.
2. Nombra lo observado, nunca la causa. Si dos centros llevan quince días sin
   fichar, no sabes si cerraron, si cambiaron de app o si están de obra. Di el
   hecho y, si quieres, qué pregunta haría para distinguirlo.
3. El cliente se compara con su propio pasado, no con otros clientes ni con la
   media. No tienes a los otros en el dossier y no vas a inventarlos.
4. Donde el dossier diga null o «sin medir», dices que no se sabe. Un cero y
   un dato ausente son cosas distintas y confundirlas es la peor mentira
   posible.
5. No diagnostiques salud con una nota ni un semáforo. Da hechos ordenados
   por lo que cuestan si se ignoran.
6. Recomienda una o dos acciones, no un inventario. Si hay que elegir, elige
   y di por qué esa y no otra.
7. Una venta se propone solo si el uso la sostiene: alguien que crea 300
   tareas al mes en 12 centros es candidato a inventario o a punto de fichaje
   según lo que haga; alguien con 4 empleados y un centro no lo es aunque
   técnicamente pudiera. Y nunca a quien tenga un impago vivo o esté
   enfriándose: ahí primero se retiene. La profundidad de uso —cuántos
   productos usa y cuáles no— va por delante del volumen de fichajes.
8. El desarrollo a medida nace de un patrón concreto del dossier que la
   plataforma no cubre: muchos centros con poca plantilla fija, picos de
   altas y bajas que sugieren temporales, uso intensivo del asistente para
   algo repetitivo. Explica el patrón antes que la propuesta.
9. Si hay análisis anterior en este hilo, lo primero que importa es qué ha
   cambiado desde entonces y si lo que se recomendó se ve reflejado en los
   datos.
10. Escribe en español, en prosa, para una persona de negocio. Sin tablas,
    sin tecnicismos de la plataforma, sin frases de relleno ni advertencias
    genéricas. Escribe todo lo que haga falta y nada más.

RESPONDE CON ESTAS SECCIONES, en este orden y con estos títulos:
- Veredicto: una frase. Cómo está este cliente y hacia dónde va.
- Qué ha cambiado: desde el análisis anterior, o desde su alta si es el
  primero.
- Cómo evoluciona: tendencia de uso y de tamaño con sus cifras, y qué implica
  para su cuota en los próximos meses.
- Señales de riesgo: cada una con su dato, ordenadas por coste de ignorarlas.
  Si no hay, dilo con una línea.
- Oportunidades: qué comprarían y por qué su uso lo dice. Si no hay, dilo.
- Desarrollo a medida: el patrón y la propuesta, o «nada que se desprenda de
  estos datos».
- Qué haría esta semana: una o dos acciones concretas, con quién hablaría y
  qué le preguntaría.
- Lo que no se puede saber con estos datos: qué dato faltaría para afinar.

FORMATO: cada título en su propia línea, empezando por «## ». Debajo, prosa en
párrafos; listas con «- » solo donde la sección enumera señales.

SOBRE EL DOSSIER. Los centros se llaman CENTRO_1, CENTRO_2… por orden de alta y
mantienen su número entre análisis. La última semana de la serie está en curso:
no la compares como si estuviera cerrada. «salidasPuestasPorElSistema» son
jornadas que la persona no cerró y cerró la plataforma con la hora prevista.
«senalesCalculadas» son las que ya enseña la pantalla: úsalas, no las repitas.
```

Los dos últimos bloques (formato y lectura del dossier) se añadieron al implementar: no cambian
el criterio aprobado, dicen cómo pintar la respuesta y cómo leer tres campos que el modelo no
puede adivinar. Vive en `services/merlin/src/soporte/analisis-cliente/prompt.ts`.

## API

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/api/v1/backoffice/entities/:id/ficha` | Todo lo de las pestañas en una respuesta, cacheada 5 min; `?fresh=1`. Permiso `entities:read`; audita `entity.ficha_viewed`. |
| `GET` | `/api/v1/backoffice/entities/:id/personas` | La plantilla buscada y paginada en el servidor: `q` (sin mayúsculas ni acentos: nombre, puesto, correo), `filtro` (`activas`, `nunca_fichan`, `sin_fichar_30`, `todas`), `page`, `limit` (25/50/100). La ficha no manda la plantilla entera. |
| `GET` | `/api/v1/backoffice/entities/:id/analisis` | Estado (en curso, último fallo, datos del hilo) y los turnos del hilo; `?turnos=0` no relee OpenAI. |
| `POST` | `/api/v1/backoffice/entities/:id/analisis` | Lanza un análisis en segundo plano: 202, o 409 `analisis_en_curso`. Permiso nuevo `analisis:write` (root y admin); audita `entity.analisis_requested`. |
| `POST` | `/api/v1/gpt/soporte/analisis-cliente` (Merlin, S2S) | `{dossier, vigilar, conversationId?}` → `{texto, conversationId, modelo, consumo}`. 422 si hay fuga. |
| `GET` | `/api/v1/gpt/soporte/analisis-cliente/:conversationId` (Merlin, S2S) | Los turnos del hilo, del más reciente al más antiguo, sin el dossier. |
| `GET` | `/api/v1/billing/internal/entities/:id/ficha` (billing, S2S) | Facturas de Stripe (hasta 100), cuota estimada y almacenamiento de una empresa. Cada pieza `null` si falla. |

Código: `services/backoffice/src/application/clientes/` (`consultas.ts`, `ficha.ts`, `dossier.ts`,
`analisis.ts`), `services/merlin/src/soporte/analisis-cliente/`, pantalla en
`apps/backoffice-web/src/pages/cliente/`. Tests: `npm test -w services/backoffice` (curva de
plantilla, dossier sin personas) y `services/merlin/test/analisisCliente.test.ts` (borde).

## Lo que falta y se dice

- **Último acceso de quien lleva la cuenta**: `lastSignInTime` de Firebase Auth no se recoge.
  Hasta que entre en la cosecha nocturna, la ficha y el dossier dicen «sin medir». Nunca cero.
- **Sector y nicho** sólo si el cliente está en el CRM de `sales`.
- **Hoja informativa**: solo del espejo en Postgres (`dim_employees.notice_*`, migración 056). Donde no está, «sin medir»; **nunca** se lee de Firestore (Jose, 2026-11-07: «espera al espejado»).
- **Documentos**: sin agregado en Postgres; la ficha sólo sabe de la hoja informativa y lo dice.
- **Alta de cada centro**: `dim_branches` no la guarda; se toma el primer fichaje del centro
  (o su primera sincronización). Sirve para numerar `CENTRO_n` de forma estable.

## Despliegue (para `deployment-prod/proximo-pase-back.md` cuando suba a staging)

- Migración 058 `backoffice_cliente_hilo`, a mano. Sin ella la ficha funciona y el análisis
  falla con su motivo en pantalla.
- Variables opcionales en Merlin: `MERLIN_ANALISIS_CLIENTE_MODELO`,
  `MERLIN_ANALISIS_CLIENTE_MAX_SALIDA`. La clave de OpenAI ya está.
- Reconstruir `backoffice`, `merlin` y `billing` (ruta interna nueva); reiniciar nginx.
  Nginx no cambia.

## Fuera de este trabajo, visto de paso

- El manual de clientes abre con «plataforma SaaS de control horario con inteligencia
  operativa» (`Clients/01-primeros-pasos/01-que-es-checkbiz360.md`). Jose, el 2026-11-07:
  somos una plataforma de control operativo; el fichaje es un producto más. Alinear el manual.
- El roadmap de `91-planes-y-funcionalidades.md` dice que los adjuntos de documento en tareas
  no están disponibles; están en producción desde el 2026-11-02 (tasks TDR-007).
