# Handoff: Landing CheckBiz360 (home general)

## Overview
Rediseño de la landing pública de **CheckBiz360, de EncodeBiz** (sustituye a
`https://checkbiz.encodebiz.com/`). Objetivo comercial: dejar de vender "fichaje" y
posicionar la plataforma como *gobierno operativo* — control horario + cumplimiento
RDL 8/2019 + tareas + inteligencia operativa. Copy aprobado en
`DOCS/MARKETING/estrategia-y-copy-landing-checkbiz360.md` (§6).

Idioma: español (`lang="es"`). Preparado para una versión EN (no incluida).

## About the Design Files
El archivo `Landing CheckBiz360.dc.html` es una **referencia de diseño en HTML**: un
prototipo que muestra el aspecto y el comportamiento previstos, **no código de
producción**. La tarea es **recrear este diseño en el entorno del proyecto destino**
(WordPress/Elementor si se mantiene el stack actual, o React/Next si se rehace),
usando los patrones y librerías ya establecidos allí. Si no hay entorno definido,
elegir el más apropiado e implementarlo con sus convenciones.

`support.js` es solo el runtime del prototipo — **no forma parte del diseño** y no debe
portarse.

## Fidelity
**Alta fidelidad (hifi).** Colores, tipografía, espaciados, sombras y estados están
definidos y deben reproducirse con precisión. Excepciones que son *placeholder*:
- Logos de clientes (Litoral Group, ACB, Ferrada) están como lockups de texto.
- No hay fotografía de producto ni de equipo: el mockup del panel es HTML/CSS real.

## Screens / Views

Una sola página, ancho de contenido **1180 px** centrado, padding lateral 48 px.
Orden de secciones (todas separadas por `border-bottom: 1px solid #E9ECF2`):

### 1. Header (sticky)
- `position: sticky; top: 0; z-index: 30`, fondo `#FFFFFF` sólido (sin blur),
  padding `16px 48px`, `display:flex; justify-content:space-between`.
- Izquierda: cuadro de marca 30×30, `border-radius: 9px`, fondo `#0A1226`, letra "C"
  blanca 14px/800. Al lado, "CheckBiz360" 17px/800, `letter-spacing:-.02em`, y debajo
  "DE ENCODEBIZ" en IBM Plex Mono 9px, `letter-spacing:.14em`, color `#7B8494`.
- Centro: nav 14px/600 color `#414C63`, gap 28px. Hover: color `#0A1226` +
  `border-bottom: 2px solid #1D4ED8`. Enlaces: Plataforma, Cumplimiento, Inteligencia,
  Sectores, Precio (anclas `#pilares`, `#cumplimiento`, `#inteligencia`, `#sectores`, `#precio`).
- Derecha: botón secundario "Agendar demo 30'" (borde `#D8DCE4`, radio 10px, hover fondo
  `#F5F6F9`) + botón primario "Empieza gratis" (fondo `#1D4ED8`, texto blanco, radio 10px,
  sombra `0 12px 24px -12px rgba(29,78,216,.8)`, hover `#173FAF` + `translateY(-2px)`).

### 2. Hero
- Fondo: `linear-gradient(180deg,#F7F9FC 0%,#FFFFFF 84%)`, `overflow:hidden`,
  padding `104px 48px 0`.
- **Grafo de fondo (SVG, decorativo)**: `viewBox="0 0 1440 760"`, absoluto a la sección.
  Malla de aristas (`stroke:#0A1226; opacity:.07; stroke-width:1`) uniendo 10 nodos;
  dos polilíneas de "flujo" superpuestas (`#1D4ED8` y `#0E9384`, `opacity:.16`,
  `stroke-width:1.2`); nodos = círculos r=3 `fill:#0A1226` con pulso de opacidad
  `.18 → .6` en 8 s (`@keyframes cb-node`, delays escalonados 1 s). **Muy sutil, es fondo.**
- Contenido centrado, `max-width: 900px`, gap 26px:
  - Píldora: `border-radius:999px`, fondo `#fff`, borde `#DDE2EC`, sombra
    `0 4px 14px -6px rgba(10,18,38,.2)`, IBM Plex Mono 11px uppercase `.08em` color
    `#414C63`; punto 7px `#0E9384` con pulso 2.4 s. Texto: "Conforme al RDL 8/2019 · Registro inmutable".
  - H1 88px / `line-height:.95` / `letter-spacing:-.045em` / 800:
    "El fichaje es solo\nel principio." — el punto final en `#1D4ED8`.
  - Subtítulo 21px/1.5 `#414C63`, max 720px: "CheckBiz360 registra la jornada de tu equipo
    y la convierte en cumplimiento legal, control operativo y decisiones con datos. Todo
    desde una sola app."
  - CTA primario "Empieza gratis — 45 días de prueba" (16px/700, `#1D4ED8`, padding
    `17px 28px`, radio 12px, sombra `0 18px 34px -16px rgba(29,78,216,.85)`).
    CTA secundario "Agenda una demo de 30'" (borde `#CFD5E0`, hover borde `#0A1226`).
  - Microcopy IBM Plex Mono 12px `#6B7484`: "Desde 2 €/empleado al mes · Sin instalar
    hardware · iOS y Android".
- **Mockup de panel** (max 1180px, margen superior 68px, pegado al borde inferior):
  contenedor `#0A1226`, `border-radius:18px 18px 0 0`, padding `12px 12px 0`, sombras
  `0 60px 100px -50px rgba(10,18,38,.6), 0 18px 40px -24px rgba(10,18,38,.35)`.
  Barra de ventana con 3 puntos `#39415A` + "panel.checkbiz360.com / vista global".
  Interior en grid `1.55fr 1fr` con `gap:1px; background:#E9ECF2`:
  - Panel izquierdo (blanco): título "Coste real vs. planificado" / "5 centros · semana en
    curso", leyenda Real (`#1D4ED8`) / Previsto (`#DDE2EC`); gráfico de 7 días, cada día con
    dos barras (real sólida, previsto en gris), altura de caja 172px, radio superior 5px,
    etiquetas L–D IBM Plex Mono 10px; abajo 3 KPI: Fiabilidad **94 %**, Eficiencia **87 %**,
    Desvío coste **+6 %** (este en `#B4560A`), cifras 26px/800.
  - Panel derecho (`#F7F8FB`): "HOY EN TUS CENTROS" + 3 filas (Madrid · Almacén 12/12,
    Ibiza · Venue Norte 8/8 en `#0E9384`; Valencia · Tienda 2 "1 sin fichar" con borde
    `#F0C9A8` y texto `#B4560A`); luego "AVISOS DE CUMPLIMIENTO" con 2 tarjetas:
    "Horas extra al 80 % del límite / 2 empleados · límite anual 80 h" y
    "Descanso entre jornadas < 12 h / Turno noche · Ibiza · revisar".

### 3. Barra de confianza
Padding `34px 48px`. Izquierda: 14px/1.5 `#5B6479` "Empresas con equipos en varios
centros, proyectos o en la calle ya operan con CheckBiz360." Derecha: lockups 17px/800
`#9AA2B2` (Litoral Group, ACB, Ferrada) + `+ logo slot` mono 11px → **sustituir por logos reales**.

### 4. Problema (fondo `#F7F8FB`)
Centrado, max 1040px. Kicker mono 11px `.16em` `#1D4ED8` "EL PROBLEMA". H2 54px/1.04/800:
"Tus fichajes están llenos de respuestas.\nSolo que nadie las lee." Párrafo 18px/1.62
`#414C63` (texto §6.3 del doc). Debajo, grid de 4 tarjetas blancas (padding 22px, borde
`#E4E8F0`, radio 14px, sombra `0 4px 14px -10px rgba(10,18,38,.2)`, hover elevación):
Horas de consolidación / Informes que llegan tarde / Sobrecostes invisibles / Riesgo de Inspección.

### 5. Cuatro pilares (`#pilares`, fondo blanco)
Cabecera: kicker "CUATRO PILARES", H2 48px "Una plataforma, cuatro cosas que hoy tienes
repartidas." + botón secundario "Verlo en una demo →".
Grid 2×2, gap 20px. Cada tarjeta: padding 32px, borde `#E4E8F0`, radio 18px, sombra
`0 6px 20px -14px rgba(10,18,38,.22)`; badge 34×34 radio 10px con número mono 13px
(01 en `#E8F4F1`/`#0E9384`; 02–04 en `#EAEFFC`/`#1D4ED8`); H3 24px/800; párrafo 16px/1.6
`#414C63`; chips mono 11px sobre `#F5F6F9`, radio 8px.
Contenido: 01 Cumplimiento sin esfuerzo · 02 Operación bajo control · 03 Decisiones con
datos · 04 Fácil para todos (textos §6.4).

### 6. Cómo funciona (fondo `#0A1226`)
Kicker `#7FA0F5`, H2 44px blanco "Tres pasos, y el resto lo hace la plataforma."
3 celdas `#0D1730`, borde `#232C43`, radio 16px, padding `34px 30px`; hover fondo `#121E3D`
+ `translateY(-4px)`. Pasos: Ficha / Gestiona / Decide (textos §6.5).

### 7. Inteligencia operativa (`#inteligencia`)
Grid `1fr 1fr`, gap 64px. Izquierda: kicker, H2 46px "La diferencia no está en fichar.
Está en lo que pasa después.", párrafo 17px, aviso legal-tono en caja `#F7F8FB` con barra
lateral 3px `#0E9384` ("Indicadores de apoyo a la gestión… nunca un sustituto del criterio
humano."), enlace "Ver la inteligencia operativa en una demo →" con subrayado 2px `#1D4ED8`.
Derecha: 2 tarjetas de índice (Fiabilidad 94 %, Eficiencia 87 %; cifra 34px/800; barra de
progreso 6px sobre `#EDF0F6`, relleno `#1D4ED8` / `#0E9384`) + tarjeta "COSTE REAL POR
CENTRO · MES" con "2 anomalías" en `#B4560A` y 4 barras: Madrid 18,2 k€ (82 %),
Ibiza 15,1 k€ (68 %), Valencia 10,4 k€ (47 %, relleno `#B4560A`), Barcelona 13,0 k€ (59 %).

### 8. Cumplimiento (`#cumplimiento`, fondo `#F7F8FB`)
Izquierda: tabla comparativa (grid `1.3fr 1fr 1fr`, `gap:1px` sobre `#E4E8F0`, radio 16px,
sombra `0 20px 50px -30px rgba(10,18,38,.35)`). Cabecera: "GARANTÍA" / "EXCEL / PAPEL" /
"CHECKBIZ360" (esta última sobre `#0A1226`, texto blanco). Filas (hover `#F7F8FB`):
hora exacta al segundo, historial inalterable, corrección con motivo, acceso del trabajador,
conservación 4 años → columna CheckBiz360 sobre `#F0F6F4` en `#0E9384` 700.
Derecha: kicker `#0E9384`, H2 46px "La tranquilidad de tenerlo todo en regla.", párrafo,
CTA oscuro `#0A1226` (hover `#1D4ED8`) "Descarga la guía «Prepara tu empresa para una Inspección»".

### 9. Integraciones / ERP (fondo blanco) — **ojo, copy nuevo**
Kicker "¿YA USAS UN ERP?", H2 46px "No sustituye a tu ERP. Lo completa."
Párrafo: CheckBiz360 se coloca al lado del ERP y añade cumplimiento horario, tareas de
campo y expediente documental; **si necesitas integrarlo, el equipo de EncodeBiz se
encarga: solo hay que solicitarlo y se estudia la viabilidad.**
3 tarjetas (mismo estilo que pilares, número mono `#1D4ED8`):
1. **Lo solicitas** — nos cuentas qué ERP usas y qué datos deben viajar.
2. **Lo estudiamos** — condiciones mínimas: API disponible, permisos y datos identificables.
3. **Nosotros lo hacemos** — si es viable, EncodeBiz desarrolla y mantiene la integración.
Cierre: caja `#F7F8FB` con "Somos una empresa de desarrollo: si tu operación necesita algo
a medida, es una conversación, no un ticket cerrado." + CTA azul "Solicitar estudio de
integración".
> **No mencionar Rentman en esta versión.**

### 10. Sectores (`#sectores`, fondo `#0A1226`)
Kicker `#7FA0F5`, H2 44px "Donde el turno cambia cada día y el coste no espera."
Grid 3×2 de celdas `#0D1730` (borde `#232C43`, radio 16px, padding 28px, hover `#121E3D`
+ `translateY(-4px)`). Orden GTM: 01 Eventos y audiovisual · 02 Hostelería ·
03 Retail multi-tienda · 04 Logística y campo · 05 Servicios y mantenimiento.
Sexta celda con borde discontinuo `#303A54`: "¿Tu sector no está aquí?…" + "Hablemos →".

### 11. Prueba social (fondo blanco)
Kicker, H2 44px "Empresas como la tuya, contándolo con sus palabras." 3 `figure`
(padding 30px, borde `#E4E8F0`, radio 18px, hover elevación): kicker mono `#0E9384`,
`blockquote` 17px/600, párrafo 14px `#5B6479`, `figcaption` con nombre 14px/700 y cargo
mono 11px `#7B8494` sobre borde superior `#EDF0F6`. Testimonios reales existentes:
Luis M. Acevedo (Litoral Group), Michel Ferrada (Ferrada), Yoan Céspedes (ACB).

### 12. Planes (`#precio`, fondo `#F7F8FB`)
Cabecera: kicker "PLANES", H2 46px "Empieza por lo que necesitas hoy. Amplía cuando
crezcas."; a la derecha "desde 2 €" 44px/800 + "por empleado / mes · 45 días de prueba"
mono 12px. Dos planes:
- **Bronze** (tarjeta blanca): control horario con validación GPS, tareas con evidencia y
  validación, inteligencia operativa básica, app iOS/Android. CTA secundario "Crear cuenta gratuita".
- **Enterprise** (tarjeta `#0A1226`, sombra `0 40px 70px -40px rgba(10,18,38,.7)`, badge
  "MULTI-CENTRO" `#1D4ED8` arriba a la derecha): todo lo de Bronze + gestión documental,
  análisis de costes y anomalías, multi-entidad y vista global. CTA azul "Agendar demo de 30'".
Cierre: caja blanca con barra 3px `#1D4ED8`: "**Nosotros te lo dejamos montado y formamos a
tu equipo.** Puesta en marcha y capacitación incluidas, sin coste. Sin permanencia para empezar."

### 13. FAQ
Max 920px. H2 40px "Preguntas frecuentes". 5 `<details>` (padding `22px 24px`, borde
`#E4E8F0`, radio 14px). `summary` 17px/700 con "+" `#1D4ED8` a la derecha; respuesta
15px/1.6 `#414C63`. Preguntas: aparato / ley española / empezar solo con control horario /
ERP (respuesta = solicitarlo y condiciones mínimas) / precio.

### 14. CTA final + formulario (`#demo`, fondo `#0A1226`)
Grid `1.05fr .95fr`. Izquierda: H2 54px/800 blanco "Deja de reaccionar a tu operación.
Empieza a gobernarla.", párrafo `#A7B1C6`, CTA blanco "Empieza gratis — 45 días" +
CTA fantasma con borde `#303A54`.
Derecha: formulario `#0D1730`, borde `#232C43`, radio 18px, padding 32px, sombra
`0 40px 70px -40px rgba(0,0,0,.7)`. Campos (`#0A1226`, borde `#2A344C`, radio 10px,
padding 14px): Nombre + Teléfono (2 col), Email de trabajo, Empresa; selector "Número de
trabajadores" en 4 opciones (<10, 10–50, 51–200, 200+) tipo chip con hover borde `#4F7CFF`;
botón azul "Quiero conocer CheckBiz360"; nota de privacidad 12px con enlace `#7FA0F5`.
**Sustituir el `onSubmit` neutralizado por el envío real y validación.**

### 15. Footer
Fondo `#070C18`, texto `#8B94A8`, padding `44px 48px`. Marca "CheckBiz360, de EncodeBiz"
con cuadro azul 26px. Enlaces: Aviso legal, Cookies, Privacidad (a encodebiz.com), hover blanco.

## Interactions & Behavior
- **Scroll reveal**: cada bloque con `[data-reveal]` entra con `opacity 0→1` y
  `translateY(22px)→0`. Implementado con animaciones ligadas al scroll
  (`animation-timeline: view(); animation-range: entry 4% cover 24%`) para no tocar el DOM;
  en un stack con librería, usar el equivalente (IntersectionObserver + clase, Framer Motion
  `whileInView`, etc.), easing `linear`/`ease-out`, ~0.7 s.
- **Barras de gráficos**: crecen desde 0 al entrar en pantalla — verticales `scaleY`
  (`transform-origin: bottom`), horizontales `scaleX` (`transform-origin: left`),
  `cubic-bezier(.2,.8,.2,1)`, rango `entry 10% cover 34%`.
- **Hover de tarjetas** (`.cb-lift`): `translateY(-5px)`, sombra
  `0 34px 60px -34px rgba(10,18,38,.42)`, borde → `#C2CDE4`, transición
  `.32s cubic-bezier(.2,.7,.2,1)`.
- **Hover de celdas oscuras**: fondo `#121E3D`, `translateY(-4px)`, `.28s`.
- **Hover de CTA**: `translateY(-2px)` + sombra azul más marcada, `.22s`.
- **Filas de tabla**: fondo `#F7F8FB` al hover, `.2s`.
- **Pulsos**: punto verde de la píldora (`scale`/`opacity`, 2.4 s) y nodos del grafo
  (opacidad `.18↔.6`, 8 s, delays escalonados). Nada más animado en bucle.
- **Nav**: anclas con scroll suave; subrayado azul 2px al hover.
- **FAQ**: `<details>` nativo (un panel puede quedar abierto sin cerrar los demás).
- Respetar `prefers-reduced-motion`: desactivar reveals, crecimiento de barras y pulsos.
- **Responsive** (no maquetado, a definir en implementación): a ≤1024px pasar los grids de
  2/3 columnas a 1, H1 a ~48–56px, mockup del panel a scroll horizontal o simplificado,
  nav a menú desplegable.

## State Management
Página estática. Estado necesario: solo el del formulario de demo (nombre, teléfono, email,
empresa, tramo de nº de trabajadores, aceptación de privacidad) + estados de envío
(idle / enviando / éxito / error) y validación (email y teléfono obligatorios, consentimiento
requerido). El tramo de empleados se usa para cualificar el lead.

## Design Tokens
**Color**
- Ink: `#0A1226` (base oscura y texto) · `#070C18` (footer) · `#0D1730` (celda oscura) ·
  `#121E3D` (hover) · `#232C43` / `#303A54` / `#2A344C` (bordes oscuros)
- Texto: `#0A1226` · `#414C63` · `#5B6479` · `#6B7484` / `#7B8494` (mono) · `#9AA2B2` (apagado)
- Sobre oscuro: `#EDF0F6` · `#C3CBDB` · `#A7B1C6` · `#8B94A8` · `#7FA0F5` (acento claro)
- Superficies: `#FFFFFF` · `#F7F8FB` · `#F5F6F9` · `#EDF0F6`
- Bordes: `#E9ECF2` · `#E4E8F0` · `#DDE2EC` · `#D8DCE4` · `#CFD5E0` · `#C2CDE4` (hover)
- Acento primario: `#1D4ED8`; hover/pressed `#173FAF`; tintes `#EAEFFC`
- Acento secundario (cumplimiento): `#0E9384`; tinte `#E8F4F1` / `#F0F6F4`
- Alerta/atención: `#B4560A`; borde `#F0C9A8`

**Tipografía**
- Titulares y cuerpo: **Manrope** (400/500/600/700/800)
- Etiquetas, datos y microcopy: **IBM Plex Mono** (400/500)
- Escala: H1 88 / H2 54–40 / H3 24–21 / cuerpo 21–14 / mono 12–9
- `letter-spacing`: −.045em en H1, −.035em en H2, −.02em en H3; mono en uppercase con
  `.12–.16em`
- `line-height`: .95 (H1), 1.04–1.08 (H2/H3), 1.5–1.62 (cuerpo)
- `text-wrap: balance` en titulares, `pretty` en párrafos largos

**Espaciado**: secciones `112px` vertical (hero `104px`), padding lateral `48px`,
contenido máx. `1180px`; gaps 64 / 48 / 40 / 20 / 14 / 10; padding de tarjeta 36 / 32 / 30 / 22.

**Radios**: 18px (tarjetas grandes) · 16px (tarjetas medias) · 14px (tarjetas menores /
FAQ) · 12–11px (botones) · 10–8px (chips, inputs, badges) · 999px (píldora).

**Sombras**
- Tarjeta base: `0 6px 20px -14px rgba(10,18,38,.22)`
- Tarjeta hover: `0 34px 60px -34px rgba(10,18,38,.42)`
- Mockup del panel: `0 60px 100px -50px rgba(10,18,38,.6)` + `0 18px 40px -24px rgba(10,18,38,.35)`
- Plan Enterprise / formulario: `0 40px 70px -40px rgba(10,18,38,.7)`
- CTA azul: `0 18px 34px -16px rgba(29,78,216,.85)`

## Assets
- **No hay imágenes**: el mockup del panel y los gráficos son HTML/CSS; el grafo de fondo
  es SVG inline decorativo (`aria-hidden`).
- **Pendiente de aportar por el cliente**: logos de Litoral Group, ACB y Ferrada (hoy
  lockups de texto), logo oficial de CheckBiz360/EncodeBiz (hoy cuadro con la letra "C"),
  y opcionalmente foto de equipo y capturas reales de producto.
- Enlaces externos ya reales: `saas.encodebiz.com/auth/register` (alta),
  `encodebiz.com/aviso-legal`, `/politica-cookies`, `/politicas-de-privacidad`.

## Files
- `Landing CheckBiz360.dc.html` — el diseño completo (referencia principal).
- `support.js` — runtime del prototipo, **no portar**.
- Fuente de copy: `DOCS/MARKETING/estrategia-y-copy-landing-checkbiz360.md` (§6) y
  `DOCS/MARKETING/diferenciadores-y-especificaciones-checkbiz360.md`.

## Notas de contenido (importantes para no sobreprometer)
- No prometer funciones pendientes de desarrollo (firma electrónica, exportación de
  costes/anomalías, modo offline, alertas de coste configurables).
- La inteligencia operativa se comunica **desde equidad y objetividad**, nunca como
  vigilancia; mantener el aviso visible de "indicadores de apoyo, no veredictos".
- Precio (2 €/empleado/mes) y 45 días de prueba están pendientes de validación final por
  dirección: dejarlos en un lugar fácil de editar.
