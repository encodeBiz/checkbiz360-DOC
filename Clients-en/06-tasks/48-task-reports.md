# Task reports

CheckBiz360 offers two routes for analysing task execution: the metrics consulted directly in the back office, and the **task report in Excel**, which is generated on demand and filed in the report history.

---

## Metrics visible in the back office

From the task list and detail, managers and owners can consult:

- **Tasks by status:** how many are in draft, assigned, in progress, completed, validated, rejected or cancelled, for the whole organisation or filtered by branch.
- **Tasks by employee:** the tasks assigned to each person with their current status, which makes it possible to identify unbalanced workloads or tasks stuck awaiting validation.
- **Time compliance:** for each task, whether it is on time, at risk, overdue, or whether it was completed inside or outside the deadline.
- **Ratings recorded:** the score given to the employee is visible in the task detail and in their profile.

> **Note:** the metrics reflect the current state as employees and managers interact with the tasks.

---

## Task report in Excel

The task report is generated from the **Reports** section of the back office and downloaded in **Excel (XLSX)** format.

### How to generate it

1. Go to **Reports** in the side menu.
2. Press the button to generate a new report.
3. Under **Report type**, select *Task report*. The format is fixed to Excel (XLSX), which is the only one available for this report.
4. Select the **period** (start and end date).
5. If you need to, filter by **branch** and by task **status**.
6. Generate the report. When it is ready, it will appear in the report history, from where you can download it.

> **Important:** the report period applies to each task's **deadline**, not to its creation date. A July report includes the tasks that were due in July, even if they were created in June.

### What it contains

The **Tasks** sheet has **one row per task and assigned person**, grouped by task. A task with three people takes up three rows, and the task's columns (Company, Site, Customer if there is one, Title, Status, Priority, Start, End, the times, Completed by, Rating and No. of evidence items) are repeated on each one, so that when you filter by a person you can still see which task each row belonged to. Each task closes with a **Total {task}** row and the report with a **Period total** row. The **−** sign in Excel's left margin collapses a task's people and leaves only its total.

It is the format designed for an accountant to work with: one row per person and task lets you add up, filter and build pivot tables by person, by job, by customer or by supplement without undoing anything by hand.

The person columns:

| Column | What it is |
|---|---|
| **Person** | Who was assigned. |
| **Job** | Which job they worked under on that task: the one chosen when assigning it or, if none was chosen, their default. See [Several jobs for the same person](../02-employees/140-several-jobs-for-the-same-person.md). |
| **Person's hours** | Their hours on the task. |
| **Source of the hours** | *Clock records*, if the person clocked in on the task; *Task clock*, if there were no clock records and the hours come from when it was started and finished, minus pauses. If a workday was left without a clock-out, it says so: *Clock records · 1 without clock-out*. |
| **Hourly rate** | The rate of the job they worked under, as it stood on the day of the clock record. |
| **Job cost** | Hours times hourly rate. |
| **Supplements** | The ones they were paid on that task, with their value in brackets. See [Supplements](../02-employees/141-supplements.md). |
| **Supplements (amount)** | What they add up to. |
| **Person cost** | Job cost plus supplements. |

The **Total** row of each task adds up the hours and the cost of its people, the supplements, the material if you have inventory and the task's **gross cost**.

If any task in the report has a customer, the **Customer** column is added after **Site** (see [The customer on the task](../17-customer-portfolio/119-the-customer-on-the-task.md)).

The money columns are seen by whoever can generate the report: the owner and administrators. Amounts **carry no currency symbol**: your company's currency is stated once in the header of each sheet (*Currency: EUR*) and is set in [Organisation configuration](../08-branches-and-organisation/61-organisation-settings.md#company-details). A person with no rate on their job leaves the cost empty, not at zero.

**Completed by** says who closed the task; if it was closed from the panel, it carries *(from administration)*, and the start and end are the times entered when closing it. See [closing it from administration](./127-who-finishes-the-task-and-closing-from-administration.md).

The time columns are worth reading carefully:

| Column | What it measures |
|---|---|
| **Time spent (h)** | The time elapsed between the start and the end of the task. It is not time worked: a task started on Friday and finished on Monday includes the weekend. |
| **Paused (h)** | The sum of the task's pauses. |
| **No. of pauses** | How many times it was paused. |
| **Time spent excluding pauses (h)** | Time spent minus time paused. It deducts the pauses someone recorded, not the interruptions nobody marked. |

A task that has not yet been started leaves the pause columns empty. If a task is paused when the report is generated, the open pause counts up to that moment.

### The "By person" and "Supplements" sheets

The file comes with two more sheets, drawn from the same rows:

- **By person**: the summary of the period, one row per person: how many tasks, hours, under which jobs, job cost, supplements (amount), total cost and, under **Supplements in the period**, which supplements they were paid and how many times. It is the sheet for preparing payroll or checking against your payroll provider.
- **Supplements**: the trail. One line per supplement paid, with the task, the site, the customer, the person, their job, the supplement, its type and its value, the hours, the hourly rate, the **amount** and the **source**: the clock-in it comes from or, if the task had no clock records, the task assignment. At the foot, how each type is calculated. If none was paid in the period, the sheet says so.

### Incidents

If any task in the period had an [incident](./125-task-incident.md), the **Tasks** sheet gains the **Incident** column: *Open* (in red) or *Resolved · Replanned*, *Cancelled* or *Solved*.

The file also always includes the **Incidents** sheet, with one row per incident, open or resolved: Site, Customer, Task, Task status, Reported, Reported by, Note, File, Incident, Resolution, Resolved, Resolved by and Resolution note. If there were none in the period, the sheet says so.

### Material for each task

If your company has [inventory](../16-inventory/100-what-is-inventory.md) subscribed (or on trial), the report also answers a question the work report rarely does: **what material was used on each job and what it cost**.

The tasks sheet gains three columns at the end:

| Column | What it is |
|---|---|
| **Material** | What was consumed on the task: each item with its quantity, and equipment by its unit. |
| **Unsettled** | What went out and nobody has declared or returned. This is what to check before validating. |
| **Material cost** | What was consumed times its unit cost. Empty if no item has a cost on its record. It goes in the task's **Total** row. |

And the file has one more sheet, **Material**, with one row per task and item or unit: the warehouse it came from, quantities reserved, issued, consumed, returned and unsettled, cost, and for equipment its reservation slot and its usage. This is the sheet to filter or build pivot tables on.

Without inventory, the report is exactly the same as always.

### If there are no results

If no task meets the selected filters, the system says so and does not generate an empty file. Widen the period or review the branch and status filters.

---

## Report history

Every report generated is listed in the **Reports** section, identified by type (tasks or working-time record) and by format (Excel or PDF), with the generation date and the period covered. From there they can be downloaded as many times as needed without regenerating them.

---

## Aggregate performance analysis

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

The aggregate metrics calculated by the platform —completion rate, average resolution time, rejection rate and average rating per period— and the automatic comparisons between branches are planned for a future version. Today those analyses can be built from the Excel report.

---

## Related articles

| Article | Description |
|---|---|
| [Several jobs for the same person](../02-employees/140-several-jobs-for-the-same-person.md) | Where the Job column and its hourly rate come from |
| [Supplements](../02-employees/141-supplements.md) | What they are, the three types and where they are chosen |
| [Employee rating](./46-employee-rating.md) | How performance scores are generated |
| [Priorities and deadlines](./44-priorities-and-deadlines.md) | Deadline configuration that affects tracking |
| [Task statuses](./42-task-statuses.md) | Meaning of the statuses and of time compliance |
| [Report types](../11-reports-and-exports/76-report-types.md) | All the reports available on the platform |
| [Export data](../11-reports-and-exports/78-export-to-excel-and-csv.md) | Export formats available |
