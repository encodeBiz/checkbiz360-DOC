# Strict and flexible workday

CheckBiz360 does not count hours worked in a single way: each calendar decides whether it applies the **official schedule** or the **time actually worked**. That decision is made with one switch, **Strict workday / Flexible workday**, and it is probably the setting with the greatest impact on hours reports.

There is an equivalent switch for breaks, following the same logic.

---

## Strict workday

With a strict workday, **the configured schedule governs**. The system does not recognise time worked outside the official window:

- Entries **before** the schedule are not counted.
- Late entries and early exits **are deducted**.
- Exits **after** the schedule are not counted as extra time.

This is the right option when the working day is fixed by collective agreement or internal policy and you do not want the habit of arriving ten minutes early to end up generating overtime in the report. The employee who arrives at 08:50 for a 09:00 shift does not accumulate those ten minutes; the one who arrives at 09:10 does see the delay deducted.

## Flexible workday

With a flexible workday, **what the employee recorded governs**:

- The actual workday worked is counted.
- Time worked before or after the schedule **is added as extra**.
- Late arrivals and early exits **are deducted**.

This is the right option when the schedule is a reference and what you want to measure is effective commitment: field teams, services with workload peaks, shifts that run long out of operational necessity.

> **Important:** neither mode changes what the employee records. The clock record always stores the real time; what changes is how that time is counted when calculating time worked. The traceability of the original record is preserved in both cases.

---

## How it is configured

1. Open the schedule you want to adjust: the organisation's in **Schedules** → **General settings**, or a branch's or an employee's from their record.
2. Under **Working day and break rules**, find the workday card.
3. Choose **Strict schedule** or **Flexible working day**. The card's text summarises the counting rules that will apply, so there is no doubt about what is being chosen.
4. Save the calendar.

Being part of the calendar, it follows the same **inheritance** as the rest of the configuration: what is defined at the organisation flows down to the branches, and what is defined at a branch flows down to its employees, unless that level has its own configuration. See [Configuration inheritance](./26-configuration-inheritance.md).

---

## Strict and flexible breaks

Breaks have their own switch, with one important difference from the workday: **it changes what the employee has to do**.

| Mode | How it is counted | What the employee does |
|---|---|---|
| **Strict break** | Exactly the configured duration is applied. Longer or shorter breaks are not recognised | **Does not mark** the start or end of the break |
| **Flexible break** | The actual break time is counted, based on the effective duration | **Marks** the start and end of each break from the app |

With a strict break you also state the **duration in minutes** that the system will deduct from the workday.

The choice depends on the actual operation: the strict break simplifies things —nobody has to remember to clock the break— but does not reflect deviations; the flexible one reflects what happened, at the cost of requiring two more clock records a day.

---

## How to choose between them

| Situation | Recommendation |
|---|---|
| Working day fixed by collective agreement, with no overtime | Strict workday |
| You want to prevent early arrivals from generating extra time | Strict workday |
| Field teams or services with a variable workday | Flexible workday |
| Overtime actually worked is paid or compensated | Flexible workday |
| Fixed lunch break, the same every day | Strict break |
| Variable breaks depending on workload | Flexible break |

> **Warning:** changing mode affects the counting of workdays recorded from that moment onwards. Before changing it in an organisation with activity under way, consider timing it to coincide with the start of a payroll period so that the month's report does not mix two counting criteria.

---

## Related articles

| Article | Description |
|---|---|
| [Base schedules and shifts](./23-base-schedules-and-shifts.md) | Configuring the weekly schedule and several shifts per day |
| [Schedule exceptions](./25-schedule-exceptions.md) | One-off adjustments to the inherited schedule |
| [Configuration inheritance](./26-configuration-inheritance.md) | Priority between organisation, branch and employee |
| [Breaks and pauses](../03-time-tracking/17-breaks-and-pauses.md) | How breaks are recorded from the app |
| [How clocking in works](../03-time-tracking/13-how-clocking-in-works.md) | The validations applied on every clock-in |
