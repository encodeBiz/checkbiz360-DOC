# Report types available in CheckBiz360

CheckBiz360 centralises your company's operational information in two distinct forms, and it is worth not confusing them:

- **Downloadable reports**, generated on demand from the **Reports** section, filed in the history and downloaded as a file. There are three: the **attendance report** (PDF or Excel), the **task report** (Excel) and the **"Equipment and PPE"** report (Excel, with the inventory add-on). With inventory subscribed, the task report also includes each task's material, and inventory has its own **consumption report**.
- **On-screen analyses**, consulted in the operational dashboard and in the branch and employee records: punctuality, costs and anomalies. They generate no downloadable file in the current version.

This guide describes each one and the roles that have access.

---

## Attendance report

The attendance report is the module's base document. It gathers employees' presence data over a given period and provides a complete picture of the team's time behaviour.

### What it includes

- List of presences and absences by employee and day.
- Total hours worked by employee in the selected period.
- Breakdown by shift, branch or period.
- Status of each workday: complete, justified absence, unjustified absence, partial workday.
- On days with more than one clock-in and clock-out (split shifts, several jobs in a row): the **working day**, from the first clock-in to the last clock-out, and the **gaps between shifts**, measured from the clock-ins. The report shows what was measured; what gets paid is the company's decision.

> **Important:** the report gathers **staff** personnel. Employees marked as **collaborators** do not appear, because time recording is an obligation of the employment relationship and does not apply to a self-employed professional who invoices the company. Employees with no relationship type recorded are still included. See [Roles and responsibility levels](../02-employees/07-roles-and-responsibility-levels.md#relationship-type-internal-versus-contractor).

If no clock record meets the filters, the system says so and does not generate the file.

### What it is for

It is the most widely used report for daily operational supervision and for calculating salary variables such as overtime or deductions for absence. It is also the basis of the regulatory compliance report described in article [79](./79-regulatory-compliance-report.md).

### Access by role

| Role | Access |
|---|---|
| Owner | All branches and all employees |
| Manager | Employees of the branches they manage |
| Supervisor | Employees of their direct team, if the manager has enabled it |
| Worker | Only their own attendance data from the app |

---

## On-screen analyses: punctuality, costs and anomalies

These three readings are **not downloadable reports**: they are consulted in the Operations dashboard and in the branch and employee records. Exporting their data is on the roadmap.

### Punctuality and schedule deviations

Gathers late arrivals, early exits and the accumulated deviation between planned hours and hours actually worked. It makes it possible to distinguish whether lateness is a one-off or a pattern, and whether it belongs to one person or to a whole site.

### Costs

Cross-references attendance with the hourly rate configured in each employee's link with their branch: cost per hour worked, per workday, per output and accumulated for the period.

It contains sensitive information and is only accessible to **Owner** and **Manager**. It requires the rates to be configured: without them, the financial indicators appear empty.

### Anomalies

Brings together the records the system has identified as potentially irregular —excessive time precision, static geolocation, unauthorised devices— along with the manual corrections made to clock records, with their author, their moment and their reason.

They surface in the dashboard's **Analysis** tab, which orders the reading from least to most pointed: process and configuration first, people last. Exclusive to **Owner** and **Manager**.

---

## Task report

The task report gathers the period's tasks with their status and their deadline compliance. It is a **downloadable report in Excel (XLSX)**.

### What it includes

- The tasks whose **deadline** falls within the selected period, with their status and their time compliance.
- The time for each task: time spent, time paused, number of pauses and time spent excluding pauses. They are explained in [Task reports](../06-tasks/48-task-reports.md#what-it-contains).
- Filters by branch and by task status.
- The data needed to calculate whatever is required in the spreadsheet: completed versus assigned, overdue, rejected.

- With [inventory](../16-inventory/100-what-is-inventory.md) subscribed: the material consumed per task, its cost and what was left unsettled, plus a detail sheet per item. See [Task reports](../06-tasks/48-task-reports.md#material-for-each-task).

> **Note:** the pre-calculated aggregate metrics —completion percentage, average resolution time, average rating— are on the roadmap. Today the report delivers the detail and the calculation is done in the spreadsheet.

### What it is for

It complements presence control with data on the real activity carried out during the workday. It allows the team's performance to be evaluated with objective, documented criteria.

### Access by role

| Role | Access |
|---|---|
| Owner | All branches |
| Manager | The branches they manage |
| Supervisor | Their direct team, if the manager enables it |
| Worker | Only their own tasks from the app |

---

## Consumption report (inventory)

Exclusive to the inventory add-on. It answers **where material goes and what it costs**: it groups a period's consumption by item, task, employee, branch or warehouse, valued at each item's cost, and exports to CSV along with the movement ledger. It is opened from the Inventory section. See [Consumption report and movements](../16-inventory/103-consumption-report-and-movements.md).

---

> **Note:** the cost and anomaly analyses contain especially sensitive information. Make sure only the roles with authorised access have active credentials on the platform. Periodically review the users with the Manager or Owner role in the team management section.

---

## "Equipment and PPE" report

Always listed in Reports; without the inventory add-on it appears in red and explains what it is and how to enable it. It is the proof for a labour inspection, in two sheets: **Handovers** (what was handed to each worker, with which documents and version, who handed it over, how they confirmed and whether the signature was verified, when and how it was returned) and **Equipment and inspections** (each unit with its status, who holds it and each document with its result and expiry). See [Equipment: documents, inspections and handovers](../16-inventory/104-equipment-documents-inspections-and-handovers.md).

## Related articles

| Article | Description |
|---|---|
| [Generate and filter reports](./77-generate-and-filter-reports.md) | Steps for generating a report with custom filters |
| [Export data](./78-export-to-excel-and-csv.md) | Export formats and usage considerations |
| [Regulatory compliance report](./79-regulatory-compliance-report.md) | The report for RDL 8/2019 and the Labour Inspectorate |
| [Automatic reports](./80-automatic-reports.md) | Periodic sending by email: planned, not available |
| [Anomaly detection](../07-operational-intelligence/55-anomaly-detection.md) | How the automatic detection mechanism works |
