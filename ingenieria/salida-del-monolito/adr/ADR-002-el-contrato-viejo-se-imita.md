# ADR-002 — El contenedor imita el contrato viejo; el panel no se toca para cortar

**Fecha:** 2026-09-08
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

## Contexto

El panel llama a las funciones de Firebase con una URL fija por operación y todo lo demás en el
cuerpo: `POST` a `/api/proxy/checkinbiz_update_employee` con el `employeeId` dentro del JSON,
`DELETE` con el cuerpo puesto. No hay path ni verbo semántico.

Los routers del contenedor se escribieron en REST: `PATCH /employees/:employeeId`,
`DELETE /employees/:employeeId`.

Para cortar hay dos caminos: cambiar el panel para que hable REST, o que el contenedor entienda
también la forma vieja.

## Decisión

**El contenedor expone un alias con la forma vieja para cada operación que el panel ya llama**,
resolviendo al mismo caso de uso que la ruta REST. La ruta REST se queda y es la que usan la
app y los integradores.

El panel no se modifica para cortar: se modifica una variable de entorno.

## Razones

- **El rollback vuelve a ser instantáneo.** Con el alias, cortar y volver atrás son la misma
  variable. Si hubiera que tocar el panel, volver atrás sería otro despliegue del front, que
  tarda más y llega justo cuando algo está fallando.
- **Separa los dos riesgos.** Estrenar el backend y estrenar el frontend a la vez multiplica las
  causas posibles de un fallo. Con alias, si algo se rompe tras el corte, es el backend.
- **Ya funcionó.** Los fichajes se cortaron así, con `POST /checklogs/update` imitando a la
  función en vez de un `PATCH` REST, y salió sin incidencias.
- **Cuesta diez líneas por operación.**

## Consecuencias

- Convivencia de dos contratos para la misma operación. Es deuda deliberada y se anota en el
  router, no en un ticket.
- **Los alias se retiran cuando el panel hable REST**, que es un trabajo del front sin prisa y
  sin riesgo, no un prerequisito de la migración.
- El contrato de errores tiene que imitarse igual de bien que el de éxito: mismo HTTP y mismo
  `code`. Un 200 idéntico con un 400 distinto rompe el panel igual, y más tarde.
