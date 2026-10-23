# Import the weekly schedule

When the work changes every week —home care, cleaning across sites, maintenance—, typing in each person's week, shift by shift or job by job, is a lost morning every Monday. This guide explains how to load the week of a branch's whole staff at once from an Excel sheet, or the week of a single person from their profile.

---

## What it solves

- **One upload for the whole staff.** One file per branch and week, with one tab per person. No need to go profile by profile.
- **Each person gets their week on their phone**: their shifts, or their jobs with the address where they have to clock in, depending on how their schedule is organised.
- **Nothing is saved before you see it.** The platform shows what it will do with each person and only applies it when you confirm.
- **Correcting means uploading again.** If the week changes, upload the corrected file: what was there is replaced and nothing is duplicated.

---

## What is uploaded depends on each person's mode

You do not choose the type of roster: each person's [schedule mode](114-shift-calendar-by-date.md#the-three-schedule-modes) decides it.

| The person's mode | What their tab loads | What happens to their tasks |
|---|---|---|
| **By shifts** | Their shifts for that week: date, clock-in and clock-out. Days without rows are off. | None is created, moved or deleted. |
| **By tasks** | One task per row, with its address. Their tasks are their schedule. | They replace their week: the tasks from the previous roster that have not started yet are removed and the ones in the file are created. Started ones stay. |
| **Standard week** | Nothing. Their schedule is the standard week and no roster is uploaded for them. | They are not touched. |

If you want to upload another type of roster for someone, change their mode first.

---

## How it works, in three steps

| Step | What happens |
|---|---|
| **1. Download the template** | From the branch, for the week you choose. It has one tab for each person in the branch, of the type that applies to them. |
| **2. Fill it in and upload it** | One row per shift or per job. Nothing is saved yet when you upload it. |
| **3. Review and confirm** | The platform shows what it will do with each person. It is only applied when you confirm. |

---

## 1. Download the template

The whole staff's roster is uploaded from a branch that is **By shifts**:

1. Go to **Branches/Projects**, open the branch and click **Edit**.
2. In **Schedules & holidays**, check that **How the schedule is organised** is set to **By shifts**.
3. Under **Import roster by shifts**, above the shift roster, click **Upload a schedule**.
4. Choose the week and click **Download template**.

Anyone at that branch who is **By tasks** also gets their tab, a task one. If the branch is on **Standard week**, the roster of anyone who is **By tasks** is uploaded from their profile (see [The week of a single person](#the-week-of-a-single-person)).

The template has a first sheet with the instructions and the list of people, and **one tab per person**, named after them and showing the type that applies: **Schedule by shifts** or **Schedule by tasks**.

> **Do not delete row 1 of any tab**: it says whose tab it is and of which type. You can rename or reorder the tabs freely.

Each tab has **two example rows** starting with the word **DELETE**: delete them or leave them, they are not imported.

### Columns

In a **roster by shifts**, each row is a shift and only the first three columns are needed. A split day is two rows with the same date.

In a **roster by tasks**, each row is a job:

| Column | What to enter |
|---|---|
| **Date** * | The day of the job: 19/10/2026. |
| **Start time** * | When it starts: 08:00. |
| **End time** * | When it ends: 10:00. |
| **Client** | Who the job is for: the person cared for, the building, the company. |
| **Address** | Where it is done. It is where the person will have to clock in. |
| **Job** | What is done: cleaning, companionship, inspection. |
| **Travel (min)** | Minutes of travel to that job. |

Columns with an asterisk are required. In a roster by tasks, always add the **address** if you can: without it the job is still created, but it can be clocked from anywhere.

### What an empty tab means

- **An empty tab** leaves that person as they are. It does not mean "not working that week": it means nothing is said about them.
- **A tab with rows** is that person's whole week: days without any row are days off.

---

## 2. Upload the file

Click **Choose file**, select the filled-in template and click **See the proposal**. Excel (.xlsx) up to 2 MB is accepted, saved with Excel or with any other spreadsheet program. CSV is not accepted, because a CSV has no tabs.

If you upload a file that is not the template, the platform says so and reads nothing.

---

## 3. Review what will be done

Before confirming, each person appears with their status, their rows and the hours of the week. Each person is reviewed according to their mode: a roster by shifts says nothing about tasks or addresses.

| Status | Meaning |
|---|---|
| **Ready** | Everything was read correctly. It will be applied when you confirm. |
| **Blocked** | Something prevents applying it: a badly written row (it says which), jobs on a day that is a holiday or leave for that person, a person on **Standard week**, or a tab whose type no longer matches their mode. That person is not applied; the others are. |
| **Unchanged** | Their tab is empty. Nothing is touched. |
| **Unrecognised tab** | The tab does not match anyone in the branch. Check row 1. |
| **Duplicate tab** | There are two tabs for the same person and it is not clear which one counts. |

Next to each person you also see the warnings worth checking. In a roster by tasks: two jobs that overlap, jobs without an address, or travel before the first job longer than the margin the person has to clock in; and which tasks of that week are replaced and which stay because they have started. In a roster by shifts: if the tab has a client, address or job, you are warned that those details are not loaded. Two rows on the same day that overlap are loaded as a single shift.

What needs attention comes first. To fix a blocked person, correct the file and click **Upload another file**. If you close the window without confirming, nothing is saved.

When you are happy, click **Confirm**. With many people it takes a moment and you see the progress; you can close the window and the import carries on. When it finishes, each person shows how many days of shifts were loaded or how many tasks were created.

---

## What each person sees

In the app, the imported week:

- **By shifts**: their shifts for each day, with the clock-in and clock-out reminder. They clock in against the branch, as always.
- **By tasks**: their jobs, each with its time and address. They will clock in at the address of each job, and their schedule for each day is those jobs.

Past dates are not loaded: days before today stay as they were.

---

## Uploading the same week again

If the week changes, fill in the template with the right version and upload it again:

- **By shifts**: each day in the file replaces whatever that day had. Nothing is duplicated.
- **By tasks**: the week is replaced. Jobs that no longer appear **are removed**, except those the person has already started: those stay, and the review warns you.

---

## The week of a single person

Open the person's profile and click **Edit**. In **Schedules & holidays**, with the person **By shifts** or **By tasks**, click **Upload a schedule** under **Import roster by shifts** or **Import weekly schedule**. You can do the same for that person alone:

- **Download template** gives you a template with their tab.
- You can also upload the document printed by your management software (PDF, Excel or CSV). In that case the platform shows you what it understood from each column so you can confirm it before going on, and it takes a little longer.

No roster is uploaded for someone on **Standard week**.

---

## Who can import

People with management access to the company panel.

---

## Related articles

| Article | Description |
|---|---|
| [By shifts: the schedule is the shifts you load](./114-shift-calendar-by-date.md) | The three schedule modes and the shift roster |
| [Base schedules and shifts](./23-base-schedules-and-shifts.md) | The standard week, with one or several shifts per day |
| [Public holidays and non-working days](./29-public-holidays-and-non-working-days.md) | Why a job on a day of leave blocks that person |
