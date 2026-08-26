# Generate and filter reports

The reports module in the CheckBiz360 back office lets you obtain detailed documents about your team's activity in any period. This guide explains the complete process for generating a report, the filters available, how to preview the result before exporting and how to save frequent configurations for reuse.

---

## Accessing the reports module

To generate a report you have to sign in to the CheckBiz360 back office with an Owner, Manager or, if the manager has enabled it, Supervisor role.

1. Sign in to the back office from your browser.
2. In the left side menu, select the **Reports** section.
3. You will see the reports panel with the five types available: Attendance, Punctuality, Costs, Anomalies and Tasks.
4. Select the type of report you want to generate.

---

## Available filters

Before generating the report you can adjust the filter parameters. The more specific the filters, the more focused the result and the shorter the generation time.

### Date range

The date filter is required. The following predefined options are available:

- **Today:** the current day only.
- **This week:** Monday to Sunday of the current week.
- **This month:** the current calendar month.
- **Custom range:** select a start date and an end date in the calendar. It can span up to 12 consecutive months in a single query.

> **Warning:** Periods longer than three months can take several minutes to process, depending on the size of your headcount and the number of accumulated records. A progress bar will be shown during generation.

### Employee

You can filter by a particular employee or include all the employees in the scope you manage. If you select a specific employee, the report will show only their records.

### Branch

If your organisation has more than one branch, you can select a particular branch or include all of them. Owners and managers with multi-site access see every branch; managers with restricted access see only their own.

### Event type

Available in the attendance report. It lets you filter by record category:

- Entries and exits only.
- Absences (justified, unjustified or both).
- Manual corrections made by a manager.
- All the period's events.

---

## Preview before exporting

Once the filters have been configured, press **Preview** to see the report on screen before downloading it. The preview shows the same data the exported file will contain and makes it possible to spot potential errors in the filter selection without having to download the document.

In the preview you can:

- Navigate through the report's pages.
- Verify that the employees and dates included are correct.
- Check totals and subtotals.

If you find that the filters are not right, press **Back to filters** and adjust them without losing the partial configuration.

---

## Saving frequent report configurations

If you regularly generate the same type of report with the same parameters (for example, the monthly attendance report for a particular branch), you can save that configuration to reuse it.

1. Configure the filters you want.
2. Press **Save configuration**.
3. Give it a descriptive name, for example: "Monthly attendance — City Centre branch".
4. The configuration will be available in the **My saved reports** section, accessible from the module's main panel.

To run a saved configuration, select it from the list and press **Generate**. You will only have to adjust the date range if the configuration used a relative range such as "this month".

> **Note:** Saved configurations are personal to each back office user and are not shared between accounts.

---

## Generation time

Generation time depends on three factors: the number of employees included, the date range selected and the type of report.

| Scenario | Estimated time |
|---|---|
| Up to 20 employees, 1 month | Under 10 seconds |
| Up to 20 employees, 6 months | 10 to 30 seconds |
| More than 100 employees, 12 months | 1 to 5 minutes |

For long periods with large headcounts, we recommend starting the report generation and keeping the tab open. The system will notify you when the report is ready to download.

---

> **Note:** The Supervisor role can only generate reports if the manager has enabled that specific permission in their access configuration. If you do not see the reports section in the back office, contact your organisation's manager.

---

## Related articles

| Article | Description |
|---|---|
| [Report types available](./76-report-types.md) | Description of each report type and access by role |
| [Export data](./78-export-to-excel-and-csv.md) | Export formats and fields included |
| [Regulatory compliance report](./79-regulatory-compliance-report.md) | The specific report for RDL 8/2019 |
| [Automatic reports](./80-automatic-reports.md) | Periodic sending of reports by email |
