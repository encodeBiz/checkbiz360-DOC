# Report types available in CheckBiz360

CheckBiz360 centralises your company's operational information in two distinct forms, and it is worth not confusing them:

- **Downloadable reports**, generated on demand from the **Reports** section, filed in the history and downloaded as a file. There are two today: the **attendance report** (PDF or Excel) and the **task report** (Excel).
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
- Filters by branch and by task status.
- The data needed to calculate whatever is required in the spreadsheet: completed versus assigned, overdue, rejected.

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

> **Note:** the cost and anomaly analyses contain especially sensitive information. Make sure only the roles with authorised access have active credentials on the platform. Periodically review the users with the Manager or Owner role in the team management section.

---

## Related articles

| Article | Description |
|---|---|
| [Generate and filter reports](./77-generate-and-filter-reports.md) | Steps for generating a report with custom filters |
| [Export data](./78-export-to-excel-and-csv.md) | Export formats and usage considerations |
| [Regulatory compliance report](./79-regulatory-compliance-report.md) | The report for RDL 8/2019 and the Labour Inspectorate |
| [Automatic reports](./80-automatic-reports.md) | Periodic sending by email: planned, not available |
| [Anomaly detection](../07-operational-intelligence/55-anomaly-detection.md) | How the automatic detection mechanism works |
