# Who finishes the task and closing it from administration

When a task has several people, you have to decide who considers it finished: the first one to finish, all of them, or one responsible person. And when nobody closed it from the app but the work was done, management can close it from the panel with its real times, so that the report is not left blank. This article explains both things and how what administration did is told apart in the history.

---

## What it solves

- **A training session for thirteen people is not closed when the first one finishes**: with *All people*, each one closes their part.
- **A team with a team leader**: only she starts and closes, even if there are managers or supervisors on the task.
- **The report comes out complete** even if the task was closed in the office: with the start and close times that are entered.
- **You know who did what**: what administration does from the panel appears as such, not as if a worker had done it.

---

## Who considers the task finished?

When creating or editing a task, the **Who considers the task finished?** field offers three options:

| Option | What happens |
|---|---|
| **One person is enough** | The first person to complete it closes it for everyone. This is the default option. |
| **All people** | Each person completes their part; the task closes when the last one finishes. |
| **One responsible person** | Only the responsible person starts, pauses and completes it, even if other assignees are supervisors or managers. On completing it, she closes it for everyone. |

With **One responsible person**, the **Responsible** field appears: choose one of the people already assigned. If you remove her from the task, you have to choose another before saving.

In the task record, the summary shows the option under **Completion** (for example, *Responsible: Ana López*), and in **Assigned team** the responsible person appears with *· Responsible*.

### What each person sees in the app

- With **All people**, whoever finishes their part sees *Your part is done. The task stays open for the others.*
- With **One responsible person**, the rest of the assignees see *… is responsible for this task: only they start, pause and complete it.* If someone tries, the app explains that only the responsible person can do it. Being a manager or supervisor and being assigned does not change this rule.

Whoever manages the task from the panel without being assigned to it can always act, to sort out whatever is needed.

> **Task-based schedule:** if staff work with a task-based schedule, the responsible person's **Exit** closes the task; the others' closes only their part.

---

## Completing a task from administration

If the work was done but nobody started the task in the app, the panel closes it by asking for the real times, so that the report is not left without a start or a time.

1. Open the task in the panel.
2. Click **Complete** (it is on assigned, in-progress or rejected tasks), or change its status to *Completed* from **Edit**.
3. **Complete task** opens: *Nobody started it from the app. Enter when it started and when it finished.* Fill in **Start** and **Close**.
4. Confirm.

The start has to be before the close, and the close cannot be later than now.

If the task had already been started, **Complete** does not ask for times: it already has its start.

### How it is recorded

- In the summary of the record, **Completed by** shows the name and *· from administration*.
- In the history, the completed line reads *From administration · started … and finished …* with the times that were entered.
- In the [task report](./48-task-reports.md), the **Start**, **End** and time columns show those times, and the **Completed by** column shows the name with *(from administration)*.

---

## "Administration" in the history

When an owner or an administrator acts from the panel —assigns, completes, cancels, validates—, the task history signs it as **By {name} · Administration**. This tells it apart from what people do from the app, even if whoever does it also has an employee record at some branch.

Assignments read *Assigned to …* and removals *Assignment removed: …*.

---

## Common problems

| Situation | What to do |
|---|---|
| The task is still open even though someone completed it | Look at **Completion**: with *All people* it closes when the last one finishes. Those who have finished see *Your part is done*. |
| An assigned manager cannot start the task | The task has a responsible person and it is not her. Change the responsible person in **Edit** or have the responsible person start it. |
| It will not save with *One responsible person* | In **Responsible**, choose one of the assigned people. |
| Completing from the panel asks for times | The task was not started from the app. Enter when it really started and finished: those are the times that will appear in the report. |
| "The close cannot be later than now" | Correct the **Close** time: a task cannot be closed in the future. |

---

## Related articles

| Article | Description |
|---|---|
| [Assign tasks to employees](./41-assign-tasks-to-employees.md) | Individual and multiple assignment |
| [Task statuses](./42-task-statuses.md) | Life cycle and time compliance |
| [Tracking and updates](./43-tracking-and-updates.md) | Starting, pausing, completing and the history |
| [Task reports](./48-task-reports.md) | The Excel with the **Completed by** column |
