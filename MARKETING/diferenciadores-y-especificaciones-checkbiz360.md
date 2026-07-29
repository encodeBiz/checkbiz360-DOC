# CheckBiz360 — Catálogo de diferenciadores y especificaciones

> Documento de referencia para marketing y ventas. Reúne, con detalle concreto, **las especificaciones que nos hacen diferentes** de un fichaje o un HR genérico.
> Fuentes: base de conocimiento de cliente (`DOCS/Clients`), módulos de ingeniería (`marco-legal-jornada`, `calendario`, `contrato-perfil`) y la integración Rentman.
> Uso: de aquí se sacan titulares de landing, bullets de venta, respuestas a objeciones y contenido SEO. Cada ficha incluye **matiz de honestidad** para no sobreprometer en un mercado que cambia rápido.

---

## Cómo usar este catálogo

En un mercado saturado (Sesame, Factorial, Bizneo, Woffu…) no ganamos diciendo "fichaje fácil". Ganamos con **especificidad**: detalles verificables que demuestran que el producto entiende la operación real y la ley española. Cada ficha sigue el mismo patrón: *qué es → especificación concreta → por qué diferencia → cómo se vende → matiz*.

Prioridad de uso en mensajes: **T1 (diferenciadores de primer nivel)** lideran; **T2 (refuerzos)** dan cuerpo y credibilidad.

---

# T1 · Diferenciadores de primer nivel

## D1 · Motor de cumplimiento legal por jurisdicción (el más infrautilizado)

**Qué es.** Además de registrar horas, CheckBiz360 tiene un modelo de perfil contractual (`ContractProfile`) que **compara la configuración de cada empleado contra el marco legal español** y genera avisos cuando algo roza o supera los límites del Estatuto de los Trabajadores. No es solo "fichar bien": es "no meterte en un problema legal sin darte cuenta".

**Especificación concreta (plantilla España, `jurisdiction = "ES"`):**

- **Jornada ordinaria:** aviso si se superan **40 h/semana** (cómputo anual) o **9 h/día** ordinarias.
- **Descanso entre jornadas:** control de las **12 h mínimas** entre el fin de un turno y el inicio del siguiente.
- **Pausa en jornada:** referencia de **15 min** si la jornada supera 6 h continuadas (30 min para menores).
- **Horas extra:** límite de **80 h/año**, con acumulado por empleado y **alerta al llegar al 80 %** del límite.
- **Trabajo nocturno:** franja **22:00–06:00**, clasificación automática de "trabajador nocturno" al superar el umbral del Art. 36, y aviso si se intentan asignar extras nocturnas (prohibidas salvo fuerza mayor).
- **Tiempo parcial:** distingue **horas complementarias** (límite 30 %, hasta 60 % por convenio) de horas extraordinarias.
- **Vacaciones y permisos:** referencias del Art. 38 (22 días laborables) y permisos legales (matrimonio 15 días, nacimiento, fallecimiento/enfermedad grave 2–4 días).
- **Descanso semanal:** 1,5 días (36 h) entre el último turno del fin de semana y el primero del siguiente.

**Por qué diferencia.** La mayoría de los fichadores registran; no *avisan*. Este motor convierte el cumplimiento en algo **preventivo**, no forense. Y el coste de no cumplir es real y citable: las sanciones de la LISOS por infracciones de jornada/registro van de **751 € a 7.500 €** (graves) y hasta **225.018 €** (muy graves, p. ej. superar el límite de extras o hacer trabajar de noche a menores).

**Cómo se vende.** Ángulo "duerme tranquilo": *"No solo fichas: el sistema te avisa antes de que una configuración te cueste una sanción."* Ideal para RRHH y gerencia. Titular candidato: **"El único control horario que además te avisa si te estás saltando la ley."**

**Matiz de honestidad.** Son **avisos auditables, no bloqueos**: la responsabilidad final de la configuración es del administrador de la entidad, y el motor no sustituye asesoría jurídica. Algún supuesto queda fuera de la V1 (p. ej. el preaviso de 5 días de distribución irregular de jornada). Los importes de sanción hay que verificarlos en el BOE vigente antes de publicarlos. → Vender como "avisos de cumplimiento", nunca como "cumplimiento garantizado".

---

## D2 · Calendario jerárquico en cascada (entidad → sucursal → empleado)

**Qué es.** La configuración de horarios, turnos y festivos no es plana: se resuelve por una **cascada de tres niveles** donde lo más cercano al empleado manda. Es lo que permite gestionar una empresa multi-centro real sin volverse loco.

**Especificación concreta:**

- **Tres ámbitos:** entidad (default global) → sucursal (sobrescribe) → empleado (excepción individual, prioridad absoluta). El sistema resuelve el **"calendario efectivo"** en cada fichaje.
- **Horario que se reemplaza / festivos que se acumulan:** el horario de sucursal reemplaza al de entidad; los festivos **se suman** (nacionales de entidad + autonómicos/locales de sucursal + excepciones de empleado).
- **Zona horaria por nivel:** cada sucursal puede tener su huso (p. ej. Península vs Canarias) heredando el de la entidad si no se define.
- **Turnos partidos:** cada día admite **varios turnos** (jornada partida real, p. ej. 09:00–14:00 y 16:00–19:00).
- **Turnos rotativos:** ciclos de alternancia semanal (semana A / semana B, o ciclos más largos) con fecha de anclaje.
- **Horario flexible:** tolerancia de entrada configurable + **ajuste automático de timestamp** que normaliza el fichaje a la hora oficial del turno **conservando el original para auditoría** (evita horas extra "fantasma").
- **Excepciones puntuales y periódicas** por empleado, y **"calendario efectivo" con el origen de cada dato** (badge que indica si un día viene de entidad, sucursal o excepción).

**Por qué diferencia.** Un fichador básico asume "un horario para todos". La realidad de retail multi-tienda, hostelería, logística o eventos es exactamente lo contrario. Esta cascada es infraestructura de verdad para operaciones distribuidas.

**Cómo se vende.** *"Configura una vez a nivel de empresa y ajusta solo las excepciones. La tienda de Canarias, el turno de noche o el horario especial de un empleado conviven sin conflictos."* Titular: **"Un calendario que entiende que no todos tus centros trabajan igual."**

**Matiz.** La importación automática de festivos oficiales del país puede depender del plan; hoy el responsable los introduce/gestiona. No prometer "festivos automáticos del BOE" sin verificar.

---

## D3 · Multiempresa real con aislamiento total

**Qué es.** Una misma persona puede pertenecer a **varias empresas (entidades)** con un único acceso, manteniendo los datos de cada empresa completamente separados.

**Especificación concreta:**

- Identidad por **email + UID**; al darse de alta en varias entidades, el sistema lo reconoce como un usuario con **múltiples contextos**.
- **Selector de entidad** al iniciar sesión y **token de sesión específico por entidad**: las operaciones y auditorías quedan separadas por empresa; es imposible mezclar datos.
- Cada entidad tiene **horarios, sucursales, documentos, tareas y roles propios**. El mismo usuario puede ser *worker* en una empresa y *supervisor* en otra.
- Casos reales cubiertos: **grupos empresariales** con varias razones sociales, **freelance/colaborador** que factura horas a varios clientes desde una sola app, y **doble contrato** dentro del mismo grupo.

**Por qué diferencia.** Es un caso que los productos pensados para "una empresa, un tenant" resuelven mal. Abre segmentos: grupos, consultoras, ETTs, proveedores de servicios, y encaja con el modelo colaborador de sectores como eventos.

**Cómo se vende.** *"Gestiona todas tus sociedades desde una cuenta, sin que se toquen entre sí; y deja que tus colaboradores externos fichen en varios clientes con un solo acceso."* Titular: **"Multiempresa de verdad: una cuenta, cada sociedad en su sitio."**

**Matiz.** Para cambiar de entidad en la misma jornada hay que cerrar y reabrir sesión (no hay conmutación en caliente). No venderlo como "cambio instantáneo".

---

## D4 · Roles, ámbitos y construcción de equipos

**Qué es.** Un modelo de permisos de cuatro niveles que se puede afinar por ámbito y delegar de forma granular — la base para montar la estructura operativa de equipos.

**Especificación concreta:**

- **Cuatro roles:** Worker (empleado), Supervisor (equipo/turno), Manager (gestión operativa completa), Owner (control total + facturación/entidad).
- **Tipo de relación:** *interno* (plantilla) vs *colaborador* (externo/freelance) — independiente del rol.
- **Ámbito del rol:** a nivel de **entidad** (toda la empresa) o de **sucursal** (solo ese centro). Un supervisor de Madrid solo ve Madrid.
- **Un empleado, varios roles a la vez:** supervisor en Barcelona y worker en Madrid, simultáneamente.
- **Delegación granular:** el manager decide, supervisor a supervisor, quién puede **crear tareas, validarlas o valorar** a los trabajadores.
- **Quién asigna qué:** owner asigna cualquier rol; manager hasta supervisor dentro de su ámbito; supervisor/worker no asignan.

**Por qué diferencia.** No es "admin y usuario". Es una estructura que refleja organigramas reales multi-centro y permite descentralizar sin perder control.

**Cómo se vende.** *"Monta tu estructura tal cual es: responsables por centro, permisos a medida y visibilidad justo hasta donde toca."* Buen argumento para el comprador de operaciones.

**Matiz.** Los permisos son configurables "dentro de ciertos límites"; no es un motor de permisos totalmente arbitrario. Describir como "roles con delegación configurable", no "permisos 100 % personalizables".

---

## D5 · Jornada manual con doble validación (protege al trabajador)

**Qué es.** Cuando un responsable corrige o crea una jornada que el empleado no pudo fichar, el registro **no cuenta hasta que el propio empleado lo valida**.

**Especificación concreta:**

- Dos modos: **jornada completa** (crea checkin+checkout, autocompletando con el turno si no se indican horas) o **solo checkout** (cierra una jornada abierta).
- Estado inicial **`pending-employee-validation`**: no computa horas hasta que el empleado **acepta** (pasa a `valid`) o **rechaza** (`failed`, con motivo).
- **Motivo obligatorio** del responsable, notificación push al empleado, y **registro inmutable** de toda la operación (quién, cuándo, estado anterior y nuevo).

**Por qué diferencia.** En muchos sistemas el responsable edita las horas de forma unilateral. Aquí el diseño **da voz al empleado y deja trazabilidad**, lo que es oro ante Inspección y ante comités de empresa: demuestra que los registros no se manipulan a espaldas del trabajador.

**Cómo se vende.** *"Las correcciones las confirma el empleado. Transparencia total y una auditoría que aguanta cualquier inspección."* Encaja con el mensaje de equidad (ver guardarraíles del doc de estrategia).

**Matiz.** Es un flujo de corrección de jornada, no un portal de autoservicio de RRHH completo. Nombrarlo con precisión.

---

# T2 · Refuerzos (dan cuerpo y credibilidad)

## D6 · Gestión de ausencias, festivos y días libres por nivel

Días no laborables y ausencias configurables por **entidad, sucursal y empleado**, con tipos diferenciados (festivo nacional/autonómico/local, puente, cierre interno) y la posibilidad de **deshabilitar un festivo puntual** para una sucursal o solo para ciertos empleados (retail/hostelería que trabajan en festivo). Bloqueo de fichaje en día no laborable con código propio y registro del intento. **Matiz a verificar antes de landing:** confirmar si existe además un flujo de *solicitud y aprobación de vacaciones con saldo de días* o si hoy se gestiona como ausencias/excepciones de calendario; comunicarlo con precisión.

## D7 · Fichaje con triple validación, sin hardware

Cada fichaje pasa por tres capas: **geolocalización** (geocerca por sucursal, con distancia registrada; se omite en trabajo remoto), **horario efectivo** (turno + tolerancia + ajuste de timestamp) y **dispositivo/biometría** (dispositivos de confianza, 2FA, huella/facial). Los **fichajes fallidos también se guardan** para auditoría. Todo desde el móvil, sin terminal físico.

## D8 · Cumplimiento RDL 8/2019 con historial inmutable

Timestamp al segundo, historial que nadie puede borrar ni alterar, cada corrección trazada con valor original/nuevo/usuario/fecha/**motivo obligatorio**, conservación **4 años**, y acceso del trabajador a sus horas desde la app. Comparativa demoledora frente a papel y hojas de cálculo editables.

## D9 · Tareas operativas con evidencia, validación y valoración

Checklists por turno/centro con adjuntos **foto/vídeo**, flujo **completar → validar/rechazar (con motivo) → valorar 1–5**, y esas valoraciones **alimentan el índice de eficiencia**. Convierte "¿vino?" en "¿se hizo, y bien?".

## D10 · Inteligencia operativa

Índices de **fiabilidad, eficiencia y puntuación de promoción** por empleado; **detección de anomalías** (precisión temporal excesiva, geolocalización estática); **análisis de coste real vs planificado** por empleado/sucursal; **paneles de mando** y **vista global multi-sucursal** en tiempo real (quién ha fichado, ausencias, anomalías, coste). *Guardarraíl obligatorio: comunicar desde equidad/objetividad, nunca como vigilancia.*

## D11 · Gestión documental como expediente de personal

No es un Drive: cada documento (nómina, contrato, certificado, PRL) queda **vinculado al empleado y su relación laboral**, con **acuse de recibo** con fecha, visibilidad por rol y el empleado viendo solo lo suyo desde la app.

## D12 · Integración con ERP (Rentman) — la cuña de nicho

Sincronización **bidireccional** con Rentman: eventos/proyectos → centros de fichaje, asignaciones de crew → asignaciones, y las horas fichadas → de vuelta a Rentman. "Un dato se introduce una sola vez." Posiciona a CheckBiz360 como la **capa de personas y cumplimiento** sobre el ERP, no como sustituto. *(Matiz: presentar el estado/plazo real en la conversación comercial.)*

## D13 · Seguridad de nivel entidad

**2FA obligatorio** configurable por entidad, **biometría** y **dispositivos de confianza** por empleado. Argumento de confianza para cuentas medianas y grupos.

## D14 · Puesta en marcha y capacitación gratuitas (diferenciador de servicio)

**Qué es.** El alta no se deja en manos del cliente: **el proceso de arranque completo y la formación del equipo van incluidos, sin coste.** Nos encargamos de la configuración inicial (entidad, sucursales, horarios, roles, calendario, empleados) y de capacitar a responsables y trabajadores para que el sistema esté operativo desde el primer día.

**Por qué diferencia.** El mayor riesgo al comprar software de gestión no es el precio: es que "nadie lo llegue a usar". Los productos de autoservicio dejan al cliente solo ante una configuración que —como muestra este mismo catálogo— es potente pero tiene profundidad (cascada de calendario, roles por ámbito, multiempresa). Ofrecer **onboarding y formación gratis** elimina la fricción de adopción y convierte la profundidad del producto en una ventaja en lugar de una barrera.

**Cómo se vende.** Neutraliza dos objeciones a la vez: *"¿y quién me lo configura?"* y *"desde 2 € debe de venir sin soporte"*. Mensaje: *"No te damos un software y suerte. Te lo dejamos montado, formamos a tu equipo y arrancas funcionando — sin coste de implantación."* Es, además, el argumento perfecto para justificar la permanencia de 6 meses en la integración: hay un trabajo de puesta en marcha detrás.

**Matiz.** Definir con producto el alcance exacto del onboarding gratuito (horas/sesiones incluidas, remoto vs presencial, hasta qué tamaño de plantilla) para poder ponerlo por escrito sin sobreprometer.

---

# Tabla resumen — qué contamos que otros no

| Diferenciador | Fichaje/HR genérico | CheckBiz360 |
|---|---|---|
| Avisos de cumplimiento legal (ET) | No | Sí — motor por jurisdicción (D1) |
| Calendario en cascada 3 niveles | Limitado | Sí — entidad/sucursal/empleado (D2) |
| Turnos partidos, rotativos y flexibles | Parcial | Sí, los tres (D2) |
| Multiempresa con aislamiento | Raro / mal resuelto | Sí — token por entidad (D3) |
| Roles por ámbito + delegación granular | Básico | Sí (D4) |
| Corrección de jornada validada por el empleado | No | Sí (D5) |
| Tareas con evidencia + valoración que puntúa | No | Sí (D9) |
| Inteligencia operativa (coste, anomalías, índices) | No | Sí (D10) |
| Documental como expediente con acuse | No | Sí (D11) |
| Integración bidireccional con ERP de nicho | No | Sí — Rentman (D12) |
| Puesta en marcha + formación incluidas | Coste extra / autoservicio | Sí, gratis (D14) |

---

# Cómo esto entra en la landing y el resto del marketing

1. **Hero:** liderar con la promesa de gobierno operativo + el gancho legal (D1) o de cumplimiento (D8) según el segmento.
2. **Sección "Pensado para operaciones de verdad":** D2 + D3 + D4 juntos (calendario cascada, multiempresa, roles) — es el bloque que grita "esto lo hizo alguien que entiende empresas multi-centro".
3. **Sección "Cumples sin esfuerzo":** D1 + D8 + D5 (motor legal, inmutabilidad, jornada validada) — el bloque anti-Inspección.
4. **Landing vertical Rentman/eventos:** D12 arriba, apoyado en D2 (turnos/venues), D6 (festivos/temporada) y D8 (legal).
5. **SEO / contenido:** cada ficha es un artículo potencial ("turnos partidos y rotativos: cómo configurarlos", "qué dice la ley sobre las 12 horas entre jornadas", "cómo funciona el registro horario multiempresa"). La KB ya tiene medio contenido escrito.
6. **Ventas:** esta tabla resumen es una hoja de batalla directa frente a competidores generalistas.

> **Antes de publicar cualquier cifra o afirmación legal:** validar con producto el estado real de cada capacidad (especialmente D1 alcance V1, D6 flujo de vacaciones y D12 plazos de Rentman) y verificar los importes de sanción en el BOE vigente. La credibilidad en este mercado se pierde una sola vez.
