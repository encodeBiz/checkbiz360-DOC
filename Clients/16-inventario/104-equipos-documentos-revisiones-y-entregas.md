# Equipos: documentos, revisiones y entregas

Ante una inspección de trabajo hay dos preguntas que una empresa tiene que poder contestar con papeles: **¿se le entregó a cada trabajador su equipo de protección?** y **¿la máquina con la que trabaja ha pasado sus revisiones obligatorias?** El inventario guarda las dos pruebas junto al propio equipo, y avisa antes de que algo caduque.

Todo esto vale para el material que se **presta** (máquinas, vehículos, herramientas, EPIs con número de serie), no para el que se gasta.

---

## Los documentos de cada equipo

En la ficha de un equipo (**Inventario → Existencias → el equipo**) está la sección **Documentos**. Ahí se guardan su propiedad o factura, la declaración CE, el manual, el seguro, la ITV o la revisión obligatoria que le corresponda, las revisiones de mantenimiento y la evaluación de riesgos.

Hay dos formas de añadir uno:

- **Subir documento**: se elige el tipo, el título, la fecha de caducidad (en una revisión, la de la próxima), el resultado si es una revisión y quién la hizo.
- **Vincular existente**: si el documento ya está en **Gestión documental**, se busca y se vincula sin volver a subirlo.

En los dos casos, **Aplica a** decide si el papel es de **todos los ejemplares** (un manual, una declaración CE) o de **uno solo** (la ITV de una furgoneta, el seguro de una máquina).

También se puede hacer desde **Gestión documental**: al subir un documento, con el ámbito **Equipo**; o desde la ficha de un documento que ya existe, con **Vincular a un equipo**. Es siempre el mismo documento: se ve en los dos sitios, y **desvincularlo no lo borra**.

---

## Qué está en regla y qué no

Cada ejemplar dice si está en regla según sus papeles:

| Marca | Qué significa |
|---|---|
| **En regla** | Tiene papeles y ninguno está caducado |
| **Revisar papeles** (ámbar) | Algún papel caduca en los próximos 30 días, o un papel no obligatorio ha caducado |
| **Fuera de regla** (rojo) | La revisión obligatoria está caducada o su resultado fue «no apto» |

Un equipo sin papeles no lleva marca. Si se sube una revisión nueva, cuenta la más reciente: la antigua aparece como **Sustituido**.

La marca se ve en la lista de ejemplares de la ficha, en **Existencias** (cuántos están fuera de regla) y al elegir material para una tarea.

**Un equipo fuera de regla no se bloquea.** Retirarlo es una decisión de la empresa, no del programa. Pero al reservarlo para una tarea o entregarlo a una persona aparece el aviso con el motivo, y hay que marcar que se sabe para seguir. Queda anotado quién lo aceptó.

---

## Avisos antes de que caduque

Los responsables del almacén del equipo reciben un aviso cuando uno de sus papeles va a caducar en menos de 30 días, y otro cuando ha caducado o una revisión sale «no apto». Si el papel es de todos los ejemplares, el aviso llega a los responsables de la empresa. Cada aviso llega una sola vez.

---

## Entregar un equipo a una persona

Desde la ficha del equipo o desde Existencias, **Entregar** asigna un ejemplar a un trabajador junto con sus documentos: el modo de uso, el folleto del fabricante o el compromiso de responsabilidad. Los que el equipo tiene marcados **Con cada entrega** en su sección de documentos salen ya marcados, y en el momento se puede quitar alguno o subir otro. Solo pueden ir con la entrega los documentos visibles para trabajadores, que es como nacen los papeles de un equipo. El trabajador confirma que ha recibido el equipo y los documentos relacionados y que está de acuerdo con la entrega; el registro guarda qué documentos eran y en qué versión. La confirmación va **firmada con la clave de su móvil** y la plataforma la verifica, igual que en los documentos (ver [Acuse de recibo y firma electrónica](../05-gestion-documental/35-firma-electronica.md)); el informe «Equipos y EPIs» dice en su columna «Firma» si fue verificada. El trabajador recibe un aviso en el móvil y lo confirma en **Mi material** con su huella, su cara o el código de desbloqueo; si su móvil no tiene bloqueo, con la contraseña de su cuenta. También puede indicar que no lo ha recibido o que no está conforme, y quien lleva el almacén recibe el aviso.

Al devolverlo se indica cómo vuelve: en buen estado, con daños o no devuelto. Si vuelve con daños o no se devuelve, queda no disponible con ese motivo. El equipo pasa a estar en el almacén que lo recibe (ver [Dónde está cada equipo](./106-donde-esta-cada-equipo.md)). Lo que tiene cada trabajador se ve también en su ficha, en la pestaña **Material**.

---

## El informe «Equipos y EPIs»

Se genera desde **Informes**, en Excel, y tiene dos hojas:

- **Entregas**: qué se entregó a cada trabajador, con qué documentos y en qué versión, quién lo entregó, qué confirmó, cuándo y cómo, y cómo lo devolvió.
- **Equipos y revisiones**: cada ejemplar con su estado, quién lo tiene ahora y cada papel con su tipo, resultado, caducidad y estado.

Es lo que se presenta ante una inspección. Sin el inventario contratado, el informe aparece en rojo en la lista y explica qué hay que hacer para tenerlo.

---

## Artículos relacionados

| Artículo | Descripción |
|---|---|
| [Qué es el inventario](./100-que-es-el-inventario.md) | Qué problemas resuelve |
| [Existencias, almacenes y entradas](./101-existencias-almacenes-y-entradas.md) | Alta del material y de cada ejemplar |
| [Tipos de informe](../11-informes-y-exportacion/76-tipos-de-informe.md) | Todos los informes de la plataforma |
