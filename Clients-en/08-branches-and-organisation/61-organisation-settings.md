# Organisation configuration

The organisation is CheckBiz360's top organisational level: it represents the company that has contracted the service and encompasses branches, employees and data. What is configured here acts as the reference for the whole structure.

It is reached from **Organisation** in the side menu, and the screen is organised into six tabs.

---

## The six tabs

| Tab | What it contains |
|---|---|
| **Company details** | Trading name, primary language, legal name, tax ID, billing email and address |
| **Workspace** | What things are called in your organisation: for example, whether your sites are called *Branch*, *Project* or *Site* |
| **Billing setup** | The account's payment methods |
| **Subscriptions** | The plan contracted and its status |
| **Invoices** | Billing history |
| **Collaborators** | Users with access to this organisation's back office |

**Company details** and **Billing setup** show a visual warning while they are incomplete. It is not decorative: **without a legal name and a payment method you cannot subscribe to a plan**.

---

## Workspace

It used to be called *Visual identity*. It no longer configures colours or images: it is used to adapt the name of the workplaces to your organisation's vocabulary. If your sites are projects or building sites, the back office will say so in the menu, in the lists and in the records —for example, "Site details"—. Leaving the field blank uses the default name.

---

## Collaborators

Collaborators are the people with access to the organisation's back office, each with their role: **Owner** or **Administrator**. They are invited by email from the **Collaborators** tab.

- **Invitation.** Until the person signs in, their invitation shows as *Pending acceptance*. It is considered accepted as soon as they sign in with the organisation assigned; it does not depend on pressing anything on the welcome screen.
- **Who manages.** Inviting, changing the role of or removing collaborators is done by owners and administrators with **active** access; an unaccepted invitation or a deactivated access does not allow anyone to be managed.
- **The owner tier.** Only an owner can appoint or remove another owner.
- **Never without an owner.** The organisation's **only active owner** cannot be removed: add another owner first.

Removing a collaborator deletes their permissions over the organisation and cannot be undone; to give them access again they have to be invited again.

---

## Company details

| Field | Required | What it is for |
|---|---|---|
| **Company name** | Yes | Trading name, the one your team sees on the platform |
| **Primary language** | — | Spanish or English. German and Portuguese are in development |
| **Legal name** | Yes | Legal denomination. Required to subscribe and for documentation |
| **Tax ID (NIF / CIF)** | — | Tax identification of the organisation |
| **Billing email** | — | Address the invoices arrive at |
| **Address** | Yes | Company address, chosen from the address search box. The coordinates and the **time zone** come from it. There is no separate city field: the normalised address already includes it |

There is no "sector of activity" field: the platform does not classify the organisation by sector and does not adjust anything based on it.

---

## Time zone

The organisation's time zone is taken from its address and acts as the **default value** for branches that do not have one of their own. If your whole organisation operates in the same zone, it is enough to let the branches inherit it.

> **Warning:** when changing the organisation's address, the new time zone only affects branches that do not have one configured. Those that have their own are unaffected.

---

## Security

Two-step verification is enabled **per user and per employee**, not as a global organisation policy: each employee record has its own 2FA option, and each user can enable it from the security section of their account.

> **Status: Not available**
> A mandatory 2FA policy for the whole organisation, forcing every back office user to configure it, is not implemented in the current version.

If your organisation needs 2FA across the board, enable it employee by employee on their record. See [Two-factor authentication](../02-employees/09-two-factor-authentication.md).

---

## Billing and subscription

From **Subscriptions** the Owner consults the plan contracted and its status, and from **Invoices** the history. Payment methods are managed under **Billing setup**.

Billing for the Bronze plan is **per employee and month**: there is no included employee quota that can be used up. See [Plans, prices and features](../14-reference/91-plans-and-features.md).

---

## How the configuration propagates to branches

The organisation's values are the reference that branches inherit or override:

1. **Organisation**: defines the global default value.
2. **Branch**: if it defines its own, that takes priority.
3. **Employee**: if they define their own, it takes priority over their branch's.

For example, with the organisation on `Europe/Madrid` and a branch in the Canary Islands on `Atlantic/Canary`, that branch uses its own and the rest inherit Madrid. The same happens with the calendar: weekly schedule, breaks and workday mode cascade down through those three levels.

Tax details and billing have no branch equivalent: they are strictly global.

---

## The difference between organisation and branch configuration

| Aspect | Organisation | Branch |
|---|---|---|
| Scope | The whole organisation | A single workplace |
| Access | Owner | Owner and Manager |
| Exclusive parameters | Tax details, workspace, collaborators, billing and subscription | Check zone and its radius |
| Inheritance | Default value | Overrides the organisation's |
| Impact of a change | The whole organisation | Only that site and its employees |

The rule is simple: what affects the company as a whole is configured at the organisation; what is specific to a site, at the branch.

---

## How to access it

1. Sign in to the back office with an **Owner** account.
2. In the side menu, select **Organisation**.
3. Go to the tab you need and modify the parameters.
4. Save.

> **Warning:** changes to the tax details affect the documentation generated from that moment on; they do not alter invoices or reports already issued.

---

> **Role note:** organisation configuration, and in particular the subscription, is the **Owner's** responsibility. To delegate day-to-day management —branches, employees, tasks and documents— use the **Manager** role.

---

## Electronic signature

The **Workspace** tab has an **Electronic signature** section with the CheckBiz360 certificate and the steps to install it in Acrobat Reader, so that the PDFs signed by your workers show in green. See [Read receipt and electronic signature](../05-document-management/35-electronic-signature.md).

## Related articles

| Article | Description |
|---|---|
| [Create an account and set up the organisation](../01-getting-started/03-create-account-and-set-up-organisation.md) | The complete sign-up process |
| [Create and manage branches](./57-create-and-manage-branches.md) | Fields, geocoding and statuses |
| [Advanced branch configuration](./58-advanced-branch-settings.md) | Check zone, schedule and workday mode |
| [Configuration inheritance](../04-calendar-and-schedules/26-configuration-inheritance.md) | How the effective calendar is resolved |
| [Plans, prices and features](../14-reference/91-plans-and-features.md) | Price, 15-day trial and how to subscribe |
