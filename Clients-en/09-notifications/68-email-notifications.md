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

### Resending an invitation

If the employee has not been able to activate their account (they did not find the email, the link expired or they entered incorrect details), the manager can resend the invitation from the back office:

1. Navigate to **Employees** and open the record of the employee whose invitation you want to resend.
2. Find the account status indicator. If the account is not activated, the **Resend invitation** button will appear.
3. Press the button. The system will send a new welcome email with a new temporary password to the employee's email address.

> **Warning:** Resending the invitation invalidates the previous temporary password. If the employee had already received the first invitation and was using it, they will have to use the new password from the second sending.

### Password reset

When a user requests a password reset (from the sign-in screen, pressing "I have forgotten my password"), the system sends an email with a secure reset link. This link is valid for 30 minutes from the moment of sending. Once expired, the user has to request a new link.

The email includes:
- A button with the reset link.
- The link's expiry time.
- A notice that if the user did not request the reset, they can ignore the email.

---

## Additional email notifications and fallback

> **Status: Planned**
> This feature is part of the roadmap and is not available yet in the current version.

Sending operational notifications by email (event alerts, read receipt reminders, task warnings, etc.) and the automatic email fallback mechanism when a push notification cannot be delivered to the user's device are planned for a future version of the platform.

---

## What to do if the email does not arrive

If an employee or manager does not receive an expected email from the system, follow these steps:

1. **Check the spam or junk folder** in the mail client. Emails from `hola@encodebiz.com` may be classified incorrectly the first time.
2. **Verify the recipient's email address** in the back office. Go to the employee's or user's record and confirm the address is written correctly and without extra spaces.
3. **Resend the invitation** if it is the welcome email (see the previous section).
4. **Contact your organisation's IT administrator** to verify that the `encodebiz.com` domain is not blocked or in quarantine.
5. If the problem persists, contact CheckBiz360 support stating the recipient's email address and the type of email that is not arriving.

---

> **Role note:** Welcome and password reset emails are addressed to all users regardless of their role. Resending invitations can be done by the **Owner** and the **Manager**.

## Related articles

- [Notification types](63-notification-types.md)
- [Push notifications in the app](64-push-notifications-in-the-app.md)
- [Configure notification preferences](65-configure-notification-preferences.md)
- [Notification history](67-notification-history.md)
