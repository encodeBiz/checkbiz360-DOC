# Review and approval of clock records

Some attendance records in CheckBiz360 are not consolidated automatically; they require explicit confirmation from the employee before being considered valid. This mechanism guarantees that no modification or workday assignment happens without the knowledge and acceptance of the person affected. This article explains when this process is triggered, how the employee handles it and what options managers have.

---

## The "pending employee validation" status

The `pending-employee-validation` status indicates that a clock record or workday exists in the system but is waiting for the employee to confirm it. While it remains in this status, the record **does not count as time worked**.

This status is visible both to the employee (through the app) and to the manager (from the back office).

---

## When a clock record pending validation is generated

There are two main situations in which a record enters `pending-employee-validation` status:

**Manual workday request:** When a manager or supervisor creates a workday on the employee's behalf (Mode A or Mode B), the system automatically assigns this status until the employee responds. See the article [Request a manual workday](19-request-a-manual-workday.md) for more detail.

**Manager correction:** When a manager proposes a correction to an existing clock record for the employee (for example, adjusting the entry or exit time), the change is not applied until the employee accepts it. In the meantime, the record remains pending validation. The proposed time cannot be in the future: the form does not allow it and the server rejects it with `checklog_update/future_not_allowed`.

---

## How the employee validates or rejects a pending record

The employee receives a push notification on their mobile device when there is a record pending validation. To handle it:

1. Tap the notification or open the CheckBiz360 app.
2. Navigate to the **Notifications** section and select the clock record update notification.
3. Review the details of the record: date, entry time, exit time, branch and the reason given by the manager.
4. Select **Accept** or **Reject** as appropriate.

The review screen is available at the route `/notifications/checklog-update/:id`, where `:id` corresponds to the unique identifier of the attendance record.

---

## What happens if the employee accepts

The record moves to `valid` status. From that moment on, it counts as time worked and is incorporated into the calculation of hours for the workday; in the case of a correction, the corrected time is the one that appears in the working-time record report. The system records the validation action in the audit history with the date, time and identifier of the employee who performed it.

---

## What happens if the employee rejects

The outcome depends on what is rejected:

- **A correction of an existing clock record.** The record **goes back to how it was before the proposal**: the original time is not touched and it recovers its previous status, so it still counts in the working-time record. The rejection, with its reason, is noted in the record's change history.
- **A manual workday.** Since the record did not exist before the proposal, it is marked with `failed` status and the reason for the rejection. It remains in the system for auditing but does not count as hours worked.

In both cases, the manager can start a new, corrected proposal or resolve the incident manually.

---

## What happens if the employee does not respond

If the employee neither validates nor rejects the record, it remains indefinitely in `pending-employee-validation` status. There is no automatic expiry period by default.

In these cases, the record appears as pending in the back office and has to be resolved manually. Managers with the **manager** or **owner** role can:

- Approve the record directly from the back office, without the employee's validation.
- Reject it and close the incident with a recorded reason.
- Contact the employee so they resolve the pending validation from the app.

---

## The pending view in the back office

The CheckBiz360 back office includes a specific view for managing records pending validation. From this screen, the manager can:

- See every record in `pending-employee-validation` status at their branch or organisation.
- Filter by employee, date or branch.
- Open the detail of each record to review the change history.
- Approve or reject records individually or in bulk.

This view is designed so that the manager has a centralised picture of all pending incidents and can resolve them without going record by record through each employee's history.

---

> **Compliance warning:** Validation by the employee is an employment protection mechanism. Unilateral approval by the manager without having contacted the employee should be properly documented and used only in exceptional cases. In environments subject to labour audits, keeping the reason for the unilateral approval in the observations field is recommended.

---

## Roles with access to this feature

Users with the **employee** role can validate or reject pending records from the app. Users with the **manager** or **owner** role can resolve pending items from the back office, including approval without the employee's validation.

---

## Related articles

- [Request a manual workday](19-request-a-manual-workday.md)
- [Traceability and change history](21-traceability-and-change-history.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
- [How clocking in works](13-how-clocking-in-works.md)
