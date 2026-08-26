# Permission matrix by role

CheckBiz360 applies a role-based access control model that determines precisely what each user can do within the platform. This matrix is the definitive reference for understanding which actions are available at each level and under what conditions.

Consult this table when configuring new profiles, resolving questions about access to features or reviewing your organisation's permission policy.

---

## Permission table

| Action | Worker | Supervisor | Manager | Owner |
|---|---|---|---|---|
| Create own clock record | Yes | Yes | Yes | Yes |
| View own history | Yes | Yes | Yes | Yes |
| View team history | No | Yes (branch) | Yes | Yes |
| Request a manual workday | Yes | Yes | Yes | Yes |
| Approve and correct clock records | No | Yes (branch) | Yes | Yes |
| Create tasks | No | Configurable | Yes | Yes |
| Validate tasks | No | Configurable | Yes | Yes |
| Rate workers | No | Configurable | Yes | Yes |
| Upload documents | No | No | Yes | Yes |
| View own documents | Yes | Yes | Yes | Yes |
| View team documents | No | Yes (by role) | Yes | Yes |
| View payslips and contracts | Own only | Own only | Team | All |
| Create incidents | Yes | Yes | Yes | Yes |
| Configure a branch | No | No | Yes | Yes |
| Manage employees | No | No | Yes | Yes |
| View operational intelligence | No | Partial | Yes | Yes |
| Generate reports | No | No | Yes | Yes |
| Configure the organisation | No | No | No | Yes |

---

## Notes on the table

### Configurable supervisor permissions

Some **supervisor** permissions are marked as "Configurable" in the table. This means that the default behaviour can be enabled or disabled by the manager or the owner according to the company's operational needs. Specifically:

- **Create tasks** — By default, supervisors cannot create tasks. The manager can enable this capability for specific supervisors.
- **Validate tasks** — The same as creation: disabled by default, activatable by the manager.
- **Rate workers** — Allows the supervisor to record performance ratings for the workers on their team. Disabled by default.

To modify these permissions, go to the profile of the supervisor in question and adjust the advanced permission settings.

### Branch scope in the supervisor role

Where the table says "Yes (branch)", it means that the supervisor can only carry out that action on employees or data belonging to the branch where they have been assigned supervisor responsibility. They have no visibility over, or ability to act on, other branches.

### Viewing team documents as a supervisor

The supervisor column says "Yes (by role)" for viewing team documents. This means the supervisor can see documents belonging to the staff assigned under their responsibility, provided those documents have been marked as accessible to their role level by the manager who uploaded them.

### Viewing payslips and contracts

This permission behaves differently depending on the role:

- **Worker and Supervisor** — Can only view their own payslip and contract documents.
- **Manager** — Can view the payslip and contract documents of every employee on their team or at their assigned branches.
- **Owner** — Has access to every payslip and contract document in the organisation, with no branch or team restriction.

### Operational intelligence for supervisors

The supervisor's "Partial" access to operational intelligence means they can consult basic metrics and statistics for their branch's team (such as hours worked or attendance rates), but they have no access to the strategic analysis dashboards, branch comparisons or aggregate financial indicators that are available to the manager and the owner.

### Configure the organisation

This action is reserved exclusively for the **owner** role. It includes configuring the company's global parameters such as the organisation name, the time zone, integrations with external systems and subscription management.

---

## Considerations on access security

Role assignment should be reviewed regularly, especially at the following moments:

- When an employee changes position or responsibilities.
- When a supervisor moves to managing a different branch.
- When an employee leaves the company.
- After organisational restructuring or the opening of new branches.

> **Note:** Assigning a higher role level than necessary can compromise the confidentiality of information. Applying the principle of least privilege is recommended: each employee should have only the level of access they need to perform their duties.

---

## Who can consult this configuration

Viewing and modifying role permissions is available to the **manager** (level 3) and **owner** (level 4) roles.

---

## Related articles

- [Roles and responsibility levels](07-roles-and-responsibility-levels.md)
- [Create and manage employees](06-create-and-manage-employees.md)
- [Document access permissions](../05-document-management/37-document-access-permissions.md)
- [What operational intelligence is](../07-operational-intelligence/49-what-is-operational-intelligence.md)
