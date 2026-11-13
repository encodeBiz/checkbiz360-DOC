# Task not started on time

A visit was due to start at 9:00 and at 9:05 nobody has tapped **Start**. It may be an oversight, or there may be nobody there. CheckBiz360 notifies after **5 minutes**: the person, so they can start it if they are already working, and management, so they can call before the customer notices.

---

## What it solves

- **You find out after 5 minutes**, not at the end of the day.
- **The person gets their reminder** on their phone, in case they forgot to tap **Start**.
- **Several tasks, a single email**: if several are left unstarted at the same time, they arrive together in a list.
- **On Home from the first one**: a single unstarted task is enough to see it on the home page.

---

## How it is turned on

The notification belongs to each task. When creating or editing it:

1. Enter the **expected start date**.
2. Tick **Notify if not started on time**.
3. Click **Save**.

Without an expected start date, the checkbox has no effect. In the task record, the **Start reminder** label shows that it is scheduled and changes to **Reminder sent** when it goes out.

> **Note:** the help text of the checkbox still mentions 15 minutes. The notification goes out after 5.

---

## What happens after 5 minutes

If 5 minutes after the expected time the task is still assigned and not started:

| Who | What they receive |
|---|---|
| **The assigned people** | An app notification. |
| **Owners and administrators** | An email with the task and its time. If several have been left unstarted at the same time, a single email goes out with the list: up to three with their time (and their site, if they are from several) and how many more there are. |
| **Owners and administrators, in the panel** | The **Tasks not started** alert in **Needs attention** on **Home**, from a single task. In **Today**, the **Tasks** figure counts them as *not started on time*. |

**Home** counts all assigned tasks with an expected start date that have gone 5 minutes without starting, whether or not the notification checkbox is ticked: the checkbox decides the app notification and the email, not what is shown on the home page. As soon as someone starts the task, it stops counting.

The email is also sent for people who work with a task-based schedule.

---

## When it does not notify

- **The task is in draft.** It is not in circulation yet.
- **The task has an open [incident](./125-task-incident.md).** It is already known why it has not started.
- **The start time passed more than an hour earlier** when the task came into the notification, for example because it was created or assigned late. No notifications are sent about something that is already old.
- **It has already notified once.** Each task notifies only once.

---

## How to turn it off

- **For a specific task:** untick **Notify if not started on time** on the task. Neither the app notification nor the email goes out; if it has an expected start date, it still counts as not started on **Home**.
- **Only the email, for the whole company:** in **Tools → Email alerts → Set up alerts**, **Right now, in operations** group, untick **Task not started** and click **Save**. People still receive their app notification and the **Home** alert still appears.

Email alerts are set up by owners and administrators, and what is ticked applies to all of them.

---

## Common problems

| Situation | What to do |
|---|---|
| No notification has arrived | Check that the task has an **expected start date** and **Notify if not started on time** ticked, and that it is not in draft and has no open incident. |
| The app notification arrives but not the email | Check in **Tools → Email alerts** that **Task not started** is ticked and that email alerts are turned on. |
| The person had started and got the notification anyway | They were probably working but did not tap **Start** on the task. The notification looks at the task, not at the clock-in. |
| Too many emails arrive | Untick **Task not started** in the email alerts, or remove the notification from the tasks where it is not needed. |

---

## Related articles

| Article | Description |
|---|---|
| [Create a task](./40-create-a-task.md) | The expected start date and the notification checkbox |
| [Task notifications](./47-task-notifications.md) | All task notifications |
| [Task incident](./125-task-incident.md) | When the task cannot be done |
| [The home page: today, alerts and recent weeks](../07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md) | The **Tasks not started** alert and the **Today** figure |
