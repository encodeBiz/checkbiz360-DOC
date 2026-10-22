# Email notifications

CheckBiz360 sends automatic emails on certain events in the account life cycle. This article describes which emails the system sends, when and from which address, and what to do if one of these emails does not reach the recipient.

## Sender of the system emails

All CheckBiz360 automatic emails are sent from the address `hola@encodebiz.com`. If a member of your organisation cannot find an expected email, they should check the spam or junk folder and confirm that this address is not blocked by the corporate mail filter.

> **Warning:** Some corporate mail systems with strict filters (such as Microsoft 365 with advanced security policies) may classify emails from `hola@encodebiz.com` as spam or hold them in quarantine. If this happens systematically, ask your organisation's IT administrator to add the `encodebiz.com` domain to the trusted senders list.

## Automatic system emails

### Welcome for the new employee

When the Owner or a Manager adds a new employee to the platform and sends the invitation, the system automatically generates a welcome email addressed to the employee's email address. This email contains:

- A message welcoming them to the platform on behalf of the company.
- The initial access credentials: email address and temporary password.
- A direct link to download the CheckBiz360 app on iOS and Android.
- Basic instructions for completing the first sign-in and changing the temporary password.

This email is the employee's first point of contact with the platform and is essential for them to be able to activate their account. It is therefore especially important that the employee's email address is correct at the moment their record is created.

### Knowing whether it arrived and resending the access

On each employee's record, the **App access** block says what happened to their welcome email: delivered, bounced, marked as spam or not sent. It also says whether the person has already used the app. If the email has not arrived, the panel's home page warns you with the **Access email not delivered** alert.

To send it again:

1. Navigate to **Employees** and open the employee's record.
2. In **App access**, press **Resend access**.
3. Confirm. The system sends a new welcome email with a new password.

> **Warning:** Resending the access invalidates the previous password, including for the panel if the person uses it. If the email bounced, the address is wrong: change it with **Change email** and send the access to the new one.

It is explained in full in [App access and email change](../02-employees/116-app-access-and-email-change.md).

### Clock-in point card

With the [clock-in point](../03-time-tracking/113-clock-in-point.md) subscribed, each person can receive their card by email, with their QR and their 6-digit code. It is sent from the employee's record, or for a whole branch from **Clock-in point → QR cards**.

### Password reset

When a user requests a password reset (from the sign-in screen, pressing "I have forgotten my password"), the system sends an email with a secure reset link. This link is valid for 30 minutes from the moment of sending. Once expired, the user has to request a new link.

The email includes:
- A button with the reset link.
- The link's expiry time.
- A notice that if the user did not request the reset, they can ignore the email.

---

## Work notifications by email, for people who do not use the app

Some people do not carry the app, or do not look at it. For them, in **Schedules & holidays** on their record, there is the **Send notifications by email** box. With it ticked, as well as the app notifications, they receive by email:

- **Their tasks**: those assigned to them, changed or removed. They arrive grouped so as not to flood their inbox: the email goes out once 15 minutes pass with no new changes. If the task starts within the next 24 hours, the notice goes out straight away.
- **Their schedule for the following week**, on Sunday at 18:00 in the company's time, with their shifts, their tasks and the place of each one. If nothing has changed since the last sending, it is not repeated.

Nothing about clock-ins goes by email. The box comes unticked and is ticked person by person.

## Storage warning

When your company reaches 90% of the storage included in its plan, the owner receives an email at the billing address. It is sent only once. It is sent again only if usage drops below 80% and then rises again. See [Plans, prices and features](../14-reference/91-plans-and-features.md#storage).

## Operational alerts by email

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Sending the home page alerts to managers by email, and the automatic email fallback when a push notification does not reach the device, are planned for a future version.

---

## What to do if the email does not arrive

If an employee or manager does not receive an expected email from the system, follow these steps:

1. **Check the spam or junk folder** in the mail client. Emails from `hola@encodebiz.com` may be classified incorrectly the first time.
2. **Verify the recipient's email address** in the back office. Go to the employee's or user's record and confirm the address is written correctly and without extra spaces.
3. **Look at the App access block** on their record if it is the welcome email: it says whether it was delivered, whether it bounced or whether it was marked as spam. Then **resend the access** (see the previous section).
4. **Contact your organisation's IT administrator** to verify that the `encodebiz.com` domain is not blocked or in quarantine.
5. If the problem persists, contact CheckBiz360 support stating the recipient's email address and the type of email that is not arriving.

---

> **Role note:** Welcome and password reset emails are addressed to all users regardless of their role. Resending the access and changing the email can be done by whoever edits employee records: the **Owner**, the administrators and the **Manager**.

## Related articles

- [Notification types](63-notification-types.md)
- [Push notifications in the app](64-push-notifications-in-the-app.md)
- [Configure notification preferences](65-configure-notification-preferences.md)
- [Notification history](67-notification-history.md)
