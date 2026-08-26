# Prompt para el front — resumen de catálogo de un add-on

> Contexto: la API ha añadido un endpoint nuevo y ha empezado a emitir dos eventos
> que el front ya tenía tipados. Esto es lo que queda por hacer del lado del front.

## 1. Lo que NO hay que tocar

La bitácora ya está lista. `AddonActivityDirection` ya contempla `import_task` e
`import_responsibility`, y los cinco idiomas ya tienen su etiqueta en
`integration.addons.activity.direction`. Hasta ahora esos eventos no llegaban nunca
porque la API no los emitía; ya los emite. **No hay que cambiar nada: empezarán a
aparecer solos.** Basta con comprobar que se pintan bien cuando lleguen.

Tampoco entran aquí las dos tarjetas en blanco del resumen general —«eventos 24h» y
«fallos abiertos»—. Siguen sin dato de backend y siguen esperando.

## 2. El hueco que hay que cerrar

Hoy lo que un cliente tiene importado **sólo se ve en la respuesta de la importación**.
Esa respuesta vive en memoria: al recargar la pantalla desaparece. Quien entra al día
siguiente no tiene forma de saber qué tiene, y la pantalla se queda en blanco como si
nunca hubiera importado nada.

El endpoint nuevo responde a «¿qué tengo?» en cualquier momento.

## 3. Endpoint

`GET /{addonId}/catalogue/summary/{entityId}`

Mismo transporte, token y trato del 2FA caducado que el resto de operaciones:
va por `addonApiRequest`, como todo lo demás.

```jsonc
{
  "ok": true,
  "summary": {
    "total": 187,
    "byKind": {
      "project":        { "imported": 16, "pending": 0, "failed": 0, "skipped": 0, "total": 16 },
      "warehouse":      { "imported": 3,  "pending": 0, "failed": 0, "skipped": 0, "total": 3 },
      "crew":           { "imported": 1,  "pending": 22, "failed": 0, "skipped": 0, "total": 23 },
      "assignment":     { "imported": 44, "pending": 0, "failed": 0, "skipped": 0, "total": 44 },
      "warehouse_task": { "imported": 0,  "pending": 0, "failed": 0, "skipped": 0, "total": 0 }
    },
    "lastSyncedAt": "2026-08-22T10:14:03.221Z"
  }
}
```

**Los cinco tipos vienen siempre, aunque estén a cero.** Es deliberado: así la rejilla
tiene la misma forma antes y después de importar, y una fila que aparece de la nada no
se lee como un cambio que no ha ocurrido. No los filtréis por `total > 0`.

## 4. Lo que hay que implementar

**Contrato** — en `IAddonOperations.ts`, junto a los demás. Ni un nombre de Rentman:
`addonId` es un parámetro, como en todo el fichero.

```ts
export interface IAddonCatalogueKindCount {
  imported?: number; pending?: number; failed?: number; skipped?: number; total?: number;
}

/** Lista abierta: un tipo nuevo debe poder llegar sin romper la pantalla. */
export type AddonCatalogueKind =
  | 'project' | 'warehouse' | 'crew' | 'assignment' | 'warehouse_task' | (string & {});

export interface IAddonCatalogueSummary {
  total?: number;
  byKind?: Partial<Record<AddonCatalogueKind, IAddonCatalogueKindCount>>;
  /** `null` = nunca se ha importado. No es lo mismo que importar y que salga cero. */
  lastSyncedAt?: string | null;
}
```

**Servicio** — en `addons.operations.service.ts`, en la sección de importación:

```ts
export async function fetchAddonCatalogueSummary(
  addonId: string, entityId: string, { token, locale }: Auth,
): Promise<IAddonCatalogueSummary | null> {
  const result = await addonApiRequest<{ ok?: boolean; summary?: IAddonCatalogueSummary }>(
    `/${addonId}/catalogue/summary/${entityId}`, { method: 'GET', token, locale },
  );
  return result?.summary ?? null;
}
```

**Controlador** — en `addonOperations.controller.ts`, un `Block<IAddonCatalogueSummary>`
más, cargado con los demás bloques de sólo lectura y con el mismo criterio: sólo si el
add-on está conectado, carga por su cuenta, y si falla se queda roto él solo sin
arrastrar a los demás.

Hay que **recargarlo cuando termine una importación real** (`dryRun: false`), porque es
justo entonces cuando cambia. Tras una simulación, no: no ha cambiado nada.

**Pantalla** — dentro de `AddonImportPanel`, **encima** de la vista previa. El orden
importa y es el mismo que ya sigue el panel: primero «qué tengo», luego «qué pasaría»,
y sólo al final «hazlo». Reutilizad `Figure` y `Figures`, que ya están en el fichero.

## 5. Los dos estados que hay que distinguir

Esto es lo único delicado:

- **`lastSyncedAt === null`** → nunca se ha importado. Estado vacío con su frase, **no**
  una rejilla de ceros. Una rejilla de ceros afirma «tienes cero centros», que es una
  medición; y aquí no se ha medido nada todavía.
- **`lastSyncedAt` con fecha** → los ceros son reales y se pintan como ceros. Aquí sí:
  cero tareas de almacén después de importar es un dato, no un hueco.

Ojo con la diferencia respecto a `Figure`, que pinta raya cuando el valor es `undefined`.
Ahí la raya es correcta porque el dato falta. Aquí, con fecha de importación, el cero se
sabe y se enseña.

El `pending` de cada tipo debe llevar al panel de pendientes que ya existe: es lo mismo
que ya cuenta `GET /pending/:entityId`, visto desde otro ángulo. No lo dupliquéis con
otra llamada, enlazad.

## 6. Traducciones

Claves nuevas en los **cinco** idiomas (`es`, `en`, `fr`, `pt`, `de`), colgando de
`integration.addons.import`: título del bloque, la frase del estado vacío, «última
importación» y el rótulo de cada uno de los cinco tipos. Los tipos se traducen a lo que
son para el cliente: montajes, almacenes, personas, plazas de trabajo y tareas de
almacén — no a los nombres técnicos que trae la API.

## 7. Sobre `detail` (respuesta a vuestro apunte)

Comprobado en los tres endpoints: **`detail` viaja siempre como texto o `null`, nunca
como objeto.** Todas las columnas son `TEXT` y todas las rutas que lo escriben están
tipadas `string | null`, así que podéis pintarlo tal cual sin comprobar el tipo.

Teníais razón en el fondo, aun así. Había un caso —cuando Rentman rechaza con un cuerpo
JSON que no trae ninguna frase dentro— en el que ese texto acababa siendo el JSON crudo
del proveedor. Seguía siendo un `string`, así que no rompía nada, pero se leía fatal en
pantalla. Corregido en origen: ahora ahí sale una frase nuestra y el cuerpo original se
queda en nuestros logs, que es donde se diagnostica.

Es decir: **no hace falta el campo aparte**. `detail` es campo de pantalla y a partir de
ahora cumple lo que promete.

## 8. Tareas importadas: `metadata.staffing`

Las tareas que crea un add-on **se asignan a su gente aunque esa gente todavía no pueda
trabajar**. En Rentman casi nadie tiene correo, y el correo es el acceso a checkbiz: sus
fichas nacen inactivas. Ocultar la tarea hasta que se completen dejaría al cliente con una
pantalla vacía y sin saber por qué, cuando el trabajo existe y está planificado.

Cuando hay algo que decir, la tarea trae `metadata.staffing`:

```jsonc
{
  "assigned": 3,        // personas asignadas
  "ready": 0,           // cuántas pueden trabajar hoy
  "blocked": ["emp_1", "emp_2", "emp_3"],
  "status": "no_active_staff"   // o "partial"
}
```

**Si el campo no viene, no pasa nada**: toda la gente asignada puede trabajar. No lo
interpretéis como cero.

- `no_active_staff` → la tarea existe pero hoy no puede hacerla nadie. Va en estado
  `draft`. Merece un distintivo claro: «sin personal activo». Es accionable — se arregla
  completando el correo de esa gente, y desde ahí se puede enlazar al panel de pendientes.
- `partial` → algunos pueden y otros no. La tarea va `assigned` y funciona; el aviso es
  informativo.

El estado de la tarea ya lo refleja (`draft` frente a `assigned`), así que no hace falta
inventar un estado nuevo: basta con leer `staffing` para explicar **por qué** está en
borrador, que es lo que hoy no se puede contar.
