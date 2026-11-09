# ADR-004 — La tarifa valora lo que la plataforma mide; la factura la hace su programa

**Fecha:** 2026-10-29
**Estado:** Reemplazado el 2026-11-03 — Jose: «tarifas y presupuestos siguen siendo documentos». No hay `rate` estructurado; la tarifa es un documento del cliente (Fase 4) y el importe del montaje sale del contrato leído (ADR-006). Se conserva el principio «valorar, no facturar». · **revisado el 2026-11-03** por [ADR-006](./ADR-006-el-contrato-es-el-montaje.md): el
presupuesto deja de ser un objeto propio; el importe vive en el contrato, que vinculado a una
sucursal o a una tarea es el montaje. La tarifa y el importe facturable del periodo siguen
como aquí se dice. Donde abajo dice `CustomerBudget`, léase el contrato con `amount`.
**Decisionario:** Jose Acevedo

---

## Contexto

Jose puso dentro del módulo, en la capa del cliente, «documentos, precios, presupuestos,
contratos». Hay que decidir hasta dónde llegan los precios, porque un paso más allá de cierto
punto el módulo deja de ser una capa y se convierte en un programa de facturación, que es
justo lo que venden veinte empresas desde hace veinte años y lo que nuestros clientes **ya
tienen**.

## Decisión

La tarifa, el presupuesto y el contrato **valoran y comparan** lo que la plataforma ya mide.
**No emiten facturas, no numeran, no liquidan impuestos, no hablan con Stripe por cuenta de
la empresa, no se integran con programas de facturación.**

- **Tarifa**: precio hora por cliente, con posible excepción por lugar. Horas imputadas ×
  tarifa = **importe facturable del periodo**. Es el número que la empresa teclea en su
  programa.
- **Presupuesto**: horas o importe acordados para un lugar o para el cliente en un periodo.
  Contra él se enseña el **desvío**, con las horas reales y, si hay inventario con coste
  unitario, el material.
- **Contrato**: un documento del documental con fechas de vigencia. **Rojo** cuando vence o
  está a punto; nada se bloquea.

## Justificación

**Lo que no vende nadie es el importe con la evidencia detrás.** Un programa de facturación
factura lo que le dicen. Nosotros podemos decir «31 horas de Marta y Luis, estas 62 fotos,
este material, 558 €», y eso es lo que la comunidad no discute. Emitir la factura después es
un trámite que su programa hace mejor que nosotros, con sus series, sus impuestos y su
contable.

**Una capa no frena.** Una factura es un documento legal con consecuencias; un importe
facturable es un dato. Si el módulo emitiera facturas, un error nuestro sería un problema
fiscal del cliente. Si enseña un importe, un error nuestro se ve y se corrige antes de
facturar.

**Nunca un cero que parezca un importe.** Sin tarifa, el informe da horas y **no** importe
(`null`, celda vacía), porque un 0 € en una hoja que la empresa manda a su cliente es peor
que no decir nada. Es la misma regla de nombrar lo observado y no inventar la causa.

**Es coherente con lo que ya hay.** Inventario tiene coste unitario en la ficha y el informe
multiplica; no valora existencias ni hace FIFO. Aquí la tarifa es el coste unitario de la
hora.

## Consecuencias

- `Customer.rate?` y `CustomerSite.rate?` con `hourly` en céntimos, `currency` y `validFrom`.
  La tarifa vigente es la de `validFrom` más reciente anterior al día; cambiar la tarifa no
  reescribe el pasado.
- `CustomerBudget` con `hours?` y/o `amount?`; `GET /budgets/:id/status` calcula al leer.
  No se guarda el desvío, no se avisa en v1.
- `CustomerContract` con `startsAt`, `endsAt?`, `warnDaysBefore` (30 por defecto) y
  `documentId?` del documental. Rojo en ficha y lista.
- El informe «Por cliente» lleva el importe **solo si hay tarifa**, y el desvío **solo si hay
  presupuesto en el periodo**.
- **Fuera**: numeración, IVA, series, remesas, cobros, integraciones con a3, Holded, Sage,
  etc. Si un cliente lo pide, es otro módulo y otra conversación, no una fase de este.
