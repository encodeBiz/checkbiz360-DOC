# Task tracking and updates

Once a task has been assigned, both the employee and the manager have tools for communicating about its progress and keeping the status up to date at all times. This article explains how tracking is handled from both sides: the employee's app and the manager's back office.

---

## How the employee updates a task's status

The employee manages their tasks from the tasks section of the mobile app. There they find a list of all the tasks assigned to them, ordered by priority and deadline.

### Starting a task

When the employee is ready to begin, they open the task detail and press **Start task**. The status changes from *assigned* to *in progress* and the manager sees it reflected in the back office.

### Marking a task as completed

Once the activity has finished, the employee presses **Mark as completed**. If the task has the evidence requirement enabled —it is by default— the system does not allow it to be closed without at least one photo or video attached, and returns the error `task/evidence_required`.

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

## Status change history

Each task keeps a chronological, immutable record of every status change it has undergone. The history is accessible from the task detail in the back office and includes:

- The exact date and time of each status change.
- Previous status and new status.
- Name of the user or system that made the change.
- Comment associated with the change, if there was one.

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
