# Check-in and check-out from the app

The CheckBiz360 mobile app is the main entry point for recording attendance. This article explains step by step how to make a check-in (entry) and a check-out (exit) from the application, what information the main attendance screen shows and how to interpret the most common error messages.

---

## The main attendance screen

On opening the app and selecting the working organisation, the employee reaches the attendance screen. This screen shows in real time:

- **Current status:** whether the employee is inside or outside their active workday.
- **Time of the last clock record:** the exact time of the last event recorded (entry, exit or break).
- **Active branch:** the name and location of the branch assigned for that shift.
- **Available clocking action:** the app shows only the action that matches the current status. If the employee has not clocked in, the check-in button appears. If they have already clocked in, the check-out or break button appears as appropriate.

This screen updates automatically whenever there is a change of status.

---

## How to make a check-in (entry)

1. Open the CheckBiz360 application on your mobile device.
2. Sign in with your credentials if you have not already done so.
3. Select the relevant working organisation.
4. On the attendance screen, press the **Record entry** button.
5. If your device requires biometric verification, confirm your identity with your fingerprint or facial recognition when the system asks for it.
6. The app will request location permission if you have not already granted it. You have to grant this permission for geofence validation to work correctly.
7. The system processes the clock-in. Within a few seconds, the screen will show the entry confirmation with the recorded time.

If the clock-in is correct, the screen status changes to "Within workday" and the entry time is shown.

---

## How to make a check-out (exit)

1. On the attendance screen, press the **Record exit** button.
2. Confirm the action if the system asks you to.
3. If you have biometric verification enabled, complete the authentication.
4. The system processes the exit record. The screen will show the confirmation with the exit time and the total time worked during the workday.

### Warnings before closing the workday

**From version 1.6.0 of the app**, if something does not add up the app says so before clocking out and lets the person decide. The warning comes first, before asking for location or biometrics, and always with two ways out: **Cancel** or **End workday**.

There are two cases:

- **The shift has not ended.** It appears when more than 30 minutes are left of the shift being worked. On a split shift it is measured against the current shift, not against the end of the day: leaving at 13:00 on a 9 to 13 shift does not warn. With no schedule set for that day, it does not warn either.
- **You are taking part in tasks that are still in progress.** Only your own tasks count, not the team's. The app neither pauses nor closes them: a task can have several people assigned and the others may still be working on it.

Neither of them prevents clocking out. They are there so nobody closes their workday by accident, not to block someone who knows what they are doing.

> **Important:** The check-out closes the active workday. If you forget to record the exit, the workday will remain in `incomplete_workday` status until a manager corrects it manually or the employee resolves it from the notifications screen.

---

## On-screen error messages

The app shows specific messages when a clock-in cannot be processed correctly. The most common are described below:

### Outside the zone

Appears when the device is outside the clocking radius defined for the branch. The app may show the approximate distance to the authorised clocking point.

**What to do:** Check that you are at the right premises. If you habitually work at that location and the error repeats, report it to your manager so they can review the radius configuration.

### Outside the schedule

Appears when the clock-in attempt takes place outside the employee's active shift.

**What to do:** Check your assigned shift in the schedules section of the app. If you believe the clock-in is correct, ask your manager for a manual workday.

### Unauthorised device

Appears when the device the clock-in is being attempted from is not registered as a trusted device and the employee has two-factor authentication enabled.

**What to do:** Contact your manager or the system administrator to register the current device as a trusted device.

---

## Availability of the record in the back office

The clock record is available in the back office immediately, with no need for manual synchronisation. The manager can see the record in real time from the attendance panel.

Both valid and failed clock records are stored and are visible in the employee's attendance history. Failed records include the error code and the technical data of the attempt (time, coordinates, distance to the radius).

---

> **Note for managers:** If an employee reports a persistent error when clocking in, go to the attendance history in the back office and review the error code of the failed record. This will let you identify whether the problem is one of configuration (radius, schedule, device) or whether it requires a manual correction.

---

## Roles with access to this feature

Recording check-in and check-out from the app is an action available to all users with the **employee** role. Reviewing clock records in the back office is available to the **manager** and **owner** roles.

---

## Related articles

- [How clocking in works](13-how-clocking-in-works.md)
- [Breaks and pauses](17-breaks-and-pauses.md)
- [Request a manual workday](19-request-a-manual-workday.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
