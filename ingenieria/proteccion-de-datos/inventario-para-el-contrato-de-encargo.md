# Inventario de tratamientos para el contrato de encargo (art. 28 RGPD)

**Para:** la abogada o abogado que redacte el contrato de encargo entre cada empresa cliente
(responsable) y ENCODEBIZ SL (encargado). **Fecha:** 2026-11-04. Lo que no está comprobado se
marca como *pendiente de verificar*; todo lo demás se ha leído del código o de la
configuración real ese día.

## 1. Las partes y el servicio

- **Encargado:** ENCODEBIZ SL, que presta CheckBiz360: registro de jornada, tareas, cuadrantes,
  documentos laborales, inventario y análisis operativo, por web (panel) y app móvil.
- **Responsable:** cada empresa cliente, sobre los datos de sus empleados y de sus propios
  clientes. Se da de alta por internet y acepta los textos legales en el registro y al crear la
  empresa (quién, cuándo, versión, IP y navegador quedan registrados desde noviembre de 2026).
- **Dónde está declarado hoy:** política de privacidad de la plataforma (en inglés, en el panel)
  y guía pública «Conservación y protección de datos» (checkbiz360.com/documentacion). No hay
  contrato de encargo: es lo que hay que redactar.

## 2. Categorías de interesados y de datos

| Interesados | Datos | De dónde salen |
|---|---|---|
| Empleados de la empresa cliente | Nombre, correo, teléfono, DNI (opcional), puesto, centro, foto de perfil, idioma | Los da de alta la empresa (panel, plantilla Excel, asistente) |
| Empleados | **Registro de jornada**: entradas, salidas y pausas con hora; posición GPS **en el momento del fichaje** (no durante la jornada) y si cayó dentro de la geocerca del centro; identificador del dispositivo; fichajes corregidos o cerrados por lote | La app móvil, el punto de fichaje (tablet del centro) o el gestor a mano |
| Empleados | Tareas asignadas y hechas, evidencias (fotos y vídeos cortos), casillas marcadas, valoraciones; cuadrantes y turnos; ausencias y vacaciones; material y EPIs entregados | Panel y app |
| Empleados | **Documentos laborales**: contratos, nóminas u otros que la empresa suba, y documentos firmados electrónicamente (firma PAdES con sello de tiempo, acta de firma con IP y hora) | Servicio documental |
| Empleados | **Análisis operativo** (Merlin): perfiles de cumplimiento («registra», «en riesgo», «sin evidencia»), desviación de horas, puntuación de promoción, quién sostiene la operación. Se calcula con los datos anteriores | Postgres + modelo de lenguaje (ver §4) |
| Empleados | Fotos del punto de fichaje (quiosco), si la empresa lo activa, guardadas unos días (configurable) | Tablet del centro |
| Usuarios del panel (dueños, administradores, gestores) | Nombre, correo, teléfono, rol, segundo factor (TOTP), inicios de sesión | Registro del panel |
| Clientes de la empresa cliente (módulo «cartera de clientes») | Nombre, dirección, contacto, tarifas, documentos | Panel y asistente |
| Datos de pago de la empresa cliente | Tarjeta (solo en Stripe; nosotros guardamos el identificador), facturas | Stripe |

No se tratan categorías especiales (salud, sindicación…) salvo lo que la empresa suba como
documento. Las ausencias se registran como tipo («vacaciones», «baja») sin diagnóstico.

## 3. Dónde están los datos

| Qué | Dónde | Comprobado |
|---|---|---|
| Base de datos principal (fichas, fichajes, tareas, cuadrantes, documentos, usuarios, aceptaciones legales) | Google Cloud, **Unión Europea** | 2026-11-04 |
| **Ficheros**: documentos laborales, PDF firmados, fotos | Google Cloud, **Estados Unidos** en producción (en desarrollo, UE). **Atención:** es el único almacén fuera de la UE; ver §6 | 2026-11-04 |
| Autenticación de usuarios | Google (Firebase Authentication), servicio global | — |
| Base de datos analítica y servidores de la aplicación | Servidores dedicados de OVH en la **Unión Europea** (producción); el entorno de desarrollo, en el Reino Unido (decisión de adecuación) | 2026-11-04 |
| Panel web (alojamiento) | Vercel; no guarda datos; región *pendiente de verificar* | — |

*(El detalle técnico de regiones, servidores y configuración se mantiene en la documentación
interna de ingeniería y no sale de EncodeBiz.)*

## 4. Subencargados (terceros que tocan datos para prestarnos servicio)

| Proveedor | Para qué | Qué recibe | País / garantía |
|---|---|---|---|
| Google Ireland / Google LLC (Firebase, Cloud) | Base de datos, ficheros, autenticación, notificaciones push, geocodificación de direcciones | Todo lo de §3 que está en Google; direcciones de centros para situarlos en el mapa | UE para Firestore; EE. UU. para Storage. Google está adherido al Marco de Privacidad de Datos UE-EE. UU. (DPF) |
| OVH SAS | Servidores (Postgres y API) | Lo de §3 en Postgres | Alemania (prod) y Reino Unido (dev, decisión de adecuación de la Comisión) |
| Amazon Web Services (SES) | Envío de correos: bienvenidas, avisos de tareas, horarios semanales, alertas, facturas | Correo del destinatario, nombre, y el contenido del aviso (tareas, horarios, nombres de compañeros) | Unión Europea, comprobado 2026-11-04 |
| OpenAI (API) | Merlin: relatos del panel, interpretación de patrones, lectura de cuadrantes y plantillas, CRM | **Métricas sin nombres**: desde el 2026-11-04 los nombres de personas se sustituyen por seudónimos (`PERSONA_1`) antes de enviar y se reponen al volver; la lectura de cuadrantes ya lo hacía. Sigue viajando el nombre de los centros y, en la lectura de cuadrantes, horarios | EE. UU. OpenAI está adherida al DPF; los datos de la API no se usan para entrenar (política de OpenAI). *Pendiente de verificar* si hay DPA firmado con OpenAI (se acepta en los términos de la API) |
| Stripe | Cobro de la suscripción | Datos de pago y facturación de la empresa cliente (no de empleados) | Irlanda / EE. UU., DPF |
| Cloudflare (Turnstile) | Comprobar que el registro del panel lo hace una persona | IP y huella del navegador en el registro | EE. UU., DPF |
| Vercel | Alojar el panel | Tráfico del panel (IPs, cabeceras) | EE. UU., DPF |
| Rentman (solo clientes con el add-on) | Sincronizar proyectos y personal con el programa de alquiler del cliente | Lo que el cliente decide sincronizar, con la cuenta Rentman del propio cliente | Países Bajos |
| Anthropic / OpenAI (conector del asistente, solo si el cliente lo conecta) | El gestor opera CheckBiz360 desde Claude o ChatGPT **con su propia cuenta** | Lo que el gestor pide ver o cambiar | El cliente es quien contrata ese asistente; nosotros solo exponemos la API con su sesión |

## 5. Conservación y borrado

- Registros de jornada: **4 años** (art. 34.9 ET), y así lo dice la guía pública.
- Posición del fichaje: se guarda **con el registro**, los mismos 4 años, como prueba de la
  validación. (La guía pública dice hoy que no se guarda; hay que corregirla.)
- Fotos del quiosco: días configurables por la empresa; después se borran por ciclo de vida del
  bucket.
- Documentos, tareas, cuadrantes: mientras dure la relación con la empresa.
- Al terminar el servicio: **no hay hoy un proceso automático de borrado o devolución**. Hay
  exportación a Excel/CSV desde el panel y borrado blando de empleados (`status: fired`). Es
  una obligación del encargado que falta por implementar. *Pendiente.*
- Copias de seguridad: *pendiente de verificar* política y plazo (Postgres y Firestore).

## 6. Medidas de seguridad (art. 32), descripción general

Lo que el contrato puede decir, sin describir cómo está montado nada:

- Aislamiento de los datos de cada empresa cliente, en la base de datos y en el servidor.
- Control de acceso por roles y segundo factor de autenticación para el panel; las operaciones
  sensibles solo las ejecuta el servidor.
- Cifrado en tránsito en todas las conexiones y cifrado en reposo en los proveedores de nube.
- Seudonimización de los datos que salen hacia modelos de lenguaje; geolocalización puntual,
  nunca continua; caducidad automática de las fotos del punto de fichaje.
- Endurecimiento y acceso restringido a los servidores, separación total entre producción y
  desarrollo, secretos fuera del código.
- Trazabilidad: registro de accesos del soporte por persona, de envíos de correo, de firmas
  electrónicas y de aceptaciones legales.
- Personal con compromiso de confidencialidad y formación.
- **Pendientes de dejar por escrito** (el abogado debe saberlo, el cliente no necesita el
  detalle): política de copias de seguridad y restauración, procedimiento de gestión y
  notificación de brechas en 72 horas, proceso de borrado o devolución al fin del servicio, y
  decisión sobre el almacén de ficheros en Estados Unidos (moverlo a la UE o documentar la
  transferencia).

## 7. Lo que el contrato debería recoger (para que el abogado no empiece de cero)

Objeto y duración (mientras dure la suscripción); naturaleza y finalidad (registro de jornada
y gestión operativa por cuenta de la empresa); tipos de datos e interesados (§2); tratar solo
por instrucciones (las del panel y la app son las instrucciones); confidencialidad del
personal; medidas de §6; subencargados de §4 con autorización general y aviso de cambios;
asistencia en derechos de los interesados y en brechas; borrado o devolución al terminar (y
el plazo); auditorías; y el régimen de los modelos de lenguaje (datos seudonimizados, sin
entrenamiento). Modelo de referencia: el de la AEPD para contratos de encargo.
