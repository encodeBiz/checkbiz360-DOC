# Capa Backoffice — encodebiz-front-saas

## 1. Stack

| Componente | Tecnología |
|---|---|
| Framework | Next.js 14 (App Router) |
| UI | Material UI v5 |
| State | React hooks + Context |
| Forms | Formik |
| HTTP | Fetch nativo + custom hooks |
| i18n | next-intl (`useTranslations()`) |
| Auth | Firebase Auth (session tokens) |
| Linting | ESLint + Prettier |
| Estilos | MUI v6 + `sx` props |

## 2. Estructura de Carpetas

```
src/
  app/main/[entityId]/checkinbiz/   → rutas App Router de CheckBiz
    calendar/                       → módulo calendario
    tasks/                          → módulo tareas
    branch/[id]/                    → detalle de sucursal
    employee/[id]/                  → detalle de empleado
  components/                       → UI compartida (Atomic Design)
  services/checkinbiz/              → servicios HTTP por módulo
  domain/features/checkinbiz/       → tipos / contratos (I*.ts)
  hooks/                            → useEntity, useAuth, useAppLocale, useToast, useLayout
  lib/firebase/                     → utilidades Firestore
locales/{es,en,fr,de}/common.json   → strings i18n
```

## 3. Patrones Obligatorios

### Server Components por defecto

`"use client"` solo cuando sea necesario (eventos, hooks, estado local). Cada uso debe justificarse.

### i18n

Todo string visible va por `useTranslations()`. Sin strings en español hardcodeados en TSX.

```typescript
const t = useTranslations("calendar");
<span>{t("save")}</span>
```

### Servicios

Una función por endpoint en `src/services/<module>/<feature>.service.ts`. Errores via `mapperErrorFromBack`.

### Tipos

En `src/domain/features/<module>/I<Entity>.ts`.

### Mutaciones Firestore

Las mutaciones siempre van por HTTP handler — nunca directamente desde la UI. Las lecturas simples pueden usar Firestore SDK directo.

### Atomic Design

```
Atoms → Molecules → Organisms → Templates → Pages
```

Componentes pequeños, puros, testeables.

## 4. Rutas de CheckBiz

```
src/app/main/[entityId]/checkinbiz/
  calendar/page.tsx          → tabs EntityCalendarTab + EmployeeHolidaysTab
  tasks/                     → listado, detalle, crear
  branch/[id]/detail/        → detalle de sucursal con BranchCalendarDetail
  employee/[id]/detail/      → detalle de empleado con EmployeeCalendarDetail
```

### Task Module

Rutas:
- Listado: `/main/[entityId]/checkinbiz/tasks`
- Crear: `/main/[entityId]/checkinbiz/tasks/new`
- Detalle: `/main/[entityId]/checkinbiz/tasks/:taskId`

Fuente de verdad para integración: `docs/DOCUMENTATION/05-task-frontend-integration.md`

## 5. Hooks Compartidos

| Hook | Propósito |
|---|---|
| `useEntity` | Datos de la entidad activa |
| `useAuth` | Usuario autenticado y permisos |
| `useAppLocale` | Locale activo |
| `useToast` | Notificaciones toast |
| `useLayout` | Control de layout |

## 6. Web Vitals Objetivo

| Métrica | Objetivo |
|---|---|
| LCP | < 2.5s |
| INP | < 200ms |
| CLS | < 0.1 |

## 7. Bugs del Módulo Calendario

Ver [modulos/calendario.md](../modulos/calendario.md#5-bugs-conocidos-en-el-backoffice) para el listado completo de 7+ bugs documentados con rutas y líneas exactas.

Los más críticos antes de tocar `CalendarSection.tsx`:
1. `useEffect` dentro de render-prop de Formik (viola Rules of Hooks)
2. IDs inconsistentes en ausencias de empleado (causa duplicaciones)
3. Estado local no usa respuesta del backend (divergencia de IDs)

## 8. Comandos

```bash
npm run dev      # Next.js dev server
npm run build    # Build de producción
npm run lint     # ESLint
```

## 9. Convenciones de Código

- React hooks al principio del componente — **nunca dentro de render-props o callbacks**
- Errores via `mapperErrorFromBack` — nunca `console.error` silencioso
- Invalidar caché tras mutaciones críticas
- Refrescar detalle y actividad tras cada acción importante
- `any` prohibido — usar `unknown` y narrowing si es inevitable
- No hacer llamadas directas a Firebase desde componentes UI
