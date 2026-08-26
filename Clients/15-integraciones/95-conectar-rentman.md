# Conectar RentmanBiz paso a paso

La conexión se hace una sola vez y consta de cuatro pasos. Calcule unos diez minutos, más el tiempo que necesite para emparejar a su plantilla.

> **Durante la fase beta**, la activación la realiza el equipo de Encodebiz a partir de los datos que usted facilite. La pantalla de autoservicio en el backoffice está en desarrollo. Los pasos son los mismos y el resultado también.

## Paso 1 — Obtener su token de Rentman

El token es la llave que permite a CheckBiz360 hablar con su cuenta de Rentman.

1. Entre en Rentman con un usuario administrador.
2. Vaya a **Configuration → Account → Integrations**.
3. Cree un nuevo token de API y cópielo.

El token tiene una validez de diez años. Le recomendamos crearlo desde un usuario dedicado a integraciones y no desde la cuenta personal de un empleado: si esa persona se marcha, la sincronización dejaría de funcionar.

## Paso 2 — Introducir el token en CheckBiz360

Peguelo en el asistente de la integración. Al guardarlo, el token se cifra: a partir de ese momento nadie —tampoco nuestro equipo— puede volver a leerlo. Si algún día necesita cambiarlo, se introduce uno nuevo y sustituye al anterior.

## Paso 3 — Comprobar la conexión

Antes de enviar nada, la plataforma verifica que el token es válido y que puede leer su plantilla de Rentman. Si algo falla, verá el motivo exacto. Los dos casos habituales son:

| Mensaje | Qué suele significar |
|---|---|
| Token no válido | Se copió incompleto o se ha revocado en Rentman |
| Sin acceso a los datos | El usuario que creó el token no tiene permisos suficientes |

No continúe hasta que esta comprobación sea correcta.

## Paso 4 — Emparejar a sus trabajadores

Este es el paso que más atención requiere, y el que determina si las horas de una persona llegarán a Rentman o no.

CheckBiz360 le mostrará dos listas: sus empleados y los *crew members* de Rentman. La plataforma le propondrá automáticamente las parejas cuyo **correo electrónico coincide**, y usted confirma o corrige. El resto se empareja a mano.

**Un trabajador sin emparejar no genera horas en Rentman.** No es un error ni un fallo de la integración: simplemente no hay ninguna ficha de Rentman a la que imputarlas. Por eso conviene revisar la cobertura del emparejamiento cada vez que entre alguien nuevo en la empresa.

## Paso 5 — Importar su catálogo

Con la conexión probada, la plataforma trae de Rentman su plantilla, sus montajes, sus almacenes y las tareas de cada función. Antes de escribir nada le enseña una **vista previa** con lo que va a ocurrir, y solo se ejecuta cuando usted lo confirma.

Lo que llegue incompleto —gente sin correo, centros sin coordenadas— se importa marcado como pendiente y sin poder operar, no se descarta. Está explicado en detalle en [Qué se importa y qué queda pendiente](97-importacion-y-pendientes.md).

## Después de conectar

A partir de ese momento, cada jornada que se cierre se enviará a Rentman en el siguiente ciclo de sincronización, que se ejecuta cada 15 minutos. No espere ver los datos al instante: si un trabajador acaba de fichar la salida, sus horas aparecerán en Rentman en los próximos minutos.

Las jornadas **anteriores** a la conexión no se envían hacia atrás de forma indefinida: la sincronización revisa los últimos siete días. Si necesita recuperar un periodo más antiguo, solicítelo desde **Soporte**.

## Artículos relacionados

- [Qué son las integraciones](93-que-son-las-integraciones.md)
- [Horas imputadas y avisos](96-horas-imputadas-y-avisos.md)
