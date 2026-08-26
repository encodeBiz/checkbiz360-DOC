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

## How CheckBiz360 blocks clock-ins on non-working days

When an employee tries to record their entry or exit on a date marked as non-working in their effective calendar, the system returns the error code `checklog/day_disabled` and rejects the clock-in.

This block operates before any other validation. The system does not check the location or the active shift if the day is marked as non-working: the rejection is immediate.

Clock-in attempts on non-working days are recorded in the history with their timestamp, the device used and the error code, which lets the manager detect whether an employee is trying to clock in on a day that does not apply to them.

---

## What happens if the company works on public holidays

There are sectors in which working on public holidays is the norm: retail, hospitality, transport and emergency services operate normally on days that are non-working for other companies.

CheckBiz360 allows a holiday to be disabled on a one-off basis so that the employees affected can clock in normally that day.

### Disabling a holiday on a one-off basis for the whole branch

1. Sign in to the back office with the owner or manager role.
2. Navigate to **Branches** and select the branch that works that day.
3. Go to **Calendar** in the side menu.
4. Find the holiday's date in the list of non-working days.
5. Select the entry and press **Disable for this date**.
6. Confirm the action. The date stops being blocked for that branch's employees.

### Disabling a holiday only for specific employees

If only some of the employees work on the holiday (for example, customer service staff but not administration), the most precise way of handling this is through individual exceptions:

1. Go to the record of each employee who works that day.
2. Create a one-off exception for that date marking the day as a working day and defining the corresponding shift.
3. Employees with an exception will be able to clock in that day. The rest will continue with the holiday block.

> **Warning:** Remember that individual exceptions take priority over the branch calendar. An individual exception marking a holiday as a working day allows the employee to clock in even if that holiday is active at organisation or branch level.

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
- [Statuses and error codes](../03-time-tracking/22-statuses-and-error-codes.md)
