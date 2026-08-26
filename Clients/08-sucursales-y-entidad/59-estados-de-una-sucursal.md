# Estados de una sucursal

En CheckBiz360, cada sucursal tiene un estado que determina si los empleados asignados pueden operar con normalidad o si el centro está suspendido temporalmente. Comprender el significado de cada estado y las consecuencias de cambiarlo es fundamental para evitar interrupciones no planificadas en el registro de asistencia.

## Estados posibles

Una sucursal puede encontrarse en uno de los dos estados siguientes:

### Activa

Es el estado normal de operación. Cuando una sucursal está activa:

- Los empleados asignados pueden fichar desde la app sin restricciones relacionadas con el estado de la sucursal.
- El calendario efectivo y los horarios configurados están en vigor.
- Los informes y análisis incluyen los datos de esa sucursal.
- Las notificaciones y alertas relacionadas con la sucursal funcionan con normalidad.

Toda sucursal recién creada queda en estado activo por defecto.

### Inactiva

Una sucursal inactiva está suspendida temporalmente. Sus efectos son los siguientes:

- Los empleados que intenten fichar desde la app en esa sucursal recibirán un error indicando que la sucursal no está disponible.
- No es posible crear nuevos registros de asistencia vinculados a esa sucursal desde la app.
- Los responsables siguen pudiendo acceder a la sucursal desde el backoffice para consultar datos históricos y modificar la configuración.
- Las asignaciones de empleados a la sucursal se conservan intactas.
- El histórico de fichajes, jornadas y documentos asociados a la sucursal permanece íntegro y es consultable.

> **Aviso:** Inactivar una sucursal tiene efecto inmediato. Si hay empleados que están intentando fichar en el momento del cambio, sus fichajes serán rechazados. Planifique los cambios de estado fuera del horario de trabajo del personal afectado o comuníquelo con antelación.

## Diferencia entre inactivar y eliminar

Inactivar y eliminar son operaciones distintas con consecuencias muy diferentes:

| Acción | Efecto sobre los datos | Reversibilidad | Recomendada para |
|---|---|---|---|
| **Inactivar** | Los datos históricos se conservan íntegramente | Reversible en cualquier momento | Cierres temporales, remodelaciones, reestructuraciones |
| **Eliminar** | Los datos de la sucursal quedan desvinculados de la estructura activa | Irreversible | Sucursales creadas por error sin datos asociados |

> **Aviso:** CheckBiz360 no permite eliminar sucursales que tengan fichajes, jornadas o documentos asociados. Si necesita dar de baja definitivamente una sucursal con datos históricos, la operación correcta es inactivarla y solicitar al equipo de soporte la desvinculación definitiva si fuera necesaria para cumplimiento de normativa de protección de datos.

En la práctica, la inmensa mayoría de los cierres de sucursal —ya sean temporales o definitivos— deben gestionarse mediante la inactivación, no mediante la eliminación.

## Cómo cambiar el estado de una sucursal

### Inactivar una sucursal activa

1. Acceda al backoffice web y navegue a **Sucursales**.
2. Localice la sucursal en el listado. Las sucursales activas se muestran con un indicador verde.
3. Pulse el icono de edición o el nombre de la sucursal para abrir su ficha.
4. En el campo **Estado**, seleccione **Inactiva**.
5. El sistema mostrará un aviso con el número de empleados asignados a la sucursal que se verán afectados.
6. Confirme la operación y pulse **Guardar cambios**.

### Reactivar una sucursal inactiva

1. Acceda a **Sucursales**.
2. En el listado, active el filtro para mostrar sucursales inactivas si no aparecen por defecto.
3. Pulse el icono de edición de la sucursal que desea reactivar.
4. En el campo **Estado**, seleccione **Activa**.
5. Pulse **Guardar cambios**.

La reactivación es inmediata. Los empleados asignados podrán fichar de nuevo en cuanto el cambio se haya guardado.

## Impacto en el histórico de datos

El estado de una sucursal no altera ningún dato histórico. Independientemente de que una sucursal esté activa o inactiva:

- Los fichajes registrados antes del cambio de estado permanecen en el sistema con su información original.
- Los informes de periodos anteriores reflejan los datos reales de esos periodos.
- Los documentos y tareas asociados a la sucursal siguen siendo accesibles para los responsables desde el backoffice.
- Los cálculos de coste y horas trabajadas de periodos pasados no se ven afectados.

El estado de una sucursal es, en esencia, un interruptor operativo que controla si los empleados pueden seguir generando nuevos registros desde esa sucursal. No tiene ningún efecto retroactivo.

---

> **Nota de rol:** El cambio de estado de una sucursal está disponible para los roles **Owner** y **Manager** con permisos de administración de organización. El rol **Supervisor** puede consultar el estado de las sucursales a las que está asignado, pero no puede modificarlo.

## Artículos relacionados

- [Crear y gestionar sucursales](57-crear-y-gestionar-sucursales.md)
- [Configuración avanzada de sucursal](58-configuracion-avanzada-de-sucursal.md)
- [Asignar empleados a sucursales](60-asignar-empleados-a-sucursales.md)
- [Vista global multi-sucursal](62-vista-global-multi-sucursal.md)
