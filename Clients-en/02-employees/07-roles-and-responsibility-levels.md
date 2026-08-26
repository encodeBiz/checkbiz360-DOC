# Roles and responsibility levels

CheckBiz360 structures access to the platform through a system of four role levels. Each level determines what a user can see and do within the system, from the front-line employee to the account owner.

Understanding how roles work and how they apply according to the scope of responsibility is essential to configuring the platform correctly and guaranteeing that each person accesses only the information that concerns them.

---

## The four role levels

### Level 1 — Worker (Employee)

This is the most basic access level. The worker can clock in, consult their own history, request manual workdays, view their own documents and create incidents. They have no visibility over the rest of the team's data and no ability to modify the platform's configuration.

**Typical use cases:** production operative, customer service agent, field technician.

### Level 2 — Supervisor

The supervisor has extended access over the team assigned to them. They can consult their branch's clock-in history, approve and correct clock records, and access certain team documents. Some of their permissions are configurable by the manager: the ability to create tasks, validate them or rate workers may or may not be enabled depending on the company's configuration.

**Typical use cases:** shift lead, team leader at a branch, section head.

### Level 3 — Manager

The manager has full access to operational management: they can create and manage employees, configure branches, approve any clock record, manage documents, generate reports and access the company's operational intelligence. It is the usual profile for the HR director or the area manager.

**Typical use cases:** human resources director, area manager, operations lead.

### Level 4 — Owner

The owner has absolute access to the platform, including the organisation's global configuration, subscription management and every manager capability. Only one or a few people in the organisation should have this level.

**Typical use cases:** CEO, founding partner, general manager, systems administrator.

---

## Relationship type: internal versus contractor

Regardless of the role level assigned, every employee has a type of relationship with the company:

- **Internal** — Payroll employee with a current employment contract. Part of the organisation's regular structure.
- **Contractor** — External person who works for the company on a one-off or recurring basis without being on the payroll. This may be a freelancer, a service provider or a self-employed professional.

Both types can hold any role level, although in practice contractors usually operate as workers or supervisors with a limited scope.

---

## Scope of responsibility: organisation versus branch

An employee's role can apply to two different scopes:

### Responsibility at organisation level

When a role is assigned at organisation level, the user has that level of access across the whole company, regardless of how many branches exist. A manager at organisation level can manage employees, clock records and documents from every branch.

### Responsibility at branch level

When a role is assigned linked to a specific branch, the user's access is limited to that location. A supervisor with responsibility at the Madrid branch will only see the clock records and the team of that branch, with no access to other locations' data.

---

## One employee, several simultaneous roles

CheckBiz360 allows the same employee to hold different roles at different branches. This flexibility covers real situations such as the following:

- A person can be a **supervisor** at the Barcelona branch (where they run the shift team) and a **worker** at the Madrid branch (where they help out occasionally).
- An HR lead can hold the **manager** role at organisation level, while at a specific branch they additionally act as a supervisor for direct management duties.

To configure this scenario, go to the employee's profile and assign the corresponding responsibilities for each branch.

---

## Assigning responsibilities: who can assign what

Not all users can assign every role. The restrictions are as follows:

- An **owner** can assign any role level to any employee in any scope.
- A **manager** can assign roles up to supervisor level to employees within their scope of management.
- A **supervisor** cannot assign roles.
- A **worker** cannot assign roles.

> **Note:** It is advisable to review responsibility assignments periodically, especially after organisational changes such as team rotations, promotions or the arrival of new managers.

---

## Who can carry out these actions

Configuring roles and responsibilities is available to the **manager** (level 3) and **owner** (level 4) roles.

---

## Related articles

- [Create and manage employees](06-create-and-manage-employees.md)
- [Permission matrix by role](08-permission-matrix-by-role.md)
- [Multi-organisation employees](11-multi-organisation-employees.md)
- [Export the employee list](12-export-employee-list.md)
