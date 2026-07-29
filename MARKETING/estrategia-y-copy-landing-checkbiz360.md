# CheckBiz360 — Estrategia de marketing y copy de landing

> Documento de trabajo para el equipo. Base: base de conocimiento de cliente (`DOCS/Clients`), documentación de la integración Rentman (`DOCS/ingenieria/rentman-integration`) y la web actual `checkbiz.encodebiz.com`.
> Objetivo: fijar posicionamiento, mensajes y una estructura de landing con copy lista para maquetar.

---

## 0. Resumen ejecutivo

CheckBiz360 es un buen producto en un mercado ruidoso. La diferenciación real (inteligencia operativa + cumplimiento legal + tareas y documental en una sola app) existe, pero **la web actual no la cuenta entera**: lidera bien con "algo más que fichajes" y analítica, pero se deja fuera tres de los argumentos de venta más fáciles —cumplimiento RDL 8/2019, gestión de tareas y gestión documental— y no aprovecha la cuña de nicho (Rentman/eventos).

La recomendación estratégica es triple:

1. **No competir por "fichaje".** Es una guerra de precio y SEO contra Sesame, Factorial, Bizneo, Woffu. Liderar por *gobierno operativo* + verticales.
2. **Sacar a la luz los tres pilares ocultos** (cumplimiento, tareas, documental) junto a la inteligencia operativa. Son ventas de dolor concreto.
3. **Entrar por nichos** donde el dolor es agudo y hay menos competencia: eventos/AV (vía Rentman), hostelería, retail multi-tienda, logística, equipos de campo.

---

## 1. Diagnóstico de la web actual (`checkbiz.encodebiz.com`)

**Lo que funciona y hay que conservar:**

- El titular *"Control horario para empresas que quieren algo más que fichajes"* es un buen ángulo de partida: promete diferenciación desde la primera línea.
- El marco de "convertir datos de fichaje en inteligencia operativa" es correcto y es el foso.
- Estructura por capas de valor, funcionalidades, beneficios por departamento y sectores: buen esqueleto.
- Prueba social con testimonios reales y sección de equipo: transmite que hay gente detrás.
- CTAs claros: *Crear cuenta gratuita* + *Agendar demo 30'*.

**Lo que falta o hay que corregir (prioridad alta):**

1. **Ausencia de tres pilares vendibles.** No se menciona el **cumplimiento RDL 8/2019** (el argumento con más miedo asociado del mercado), ni la **gestión de tareas**, ni la **gestión documental**. Son fortalezas documentadas del producto que hoy no aparecen. Es el mayor desperdicio de la web.
2. **Sin integraciones ni Rentman.** No hay bloque de integraciones. La cuña de nicho no existe en la web.
3. **Inconsistencia de marca.** La web dice "CheckBiz"; la documentación dice "CheckBiz360"; internamente conviven checkinbiz, passbiz, encodeBiz. Hay que fijar la arquitectura de marca (ver §2).
4. **Riesgo de vender heurística/insights por delante del cumplimiento.** La analítica avanzada engancha al perfil "ops/dirección", pero el cumplimiento y la app fácil son los que quitan la fricción de la compra. Conviene equilibrar.
5. **Sin precio ni oferta clara.** No aparece el "desde 2 €/empleado" ni los 45 días de prueba. Falta un ancla de conversión.
6. **Cuidado con prometer roadmap.** Varias capacidades de la doc están *pendientes de desarrollo* (firma electrónica, exportación de costes/anomalías a CSV/PDF, modo offline, alertas de coste configurables, workflow de anomalías). La web debe vender lo que embarca hoy; el resto, "próximamente" o fuera.

---

## 2. Arquitectura de marca y naming

**DECISIÓN TOMADA (dirección):** el nombre del producto es **CheckBiz360**, con dominio canónico **checkbiz360.com**. Queda descartado usar "CheckBiz" a secas. A partir de aquí, se unifica en todos los canales.

**Jerarquía de marca:**

- **EncodeBiz** = marca paraguas / empresa (el "sello de confianza"). Razón social: Encodebiz SL.
- **CheckBiz360** = nombre del producto de control horario e inteligencia operativa. **Siempre "CheckBiz360", nunca "CheckBiz" a secas.** Dominio: checkbiz360.com.
- **PassBiz** = producto hermano (posicionarlo como parte de la familia "…Biz de EncodeBiz").
- **Integración Rentman** = un módulo/add-on de CheckBiz360, no una marca.

Firma recomendada en web: **"CheckBiz360, de EncodeBiz"**.

**Regla de uso (aplicar en todo):** el nombre completo es **CheckBiz360** (una palabra "CheckBiz" + "360" pegado, C y B mayúsculas). En primera mención de cada pieza, "CheckBiz360"; después puede repetirse igual. No abreviar a "CheckBiz", "Checkbiz", "CB360" ni "CheckBiz 360" (sin espacio antes del 360).

**Checklist de unificación (dónde corregir "CheckBiz" → "CheckBiz360"):**

1. Landing de producto `checkbiz.encodebiz.com` (hoy titula "CheckBiz"): logo, titulares, textos y metadatos.
2. Consolidar el dominio: decidir si `checkbiz360.com` es el principal y `checkbiz.encodebiz.com` redirige a él (recomendado para no dividir autoridad SEO). **Ojo:** `checkbiz360.com` dio un error de certificado SSL al comprobarlo — verificar que el HTTPS está bien configurado antes de promocionarlo.
3. Fichas de app (App Store / Google Play): ya figuran como "CheckBiz360" — mantener.
4. Blog, redes, firmas de email, plantillas comerciales y los emails a clientes (carpeta SONOIBIZA ya usa CheckBiz360).
5. Perfiles en comparadores/reseñas cuando se creen (Capterra, G2, Appvizer): dar de alta como "CheckBiz360".

---

## 3. Posicionamiento y propuesta de valor central

**Categoría en la que jugamos:** no "software de fichaje", sino **plataforma de gobierno operativo del equipo** (control horario + cumplimiento + tareas + documental + inteligencia operativa).

**Statement de posicionamiento (interno):**
> Para empresas de 10 a 500 empleados con equipos en varios centros, proyectos o en la calle, CheckBiz360 es la plataforma que convierte el fichaje en gobierno operativo: cumples la ley sin esfuerzo, sabes qué se hace en cada turno y decides con datos reales de coste y rendimiento. A diferencia de los fichadores tradicionales, no solo registra presencia: la convierte en decisiones.

**Claim central (candidatos para el hero):**

- A) *"El fichaje es solo el principio."*
- B) *"Ficha, cumple y gobierna tu operación desde una sola app."*
- C) *"Control horario que además te dice qué está pasando en tu operación."*
- D) (vertical) *"La capa de personas y cumplimiento para tu operación de campo."*

Recomendado para la home general: **A** como gancho + una bajada explicativa (ver copy §6).

---

## 4. Público objetivo y verticales

**ICP (perfil de cliente ideal):** empresas de **10–500 empleados**, con **varios centros, proyectos o equipos de campo**, para las que el coste laboral pesa y el cumplimiento es un riesgo real.

**Buyer personas:**

1. **La Dirección de Operaciones / Gerencia (comprador económico).** Quiere control, coste real por centro y decisiones con datos. Le hablan: inteligencia operativa, análisis de costes, paneles, comparativa entre sedes.
2. **RRHH / Administración (usuario e influencer).** Le quita horas de gestión y el miedo a la Inspección. Le hablan: cumplimiento RDL 8/2019, documental con acuse de recibo, informes listos, correcciones trazadas.
3. **El responsable de equipo / jefe de obra o montaje (usuario de campo).** Necesita que la app sea trivial y saber quién está y qué se hizo. Le hablan: fichaje por GPS sin hardware, tareas con foto, alertas de "no ha fichado".

**Verticales de ataque (orden sugerido de prioridad GTM):**

1. **Eventos / audiovisual y alquiler técnico** — cuña vía Rentman. Dolor agudo (equipos en venues, jornadas nocturnas, cumplimiento difícil), competencia baja en este ángulo. *(Sono Ibiza es el caso de entrada.)*
2. **Hostelería** — turnos rotativos, control de costes en sala y cocina.
3. **Retail multi-tienda** — comparativa de productividad y coste entre centros.
4. **Logística y equipos de campo** — fichaje GPS sin terminal físico.
5. **Servicios profesionales / mantenimiento** — imputación de horas por proyecto/cliente.

---

## 5. Casa de mensajes (message house)

**Claim techo:** *El fichaje es solo el principio: CheckBiz360 convierte cada jornada en cumplimiento, control y decisiones.*

**Cuatro pilares (con su prueba):**

| Pilar | Promesa al cliente | Prueba (de la documentación) |
|---|---|---|
| **Cumplimiento sin esfuerzo** | "Duerme tranquilo ante la Inspección." | Registro RDL 8/2019, timestamp al segundo, historial inmutable, correcciones trazadas con motivo, 4 años de conservación, acceso del trabajador. |
| **Operación bajo control** | "Sabes qué se hace en cada turno, no solo quién vino." | Tareas asignadas con checklist, evidencia foto/vídeo, validación y valoración 1–5; alertas de responsable. |
| **Decisiones con datos** | "Conoce el coste y el rendimiento real de cada centro." | Índices de fiabilidad/eficiencia/promoción, análisis de costes real vs planificado, detección de anomalías, paneles y vista global multi-sede. |
| **Fácil para todos** | "Tu equipo solo tiene que fichar; tú lo gestionas desde un panel." | App iOS/Android gratis, fichaje GPS sin hardware; backoffice web único; se conecta con tu ERP (Rentman). |

**Guardarraíles de mensaje (importante, no negociable):**

- **Tema sensible — inteligencia/anomalías/promoción.** Comunicar siempre desde **equidad y objetividad**, nunca desde vigilancia. Evitar "controla/vigila a tus empleados"; usar "decisiones más justas y basadas en datos". La propia doc insiste: los índices son señales de apoyo, no veredictos, y no deben ser base única de decisiones disciplinarias. El copy debe reflejarlo para no generar rechazo (comités de empresa, RGPD, reputación).
- **Roadmap.** No prometer en web funciones marcadas como pendientes (firma electrónica, exportaciones de costes/anomalías, offline, alertas de coste, workflow de anomalías). Vender lo que hoy embarca en Bronze/Enterprise.
- **Rentman.** Presentarlo como integración **disponible/activable** con matices honestos en la conversación comercial (estado y plazos reales). En web puede figurar como "Se integra con tu ERP: Rentman" en el bloque de integraciones, sin sobreprometer automatismos aún no cerrados.

---

## 6. Estructura de la landing (home general) con copy

> Copy listo para maquetar. Entre corchetes, notas de diseño/CTA. Sustituir cifras/pruebas por datos verificados antes de publicar.

### 6.1 Hero
**H1:** El fichaje es solo el principio.
**Subtítulo:** CheckBiz360 registra la jornada de tu equipo y la convierte en cumplimiento legal, control operativo y decisiones con datos. Todo desde una sola app.
**CTA primario:** Empieza gratis — 45 días de prueba
**CTA secundario:** Agenda una demo de 30'
**Microcopy bajo CTA:** Desde 2 €/empleado al mes · Sin instalar hardware · iOS y Android
[Diseño: captura del panel + app móvil. Azul marca sobre fondo claro.]

### 6.2 Barra de confianza
*"Empresas con equipos en varios centros, proyectos o en la calle ya operan con CheckBiz360."*
[Logos de clientes / sectores + testimonios reales ya existentes.]

### 6.3 El problema (agitar)
**Titular:** Tus fichajes están llenos de respuestas. Solo que nadie las lee.
**Cuerpo:** La mayoría de los sistemas registran entradas y salidas y ahí se quedan. El resultado: horas cada semana consolidando datos a mano, informes que llegan tarde, costes que se escapan y el miedo latente a una Inspección de Trabajo. CheckBiz360 nace justo para el momento en que el fichaje simple deja de ser suficiente.

### 6.4 Los 4 pilares de valor
[Cuatro tarjetas, una por pilar de §5.]

**1. Cumplimiento sin esfuerzo.**
Cumple el RDL 8/2019 sin preparar nada. Registro con hora exacta, historial que nadie puede alterar, cada corrección trazada con su motivo y cuatro años de conservación. Si llama la Inspección, ya está todo listo.

**2. Operación bajo control.**
No solo sabes quién vino: sabes qué se hizo. Asigna tareas y checklists a cada turno, recibe la evidencia en foto y valídalo desde el panel. El trabajo real, documentado.

**3. Decisiones con datos.**
Coste real por empleado y por centro, comparativa entre sedes e índices de rendimiento que te ayudan a decidir con criterio y no con intuición. Más justo para tu equipo, más claro para ti.

**4. Fácil para todos.**
Tu gente solo tiene que fichar desde el móvil, con validación por GPS y sin ningún aparato que instalar. Tú lo gestionas todo desde un único panel web.

### 6.5 Cómo funciona (3 pasos)
1. **Ficha.** El empleado ficha desde la app; el sistema valida ubicación, turno y dispositivo.
2. **Gestiona.** Asignas tareas, revisas jornadas y publicas documentos desde el backoffice.
3. **Decide.** La plataforma convierte todo en indicadores de coste, cumplimiento y rendimiento.

### 6.6 Bloque profundo — Inteligencia operativa
**Titular:** La diferencia no está en fichar. Está en lo que pasa después.
**Cuerpo:** Cada jornada y cada tarea alimentan un perfil que detecta tendencias antes de que sean problemas: fiabilidad y eficiencia por persona, coste real frente al previsto, comparativa entre centros y detección automática de anomalías. Todo desde paneles que se actualizan solos.
**Nota de tono/legal (visible):** Indicadores de apoyo a la gestión, pensados para decisiones más justas y objetivas — nunca un sustituto del criterio humano.
**CTA:** Ver la inteligencia operativa en una demo.

### 6.7 Bloque cumplimiento
**Titular:** La tranquilidad de tenerlo todo en regla.
**Cuerpo:** Registro conforme al RDL 8/2019, inmutable y trazable, con acceso del trabajador a sus propias horas desde la app y conservación durante cuatro años. El papel y las hojas de cálculo editables no ofrecen las mismas garantías ante la Inspección; CheckBiz360 sí.
**CTA:** Descarga la guía "Prepara tu empresa para una Inspección de Trabajo". [Lead magnet — ver §9]

### 6.8 Integraciones
**Titular:** No sustituye a tu ERP. Lo completa.
**Cuerpo:** ¿Ya usas un ERP potente para planificar proyectos y facturar? CheckBiz360 se coloca al lado y añade lo que un ERP no cubre: el cumplimiento horario legal, las tareas de campo y el expediente documental de tu equipo. Se integra con **Rentman** para que planifiques donde siempre y el registro de horas fluya solo.
**CTA:** ¿Usas Rentman? Descubre la integración → [enlace a landing vertical §7]

### 6.9 Sectores
[Grid con: Eventos y audiovisual · Hostelería · Retail multi-tienda · Logística y campo · Servicios y mantenimiento · Educación.] Una línea de dolor por sector.

### 6.10 Prueba social
[Testimonios reales existentes + resultado cuantificado cuando lo haya: horas de gestión ahorradas, % de reducción de incidencias, etc. Verificar antes de publicar.]

### 6.11 Planes y precio
**Titular:** Empieza por lo que necesitas hoy. Amplía cuando crezcas.
**Bronze:** Control horario, tareas e inteligencia operativa básica.
**Enterprise:** Todo lo de Bronze + gestión documental, análisis de costes, detección de anomalías y multi-entidad.
**Ancla:** Desde 2 €/empleado al mes · 45 días de prueba · sin permanencia para empezar.
[Nota interna: la permanencia de 6 meses aplica al activar la integración Rentman; no confundir con el alta general.]
**CTA:** Crear cuenta gratuita.

### 6.12 FAQ
- ¿Necesito instalar algún aparato? No: se ficha desde el móvil con validación por GPS.
- ¿Cumple la ley española de registro horario? Sí, el RDL 8/2019, con historial inmutable y trazable.
- ¿Puedo empezar solo con el control horario? Sí, con el plan Bronze, y ampliar cuando quieras.
- ¿Se integra con mi ERP? Se integra con Rentman; cuéntanos tu caso.
- ¿Cuánto cuesta? Desde 2 €/empleado al mes, con 45 días de prueba.

### 6.13 CTA final
**Titular:** Deja de reaccionar a tu operación. Empieza a gobernarla.
**CTA primario:** Empieza gratis — 45 días.
**CTA secundario:** Habla con nosotros.

---

## 7. Variante de landing vertical — Eventos / Rentman

> Misma plataforma, mensaje afilado al nicho. Es la puerta de entrada comercial más eficiente a corto plazo.

**H1:** La capa de personas y cumplimiento para tu operación de campo.
**Subtítulo:** Tu Rentman planifica y factura. CheckBiz360 gobierna lo que pasa en el evento: fichaje legal de tu equipo en el propio venue, tareas de montaje con evidencia y las horas de vuelta a Rentman.
**CTA:** Descubre la integración con Rentman.

**Bloques propios:**
- *"Rentman es la sala de planificación; CheckBiz360, la cabina de operación de campo."* — explicación de las 3 capas (evento→centro de fichaje, asignación→técnico, jornada→horas a Rentman), con el mensaje de sincronización bidireccional y "un dato se introduce una sola vez".
- *"Lo que Rentman no cubre, y es tu día a día":* cumplimiento RDL 8/2019 + tareas de montaje/desmontaje con foto.
- Dolores del sector: técnicos moviéndose entre venues, jornadas hasta la madrugada, fichaje sin hardware en cada sitio.
- Oferta: desde 2 €/empleado/mes · 45 días de prueba · la integración se activa como módulo (permanencia de 6 meses).

---

## 8. Conversión y activación

- **Oferta ancla:** 45 días de prueba + "desde 2 €/empleado/mes". Destacar la prueba por encima del precio.
- **Doble CTA en toda la web:** *Crear cuenta gratuita* (autoservicio, para PYME pequeña) + *Agendar demo 30'* (para cuentas con más empleados o con ERP). Mantener el formulario de demo actual (nombre, teléfono, email, empresa, nº empleados) — el nº de empleados sirve para cualificar.
- **Lead magnet de cumplimiento:** guía "Prepara tu empresa para una Inspección de Trabajo" (ya tenéis el contenido en la KB, artículo 84). Captura email y alimenta nurturing.
- **Palanca anti-fricción — arranque y formación gratis:** destacar en el hero, en el bloque de precio y en la demo que **la puesta en marcha completa y la capacitación del equipo van incluidas, sin coste**. Neutraliza la objeción "¿quién me lo configura?" y la lectura de "barato = sin soporte", y justifica la permanencia de 6 meses de la integración. Copy sugerido: *"Nosotros te lo dejamos montado y formamos a tu equipo. Tú solo empiezas a usarlo."* (Ver ficha D14 del catálogo de diferenciadores; validar alcance exacto con producto.)

---

## 9. SEO y contenido (activo infrautilizado)

Tenéis una base de conocimiento de ~90 artículos de altísima calidad. Es una mina para SEO y para nutrir leads. Propuesta:

- Publicar la KB como **centro de ayuda / blog** indexable (muchos artículos ya atacan intención de búsqueda real: "registro horario obligatorio en España", "cómo preparar una inspección de trabajo", "turnos rotativos", "geocercas de fichaje").
- Clústers de contenido por pilar: *Cumplimiento RDL 8/2019*, *Control de costes de personal*, *Gestión de equipos de campo*, *Control horario por sector*.
- Piezas de comparación honestas ("control horario vs. fichaje tradicional") — ya tenéis el artículo base.
- Reutilizar los emails de la carpeta SONOIBIZA como plantilla de outbound por vertical.

---

## 10. Próximos pasos propuestos

1. ✅ **Naming cerrado: CheckBiz360** (dominio checkbiz360.com). Pendiente solo la ejecución de la unificación en web y canales (ver checklist en §2) y verificar el SSL de checkbiz360.com.
2. **Validar datos sensibles:** precio "desde 2 €", condiciones de prueba y permanencia, y estado real de la integración Rentman para no sobreprometer. — Producto/Dirección.
3. **Aprobar el copy de este documento** (o marcar cambios).
4. Con el copy cerrado, monto la **landing en HTML navegable** (mockup real, responsive) para validar visualmente antes de pasarla a producción.
5. Definir el **plan de contenido/SEO** a partir de la KB.

> Dime por cuál seguimos y lo ejecuto. Mi recomendación: cerrar naming + validar datos, y en paralelo yo maqueto ya la home general y la vertical de Rentman en HTML para que las veas.
