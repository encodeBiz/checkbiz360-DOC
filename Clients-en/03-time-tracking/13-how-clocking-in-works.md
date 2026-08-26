# How clocking in works in CheckBiz360

Clocking in with CheckBiz360 is not a simple time stamp. Every time an employee records their entry or exit, the system runs a three-layer validation process that guarantees the integrity of the data, its consistency with the active shift and the identity of the device used. This article explains how that process works from start to finish.

---

## The three validation layers

When an employee presses the clock-in button, the system evaluates three conditions in sequence. If any of them is not met, the clock record is stored as failed with a specific error code indicating the exact cause.

### Layer 1 — Geolocation

The system obtains the device's GPS coordinates at the moment of the clock-in and compares them with the location of the branch assigned to the employee. Each branch has a clocking radius configured (expressed in metres). If the employee is outside that radius, the clock-in is rejected with the code `checklog/out_of_radius`.

The actual distance between the employee and the centre of the geofence is recorded in the system for later analysis. This lets the manager review whether the radius is correctly sized or whether there is a pattern of clock-in attempts from incorrect locations.

If the employee works in teleworking mode and has the "remote work" field enabled, this validation layer is skipped entirely. The geofence does not apply in remote working environments.

### Layer 2 — Effective schedule

Once the location has been validated, the system checks that the clock-in is taking place within the employee's active shift for that day, according to their effective calendar.

The clock record always stores the **real time**. What decides whether time worked outside the official window counts or not is the calendar's **workday mode**: with a strict workday it is not counted; with a flexible workday it is added as extra time. See [Strict and flexible workday](../04-calendar-and-schedules/28-flexible-schedule.md).

If the clock-in takes place outside the active shift, the system rejects it with the code `checklog/out_of_schedule`.

### Layer 3 — Device and biometrics

The third layer verifies the device's identity and, where applicable, the employee's biometrics.

If the employee has two-factor authentication (2FA) enabled, they can only clock in from devices that have previously been registered as trusted devices. Attempting to clock in from an unregistered device generates the error `auth/untrusted_device`.

If the employee's or the branch's configuration has biometric verification enabled, the employee must complete biometric verification (fingerprint or facial recognition depending on the device) before the clock-in is processed.

---

## Result of the clock-in

Once the three validation layers have been passed, the clock record is stored with status `valid`. This status indicates that the record is correct, consistent with the shift and authenticated.

If any layer fails, the record is stored with status `failed` and the corresponding error code. One important point: **failed clock records are also stored in the system**. They are not discarded. They remain available for auditing, incident analysis and review by the manager.

| Status after the clock-in | Meaning |
|---|---|
| `valid` | All validations passed. Workday active. |
| `failed` | One or more validations failed. Error code available. |

---

## The difference between a valid and a failed clock record

The distinction matters for payroll management and regulatory compliance. A valid clock record counts as time worked within the workday. A failed clock record is stored for auditing but does not count hours.

When an employee accumulates repeated failed clock records, the manager can review the pattern from the back office and determine whether it is a configuration problem (a radius that is too small, a badly assigned schedule) or an incident that needs attention.

If an employee was unable to clock in for justified reasons, the manager can create a manual workday request to record the attendance retroactively.

---

> **Note on auditing:** Every clock record, valid and failed alike, is stored with its original timestamp, the validation data (coordinates, distance, device) and the result of each layer. This record is immutable and can be consulted in the event of a labour inspection.

---

## Roles with access to this feature

The configuration of the validation layers (check zone, biometrics, 2FA) is managed by users with the **owner** or **manager** role. Employees interact with the clocking system from the mobile app without having to configure anything.

---

## Related articles

- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
- [Remote clocking in](15-remote-clocking-in.md)
- [Geofences and clocking radius](16-geofences-and-clocking-radius.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
