# SAD / ayuda a domicilio - GTM inicial

**Fecha:** 2026-09-08
**Estado:** nicho prioritario en investigacion
**Prioridad:** 1

## Decision

SAD, ayuda a domicilio y dependencia pasan a ser el primer nicho de investigacion
comercial para CheckBiz360.

La decision se apoya en un caso real: una auxiliar con cuadrante semanal de
visitas domiciliarias, horarios, duracion, domicilios, servicios y tiempos de
desplazamiento. El problema observado no es solo registrar jornada, sino
convertir una planilla estatica en una operacion verificable.

## Hipotesis central

Las empresas SAD necesitan demostrar que cada visita se realizo en el domicilio
correcto, dentro del horario previsto, con el servicio adecuado y con incidencias
registradas cuando algo falla.

CheckBiz360 puede posicionarse como la capa de control operativo del servicio:

> Del cuadrante semanal al seguimiento real de cada visita.

## Dolor operativo

- Muchas auxiliares trabajan solas y distribuidas en domicilios distintos.
- La coordinacion depende de cuadrantes, llamadas, WhatsApp o partes manuales.
- El cuadrante en papel o PDF obliga a la auxiliar a interpretar la ruta,
  horarios, domicilios y cambios sin una guia operativa dentro de la app.
- Parte de la plantilla puede tener baja tolerancia tecnologica, por edad,
  habito o falta de formacion digital. El producto debe reducir pasos, no anadir
  carga.
- Un retraso, ausencia o cambio de domicilio impacta sobre personas vulnerables.
- La empresa necesita justificar servicio ante familias, administracion publica o
  cliente privado.
- La direccion necesita saber si el servicio se hizo, no solo si habia una
  planificacion.

## Encaje de CheckBiz360

| Necesidad SAD | Encaje CheckBiz360 |
|---|---|
| Confirmar llegada y salida en domicilio | Fichaje movil con ubicacion puntual |
| Controlar servicios por dia | Tareas o bloques operativos asociados a visitas |
| Eliminar papel para la auxiliar | Cuadrante listo para operar dentro de la app |
| Reducir friccion tecnologica | Flujo simple: ver visita, llegar, fichar, cerrar o reportar incidencia |
| Registrar problemas en el domicilio | Incidencias con historial y responsable |
| Demostrar servicio realizado | Timestamp, ubicacion, estado y trazabilidad |
| Coordinar auxiliares distribuidas | App movil, notificaciones y panel de gestion |
| Justificar jornada laboral | Informe horario y trazabilidad de correcciones |
| Gestionar documentacion laboral | Documentos con acuse de recibo |

## Insight de usuario final

Fuente: caso real de auxiliar SAD en prueba inicial.

**Confianza:** baja-media. Es un caso real y muy relevante, pero todavia debe
validarse con mas empresas y auxiliares.

Insight:

> El valor no es pedirle a la auxiliar que "use una app". El valor es darle el
> cuadrante ya preparado y convertir cada visita en una accion sencilla:
> llegar, fichar con ubicacion puntual, saber que toca hacer y cerrar la visita.

Implicacion para producto y marketing:

- El GPS no debe venderse como vigilancia. Debe venderse como evidencia puntual
  de servicio realizado en el domicilio correcto.
- El mensaje no debe sonar a control laboral agresivo. Debe sonar a menos papel,
  menos llamadas, menos dudas y mas proteccion para empresa, auxiliar y usuario.
- Para auxiliares con poca soltura digital, la promesa operativa es: "abre la
  app y tienes tu dia listo".
- Para coordinacion, la promesa es: "ves que esta pasando sin perseguir por
  WhatsApp".

## Competencia observada

El nicho ya tiene proveedores verticales, lo que confirma que existe dolor y
presupuesto. La competencia no invalida el nicho; obliga a entrar con una cuña
clara, no con una suite generica.

| Competidor / categoria | Senal relevante | Fuente |
|---|---|---|
| Gesad | Habla de planificacion compleja, control de presencia, hora exacta de inicio/fin en domicilio e incidencias en tiempo real | https://gesad.trevenque.es/funcionalidades/control-de-presencia/ |
| Politeia Soft SAD | Suite integral para ayuntamientos y entidades prestadoras: ciudadanos, auxiliares, horarios, cuadrantes, incidencias, fichaje y facturacion | https://politeiasoft.com/sad |
| IxisSocialGest | Gestiona visitas, horas, expediente, seguimiento en domicilio y facturacion | https://www.ixissocialgest.com/software-ayuda-a-domicilio |
| CIBERSAD | Gestion SAD con planificacion, control de asistencia, puntualidad, intensidad, comunicacion e incidencias | https://cigesoc.es/cibersad/ |
| Ekippo | Software para fichajes en remoto orientado a sociosanitario, limpieza, seguridad y mantenimiento | https://ekippo.es/ |

## Dolores SAD ampliados

| Dolor / oportunidad | Valor potencial | Estado |
|---|---|---|
| Validacion de visita en domicilio | Evitar fichajes en transito o fuera del domicilio previsto mediante ubicacion puntual/geocerca | Promesa valida si se formula como verificacion de ubicacion en el fichaje; revisar si el producto bloquea o solo marca fallo |
| Cuadrante listo para operar | Reducir papel, PDF, llamadas y dudas de auxiliares con baja friccion digital | Alta prioridad; sale del caso real de auxiliar SAD |
| Trazabilidad de cuidados e incidencias | Registrar tareas realizadas, observaciones e incidencias por visita | Promesa fuerte, pero limitar datos sensibles en V1 |
| Cruce jornada vs visita/tarea | Diferenciar tiempo laboral total de tiempo efectivo en domicilio y desplazamientos entre servicios | Alta prioridad; permite detectar tiempos de desplazamiento mal calculados, visitas que se alargan y desviaciones de coste |
| Respaldo ante familias y auditorias | Evidencia de visita, hora, ubicacion puntual, estado e incidencia | Fuerte, siempre que se evite prometer auditoria sanitaria completa |
| Cumplimiento frente a Administracion | Registros trazables e informes de horas efectivas para justificar servicio | Complementario; no abrir la landing con licitaciones ni administracion publica |
| Coordinacion sin WhatsApp | Saber que visitas estan iniciadas, cerradas o con incidencia sin perseguir a cada auxiliar | Alta prioridad para coordinacion SAD |

## Diferenciacion frente a verticales SAD

La competencia vertical fuerte no es una amenaza menor. Gesad, IxisSocialGest,
Progisap y soluciones similares ya hablan de planificacion SAD, control de
presencia, expediente, rutas, incidencias, facturacion, copagos o administracion
publica.

Por tanto, CheckBiz360 no debe posicionarse como "ERP SAD completo" en esta
fase.

La diferenciacion defendible es:

> Capa ligera de control operativo para convertir cuadrantes y visitas en
> evidencia verificable, sin sustituir de golpe el sistema SAD que ya use la
> empresa.

### Donde NO competir de frente

- Expediente social completo del usuario.
- Baremos de dependencia.
- Copagos.
- Facturacion publica especifica de SAD.
- Optimizacion avanzada de rutas por proximidad.
- Gestion integral de licitaciones o pliegos.

### Donde si competir

- Cuadrante operativo en app.
- Fichaje con ubicacion puntual en el domicilio.
- Estado real de visita: pendiente, iniciada, completada, incidencia.
- Tareas/checklists por servicio.
- Cruce entre inicio/fin de jornada e inicio/fin de cada visita.
- Evidencia simple para coordinacion.
- Registro horario trazable.
- Implantacion mas rapida y menos pesada que un ERP vertical.
- Capa encima de herramientas existentes.

## Cruce jornada-visita como diferenciador

En SAD, la jornada laboral y la visita al domicilio no son lo mismo. Una auxiliar
puede empezar jornada, desplazarse, entrar en una vivienda, cerrar el servicio y
volver a desplazarse. Si solo se mide la jornada, se pierde el dato que explica
el coste real.

CheckBiz360 puede aportar valor cruzando:

- inicio y fin de jornada;
- inicio y fin de cada tarea/visita;
- domicilio o centro asociado a la visita;
- tiempo previsto vs tiempo real;
- desplazamiento entre visitas;
- incidencias o tareas no cerradas.

Esto permite detectar preguntas de negocio muy concretas:

- Si se esta dando demasiado poco tiempo de desplazamiento entre domicilios.
- Si una visita se alarga de forma recurrente.
- Si hay auxiliares con desviaciones sistematicas que requieren apoyo,
  formacion o revision de rutas.
- Si el coste real por usuario, zona o servicio no coincide con lo planificado.
- Si el problema esta en la planificacion, en la ejecucion o en una incidencia
  recurrente.

Modelo correcto para SAD:

- La jornada marca inicio y fin laboral segun contrato, convenio y horario
  aplicable.
- Las tareas representan domicilios/servicios concretos.
- Cada tarea puede tener ubicacion, hora prevista, inicio, cierre, notas,
  evidencia e incidencia.
- El cruce entre jornada y tareas muestra tiempo laboral total, tiempo efectivo
  de servicio y tiempo de desplazamiento o espera.

El lenguaje comercial debe evitar acusar al trabajador. No se vende como "pillar
a auxiliares", sino como:

> Saber si el servicio planificado es viable y donde se esta perdiendo margen.

Casos de uso de evidencia:

- Usuario ausente o que no permite realizar el servicio.
- Parte firmado o documento autorizado como constancia.
- Foto de salida o evidencia asociada al cierre de la tarea.
- Incidencia en domicilio.
- Solicitud del usuario o familiar de una tarea no permitida por la empresa,
  como subirse a una escalera o realizar una actuacion fuera de protocolo.

Estas evidencias deben tratarse con cuidado: no convertir la landing en una
promesa de gestion sanitaria ni de subida libre de datos sensibles. El mensaje
correcto es evidencia operativa controlada, con permisos, trazabilidad y reglas
de privacidad.

## Riesgos criticos antes de landing y venta

| Riesgo | Por que importa | Decision de marketing |
|---|---|---|
| RGPD y datos de salud/dependencia | Fotos de recetas, caidas o situaciones personales pueden ser datos especialmente protegidos | No prometer fotos sanitarias ni historias clinicas. En V1 hablar de incidencias operativas, notas y evidencia controlada |
| Encargado del tratamiento | CheckBiz360 procesaria datos siguiendo instrucciones de la empresa SAD | Preparar discurso de contrato de encargado, hosting UE, medidas de seguridad y roles de acceso antes de cerrar pilotos |
| BYOD y geolocalizacion | Si el movil es personal, el GPS puede percibirse como vigilancia | Repetir: no hay seguimiento continuo; solo ubicacion puntual en fichaje o accion operativa |
| Geocerca estricta | "No permitir iniciar servicio si no esta en domicilio" es potente, pero debe coincidir con el comportamiento real del producto | Validar tecnicamente si se bloquea, se alerta o se marca como fallo antes de escribirlo en landing |
| Adopcion por auxiliares | Si la app exige demasiados pasos, fracasa aunque guste a direccion | Mensaje y demo deben demostrar simplicidad: abrir app, ver visita, fichar, cerrar/incidir |
| Cumplimiento fuera de oficina | La normativa es mas dificil de cumplir cuando el trabajo ocurre en domicilios, sin supervisor presencial y con evidencias dispersas | Tratarlo como plus fuerte: cumplimiento con evidencia de campo, no como gancho generico de control horario |
| Competidores verticales | Tienen funciones SAD profundas | Posicionarnos como capa operativa rapida, no como reemplazo total |

## Promesas permitidas vs promesas prohibidas

| Tipo | Copy permitido | Evitar |
|---|---|---|
| GPS | "Ubicacion puntual en el momento del fichaje" | "Seguimiento en tiempo real de cada auxiliar" |
| Visitas | "Verifica llegada y salida asociadas al domicilio/servicio" | "Garantizamos que nunca habra desvios de ruta" |
| Incidencias | "Registra incidencias operativas con notas/evidencias controladas" | "Gestiona datos sanitarios sin revisar RGPD" |
| Administracion | "Informes trazables para justificar horas y servicio" | "Cumple automaticamente cualquier pliego SAD" |
| Competencia | "No sustituye tu ERP SAD; completa la operacion real" | "El ERP SAD definitivo" |

## Mercado y alcance en Espana

La primera lectura nacional indica que SAD si merece investigacion prioritaria:

- El mercado espanol de servicios asistenciales a domicilio alcanzo 2.650 M EUR
  en 2024, segun DBK.
- El segmento de ayuda a domicilio represento 2.410 M EUR en 2024.
- Hubo alrededor de 656.000 usuarios de ayuda a domicilio en 2024.
- El mercado crecio un 10,2% en valor en 2024.
- Los cinco primeros operadores concentran cerca del 48,8% del mercado y los
  diez primeros alrededor del 60,5%.
- Coexisten grandes operadores con contratos publicos y muchas empresas pequenas
  o regionales.
- Madrid muestra gasto publico muy alto: el Ayuntamiento aprobo un contrato SAD
  de 677 M EUR y la Comunidad de Madrid formalizo lotes por zonas con importes
  de decenas de millones.

### Lectura estrategica

Hay dos mercados distintos:

1. **Grandes adjudicatarias publicas.** Alto volumen, procesos lentos, venta mas
   institucional, posible necesidad de integraciones y cumplimiento de pliegos.
2. **Empresas privadas y regionales acreditadas.** Menor barrera de entrada,
   contacto mas directo, mas adecuadas para demos presenciales y pilotos.

La primera entrada comercial debe priorizar empresas privadas/regionales y
entidades acreditadas con operacion real de auxiliares. Los grandes operadores
sirven para entender estandar de mercado, lenguaje, pliegos y requisitos, pero
no son el primer objetivo de venta salvo que exista contacto directo.

## Cuña estrategica

No competir de entrada como "software integral SAD" contra suites grandes con
expediente social, copago, licitaciones y facturacion publica.

Competir como:

> Control operativo verificable para auxiliares en domicilio.

El mensaje debe centrarse en el tramo donde CheckBiz360 es fuerte:

- presencia real;
- hora real;
- domicilio correcto;
- incidencias;
- tareas;
- trazabilidad;
- cumplimiento horario;
- supervision sin perseguir por WhatsApp.

## Compradores probables

| Rol | Que le duele | Mensaje |
|---|---|---|
| Gerencia / direccion | Margen, reclamaciones, control del servicio, riesgo reputacional | Saber que cada servicio se hizo y poder demostrarlo |
| Coordinacion SAD | Cambios diarios, ausencias, retrasos, llamadas, incidencias | Ver el estado de las visitas sin perseguir a cada auxiliar |
| RRHH / administracion | Jornada, correcciones, documentacion, cumplimiento | Registros trazables y exportables |
| Responsable de calidad | Evidencia de servicio, incidencias, seguimiento | Historial verificable por visita y trabajador |

## Demo vertical

La demo debe partir de una planilla semanal real y mostrar el antes/despues:

1. Antes: PDF/cuadrante con dias, horas, domicilios, usuario y servicio.
2. Despues: cada visita aparece como accion operativa en CheckBiz360.
3. La auxiliar abre la app y ve su dia listo, sin papel.
4. Ficha llegada en el domicilio con ubicacion puntual.
5. Ve el servicio previsto y registra salida o incidencia.
6. Coordinacion ve cumplimiento y problemas sin llamar una por una.
7. Direccion consulta trazabilidad e informes.

La demo no debe empezar por "cumplimos RDL 8/2019". Eso entra al final como
respaldo legal.

## Preguntas de investigacion

- Como generan hoy los cuadrantes.
- Que software usan para SAD, si usan alguno.
- Como verifican que la auxiliar llego al domicilio.
- Si la auxiliar recibe papel, PDF, WhatsApp, Excel o app.
- Que parte del proceso le cuesta mas a la auxiliar en el dia a dia.
- Que resistencia tienen las auxiliares a usar una app y por que.
- Si el GPS se percibe como ayuda operativa, control, obligacion del cliente o
  requisito administrativo.
- Como gestionan retrasos, bajas, cambios y usuarios ausentes.
- Como justifican servicio ante administracion, familia o cliente privado.
- Que datos necesita coordinacion en tiempo real.
- Que parte del proceso sigue en papel, Excel o WhatsApp.
- Que integraciones serian imprescindibles para no duplicar trabajo.

## Criterios para prospectos

Prospecto caliente:

- Empresa SAD privada o entidad prestadora.
- 20 o mas auxiliares.
- Operacion en varios barrios, municipios o zonas.
- Usa cuadrantes manuales, PDF, Excel o gestion parcial.
- Tiene coordinador/a SAD identificable.
- Puede aceptar demo presencial o piloto.

Descartar de inicio:

- Cuidadores particulares sin estructura empresarial.
- Empresas sin empleados propios.
- Entidades que solo buscan un software integral de expediente social y
  facturacion publica si no hay dolor de control operativo.
- Zonas donde la conectividad impida fichaje movil y no acepten correccion
  manual.

## Objetivos iniciales

1. Identificar 30 empresas SAD en Madrid y alrededores.
2. Priorizar 10 con mayor probabilidad de demo presencial.
3. Conseguir 3 conversaciones exploratorias.
4. Conseguir 1 demo presencial basada en cuadrante real.
5. Validar si la cuña "del cuadrante al seguimiento real" despierta interes.

## Siguiente paso

Construir una lista corta de prospectos SAD en Madrid con:

- nombre de empresa;
- zona;
- web;
- telefono publico;
- email publico;
- responsable si aparece en fuente publica;
- senal de encaje;
- fuente;
- prioridad de contacto.

## Registro oficial Madrid - lectura inicial

Fuente base: Registro de servicios de atencion social de la Comunidad de Madrid,
dataset publico actualizado el 2026-09-01.

Extraccion realizada el 2026-09-08:

- 323 servicios registrados como `SERVICIO DE AYUDA A DOMICILIO`.
- 194 entidades unicas deduplicando por NIF o denominacion.
- 147 entidades privadas con animo de lucro.
- 46 entidades privadas sin animo de lucro.
- 68 entidades aparecen como `PRIVADA + PEVS`.
- 125 entidades aparecen como `PRIVADA TOTAL`.
- 207 servicios SAD estan en Madrid capital.

### Lectura comercial

Madrid confirma volumen suficiente para una primera validacion sin salir de la
Comunidad Autonoma.

La prioridad no debe ser empezar por las grandes adjudicatarias, aunque muevan
mucho volumen. Para una primera venta o piloto, el mejor subsegmento son
empresas privadas acreditadas con PEVS, contacto publico, varios servicios
registrados y operacion de auxiliares distribuida.

### Segmentacion operativa Madrid

| Segmento | Senal | Uso comercial |
|---|---|---|
| Privada + PEVS | Empresa acreditada para Cheque Servicio o prestacion vinculada | Prioridad A para demos y pilotos |
| Privada total | Operacion privada sin PEVS visible | Prioridad B si tiene volumen o dolor operativo claro |
| Grandes adjudicatarias | Muchos contratos, licitaciones y estructura corporativa | No primer ataque salvo contacto directo |
| Asociaciones / sin animo de lucro | Operacion real, posible menor capacidad de compra | Buenas para entrevistas de dolor, no siempre venta rapida |

## Hipotesis de ataque Madrid v0

1. Empezar con 20-30 empresas privadas acreditadas.
2. Validar por telefono si gestionan cuadrantes, visitas, incidencias y fichajes
   con herramientas separadas.
3. Intentar 3 entrevistas exploratorias antes de cambiar la landing.
4. Convertir el cuadrante real SAD en una demo vertical.
5. Si la respuesta es positiva, crear landing especifica SAD y campana separada.
