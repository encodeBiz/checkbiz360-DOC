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
- **Customer** — Who the task is for, among the customers assigned to the branch. It only appears if the branch has customers. With a customer, the task can use their address as the work site and takes their instructions and contacts to the staff. See [The customer on the task](../17-customer-portfolio/119-the-customer-on-the-task.md).
- **Contract** — Which of the customer's contracts the task belongs to, or **No contract**. It appears when the customer has contracts. See [Contracts and profitability](../17-customer-portfolio/121-contracts-and-profitability.md).
- **Work site** — Address where the work is done when it is not the branch itself, with its **margin** in metres. See [Own work site](#own-work-site).
- **Expected start date** — Time at which the employee is expected to start. It does not block anything on its own: its purpose is to trigger the late-start warning.
- **Notify if not started on time** — If enabled and the task has an expected start date, the system warns when **5 minutes** have passed since that time without the task having been started: the assigned people in the app, and owners and administrators by email. Without an expected start date, the option has no effect. See [Task not started on time](./126-task-not-started-on-time.md).
- **Status** — Status the task is born with. The usual options are *Draft* (not yet visible to the team) or *Assigned* (already sent). The *Validated*, *Rejected* and *Cancelled* statuses cannot be selected manually at creation: they are the result of the task's life cycle.
- **Priority** — Low, medium, high or **critical**. It affects the order in which the task appears in the employee's app.
- **Assigned employees** — The person or people responsible for completing it. Several can be searched for and selected.
- **Who considers the task finished?** — *One person is enough* (the default), *All people* or *One responsible person*. See [Who finishes the task and closing it from administration](./127-who-finishes-the-task-and-closing-from-administration.md).

### Task configuration options

Three options control how the task is closed and reviewed:

| Option | Default | What it does |
|---|---|---|
| **Require evidence on completion** | Disabled | If you enable it, the employee cannot mark the task as completed without attaching at least one photo or video. If they try, they receive the error `task/evidence_required` |
| **Allow validation by supervisor** | Enabled | A branch supervisor can validate or reject the task, without needing a manager |
| **Allow rating by supervisor** | Enabled | A supervisor can score the employee's work when closing the task |

---

## Steps to create a task from the back office

1. Sign in to the back office with your manager, owner or supervisor-with-creation-permission credentials.
2. In the side menu, select **Tasks** and press the new task button.
3. Write the **title**.
4. Draft the **description**. Use the formatting bar to add checklists, headings or links if the task has several steps.
5. Search for and select the **branch**. The time zone the dates will be sent in appears below the field.
6. If the task is for a customer, choose them in **Customer** and, if it appears, their **Contract**. With **Use the customer's address as the work site**, review the **Margin**. If the work is done at another address, fill in **Work site (optional)** and review the **margin**.
7. Where appropriate, state the **expected start date** and enable **Notify if not started on time**.
8. Set the **deadline** (date and time).
9. Choose **status** and **priority**.
10. Search for and select the **assigned employees** and, if there are several, choose **Who considers the task finished?**.
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

### The boxes are ticked from the app

The assigned people tick and untick the boxes in the list from the task detail in the app, as they make progress. That way you can see in the panel which steps are done without asking.

- **There is one list per task.** If several people are assigned, what one ticks the others see.
- **Each tick goes into the history**: *Box ticked: "Count the till"* or *Box unticked: …*, with who and when.
- **Only boxes can be ticked from the app**: the rest of the text is changed by whoever manages the task, with **Edit**.
- **Once the task is closed** (completed, validated or cancelled) the list can no longer be changed from the app: it is the record of what was delivered.
- **If two people tick at the same time**, the app warns that the list had changed and shows the current one so they can tick again.
- **Ticking boxes does not send notifications.**
- **When the task is duplicated**, the copy is born with all the boxes unticked.

---

## Own work site

By default, a task is carried out at its branch, and the only location check is the clock-in one: the branch geofence when opening the workday.

When the work is done at another address —a customer's home, a building site, premises that change every day—, the task can carry its **own work site**. That way there is no need to set up a branch for each job.

### How it is configured

1. In the task form, type the address in **Work site (optional)** and **choose it from the list** of suggestions.
2. Review the **margin**: it is the radius, in metres, within which the employee is considered to be at the site. By default it takes the branch's radius and it can be widened; an underground car park or a warehouse needs more margin than a street doorway.
3. Save the task.

If the task is for a customer with an address, you can use **Use the customer's address as the work site** and adjust its **Margin** below; this is explained in [The customer on the task](../17-customer-portfolio/119-the-customer-on-the-task.md).

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

The copy is created at the **same branch** and inherits the job: description (with the boxes unticked), priority, configuration options, work site and attached documents. It **does not inherit** its execution: no assigned employees, evidence, notes, ratings or history.

### Steps

1. Press **Duplicate** on the task you want to copy.
2. Review the **title of the copy**, which is proposed from the original's.
3. State the **deadline** and, where appropriate, the **expected start date**. The original's dates are deliberately not inherited: a copy with the old deadline would be born already overdue. They are interpreted in the branch's time zone.
4. Press **Duplicate**.

The copy is born as a **Draft** and unassigned. From the record, duplicating takes you straight to the copy: the next step is to edit it, assign the employees and set it to **Assigned**.

Anyone who can create tasks at that branch can duplicate them. The branch has to be active.

---

## Attached documents and evidence

A task holds two kinds of file, and on the record (panel and app) they go in separate blocks:

| | **Attached documents** | **Evidence** |
|---|---|---|
| What for | What the person doing the task needs: a case file, some instructions, a plan | Proof that the task was done |
| Who usually uploads them | Management, when preparing the task | The person, when doing the work |
| Count towards **Require evidence on completion** | No | Yes |
| When the task is duplicated | They are copied with it | They are not copied |
| Can be removed | Yes, with **Remove from this task** | No |

### Attaching from the panel

1. On the task record, under **Resources**, press **Attach**.
2. Leave **It is evidence of the work done** unticked to upload an attached document: it accepts PDF (up to 20 MB) and JPG, PNG or WEBP photos (up to 5 MB).
3. Tick it only if the file proves the work done: then choose which **Employee** it belongs to; photos are accepted as evidence.
4. If you wish, write a **Description** and confirm.

### From the app

- When **creating or editing** a task from the app, **Attach document** adds PDFs or photos, which are uploaded on saving.
- In the task detail, the **Files and expenses** card has **Add → File** to upload a photo or a PDF that goes with the task.
- Evidence is uploaded as always: photo or video (up to **25 MB**) from the camera or the gallery.

Attaching Word or Excel documents is not available: convert them to PDF.

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
| [The customer on the task](../17-customer-portfolio/119-the-customer-on-the-task.md) | Choosing customer and contract, and what the staff see of the customer |
| [Geofences and clocking radius](../03-time-tracking/16-geofences-and-clocking-radius.md) | The location check when clocking in |
| [Task notifications](./47-task-notifications.md) | What notifications employees receive |
| [Who finishes the task and closing it from administration](./127-who-finishes-the-task-and-closing-from-administration.md) | One, all or one responsible person; completing with times from the panel |
| [Task not started on time](./126-task-not-started-on-time.md) | The warning after 5 minutes |
