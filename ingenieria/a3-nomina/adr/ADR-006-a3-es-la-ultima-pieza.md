# ADR-006 — Se construye contra un puerto; A3 es la última pieza

**Fecha:** 2026-10-26
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

No hay sandbox de a3innuva. Para probar contra A3 hay que contratar a3innuva Nómina y
Conectia, y esa cuenta todavía no la tenemos. Tampoco hemos podido leer la documentación
técnica entera: no sabemos si la autenticación es por clave o por OAuth, ni si las
variables se mandan como cantidades o como importes.

Casi todo el valor del add-on, sin embargo, no depende de A3:

- medir bien el periodo;
- enseñarlo para que se apruebe;
- asociar personas y conceptos;
- guardar lo enviado.

## Decisión

1. **El dominio habla con A3 a través de un puerto**, `NominaExterna`, con lo mínimo:
   - probar la conexión;
   - listar empresas y empleados de la cuenta (para asociar);
   - listar los conceptos de una empresa (para asociar);
   - enviar las variables y ausencias de un periodo;
   - leer el resultado de un envío.
2. **Primero se construye todo lo demás**, con un adaptador falso que guarda lo que se
   habría enviado y devuelve respuestas configurables: éxito, rechazo de una línea, fallo
   transitorio.
3. **El adaptador de Conectia se escribe cuando haya cuenta.** Lo que descubramos se absorbe
   dentro del adaptador. Si algo obliga a cambiar el puerto, se cambia y se anota aquí.
4. **No se publica en el catálogo ni se vende** hasta que el adaptador real haya hecho un
   cierre completo contra nuestra empresa de pruebas. Se ofrece hecho, no por hacer.

## Justificación

**El riesgo está en A3, y el trabajo no.** Lo que no sabemos de la API afecta a una pieza
pequeña. Esperar a la cuenta para empezar retrasa todo lo que no depende de ella.

**El adaptador falso no se tira.** Sirve para los tests del cierre y para que QA pruebe la
pantalla sin tocar ninguna nómina real.

## Riesgo aceptado

Puede que la API obligue a cambiar algo del puerto, por ejemplo que las ausencias vayan
por otro sitio que las variables, o que un periodo calculado no admita correcciones. Se
acepta porque el puerto es pequeño y lo que hay detrás (medir, aprobar, asociar) sirve igual.
