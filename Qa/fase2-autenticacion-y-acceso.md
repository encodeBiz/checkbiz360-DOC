# QA — Fase 2: Autenticación y acceso. Lectura técnica y automatización

> Qué se puede automatizar del plan «FASE 2 — Autenticación y acceso», qué se queda en
> navegador o en móvil, y —lo más importante— **qué casos van a fallar hoy y por qué**.
>
> Se apoya en [automatizacion-qa-staging.md](./automatizacion-qa-staging.md), que explica
> dónde corre la suite y con qué reglas.
>
> Fecha: 2026-08-26 · Estado: hallazgos pendientes de triaje antes de ejecutar la fase

---

## 1. La conclusión, en corto

De los 40 casos QA-AUTH-001 a 040, alrededor de **22 tienen un núcleo automatizable**: la
parte que decide quién puede hacer qué. El resto es formulario, pantalla, correo o
teléfono, y se queda en manos de personas.

Pero eso no es lo importante de esta fase. Al contrastar el plan con el sistema han
aparecido **cuatro comportamientos que hacen fallar casos concretos del plan**, y tres de
ellos son de seguridad. No son fallos de QA ni de la automatización: son cosas que la
Fase 2 está diseñada precisamente para encontrar, y las ha encontrado antes de ejecutarse.

La recomendación es triarlos primero. Ejecutar la fase sabiendo que va a dar rojo en sitios
conocidos gasta el tiempo de QA en confirmar lo que ya sabemos.

---

## 2. Hallazgos que condicionan la fase

Todo lo que sigue está observado leyendo el código de los servicios y de las funciones.
**Ninguno está confirmado todavía con una petición real contra staging**; ese es el primer
trabajo de la automatización, y por eso conviene hacerlo antes de que QA ejecute a mano.

### H1 — La validación de empleado es pública y su token no va firmado

El arranque de la app llama a un endpoint público de validación al que se le entrega un
token que es, literalmente, un JSON codificado en base64 con el identificador del empleado
y el de la empresa. No lleva firma ni nada que impida fabricarlo: el servidor lo
descodifica, comprueba que ese empleado existe y **devuelve un token de sesión válido**.

Consecuencia: quien conozca —o acierte— un par identificador de empleado + identificador de
empresa obtiene una sesión de trabajador sin contraseña.

Afecta al criterio de cierre «no existe ningún método simple para saltarse permisos».

### H2 — El token de sesión del trabajador no caduca

Ese mismo token de sesión se firma sin fecha de expiración, y la respuesta lo dice
explícitamente devolviendo una caducidad vacía. Una vez emitido, vale para siempre.

Combinado con H1 y con H4, significa que cerrar sesión, cambiar la contraseña o desactivar
a alguien no invalida lo que ya tenía en el móvil.

Afecta a QA-AUTH-013, QA-AUTH-014, QA-AUTH-016 y a todo el Bloque F.

### H3 — La invitación de colaboradores comprueba permisos solo si quien llama se identifica

En el alta de colaborador, la comprobación de permisos se hace **solo si la petición trae
un identificador de usuario en el cuerpo**, y ese identificador **no procede del token
verificado**, sino de lo que manda el cliente. Si no viene, no se comprueba nada; si viene
otro, se comprueba el de otro. Otras rutas equivalentes del mismo repositorio sí pasan el
identificador ya verificado, así que parece un descuido y no una decisión.

Afecta a QA-AUTH-034, QA-AUTH-035 y al criterio «admin gestiona o invita colaboradores».

### H4 — Desactivar a alguien no le impide seguir operando

El estado de la ficha del trabajador no se comprueba **en ninguno** de los tres sitios que
importan para esta fase: ni al entrar en la app, ni al fichar, ni al operar sobre tareas.
Solo se comprueba al asignar a alguien a una tarea nueva y en la gestión documental.

Hay que distinguir dos cosas que el plan llama igual:

- **Dar de baja** a un trabajador sí le retira sus responsabilidades en las sucursales, y
  sin responsabilidad el fichaje se rechaza. Por ese camino indirecto, la baja funciona.
- **Desactivarlo** —dejar la ficha en un estado no activo— no toca sus responsabilidades ni
  su usuario. Sigue pudiendo entrar y seguir fichando.

Afecta a QA-AUTH-022, QA-AUTH-023 y al criterio «usuario desactivado continúa operando».

### H5 — Propietario y admin son el mismo permiso en el backend

Ya recogido en la Fase 1. El backend no distingue entre Colaborador Propietario y
Colaborador Admin: ambos pasan la misma comprobación. Lo único que los separa hoy son las
pantallas del panel, que esconden las opciones al admin.

Afecta a QA-AUTH-002, QA-AUTH-026, QA-AUTH-035 y a tres de los errores críticos del §17 del
plan.

### H6 — Dos verificadores de token distintos, y solo uno mira si la sesión fue revocada

Las rutas que protege el middleware general comprueban si la sesión ha sido revocada. Las
de fichaje y tareas usan otro verificador que no lo comprueba. Es decir: revocar la sesión
de alguien surte efecto en una parte del sistema y no en la otra.

Afecta a QA-AUTH-017, QA-AUTH-023.

### H7 — El segundo factor del panel es un sello permanente, no de sesión

Cuando un usuario del panel verifica su código, el sistema le marca la cuenta como
verificada **de forma permanente**. El comentario del propio código dice que confirma la
verificación «en esta sesión», pero la marca no es de sesión: una vez puesta, se queda.

No invalida ningún caso del plan, pero cambia lo que significa «volver a entrar»: el
segundo factor no se vuelve a pedir en el sentido en que QA podría esperarlo.

---

## 3. Qué se automatiza de esta fase

La regla es sencilla: **si el caso decide quién puede hacer qué, se automatiza; si decide
qué se ve en pantalla, no**.

**Se automatiza el núcleo de:**

- Bloque A, la parte de permisos: que cada usuario reciba exactamente las empresas,
  sucursales y capacidades que le tocan al entrar (dentro de QA-AUTH-001 a 004).
- Bloque D, la parte de fondo: que ninguna petición protegida funcione sin credencial
  válida (QA-AUTH-017, QA-AUTH-018).
- Bloque F entero: desactivar, intentar operar, reactivar (QA-AUTH-022 a 024). Hoy da rojo,
  ver H4.
- Bloque G entero: la separación entre capa administrativa y rol operativo, que es la razón
  de ser de la fase (QA-AUTH-025 a 028).
- Bloque H, la parte de autorización: que los permisos de QA-06 se recalculen por empresa y
  que no arrastre nada de una a otra (QA-AUTH-029 a 031).
- Bloque I, el fondo de la fuga: que un recurso de la Empresa A no se pueda leer estando en
  contexto de Empresa B (QA-AUTH-032).
- Bloque J, la autorización de invitar (QA-AUTH-034, QA-AUTH-035).
- Bloque K entero: que un rol operativo no abra nada administrativo (QA-AUTH-038, 039).
- Bloque L entero: que un colaborador administrativo sin rol operativo no pueda fichar
  (QA-AUTH-040).

**Se queda para personas:**

- Los formularios: campos vacíos, espacios accidentales, mensajes de validación
  (QA-AUTH-007 a 010). Son de navegador y se ven en dos minutos.
- Contraseña incorrecta y correo inexistente (QA-AUTH-005, 006): los resuelve el proveedor
  de identidad, no nuestro código. Automatizarlos es probar a un tercero.
- Recuperación de contraseña entera (Bloque C): hay correo de por medio. Lo único
  automatizable es que el enlace se genera y que solo sirve una vez.
- Logout, botón atrás y recarga (QA-AUTH-016, 019): comportamiento de navegador.
- Sesiones simultáneas (Bloque E) y varias pestañas (QA-AUTH-033).
- Todo lo visual: menús, opciones ocultas, «no ve facturación». Que la opción no aparezca
  es exactamente lo que la API no puede contar.
- Aceptar una invitación desde el correo (QA-AUTH-036, 037).

---

## 4. Desajustes entre el plan y lo que hay

**Los roles de los seis usuarios no coinciden con los de la Fase 1.** En el plan de Fase 1,
QA-03 es Owner/Manager y QA-04 es Supervisor; en el de Fase 2, QA-03 es Supervisor y QA-04
es Worker. Además, QA-01 y QA-02 pasan de no tener rol operativo a tenerlo, y QA-06 pasa de
no tener acceso administrativo a ser Admin en la Empresa A.

Puede ser deliberado —la Fase 1 ya avisa de que las asignaciones se cambian cuando una fase
lo pide—, pero entonces hace falta decirlo: **hay una reconfiguración entre fases** y
alguien tiene que ejecutarla. La automatización lo soporta sin problema, sembrando por
fases, pero necesita saber cuál es la buena en cada momento. Tal y como están hoy los dos
documentos, se contradicen.

**El plan omite el segundo factor del panel.** QA-AUTH-001 y 002 describen entrar con correo
y contraseña. En el panel hay además un paso de código de un solo uso, y sin superarlo las
llamadas al backend se rechazan. Los pasos del caso deberían recogerlo.

**«Desactivar» significa dos cosas.** Ver H4. El plan debería decir cuál de las dos se
prueba en QA-AUTH-022 y 023, porque el resultado es distinto.

**El Bloque B mezcla dos cosas.** Los casos de credenciales incorrectas prueban al proveedor
de identidad, no a CheckBiz360. Merece la pena mantenerlos como comprobación de que la
pantalla se comporta, pero no cuentan como cobertura de nuestro sistema.

---

## 5. Cómo proponemos proceder

**Primero, confirmar los hallazgos con peticiones reales contra el entorno de desarrollo.**
Es rápido, y convierte «según el código» en «comprobado». Salen de ahí cuatro o cinco
comprobaciones que además se quedan como pruebas permanentes.

**Segundo, triar H1 a H4 fuera de QA.** Son trabajo de desarrollo, no incidencias de una
regresión. H1, H2 y H3 son de seguridad y deberían tener su propia ficha; H4 y H5 son de
producto, aunque el efecto sea de permisos.

**Tercero, ejecutar la Fase 2 con los casos ya arreglados.** Lo que quede en rojo entonces
será información nueva, que es para lo que sirve una regresión.

Mientras tanto, QA puede ejecutar sin esperar a nada todos los bloques que no dependen de
los hallazgos: A, B, C, D, E, I y la parte visual de G y H. Es aproximadamente la mitad del
plan y no se pisa con nada de lo anterior.

---

## 6. Lo que necesitamos de QA

**Aclarar la configuración de roles entre fases** (§4). Es lo único que bloquea la siembra
automática: sin saber qué rol tiene cada usuario en cada fase, el entorno no se puede
preparar solo.

**Decidir qué significa «desactivar»** en QA-AUTH-022 y 023.

**Confirmar que el segundo factor entra en los pasos** de QA-AUTH-001 y 002.

Y una petición de método, la misma que en el documento anterior: numerar los criterios de
cierre del §19 igual que están numerados los casos, para que el informe automático pueda
apuntar a ellos sin traducción.
