# Diseno landing SAD CheckBiz360

Carpeta de trabajo para el prototipo de landing vertical SAD recibido desde diseno.

## Archivos principales

- `landing-sad-checkbiz360.html`: HTML de referencia editado para marketing SAD.
- `img/`: recursos visuales exportados para la landing.
- `support.js` e `image-slot.js`: runtime del prototipo de diseno. No deben portarse como codigo final de produccion.

## Estado

Base estrategica aprobable para pasar a implementacion, con estas decisiones:

- CheckBiz360 se posiciona como plataforma de ejecucion en campo para empresas SAD.
- El fichaje es el inicio, no la promesa central.
- La visita/domicilio se trata como tarea operativa verificable.
- El valor diferencial esta en cruzar jornada, visita, desplazamiento, incidencias, evidencia y coste real.
- El cumplimiento se comunica como apoyo con evidencia trazable, no como promesa legal absoluta.
- La geolocalizacion se comunica como puntual y vinculada a acciones operativas, no como vigilancia continua.

## Ajustes ya aplicados al HTML

- Anadidos `title` y `meta description`.
- Sustituido CTA roto de WhatsApp por CTAs internos de demo/valoracion.
- Reforzado el CTA final con formulario de cualificacion SAD.
- Anandidos campos ocultos `interest=checkbiz360-sad` y `source=landing-sad`.
- Ajustado copy de privacidad/cumplimiento para reducir riesgo de sobrepromesa.
- Anadido soporte basico para `prefers-reduced-motion`.
- Ajustado grid principal del hero para evitar overflow en pantallas pequenas.
- Incorporado detalle de visita con geovalla en `#como`, enlazable como `#detalle-visita`, con imagen ampliable.
- Recurso: `img/sad-detalle-tarea-geovalla.png`. Derivado del pantallazo aportado el 09/09/2026 a las 15:35, editado con imagegen integrado. Prompt: conservar interfaz, estados, horarios y aviso; anonimizar nombres y direccion; retirar etiqueta de compilacion de desarrollo.
- La captura muestra una advertencia de distancia (3,5 km frente a 75 m); el copy no infiere bloqueo del boton ni presenta ese radio como universal.

## Pendiente antes de produccion

- Conectar el formulario al endpoint real de leads.
- Definir URL real de WhatsApp o eliminar ese canal si no se va a operar.
- Revisar imagenes `sad-oficina.png` y `sad-panel.png`: aparece marca de entorno `development` en el backoffice.
- Sustituir `image-slot` por `<img>`/componente real segun el stack final.
- Revisar responsive real en navegador despues de implementarlo en el proyecto.
- Validar textos legales con politica RGPD/encargado de tratamiento antes de campanas pagadas.
