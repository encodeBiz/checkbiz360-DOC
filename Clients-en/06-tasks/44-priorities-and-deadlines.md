# Priorities and deadlines

The combination of priorities and deadlines lets the manager communicate to the employee which tasks are more urgent and how much time they have to complete them. Managing both parameters correctly reduces oversights, orders the team's work and generates reliable data on operational compliance.

---

## Priority system

CheckBiz360 classifies tasks into four priority levels:

| Priority | Recommended use |
|---|---|
| **Critical** | The task admits no delay: there is an operational, safety or legal risk if it is not resolved immediately. |
| **High** | It has to be completed ahead of the rest of the day's work. It directly affects operations or has consequences if delayed. |
| **Medium** | Important, but with some flexibility as to when it is carried out. |
| **Low** | Worth doing but not critical. It can be postponed if more urgent tasks arise. |

Priority is set when the task is created and can be modified afterwards from the back office while the task remains open. In the list, each priority has its colour: red for critical, amber for high, blue for medium and green for low.

> **Tip:** reserve critical and high priority for what really is. If every task is urgent, priority stops ordering the work and the employee loses any basis for deciding where to start.

---

## A task's dates

A task handles two dates, with different purposes:

- **Deadline** (required): the latest moment by which the task has to be completed. It is the reference for the time-compliance indicator.
- **Expected start date** (optional): the time at which the employee is expected to start. It does not block anything on its own; it serves to trigger the late-start warning.

Both are interpreted in the **operational time zone of the task's branch**. If the branch has no time zone of its own, the organisation's is used. This matters in organisations with sites in different time zones: an 18:00 deadline means 18:00 at the site where the task is carried out, not in the browser of whoever created it.

### Considerations when setting a deadline

- Bear in mind the assigned employee's shift. If the task is due at 10:00 and the employee starts at 11:00, it will expire before they can deal with it.
- For repeating tasks, the deadline delimits each instance's cycle.
- You can modify the deadline of an open task at any time from the back office.

---

## Late-start warning

This is the automatic warning that is configured task by task. If the task has an **expected start date** and the **Notify if not started on time** option is enabled, the system sends a notification when **15 minutes** have passed since that time without the task having been started.

The dispatch is recorded in the task's activity, so the manager can check whether the warning actually went out.

Without an expected start date, the option has no effect: there is no time against which to measure the delay.

---

## Deadline warnings

In addition to the late-start warning, the platform gives notice when a task is approaching its deadline and when it passes it. Each warning is issued only once per task and is recorded, so that the same deadline does not generate repeated notifications.

> **Status: Planned**
> How far in advance these warnings are sent is not configurable by the customer in the current version. Being able to adjust the lead time, enable a second reminder or vary the frequency by priority is part of the roadmap.

---

## What happens when a task expires without being completed

When the deadline arrives and the task is not completed, **it does not change status**: it stays in *assigned* or *in progress*. What changes is its **time-compliance indicator**, which moves to *overdue*.

The consequences are:

- The task appears marked as overdue in the back office list and in the employee's app.
- The overrun is recorded and is reflected in the task report.
- The employee can still complete it after it has expired. On closing it, the indicator will move to *completed late*, not *completed on time*.

> **Important:** an overdue task does not disappear or close itself. The record that it passed the deadline remains in the history even if it is later completed and validated.

---

## Extending the deadline

If circumstances justify allowing more time, the manager can edit the task and change the deadline. The change is reflected in the task's activity, with the user who made it and the moment.

### Steps to extend the deadline

1. Sign in to the back office and open the task detail.
2. Press **Edit**.
3. Modify the **Deadline** field.
4. Save the changes.

If you also want to record the reason for the employee, add a **note** to the task: it is the mechanism provided for written communication within a task.

Extending the deadline does not change the task's status. The time-compliance indicator is recalculated against the new deadline.

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](./40-create-a-task.md) | Fields available when creating a task |
| [Task statuses](./42-task-statuses.md) | Life cycle, statuses and time compliance |
| [Tracking and updates](./43-tracking-and-updates.md) | Real-time progress tracking |
| [Task notifications](./47-task-notifications.md) | Automatic platform alerts |
| [Task reports](./48-task-reports.md) | Overdue tasks versus completed on time |
