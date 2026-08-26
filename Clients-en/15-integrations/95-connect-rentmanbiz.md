# Connecting RentmanBiz step by step

Connecting is a one-off job in five steps. Allow about ten minutes, plus however long you need to match your crew.

> **During the beta**, the Encodebiz team performs the setup from the details you provide. The self-service screen in the backoffice is in development. The steps are the same and so is the result.

## Step 1 — Get your Rentman token

The token is the key that lets CheckBiz360 talk to your Rentman account.

1. Sign in to Rentman as an administrator.
2. Go to **Configuration → Account → Integrations**.
3. Create a new API token and copy it.

The token is valid for ten years. We recommend creating it from a user dedicated to integrations rather than an employee's personal account: if that person leaves, syncing would stop.

## Step 2 — Enter the token in CheckBiz360

Paste it into the wizard. On saving, the token is encrypted: from that moment nobody — not even our team — can read it back. If you ever need to change it, you enter a new one and it replaces the old.

## Step 3 — Check the connection

Before anything is sent, the platform verifies that the token is valid and that it can read your crew. If something fails you will see the exact reason. The two usual cases:

| Message | What it usually means |
|---|---|
| Invalid token | It was copied incomplete, or revoked in Rentman |
| No access to data | The user who created the token lacks permissions |

Do not continue until this check passes.

## Step 4 — Match your crew

This is the step that deserves the most attention, and the one that decides whether someone's hours reach Rentman.

CheckBiz360 shows two lists: your employees and your Rentman crew. Matches by **email address** are proposed automatically and you confirm or correct them. The rest are matched by hand.

**An unmatched worker generates no hours in Rentman.** That is not an error: there is simply no Rentman record to post them to. Worth reviewing whenever someone new joins.

## Step 5 — Import your catalogue

With the connection tested, the platform brings in your crew, your jobs, your warehouses and the tasks for each role. Before writing anything it shows you a **preview** of what will happen, and it only runs once you confirm.

Anything arriving incomplete — people without an email, sites without coordinates — is imported flagged as pending and unable to operate, not discarded. Explained in detail in [What gets imported and what stays pending](97-import-and-pending.md).

## After connecting

From then on, every shift that closes is sent to Rentman in the next sync cycle, which runs every 15 minutes. Don't expect data instantly: if someone has just clocked out, their hours will show up in Rentman within minutes.

Shifts **before** the connection are not sent back indefinitely: syncing looks at the last seven days. If you need an older period recovered, request it from **Support**.

## Related articles

- [What integrations are](93-what-are-integrations.md)
- [Posted hours and alerts](96-posted-hours-and-alerts.md)
