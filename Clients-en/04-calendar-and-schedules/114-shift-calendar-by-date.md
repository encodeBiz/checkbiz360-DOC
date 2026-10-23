# By shifts: the schedule is the shifts you load

The standard week works when every week looks alike. When each week is different, a week that repeats falls short: Tuesday the 21st has one shift and Tuesday the 28th another. That is what the **By shifts** mode is for. Each person's schedule is whatever you load in the shift roster, week by week, and the person clocks in with the usual gesture.

---

## What it solves

- **Planning week by week.** Each day carries its own shifts, with no standard week repeating on its own.
- **Clocking in as normal.** The person clocks in as always against that day's shift, without having to start tasks.
- **Fitting the work inside the shift.** The day's tasks are normal tasks, inside their shift. Loading shifts never creates, moves or deletes a task.

If it is not on the roster, they do not work. A day with no shifts loaded is a day off, and a week with nothing loaded is off entirely.

---

## The three schedule modes

Each person has one mode, and **the mode is the only source of their schedule**. It is chosen in **Schedules & holidays**, in the **How the schedule is organised** section:

| Mode | Where the schedule comes from | Where it can be set |
|---|---|---|
| **Standard week** | The standard week, the same every week. | Company, branch or person. |
| **By shifts** | Only the shifts loaded for each date. A day with no shifts is off. | Company, branch or person. |
| **By tasks** | Each day's tasks: each task is a shift. | Only on a person's profile. |

Each mode shows only what is its own. Someone on **Standard week** sees no roster, and loaded shifts do not count even if they exist. Someone **By shifts** has no standard week behind them: if a week is not loaded, that week is off.

**Standard week** and **By shifts** are inherited like the rest of the schedule: the closest level wins. A roster is planned per branch, so the usual thing is to set **By shifts** on the branch. If someone at that branch has a fixed schedule, for example the office staff, leave them on **Standard week** on their profile. With **Use base schedule** on for a branch or a person, the mode is inherited too.

---

## Changing the mode

1. Open the branch's or the person's profile and click **Edit**.
2. In **Schedules & holidays**, under **How the schedule is organised**, click the mode you want.

On a branch or a person, **the mode is saved as soon as you click it**: "Mode saved." appears and what is below changes straight away. You do not need to click the form's save button. In the company's general settings, the mode is saved with the rest of the schedule.

> **Warning:** when you switch a branch to **By shifts**, anyone without shifts loaded is off until they are loaded, and will not be able to clock in on those days. People with another mode on their own profile do not change. Load the shifts before the week starts.

Removing the mode does not delete the loaded shifts. They simply stop being used.

---

## Loading shifts

With the branch or the person **By shifts**, under **Edit** → **Schedules & holidays** you will find the **Shift roster**. On the branch it shows the week of everyone who is **By shifts**; anyone at the branch with another mode is not shown, and the panel says how many people that is. On a person's profile it shows only theirs.

The roster draws the week with the hours running down and each shift from its clock-in to its clock-out. Today and the current time are marked. The top row says who is off each day.

1. Move between weeks with the arrows, or go back to **Today**.
2. Click **Add shift**, or the **+** on the day you want. You can also click a free hour or an existing shift.
3. **Shifts for the day** opens, with that person's whole day. Choose the person and the day if needed, and enter the **Clock-in** and **Clock-out**.
4. If it is a split day, click **Add another shift (split day)**. Two shifts on the same day cannot overlap.
5. Click **Save**.

Shifts are saved straight away, without going through the form's button. To make a day a day off again, remove all its shifts with **Remove** and save: the day is left as "No shifts: that day is off."

If someone has nothing loaded in the week you are viewing, the panel warns you in red: that person is off the whole week.

Days that are over cannot be changed. Today can.

### Copying the week

**Copy to next week** copies the shifts of the week you are viewing to the following one, person by person. Whatever those days already had is replaced. It is the quick way to build a month that looks alike week by week, and then adjust whatever changes.

### Tasks

The shift roster does not create tasks. Tasks are created in **Tasks**, as always, and sit inside that day's shift. Changing a shift does not move any task.

### Loading the week from Excel

Above the roster you will find **Import roster by shifts**. With the [roster importer](108-import-the-weekly-schedule.md), each person who is **By shifts** gets a tab with the date, the clock-in time and the clock-out time of each shift. Their tab is their whole week: days without rows are off. No task is created or touched, and past dates are skipped.

---

## What the profile shows

Without clicking **Edit**, the branch's or the person's profile is read-only. The **Schedule** section states the mode and shows what is its own: the standard week, the week of loaded shifts or the week of tasks. **By shifts**, you move between weeks with the arrows or **Today**, and days with no shifts show as **Off**.

---

## What the person sees

In the app, their week with the loaded shifts and the clock-in and clock-out reminder for each shift, just as with the standard week. They clock in with the usual gesture. Public holidays and their absences still take precedence in all three modes: a holiday or a vacation blocks clocking in even if a shift is loaded that day.

---

## Where the clock-in is measured

The shift has no location of its own. The clock-in is measured against the **branch**, as with the standard week. Each task with an address is measured against its own location when it is started.

If the work is away from the branch, create a branch with the geofence disabled so people can clock in from anywhere, and put the address on each task. Bear in mind that a task without an address at that branch does not check any location.

---

## Who can load shifts

The company's owner and administrators, and the supervisors of the person's branch.

---

## Common problems

| What happens | What to do |
|---|---|
| "This person is on «Standard week»: switch them to «By shifts» to load shifts." | Their schedule is the standard week. Change their mode under **Edit**, on their profile or on their branch's. |
| "This person is «By tasks»: switch them to «By shifts» to load shifts." | Their schedule is their tasks. If you want to run them by shifts, change the mode on their profile. Their tasks stay. |
| "A past day cannot be changed." | Days before today stay as they were. If a clock-in needs correcting, do it from the clock record review. |
| "Two shifts on the same day cannot overlap." | Adjust the times so one shift ends before the other starts. |
| Someone at the branch does not appear on the roster | They have another mode on their profile. Only people who are **By shifts** appear. |
| Someone cannot clock in after switching to **By shifts** | That day has no shifts loaded, so they are off. Load their shift from the shift roster. |

---

## Related articles

- [Base schedules and shifts](23-base-schedules-and-shifts.md)
- [Configuration inheritance](26-configuration-inheritance.md)
- [Import the weekly schedule](108-import-the-weekly-schedule.md)
- [Availability board](98-availability-board.md)
- [Geofences and clocking radius](../03-time-tracking/16-geofences-and-clocking-radius.md)
- [Your operations manager in Claude or ChatGPT](../15-integrations/109-your-operations-manager-in-claude-or-chatgpt.md)
