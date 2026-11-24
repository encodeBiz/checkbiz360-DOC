# Supplements: driving, public holidays, night work

The collective agreement or the arrangement with your staff says that certain work is paid separately: driving more than a hundred kilometres, working on a public holiday, working nights, a hazard allowance. Until now that was noted down elsewhere and the task's cost came out short.

**Supplements** are what a person is paid **on top of** their job's rate for a particular task or shift. They are defined once in your company's catalogue and chosen afterwards, when assigning the task or loading the shift of whoever is paid them. The clock record stores them, and the task report, the contracts and the analyses add them to the cost, itemised.

---

## What it solves

- **Costing the task at what it really costs**, allowances included.
- **No typing in amounts every time.** The supplement is defined once; on the task you just choose it.
- **Having the trail.** The report says which supplement each person was paid, on which task, from which clock record and how much it came to.

---

## The three types

| Type | What it means | Example |
|---|---|---|
| **Fixed** | An amount per task or per clock-in session, regardless of the hours. | Driving allowance: an amount for the day they drive. |
| **Per hour** | An amount for every hour worked, on top of the job's rate. | Night work as an amount per hour. |
| **Percentage** | A percentage on top of the job's hourly rate. | Public holiday: *25* means 25% more on the hourly rate. |

A percentage is calculated on the rate of the job the work was done under, so the same "Public holiday, 25%" is worth a different amount for a skilled worker and for a labourer. That is usually what the agreement says.

---

## Creating the catalogue

Supplements live under **Employees**, on the **Supplements** tab.

1. Press **Add supplement**.
2. Enter the **Name**, as your agreement calls it: *Driving allowance*, *Public holiday*, *Night work*.
3. Choose the **Type**: *Fixed*, *Per hour* or *Percentage*.
4. Enter the **Value**: the amount or, for a percentage, a figure from 0 to 500.
5. Save.

There cannot be two supplements with the same name. **Edit** changes the name, type or value for whatever is chosen from then on: **what has already been assigned keeps the value it had when it was chosen**. **Deactivate** removes it from the selectors without deleting anything; whatever already had it does not change, and you can **Reactivate** it.

Only the **owner and administrators** see and edit the value of supplements. Managers see the catalogue by name and can choose supplements on tasks and shifts, without seeing amounts.

---

## Choosing them on the task or on the shift

A supplement belongs to **one person on one particular piece of work**, not to the whole task: on a task with three people, only the one who drives may be paid it.

| Where | How |
|---|---|
| **When assigning a task** | In the row of each assigned person, press **Supplement** and choose one from the catalogue; repeat if they are paid more than one. Each one appears as a tag that can be removed. See [Assign tasks to employees](../06-tasks/41-assign-tasks-to-employees.md#which-job-and-which-supplements). |
| **From the task page** | Under **Assigned team**, the **Job and supplements** action for each person lets you change them while the task is not completed. |
| **When loading a shift** | Under **More options** in the shift editor, the **Supplements** field. It applies to the shifts in the roster and to the standard week. See [By shifts](../04-calendar-and-schedules/114-shift-calendar-by-date.md#job-and-supplements-for-the-shift). |

If a person also has [several jobs](./140-several-jobs-for-the-same-person.md), they choose which one they go with in the same row.

When the person clocks in, the clock record stores the supplements that applied: those of the task they start or, failing that, the shift's. Each one is stored with the value it had at that moment.

A **fixed** supplement is paid once per clock-in session (or once for the assignment, if the task had no clock records). **Per hour** and **percentage** supplements go with that person's hours on that task.

---

## Where you notice it

- **Task report**: each person row carries **Supplements** (the names with their value) and **Supplements (amount)**, and the person's cost includes them. The **Supplements** sheet is the trail, line by line. See [Task reports](../06-tasks/48-task-reports.md).
- **Contracts and customer analysis**: the contract's gross cost adds supplements as a line of their own, alongside staff, material and expenses. See [Contracts and profitability](../17-customer-portfolio/121-contracts-and-profitability.md).
- **Statistics and costs**: the branch's cost, the cost per hour and the financial deviation include them and state them separately.

The attendance report does not carry them: it is about time, not money.

---

## What the person sees in the app

Nothing: neither values nor amounts. Supplements are an administration tool.

---

## Common problems

**I cannot see the "Supplements" tab or the amounts.** Your account is a manager's. The owner and administrators create the catalogue; you can choose supplements by name on tasks and shifts.

**I cannot choose a supplement on the task.** The catalogue is empty or every supplement is deactivated. Create it under **Employees → Supplements**.

**I corrected a supplement's value and the report does not change.** What has already been chosen keeps its value. If it was a mistake on a particular task, remove the supplement from that person under **Job and supplements** and add it again: it comes in with the new value.

**I want the public holiday or the night shift to apply on their own.** Today supplements are chosen by hand on the task or the shift: the platform does not decide for you which day is a public holiday under your agreement. Load the holiday's shift with its supplement.

**An allowance that is an amount per kilometre.** Define it as fixed with the amount of the usual distance, or create two (*Short drive*, *Long drive*). The exact amount per kilometre is not calculated.

---

## Related articles

| Article | Description |
|---|---|
| [Several jobs for the same person](./140-several-jobs-for-the-same-person.md) | Jobs with their rate and the default |
| [Assign tasks to employees](../06-tasks/41-assign-tasks-to-employees.md) | Choosing job and supplements when assigning |
| [By shifts: the schedule is the shifts you load](../04-calendar-and-schedules/114-shift-calendar-by-date.md) | "More options" on the shift |
| [Task reports](../06-tasks/48-task-reports.md) | The By person and Supplements sheets |
| [Contracts and profitability](../17-customer-portfolio/121-contracts-and-profitability.md) | Supplements in the contract's cost |
