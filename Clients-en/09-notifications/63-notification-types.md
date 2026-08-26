# Notification types

CheckBiz360 generates automatic notifications to inform the platform's various users about relevant events in real time. Notifications are organised into categories according to the operational area they belong to, and each type has predefined recipients according to each user's role. This article describes all the notification categories and types available in the system.

## Notification categories

### Attendance notifications

Attendance notifications report on events related to employees' working-time records.

| Type | Description | Recipients |
|---|---|---|
| Employee who has not clocked in | Generated when an employee with an active shift has not recorded their entry after the time configured as the threshold | Manager, Supervisor |
| Incomplete workday | Generated at the end of the shift if the employee has not recorded their exit | Manager, Supervisor, Worker |
| Suspicious clock record | Generated when the system detects that a clock record shows an anomaly indicator | Manager |
| Clock-in outside the geofence | The employee has clocked in from a location outside the radius defined for their branch | Manager, Supervisor |
| Manual workday approved | Notifies the employee that their manual workday request has been approved by the manager | Worker |
| Manual workday rejected | Notifies the employee that their manual workday request has been rejected | Worker |

### Document notifications

Document notifications manage the distribution of documents and the tracking of read receipts.

| Type | Description | Recipients |
|---|---|---|
| New document available | Sent to the employee when a document is assigned to them for consultation | Worker |
| Read receipt pending | Reminder that an assigned document is pending confirmation | Worker |

> **Note:** the platform manages **read receipts**, not electronic signatures. There is therefore no "document signed" or signature refusal notification.

### Task notifications

Task notifications keep employees and managers informed about the status of assigned tasks.

| Type | Description | Recipients |
|---|---|---|
| New task assigned | Sent to the employee when a new task is assigned to them | Worker |
| Deadline reminder | Alert that an assigned task is due in the next few hours or the following day | Worker |
| Task completed | Notifies the manager that the employee has marked the task as completed | Manager, Supervisor |
| Task pending validation | The employee has completed the task and the system is awaiting the manager's validation | Manager, Supervisor |
| Task validated | Notifies the employee that their task has been validated by the manager | Worker |
| Task rejected | Notifies the employee that their task has been rejected and requires review | Worker |

### Security alerts

Security alerts are high-priority notifications relating to the integrity of the system and to authentication. They cannot be disabled.

| Type | Description | Recipients |
|---|---|---|
| Suspicious clock record | Clock record flagged as potentially fraudulent by the analysis engine | Manager, Owner |
| Unauthorised device | An attempt to clock in from a device that has not been authorised for the employee is detected | Manager, Owner |
| Access from a new location | Sign-in to the back office from an unusual IP address or location | User affected, Owner |
| Repeated failed access attempts | Several consecutive failed attempts to access an account have taken place | User affected, Owner |

> **Warning:** Security alerts cannot be disabled by any user, regardless of their role or preference configuration. Their receipt is guaranteed by design to protect the platform's operational integrity.

### Administrative notifications

Administrative notifications report on processes requiring manual intervention by managers.

| Type | Description | Recipients |
|---|---|---|
| Manual workday pending approval | An employee has requested the manual recording of a workday requiring validation | Manager, Supervisor |
| Leave request pending | The employee has submitted an absence or leave request requiring approval | Manager |
| New employee activated | A new employee has completed their account activation process | Manager, Owner |
| Invitation not accepted | An invited employee has not activated their account after the usual period | Manager |

## Delivery channels

CheckBiz360 notifications are sent through two main channels:

- **Push notification in the app**: for employees (Workers) and, where appropriate, for managers who have the app installed.
- **Back office notification**: appears in the administration panel's notification centre, visible to Manager, Supervisor and Owner.

Some notification types additionally have a fallback email channel to guarantee delivery even when the device is unavailable. Details on channel configuration and preferences are described in the corresponding articles of this section.

---

> **Role note:** Notification visibility depends on the user's role. Each role receives only the notifications that concern them according to the table above. The Owner receives all administrative and security notifications on a consolidated basis for the whole organisation.

## Related articles

- [Push notifications in the app](64-push-notifications-in-the-app.md)
- [Configure notification preferences](65-configure-notification-preferences.md)
- [Alerts for managers](66-alerts-for-managers.md)
- [Notification history](67-notification-history.md)
- [Email notifications](68-email-notifications.md)
