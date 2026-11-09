# Hoja informativa de protección de datos, firmada desde la app

**Abierto:** 2026-11-04 · **Estado:** diseño cerrado con las decisiones de Jose (abajo); sin código todavía.
**De dónde sale:** la carta de un alumno de FP Dual a un cliente (2026-11-04) y el paso 4 del
correo de alta: la empresa tiene que informar a cada trabajador antes de que fiche y guardar
la prueba. Hoy le damos el texto (Anexo IV del contrato de encargo) y nada más. Jose: «que
firmen el anexo desde la propia app».

## Qué es

La hoja informativa es el texto que la empresa entrega a cada trabajador antes de que use
CheckBiz360: quién trata sus datos, para qué, qué datos, cuánto tiempo, sus derechos. Es el
Anexo IV del contrato de encargo, rellenado con los datos de la empresa y del trabajador. El
trabajador la recibe en la app como recibe hoy una nómina, la lee y firma **«He recibido esta
información»**.

**Cómo se llama y cómo no.** Se llama «hoja informativa» y lo que el trabajador firma es un
enterado. Nunca «consentimiento»: el consentimiento no es la base legal del registro de jornada
y, si lo llamáramos así, el trabajador podría retirarlo y dejaríamos a la empresa peor que sin
nada. Esto vale para los textos del panel, de la app, del correo y del PDF.

## Lo que se reutiliza (y no se construye)

- **El documental** ya crea documentos dirigidos a un empleado, con acuse obligatorio
  (`requiresAcknowledgement`, `acknowledgementMode: single_employee`), avisa a la app y guarda
  quién acusó, cuándo y cómo.
- **La firma** ya existe: la app firma con la clave del móvil, dentro del PDF (PAdES) cuando
  hay clave con certificado, o como acuse firmado; queda el acta y el PDF firmado descargable
  desde la ficha del documento en el panel.
- **La generación de PDF** en el servidor ya existe (actas, informes).
- **El Anexo IV** ya está escrito, por funciones, y es la fuente del texto.

La app **no cambia**: el documento le llega como cualquier otro para firmar.

## El flujo

### 1. La empresa completa sus datos (una vez)

En Entidad → Protección de datos, tres cosas que la plantilla necesita y que no sabemos:

- Persona de contacto para protección de datos: nombre y correo (por defecto, el dueño).
- Cómo se ficha en cada centro: con la app en el móvil, en el punto de fichaje, o las dos. Si
  el centro tiene un punto de fichaje activo, por defecto «las dos».
- Un párrafo libre opcional (por ejemplo, la referencia a su convenio).

Los demás datos salen solos: razón social, NIF y domicilio de la ficha de la empresa; las
funciones activadas (tareas, punto de fichaje con foto, análisis operativo) de la
configuración; el plazo de las fotos del punto de fichaje, del ajuste del quiosco.

Mientras esto no esté completo, la casilla del alta aparece deshabilitada, en naranja, con el
texto «Completa los datos de protección de datos de la empresa para poder enviar la hoja
informativa» y el enlace a la pantalla. No se bloquea el alta.

### 2. La casilla en el alta de un empleado

En el formulario de alta (y en la alta masiva por plantilla y por el asistente, a nivel de
lote), una casilla **marcada por defecto**, que se puede desmarcar, **en naranja** mientras está
marcada:

> ☑ **Enviar la hoja informativa de protección de datos para que la firme desde la app.**
> La ley obliga a informar a cada persona antes de que fiche por primera vez y a guardar la
> prueba. Con esta casilla, la hoja se genera con los datos de tu empresa, le llega a la app
> y, cuando la firme, tendrás la prueba en su ficha.

Si la desmarca, el texto de debajo pasa a **rojo**:

> Sin la hoja firmada, tu empresa tiene que informar a esta persona por otro medio y guardar la
> prueba de haberlo hecho. Podrás enviarla más tarde desde su ficha.

Al guardar el alta con la casilla marcada, el envío es **automático**: se genera el PDF, se
crea el documento y la app avisa al trabajador. No hay un segundo paso.

Naranja y no rojo mientras está marcada: el rojo del panel ya significa «algo está mal», y
aquí no hay nada mal; la casilla señala una obligación que importa. El rojo se reserva para
cuando la empresa la desmarca, que es cuando asume algo que la deja al descubierto.

### 3. Lo que recibe el trabajador

Un documento en la app, en Documentos, con aviso, titulado «Hoja informativa de protección de
datos», y un texto previo en la propia app antes de abrirlo:

> Tu empresa está obligada a explicarte cómo se tratan tus datos al fichar con CheckBiz360.
> Léelo y firma que lo has recibido. **Firmar no es dar tu consentimiento ni renunciar a
> nada**: es dejar constancia de que te lo han explicado. Tus derechos están dentro del
> documento.

El PDF lleva la versión del texto, la fecha, los datos de la empresa y el nombre del
trabajador, y los apartados de las funciones que la empresa tiene activadas (tareas, foto al
fichar, indicadores), en el idioma del trabajador (ES, EN, PT; los demás en inglés).

Firmar es el **acuse firmado** de siempre (la app firma el acuse con la clave del móvil; si no
hay clave, el acuse pulsado). No hace falta la firma dentro del PDF. **Ni se avisa ni se
impide nada** a quien no firma: informar a la plantilla es obligación de la empresa; la
plataforma solo se lo facilita y le guarda la prueba.

### 4. Lo que ve la empresa

- En la **lista de empleados**, una columna «Hoja informativa» informativa, sin colores de
  alarma: *firmada el dd/mm*, *enviada el dd/mm* o vacía. Es información para la empresa, no
  un aviso: lo que haga con ella es suyo.
- En la **ficha del empleado**, el documento y el acta del acuse, como con cualquier documento.
- **Envío manual, sin subir nada:** en el selector de tipo del modal de subir documentos, un
  tipo «Hoja informativa de protección de datos». Al elegirlo, el campo del fichero desaparece y
  el texto dice que se enviará la hoja de la plataforma con los datos de la empresa. Sirve para
  una persona o para varias (el modal ya permite elegir destinatarios), y es la forma de
  mandarla a la plantilla que ya existía.
- Un **informe exportable** (CSV) con el estado por persona, para enseñarlo a una inspección.

### 5. Cuando cambia el texto

La hoja lleva la versión del Anexo IV y la fecha. Si el texto cambia, no se avisa ni se
reenvía nada: la empresa puede volver a mandarla desde el modal de documentos cuando quiera, y
la lista muestra la fecha de la última firmada.

## Lo que hay que construir

**Servicio documental (servidor):**

- La plantilla de la hoja, en el servicio, generada desde el Anexo IV publicado, con bloques
  por función y por idioma.
- `POST /documents/data-protection-notice` con `employeeIds` (dueño o administrador): genera
  el PDF por persona, lo guarda bajo `entities/{entityId}/…` (así cuenta en el almacenamiento
  de la empresa, como todo fichero suyo), crea el documento dirigido a esa persona con acuse
  obligatorio y avisa. Devuelve creados y omitidos (ya tenía esa versión).
- Un resumen por empleado (`dataProtectionNotice: {version, documentId, sentAt, signedAt}`)
  que el servidor actualiza al crear el documento y al registrar el acuse, para que la lista
  del panel no tenga que cruzar documentos.
- Un tipo de documento propio, «hoja informativa de protección de datos», que el modal de
  subida ofrece sin fichero: al crearse con ese tipo, el servidor genera el PDF él mismo.

**Panel:**

- Pantalla Entidad → Protección de datos (§1).
- Casilla en el alta individual, en la alta por plantilla y en la confirmación del asistente
  (§2); llamada automática al servicio al guardar.
- El tipo nuevo en el modal de subir documentos, sin campo de fichero (§4).
- Columna en la lista de empleados y exportación (§4).

**App:** nada. **Correo de alta a la empresa:** el paso 4 pasa a decir que la hoja se envía
desde el panel al dar de alta a cada persona.

## Decisiones ya tomadas por Jose (2026-11-04)

- Envío automático al guardar si la casilla está marcada.
- Casilla marcada por defecto y desmarcable.
- Naranja mientras está marcada; rojo solo al desmarcarla.
- Explicar bien el porqué a los dos lados: a la empresa en la casilla, al trabajador en la
  app antes de abrir el documento.

## Decisiones de Jose sobre las preguntas abiertas (2026-11-04)

1. **Con el acuse firmado basta.** No se exige la firma dentro del PDF.
2. **Dos caminos de envío:** automático al crear el empleado (casilla), y manual eligiendo el
   tipo en el selector del modal de documentos, que manda la hoja de la plataforma sin subir
   ningún fichero. Quien pueda subir documentos a una persona puede enviarle la hoja.
3. **Usuarios del panel sin ficha de empleado: no.**
4. **Ni se avisa ni se impide** a quien no firma. Es cosa de la empresa; la plataforma lo
   facilita y guarda la prueba.

   **Cambia el 2026-11-06 hacia la empresa** (Jose: «si no tienen un documento de tipo Hoja
   informativa de protección de datos debe saltar alarma»). Al trabajador sigue sin llegarle
   nada ni se le impide fichar; a owner y admin, la alerta `notice_unsigned` en rojo en la
   portada y en el resumen de la mañana. Ver alertas-por-correo §1.

## Fuera de alcance

La aceptación del contrato de encargo por la empresa (ya se hace con la casilla del panel) y
cualquier «consentimiento».
