# Several jobs for the same person

In many companies a person does not always do the same thing. The fitter who drives the van one day, the care assistant who covers as coordinator, the waiter who acts as head waiter at an event. Each job usually has its own hourly rate, and until now the record only allowed one per branch: that day's cost came out at the wrong rate.

Now a person can have **several jobs at the same branch**, each with its own hourly rate. One of them is the **default**, the one that applies when nobody chooses another. When you assign them a task or load a shift for them, you choose which job they go with, and the hours of that work are valued at that rate.

---

## What it solves

- **Paying for and costing each piece of work at its own rate**, not at the rate of the usual job.
- **No duplicate records.** One person, one record, several jobs.
- **Knowing afterwards who did what.** The task report says which job each person worked under on each task.

---

## Where it is configured

On the person's record, in the branch block (the same one that holds their responsibility, their **Current occupation** and their **Hourly wage**):

1. Open **Employees**, go into the person's record and open the relevant branch.
2. Their usual job stays in **Current occupation** with its **Hourly wage**: that is the default, and the *Default: {job}* label says so.
3. Under **Can also work as**, press **Add job** and enter the **Job** (from your company's job catalogue or a new one) and its **Hourly rate**.
4. Repeat for each job. **Remove job** takes it off the list.
5. Save.

To make another job the usual one, press **Make default** on its row: the two swap places and the old default moves to the list of additional jobs. A job cannot appear twice at the same branch, nor duplicate the default.

Jobs are **per branch**: the same person can have their own set at each site.

Only the **owner and administrators** see and edit each job's rate. Managers see the names of the jobs, without the rate.

---

## Where the job is chosen

With a single job there is nothing to choose: everything goes with that one. As soon as a person has more than one at a branch, an **As** selector appears in three places:

| Where | What happens |
|---|---|
| **When assigning a task** | In the row of each assigned person, **As** offers their jobs at that branch, with the default pre-selected. It can be changed later from **Assigned team** on the task page. See [Assign tasks to employees](../06-tasks/41-assign-tasks-to-employees.md#which-job-and-which-supplements). |
| **When loading a shift** | Under **More options** in the shift editor, the **Job** field. It applies to the shifts in the roster and to the standard week. See [By shifts](../04-calendar-and-schedules/114-shift-calendar-by-date.md#job-and-supplements-for-the-shift). |
| **If nothing is chosen** | The default applies. |

When the person clocks in, the clock record stores the job that applied that day: the one of the task they start, otherwise the shift's, otherwise the default. Changing a job's rate on the record later **does not change** what has already been clocked.

---

## Where you notice it

- **Task report**: the **Job** column of each row says which job the person worked under, and the hourly rate is that job's. See [Task reports](../06-tasks/48-task-reports.md).
- **Contract profitability** and **customer analysis**: hours are valued at the job they were done under. See [Contracts and profitability](../17-customer-portfolio/121-contracts-and-profitability.md).
- **Statistics and costs**: a person's cost per hour becomes the effective one, that of the jobs they actually held.
- **Teams**: a team carries one job per person, the one they are added with as the default. Additional jobs are added afterwards at the branch. See [Teams](./99-teams.md).

The attendance report does not change: it is about time, not money.

---

## What the person sees in the app

No rates. If you want, the job each task goes with may appear in its detail in an upcoming version of the app; today the app does not show it, and there is no need to update it to use this.

---

## Common problems

**I cannot see "Can also work as".** Open the branch inside the person's record: it is below the hourly wage. If you cannot see rates, your account is a manager's.

**The "As" selector does not appear on the task.** That person has a single job at that branch. Add the second one on their record.

**I changed the rate and last month's report is still the same.** That is expected: each clock record stores the rate it had when it was made. The new rate applies to clock records from now on.

**I want a different job to be the default.** **Make default** on the job's row, and save.

---

## Related articles

| Article | Description |
|---|---|
| [Supplements](./141-supplements.md) | What a person is paid on top of their job's rate |
| [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md) | Where the responsibility, the job and the hourly wage are set |
| [Assign tasks to employees](../06-tasks/41-assign-tasks-to-employees.md) | The "As" selector when assigning |
| [Task reports](../06-tasks/48-task-reports.md) | One row per task and person, with their job |
| [Cost analysis](../07-operational-intelligence/54-cost-analysis.md) | Where the cost per hour comes from |
