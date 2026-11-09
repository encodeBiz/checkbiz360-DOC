# 09 — Guion de QA de la cartera (Fases 0–5) en staging

**Fecha:** 2026-11-05
**Entorno:** staging (`api-staging.checkbiz360.com`, Firebase `dev-encodebiz`). Nunca producción.
**Empresa:** «QA qa-cartera-20261105» (`U25wR3YB91yMGS70Y2dz`), creada para esta QA por el alta real
(suscripción, calendario abierto todo el día, sucursales, personas). Sucursales «QA Sede Badalona»
(`CWbaLhFhWmanup5DrsKJ`) y «QA Obra Diagonal» (`qTgflNA1sxTOdcq2vmo8`).
**Accesos:** `encodebiz-api/secrets/qa-cartera-accesos.md` (no se commitea): propietario, gestor
de la Sede, una trabajadora con tareas y otra sin tareas, cada una con su contraseña. Correos del
simulador de SES: no llega nada a ningún buzón.

## Cómo se arranca

| Pieza | Cómo |
|---|---|
| API | En staging (`b06ecd4` o posterior): `customers`, `tasks`, `documents`, `merlin` |
| Panel | Staging del panel es el portátil: rama `feat/cartera-de-clientes`, `npx next dev -p 3100` con `.env.development` apuntando a staging (incluye `NEXT_BACKEND_URI_CONTRATOS_LEER`). Está levantado en http://localhost:3100 |
| App | `checkbiz360` `develop` (`2a53347`): `flutter run -t lib/main_development.dart --flavor development --dart-define=ENVIRONMENT=development` |

## Lo que ya está comprobado al montarlo (2026-11-05, por la API)

- Las cuatro cuentas entran con su contraseña; las tres de la app pasan el login y la validación.
- La trabajadora con la «QA Visita SAD» recibe la ficha de la usuaria y a la hija; **el contrato no**.
- La otra trabajadora, sin esa tarea: 403 `customers/forbidden_for_task`.
- El gestor ve los dos contratos de QA Eventos **sin importe ni coste** y no puede crear (403); el
  propietario sí.
- «QA Limpieza escalera» tomó sola el único contrato de la comunidad; «QA Montaje stand» lleva el
  elegido; «QA Revisión mantenimiento» va sin contrato porque QA Eventos tiene dos vigentes.

## Los datos

| Qué | Para probar |
|---|---|
| **QA Comunidad Diagonal**: dirección, contacto visible y otro no, notas de campo en Markdown, notas de gestión, un presupuesto (gestores) y un contrato vigente «Limpieza comunidad 2026» | Ficha, notas, contactos, un único contrato → la tarea lo toma sola |
| **QA Usuaria SAD**: persona, ficha visible para trabajadores, contrato solo gestores que **vence en 12 días** | El rojo del vencimiento, lo que ve la trabajadora y lo que no |
| **QA Eventos S.A.**, asignado a las **dos** sucursales: «Mantenimiento anual» (sin fin) y «Stand feria» (con PDF) | El selector de contrato en la tarea, la tarjeta, el total, un cliente en dos sucursales |
| Tareas de la trabajadora: «QA Limpieza escalera», «QA Visita SAD», «QA Tarea sin cliente» (mañana) | La app |
| Sin asignar: «QA Montaje stand» (Obra Diagonal), «QA Revisión mantenimiento» (Sede) | Contrato elegido y sin elegir |

## Copia en Neteges Demo (2026-11-07)

Los mismos datos, sembrados también en **Neteges Demo** (`318Ey5ZHBMeqm5fsQ0Md`) para probar con la
cuenta de Jose en panel y app, con el script `seed-neteges-clientes.sh` del scratchpad de la sesión.
Clientes QA Comunidad Diagonal `K0fP3RPcm1aEE0OEgB11`, QA Usuaria SAD `MZqFshKtwpRKbkJxG9c0` y QA
Eventos S.A. `dS2KRFWRtlodeb2bXyOL` (este en Oficina Badalona y Delegación Madrid, con «QA
Mantenimiento anual» y «QA Stand feria» vigentes a la vez). Tareas de Jose (empleado
`Delui9VnI5OAyNHrSuKN`) el lunes 9-nov: «QA Limpieza escalera», «QA Visita SAD», «QA Tarea sin
cliente»; sin asignar, «QA Montaje stand» (10-nov, con contrato) y «QA Revisión mantenimiento»
(11-nov, sin contrato). **Ojo con A2:** Jose es owner operativo de Badalona, y hasta que entre el
nivel «Administración» (TDR-002 del documental) la hoja del cliente en la app le enseña también el
contrato. Para A2 tal como está escrito, con una trabajadora sin mando.

## Panel

| # | Paso | Resultado esperado |
|---|---|---|
| P1 | Menú «Clientes» | Los tres clientes QA; la búsqueda «diagonal» encuentra la comunidad; el filtro por sucursal funciona |
| P2 | Ficha de **QA Comunidad Diagonal** | Dirección bajo el nombre; notas de campo con formato; contactos con el ojo solo en la presidenta; notas de gestión abajo |
| P3 | Editar la comunidad: cambiar la dirección con el mismo campo de las tareas, guardar | La dirección nueva sale en la ficha; sin radio en el formulario |
| P4 | Ficha de **QA Usuaria SAD**, bloque Documentos | La ficha (todos) y el contrato (gestores) **en rojo**, con «vence el…»; la cabecera avisa de un contrato que vence |
| P5 | Subir un documento de tipo «Contrato con el cliente» | «Visible para» pasa sola a Gestores. Marcar Trabajadores → **aviso en rojo**. Se puede guardar igual |
| P6 | Ficha de **QA Eventos S.A.**, bloque Contratos | Dos tarjetas con importe, horas 0 y «Ninguna tarea…» o una tarea; el total del cliente arriba; previsión «aún no hay suficientes contratos cerrados (0 de 5)» |
| P7 | «Nuevo contrato» → elegir «Contrato stand feria» (o «Subir PDF» con uno propio) → «Leer el PDF» | «Leer el PDF» se activa al haber documento elegido; un PDF subido queda como contrato del cliente, solo gestores, y elegido. Sale el **aviso de la IA**; el formulario se rellena: 8 400 €, 1 y 12 de diciembre, 96 h, complejidad; cada campo con «Del documento: …» debajo. Cancelar |
| P8 | «Nuevo contrato» sin PDF, con importe 1.000 y horas estimadas | Se crea; el total del cliente sube y dice «contratado» (no «cobrado»); la tarjeta pone «Horas planificadas / hechas / previstas» con las tres cifras |
| P9 | Editar un contrato: cambiar las horas estimadas | Se guarda; la primera estimación no cambia (se ve en el historial de la API) |
| P10 | Cerrar un contrato y reabrirlo | Pide confirmación; cerrado sale con su fecha y sin previsión. Con él cerrado, editar y guardar una tarea suya: se guarda y lo conserva. Reabrir lo devuelve |
| P11 | Borrar «Stand feria» | **No deja**: tiene una tarea. Mensaje claro. Borrar uno sin tareas y con PDF: el PDF desaparece también de Documentos |
| P12 | Nueva tarea en «QA Sede Badalona», elegir **QA Eventos S.A.** | Check «usar la dirección del cliente» marcado; **aparece «Contrato»** (dos vigentes), sin preseleccionar |
| P13 | Nueva tarea, elegir **QA Comunidad Diagonal** | **No aparece «Contrato»**; al guardar, el detalle de la tarea dice «Limpieza comunidad 2026» |
| P14 | Editar «QA Revisión mantenimiento» y elegir «Mantenimiento anual» | Se guarda; el detalle muestra el contrato; la tarjeta del contrato cuenta una tarea |
| P15 | Cambiar el cliente de una tarea con contrato | El contrato se suelta; si el nuevo cliente tiene uno solo, lo toma |
| P16 | Detalle de «QA Visita SAD» | Enlace al cliente; bloque de documentos del cliente en solo lectura, **solo con lo visible para trabajadores**: la ficha sí, el contrato no |
| P17 | Lista de tareas, filtro por cliente | Solo las del cliente elegido |
| P18 | Gestión documental, filtro ámbito «Cliente» | Salen los documentos QA con el nombre del cliente. **Automatizado:** CLI-18 (`qa/tests/con-datos/59-cartera-clientes.spec.ts`) |
| P19 | Con la cuenta del **gestor** (si el panel le deja entrar como responsable; si no, comprobado ya por la API): ficha de QA Eventos | Ve contratos y horas, **sin importe, coste ni margen**, sin botones; texto «solo propietarios y administradores». **La API, automatizada:** CLI-19; la pantalla, a mano |
| P20 | Importar cuadrante de una persona | Sale el **aviso de la IA** junto al fichero. Solo pantalla: a mano |

## App (trabajadora)

Con la cuenta de la **trabajadora con tareas**: ya tiene asignadas «QA Visita SAD», «QA Limpieza escalera» y «QA Tarea sin cliente».

| # | Paso | Resultado esperado |
|---|---|---|
| A1 | Detalle de «QA Visita SAD» | «Cliente: QA Usuaria SAD» y «Ver datos del cliente» |
| A2 | Ver datos del cliente | Notas de campo, la hija con su teléfono (se puede llamar), la **ficha** en documentos; **el contrato no sale** |
| A3 | Abrir la ficha | Se descarga y se abre |
| A4 | Una tarea sin cliente | Igual que siempre, sin bloque de cliente |
| A5 | Fichar contra la tarea | La valla es la dirección de la usuaria |
| A6 | Entrar con la **otra trabajadora** | No ve las tareas QA ni los datos de ningún cliente |

## Rentabilidad con datos reales (opcional esta noche)

Empezar y terminar «QA Montaje stand» desde la app, o fichar con ella en horario por tareas. Al
recargar la ficha de QA Eventos, la tarjeta de «Stand feria» enseña horas, su fuente («del reloj
de sus tareas» o «de los fichajes») y, si la persona tiene precio en su puesto, el coste en bruto
y el margen.

## Si algo falla

Anotar el número del paso, la cuenta, la hora y lo que salió. Los errores de la API llegan con
`code` (`customers/…`, `task/contract_…`); el log está en el VPS:
`docker compose -p encodebiz-api-dev -f docker-compose.staging.yml logs --since 30m customers tasks merlin`.

## Limpieza después de la QA

Todo está en una empresa propia, así que no ensucia a nadie: se puede dejar para la siguiente
ronda. **Ojo:** `node qa/scripts/limpiar.mjs --apply` borra toda empresa de QA de más de un día
con correo del simulador, y esta lo es: no lanzarlo mientras dure la QA. Para quitarla del todo, `qa/scripts/limpiar.mjs` busca lo marcado `qa-cartera-20261105`
(empresa, usuarios de Auth); los documentos del cliente están además en el bucket
`dev-encodebiz.firebasestorage.app` bajo `documents/entities/U25wR3YB91yMGS70Y2dz/`, y los
contratos en `customer_contracts`, `contract_events` y `contract_forecasts` de `encodebiz_staging`.
