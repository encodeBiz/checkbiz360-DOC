# ADR-004 — Todos los ficheros de una empresa se cifran y se sirven con una sola pieza de `shared`

**Fecha:** 2026-11-14
**Estado:** Propuesta, pendiente de revisión de Jose
**Decisionario:** Jose Acevedo
**Enmienda:** [ADR-003](ADR-003-cifrado-de-documentos-con-llave-en-el-servidor.md), puntos 3 y 5
**Diseño:** [TDR-002 — ficheros de empresa con una sola pieza](../tdr/TDR-002-ficheros-de-empresa-una-sola-pieza.md)

## Contexto

El 14-nov, probando el cifrado del documental en staging (TDR-001), Jose subió una foto a una
tarea y salió en claro. Es lo previsto: TDR-001 solo cifra `documents/entities/…` y
`signatures/pending/…`. Pero la foto también enseñó algo peor. **Cada adjunto de tarea tiene un
enlace de descarga válido hasta 2050, que no pide sesión.** Ese enlace se guarda en Firestore,
la app y el panel lo leen tal cual, y viaja en el evento `task.resource_uploaded`.

Jose: «imagina que suban una ficha de datos médicos a una tarea». Y sobre cómo arreglarlo:
«no es que crucen módulos en servidores, sino que usen `shared`, porque si mañana cambia algo
de seguridad documental solo hay que cambiarlo en `shared`».

Hoy cada módulo procesa sus ficheros a su manera:

| Quién procesa | Qué | Cifrado | Enlace |
|---|---|---|---|
| `documents` | documental, firmados, hoja propia | sí (TDR-001) | propio, de minutos |
| `customers` → `documents` | contratos y justificantes de gasto | sí, vía `documents` | propio, de minutos |
| `tasks` | evidencias, adjuntos, incidencias, fotos de valoración | **no** | **Google, hasta 2050, sin sesión** |
| `inventory`, `documents` (vía `shared`) | evidencia JSON de las firmas (EPI y documentos) | no | se sirve con sesión (`reports`) |
| `reports` | actas, exportaciones | no | — |
| `checkinbiz` | fotos del quiosco | no | Google, 5 minutos, pedido cada vez |
| `entities` | marca (logos) | no; es pública por naturaleza | Google, hasta 2050 |

## Decisión

1. **Una sola pieza en `@encodebiz/shared` (`secureFiles`) hace todo el mecanismo de los
   ficheros de empresa:** guardar cifrado, leer descifrado, emitir el enlace corto y anotar quién
   descargó qué. Sale de `services/documents` (`DocumentCrypto`, la parte de cifrado de
   `DocumentStorageService` y el token de descarga) sin cambiar el formato `CBZE v1`.
2. **Cada módulo la usa directamente,** en su propio proceso, sin llamar a otro servicio para
   guardar o leer. **Los permisos siguen en cada módulo:** solo `tasks` sabe quién puede ver el
   adjunto de una tarea, y solo `inventory` sabe a quién se entregó un EPI. La pieza no decide
   quién puede ver: decide cómo se guarda y cómo se sirve.
3. **La llave maestra se monta en los servicios que procesan ficheros de empresa, y solo en
   ellos** (enmienda al punto 3 del ADR-003). Sigue siendo un secreto de Compose, nunca el `.env`
   compartido. Hoy los servicios serían `documents`, `tasks`, `inventory`, `reports` y, en su fase,
   `checkinbiz`.
4. **Una sola puerta de salida.** El enlace de descarga lo sirve siempre la misma ruta pública:
   `GET /api/v1/documents/files/<token>`, la de hoy. El token va firmado, lleva la ruta y la
   empresa, y caduca en minutos. Quien lo sirve solo comprueba la firma y descifra. Así hay una
   ruta en nginx, un registro de descargas y un sitio que vigilar.
5. **Se acaban los enlaces eternos.** Ningún fichero de empresa se guarda con su enlace. La app
   y el panel lo piden a la API al abrirlo.
6. **Leer antes de escribir.** Un cambio de formato se despliega primero, en todos los servicios
   que usan la pieza, como capaz de *leer* el formato nuevo. Solo después se empieza a *escribir*
   en él.
7. **Gasto cero**, igual que el ADR-003.

Los puntos 1, 2, 4, 6 y 7 del ADR-003 se mantienen. El punto 5 («solo `documents` descifra»)
pasa a decir: **solo la pieza `secureFiles` descifra, y solo en los servicios que tienen la
llave.**

## Por qué una librería y no un servicio central de ficheros

- **Los permisos.** Un servicio central tendría que fiarse de quien le llama o duplicar los
  permisos de todos los módulos. Con la librería, cada módulo comprueba lo suyo y luego usa el
  mismo mecanismo.
- **Sin punto único de fallo.** Si `documents` se cae, las tareas siguen subiendo evidencias.
- **Es lo que ya hace la firma.** `shared/checkbiz/signature` la usan `documents` e `inventory`,
  cada uno en su proceso.
- **La llave en un solo contenedor compra poca seguridad aquí.** Todos corren en la misma máquina
  con el mismo `.env`: quien entra en el servidor lo tiene todo igualmente. Lo que de verdad
  protege es el cifrado en reposo, que no haya enlaces eternos y que el acceso pida sesión, y las
  tres cosas se consiguen igual con la llave montada en cuatro o cinco contenedores.

## Lo que protege y lo que no

Igual que el ADR-003. Además, **mata los enlaces de 2050 que ya circulan.** Un enlace firmado de
Google no fija la versión del objeto: cuando se cifra en su sitio, el enlace sigue descargando,
pero solo algo ilegible. Es la única forma de revocarlos sin rotar la cuenta de servicio que los
firmó.

No protege más que el ADR-003 frente a quien tome el servidor. Amplía un poco lo que se expone si
alguien toma uno de los contenedores con llave: antes era uno, ahora son cuatro o cinco.

## Consecuencias

- **Un cambio en `shared/secureFiles` obliga a redesplegar todos los servicios que la usan,** no
  solo el que cambia. Choca a propósito con «desplegar solo lo que cambia» y queda escrito en la
  cabecera del módulo y en el pase. Quien olvide uno tendrá un servicio con la versión vieja: si se
  respeta «leer antes de escribir» lee igual, y si no, falla al abrir.
- **La app y el panel cambian para tareas:** dejan de usar el `url` guardado y piden el enlace al
  abrir. Hay que publicar versión de la app y hacerla obligatoria **antes** de cifrar lo que ya
  existe, o las fotos dejan de verse en los móviles con la versión vieja.
- El evento `task.resource_uploaded` deja de llevar un enlace eterno. Hay que revisar quién lo
  consume.
- Los documentos de hoy no cambian: mismo formato, misma llave, misma ruta de descarga.

## Descartado

- **Servicio central de ficheros** (que `tasks` e `inventory` le manden los ficheros a
  `documents` por HTTP, como hoy `customers`). Es lo que proponía TDR-001 §7 para los demás
  módulos. Descartado por los permisos y por el punto único de fallo. `customers` y `merlin`
  pueden quedarse como están o pasar a la pieza: el código es el mismo.
- **La llave en todos los contenedores**, o en el `.env` compartido: igual que en el ADR-003.
- **Cada módulo con su propia ruta de descarga:** multiplica las rutas públicas y los registros
  sin ganar nada, porque el token ya dice qué fichero es.
