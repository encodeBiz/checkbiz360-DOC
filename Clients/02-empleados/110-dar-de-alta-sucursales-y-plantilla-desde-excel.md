# Dar de alta sucursales y plantilla desde Excel

El primer día con CheckBiz360 suele empezar con una lista: la gestoría manda la plantilla, usted tiene los centros en una hoja, y crear cuarenta fichas y seis sucursales una a una es una tarde entera. No hace falta. Una plantilla de Excel, una subida y una revisión bastan para dar de alta a toda la empresa de una vez, sin que nada se cree hasta que usted lo confirme.

---

## Qué resuelve

- **Toda la plantilla y todos los centros de una vez**, desde una hoja con dos pestañas.
- **Lo ve antes de crear nada.** Cada sucursal y cada persona aparece con lo que va a pasar: nueva, ya existe, se le añaden sucursales, sin cambios o con error.
- **Un error no lo para.** Las filas con error se quedan fuera; las demás se crean. Corrija el fichero y vuelva a subirlo: lo que ya se creó no se duplica.
- **La bienvenida, cuando usted decida.** Al importar no se manda ningún correo. Cuando haya comprobado que todo está bien, un botón envía la bienvenida a la app a la gente nueva.
- **Vale para crecer, no solo para empezar.** Súbala otra vez con la gente nueva: a quien ya existe se le reconoce por su correo, y a las sucursales por su nombre.

---

## Cómo funciona, en tres pasos

| Paso | Qué pasa |
|---|---|
| **1. Descargar la plantilla** | Desde la lista de empleados o la de sucursales, con el botón **Importar**. |
| **2. Rellenarla y subirla** | Una pestaña para las sucursales y otra para las personas. Al subirla no se crea nada todavía. |
| **3. Revisar y confirmar** | La plataforma enseña qué hará con cada fila. Solo al confirmar se crea. |

---

## 1. Descargar la plantilla

1. Vaya a **Empleados** (o a **Sucursales**) y pulse **Importar**.
2. En la ventana **Importar sucursales y plantilla**, pulse **Descargar plantilla**.

La plantilla trae dos pestañas, **Sucursales** y **Empleados**, con **filas de ejemplo que empiezan por ELIMINAR**: puede borrarlas o dejarlas, no se importan.

> Si una sucursal ya existe en CheckBiz360, no hace falta repetirla en la pestaña Sucursales: basta con escribir su nombre en la fila de cada persona.

### Pestaña Sucursales

| Columna | Qué poner |
|---|---|
| **Nombre** * | Cómo llama usted al centro. Es el nombre que usará en la pestaña Empleados. |
| **Dirección** * | Calle y número. Es donde su gente fichará. |
| **Código postal**, **País** | Si no los pone, se completan a partir de la dirección. |
| **NIF** | El de ese centro, si lo tiene propio. |
| **Radio de fichaje (m)** | Hasta qué distancia del centro se admite el fichaje. En blanco, el radio habitual. |

Una dirección sin número de portal no sirve: si solo se localiza de forma aproximada, la fila sale con error y le pide calle y número.

### Pestaña Empleados

| Columna | Qué poner |
|---|---|
| **Nombre completo** * | Nombre y apellidos. |
| **Correo** * | Con él entra en la app y recibe la bienvenida. Es lo que identifica a la persona: si ya existe, no se crea otra. |
| **Teléfono**, **DNI/NIE** | Opcionales. |
| **Puesto** | Su ocupación. Si no existe aún en su catálogo de puestos, se añade; la revisión le avisa de cuáles son nuevos. |
| **Tipo** | **Plantilla** o **Colaborador**. En blanco, plantilla. |
| **Sucursal** * | El nombre de su centro, tal como está en la pestaña Sucursales o como ya se llama en CheckBiz360. Si trabaja en varias, sepárelas con punto y coma. |
| **Responsabilidad** | **Trabajador**, **Supervisor** o **Gerente** en ese centro. En blanco, trabajador. |
| **Precio hora** | El que alimenta el análisis de costes. En blanco, el del puesto si ya existe. |
| **Horario** | **Semanal** (el de siempre) o **Por tareas**. En blanco, semanal. |

Las columnas con asterisco son obligatorias.

---

## 2. Subir el fichero

Pulse **Elegir fichero**, seleccione la plantilla rellena y pulse **Revisar**. Vale el Excel (.xlsx) de hasta 2 MB y 2.000 personas. Si sube un fichero que no es la plantilla, la plataforma lo dice y no lee nada.

Mientras lee el fichero comprueba las direcciones, así que con muchos centros tarda unos segundos.

---

## 3. Revisar lo que se hará

Antes de confirmar ve dos tablas, **Sucursales** y **Personas**, cada fila con su estado:

| Estado | Significa |
|---|---|
| **Nueva** | Se creará. En las sucursales, con la dirección tal como se ha localizado (exacta o aproximada en la calle). |
| **Ya existe** | No se toca. |
| **Se le añaden sucursales** | La persona ya existía y gana los centros nuevos de su fila. |
| **Se actualiza su horario** | Solo cambia su modo de horario. |
| **Sin cambios** | Nada que hacer con esa fila. |
| **Error** | Esa fila no se importa: la observación dice por qué (una dirección imprecisa, un correo mal escrito, una sucursal que no existe). Las demás filas sí se importan. |

Arriba, un resumen: cuántas sucursales y personas nuevas, cuántas ya existían, cuántas con error, y cuántas personas activas se añaden a su factura.

Si quiere arreglar algo, corrija el fichero y pulse **Subir otro fichero**. Si cierra la ventana sin confirmar, no se crea nada.

Cuando esté conforme, pulse **Confirmar e importar**. Se ve el avance; puede cerrar la ventana y la importación sigue. Si no termina, **Reintentar** continúa donde se quedó sin duplicar nada.

---

## 4. Enviar la bienvenida

Al terminar, la ventana dice cuántas personas nuevas todavía no han recibido la bienvenida a la app. Cuando haya comprobado que sus fichas están bien, pulse **Enviar bienvenidas**: cada persona recibe el correo con el que entra por primera vez en la app. Si prefiere mandarlas más tarde, cierre la ventana: la gente queda creada igual.

---

## Quién puede importar

Propietarios y administradores de la empresa. Cada persona activa que se crea cuenta en la factura desde ese momento, igual que si la hubiera dado de alta a mano.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Crear y gestionar empleados](./06-crear-y-gestionar-empleados.md) | El alta de una sola persona y los estados de la ficha |
| [Crear y gestionar sucursales](../08-sucursales-y-entidad/57-crear-y-gestionar-sucursales.md) | El alta de un centro y su dirección |
| [Roles y niveles de responsabilidad](./07-roles-y-niveles-de-responsabilidad.md) | Qué puede hacer un trabajador, un supervisor y un gerente |
| [Su gestor operativo en Claude o ChatGPT](../15-integraciones/109-su-gestor-operativo-en-claude-o-chatgpt.md) | Las mismas altas, pedidas a su asistente desde la lista de la gestoría |
