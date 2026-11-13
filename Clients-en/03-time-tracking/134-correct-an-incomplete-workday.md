# Correct an incomplete workday in one go

When someone forgets to clock out, the workday is left incomplete and an issue is opened. If it was a split workday, with several shifts, there may be several records to correct. From the issue, the whole workday is corrected on a single screen, with a single reason, and the person receives a single notification to accept or reject it.

---

## What it solves

- **A split workday of five shifts is not five corrections.** All the day's shifts are shown together and corrected in one go.
- **A single reason** for all the corrected records, instead of writing it on each one.
- **A single notification to the person**, who accepts or rejects the whole workday from the app.
- **The issue closes by itself** when the person accepts.

The correction changes nothing until the person accepts it: the time record is still the one they consider correct.

---

## Correcting the workday from the panel

1. Open the incomplete-workday issue, in **Contact → Issues**.
2. Click **Correct workday**. A window opens with the person's name and the day, and below it each **Shift** of that workday with its records (clock-in, breaks and clock-out) and its status: *Incomplete workday*, *Valid* or *Pending validation*.
3. Tick the shifts you want to correct and adjust the times. If the clock-out was set by the system at the planned time, it says so: *Set by the system at the planned time*. The times are in the time zone shown in the window itself.
4. Write the reason in **Reasons for change**. There is only one for all the corrected records.
5. Click **Correct and send**. The button says how many records are being sent.

From that moment, the issue says *Correction sent. Waiting for [person] to accept it.* While it waits, no other correction can be sent for the same workday.

> **Warning:** a time in the future cannot be set. If any is, the window warns you before sending.

---

## What the person does in the app

They receive a single notification. On opening it they see **Your workday correction**, with a card for each shift: what has been corrected appears struck through next to the new time, and the missing clock-out appears as *not clocked* followed by the proposed time.

- **Accept workday**: all the workday's corrections are applied. The records become valid and the issue is closed.
- **Reject**: the whole workday goes back to the company for review. They can write why they disagree; it is optional.

To see the whole workday on a single screen, the person needs the latest version of the app. With an earlier version, the changes reach them as separate notifications and they accept them record by record; when they accept the last one, the correction is closed just the same.

---

## What you see afterwards

In the issue itself:

| Message | What happened |
|---|---|
| *[Person] accepted the workday correction.* | Records valid with the corrected times and issue resolved. |
| *[Person] rejected the correction.* | The records stay as they were and the issue remains open, with the reason if they wrote one. You can send another correction. |
| *The correction was only partly accepted. Check the workday records.* | The person, with an earlier version of the app, accepted some records and not others. |

Each corrected record leaves its entry in the change history, with the reason, who proposed it and who accepted it. See [Traceability and change history](./21-traceability-and-change-history.md).

---

## Who can do it

The workday is corrected by the owner, an administrator or a manager with the manager role. Only the person themselves can accept or reject, from their app.

---

## Common problems

**I do not see the Correct workday button.** It only appears on incomplete-workday issues that are still open and without a correction awaiting a reply.

**The person says nothing has reached them.** Ask them to open the app and check their notifications; if phone notifications are turned off, the notification is still in the app. If they use an old version, they should update it.

**They have accepted and the record is still flagged as suspicious.** Accepting the correction does not change that flag. See [Anomaly detection](../07-operational-intelligence/55-anomaly-detection.md).

---

## Related articles

| Article | Description |
|---|---|
| [Reviewing and approving clock records](./20-reviewing-and-approving-clock-records.md) | Corrections of a single record and manual workdays |
| [Statuses and error codes](./22-statuses-and-error-codes.md) | What an incomplete workday means |
| [Traceability and change history](./21-traceability-and-change-history.md) | What is recorded of each correction |
| [Email alerts](../09-notifications/133-email-alerts.md) | The workdays-not-closed alert in the morning summary |
