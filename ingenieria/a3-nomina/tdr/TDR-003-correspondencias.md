# TDR-003 — Correspondencias de personas y conceptos

**Fecha:** 2026-10-26
**Estado:** Diseño propuesto
**Componente:** `services/a3nomina` — `Correspondencias`
**Decisiones de referencia:** [ADR-003](../adr/ADR-003-unidades-no-euros.md),
[ADR-005](../adr/ADR-005-cada-linea-sabe-de-donde-sale.md)

---

## 1. Personas

**Se empareja por NIF.** En CheckBiz es `Employee.nationalId` (con `metadata.dni` como
respaldo de los antiguos). En A3, el NIF del trabajador. *A confirmar con la cuenta* si A3
expone el NIF, el código de empleado o los dos. Si solo expone el código, el emparejamiento
inicial se hace igualmente por NIF, leyendo la ficha, y lo que se guarda es el código.

Proceso:

1. Al conectar, y luego bajo petición («volver a emparejar»), se leen los empleados de la
   empresa A3 asociada.
2. **Coincidencia exacta de NIF normalizado** (mayúsculas, sin espacios ni guiones): se
   propone la asociación.
3. **Sin NIF en CheckBiz, o sin coincidencia:** la persona queda *sin asociar* y se enseña
   en la pantalla, con los candidatos de A3 que tengan nombre parecido para elegir a mano.
   Nunca se asocia por nombre sin que alguien lo confirme.
4. **Un NIF que coincide con dos empleados en A3** (por ejemplo, una recontratación) no se
   resuelve solo: se pregunta.

Lo asociado se guarda en `a3nomina_empleado`, **no en la ficha del empleado**. Existe
`metadata.source.externalId` en `Employee`, pero escribirlo sería tocar el núcleo por un
tercero. Si mañana se retira el add-on, la tabla se borra y no queda rastro.

Una persona dada de baja en A3 pero activa en CheckBiz, o al revés, se señala en la
pantalla. No se corrige sola.

## 2. Conceptos

La pantalla lista los conceptos de CheckBiz (TDR-002 §2), y para cada uno, un desplegable
con los conceptos de la empresa en A3 (`listarConceptos`). Por concepto:

- **Asociado:** se envía.
- **Sin asociar:** no se envía, y el cierre lo dice.
- **«No se usa en esta empresa»:** una elección explícita; el concepto deja de avisar. Por
  ejemplo, una empresa sin turno de noche marca así `horas_nocturnas`.

No hay códigos por defecto (ADR-003). Si en el piloto vemos que la mayoría de empresas usan
los mismos códigos estándar de A3, se puede **sugerir** el habitual con una marca de
«sugerido». Seguiría haciendo falta que alguien lo acepte.

Si la API distingue el tipo de concepto A3 (cantidad o importe; cotizable o no), la pantalla
lo enseña junto al nombre. Así quien asocia ve si está mandando *horas* a un concepto que
espera *euros*, y el sistema lo impide.

## 3. Quién lo hace

Las correspondencias las hace `owner` o `admin` de la entidad. Es la tarea central del
piloto con el primer cliente, hecha con su responsable de nóminas delante. Cada cambio guarda
autor y fecha. Un cierre aprobado guarda los códigos que usó: cambiar una correspondencia no
reescribe lo ya enviado.

## 4. Pantalla

Una sola pantalla del add-on, **Conexión con A3**, con tres bloques:

1. **Conexión:** estado, empresa A3 asociada y `tokenRef`.
2. **Personas:** asociadas, sin asociar y avisos.
3. **Conceptos:** la lista del §2.

Los textos dicen lo que hace el cliente, no la mecánica: «Elige qué concepto de tu nómina
corresponde a las horas nocturnas», no «mapear concepto externo».
