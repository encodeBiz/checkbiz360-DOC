# Base schedules and shifts in CheckBiz360

The base schedule defines when an employee is expected to be present at their workstation. In CheckBiz360, this schedule is not configured employee by employee individually; it is defined at organisation or branch level and inherited automatically. This article explains what a base schedule is, how it is configured and how the system selects the active shift at the moment of each clock-in.

---

## What a base schedule is

The base schedule is the set of shifts that make up the standard working day for a group of employees. It is defined at the organisation or at each branch and specifies, for each day of the week, which shifts are active and in which time window they fall.

When an employee clocks in, the system consults their effective calendar and locates the shift corresponding to that moment. If the clock-in falls within the window of an active shift (according to the schedule and the configured workday mode), the record is accepted as valid.

---

## Shift types

### Single daily shift

This is the most common type of shift. The employee has a single continuous time window per day: one start time and one finish time.

The window is defined by four parameters:

- `start.hour` and `start.minute`: hour and minute the shift starts.
- `end.hour` and `end.minute`: hour and minute the shift ends.

For example, a standard morning shift could be configured with `start.hour: 9`, `start.minute: 0`, `end.hour: 17`, `end.minute: 0`.

### Multiple shifts per day

Some companies structure the working day into two blocks: morning and afternoon. In these cases it is possible to define two shifts for the same day, each with its own time window.

A typical example would be a morning shift from 09:00 to 14:00 and an afternoon shift from 16:00 to 20:00. The employee makes two entry records and two exit records, one for each block.

The system evaluates the clock-in against the shift whose time window corresponds to the moment of the record. If the employee clocks in at 09:05, the system links it to the morning shift. If they clock in at 16:00, it links it to the afternoon shift.

The exit follows the same rule: it is attributed to the shift that contains the exit time and, if all of them have already ended, to the last one that started, which is the one being closed late. With a strict workday, an exit at 20:10 on a day of 09:00–14:00 and 16:00–20:00 is adjusted to the end of the afternoon shift, not the morning one.

---

## How the system selects the active shift

At the moment of the clock-in, the system goes through the day's active shifts and determines which one is in force at that instant. The selection is based on comparing the time of the clock-in with the time windows of the shifts defined for that day.

If there are several shifts in the day, the system selects the one whose time window includes the moment of the clock-in. If the clock-in falls between two shifts —for example, during the break between the morning and afternoon blocks— the system rejects it with the code `checklog/out_of_schedule`.

> **Note:** whether time worked outside the window counts or not depends on the workday mode —strict or flexible— configured in the calendar. This is explained in detail in [Strict and flexible workday](28-flexible-schedule.md).

---

## The working week: working days and disabled days

The base schedule does not only define the time windows, but also which days of the week are working days for that employee or branch.

For each day of the week it is possible to indicate whether it is enabled or disabled. A disabled day is equivalent to a non-working day: if an employee tries to clock in on a day marked as disabled, the system returns the code `checklog/day_disabled`.

### Configuring the days of the week

Configuring working days is done from the back office:

1. Sign in to the back office with a role that has editing permissions (owner or manager).
2. For the organisation's schedule, open **Schedules** in the side menu and the **General settings** tab. For a branch or an employee, open their record: the schedule is inherited while **Use base schedule** is enabled, and when you disable it you can define a **Custom schedule**.
3. In the **Weekly schedule**, switch each day on or off. A day that is switched off shows "No shifts defined".
4. Add the shifts for the active days.
5. Press **Save calendar**. You are asked to confirm, and in that same step you can also save the schedule as a template (see [Schedule templates](#schedule-templates)).

Changes to working days take effect immediately on the effective calendar of every employee who inherits that schedule.

### If there is no schedule yet

The working-time record is a legal obligation and cannot fail because the schedule has not been configured yet. That is why, **while no schedule exists at any level** —not at the organisation, not at the branch and not at the employee, or there is not a single shift in the whole week—, the clock-in is accepted with an open window from 00:00 to 23:59.

It is only a safety net for the first few days: without a schedule there is no way of knowing whether someone arrived late or worked extra hours. The back office onboarding guide asks for it to be configured before anything else.

As soon as a schedule is defined, that schedule governs: a week configured with every day switched off **closes** those days, and the clock-in is rejected with `checklog/day_disabled`.

> **Important warning:** Disabling a working day affects every employee who inherits the schedule from that organisation or branch. If you need to disable a day for one specific employee only, use the individual schedule exceptions described in the article [Schedule exceptions](25-schedule-exceptions.md).

---

## Configuring the base schedule at the organisation and at the branch

The base schedule can be configured at two levels:

- **Organisation level:** Defines the general schedule that applies across the whole organisation. It is the starting point of the hierarchy.
- **Branch level:** Allows each branch to have a different schedule from the organisation's. If a branch has its own schedule configured, that branch's employees inherit the branch schedule instead of the organisation's.

This architecture is especially useful in companies with multiple sites operating in different time bands or with different working days.

It can also be configured at **employee level**, for those who have their own schedule different from their branch's.

---

## Breaks within the shift

In addition to shifts, each day supports **breaks** with their start and finish times. They are configured in the same weekly schedule, under the corresponding day, and several can be added.

How those breaks are counted —with the fixed duration configured or with the actual time the employee marks— depends on the break mode chosen. See [Strict and flexible workday](28-flexible-schedule.md).

---

## Schedule templates

Configuring the weekly schedule site by site is repetitive when several branches share the same pattern. To avoid this, a schedule can be **saved as a template** and applied later wherever it is needed.

- **Saving a template.** In the general settings, press **Save calendar**; in the confirmation, tick **Save as template** and give it a name. In a branch's or an employee's record, use the **Save as template** button.
- **Applying a template.** In **Select a template**, choose the one you want: when you choose it, it is loaded onto the schedule you are editing. Review the result and save.
- Templates that fall out of use can be deleted.

The template is a copy of the **schedule already saved**, not of what is on screen. That is why, when creating a branch or an employee, **Save as template** is disabled until the record exists: save first and create the template afterwards.

It is the practical way to set up a new branch with the same schedule as the others without redoing it day by day.

---

## Related articles

- [Work calendar](24-work-calendar.md)
- [Schedule exceptions](25-schedule-exceptions.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Rotating shifts](27-rotating-shifts.md) — not available in the current version; alternatives
- [Strict and flexible workday](28-flexible-schedule.md)
- [Public holidays and non-working days](29-public-holidays-and-non-working-days.md)
- [Availability board](98-availability-board.md)
