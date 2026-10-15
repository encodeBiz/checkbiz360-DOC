# ADR-006 — Claude prepara, la persona envía

**Fecha:** 2026-10-13
**Estado:** Propuesto
**Decisionario:** Jose Acevedo

---

## Contexto

Las notas proponen «probar automatizar Claude en LinkedIn» y «cold email». Dos riesgos:

- **LinkedIn:** sus condiciones de uso prohíben el software que automatiza la actividad o extrae
  datos de la plataforma, y el castigo habitual es restringir la cuenta. La cuenta personal de
  Jose es el activo del embudo de autoridad.
- **Email:** el art. 21 de la LSSI exige consentimiento previo para comunicaciones comerciales
  por correo, salvo relación contractual previa ([06 §D5](../06_decisiones-abiertas.md)).

## Decisión

- El CRM y el agente **no envían nada**. No hay integración de envío en `sales`.
- El agente investiga, redacta el mensaje y lo deja listo; la persona lo envía desde su cuenta y
  registra la actividad (o se la pide registrar al agente).
- LinkedIn se usa en lectura manual y para contenido propio (`marca-personal`). LinkedIn Ads
  queda fuera de este riesgo.

## Consecuencias

- El volumen lo limita la persona, no la herramienta: es lo que se quiere al principio, porque
  cada conversación enseña algo del nicho.
- Si más adelante se quiere enviar en volumen, será con un proveedor y una base legal revisados,
  y con un ADR nuevo.
