# Catálogo de casos — QA de CheckBiz360

Inventario de todo lo que la suite automática tiene que comprobar. Se construye desde el
sistema —endpoints, listeners, programadas y el recorrido real de los clientes—, no desde los
planes manuales de QA. El método está en [../plan-automatizacion.md](../plan-automatizacion.md).

## Cómo se lee

- Cada caso tiene un identificador `MÓDULO-NN-MM`: módulo, endpoint o elemento, caso. La
  prueba que lo cubre lleva ese identificador al principio del título, así que el informe se
  lee contra este catálogo sin traducir nada.
- El resultado esperado de cada caso es lo que hace el código **hoy**. Lo que parece un fallo
  va aparte, como *sospecha*. Si se confirma, pasa a [hallazgos.md](./hallazgos.md) con un
  identificador `HAL-NN`, y la prueba afirma lo correcto marcada como fallo esperado.
- Los actores —`PROP`, `ADMIN`, `OP_SUPERVISOR`, `AJENO`…— tienen nombres fijos, iguales
  aquí y en las pruebas: ver el §8 del plan.
- Cada fichero lleva al principio una nota de verificación: qué se ha comprobado contra el
  código o contra el entorno, y qué es solo lectura del código.

## Ficheros

| Fichero | Qué cubre | Prefijos | Estado |
|---|---|---|---|
| [recorrido-alta-a-fichaje.md](./recorrido-alta-a-fichaje.md) | El flujo normal completo, del registro al primer fichaje, tal como lo hacen el panel y la app | REC | Publicado, verificado por muestreo |
| [listeners-y-programadas.md](./listeners-y-programadas.md) | Triggers, receptores, tareas programadas y snapshots activos en desarrollo | LIS, PRG, SNP | Publicado, verificado por muestreo |
| [checkinbiz.md](./checkinbiz.md) | Autenticación de la app, fichajes, calendario, geocodificación | CHK | Publicado · análisis estático |
| [tareas.md](./tareas.md) | Tareas: permisos, interruptores, máquina de estados | TSK | Publicado · análisis estático |
| [documentos.md](./documentos.md) | Gestión documental | DOC | Publicado · análisis estático |
| [empleados-sucursales-empresas.md](./empleados-sucursales-empresas.md) | Empleados, sucursales, empresas y colaboradores | EMP, SUC, ENT, COL | Publicado · análisis estático |
| [equipos.md](./equipos.md) | Equipos: plantillas de responsabilidades, aplicar a una sucursal, guardar una sucursal | EQP | Publicado · con prueba (`52-equipos.spec.ts`) |
| [facturacion-informes-eventos.md](./facturacion-informes-eventos.md) | Facturación, informes, webhooks salientes y analítica | FAC, INF, EVT, ANA | Publicado · análisis estático |
| [mapa-migracion.md](./mapa-migracion.md) | Qué llama cada cliente, adónde va y qué queda fuera del HTTP | MAP | Publicado · análisis estático |
| [firma.md](./firma.md) | Firma del trabajador desde el móvil: clave y certificado, reto, acuse de recibo firmado con evidencia y acta | FIR | 27 casos (incluida la firma dentro del PDF), en verde contra dev el 09-oct-2026 |
| [hallazgos.md](./hallazgos.md) | Fallos y comportamientos dudosos, confirmados, con su corrección debajo | HAL | 35 de 37 corregidos o con código listo (14-sep-2026); 2 esperan decisión |
| [hallazgos-triaje.md](./hallazgos-triaje.md) | Los hallazgos clasificados por importancia, con su resolución y el orden de ataque | HAL | Auditoría y primera tanda de arreglos, 2026-09-13 |
