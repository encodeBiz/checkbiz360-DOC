# 02 · Caso real — Tapissat de Carrosseries

Un cliente rellenó la plantilla el 2026-09-04. Es el primer fichero real que entra, y sirve
de banco de pruebas del asistente: **todo lo que aparece aquí es lo que tendrá que resolver
en producción**, y nada de ello es hipotético.

**Quién es:** Tapissat de Carrosseries S.L., B17576000, tapicería de carrocerías en Arbúcies
(Girona). Cuatro personas, cuatro ubicaciones de trabajo, jornada continua de 07:00 a 15:00
de lunes a viernes.

**Volumen:** 4 sucursales · 4 empleados · **16 responsabilidades** (ver §2) · 1 horario
semanal · 17 filas de festivos que **se expanden a 66 días**, de los que 50 caen en día
laborable.

---

## Lo que la plantilla ya hace bien

La versión que rellenó el cliente incorpora dos arreglos respecto a la revisada el 03-09, y
los dos funcionan:

- **Los horarios van por fila de día y turno** (`dia | turno | hora_inicio | hora_fin`), con
  la instrucción de repetir el día con turno 1 y turno 2 si es partido. La jornada partida
  ya se puede expresar.
- **Las fechas de festivos son enteros limpios**, sin hora ni desfase. Decodificadas, salen
  todas correctas: la Diada el 11/09, la Festa Nacional el 12/10, el Divendres Sant el
  26/03/2027. La trampa de formato está cerrada.

Y el cliente ha usado `owner`, que era el hueco señalado: el cuarto es el propietario.

---

## Lo que el asistente tendrá que resolver

### 1. Los costes son los del ejemplo — y esto es lo grave

| persona | puesto | coste_mes | coste_hora |
|---|---|---|---|
| 1 | Responsable de operaciones | 3200 | 22,50 EUR |
| 2 | Secretaria | 2600 | 18,00 EUR |
| 3 | Responsable de innovación | 1800 | 14,00 EUR |

Son **exactamente los valores de muestra de la plantilla** (3200/22,5 · 2600/18 · 1800/14),
en el mismo orden de filas. Se delata solo: la Secretaria cobraría más que la Responsable de
innovación. El cliente no ha rellenado los costes, ha dejado el ejemplo.

Sembrar esto mete nóminas inventadas en un cliente real. Y por
[ADR-002](./adr/ADR-002-la-puesta-en-marcha-siembra-patron-y-coste.md), el precio se congela
dentro de cada fichaje: corregirlo después no arregla lo ya registrado.

**El asistente tiene que detectar que un valor coincide con el del ejemplo y preguntarlo, no
importarlo.**

### 2. Las responsabilidades son 16, no 4 — y si se hacen mal nadie ficha

La hoja 04 trae cuatro filas con `nombre_sucursal` **vacío**. Leído literalmente, eso es
ámbito entidad. Y ámbito entidad **no sirve para fichar**:

`createChecklog` resuelve la responsabilidad con
`findResponsibilities({entityId, branchId}, employeeId)`, y esa consulta añade
`where("scope.branchId", "==", branchId)`. Una responsabilidad sin `scope.branchId` no
aparece en el resultado, y el controlador corta con **404 `employee/not_resposibility`**.
Las cuatro personas de Tapissat no podrían fichar en ninguna parte.

Lo que quiere decir la hoja lo dice la hoja 03: los cuatro tienen
`sucursales_asignadas = Taller, Ayats, Indcar, Beulas`. Es decir, **`nombre_sucursal` vacío
significa «lo mismo en todas sus sucursales»**, no «en ninguna». Son cuatro personas por
cuatro centros: **16 responsabilidades**.

Y hay una confirmación en el código: `createResponsibility` hace
`arrayUnion(scope.branchId)` sobre la ficha del empleado. `Employee.branchId[]` no se
rellena por separado — se rellena al crear cada responsabilidad. Son la misma operación, y
por eso el cliente puso las sucursales en la hoja de empleados y las dejó vacías en la de
responsabilidades.

**Es el ejemplo de manual de un dato que hay que cruzar entre hojas, no leer en una.**

### 2b. La fila del owner se apoya en la hoja anterior

La fila del propietario es `<su correo> | owner` y ahí se acaba: sin `job_nombre`, sin coste, sin `activo`.
Pero el puesto **sí está**, en la hoja 03: el puesto del propietario es «Propietario». El `job.job` se
arrastra de ahí, igual que se arrastran las sucursales. Lo que de verdad le falta es el
coste por hora, como a los otros tres.

### 3. `coste_hora` no es un número

Viene como texto: `22,50 EUR`. Coma decimal y sufijo de moneda. Y la columna se titula
`coste_hora (opcional)` cuando es la única que el modelo sabe usar —`Job.price` es por
hora—, mientras `coste_mes`, que el cliente sí rellenó, no existe en el modelo.

### 4. Media plantilla se queda fuera de la geocerca

El responsable de operaciones y el propietario traen `trabaja_fuera_de_oficina = si`, que mapea a `enableRemoteWork`. Y eso
no significa «se mueve entre sedes»: en `createChecklog`, `enableRemoteWork === true`
**exime del control de ubicación por completo**. Dos de cuatro personas ficharían desde
cualquier sitio.

Es casi seguro que el cliente quiso decir lo primero. Hay que preguntarlo.

### 5. Las «sucursales» no son suyas

Ayats, Indcar y Beulas son fabricantes de carrocerías: son **clientes** de Tapissat, no sedes
propias. Solo «Taller» lleva su NIF; las otras tres lo tienen vacío. Es un uso legítimo de
sucursal como lugar de trabajo —y explica el radio de 500 m—, pero conviene que quede
escrito, porque cambia cómo se lee el panel: ahí «sucursal» significa «obra».

### 6. Los festivos vienen en rangos, y el modelo no los tiene

`Holiday` es una fecha suelta: `{name, date, paid}`, sin `endDate`. El cliente ha metido
periodos:

- Vacances Nadal 2026: 23/12 → 06/01 (15 días)
- Vacances agost 2027: 09/08 → 29/08 (21 días)
- Pont de la puríssima: 07/12 → 08/12 (2 días)
- Vacances Nadal 2027: 23/12 → 06/01 (15 días)

De 17 filas salen **66 documentos de festivo**, de los cuales 50 caen en día laborable y 16
en sábado o domingo, ya cerrados por el horario.

Se guardan los 66. Podar los de fin de semana ahorra dieciséis entradas de un array —nada— y
a cambio pierde información: el día que abran los sábados, el 26 de diciembre debería seguir
siendo festivo y ya no lo sería.

Aparte, «Vacances Nadal» y «Vacances agost» no son festivos sino **cierres de empresa**. El
modelo no distingue las dos cosas y `holiday` es lo que hay, así que funciona; pero el
cliente verá veintiún «festivos» en agosto y conviene decírselo.

### 7. Residuos del ejemplo y ruido de normalización

- `observaciones = "Sucursal ejemplo."` en la fila de Ayats.
- `coste_mes` suelto en la celda A1 de la hoja 04.
- `pais` es «España» en una sucursal y «Espana» en las otras tres.
- La calle es «Palacagüina» en la hoja de empresa y «Palacaguïna» en la de sucursales.
- `puesto` dice «Responsable innovación» y `job_nombre` dice «Responsable de innovación».
- Las sucursales asignadas van separadas por coma, no por el separador de las instrucciones.
- Las hojas 06 y 07 traen prosa dentro del área de datos («Todas las sucursales tienen el
  mismo horario»), donde un lector ingenuo buscaría una fila.
- `region` es «Arbúcies», que es el municipio; el campo espera la provincia.

### 8. Direcciones flojas para geocodificar

`c/ Riera Xica, s/n Polígon Industrial, 17401, Girona` no tiene número y mezcla el código
postal de Arbúcies con el nombre de la provincia. Con 500 m de radio probablemente cuele,
pero la precisión que devuelva el geocodificador hay que mirarla sucursal por sucursal: es
la diferencia entre poner la valla en la nave o en mitad del polígono.

---

## Sobre los datos

Este documento describe un fichero con datos personales reales —nombres, DNIs, teléfonos y
correos de cuatro personas—. **El fichero relleno y el borrador que sale de él no se guardan
en este repositorio.** Aquí queda el análisis y la forma; los datos viven donde los dejó el
cliente.

---

## Qué prueba este caso

Que el trabajo del asistente **no es leer el fichero, es cruzarlo**. El fichero se lee bien.
Lo que hay que hacer es todo lo demás: sacar el puesto del owner de la hoja de empleados,
entender que una casilla vacía significa «en todas» y no «en ninguna», darse cuenta de que
unos números son los del ejemplo, de que un «sí» significa algo distinto de lo que el cliente
cree, y de que 17 filas son 66 documentos.

Ninguna hoja, leída sola, dice la verdad.

Ninguna de las ocho cosas de arriba daría un error de importación. Las ocho producirían un
cliente que parece montado.
