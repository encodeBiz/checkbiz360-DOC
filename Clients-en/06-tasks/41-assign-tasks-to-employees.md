# Assign tasks to employees

Assignment is the mechanism by which a task goes from existing in the system to being active on an employee's device. CheckBiz360 offers flexibility to assign tasks individually or to groups of employees, and allows them to be reassigned at any time if circumstances change.

---

## Individual assignment

Individual assignment links a task to a single employee. It is the most common method for specific activities where responsibility rests with one particular person.

When you select the employee during the creation or editing of the task, the system registers them as responsible. From that moment on, the task appears in their list of pending tasks inside the app and they receive a push notification.

This method is appropriate for maintenance tasks, specific training, handling an incident or any activity that has to be completed by one particular person.

---

## Assignment by team or branch

When the task is collective in nature or you want to distribute work among several members, it is possible to select more than one employee during assignment. All the recipients will receive the task in their app simultaneously.

> **Important:** in multiple assignment there is **a single task** shared by everyone assigned, not a copy for each. By default, **any of them can complete it**, and doing so closes the task for the group. What is recorded separately is each employee's participation: their assignment, when they started and what they contributed.

If you need each person to carry out the work independently, create one task per employee.

A task always belongs to a branch, so employee selection is made from those who work at that site.

> **Note:** the [teams](../02-employees/99-teams.md) in the Employees section are applied to branches, not to tasks. After applying a team to the branch, its members are selected in the task one by one, like the rest of the staff. Adding a whole team to a task at once is planned.

---

## Reassigning tasks

Circumstances change: an employee may be absent, change shift or turn out not to be the right person for a particular task. CheckBiz360 allows a task to be reassigned to another employee at any time, provided it is not in "completed" or "validated" status.

### Steps to reassign a task

1. Sign in to the back office and open the **Tasks** list.
2. Find the task you want to reassign and click on it to open the detail.
3. Press **Edit**. In the assigned employees field, remove the current employee and select the new recipient.
4. Press **Save**. On saving, whoever you have added is assigned and whoever you have removed is withdrawn. The new employee receives a push notification.
5. If you think it appropriate, add a note explaining the reason for the change.

You can also withdraw a person directly from the **Assigned team** block in the task detail.

> **Important:** On reassignment, the original employee stops seeing the task in their app. If they had already started the task or left comments, those entries are preserved and are visible from the back office.

> **Note:** a task's branch cannot be changed when editing it, so the employees you add have to work at that same branch.

---

## What the employee sees in the app

When a task is assigned to them, the employee receives a push notification on their device. On opening the app, they will find the task in their list of active tasks, ordered by priority and deadline.

Inside the task detail, the employee can consult:

- The title and the complete description of the activity, with its formatting: lists, checklists, headings and links.
- The priority assigned (critical, high, medium or low).
- The deadline date and time, and the expected start date if one was given.
- The work site, if the task has its own, with the **View in Maps** link.
- The evidence already uploaded and the task notes.
- The time spent and the total of pauses, and the task history (from version 1.4.0 of the app).

The employee can start the task, pause and resume it, add progress notes, upload evidence and, when they finish, mark it as completed.

---

## Automatic push notification on assignment

The moment the assignment is saved, CheckBiz360 automatically sends a push notification to the employee's device. No additional action is needed from the manager.

The notification includes the task title and the deadline, so that the employee has the essential information without needing to open the app.

If the employee has push notifications disabled on their device, the task will still appear in their list inside the app, but they will not receive the on-screen alert.

---

## Who has worked on the task

The **Assigned team** block in the task detail shows the people assigned. The **History** section tells the complete story —who created it, who started it, who paused or completed it— with the date and role of each action; it is described in [Tracking and updates](./43-tracking-and-updates.md#task-history).

None of this can be modified or deleted from the back office.

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](./40-create-a-task.md) | Fields and steps for creating a task from scratch |
| [Task statuses](./42-task-statuses.md) | Life cycle and status changes |
| [Tracking and updates](./43-tracking-and-updates.md) | How the employee updates progress |
| [Task notifications](./47-task-notifications.md) | Notification types and configuration |
| [Roles and responsibility levels](../02-employees/07-roles-and-responsibility-levels.md) | Description of each role on the platform |
