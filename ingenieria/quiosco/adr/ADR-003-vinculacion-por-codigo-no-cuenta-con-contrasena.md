# ADR-003 — La tablet se vincula a la sucursal con un código de un solo uso, no con una cuenta y contraseña; y es la misma app

**Fecha:** 2026-10-18
**Estado:** Aceptada
**Decisionario:** Jose Acevedo

## Contexto

Jose, 2026-10-18: «que se instale en un terminal y, logándose con la cuenta del usuario de la
sucursal tipo quiosco, se pueda implementar sin problema». La idea natural es una cuenta por
sucursal con la que se entra en la tablet. Hay que decidir qué credencial vive en un
dispositivo compartido, colgado en una pared, y si el quiosco es la app checkbiz360 o una app
aparte.

## Decisión

**Vinculación por código de un solo uso, generado en el panel para una sucursal, que deja en la
tablet un token de quiosco revocable desde el panel. Sin contraseña en la tablet.** Y **la misma
app checkbiz360**, con un modo quiosco que se activa al vincular, no una segunda app en las
tiendas.

## Razones

**Una contraseña en una pared acaba en un post-it, y abre más de lo que debe.** Una cuenta de
empleado o de panel da acceso a lo que esa cuenta puede ver (fichajes, documentos, plantilla).
El token de quiosco sólo puede hacer dos cosas, identificar un código y fichar, y sólo en esa
sucursal. Si la tablet desaparece, se desvincula desde el panel y el token muere en la
siguiente petición; con una contraseña habría que cambiarla y reconfigurar las demás tablets.

**El código de un solo uso es el patrón que ya usa la plataforma.** El `customToken` del
empleado y el código de vinculación del colaborador funcionan así: el panel acuña algo que
caduca, el dispositivo lo canjea una vez, y queda una credencial propia del dispositivo. El
quiosco repite el patrón con un `kind: "kiosk"` en el JWT y un documento `kiosks/{kioskId}` que
es la fuente de verdad sobre si sigue vivo.

**La cuenta de empleado es de una persona; el quiosco no es nadie.** Entrar con un empleado
«quiosco» de la sucursal habría exigido darle responsabilidad, calendario y dispositivo de
confianza, y el fichaje saldría con la firma de ese falso empleado (`updateBy`). Con el actor
`kiosk`, el fichaje es de la persona que tecleó su código y el rastro dice en qué tablet.

**La misma app, porque el quiosco es un modo de uso, no otro producto.** Comparte diseño,
l10n, cliente HTTP, lectura de errores de fichaje y el pipeline de releases. Una segunda app
duplica tiendas, firmas, versiones y revisiones; y el modo quiosco no necesita nada que la app
no pueda llevar (un token en almacenamiento seguro, `kiosk_mode`, `wakelock_plus`). Si Google
Play exigiera algún día una app de dispositivo dedicado aparte para el aprovisionamiento a
escala, se abre un `main_kiosk.dart` sobre las mismas features; no antes.

**Salir del modo quiosco necesita a un administrador, no al trabajador.** Una pulsación larga y
el código de seis dígitos de un administrador de la entidad, comprobado en el servidor. El
encargado sale con eso o con el PIN del sistema; nadie más.

## Consecuencias

- El panel gana «Quiosco» dentro de la sucursal (vincular, listar, desvincular, imprimir tarjetas
  QR) y «Generar QR» y «Generar código de quiosco» en la ficha del empleado y en lote.
- La app arranca en modo quiosco si hay token; nada de la sesión de empleado interviene, y
  `logoutInvalidationProvider` no tiene que saber del quiosco.
- Token de un año, comprobado contra `kiosks/{kioskId}.status` en cada petición: revocar es
  inmediato aunque el JWT siga siendo válido.
- La guía de cliente del quiosco tiene que decir, en una línea, que la tablet es del cliente,
  que el PIN del sistema lo guarda el encargado y que desvincular se hace desde el panel.
