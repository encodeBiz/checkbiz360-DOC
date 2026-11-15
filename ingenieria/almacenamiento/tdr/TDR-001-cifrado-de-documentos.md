# TDR-001 — Cifrado de los documentos en Storage

**Fecha:** 2026-11-11
**Estado:** Diseño aprobado ([ADR-003](../adr/ADR-003-cifrado-de-documentos-con-llave-en-el-servidor.md)) · implementación en `feat/cifrado-documentos`
**Componentes:** `services/documents` (todo lo criptográfico), `packages/shared` (cliente interno),
`services/customers` y `services/merlin` (dejan de tocar ficheros por su cuenta), compose de
staging y producción
**Tarea:** CheckBiz360 `vq6ZP2dzeaTiyHGEK2rh` («Seguridad de documentos en Storage»)

---

## 1. Qué se cifra

Todo objeto bajo estos prefijos del bucket por defecto:

| Prefijo | Qué es |
|---|---|
| `documents/entities/{e}/…` | el fichero del documento, el firmado (`signed/…`), la hoja propia (`entity/data-protection-notice/…`) y los justificantes (`customer/…`) |
| `signatures/pending/{e}/…` | el PDF preparado para firmar: es el documento entero |

**No** se cifran (no llevan el contenido del documento): `signatures/evidence/…` (firma y
atributos), las actas de `checkbiz/reports/…`, los adjuntos de tareas (`media/…`), las fotos del
quiosco ni nada fuera de esos prefijos. Quedan para otra decisión.

`contentSha256`, `signed.sha256` y `sizeBytes` siguen siendo **del contenido en claro**: la
firma, la evidencia y el acta se atan al contenido, no al cifrado.

## 2. La llave maestra

- Un fichero JSON montado **solo** en el contenedor de `documents` como secreto de Compose:

  ```json
  {"current": "k2026a", "keys": {"k2026a": "<32 bytes en base64>"}}
  ```

  `keys` puede tener varias (la anterior durante un cambio de llave). `current` es con la que se
  cifra; con cualquiera de `keys` se descifra. `kekId`: `[a-z0-9]{1,32}`.
- En el servidor: `./secrets/documents-kek.json` (fuera de `x-secret-volumes`, que se monta en
  todos). Compose:

  ```yaml
  secrets:
    documents_kek:
      file: ./secrets/documents-kek.json
  services:
    documents:
      secrets: [documents_kek]       # → /run/secrets/documents_kek
  ```

  Ruta configurable con `DOCUMENTS_KEK_FILE` (por defecto `/run/secrets/documents_kek`). Comprobar
  que el usuario del contenedor puede leerlo (permisos del fichero en el host).
- **Copia**: la carpeta `./secrets` ya entra en la copia de seguridad del servidor (cifrada con la
  clave pública de copias). Además, **una copia fuera del servidor, a mano, donde diga Jose**,
  antes de activar la escritura cifrada en producción. Sin esa copia, no se activa.
- Nunca se escribe la llave en un log, un error ni una respuesta.

## 3. Formato del fichero cifrado (v1)

```
0      "CBZE"                       4 bytes (43 42 5A 45)
4      versión = 0x01               1 byte
5      L = longitud del kekId       1 byte (1..32)
6      kekId                        L bytes ASCII
6+L    clave del fichero envuelta   60 bytes = iv(12) ‖ cifrado(32) ‖ tag(16)
66+L   iv del contenido             12 bytes
78+L   contenido cifrado            n bytes
       tag del contenido            16 bytes
```

- **Clave del fichero**: 32 bytes aleatorios por fichero (`crypto.randomBytes`), nueva en cada
  escritura, también al copiar o volver a subir.
- **Envuelta** con la llave `current`: AES-256-GCM, iv aleatorio, AAD = `"cbz-dek:v1:" + kekId`.
- **Contenido**: AES-256-GCM con la clave del fichero, iv aleatorio, AAD = **todos los bytes de
  la cabecera** (de 0 a 78+L). Cambiar un byte de la cabecera o del cifrado hace fallar el tag.
- **Detección**: un objeto está cifrado si empieza por `CBZE` + `0x01`. Los ficheros admitidos
  (PDF `%PDF`, JPEG, PNG, WebP, Office) nunca empiezan así. Además, al subir cifrado se pone el
  metadato del objeto `cbzEncryption: v1`, solo informativo: **manda la cabecera**.
- Sobrecoste: 94 + L bytes por fichero. El contador de espacio verá el tamaño cifrado; no cambia
  el cobro.

## 4. Lectura y escritura dentro de `documents`

Un único módulo (`DocumentCrypto` o el nombre que encaje) con `encrypt(plain)`, `decrypt(stored)`
e `isEncrypted(stored)`, y **todas** las lecturas y escrituras de ficheros de documentos pasan
por dos funciones del `DocumentStorageService`:

- `writeDocumentFile(path, bytes, contentType)`: cifra si la escritura cifrada está activa (§6).
- `readDocumentFile(path)`: lee y, si empieza por `CBZE`, descifra; si no, lo devuelve tal cual
  (transición).

Sitios que pasan a usarlas (inventario del 11-nov): `CreateDocument` (subida),
`PrepareDocumentSignature` (lee el original, escribe el preparado), `AcknowledgeDocument` (lee el
preparado, escribe el firmado), `SendDataProtectionNotice` (lee la hoja propia; vista previa) y
`dataProtectionNotice.controller` (escribe la hoja propia). `uploadPrivateOnce` mantiene su
`ifGenerationMatch: 0`. Borrados y metadatos no cambian.

Si un objeto está cifrado y la llave no está (o el `kekId` no está en `keys`): error
`documents/key_unavailable` (500) y una línea de log con la ruta y el `kekId`. Nunca se devuelve
el cifrado como si fuera el fichero.

## 5. La descarga: misma respuesta, URL nuestra

`GET /documents/:id/download` **sigue devolviendo `{url}`** (panel y app no cambian). Con la llave
cargada, la URL deja de ser de Google y pasa a ser:

```
{DOCUMENTS_PUBLIC_BASE_URL}/api/v1/documents/files/{token}
```

- `token = base64url(payload) + "." + base64url(HMAC-SHA256(Ktok, base64url(payload)))`
- `payload` (JSON): `{e: entityId, d: documentId, p: storagePath, n: nombre, m: mimeType, x: caduca_unix}`
  con `x = ahora + 60 s`, como la URL de Google de hoy.
- `Ktok = HKDF-SHA256(llave current, salt vacía, info "cbz-download-token:v1", 32 bytes)`. Al
  cambiar de llave caducan los tokens vivos (un minuto): aceptado.
- `GET /api/v1/documents/files/:token` **sin** cabecera `Authorization` (igual que una URL firmada
  de Google: el permiso ya se comprobó al pedir la URL). Comprueba firma en tiempo constante y
  caducidad, lee con `readDocumentFile(p)` y responde los bytes con `Content-Type: m`,
  `Content-Disposition: inline; filename*=UTF-8''<n>`, `Cache-Control: private, no-store`,
  `X-Content-Type-Options: nosniff`. Token inválido o caducado → 404 sin detalle.
- El registro de actividad `download_requested` se sigue escribiendo al pedir la URL, como hoy.
- Sin llave cargada, la descarga sigue con la URL firmada de Google (comportamiento de hoy).
- `DOCUMENTS_PUBLIC_BASE_URL`: `https://api-staging.checkbiz360.com` / `https://api.checkbiz360.com`.
  Comprobar que nginx deja pasar `/api/v1/documents/files/…` hasta `documents`.

## 6. Activación y vuelta atrás

| Estado | Llave | `DOCUMENTS_ENCRYPT_WRITES` | Qué pasa |
|---|---|---|---|
| Hoy | no | — | Todo en claro, URL de Google. El código nuevo desplegado sin llave no cambia nada. |
| Lectura preparada | sí | `false` | Escribe en claro; lee ambos; descarga por URL nuestra. Primer paso en cada entorno. |
| **Cifrando** | sí | `true` | Todo lo nuevo se escribe cifrado. |
| Vuelta atrás | sí | `false` | Deja de cifrar lo nuevo; lo ya cifrado se sigue leyendo. **La llave no se quita nunca** mientras exista un fichero cifrado. |

Con `DOCUMENTS_ENCRYPT_WRITES=true` y la llave ausente o inválida, `documents` **no arranca**
(falla cerrado, el healthcheck lo enseña al desplegar).

## 7. Los demás servicios dejan de tocar ficheros de documentos

Solo `documents` tiene la llave. Lo que hoy lee o escribe ficheros del documental por su cuenta
pasa por dos rutas internas nuevas de `documents`, con la misma autenticación servicio a
servicio que ya usa `/documents/internal/data-protection-notice`:

- `POST /api/v1/documents/internal/files` — cuerpo `{entityId, storagePath, contentType, contentBase64}`.
  `storagePath` tiene que empezar por `documents/entities/{entityId}/`; tope de 10 MB. Escribe con
  `writeDocumentFile` y devuelve `{sizeBytes, sha256}` del contenido en claro.
- `GET /api/v1/documents/internal/files?entityId=…&storagePath=…` — misma regla de prefijo;
  devuelve los bytes en claro (`application/octet-stream`).

Cliente en `@encodebiz/shared` (junto a `dataProtectionNoticeClient`, mismo estilo y misma
variable de URL interna): `putDocumentFile(…)` y `getDocumentFile(…)`.

Consumidores que cambian:

| Dónde | Hoy | Pasa a |
|---|---|---|
| `customers` `FirestoreExpenseReceipts.copyFile` | baja el ticket y lo sube al documental | baja el ticket (`media/…`, en claro) y lo sube con `putDocumentFile` |
| `customers` `FirestoreExpenseReceipts.saveFile` | sube directo | `putDocumentFile` |
| `merlin` `contratos.router.ts:63` («Leer el PDF») | lee el fichero | `getDocumentFile` |
| `merlin` `gastos/application/documento.ts:64` | lee el justificante | `getDocumentFile` |

Los borrados de `customers` (`removeFile`, `FirestoreCustomerDocuments.remove`) siguen directos:
borrar no necesita la llave. La purga del backoffice copia objetos tal cual: el cifrado viaja con
ellos y la llave sigue en el servidor; no cambia.

## 8. Los documentos que ya existen

Script `services/documents/src/scripts/encrypt-existing.ts`:

- `--entity <id>` o `--all`; **simula por defecto** y solo escribe con `--apply`.
- Recorre `documents/entities/{e}/` y `signatures/pending/{e}/`; salta lo que ya empieza por `CBZE`.
- Por objeto: baja, cifra, **descifra lo cifrado y compara el sha256 con el original** antes de
  escribir; escribe en la misma ruta con `ifGenerationMatch` de la generación leída (si alguien lo
  cambió entretanto, lo salta y lo cuenta), conservando `contentType` y metadatos.
- `--reverse`: lo contrario (descifra en su sitio), para volver atrás. También simula por defecto.
- Informe final: vistos, ya cifrados, cifrados, saltados por cambio, errores. Nunca borra.
- El borrado blando del bucket (7 días hoy) guarda la versión anterior de cada objeto reescrito.

## 9. Pruebas

**Unitarias (`documents`)**: ida y vuelta de varios tamaños (0 bytes, 1 byte, 10 MB); un byte
cambiado en cabecera, clave envuelta, iv, contenido o tag → falla; `kekId` desconocido →
`key_unavailable`; descifrado con la llave anterior de `keys`; un PDF en claro se lee tal cual;
token de descarga válido, caducado, con firma cambiada y con payload cambiado; arranque con
escritura cifrada y sin llave → error. Las suites existentes de `documents`, `customers`, `merlin`
y `shared` siguen en verde.

**En staging** (empresa de pruebas, nunca datos de cliente):

1. Subir un documento → el objeto del bucket empieza por `CBZE`; el panel y la app lo abren.
2. Firmar un PDF desde la app (PAdES) → el preparado y el firmado están cifrados; el acta se genera.
3. Hoja propia: subir, vista previa y envío a empleados.
4. Justificante de gasto desde un ticket de tarea y subido a mano; «Leer el PDF» de un contrato.
5. Script: simular sobre la empresa de pruebas, `--apply`, abrir documentos viejos, `--reverse`.
6. Vuelta atrás: `DOCUMENTS_ENCRYPT_WRITES=false` → lo nuevo en claro, lo cifrado se sigue abriendo.

## 10. Antes de producción (no es de hoy)

- **La Cloud Function antigua `documentsHandler` sigue desplegada en producción** y escribe y
  descarga en claro. Antes de activar nada: confirmar en Vercel que
  `NEXT_BACKEND_URI_CHECKINBIZ_DOWNLOAD_DOCUMENTS` y `…_DOCUMENTS_HANDLER` apuntan al contenedor,
  y apagar esa función (con `--project` explícito y OK de Jose).
- La copia de la llave fuera del servidor (§2).
- Orden: código sin llave → llave con `ENCRYPT_WRITES=false` → `true` → script por empresas.

## 11. Precisiones de la implementación (11-nov) y despliegue en staging

Revisado contra este TDR; el formato se ha comprobado descifrando con una implementación escrita
aparte solo desde §3 (ida y vuelta de 0 B, 1 B y 200 KB; manipular kekId, clave envuelta, iv,
contenido o tag hace fallar; dos cifrados del mismo fichero difieren). Tests: `shared` 203,
`documents` 95, `customers` 113, `merlin` 163, todos en verde.

Donde el TDR dejaba margen:

- Fichero de llave **ausente o vacío** = sin llave (como hoy). Fichero **con contenido que no
  vale** = `documents` no arranca, aunque no cifre: seguir sin llave dejaría ilegible lo cifrado.
- Con llave y **sin `DOCUMENTS_PUBLIC_BASE_URL`**, no arranca: volver a la URL de Google
  entregaría el cifrado.
- Fichero manipulado: `documents/decrypt_failed` (500). Llave o `kekId` ausentes:
  `documents/key_unavailable` (500).
- El token de descarga solo abre rutas `documents/entities/{e}/` de su propia empresa.
- Las rutas internas rechazan segmentos vacíos, `.` y `..`; JSON de hasta 14 MB solo en
  `/internal/files` (10 MB de fichero en base64); todas las escrituras con
  `cacheControl: private, no-store`.
- `customers` y `merlin`: el cliente de `shared` lanza `DocumentFileError` (no se traga el
  error como el de la hoja). `merlin` sigue respondiendo 404 `fichero_no_encontrado` ante
  cualquier fallo (contrato sin cambios; el log lleva el código real).
- Un ticket de tarea de más de 10 MB ya no se copia como justificante (antes sí): se registra
  y se puede reintentar.
- `DOCUMENTS_INTERNAL_URL` por defecto `http://documents:3007`; `customers` y `merlin` llegan
  sin tocar compose. `customers` no está aún en el compose de producción.
- nginx ya deja pasar `/api/v1/documents/files/…`. Pone `X-Frame-Options: DENY`: el panel no
  incrusta documentos en iframe, pero comprobarlo al probar.
- El contenedor de `documents` corre como root: lee el fichero de la llave con cualquier permiso;
  dejarlo en `600`.

**RIESGO DE DESPLIEGUE — antes de fusionar en `staging` (y luego en `main`):** el secreto de
Compose es un *bind mount* que no se crea solo. Si `./secrets/documents-kek.json` **no existe**
en el servidor, `documents` no se crea y `up -d` falla (y en staging nginx depende de que
`documents` esté sano). Primero, en el servidor: `touch secrets/documents-kek.json` (vacío =
sin llave); después, desplegar.

**Orden en staging (12-nov):**

1. En el VPS, `touch /opt/encodebiz-api-dev/secrets/documents-kek.json`.
2. Push de `feat/cifrado-documentos`; merge a `develop` y `staging` con `[skip ci]`.
3. `up -d --build --no-deps documents customers merlin` + reiniciar nginx. Sin llave: todo como
   hoy (comprobar descarga y firma).
4. Generar la llave de staging y escribir el JSON en ese fichero; `DOCUMENTS_PUBLIC_BASE_URL` en
   `.env.staging`; reiniciar `documents` → «lectura preparada» (§6). Descargas por URL nuestra.
5. `DOCUMENTS_ENCRYPT_WRITES=true`; reiniciar → pruebas de §9 en la empresa de pruebas.
6. Script sobre la empresa de pruebas: simular, `--apply`, abrir, `--reverse`, `--apply`.

**Hecho en staging el 13-nov**, del paso 1 al 6 y la vuelta atrás de §9.6. Llave `dev2026a`, generada en
el VPS, y cifrado de escritura activo. Resultados y pasos de producción en
[proximo-pase-back §71](../../../deployment-prod/proximo-pase-back.md). Quedan por probar a mano el panel,
la app, «Leer el PDF» y el justificante desde un ticket.

## Siguiente fase, decidida: evidencias y actas de firma

Jose, 15-nov, validando en staging: «hay que pasarlo en la siguiente fase, esto es importante». Al firmar
el acuse de una imagen en Cuidama quedaron en claro en el bucket la evidencia
(`signatures/evidence/{e}/documents.acknowledgement/{reto}.json`) y el acta
(`checkbiz/reports/entities/{e}/actas/v2/acta_{reto}.pdf`, entregada con enlace de Google). No llevan el
documento, pero sí quién firmó qué y cuándo, su `uid`, el id y los datos de su móvil y, en el acta, su
nombre: son tan privados como el documento. No permiten firmar por nadie —solo llevan la clave pública—.

Lo que hay que resolver, sin diseñar todavía:

- la evidencia la escribe `shared` (`SignatureEvidence`) desde varios servicios (documentos, inventario)
  y la lee `reports` para montar el acta; hoy solo `documents` tiene la llave (ADR-003 §5; ADR-004 propone
  otra cosa y hay que cerrarla antes);
- el acta deja de entregarse con enlace de Google y pasa a enlace propio, como los documentos;
- el script de migración se amplía a esos dos prefijos;
- el perito tiene que seguir pudiendo verificar la evidencia: los pasos de OpenSSL del acta no cambian,
  pero la evidencia se le entrega ya descifrada.

## Fuera de alcance

Mover el bucket a Europa; cifrar adjuntos de tareas y fotos del quiosco; las
fases 1 y 3 del [diseño](../seguridad-de-documentos.md); `purgaEmpleado` no encuentra los
firmados bajo `signed/{doc}/{empId}-vN/` (fallo aparte, anotado aquí para no perderlo).
