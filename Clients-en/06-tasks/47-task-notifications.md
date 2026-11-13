# Task notifications

CheckBiz360 sends automatic notifications to the people involved every time a relevant event occurs in a task's life cycle. The aim is that nobody has to review task statuses manually: the system informs each person at the exact moment they need to act or be aware.

Notifications are based on specific life-cycle events —assignment, validation, rejection, update— and on two alerts the system triggers itself: the **late start** one and the **deadline** ones. Both are described below.

---

## Notification channels

Task notifications are distributed through two channels:

**Push notifications in the mobile app:** Sent to the employee's device. They appear as alerts on the phone screen even when the app is not open, provided the employee has granted notification permission to the application.

**Back office notifications:** They accumulate in the back office notification panel and are visible to the manager and the supervisor. They include a counter of unread notifications on the bell icon in the top menu.

---

## Notification types

### New task assigned

**Recipient:** Employee assigned to the task.

**Channel:** Push in the app.

**When it is sent:** At the moment the manager saves the task with the employee assigned.

**Content:** Task title, priority assigned and deadline. The employee can tap the notification to open the task detail in the app directly.

---

### Grouped notifications: many tasks, one notification

When a person receives many tasks at once —when a rota is loaded, when the month is planned—, they do not get one notification per task. The **new**, **changed** and **removed** tasks are grouped and **a single notification** arrives once changes stop coming in, for example: *You have 84 new tasks from 3 to 30 November, 2 changed*. When tapped, the app opens their task list with those days.

A single task arrives as always, with its title, at most a couple of minutes later. If a task is removed from the person or cancelled, the notification says so: *You no longer have the task …: it has been removed or cancelled.* Confirming a rota again without changes sends nothing.

---

### Task validated

**Recipient:** Employee whose task has been validated.

**Channel:** Push in the app.

**When it is sent:** At the moment the manager or supervisor confirms the validation.

**Content:** Task title, name of the manager who validated it and the score obtained if a rating has been recorded.

---

### Task rejected

**Recipient:** Employee whose task has been rejected.

**Channel:** Push in the app.

**When it is sent:** At the moment the manager or supervisor records the rejection.

**Content:** Task title, name of the manager who rejected it and the reason for the rejection. The employee can tap the notification to see the full detail and the associated comment.

---

### Task updated by the employee

**Recipient:** Manager or supervisor responsible for the task.

**Channel:** Back office notification; optionally push if the manager has the app installed.

**When it is sent:** When the employee changes the task status (starts, completes) or adds a comment.

**Content:** Employee's name, task title and the nature of the change made.

> **Note:** pausing and resuming a task does not send any notification. It is a routine action, and alerting on every pause would lead to the important alerts being ignored. Pauses can be consulted in the task history.

---

### Late-start warning

**Recipient:** the assigned people, with a notification in the app, and the owners and administrators, by email.

**When it is sent:** when **5 minutes** have passed since the expected start date without the task having been started. Tasks left unstarted at the same time go in a single email. It is explained in full in [Task not started on time](./126-task-not-started-on-time.md).

**Requirements:** the task must have an **expected start date** and the **Notify if not started on time** option enabled. Without an expected start date, the option has no effect.

It is the only alert configured task by task, and it is enabled when creating or editing the task. The dispatch is recorded in the task's activity, so the manager can check whether it actually went out.

---

### Task incident

**Recipient:** the branch managers and the supervisors, with a notification in the app; the owners and administrators, by email and with a red alert on **Home**.

**When it is sent:** at once, when someone reports that they cannot do the task.

**Content:** who reported it, the task, the branch and the note. It is explained in [Task incident](./125-task-incident.md).

---

### Deadline warnings

**Recipient:** the people involved in the task.

**When they are sent:** when the task is approaching its deadline and when it passes it without being completed.

Each warning is issued **only once per task** and is recorded, so that the same deadline does not generate repeated notifications day after day.

---

## Configuring how often alerts are sent

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

How far in advance deadline warnings are sent is not configurable by the customer in the current version. Being able to adjust that lead time, enable a second reminder and vary the frequency by task priority is planned for a future version.

---

## Requirements for receiving push notifications

For the employee to receive push notifications on their device, the following conditions have to be met:

1. Have the CheckBiz360 app installed and have signed in at least once.
2. Have granted notification permissions to the app when the operating system asked for them.
3. Have an internet connection on the device at the moment of sending, or get one as soon as they connect.

If the employee has disabled the device's notification permissions, the alerts will not reach their screen. In that case, the task will still appear in their list inside the app, but the employee will have to open it manually to see what is new.

---

## Related articles

| Article | Description |
|---|---|
| [Assign tasks to employees](./41-assign-tasks-to-employees.md) | Automatic notification on assignment |
| [Task statuses](./42-task-statuses.md) | Events that generate notifications |
| [Priorities and deadlines](./44-priorities-and-deadlines.md) | Deadline alerts and configuration |
| [Task validation](./45-task-validation.md) | Notification on validating or rejecting |
| [What the tasks module is](./39-what-is-the-tasks-module.md) | Overview of the module |
| [Task not started on time](./126-task-not-started-on-time.md) | The warning after 5 minutes and how to turn off the email |
| [Task incident](./125-task-incident.md) | The immediate notification when a task cannot be done |
