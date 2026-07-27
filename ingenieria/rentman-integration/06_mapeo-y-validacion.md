# 06 — Mapeo y validación de datos (garantía de integridad)

> **Problema:** Rentman no aporta todos los campos que exigen `Branch` y `Employee` de
> checkbiz360. Crear registros a ciegas produciría **branches donde no se puede fichar** y
> **empleados inválidos**. Este doc define cómo se garantiza la integridad en la sync.

---

## 1. El desajuste (impedance mismatch)

### Branch (checkbiz) — campos obligatorios
De `services/checkinbiz/src/domain/entities/Branch.ts`:

| Campo obligatorio | ¿Fuente en Rentman? |
|---|---|
| `name` | ✅ `project.name` |
| `entityId` | ✅ contexto del tenant |
| `address.street / city / country` | ⚠️ del `contact` de `project.location` (puede faltar) |
| `address.geo {lat, lng}` | ⚠️ `contact.latitude / longitude` (puede venir a 0/null) |
| **radio de geocerca** | ❌ **no existe en Rentman** — solo checkbiz |
| `address.timeZone` (necesario para fichar bien) | ❌ no existe — derivar o manual |
| `advance.workSchedule` / horarios | ❌ no existe — solo checkbiz |
| `disableRatioChecklog` | — default `false` |
| `status` | — lo controla checkbiz |
| `createdAt` | — `now` |

### Employee (checkbiz) — campos obligatorios
De `Employee.ts`:

| Campo obligatorio | ¿Fuente en Rentman? |
|---|---|
| `fullName` | ✅ `crew.displayname` / `firstname`+`lastname` |
| `entityId` | ✅ contexto del tenant |
| `email` | ⚠️ `crew.email` — **puede ser null** |
| `role` (`internal`/`collaborator`) | ❌ no existe — default/regla |
| `status` | ⚠️ derivar de `crew.active` |
| `enableRemoteWork` | ❌ default `false` |
| `branchId[]` | ⚠️ de las asignaciones (`projectcrew`) |
| `createdAt` | — `now` |

---

## 2. Las cinco capas de garantía

### Capa 1 — Validación en el borde
Cada objeto entrante de Rentman pasa por **mapper → validador (zod)** contra el esquema real
de `Branch` / `Employee`. **Nada se escribe en Firestore si no cumple el contrato.**

### Capa 2 — Defaults deterministas
Para lo que checkbiz exige y Rentman no da, pero es asumible sin ambigüedad:
- Employee: `role = "internal"` (regla a confirmar, D3), `enableRemoteWork = false`,
  `status = crew.active ? "active" : "inactive"`, `fullName` desde `displayname`.
- Branch: `disableRatioChecklog = false`, `metadata = { rentmanProjectId, … }`,
  `status = "inactive"` (ver capa 4).

### Capa 3 — Enriquecimiento desde referencias
- **Branch geo/dirección** ← el `contact` referenciado en `project.location`
  (`latitude`, `longitude`, `street`, `city`, `country`).
- **Employee** ← emparejamiento por `email` (y/o DNI) contra empleados existentes
  **antes de crear**, para no duplicar.

### Capa 4 — Estado "pendiente de completar" (no romper, no activar a ciegas)
Cuando falta un dato **esencial que no se puede derivar** (radio de geocerca, huso horario,
geo del branch, email de un empleado sin correo):
1. El registro **se crea en estado `inactive`**.
2. Se marca en el panel como **"Requiere configuración"**, con la **lista de campos que faltan**.
3. **No se puede operar** contra él (no se ficha en un branch sin geocerca) hasta que el
   responsable lo complete **una vez**.
4. **La sync no se bloquea**: sigue con el resto. Un registro incompleto nunca frena la pasada.

Esto es lo que garantiza la integridad: **nunca hay un branch/empleado _activo_ con datos incompletos.**

### Capa 5 — Los campos "solo checkbiz" son intocables por la sync
La sync **solo escribe los campos compartidos del catálogo** (nombre, dirección, estado,
asignación). **Nunca sobreescribe** lo que es propiedad de checkbiz y no existe en Rentman:
- radio de geocerca, `address.timeZone`,
- `advance.workSchedule` y horarios,
- verificación biométrica, dispositivos de confianza, ratios.

Así, cuando el responsable completa un branch una vez, **la siguiente pasada no lo pisa**.

---

## 3. Registro de completitud
El mapping (PostgreSQL) guarda por registro **qué campos faltan** y el **estado**
(`pending_config` / `active`). Alimenta el panel "Requiere configuración" y evita reintentar
crear algo que ya está a la espera de intervención humana.

---

## 4. Decisiones a cerrar

- **D3 — Rol por defecto del empleado importado:** ¿`internal` siempre? ¿O regla (p.ej. según
  `tags` de Rentman)? Afecta permisos.
- **D4 — Geo del branch:** si el contacto de localización no trae `lat/lng`, ¿**geocodificamos**
  la dirección automáticamente, o se deja a completar a mano?
- **D5 — Crew sin email:** ¿se crea el empleado en `pending_config` (sin poder invitarlo hasta
  tener email), o se omite hasta que tenga correo en Rentman?
