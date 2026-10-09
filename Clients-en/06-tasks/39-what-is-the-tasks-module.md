# What the tasks module is

The CheckBiz360 tasks module lets the company's managers create, assign and track specific operational activities. Unlike time tracking, which records when an employee works, the tasks module records what that employee does during their workday and whether they have completed it correctly.

It is a complementary tool that provides visibility over the real work done in each shift, branch or department.

---

## The difference between tasks and clock records

Time tracking and the tasks module have different objectives and complement each other.

| Aspect | Time tracking | Tasks module |
|---|---|---|
| What it records | Presence: entry and exit | Activity: what has been done |
| Unit of measurement | Time worked | Task completed or not |
| Who acts | The employee clocks in | The employee updates the status |
| What it is for | Payroll and regulatory compliance | Operational tracking and performance |

An employee may have clocked in correctly and still not have completed the tasks assigned for that shift. The tasks module makes that difference visible.

---

## Common use cases

### Opening and closing checklist for a site

Shops and customer-facing premises need a series of specific actions to be carried out before opening or when closing. The manager creates an opening task and writes the steps as a **checklist in the description**, which the employee on shift follows from the app and confirms when finished.

### Maintenance tasks

Technical incidents or periodic inspections of facilities can be managed as tasks assigned to the maintenance lead. The system keeps the execution history and allows photo or video evidence of the result to be attached.

### Training activities

When an employee has to complete a training module, view a corporate document or attend an internal session, that obligation can be turned into a task with a deadline. The manager can check who has completed it and who has not.

### Tracking operational objectives

Short-term objectives —restocking, contacting a list of customers, completing a report— can be broken down into tasks assigned to the right people, with priority and deadline clearly defined.

### Home services or work at the customer's premises

When the work changes address every day —a repair, a cleaning job, a technical visit—, the task can carry its **own work site** without setting up a branch for each job. The employee can only start it while at that address. This is explained in [Create a task](./40-create-a-task.md#own-work-site).

### Recurring work

A job that is repeated with few variations does not need to be written again: the task is **duplicated** from the list or from its record, and the copy only asks for a title and dates. This is explained in [Create a task](./40-create-a-task.md#duplicating-a-task).

---

## Roles that interact with the module

The tasks module respects CheckBiz360's role hierarchy. Each role has different capabilities:

### Owner and Manager

They have full access to the module. They can create, assign, modify and cancel tasks at any branch in the organisation, validate them and rate the employee's performance.

### Supervisor

Their scope is decided **on each task**, not on their profile. Every task includes two options —**Allow validation by supervisor** and **Allow rating by supervisor**, both enabled by default— that let the branch supervisor close the loop on that specific task. Task creation by supervisors is disabled by default.

### Worker (employee)

Receives the assigned tasks, consults their description and evidence, starts the work, pauses and resumes it when they have to interrupt it, adds progress notes, uploads evidence and marks the task as completed. They cannot create or assign tasks to other employees.

---

## Relationship with time tracking

Tasks and clock records measure different things, but they do not run separately: to **start**, **resume** or **complete** a task, the employee has to have an **open workday**, that is, to have clocked in. Being on a break counts as an open workday. If they have not clocked in, the action is rejected with the error `task/no_open_session`.

**Pausing** does not require it: a task is paused right at the moment of leaving.

Owners and administrators acting from the back office have no workday to open and are exempt; that way they can, for example, close the task of someone who has already left. A supervisor or manager working with their own employee record does need an open workday.

Dates, on the other hand, are free: a task can have its deadline on a public holiday or outside normal hours if the operation requires it.

---

> **Note:** To get the most out of the tasks module, we recommend combining it with the operational reports module. Task completion data feeds the team's efficiency indicators in the operational intelligence section.

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](./40-create-a-task.md) | Fields, steps and options when creating a task |
| [Assign tasks to employees](./41-assign-tasks-to-employees.md) | Individual and team assignment |
| [Task statuses](./42-task-statuses.md) | Complete life cycle of a task |
| [Tracking and updates](./43-tracking-and-updates.md) | Starting, pausing, resuming and the task history |
| [Task validation](./45-task-validation.md) | Validation flow and permissions |
| [Task reports](./48-task-reports.md) | Metrics and data export |
