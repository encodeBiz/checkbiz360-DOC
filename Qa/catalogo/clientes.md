# Catálogo de casos de uso — cartera de clientes (prefijo CLI)

> Escrito el 2026-11-07 junto con el código y afirmado contra `dev-encodebiz` el mismo día
> (`qa/tests/con-datos/59-cartera-clientes.spec.ts`). Automatiza los pasos P18 y P19 del guion
> [ingenieria/cartera-de-clientes/09_guion-qa.md](../../ingenieria/cartera-de-clientes/09_guion-qa.md).
> El P20 (aviso de la IA al importar un cuadrante) es solo pantalla y se mira a mano.

## Actores
- PROP: la propietaria; crea los clientes, sube los documentos y crea el contrato.
- OP_MANAGER: gestor de la sucursal principal, donde están los clientes.

## Preparación
Dos clientes en la sucursal principal. Al primero, una ficha (`customer_record`, visible para
todos) y un contrato en PDF (`customer_contract`, solo gestores), y un contrato de 1.000 € y
20 h colgado de ese PDF.

## GET /api/v1/documents (ámbito cliente) · CLI-18
- CLI-18-01 · PROP · `scope=customer` → solo documentos con `scope: customer`, los dos subidos entre ellos.
- CLI-18-02 · PROP · `scope=customer&customerId=A` → exactamente la ficha y el contrato, con su `customerId`; la ficha del cliente lleva el nombre que pinta el panel. Con el cliente B → ninguno.
- CLI-18-03 · PROP · `scope=entity` → no trae documentos de clientes.

## GET/POST /api/v1/customers/…/contracts para quien no es owner ni admin · CLI-19
- CLI-19-01 · PROP · la lista trae importe, horas estimadas, `plannedMinutes` y `totals` (1 contrato, 1.000 €).
- CLI-19-02 · OP_MANAGER · la lista trae título, horas estimadas y `plannedMinutes`; sin `amount`, `extraction` ni `notes`; `costCents`, `marginCents` y `marginPct` a `null`; sin `totals`.
- CLI-19-03 · OP_MANAGER · el detalle del contrato, sin importe ni coste y con `events` vacío.
- CLI-19-04 · OP_MANAGER · crear, cerrar y borrar un contrato → `403`; el contrato sigue activo.
