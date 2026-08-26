# Alerts for managers

Alerts for managers are operational notifications the system sends to the Manager and Supervisor roles when events occur that require attention or action from the management team. Unlike notifications aimed at employees, these alerts are designed to detect irregularities, guarantee process compliance and allow a rapid response to situations that could affect operations. This article describes the alert types available, how to configure them and how to adjust the activation thresholds.

## Types of alert for managers

### Employee who has not clocked in

This alert is sent to the branch's Manager and Supervisor when an employee with an active shift has not recorded their entry after a given time. It is the most widely used alert in operations with defined shifts, since it lets the manager know immediately who is missing before the absence affects operations.

The alert includes:
- The employee's name.
- The branch and shift they should have joined.
- The shift start time and the time elapsed since then.

### Manual workday pending approval

When an employee requests the manual recording of a workday (because they could not clock in at the relevant moment), the system sends an alert to the manager so they review and approve or reject the request. The alert includes the reason given by the employee and a direct link to the record to handle the request.

> **Warning:** Manual workday requests not approved within 48 hours generate an additional reminder alert. If the payroll period closes with pending requests, the system will flag it as a compliance incident.

### Clock record flagged as suspicious

CheckBiz360's analysis engine evaluates every clock record in context and can flag it with an anomaly indicator when it detects irregular characteristics, such as:

- An abrupt change of GPS location between consecutive clock records.
- GPS coordinates inconsistent with the physical movement possible in the time elapsed.
- Clocking patterns matching known control-evasion behaviour.
- Clocking from a device other than the usual one without prior authorisation.

When this alert is generated, the manager receives the notification with the detail of the suspicious record and can decide to validate it, modify it or escalate it for investigation.

### Employee repeatedly outside the geofence

If an employee records clock-ins outside the radius defined for their branch on a recurring basis (the default threshold is three times in one week), the system generates a consolidated alert addressed to the Manager. This alert is different from the individual "clock-in outside the geofence" notification: it is not generated on each individual occurrence, but when the pattern becomes systematic.

## How to configure which alerts each manager receives

The Owner and the Manager can adjust alert distribution from the back office:

1. Go to **Branches** and open the branch you want to configure alerts for.
2. Select the **Managers** or **Alert configuration** tab.
3. You will see the list of Managers and Supervisors assigned to that branch.
4. Press the configuration icon next to the manager's name to adjust which alert types they receive.
5. Enable or disable the alert types according to that manager's responsibilities.
6. Press **Save**.

This configuration allows, for example, the Supervisor to receive the day-to-day clocking and absence alerts, while the Manager receives only the alerts for suspicious clock records and pending manual workdays.

## Configuring the entry time limit threshold

The "employee who has not clocked in" alert requires an entry time limit to be defined for each shift. If the shift starts at 08:00 and the time limit is configured at 30 minutes, the alert will be generated at 08:30 if the employee has not clocked in.

To configure this threshold:

1. Go to **Organisation** > **Calendars** and open the calendar containing the shift you want to configure.
2. Select the specific shift and find the **Entry alert tolerance** field (expressed in minutes).
3. Enter the number of minutes after the shift start time from which the system should generate the alert.
4. Save the changes. The new threshold will apply from the following day.

> **Warning:** A threshold that is too low (for example, 5 minutes) can generate an excessive volume of alerts for minor, normal delays in transport or site access. Starting with a threshold of between 15 and 30 minutes and adjusting it according to the branch's real operation is recommended.

## Receiving alerts: back office and push notification

Managers receive alerts through two simultaneous channels:

- **Back office notification centre**: visible on the bell icon in the top bar. Unread alerts are shown with a numerical indicator and remain in the centre until the manager reviews them.
- **Push notification in the app**: if the Manager or the Supervisor has the CheckBiz360 app installed and has signed in, alerts are also received as push notifications on their mobile device.

Critical alerts (suspicious clock record, unauthorised device) additionally have an email fallback channel guaranteeing their delivery even if the manager does not have the app active.

## Handling alerts received

From the back office notification centre, the manager can:

- **Mark as reviewed**: indicates that the alert has been seen and processed.
- **Go to the resource**: navigate directly to the clock record, workday or employee the alert refers to.
- **Add an internal comment**: record a note about the action taken, visible to other managers at the same branch.

Reviewed alerts are archived automatically and remain available in the notification history.

---

> **Role note:** Alerts for managers are available to the **Manager** and **Supervisor** roles. The **Owner** receives the critical security alerts for the whole organisation. The **Worker** role has no access to operational alerts.

## Related articles

- [Notification types](63-notification-types.md)
- [Configure notification preferences](65-configure-notification-preferences.md)
- [Notification history](67-notification-history.md)
- [Multi-branch global view](../08-branches-and-organisation/62-multi-branch-global-view.md)
