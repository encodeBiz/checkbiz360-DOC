# 07 — Verificación de fuentes de señales (D7)

Verificado el **2026-10-13**: ficheros reales descargados con curl y condiciones de uso
leídas en las fuentes oficiales. Responde a [D7](./06_decisiones-abiertas.md#d7--fuentes-de-señales).
No hay código; esto es lo que se puede afirmar antes de diseñar la ingesta de la Fase 4.

**Conclusión:** se empieza por la **PLACSP**: trae NIF del adjudicatario, CPV, estado y fecha,
y su reutilización comercial está autorizada. El **BORME** sirve como segunda fuente, pero sin
CIF ni CNAE estructurado. Los **portales de empleo** quedan fuera: sus condiciones prohíben
leerlos de forma automática y sus API no están pensadas para este uso.

---

## 1. Plataforma de Contratación del Sector Público (PLACSP)

### Acceso

Hay sindicación oficial en **ATOM (RFC 4287) con contenido CODICE** (XML). Está documentada en
la [especificación de sindicación](https://www.hacienda.gob.es/Documentacion/Publico/D.G.%20PATRIMONIO/Plataforma_Contratacion/especificacion-sindicacion-1-3.pdf)
(DGPE, 163 págs.) y en la [página de datos abiertos de Hacienda](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/licitaciones_plataforma_contratacion.aspx),
que publica 6 conjuntos de datos. Estos tres sirven para las señales:

| Canal | URL vigente (sin autenticación) | Refresco observado |
|---|---|---|
| Perfiles de contratante alojados en la PLACSP (sin menores, desde 2012) | `https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom` | Casi en tiempo real: a las 20:16 traía entradas de las 20:08 |
| Agregación de plataformas autonómicas (sin menores, desde 2016) | `.../sindicacion_1044/PlataformasAgregadasSinMenores.atom` | Una vez al día (`Last-Modified` a las 01:00 UTC) |
| Contratos menores (desde 2018) | `.../sindicacion_1143/contratosMenoresPerfilesContratantes.atom` | Una vez al día (a las 01:02 UTC) |

- **Paginación:** cada fichero enlaza con el anterior mediante `<link rel="next">`
  (`..._AAAAMMDD_HHMMSS.atom`). Las bajas llegan como `<at:deleted-entry>`.
- **Histórico:** `..._AAAAMM.zip` por mes y `..._AAAA.zip` por año. El de septiembre de 2026
  pesa **más de 62 MB** (la descarga se cortó a los 60 s con 62,7 MB recibidos).
- **Volumen:** una página de perfiles pesa **7-16 MB** y trae unas 220-470 entradas. En 9
  páginas había 4.210 entradas (4.016 expedientes distintos), casi todas del 9 al 13 de octubre.
  Agregación y menores: alrededor de 1 MB por página.
- **Cobertura de la agregación:** en la página leída solo aparecían Cataluña (35), Madrid (13) y
  Galicia (1). Las demás autonomías sin plataforma propia publican en la PLACSP directamente.
- **Trampa de TLS:** el certificado lo emite la **FNMT** («AC RAIZ FNMT-RCM SERVIDORES SEGUROS»),
  que no viene en el almacén de CA de curl ni en el de Node. Sale `self signed certificate in
  certificate chain`. Se resuelve añadiendo esa raíz (`--cacert` / `NODE_EXTRA_CA_CERTS`),
  **nunca desactivando la verificación**. El dominio nuevo `contrataciondelsectorpublico.gob.es`
  (el que enlaza ya Hacienda) tiene el mismo problema; el antiguo sigue sirviendo los ficheros.
- Una petición `HEAD` a veces se responde con un *connection reset*. Hay que usar `GET`.

### Estructura de una entrada adjudicada

Ejemplo real: limpieza de centros de un organismo estatal, CPV 90911200, por lotes. Se omiten
valores identificativos. Todas las rutas cuelgan de `entry/cac-place-ext:ContractFolderStatus`:

| Dato | Ruta |
|---|---|
| Expediente | `cbc:ContractFolderID` y `cbc:UUID` |
| Estado | `cbc-place-ext:ContractFolderStatusCode`: `PRE` anuncio previo, `PUB` en plazo, `EV` pendiente de adjudicación, `ADJ` adjudicada, `RES` resuelta (formalizada, desierta o con desistimiento), `ANUL` |
| Órgano contratante | `cac-place-ext:LocatedContractingParty/cac:Party/cac:PartyName/cbc:Name` (más su DIR3 en `PartyIdentification/cbc:ID`) |
| Objeto | `cac:ProcurementProject/cbc:Name` (también en `entry/title`) |
| CPV | `cac:ProcurementProject/cac:RequiredCommodityClassification/cbc:ItemClassificationCode` (y lo mismo por lote en `cac:ProcurementProjectLot/...`) |
| Importe y lugar | `.../cac:BudgetAmount/cbc:TaxExclusiveAmount`, `.../cac:RealizedLocation/cbc:CountrySubentityCode` (NUTS) |
| Resultado (uno por lote) | `cac:TenderResult/cbc:ResultCode`: `8` adjudicado, `9` formalizado, `3`/`4` desierto, `5` desistimiento, `6` renuncia |
| Fechas | `cac:TenderResult/cbc:AwardDate`; formalización en `cac:TenderResult/cac:Contract/cbc:IssueDate` |
| **Adjudicatario** | `cac:TenderResult/cac:WinningParty/cac:PartyIdentification/cbc:ID` con `schemeName="NIF"`, y `.../cac:PartyName/cbc:Name` |
| Importe adjudicado | `cac:TenderResult/cac:AwardedTenderedProject/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount` |
| Lote | `cac:TenderResult/cac:AwardedTenderedProject/cbc:ProcurementProjectLotID` |
| Enlace público (la URL de la señal) | `entry/link/@href` (deeplink `detalle_licitacion`) |

Medido en la primera página: de 220 entradas, 101 traían `WinningParty` y **todas con ID**.
Los 350 adjudicatarios de esa página se reparten en 343 con `schemeName="NIF"` y 7 con `OTROS`.
Por forma del identificador: 316 son personas jurídicas (empiezan por letra de sociedad), 29
son otros (UTE, extranjeras) y **5 son personas físicas** (NIF/NIE).

**Ojo:** una entrada se reemite cada vez que cambia cualquier dato del expediente. El ejemplo
salió en el feed de hoy con una adjudicación de **agosto de 2024**. La fecha de la señal tiene
que ser `AwardDate` o `IssueDate`, nunca `entry/updated`. Para no duplicar, la clave es
expediente + lote + `ResultCode`.

### CPV por nicho

Prefijos contrastados con los títulos de las licitaciones de las 9 páginas descargadas
(ocurrencias entre paréntesis):

- **Limpieza (81.2x):** `90910000` limpieza, `90911000`/`90911200` (39) edificios, `90911300`
  ventanas, `90919000`/`90919200` (23) oficinas, `90919300` escuelas. `90610000`/`90611000`
  (limpieza viaria) salen mezclados en contratos de limpieza; se clasifican aparte.
- **SAD (88.1x):** `85312000` (6) asistencia social sin alojamiento, `85310000`, `85312100`,
  `85320000` servicios sociales, `98513310` ayuda a domicilio. El título hay que comprobarlo:
  `853*` también abarca residencias y centros de día.
- **Obras (41-43):** todo `45*`. Es el grueso: 297 adjudicaciones de septiembre-octubre
  en la muestra.
- **Eventos / alquiler AV (77.39, 90.0x, 82.30):** `79952000`/`79952100` eventos, `79950000`,
  `79954000` fiestas, `79956000` ferias, `51313000`/`51314000` instalación de equipos de sonido
  y vídeo, `92370000` técnicos de sonido, y equipos `32321200`, `32321300`, `32342410`
  (aparecen cuando se alquila con montaje).

En la muestra, adjudicaciones con `AwardDate` desde septiembre de 2026: obras 297, eventos y AV
unas 100, SAD 14, limpieza 12. El volumen de limpieza y SAD es bajo en los perfiles estatales.
Casi todo está en ayuntamientos y en la agregación autonómica, que también hay que leer.

### Condiciones de reutilización

- El fichero no declara licencia propia. Vale el [aviso legal del Ministerio de Hacienda](https://www.hacienda.gob.es/es-ES/Paginas/AvisoLegal.aspx),
  según la **Ley 37/2007** y el RD 1495/2011: permite el uso «para fines comerciales y no
  comerciales» con «cesión gratuita y no exclusiva» de derechos.
- Condiciones: **citar la fuente** («Origen de los datos: Ministerio de Hacienda»), con la
  fecha de actualización; no desnaturalizar el sentido; no sugerir respaldo oficial; conservar
  los metadatos.
- **RGPD:** la reutilización no exime. Los adjudicatarios que son personas físicas
  (autónomos) son datos personales. Se descartan, o se tratan con base jurídica e informando al
  interesado.

## 2. BORME (BOE)

- **API oficial:** `https://www.boe.es/datosabiertos/api/borme/sumario/{AAAAMMDD}`, en XML o
  JSON según la cabecera `Accept` ([doc. API](https://www.boe.es/datosabiertos/api/api.php)).
  No documenta límites de uso.
- Probado con el **sumario del 2026-10-13** (BORME-S-2026-197): HTTP 200, 58 KB en JSON. Trae
  la sección A, actos inscritos, con 30 ítems (uno por provincia), la sección B, otros actos
  (4), y la C, avisos (0). Cada ítem tiene `url_xml`
  (`https://www.boe.es/diario_borme/xml.php?id=BORME-A-2026-197-03`), además de `url_html` y
  `url_pdf`.
- **El XML de cada provincia no está estructurado por acto.** Es `<texto>` con párrafos
  `<p class="articulo">NNNNNN - RAZÓN SOCIAL SL.</p>` seguidos de `<p class="parrafo">` en texto
  libre: «Constitución. Comienzo de operaciones… Objeto social… Domicilio… Capital…»,
  «Nombramientos. Adm. Unico: …», «Datos registrales. S 8, H A 192104…».
- **No hay filtro por actividad ni CNAE.** En los 30 ficheros del día (2.736 inscripciones),
  «CNAE» aparecía 151 veces y solo dentro del objeto social, cuando el notario lo redacta así.
  Lo demás es texto libre: filtrar por nicho obliga a buscar palabras clave en el objeto social
  y deja huecos.
- **No hay CIF.** La empresa se identifica por su razón social, y la hoja registral (`H A 192104`,
  por provincia) es lo único estable. Casar con un lead exige comparar nombres normalizados.
- **Actos útiles y recuento del día:** Constitución (450; empresa nueva del nicho), Nombramientos
  (1.343) y Ceses (456) (cambio de gerencia), Ampliación de capital (94; crece), Cambio de
  domicilio (174), Cambio de objeto social (65; entra en el nicho), Fusión (12). Situación
  concursal (45), Disolución (114) y Extinción (118) sirven como señal **negativa** (descartar
  el lead).
- **Condiciones:** el [aviso legal del BOE](https://www.boe.es/informacion/aviso_legal/index.php#reutilizacion)
  (RD 1979/2008) permite el uso comercial. Obliga a citar la fuente «incluyendo en todo caso un
  enlace» y prohíbe «desnaturalizar el sentido». Y añade: «cuando los documentos contengan
  datos de carácter personal, su reutilización deberá realizarse con pleno respeto al Reglamento
  (UE) 2016/679». Los nombres de administradores y socios únicos **son datos personales**. Lo
  prudente es guardar el acto («nuevo administrador único») sin el nombre de la persona.

## 3. Portales de empleo

- **Indeed:** las [Condiciones](https://www.indeed.com/legal?hl=es), en sus reglas de uso del
  sitio, prohíben «use ningún sistema automatizado (bots, scrapers, arañas, IA o Agentic AI) para
  acceder, extraer datos o enviar contenido al Sitio, de forma masiva o de otro modo, sin el
  permiso expreso por escrito de Indeed». Sus API sirven para publicar ofertas e integrar ATS,
  no para leer ofertas de terceros.
- **LinkedIn:** el [User Agreement](https://www.linkedin.com/legal/user-agreement) prohíbe en el
  §8.2(2) «use software, devices, scripts, robots or any other means… (such as crawlers, browser
  plugins…) to scrape or copy the Services», y en el §8.2(13) el uso de bots. Sus API de empleo
  son para socios de Talent Solutions (esto no lo he comprobado hoy).
- **InfoJobs:** tiene [API oficial](https://developer.infojobs.net/) con búsqueda de ofertas;
  pide cuenta y registrar la aplicación. Su `robots.txt` bloquea por completo a agregadores
  (`jobrapido`) y a los bots de IA (`GPTBot`, `ClaudeBot`…), y a todos los demás les cierra los
  listados de resultados. **No he podido leer sus condiciones de uso** (el sitio devuelve 456 a
  clientes automáticos y 404 en las rutas probadas). No queda verificado si la API permite este
  uso comercial.
- Además, la base de datos de un portal está protegida por el derecho *sui generis* de la Ley de
  Propiedad Intelectual (arts. 133 y siguientes). Leerla de forma automática sin permiso es un
  riesgo legal, no solo un incumplimiento de contrato.

## 4. Recomendación

1. **Empezar por la PLACSP, adjudicaciones.** El proceso programado sería:
   - Leer los tres feeds: el de **perfiles cada hora** y el de agregación y el de menores
     **una vez al día, a las 03:00**. Se recorre `rel="next"` hasta volver a una
     `updated` ya procesada (se guarda un cursor por canal).
   - **Filtrar** por estado `ADJ`/`RES` con `ResultCode` 8 o 9, y por los prefijos CPV de la
     sección 1 en el proyecto o en el lote.
   - **Fecha de la señal:** `AwardDate` (o `IssueDate` si está formalizada). Se descarta lo
     anterior a 30 días, para que las reemisiones de expedientes viejos no generen señales.
   - **Identificar** la empresa por el NIF de `WinningParty`, normalizado, contra el CIF de la
     cuenta o del lead. Sin coincidencia, la señal queda pendiente de casar o crea un lead
     sugerido. **Se descartan los NIF de persona física.**
   - **Texto:** «Adjudicado “{objeto}” por {órgano}, {importe} €», con URL al `entry/link` y la
     cita «Origen de los datos: Ministerio de Hacienda».
   - Para **arrancar**, se carga una vez el zip del mes en curso.
2. **BORME en segunda fase, solo constituciones y cambios de objeto social.** Se lee el sumario
   diario de las 08:00 y se filtran por palabras clave del objeto social («limpieza», «ayuda a
   domicilio», «construcción», «audiovisual», «eventos») o por el CNAE cuando venga escrito. La
   empresa se casa por razón social normalizada. No se guardan nombres de personas.
3. **Portales de empleo: no.** Si se quieren, se pide permiso por escrito o se contrata un
   proveedor de datos con licencia.

## 5. Riesgos

- Falsos positivos de CPV: `853*` incluye residencias y `45*` cualquier obra pública. Hace falta
  una segunda capa de palabras clave en el título.
- Las licitaciones de muchos ayuntamientos están solo en plataformas autonómicas. Si la
  agregación de alguna autonomía no está completa, faltarán justo los contratos de limpieza
  y SAD.
- UTEs: el NIF es de la UTE (empieza por U), no de las empresas que la forman. Hay que casarlas
  por nombre.
- Volumen: unos 70 MB al día solo en perfiles. Hay que procesar el XML por streaming, no
  cargarlo entero en memoria.
- Aunque la publicación sea legal, el RGPD sigue aplicando a autónomos y administradores.

## 6. Sin verificar

- Condiciones de uso de InfoJobs y alcance de su API.
- La frecuencia oficial del feed de perfiles: la observada es horaria o mejor, pero la página de
  Hacienda dice «diaria».
- Cobertura real de la agregación por autonomía (solo se vio una página).
- Si el dominio antiguo `contrataciondelestado.es` dejará de servir la sindicación.
- Los CPV de SAD salen de una muestra pequeña (14 casos). Hay que confirmarlos con un mes completo.
