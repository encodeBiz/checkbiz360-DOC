# Multi-branch global view

CheckBiz360's global dashboard is the consolidated supervision tool for organisations operating across several branches. From a single screen, managers can see the attendance status of the whole organisation in real time, compare performance between sites, detect anomalies and export consolidated data without having to navigate branch by branch. This article describes the global dashboard's features and how to get the most out of them.

## Who this view is for

The global view is designed for profiles supervising operations at scale: operations directors with several stores, HR leads at multi-site companies, regional managers or anybody who needs an overall picture before going into the detail of each branch.

A typical use case is that of an operations director with 20 stores who, at 9:30 in the morning, wants to know in under a minute how many stores have employees who have not yet clocked in, which sites are operating with full staff and where there is a critical anomaly requiring immediate attention.

## How to access the global dashboard

1. Go to the web back office and sign in with an **Owner** or **Manager** role with access to multiple branches.
2. In the side menu, select **Global dashboard** or **Dashboard**.
3. The system will automatically load the consolidated view with the current day's data.

## Consolidated attendance view for today

The global dashboard's main section shows, for the current day, the attendance status of every employee at every branch the user has access to. The information is organised by branch and makes it possible to identify each site's situation immediately.

### Global KPIs

At the top of the dashboard, the day's key attendance indicators are shown:

- **Employees present**: number and percentage of employees who have clocked in and are currently on shift.
- **Absences**: employees who should have clocked in and have not. A distinction is made between justified absences (recorded with approved leave) and unjustified ones (with no record and no justification).
- **Anomalies**: clock records automatically flagged by the system as suspicious or irregular, including late entries, early exits, clock-ins outside the geofence and incomplete workdays.
- **Active breaks**: employees who are on a break at this moment.

The KPIs update in real time as employees clock in throughout the day.

## Filters by branch

The global dashboard lets you filter the data to view only the branches that interest you at each moment. The filters available are:

- **By specific branch**: select one or several branches from the list to see only their data.
- **By region or group**: if your organisation has grouped branches by region or type, you can filter by that grouping.
- **By status**: enable the anomalies filter to see only the branches with active incidents.

Filters are cumulative and persistent during the session. If you leave the global dashboard and return, the filters applied will be retained.

## Comparisons between branches

The comparisons section allows the relative performance of branches to be analysed over time. The metrics available for comparison include:

### Cost and efficiency

- **Total hourly cost**: sum of the cost of the hours worked by all the employees at each branch in the selected period.
- **Average cost per employee**: hourly cost divided by the number of active employees at the branch.
- **Hours worked vs. planned hours**: percentage of compliance with the planned schedule.

### Attendance and punctuality

- **Punctuality rate**: percentage of entry clock records made within the configured tolerance margin.
- **Absence rate**: percentage of absences against the total workdays planned in the period.
- **Anomalies per employee**: average number of anomalies per employee in the period, useful for identifying branches with systematic compliance problems.

The comparisons can be viewed as a table or as a bar chart. The analysis period is configurable: today, this week, this month or a custom range.

> **Warning:** Cost comparisons are more accurate when every employee has their hourly cost correctly configured on their record. If an employee has no cost configured, those hours are counted as zero cost and can distort the branch's metrics.

## Exporting consolidated data

From the global dashboard you can export a report with the data of all the selected branches in a single file. The process is as follows:

1. Apply the branch and period filters you want to include in the report.
2. Press the **Export** button in the top right corner of the dashboard.
3. Select the export format: CSV for analysis in spreadsheets or PDF for executive reports.
4. The system will generate the file and download it automatically. For large volumes of data (more than 90 days or more than 50 branches), generation may take a few seconds and the file will also be sent by email to the user's address.

The consolidated report includes, for each branch, the summary of hours worked, absences, anomalies and cost for the selected period.

## Active alerts on the global dashboard

The global dashboard includes an alerts section grouping all the active incidents across the whole organisation in real time. From here you can:

- See which branches have unresolved alerts.
- Go straight to the problematic record with a single click.
- Assign the handling of an alert to a specific manager.

---

> **Role note:** The global dashboard is available to the **Owner** and **Manager** roles. The Owner sees every branch in the organisation. The Manager sees only the branches they are assigned to. The **Supervisor** role has no access to the global dashboard; they only access their branch's view.

## Related articles

- [Create and manage branches](57-create-and-manage-branches.md)
- [Assign employees to branches](60-assign-employees-to-branches.md)
- [Organisation configuration](61-organisation-settings.md)
- [Notification types](../09-notifications/63-notification-types.md)
- [Alerts for managers](../09-notifications/66-alerts-for-managers.md)
