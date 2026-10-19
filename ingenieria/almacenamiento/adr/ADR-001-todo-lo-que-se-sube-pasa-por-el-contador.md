# ADR-001 — Todo lo que se sube a Storage pasa por el contador de la empresa

**Fecha:** 2026-10-18
**Estado:** Sustituida el 2026-10-19 por [ADR-002](./ADR-002-cuenta-un-trigger-de-storage.md): cuenta un trigger de Storage, sin helper obligatorio ni regla de CI, y sin packs
**Decisionario:** Jose Acevedo

## Contexto

Para vender espacio hay que saber cuánto ocupa cada empresa, y saberlo siempre, no sólo en los
módulos que se acordaron de contar. Hoy cinco módulos escriben en el bucket por su cuenta
(documental, tareas, firma, informes, campañas), cada uno con su ruta y ninguno contando. El
quiosco sería el sexto. Jose, 2026-10-18: «todo lo que se suba debe tributar a este módulo
contador de Storage para poder vender espacio».

## Decisión

**Ningún servicio escribe ni borra en Storage directamente.** Lo hace a través del módulo de
almacenamiento de `@encodebiz/shared` (`checkbiz/storage`: `accountedUpload`,
`accountedDelete`, `accountedDeletePrefix`), que exige `entityId` y `module`, escribe en la ruta
canónica `{módulo}/entities/{entityId}/…` (o la carpeta de retención del quiosco), y suma o
resta el tamaño al contador de la empresa en la misma operación. **Cuenta todo**: documentos,
evidencias de tareas, evidencia y actas de firma, fotos del quiosco, imágenes de campañas,
informes y exportaciones. Lo regenerable no se exime de contar: se le pone caducidad corta
(informes y exportaciones, 30 días) para que no pese.

## Razones

**Lo que no se cuenta no se puede vender, y lo que se cuenta a medias se vende mal.** Un cliente
que compra 10 GB y ve «usado: 3 GB» mientras el bucket tiene 7 GB suyos descubre tarde que
pagaba por un número inventado, o nosotros descubrimos tarde que regalábamos espacio. La única
forma de que el número sea verdad es que no haya camino para subir sin contar.

**Un helper, no una norma.** Una norma de revisión de código se olvida en el sexto módulo;
un helper que es la única forma cómoda de subir, con la ruta canónica dentro, no. Para que no
sea cómodo saltárselo, el CI falla si aparece `getStorage().bucket()` o `.bucket().file(` fuera
de `packages/shared/src/checkbiz/storage/` (un `grep` en el `lint` del monorepo).

**La reconciliación nocturna es la red, no la regla.** Lista los prefijos canónicos y corrige
el contador. Un fichero subido fuera de la ruta canónica no lo encuentra, y ésa es otra razón
para que la ruta la ponga el helper y no cada módulo.

**Las excepciones se escriben aquí.** Hoy, ninguna. Si un módulo necesita un bucket distinto
(el quiosco usa el europeo), lo pide al helper por nombre; sigue contando.

## Consecuencias

- Migrar los cinco módulos existentes al helper (sin mover ficheros: el helper acepta la ruta
  actual de cada uno como canónica mientras lleve `entities/{entityId}`), y poner la empresa en
  la ruta de campañas, que hoy no la lleva.
- Informes y exportaciones ganan una regla de ciclo de vida de 30 días en el bucket.
- Un módulo nuevo que guarde ficheros empieza por el helper. Es la primera línea de su diseño.
- `encodebiz-api/CLAUDE.md` lleva la regla, para que los agentes la apliquen sin leer este ADR.
