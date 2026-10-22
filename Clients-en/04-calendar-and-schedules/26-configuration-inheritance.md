# Configuration inheritance: how the effective calendar is resolved

When an employee clocks in, the system needs to determine which schedule to apply at that specific moment. This determination is not made by consulting a single value: the system walks a hierarchical chain of configurations and applies the rule that is closest to the employee. This mechanism is known as configuration inheritance, or the schedule cascade.

---

## The three levels of the hierarchy

CheckBiz360 organises schedule configuration into three levels:

1. **Organisation:** The most general level. Defines the parameters that apply across the whole organisation.
2. **Branch:** The intermediate level. A branch can have its own configuration that partially or entirely replaces the organisation's.
3. **Employee:** The most specific level. An employee's individual exceptions have absolute priority over any higher-level configuration.

The fundamental rule is that the configuration closest to the employee always wins.

---

## The cascade resolution algorithm

When the system needs to know an employee's effective schedule for a specific date and time, it runs the following process:

1. It checks whether the employee has an active individual exception for that day (one-off exception) or for that day of the week (recurring exception).
2. If an individual exception exists, it uses it as the effective schedule and stops searching. It does not consult the higher levels.
3. If there is no individual exception, it checks whether the employee's branch has its own schedule configured.
4. If the branch has its own schedule, it uses it as the effective schedule and stops searching.
5. If the branch has no schedule of its own, it consults the organisation's schedule and uses that.

This process guarantees that a valid effective schedule always exists, even if the intermediate levels have no configuration of their own.

---

## A concrete example with three different levels

Consider the following configuration in a company with a head organisation and a branch in a different city:

| Level | Day | Start | End |
|---|---|---|---|
| Organisation | Monday to Friday | 09:00 | 17:00 |
| Madrid branch | Monday to Friday | 08:30 | 16:30 |
| Employee García | Monday to Friday | 07:00 | 15:00 (recurring exception) |

The employee García works at the Madrid branch. Their effective schedule is neither the organisation's (09:00–17:00) nor the branch's (08:30–16:30), but their individual exception (07:00–15:00). If García clocks in at 07:05, the system accepts it because it falls within their effective shift.

An employee at the Madrid branch with no individual exception will clock in under the branch schedule (08:30–16:30). An employee at a branch with no configuration of its own will inherit the organisation's schedule directly (09:00–17:00).

---

## Which configurations are inherited and which are not

Inheritance does not work the same way for every parameter. In general terms:

- The **public holiday calendar** accumulates: the organisation's holidays plus the branch's own holidays make up the non-working day calendar for that branch's employees.
- The **shift schedule** is replaced: if the branch has its own schedule, it completely replaces the organisation's. They are not merged.
- An employee's **individual exceptions** completely replace the higher level's schedule for the dates or days they apply to.
- How the **schedule is set** is inherited too: if a branch is on **Calendar**, its employees are as well, except anyone with another mode on their record. **Schedule from tasks** is the exception: it is only chosen on each person's record. See [Calendar: shifts loaded by date](114-shift-calendar-by-date.md).

> **Note:** The accumulation behaviour for holidays means an employee at a local branch can inherit both the organisation's national holidays and their branch's local holidays. This is intentional and reflects the regulatory reality of most companies.

---

## How to debug an employee's effective schedule in the back office

If a manager needs to verify which schedule an employee is using at a given moment, they can check it from the back office by following these steps:

1. Sign in to the back office with the owner or manager role.
2. Navigate to **Employees** and select the employee whose schedule you want to review.
3. Open the **Effective calendar** section.
4. The system shows the current month's calendar with the origin of each configuration: whether the day uses the organisation's schedule, the branch's or an individual exception is indicated clearly.
5. To consult a different month, use the calendar's navigation controls.
6. To see the detail of a specific day (active shifts, time windows, exceptions applied), click on the day's cell.

This tool is the first place to look when an employee reports that they could not clock in or that the system validated their entry at an unexpected time.

---

## Common errors related to inheritance

### The employee cannot clock in when they should be able to

Check that there is no individual exception marking that day as non-working. Individual exceptions prevail over the branch schedule, so an active exception may be blocking valid clock-ins.

### The employee can clock in at a time that does not correspond to them

Check whether there is an active recurring exception with a wider time window than the branch schedule's. If there is, the system will use it instead of the standard schedule.

### The branch has a holiday but the employee can clock in

The employee may have an individual exception marking that day as a working day. Individual exceptions override higher-level holidays when they are explicitly configured.

> **Warning:** Before contacting support about unexpected behaviour in an employee's clock-in, always review the effective calendar from the back office. Most incidents originate in an incorrectly configured individual exception or in a holiday that was not removed after becoming obsolete.

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Work calendar](24-work-calendar.md)
- [Schedule exceptions](25-schedule-exceptions.md)
- [Rotating shifts](27-rotating-shifts.md) — not available in the current version; alternatives
- [Strict and flexible workday](28-flexible-schedule.md)
- [Public holidays and non-working days](29-public-holidays-and-non-working-days.md)
- [Calendar: shifts loaded by date](114-shift-calendar-by-date.md)
