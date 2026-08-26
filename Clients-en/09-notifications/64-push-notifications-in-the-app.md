# Push notifications in the app

Push notifications are the main channel through which CheckBiz360 communicates relevant events to employees in real time. When an event occurs that requires the employee's attention —an assigned task, a document pending a read receipt, a workday approval— the system sends a notification directly to the mobile device, even if the app is not open at that moment. This article explains how these notifications work, what information they contain and what to do if they do not arrive correctly.

## How push notifications reach the device

When an event is generated in CheckBiz360 with an employee as its recipient, the server sends a push notification through the device operating system's messaging service: APNs (Apple Push Notification service) for iOS devices and FCM (Firebase Cloud Messaging) for Android devices.

The complete process, from the event being generated to the notification appearing on the employee's screen, usually takes less than five seconds if the device is connected to the internet. If the device is offline at the moment of sending, the notification will be delivered as soon as it regains connectivity, provided the operating system's expiry time (generally 24 hours) has not elapsed.

## What information each notification contains

The content of each notification varies according to its type, but all include as a minimum:

- **Title**: identifies the type of event concisely (for example, "New document available" or "Task assigned").
- **Body**: a brief description of the event with the most relevant piece of data (document name, task name, name of the manager who approved the workday).
- **Timestamp**: the moment the event was generated.

Some notification types include additional information:

- Notifications for **documents pending a read receipt** include the document's name.
- **Task** notifications include the task name, the due date and the branch or project it is linked to.
- **Workday** notifications include the result of the validation (approved or rejected) and, in the case of rejection, the reason given by the manager.

## Behaviour on tapping the notification

Tapping a push notification opens the CheckBiz360 app and navigates directly to the resource that notification refers to. There is no need to search for the information manually inside the app; the system takes the employee to the exact place where they need to act.

| Notification type | Destination in the app |
|---|---|
| New document / Receipt pending | Document detail screen with the read receipt button visible |
| Task assigned / Deadline reminder | Task detail screen with the available actions |
| Workday approved / rejected | The corresponding workday record |
| Security alert | Account security screen |

If the app is not installed on the device or the employee has not signed in, tapping the notification will open the app store or the sign-in screen as appropriate.

## Requirements for receiving push notifications

For push notifications to work correctly the following conditions have to be met:

1. **The CheckBiz360 app has to be installed** on the employee's device (iOS or Android).
2. **The employee has to have signed in** at least once in the app, so that the system registers the device token needed for sending.
3. **Notification permissions have to be granted** in the device's operating system. If the employee denied permissions during installation, notifications will not arrive even though the system sends them correctly.
4. **The device has to have an internet connection** at some point within the notification's validity period.

> **Warning:** The device's operating system may limit or delay notifications depending on battery saving mode, do-not-disturb mode or the app's background restrictions. If the employee has any of these modes enabled, they may not receive notifications immediately.

## What to do if notifications do not arrive

If an employee does not receive push notifications, follow these diagnostic steps in order:

### 1. Check the operating system permissions

**On iOS:**
1. Open **Settings** on the iPhone or iPad.
2. Scroll to the **CheckBiz360** app and tap it.
3. Go to **Notifications** and check that the main switch is enabled.
4. Make sure the alert type selected is **Lock Screen**, **Notification Centre** or **Banners**, or all of them.

**On Android:**
1. Press and hold the **CheckBiz360** app icon and select **App info**.
2. Tap **Notifications** and check that they are enabled.
3. Verify that no specific notification channels are disabled.

### 2. Check that the session is active

The employee has to have an active session in the app. If the session has expired through prolonged inactivity, the device token may have become outdated. Signing out and back in regenerates the token and restores notification delivery.

### 3. Check the internet connection

Make sure the device has an active internet connection, whether over WiFi or mobile data.

### 4. Contact support

If the steps above do not resolve the problem, contact the CheckBiz360 support team stating the device's operating system and version, the version of the app installed and the type of notification that is not being received.

---

> **Role note:** Push notifications in the app are aimed mainly at the **Worker** role. The **Manager** and **Supervisor** roles can also receive push notifications if they have the app installed, although their main notification channel is the web back office.

## Related articles

- [Notification types](63-notification-types.md)
- [Configure notification preferences](65-configure-notification-preferences.md)
- [Notification history](67-notification-history.md)
- [Email notifications](68-email-notifications.md)
