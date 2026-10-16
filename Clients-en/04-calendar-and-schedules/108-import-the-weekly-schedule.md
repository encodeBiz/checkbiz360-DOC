# Import the weekly schedule

When the work changes every week —home care, cleaning across sites, maintenance—, typing in each person's week, job by job, is a lost morning every Monday. This guide explains how to load the week of a branch's whole staff at once from an Excel sheet, or the week of a single person from their profile.

---

## What it solves

- **One upload for the whole staff.** One file per branch and week, with one tab per person. No need to go profile by profile.
- **Each person gets their week on their phone**: their schedule for each day and one job per service, with the address where they have to clock in.
- **Nothing is saved before you see it.** The platform shows what it will do with each person and only applies it when you confirm.
- **Correcting means uploading again.** If the week changes, upload the corrected file: what was there is updated and nothing is duplicated.

---

## How it works, in three steps

| Step | What happens |
|---|---|
| **1. Download the template** | From the branch, for the week you choose. It has one tab for each person in the branch. |
| **2. Fill it in and upload it** | One row per job. Nothing is saved yet when you upload it. |
| **3. Review and confirm** | The platform shows what it will do with each person. It is only applied when you confirm. |

---

## 1. Download the template

1. Go to **Branches/Projects** and open the branch.
2. In the **Schedules & holidays** tab, expand **Weekly schedule for the whole staff** and click **Import schedule**.
3. Choose the week and click **Download template**.

The template has a first sheet with the instructions and the list of people, and **one tab per person**, named after them.

> **Do not delete row 1 of any tab**: it says whose tab it is. You can rename or reorder the tabs freely.

Each tab has **two example rows** starting with the word **DELETE**: delete them or leave them, they are not imported.

### Columns

| Column | What to enter |
|---|---|
| **Date** * | The day of the job: 19/10/2026. |
| **Start time** * | When it starts: 08:00. |
| **End time** * | When it ends: 10:00. |
| **Client** | Who the job is for: the person cared for, the building, the company. |
| **Address** | Where it is done. It is where the person will have to clock in. |
| **Job** | What is done: cleaning, companionship, inspection. |
| **Travel (min)** | Minutes of travel to that job. |

Columns with an asterisk are required. Always add the **address** if you can: without it the job is still created, but it can be clocked from anywhere.

### What an empty tab means

- **An empty tab** leaves that person as they are. It does not mean "not working that week": it means nothing is said about them.
- **A tab with jobs** is that person's whole week: days without any row are days off.

---

## 2. Upload the file

Click **Choose file**, select the filled-in template and click **See the proposal**. Excel (.xlsx) up to 2 MB is accepted, saved with Excel or with any other spreadsheet program. CSV is not accepted, because a CSV has no tabs.

If you upload a file that is not the template, the platform says so and reads nothing.

---

## 3. Review what will be done

Before confirming, each person appears with their status, their jobs and the hours of the week:

| Status | Meaning |
|---|---|
| **Ready** | Everything was read correctly. It will be applied when you confirm. |
| **Blocked** | Something prevents applying it: a badly written row (it says which), or jobs on a day that is a holiday or leave for that person. That person is not applied; the others are. |
| **Unchanged** | Their tab is empty. Nothing is touched. |
| **Unrecognised tab** | The tab does not match anyone in the branch. Check row 1. |
| **Duplicate tab** | There are two tabs for the same person and it is not clear which one counts. |

Next to each person you also see the warnings worth checking: two jobs that overlap, jobs without an address, or travel before the first job longer than the margin the person has to clock in.

What needs attention comes first. To fix a blocked person, correct the file and click **Upload another file**. If you close the window without confirming, nothing is saved.

When you are happy, click **Confirm**. With many people it takes a moment and you see the progress; you can close the window and the import carries on.

---

## What each person sees

In the app, the imported week: their schedule for each day and their jobs, each with its time and address. They will clock in at the address of each job.

- With the usual schedule, their working day runs from the start of the first job to the end of the last one.
- If the person works with **Schedule from tasks**, their schedule for each day is their jobs, one after another, with the gaps in between. A day without jobs is a day off. In the app they always see the current week as it stands.

---

## Uploading the same week again

If the week changes, fill in the template with the right version and upload it again:

- What was there **is updated** and nothing is duplicated.
- Jobs that no longer appear **are removed**, except those the person has already started: those stay, and the review warns you.

---

## The week of a single person

From the person's profile, in **Schedules & holidays**, expand **Import weekly schedule** and click **Upload a schedule**. You can do the same for that person alone:

- **Download template** gives you a template with their tab.
- You can also upload the document printed by your management software (PDF, Excel or CSV). In that case the platform shows you what it understood from each column so you can confirm it before going on, and it takes a little longer.

---

## Who can import

People with management access to the company panel.

---

## Related articles

| Article | Description |
|---|---|
| [Base schedules and shifts](./23-base-schedules-and-shifts.md) | The usual schedule, with one or several shifts per day |
| [Public holidays and non-working days](./29-public-holidays-and-non-working-days.md) | Why a job on a day of leave blocks that person |
