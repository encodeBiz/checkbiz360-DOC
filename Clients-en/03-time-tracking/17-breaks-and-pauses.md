# Breaks and pauses

CheckBiz360 makes it possible to record rest periods within the working day precisely. Breaks differ from the end of the workday in that they do not close the active shift: the employee is still within their workday, but the break time is deducted from the count of hours worked. This article explains how breaks work, how to record them and how to configure them per branch.

---

## Break event types

The system uses two specific record types to manage breaks:

- **Restin (`restin`):** Marks the start of a break. The employee temporarily leaves their workstation.
- **Restout (`restout`):** Marks the end of the break. The employee resumes their activity.

Both events are stored in the employee's attendance history with their corresponding timestamp, just like entry and exit events.

---

## The difference between a break and the end of the workday

The distinction matters for calculating hours:

| Event | Effect on the workday |
|---|---|
| `restin` (start of break) | The workday stays open. Break time starts being counted. |
| `restout` (end of break) | The workday continues. The break time is closed and deducted. |
| `checkout` (exit) | The workday closes definitively. |

If the employee records a `checkout` without having closed an active break with `restout`, the system may mark the workday as incomplete or flagged, depending on the branch configuration.

---

## How to record a break from the app

### Start a break (restin)

1. On the attendance screen, press the **Start break** button.
2. Confirm the action if the system asks you to.
3. The app will show that the employee is on a break and record the start time.

### End a break (restout)

1. On the attendance screen, press the **End break** button.
2. The app will confirm that the workday has resumed and show the break time elapsed.

The main attendance screen reflects at all times whether the employee is on an active workday or on a break.

---

## Breaks in the attendance history

Each break event is stored in the employee's attendance history with:

- Event type (`restin` or `restout`).
- Exact timestamp of the record.
- Validation status (valid or failed).
- Geolocation data, where geofence validation applies.

The manager can consult the break detail for any employee from the back office, including the total break duration per workday.

---

## Break configuration per branch

Breaks can be configured with different parameters at branch level:

### Disable breaks

If the branch's operation does not involve recorded breaks, this feature can be disabled using the "disable breaks" option. When active, the break buttons do not appear in the app for that branch's employees and `restin`/`restout` events are not processed.

### Standard break duration

The "standard break duration" field lets you define a standard break duration in minutes. This value is used as a reference for the automatic calculation of breaks and can be used in reports to compare the actual duration of rest periods against the standard time established.

To configure these parameters:

1. Sign in to the back office with the **manager** or **owner** role.
2. Navigate to **Branches** and select the relevant branch.
3. Open the attendance configuration section.
4. Adjust the "disable breaks" and "standard break duration" fields as you need.
5. Save the changes.

---

## Automatic deduction of breaks when calculating hours

The system automatically deducts break time from the total hours worked in the workday. The calculation is as follows:

**Hours worked = (checkout time - checkin time) - total break time**

If the employee has taken several breaks during the workday, the system adds up the duration of all of them and deducts them from the total. This calculation is available in the attendance reports and in the employee's workday summary.

> **Warning:** If an employee starts a break with `restin` but does not close it with `restout` before recording the checkout, the system may record the break as unfinished. In these cases, the manager has to review and correct the workday manually from the back office.

---

## Roles with access to this feature

Recording breaks from the app is an action available to all users with the **employee** role. Configuring breaks per branch ("disable breaks", "standard break duration") requires the **manager** or **owner** role.

---

## Related articles

- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
- [How clocking in works](13-how-clocking-in-works.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
- [Request a manual workday](19-request-a-manual-workday.md)
