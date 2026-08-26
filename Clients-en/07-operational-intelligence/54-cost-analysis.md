# Cost analysis

## What it is for

CheckBiz360's cost analysis module translates attendance data into financial information that management control can use directly. The aim is for management to be able to answer at any moment questions such as: how much has it really cost to operate this branch this week? Which employee has the highest cost per hour actually worked? In which periods are we deviating most from the staffing budget?

The system requires no integration with payroll or access to external accounting data. It works only with two variables: the real hours recorded on the platform and the hourly rate configured for each employee.

## Configuring the employee's cost per hour

The starting point is defining each employee's **hourly rate**. It is configured **in the employee's link with their branch**, not in their personal details: the same person can have different rates at different sites, alongside their position and their responsibility there.

To configure it:

1. Go to **Employees** and open the employee's record.
2. Go to the branches section and open the link with the relevant site.
3. Enter the rate alongside the position and the responsibility.
4. Save the changes.

The value should reflect the **real cost to the company**, not the gross salary: include the proportional share of employer social security contributions if you want a realistic total cost.

> **Important:** without a configured rate there is no possible cost analysis. It is the most frequent cause of the financial indicators appearing empty or strange. The **data status** block of the Operations dashboard indicates this configuration coverage: consult it before accepting —or dismissing— any cost figure.

## What the system calculates

From the recorded hours and the configured rate, the employee's record shows:

| Indicator | What it shows |
|---|---|
| **Cost per hour worked** | The real unit cost of an effective hour |
| **Cost per workday** | The average cost of a working day |
| **Cost per output** | The cost weighted by the effectiveness observed |
| **Return on cost invested** | What is obtained for each unit of cost |
| **Accumulated cost** | The real total for the period |

All are calculated on **validated workdays** and compared against the consolidated history of the employee or site themselves, not against a budget: the platform does not manage budgets or planned costs.

## Comparisons between branches

The Operations dashboard allows sites to be compared with each other within a period. Cost, however, no longer presides over the reading: it is not a measure of operability but a consequence, which is why it lives inside each site's and each person's profile, rather than as a tab of its own.

The comparisons make it possible to detect situations that a branch-by-branch analysis does not reveal:

- A branch with a greater employee presence may have a higher cost per hour actually worked than one with fewer staff if the first accumulates more unplanned overtime.
- Two branches with similar budgets can have very different cost deviations depending on the time discipline of their teams.
- Identifying the branch with the greatest cost efficiency does not mean it is better managed, but it does indicate where time management practices are working better.

## Cost-overrun alerts and configurable thresholds

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

In a future version, CheckBiz360 will allow automatic alerts to be configured that will trigger when a branch's or an employee's cost deviation exceeds a user-defined threshold. The alerts will be sent to the Manager and the Owner as a back office notification and, optionally, by email. For now, cost analysis is a metric visible on the dashboards that has to be consulted manually.

## Export for management control

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Exporting cost analysis data in CSV and PDF format is not available in the current version. The data can be consulted directly from the back office cost panel, but cannot be downloaded at this time. This export capability is planned on the platform's roadmap.

## Related articles

- [What operational intelligence is](49-what-is-operational-intelligence.md)
- [Operational efficiency index](52-efficiency-index.md)
- [The Operations dashboard](56-dashboards.md)
- [Report types](../11-reports-and-exports/76-report-types.md)
- [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md)
