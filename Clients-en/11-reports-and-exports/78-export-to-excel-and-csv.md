# Exporting data: attendance and tasks

CheckBiz360 gets data out of the platform through **reports**: the attendance one, in **PDF or Excel (XLSX)**, and the task one, in **Excel (XLSX)**. This article describes both, the data they include and the practical considerations for their use.

---

## Exporting the employee directory

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

The **Employees** list does not currently generate a downloadable file. What does work is the opposite direction: **importing** employees from a CSV, useful when getting the platform up and running with a large headcount.

If you need a complete extraction of the directory, request it from support at hola@encodebiz.com. See [Export the employee list](../02-employees/12-export-employee-list.md).

---

## Downloading the attendance report (PDF or Excel)

The attendance report is generated on demand from the back office and can be downloaded in **PDF** or in **Excel (XLSX)**. There is no automatic or scheduled generation; each report is launched by the manager when they need it.

Choose the format according to use: **PDF** to present or file —it is the one that suits an inspection— and **Excel** to work the data in a spreadsheet or pass it to your accountancy firm.

### How to generate and download the attendance report

1. Sign in to the back office with an Owner or Manager role.
2. Go to the **Reports** section.
3. Generate a new report and select the *Working-time record* type.
4. Choose the **format**: PDF or Excel (XLSX).
5. Configure the **period** and, if you need to, filter by branch or employee.
6. Generate the report. It will appear in the history with its type and its format.
7. Download it from the history, as many times as you need.

### Fields included in the attendance report

| Field | Description |
|---|---|
| Name | The employee's full name |
| Branch | The branch the employee is assigned to |
| Date | Date of the record (DD/MM/YYYY format) |
| Entry time | Timestamp of the entry record |
| Exit time | Timestamp of the exit record |
| Hours worked | Total hours and minutes of the workday recorded |
| Status | Complete, justified absence, unjustified absence, partial workday |

---

## Downloading the task report (Excel)

The task report is generated in the same way as the attendance one, by selecting the *Task report* type. It is produced only in **Excel (XLSX)**.

It supports filters by **branch** and by task **status**. The period applies to each task's **deadline**, not to its creation date: a July report gathers the tasks that were due in July, even if they were created earlier.

If no task meets the filters, the system says so and does not generate an empty file.

---

## Exporting the operational intelligence dashboards

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Direct export of the dashboard data —costs, anomalies and comparisons between branches— to Excel or CSV is planned for a future version. Today that data is consulted on screen; what can be exported are the attendance and task reports described above.

---

## GDPR considerations when exporting employee data

Exported files contain employees' personal data within the meaning of the General Data Protection Regulation (GDPR). The company, as data controller, should bear the following in mind when handling these files:

- **Secure storage.** Exported files have to be kept in locations with restricted access. They should not be stored in shared folders without access control or in cloud storage services without encryption or permission management.
- **Protected transmission.** If you send the file by email to your accountancy firm or other external recipients, use encrypted channels or protect the file with a password.
- **Data minimisation.** Export only the fields and the data period necessary for each specific purpose.
- **Record of activities.** If your company is required to keep a record of processing activities under Article 30 of the GDPR, the export and transmission of employee data has to be documented in that record.
- **Retention period.** Exported files have to be deleted once their purpose has been fulfilled, unless there is a legal obligation to retain them.

> **Warning:** CheckBiz360 keeps the original data stored on the platform with the security measures required by the applicable regulations. Once the data has been exported and has left the platform, the security of those files is your company's responsibility.

---

> **Note:** Access to the export functions requires an Owner or Manager role.

---

## Related articles

| Article | Description |
|---|---|
| [Report types available](./76-report-types.md) | What each report type contains and who can access it |
| [Generate and filter reports](./77-generate-and-filter-reports.md) | Steps for generating a report with custom filters |
| [Regulatory compliance report](./79-regulatory-compliance-report.md) | The report for RDL 8/2019 |
| [Data retention and protection](../12-regulatory-compliance/83-data-retention-and-protection.md) | Legal basis and employees' rights over their data |
