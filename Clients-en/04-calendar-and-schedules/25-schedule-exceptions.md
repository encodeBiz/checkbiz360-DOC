# Schedule exceptions

The base schedule of a branch or organisation defines the standard working conditions for the bulk of employees. There are, however, legitimate situations in which an employee needs a different schedule from the rest: reduced hours for family reasons, a temporary adjustment during a recovery period, or a special schedule agreed contractually.

To cover these cases, CheckBiz360 allows individual schedule exceptions to be configured. An exception is a schedule rule linked exclusively to a specific employee that takes precedence over the schedule inherited from the branch or the organisation.

---

## Types of exception

### One-off exception

A one-off exception applies to a single specific day. It is useful for isolated cases: the employee starts earlier or later than usual on a particular day, or that day is marked as non-working for them alone.

Example: on 15 June, the employee has a medical appointment and their workday starts at 11:00 instead of 09:00. A one-off exception is created for that date with the adjusted shift.

### Recurring exception

A recurring exception repeats systematically, generally on a weekly cadence. It is the most appropriate mode for long-running situations such as reduced hours for legal guardianship or an adjusted schedule following a period of leave.

Example: every Friday, the employee works a continuous day and leaves at 15:00 instead of 17:00. A recurring exception is configured that applies every Friday for as long as the adjustment period is in force.

---

## How to create a schedule exception

1. Sign in to the back office with the owner or manager role.
2. Navigate to **Employees** and select the relevant employee.
3. Go to the **Schedule and calendar** section.
4. Press the **New exception** button.
5. Select the exception type: **One-off** or **Recurring**.
6. If it is one-off, state the specific date.
7. If it is recurring, select the days of the week it applies to and define the start date and, optionally, the end date.
8. Configure the exception's time window: start time (`start.hour`, `start.minute`) and finish time (`end.hour`, `end.minute`).
9. If the exception marks the day as non-working for that employee, enable the **Non-working day** option.
10. Save the exception.

Once saved, the exception comes into force immediately. The system will use it on the employee's next clock-ins.

> **Warning:** Schedule exceptions have no retroactive effect on clock records already stored. They only affect records made from the moment of their creation onwards.

---

## Common use cases

### Employee with reduced hours

An employee with reduced hours for family reasons works from 09:00 to 14:00 instead of the standard 09:00 to 17:00. A recurring exception is configured that applies Monday to Friday with the reduced shift. The rest of the branch's employees keep their usual schedule with no change at all.

### Adjusted return-to-work schedule

An employee returning after long-term leave starts with shorter workdays during the first few weeks. A recurring exception is created with a defined end date. When that date arrives, the system stops applying the exception and the employee automatically returns to the branch schedule.

### One-off non-working day

An employee requests a day of unpaid leave. The manager can create a one-off exception marking that day as non-working for that employee. Any attempt to clock in that day will generate the code `checklog/day_disabled`, just as happens on the general calendar's public holidays.

---

## Priority of individual exceptions

When the system resolves an employee's effective calendar, it follows an order of priority. Individual exceptions have the highest priority and always prevail over the branch's and the organisation's schedule.

The logic is as follows:

1. The system checks whether the employee has an active individual exception for that day.
2. If an exception exists, it uses it as the reference for validating the clock-in.
3. If there is no exception, it consults the branch's schedule.
4. If the branch has no schedule of its own configured, it uses the organisation's schedule.

This means that an individual exception can both restrict and extend the inherited schedule. If the branch schedule defines a shift from 09:00 to 17:00 but the employee has an exception from 07:00 to 15:00, the system will use the 07:00 to 15:00 shift for that employee.

> **Note:** For a complete explanation of the hierarchical resolution algorithm, see the article [Configuration inheritance](26-configuration-inheritance.md).

---

## Managing and reviewing active exceptions

The manager can check an employee's active exceptions at any time from the employee's record in the back office. The **Schedule and calendar** section shows the list of exceptions in force with their type, application dates and the configured time window.

To deactivate an exception before its planned end date, select it and press **Deactivate**. The exception is archived and the employee returns to the schedule inherited from the branch or the organisation.

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Work calendar](24-work-calendar.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Strict and flexible workday](28-flexible-schedule.md)
- [Public holidays and non-working days](29-public-holidays-and-non-working-days.md)
