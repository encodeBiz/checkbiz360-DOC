# ADR-002 — Cuenta un trigger de Storage, y el exceso de 2 GB se cobra a 0,25 €/GB

**Fecha:** 2026-10-19
**Estado:** Aceptada · sustituye a [ADR-001](./ADR-001-todo-lo-que-se-sube-pasa-por-el-contador.md)
**Decisionario:** Jose Acevedo

## Contexto

ADR-001 (2026-10-18) obligaba a que todo fichero se subiera por un helper de `shared` que
contaba, con una regla de CI que fallara si alguien llamaba a `bucket()` por su cuenta, y lo
acompañaba de cuotas por plan, packs y exceso `metered`. Al revisarlo el 2026-10-19 aparecieron
tres problemas:

- Había más sitios que suben de los que el diseño conocía (la marca de la empresa en
  `services/entities`) y la regla de CI propuesta no habría detectado la mitad de las llamadas
  (`admin.storage().bucket(process.env…)`).
- `storage.rules` deja escribir en el bucket a cualquier usuario autenticado, así que un helper
  en el servidor nunca habría visto todas las subidas.
- `billing` no tiene nada `metered`: el cobro del exceso no era «sin una línea de código».

Jose, 2026-10-19: «la idea no es limitar, la idea es contabilizar todo lo posible, simplemente
con un trigger de Storage […] cuando se sube algo que referencie entidad se le agrega al
contador, cuando se borre se descuenta, y si pasa de 2 GB se comienza a contabilizar
redondeando al suelo». Y sobre el precio, descartando «Google + 5 %»: «0,25 € mejor».

## Decisión

- **Cuenta un trigger de Storage**, no el código que sube. Al terminar una subida suma el
  tamaño a la empresa que aparece en la ruta, y al borrarse un objeto lo resta. Un registro
  por objeto con su `generation` evita contar dos veces un evento repetido o una sobrescritura.
- **Cuenta lo que lleve la empresa en la ruta**, salvo la marca de la empresa, que Jose deja
  fuera. Las campañas no son de ninguna empresa y no cuentan.
- **Nada se limita.** 2 GB incluidos para todas las empresas; por encima,
  `⌊GB⌋ − 2` a **0,25 € por GB y mes**, con el valor del día en que Stripe crea la factura.
- **No hay packs, cuotas por plan, avisos de cuota ni regla de CI.**
- **El cliente no escribe en Storage**: se cierran las reglas como se hizo con Firestore.

## Razones

**El trigger ve todo lo que llega al bucket**, venga de donde venga, y no depende de que cada
módulo se acuerde de usar un helper. Es menos código y menos disciplina que mantener.

**0,25 € y no el coste más un 5 %.** Guardar un GB cuesta unos 2 céntimos al mes, pero
descargarlo una vez cuesta 12, y Stripe se queda en torno al 2 %. Un margen del 5 % sobre el
almacenamiento perdería dinero con cualquier cliente que descargue. A 0,25 € se cubren las
descargas sin medirlas y el precio sigue siendo bajo.

**Redondear hacia abajo** hace que nadie pague por unos megas de más y que la línea de la
factura sea fácil de explicar.

## Consecuencias

- Triggers en el bucket del proyecto y en `encodebiz-media-eu`, en `services/firebase_sdk`.
- Un script de carga inicial cuenta lo que ya existe y sirve también para reparar.
- El helper de `feat/quiosco` deja de contar; si contaran los dos, todo sumaría el doble.
- `billing` añade la línea de exceso al borrador de la factura con `invoice.created`.
- Queda abierto qué se hace con las empresas gratuitas, que no tienen factura en Stripe: hasta
  que se decida, se cuentan y no se cobran.
- `encodebiz-api/CLAUDE.md` cambia la regla «nada se sube sin contar» por esta.
