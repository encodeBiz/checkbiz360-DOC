# Conector para asistentes (Claude y ChatGPT) — Documento de Ingeniería

**Proyecto:** encodebiz-api
**Dominio:** `services/assistant` (nuevo) — acceso de un asistente de IA a checkbiz360 en nombre de un cliente
**Fecha de inicio:** 2026-10-15
**Estado:** Fase 1 (acceso) en staging desde el 2026-10-15 y probada con ChatGPT el 2026-10-16. Fase 2 (la semana) diseñada el 2026-10-16: ADR-004 a ADR-006 y TDR-002.
**Autor:** Jose Acevedo

---

## Contexto y Motivación

El conector del CRM (`sales-crm`, ADR-005) enseñó dos cosas en una semana: que hablarle a la
plataforma desde Claude funciona, y que lo que más tiempo quita a un cliente no es consultar,
es **configurar**. Cada lunes un administrador vuelve a montar la semana: horarios por
persona, tareas por servicio, sustituciones. La lectura de cuadrantes ya ataca una parte
(el impreso del ERP se convierte en horario y tareas), pero el cliente que planifica de
cabeza, o con una hoja, sigue tecleando.

La idea es que ese administrador conecte checkbiz360 a su Claude o a su ChatGPT **una vez**,
entrando con su cuenta del panel, y a partir de ahí diga lo que quiere: «la misma semana que
la pasada, pero Marta cubre a Lucía el martes y el jueves». El asistente propone, enseña la
semana con sus horas, el administrador aprueba y entonces se escribe.

Antes de que nada de eso exista hay que resolver **quién es el que habla**. El conector del
CRM va con un token en la URL porque el único usuario somos nosotros. Con clientes, cada
conexión es una persona concreta en una empresa concreta, con sus permisos, y revocable. Eso
es OAuth, y es la fase 1.

## Principio de diseño

> **El asistente es una persona más entrando por otra puerta. Mismo usuario, mismo segundo
> factor, mismos permisos; y nada se escribe sin que esa persona lo haya visto.**

De ahí salen las decisiones que gobiernan el resto:

1. **La identidad es la de Firebase Auth** ([ADR-001](./adr/ADR-001-la-identidad-es-la-de-firebase-auth.md)).
   No hay usuarios nuevos ni un proveedor de identidad aparte: el administrador entra con su
   correo y contraseña (o Google) y su segundo factor, igual que en el panel. La plataforma
   emite los tokens OAuth que Claude y ChatGPT necesitan, apoyándose en esa identidad.
2. **Una conexión es una persona en una empresa** ([ADR-002](./adr/ADR-002-una-conexion-es-una-persona-en-una-empresa.md)).
   La empresa va en la URL del conector: cada empresa es un conector distinto para Claude o
   ChatGPT, el token queda atado a un `uid` y a esa empresa, el modelo nunca maneja ids de
   empresa y la revocación es por empresa.
3. **Sólo clientes conocidos** ([ADR-003](./adr/ADR-003-solo-clientes-conocidos.md)). El
   servidor de autorización sólo devuelve códigos a Claude y a ChatGPT. Nadie registra un
   «asistente» propio para que un cliente le dé acceso sin querer.
4. **El token del asistente no sale del servicio.** Las herramientas llaman al núcleo con la
   clave S2S y el `actorUid` de la conexión, como ya hace la tarea de sistema de `tasks`, y el
   núcleo vuelve a comprobar los permisos de esa persona. Un token OAuth nunca se reenvía.

## Alcance

**Fase 1 — acceso (este diseño):** servicio `assistant` con el servidor de autorización
OAuth 2.1 (metadatos, registro de cliente, pantalla de inicio de sesión y consentimiento,
emisión y rotación de tokens, revocación) y el servidor MCP con **una sola herramienta de
prueba** que dice quién está conectado y a qué empresa. Probado en staging desde claude.ai y
desde ChatGPT. Detalle en [TDR-001](./tdr/TDR-001-servidor-de-autorizacion-sobre-firebase-auth.md).

**Fase 2 — la semana** ([TDR-002](./tdr/TDR-002-herramientas-de-la-semana.md)): el asistente
es un lector más del lote de la plantilla de cuadrantes (copiar la semana, de cero o desde un
documento que el cliente sube a su IA), con el Excel relleno para revisar; cambios sueltos de
tareas y la semana tipo del modo estándar por una puerta delegada que respeta los permisos de
la persona; y una semana propuesta de nuevo retira lo que ya no trae.

**Fase 3 — panel y producto:** pantalla «Conexiones» en el panel para ver y cortar accesos,
ficha del add-on en el catálogo con la URL de conexión de cada empresa para copiar, cobro, condiciones (los nombres de los empleados viajan al
proveedor que el cliente eligió), y pase a producción.

**Fuera, y explícitamente:** cualquier escritura automática sin aprobación de una persona;
acceso de empleados o supervisores por el conector (v1 es sólo para `owner` y `admin`);
cambiar el conector del CRM, que sigue como está.

## Lo que ya existe y se reutiliza

| Pieza | Dónde | Para qué sirve aquí |
|---|---|---|
| Servidor MCP sin sesión, un transporte por petición | `services/sales/src/interfaces/mcp/crm.mcp.ts` | El mismo montaje para el MCP del asistente |
| Inicio de sesión del panel | `encodebiz-front-saas/src/lib/firebase/authentication/login.ts` | Correo+contraseña y Google: los mismos dos caminos en la pantalla de consentimiento |
| Segundo factor del panel | `checkinbiz` `/auth/2fa/user/status` y `/verify` | Se exige en la autorización igual que en el panel |
| Asiento en la empresa | `user_entity_roles/{uid}_{entityId}` (`canWrite`, `entityRole`) | Quién puede conectar qué empresa |
| Actor delegado por S2S | `tasks` `POST /system` con `actorUid`; `merlin` `puertaDeServicio` | Cómo llega la identidad del cliente al núcleo sin reenviar tokens |
| Propuestas de cuadrante | `merlin/src/soporte/cuadrantes` | El ciclo proponer → aprobar → aplicar de la fase 2 |

## Documentos

| Documento | Estado |
|---|---|
| [ADR-001 — La identidad es la de Firebase Auth](./adr/ADR-001-la-identidad-es-la-de-firebase-auth.md) | Aceptado (Jose, 2026-10-15) |
| [ADR-002 — Una conexión es una persona en una empresa, y la empresa va en la URL](./adr/ADR-002-una-conexion-es-una-persona-en-una-empresa.md) | Aceptado (Jose, 2026-10-15) |
| [ADR-003 — Sólo clientes conocidos](./adr/ADR-003-solo-clientes-conocidos.md) | Aceptado (Jose, 2026-10-15) |
| [TDR-001 — Servidor de autorización sobre Firebase Auth](./tdr/TDR-001-servidor-de-autorizacion-sobre-firebase-auth.md) | Implementado, en staging |
| [ADR-004 — El asistente es un lector más del lote](./adr/ADR-004-el-asistente-es-un-lector-mas-del-lote.md) | Aceptado (Jose, 2026-10-16) |
| [ADR-005 — La persona delegada por la puerta de servicio](./adr/ADR-005-la-persona-delegada-por-la-puerta-de-servicio.md) | Aceptado (Jose, 2026-10-16) |
| [ADR-006 — Retirar lo que ya no está](./adr/ADR-006-retirar-lo-que-ya-no-esta.md) | Aceptado (Jose, 2026-10-16) |
| [ADR-007 — El cuadrante se llena por tandas](./adr/ADR-007-el-lote-se-llena-por-tandas.md) | Aceptado (Jose, 2026-10-16) |
| [TDR-002 — Las herramientas de la semana](./tdr/TDR-002-herramientas-de-la-semana.md) | En implementación |

## Decisiones cerradas (Jose, 2026-10-15)

Las cuatro quedaron con el valor por defecto del TDR:

1. **Nombre del servicio:** `services/assistant`, puerto `3017`, ruta `/api/v1/assistant`.
   Es lo que ve el cliente: «Asistente».
2. **Sólo `owner` y `admin` en v1.** Un supervisor con responsabilidad de sucursal no puede
   conectar. Se abre cuando haya herramientas de sucursal (fase 2).
3. **Claude Code y otros clientes con redirección a `localhost`:** fuera para clientes; sólo
   en desarrollo, por variable de entorno, para probar nosotros.
4. **Credenciales manuales:** si un cliente configura el conector pegando client id y secret
   (la casilla «Avanzado» de claude.ai), el servidor las acepta. No hace falta para la prueba.

## Lo que hay que verificar en la primera prueba

Dos datos salen de documentación de terceros, porque el artículo de soporte de Anthropic no
se pudo abrir el 2026-10-15: la URL de retorno de claude.ai
(`https://claude.ai/api/mcp/auth_callback`, con aviso de que puede pasar a `claude.com`) y
que claude.ai usa documentos de metadatos de cliente (CIMD) además del registro dinámico. El
TDR deja las dos cosas como lista configurable y la prueba en staging las confirma.
