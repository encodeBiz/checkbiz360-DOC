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

One row per task, with these columns: Company, Site, Title, Status, Priority, Start, End, **Time spent (h)**, **Paused (h)**, **No. of pauses**, **Time spent excluding pauses (h)**, Team, Rating and No. of evidence items.

The time columns are worth reading carefully:

| Column | What it measures |
|---|---|
| **Time spent (h)** | The time elapsed between the start and the end of the task. It is not time worked: a task started on Friday and finished on Monday includes the weekend. |
| **Paused (h)** | The sum of the task's pauses. |
| **No. of pauses** | How many times it was paused. |
| **Time spent excluding pauses (h)** | Time spent minus time paused. It deducts the pauses someone recorded, not the interruptions nobody marked. |

A task that has not yet been started leaves the pause columns empty. If a task is paused when the report is generated, the open pause counts up to that moment.

### Material for each task

If your company has [inventory](../16-inventory/100-what-is-inventory.md) subscribed (or on trial), the report also answers a question the work report rarely does: **what material was used on each job and what it cost**.

The tasks sheet gains three columns at the end:

| Column | What it is |
|---|---|
| **Material** | What was consumed on the task: each item with its quantity, and equipment by its unit. |
| **Unsettled** | What went out and nobody has declared or returned. This is what to check before validating. |
| **Material cost (€)** | What was consumed times its unit cost. Empty if no item has a cost on its record. |

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
| [Employee rating](./46-employee-rating.md) | How performance scores are generated |
| [Priorities and deadlines](./44-priorities-and-deadlines.md) | Deadline configuration that affects tracking |
| [Task statuses](./42-task-statuses.md) | Meaning of the statuses and of time compliance |
| [Report types](../11-reports-and-exports/76-report-types.md) | All the reports available on the platform |
| [Export data](../11-reports-and-exports/78-export-to-excel-and-csv.md) | Export formats available |
