# Create and manage employees

Managing the team is the starting point of any operation in CheckBiz360. From the back office, the company's managers can bring in new employees, update their information at any time and control their employment status over time.

This article explains how to create an employee from scratch, which fields are required and which are optional, and how to manage the statuses a person can go through during their employment relationship with the organisation.

---

## Create a new employee

### Required fields

- **Full name** — First name and surnames as they should appear in the records.
- **Email address** — Unique address on the platform. It is the employee's identifier and the address the initial access is sent to. It is changed separately, with **Change email**, because it is what the person uses to sign in to the app. See [App access and email change](116-app-access-and-email-change.md).
- **Phone** — Contact number, with international dialling code.
- **Relationship type** — *Staff* (company personnel) or *Collaborator* (external, freelance or service provider). It appears on the record next to the status, and it is not a minor detail: collaborators **are not included in the working-time record report**, which is mandatory for the employment relationship. See [Roles and responsibility levels](07-roles-and-responsibility-levels.md#relationship-type-internal-versus-contractor).

> **Important:** the responsibility level —worker, supervisor, manager or owner— **is not assigned at creation**. It is defined when linking the employee to a branch, because the same person can hold different responsibilities at each site. See [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md).

### Steps to create an employee

1. Sign in to the back office with manager or owner credentials.
2. In the side menu, select **Employees** and press the new employee button.
3. Complete the required personal details.
4. Adjust the security options and any additional details you need.
5. Configure the employee's calendar if it differs from their branch's.
6. Save. The system creates the profile and sends the welcome email.
7. Link the employee to their branch and assign their responsibility and position there.

### Automatic welcome email

On saving the profile, CheckBiz360 automatically sends the employee an email with the instructions for activating their account and accessing the mobile app. No further action is required from the administrator.

On the record, the **App access** block says whether that email was delivered, whether it bounced or whether the person is already using the app. You can resend the access from there. It is explained in [App access and email change](116-app-access-and-email-change.md).

---

## Security and work options

Three options are enabled or disabled per employee:

| Option | What it does |
|---|---|
| **Two-step verification (2FA)** | Requires a temporary code in addition to the password |
| **Biometrics required** | The employee must authenticate with a fingerprint or facial recognition before their clock-in is accepted |
| **Works off-site** | Allows clocking in outside the branch geofence (it used to be called *Remote work*). When enabled, **the employee's address becomes required**, because it is the reference against which the clock-in is validated. See [Working off-site](../03-time-tracking/15-remote-clocking-in.md) |

---

## Other fields

- **Identity document** — Useful for audits and HR exports.
- **Address** — Optional, unless working off-site is enabled. It is chosen from the address search box; there is no separate city field, because the normalised address already includes it.
- **Employee calendar** — Their own schedule and exceptions, when they differ from their branch's. If it is not configured, the employee inherits the branch calendar.
- **Additional data** — Free key/value fields for information specific to your organisation (employee number, collective agreement, cost centre, etc.).

Linking the employee to a branch also defines their **responsibility** at that site, their **position** and their **hourly rate**, the last of which feeds the cost analysis.

---

## Employee statuses

CheckBiz360 covers seven employment statuses, plus the **Pending** status for records that are only partly completed:

| Status | Description |
|---|---|
| **Pending** | The record exists but the person cannot work yet, usually because the email address is missing (common in records imported from an integration). They receive no access and no welcome email, and **are not billed**. The record leaves this status when the email is completed. It is not assigned by hand. |
| **Active** | The employee is working normally and has access to the platform. |
| **Inactive** | The employee is not operational. This is the status used when the employment relationship ends: the profile and its history are retained. |
| **Holiday** | The employee is on holiday. |
| **Sick leave** | The employee is on leave through illness. |
| **Career break** | The employee is on a career break. |
| **Paternity leave** | The employee is on paternity leave. |
| **Maternity leave** | The employee is on maternity leave. |

To change the status, open the employee's profile, press **Edit** and select the new status. The status filter in the employee list includes **Pending**, to locate the records still to be completed.

> **Important:** for billing purposes, every employee who is neither pending nor deleted counts. An **Inactive** employee, or one on leave, is still part of the workforce and **is billed**.

> **Note:** the absence statuses (holiday, sick leave, career break) can also be managed as **absences with dates** from the calendar, which allows them to be planned in advance instead of changing the status by hand on the day they start.

---

## Edit an employee's details

1. Go to **Employees** in the side menu.
2. Find the employee with the search box or the filters.
3. Click on their name to open the profile.
4. Select **Edit** and make the changes.
5. Save.

Changes take effect immediately. The email address is changed with its own button, **Change email**, which explains everything it involves before you confirm.

---

## Deactivating versus deleting an employee

These two actions have very different consequences:

- **Deactivate** (*Inactive* status): the employee loses access to the platform, but all their history —clock records, documents, tasks, incidents— is retained in full. It is the right option when the employment relationship ends or when access has to be suspended temporarily.
- **Delete**: permanently erases the profile. It is irreversible. Reserve this action for exceptional cases, such as a profile created in error or a duplicate.

> **Important:** the working-time record has to be retained for four years under RDL 8/2019. Deactivating, rather than deleting, is what makes it possible to meet that obligation.

---

## Who can carry out these actions

Profile management is available to **manager** (level 3) and **owner** (level 4). Supervisors and workers have no access to managing other employees' profiles.

---

## Adding many people at once

If you are starting with a staff of thirty or forty people, there is no need to create them one by one. In the employee list, **Import** downloads an Excel template with one sheet for branches and another for people; you fill it in, upload it and, before anything is created, see what will happen with each row. The app welcome is sent at the end, when you decide. See [Add branches and staff from Excel](./110-add-branches-and-staff-from-excel.md).

---

## Related articles

- [Roles and responsibility levels](07-roles-and-responsibility-levels.md)
- [Permission matrix by role](08-permission-matrix-by-role.md)
- [Two-factor authentication](09-two-factor-authentication.md)
- [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md)
- [Export the employee list](12-export-employee-list.md)
- [Teams](99-teams.md)
- [App access and email change](116-app-access-and-email-change.md)
