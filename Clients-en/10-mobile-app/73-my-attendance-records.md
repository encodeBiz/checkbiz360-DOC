# My attendance records

The "My records" section of CheckBiz360 lets you consult the complete history of your clocking activity from the mobile application itself. This article explains how to access your history, what information each record contains, how to interpret the statuses and what to do if you spot an error.

---

## Accessing the records section

1. Open CheckBiz360 and sign in with your account.
2. Tap the **My records** icon in the bottom navigation bar (usually represented by a list or history icon).
3. The list of your attendance records will load, ordered chronologically from most recent to oldest.

---

## Available filters

To make finding particular records easier, the application offers several filters you can combine:

### Filter by date

1. Tap the filter icon or the date selector at the top of the screen.
2. Select a specific date or a date range (start date and end date).
3. Tap **Apply** to update the list with the corresponding results.

### Filter by branch

1. Within the filter options, find the **Branch** or **Workplace** selector.
2. Select the branch you want from the list available.
3. The list will show only the records associated with that branch.

### Filter by event type

Each record is classified according to the type of action carried out:

- **Check-in**: entry at the start of the workday.
- **Check-out**: exit at the end of the workday.
- **Break**: start of an intermediate break.
- **End of break**: resumption of activity after a break.

You can filter the list to show only one or several of these types by selecting them in the corresponding selector.

---

## Detail of each record

Tapping any record in the list takes you to the detail view, which includes the following information:

| Field | Description |
|-------|-------------|
| Exact date and time | Timestamp of the moment the clock record was made |
| Type | Check-in, check-out, break or end of break |
| Branch | Name of the workplace associated with the record |
| Status | Valid or failed |
| Distance to the radius | Distance in metres between your position and the branch's permitted perimeter (where applicable) |
| Validation method | GPS, WiFi, manual or another method configured by your organisation |

---

## Interpreting the statuses

### Valid record

A record with **Valid** status indicates that the clock record was accepted correctly by the system. It met all the validation requirements at the moment it was made (location within the permitted radius, authorised schedule, etc.).

### Failed record

A record with **Failed** status indicates that the system tried to process the clock record but could not validate it correctly. The most frequent causes are:

- The employee was outside the geolocation radius permitted for the branch.
- The device's GPS did not have sufficient accuracy at that moment.
- A connectivity error occurred during transmission of the record.
- The clocking attempt was made outside the authorised schedule for that shift.

> **Warning:** A failed clock record does not count as recorded presence. If you spot failed records that do not correspond to a real error on your part, you should report it to your manager so they can review the situation.

---

## What to do if you spot a failed or incorrect record

If you identify a failed record in your history, or a clock record that does not match your real activity (for example, an entry or exit that was not recorded), you can start a correction request from the application itself:

1. Tap the record affected to open its detail view.
2. Find the **Request correction** or **Report incident** option and tap it.
3. State the reason for the request and, if possible, the real time at which the record should have been made.
4. Add any additional comment you consider relevant so that your manager can assess the request.
5. Tap **Send request**.

The manager or administrator will receive a notification with your request and will be able to approve it, deny it or ask for additional information.

---

## Requesting a manual workday from the app

If on a given day you were unable to make any clock record (for example, because of a device failure or lack of connectivity throughout the workday), you can request the creation of a manual workday:

1. In the "My records" section, find the day with no records or tap the **New manual request** button if it is available on the screen.
2. State the date, entry time and exit time concerned.
3. Select the branch you worked at that day.
4. Add a justification or reason for the absence of automatic clocking.
5. Tap **Send**.

> **Warning:** Manual workday requests are not approved automatically. They require review and approval by your manager or administrator. The workday will not be considered valid until the manager approves it in the system.

---

## Role note

This article is aimed at **employees** consulting their attendance history from the app. Managers and administrators can consult all employees' records from the web portal, with additional filtering and export options.

---

## Related articles

- [Main app navigation](71-main-app-navigation.md)
- [Offline use](74-offline-use.md)
- [Profile settings in the app](72-profile-settings-in-the-app.md)
