# Campañas in-app — Documento de Ingeniería

**Proyecto:** encodeBiz SaaS
**Dominio:** plataforma — avisos a los usuarios del panel
**Fecha de inicio:** 2026-09-16
**Estado:** panel en `feat/campanas-inapp` del front, sin commitear · gestión (checkinbiz + backoffice) en `feat/backoffice-campanas` de la API, sin promocionar
**Autor:** Jose Acevedo

---

## Para qué

Contar a los clientes lo que sale nuevo —equipos, por ejemplo— dentro del propio panel, en el
momento en que entran, y una sola vez a cada uno. No es marketing por correo: es un diálogo con
imagen, texto y un botón que lleva a la pantalla de la novedad.

## Principio de diseño

> **Una campaña es un documento que el panel solo lee. Cada persona deja su propia marca al
> cerrarla, y esa marca es lo único que el navegador escribe.**

---

## Datos en Firestore

```
campaigns/{campaignId}
  active: boolean
  startAt: Timestamp            // desde cuándo sale
  endAt: Timestamp | null       // hasta cuándo; null, hasta que se apague
  roles: string[]               // owner | admin; vacío = todos
  image: string | null          // URL https de la cabecera
  ctaUrl: string | null         // ruta del panel ("/checkinbiz/employee?tab=teams") o https://…
  content: {
    es: { title, body, ctaText? },   // obligatorio
    en | de | fr | pt: { … }         // opcionales; si falta el del usuario, sale es
  }
  createdAt, createdBy, updatedAt, updatedBy   // procedencia; el panel los ignora

campaigns/{campaignId}/openBy/{uid}
  openedAt: Timestamp
  action: "cta" | "dismiss"
  entityId?: string
```

## Quién escribe qué

| Qué | Quién | Cómo |
|---|---|---|
| Leer campañas activas | Panel | Firestore directo, `active == true`, tope 20; fechas y rol en el navegador |
| Marca `openBy/{uid}` | Panel | Firestore directo, solo alta, al cerrar el diálogo |
| Crear y editar campañas | **checkinbiz** | `/api/v1/checkinbiz/campaigns`, solo con clave S2S |
| Permiso, auditoría y pantalla | **backoffice** | `/api/v1/backoffice/campaigns` → checkinbiz |

checkinbiz es el dueño de la colección, igual que de `user_entity_roles`: la validación de la
forma que el panel lee vive en un solo sitio. El backoffice pone lo que checkinbiz no tiene:
quién lo pide, si puede (`campaigns:write`, root y admin) y el apunte de antes y después.

## Decisiones

- **No se borran, se apagan.** Firestore no borra las subcolecciones con el documento: borrar la
  campaña dejaría `openBy` huérfano y perdería quién la vio. `active: false` y listo.
- **Editar no vuelve a avisar.** Quien ya la cerró no la verá otra vez aunque cambie el texto.
  Para volver a avisar a todos se crea una campaña nueva. La pantalla lo advierte al editar una
  campaña que ya tiene vistas.
- **El tope de 20 activas del panel es real.** La consulta no ordena por fecha: una campaña
  caducada que sigue `active: true` ocupa un hueco. El backoffice marca las caducadas y avisa
  si hay más de 20 encendidas.
- **La imagen va por URL.** No hay subida de ficheros en esta primera versión.
- **`ctaUrl` solo admite ruta del panel (`/…`) o `https://`.** Nada de `javascript:` ni `//host`.
- **Roles, solo `owner` y `admin`.** El tipo del panel declara también `member` y `viewer`, pero
  checkinbiz solo reconoce esos dos (ver `EntityMembership`): los otros no dan acceso a nada, y
  ofrecerlos sería apuntar a gente que no existe.
- **Nace apagada.** Encenderla es un gesto aparte, con confirmación en el backoffice, porque sale
  a la vez a todos los clientes que entren al panel.
- **Escribir campañas es de root y admin.** El editor las ve pero no las toca.

## Reglas de Firestore

No están versionadas; en dev siguen abiertas a todo. Antes de subir el panel a producción hay
que añadir en consola:

```
match /campaigns/{campaignId} {
  allow read: if request.auth != null;
  allow write: if false;
  match /openBy/{uid} {
    allow read, create: if request.auth != null && request.auth.uid == uid;
    allow update, delete: if false;
  }
}
```

checkinbiz escribe con el SDK de administración, que no pasa por reglas: `write: if false` no le
afecta y es lo que impide que un navegador cree o edite campañas.
