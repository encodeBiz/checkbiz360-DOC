# Platform structure

CheckBiz360 organises information across three hierarchical levels: organisation, branch and employee. This architecture lets a company with dozens of sites and hundreds of employees operate from a single account, with configurations differentiated per unit and individual exceptions wherever they are needed.

Understanding this structure is essential to configuring schedules, calendars and control policies correctly. A well-considered configuration removes the need to enter data over and over and guarantees that every employee always operates under the right rules.

## The three hierarchical levels

### Level 1: Organisation

The organisation represents the company as a whole. It is the highest level of the hierarchy and the container for everything else.

The configuration at organisation level establishes the default values that will apply to every branch and employee, unless one of the lower levels explicitly overrides them.

What is configured at organisation level:

- Tax and corporate details: trading name, legal name, tax ID and address.
- Primary language and visual identity.
- Default time zone, derived from the organisation's address.
- Global work calendar: base weekly schedule and public holidays that affect the whole organisation.
- Billing and subscription.

### Level 2: Branch or project

The branch is the operational unit. It can represent a store, an office, a site, a department or any other functional grouping of employees.

The branch inherits the organisation's entire configuration, but can override those elements that differ from the global set-up. This lets a company with sites in different regions have different local public holiday calendars without needing to create separate accounts.

What can be configured at branch level:

- Name, address and GPS coordinates.
- Check zone and its radius in metres.
- Its own time zone, if it differs from the organisation's.
- Weekly schedule and breaks, which may differ from the organisation's.
- Workday and break mode: strict or flexible.
- Local public holiday calendar.

> **Note:** A branch cannot have configurations more permissive than the security restrictions defined at organisation level. For example, if the organisation requires 2FA, no branch can disable it for its employees.

### Level 3: Employee

The employee is the smallest unit in the hierarchy. They are assigned to one or several branches with a given role and receive the effective calendar that results from combining the organisation's configuration with their branch's.

In specific cases —remote employees, workers with irregular schedules, staff on secondment— individual exceptions can be defined that override the branch's values.

What can be configured at employee level:

- Their own time zone (for remote employees in another region).
- Schedule exceptions (one-off or recurring changes).
- Hourly cost (for cost analysis).
- Associated documents (contracts, payslips, certificates).

## Cascading inheritance

An employee's effective calendar on a given day is resolved following a clear order of priority:

```
Employee configuration      (highest priority)
         |
         v
Branch configuration
         |
         v
Organisation configuration  (base priority)
```

In practice, this means that if the organisation defines the base schedule as 09:00-17:00, but the "South Warehouse" branch has a 07:00-15:00 schedule, and the employee Juan García has an individual schedule exception for the afternoon shift (15:00-23:00), the system will apply Juan García's schedule and use that as the reference for calculating late arrivals, absences and overtime.

This inheritance logic removes the need to configure every employee from scratch and guarantees that changes at organisation or branch level propagate automatically to all the employees affected.

## Back office roles

The managers who administer the platform from the web back office operate under one of these three roles:

| Role | Scope | Main capabilities |
|---|---|---|
| Owner | The whole organisation | Complete configuration, billing, branch creation, management of all employees, access to all reports |
| Manager | Assigned branches | Management of employees and schedules at their branches, access to records and reports for their sites |
| Supervisor | Assigned branches | Review and approval of records, incident management, consultation of basic reports |

> **Note:** A manager can manage several branches at once. An employee can have the manager role at one branch and the supervisor role at another, if the organisation requires it.

## Mobile app role

The **Worker** role corresponds to the employee who uses the CheckBiz360 app to clock in. This role has no access to the web back office.

From the app, the Worker can:

- Record entry and exit.
- Consult their own attendance records.
- See their assigned schedule.
- Receive notifications from the platform.
- Access their employment documents (if the document module is active).
- Consult and manage their assigned tasks (if the tasks module is active).

## Modules available by role

| Module | Owner | Manager | Supervisor | Worker (app) |
|---|---|---|---|---|
| Time tracking and clock records | Full | Per branch | Per branch | Own only |
| Employee management | Full | Per branch | Read-only | No |
| Schedule configuration | Full | Per branch | No | No |
| Cost analysis | Full | Per branch | No | No |
| Operational intelligence | Full | Per branch | Summary | No |
| Document management | Full | Per branch | No | Own only |
| Operational tasks | Full | Per branch | Per team | Assigned only |
| Reports and exports | Full | Per branch | Basic | No |
| Organisation configuration | Full | No | No | No |
| Billing and subscription | Full | No | No | No |

> **Note:** both plans, Bronze and Enterprise, give access to every module of the platform; what changes between them is the support and the integrations. See [Plans, prices and features](../14-reference/91-plans-and-features.md).

## Related articles

- [What CheckBiz360 is](01-what-is-checkbiz360.md)
- [Create an account and set up the organisation](03-create-account-and-set-up-organisation.md)
- [Create and manage branches](../08-branches-and-organisation/57-create-and-manage-branches.md)
- [Roles and responsibility levels](../02-employees/07-roles-and-responsibility-levels.md)
- [Base schedules and shifts](../04-calendar-and-schedules/23-base-schedules-and-shifts.md)
