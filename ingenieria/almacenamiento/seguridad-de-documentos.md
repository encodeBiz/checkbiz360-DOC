# Seguridad de los documentos en Storage · Documento de Ingeniería

Estado: **diseño, sin código**. Pedido por Jose el 2026-11-06: «necesito saber cómo podemos
securizar al máximo ese storage; si nos hackean, que los documentos no se puedan abrir».
Se hace en tres fases, una detrás de otra, y cada una se prueba en `dev-encodebiz` antes de
tocar `encodebiz-services`.

## De dónde partimos (medido el 2026-11-06, solo lectura)

Lo que ya está bien:

- Las reglas de Storage están cerradas del todo (`storage.rules`, desde el 2026-10-19): ningún
  cliente lista, sube ni descarga por el SDK. Todo pasa por la API.
- El servicio de documentos comprueba permisos y entrega URLs firmadas que caducan al minuto.
- Los registros de acceso a datos (`DATA_READ`, `DATA_WRITE`) están encendidos para todos los
  servicios del proyecto: cada descarga deja rastro.
- Borrado blando del bucket: 7 días.

Lo que nos deja al descubierto:

- **Una sola llave para todo.** Todos los contenedores usan la cuenta
  `firebase-adminsdk-fbsvc-clean`, que tiene `storage.admin` y es administradora de Firebase. Su
  clave está en el servidor. Quien la saque de cualquier contenedor, de un `.env` o del disco
  descarga todos los documentos de todos los clientes.
- **Los ficheros están en claro.** Google cifra sus discos, pero descifra para cualquiera que
  tenga permiso. Con la llave anterior, un contrato se abre tal cual.
- **Cuatro propietarios del proyecto con Gmail personal:** `encodebiz`, `joseAceMedina`,
  `asuar.abello` y `yasiel.encodebiz`. Una contraseña robada sin verificación en dos pasos da el
  proyecto entero.
- El bucket no tiene la prevención de acceso público forzada (`inherited`) ni el acceso
  uniforme activado.
- El bucket está en `US-CENTRAL1` (ver [aceptación legal](../aceptacion-legal/README.md)).
- `sheets-reader-service` tiene 2 claves de usuario activas: revisar si se usan.

## Fase 1 — Cerrar las puertas (sin código)

Objetivo: que nadie entre por una cuenta o un ajuste del bucket. Es una tarde de consola.

1. **Propietarios.** Quedan como `owner` solo quienes lo necesitan de verdad. El resto pasa a un
   rol menor o sale. Verificación en dos pasos obligatoria para todos, a ser posible con llave
   física.
2. **Bucket:**
   - prevención de acceso público **forzada**;
   - acceso uniforme activado: antes, comprobar en dev que siguen funcionando las URLs con token
     ya emitidas (In-App Messaging, `assets/`, avatares antiguos);
   - borrado blando a 30 días.
3. **Alerta de descarga masiva.** Los registros ya existen; falta que alguien los mire. Una
   métrica de registros sobre `storage.objects.get` bajo `documents/`, con aviso por correo si
   una misma identidad pasa de N lecturas en 10 minutos.
4. **Claves.** Rotar la de `fbsvc-clean`. Borrar las de `sheets-reader-service` si no se usan.

Se hace primero en `dev-encodebiz` y después, con OK de Jose, en `encodebiz-services`.

## Fase 2 — Cifrar cada documento antes de subirlo

Objetivo: que lo que hay en el bucket, aunque se lo lleven, no se pueda abrir.

**Cómo funciona (cifrado de sobre).**
- Al subir, el servicio de documentos genera una clave aleatoria para ese fichero (AES-256-GCM),
  cifra el contenido y sube solo el cifrado.
- La clave del fichero se guarda cifrada con una llave de **Cloud KMS** (anillo en Europa) que
  nunca sale de Google; va junto al documento, en Firestore.
- Para abrirlo, el servicio pide a KMS que descifre la clave del fichero y descifra en memoria.

**Quién puede usar la llave.** Una cuenta de servicio nueva y solo del servicio de documentos
(`documents-kms`), con permiso únicamente para cifrar y descifrar con esa llave. La llave
maestra de los demás servicios no puede.

**Lo que cambia en la descarga.** Hoy el panel y la app descargan directamente de Google con la
URL firmada. Un fichero cifrado no sirve así: la descarga pasa a ser una ruta del servicio que
comprueba permisos, descifra y entrega el fichero. Para el usuario no cambia nada.

**Lo que hay que repasar, porque lee documentos:**
- la firma PAdES y el acuse firmado (`AcknowledgeDocument`, `SignatureEvidence` de `shared`);
- la hoja propia de la empresa;
- el export de la purga de empresas del backoffice (`purgaEmpresas.ts`), que descarga ficheros
  y pasaría a pedirlos al servicio de documentos;
- el contador de espacio: cuenta el tamaño del objeto cifrado, unas decenas de bytes más; no
  cambia el cobro.

**Migración.** Un script cifra los documentos existentes y los copia a un **bucket nuevo en
Europa**: se aprovecha para salir de EE. UU. Como todo lo que borra, simula por defecto y solo
actúa con `--apply`. Los originales en claro se borran cuando se haya comprobado que cada
documento migrado se abre.

**El límite.** Si alguien toma el control del propio servicio de documentos mientras funciona,
puede descifrar lo mismo que él. Lo que gana esta fase es que un robo deje de ser «se lo
llevaron todo»: hay que atacar un servicio concreto, cada uso de la llave queda registrado y la
llave se puede desactivar en un segundo, lo que deja todo ilegible al instante.

## Fase 3 — Una llave por servicio

Objetivo: que un fallo en un servicio no abra los demás.

- Una cuenta de servicio por contenedor, con solo los permisos que usa. Storage, con condiciones
  por prefijo: solo `documents` ve `documents/`, `reports` sus informes, etc.
- `fbsvc-clean` pierde `storage.admin`. Lo mismo, cuando toque, con Firestore.
- Requiere inventario de qué toca cada servicio: hoy lo hacen `shared`, `backoffice`, `billing`,
  `checkinbiz`, `documents`, `entities`, `reports` y `tasks`.

## Orden y criterio de cierre

| Fase | Riesgo que quita | Esfuerzo | Se da por cerrada cuando |
|---|---|---|---|
| 1 | Entrar por una cuenta o por el bucket | Una tarde, sin código | Propietarios revisados con 2FA, bucket endurecido, alerta probada en dev |
| 2 | Que un robo del bucket o de la llave común abra los documentos | Unos días | Todo documento nuevo y migrado está cifrado y en Europa; descarga por el servicio; QA en verde |
| 3 | Que un servicio caído abra los demás | Unos días | Cada contenedor con su cuenta; `fbsvc-clean` sin `storage.admin` |

Nada de esto sale a producción sin el OK de Jose, y siempre primero en desarrollo.
