# Task incident

Sometimes the work cannot be done for reasons outside the control of the person who is going to do it: nobody opens the door, the material is missing, the customer has cancelled the visit. With the **task incident**, that person says so at the time, with a note and, if they wish, a photo. You find out straight away, by email and in the panel, without waiting for someone to open the task, and you decide what happens next: it is replanned, cancelled or marked as solved.

---

## What it solves

- **You find out while it can still be fixed**, not the next day when going through the list.
- **You know what happened**, in the words of whoever was there and with the photo if they took one.
- **Nobody pays for what did not depend on them**: while the incident is open, the task does not count in the overdue or late alerts.
- **There is a record**: who reported it, when, what they said and how it was resolved, in the history and in the task report.

---

## Reporting an incident

The people assigned to the task can report it and, from the app, so can supervisors and higher roles. From the panel, whoever manages the task. It can only be reported while the task is still to be done: not on a completed, validated, rejected or cancelled task.

### From the app

1. Open the task.
2. Tap the **three dots** at the top right and choose **Report incident**.
3. In **What happened?** explain what stopped you from doing the task. It is mandatory, up to 1,000 characters. For example: *nobody opened the door and I couldn't get in*.
4. If you wish, add a photo (JPG, PNG or WEBP) or a PDF of up to 20 MB in **Photo or file (optional)**.
5. Tap **Report incident**.

If you do not see the option, update the app to the latest version.

### From the panel

In the task record, the red **Report incident** button, the first one at the top. It asks for the same: the note and, if you wish, a photo or a file.

A task only has **one open incident at a time**. If there is already one, the app says so and shows the existing one.

---

## Who it notifies

As soon as it is reported, without waiting for anything:

| Who | How they find out |
|---|---|
| **Owners and administrators** | An email with who reported it, the task, the branch, the note and a **View task** button. |
| **Owners and administrators, in the panel** | The red **Incident on a task** alert, the first one in **Needs attention** on **Home**, with the task title and the note. |
| **Branch managers and supervisors** | An app notification with who reported it, the task and the note. |

The email can be turned off in **Tools → Email alerts → Set up alerts**, in the **Waiting for your decision** group, with the **Incident on a task** checkbox. The **Home** alert and the app notification do not depend on that checkbox.

---

## How a task with an incident looks

- **In the task record** (panel and app): a red band at the top, **Open incident**, with the note, *Reported by … · date* and the link to the file if there is one.
- **In Task management** (panel): the row is shown in red with the **Incident** label. A red chip with the number appears at the top, for example *2 tasks with an incident*, counting those across the whole company. Click it to see only those; with its **X**, or by changing any other filter, you go back to the full list. The chip only appears if there is at least one.
- **In the app**: the card has a red border and, if any is open, the **With incident** filter appears at the top of the list.

---

## Resolving the incident

It is resolved **from the panel**, by whoever manages the task.

1. Open the task: from the **Home** alert, from the link in the email or from the chip in **Task management**.
2. In the red band, click **Resolve incident**.
3. In **How was it resolved?**, choose:

| Option | What it does |
|---|---|
| **Replanned** | Changes the dates, the people or both: **New planned start**, **New due date** and **Assigned people**. Something has to change; if nothing needs to, choose *Solved*. |
| **Cancelled** | The task is cancelled, with the text of **Cancellation reason**. |
| **Solved** | It was fixed without touching the task, which stays as it was. |

4. If you wish, leave a **Note (optional)**.
5. Click **Resolve incident**.

The red band disappears, so does the **Home** alert, and the task counts normally again, with its new dates if it was replanned.

---

## What happens to the task in the meantime

- **Its status does not change.** It stays assigned or in progress, as it was.
- **It does not count as overdue or late** on **Home**, in the email alerts for overdue tasks or customer tasks not done, or among the tasks not started on time. The person went and could not do it: it makes no sense for it to count against them.
- **The task-not-started notification is not sent.**

---

## In the history and in the report

The task history records **Incident reported** (with *With photo or file* if it had one) and **Incident resolved: Replanned**, *Cancelled* or *Solved*, with who and when. It is the same in the app and in the panel.

The Excel [task report](./48-task-reports.md) includes them, open or already resolved:

- In the **Tasks** sheet, the **Incident** column (*Open* or *Resolved · how*), only if some task in the period had one.
- The **Incidents** sheet, with one row per incident: site, customer, task, task status, when and by whom it was reported, the note, whether it had a file, whether it is still open, how it was resolved, when, by whom and their note.

---

## Common problems

| Situation | What to do |
|---|---|
| **Report incident** does not appear in the app | Update the app. Also check that the task is not already completed or closed, that it does not have another open incident and that the person is assigned to it or is a supervisor. |
| "This task already has an open incident" | Only one fits at a time. Have it resolved from the panel and, if something else happens, report it afterwards. |
| The email does not arrive | Check in **Tools → Email alerts** that the **Incident on a task** checkbox is ticked and that email alerts are turned on. The **Home** alert appears anyway. |
| You used to leave an "Incident" type note | They are no longer created: to report a problem, use **Report incident**, which does notify. Old notes of that type are still visible. |

---

## Related articles

| Article | Description |
|---|---|
| [Task statuses](./42-task-statuses.md) | Life cycle and time compliance |
| [Tracking and updates](./43-tracking-and-updates.md) | Notes, history and tracking from the panel |
| [Task not started on time](./126-task-not-started-on-time.md) | The notification after 5 minutes, through the app, by email and on Home |
| [Task reports](./48-task-reports.md) | The Excel, with the incident column and sheet |
| [The home page: today, alerts and recent weeks](../07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md) | Where the red alert appears |
