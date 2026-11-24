# 10 — El cliente en la app: primera versión (fase dos)

**Fecha:** 2026-11-16, revisado el 2026-11-17, el 2026-11-20 y el 2026-11-21 con las respuestas de Jose
**Estado:** alcance fijado por Jose; falta el detalle técnico (ADR de la entrada y TDR, 26 y 27 de noviembre). Sin código. Sale en diciembre.
**Sustituye:** la forma de entrar de [07](./07_portal-del-cliente.md) y de [ADR-005](./adr/ADR-005-el-portal-del-cliente-es-el-add-on-como-el-quiosco.md), que era una web por enlace sin cuenta. Lo demás del 07 sigue valiendo como lista de ideas para después.

**Lo que fijó Jose:**

- El cliente entra en la app con un rol nuevo, como entra el punto de fichaje.
- Lleva tareas, documentación y contacto.
- **El cliente firma y valora la ejecución de la tarea, desde la primera versión.** Es necesario para administración y para los modelos que vendrán.
- Contacto funciona como hoy, con una etiqueta más: Clientes.
- Se cobra cada acceso activo al Área cliente, no el cliente: cada contacto al que administración le ha dado acceso, entre o no en la app.
- Precio: 0,75 € al mes por acceso activo, con un mínimo de 15 € (21-nov).
- (20-nov) Lo principal va siempre; el resto lo habilita el administrador para cada cliente: valorar, comentar, subir evidencias, subir documentación y otras. Subir documentación es también una forma de cobro, por el almacenamiento. Todo se configura en el módulo de pago, «Área cliente».

---

## Qué es

Un apartado de la app de CheckBiz360 para **el cliente de la empresa**: la presidenta de la comunidad, la familia de la persona atendida, la agencia que contrató el montaje. Entra con su correo y ve solo lo suyo: qué trabajos tiene, qué le ha compartido la empresa, y da su conformidad y su valoración a cada trabajo terminado.

Es de cara al cliente final, así que manda una regla sobre todas las demás: **no sale nada que la empresa no haya decidido enseñar.** Por defecto no se comparte ninguna foto ni ningún documento.

## Qué cambia respecto a lo escrito el 3 de noviembre

| | Diseño del 3-nov (07 y ADR-005) | Esta versión |
|---|---|---|
| Dónde entra | Una web para móvil, por enlace | La app, en un apartado propio |
| Quién es | Nadie: una sesión de enlace, sin cuenta | Una cuenta con el rol de cliente |
| Qué lleva de salida | Calendario, documentos con firma y partes | Tareas con firma y valoración, documentación y contacto |
| Cómo se cobra | Sin decidir | 0,75 € por acceso activo al Área cliente, mínimo 15 € |
| Add-on aparte, como el quiosco | Sí | Sí, no cambia |

## El rol de cliente

**Cómo entra el quiosco hoy**, que es el modelo: tiene una cuenta propia que no es de ningún empleado ni ocupa plaza de administración. Sus rutas van aparte del resto y en cada petición el servidor vuelve a mirar si sigue activo y si la empresa sigue suscrita. Por eso apagarlo corta el acceso en el acto.

**El cliente, igual:**

- Una cuenta por contacto del cliente, con su correo. No es empleado, no tiene plaza de propietario ni de administrador y no aparece en la plantilla.
- **Entra como todos** (Jose, 21-nov): la misma app y la misma pantalla de entrada que un empleado. Al cargar la sesión, el servidor dice que es una sesión de cliente (`customer`) y la app enseña su apartado en vez del de empleado. No hay enlace mágico ni código de un solo uso.
- El acceso es un registro propio: qué persona, de qué cliente y de qué empresa, y en qué estado. Ese registro manda, y se comprueba en cada petición.
- Sus rutas viven en `customers`, bajo `/api/v1/customers/portal/…`. El cliente nunca llama a tareas ni a documentos directamente: `customers` lee y escribe por él.

**Qué puede hacer:** leer lo suyo, firmar y valorar sus tareas terminadas y escribir a la empresa. No crea, no edita y no borra nada de la operativa.

**Qué no ve nunca:** costes, importes de contrato, márgenes, gastos, notas internas, notas de campo para el trabajador, datos de otros clientes ni datos personales del trabajador más allá del nombre.

### Cómo se activa y cómo se apaga

1. **Administración lo abre** en Área cliente: elige el cliente y marca cuáles de sus contactos tienen acceso a la app. Al contacto le llega la invitación por correo, como la bienvenida de un empleado, con la descarga de la app y cómo poner su contraseña.
2. **El acceso está activo desde que administración lo da**, entre o no el contacto en la app.
3. **Se apaga** cuando administración le retira el acceso o cuando se desactiva el cliente. En los dos casos queda fuera en la siguiente petición.

Cada acceso tiene uno de dos estados:

| Estado del acceso | Qué significa |
|---|---|
| Activo | Administración le ha dado acceso. Cuenta para el cobro, haya entrado o no |
| Retirado | Lo sacó administración o se desactivó el cliente. No cuenta |

En Área cliente se ve, como información, si el contacto ha entrado alguna vez. Sirve para que la empresa sepa a quién recordárselo; no cambia el cobro.

**Lo que se cobra es cada acceso activo**, no el cliente ni sus contactos de la cartera (Jose, 21-nov). Un cliente con diez contactos y uno solo con acceso cuenta 1; con tres accesos activos, cuenta 3.

### Tres cosas que hay que construir para que esto exista

- Los contactos del cliente son hoy una lista dentro de la ficha, sin identificador propio. Para dar acceso a una persona hay que poder señalarla.
- No existe ninguna credencial de «persona de fuera». Las rutas de `customers` solo conocen a quien entra por el panel y al empleado.
- El resto de servicios no rechaza de forma expresa a una cuenta que no sea de empleado: hoy la deja fuera solo que no tiene ficha. Con clientes dentro hay que poner el rechazo expreso.

## Lo que el administrador habilita para cada cliente

Jose, 20-nov: el administrador elige qué puede hacer cada cliente en la app. Lo principal va siempre; el resto lo enciende o lo apaga él, cliente a cliente. **Todo se configura en el módulo de pago, «Área cliente»**, no en la cartera, que es gratuita. Sin el add-on, el módulo no aparece.

**Siempre, sin opción**

| Qué | Por qué no se apaga |
|---|---|
| Ver sus tareas | Es para lo que entra |
| Ver la documentación que la empresa le comparte | Lo que no se comparte no sale igualmente |
| Contacto con la empresa | Es la vía para todo lo demás, incluida la queja |

**A elección del administrador**

| Opción | Qué hace el cliente | De salida |
|---|---|---|
| Firmar la conformidad | Firma el parte de cada tarea terminada | Encendida |
| Valorar la tarea | Nota de 1 a 5 y comentario opcional al firmar, o sola si la firma está apagada | Encendida |
| Comentar la tarea | Deja un comentario en una tarea, hecha o por hacer: «la llave está en conserjería». Llega a administración y queda en el historial de la tarea | Apagada |
| Subir evidencias a la tarea | Añade fotos a una tarea terminada: cómo lo encontró, lo que falta | Apagada |
| Subir documentación | Sube documentos a su propia documentación: facturas, certificados, planos, autorizaciones | Apagada |
| Ver las fotos de la tarea | Ve las evidencias que la empresa haya marcado para compartir | Encendida |
| Ver la hora exacta | Ve la hora de la visita; apagada, solo el día | Encendida |
| Ver quién va | Ve el nombre de quien hace la tarea | Encendida |
| Pedir un trabajo | Pide un trabajo extra desde la app. Llega a Contacto, etiqueta Clientes, como solicitud | Apagada |
| Descargar el parte del mes | Descarga su parte del mes cuando la empresa lo genera | Apagada |

**Cómo se aplica**

- Las opciones están en Área cliente, en el cliente, junto al acceso de sus contactos. Valen para todos los contactos de ese cliente.
- Al dar el primer acceso, el cliente arranca con las opciones de la tabla. Si una empresa quiere otros valores de partida para todos sus clientes, los pone en la configuración de Área cliente y los clientes nuevos los heredan. Cambiar los valores de partida no toca a los clientes que ya tienen los suyos.
- Apagar una opción no borra nada. Las firmas, notas, comentarios, fotos y documentos que ya subió se quedan; solo deja de poder hacerlo.
- Todo lo que sube el cliente llega a administración marcado como «del cliente» y no lo ve el trabajador hasta que administración lo comparta.

### Lo que sube el cliente cuenta como almacenamiento

Subir documentación y subir evidencias es, además de útil, otra forma de cobro: lo que sube el cliente ocupa espacio de la empresa, y el espacio ya se cobra a partir de 2 GB, a 0,25 € el GB al mes.

- **Las rutas llevan la empresa**, como pide la regla de almacenamiento. Los documentos van a la documentación del cliente, `documents/entities/{entityId}/customer/{customerId}/…`, que ya existe y ya se cuenta. Las fotos van a los recursos de la tarea, bajo la empresa. El contador de Storage lo suma solo; ningún código del portal suma por su cuenta.
- **Nunca bloquea.** Pasar de 2 GB cobra el exceso y la subida sigue.
- **Tope por fichero, el de la plataforma** (Jose, 21-nov: «alineado con la documentación»). Las evidencias que sube el cliente a la tarea llevan los topes de la tarea: el de foto y el de vídeo de su configuración (5 MB y 25 MB de salida). Los documentos que sube a su documentación llevan el del documental, 10 MB. No hay topes propios del portal.
- En Área cliente se ve cuánto ocupa lo que ha subido cada cliente. Así la empresa sabe qué cliente le llena el espacio.

## Lo que lleva la primera versión

### Tareas

- Las tareas de ese cliente, por lugar: las que vienen y las hechas.
- De cada una: día, lugar, de qué trata, estado y el nombre de quien va.
- De las hechas: cuándo empezó y terminó, y las fotos que la empresa haya marcado para compartir.
- Las canceladas se enseñan como canceladas, para que no parezca que se esconden.
- La empresa elige si enseña la hora o solo el día.
- Las lecturas salen de Postgres, donde la tarea ya lleva su cliente.

### Firma y valoración de la tarea

Cuando una tarea del cliente se termina, le aparece como **pendiente de su conformidad**. En un solo gesto la valora y la firma.

**Lo que hace el cliente**

- Ve lo que se hizo: quién, cuándo y las fotos compartidas.
- Valora de 1 a 5. El comentario es opcional.
- Firma con el dedo en la pantalla.
- Si no está conforme, lo dice en el mismo sitio y se abre un mensaje en Contacto, etiqueta Clientes, enlazado a la tarea. No hay botón de «rechazar» que deje la tarea en el aire.

**Lo que queda**

- Un parte de esa tarea en PDF, sellado con la firma electrónica que ya tiene la plataforma, con quién firmó, cuándo y desde qué dispositivo. Se guarda en la documentación del cliente y se ve desde la tarea.
- La valoración como dato, no como texto dentro del PDF: nota, comentario, tarea, cliente, lugar, personas que la hicieron y cuánto tardó el cliente en responder. Es lo que usarán administración y los modelos.
- En el historial de la tarea, igual en la app y en el panel: «conforme y valorada por el cliente».

**Reglas**

- **Nunca bloquea.** Una tarea sin firmar sigue terminada; solo queda marcada como pendiente de conformidad.
- Firma cualquier contacto activo del cliente. La primera firma cierra la tarea para todos.
- Una vez firmada no se cambia. Si el cliente quiere añadir algo, escribe por Contacto.
- Firma y valoración son dos opciones del cliente, encendidas de salida. Con la firma apagada y la valoración encendida, el cliente valora sin firmar; con las dos apagadas, la tarea no le pide nada.

**Lo que hay que construir**, porque hoy no existe:

- El parte de una sola tarea. Existe el parte del cliente por periodo; el de una tarea sale del mismo código.
- La firma a nombre de un cliente. Hoy la firma solo sabe firmar a nombre de un empleado.
- La tabla de valoraciones en Postgres, para el panel, los informes y los modelos.

### Documentación

- Los documentos del cliente que la empresa marque para compartir, uno a uno: contratos, certificados, seguros, el parte del mes.
- Los partes de tarea que el cliente ha firmado.
- Los de tipo administrativo no salen nunca, se marque lo que se marque.
- Cada apertura queda registrada, como con los empleados.

### Contacto

Funciona como el Contacto de hoy: un mensaje con su tipo, su estado y un hilo de respuestas.

- **En la app,** el cliente tiene su apartado Contacto: escribe, ve el estado y lee las respuestas. También ve el teléfono, el correo y el horario de la empresa.
- **En el panel,** Contacto gana una tercera pestaña. Hoy tiene Incidencias (lo que escribe el empleado) y Solicitudes (vacaciones y permisos); ahora también **Clientes**, con su contador de pendientes.
- Cada mensaje de cliente lleva el cliente, el lugar y, si viene de una tarea, la tarea.
- Responde administración. El cliente nunca habla con el trabajador directamente.

Una diferencia por dentro: el empleado escribe hoy sus incidencias directamente en la base de datos, y el cliente las mandará por el servidor, que es quien comprueba su acceso.

### En el panel, para la empresa: el módulo «Área cliente»

Es un módulo propio del menú, como Inventario: aparece cuando la empresa tiene el add-on y desaparece si se da de baja, sin borrar nada.

**Dentro del módulo**

- **Clientes con acceso:** la lista de clientes con sus accesos (activos o retirados, y si cada contacto ha entrado alguna vez), lo pendiente de firmar, su nota media y lo que ocupa lo que han subido. Se ve también lo que se cobra: cuántos accesos están activos este mes.
- **Cada cliente:**
  - sus contactos, para dar y retirar el acceso a la app;
  - sus opciones;
  - sus valoraciones;
  - lo que ha subido, marcado como suyo.
- **Configuración:** los valores de partida de las opciones para los clientes nuevos.

**Fuera del módulo, solo si la empresa tiene el add-on**

- En la documentación del cliente y en las fotos de la tarea, una casilla para compartir con el cliente. Apagada de salida.
- En la tarea: si está conforme, la nota y el parte firmado.
- En Contacto, la pestaña Clientes.
- En la ficha del cliente de la cartera, un enlace a ese cliente en Área cliente. La ficha no gana pestañas ni ajustes: la cartera sigue siendo la gratuita.

## Lo que se queda fuera de la primera versión

- Firmar otros documentos que no sean el parte de la tarea: contratos, presupuestos, parte del mes.
- Convertir en tarea, con un clic, el trabajo que pide el cliente. En la primera versión, administración lo lee en Contacto y crea la tarea como siempre.
- «Quién está ahora en mi edificio».
- Enseñar la valoración al trabajador. De salida la ve solo administración.
- Pagar, reservar cita y cualquier cosa de facturación.

Los avisos en el móvil no estaban en la primera lista, pero con la firma hacen falta al menos dos: «tienes un trabajo pendiente de conformidad» y «la empresa te ha respondido». Sin el primero, las firmas no llegan.

## Cómo se cobra

**Qué se cuenta: los accesos al Área cliente** (Jose, 21-nov: «lo que cobramos es el acceso a esa área cliente, no el cliente en sí»). Un acceso es un contacto al que administración le ha dado entrada. Cuenta desde que se da, entre o no el contacto en la app. Deja de contar cuando administración se lo retira o desactiva el cliente.

- **Los contactos del cliente no cuentan por estar en la cartera.** Un cliente con diez contactos en su ficha y uno solo con acceso al Área cliente cuenta 1.
- **Si administración da acceso a tres de esos contactos,** cuenta 3, aunque solo entre uno.

**Por mes completo** (Jose, 21-nov). Un acceso que ha estado activo en algún momento del mes cuenta ese mes entero, sin prorrateo. Si se retira, deja de contar a partir del mes siguiente.

- Activado el 28 de noviembre: cuenta noviembre entero.
- Retirado el 3 de diciembre: cuenta diciembre, porque estuvo activo tres días. En enero ya no cuenta.
- Activado y retirado dentro del mismo mes: cuenta ese mes.

Para el recuento: el número de contactos con acceso activo en algún momento del periodo de la factura. No es el número de clientes ni el de entradas. Por eso el registro de acceso guarda la fecha en que se dio y la fecha en que se retiró, no solo el estado de hoy. Es la misma idea que ya usa la plantilla, donde un empleado despedido sigue contando el mes en que fichó.

**Precio, confirmado por Jose el 21-nov:** **0,75 € al mes por acceso activo, con un mínimo de 15 €**, más IVA. Es lo mismo que «15 € con 20 accesos incluidos y 0,75 € por cada uno de más».

Antes estuvieron sobre la mesa 30 € con 60 incluidos y 15 € con 20 y 0,40 € de más. La segunda se descartó porque un acceso de más costaba casi la mitad que uno incluido: 0,40 € frente a 0,75 €.

| Accesos activos | Al mes |
|---|---|
| hasta 20 | 15,00 € |
| 60 | 45,00 € |
| 142 | 106,50 € |
| 300 | 225,00 € |
| 1.000 | 750,00 € |

- Se explica en una frase: 75 céntimos por cada persona que entra en el Área cliente. Ningún acceso cuesta menos que otro.
- En Stripe son dos tramos, como el quiosco: hasta 20, 15 € fijos; desde el 21, 0,75 € por acceso.
- La empresa decide cuánto paga: decide a cuántos contactos de cada cliente da acceso.
- Como cuenta todo acceso activo, dar acceso a la cartera entera se cobra entera. La empresa debe dar acceso a quien lo vaya a usar, y retirarlo a quien no.

**Lo demás, como el resto de add-ons**

- Se cuenta al preparar cada factura.
- 15 días de prueba.
- Pasarse de los incluidos no corta nada: se cobra el exceso y el servicio sigue.
- Sin add-on no hay accesos ni casillas de compartir. Darse de baja apaga la entrada y no borra nada: partes firmados, valoraciones y mensajes se quedan en el cliente.

## Piezas

- **API, `customers`:** identificador por contacto, el registro de acceso con sus dos estados, las fechas en que se dio y se retiró y la de la primera entrada, las opciones de cada cliente y sus valores de partida, la credencial de cliente, las rutas del portal (tareas, conformidad, comentarios, subidas, documentos, contacto) y la puerta de suscripción. Cada ruta comprueba su opción en el servidor: la app esconde el botón, pero quien manda es el servidor.
- **API, informes y firma:** el parte de una tarea y su sellado a nombre de un cliente.
- **API, resto:** casilla de compartir en la foto y en el documento; mensajes de cliente en Contacto; rechazo expreso de la cuenta de cliente fuera de sus rutas; el add-on en el cobro, con su recuento; la tabla de valoraciones.
- **Panel:** el módulo Área cliente (clientes con acceso, cada cliente con sus contactos, opciones, valoraciones y subidas, y la configuración), las casillas de compartir, conformidad y nota en la tarea, la pestaña Clientes en Contacto, el enlace desde la ficha y la contratación del add-on.
- **App:** la entrada distingue al cliente y le abre su apartado: tareas, conformidad con firma y nota, documentación y contacto, más los dos avisos.
- **Stripe:** precio por tramos en desarrollo. En producción, solo con Jose.

## Lo que puede mover la fecha

- **La firma y la valoración agrandan el trabajo**, sobre todo en la app y en la firma a nombre de un cliente. Con ellas dentro, dos semanas de desarrollo quedan justas. La estimación por pieza sale del TDR del 26 y 27 de noviembre, y ahí se sabe si cabe entero.
- **La app tiene que pasar por las tiendas.** Para salir la semana del 14 de diciembre, la versión tiene que estar enviada a revisión hacia el 11. Abrir la app a quien no es empleado puede traer alguna pregunta de la revisión.
- **Las fotos de las tareas** se guardan hoy con una dirección pública. Compartirlas con el cliente no lo empeora, pero es el mismo problema que resuelve la propuesta de ficheros seguros (ADR-004 de almacenamiento), que sigue sin revisar.

## Calendario

| Cuándo | Qué |
|---|---|
| 26 y 27 de noviembre | ADR de la entrada, TDR y estimación por pieza |
| 30 de noviembre a 11 de diciembre | Desarrollo: API y panel primero, app a la vez; staging |
| hacia el 11 de diciembre | App enviada a las tiendas |
| semana del 14 de diciembre | Pruebas y producción |

Si el proyecto de Hencok pide más tiempo, lo que se mueve a enero es esto.

## Lo que queda por decidir

Nada. Cerrado el 21-nov:

- el precio;
- la entrada: como todos, con sesión `customer`;
- las opciones de salida;
- el tope por fichero;
- la valoración: nota de 1 a 5 y comentario opcional, como estaba desde el principio.

Queda para el TDR, sin que Jose tenga que decidirlo: qué pasa cuando el correo de un contacto ya es de un empleado, o cuando la misma persona es cliente de dos empresas.
