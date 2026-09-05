# ADR-005 — Los datos personales no salen del servidor

**Fecha:** 2026-09-05
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

El borrador de una puesta en marcha lleva la plantilla entera de un cliente: nombres, correos,
DNIs, teléfonos y en algunos casos direcciones particulares. Son datos personales de personas
que no son nuestras clientas —son las empleadas de nuestra clienta—, y de las que somos
encargados de tratamiento.

El contrato del turno decía que Merlin recibía «el borrador tal y como está». Eso significa
mandar esos datos al proveedor del modelo, que está fuera de la UE. Se puede sostener con un
encargo y unas cláusulas, pero es una transferencia que hay que documentar, justificar y
defender.

Y no hace falta.

## La observación que lo resuelve

**El modelo revisa los valores; lo que no sabe nunca es de quién son.**

Esa distinción es todo. El modelo *tiene* que mirar los datos —revisarlos es justamente lo que
aporta: darse cuenta de que una secretaria cobra más que una responsable de innovación, o de
que una dirección está incompleta—. Lo que no necesita para eso es saber cómo se llama la
secretaria.

Repasando el trabajo del asistente:

| Trabajo | Quién lo hace |
|---|---|
| Leer un CSV o un libro de Excel | Código |
| Cruzar centros entre bloques, detectar correos repetidos, contar `owner` | Código |
| Detectar que un valor es el de la fila de ejemplo | Código |
| Expandir periodos y responsabilidades | Código |
| Geocodificar | Código |
| Adivinar que la columna «Trabajador» es `nombre_completo` | Modelo |
| Entender «de 9 a 2 y de 4 a 7, sábados alternos» | Modelo |
| **Ver que un coste no encaja con su puesto, o que una dirección está coja** | Modelo |
| Redactar la pregunta y explicar por qué hace falta | Modelo |

Todo lo determinista es código y corre en el servidor. Al modelo le queda el juicio sobre los
valores y el lenguaje — y para las dos cosas le basta con
`PERSONA_1 · Responsable de operaciones · 22,50 €/h · CENTRO_1, CENTRO_2`.

## Decisión

**El borrador no sale del servidor.** Lo que se manda al modelo es una proyección sin datos
personales:

- **Para mapear columnas**, sólo las cabeceras. `["Trabajador", "Correo", "N.I.F."]`, sin una
  sola fila.
- **Para entender un horario o una frase suelta**, el texto, que no identifica a nadie.
- **Para redactar**, el estado del borrador en agregado: cuántos elementos tiene cada bloque,
  qué campos faltan y de qué tipo son. *«Faltan 4 costes por hora»*, no cuáles.
- **Cuando una frase del cliente sí nombra a alguien** —«Ricard trabaja en el taller y en
  Ayats»— se sustituye por identificadores estables antes de salir —`PERSONA_1 trabaja en
  CENTRO_1 y CENTRO_2`— y se deshace la sustitución al volver. El modelo necesita la
  estructura de la frase, no el nombre.

La sustitución y su inversa viven en el borde, en un solo sitio, y **ninguna llamada al modelo
puede saltárselas**.

## Consecuencias

**La Fase 1 gana sentido por partida doble.** El normalizador y el seed no usan modelo en
absoluto: son código determinista sobre un fichero. Que fueran primero se decidió por otra
razón —validar la forma del muñeco usándola—, pero además resulta ser la parte que nunca
tendrá esta discusión.

**El asistente es menos «mágico» y más comprobable.** Un mapeo de columnas sobre cabeceras se
puede enseñar y corregir; una detección de duplicados en código se puede probar. La parte que
alucina queda acotada a redactar.

**Merlin no guarda nada, y ahora tampoco ve nada.** Lo que ya decía
[05_contratos-api](../05_contratos-api.md) sobre que no persiste se refuerza: el turno no
recibe el borrador, recibe su sombra.

**Hay que poder demostrarlo.** La proyección se construye en un solo punto y se registra qué
se envió. Si algún día hay que enseñar que los DNIs no salieron de aquí, tiene que poder
enseñarse.
