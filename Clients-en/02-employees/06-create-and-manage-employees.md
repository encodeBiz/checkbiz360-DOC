# Create and manage employees

Managing the team is the starting point of any operation in CheckBiz360. From the back office, the company's managers can bring in new employees, update their information at any time and control their employment status over time.

This article explains how to create an employee from scratch, which fields are required and which are optional, and how to manage the statuses a person can go through during their employment relationship with the organisation.

---

## Create a new employee

### Required fields

- **Full name** — First name and surnames as they should appear in the records.
- **Email address** — Unique address on the platform. It is the employee's identifier and the address the initial access is sent to. **It cannot be changed once the profile has been created.**
- **Phone** — Contact number, with international dialling code.
- **Relationship type** — *Internal* (payroll) or *Contractor* (external, freelance or service provider).

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

---

## Security and work options

Three options are enabled or disabled per employee:

| Option | What it does |
|---|---|
| **Two-step verification (2FA)** | Requires a temporary code in addition to the password |
| **Biometrics required** | The employee must authenticate with a fingerprint or facial recognition before their clock-in is accepted |
| **Remote work** | Allows clocking in outside the branch geofence. When enabled, **the employee's address becomes required**, because it is the reference against which the remote clock-in is validated |

---

## Other fields

- **Identity document** — Useful for audits and HR exports.
- **Address** — Optional, unless remote work is enabled.
- **Employee calendar** — Their own schedule and exceptions, when they differ from their branch's. If it is not configured, the employee inherits the branch calendar.
- **Additional data** — Free key/value fields for information specific to your organisation (employee number, collective agreement, cost centre, etc.).

Linking the employee to a branch also defines their **responsibility** at that site, their **position** and their **hourly rate**, the last of which feeds the cost analysis.

---

## Employee statuses

CheckBiz360 covers seven employment statuses:

| Status | Description |
|---|---|
| **Active** | The employee is working normally and has access to the platform. |
| **Inactive** | The employee is not operational. This is the status used when the employment relationship ends: the profile and its history are retained. |
| **Holiday** | The employee is on holiday. |
| **Sick leave** | The employee is on leave through illness. |
| **Career break** | The employee is on a career break. |
| **Paternity leave** | The employee is on paternity leave. |
| **Maternity leave** | The employee is on maternity leave. |

To change the status, open the employee's profile, press **Edit** and select the new status.

> **Note:** the absence statuses (holiday, sick leave, career break) can also be managed as **absences with dates** from the calendar, which allows them to be planned in advance instead of changing the status by hand on the day they start.

---

## Edit an employee's details

1. Go to **Employees** in the side menu.
2. Find the employee with the search box or the filters.
3. Click on their name to open the profile.
4. Select **Edit** and make the changes.
5. Save.

Changes take effect immediately. The email address is the only piece of data that cannot be changed.

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

## Related articles

- [Roles and responsibility levels](07-roles-and-responsibility-levels.md)
- [Permission matrix by role](08-permission-matrix-by-role.md)
- [Two-factor authentication](09-two-factor-authentication.md)
- [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md)
- [Export the employee list](12-export-employee-list.md)
