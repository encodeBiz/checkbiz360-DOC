# Rotating shifts

In sectors such as manufacturing, logistics, healthcare or hospitality, the working day is not uniform from one week to the next: teams alternate time bands following a cycle. This article explains how that need is covered in CheckBiz360.

---

## Feature status

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

CheckBiz360 **does not have a rotating schedule type** with an automatic alternation cycle: there is no "week A / week B" configuration with an anchor date that the system resolves on its own. The weekly schedule configured for an organisation, branch or employee repeats identically every week.

---

## How to cover rotation with what exists today

There are three ways of operating with rotating teams. The choice depends on whether the rotation is stable or changes frequently.

### Option 1: one branch per shift (stable rotation)

If the shifts are fixed and it is the people who rotate, configure **one branch per time band** —for example "Plant - Morning" and "Plant - Afternoon", with the same coordinates and the same geofence— and move the employee's assignment from one to the other when their turn to change comes.

This is the cleanest option: each branch has its schedule, its holidays and its effective calendar, and the clock record history is attributed to the band that was actually worked.

### Option 2: a custom schedule on the employee (variable rotation)

If the rotation is irregular, configure the schedule on the **employee's** record instead of inheriting it from the branch, and adjust it when the cycle changes. The employee's calendar takes priority over their branch's.

It is more flexible, but it requires maintaining the change by hand on each cycle and for each person.

### Option 3: the By shifts mode (planned rotation)

If you plan the weeks in advance, put the branch on the **By shifts** mode and load each person's shifts week by week. **Copy to next week** repeats a week and then you adjust whatever changes, and the roster importer loads the whole branch's week from Excel. The cycle is not generated on its own, but there is no schedule to change when moving from one week to the next. Bear in mind that, **By shifts**, a week with nothing loaded is off entirely. See [By shifts: the schedule is the shifts you load](114-shift-calendar-by-date.md).

> **Warning:** in the first two options, change the schedule **before** the new cycle starts. Every clock record is validated against the effective calendar in force at that moment; updating the schedule afterwards does not re-evaluate records already stored.

---

## Example: alternating morning and afternoon

A logistics company needs cover from 07:00 to 15:00 and from 15:00 to 23:00, with two teams alternating each week.

With Option 1, two branches are created over the same warehouse:

| Branch | Monday to Friday schedule |
|---|---|
| Warehouse - Morning | 07:00 – 15:00 |
| Warehouse - Afternoon | 15:00 – 23:00 |

Each changeover Monday, the manager reassigns the employees from one branch to the other. Each week's clock records are validated against the correct schedule and the reports distinguish the activity of each band.

---

## Rotation and public holidays

Public holidays apply by date, regardless of which shift fell on that day: a holiday configured at the organisation or at the branch disables the day for every employee who inherits that calendar, and a clock-in attempt returns `checklog/day_disabled`.

If your organisation works on public holidays by shift, do not mark the day as a holiday at the branch: treat it as a working day and record the absences of those who are off on each employee's record. See [Public holidays and non-working days](./29-public-holidays-and-non-working-days.md).

---

## Related articles

| Article | Description |
|---|---|
| [Base schedules and shifts](./23-base-schedules-and-shifts.md) | Configuring the weekly schedule and several shifts per day |
| [Work calendar](./24-work-calendar.md) | Public holidays and the effective calendar |
| [Schedule exceptions](./25-schedule-exceptions.md) | One-off adjustments to the inherited schedule |
| [Configuration inheritance](./26-configuration-inheritance.md) | Priority between organisation, branch and employee |
| [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md) | Moving an employee between sites or shifts |
