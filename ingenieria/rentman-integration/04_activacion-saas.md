# 04 — Activación y modelo SaaS

> **Qué cubre:** cómo se activa, configura y factura la integración Rentman. Es un
> **add-on de pago**, no una función que venga encendida. Marca el diseño tanto como la parte técnica.

---

## 1. Es un módulo de activación, no una feature

La integración Rentman es un **módulo dentro de "Integraciones"** que el tenant
**activa explícitamente**. **No se enciende solo.** En paridad con activar **checkbiz**
o **passbiz**: es un producto que se contrata, con su **coste** propio.

Consecuencias de diseño:
- El tenant tiene un **entitlement** (derecho de uso) para "integración Rentman".
- El `sync` **solo procesa tenants con el módulo activo y configurado**. Sin entitlement,
  el job ni sondea ni escribe: la integración es inexistente para ese tenant.
- Es **valor agregado**: no compite con el core, lo amplía. La venta es "conecta tu
  Rentman"; el foso (tareas + fichaje legal) es lo que retiene.

## 2. Ciclo de vida

```
  [Contratado]  →  [Activado]  →  [Configurado]  →  [Activo]  →  [Pausado/Baja]
      │              │               │                │              │
   billing        entitlement     token + mapping   sync corre    sync parado,
   habilita       ON              (ver §3)          en cada pasada mapping conservado
```

1. **Contratación / billing.** Igual que checkbiz/passbiz: alta del add-on con su tarifa.
   Habilita el entitlement del tenant.
2. **Activación.** El tenant enciende "Rentman" en Integraciones. Sin esto, oculto.
3. **Configuración (obligatoria, manual).** Sin ella el módulo está activo pero inerte:
   - **Token** de Rentman (Configuration → Account → Integrations), guardado **cifrado**.
   - **Mapeos** iniciales (crew↔employee, project↔…) — asistidos por auto-match (email).
   - Parámetros de sync (cadencia, sentido de horas según D2).
4. **Activo.** El `sync` incluye al tenant en cada pasada de reconciliación.
5. **Pausa / baja.** Se puede pausar (para el sync, conserva mapping) o dar de baja (fin
   de billing → entitlement OFF → sync lo excluye).

## 3. Puertas (gates) que respeta el código

Antes de cualquier pull/push de un tenant, el `sync` comprueba **en orden**:

1. **Entitlement activo** (billing al día). Si no → excluido.
2. **Módulo activado** por el tenant. Si no → excluido.
3. **Configuración completa** (token válido + al menos el mapping mínimo). Si no →
   estado "configuración pendiente", no se sincroniza, se avisa en el panel.

Solo si las tres pasan, el tenant entra en la reconciliación.

## 4. Encaje con la plataforma

- Vive bajo **Integraciones** en el backoffice, junto a futuros conectores.
- Modelo de cobro **paritario con checkbiz / passbiz** (add-on contratable).
- El entitlement es la fuente de verdad de "¿este tenant tiene Rentman?": ni el token
  guardado ni el mapping activan nada por sí solos si el entitlement está OFF.

## 5. Reutilizar la monetización existente (servicio + planes en Firestore)

**Principio:** no construimos una monetización nueva. Rentman se da de alta como **un
servicio más**, con sus **planes**, siguiendo exactamente la línea de **checkbiz** y
**passbiz**, para **reutilizar** el motor de activación/facturación que ya existe.

Lo que sabemos del precedente (a confirmar contra el backend SAAS):
- Existe un mecanismo de **activación por servicio** — hay un trigger Firestore
  `onActivateCheckbiz` (`apiV100-firebaseFirestoreTriggersCheckinBiz-onActivateCheckbiz`).
  Rentman necesitaría su equivalente `onActivateRentman` (o encajar en un activador genérico).
- La plataforma trabaja con **planes** (hoy Bronze / Enterprise en checkbiz). Rentman
  define **su(s) plan(es)** dentro del mismo modelo.

Tareas de monetización (planificación):
1. **Crear el servicio `rentman`** en Firestore con la **misma forma** que `checkbiz` /
   `passbiz` (⚠️ el esquema exacto —colección, campos, doc de plan— hay que **espejarlo
   del backend SAAS `encodeBiz-SAAS/functions`**, que aún no está inspeccionado; no
   inventarlo aquí).
2. **Definir los planes** de Rentman siguiendo esa estructura.
3. **Enganchar el activador** (`onActivate…`) para que encender el servicio prepare el
   entitlement y deje el módulo en estado "configuración pendiente" (§2).
4. El servicio `sync` lee el **mismo entitlement** para decidir a quién sincroniza (§3).

> **Pendiente de ingeniería:** inspeccionar en `encodeBiz-SAAS/functions` cómo están
> modelados los servicios y planes de checkbiz/passbiz y calcar la estructura para Rentman.
> **Pendiente de producto:** definir la **tarifa** y el modelo (fijo por tenant, por
> nº de empleados sincronizados, por volumen de sync…). No decidido aquí.
