# TDR-001 — Servicio, conexión y datos propios

**Fecha:** 2026-10-26
**Estado:** Diseño propuesto
**Componente:** `encodebiz-api` — `services/a3nomina` (nuevo)
**Decisiones de referencia:** [ADR-006](../adr/ADR-006-a3-es-la-ultima-pieza.md),
[contrato de activación de add-ons](../../integraciones/contrato-activacion.md)

---

## 1. Dónde vive

Un servicio nuevo con la plantilla de siempre: Express, un contenedor, `/health`, `expose`
sin `ports:`.

| | Propuesta | Nota |
|---|---|---|
| Carpeta | `services/a3nomina` | Por el tercero, como `services/rentman` |
| `addonId` | `nominabiz-a3` | Patrón Biz, como `fleetbiz-glovo`: el producto es nuestro y el vendor es Wolters Kluwer. **Decisión abierta**: el nombre comercial |
| Puerto | `3018` | El siguiente libre después de `assistant` (3017) |
| Ruta pública | `/api/v1/nominabiz-a3` | Igual que el `addonId`, como pide el contrato |

Nada entra en `encodeBiz-SAAS`. Del núcleo se lee en solo lectura:

- Postgres: `employee_daily_reports`, `checklogs_raw`, `dim_calendars`, `dim_calendar_days`.
- Firestore: `absence_requests`, empleados, sucursales y la entidad, a través de `@encodebiz/shared`.

## 2. Capas

```
domain/
  periodo.ts           Periodo, LineaCierre, Concepto (los conceptos de CheckBiz, cerrados)
  medicion.ts          reglas puras: nocturnas, festivo, exceso (TDR-002 §3)
  NominaExterna.ts     el puerto (ADR-006)
application/
  PrepararCierre.ts    mide el periodo y deja el borrador
  AjustarCierre.ts     confirma o descarta horas extra, excluye personas (con motivo)
  AprobarYEnviar.ts    aprueba, envía por el puerto y guarda la respuesta
  Correspondencias.ts  asocia personas y conceptos (TDR-003)
infrastructure/
  FakeNominaExterna.ts guarda lo que se habría enviado; respuestas configurables
  ConectiaClient.ts    el adaptador real (fase 2, con cuenta)
  Postgres*Reader.ts   lectura del núcleo
interfaces/http/       rutas de gestión (Firebase ID token) y S2S (x-encodebiz-key)
```

El puerto queda así. Los tipos son nuestros; lo que hable el idioma de A3 se traduce dentro
del adaptador:

```ts
interface NominaExterna {
  probarConexion(cred: Credencial): Promise<{ ok: true; cuenta: string } | { ok: false; motivo: string }>;
  listarEmpresas(cred: Credencial): Promise<EmpresaExterna[]>;              // empresa / CCC
  listarEmpleados(cred: Credencial, empresa: string): Promise<EmpleadoExterno[]>; // con NIF
  listarConceptos(cred: Credencial, empresa: string): Promise<ConceptoExterno[]>;
  enviarPeriodo(cred: Credencial, envio: EnvioPeriodo): Promise<ResultadoEnvio>;  // por línea
}
```

`ResultadoEnvio` separa, línea a línea, lo aceptado, lo rechazado (el «no» definitivo, un
4xx) y lo transitorio (429, 5xx). Es la misma distinción que exige el modelo de
integraciones.

## 3. Conexión

Se sigue el contrato de add-ons tal cual: activar (comprueba que `checkinbiz` está activo),
conectar, desconectar y apagar o encender. El documento
`entities/{entityId}/addons/nominabiz-a3` guarda la credencial cifrada con `ENC_KEY` y su
`tokenRef`.

**A confirmar con la cuenta:** qué es la credencial.

- Si es la **clave de suscripción** de Conectia del cliente, se pega en el asistente de
  conexión, se valida con `probarConexion` y se cifra. `connection.type: "api_token"`.
- Si es **OAuth**, el asistente redirige a A3 y guardamos el token de refresco cifrado.
  `connection.type: "oauth"`.

El documento de activación tiene `tokenEncrypted` como campo genérico, así que las dos
opciones caben sin tocar el contrato.

Tras conectar, el cliente elige **qué empresa de su cuenta A3** corresponde a esta empresa
de CheckBiz. Se guarda en `a3nomina_empresa`. Una entidad de CheckBiz se asocia a una sola
empresa de A3 en v1; un cliente con varias empresas en A3 tendrá varias entidades en CheckBiz.

## 4. Tablas (migración `044_a3nomina.sql`, aplicada a mano)

```sql
a3nomina_empresa          (entity_id PK, empresa_externa, nombre_externo, asociada_por, asociada_en)
a3nomina_empleado         (entity_id, employee_id, empleado_externo, nif, asociado_por, asociado_en,
                           PRIMARY KEY (entity_id, employee_id))
a3nomina_concepto         (entity_id, concepto,           -- nuestro: horas_ordinarias, nocturnas, ...
                           concepto_externo, asociado_por, asociado_en,
                           PRIMARY KEY (entity_id, concepto))
a3nomina_cierre           (id PK, entity_id, desde, hasta, estado,  -- borrador|aprobado|enviado|con_errores
                           preparado_en, aprobado_por, aprobado_en, enviado_en, sustituye_a)
a3nomina_linea            (cierre_id, employee_id, concepto, cantidad, unidad, -- horas|dias
                           origen JSONB, huella, estado,      -- incluida|excluida|aceptada|rechazada
                           motivo, respuesta JSONB)
a3nomina_ajuste           (cierre_id, employee_id, concepto, antes, despues, motivo, autor, en)
```

`a3nomina_linea.origen` lleva los `checkin_id` o ids de ausencia y la regla aplicada
(ADR-005). `huella` es el hash de `(employee_id, concepto, cantidad, origen)` y permite
reenviar sin duplicar y detectar diferencias en el cierre siguiente.

## 5. Rutas

| Familia | Rutas |
|---|---|
| Gestión (Firebase ID token, `owner`/`admin` de la entidad) | `activate`, `connect`, `disconnect`, `active`, `connection/:entityId`; `empresas`, `correspondencias/*`; `cierres` (listar, preparar, ver, ajustar, aprobar), `cierres/:id/descarga` |
| S2S (`/api/v1/nominabiz-a3/sync/…`, `x-encodebiz-key`) | reenviar las líneas transitorias de un cierre; preparar un cierre a mano para soporte |

No hay cron que envíe nada (ADR-002). El único proceso periódico es reintentar las líneas
transitorias de un cierre ya aprobado, con presupuesto de llamadas por pasada.

## 6. Pruebas sin cuenta

- `FakeNominaExterna` con escenarios: todo aceptado, una persona rechazada (NIF
  desconocido), fallo transitorio a mitad.
- Las reglas de medición (`medicion.ts`) son puras y se prueban con casos: jornada que cruza
  medianoche, festivo local de la sucursal, cambio de hora, persona en modo *Por turnos* con
  un día sin turno.
- Para la pantalla, en staging el servicio arranca con el adaptador falso
  (`A3NOMINA_ADAPTER=fake`). En producción ese valor está prohibido: si llega, el servicio no
  arranca.
