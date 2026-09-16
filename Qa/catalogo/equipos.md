# Catálogo de casos de uso — Equipos (EQP)

> **Verificación (2026-09-16).** Casos escritos desde el diseño
> ([ingenieria/equipos](../../ingenieria/equipos/README.md)) y el código de la rama
> `feat/equipos-sucursal` de `encodebiz-api`. La prueba es
> `qa/tests/con-datos/52-equipos.spec.ts`. Lo marcado **sin prueba** es lectura del código.

Un equipo es una plantilla de responsabilidades sin centro. Sus miembros viven en
`entities/{entityId}/teams/{teamId}/team_responsibilities/{employeeId}`, y aplicarlo a una
sucursal los copia a `employee_responsibilities`. Todas las rutas cuelgan de
`/api/v1/employees/teams` (servicio `employees`, puerto 3013), exigen ID token de Firebase y
pasan por `canWrite`: asiento activo de owner o admin.

Respuestas: `{success: true, data}` o `{error, code}`. Validación de forma:
`400 {error: "Invalid payload", details, code: "team/bad_request"}`.

---

## GET /api/v1/employees/teams?entityId=  ·  EQP-01

- EQP-01-01 · PROP · entidad con un equipo de tres miembros → 200; el equipo aparece con `memberCount: 3`.
- EQP-01-02 · PROP · sin `entityId` → 400 `team/bad_request`. **Sin prueba.**

## POST /api/v1/employees/teams  ·  EQP-02

- EQP-02-01 · PROP · `{entityId, name: "  Equipo   A "}` → 201; `name` sin espacios de más, `createdBy` = uid del token.
- EQP-02-02 · ADMIN · ídem con otro nombre → 201.
- EQP-02-03 · PROP · el mismo nombre con otras mayúsculas, tildes o espacios → 409 `team/name_taken`.
- EQP-02-04 · PROP · nombre vacío → 400 `team/bad_request`.
- EQP-02-05 · OP_MANAGER · mando en un centro, sin asiento en la empresa → 403 `auth/unauthorized`.
- EQP-02-06 · AJENO · `entityId` de otra empresa → 403.
- EQP-02-07 · ANON → 401 `unauthenticated`.

## GET /api/v1/employees/teams/:teamId?entityId=  ·  EQP-03

- EQP-03-01 · PROP · equipo con miembros → 200 `{team, members}`; cada miembro con su puesto, precio y nivel, `scope: {entityId, teamId}`.
- EQP-03-02 · PROP · equipo inexistente → 404 `team/not_found`.

## PATCH /api/v1/employees/teams/:teamId  ·  EQP-04

- EQP-04-01 · PROP · nombre nuevo → 200 con el nombre cambiado.
- EQP-04-02 · PROP · el nombre de otro equipo → 409 `team/name_taken`.
- EQP-04-03 · PROP · su propio nombre con otras mayúsculas → 200: no choca consigo mismo.

## DELETE /api/v1/employees/teams/:teamId?entityId=  ·  EQP-05

- EQP-05-01 · PROP · → 200 `{deletedMembers}`; después `GET` → 404. Las responsabilidades que el equipo dio en una sucursal **siguen** allí.
- EQP-05-02 · PROP · equipo inexistente → 404 `team/not_found`. **Sin prueba.**

## POST /api/v1/employees/teams/:teamId/members  ·  EQP-06

- EQP-06-01 · PROP · `{employeeId, responsibility: "worker", job: {job: "electricista", price: 20}}` → 201; `level: 1` derivado del cargo, `assignedBy` = uid del token.
- EQP-06-02 · PROP · la misma persona otra vez con otro precio → 409 `team/member_exists`; el precio guardado no cambia.
- EQP-06-03 · PROP · `employeeId` inexistente → 404 `employee/not_found`.
- EQP-06-04 · PROP · empleado dado de baja (`fired`) → 400 `employee/fired`.
- EQP-06-05 · PROP · `job.price` negativo o en texto → 400 `team/bad_request`.
- EQP-06-06 · PROP · una persona en dos equipos → está en los dos.
- EQP-06-07 · PROP · ser miembro **no** da centro: `Employee.branchId` no cambia y el listado de responsabilidades de la empresa no incluye ningún documento con `scope.teamId`.
- EQP-06-08 · PROP · entrar en un equipo no genera aviso `assign_created`.

## PATCH /api/v1/employees/teams/:teamId/members/:employeeId  ·  EQP-07

- EQP-07-01 · PROP · `{responsibility: "manager", job: {job: "diseñadora", price: 16}}` → 200; `level: 3`.
- EQP-07-02 · PROP · persona que no está en el equipo → 404 `team/member_not_found`.

## DELETE /api/v1/employees/teams/:teamId/members/:employeeId?entityId=  ·  EQP-08

- EQP-08-01 · PROP · → 200; ya no aparece en el equipo; repetir → 404 `team/member_not_found`.

## POST /api/v1/employees/teams/:teamId/apply  ·  EQP-09

- EQP-09-01 · PROP · `{entityId, branchId}` de una sucursal donde no están → 200; `created` con ellos; en la sucursal cada uno tiene el puesto, el precio y el nivel del miembro.
- EQP-09-02 · PROP · quien ya tenía responsabilidad en esa sucursal sale en `skipped` con `already_in_branch`, y su puesto y su precio **no cambian**.
- EQP-09-03 · PROP · los creados tienen la sucursal en `Employee.branchId`.
- EQP-09-04 · PROP · aviso `assign_created` a cada creado, y a nadie más.
- EQP-09-05 · PROP · aplicar otra vez → 200 con `created` vacío y todos en `skipped`.
- EQP-09-06 · PROP · sucursal inexistente → 404 `branch/not_found`.
- EQP-09-07 · OP_MANAGER y AJENO → 403.
- EQP-09-08 · PROP · miembro `fired` o `pending` → `skipped` con `employee_not_active`. **Sin prueba:** la baja ya lo saca de sus equipos (EQP-11-01), así que solo se da con una ficha `pending`.
- EQP-09-09 · PROP · alguien da de alta a un miembro en la sucursal mientras se aplica → 409 `team/apply_conflict` y no se escribe nada. **Sin prueba:** es una carrera.

## POST /api/v1/employees/teams/from-branch  ·  EQP-10

- EQP-10-01 · PROP · `{entityId, branchId, name}` → 201 `{team, members, skipped}`; el equipo tiene a la plantilla activa de la sucursal con su puesto y su precio.
- EQP-10-02 · PROP · nombre ya usado → 409 `team/name_taken`.
- EQP-10-03 · PROP · sucursal inexistente → 404 `branch/not_found`.
- EQP-10-04 · PROP · sucursal sin nadie → 400 `team/branch_without_staff`. **Sin prueba.**

## Baja de empleado  ·  EQP-11

- EQP-11-01 · PROP · `DELETE /api/v1/employees/:employeeId` de un miembro → deja de estar en el equipo.
