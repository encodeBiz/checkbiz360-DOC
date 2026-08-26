# Prompt para el front — declaración de plantilla (bloqueante)

## Qué es esto y por qué bloquea

Rentman organiza al personal en carpetas que el cliente nombra a mano: «1. Personal en
plantilla», «2. Autónomos», «3. Freelancers». **No hay tipo ni identificador**: es texto
libre, y los ids sólo valen dentro de su cuenta. Nosotros no podemos deducir de ahí quién
tiene relación laboral con la empresa.

Y hay que saberlo, porque decide dos cosas:

- **El registro horario es obligatorio para el personal de la empresa**, no para un
  autónomo que le factura. Meter a todos en el mismo saco ensucia justo el documento que
  sirve para demostrar cumplimiento ante una inspección.
- **Se factura por empleado activo.**

Por eso es la **única pregunta bloqueante** del add-on: sin ella no se importa nada.

## Reglas de la pantalla

**Se enseña SIEMPRE.** Aunque haya una sola carpeta. Aunque ya esté contestada. No es un
ajuste que se rellena una vez y desaparece: es una afirmación del cliente sobre quién es su
personal, y tiene que poder revisarla y rehacerla cuando cambie su plantilla. Si sólo tiene
una carpeta, también se le pregunta — así se organiza, y en cualquier caso afirma.

**Se clasifican TODAS, una por una.** Dos opciones por carpeta: **plantilla** o
**colaboradores**. No vale «marca las de plantilla y el resto se asume»: dejar una carpeta
sin marcar la sacaría del registro horario sin que nadie lo haya declarado, que es
exactamente la vía para colar menos trabajadores de los que hay. Mientras quede una sin
clasificar, no se puede continuar.

**Se dice para qué es, sin rodeos.** Un texto del tipo: *«El registro horario es obligatorio
para el personal de tu empresa. Indica qué carpetas son plantilla y cuáles son
colaboradores externos; de esto depende quién aparece en tus informes legales.»* No es
letra pequeña: es lo que hace que el cliente se lo tome en serio.

**Y se afirma.** Un check explícito —«Confirmo que esta clasificación es correcta»— que
habilita el botón. La API **rechaza** el guardado sin él.

## Datos

La vista previa (`GET /{addonId}/catalogue/preview/{entityId}`) trae ya todo lo necesario:

```jsonc
"staff": {
  "declared": null,                  // o { "40": "staff", "41": "collaborator", ... }
  "declaredBy": null,                // uid de quien lo declaró
  "declaredAt": null,                // ISO
  "folders": [
    { "id": 40, "name": "1. Personal en plantilla", "people": 4 },
    { "id": 41, "name": "2. Autónomos",             "people": 7 },
    { "id": 43, "name": "3. Freelancers",           "people": 6 }
  ],
  "withoutFolder": 6,                // gente sin carpeta
  "unclassified": [40, 41, 43]       // mientras no esté vacío, no se importa
}
```

Enseñad el nombre **tal cual** y el número de personas al lado: el cliente reconoce su
propia estructura, y eso convierte la decisión en dos clics en vez de un formulario.

**`withoutFolder`** hay que mostrarlo también, como aviso, no como opción: esa gente entra
siempre como colaborador —fuera del registro horario— porque es el lado que no ensucia un
documento legal. En la cuenta de pruebas son integraciones y proveedores (Shopify, OpenAPI,
Webshop…), no personas.

## Guardar

`POST /{addonId}/settings/crew-folders`

```jsonc
{
  "entityId": "…",
  "folders": { "40": "staff", "41": "collaborator", "43": "collaborator" },
  "affirmed": true
}
```

Sin `affirmed: true` la API devuelve error de validación. Debe estar **toda** carpeta
existente en el objeto.

## Si se intenta importar sin declarar

`POST /{addonId}/catalogue/import` responde **409**:

```jsonc
{ "ok": false, "error": "crew_folders_undeclared",
  "folders": [ { "id": 40, "name": "1. Personal en plantilla" }, … ] }
```

Vienen las carpetas dentro para que podáis abrir la pregunta ahí mismo sin volver a pedir
la vista previa. **No lo tratéis como una avería**: es una pregunta pendiente, y el mensaje
al usuario debe llevarle a contestarla, no a reintentar.

## Dónde vive

En los **ajustes del add-on**, junto a la conexión, no escondido en el asistente de alta:
tiene que poder revisarse. Enseñad quién la declaró y cuándo (`declaredBy`, `declaredAt`) —
es una afirmación con consecuencias legales y conviene que se vea de quién es.
