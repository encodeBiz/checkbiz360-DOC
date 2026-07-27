# Security-Audit — EncodeBiz / CheckBiz360

Auditoría de seguridad del ecosistema EncodeBiz realizada el **2026-05-25**.

Cubre los tres sub-proyectos: backend Firebase Functions, backoffice Next.js y app móvil Flutter.

---

## Índice de auditorías

### 2026-05-25

| Archivo | Descripción |
|---|---|
| [AUDIT-BACKEND.md](./2026-05-25/AUDIT-BACKEND.md) | Hallazgos en `encodeBiz-SAAS` (Cloud Functions, Firestore, Storage) |
| [AUDIT-BACKOFFICE.md](./2026-05-25/AUDIT-BACKOFFICE.md) | Hallazgos en `encodebiz-front-saas` (Next.js, API routes, auth) |
| [AUDIT-MOBILE.md](./2026-05-25/AUDIT-MOBILE.md) | Hallazgos en `checkbiz360` (Flutter, Dio, SecureStorage) |
| [REMEDIATION-PLAN.md](./2026-05-25/REMEDIATION-PLAN.md) | Plan de remediación priorizado con owners y fechas objetivo |

---

## Resumen ejecutivo

| Severidad | Total | Crítico | Alto | Medio | Bajo |
|---|---|---|---|---|---|
| Hallazgos | **17** | 5 | 5 | 5 | 2 |

### Hallazgos críticos — acción inmediata requerida

| ID | Proyecto | Descripción |
|---|---|---|
| BE-01 | Backend | Service account JSON keys comprometidos en disco (3 archivos) |
| BE-02 | Backend | `functions/.env` con secretos de producción (Stripe, Twilio, JWT, SMTP) en disco |
| BE-04 | Backend | `storage.rules` catch-all `allow read, write: if true` — Storage público |
| BE-05 | Backend | `firestore.rules` ausente del repositorio — sin control de versiones de reglas |
| BO-01 | Backoffice | `.env.development` con private key RSA completa de service account en disco |

---

## Leyenda de severidades

| Nivel | Impacto | Tiempo objetivo de remediación |
|---|---|---|
| 🔴 CRÍTICO | Compromiso de datos/infraestructura | Inmediato (< 24 h) |
| 🟠 ALTO | Superficie de ataque significativa | Esta semana (< 7 días) |
| 🟡 MEDIO | Mejora de postura de seguridad | Este sprint (< 30 días) |
| 🟢 BAJO | Hardening adicional | Backlog priorizado |

---

## Metodología

La auditoría fue realizada mediante análisis estático del código fuente. Se revisaron:
- Control de secretos y variables de entorno
- Reglas de Firebase (Firestore + Storage)
- Middleware de autenticación y autorización
- Configuración de CORS y headers HTTP
- Almacenamiento de tokens y credenciales en cliente
- Permisos de la aplicación móvil
- Interceptores de red y manejo de errores

No se realizaron pruebas de penetración activas (análisis estático únicamente).
