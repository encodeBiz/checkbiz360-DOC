# TDR-005 — Importación, enriquecimiento en cascada y fuentes de señales

**Fecha:** 2026-10-13
**Estado:** Boceto (Fase 4; depende de [06 §D5 y §D7](../06_decisiones-abiertas.md))

---

## 1. `POST /crm/import`

CSV UTF-8 con cabecera. Columnas:

`name*, niche*, cif, domain, cnae, employees_band, province, linkedin_url, contact_full_name,
contact_role_title, contact_email, contact_email_source, contact_linkedin_url`

(`*` obligatorias).

- **Simula por defecto**; escribe solo con `?apply=1`. Mismo principio que los scripts del repo.
- Por fila: normalizar → buscar por CIF o dominio → `create` o `link` (añade el contacto a la
  cuenta existente) → o `skipped` con motivo.
- Todo en una transacción por lote: o entra el lote o no entra nada.
- `source = import`, `stage = signal`, actor del llamante.
- `app.ts` solo monta `express.json({ limit: "64kb" })`. La ruta lleva su propio
  `express.text({ type: "text/csv", limit: "1mb" })`, montado solo en ella: subir el límite
  global abriría el endpoint público a cuerpos de 1 MB.

## 2. Enriquecimiento en cascada

> Con [ADR-005](../adr/ADR-005-el-agente-habla-con-sales-por-mcp-propio.md) el criterio es centralizar
> en CheckBiz360. Al abrir la Fase 4 se decide si estos procesos van en n8n o como tarea
> programada dentro de `sales` (como el barrido de Ads). Si van en n8n, con una clave propia
> que solo abra `POST /crm/import` y `crm/signals`, nunca `ENCODEBIZ_API_KEY`.

Un proceso por lote:

1. Entrada: empresas de un nicho exportadas de Apollo (o de la fuente que salga de `tam-icp`).
2. Por cada contacto sin email: proveedor 1 → si no hay resultado, proveedor 2 → verificación.
3. Se anota en `contact_email_source` qué proveedor lo dio.
4. Salida: el CSV de arriba contra `POST /crm/import` **sin** `apply`; la persona revisa la
   simulación y aplica.

Los proveedores concretos se eligen en la Fase 4. Criterios: tratamiento de datos en la UE o con
garantías, precio por resultado y no por intento, y verificación incluida.

## 3. Fuentes de señales

**Implementado (2026-10-13) para la PLACSP**, tras la verificación de
[07](../07_verificacion-fuentes-senales.md): `application/crm/signals/` (lector, clasificación
por CPV, ingesta con cursor por canal), script `senales-placsp` (simula salvo `--apply`) y
barrido `CRM_PLACSP_SWEEP=on` que solo escribe en cuentas existentes. Migración `033`. BORME
queda como segunda fuente; portales de empleo, descartados por sus condiciones.

Diseño original, pendiente de [06 §D7](../06_decisiones-abiertas.md): Para cada fuente que pase la verificación:
proceso programado → filtra por nicho → busca la cuenta por CIF o nombre →
`crm_add_signal` (o `crm_create_account` + señal si no existe) con `sourceUrl` y la caducidad del
tipo.
