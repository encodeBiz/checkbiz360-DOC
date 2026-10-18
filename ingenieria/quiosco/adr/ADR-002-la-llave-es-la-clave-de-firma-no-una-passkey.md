# ADR-002 — Si el móvil propio es la llave del quiosco, la llave es la clave de firma que ya existe, no una passkey WebAuthn

**Fecha:** 2026-10-18
**Estado:** Aceptada
**Decisionario:** Jose Acevedo

## Contexto

Jose, 2026-10-18: «¿podemos hacer un passkey en el móvil, por ejemplo? No lo sé, hay que
investigarlo bien». La pregunta es cómo, con biometría en el móvil de la persona y no en la
plataforma, el quiosco puede dar por buena una identidad.

Hay dos caminos:

1. **Passkeys (WebAuthn/FIDO2) con transporte híbrido**: la tablet, como *relying party*,
   enseña un QR; el móvil lo lee, comprueba proximidad por Bluetooth y firma con la passkey
   guardada en iCloud Keychain o Google Password Manager.
2. **La clave de firma que ya tenemos** ([firma/README](../../firma/README.md)): ECDSA P-256 en
   el chip seguro del móvil, una por empleado y móvil, registrada en el servidor en el login,
   desbloqueada con huella, cara o PIN del móvil; el servidor emite retos de un solo uso y
   verifica la firma, deja evidencia y acta. Probada en staging, 27 casos de QA en verde.

## Decisión

**La llave es la clave de firma existente.** El quiosco, cuando llegue la Fase 3, enseña un QR
con un `nonce` que rota; la app lo lee, pide un reto con `purpose: "checklog.kiosk"`, firma el
`payload` con la clave del chip y manda `{ challengeId, signature }`. No se implementa WebAuthn.

## Razones

**Ya está hecho y verificado, con evidencia que un tercero puede comprobar.** Registro, reto,
verificación, evidencia en Storage, acta en PDF y comprobación con OpenSSL existen y corren en
el CI. Para el quiosco es un `purpose` más y un lector de QR en la app. Una passkey obligaría a
montar un *relying party* WebAuthn (origen web, `rpId`, ceremonias de registro y
autenticación) para llegar al mismo sitio.

**Una passkey no está atada al móvil; nuestra clave sí.** Las passkeys de plataforma se
sincronizan entre dispositivos de la misma cuenta de Apple o Google: la «huella» que firma
puede estar en cualquiera de ellos, y el acta ya no podría decir «desde este móvil». La clave
del chip no sale del aparato y el servidor sabe de qué `deviceId` es.

**La proximidad por Bluetooth no compensa lo que cuesta.** Es lo único que WebAuthn añade. Pero
el quiosco está en el centro y el reto lleva `kioskId`, `branchId` y un `nonce` de 30 s: para
fichar desde fuera habría que tener delante la pantalla de la tablet en ese medio minuto, que
es estar en el centro. Y la app ya comprueba su propia ubicación cuando ficha.

**En una tablet Flutter en modo quiosco, el cliente WebAuthn híbrido no existe.** El transporte
híbrido lo arranca el navegador o el Credential Manager de la plataforma, con su interfaz; en
nuestra app sería rodear al sistema para hacer lo que ya hacemos con un reto propio. Los datos
de conversión que publican los proveedores de passkeys para el flujo QR entre dispositivos
tampoco animan (menos de un tercio de usuarios lo completa en Android, según un proveedor).

**No resuelve la objeción de Serlimar.** Quien no quiere la app en su móvil no va a sacar el
móvil delante de la tablet. Por eso esto es Fase 3 y el código personal es Fase 1
([README §7](../README.md#7-fase-3-el-móvil-propio-como-llave-en-el-quiosco-adr-002)).

## Consecuencias

- Hace falta un lector de QR en la app (`mobile_scanner`) y permiso de cámara, sólo para
  «Fichar en el quiosco». Nada más cambia en el móvil.
- El servidor añade el `purpose` `checklog.kiosk` a los que sabe emitir y la ruta
  `POST /checklogs/kiosk-signed`. `verifySignedChallenge` no cambia.
- El fichaje firmado lleva `identification: "device_signature"` y la misma evidencia que un
  acuse de nómina: es el fichaje con más prueba de toda la plataforma, y lo hace la persona que
  más fácil lo tenía.
- Si algún día un cliente exige FIDO certificado, es otra pieza con otro alcance, no una
  evolución de esta.
