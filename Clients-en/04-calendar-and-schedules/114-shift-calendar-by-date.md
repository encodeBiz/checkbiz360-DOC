# Calendar: shifts loaded by date

The weekly schedule works when every week looks alike. When each week is different, a template week that repeats falls short: Tuesday the 21st has one shift and Tuesday the 28th another. That is what the **Calendar** mode is for. Each person's schedule is whatever you load in a shift calendar, date by date, and the person clocks in with the usual gesture.

---

## What it solves

- **Planning month by month.** Each day carries its own shifts, with no templates repeating on their own.
- **Clocking in as normal.** The person clocks in as always against that day's shift, without having to start tasks.
- **Fitting the work inside the shift.** The day's tasks are normal tasks, inside their shift.

If it is not on the roster, they do not work. A day with no shifts loaded is a day off.

---

## The three schedule modes

In **Schedules & holidays**, the **How the schedule is set** section has three options:

| Mode | Where each day's schedule comes from |
|---|---|
| **Weekly schedule** | The template week, repeated every week. |
| **Schedule from tasks** | That day's tasks: each task is a shift. Only chosen on a person's profile. |
| **Calendar** | The shifts loaded for that date. A day with nothing loaded is a day off. |

**Calendar** can be set on the company, on a branch or on a person, and it is inherited like the rest of the schedule: the closest level wins. A roster is planned per branch, so the usual thing is to set it on the branch. If someone at that branch has a fixed schedule, for example the office staff, leave them on **Weekly schedule** on their profile.

> **Warning:** when you set **Calendar** on a branch, anyone without shifts loaded will have their days off until they are loaded. They will not be able to clock in on those days. People with another mode on their profile do not change. The panel reminds you before saving.

Removing the mode does not delete the loaded shifts. They simply stop being used.

---

## Loading shifts

On the branch's or the person's profile, in **Schedules & holidays**, you will find the **Shift calendar**. On the branch it shows the week of all its people, one row per person. On a person's profile it shows only theirs.

1. Move between weeks with the arrows, or go back to **Today**.
2. On the day and person you want, click **Add shift**.
3. Enter the **Start** and **End** and click **Save**.
4. If it is a split day, add a second shift. Two shifts on the same day cannot overlap.

To change a shift, tap it. To make the day a day off again, click **Remove**.

Each day shows in one of three ways:

| On screen | What it means |
|---|---|
| **Shift** | It has shifts loaded, with their start and end times. |
| **Off** | Someone has deliberately left it without shifts. |
| **Not loaded** | Nobody has loaded anything yet. For clocking in it is a day off, but it is shown differently so you notice what is missing. |

Days that are over cannot be changed. Today can.

### Copying the week

**Copy to next week** copies the shifts of the week you are viewing to the following one, person by person. Whatever those days already had is replaced. It is the quick way to build a month that looks alike week by week, and then adjust whatever changes.

### Creating a task inside a shift

From a shift, **Create task** opens the usual form with the person, the day and the time already filled in. The task is a normal task: creating it does not change the shift, and clocking in does not start or close it.

### Loading a month from Excel

The [roster importer](108-import-the-weekly-schedule.md) works too. For anyone on **Calendar**, each date in the template loads that day's shift, from the first to the last time, as well as creating the tasks as usual. A template with a whole month loads each person's month. Past dates are skipped.

---

## What the person sees

In the app, their week with the loaded shifts and the start and end reminder for each shift, just as with the weekly schedule. They clock in with the usual gesture. Public holidays and their absences still take precedence: a holiday or a vacation blocks clocking in even if a shift is loaded that day.

---

## Where the clock-in is measured

The shift has no location of its own. The clock-in is measured against the **branch**, as with the weekly schedule. Each task with an address is measured against its own location when it is started.

If the work is away from the branch, create a branch with the geofence disabled so people can clock in from anywhere, and put the address on each task. Bear in mind that a task without an address at that branch does not check any location.

---

## Who can load shifts

The company's owner and administrators, and the supervisors of the person's branch.

---

## Common problems

| What happens | What to do |
|---|---|
| "This person is not on “Calendar”" | Choose that mode on their schedule or on their branch's. Shifts are only loaded for people on that mode. |
| "A day that is over cannot be changed" | Days before today stay as they were. If a clock-in needs correcting, do it from the clock record review. |
| "Two shifts on the same day cannot overlap" | Adjust the times so one shift ends before the other starts. |
| Someone cannot clock in after the mode was switched on | Their day is **Not loaded**. Load their shift from the shift calendar. |

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Import the weekly schedule](108-import-the-weekly-schedule.md)
- [Availability board](98-availability-board.md)
- [Geofences and clocking radius](../03-time-tracking/16-geofences-and-clocking-radius.md)
- [Your operations manager in Claude or ChatGPT](../15-integrations/109-your-operations-manager-in-claude-or-chatgpt.md)
