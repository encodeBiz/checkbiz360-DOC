# ADR-003 — Un usuario de quiosco por sucursal, creado al activar el módulo; sólo entra a 200 m del centro y en un dispositivo a la vez; y es la misma app

**Fecha:** 2026-10-18 (sustituye, el mismo día, a la primera versión: «vinculación por código
de un solo uso, sin cuenta ni contraseña»)
**Estado:** Aceptada
**Decisionario:** Jose Acevedo

## Contexto

Jose, 2026-10-18, por la mañana: «que se instale en un terminal y, logándose con la cuenta del
usuario de la sucursal tipo quiosco, se pueda implementar sin problema». La primera versión de
este ADR lo cambió por un código de vinculación de un solo uso, para no tener una contraseña
en una tablet compartida. Por la tarde Jose lo cerró como lo había dicho, con dos condiciones
que resuelven precisamente lo que preocupaba de la contraseña: «el quiosco lleva consigo un
nuevo rol, quiosco, que se generaría de forma automática cuando se active el módulo, y al
logarte en la app con este usuario salta el quiosco automático; el quiosco sólo puede
activarse en la dirección de su sucursal con un radio bastante corto, 200 m o algo así, eso
es sumamente importante; y sólo puede estar en un dispositivo a la vez».

## Decisión

0. **El quiosco es un add-on de pago, como el inventario** (Jose, 2026-10-19). Contratarlo es
   activarlo: no hay interruptor aparte de la suscripción `kiosk`. Va en el bloque
   «Complementos» del menú del panel, junto a Inventario.
1. **Un usuario con rol `kiosk` por sucursal**, cuenta de Firebase Auth con correo no
   enrutable y contraseña generada, con claims `{ kind: "kiosk", entityId, branchId }`.
   **Lo crea el servidor al contratar el add-on** para cada sucursal con dirección, y para cada
   sucursal nueva con dirección mientras siga contratado. Nadie lo crea a mano. Las
   credenciales no se enseñan al crearlo: se generan desde el panel cuando se van a usar.
2. **Entrar con él en la app arranca el quiosco.** Es el login de siempre; el servidor
   reconoce el claim y devuelve una sesión de quiosco en vez de una de empleado. Sin 2FA ni
   dispositivo de confianza: lo sustituyen el radio y el dispositivo único.
3. **El dispositivo tiene que cumplir los requisitos, y si no, es «dispositivo no válido»:**
   ubicación encendida con permiso, una posición con precisión de 100 m o mejor, cámara
   frontal y sistema admitido. La app lo comprueba antes de entrar y enseña el motivo; el
   servidor lo vuelve a comprobar. **Sólo se activa a menos de 200 m de la dirección de la
   sucursal** (ajustable por sucursal entre 50 y 500 m). La tablet vuelve a comprobarlo al
   arrancar y una vez al día; si deja de cumplir o sale del radio, el quiosco se suspende y
   avisa. Una sucursal sin dirección no tiene quiosco.
4. **Un dispositivo a la vez.** Entrar desde otro sustituye al anterior, que se entera en su
   siguiente petición y vuelve al login; los administradores reciben el aviso.
5. **La misma app checkbiz360**, con el modo quiosco como una forma de entrar, no una
   segunda app en las tiendas.

## Razones

**Es lo que pidió quien decide, y el radio y el dispositivo único hacen inofensiva la
contraseña.** Lo que preocupaba de una contraseña en una pared era que, copiada, sirviera en
cualquier sitio. Con el radio, sólo sirve en el centro; con el dispositivo único, usarla
expulsa a la tablet y avisa; y el usuario de quiosco no abre el panel ni ningún dato: sólo
identifica y ficha. Lo que queda es una contraseña que se regenera en un clic desde el panel.

**Crear el usuario al activar el módulo quita el paso de «vincular».** No hay código que
acuñar ni pantalla de vinculación en el panel: activas el módulo, cada sucursal tiene su
quiosco, y en la tablet se entra como en cualquier app. Es el camino que menos pide al
cliente (dos toques para el supervisor, cero para el operario).

**El radio es la garantía de que el quiosco es del centro.** Un quiosco es un punto de
fichaje *en* la sucursal; si pudiera activarse en cualquier parte, sería un móvil con una
contraseña compartida. 200 m y no 50 porque una tablet wifi sin GPS se ubica por la red con
decenas de metros de error en interior: el radio protege contra llevárselo, no contra estar
en la otra punta del edificio. **Un fichaje nunca falla por la ubicación de la tablet**: se
marca y, si se repite, se suspende el quiosco; lo que se corta es el quiosco, no el fichaje
de la persona que está delante.

**Sustituir el dispositivo, no rechazarlo.** La tablet rota o perdida es el caso normal y no
debe exigir un paso en el panel. Quien sustituye ha tenido que estar en el centro con la
contraseña, y lo que gana es lo que ya podía hacer en la tablet; y el aviso llega al instante.

**La misma app, porque el quiosco es un modo de uso, no otro producto.** Comparte diseño,
l10n, cliente HTTP, lectura de errores de fichaje y el pipeline de releases. Si Google Play
exigiera algún día una app de dispositivo dedicado aparte para el aprovisionamiento a escala,
se abre un `main_kiosk.dart` sobre las mismas features; no antes.

**Salir del modo quiosco necesita a un administrador, no al trabajador.** Una pulsación larga y
el código de seis dígitos de un administrador de la entidad, comprobado en el servidor; o
cerrar la sesión del dispositivo desde el panel.

## Consecuencias

- `POST /auth/login` aprende el claim `kind: "kiosk"` y exige `geo` para esa clase de usuario.
  Es el único punto de auth que cambia.
- El panel gana «Activar módulo Quiosco» y, en cada sucursal, las credenciales, el dispositivo
  activo, el radio y «Cerrar sesión del dispositivo»; más lo que ya tenía (revisar, imprimir
  tarjetas, generar QR y código).
- La app pide ubicación en el login cuando el servidor dice que el usuario es de quiosco, y
  arranca en modo quiosco sin que la sesión de empleado ni `logoutInvalidationProvider`
  intervengan.
- Un usuario de quiosco nunca aparece en plantilla, informes ni facturación por asientos: no
  es un empleado. `countSource: checkinbiz.employees` no lo cuenta.
- La guía de cliente del quiosco dice, en una línea, que la tablet es del cliente, que tiene
  que llevar GPS y cámara frontal con la ubicación activada, que el PIN del sistema lo guarda
  el encargado y que la contraseña se regenera desde el panel. Una tablet que no cumple no es
  un caso que haya que soportar: es una tablet que no vale para esto.
