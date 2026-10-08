# Firma electrónica del trabajador — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** checkinbiz — Firma (módulo propio, transversal)
**Fecha de inicio:** 2026-10-08
**Estado:** Idea anotada. Sin diseño detallado, sin código. Jose, 2026-10-08: «esto es otro
módulo, así que déjalo documentado y terminemos con lo de Inventario ahora».
**Autor:** Jose Acevedo

---

## De dónde sale

Diseñando la entrega de EPIs del inventario ([inventario/07 §4.5](../inventario/07_operables-documentos-y-entregas.md))
se vio que la forma de confirmar con huella no es del inventario: es la misma que haría falta
para que un trabajador firme el recibí de una **nómina** o el enterado de una **amonestación**.
Jose: «tenemos alternativas, porque esto puede también usarse para firmar documentos».

## Qué es

Una capacidad de la plataforma, construida una vez, que cualquier módulo usa: **el trabajador
firma desde su móvil lo que se le pone delante, y el servidor puede comprobar esa firma.**

- **Nivel 1, verificable:** la huella o la cara desbloquean una clave creada en el chip seguro
  del móvil (Secure Enclave en iOS, Keystore/StrongBox en Android); con ella la app firma un
  reto del servidor y el servidor comprueba la firma con la clave pública registrada al activar.
  En Flutter, `biometric_signature`; la app ya lleva `local_auth`, que solo devuelve sí/no.
- **Nivel 2:** sin biometría pero con bloqueo de pantalla, el PIN o patrón del móvil.
- **Nivel 3:** sin bloqueo de pantalla, la contraseña de la cuenta, pedida otra vez justo antes.

El servidor guarda siempre uid, hora, dispositivo, qué nivel fue y si la firma se verificó.

## Lo que un documento exige y una entrega no

- **Atar la firma al contenido**: se firma el hash del fichero (y su versión), para poder
  demostrar qué se firmó y que no cambió después.
- **«No conforme»**: en una amonestación el trabajador puede firmar que la ha recibido sin
  estar de acuerdo. Es un resultado propio, no un rechazo.
- **Acta de firma**: un PDF por documento con quién, cuándo, desde qué móvil, cómo (nivel) y el
  hash firmado, para enseñarlo a quien lo pida.

## Dónde encaja

En el servicio documental, donde ya viven los acuses de recibo (`requiresAcknowledgement`),
subiendo el acuse de «pulsó sí» a «firmó». Claves por empleado y por móvil
(`POST /employees/me/devices`), reto de un solo uso y comprobación en el servidor. Los
consumidores previstos: nóminas y amonestaciones (documental), entrega de EPIs (inventario,
Fase 6).

## Valor legal, con cuidado

Una firma con clave en el chip seguro, vinculada al trabajador y a su móvil, bajo su control y
atada al documento, tiene los ingredientes de la **firma electrónica avanzada** del reglamento
eIDAS. **No** es una firma cualificada, que exige un certificado de un prestador reconocido; si
un cliente la necesita, es otra pieza con un prestador detrás. Lo que diga un juez o un
inspector depende del caso y de la normativa aplicable, no de la herramienta.

## Qué queda por hacer cuando toque

Diseño detallado (modelo, contratos, acta), ADR de la decisión «firma avanzada propia, no
cualificada», prueba de `biometric_signature` en móviles reales de gama baja, y el ajuste por
empresa para exigir el nivel 1.
