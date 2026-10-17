# The home page: today, alerts and recent weeks

When you sign in to the panel, the first thing you see is today's operation: how many people are in each site, who has not clocked in, which tasks are going wrong and what the day is costing so far. There is nothing to open and no period to choose: it is on **Home** and it refreshes on its own. Below it, the recent weeks with the same figures, so you know whether a bad day is one day or the start of something.

---

## What it solves

- **At 8:30, without clicking anything:** how many of those expected are already in each site, which site has nobody, and who is late.
- **Which tasks are due today** and which have not started on time.
- **How much has been spent so far today**, in hours and in materials.
- **Whether the week is going worse than the previous ones**, with the same figures week by week.
- **What needs attention**, in a short list that disappears when there is nothing.

It all comes from the clock-ins, tasks and schedules you already have in CheckBiz360: there is nothing to set up or maintain.

---

## Needs attention

At the very top, if there is something to look at, a list of alerts with a **View** link that takes you to the screen where it is fixed. When there is nothing, it says so: *No alerts: nothing needs your attention right now*.

| Alert | What happened |
|---|---|
| **No one on site** | People were expected at a site and nobody has clocked in. |
| **Low check-ins today** | Of those who should already be in, fewer than expected have clocked in. |
| **Many late arrivals** | A high share of those who clocked in today arrived late. |
| **Low check-ins** | Last week, only a small share of the planned working days had a clock-in. |
| **Overdue tasks** / **Tasks not started** | There are overdue tasks still open, or tasks that did not start on time. |
| **Workdays not closed** | Yesterday some working days were left open: people clocked in and never clocked out. |
| **Rising cost** | The daily cost is running above last month's. |
| **Missing rates** | Part of this month's hours has no rate: the estimated cost falls short. |
| **Many exits** | This month there are many leavers relative to the active headcount. |
| **Low availability** | One day this week has fewer than a third of the people available. |

---

## Today

Three figures and a table by site. Top right it shows when it last refreshed and whether it is **Live**; if there are clock-ins that have not arrived yet, it warns you.

| Figure | What it counts |
|---|---|
| **Workday** | *X of Y in*: of the people expected today, how many have clocked in and are still working or on a break. Below, how many are **not checked in** and how many are **late**. Lateness is measured against the entry tolerance configured for the site. |
| **Tasks** | How many are **due today**, how many have **not started on time** and how many are already **overdue**, counted against the current time. |
| **Hours** | The hours clocked today and what they cost: **labour** (each working day at its rate) and, if you have inventory, the **materials** consumed. If someone has no rate, the amount is marked *partial: missing rates*. |

The table shows, site by site, expected, in, not clocked in, late, today's tasks and cost. The sites that need most attention come first; **See all** unfolds the rest. A site in red is one where people should be and nobody has clocked in. A site closed today says *No workday scheduled today*.

### See more

Each figure has a **See more** that opens the detail without leaving the home page:

- **Workday:** by site, the list of people in the order that matters: first those **not checked in** (with the minutes late if they should already be in), then those **working** or **on break**, those whose **workday is finished**, those with a **workday not closed** and those **at another site** of theirs. Below, separately, those who **clocked in without being expected** and those with **yesterday's workday not closed**. If someone tried to clock in and was rejected, that shows too.
- **Tasks:** each task with its site, its assignees, the planned time and the deadline, and what is happening to it (*due today*, *not started on time*, *overdue*, *paused*). Each row opens the task record.
- **Hours:** by site, the hours and what they cost, what share of working days has a rate, and the material movements. It is the cost of what has been clocked today: it does not include what is planned for those who have not clocked in yet.

---

## Recent weeks

The same picture, week by week, for the last two months:

- **Coverage**: of the planned working days, how many had a clock-in.
- **Lateness**: what share of those who clocked in arrived late.
- **Tasks on time**: what share of the week's tasks was done on time.
- **Cost per week**: hours at their rate, plus materials.

Each figure carries the difference from the previous week, with the table by site below. The current week appears as *incomplete week*. Weeks before the home page started keeping the day-to-day record are marked *Rebuilt with the current calendar*: good for orientation, not for arguing about a payslip. At the start, until there are closed weeks, the block says so.

**Trend** links to **See in Analysis**, which opens the Operations panel on the last closed week.

---

## This week's availability

The next seven days, site by site: how many people are available each day according to schedules, public holidays and absences, and which is the **worst day**. A *Closed* day is one where nobody works nor should. It is the same calculation as the [availability board](../04-calendar-and-schedules/98-availability-board.md), narrowed to the coming week.

---

## Workforce over time

How many people the company had at the close of each month, split into **active**, **inactive** and **dismissed**, with each month's **hires** and **exits** and today's figure. **See employees** takes you to the list. Months before the platform started tracking status changes are marked as estimated: dismissals are dated by the last edit of the record, and inactive people count as active.

---

## Estimated costs

What the operation is costing in hours worked, **this month** against **last month**:

- **Cost per hour worked** and **cost per shift**, with the hours and working days behind them.
- How far the cost **per day** is above or below last month.
- **Workdays not closed** do not add up: nobody knows when they ended.
- If part of the hours has no rate, the amount is marked **incomplete** and says what percentage does.
- **Materials consumed**, if you have inventory.

It is an estimate: hours recorded at each job's rate, without social charges, and up to yesterday. Today is in the block above. Rates are set where each person is linked to their site: the more there are, the more exact the figure.

---

## Estimated CheckBiz cost this month

What your subscription will cost this month, worked out with today's headcount and the price of each contracted service, VAT excluded. It counts the active headcount plus dismissed people who clocked in this month, just like the invoice, and changes on its own when someone joins or leaves. On a trial, it says until when; on a custom price, it says so without a figure.

---

## Worth knowing

- **"Not clocked in" does not mean "absent".** The person may be working and not have clocked in. The home page shows the fact; the explanation is with their supervisor.
- **A site in red is something to look at, not an error.**
- **Someone who works at two sites counts at both.**
- **If a block cannot load, it does not show zeros**: it shows the notice. A zero on the home page is a real zero.
- The operation blocks appear **with CheckBiz contracted**. Without it, the home page shows only your services.

---

## Who can see it

Owners and administrators of the company.

---

## Related articles

| Article | Description |
|---|---|
| [The Operations panel](./56-dashboards.md) | The analysis by month: reliability, site effect and dependency |
| [Cost analysis](./54-cost-analysis.md) | Where the rate comes from and how to read the cost |
| [Availability board](../04-calendar-and-schedules/98-availability-board.md) | The full availability, month by month, with the breakdown of who is missing |
| [Weekly task calendar](../06-tasks/111-weekly-task-calendar.md) | The week's tasks, day by day and hour by hour |
| [Multi-branch global view](../08-branches-and-organisation/62-multi-branch-global-view.md) | Where each overview lives |
