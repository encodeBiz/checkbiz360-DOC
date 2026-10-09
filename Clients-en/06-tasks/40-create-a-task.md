# Create a task

Creating a task in CheckBiz360 is the starting point for assigning specific work to one or several employees. From the back office, managers and supervisors with permission can define every detail of the activity before sending it to the team.

This article describes all the fields available when creating a task and explains the process step by step.

---

## Task fields

### Required fields

- **Title** — Short, descriptive name of the task. It has to be clear enough for the employee to understand what it is about without having to read the full description.
- **Branch** — Workplace the task belongs to. It also determines the **operational time zone** used to interpret the task's dates; if the branch has no time zone of its own, the organisation's is used. **It cannot be changed once the task has been created**: if the wrong one was chosen, cancel the task and create another at the correct branch.
- **Deadline** — Date and time by which the task has to be completed. If it passes without completion, the task moves to *overdue* in its time-compliance indicator.

### Optional fields

- **Description** — Detailed explanation of what has to be done. It supports formatting: headings, lists, **checklists with tick boxes**, quotes, bold, italics and links. There is no length limit.
- **Work site** — Address where the work is done when it is not the branch itself, with its **margin** in metres. See [Own work site](#own-work-site).
- **Expected start date** — Time at which the employee is expected to start. It does not block anything on its own: its purpose is to trigger the late-start warning.
- **Notify if not started on time** — If enabled and the task has an expected start date, the system sends an automatic notification when **15 minutes** have passed since that time without the task having been started. Without an expected start date, the option has no effect.
- **Status** — Status the task is born with. The usual options are *Draft* (not yet visible to the team) or *Assigned* (already sent). The *Validated*, *Rejected* and *Cancelled* statuses cannot be selected manually at creation: they are the result of the task's life cycle.
- **Priority** — Low, medium, high or **critical**. It affects the order in which the task appears in the employee's app.
- **Assigned employees** — The person or people responsible for completing it. Several can be searched for and selected.

### Task configuration options

Three options control how the task is closed and reviewed:

| Option | Default | What it does |
|---|---|---|
| **Require evidence on completion** | Enabled | The employee cannot mark the task as completed without attaching at least one photo or video. If they try, they receive the error `task/evidence_required` |
| **Allow validation by supervisor** | Enabled | A branch supervisor can validate or reject the task, without needing a manager |
| **Allow rating by supervisor** | Enabled | A supervisor can score the employee's work when closing the task |

---

## Steps to create a task from the back office

1. Sign in to the back office with your manager, owner or supervisor-with-creation-permission credentials.
2. In the side menu, select **Tasks** and press the new task button.
3. Write the **title**.
4. Draft the **description**. Use the formatting bar to add checklists, headings or links if the task has several steps.
5. Search for and select the **branch**. The time zone the dates will be sent in appears below the field.
6. If the work is done at another address, fill in **Work site (optional)** and review the **margin**.
7. Where appropriate, state the **expected start date** and enable **Notify if not started on time**.
8. Set the **deadline** (date and time).
9. Choose **status** and **priority**.
10. Search for and select the **assigned employees**.
11. Review the three configuration options (evidence, validation and rating by supervisor).
12. Press **Save**. The assigned employees receive an automatic push notification.

> **Tip:** for tasks with several steps —opening premises, checking equipment, a cleaning protocol— use a checklist in the description. The employee reads the complete sequence in the app without needing a task per step.

---

## Writing the description with formatting

The description field includes a toolbar with bold, italics, code, heading, bulleted list, numbered list, **checklist**, quote and link. Pressing Enter inside a list continues the list automatically.

The **Preview** tab shows how the text will look once saved.

An example of a description with a checklist:

```
## Opening the premises
- [ ] Check the cameras
- [ ] Count the till
- [ ] Open the shutter

**Important:** notify the supervisor if cash is missing.
```

> **Note:** the tick boxes in the description are part of the task's text, not a saved state. They serve as a working script for the employee; the task's real progress is reflected through status changes, notes and evidence.

---

## Own work site

By default, a task is carried out at its branch, and the only location check is the clock-in one: the branch geofence when opening the workday.

When the work is done at another address —a customer's home, a building site, premises that change every day—, the task can carry its **own work site**. That way there is no need to set up a branch for each job.

### How it is configured

1. In the task form, type the address in **Work site (optional)** and **choose it from the list** of suggestions.
2. Review the **margin**: it is the radius, in metres, within which the employee is considered to be at the site. By default it takes the branch's radius and it can be widened; an underground car park or a warehouse needs more margin than a street doorway.
3. Save the task.

If the address is not precise enough to place the point —for example, the street number is missing—, the task is not saved and the error `task/worksite_imprecise` is shown. Complete the address and choose it again.

### What changes for the employee

- **Starting** the task requires being within the margin. The app sends the position and the server checks it; outside the margin, the start is rejected with `task/out_of_worksite`, which states the distance and the permitted margin, and the attempt is noted in the task history.
- **Resuming** a paused task requires the same as starting it.
- **Completing** is not blocked: the position is recorded, but the task can be closed even if the employee has already left the site.
- In the app, the task detail shows the address and a **View in Maps** link to get there.

In the back office, the **Work site** block in the task detail shows the branch, the address, the margin and a button to open the map.

> **Important:** a task with its own work site **can only be started, resumed or completed from the app**, because the back office does not send any location: if it is attempted from the panel, the action is rejected with `task/geo_required`. Pausing, cancelling, validating or rejecting it from the back office works normally.

---

## Duplicating a task

When a job is repeated, there is no need to fill in the form again. A task is duplicated with the **Duplicate** action, available in the task list and in the task's record.

The copy is created at the **same branch** and inherits the job: description, priority, configuration options and work site. It **does not inherit** its execution: no assigned employees, evidence, notes, ratings or history.

### Steps

1. Press **Duplicate** on the task you want to copy.
2. Review the **title of the copy**, which is proposed from the original's.
3. State the **deadline** and, where appropriate, the **expected start date**. The original's dates are deliberately not inherited: a copy with the old deadline would be born already overdue. They are interpreted in the branch's time zone.
4. Press **Duplicate**.

The copy is born as a **Draft** and unassigned. From the record, duplicating takes you straight to the copy: the next step is to edit it, assign the employees and set it to **Assigned**.

Anyone who can create tasks at that branch can duplicate them. The branch has to be active.

---

## Evidence and attachments

Evidence is not attached when creating the task: it is uploaded during execution, from the employee's app or from the task detail in the back office.

- From the **back office**, photos are attached in JPG, PNG or WEBP format, with a maximum of **5 MB** per file.
- From the **employee's app**, videos are also supported, with a maximum of **25 MB** per file.

The limits are the platform's default values and can be adjusted by configuration.

### Document-type attachments

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Attaching documents in PDF, Word or Excel format to a task is planned for a future version. When it is available, it will allow protocols, forms and data sheets to be included directly in the task detail.

---

## Assignment to several employees

The same task can be assigned to more than one employee. By default, **any of those assigned can complete it**: this is useful when the activity is resolved by whoever is available first.

If you need each employee to complete it independently, create one task per employee.

> **Note:** when you assign a task to several employees, each receives their own push notification, and each one's action history is recorded separately in the task's activity.

---

## Related articles

| Article | Description |
|---|---|
| [What the tasks module is](./39-what-is-the-tasks-module.md) | Overview of the module and its use cases |
| [Assign tasks to employees](./41-assign-tasks-to-employees.md) | Individual and team assignment |
| [Priorities and deadlines](./44-priorities-and-deadlines.md) | How to manage urgency and time limits |
| [Task statuses](./42-task-statuses.md) | Life cycle of a task |
| [Tracking and updates](./43-tracking-and-updates.md) | Starting, pausing and resuming a task |
| [Geofences and clocking radius](../03-time-tracking/16-geofences-and-clocking-radius.md) | The location check when clocking in |
| [Task notifications](./47-task-notifications.md) | What notifications employees receive |
