# Puesta en marcha asistida — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** backoffice — Alta de ecosistema (entidad, sucursales, plantilla, calendario)
**Fecha de inicio:** 2026-09-05
**Estado:** Diseño abierto · sin implementar
**Autor:** Jose Acevedo

---

## Contexto y Motivación

Montar un cliente nuevo en checkbiz360 son hoy varias horas de llamada. Hay que crear la
entidad, sus sucursales, la plantilla entera, las responsabilidades de cada persona y el
calendario en tres niveles —y en ese orden, porque cada paso depende del anterior—. El
cliente llega con un Excel que le pasó su gestoría, y alguien lo traduce a mano.

Es el punto donde se cae la gente en plataformas complejas, y donde se pierden clientes que
ya habían dicho que sí.

La propuesta no es un formulario más. Es que **el equipo de encodeBiz use a Merlin para
modelar los datos desordenados que manda el cliente**, los corrija sobre la marcha en
conversación, y cuando el resultado esté validado se levante todo de una vez desde un seed.

El asistente **conduce**: va pidiendo los datos bloque a bloque, en el orden en que dependen
unos de otros, y acepta lo que el cliente le dé en el formato que sea. El cliente no rellena
nada nuestro; contesta, o manda lo que ya tiene.

---

## Principio de diseño

> **Merlin no escribe en la plataforma: edita un borrador. Sólo el seed escribe, una vez, y
> sobre un borrador que una persona ha aprobado.**

Todo el riesgo se concentra así en un único momento —el de sembrar— en vez de repartirse por
cincuenta llamadas a lo largo de una conversación. Y lo que se enseña al cliente para que dé
el visto bueno no es el borrador crudo: es su configuración en lenguaje suyo.

---

## Alcance

**Dentro:** la ingesta de lo que mande el cliente (Excel, CSV o texto suelto), la
conversación de modelado y corrección, el borrador versionado por entidad, el documento de
validación que se le enseña al cliente, el seed idempotente que lo ejecuta, y el
deshacer.

**Fuera:** que el cliente lo use solo. Esto es una herramienta interna del equipo, y esa
decisión cambia el diseño entero: el asistente puede ser mucho menos desconfiado, y la
validación con el cliente ocurre por fuera, sobre un documento.

---

## Lo que ya sabemos, medido

Antes de escribir este documento se sembró un mes de asistencia real contra `dev-encodebiz`
(rama `feat/seed-asistencia` de `encodebiz-api`, 2026-09-03). Salieron cuatro cosas que
**cambian lo que la puesta en marcha tiene que hacer**, y ninguna era evidente desde el
código:

1. **Sin patrón de sucursal no hay analítica, nunca.** El trigger comprueba
   `existsPatterns(branchId)` y, si no encuentra el documento, se va sin acumular nada. Un
   cliente puede fichar un mes entero y no tener ni un dato de comportamiento, sin ningún
   error visible por ninguna parte. Crear la sucursal no basta: hay que crear su patrón
   inicial.

2. **El coste por hora hay que ponerlo antes de que nadie fiche.** El fichaje se lleva una
   copia *aplanada* de la responsabilidad dentro de `metadata.employeeResponsibility`, y de
   ahí saca el precio el trigger. Si la responsabilidad nace con `price: 0`, todo el
   análisis de coste sale plano —y ponerlo después no arregla lo ya registrado.

3. **El primer mes el cliente se verá la plantilla en rojo.** `reliability` es
   `dataMaturity × dataQuality`; con tres semanas de fichajes impecables el producto se
   queda en 0,43, por debajo del 0,5 que marca `at-risk` por asistencia sola. Con datos
   sembrados perfectos salieron 30 de 42 empleados "en riesgo". La etiqueta no dice que la
   persona sea un problema, dice que el sistema aún no tiene datos; en pantalla se leen
   igual. Ver [ADR-003](./adr/ADR-003-arranque-en-frio-y-fiabilidad.md).

4. **Deshacer no es gratis.** `deleteEmployee` es borrado blando —deja la ficha en
   `fired`—, la entrada del `searchIndex` hay que retirarla aparte, el usuario de Auth
   sobrevive, y los patrones acumulados no se restan solos. El deshacer se construye a la
   vez que el seed, no después.

---

## Documentos

| | |
|---|---|
| [01_as-is.md](./01_as-is.md) | Cómo se monta hoy un cliente, y qué cuesta |
| [02_caso-real-tapissat.md](./02_caso-real-tapissat.md) | El primer fichero real, y las ocho cosas que trae |
| [03_to-be.md](./03_to-be.md) | La conversación por bloques, el borrador y el seed |
| [04_el-relato.md](./04_el-relato.md) | Cómo se conduce: qué se dice, qué CSV se entrega y cuándo |
| `05_contratos-api.md` | Rutas del asistente en backoffice — *pendiente* |
| `06_fases.md` | Orden de construcción — *pendiente* |

**Decisiones:** en [`adr/`](./adr/) — ADR-001 a ADR-004. El diseño técnico
(`tdr/`) se escribirá cuando el borrador esté cerrado.
