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

## Which job and which supplements

When assigning, each person chosen takes up a row on the form. Two more things can appear in that row, depending on what your company has configured:

- **As**: which job that person goes with on that task. It only appears if they have **more than one job** at that branch; the default is pre-selected. See [Several jobs for the same person](../02-employees/140-several-jobs-for-the-same-person.md).
- **Supplement**: what they are paid on top for that task (driving, public holiday, night work, etc.), chosen from your company's catalogue. Several can be added, and each one is removed from its tag. It only appears if the company has defined supplements. See [Supplements](../02-employees/141-supplements.md).

Both belong to **the person on that task**, not to the whole task: on a task with three people, only the one who drives may be paid the driving allowance. If nothing is chosen, the person goes with their default job and no supplements, as before.

From the task page, in the **Assigned team** block, the **Job and supplements** action for each person lets you change them afterwards, as long as the task is not completed or validated. When the person clocks in on the task, the clock record stores the job and the supplements that applied: that is where the columns of the [task report](./48-task-reports.md#what-it-contains) and the cost of [contracts](../17-customer-portfolio/121-contracts-and-profitability.md) come from.

Managers and supervisors choose job and supplements by name, without seeing rates or amounts.

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
- The attached documents, the evidence already uploaded and the task notes.
- The time spent and the total of pauses, and the task history (from version 1.4.0 of the app).

The employee can start the task, pause and resume it, tick the boxes in the description, add progress notes, upload evidence, [report an incident](./125-task-incident.md) if they cannot do it and, when they finish, mark it as completed.

---

## Automatic push notification on assignment

The moment the assignment is saved, CheckBiz360 automatically sends a push notification to the employee's device. No additional action is needed from the manager.

The notification includes the task title and the deadline, so that the employee has the essential information without needing to open the app.

If many tasks are assigned to the same person at once, they receive **a single notification** with the summary (*You have 84 new tasks from 3 to 30 November*), which opens their list with those days when tapped. See [Grouped notifications](./47-task-notifications.md#grouped-notifications-many-tasks-one-notification).

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
| [Several jobs for the same person](../02-employees/140-several-jobs-for-the-same-person.md) | The "As" selector when assigning |
| [Supplements](../02-employees/141-supplements.md) | What a person is paid on top on a task |
| [Roles and responsibility levels](../02-employees/07-roles-and-responsibility-levels.md) | Description of each role on the platform |
