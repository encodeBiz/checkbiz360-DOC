# Aceptación de los textos legales con prueba

**Abierto:** 2026-11-04 · **Estado:** en desarrollo (panel, rama `feat/aceptacion-legal`)

## El problema

El registro del panel tiene una casilla obligatoria de «acepto los términos y la política de
privacidad», pero no sirve como prueba: no se guarda quién la marcó, cuándo ni qué versión del
texto aceptó. Quien entra con Google no la ve nunca, y la ficha se crea con «aceptó» puesto a
mano. La política que enlaza es la de la web (cookies y formulario de contacto), no la de la
plataforma. Y el contrato de encargo del tratamiento (art. 28 RGPD), que es el documento que la
AEPD pide primero a un proveedor como nosotros, no existe todavía.

Este diseño cubre la **mecánica**: registrar la aceptación con prueba en todos los caminos de
alta y poder exigirla a quien ya está. Los **textos** (contrato de encargo y política de
privacidad de la plataforma en castellano) los pone el abogado; cuando lleguen, se publican y se
sube el número de versión.

## Qué se guarda

Colección `legal_acceptances`, solo de añadir, escrita únicamente desde el servidor del panel
(rutas `/api/...` con el Admin SDK). Un documento por aceptación:

| Campo | Qué es |
|---|---|
| `uid`, `email` | quién aceptó |
| `entityId` | la empresa a la que vincula, o `null` si es la aceptación personal del alta |
| `docs` | `{ terms: "2026-11-04", privacy: "2026-11-04", dpa?: "…" }`: qué versión de cada texto |
| `acceptedAt` | fecha y hora del servidor |
| `ip`, `userAgent`, `locale` | desde dónde y en qué idioma |
| `source` | `register`, `complete_profile`, `entity_create` o `panel_gate` |

Y un resumen para leer rápido, que también escribe solo el servidor:

- `entities/{id}.legalAcceptance = { terms: {version, acceptedAt, uid}, privacy: …, dpa?: …, acceptanceId }`
- `users/{uid}.legalAcceptance = { … }` para la aceptación personal del alta.

Las versiones viven en `src/config/legal.ts` (`LEGAL_DOCS`), una fecha por documento. El
servidor pone las versiones; el navegador nunca las manda. Un cambio de texto = subir la fecha.

## Los cuatro caminos

1. **Alta con correo** (`/api/auth/register`). El servidor exige `acceptTerms === true` (hoy solo
   lo comprobaba el navegador) y, tras crear la cuenta, escribe la aceptación personal. Si no
   puede escribirla, el alta falla y la cuenta se deshace: no queremos cuentas sin prueba.
2. **Alta con Google** (`/main/user/complete-profile`). Gana la misma casilla que el alta con
   correo, obligatoria; al guardar el perfil se llama a `/api/legal/accept` sin empresa.
3. **Crear empresa** (`/main/core/entity/create`). Casilla «acepto en nombre de la empresa»
   con los términos, la política y, cuando exista, el contrato de encargo. Al volver el id, se
   llama a `/api/legal/accept` con `entityId`. Es el momento legalmente bueno: la empresa ya
   tiene razón social y CIF.
4. **Quien ya está** (`LegalGateModal`, montado en `AdminLayout` junto al de 2FA). Si la empresa
   actual no tiene aceptadas las versiones vigentes y quien entra es `owner` o `admin`, una
   ventana que no se cierra: enlaces a los textos, casilla y botón. Un `member` o `viewer` no la
   ve: no puede obligar a la empresa. La ventana solo se activa con
   `LEGAL_DOCS.gateEnabled = true`; hasta que el abogado entregue los textos queda apagada y
   las altas nuevas van registrando aceptaciones desde el primer día.

## La ruta `/api/legal/accept`

`POST`, `Authorization: Bearer <idToken>`, cuerpo `{ entityId?: string, source }`. Verifica el
token; con `entityId`, comprueba en `user_entity_roles` que el usuario es `owner` o `admin` de
esa empresa y está activo. Escribe el documento de `legal_acceptances` y el resumen. Devuelve
el resumen.

## Reglas de Firestore

Hechas y probadas con el emulador (once casos, `feat/reglas-legal-acceptances` en el repo de la
API): `legal_acceptances` entra en `cerradas()` y `noTocaLegalAcceptance()` impide que desde el
navegador se cree, cambie o quite `legalAcceptance` en `entities/{e}` y en `users/{uid}`; todo
lo demás sigue igual. Ojo con el `updateMask`: un campo en la máscara sin valor lo borra, y la
primera versión de la regla lo dejaba pasar. Desplegadas en `dev-encodebiz` el 2026-11-04;
producción, en el próximo pase.

## Fuera de este diseño, para después

- **Copia para el cliente:** botón «Descargar contrato de encargo» que genere un PDF con el
  texto y el registro de aceptación, firmado con el servicio documental.
- **Modelo de cláusula informativa para empleados** descargable desde el panel, para que el
  paso 4 del correo de alta no se quede en «infórmales».
- **Registro de actividades de tratamiento** e inventario de subencargados: en
  `DOCS/ingenieria/proteccion-de-datos/`.
