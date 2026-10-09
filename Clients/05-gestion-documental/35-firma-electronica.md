# Acuse de recibo y firma electrónica

Un documento puede pedir que el empleado confirme que lo ha recibido. Esa confirmación se hace desde la app y, desde octubre de 2026, **se firma con el móvil**: el empleado la confirma con su huella, su cara o el código de desbloqueo, y la plataforma guarda una firma electrónica que se puede comprobar fuera de CheckBiz360. Para los documentos dirigidos a una sola persona, como una nómina o una amonestación, la firma **queda dentro del propio PDF**.

---

## Qué ve el empleado

Cuando un documento pide acuse de recibo, el empleado lo abre en la app, lo lee y pulsa **Confirmar**. La app le pide la huella o la cara; si su móvil no tiene biometría, el código de desbloqueo; y si no tiene bloqueo de pantalla, la contraseña de su cuenta. No tiene que dibujar nada ni instalar nada.

Si el documento es un PDF dirigido solo a él, al confirmar recibe el **PDF firmado**, que sustituye al anterior en su lista. Lleva en el margen inferior de cada página, en letra pequeña, quién firmó, cuándo y las referencias para comprobarlo.

> **Nota:** si el empleado cierra el documento sin confirmar, sigue en su lista de pendientes.

## Qué ve la empresa

En la ficha del documento, en el apartado de acuse de recibo, cada confirmación dice cómo se hizo:

| Marca | Qué significa |
|---|---|
| **Firmada y verificada (huella o cara)** | el empleado confirmó con biometría y la plataforma comprobó la firma con la clave de su móvil |
| **Firmada y verificada (desbloqueo del móvil)** | igual, con el código, patrón o PIN del móvil |
| **Confirmada con contraseña** | el móvil no tiene bloqueo de pantalla; confirmó volviendo a escribir su contraseña |
| **Confirmada pulsando** | confirmaciones anteriores a la firma, o desde una app sin actualizar |

Junto a cada confirmación firmada hay **Descargar el acta de firma**: un PDF de una página con quién firmó, cuándo, desde qué móvil, qué documento y en qué versión, la firma, la clave con la que se comprobó y las instrucciones para repetir la comprobación con una herramienta estándar. Es lo que se entrega a una inspección o a un perito.

Si el documento era un PDF para una sola persona, la descarga del documento entrega ya el **PDF firmado**. El original se conserva en la plataforma.

## Qué documentos se firman dentro del PDF

Solo los que van dirigidos a **un único empleado**: nóminas, amonestaciones, comunicaciones individuales. Un documento para toda una sucursal o para toda la empresa, por ejemplo una política interna, lo confirman muchas personas: cada confirmación queda firmada y con su acta, pero el fichero no se modifica. Lo mismo pasa con un documento que no sea PDF.

## Qué vale esta firma

Es una **firma electrónica avanzada** según el Reglamento eIDAS: está vinculada al firmante, bajo su control y atada al contenido exacto que firmó. No es una firma cualificada, que requiere un certificado emitido por un prestador reconocido; si un trámite la exige, use un servicio externo.

Dos cosas que debe hacer la empresa para que la firma tenga pleno valor:

- **Recoger el consentimiento del trabajador.** Para que confirmar con la huella valga como su firma, el empleado tiene que haber aceptado ese medio. Es responsabilidad de la empresa, no de la plataforma; cómo hacerlo con la propia plataforma, en el apartado siguiente.
- **Instalar el certificado de CheckBiz360**, si quiere que los lectores de PDF muestren la firma en verde. Sin instalarlo, el lector dirá que la firma es válida pero de confianza desconocida; la comprobación es la misma. El certificado se descarga en el backoffice, en la ficha de la empresa, pestaña **Entorno de trabajo**, apartado **Firma electrónica**, donde están también los pasos para instalarlo en Acrobat Reader.

## Comprobar una firma sin la plataforma (para peritos)

El acta de firma lleva todo lo necesario para repetir la comprobación con OpenSSL, una herramienta estándar que viene en cualquier Linux o Mac y se instala en Windows. No hace falta confiar en CheckBiz360 ni en ningún certificado: solo matemáticas.

Del acta se copian tres cosas: la **cadena firmada** (el bloque «tal cual» del apartado 2), la **firma** en base64 (apartado 3) y la **clave pública** en PEM (apartado 3). Después, en una carpeta vacía:

1. Guarde la cadena firmada en un fichero `payload.txt`, exactamente como aparece, sin añadir un salto de línea al final.
2. Guarde la firma en `sig.b64` y decodifíquela: `base64 -d sig.b64 > sig.der`
3. Guarde la clave pública, con sus líneas `BEGIN PUBLIC KEY` y `END PUBLIC KEY`, en `key.pem`.
4. Compruebe la firma: `openssl dgst -sha256 -verify key.pem -signature sig.der payload.txt` → debe responder **Verified OK**.
5. Compruebe que la clave es la que consta en el acta: `openssl pkey -pubin -in key.pem -outform DER | openssl dgst -sha256` → debe coincidir con la **huella de la clave pública (keyId)** del acta.

Con eso queda demostrado que **esa clave firmó exactamente esa cadena**, y la cadena lleva dentro el documento, su versión y el hash de su contenido (o la entrega y sus documentos). Para atar la clave a la persona, el acta indica cuándo se registró y desde qué móvil, y el consentimiento del trabajador cierra el círculo.

Si el perito prefiere el fichero de evidencia original en JSON, con los mismos datos y su propio SHA-256, soporte puede facilitárselo a partir del número de acta.

## Recoger el consentimiento con la propia plataforma

El consentimiento no necesita papel: se recoge como cualquier otro acuse de recibo, y así queda con fecha, firmado y con su acta.

1. Redacte un documento breve, **«Condiciones de la firma electrónica»**, que diga: que confirmar un documento o una entrega desde la app de CheckBiz360 con la huella, la cara o el código del móvil es la firma electrónica del trabajador y tiene el mismo valor que su firma manuscrita a efectos internos; que la clave se crea en su móvil y no sale de él; que si su móvil no tiene bloqueo de pantalla confirmará con la contraseña de su cuenta; que puede pedir en cualquier momento una copia de lo firmado y del acta; y a quién dirigirse con dudas. Conviene que lo revise su asesoría.
2. Súbalo **a cada sucursal** con **Requiere confirmación de lectura** activado, visible para todos los roles. El acuse de recibo se pide por sucursal o por empleado, no a toda la empresa de una vez.
3. Cada trabajador lo confirma desde la app. Esa confirmación es el registro del consentimiento: quién, cuándo y sobre qué texto, con su acta si la hizo con la app actualizada.
4. A los que entren después, inclúyalo en el contrato o súbaselo a ellos individualmente al darles de alta.

Hasta que un trabajador lo haya confirmado, trátelo como si confirmara pulsando: la plataforma registra igual, pero la empresa no tendrá el consentimiento que respalda la firma.

## Descargar e instalar el certificado de CheckBiz360

Solo hace falta si quiere que Acrobat Reader muestre las firmas **en verde**. Sin instalarlo, el lector dice que el documento no se ha modificado y que la firma es válida, pero que la identidad del firmante es «desconocida» porque CheckBiz360 no está en su lista de confianza. La comprobación es la misma en los dos casos.

**Descargar:** en el backoffice, abra la ficha de la empresa, pestaña **Entorno de trabajo**, apartado **Firma electrónica**, y pulse **Descargar el certificado (.zip)**. Descomprima el zip: lleva el mismo certificado en dos formatos, **checkbiz360-firma-ca.cer** para Acrobat y Windows y **checkbiz360-firma-ca.crt** en texto para el llavero de Mac o Linux, y un fichero con estas instrucciones.

**Instalar en Acrobat Reader:**

1. Abra **Edición → Preferencias → Firmas**.
2. En **Identidades y certificados de confianza**, pulse **Más**.
3. Entre en **Certificados de confianza** y pulse **Importar**.
4. Elija el fichero **.cer** y, en las opciones del certificado, marque **Utilizar este certificado como raíz de confianza**. Acepte.
5. Cierre el PDF firmado y vuelva a abrirlo: la firma aparece en verde.

**Si la empresa tiene varios ordenadores (Windows):** el informático puede instalarlo una vez en cada equipo, o por directiva, en el almacén de certificados de Windows, dentro de **Entidades de certificación raíz de confianza**, y en Acrobat, en **Preferencias → Firmas → Verificación → Más**, marcar que confíe en los certificados raíz del almacén de Windows.

> **Nota:** en Mac, Vista Previa no comprueba firmas; use Acrobat Reader, donde los pasos son los mismos.

**Otros lectores y validadores.** Acrobat no es obligatorio: la firma es PAdES, el estándar europeo, y la validan también Foxit, PDF-XChange o LibreOffice, cada uno con su forma de importar el certificado. AutoFirma es una herramienta para firmar con certificados reconocidos, no para validar; el validador de la Administración, VALIDe, confirmará que el documento no se ha modificado, pero marcará el certificado del firmante como no reconocido, porque CheckBiz360 no es un prestador cualificado. Para demostrar la firma ante un perito sirve el acta, que se comprueba sin ninguna lista de confianza.

## Cómo activar el acuse de recibo

1. Al subir o editar el documento, active **Requiere confirmación de lectura**.
2. Para una nómina o una amonestación, suba el documento **al empleado** (ámbito empleado): así podrá firmarse dentro del PDF.
3. Compruebe que el documento es visible para su destinatario.

Si tiene activadas las notificaciones del módulo documental, el empleado recibe un aviso con el documento pendiente.

---

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
- [Nóminas y contratos](32-nominas-y-contratos.md)
- [Documentos privados](33-documentos-privados.md)
- [Notificaciones de documentos](34-notificaciones-de-documentos.md)
- [Primer inicio de sesión en la app](../10-app-movil/70-primer-inicio-de-sesion.md)
