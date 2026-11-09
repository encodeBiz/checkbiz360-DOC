# Nómina en a3innuva (Conectia) — Documento de Ingeniería

**Proyecto:** encodebiz-api
**Dominio:** add-on de integración con a3innuva Nómina (Wolters Kluwer) por su API, Conectia
**Fecha de inicio:** 2026-10-26
**Estado:** Diseño propuesto. **Sin cuenta de A3 todavía**: lo que depende de ver la API está
marcado *a confirmar con la cuenta* y se cierra el día que la tengamos.
**Autor:** Jose Acevedo

---

## Contexto y motivación

Un cliente que lleva su nómina en a3innuva (él mismo, sin gestoría en medio) pidió que
CheckBiz se conecte. Hoy, a fin de mes, alguien coge las horas, las horas extra, las
vacaciones y los permisos y los vuelve a teclear en A3. Es trabajo repetido, se equivoca, y
lo que se paga deja de coincidir con lo que se fichó.

La competencia ya lo hace (Factorial, Woffu, HRLOG y netTime están en el a3Marketplace), así
que para vender control horario a empresas con A3 es casi un mínimo. Pero donde más valor
tiene es en las **empresas de servicios que pagan por horas**: la misma hora fichada sirve
para pagar la nómina y para saber cuánto cuesta de verdad cada servicio.

Lo que confirmó a3Developers por correo (octubre de 2026):

- No hay sandbox ni entorno de partner. Para desarrollar hay que **contratar a3innuva Nómina
  y Conectia** y crear una empresa de pruebas.
- El token se obtiene según la documentación de a3developers (no se ha podido leer entera).
- La certificación y la entrada en el a3Marketplace se tratan con el comercial al contratar
  Conectia.

## Principio de diseño

> **CheckBiz prepara, A3 calcula. Mandamos hechos medidos y aprobados por una persona; la
> nómina, los importes y la tributación son de A3.**

## Modelo de negocio (decidido por Jose, 2026-10-26)

- El cliente paga su a3innuva. **Conectia lo asumimos nosotros** y lo cobramos dentro de una
  cuota de **20–25 € al mes por empresa**. Conectia se anuncia desde unos 13,5 €/mes; la tarifa
  real, a confirmar con el comercial.
- **Nuestra cuenta de A3 es para desarrollar, probar y enseñar.** No gestiona las empresas de
  los clientes: cada cliente conecta **su** cuenta de a3innuva. Si Wolters Kluwer no deja que
  un partner contrate Conectia en nombre del cliente, lo contrata el cliente y se lo
  descontamos de la cuota; la cuenta sale igual.
- Se ofrece **hecho**, no por hacer: no se vende hasta que funcione contra nuestra cuenta.

## Decisiones

| Documento | Estado |
|---|---|
| [ADR-001 — CheckBiz prepara, A3 calcula](./adr/ADR-001-checkbiz-prepara-a3-calcula.md) | Propuesto |
| [ADR-002 — Se envía el cierre aprobado, no cada fichaje](./adr/ADR-002-se-envia-el-cierre-aprobado.md) | Propuesto |
| [ADR-003 — Unidades, no euros; conceptos por empresa](./adr/ADR-003-unidades-no-euros.md) | Propuesto |
| [ADR-004 — El exceso lo mide CheckBiz; la hora extra la decide una persona](./adr/ADR-004-la-hora-extra-la-decide-una-persona.md) | Propuesto |
| [ADR-005 — Cada línea enviada sabe de dónde sale](./adr/ADR-005-cada-linea-sabe-de-donde-sale.md) | Propuesto |
| [ADR-006 — Se construye contra un puerto; A3 es la última pieza](./adr/ADR-006-a3-es-la-ultima-pieza.md) | Propuesto |
| [TDR-001 — Servicio, conexión y datos propios](./tdr/TDR-001-servicio-y-conexion.md) | Diseño propuesto |
| [TDR-002 — El cierre del periodo](./tdr/TDR-002-el-cierre-del-periodo.md) | Diseño propuesto |
| [TDR-003 — Correspondencias de personas y conceptos](./tdr/TDR-003-correspondencias.md) | Diseño propuesto |

## Alcance

**Fase 1 — lo que se puede construir ya, sin cuenta:**

- el servicio y su conexión;
- el cálculo del cierre del periodo desde lo que CheckBiz ya mide (horas, nocturnas, festivos
  trabajados, exceso sobre lo previsto, vacaciones y permisos);
- la vista previa, la aprobación, las correspondencias de personas y conceptos y el registro
  de envíos.

Todo ello detrás de un puerto `NominaExterna` con un adaptador falso que guarda lo que *se
habría enviado* (ADR-006).

**Fase 2 — con la cuenta:** el adaptador real de Conectia, la prueba completa contra la
empresa de pruebas, la ficha del catálogo y el piloto con el cliente (configurar sus
conceptos y validar su primer cierre).

**Fase 3 — después:**

- leer de A3 empleados y contratos: altas sin teclear dos veces, y coste por hora con el
  contrato real;
- conceptos variables (dietas, kilometraje, pluses), que pide el caso VTC;
- certificación y entrada en el a3Marketplace.

**Fuera, y explícitamente:**

- un motor de nómina propio (ADR-001);
- mandar importes en euros por conceptos que tienen precio en A3 (ADR-003);
- enviar nada sin que una persona lo apruebe (ADR-002);
- tocar el núcleo de CheckBiz para acomodar a A3 (regla de oro de
  [`integraciones/`](../integraciones/README.md)).

## Lo que ya existe y se reutiliza

| Pieza | Dónde | Para qué sirve aquí |
|---|---|---|
| Jornada diaria por persona | Postgres `employee_daily_reports` (`services/reports/src/application/BuildEmployeeDailyReports.ts`, 02:30 UTC) | Fuente de las horas. Es la **misma tabla que el informe legal de jornada** (`GenerateReportPDF.ts`): nómina e informe no pueden discrepar |
| Horario previsto | `checklogs_raw.schedule_applied`; `dim_calendars` / `dim_calendar_days` | Contra qué se mide el exceso (ADR-004) |
| Festivos y ausencias | `dim_calendars.holidays` / `.absences`; Firestore `entities/{e}/absence_requests` (`packages/shared/src/calendar/absenceRequests.ts`) | Vacaciones, permisos y festivos trabajados |
| Retribuida o no | `Holiday.paid` y `absence_requests.paid` ([disponibilidad ADR-004](../disponibilidad/adr/ADR-004-ausencias-retribuidas.md)) | Separar permiso retribuido de no retribuido; «no consta» no se envía |
| Validación de jornadas manuales | `CheckLog.status = pending-employee-validation` | Una jornada sin validar bloquea el cierre de esa persona |
| Identidad fiscal | `Employee.nationalId`, `Branch.nif`, `Entity.taxId` | Emparejar personas y empresas con A3 |
| Contrato de add-on | [`integraciones/contrato-activacion.md`](../integraciones/contrato-activacion.md) | Catálogo, activar/conectar, credencial cifrada con `ENC_KEY` |
| Patrón de envío | `services/rentman` (`rentman_time_registration`, huella `pushed_hash`, `rentman_sync_log`) | Idempotencia por huella y registro de lo enviado |

**Lo que no existe y este diseño tiene que crear:**

- horas extra por persona (hoy solo hay una aproximación por sucursal en `FetchCheckbizStats.extraHours`);
- horas nocturnas;
- festivos trabajados;
- cierre de mes o bloqueo de periodo;
- NSS y número de empleado;
- conceptos de dietas o kilometraje.

## Lo que hay que verificar con la cuenta

1. **Autenticación:** ¿clave de suscripción (`Ocp-Apim-Subscription-Key`) por cliente, OAuth,
   o las dos? ¿Puede un cliente autorizar a una aplicación de terceros sin darle su clave?
2. **Escritura de variables:** ¿se mandan cantidades por concepto, importes o las dos cosas?
   ¿Qué tipos de concepto se pueden escribir?
3. **Ausencias:** ¿qué tipos se pueden escribir? Por lo publicado: vacaciones, permisos
   retribuidos y bajas con campos propios. ¿Se solapa con las bajas que A3 ya recibe por
   el sistema RED?
4. **Periodos:** ¿se puede reescribir un periodo ya enviado? ¿Y uno ya calculado? ¿Cómo se
   corrige después?
5. **Identificadores:** ¿se empareja por NIF o por código de empleado? ¿Cómo se identifica
   cada empresa y centro (CCC) dentro de una cuenta?
6. **Límites:** cuotas de llamadas y precio de Conectia por volumen.
7. **Disparar el cálculo:** ¿se puede lanzar el cálculo de la nómina por API? Solo como
   comodidad: no cambia ADR-001.
8. **Importación sin API:** ¿importa a3innuva las incidencias desde un Excel? Si es así, la
   vista previa del cierre sirve como entregable antes de tener la API. Sin comprobar.
