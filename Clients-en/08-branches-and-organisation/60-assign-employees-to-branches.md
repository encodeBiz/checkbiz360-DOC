# Assign employees to branches

Assigning an employee to a branch is the mechanism by which CheckBiz360 links a person with a specific workplace. This link determines which branch the employee can clock in from, which schedules apply, which managers supervise their records and which geofence is used to validate their location. This article explains how to make this assignment, how to manage employees who work at several branches and what impact the assignment has on the system.

## Concepts to know first: responsibilities and branch assignment

Each employee in CheckBiz360 has one or several **responsibilities** associated with them. Each responsibility defines the context in which that employee operates: the branch assignment, the role they hold there and, optionally, the project or functional area.

The branch assignment is the link joining an employee with a branch. When the employee clocks in from the app, the system identifies which branch that record belongs to from this assignment. If an employee has no responsibility with an assigned branch, they will not be able to clock in.

## Assign an employee to a branch

### From the employee's record

1. Go to the web back office and navigate to **Employees** in the side menu.
2. Find the employee you want to assign and click on their name to open their record.
3. Scroll to the **Responsibilities** or **Assignments** section.
4. Press **Add responsibility**.
5. Select the branch from the **Branch** dropdown. The list shows only the active branches of your organisation.
6. Assign the role the employee will hold at that branch: **Worker**, **Supervisor** or **Manager**.
7. Where appropriate, select the effective calendar that will apply to this employee at that branch.
8. Press **Save**. The assignment applies immediately.

### From branch management

You can also assign employees directly from the branch record:

1. Navigate to **Branches** and open the branch you want.
2. Go to the **Employees** tab inside the branch record.
3. Press **Assign employee** and enter the employee's name or email address in the search box.
4. Select the role and the calendar and press **Confirm**.

### Add a whole team at once

If the same crew works on several projects, there is no need to link each person separately. In the employee list of the branch record, **Apply team** adds all the members of a team at once, each with their responsibility, job and rate, and skips anyone who was already there. **Save as team** does the opposite: it turns the branch's staff into a reusable team. See [Teams](../02-employees/99-teams.md).

## Multi-branch: one employee at several branches

CheckBiz360 supports the same employee being assigned to several branches at once, with different roles at each. This feature is designed to cover cases such as:

- An employee who works at two stores on an alternating basis.
- A manager who acts as Supervisor at their usual branch and as Manager at a smaller one.
- Field teams who move between facilities according to weekly planning.

### How multi-branch works

When an employee with multiple responsibilities clocks in from the app, the system automatically determines which branch they are clocking in at by comparing the device's GPS location with the coordinates and radii of each assigned branch. If the employee is within branch A's radius, the record is stored at branch A; if they are within branch B's radius, it is stored at branch B.

If the employee is outside the radius of all their assigned branches and the geofence is not disabled, the clock-in will be rejected with the code `checklog/out_of_radius`.

> **Warning:** If two branches' radii overlap geographically, there can be ambiguity in assigning the clock record. In those cases, the system prioritises the branch whose centre is closest to the employee's real position. Review the configured radii if you detect incorrect assignments recurrently.

### Different roles per branch

Each responsibility is independent. The same employee can be a Worker at one branch and a Supervisor at another. The permissions applied in each context are those of that specific responsibility's role, not those of the employee's highest role.

## Impact of the assignment on the effective calendar

When assigning an employee to a branch, the system links that assignment with the effective calendar selected. The calendar defines the working days, the branch's own public holidays and the work shifts. This link has the following implications:

- The employee's clock records are compared with the calendar's shifts to detect anomalies (late arrivals, absences, early exits).
- The count of hours worked is calculated in relation to the shifts planned in that calendar.
- Absence or incomplete workday notifications are generated based on that branch's calendar shifts.

If an employee works at two branches with different calendars, each clock record is validated against the calendar of the branch where it occurs.

## Impact of the assignment on clock records

Once the employee has one or more active responsibilities, the app will automatically show the clocking button and the corresponding branch information. The employee does not need to select their branch manually in the app; the system detects it by GPS.

If the employee has no active assignment or their only assigned branch is inactive, the app will show an error message and will not let them clock in.

## Removing or modifying an assignment

To unlink an employee from a branch:

1. Open the employee's record in **Employees**.
2. Find the responsibility you want to remove in the **Responsibilities** section.
3. Press the delete icon next to the corresponding responsibility.
4. Confirm the operation. The employee will no longer be able to clock in at that branch from that moment on. The history of previous clock records at that branch is kept intact.

---

> **Role note:** Assigning employees to branches is available to the **Owner** and **Manager** roles. The **Supervisor** role can view the assignments of the employees on their team, but cannot create or modify them.

## Related articles

- [Create and manage branches](57-create-and-manage-branches.md)
- [Teams](../02-employees/99-teams.md)
- [Branch statuses](59-branch-statuses.md)
- [Organisation configuration](61-organisation-settings.md)
- [Multi-branch global view](62-multi-branch-global-view.md)
