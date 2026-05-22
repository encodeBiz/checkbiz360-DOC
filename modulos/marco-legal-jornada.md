# Marco Legal — Jornada Laboral, Horas Extras y Registro (España)

> Fuentes: Real Decreto Legislativo 2/2015 (ET); Real Decreto-ley 8/2019; Real Decreto Legislativo 5/2000 (LISOS).
> Última revisión normativa: mayo 2026. BOE-A-2015-11430 muestra texto consolidado con última actualización publicada el 04/12/2025.
> Este documento es un resumen operativo para el diseño del módulo `ContractProfile`. No sustituye asesoría jurídica laboral.

---

## 1. Jornada Ordinaria — Art. 34 ET

| Límite | Valor legal | Nota |
|---|---|---|
| Jornada máxima anual | 40 h/semana en cómputo anual | No se pueden superar 40 h de media aunque haya semanas de menos |
| Jornada máxima diaria | 9 h ordinarias | Puede reducirse o aumentarse por convenio colectivo (CT) |
| Descanso mínimo entre jornadas | 12 h consecutivas | Obligatorio. No negociable por convenio |
| Pausa dentro de la jornada | 15 min si jornada > 6 h continuadas | CT puede ampliarla. Para menores: 30 min si jornada > 4,5 h |
| Distribución irregular | Hasta 10 % de la jornada, si no hay CT | Con CT, el porcentaje puede modificarse. Preaviso 5 días al trabajador |

**Implicaciones para CheckBiz360:**
- `weeklyHoursContracted` no puede superar 40 h en jornada completa.
- Si un empleado acumula >40 h/semana de media anual, el sistema debe alertar.
- Las 12 h de descanso entre jornadas se pueden validar en el checkout (comparar `checkOutAt` con el próximo `scheduledStartAt`).

---

## 2. Horas Extraordinarias — Art. 35 ET

| Concepto | Valor | Nota |
|---|---|---|
| Límite anual | 80 h/año | Excluye horas extra por fuerza mayor |
| Fuerza mayor | Sin límite anual | Deben comunicarse a la autoridad laboral y cotizar |
| Carácter | Voluntario | Salvo que CT o contrato individual las pacte como obligatorias |
| Compensación mínima | Al menos igual a la hora ordinaria en dinero | O compensación con descanso equivalente |
| Plazo para descanso compensatorio | 4 meses desde la realización | Si no se compensan en plazo, se abonan en nómina |
| Cotización SS | Igual que horas ordinarias | Desde 2013: cotizan al tipo ordinario |
| Trabajadores nocturnos | Prohibidas salvo fuerza mayor | ET Art. 36.1 — no pueden hacer extras |
| Menores de 18 años | Prohibidas absolutamente | Sin excepciones |

**Implicaciones para CheckBiz360:**
- El campo `overtime.yearlyLimitHours` en `ContractProfile` tiene como techo legal 80.
- El sistema debe acumular `overtimeHoursYTD` por empleado y alertar al 80 % del límite configurado.
- Si el empleado tiene `nightShift.enabled = true` y `nightShift.overtimeAllowed = false` (default correcto por ley), el motor debe bloquear el cómputo de extras nocturnas y marcar la anomalía.

---

## 3. Trabajo Nocturno y a Turnos — Art. 36 ET

| Concepto | Valor | Nota |
|---|---|---|
| Franja nocturna | 22:00–06:00 | Referencia legal mínima para trabajo nocturno |
| Trabajador nocturno | Quien trabaja ≥ 3 h/noche de forma habitual, o ≥ 1/3 de su jornada anual en franja nocturna | Clasificación relevante para protecciones |
| Jornada máxima nocturna | 8 h/noche como media en 15 días | Promedio, no límite diario estricto |
| Complemento de nocturnidad | No fijado por ley — lo establece el CT | Rango habitual: 25–35 % sobre tarifa base |
| Evaluación de salud | Obligatoria para trabajadores nocturnos | Antes del inicio y periódicamente |
| Traslado a turno diurno | Obligatorio si hay problemas de salud acreditados | El trabajador tiene derecho preferente |
| Menores de 18 | Prohibido trabajo nocturno | Sin excepciones |

**Implicaciones para CheckBiz360:**
- `nightShift.startTime = "22:00"` y `nightShift.endTime = "06:00"` son los valores legales de referencia. El modelo los expone como configurables para soportar convenios o políticas internas más protectoras, pero el default debe ser el legal.
- El motor de checklog debe calcular `nightShiftMinutes` comparando el intervalo del turno con la franja nocturna configurada.
- Clasificar automáticamente a un empleado como "trabajador nocturno" cuando supere el umbral del Art. 36 es un input útil para alertas de gestión.

---

## 4. Contrato a Tiempo Parcial y Horas Complementarias — Art. 12 ET

| Concepto | Valor | Nota |
|---|---|---|
| Definición parcial | Horas < jornada comparador a tiempo completo | Puede ser horas/día, semana, mes o año |
| Horas complementarias pactadas (máx.) | 30 % horas ordinarias contratadas | CT puede elevar hasta 60 % |
| Horas complementarias voluntarias (máx.) | 15 % adicional sobre las ordinarias | CT puede elevar hasta 30 % |
| Preaviso | 3 días | Salvo que CT establezca otro plazo |
| Aceptación | Voluntaria por el trabajador | El rechazo no es causa de despido |
| Registro | Obligatorio mensual | Igual que jornada completa |
| Conservación | 4 años | Misma obligación que RDL 8/2019 |
| Cotización | Proporcional a horas trabajadas | Aplica el mismo tipo que jornada completa |

> Las horas complementarias **no son horas extraordinarias**. Si se supera el límite de complementarias, las horas adicionales sí pasan a ser extraordinarias y se aplica el Art. 35 ET.

**Implicaciones para CheckBiz360:**
- Si `contractType = "part_time"`, el motor usa el bloque `complementaryHours` en lugar de `overtime`.
- El sistema debe distinguir horas complementarias (dentro del límite del 30/60 %) de horas extraordinarias (si se supera ese límite).
- Alert: cuando el empleado parcial supera `weeklyHoursContracted * complementaryHoursLimitPercent / 100`.

---

## 5. Descanso Semanal y Fiestas — Art. 37 ET

| Concepto | Valor | Nota |
|---|---|---|
| Descanso semanal | 1,5 días consecutivos | Normalmente sábado tarde + domingo. CT puede acumular hasta 14 días |
| Fiestas nacionales | 14 días/año | Incluidas en el calendario de festivos del sistema |
| Trabajo en festivo | Debe compensarse con descanso o abono | CT establece el régimen. Si no hay CT: descanso + salario ordinario |
| Permiso por matrimonio | 15 días naturales | |
| Permiso por nacimiento/adopción | 2 días (trabajador no gestante) | CT puede ampliar |
| Permiso por fallecimiento/enfermedad grave familiar | 2 días (4 si hay desplazamiento) | |
| Permiso por examen | Tiempo necesario | Solo si el trabajador cursa estudios para obtener titulación |

**Implicaciones para CheckBiz360:**
- El módulo de festivos ya gestiona los 14 días nacionales.
- El descanso semanal de 1,5 días se puede validar como check en el motor de jornada (comprobar que entre el último turno del fin de semana y el primero del siguiente hay 36 h mínimas).

---

## 6. Vacaciones — Art. 38 ET

| Concepto | Valor | Nota |
|---|---|---|
| Duración mínima | 22 días laborables/año (≈ 30 días naturales) | CT puede ampliar |
| Fraccionamiento | Mínimo 2 semanas consecutivas | El resto puede fraccionarse de mutuo acuerdo |
| Retribución | Salario ordinario durante vacaciones | No se pueden compensar en metálico salvo extinción del contrato |
| Planificación | Conocida con 2 meses de antelación | Obligación del empresario |
| Prescripción | 18 meses desde el final del año de devengo | Si no se disfrutan por IT, se amplía el plazo |

---

## 7. Registro de Jornada — RDL 8/2019, Art. 10 (modifica ET Art. 34.9)

| Obligación | Detalle |
|---|---|
| Qué registrar | Hora de inicio y fin de la jornada de cada trabajador |
| Para quién | Todas las empresas, todos los trabajadores (sin excepción de sector o tamaño) |
| Forma | Negociación colectiva, acuerdo de empresa, o decisión del empresario previa consulta a RLT |
| Conservación | 4 años mínimo (accesible a trabajadores, RLT e Inspección) |
| Disponibilidad | El registro debe estar disponible en el centro de trabajo o accesible en tiempo real |

**CheckBiz360 cumple este requisito** mediante el timestamp inmutable de cada checklog (inicio y fin de jornada con coordenadas GPS, dispositivo y turno activo).

---

## 8. Sanciones — LISOS (RDL 5/2000)

### Infracciones graves (Art. 7 LISOS)

Superar los límites de jornada, no respetar descansos, no llevar registro de jornada o no conservarlo 4 años.

| Grado | Importe |
|---|---|
| Mínimo | 751 € – 1.500 € |
| Medio | 1.501 € – 3.750 € |
| Máximo | 3.751 € – 7.500 € |

### Infracciones muy graves (Art. 8 LISOS)

Superar el límite de horas extraordinarias (80 h/año), hacer trabajar a menores de noche o en extras.

| Grado | Importe |
|---|---|
| Mínimo | 7.501 € – 30.000 € |
| Medio | 30.001 € – 120.005 € |
| Máximo | 120.006 € – 225.018 € |

> Los importes se actualizan periódicamente. Los vigentes desde la reforma de la LISOS de 2023 pueden ser superiores. Verificar en el BOE vigente antes de comunicar a clientes.

---

## 9. Resumen para Diseño del Módulo ContractProfile

| Campo del modelo | Límite legal de referencia | Flexible por CT |
|---|---|---|
| `weeklyHoursContracted` | Max 40 h | No (es la jornada máxima) |
| `dailyHoursMax` | Max 9 h ordinarias | Sí |
| `minRestBetweenShiftsHours` | Min 12 h | No |
| `overtime.yearlyLimitHours` | Max 80 h | Solo a la baja |
| `overtime.payRate` | Min 1.0 (igual a ordinaria) | Sí (al alza) |
| `overtime.restMaxWeeks` | Max 16 semanas (4 meses) | Sí (a la baja) |
| `nightShift.startTime / endTime` | 22:00–06:00 | Sí por CT |
| `nightShift.dailyHoursMaxNight` | Max 8 h/noche (media 15 días) | No |
| `complementaryHours.limitPercent` | Max 30 % (60 % con CT) | Sí |
| `complementaryHours.noticeDays` | Min 3 días | Sí (a la baja si CT lo permite) |

---

## 10. Referencias Normativas

| Norma | BOE | Contenido |
|---|---|---|
| Real Decreto Legislativo 2/2015 (ET) | BOE-A-2015-11430 | Texto refundido del Estatuto de los Trabajadores |
| Real Decreto-ley 8/2019 | BOE-A-2019-3481 | Registro obligatorio de jornada (modifica ET Art. 34.9) |
| Real Decreto Legislativo 5/2000 (LISOS) | BOE-A-2000-15060 | Infracciones y sanciones en el orden social |
| Criterio Técnico ITSS 101/2019 | — | Criterios de actuación inspectora sobre registro de jornada |
