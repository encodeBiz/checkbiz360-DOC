# Request a manual workday

There are situations in which an employee cannot record their attendance through the app at the usual moment: a one-off device failure, an emergency, lack of coverage or any other justified circumstance. In these cases, a manager or supervisor can create an attendance record manually for the employee affected. This article explains how this process works and what happens after the request is created.

---

## What a manual workday request is

A manual workday is an attendance record created by a manager on an employee's behalf, retroactively or after the fact. Unlike an ordinary clock-in, it does not require the employee to be present with their device at the moment of the record.

The system distinguishes two modes of creating a manual workday, depending on the context of the employee's workday:

---

## Mode A — Full workday

Used when the employee has recorded no event during the workday: neither entry nor exit.

In this mode, the manager simultaneously creates a **checkin** and a **checkout** for a specific date. If the manager does not specify the exact times, the system fills them in automatically using the shift times from the effective calendar assigned to the employee for that day.

This mode is appropriate for situations such as:

- The employee worked but forgot or was unable to clock in at any point.
- Attendance corresponding to a previous day is being recorded.
- The employee was present but their device did not work throughout the workday.

---

## Mode B — Checkout only

Used when the employee already has a **valid open checkin**: they arrived and were recorded correctly, but did not clock out.

In this mode, the manager creates only the corresponding **checkout** to close the workday. The existing checkin is not modified.

This mode is appropriate for situations such as:

- The employee forgot to clock out at the end of the shift.
- The employee was unable to record the checkout because of a technical problem at the end of the workday.
- The workday appears in `incomplete_workday` status and has to be closed.

---

## How to create a manual workday

1. Sign in to the back office with the **manager** or **owner** role.
2. Navigate to the **Attendance** section or to the employee's profile.
3. Select the **New manual workday** or **Request manual workday** option.
4. Choose the employee, the branch and the date of the workday.
5. Select the relevant mode (full workday or checkout only).
6. Enter the times if you want to specify them manually, or let the system complete them according to the shift.
7. State the reason for the request. This field is required and will be stored in the audit history.
8. Confirm the request.

---

## What happens after the request is created

Once the manual workday has been created, the system automatically carries out the following actions:

### Initial status: pending validation

The manual workday is set to `pending-employee-validation` status. This means the record exists in the system but **does not count as hours worked until the employee accepts it**. This mechanism protects the employee against unauthorised modifications to their attendance record.

### Push notification to the employee

The employee receives a push notification on their device informing them that a manual workday has been created in their name. The notification invites them to review and validate or reject the record.

### Validation or rejection by the employee

The employee goes to the notifications screen in the app and reviews the details of the proposed workday: date, times, branch and the reason given by the manager.

- If the employee **accepts**, the workday moves to `valid` status and starts counting as hours worked.
- If the employee **rejects**, the workday is marked as `failed` with the reason for the rejection.

---

## Traceability of the manual workday

Every manual workday request is recorded in the change history with the following information:

- Unique identifier of the entry.
- Date and time the request was made.
- Action performed (`manual_request_created` or `manual_checkout_created`, depending on the mode).
- UID of the manager who created the request.
- Data on the previous state and the new state of the workday.

This record is immutable. It cannot be modified or deleted, which guarantees the integrity of the history in the face of labour inspections or internal audits.

---

> **Warning:** The reason field is required and is permanently linked to the record. Always give a clear and truthful description of the reason justifying the manual workday. This data may be required in the event of a labour inspection.

---

## Roles with access to this feature

Creating manual workdays is restricted to users with the **manager** or **owner** role. Users with the **employee** role can only validate or reject the manual workdays assigned to them.

---

## Related articles

- [Review and approval of clock records](20-reviewing-and-approving-clock-records.md)
- [Traceability and change history](21-traceability-and-change-history.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
