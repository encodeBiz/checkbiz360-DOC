# Posted hours and alerts

Once the integration is connected, the Rentman screen shows you what is happening with your hours. This article explains what each figure means and what to do when something needs you.

## What you will see

| Indicator | What it tells you |
|---|---|
| **Shifts posted** | How many closed shifts have been sent to Rentman |
| **Hours posted** | Total net hours sent in the period |
| **Matching coverage** | How many of your employees have a linked Rentman record |
| **Open discrepancies** | Shifts someone edited in Rentman after they were sent |

## Sync on demand

Syncing runs on its own every 15 minutes, but right after connecting — or whenever you want to check something — you can press **Sync now** and skip the wait. If you press it twice in a row the platform will ask you to wait a few seconds: that is protection against overloading Rentman, not an error.

And if the result comes back at zero, that is not a failure either: there may be no newly closed shifts, or those people may not be matched yet.

## Why the hours match your legal report

The hours sent to Rentman are the **net** ones: clock-out minus clock-in, minus the break.

The break does not travel inside the clock-in. It comes from the site's configuration: either a fixed break defined for the workplace, or the sum of the breaks the worker recorded. The integration applies **exactly the same rule as the time-tracking report**, so the figure you see in Rentman and the one you certify to an inspector are the same.

If those two figures ever disagree, tell us: that is a problem we want to know about.

## Discrepancies

A discrepancy appears when someone **edits in Rentman** hours that CheckBiz360 had already sent, or deletes them.

In that case the platform:

1. Detects the change when it re-checks the record, which it does every 24 hours.
2. Flags that shift and shows you both versions: yours and Rentman's.
3. **Does not modify your clock-in.** The legal record stays intact.
4. Does not undo the Rentman change either: that decision is yours.

What to do depends on who is right:

- **If the clock-in is correct** and the Rentman edit was a mistake, fix it in Rentman.
- **If the clock-in is the wrong one** (a worker forgot to clock out, say), fix it in CheckBiz360 first. The shift will then be re-sent with the new values.

## Shift statuses

| Status | Meaning | Needs action |
|---|---|---|
| Queued | Detected, waiting to be sent | No |
| Sent | Already in Rentman | No |
| Error | A temporary connection failure | No, it retries itself |
| Rejected | Rentman will not accept it | Yes, check the reason |
| Discrepancy | Edited in Rentman | Yes, review both versions |

## Frequently asked questions

**A worker clocked in but their hours are not in Rentman.**
Check three things in this order: that the shift is **closed** (clock-out recorded), that the worker is **matched** to their Rentman record, and that at least 15 minutes have passed.

**A shift shows as "rejected" by Rentman.**
The usual reason is that Rentman already had hours or an absence for that person in that same period; it does not accept overlapping records. Check those dates in Rentman: it is normally hours entered by hand before the integration was connected.

**Are incomplete shifts sent?**
No. A shift with no clock-out is not a closed shift. If that happens often, review the automatic closing alerts in the time-tracking module.

**Can I edit in Rentman the hours CheckBiz360 sends?**
You can, but it is not advisable. Your edit will not travel back and will create a discrepancy. If the shift is wrong, fix it in CheckBiz360 and let the correction travel on its own.

**What if Rentman is down?**
Nothing serious. Clock-ins carry on as normal — the integration never blocks time tracking — and pending shifts are sent when the service returns.

**Can hours be duplicated?**
No. Each shift carries an internal fingerprint that prevents it being sent twice, however many times syncing runs.

## Related articles

- [RentmanBiz](94-rentmanbiz.md)
- [Connecting RentmanBiz step by step](95-connect-rentmanbiz.md)
