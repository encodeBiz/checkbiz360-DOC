# Task tracking and updates

Once a task has been assigned, both the employee and the manager have tools for communicating about its progress and keeping the status up to date at all times. This article explains how tracking is handled from both sides: the employee's app and the manager's back office.

---

## How the employee updates a task's status

The employee manages their tasks from the tasks section of the mobile app. There they find a list of all the tasks assigned to them, ordered by priority and deadline.

### Starting a task

When the employee is ready to begin, they press **Start**. The status changes from *assigned* to *in progress* and the manager sees it reflected in the back office.

**From version 1.6.0 of the app** the button is in three places, and does the same in all three: on the task card in the list itself, on the **Today's tasks** card of the attendance screen, and inside the detail as before. There is no need to open the task to start it.

The buttons only appear on tasks assigned to the employee. A supervisor who sees their team's tasks still acts on them from the detail.

Starting requires an **open workday** (having clocked in) and, if the task has its own work site, being within its margin. See [Relationship with time tracking](./39-what-is-the-tasks-module.md#relationship-with-time-tracking) and [Own work site](./40-create-a-task.md#own-work-site).

### Marking a task as completed

Once the activity has finished, the employee presses **Complete**. If the task has the evidence requirement enabled —it is by default— the system does not allow it to be closed without at least one photo or video attached, and returns the error `task/evidence_required`.

**From version 1.6.0**, completing asks for confirmation before closing the task. It is the only one of the four actions the employee cannot undo on their own: going back requires a manager to reject it. Starting, pausing and resuming do not ask, because another tap undoes them.

If the task requires evidence and **Complete** is pressed from the list, the app opens the detail instead of trying to close it: that is where photos are uploaded.

---

## Pausing and resuming a task

When the work is interrupted —for lunch, to fetch materials, or because it carries on the next day—, the task is **paused** and then **resumed**, as many times as needed. Time spent paused is added up separately and appears in the [task report](./48-task-reports.md).

### From the app

In the detail of a task in progress, the employee presses **Pause**; to carry on, they press **Resume**. It is available **from version 1.4.0 of the app**.

**From 1.6.0** they are also outside the detail: on the task card in the list, next to **Complete**, and on **Today's tasks** as an icon button beside the main one.

- In the app, the pause button appears when the employee has clocked in for the workday.
- **Resume** requires the same as starting: an open workday and, if the task has its own work site, being within its margin.
- The detail shows the **time spent** —from start to finish, or up to now, excluding pauses— and the total of pauses.

### From the back office

In the detail of a task in progress, the **Pause** and **Resume** buttons appear. In the task summary, the **Pauses** figure shows since when it has been paused or, if it no longer is, how much the pauses have added up to.

The assigned employees can pause and resume and, from the back office, so can supervisors, managers and owners.

> **Important:** a task with its own work site cannot be resumed or completed from the back office, because the panel does not send a location. An employee has to do it from the app. Pausing it from the back office is possible.

### Pause rules

- **The pause belongs to the task**, not to each person. There is only one open pause at a time: if several people are assigned, any of them can pause or resume it, and who did so is recorded.
- **Completing, cancelling or rejecting** a paused task is allowed: the pause is closed at that moment. There is no need to resume it just to be able to close it.
- **Reopening** the task resets the pause counters to zero; the history keeps the previous pauses.
- The pause **does not extend the deadline**: time compliance is still calculated in the same way.
- Pausing and resuming **do not send notifications**.

> **Tip:** Encouraging employees to add a brief comment when completing the task —even though it is not mandatory— improves the quality of the record and makes validation easier for the manager.

---

## Progress notes

For as long as a task is active, the employee can add notes at any time from the task detail in the app. They are visible to the manager in the back office, and vice versa.

Each note is classified with a type, which makes the nature of the communication clear at a glance:

| Note type | What it is used for |
|---|---|
| **Specification** | Setting out precisely how the work should be done |
| **Operational note** | Reporting progress or the day-to-day of execution |
| **Clarification** | Resolving a question raised about the task |
| **Incident note** | Recording a problem encountered during execution |

Notes are useful for:

- Reporting that part of the task has been completed and work continues on another.
- Communicating an incident or difficulty encountered during execution.
- Attaching a photo or document as partial evidence of progress.
- Requesting clarification or confirmation before continuing.

The manager can also add comments from the back office, which the employee will see in the app. This allows direct communication about the task without needing calls or external messages.

---

## Task history

The **History** section of the task detail tells its complete story, in order: created, assigned, started, paused and resumed, completed, validated or rejected, cancelled, and status changes made by hand. Each line states:

- Date and time.
- Who did it and in what role. Automatic actions appear as **System**; if a back office user has no name recorded, they appear as **Panel user**.
- The reason, in validations, rejections and the latest cancellation.

Attempts to start or resume a task **outside its work site** are also noted ("Start rejected: outside the work site"), which help to understand why an employee could not begin.

Notes, evidence and ratings have their own section in the detail and are not repeated in the history. From version 1.4.0, the app also shows the task history, pauses included.

This history cannot be edited or deleted. It guarantees the task's complete traceability and serves as the basis for resolving discrepancies or auditing the team's performance.

---

## Real-time tracking from the back office

The manager does not need to wait for the employee to report: status changes are synchronised immediately between the app and the back office.

From the back office tasks panel, the manager or supervisor can:

- See the current status of every active task, filtered by status, priority, employee or branch.
- Open the detail of each task to read the employee's notes and review their evidence.
- Identify tasks that have been *in progress* for too long with no movement.
- Detect those that are *at risk* or *overdue* through the time-compliance indicator.

> **Note:** the system raises alerts on its own in two situations: when a task with an expected start time has not begun 15 minutes later, and when the deadline is approaching or has passed. A task being *in progress* for a long time with no news does not trigger any automatic alert: that is detected by reviewing the list.

---

## Update notifications

When a task's status changes, the system notifies the parties involved automatically. The manager receives a notification in the back office when the employee marks a task as completed or adds a relevant comment. The employee receives a push notification when the manager validates, rejects or comments on a task.

This removes the need for manual follow-up: the system informs each person at the moment they need to act.

For a detailed description of all the notification types, see the article [Task notifications](./47-task-notifications.md).

---

## Related articles

| Article | Description |
|---|---|
| [Task statuses](./42-task-statuses.md) | Life cycle and status transitions |
| [Task validation](./45-task-validation.md) | Validation flow by the manager |
| [Task notifications](./47-task-notifications.md) | Alert types and notification channels |
| [Task reports](./48-task-reports.md) | Tracking metrics and export |
| [Assign tasks to employees](./41-assign-tasks-to-employees.md) | How to assign and reassign tasks |
