# TDR-002 — El contrato desde la ficha del empleado: aviso, subida y puesto nuevo

**Estado:** aprobado por Jose el 25-nov-2026 («sí», a los dos puntos). **Hecho el 25-nov**: API en
staging (merlin, `0a652ff`), panel en `develop` del front (`8b7fe8b2c`), manual 138 y 06 en es/en/pt.
Sin probar todavía en el navegador contra staging; nada en producción.
**Componentes:** panel (`encodebiz-front-saas`, ficha del empleado y bloque «Aplicar a la ficha»),
merlin (`services/merlin/src/soporte/contratos-laborales`, `aplicar` y una consulta nueva).
**Depende de:** TDR-001 (catálogo de convenios) y de la lectura del contrato (README de esta carpeta).

## 1. Problema

Lo que Jose vio el 24-nov al probar la lectura del contrato:

1. Para ponerle contrato a una persona hay que salir de su ficha, ir a Gestión Documental y volver.
   La ficha no dice si la persona tiene contrato ni si su precio por hora sale de él. Y el
   precio es lo que hace que la persona «cuente bien» en costes y rentabilidad: hoy nadie se
   entera de que falta hasta que un informe sale raro.
2. Al aplicar lo leído, si el oficio del contrato no está en el catálogo de puestos de la
   empresa, la única salida es «Mantener el puesto que ya tiene» o irse a crear el puesto a mano
   y volver. «Crear ese skill a partir del contrato si no existe, así ya quedaría semiautomático
   lo del precio».

Jose: «un plus ventajoso… un warning diciendo que no tiene contrato asociado, algo sutil pero
visible, y que al clicarlo te lleve a gestión documental del empleado con el contrato
seleccionado».

## 2. Decisión

### 2.1 Una línea de estado bajo la cabecera del empleado

Debajo de la cabecera de `employee/[id]/detail/Detail.tsx` (donde ya está el `Alert` de problemas
de acceso), una sola línea discreta (`Alert severity="info"` con un enlace, o un chip con texto;
nunca un banner rojo) con **tres estados**:

| Estado | Texto | Al pulsar |
|---|---|---|
| Sin contrato | *Sin contrato de trabajo. Súbelo para que su precio por hora salga del contrato.* | Abre la pestaña **Documentos** (`HelpTabs` con `initialTabId: "documents"`) y, encima, `DocumentUploadModal` ya en tipo **Contrato**, ámbito empleado y `defaultEmployeeId` fijo. |
| Contrato leído, sin aplicar | *El contrato propone un precio por hora que aún no está en la ficha.* | Va a la ficha del documento (`employmentContractDetailPath(documentId)`), donde está «Aplicar a la ficha». |
| Leyendo / no se pudo leer | *Estamos leyendo el contrato…* / *El contrato no se pudo leer.* | La ficha del documento. |
| Aplicado | nada | — |

Lo ve y lo usa quien puede subir documentos a la persona (propietario y administradores), como
el bloque «Lo que dice el contrato».

**De dónde sale el dato.** Hoy el panel tendría que listar los documentos de la persona
(`fetchDocuments` tipo `contract`, ámbito empleado, no archivados), quedarse con el más reciente
y pedir su lectura (`GET contratos_laborales_handler/:documentId`). Son dos o tres llamadas para
una línea. Mejor **una consulta en merlin**:

```
GET /api/v1/gpt/soporte/contratos-laborales/empleado/:employeeId  ?entityId=
→ {ok, contract: null | {documentId, fileName, uploadedAt,
     reading: "none" | "processing" | "done" | "failed",
     applied: boolean, appliedAt: string | null,
     proposedPrice: number | null}}
```

`documents` del empleado con `type: "contract"`, `scope: "employee"`, `status != archived`, el
más reciente por `createdAt`; su `readings/employment_contract` da `status`, `appliedAt` y
`result.proposal.hourlyPrice`. Misma autorización que el resto del router (escritor de la
empresa). Sin campo nuevo en la ficha del empleado: el estado se deriva, no se duplica.

El panel la llama al abrir la ficha y después de subir un contrato desde la pestaña Documentos
(`EmployeeDocumentsSection` ya sabe cuándo acaba una subida de contrato:
`isEmploymentContractUpload`).

### 2.2 Crear el puesto desde el contrato

En `EmploymentContractApply.tsx`, cuando `proposal.occupation.inCatalog` es `false` y hay
`occupation.text`, el desplegable de puesto ofrece, además de «Mantener el puesto que ya tiene» y
los del catálogo, la opción **«Crear el puesto “<oficio leído>”»**, seleccionada por defecto.

API: `POST /:documentId/aplicar` acepta `newJobName: string` (excluyente con `jobId`). El
servidor:

1. Normaliza el nombre (`normalizarString`, como `addJobs` del panel) y lo **casa con el catálogo**
   antes de crear: si ya hay uno igual salvo mayúsculas, tildes o espacios, usa ese (`jobId`
   efectivo) y lo dice en la respuesta (`jobCreated: false, jobId`). Es lo que evita «Técnico
   operaciones sr» junto a «Técnico de operaciones senior».
2. Si no hay, crea `entities/{e}/jobs/{nuevo}` con la forma que escribe hoy el panel
   (`{job, price}`; comprobar `Job` en `src/domain/features/checkinbiz` por si TDR-010 añadió
   campos como el icono y ponerlos con su valor por defecto) y sigue con `planAplicar` como si
   se hubiera pedido ese `jobId`. Todo en el mismo lote que las responsabilidades.
3. El `price` del puesto del catálogo **no** se toca con el del contrato: el precio es de la
   persona (responsabilidad), no del puesto. El puesto nace solo con nombre.

Esto revierte una frase del manual (138, «Desde aquí no se crean puestos nuevos») y la regla de
que `aplicar` no toca el catálogo (README §6 de esta carpeta): pasa a tocarlo **solo para crear
el puesto leído, nunca para cambiar uno existente**. Escritura por backend, como manda
[permisos por backend](../../../../memory). Respeta «puestos: una sola lista» (la primera es la
predeterminada; aquí se añade al final).

## 3. Lo que NO se hace

- No se crea el puesto al leer: solo al pulsar «Aplicar a la ficha». La lectura sigue sin tocar
  nada de la empresa.
- No se cambia el precio del puesto ni el de otras personas con ese puesto.
- No se añade ningún campo al empleado (`hasContract` ni parecidos): se deriva.

## 4. Manual

- 138 «Lo que dice el contrato de trabajo»: en «Aplicar a la ficha», punto 1, «Si no, elija uno
  o deje **Mantener el puesto que ya tiene**» pasa a «Si no, puede **crear el puesto** con el
  nombre que dice el contrato, elegir otro del catálogo o dejar **Mantener el puesto que ya
  tiene**»; y quitar «Desde aquí no se crean puestos nuevos» de «Antes de empezar».
- 06 «Crear y gestionar empleados» (o el artículo de la ficha): la línea de estado del contrato
  y a dónde lleva.
- En es, en y pt.

## 5. Pruebas

- Merlin: `planAplicar` con `newJobName` que casa con uno existente (usa el existente), que no
  casa (crea), y con `jobId` y `newJobName` a la vez (400). La consulta del empleado: sin
  documentos, con contrato leyendo, leído sin aplicar, aplicado, archivado (no cuenta).
- Panel: los tres estados de la línea con contratos **ficticios** en staging; la subida desde la
  ficha deja la línea en «leyendo» y, al terminar, en «sin aplicar».

## 6. Fases

1. API: consulta del empleado + `newJobName` en `aplicar` (merlin), con pruebas. **Hecha** (25-nov).
2. Panel: línea de estado y modal preabierto; opción «Crear el puesto» al aplicar. **Hecha** (25-nov).
3. Manual es/en/pt. **Hecha** (25-nov).

## 7. Lo que quedó como se construyó

- Errores nuevos de `aplicar`: `puesto_doble` (vienen `jobId` y `newJobName`) y
  `nombre_de_puesto_no_valido` (vacío, más de 80 caracteres o sin dos letras seguidas). La respuesta
  lleva `job: {id, name, created}` cuando se pidió `newJobName`.
- El puesto nuevo se escribe `{job: <minúsculas>, price: 0}`, la forma con que lo crea hoy el
  servicio de empleados (`asegurarOcupacion`). Su id se reserva antes del plan para que la
  responsabilidad ya lo lleve, y va en el mismo lote que las responsabilidades.
- La consulta del empleado filtra solo por igualdades (`employeeId`, `type`, `status`), sin índice
  compuesto; el más reciente se elige en memoria. Devuelve además `error` (código del fallo).
- Panel: la línea es un `Alert` `outlined` info (warning si falló) con un solo botón. Mientras lee,
  vuelve a preguntar cada 30 s. Si la consulta falla (p. ej. 403 a un gestor), no se enseña nada.
  `HelpTabs` obedece cambios de `initialTabId` y `DocumentUploadModal` admite `defaultType`.
- Al aplicar, «Crear el puesto «…»» sale elegido por defecto solo si ningún puesto del catálogo
  casa por nombre normalizado; si casa, se elige ese y no se crea nada.
