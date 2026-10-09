# Create an account and set up the organisation

Before any employee can clock in, you have to build the base structure of your organisation in CheckBiz360. It is a one-off process that lays the foundations everything else rests on: schedules, branches, employees and control policies.

This article walks the path from registration to having the first operational branch and the first employee invited.

> **Note:** whoever completes this process becomes the **Owner** of the organisation. Managing the subscription is exclusive to that role; the rest of the configuration can be delegated to a Manager afterwards.

---

## Concepts to know first

Three terms structure the platform:

- **Organisation**: your company. It holds the global configuration —legal details, language, address and time zone— that applies across the whole organisation.
- **Branch**: each operational unit (store, office, site, project). It inherits the organisation's configuration, but can have its own time zone, check zone, schedule and public holidays.
- **Employee**: linked to one or several branches. Each link defines their responsibility, their position and their rate. They inherit their branch's calendar, unless they have one of their own.

---

## Step 1. Create the account

Registration takes place in the back office itself, at `saas.encodebiz.com`.

1. Open `saas.encodebiz.com` in any browser.
2. From the sign-in screen, go to the registration form.
3. Fill in the fields, **all of them required**:
   - **Full name**
   - **Email address**
   - **Phone**
   - **Password** and its **confirmation**
4. Accept the terms and the privacy policy.
5. Complete the **verification challenge** shown in the form. It is an automatic Cloudflare check that confirms the person registering is a human; the submit button becomes active once it has been passed.
6. Submit the form.

There is no intermediate email verification step: on completing registration, the system takes you **straight to the organisation creation screen**.

> **Note:** the verification challenge expires after a few minutes. If you take a while to submit the form and the `turnstile/failed` warning appears, reload the page and try again. The same challenge is requested when recovering your password.

> **Note:** use a corporate email address. That address is linked as the account Owner and is where administrative communications are sent. If the email is already in use, the system reports it with the error `auth/email-already-in-use`.

---

## Step 2. Create the organisation

This is the screen you reach right after registering. If you are already inside the back office, you get there from **Organisation** in the side menu.

| Field | Required | Description |
|---|---|---|
| **Company name** | Yes | Trading name, the one your team will see on the platform |
| **Primary language** | — | Spanish or English. German and Portuguese are in development |
| **Legal name** | Yes | Legal denomination, the one that appears on documentation |
| **Billing email** | — | Address the invoices are sent to; the registration one is proposed |
| **Tax ID (NIF / CIF)** | — | Tax identification of the organisation |
| **Address** | Yes | Company address. Selecting it resolves the coordinates and the **time zone**, which acts as the default for branches that do not have one of their own |

Save to continue.

> **Important:** the legal name and the tax details are not an optional formality. **Without them you cannot subscribe to a plan**: the back office blocks the subscription until the legal details and a payment method are complete.

---

## Step 3. Activate CheckBiz360

With the organisation created, the service has to be activated. In the side menu, go to **CheckBiz360** and review the available plans.

Before subscribing, the system checks two requirements and warns you if either is missing, linking to the relevant screen:

- **Company details** complete.
- **Payment method** configured. **Without a payment method the service cannot be activated.**

Adding the card does not generate any charge, and there is no charge during the trial either: the first subscription includes a **15-day trial**, and if you decide not to continue before it ends, you cancel the subscription and nothing is charged. The card also serves to confirm that there is a person behind the account. See [Plans, prices and features](../14-reference/91-plans-and-features.md).

Once the service is activated, the CheckBiz360 sections —Employees, Branches, Schedules, Tasks, Documents, Reports…— appear directly in the side menu.

---

## Step 4. Create the first branch

When the service is activated, CheckBiz360 creates a first branch with the company details. Review its address and its check zone from its record. If your account does not have it, or you need more sites, go to **Branches** in the side menu and create one.

| Field | Required | Description |
|---|---|---|
| **Name** | Yes | Identifier of the operational unit: "City Centre Store", "Madrid Office" |
| **Address** | Yes | It is chosen from the search box. The system obtains the site's coordinates and time zone, and fills in the country and the postcode |
| **Check zone in metres** | Yes | The radius within which a clock-in is accepted. Between 50 and 200 metres depending on the size of the site |
| **Tax ID** | — | Only if the site has its own tax identification |
| **Status** | — | Active by default |

> **Note:** the check zone is what prevents clocking in from outside the site. Too wide a radius makes it useless; too narrow a one generates rejections through GPS imprecision. For most offices and stores, **100 metres** is a good starting point, and it is adjusted afterwards with the data from the first few weeks.

Save. You will then be able to configure its weekly schedule from **Schedules**.

---

## Step 5. Create the first employee

In **Employees**, create a new one.

1. Fill in the required details: **full name**, **email address**, **phone** and **relationship type** (staff or collaborator).
2. Save. The system creates the profile and **automatically sends the welcome email** with the activation instructions.
3. Open the employee's record and **link them to the branch** you have just created. It is in that link that their **responsibility** —worker, supervisor, manager or owner—, their **position** and their **hourly rate** are defined.

> **Important:** the responsibility level is not chosen when creating the employee, but in the link with each branch. The same person can be a worker at one site and a supervisor at another.

If the employee does not receive the email, see the relevant section in [Common problems and solutions](../13-support-and-incidents/88-common-problems-and-solutions.md).

---

## Step 6. Install the app

The employee needs the CheckBiz360 app on their phone in order to clock in. It is available free of charge for iOS and Android.

When they open it for the first time, they will sign in with the email and password they set when activating their account from the welcome email.

---

## Where you stand at the end

On completing these steps your organisation has:

- An organisation with its legal details and its time zone.
- The CheckBiz service active.
- An operational branch with its check zone.
- An employee created, linked to that branch and with access to the app.

From here you can repeat steps 4 and 5 for the rest of the sites and people, or move on to the quick start guide to make the first test clock-in.

---

## Related articles

| Article | Description |
|---|---|
| [Quick start guide](04-quick-start-guide.md) | From creation to the first validated clock-in |
| [Platform structure](05-platform-structure.md) | Organisation, branch and employee |
| [Create and manage branches](../08-branches-and-organisation/57-create-and-manage-branches.md) | Fields, geocoding and statuses |
| [Create and manage employees](../02-employees/06-create-and-manage-employees.md) | Creation, employment statuses and security options |
| [Plans, prices and features](../14-reference/91-plans-and-features.md) | Price, 15-day trial and how to subscribe |
