# ADR-001 — El quiosco no lleva biometría, ni en la tablet ni en el servidor

**Fecha:** 2026-10-18
**Estado:** Aceptada
**Decisionario:** Jose Acevedo

## Contexto

Serlimar pide un quiosco para quien no quiera fichar con su móvil, y la primera idea fue que
«debe ser biométrico». Jose, 2026-10-18: «esto puede ser un problema ya que hay que enlazar la
biometría de los empleados y eso ya es GDPR gordas, o si tienes otra vía menos agresiva y
sencilla, genial».

La AEPD cerró la cuestión en noviembre de 2023 con su guía sobre control de presencia
biométrico, leída entera para esta decisión. Lo que dice, en lo que nos toca:

- Fichar con huella o cara es tratar **categorías especiales** y es **alto riesgo**: hay que
  levantar la prohibición del art. 9 y hacer una **EIPD antes** de empezar.
- En lo laboral, **el consentimiento no vale** y **el Estatuto de los Trabajadores no basta**:
  hace falta ley específica o convenio que regule ese uso concreto.
- El responsable «debe justificar que el empleo de otros sistemas existentes como tarjetas,
  certificados, claves, sistemas contact-less, etc. que evitan el tratamiento de categorías
  especiales de datos no son adecuados». Si hay alternativa para todos, la biometría «deja de ser
  necesaria» y falla el art. 5.1.c.
- Primera sanción tras la guía: 365.000 € por fichar con biometría. Iberia la retiró y puso
  tarjetas.

## Decisión

**El quiosco identifica con un código personal, y después con tarjeta NFC o con el móvil de la
persona. Nunca con huella ni cara en la tablet, y nunca con plantillas biométricas en la
plataforma.** La foto opcional de la Fase 2 es una imagen que mira un humano; no se le aplica
reconocimiento de ningún tipo, ni ahora ni en una versión futura.

## Razones

**Es la alternativa que la propia AEPD usa como vara.** Un código o una tarjeta es exactamente lo
que la guía pone como «otros sistemas existentes» que hay que haber descartado para justificar
biometría. Si nosotros los ofrecemos, ningún cliente puede justificarla con nuestro producto,
y nosotros no tendríamos por qué querer que lo hiciera.

**Lo que venderíamos con huella no es un quiosco: es una EIPD, un convenio y una multa en
potencia.** Serlimar tiene 42 nacionalidades y 1.000 personas sin terminal de empresa; su
problema es que la gente fiche, no demostrar ante la AEPD que la huella era imprescindible.

**Ya tenemos la única biometría que no es nuestra.** La clave de firma del módulo
[firma](../../firma/README.md) se desbloquea con la huella o la cara **del móvil de la
persona**: la plataforma recibe una firma, nunca la huella. Es la misma relación que tiene la
empresa con el PIN del móvil de su trabajador: ninguna. Quien quiera biometría la tiene ahí,
bajo su control, y el servidor lo puede comprobar ([ADR-002](./ADR-002-la-llave-es-la-clave-de-firma-no-una-passkey.md)).

**Una tablet compartida no sabe de biometría multiusuario.** Android y iOS atan el sensor al
dueño del dispositivo; un quiosco con cien personas necesitaría un lector externo y una base de
plantillas nuestra. Eso es exactamente el tratamiento que la guía describe, y además una pieza
de hardware que no controlamos.

**La foto no es biometría mientras no la mire una máquina.** El considerando 51 del RGPD, citado
en la guía, deja fuera de categoría especial las fotografías no tratadas «con medios técnicos
específicos» para identificar. Por eso la Fase 2 puede ofrecer foto como disuasión, con
retención corta e información a la plantilla, y por eso **queda prohibido** añadirle
reconocimiento después: convertiría todo el diseño en lo que esta decisión evita.

## Adenda 2026-10-20 — detectar que hay una cara no es biometría

Jose pidió que la tablet compruebe, si se puede, que en la foto hay una persona. Se hace con la
**detección de caras** de ML Kit en el propio dispositivo: responde «hay una cara en el
encuadre» o «no la hay», y nada más. No calcula ninguna plantilla, no compara con nadie, no
identifica, y nada de eso sale de la tablet; lo único que viaja es `faceDetected: true/false`
junto a la foto, que ya se enviaba. Eso no es un tratamiento biométrico (no sirve para
identificar a una persona física, RGPD art. 4.14 y art. 9) y esta decisión sigue en pie: **se
comprueba que hay una cara, nunca de quién es.** Sin cara no se impide fichar: se marca para
la revisión, y el aviso de la pantalla dice que sin cara el fichaje se puede invalidar.

Va **sólo en Android** (donde va el quiosco), en el código nativo de la app (`MainActivity`,
ML Kit vía Google Play Services, que baja el modelo al instalar). El plugin de Flutter de ML
Kit exige CocoaPods y el iOS de la app está en Swift Package Manager; en iOS la app responde
«no se pudo comprobar» (`faceDetected: null`) y el fichaje sale sin marca.

## Consecuencias

- Sin biometría, la prueba de que fichó quien dice es **una foto en cada fichaje, mirada por
  un humano** (README §5 bis): cámara en vivo al pulsar, ráfagas detectadas en el servidor y
  revisión en el panel. Es Fase 1 y viene encendida; un código o una tarjeta sin foto es el
  caso del ayuntamiento en el que una persona pasaba todas las tarjetas. Lo que no hay es una
  máquina que identifique sola: eso es exactamente lo que esta decisión cierra. Es el precio de
  no tratar biometría, y la AEPD ya ha decidido que se paga; ella misma prefiere la
  intervención humana a los medios exclusivamente tecnológicos.
- Ningún ajuste por empresa, ningún add-on y ninguna petición de cliente reabre esto. Si un
  cliente exige huella en la pared, la respuesta es la guía de la AEPD y este documento.
- `employee.biometricRequired` (hoy sólo lo devuelve `/auth/validate`) se refiere a la
  biometría del móvil propio para abrir la app. No significa, y no significará, biometría en
  el quiosco.
