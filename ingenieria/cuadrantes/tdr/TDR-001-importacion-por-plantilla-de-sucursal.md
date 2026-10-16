# TDR-001 — Importación del cuadrante por plantilla de sucursal

**Fecha:** 2026-10-15
**Estado:** Decidido en conversación e implementado el 2026-10-15 en `feat/cuadrantes-plantilla` de `encodebiz-api` y de `encodebiz-front-saas`, sin fusionar a `develop`. Lo comprobado y lo que queda, en el §11.
**Componente:** `encodebiz-api` — `merlin` (`soporte/cuadrantes/plantilla`); panel `checkinbiz/branch/[id]` (ficha de la sucursal, pestaña de calendario)
**Decisiones de referencia:** [README](../README.md) de la lectura de cuadrantes, [ADR-001](../adr/ADR-001-la-sombra-por-lista-blanca.md), y la importación de inventario por plantilla ([TDR-007 de inventario](../../inventario/tdr/TDR-007-importacion-masiva-por-plantilla.md)), de la que esto es calco

---

## 1. El dolor y la decisión

La lectura por modelo (README) hace una cosa que ningún otro camino hace: entender el impreso
que saca el ERP de cada cliente, sea el que sea. A cambio tiene dos costes que se notan cada
lunes:

- **Tarda uno o dos minutos por documento**, y la pantalla se queda esperando.
- **Entra de uno en uno**: una persona, una semana, desde la ficha de cada empleado. Una
  empresa de veinte auxiliares son veinte subidas, veinte lecturas, veinte confirmaciones de
  columnas y veinte firmas.

Decidido con Jose el 2026-10-15:

1. **La importación pasa a ser por plantilla**, como la de inventario: un Excel que se baja, se
   rellena y se sube, y el servidor lo lee sin modelo. Es un trámite, no una interpretación.
2. **La plantilla es de la sucursal y lleva a toda su gente**: una pestaña por empleado,
   generadas por el servidor con el nombre de cada persona. Un fichero por semana, **una subida
   para toda la plantilla**. «Una hoja por empleado, así subimos el cuadrante de toda una
   plantilla, y no ir empleado por empleado».
3. **El lector por modelo no se quita.** Se queda donde está —la ficha del empleado— para el
   documento que no es la plantilla: el PDF que imprime ServiSAD para DomusVi y que nadie
   teclea. Lo que se quita es que ése sea el único camino.

Lo que sigue a la lectura **no cambia**: la revisión contra el calendario, la geocodificación de
cada dirección, la propuesta con su identificador, la firma, la simulación por defecto y las
tareas idempotentes son las mismas funciones. Cambia quién produce la lectura: un lector de
columnas fijas en vez del modelo. Con eso desaparecen, en este camino, la sombra (nada sale del
servidor, así que no hay nada que tachar), el paso de confirmar columnas, los presets del
cliente, la «confianza» del modelo y la red de totales impresos: cada fila se lee entera o es un
error con su motivo y su número de fila.

## 2. La plantilla

Se baja desde la ficha de la sucursal, para una semana (lunes a domingo). Es un Excel con:

**Una primera hoja, «Semana»**, que no se lee al subir: el nombre de la sucursal, la semana, cuatro
líneas de cómo rellenarla y la lista de la gente con la pestaña de cada uno.

**Una pestaña por persona de la sucursal** —todas las fichas que no estén despedidas, pendientes
ni de baja—, con el nombre de la persona como título de la pestaña. Dentro:

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 1 | Ana López García | ana@empresa.com | *(identificador, en gris)* | | | | |
| 2 | **Fecha \*** | **Hora inicio \*** | **Hora fin \*** | **Cliente** | **Dirección** | **Trabajo** | **Viaje (min)** |
| 3 | 13/10/2026 | 08:00 | 10:00 | ELIMINAR Carmen Ruiz | Calle Mayor 12, 3ºB, Madrid | Limpieza del hogar | 15 |
| 4 | 14/10/2026 | 10:15 | 12:15 | ELIMINAR Luis Pérez | Avenida de la Paz 4, Madrid | Acompañamiento | 10 |

- **La fila 1 identifica a la persona.** Lleva su nombre, su correo y su identificador. Es lo que
  permite que el cliente renombre la pestaña, la copie o la reordene sin que se pierda de quién
  es. La hoja «Semana» pide no borrarla.
- **Una fila por trabajo.** Fecha, hora de inicio y de fin son obligatorias. Cliente, dirección y
  trabajo son texto libre, y la dirección conviene traerla: es la valla de la tarea; sin ella la
  tarea se crea igual y se ficha desde cualquier sitio, como en el camino del modelo. «Viaje» son
  los minutos de desplazamiento hasta ese trabajo.
- **Dos filas de ejemplo por pestaña**, con las fechas del lunes y el martes de esa semana y la
  palabra `ELIMINAR` delante del cliente, en gris. Cualquier fila con una celda de texto que
  empiece por la palabra del idioma (ELIMINAR, DELETE, EXCLUIR, LÖSCHEN, SUPPRIMER) se ignora y se
  enseña como ignorada: si el cliente no las borra, no aparece una «Carmen Ruiz» de ejemplo en el
  móvil de nadie.
- **Una pestaña vacía deja a esa persona sin tocar.** No es «esa semana no trabaja»: es que no se
  ha dicho nada de ella. Una pestaña con trabajos es la semana entera de esa persona: los días de
  la semana que no traen ninguna fila quedan libres.
- **Solo Excel.** Las pestañas no caben en un CSV. La subida de un PDF, un CSV o un `.xls` de
  Excel 97 devuelve un error con nombre que dice que eso no es la plantilla y de dónde se baja.
  Las cabeceras se aceptan en los cinco idiomas del panel y con los nombres habituales (`Día`,
  `Entrada`, `Salida`, `Desde`, `Hasta`, `Usuario`, `Domicilio`, `Servicio`…).

**Formatos que se leen.** La fecha como celda de fecha de Excel, `AAAA-MM-DD`, `DD/MM/AAAA` o
`DD-MM-AAAA`; sin año es un error, no se adivina. La hora como celda de hora de Excel, `8:00`,
`08:00`, `8.00`, `8h`, `8h30` o `08:00:00`. El viaje como número; `15'` y `15 min` se leen como 15.

## 3. El flujo: subir, ver, confirmar

> **La subida no escribe nada. Primero enseña, después aplica.** El mismo patrón que la lectura
> por modelo y que la importación de inventario.

Subir el fichero produce un **lote** con una propuesta por persona —la misma `Propuesta` de la
lectura por modelo, guardada en `cuadrante_proposals`, con su `puedeAplicar`, sus hallazgos y sus
servicios—, y el lote las agrupa:

| Estado de una pestaña | Significado |
|---|---|
| `lista` | Todas las filas se han leído y la revisión no bloquea: se aplicará. |
| `bloqueada` | Alguna fila no se ha podido leer, o la revisión bloquea (un día con trabajos que para esa persona es festivo o ausencia, sin zona horaria…). Se enseña el motivo, con la fila. **No se aplica esa persona; las demás sí.** |
| `vacía` | Sin filas de datos (o solo los ejemplos). No se toca a esa persona. |
| `desconocida` | La pestaña no corresponde a nadie de la sucursal (§4). Se enseña y se sigue. |

Una pestaña con errores bloquea a **su** persona entera, no fila a fila como en inventario: media
semana es peor que ninguna —la franja del día saldría de las filas que sí se leyeron, y faltaría
un trabajo en el móvil sin que nadie lo echara en falta—. Se corrige el fichero y se vuelve a
subir; volver a subir no duplica nada (§6).

La propuesta del lote lleva por persona: nombre, pestaña, estado, trabajos, horas de servicio,
días con trabajo, y los hallazgos (bloqueantes y avisos) de su revisión, ya con nombres y
direcciones de verdad porque es el cliente mirando sus propios datos.

## 4. Cómo se reconoce a la persona de cada pestaña

En este orden:

1. **El identificador de la fila 1** (cualquier celda de la fila 1 que sea el id de un empleado de
   la sucursal). Es lo que pone la plantilla, y sobrevive a renombrar la pestaña.
2. **Un correo en la fila 1** que sea el de un empleado de la sucursal. Es cómo se añade a alguien
   que no estaba al bajar la plantilla: se copia una pestaña, se cambia la fila 1.
3. **El título de la pestaña**, comparado con el nombre normalizado de los empleados de la sucursal
   (`normalizeText` del buscador), si casa con uno solo.
4. Lo demás es `desconocida`. Dos pestañas para la misma persona son un error de las dos: no se
   sabe cuál manda.

La hoja «Semana» y cualquier hoja sin fila de cabeceras reconocible se saltan sin decir nada.

## 5. Lo que se comprueba antes de escribir

Lo que ya comprobaba la revisión de la lectura por modelo, sobre los valores de verdad:

| Comprobación | Si falla |
|---|---|
| Una fila sin fecha, sin hora, con hora de fin anterior a la de inicio, o con fecha fuera de la semana del fichero | **Bloquea esa persona**, con el número de fila |
| Dos trabajos de la misma persona a la misma hora del mismo día | **Bloquea esa persona** (compartirían `externalRef`) |
| Un día con trabajos que en el calendario es festivo o tiene una ausencia | **Bloquea esa persona** |
| Sin zona horaria para esa persona ni su centro | **Bloquea esa persona** |
| Dos trabajos que se solapan | Avisa |
| Trabajos sin dirección | Avisa, una vez, agrupado |
| Viaje antes del primer trabajo mayor que la tolerancia de entrada | Avisa |
| Días de la semana sin trabajos | Se dice una vez («sábado y domingo quedan libres»), no por día |

La semana del fichero es la del lunes de la fecha más temprana que trae. Dos semanas en un fichero
no caben: el horario que se escribe es un patrón semanal (`overridesSchedule`), no un calendario
por fecha.

Lo que no aplica aquí y se desactiva en la revisión cuando la lectura viene de la plantilla: la
red de totales impresos (no hay pie), la heurística de columnas cambiadas (las columnas son fijas)
y la comparación entre lo que dijo el modelo y lo calculado (no hay modelo).

## 6. Qué escribe «confirmar»

Confirmar el lote aprueba, **una por una y por las mismas funciones que la lectura por modelo**,
las propuestas en estado `lista`: `aprobar` → `aplicar`, que escribe el horario de la persona
(`overridesSchedule`, reemplazando la semana anterior) y crea una tarea por trabajo contra
`POST /api/v1/tasks/system`, con la dirección como valla y el radio de 150 m por defecto.

- **Idempotente.** Las tareas llevan `externalRef = cuadrante:{employeeId}:{fecha}:{inicio}`, así
  que confirmar dos veces, o volver a subir el fichero corregido, no duplica el trabajo de nadie.
- **Se aplica en segundo plano.** Veinte personas por dieciséis trabajos son más de trescientas
  tareas, cada una con su geocodificación: pasa del minuto. «Confirmar» pasa el lote a *aplicando*
  en una transacción —dos clics no lanzan dos aplicaciones—, responde `202` y aplica de dos en dos
  personas, apuntando el avance. El panel pregunta por el lote hasta que termina; cerrar la
  ventana no lo para. Un lote *aplicando* que lleva cinco minutos sin dar señales se da por
  muerto y se puede volver a confirmar: lo ya aplicado no se repite.
- **La firma** queda en cada propuesta (`aprobacion: {quien, cuando}`) y en el lote.
- **El lote queda registrado** en `entities/{e}/cuadrante_lotes/{id}`: quién, cuándo, nombre del
  fichero, sucursal, semana, propuesta por persona y resultado por persona. Lleva nombres y
  direcciones de clientes del cliente, así que —como `cuadrante_proposals`— **solo lo escribe y lo
  lee el servidor**: las dos colecciones entran en `soloServidor` de las reglas de Firestore.

**Lo que no hace, heredado del camino del modelo:** al resubir una semana corregida, una tarea que
ya no está en el fichero no se retira sola, y una cuyo inicio cambió es otra tarea (cambia el
`externalRef`). Es la misma limitación que ya tenía la lectura por modelo y sigue abierta en el
README. Con una subida por sucursal esto va a pasar más, y se decidirá aparte.

**Límites:** 2 MB por fichero, 1.000 filas por pestaña. Sin límite de plan.

## 7. Rutas y permisos

Cuelgan del mismo router de cuadrantes, así que llegan por las dos puertas —el panel con token de
Firebase y `requireEntityWriter`, y el backoffice y el CLI con la API key—:

```
GET  /plantilla?entityId&branchId&semana&lang         → {filename, mimeType, base64}
POST /lotes   {entityId, branchId, nombre, ficheroBase64, lang}   → 201 {ok, lote}
GET  /lotes/:id?entityId                              → {ok, lote}  (estado, avance, resultado)
POST /lotes/:id/aprobar   {entityId, aplicar: true}   → 202 {ok, lote} (aplicando) · 200 si ya estaba aplicado
POST /lotes/:id/descartar {entityId}                  → {ok, lote}
```

- `semana` es el lunes (`AAAA-MM-DD`); sin él, el próximo lunes en la zona horaria de la sucursal.
- El fichero viaja en base64 dentro de JSON por lo mismo que en inventario: el proxy del panel solo
  transporta JSON. La ruta ya lee cuerpos de 8 MB; el `location /api/v1/gpt/` de nginx no fijaba
  `client_max_body_size` (1 MB por defecto) y pasa a 4 MB, como el de inventario.
- `aprobar` sin `aplicar: true` simula, como en todo lo que escribe aquí.
- Errores con nombre: `plantilla_no_reconocida` (no es un Excel de plantilla), `fichero_ilegible`
  (`.xls` de Excel 97: guardarlo como `.xlsx`), `fichero_vacio`, `fichero_demasiado_grande`,
  `sucursal_no_encontrada`, `lote_no_encontrado`, `lote_cerrado`.

## 8. El panel

En la ficha de la sucursal, pestaña de calendario, un bloque «Cuadrante semanal de la plantilla»
con la explicación corta y un botón. El diálogo (`ImportarCuadranteSucursalModal`, cargado aparte)
sigue cuatro pasos, calcados del de inventario:

1. **El fichero**: la semana (un selector de fecha que salta al lunes; por defecto el próximo),
   «Descargar plantilla» y el fichero.
2. **La propuesta**: los totales en pastillas (personas listas, bloqueadas, vacías, pestañas no
   reconocidas; trabajos a crear) y una tabla por persona con su estado, sus trabajos y horas, y
   sus hallazgos. Lo que pide atención, primero.
3. **El avance**, por personas, que se puede cerrar sin parar.
4. **El resultado**, por persona: tareas creadas y errores.

El modal de la ficha del empleado («Subir un cuadrante») se queda como está, para el documento
que no es la plantilla.

## 9. Fuera de la primera versión

- **Retirar las tareas que ya no están** al resubir una semana (§6).
- **Leer un Excel plano de varias personas** con una columna de empleado (lo que exporta un ERP).
  Si llega un caso, es un segundo lector sobre el mismo lote.
- **Semanas ya empezadas** con días fichados: hoy se reescriben igual, como en el camino del modelo.
- **Elegir qué personas aplicar** dentro de un lote: se aplican todas las listas.

## 10. Criterio de éxito

Un cliente baja la plantilla de una sucursal de veinte personas para la semana que viene, rellena
en Excel los trabajos de doce de ellas, deja ocho pestañas vacías y sube el fichero. Ve en una
pantalla doce personas listas con sus trabajos y horas, ocho sin tocar, y si una tiene un día de
vacaciones con trabajos, la ve bloqueada con el motivo y las otras once siguen. Confirma, ve el
avance, y al terminar cada una de las doce tiene su horario de la semana y sus tareas con su
dirección en el móvil. Sube el mismo fichero otra vez y no se duplica nada. Todo sin que el modelo
intervenga y sin esperar más que lo que tarda en geocodificar.

## 11. Comprobado el 2026-10-15, y lo que queda

- **Parte pura** (plantilla, lectura, revisión y propuesta, sin Firestore): 15 comprobaciones
  en verde con `npm test -w services/merlin` —las cinco plantillas releídas con sus ejemplos
  ignorados; fechas, horas y viaje como los escribe una persona (celdas de Excel incluidas);
  cabeceras en cinco idiomas y con los nombres de un ERP; una pestaña lista con sus siete días;
  filas mal escritas que bloquean a su persona con el número de fila mientras las demás siguen;
  dos trabajos a la misma hora; la persona reconocida por identificador, por correo y por título;
  dos pestañas de la misma persona; lo que no es la plantilla rechazado con su nombre; la revisión
  sin totales y con los días libres agrupados; una ausencia que bloquea; y la propuesta armada
  con nombres, direcciones, `externalRef` y el horario semanal—. `tsc` de `merlin` en verde.
- **Panel**: tipos y lint en verde (el modal, el bloque en la pestaña de calendario de la
  sucursal, el servicio, el proxy y los textos en cinco idiomas).
- **No se ha probado contra dev ni en un navegador**: esta sesión no pudo leer Firestore de
  dev. Falta subir una plantilla real desde el panel de staging, ver la propuesta y confirmar
  sobre una sucursal de pruebas.

**2026-10-16 — la regla de §6 no cerraba nada.** `soloServidor` solo miraba la colección raíz y
estas cuelgan de `entities/{e}`. Corregida (se cierra si cualquier tramo de la ruta es una colección
cerrada) y probada con el emulador, 26 casos en verde (`qa/reglas/`). El pase a producción, con
todo lo que lleva, está en
[deployment-prod/2026-10-cuadrantes-plantilla.md](../../../deployment-prod/2026-10-cuadrantes-plantilla.md).

Pendiente, en este orden:

1. Probar en local contra dev o en staging (arriba) y fusionar las dos ramas a `develop` y,
   cuando sea una versión usable, a `staging`.
2. Desplegar las reglas de Firestore a dev y después a prod (`cuadrante_proposals` y
   `cuadrante_lotes` pasan a `soloServidor`): `firebase deploy --only firestore:rules --project
   dev-encodebiz`. Hoy las dos colecciones se leen desde el navegador con el comodín heredado.
3. El `client_max_body_size 4m` del `location /api/v1/gpt/` llega con el despliegue del nginx
   de cada entorno.
4. Lotes y propuestas abandonados: caducan a los treinta días por `expiraEn`, que barre cada
   subida nueva de ese cliente; como en inventario, hará falta un barrido si se acumulan.

