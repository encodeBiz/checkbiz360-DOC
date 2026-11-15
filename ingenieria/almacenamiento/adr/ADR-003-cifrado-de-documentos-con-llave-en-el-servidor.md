# ADR-003 — Cada documento se cifra antes de subirlo, con la llave maestra en el servidor (sin Cloud KMS por ahora)

**Fecha:** 2026-11-11
**Estado:** Aceptada
**Decisionario:** Jose Acevedo
**Desarrolla:** [seguridad-de-documentos.md](../seguridad-de-documentos.md), «Fase 2»
**Diseño:** [TDR-001 — cifrado de documentos](../tdr/TDR-001-cifrado-de-documentos.md)
**Enmendada por (propuesta, 14-nov):** [ADR-004](ADR-004-ficheros-de-empresa-con-una-sola-pieza-en-shared.md), puntos 3 y 5: una sola pieza en `shared` y la llave en los servicios que procesan ficheros

## Contexto

Jose, 2026-11-06: «necesito saber cómo podemos securizar al máximo ese storage; si nos hackean,
que los documentos no se puedan abrir». Hoy los ficheros de los documentos están en claro en el
bucket: Google cifra sus discos, pero descifra para cualquiera con permiso, y el permiso lo da
una sola cuenta (`fbsvc-clean`, `storage.admin`) cuya clave está en el servidor y que también
abre cualquiera de los cuatro propietarios del proyecto, todos con cuentas Gmail personales.

El diseño del 06-nov proponía **cifrado de sobre con la llave maestra en Cloud KMS**. Jose,
2026-11-11: «Cloud KMS mejor en los env o secrets del servidor por el momento, ya que no podemos
permitirnos más gastos».

## Decisión

1. **Cifrado de sobre por fichero.** Cada documento se cifra con su propia clave aleatoria
   (AES-256-GCM) antes de subirlo; en el bucket solo hay cifrado.
2. **La clave de cada fichero se guarda envuelta** (cifrada con la llave maestra, también
   AES-256-GCM) **en la cabecera del propio fichero**, nunca en claro. *Cambiado respecto al
   diseño del 06-nov, que la ponía en Firestore:* el inventario del 11-nov encontró que un mismo
   documento tiene hasta tres ficheros (original, preparado para firmar y firmado) y que la
   purga copia objetos tal cual a otra ruta. Con la clave dentro, cada objeto se basta solo, las
   copias no se rompen y no hay un segundo sitio que mantener al día.
3. **La llave maestra vive en el servidor, no en Cloud KMS.** Un fichero de secreto montado
   **solo en el contenedor de `documents`** (secreto de Docker Compose), no en el `.env`
   compartido: hoy todos los contenedores leen el mismo `.env.production`, y la llave no puede
   ser visible para todos.
4. **La llave lleva identificador** (`kekId`), y cada clave envuelta dice con cuál se envolvió.
   Así se puede cambiar de llave —o pasar a Cloud KMS el día que se pueda pagar— re-envolviendo
   las claves de los ficheros, **sin volver a cifrar ningún fichero**.
5. **Los ficheros solo se abren a través de `documents`.** Ninguna otra pieza descifra; quien
   necesite el contenido de un documento se lo pide a `documents`.
6. **Gasto cero.** Ni KMS, ni Secret Manager, ni servicios nuevos.

## Lo que protege y lo que no

Protege —y es lo que hoy está más expuesto—:

- un robo del bucket o de la clave de `fbsvc-clean` **fuera** del servidor (un portátil, una
  copia, un `.env` filtrado, un repositorio);
- que entre alguien por una de las **cuentas de propietario** del proyecto: ve el bucket, no la
  llave, que no está en Google;
- una exposición del bucket por mala configuración (público por error, enlace filtrado).

No protege:

- **quien tome el servidor**: tendrá la llave maestra y la cuenta de Storage a la vez. Con KMS
  tendría que, además, usar la llave desde dentro, dejando rastro y pudiendo cortarse en un
  segundo. Es la diferencia que se paga con KMS y que hoy se acepta no pagar.
- quien tome el propio servicio de `documents` mientras funciona (igual que con KMS).

## Consecuencias

- **Perder la llave maestra es perder todos los documentos.** La llave entra en la copia de
  seguridad del servidor (que ya va cifrada con la clave pública de copias) **y** se guarda una
  copia fuera del servidor, a mano y una sola vez, donde decida Jose. Sin esto no se activa.
- La descarga cambia por dentro, no por fuera: hoy el panel y la app reciben una URL firmada de
  Google y la abren; un fichero cifrado no se puede abrir así. Seguirán recibiendo `{url}`, pero
  la URL será de `documents` (firmada por él y de un minuto), que descifra y entrega. **Ni el
  panel ni la app cambian**, ni hay que publicar versión de la app.
- Todo lo que hoy lee, copia o sube ficheros de documentos fuera de `documents` (justificantes
  de gastos de `customers`, firma, hoja propia, purga del backoffice, adjuntos de tareas que
  apuntan al mismo fichero) se repasa y pasa a pedírselo a `documents`. Inventario en el TDR.
- Los documentos que ya existen se migran con un script que **simula por defecto** y solo actúa
  con `--apply`. Durante la transición conviven ficheros cifrados y en claro: cada documento
  dice si está cifrado.
- La salida del bucket de EE. UU. a Europa que proponía el diseño del 06-nov **no entra aquí**:
  es otra decisión, que se puede tomar en la misma migración más adelante.
- Pasar a Cloud KMS más adelante es un cambio de `kekId` y un re-envuelto de claves: el formato
  de los ficheros no cambia.

## Descartado

- **Cloud KMS**: el diseño original. Aplazado por coste (Jose, 11-nov), no descartado.
- **Llave en el `.env` compartido**: la verían todos los contenedores, y `docker inspect`.
- **Secret Manager de Google**: también cuesta, y pondría la llave en el mismo proyecto que el
  bucket, que es justo lo que se quiere separar.
- **Cifrado del lado del cliente (panel/app)**: el servidor necesita leer los PDF para firmarlos
  e incrustar la firma; y movería la llave a millones de dispositivos.
