# TDR-008 — Ajustes del CRM: los topes diarios y lo demás, en un sitio

**Fecha:** 2026-10-16
**Estado:** En implementación
**Decisión:** Jose Acevedo («es importante ponerle un límite para no saturar ventas; debería poder configurarse en el apartado de CRM; ahí meteremos todo»)

---

## 1. Por qué

Lo automático del CRM mete trabajo nuevo cada día: la vigilancia de licitaciones da de
alta empresas, Merlin las investiga, la agenda las reclama. Sin un freno proporcionado a la
capacidad comercial, el CRM se llena más deprisa de lo que una persona puede trabajar (24
empresas en dos noches). Los topes que había vivían en variables del servidor: cambiarlos
exigía redesplegar, y la vigilancia no tenía ninguno.

## 2. Qué

Una fila en `sales_crm_settings` (migración `039`) con lo que decide el ritmo, editable
desde **Comercial → Ajustes del CRM** (permiso `crm:settings`, root y admin). Las variables
del servidor pasan a ser **solo el valor de arranque**: lo efectivo es `defaults(env) ⊕
guardado`. `sales` lo lee en cada pasada (caché de 30 s), sin redesplegar.

| Sección | Ajuste | Por defecto | Dónde manda |
|---|---|---|---|
| Licitaciones | vigilancia sí/no · alta automática sí/no · nichos con alta · **máximo de empresas nuevas al día** · solo pymes | on · on · limpieza, sad · 5 · sí | `placspSweep` |
| Investigación (Merlin) | activa · máximo al día · tokens al día · hora · días sin reintentar · modelo (selector) · razonamiento · cuánto lee de cada página | off · 5 · 400.000 · 7 · 7 · el de Merlin · el de Merlin · el de Merlin | `researchSweep`, botón |
| Agenda | correo · hora · días sin respuesta · **enviar aunque no haya nada para hoy** | del entorno · 8 · 5 · sí | `agendaEmail` |

Lo que no entra por el tope no se pierde: las adjudicatarias quedan como candidatas en el
informe y entran al día siguiente; las cuentas sin investigar esperan en `signal`.

La pantalla enseña además **lo gastado hoy**: investigaciones y tokens, y empresas nuevas
por licitaciones, para que el tope se lea contra algo.

## 3. Cambios que arrastra

- **Solo pymes** en licitaciones: `cbc:SMEAwardedIndicator` del `TenderResult`. `false` →
  descartada (`no_pyme`); ausente → entra (no se pierde por falta de dato).
- **Agenda todos los días laborables**: con «enviar aunque no haya nada» el correo llega
  igual, con una sección «Esta semana» (lo de los próximos 7 días por persona) y, si no hay
  nada en toda la semana, una línea que lo diga. Fin de semana no se manda.
- El modelo de Merlin se puede fijar desde aquí por investigación (viaja en la petición a
  Merlin); si está vacío, manda el entorno de Merlin.
- Las personas que propone Merlin necesitan nombre y apellido: «Cristina, supervisora
  (mencionada en testimonios)» no es un contacto.

## 3b. El selector de modelos

El modelo no se escribe: se elige. Merlin pide a la API de OpenAI los modelos de la cuenta
(`GET /api/v1/gpt/investigacion/modelos`) y los filtra a la familia que investiga con
búsqueda web (`gpt-5`, `gpt-5.x` y sus `-mini`; fuera `nano`, `codex`, `chat`, `pro` y los
snapshots con fecha), la generación más nueva y el tamaño grande primero. Caché de 10 min;
si la API no responde, `gpt-5-mini` y `gpt-5` como respaldo. `sales` lo incluye en
`GET /crm/settings` (`modelos`). Si hace falta un modelo que el filtro no lista, sigue
valiendo la variable de Merlin.

## 4. API

`GET /crm/settings` → `{ settings, defaults, stored: { updatedBy, updatedAt }, usage: { investigaciones, tokens, nuevasLicitaciones } }`
`PATCH /crm/settings` con un parcial anidado (`.strict()` por sección); responde lo efectivo.
Backoffice: proxy con `crm:settings` y apunte en la auditoría de qué secciones cambian.
