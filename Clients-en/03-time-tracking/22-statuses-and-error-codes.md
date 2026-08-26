# Clock record statuses and error codes

CheckBiz360 assigns each attendance record a status that reflects its situation in the workday life cycle. When a clock-in cannot be processed correctly, the system also generates an error code that identifies the cause precisely. This article describes every possible status and the available error codes, together with the recommended actions for resolving them.

---

## Clock record statuses

Statuses indicate where in the process an attendance record stands. They are assigned automatically by the system and can change over time, for example when an employee validates a manual workday or when a manager corrects an incident.

| Status | Meaning |
|---|---|
| `valid` | Correct clock record. All validations passed. The record counts as time worked. |
| `failed` | Rejected clock record. One or more validations failed. The record is stored for auditing but does not count hours. Includes an error code. |
| `pending-employee-validation` | Record created by a manager or modified. Waiting for the employee's confirmation. Does not count hours until accepted. |
| `incomplete_workday` | Unclosed workday. There is a valid checkin with no corresponding checkout. Requires manual resolution or a later checkout. |

---

### `valid` status

This is the target status for every clock record. It indicates that the record has passed the geolocation, schedule and authentication validations, and that the employee has confirmed it (where necessary). Calculations of hours worked are performed exclusively on records in `valid` status.

### `failed` status

A clock record can end up in `failed` status for a number of reasons: the employee was outside the radius, the clock-in took place outside the shift, the device was not authorised or the employee rejected a manual workday. In every case, the record is retained in full for auditing.

### `pending-employee-validation` status

This status is temporary. It appears when a manual workday is created or when a manager modifies a clock record and the system requires the employee's confirmation. While the record remains in this status, it does not alter the count of hours.

### `incomplete_workday` status

Indicates that the employee recorded their entry but not their exit. The workday remains open. This status can be resolved by recording the corresponding checkout (manually or from the app) or by the manager creating a manual checkout.

---

## Error codes

When a clock record ends up in `failed` status, the system associates an error code identifying the exact cause of the rejection. These codes let the manager diagnose and resolve the incident efficiently.

| Code | Cause | Recommended action |
|---|---|---|
| `checklog/out_of_schedule` | The clock-in took place outside the employee's active shift. | Review the schedule assigned to the employee. If the attendance was correct, request a manual workday. |
| `checklog/out_of_radius` | The device was outside the branch's clocking radius at the moment of the record. | Review the branch's GPS coordinates and the configured radius value. If the radius does not cover the actual working area, widen it. |
| `checklog/day_disabled` | The day on which the clock-in was attempted is disabled in the branch's or the employee's calendar. | Review the calendar configuration. If the day should be enabled, activate it in the relevant effective calendar. |
| `auth/untrusted_device` | The device the clock-in was attempted from is not registered as a trusted device. The employee has two-factor authentication enabled. | Register the current device as a trusted device through the 2FA process. |
| `employee/not_found` | The employee identifier does not correspond to any active record in the system. | Check that the employee is active on the platform and correctly assigned to the branch. |
| `checklog/overlap_detected` | A clock record already exists for the time range in which the new record is being created. Two records of the same type cannot overlap. | Review the employee's existing records for that date and resolve the overlap before creating a new record. |

---

## How to consult a clock record's status and error code

From the back office, the manager can access the detail of any clock record and see:

- The record's current status.
- The error code if the status is `failed`.
- The technical data of the attempt: coordinates, distance to the radius, active shift at the moment of the record, device used.
- The complete change history.

Employees can see the status of their clock records from the attendance history section in the app. For failed records, the app shows a description of the reason in plain language.

---

> **Warning for managers:** A failed clock record does not necessarily mean the employee acted incorrectly. In many cases the error is one of configuration: a radius that is too small, a badly assigned shift or an unregistered device. Before taking any disciplinary action, always review the technical details of the error and check with the employee.

---

## Roles with access to this feature

All users with the **employee** role can see the status of their own clock records from the app. Users with the **manager** or **owner** role have full access to the statuses, error codes and technical data of every clock record in their organisation from the back office.

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Geofences and clocking radius](16-geofences-and-clocking-radius.md)
- [Request a manual workday](19-request-a-manual-workday.md)
- [Traceability and change history](21-traceability-and-change-history.md)
