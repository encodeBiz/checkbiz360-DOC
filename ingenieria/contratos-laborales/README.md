# Contratos laborales: oficio y salario al subir el contrato

**Componente:** `services/merlin/src/soporte/contratos-laborales` (lectura), `services/documents`
(disparo al subir), `services/entities` (bandeja `inbox`), panel (`encodebiz-front-saas`).
**Estado:** en staging desde el 22-nov-2026; no está en producción.

## Qué hace

Al subir un documento de tipo `contract` de un empleado, `documents` llama a merlin
(`POST /api/v1/gpt/soporte/contratos-laborales/procesar`, ruta interna). Merlin:

1. Descarga el PDF por el documental (solo él tiene la llave del cifrado) y lo pasa a texto.
2. Tapa nombre, DNI/NIE y correo de las personas y nombre, CIF y correo de la empresa
   (`borde/sombra-contrato-laboral.ts`). Nada más se tapa; ver la regla de anonimato.
3. Una llamada al modelo (`application/leer.ts`) saca oficio, categoría (grupo y nivel),
   convenio (nombre, sector, ámbito, territorio), jornada semanal, modalidad, fechas y salario.
4. Si el PDF es el formulario Contrat@ del SEPE, `domain/contrata.ts` lo lee por posiciones y
   cruza con lo que dijo el modelo.
5. `application/proponer.ts` arma la propuesta: ocupación casada con el catálogo de la empresa
   (`entities/{e}/jobs`), salario y **precio por hora bruto** (`domain/costeHora.ts`), con sus
   avisos (como mucho 4, `priorizar`).
6. Guarda `documents/{d}/readings/employment_contract` y deja una entrada en la bandeja
   `entities/{e}/inbox/{kind}_{refId}`. El panel la enseña (burbuja en `AdminLayout`) y, al
   confirmar, `POST …/:documentId/aplicar` escribe `job` y `price` en las responsabilidades del
   empleado sin tocar el catálogo (`domain/aplicar.ts`).

El precio por hora es **salario bruto**, sin Seguridad Social de la empresa, y se dice así.

## Las horas al año

El precio sale de dividir el salario anual entre las horas anuales del convenio. Si no se saben,
se estima con 52 semanas (`estimated: true`), que infla las horas y baja el precio en torno a un
14 % (con 1.792 h del convenio un contrato dio 8,10 €/h; a 40 × 52 daría 6,98 €/h). Por eso
importa tener la jornada del convenio aunque el contrato traiga la cifra.

## De dónde salen las tablas del convenio (historia corta)

Cuando el contrato remite «a las tablas» o no se saben las horas, hace falta el convenio.
Entre el 22 y el 23-nov-2026 se probó que lo buscase el modelo en internet (`application/tablas.ts`:
localizar con `web_search` en 68 dominios oficiales → descargar → elegir páginas → leer). Leer
la fila de un documento ya descargado funcionó (metal Madrid 2026: 1.590,26 € × 14 para el
grupo 5, del BOCM); **localizar el documento, no**: unas veces daba la revisión salarial de
2026 y otras el convenio de 2022, y las horas anuales cambiaban de una lectura a otra. Una
lectura con tablas costaba 35–48 mil tokens y 1–2 minutos.

La decisión del 23-nov (Jose) es sustituir la búsqueda por un **catálogo de convenios** que
mantiene Encodebiz y al que las empresas pueden añadir el suyo: [TDR-001](tdr/TDR-001-catalogo-de-convenios.md).

## Reglas que no se negocian

- Al modelo solo le llegan los datos tapados; al cliente no se le habla de IA.
- Un aviso dice lo observado («las tablas guardadas son de 2025»), no la causa.
- Nada se propone con aspecto de dato oficial si no sale de un documento concreto que se
  pueda enseñar.
- El consumo de tokens de cada llamada se apunta por empresa en `ai_usage/{entityId}_{mes}`
  (`contrato_laboral` y `tabla_convenio`), desde el envoltorio de `shared` y en ningún otro
  sitio: [consumo-ia](../consumo-ia/README.md).

## Pendiente antes de producción

- Catálogo de convenios (TDR-001) y retirada de la búsqueda web.
- En el contrato real probado el 23-nov no se leyeron bien las fechas ni el CNO; en los 13 de
  Contrat@ de Ayudarte sí. Hay que mirar por qué (el PDF tenía 45 mil caracteres con cláusulas).
- Nginx de producción (location con comillas: probar en un contenedor aparte), `PANEL_URL`
  de producción, reglas de `inbox` y `readings`.
- `AiPrivacyNotice` en el resto de pantallas que leen con modelo.
