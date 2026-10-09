# Task statuses

Every task in CheckBiz360 goes through a defined life cycle, from creation to closure. Understanding the statuses and the transitions between them is essential for tracking assigned work correctly.

A task carries **two independent indicators**: its **status**, which reflects where the work stands, and its **time compliance**, which reflects how it is doing against the deadline. It is worth not confusing them: a task can be *in progress* and *overdue* at the same time.

---

## The life cycle of a task

The usual path is:

**Draft → Assigned → In progress → Completed → Validated**

With two possible detours: the manager can **reject** a completed task, or **cancel** the task at any time before it closes.

While it is *in progress*, the task can be **paused** once or several times. The pause is not one more status: it is explained in [Paused task](#paused-task).

---

## Status table

| Status | Description | Who can trigger it |
|---|---|---|
| **Draft** | The task has been created but not yet put into circulation. It serves to prepare it before sending it to the team. | Whoever creates it, from the back office |
| **Assigned** | The task has been sent to those responsible, who have received the notification, but nobody has started yet. | Whoever creates it, or the system on assignment |
| **In progress** | An assigned employee has started the task and is working on it. | Employee from the app |
| **Completed** | The employee has marked the task as finished and it is awaiting review. | Employee from the app |
| **Validated** | The manager has reviewed the work and accepted it as correct. This is the satisfactory closure. | Manager, or owner or supervisor with validation permission |
| **Rejected** | The manager has reviewed the completed task and returned it with a mandatory reason. | Manager, or owner or supervisor with validation permission |
| **Cancelled** | The task is annulled because it no longer applies. It requires a reason and does not count as non-compliance. | Manager or owner from the back office |

The *Validated*, *Rejected* and *Cancelled* statuses cannot be assigned by hand when creating or editing a task: they are the result of a life-cycle action (validate, reject, cancel). The only way out of them is **reopening** the task, as explained below.

---

## Time-compliance indicator

Alongside the status, each task maintains a compliance indicator against its deadline:

| Indicator | What it means |
|---|---|
| **Not started** | Work on it has not yet begun |
| **On time** | Under way, within the deadline |
| **At risk** | Under way, but approaching the deadline |
| **Overdue** | The deadline has passed without completion |
| **Completed on time** | It was closed within the deadline |
| **Completed late** | It was closed after the deadline |

When the task is rejected, the indicator shows *Rejected*, because meeting the deadline stops being the relevant information.

---

## What triggers each status change

### From draft to assigned

Whoever creates the task saves it with *Assigned* status, or edits a draft task to put it into circulation. At that moment the assigned employees receive the push notification.

### From assigned to in progress

The employee opens the task in the app and presses start. They need an open workday and, if the task has its own work site, to be within its margin. The back office reflects the change and, if the task had the late-start warning enabled, that warning stops being pending.

### From in progress to completed

The employee presses finish in the app. If the task has the evidence requirement enabled, the system does not allow it to be closed without at least one photo or video attached, and returns the error `task/evidence_required`. If the task was paused, the pause is closed at that moment.

### From completed to validated

The manager reviews the work from the back office and accepts it. The task is closed and the employee rating is enabled.

### From completed to rejected

The manager reviews the work and returns it stating a **mandatory reason**, visible to the employee in the task detail. If the work has to be redone, the manager can edit the task and return it to *Assigned* status.

### Cancellation

A task that no longer applies is cancelled by stating a reason. It is an administrative closure: it does not count as non-compliance by the employee. The reason is saved on the task and appears in its history; if there was an open pause, it is closed.

> **Note:** cancellations made from the back office before 11 September 2026 did not keep their reason, even though the dialog asked for one. Later ones do keep it.

### Reopening a task

A validated, rejected or cancelled task is reopened from **Edit**, by changing its status to **Assigned** or **Draft**. Owners and managers can do this. To return to *Assigned*, the task has to have at least one employee assigned.

On reopening:

- The previous validation, rejection or cancellation is withdrawn, with its reasons, so that the task does not carry the sign-off of the past execution.
- Time compliance goes back to *Not started*. Review the deadline if it has already passed.
- The pause counters go back to zero.
- The history keeps everything that happened before reopening.

---

## Paused task

A task *in progress* can be **paused** and **resumed** as many times as needed, from the app or from the task detail in the back office. The steps and conditions are explained in [Tracking and updates](./43-tracking-and-updates.md#pausing-and-resuming-a-task).

The pause **is not a status**: the task remains *in progress* for all purposes —filters, reports, time compliance— and the status label shows **Paused** while it lasts. The deadline is not extended because the task is paused.

---

### Automatic "overdue" status

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

The automatic move to an explicit "overdue" task status is planned for a future version. Today the deadline being passed is reflected in the time-compliance indicator, not in the task status.

---

## The difference between completed and validated

This distinction implies different levels of responsibility.

**Completed** means the employee has declared that they have finished. It is a unilateral action: it closes things from their side, but the manager has not yet verified the result.

**Validated** means the manager has checked the work and accepted it. It is the definitive closure of a well-executed task.

In organisations where execution quality is critical —catering, logistics, technical installations— this distinction guarantees that no task is closed without supervision.

> **Important:** the employee rating is recorded on work that has already been reviewed. A task that is completed but not validated does not close the quality loop.

---

## Viewing statuses in the back office

From the task list you can filter by status and by priority. This lets the manager:

- See at a glance how many tasks are pending validation.
- Identify overdue or at-risk tasks through the time-compliance indicator.
- Check the progress of active tasks at a branch or for a particular employee.

Each task shows two colour labels: one for the status and one for time compliance. The colour code is consistent across the platform: grey for what has not yet started or is stopped (draft, cancelled, not started, paused), blue for what is under way or awaiting review (assigned, completed), amber for what needs attention (in progress, at risk, completed late), green for what is correct (validated, on time, completed on time) and red for what has failed (rejected, overdue).

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](./40-create-a-task.md) | Fields and options when creating a task |
| [Tracking and updates](./43-tracking-and-updates.md) | How progress is updated, pauses and the history |
| [Priorities and deadlines](./44-priorities-and-deadlines.md) | Configuring deadlines and alerts |
| [Task validation](./45-task-validation.md) | Validation flow and permissions |
| [Task notifications](./47-task-notifications.md) | Automatic alerts on status change |
