# TDR-005 — Panel Análisis: el cruce de los cuatro ejes

**Estado**: propuesto · **Fecha**: 2026-07-29 · **Sustituye a**: nada
**Depende de**: TDR-003 (fiabilidad normalizada), TDR-004 (contrato API)

---

## 1. El problema

El panel mide bien **presencia y cumplimiento horario**. No mide **si la persona
es fiable**, que es una pregunta distinta y es la que un gestor hace de verdad.

Hoy las señales existen pero están sueltas, y sueltas no significan nada:

| eje | dónde vive hoy | estado |
|---|---|---|
| Desviación de horas | `operatingCost.profile` | cruzado con cierre |
| Jornadas incompletas (cierre) | `operatingCost.profile` | cruzado con desviación |
| Geocerca | `geo.people[].band` | **suelto**, no se cruza con nada |
| Tareas | — | **no existe** |

Dos cruzados, uno aparte, uno ausente. El valor está en el cruce: alguien que
cumple horas *y* cierra bien *y* ficha donde debe *y* entrega sus tareas es una
afirmación que ningún competidor puede hacer, porque exige las cuatro fuentes a la
vez. Cualquiera de las cuatro por separado es una métrica más.

## 2. El error a evitar (aprendido, no teórico)

En la construcción de julio de 2026 el panel se pasó al extremo contrario del que
tenía: por evitar acusar en falso, **filtró hasta vaciarse**.

Medido sobre producción el 2026-07-29:

- El bloque geo analiza **722 fichajes**, detecta **75 fuera de zona** y la tabla
  de personas muestra **cero filas**.
- Un evento aislado a **1.571 m** de una valla de 50 m desaparece por la regla de
  reincidencia.
- **12 días** de incidencias de una misma persona quedan etiquetados "dentro del
  margen" y por tanto invisibles.
- Los fichajes con trabajo remoto o sin valla se saltan con un `continue`: ni
  siquiera se cuentan como categoría.
- La desviación de horas se calcula sobre **714 de 3.684** horas planificadas
  (19 %).

Un panel que no dice nada es tan inútil como uno que miente.

## 3. Decisión: no descartar, clasificar

**Todo registro cae en un cajón con nombre y visible, y la suma de los cajones
cuadra con el total.** Nada se filtra en silencio.

Es la disciplina que ya funciona en el reparto de horas planificadas —fiable /
sin cerrar / sin actividad registrada, que suma exactamente el plan del mes— y que
no se aplicó ni al geo ni al perfil.

Consecuencias operativas:

- Prohibido el `continue` silencioso. Remoto, sin valla, sin dato y confusión son
  **cajones**, no exclusiones.
- Cada eje declara explícitamente su cajón `sin_evidencia`. No llegar al mínimo no
  es "no aparece": es "no se puede afirmar", y se muestra como tal.
- El perfil es un **cruce**, no un filtro. Nadie desaparece del panel por no
  alcanzar un umbral en un eje; queda clasificado como indeterminado en ese eje y
  sigue clasificado en los demás.
- Todo bloque publica sus totales, y los totales deben cuadrar. Un cuadre que no
  da es un bug, y se ve.

## 4. Los cuatro ejes

Cada eje produce un **veredicto propio** con su propio umbral de evidencia. Ningún
eje se pondera contra otro.

### 4.1 Cumplimiento de horas
Desviación sobre jornadas fiables. Ya implementado en `BuildOperatingCost`.
Veredictos: `cumple` · `trabaja_de_menos` · `trabaja_de_mas` · `sin_evidencia`.

### 4.2 Registro de jornada
Tasa de cierre correcto. Ya implementado.
Veredictos: `registra` · `registro_irregular` · `no_registra` · `sin_evidencia`.

### 4.3 Ubicación
Ver TDR-006 (pendiente) y la memoria del criterio geo. Cuatro lecturas:
`no_consigue_fichar` · `valla_corta` · `incidencia_puntual` ·
`patron_de_conducta` · `sin_evidencia`.

La gravedad es **proporcional al radio** —el radio es la tolerancia que el cliente
declara— **con un suelo absoluto de GPS como guarda**: el móvil se equivoca en
metros, no en porcentaje, y sin ese suelo toda la plantilla de un cliente con
valla de 50 m sale infractora mientras uno con 500 m sale limpio haciendo lo mismo.

### 4.4 Tareas
**No existe.** `avgTaskRating30d` está a 0 en 491 snapshots y `task_ratings_raw`
tiene 1 fila. Antes de construir este eje hay que averiguar por qué no se escribe
— se sospecha el mismo patrón que `experienceByJob`: un trigger que no dispara o
un sync que no llega.

**Hasta entonces el eje se publica como `sin_evidencia` para todo el mundo, y se
dice en pantalla.** No se omite: su ausencia es información.

## 5. El cruce

El perfil **no es una puntuación ponderada**. Es una tabla de decisión donde cada
casilla se explica en una frase.

Razón: el modelo anterior (`effectiveRealCost` en Firebase) sumaba cinco
penalizaciones con coeficientes elegidos a mano (0,4 · 0,5 · 0,2 · 0,1 · 0,15) y
un techo de 1,5×. Servía como índice pero no se podía defender ante nadie que
preguntara de dónde salía cada coeficiente. Un encargado va a preguntar por qué
Fulano está por encima de Mengano, y la respuesta tiene que caber en una frase.

Reglas del cruce:

1. **Un eje en `sin_evidencia` no penaliza.** Reduce la confianza del perfil, que
   se publica junto a él (`ejes_con_evidencia: 3/4`).
2. **El perfil nombra el problema dominante**, no la media. Quien cumple horas
   pero no registra tiene un problema de proceso; quien registra pero no cumple lo
   tiene de horas. Son acciones distintas y el perfil debe decir cuál.
3. **Ningún perfil negativo se emite si el problema tiene una explicación
   estructural conocida** — valla corta, horario configurado imposible, confusión
   de centro. Esos casos producen un aviso al gestor sobre la configuración, no un
   juicio sobre la persona.

## 6. Representación

Regla de fondo: **el panel pinta excepciones, nunca el censo**, y no publica una
tasa sin evidencia suficiente. Con 500 empleados la pantalla ocupa lo mismo que
con 14; lo que mejora es la señal, no el tamaño.

- Denominador mínimo para publicar una tasa: **10 observaciones**. Con *n* la tasa
  salta de 1/n, así que por debajo de 10 un solo incidente la mueve más de 10
  puntos — más que las diferencias que se quieren detectar. Por debajo se publica
  el recuento crudo.
- Formas: número grande + barras para un hallazgo; tabla para pocos elementos;
  cuadrícula día × hora para el patrón temporal (única forma inmune al volumen:
  agrega, no enumera); dispersión de cuadrantes para el cruce de dos ejes.
- Nunca tarta ni doble eje. Paleta validada contra daltonismo.
- El cliente es gestor, no analista: por defecto **frase y número**; gráfica solo
  donde gana claramente a una frase.

## 7. Orden de construcción

1. **Tasa de fallo del fichaje** — la lectura más potente y la única agnóstica de
   la causa. Con denominador mínimo.
2. **Las tres lecturas restantes del geo** y el cierre del cuadre por cajones.
3. **El cruce de los tres ejes disponibles**, con tareas declarado
   `sin_evidencia`.
4. **Investigar por qué no llegan las valoraciones de tareas** y, cuando lleguen,
   activar el cuarto eje.
5. **Merlin**: builder con prompt de analista que recibe las **claves estables**
   del cruce, no datos crudos. Narra y prioriza; no calcula. Así el relato no puede
   contradecir a la pantalla, y si el modelo falla el panel sigue funcionando.

## 8. Criterio de aceptación

- Los totales de cada bloque cuadran con el número de registros de entrada.
- Ningún registro desaparece sin quedar contado en un cajón con nombre.
- Cada persona del cruce tiene los cuatro ejes informados, aunque alguno sea
  `sin_evidencia`.
- Verificado contra producción antes y después de escribir el código.
