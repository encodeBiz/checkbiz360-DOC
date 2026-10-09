# Task validation

Validation is the step by which a manager confirms that the work carried out by the employee meets the requirements. CheckBiz360 separates the act of completing a task (done by the employee) from that of validating it (done by the manager), guaranteeing a double level of control over the quality of the work.

---

## Validation flow

The process always follows the same order:

1. The employee carries out the task and marks it as **completed** from the app.
2. The system alerts the manager that there is work pending review.
3. The manager goes to the back office, reviews the work and decides whether to **accept** or **reject** it.
4. If they accept, the task moves to **validated** and is closed.
5. If they reject, the task moves to **rejected**, with the reason visible to the employee.

---

## Accepting a completed task

To validate a task, the manager has to:

1. Sign in to the back office and open the **Tasks** section.
2. Filter by **Completed** status to see those awaiting review.
3. Open the task detail.
4. Read the employee's notes and review the evidence provided.
5. Validate the task.

Once validated, the task is closed: the *validated* status is not assigned by hand from the edit form. If it has to be revisited, it is **reopened** by returning it to *Assigned*, which withdraws the validation (see [Reopening a task](./42-task-statuses.md#reopening-a-task)). If rating is enabled, you can then score the employee's work.

---

## Rejecting a completed task

If the manager considers that the work is not correct, they can reject it.

### Steps to reject a task

1. From the task detail in the back office, press **Reject**.
2. Write the reason for the rejection. **It is mandatory**: without text, the action cannot be confirmed.
3. Confirm the rejection.

The task moves to **rejected** status and the reason is visible to the employee alongside the task's complete history.

> **Important:** the reason for rejection is mandatory. A clear explanation is what allows the employee to correct the work and not repeat the mistake.

---

## Consequences of rejection

When a task is rejected:

- It stays in **rejected** status, which is a closure with a reason: the task does not return to the employee's work list on its own.
- The time-compliance indicator changes to show *Rejected*, because meeting the deadline stops being what matters.
- The history records the rejection, the reason, the author and the date, so that there is evidence of the complete cycle.

**If the work has to be redone**, the manager edits the task and returns it to **assigned** status, adjusting the deadline where appropriate. Doing so withdraws the previous rejection, although it still appears in the history. The employee gets it back in their list and the cycle starts again.

---

## Who can validate

By default, **managers and owners** validate. Each task also includes the **Allow validation by supervisor** option, enabled by default, which lets the branch supervisors validate or reject that task.

It is a decision made **per task**, not a permission on the employee's profile: it is ticked when creating the task or when editing it, alongside the rating and mandatory evidence options. This makes it possible to decentralise day-to-day operations and reserve the validation of sensitive tasks for the manager.

> **Note:** the manager always retains full visibility over their supervisors' validations. Every action is recorded in the history with the name of whoever carried it out and their level of responsibility.

---

## Related articles

| Article | Description |
|---|---|
| [Task statuses](./42-task-statuses.md) | Life cycle and meaning of each status |
| [Tracking and updates](./43-tracking-and-updates.md) | How the employee updates progress |
| [Employee rating](./46-employee-rating.md) | Performance scoring after validation |
| [Task notifications](./47-task-notifications.md) | Alerts on validating or rejecting a task |
| [Roles and responsibility levels](../02-employees/07-roles-and-responsibility-levels.md) | Description of permissions by role |
