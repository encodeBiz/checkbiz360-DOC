# The work calendar in CheckBiz360

The work calendar is the record of non-working days that the system consults on every clock-in to determine whether that day is enabled for work. In CheckBiz360, this calendar can be configured at different hierarchical levels, which allows the same organisation to manage common national public holidays alongside local holidays specific to each branch.

---

## What the work calendar is

The work calendar in CheckBiz360 is a list of dates that the system marks as non-working. When an employee tries to clock in on one of those dates, the system detects it and returns the code `checklog/day_disabled`, rejecting the clock-in.

This mechanism protects the integrity of attendance records and prevents workdays from being generated on days when the company, by regulation or internal policy, does not operate.

---

## Types of non-working day

CheckBiz360 allows each calendar entry to be classified according to its scope:

- **National public holiday:** Applies to the whole organisation and, by inheritance, to all its branches and employees.
- **Regional or local holiday:** Configured at branch level. It only affects the employees of that specific branch.
- **Internal non-working day:** Any date the company decides to mark as non-working for its own reasons (closure for stocktaking, company bridge day, etc.).

Each type has a different scope within the configuration hierarchy, as detailed in the next section.

---

## The entity → branch → employee hierarchy

The work calendar follows the same three-level hierarchy as the rest of the configuration in CheckBiz360: organisation, branch and employee.

### Organisation level

Public holidays configured at the organisation apply by default to every employee in the organisation, regardless of the branch they belong to. This is the right level for managing national holidays or corporate closures.

### Branch level

Each branch can have its own calendar of additional non-working days. These days are added to the holidays inherited from the organisation. A holiday configured at one branch does not affect the other branches.

### Employee level

A specific employee can have their own non-working days: holidays, leave or any absence. They are added to the public holidays of the organisation and of their branch, and only affect that employee.

> **Important:** public holidays **add up** across levels; they do not cancel each other out. An organisation or branch holiday applies to all its employees even if one of them has a custom schedule with a shift that day: the clock-in is still rejected with `checklog/day_disabled`. The inheritance in which the level closest to the employee prevails is that of the **weekly schedule**, not that of public holidays. If in your organisation only part of the workforce works on a public holiday, see [Public holidays and non-working days](29-public-holidays-and-non-working-days.md#what-happens-if-the-company-works-on-public-holidays).

Each non-working day shows which level it comes from —organisation, branch or employee—, so that on the employee's record you can tell what the company closes apart from what is the employee's own absence.

---

## How to add a public holiday

To add a holiday to the work calendar, follow these steps:

**At organisation level:**

1. Sign in to the back office with the owner role.
2. Open **Schedules** in the side menu and go to the **General settings** tab.
3. Under **Entity holidays**, press **Add holiday**.
4. Enter the holiday's name and select the date; if you wish, add a description.
5. Press **Save holiday**.

**At branch level:**

1. Sign in to the back office with the owner or manager role.
2. Open the record of the relevant branch.
3. In the branch's **days off** block, add the holiday with the same details.

**At employee level:** a person's absences are recorded from their record or directly from the [availability board](98-availability-board.md). The **Employee non-working days** tab in **Schedules** lets you search for an employee and consult their non-working days with their origin. An absence can cover a **date range** and carry the **Paid** mark; this is explained in [Public holidays and non-working days](29-public-holidays-and-non-working-days.md#employee-absences).

Changes take effect immediately. Once the holiday has been saved, any attempt to clock in on that date by the employees affected will be blocked.

---

## Impact on clock records

When an employee tries to record their entry or exit on a date marked as non-working in their effective calendar, the system returns the error code `checklog/day_disabled`.

This error is recorded in the employee's history with its timestamp and the data of the attempt. No workday is generated and no hours are counted.

| Situation | Result |
|---|---|
| Clock-in on an active working day | Normal validation process. |
| Clock-in on an organisation holiday | `checklog/day_disabled`. Clock-in rejected. |
| Clock-in on a branch holiday | `checklog/day_disabled`. Clock-in rejected. |
| Clock-in on a day disabled in the base schedule | `checklog/day_disabled`. Clock-in rejected. |
| Clock-in on one of the employee's own non-working days (holiday, leave) | `checklog/day_disabled`. Clock-in rejected. |
| Clock-in with a recorded absence covering that day | `checklog/absence`. Clock-in rejected. |

From version 1.3.2, the app does not just show the code: it explains in a dialog that the day is not a working day and that, if the employee worked, they can [request a manual workday](../03-time-tracking/19-request-a-manual-workday.md). On the day card it also distinguishes a **public holiday** from a **day off**.

> **Warning:** If your company routinely works on public holidays (for example, in the retail or hospitality sectors), you have to review the calendar configuration so as not to block valid clock-ins. See the article [Public holidays and non-working days](29-public-holidays-and-non-working-days.md) to learn how to handle this case.

---

## Consulting an employee's calendar

From the back office, the manager can check which days are marked as non-working for a specific employee:

1. Go to **Employees** and open the employee's record.
2. Open the schedules tab.
3. Next to their schedule, the record shows their non-working days separated by origin: **Inherited from the entity**, **inherited from their branch** and **Employee's own**. Absences of several consecutive days appear grouped in a single row with their range.

This view is especially useful for debugging situations where an employee reports that they could not clock in on a particular date. To see at a glance who is available each day across a whole branch, use the [availability board](98-availability-board.md).

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Schedule exceptions](25-schedule-exceptions.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Public holidays and non-working days](29-public-holidays-and-non-working-days.md)
- [Availability board](98-availability-board.md)
- [Statuses and error codes](../03-time-tracking/22-statuses-and-error-codes.md)
