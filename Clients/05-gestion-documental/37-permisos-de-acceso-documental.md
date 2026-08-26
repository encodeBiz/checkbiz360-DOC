# Permisos de acceso documental

El módulo documental de CheckBiz360 aplica un modelo de permisos basado en roles que determina qué acciones puede realizar cada usuario sobre los documentos. Comprender esta estructura es fundamental para configurar correctamente el acceso, proteger la documentación sensible y garantizar que cada persona de la organización ve únicamente lo que le corresponde.

## Roles y permisos generales

CheckBiz360 define cuatro roles principales con distintos niveles de acceso al módulo documental:

| Acción | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| Ver documentos propios | Sí (públicos) | Sí (públicos) | Sí (todos) | Sí (todos) |
| Ver documentos de otros empleados | No | Solo su equipo (si tiene permiso) | Sí (su entidad) | Sí (toda la entidad) |
| Subir documentos | No | Según delegación | Sí | Sí |
| Editar documentos | No | Según delegación | Sí | Sí |
| Eliminar documentos | No | No | Sí | Sí |
| Solicitar firma | No | No | Sí | Sí |
| Acusar recibo | Sí (los propios) | Sí (los propios) | No aplica | No aplica |
| Ver documentos privados | No | Según delegación | Sí | Sí |
| Exportar documentos | No | No | Sí | Sí |

> **Nota:** Esta tabla refleja los permisos por defecto de cada rol. Los permisos específicos de los supervisores pueden ampliarse o restringirse a través de la delegación configurada por el manager. Los permisos del Owner no son modificables.

## Visibilidad de nóminas y contratos

Las nóminas y los contratos son los tipos de documentos más habituales y también los que con mayor frecuencia generan dudas sobre quién puede acceder a ellos.

### Nóminas

- **Owner y Manager**: pueden ver las nóminas de todos los empleados de la entidad, independientemente de si están marcadas como privadas o no.
- **Supervisor**: puede ver las nóminas de los empleados de su equipo únicamente si el manager le ha concedido acceso explícito a los documentos de ese equipo. Por defecto, el supervisor no tiene acceso a las nóminas.
- **Worker**: puede ver sus propias nóminas si no están marcadas como privadas. No puede ver las nóminas de ningún otro empleado.

### Contratos

Las mismas reglas se aplican a los contratos. Un empleado puede ver su propio contrato si está publicado y no es privado. No puede ver los contratos de sus compañeros.

## Restricciones por el campo privado

Cuando un documento tiene el campo `private` activado, las restricciones de visibilidad se aplican de la siguiente manera:

- El documento es invisible para el empleado (Worker) con independencia de si está publicado.
- El supervisor solo puede ver el documento si tiene permisos delegados para gestionar documentos del equipo afectado y si el manager le ha concedido expresamente acceso a documentos privados.
- El Manager y el Owner siempre pueden ver todos los documentos, incluyendo los privados.

Esta jerarquía garantiza que la información sensible —como notas disciplinarias, evaluaciones o cartas de amonestación— permanezca protegida frente al acceso no autorizado.

## Delegación de permisos desde Manager a Supervisor

El manager puede ampliar los permisos de un supervisor para incluir la gestión documental de su equipo. Esto permite que el supervisor asuma responsabilidades de subida y organización de documentos sin necesidad de dar acceso completo de manager.

La delegación puede cubrir:

- **Subida de documentos**: el supervisor puede crear y publicar documentos para los empleados de su equipo.
- **Edición de documentos**: el supervisor puede modificar los metadatos de documentos existentes de su equipo.
- **Visibilidad de documentos privados**: el supervisor puede ver los documentos marcados como privados de los empleados de su equipo.

> **Importante:** La delegación de permisos no convierte al supervisor en manager. El supervisor con permisos documentales ampliados solo puede actuar sobre los empleados de su equipo asignado. No tiene acceso a la configuración global del módulo, a los documentos de otros equipos ni a la exportación masiva del archivo.

Para configurar la delegación de permisos:

1. Acceda al backoffice como Manager u Owner.
2. Navegue a la sección de **Gestión de empleados** o **Configuración de equipos**.
3. Seleccione el supervisor al que desea delegar permisos.
4. En la sección de permisos del supervisor, active las opciones documentales correspondientes.
5. Guarde los cambios.

## Permisos de eliminación

La eliminación de documentos es una acción irreversible que solo pueden realizar los usuarios con rol Manager u Owner. Antes de eliminar un documento, verifique:

- Si el documento tiene firma registrada, la eliminación borrará también el registro de trazabilidad de firma.
- Si el documento forma parte de un expediente que debe conservarse por obligación legal, no lo elimine aunque haya vencido su utilidad operativa inmediata.

Se recomienda marcar los documentos obsoletos como privados en lugar de eliminarlos, especialmente en documentos con firma o con relevancia laboral, para conservar el historial sin exponer el documento al empleado.

## Artículos relacionados

- [Qué es el módulo documental](30-que-es-el-modulo-documental.md)
- [Documentos privados](33-documentos-privados.md)
- [Acuse de recibo](35-firma-electronica.md)
- [Exportar documentos](38-exportar-documentos.md)
- [Subir y organizar documentos](31-subir-y-organizar-documentos.md)
