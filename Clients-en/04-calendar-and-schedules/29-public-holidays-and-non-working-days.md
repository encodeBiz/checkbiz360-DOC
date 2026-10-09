# Public holidays and non-working days

Managing public holidays is one of the most delicate aspects of attendance control, especially in companies operating across several regions or in sectors that routinely work on days that are non-working for others. CheckBiz360 offers a flexible system that allows clock-ins to be both blocked on holidays and enabled when the company's activity requires it.

---

## Types of holiday and non-working day

CheckBiz360 classifies non-working days into different categories that determine their scope within the configuration hierarchy:

### National public holiday

A national public holiday is a date declared non-working by state legislation that applies to the whole organisation. It is configured at organisation level and inherited automatically by all branches and employees.

### Regional public holiday

A regional public holiday applies only to the branches located in the corresponding region. It is configured at branch level so that it affects only the employees of that site.

### Local public holiday

Similar to the regional one, a local holiday applies to a specific municipality or area. It is managed at branch level, so that only that branch's employees are affected by the clocking block.

### Bridge day

A bridge day is a working day that the company, by internal decision, turns into a non-working day to give continuity to an official holiday. It is configured as an internal non-working day with a description identifying it.

### Internal non-working day

This category covers any date the company decides to block for its own reasons: closures for stocktaking, refurbishment, mandatory training with no regular workday, and so on.

---

## Employee absences

A specific person's holidays, leave and days off are recorded as **absences** in their calendar. They are added from the employee's record or from the [availability board](98-availability-board.md), and can also be consulted in the **Employee non-working days** tab in **Schedules**.

- **Date range.** An absence can cover several consecutive days. In the lists it appears as a single row with its start, its end and the number of days (for example, "1 – 15 Sep · 15 days"), which expands to view or remove individual days.
- **Paid.** Each employee absence carries a **Paid** box with three possible values: *paid*, *unpaid* or *not set*. *Not set* means it is not recorded —for example, in absences recorded before the box existed— and is displayed differently from *unpaid* so as not to confuse missing data with a "no". Organisation or branch public holidays do not carry this mark.

A day of absence blocks that person's clock-in just like a public holiday.

---

## How CheckBiz360 blocks clock-ins on non-working days

When an employee tries to record their entry or exit on a date marked as non-working in their effective calendar, the system returns the error code `checklog/day_disabled` and rejects the clock-in.

This block operates before any other validation. The system does not check the location or the active shift if the day is marked as non-working: the rejection is immediate.

Clock-in attempts on non-working days are recorded in the history with their timestamp, the device used and the error code, which lets the manager detect whether an employee is trying to clock in on a day that does not apply to them.

---

## What happens if the company works on public holidays

There are sectors in which working on public holidays is the norm: retail, hospitality, transport and emergency services operate normally on days that are non-working for other companies.

A configured public holiday applies to **all** the employees within its scope: there is no way to cancel it for just one branch or just one person. Not even a custom schedule with a shift that day gets round it; the clock-in is rejected with `checklog/day_disabled`. That is why the way to work on a public holiday is not to mark as a holiday what does not close.

### The whole branch works that day

- If the holiday is at the **branch**, delete it from its days off. The date stops being blocked for that branch's employees.
- If the holiday is at the **organisation**, it affects every branch. Remove it from the organisation and add it as a local holiday only at the branches that do close.

### Only part of the workforce works that day

If only some of them work (for example, customer service staff but not administration):

1. Do not mark the day as a holiday at the branch: treat it as a working day.
2. Record an **absence** that day for those who have the day off, from their record or from the [availability board](98-availability-board.md).
3. Those who work clock in normally; those with the absence are blocked.

> **Warning:** organisation, branch and employee holidays **add up**; they do not cancel each other out. The inheritance in which the employee's level prevails is that of the weekly schedule, not that of public holidays.

---

## Sector considerations

### Retail

Retail usually operates during bridge days, local holidays and even some national holidays. It is common to configure the branch with a calendar free of holidays and manage one-off closures (for example, Christmas or New Year) by manually adding the days the store stays closed.

### Hospitality and catering

Hospitality works virtually without interruption throughout the year, including the most significant holidays. In this sector it is advisable to leave the branch calendar clear of holidays and add only the days of actual closure of the establishment.

### Healthcare and emergency services

In these sectors, working on public holidays is part of the collective agreement. CheckBiz360 allows working time to be recorded on holidays without blocks and, if the company needs to identify the holidays worked in order to calculate salary supplements, it can use the working-time reports filtered by day type.

### Seasonal activities

Companies with seasonal activity (tourism, agriculture, events) may have periods in which they operate normally during holidays and others in which they stay closed. The recommended configuration in these cases is to define the holiday calendar at organisation level with the national holidays and manage each season's particularities through the branch calendar or through internal non-working days.

---

## Managing public holidays in advance

Configuring the holiday calendar at the start of each calendar year, or sufficiently far ahead of each holiday, is recommended. CheckBiz360 does not automatically apply the country's official holidays: the manager has to enter them manually or import them if the platform offers that feature under their subscription plan.

> **Note:** If a holiday is not configured in the calendar and employees clock in that day, the records will remain valid. There is no way to retroactively mark an already stored clock record as a "holiday worked" without reviewing and manually adjusting the records affected. Configuring the calendar in advance avoids this kind of incident.

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Work calendar](24-work-calendar.md)
- [Schedule exceptions](25-schedule-exceptions.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Rotating shifts](27-rotating-shifts.md) — not available in the current version; alternatives
- [Availability board](98-availability-board.md)
- [Statuses and error codes](../03-time-tracking/22-statuses-and-error-codes.md)
