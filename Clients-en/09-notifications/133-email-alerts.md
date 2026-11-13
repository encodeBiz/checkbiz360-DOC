# Email alerts

What needs your attention does not wait for you to open the panel. Every morning, the company's owner and administrators receive an email with what is worth looking at that day; and what cannot wait, such as a vacation request starting the day after tomorrow or a new issue from staff, arrives straight away. You choose which alerts arrive and what time the summary goes out.

---

## What it solves

- **Starting the day knowing what to look at**, without opening the panel: workdays left open yesterday, overdue tasks, days of the week with few people, information sheets not signed.
- **Not leaving anyone waiting**: requests, issues and documents waiting for your reply arrive in the same email.
- **Reacting in time** to what is happening in the day's operation, such as a task that has not started on time.
- **An inbox that does not fill up**: if there is nothing new, nothing is sent.

There is nothing to activate: it comes turned on for every company, with all alerts ticked and the summary at 8:00.

---

## Who receives it

The company's **owners and administrators**, and nobody else. Being a manager or supervisor of a site does not get you the email. The email is the same for all of them: what is chosen in Tools applies to all of them. A person who is both owner and administrator receives a single email.

It comes from `hola@encodebiz.com`. If you do not see it, check your spam folder (see [Email notifications](./68-email-notifications.md#what-to-do-if-the-email-does-not-arrive)).

---

## The three groups of alerts

### Morning summary

One email a day, at the time you choose between 6:00 and 10:00 (company time), with what is worth looking at. Each alert has a button that takes you to the screen where it is resolved.

| Alert | What it tells you |
|---|---|
| **Overdue tasks** | Tasks past their date and still open. |
| **Workdays not closed** | Yesterday's workdays left without a clock-out. |
| **Many late arrivals** | Sites where a large share of staff arrived late yesterday. |
| **Low availability** | Days this week with few people available. |
| **Low check-ins this week** | On Mondays, sites with few check-ins last week. |
| **Access email not delivered** | People who have not received their app access email. |
| **Data protection notice not signed** | People who have not signed the data protection information sheet. |
| **Workdays over 9 h** | People with a configured workday of more than 9 hours. |
| **No weekly rest** | People with all 7 days of the week planned. |
| **Rising cost** | On Mondays, if the daily cost is above last month's. |
| **Missing rates** | On Mondays, if many hours have no rate and the cost falls short. |
| **Many exits** | On Mondays, if there are more leavers than usual this month. |

The same list in the panel also includes the customer portfolio alerts (customer tasks not done, fewer hours for a customer, contracts over plan or ending). They are explained in [The customer in the analyses](../17-customer-portfolio/123-the-customer-in-the-analyses.md).

The three about workdays and the information sheet are explained in [Schedule and information sheet alerts](#schedule-and-information-sheet-alerts), further down.

### Right now, in operations

What is happening right now in the day's work and needs a quick response. Today it is **Task not started**: a task with a start reminder that has not started on time. Those from the same site at the same moment go in a single email. It is explained in the tasks section.

### Waiting for your decision

What someone on staff is waiting for you to answer or sign.

| Alert | When it arrives |
|---|---|
| **Requests awaiting a decision** | In the morning summary: vacation and leave requests waiting for your reply, with the oldest one. |
| **Request starting soon** | Straight away, when an unanswered request starts today, tomorrow or the day after. |
| **Open issues** | In the summary: issues from staff still under review. |
| **New issue** | Straight away, when someone on staff opens an issue from the app. |
| **Incident on a task** | Straight away, when someone reports they could not do a task. |
| **Document not signed** | In the summary, only twice: 2 days after it was sent and again after a week. It says who has yet to sign. |
| **Document signed** | Straight away, when someone signs a document that requires acknowledgement. It says whether they signed with the phone's fingerprint or face or only confirmed they had read it. |
| **Expenses to approve** | In the summary, the expenses staff logged from the app that are waiting for your approval. |

Issues opened by the system itself when a workday is left without a clock-out do not count here: they already appear as **Workdays not closed**.

---

## When it arrives and when it does not

- **Nothing new, no email.** An alert goes into the summary on the day it appears and on the day it gets worse. If it stays the same, it comes back only on Mondays. That way, a rising cost lasting three weeks does not reach you twenty mornings in a row.
- **Nothing is sent at night.** Between 22:00 and 6:00, company time, the "straight away" alerts wait and go out at the time of the morning summary.
- **A company with no activity** in the last 30 days does not receive a summary.

---

## Choosing which alerts are received

1. In the side menu, open **Tools**.
2. In the **Email alerts** block, click **Set up alerts**.
3. With **Send alerts by email** off, no alert emails go out. With it on, choose:
   - **Morning summary time**, between 06:00 and 10:00.
   - The checkboxes for each alert, in their three groups. Untick the ones you do not want to receive.
4. Click **Save**.

The change applies to all the company's owners and administrators. Unticking an alert only removes the email: the alert still appears on **Home**.

> **Role note:** **Tools** is only visible to the company's owners and administrators.

---

## Schedule and information sheet alerts

Three alerts for things that may bring a legal problem and are not visible day to day. They appear on **Home**, in **Needs attention**, and in the morning summary.

| Alert | Colour | What it says | What to do |
|---|---|---|---|
| **Workdays over 9 h** | Orange | Who has a configured workday of more than 9 hours, with names. | Check that their schedule is the real one. It may be covered by their collective agreement: the alert states the fact, not that it is wrong. |
| **No weekly rest** | Orange | Who has all 7 days of the week planned. | Check those people's schedules. |
| **Data protection notice not signed** | Red | Who has not signed the data protection information sheet, and how many have not been sent it. | Send it from Document management. See [Data protection information sheet](../12-regulatory-compliance/137-data-protection-information-sheet.md). |

The two schedule alerts look at the schedule each person clocks in with; anyone who has not clocked in during the last two weeks is not included. That is why the figure may not match the one in the Analysis tab, which covers the whole month.

> **Warning:** on the first day, "Data protection notice not signed" will show almost all your staff if you never sent them the sheet. That is expected: it shrinks as staff sign from the app.

---

## Common problems

**The summary does not reach me.** Check your spam folder. Check in Tools → Email alerts that the switch is on. And remember that on a day with nothing new there is no email.

**It reaches someone who should not get it.** All accounts with owner or administrator access receive it. If an administrator account should not receive it, change its role in **Entity → Collaborators**.

**I want a site manager to receive it.** That is not possible: these emails are only for owners and administrators.

**A request notified me at 8:00 and not during the night.** That is intended: what comes up between 22:00 and 6:00 waits until the summary time.

---

## Related articles

| Article | Description |
|---|---|
| [The home page: today, alerts and recent weeks](../07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md) | The same alerts, on Home |
| [Email notifications](./68-email-notifications.md) | The rest of the platform's emails |
| [Vacation and leave from the app](../04-calendar-and-schedules/115-vacation-and-leave-from-the-app.md) | Replying to requests |
| [Correct an incomplete workday](../03-time-tracking/134-correct-an-incomplete-workday.md) | Closing workdays left without a clock-out |
| [Data protection information sheet](../12-regulatory-compliance/137-data-protection-information-sheet.md) | Sending it and keeping proof of the signature |
