# Hoja informativa: versionado

**Estado:** Hallazgo y propuesta, sin código. Nada de lo de abajo está decidido.
**Fecha:** 2026-11-15. Leído en la API en `origin/staging` (lo desplegado en el VPS de desarrollo;
el checkout local de `staging` iba 25 commits por detrás y no traía el cifrado) y en el panel en
`develop`. Las líneas citadas son las de esa versión.

Va con el diseño de la hoja (`README.md` de esta carpeta) y con el documental
(`../documental-service/`).

## 1. El problema, tal como lo contó Jose

Probando en staging con Cuidama, el 2026-11-15: «la hoja informativa tiene un problema y es que
si se ha firmado una vez no me deja actualizarla; esto debe estar versionado; imagina que se
actualice, la liada es gorda».

Lo que espera: publicar una versión nueva de la hoja, que cada firma anterior siga ligada a la
versión que esa persona firmó, y ver claro quién tiene que volver a firmar.

## 2. Qué lo impide hoy

**Comprobado en el código.** Ni el servidor ni el panel tienen una condición del tipo «si ya
está firmada, no se deja cambiar». Lo que hay:

- **La única negativa es el envío, y no mira la firma, mira la versión.**
  `services/documents/src/application/use-cases/document/SendDataProtectionNotice.ts:155-156`:
  si la ficha de la persona ya tiene la versión vigente y un `documentId`, se la salta con
  `already_current`. El panel lo dice con un aviso informativo
  (`encodebiz-front-saas/src/app/main/[entityId]/checkinbiz/documents/components/DocumentUploadModal.tsx:331-333`,
  texto en `locales/es/common.json:1166`): «Esta persona ya tiene la versión vigente de la hoja
  informativa.» No hay error HTTP: la respuesta es 201 con la persona en `skipped`.
- **La hoja de CheckBiz360 casi nunca cambia de versión.** Su versión es una constante,
  `NOTICE_VERSION = "2026-11-04.5"`
  (`services/documents/src/application/services/dataProtectionNotice/template.ts:13`), que solo
  cambia al tocar el código. Cambiar los datos en Entidad → Protección de datos (contacto, modo
  de fichaje) no la cambia (`dataProtectionNotice.controller.ts:67`). Aunque el PDF salga
  distinto, para el servidor es «la misma versión» y no se reenvía.
- **La hoja propia sí cambia de versión al subirla.** Cada subida es `propia-<ms>`
  (`dataProtectionNotice.controller.ts:96`). El botón «Sustituir» del panel solo se desactiva
  mientras sube
  (`src/app/main/[entityId]/entity/tabs/tabEntity/DataProtectionNoticeSettings.tsx:149-151`), y
  después el envío ya no se salta a nadie.
- **Un documento enviado no se puede cambiar de fichero.** Editar solo toca título,
  descripción, visibilidad, acuse, caducidad y metadatos
  (`services/documents/src/application/use-cases/document/UpdateDocument.ts:21-30`). Cambiar la
  hoja de alguien siempre es mandarle un documento nuevo.

**Lo que supongo.** No he podido reproducir lo que hizo Jose. Hay dos explicaciones posibles y
las dos encajan con «no me deja»:

- **A.** Cambió los datos de la hoja de CheckBiz360 y la volvió a mandar. Le salió «ya tiene la
  versión vigente» porque la versión no cambia (punto 2). Es un efecto colateral: el comentario
  de `SendDataProtectionNotice.ts:15-17` dice que se omite «quien ya tiene la versión vigente:
  mandarla dos veces solo molesta», pero da por hecho que todo cambio del texto sube
  `NOTICE_VERSION`, y los datos de la empresa no la suben.
- **B.** Sustituyó su hoja propia y la mandó. El envío funciona, pero la lista de empleados
  sigue diciendo «Firmada el <fecha antigua>» (ver el punto 4) y parece que no ha cambiado nada.

Hay que preguntarle a Jose cuál de las dos fue (pregunta 1 del punto 6).

## 3. Cómo funciona hoy la versión y qué guarda cada firma

**Comprobado en el código.**

Hay **tres «versiones» distintas** y no hablan entre sí:

1. **La versión de la hoja** (`NOTICE_VERSION` o `propia-<ms>`), que devuelve
   `currentNoticeVersion` (`SendDataProtectionNotice.ts:116-118`). Se guarda en la ficha de la
   persona y en `metadata.externalRef = "data_protection_notice:<versión>"` del documento
   (`SendDataProtectionNotice.ts:178`). Cuando la empresa sube un PDF suelto a una persona desde el
   modal, la ficha guarda la versión literal `"propia"`, sin fecha (`markOwnNotice`,
   `SendDataProtectionNotice.ts:86-90`, llamada desde `createDocument.controller.ts:277-279`).
2. **La versión del documento** (`doc.version`). Empieza en 1 (`CreateDocument.ts:81`) y sube con
   cada edición de metadatos (`UpdateDocument.ts:59`). No es la versión de la hoja.
3. **`documentVersion` del acuse**: el `doc.version` del momento de firmar
   (`AcknowledgeDocument.ts:83`).

**Qué se guarda al enviar.** Cada envío crea un documento nuevo para cada persona, con **su
propia copia** del PDF en
`documents/entities/{entityId}/employee/{employeeId}/{documentId}/{ts}-{fichero}`
(`CreateDocument.ts:47-57`, ruta en `DocumentStorageService.buildStoragePath`) y la huella del
contenido en claro, `contentSha256` (`CreateDocument.ts:77`). Luego escribe en la ficha
`dataProtectionNotice: {version, documentId, sentAt}` (`SendDataProtectionNotice.ts:182-184`).

**La plantilla de la hoja propia** está en
`documents/entities/{entityId}/entity/data-protection-notice/{ms}-{fichero}`
(`SendDataProtectionNotice.ts:120-123`) y su ficha en `entity.dataProtectionNotice.ownDocument`
(`dataProtectionNotice.controller.ts:91-100`). Solo existe una a la vez: al subir otra, la
anterior **se borra de Storage** (`dataProtectionNotice.controller.ts:101-102`), y al quitarla
también (`:115-118`). No queda ningún registro de qué plantillas hubo.

**Qué guarda cada firma.** El acuse (`AcknowledgeDocument.ts:77-88`) guarda `documentId`,
`documentVersion`, el método y, si va firmado, la firma con su reto. El reto firmado incluye
`{documentId, version, contentSha256, keyId}` (`AcknowledgeDocument.ts:63`;
`PrepareDocumentSignature.ts:75`). Con firma dentro del PDF (PAdES), el PDF firmado queda en
`documents/entities/{entityId}/signed/{documentId}/{employeeId}-v{doc.version}/…-firmado.pdf`.
El documento pasa a apuntar a ese fichero y el original se conserva en
`signed.originalStoragePath` (`AcknowledgeDocument.ts:127-138`). El acta la dibuja `reports` en
`checkbiz/reports/entities/{entityId}/actas/v2/acta_{challengeId}.pdf`
(`DeleteDocument.ts:25-28`). Al firmar, la ficha apunta `signedAt`, pero solo si su
`documentId` sigue siendo el firmado (`SendDataProtectionNotice.ts:215-221`).

**En resumen:** la prueba de cada firma está atada a **su** documento y a la huella de **su**
copia, y eso aguanta. Lo que no aguanta es la ficha de la persona, que solo recuerda la última
hoja enviada.

## 4. Qué pasa hoy si se manda una versión nueva

**Comprobado en el código**, salvo donde se indica.

- **No se sobrescribe lo que alguien ya firmó.** Cada persona tiene su copia y su documento
  (punto 3). Borrar la plantilla anterior (`dataProtectionNotice.controller.ts:102`) no toca las
  copias. Las actas y los PDF firmados siguen apuntando a ficheros que existen.
- **La ficha se queda con un «firmada» que ya no vale.** Esto es lo grave.
  `SendDataProtectionNotice.ts:182-184` escribe `{version, documentId, sentAt}` con
  `set(…, {merge: true})`. Firestore mezcla los campos de dentro del mapa (comportamiento
  documentado del SDK; no lo he probado contra la base), así que el `signedAt` de la versión
  anterior **se queda**. Después de mandar la versión nueva, la ficha dice «versión nueva,
  documento nuevo, firmada el <fecha de la versión anterior>». Lo mismo pasa con `markOwnNotice`
  (`:86-90`). Las consecuencias:
  - La lista de empleados enseña «Firmada el dd/mm» aunque no haya firmado la nueva
    (`src/app/main/[entityId]/checkinbiz/employee/page.controller.tsx:236-240` mira solo
    `signedAt`).
  - El espejo copia ese `signedAt` a `dim_employees.notice_signed_at`
    (`services/analytics/src/application/SyncDimensions.ts:140, 178-180`), y la alerta
    `notice_unsigned` cuenta solo a quien tiene `notice_signed_at IS NULL`
    (`services/analytics/src/application/alerts/BuildPanelAlerts.ts:102-108`). **Quien firmó la
    versión anterior y no la nueva no sale en la alerta.**
  - Cuando firme la nueva, `markSigned` pisa el `signedAt`. Hasta entonces no hay forma de verlo.
- **No se distinguen versiones en ningún sitio que la empresa vea.** La columna, el CSV y la
  alerta solo saben «firmada / enviada / nada». `notice_version` está en `dim_employees`, pero
  nadie la lee para avisar.
- **Se pierde el historial en la ficha, no en el documental.** La ficha solo guarda la última
  hoja. Las anteriores (documento, acuse, acta) siguen en el documental y se pueden buscar por
  persona y tipo `data_protection_notice`, pero nadie las cruza.
- **Las hojas subidas sueltas no se distinguen entre sí.** Con versión `"propia"`, dos hojas
  distintas subidas a mano a la misma persona tienen la misma versión.
- **Borrar no arregla la ficha.** Al eliminar una hoja que no es la última de la ficha, la ficha
  no cambia (`DeleteDocument.ts:182-187`). Esto está bien, pero conviene saberlo.

**Lo que supongo.** La app no tiene lógica propia de la hoja (no he encontrado
`data_protection_notice` en `checkbiz360/lib`). La trata como un documento más con acuse, así que
la versión nueva le llega como un documento pendiente más y la anterior sigue en la lista como
firmada. No lo he probado en un móvil.

## 5. PROPUESTA de versionado (sin decidir)

Ordenada de lo que hace falta antes a lo que puede esperar.

1. **Arreglar el `signedAt` heredado.** Esto vale para cualquier opción de abajo. Al apuntar un
   envío nuevo en la ficha, `signedAt` se borra (escribir el mapa entero, o
   `signedAt: FieldValue.delete()`). Es un cambio de una línea en `SendDataProtectionNotice.ts:182`
   y otra en `markOwnNotice`. Además, hay que corregir las fichas que ya tengan una firma heredada:
   un script que simula por defecto y compara `signedAt` con el acuse de `documentId`.
2. **Una versión que salga del contenido, no de la mano.** Cada hoja que se envía guarda la huella
   de su PDF (`contentSha256`, que ya se calcula sobre el contenido en claro). La empresa tiene un
   registro de versiones publicadas en `entities/{id}/dataProtectionNoticeVersions/{versionId}`:
   origen (plataforma o propia), `NOTICE_VERSION` o fichero, huella de la plantilla, quién la
   publicó, cuándo y una nota opcional («cambio del encargado»). La hoja de CheckBiz360 lleva datos
   de cada persona, y por eso el PDF de cada una tiene una huella distinta. Para ella, la versión
   sería `NOTICE_VERSION` más una huella de los datos de la empresa con los que se dibuja
   (`noticeParams` sin el nombre de la persona). Así, cambiar el contacto o el modo de fichaje
   crea una versión nueva sin que nadie tenga que acordarse de subir la constante.
3. **No borrar plantillas.** Subir una hoja propia nueva no borra la anterior (quitar
   `dataProtectionNotice.controller.ts:101-102`): pasa a «retirada» en el registro. El espacio es
   poco y cuenta en el almacenamiento de la empresa, porque la ruta ya lleva el `entityId`.
4. **La ficha con historial.** `dataProtectionNotice` sigue siendo la última, para que la lista no
   cruce nada, y gana `versionId` y `currentVersionId`. Debajo, una subcolección
   `noticeHistory/{documentId}` con `{versionId, documentId, sentAt, signedAt}` por cada hoja
   recibida. Cada firma ya está atada a su documento. Esto solo permite responder «qué versión
   firmó» sin buscar.
5. **Publicar una versión nueva es una acción explícita.** Al sustituir la hoja propia (o al
   guardar datos que cambian la de CheckBiz360), el panel dice cuántas personas firmaron la
   anterior y pregunta qué hacer: «enviársela a todos los que tienen una anterior» o «solo a las
   altas nuevas». Lo que ya está firmado no se toca: sigue siendo la prueba de lo que se informó
   entonces.
6. **Estado por persona con tres valores, no dos.** «Firmada la vigente», «firmó una anterior»
   (con la fecha y la versión), «enviada sin firmar» o nada. La alerta `notice_unsigned` cuenta a
   quien no tiene firmada la **vigente**, y en el texto separa «sin firmar ninguna» de «firmó una
   anterior». Esto pide `notice_version` comparada con la vigente en el espejo, o un
   `notice_current` que escriba el documental.
7. **El envío deja de saltarse por versión sola.** Se salta a quien ya tiene la vigente **y** no la
   tiene pendiente de firma. Reenviar a quien ya la tiene firmada sigue sin hacerse, pero el panel
   lo explica con la fecha de la firma.
8. **App.** La versión anterior pasa a «sustituida» en la lista de documentos de la persona
   (archivada para ella, no borrada), para que en el móvil solo haya una hoja pendiente. Mientras
   la app no cambie, esto se puede hacer desde el servidor archivando el documento anterior al
   mandar el nuevo, siempre que archivar no oculte el acta en el panel. **No lo he comprobado.**

**El cifrado no estorba** (comprobado). La plantilla se escribe con `writeDocumentFile`
(`dataProtectionNotice.controller.ts:90`) y se lee con `readDocumentFile`
(`SendDataProtectionNotice.ts:148, 200`). Este lee también las plantillas en claro anteriores al
cifrado (`DocumentStorageService.readDocumentFile` → `openStored`: lo que no empieza por `CBZE` se
devuelve tal cual). Solo hay una regla que respetar: **la huella de una versión se calcula siempre
sobre el PDF en claro** (como ya hace `CreateDocument.ts:77`), nunca sobre lo guardado en Storage
ni sobre su `md5Hash`. Cada escritura cifrada usa una clave de fichero nueva, así que dos subidas
del mismo PDF dan bytes guardados distintos. Para comparar versiones hay que usar
`contentSha256`.

## 6. Preguntas que tiene que cerrar Jose

1. ¿Qué hiciste exactamente cuando no te dejó: cambiar los datos de la hoja de CheckBiz360 y
   reenviarla (A), o sustituir tu hoja propia (B)? ¿Qué viste: el aviso «ya tiene la versión
   vigente» o la lista que seguía diciendo «Firmada»?
2. Al publicar una versión nueva, ¿se reenvía sola a toda la plantilla que tenía la anterior, o
   la empresa elige? El diseño de hoy dice «ni se avisa ni se reenvía» (`README.md` §5).
3. ¿Cambiar el contacto o el modo de fichaje de la hoja de CheckBiz360 cuenta como versión nueva
   que hay que volver a firmar, o solo cuando cambia el texto legal?
4. Quien firmó una versión anterior y no la nueva, ¿sale en rojo en `notice_unsigned` igual que
   quien no firmó nunca, o con otro aviso menos grave?
5. En la app, ¿la hoja anterior firmada desaparece de la lista de la persona (archivada) o se
   queda como «sustituida»?
6. ¿Arreglamos ya el punto 5.1 (el «firmada» heredado) como hotfix, antes del versionado
   completo? Hoy en staging puede enseñar como firmada a quien no ha firmado la hoja vigente.
