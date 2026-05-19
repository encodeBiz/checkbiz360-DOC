# Reglas de Ingeniería — Todos los Stacks

> Protocolo unificado de ingeniería para encodeBiz-SAAS, encodebiz-front-saas y CheckBiz360.
> Aplica a cualquier desarrollador o asistente IA trabajando en este ecosistema.

## 1. Reglas Irrompibles

1. No inventar endpoints, campos o comportamientos que no estén en esta documentación o en el código existente.
2. No realizar operaciones destructivas sin confirmación explícita del usuario (rm -rf, reset --hard, drop table).
3. No saltarse hooks ni validaciones (`--no-verify`, bypass de auth en tests).
4. No commitear sin revisar lo que se está incluyendo (nunca `git add -A` ciego).
5. No hacer push a `main` o `master` sin aprobación.
6. No hardcodear strings de interfaz — usar i18n siempre.
7. No hardcodear números mágicos — usar constantes con nombre.
8. No usar `any` en TypeScript sin comentario justificado.
9. No añadir lógica de negocio en widgets Flutter ni en componentes React.
10. No asumir que el estado local es el estado real — siempre verificar contra backend/Firestore.

## 2. Arquitectura

### Principios
- **SRP**: cada clase/función tiene una sola responsabilidad
- **DRY**: si se repite más de dos veces, extraer
- **YAGNI**: no diseñar para requisitos futuros hipotéticos
- **KISS**: la solución más simple que funcione

### Capas (Backend)
```
interfaces/http/    → controllers (validación, permisos, mapeo HTTP)
application/        → use cases (lógica de negocio, orquestación)
domain/             → entities, value objects, interfaces de repos
infrastructure/     → repositorios Firestore, externos
```

### Capas (App Móvil)
```
presentation/       → widgets, screens, providers Riverpod
application/        → use cases, lógica de negocio
data/               → datasources (Firestore, HTTP via Dio)
domain/             → entities, interfaces de repositorios
```

### Capas (Backoffice)
```
app/(routes)/       → páginas Next.js (server components por defecto)
components/         → UI atómica (atoms → molecules → organisms)
hooks/              → lógica reutilizable (useEntity, useAuth, etc.)
services/           → llamadas HTTP
lib/                → utilidades, constantes, tipos
```

## 3. Calidad de Código

- Funciones < 40 líneas (idealmente < 20)
- Naming: verbos para funciones, sustantivos para clases/tipos
- Comentarios solo cuando el PORQUÉ no es obvio — nunca el QUÉ
- Tests: unitarios para lógica de negocio, integración para repos Firestore
- Todo `async` debe tener manejo de errores explícito
- Evitar callbacks anidados — usar `async/await`

## 4. Seguridad

- Nunca enviar secretos en el código fuente ni en logs
- Validar toda entrada en el borde del sistema (controllers/routes)
- Principio de mínimo privilegio: pedir solo los permisos necesarios
- Reglas de Firestore para operaciones directas desde cliente
- Usar Cloud Functions para operaciones sensibles (nunca directamente desde cliente)
- OWASP Top 10: SQL injection, XSS, CSRF — aplicar en todo endpoint
- Firebase App Check activo en producción

## 5. Testing

```
Pirámide:
    /\
   /E2E\          (pocos, costosos)
  /------\
 /integr. \       (repos Firestore, endpoints)
/------------\
/ unit tests  \   (muchos, rápidos, baratos)
```

- Unitarios: lógica de dominio, use cases, helpers
- Integración: repositorios Firestore, controllers con mocks de repos
- E2E: flujos críticos (checkin, task approval)

## 6. Stack por Capa

### TypeScript (Backend)
- `strict: true` en tsconfig
- ESLint con reglas de Anthropic (quote-props, operator-linebreak, no-multi-spaces)
- Imports: absolute paths desde `src/`
- No `require()` excepto en lazy imports (cold start)

### Flutter (App)
- Null safety obligatorio
- `const` constructors siempre que sea posible
- No lógica de negocio en `build()`
- `autoDispose` en providers de detalle (evitar memory leaks)
- Prefer `AsyncValue` sobre gestión manual de loading/error states

### Next.js (Backoffice)
- Server Components por defecto; `"use client"` solo cuando sea necesario (eventos, hooks)
- Atomic Design: atoms → molecules → organisms → templates → pages
- i18n: todos los strings via `useTranslations()`, nunca hardcodeados
- Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 7. Git y Commits

### Formato Conventional Commits
```
<type>(<scope>): <descripción>

feat(task): add supervisor resource upload permission
fix(checklog): handle Firestore Timestamp in Mode B
refactor(checkinbiz): unify canManageTask permission function
docs(task): update supervisor permissions in unified doc
```

### Tipos
- `feat`: nueva funcionalidad
- `fix`: bug fix
- `refactor`: reestructuración sin cambio funcional
- `docs`: solo documentación
- `test`: tests
- `chore`: mantenimiento (deps, config)

### Ramas
- `main` — producción, protegida
- `feat/<nombre>` — nueva feature
- `fix/<nombre>` — bug fix
- `docs/<nombre>` — solo documentación

## 8. Firebase / Firestore

- Índices compuestos documentados en `firestore.indexes.json`
- Nunca leer documentos completos si solo se necesitan campos específicos — usar `select()`
- Operaciones batch para escrituras atómicas relacionadas
- `FieldValue.arrayUnion()` para arrays append-only (requestUpdates, etc.)
- `set({merge: true})` hace deep merge — NO reemplaza nested maps
- Timestamps: Firestore devuelve objetos `Timestamp` (con `.toDate()`) — nunca asumir `Date` nativo
- Cold start: heavy deps (sharp, pdfkit, twilio, nodemailer) con lazy import

## 9. Notificaciones Push (FCM)

- Tipo `update_checklog_pending` para validaciones de checklog pendientes
- Incluir siempre: `updateId`, `id` (docId), `entityId`, `employeeId`, `requestAction: true`
- El idioma del empleado (`employee.language`) determina el mensaje
- Las notificaciones son fire-and-forget — nunca bloquear el flujo principal esperando FCM

## 10. Comunicación IA / Desarrollador

- Siempre leer el código antes de proponer cambios
- Citar rutas y líneas exactas en las respuestas
- Fallar con claridad si falta contexto — no inventar
- Si algo puede romper producción: preguntar antes de ejecutar
- Documentar en este repo toda decisión arquitectónica no obvia
