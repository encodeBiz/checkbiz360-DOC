# Prueba de extremo a extremo — firma, documentos e inventario (octubre 2026)

**Para qué:** es la **aceptación previa al pase a producción** de octubre
([deployment-prod/2026-10](../../deployment-prod/2026-10-inventario-firma-back.md)). Se ejecuta
entera en staging con la versión de la app que se va a publicar; no se sube nada a producción
hasta que los pasos 1 a 8 estén en verde. Después del pase, se repiten en producción los pasos
**1, 2 (hasta 2.6) y 7** con una empresa piloto y un móvil real, antes de anunciarlo a nadie.

**Entorno:** staging (`api-staging.checkbiz360.com`, Firebase `dev-encodebiz`). Panel en local con
`npm run start:dev`. App en sabor `development`.
**Empresa de pruebas:** Cuidama Servicios. **Propietaria:** Marta (panel). **Trabajador:** Jose
Manuel Acevedo (app), empleado `qj6b3ReOfrOUo0vE3yDE`, sucursal con almacén «Central».
**Equipo de pruebas:** operable «Fregadora», ejemplares FR-1, FR-2, FR-3. Artículo consumible
«Guantes». Tarea de pruebas `10PSo4gz9j0N608oc5sH` o una nueva.
**Ficheros:** `encodebiz-api/qa/tests/con-datos/fixtures/nomina-sintetica.pdf` (dos páginas, datos
ficticios) y cualquier imagen PNG.

Cada paso dice **quién** lo hace (Panel = Marta en el backoffice; App = Jose Manuel en el móvil;
Terminal = quien haga de perito) y **qué debe verse**. Si algo no sale como se dice, anotarlo con
el paso y seguir: lo que viene después no depende, salvo que se indique.

---

## 0. Antes de empezar (10 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 0.1 | Panel | Parar y volver a arrancar `npm run start:dev` | Arranca sin errores (hay variables nuevas en `.env.development`: acta, certificado, informes) |
| 0.2 | App | Instalar la versión nueva (rama de la sesión de la app) y **cerrar sesión** si la había | Pantalla de inicio de sesión |
| 0.3 | Móvil | Comprobar que tiene **huella o cara** activas (Ajustes del móvil) | Si no, la prueba sale por el camino del PIN o la contraseña, también válido |
| 0.4 | Panel | Suscripciones → el inventario está activo en Cuidama | «Activo» o «En prueba» |
| 0.5 | Panel | Inventario → Existencias → Fregadora: FR-3 libre, sin entrega activa | Si está entregado, devolverlo primero |
| 0.6 | Panel | Gestión documental: archivar restos de pruebas anteriores con «prueba» en el título | Lista limpia |

## 1. La clave del móvil (App, 2 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 1.1 | App | Iniciar sesión como Jose Manuel | Entra como siempre. **No aparece ningún diálogo** pidiendo huella: la clave se crea en silencio |
| 1.2 | App | Cerrar sesión y volver a entrar | Igual de rápido; la clave se reutiliza |

> No hay nada que mirar en el panel: la clave y su certificado se ven solo cuando firma.

## 2. Nómina firmada dentro del PDF (Panel → App → Panel, 15 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 2.1 | Panel | Gestión documental → Subir: ámbito **Empleado** = Jose Manuel, tipo **Nómina**, título «Nómina prueba E2E», **Requiere confirmación de lectura**, fichero `nomina-sintetica.pdf` | Documento creado; en la ficha, acuse pendiente |
| 2.2 | App | Llega la notificación; abrir el documento | Se ve el PDF original (sin marca en el margen) y el botón de confirmar |
| 2.3 | App | **Confirmar** | Pide la huella (o la cara). Tras ella, el documento se recarga: **el PDF lleva una línea gris muy pequeña en el margen inferior** de cada página con «Firmado electrónicamente por Jose Manuel Acevedo · fecha · CheckBiz360 · verificación … · acta …» |
| 2.4 | Panel | Abrir la ficha del documento | En confirmaciones: Jose Manuel, fecha, marca **«Firmada y verificada (huella o cara)»** y el icono de PDF «Descargar el acta de firma» |
| 2.5 | Panel | Pulsar «Descargar el acta de firma» | Se abre un PDF de una página: quién, cuándo, cómo; documento, versión y SHA-256; cadena firmada; firma; clave pública y su huella; evidencia; cómo comprobarla |
| 2.6 | Panel | En la misma ficha, **Descargar** el documento | Es el **PDF firmado** (con la marca del margen), no el original |
| 2.7 | Acrobat | Abrir ese PDF en Acrobat Reader → panel de firmas | «La firma es válida… identidad del firmante desconocida» (interrogación amarilla); «el documento no se ha modificado» |
| 2.8 | Panel | Entidad → **Entorno de trabajo** → **Firma electrónica** → «Descargar el certificado (.zip)» | Baja `checkbiz360-firma-ca.zip`; dentro, `.cer`, `.crt` y `LEEME.txt` |
| 2.9 | Acrobat | Edición → Preferencias → Firmas → Identidades y certificados de confianza → Más → Certificados de confianza → Importar el `.cer` del zip → marcar «raíz de confianza» → cerrar y reabrir el PDF | **Tick verde**: firma válida y firmante «CN=Jose Manuel Acevedo», emitido por «CheckBiz360 Firma CA (dev)» |
| 2.10 | Panel | Intentar volver a subir… no: editar el título del documento y guardar | La confirmación y el acta siguen; el PDF sigue siendo el firmado |

## 3. El perito (Terminal, 10 min)

Con el acta del paso 2.5 abierta, en una carpeta vacía:

| # | Hacer | Debe verse |
|---|---|---|
| 3.1 | Copiar la **cadena firmada** (apartado 2 del acta) a `payload.txt`, **sin salto de línea final** | — |
| 3.2 | Copiar la **firma** (apartado 3) a `sig.b64` y ejecutar `base64 -d sig.b64 > sig.der` | Fichero `sig.der` de ~70 bytes |
| 3.3 | Copiar la **clave pública** (BEGIN/END PUBLIC KEY) a `key.pem` | — |
| 3.4 | `openssl dgst -sha256 -verify key.pem -signature sig.der payload.txt` | **Verified OK** |
| 3.5 | `openssl pkey -pubin -in key.pem -outform DER \| openssl dgst -sha256` | Coincide con la **huella de la clave pública (keyId)** del acta |
| 3.6 | Cambiar una letra de `payload.txt` y repetir 3.4 | **Verification Failure** (así se ve que la comprobación es real) |

## 4. Acuse firmado sin tocar el fichero (Panel → App, 10 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 4.1 | Panel | Subir «Política prueba E2E», ámbito **Sucursal** (la de Jose Manuel), tipo Política interna, **Requiere confirmación**, cualquier PDF | Creado |
| 4.2 | App | Abrir y **Confirmar** con la huella | Confirma; **el documento no cambia** (sin marca en el margen): es de muchos |
| 4.3 | Panel | Ficha del documento | «Firmada y verificada (huella o cara)» y el acta disponible; la descarga sigue siendo el PDF original |
| 4.4 | Panel | Subir «Imagen prueba E2E», ámbito **Empleado** = Jose Manuel, **Requiere confirmación**, un **PNG** | Creado |
| 4.5 | App | Confirmar con la huella | Confirma; la imagen no cambia; en el panel, firmada y verificada, con acta |
| 4.6 | App (opcional) | En un móvil **sin bloqueo de pantalla**, confirmar un documento | Pide la **contraseña** de la cuenta; en el panel, «Confirmada con contraseña», sin acta |

## 5. Documentos del equipo y el rojo (Panel, 15 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 5.1 | Panel | Inventario → Existencias → Fregadora → sección **Documentos** → **Subir documento**: tipo **Revisión obligatoria**, título «ITV prueba E2E», **Aplica a** FR-1, resultado Apto, **Próxima revisión antes del** = ayer | En la lista de ejemplares, FR-1 con la pastilla **«Fuera de regla»** y el motivo al pasar el ratón |
| 5.2 | Panel | Existencias | La fila de Fregadora dice **«1 fuera de regla»** |
| 5.3 | Panel | Documentos → **Vincular existente** → buscar «Manual» (o subir uno tipo Manual) → Aplica a **Todos sus ejemplares** | Aparece en la lista con «Todos los ejemplares» |
| 5.4 | Panel | Marcar en ese manual la casilla **«Con cada entrega»** | Queda marcada al recargar |
| 5.5 | Panel | Gestión documental | Los dos documentos aparecen también ahí, con ámbito Equipo |
| 5.6 | Panel | Subir otra «Revisión obligatoria» a FR-1 con fecha el año que viene | FR-1 pasa a **«En regla»**; la ITV antigua aparece como **«Sustituido»** |
| 5.7 | Panel | Desvincular la ITV antigua | Desaparece de la lista; en Gestión documental sigue existiendo |

## 6. Reservar un ejemplar en rojo (Panel, 5 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 6.1 | Panel | Dejar un ejemplar en rojo (subir a FR-2 una revisión obligatoria caducada) | FR-2 «Fuera de regla» |
| 6.2 | Panel | Tareas → una tarea asignada → Añadir material → Fregadora → ejemplar FR-2 | Debajo de la línea, aviso rojo con el motivo y la casilla **«Lo sé y lo reservo igualmente»**; sin marcarla, la línea no se pide |
| 6.3 | Panel | Marcar la casilla y reservar | Reserva creada; en la ficha del ejemplar, la reserva |
| 6.4 | Panel | Liberar la reserva y subir a FR-2 una revisión vigente | FR-2 en regla |

## 7. Entrega con documentos y acuse firmado (Panel → App → Panel, 15 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 7.1 | Panel | Fregadora → FR-3 → **Entregar** → Jose Manuel | En el diálogo, **«Documentos que se entregan»** con el manual **ya marcado** (paso 5.4); no hay campo de texto libre |
| 7.2 | Panel | Entregar | FR-3 «Entregado · Jose Manuel», acuse pendiente |
| 7.3 | App | Notificación «Se te ha entregado…» → **Mi material** | La entrega, con la frase genérica «Confirmo que he recibido este equipo y los documentos relacionados…» y el manual listado y abrible |
| 7.4 | App | Confirmar con la huella | Confirmada |
| 7.5 | Panel | Ficha de Fregadora / ficha del empleado → Material | Acuse **confirmado** |
| 7.6 | Panel | Informes → **Equipos y EPIs** → periodo de hoy → generar | Excel con dos hojas. **Entregas**: fila de Jose Manuel con «Cómo se confirmó: Huella o cara», **«Firma: Verificada (huella o cara) · clave … · acta …»** y **«Documentos entregados: Manual… (v1)»**. **Equipos y revisiones**: cada ejemplar con su estado y sus papeles |
| 7.7 | Panel | Devolver FR-3 «En buen estado» | FR-3 libre |
| 7.8 | Panel | Informes sin el add-on (otra empresa sin inventario) | «Equipos y EPIs» en **rojo**, y al pulsar, la explicación |

## 8. Consumo y cuadre, por no romper lo de antes (Panel → App → Panel, 10 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 8.1 | Panel | Tarea nueva para hoy, asignada a Jose Manuel, con material: Guantes × 4 del almacén Central | Reservado 4 |
| 8.2 | App | Tarea → material → **Declarar consumo** (precargado 4) → poner 3 | Declarado |
| 8.3 | Panel | Tarea: material | Salida 3, consumido 3, pendiente 0; reservado 1 sin salir |
| 8.4 | Panel | Validar la tarea → aparece el cuadre con lo reservado no salido (1) | Elegir «devuelto»; cuadrar **cierra el modal y no valida**; validar después |
| 8.5 | Panel | Existencias → Informe de consumo de hoy | Guantes 3 con su coste |

## 9. Avisos (Panel/Terminal, 5 min)

| # | Quién | Hacer | Debe verse |
|---|---|---|---|
| 9.1 | Terminal | En el VPS de desarrollo: `docker compose -f docker-compose.staging.yml -p encodebiz-api-dev exec -T inventory node services/inventory/dist/scripts/document-expiry.js` | Simulación: lista «avisaría» / «ya avisado» de las revisiones caducadas del paso 5 y 6 |
| 9.2 | Terminal | Lo mismo con `--apply` | «Avisado a N» |
| 9.3 | Panel/App | Campana de avisos del responsable del almacén | «ITV prueba E2E de Fregadora (FR-2) caducó el …» |

## 10. Limpieza (5 min)

Archivar los documentos «prueba E2E» desde Gestión documental; devolver FR-3 si sigue entregado;
liberar reservas de la tarea de pruebas; dejar FR-1 y FR-2 en regla o desvincular las revisiones
caducadas.

---

## Lo que se anota al terminar

- Paso que falló, qué se vio y qué se esperaba (captura si es del móvil).
- Modelo y sistema del móvil, y si entró por huella, cara, código o contraseña.
- Lector de PDF usado en 2.7 y 2.9.

Lo que esta prueba **no cubre**: Vercel (el panel es local), producción, y el sello de tiempo.
