# Your operations manager in Claude or ChatGPT

Building the week, adding the new hires, finding out who has not clocked in this morning and who can cover for them: it is the work that eats the evenings of whoever runs the operation. If you already use Claude or ChatGPT, you can hand it over. Connect CheckBiz360 to your assistant and ask for things in your own words: it does them in CheckBiz360 with your permissions, shows you what it is about to do, and saves nothing until you say yes.

---

## What it solves

- **"How is today going?"** Who has clocked in, who has not, who was late and which tasks have not started on time, site by site, starting with what needs attention.
- **"Lucía hasn't clocked in. Who can cover her ten o'clock job?"** The assistant tells you who is free at that time, who could with caveats and who is not available, and makes the change once you choose.
- **"Build next week for the North crew like last week, but Marta is off on Thursday."** It prepares the whole week, shows it to you and applies it when you confirm.
- **"Add these twelve people and these three sites."** Paste the list your accountant sent, an Excel file or a photo: the assistant reads it, tells you what it will create, and creates it.
- **"Are we doing better or worse than last month?"** It compares weeks, costs and alerts, and produces the working-time report you need.

It does all this with the permissions of whoever connects: no more and no less than that person can do in the panel.

---

## How it works, in three steps

| Step | What happens |
|---|---|
| **1. Connect** | Just once, with one address that works for all your companies. It takes two minutes. |
| **2. Ask** | In Claude or ChatGPT, in your words: "how is today going?", "build", "change", "add", "who…?". |
| **3. Review and confirm** | The assistant shows what it is about to do. It only applies it when you say yes. |

---

## 1. Connect

Use this connection address. It is the same for every company you administer:

```
https://api.checkbiz360.com/api/v1/assistant/mcp
```

**In Claude**

1. Open **Settings → Connectors** and click **Add custom connector**.
2. Type a name (for example, *CheckBiz360*), paste the address and click **Add**.
3. Click **Connect**, sign in with your CheckBiz360 user and your verification code, and authorise access.

**In ChatGPT**

1. Open **Settings → Apps and connectors** and click **Create**. If it is not there, first enable developer mode under **Advanced settings**.
2. Type a name, paste the address as the server URL, choose **OAuth** authentication and confirm.
3. Sign in with your CheckBiz360 user and your verification code, and authorise access.

When you authorise, you will see the list of companies it will have access to: the ones you administer. If you are given access to another company later, the assistant sees it without reconnecting; if your access is removed, it stops seeing it.

> **If you already connected a company with its own address** (the one shown under **Workspace**, in the company settings), it keeps working for that company. To work with all of them from a single connector, add the address above.

> **Before you start:** you need two-factor authentication enabled and to be an owner or administrator of at least one company. If the connection will not let you in, it is almost always one of those two.

---

## 2. Which company it works with

If you administer more than one company, the assistant asks at the start which one you want to work with. From then on:

- **It always names the company** when it proposes a change, so there is no doubt.
- **It does not mix companies** in a single action.
- **To switch**, just say so: "now for South Cleaning". You can have two conversations open with different companies without them getting in each other's way.

---

## 3. What you can ask

There are no commands to learn. Tell it what you need as you would tell someone on your team.

### See how the day is going

Who is working, who is on a break, who has not clocked in, who was late and by how much, working days left unclosed or still open since yesterday, clock-ins waiting for validation, and tasks due today or not started on time. It is the same data as the panel's home page. If you ask "what should I look at first?", it starts with the alerts.

The assistant says what it sees, not what it assumes: "has not clocked in", never "did not come in". CheckBiz360 knows the first; only you know the second.

### Cover for someone

Ask it who can cover a task. It answers in three groups:

- **Free:** their schedule covers that slot and they have nothing else at that time.
- **With caveats:** their shift does not cover the whole slot, or they already have another task at that time; it tells you which.
- **Not available:** on holiday, on leave, on a public holiday or without a shift that day, with the reason.

If the task is today, it also tells you who has clocked in. You choose the person; the assistant makes the change with the before and after in front of you.

### See availability

How many people are available each day at each site, and who is missing on a given day and why. It lets you spot next week's thin day before it arrives. In very large companies the query goes site by site.

### Build the whole week

- **Copy last week**, with the changes you tell it.
- **From scratch**, dictating the jobs.
- **From a document**: the rota your management software prints, an Excel file, a photo of the paper. The assistant reads it, recognises your people and turns it into each person's week.

In all three cases it shows you the proposal person by person, with the warnings worth checking (two jobs that overlap, a day that is a public holiday for someone), and a link to an Excel file with everything so you can review it calmly. Each person receives their week on their phone, with their hours and the address of each job, only when you confirm.

There is no limit on the number of tasks: if the rota is very large, the assistant loads it in parts and you confirm once at the end. If the week changes, ask it to propose it again with the right version: what was already there is updated and nothing is duplicated. Jobs the person had already started are kept.

### Single changes

Create a task, move it to another day or time, hand it to someone else, cancel it. Also change someone's standard week or move them to task-based scheduling. Before touching anything it shows you the before and after and waits for your yes.

### Add people and sites

A single person or site, or many at once from your accountant's list, an Excel file or a document. The assistant checks who already exists, tells you what it will create and which address it understood for each site, and creates everything when you confirm. The app welcome is not sent automatically: ask for it once you have checked everything is right.

### Analyse

- **Week-by-week trends:** clock-in coverage, lateness, tasks on time, hours and cost, for the whole company or by site.
- **This month's costs** against last month. If someone has no rate, the amount comes out as partial and the assistant tells you.
- **The alerts** the panel considers important, ordered by severity.
- **The working-time report** as PDF or Excel, for the company, a site or a person, between the dates you say. It gives you a link that expires in one hour, and the report also stays in the panel's report history.

---

## 4. What protects you

- **Nothing is saved without your yes.** Anything that changes the operation is proposed first and applied when you confirm. If you close the conversation without confirming, nothing happens.
- **It acts with your permissions, checked on every request.** It cannot do anything you could not do in the panel.
- **Whoever stops administering stops getting in, immediately.** If you remove or deactivate a collaborator in the company, their assistant loses access to it at that very moment. If they no longer administer any company, their connection is cut entirely.
- **It does not guess who you mean.** If a name is unclear or two people look alike, it asks, showing each person's email.
- **Times are the site's times.** "At ten" means ten in the branch's time zone, even if you are somewhere else.

---

## Privacy

When you connect, your employees' names and operational data are sent to the Claude or ChatGPT account you use. It is best to use a company account, not a personal one, and to check what that service does with your data. You can remove the connector at any time from Claude or ChatGPT: from that moment the assistant no longer has access.

---

## Common problems

| What happens | What to do |
|---|---|
| **Create** does not appear in ChatGPT | Enable developer mode under **Advanced settings** and go back to **Apps and connectors**. |
| The connection will not let me in | Check that two-factor authentication is enabled and that you are an owner or administrator of a company. |
| It says it has no access to a company | You do not administer it, or your access was removed. Ask it to show your companies: they are the ones you administer today. |
| I am not sure which company it is working with | Ask it. Tell it the company if you want to switch. |
| It says it cannot find a person | Their record may use a different name. Give it that person's email. |
| It proposes but does not apply | Say it clearly: "confirm", "apply it". It makes no changes without an explicit yes. |
| It suddenly stopped working | Reconnect from Claude or ChatGPT. If your access to your companies was removed, the connection is cut and you have to sign in again. |

---

## Who can connect

Owners and administrators with two-factor authentication enabled. Each person only sees the companies they administer.

---

## Related articles

| Article | Description |
|---|---|
| [The home page: today, alerts and recent weeks](../07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md) | The same data the assistant tells you, in the panel |
| [Availability board](../04-calendar-and-schedules/98-availability-board.md) | The availability the assistant cross-checks to cover for someone |
| [Import the weekly schedule](../04-calendar-and-schedules/108-import-the-weekly-schedule.md) | The same thing you ask the assistant for, done with an Excel sheet from the panel |
| [Add branches and staff from Excel](../02-employees/110-add-branches-and-staff-from-excel.md) | Bulk onboarding from the panel |
| [Organisation configuration](../08-branches-and-organisation/61-organisation-settings.md) | Where the Workspace tab is |
| [Two-factor authentication](../02-employees/09-two-factor-authentication.md) | The second factor the connection requires |
