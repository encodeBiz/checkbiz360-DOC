# Availability board

The availability board answers a question that the schedule alone does not: **how many people are actually available each day at each branch, and who is missing**. It is not data that has to be maintained: the board calculates it by crossing each employee's schedule with the public holidays, their absences and the status of their record.

It is found in **Schedules** → **Availability** tab.

---

## What it shows

A grid with one row per branch and one column per day. Each cell shows how many people are available that day out of the branch's total workforce, with the coverage percentage.

The colour of each cell summarises the situation:

| Colour | Legend | What it means |
|---|---|---|
| Green | **Coverage ≥ 70%** | Most of those who should be working are available. |
| Amber | **Tight coverage 55 – 70%** | Quite a few people are missing; it is worth reviewing. |
| Red | **Critical coverage < 55%** | There are people who should be there and are not: a coverage gap. |
| Grey | **Day off or holiday** | Nobody works that day, nor should they: the branch is closed or it is a public holiday. |

The difference between grey and red is the most important one on the board. A company public holiday shows as **grey**, because nobody is missing. A working day on which half the workforce is on holiday shows as **red**, because it is a coverage problem.

Employees who have no branch assigned appear grouped in a separate row.

---

## How to use it

- **Monthly or weekly view.** Switch between **Monthly** and **Weekly**, and move forwards or backwards with the period arrows.
- **Filter by branch.** By default **All** are shown; choose one to focus on it.
- **Export.** The **Export** button downloads a CSV file with one row per branch and day: team, date, available, headcount and coverage percentage.

> **Note:** if the workforce is too large to be calculated all at once, the board will ask you to choose a branch to see its coverage.

---

## The breakdown of a day

Click a cell to open the breakdown for that day at that branch. It shows two columns:

- **Available**: who is in.
- **Unavailable**: who is not, and why.

The possible reasons are:

| Reason | What it means |
|---|---|
| **No shift** | Their schedule has no shift that day. |
| **Holiday** | It is an organisation or branch public holiday. |
| **Absence** | They have an absence of their own recorded: holidays, leave, a day off. |
| **Leave** | The status of their record indicates that they are not active. |

The breakdown includes a search box by name, which ignores accents and the letter ñ and accepts first name and surname in any order.

---

## Adding or removing a day off from the breakdown

The most common action when looking at the board is "this person is not coming in tomorrow". It is recorded from the breakdown itself:

- **Add day off**: drag the person from **Available** to **Unavailable**, or press the arrow on their row.
- **Remove day off**: drag the person back, or press the arrow.

Dropping does not save anything on its own: the usual form opens, with the person and the date already filled in, where you can state whether the absence is **paid**. An accidental drag is undone with **Cancel**.

Only someone who is missing because of an **absence of their own** can be returned to available. The other reasons cannot be fixed from here, and their arrow appears disabled with an explanation:

- An organisation or branch **public holiday** affects the whole workforce: it is managed in its calendar.
- **No shift** depends on that person's schedule: it is changed in their calendar.
- **Leave** is the status of their record: it is changed there.

After each change, the board recalculates coverage with the saved data.

---

## Who can see it

- Owners, administrators and managers see the availability of the whole organisation.
- Supervisors see the availability of their branches.
- Employees without management responsibility have no access.

---

## Current limitations

- Someone who works at **two branches** counts at both: assigning a shift by day and branch does not exist yet.
- If a public holiday has a date that cannot be read, the board discards it and warns about it on screen; the coverage figure does not count it.

---

## Related articles

| Article | Description |
|---|---|
| [Base schedules and shifts](./23-base-schedules-and-shifts.md) | The weekly schedule the calculation starts from |
| [Work calendar](./24-work-calendar.md) | Public holidays by level and their effect on clocking in |
| [Public holidays and non-working days](./29-public-holidays-and-non-working-days.md) | Employee absences, ranges and the paid mark |
| [Assign employees to branches](../08-branches-and-organisation/60-assign-employees-to-branches.md) | Which branch each person belongs to |
