# Exportar el listado de empleados

Este artículo explica cómo obtener los datos de su plantilla fuera de la plataforma y qué alternativas existen mientras la exportación directa del directorio no está disponible.

---

## Estado de la funcionalidad

> **Estado: Pendiente de desarrollo**
> Esta funcionalidad forma parte del roadmap y no está disponible todavía en la versión actual.

El backoffice **no dispone hoy de un botón para exportar el listado de empleados a CSV**. El listado de **Empleados** se consulta, filtra y busca en pantalla, pero no genera un fichero descargable.

La **importación** de empleados desde CSV, en cambio, sí está disponible: consulte más abajo.

---

## Qué sí puede exportar hoy

| Necesidad | Vía disponible |
|---|---|
| Horas trabajadas, presencias y ausencias por empleado y periodo | **Informe de asistencia**, en PDF o Excel (XLSX) |
| Tareas del periodo con su estado y cumplimiento | **Informe de tareas**, en Excel (XLSX) |
| Justificación del registro de jornada ante una inspección | **Informe de cumplimiento normativo** |

Ambos informes incluyen la identificación del empleado, de modo que una exportación de asistencia de un periodo amplio permite reconstruir el listado de personas activas y sus datos de referencia.

Consulte [Exportar datos](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md) para el detalle de cada informe.

---

## Importar empleados desde CSV

El sentido contrario sí está cubierto. Si viene de otro sistema o necesita dar de alta a muchas personas, puede cargar un fichero CSV con los datos de sus empleados y mapear sus columnas con los campos de la plataforma durante el proceso de importación.

Es la vía recomendada en una puesta en marcha con plantilla grande, en lugar de crear los perfiles uno a uno.

---

## Si necesita el directorio completo

Para una extracción completa del directorio de empleados —por ejemplo, para una auditoría, un cambio de sistema o el ejercicio del derecho de portabilidad de datos— escriba a **hola@encodebiz.com** solicitándolo. El equipo de soporte puede facilitar la extracción.

---

## Consideraciones RGPD

Cualquier fichero que salga de la plataforma contiene datos personales de los empleados (nombre, correo, documento de identidad) y pasa a ser responsabilidad de su empresa:

- **Almacenamiento seguro.** Guarde los ficheros en ubicaciones con acceso restringido, no en carpetas compartidas sin control.
- **Transmisión protegida.** Si envía el fichero a su gestoría, use un canal cifrado o protéjalo con contraseña.
- **Minimización.** Extraiga solo el periodo y los campos necesarios para cada finalidad.
- **Conservación.** Elimine el fichero una vez cumplida su finalidad, salvo obligación legal de conservarlo.

> **Aviso:** CheckBiz360 custodia los datos dentro de la plataforma con las medidas de seguridad exigidas por la normativa. Una vez exportados, la seguridad de esos ficheros corresponde a su empresa.

---

## Nota de rol

La generación de informes está disponible para **manager** (nivel 3) y **owner** (nivel 4).

---

## Artículos relacionados

- [Crear y gestionar empleados](06-crear-y-gestionar-empleados.md)
- [Roles y niveles de responsabilidad](07-roles-y-niveles-de-responsabilidad.md)
- [Exportar datos](../11-informes-y-exportacion/78-exportar-a-excel-y-csv.md)
- [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md)
- [Conservación y protección de datos](../12-cumplimiento-normativo/83-conservacion-y-proteccion-de-datos.md)
