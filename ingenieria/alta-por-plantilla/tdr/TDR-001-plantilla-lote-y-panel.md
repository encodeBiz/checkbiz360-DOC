# TDR-001 — La plantilla, el lote y el panel

**Fecha:** 2026-10-16
**Estado:** Diseño aceptado; implementación en `feat/importacion-plantilla` (API y panel)
**Componentes:** `services/employees` (importación, bienvenidas), `services/branches` (puerta delegada), `packages/shared` (el cupo deja de bloquear), panel
**Referencias:** [README](../README.md); [inventario TDR-007](../../inventario/tdr/TDR-007-importacion-masiva-por-plantilla.md), que es el calco; [cuadrantes TDR-001](../../cuadrantes/tdr/TDR-001-importacion-por-plantilla-de-sucursal.md); [conector-asistente ADR-005](../../conector-asistente/adr/ADR-005-la-persona-delegada-por-la-puerta-de-servicio.md)

---

## 1. La plantilla

Un Excel con tres hojas: una portada que no se lee (cómo rellenarla) y dos pestañas, en el idioma
del panel (es, en, pt, fr, de). Dos filas de ejemplo por pestaña, en gris y con la palabra de
ignorar delante (ELIMINAR, DELETE, EXCLUIR, LÖSCHEN, SUPPRIMER), como en las demás plantillas.

**Sucursales**

| Columna | Obligatoria | Va a |
|---|---|---|
| Nombre | sí | `name` |
| Dirección | sí | se geocodifica: `address.street` (la normalizada), `geo`, `timeZone`, `postalCode` |
| Código postal | | ayuda al geocodificador |
| País | | código ISO de dos letras o nombre; por defecto, `ES` |
| NIF | | `nif` |
| Radio de fichaje (m) | | `ratioChecklog`; por defecto, 200 |

**Empleados**

| Columna | Obligatoria | Va a |
|---|---|---|
| Nombre completo | sí | `fullName` |
| Correo | sí | `email`: es la clave de la persona y su acceso a la app |
| Teléfono | | `phone` |
| DNI/NIE | | `nationalId` |
| Puesto | | `jobTitle`, y el oficio de su responsabilidad |
| Tipo | | `role`: Plantilla (`internal`, por defecto) o Colaborador (`collaborator`) |
| Sucursal | sí | el nombre de una sucursal del fichero o de las que ya existen; varias, separadas por `;` |
| Responsabilidad | | Trabajador (por defecto), Supervisor o Gerente |
| Precio hora | | `job.price`; por defecto, 0 |

Las cabeceras se reconocen en los cinco idiomas y con los nombres habituales de una gestoría
(«Nombre y apellidos», «Email», «Centro», «Delegación», «NIF», «Cargo»…), por el mismo
mecanismo de vocabulario que la plantilla de cuadrantes.

## 2. La propuesta

`POST` del fichero → se lee, se cruza con lo que ya hay, se geocodifica cada dirección nueva y se
devuelve una propuesta fila a fila, guardada como lote. **No se escribe nada.**

**Estados de una sucursal:** `nueva` (con la dirección resuelta y su precisión), `existe` (se usa
tal cual), `ignorada` (ejemplo), `error` (sin nombre, dirección que no se
resuelve o sólo a ciudad, nombre repetido en el fichero).

**Estados de una persona:** `nueva`, `existe, se le añaden sucursales` (con cuáles),
`existe, sin cambios`, `ignorada`, `error` (sin nombre o correo, correo mal
escrito, correo repetido en el fichero, sucursal que no está ni en el fichero ni en la empresa,
responsabilidad o tipo desconocidos, persona dada de baja con ese correo).

**Sin cupo** (README D4): no se calculan plazas ni se deja nada fuera. El alta de empleados y de
sucursales deja de bloquear por cupo en `subscriptionLimits.ts`: sin suscripción no se crea
nada; con suscripción, siempre.

**Totales:** sucursales nuevas, personas nuevas, personas a las que se añaden sucursales, sin
cambios, ignoradas, errores; y la frase de la factura: «N personas nuevas
pasarán a contar en tu factura».

## 3. Confirmar

Igual que inventario: «confirmar» pasa el lote a *aplicando* en una transacción, responde `202` y
aplica en segundo plano, apuntando el avance cada dos segundos; un lote *aplicando* sin señales
durante cinco minutos se puede volver a confirmar. **Se vuelve a planificar** contra lo que haya
en ese momento con la misma función que hizo la propuesta, así que un reintento encuentra lo que
el anterior ya creó y no duplica nada.

Orden: sucursales (de dos en dos), después personas (de cuatro en cuatro), y por cada persona sus
responsabilidades.

- **Sucursal**: `POST /api/v1/branches/delegated` con la persona que confirma; la validación,
  el índice y el evento son los del alta a mano.
- **Persona**: `darDeAlta(uid, datos, {sendWelcome: false})`, la función que la ruta de alta usa
  desde ahora, con la validación y el control de duplicados de siempre.
- **Responsabilidad**: `asignarResponsabilidad(uid, …)`, la de la ruta de responsabilidades, con
  el oficio del puesto (o «Trabajador») y el precio hora.

El resultado por fila (creada, ya existía, error con su motivo) y los ids de las personas creadas
quedan en el lote.

## 4. Enviar bienvenidas

`POST /api/v1/employees/welcome {entityId, employeeIds}` → manda la bienvenida a cada una
(`sendWelcomeEmail`, la de «reenviar»), de cinco en cinco, y devuelve enviadas y fallidas. Hasta
500 por llamada. El resultado de la importación lo ofrece con los ids que creó; también vale para
cualquier lista de personas.

## 5. Rutas

En `employees`, bajo `/api/v1/employees/import`, con el token de Firebase y `canWrite` sobre la
empresa:

```
GET    /import/template?entityId&lang          → {filename, mimeType, base64}
POST   /import   {entityId, filename, content (base64), lang} → 201 {lote}
GET    /import/:id?entityId                    → el lote: estado, avance, resultado
POST   /import/:id/apply {entityId}            → 202 (aplicando) · 200 si ya estaba aplicado
DELETE /import/:id?entityId                    → descartar una propuesta sin confirmar
POST   /welcome {entityId, employeeIds}         → {enviadas, fallidas}
```

El fichero viaja en base64 dentro de JSON, como en inventario y cuadrantes (el proxy del panel
sólo transporta JSON). La ruta de subida lleva su propio lector de 4 MB y el `location` de
`employees` en nginx sube a 4 MB. Límites: 2 MB, 200 sucursales y 2.000 personas por fichero.

**El lote** se guarda en `entities/{e}/staff_imports/{id}` con las filas en una subcolección por
trozos, como inventario: quién, cuándo, fichero, propuesta, resultado. Entra en `soloServidor` de
las reglas de Firestore: lleva correos, teléfonos y DNI.

**`branches`** monta su router además en `/api/v1/branches/delegated`, detrás de
`requireDelegatedUser`: las mismas rutas y guardas, que leen a la persona de `req.user`.

## 6. El panel

- Botón **«Importar»** junto a «Añadir empleado» y junto a «Añadir sucursal», con el mismo diálogo.
- El diálogo calca el del material y el del cuadrante: el fichero con «Descargar plantilla»; la
  propuesta, con los totales en pastillas, la frase de la factura y dos tablas (sucursales y
  personas) con lo que pide atención primero; el avance, que se puede cerrar sin pararlo; y el
  resultado, con **«Enviar bienvenidas a N personas»**.
- Cerrar en la propuesta la descarta. Al terminar se repinta la lista.
- Proxy `employees_import_handler`, con sus subrutas.

## 7. Pruebas

- La parte pura (leer la plantilla, cruzar con lo que hay, estados de cada fila)
  con ficheros en memoria y repositorios de mentira.
- La plantilla generada y releída sin pérdidas en los cinco idiomas.
- Contra dev: una plantilla con dos sucursales nuevas, una existente, cinco personas nuevas, una
  existente con una sucursal nueva, un correo repetido y una dirección que no se resuelve.
