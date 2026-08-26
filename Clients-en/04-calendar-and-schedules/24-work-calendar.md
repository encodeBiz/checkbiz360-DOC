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

A specific employee can have individual exceptions that mark particular days as non-working (or, conversely, as working days if the branch has them marked as holidays). Individual exceptions have the highest priority in the hierarchy.

> **Note:** Hierarchical resolution follows the rule that the configuration closest to the employee prevails over the more general one. If a date is a holiday at the organisation but the employee has an individual exception marking it as a working day, the employee will be able to clock in that day.

---

## How to add a public holiday

To add a holiday to the work calendar, follow these steps:

**At organisation level:**

1. Sign in to the back office with the owner role.
2. Navigate to **Calendar** and go to the **General configuration** tab.
3. Press the **Add non-working day** button.
4. Select the date in the calendar picker.
5. State the type (national holiday, bridge day, internal closure, etc.) and, optionally, add a description.
6. Save the record.

**At branch level:**

1. Sign in to the back office with the owner or manager role.
2. Navigate to **Branches** and select the relevant branch.
3. Go to **Calendar** and open the **Branch** tab.
4. Follow steps 3 to 6 of the previous procedure.

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

> **Warning:** If your company routinely works on public holidays (for example, in the retail or hospitality sectors), you have to review the calendar configuration so as not to block valid clock-ins. See the article [Public holidays and non-working days](29-public-holidays-and-non-working-days.md) to learn how to handle this case.

---

## Consulting an employee's calendar

From the back office, the manager can check which days are marked as non-working for a specific employee:

1. Go to **Employees** and select the employee.
2. Open the **Effective calendar** section.
3. The system shows the monthly calendar with the working days, the holidays inherited from the organisation and branch, and the employee's individual exceptions.

This view is especially useful for debugging situations where an employee reports that they could not clock in on a particular date.

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Schedule exceptions](25-schedule-exceptions.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Public holidays and non-working days](29-public-holidays-and-non-working-days.md)
- [Statuses and error codes](../03-time-tracking/22-statuses-and-error-codes.md)
