# Teams

A **team** stores who works together, with which responsibility, in which job and at what hourly rate. It lets you add a whole crew to a branch —or to a project or site, depending on what your organisation calls its locations— in one go, instead of person by person.

It is designed for companies that move the same people from one project to the next: you set up the team once and apply it to each new project.

---

## How it works

- **A team is a template.** Each member carries their responsibility (worker, supervisor, manager or owner), their job and their hourly rate, but no branch.
- **Applying it to a branch** adds each member to that branch with those details, exactly as if it had been done by hand.
- **The branch prevails over the template.** Changing a job or a rate in the team does not change the branches where it was already applied: that is adjusted in each branch. The rate used by costs and reports is always the branch's.
- **Schedules are not part of the team.** They are set in the branch, as always.
- The same person can be in **several teams**, but not twice in the same one.

Teams are found in **Employees**, **Teams** tab.

---

## Create a team

1. In the side menu, open **Employees** and go to the **Teams** tab.
2. Press **Create team** and enter the **Team name**. There cannot be two teams with the same name; capitals, accents and extra spaces are ignored when comparing.
3. Open the team with **View team** and press **Add member**.
4. Choose the **Employee**, their **Responsibility**, their job in **Current occupation** —from the job catalogue or by typing a new one— and their **Hourly wage**.
5. Save. Repeat step 4 for each member.

From the team's page you can also **edit a member** or **remove them from the team**, and from the list you can **rename** or **delete** the team.

- Adding someone to a team or removing them **does not notify anyone** and gives them access to nothing: it only changes the template.
- Removing a person from the team does not take them out of the branches where the team was already applied.
- Deleting a team deletes the template; anyone already added to a branch with that team stays where they are.
- An employee who has left the company cannot be added (`employee/fired`). Being on holiday, on sick leave or having a **Pending** record does not prevent being in a team.

> **Tip:** if you already have a project with the crew set up, the quickest way is not to start from scratch: save that branch's staff as a team (see below).

---

## Apply a team to a branch

1. Open the branch record and, in its employee list, press **Apply team**.
2. Choose the **Team**. Before you confirm, its members are shown with their job and rate.
3. Review the list and confirm with **Apply to N people**.
4. When it finishes, the screen shows who was **Added** and who was **Not added**, with the reason.

What happens when you apply:

- Each person added is linked to the branch with the team's responsibility, job and rate. From that moment they can clock in there and can be assigned that branch's tasks.
- Each person added **receives the usual notification** of a new assignment.
- **Applying never overwrites what already exists.** Anyone already in that branch is skipped and keeps their job and rate. It also skips anyone who has left, whose record is incomplete, or whose record no longer exists.

The reasons you may see under **Not added** are:

| Reason | What it means |
|---|---|
| **Was already in this branch** | They had a responsibility there; it is kept as it was. |
| **Has left or their record is incomplete** | Their status is left or *pending*: they cannot work yet. |
| **Their record no longer exists** | The employee was deleted after being added to the team. |

> **Important:** review the list before confirming. Applying the wrong team to the wrong branch sends a notification to every person, and undoing it means removing each of them from the branch.

If, while the team is being applied, someone adds one of its members to that branch, the operation stops without changing anything and `team/apply_conflict` is shown. Apply the team again: that person will be skipped.

---

## Save a branch's staff as a team

1. Open the branch record and, in its employee list, press **Save as team**.
2. Give it a name and confirm.

Everyone active in that branch is copied with their responsibility, job and rate. **Schedules are not copied**, and anyone who has left is skipped. A branch with nobody active cannot be saved as a team (`team/branch_without_staff`).

---

## Teams and tasks

Teams are applied to **branches**, not to tasks. Once the team has been applied, its members are part of the branch and are selected one by one in the task form, like any other employee of that branch.

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Choosing the whole branch staff in a task, filtering by job or adding an entire team at once is planned for a future version.

---

## The employee app

Nothing changes for the employee. Someone who joins a branch through a team sees that branch in the app exactly as if they had been added by hand, with no need to update the app.

---

## Who can manage teams

Creating, editing and deleting teams, applying them and saving a branch as a team is reserved for the organisation's **owners and administrators** with active access to the back office.

---

## Related articles

| Article | Description |
|---|---|
| [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md) | Responsibilities, multi-branch and person-by-person assignment |
| [Roles and responsibility levels](./07-roles-and-responsibility-levels.md) | The levels each member carries |
| [Create and manage employees](./06-create-and-manage-employees.md) | Adding employees and their statuses, including Pending |
| [Assign tasks to employees](../06-tasks/41-assign-tasks-to-employees.md) | How tasks are assigned to the people in a branch |
| [Cost analysis](../07-operational-intelligence/54-cost-analysis.md) | Why the rate that counts is the branch's |
