# App access: whether it arrived, resending it and changing the email

When someone says they cannot get into the app, the first thing is to know whether the access email reached them. Before, you had to ask them whether they had checked spam. Now each person's record says whether the email was delivered, whether it bounced or whether they are already using the app, and from there you can resend the access or change their email.

---

## What you see on the record

On the employee's record, the **App access** block brings together three things:

- **Access email.** The status of the last welcome email: which address it went to, when, and what happened to it.
- **Clock-in point card.** If you have the [clock-in point](../03-time-tracking/113-clock-in-point.md), the status of the last time their card was sent.
- **Activity in the app.** The date they were **Last active**, or *No activity in the app* if they have not signed in yet. If they have no user, it says so: *No app user*.

Once the person has used the app, the block says **Access confirmed**: there is nothing else to check.

In the employee list, the **Access** column gives the same summary person by person.

### Email statuses

| Status | What it means |
|---|---|
| **Sent** | It has gone out and there is no news yet from the receiving server. |
| **Delivered** | The person's mail server has accepted it. If they cannot see it, ask them to look in spam. |
| **Delayed** | The receiving server is holding it. It usually sorts itself out. |
| **Bounced** | The address does not exist or does not accept mail. |
| **Marked as spam** | The person marked it as junk mail. |
| **Rejected** | The receiving server rejected it. |
| **Could not be sent** | It never went out. |
| **No record** | There is no record of the sending, usually because it was sent before this tracking existed. |

When the email has not arrived, the record warns you at the top, with what happened and what to do. For example, if it bounced, it suggests changing the email to one that works.

---

## Resend access

**Resend access** sends the welcome email again with a **new password**. The previous one stops working at that moment, including for the panel if the person uses it. The panel reminds you before you confirm.

Use it when the person cannot find the email, deleted it or does not remember the initial password.

---

## Change the email

The email is what the person uses to sign in to the app, so it has its own button: **Change email**, on the record. In **Edit**, the same button is next to the email field.

1. Click **Change email** and type the **New email**.
2. Decide whether to tick **Send access to the new email**.
3. Click **Change email**.

Before you confirm, the panel shows **What changes**:

- The person will sign in to the app with the new email, and to the panel if they use it. The previous one no longer works for signing in.
- It changes on their record and in search.
- Email notifications will go to the new address.
- Nothing else changes. Their clock-ins, their documents, their QR and their clock-in point code stay the same. If you want the card at the new email, use **Send card**.
- If the new email is already used by another account, nothing is changed.

With **Send access to the new email** ticked, the welcome goes to the new address with a new password and they will have to sign in to the app again. Without it, nothing is sent: they will sign in with the new email and their usual password, and you will have to let them know yourself.

---

## Send the clock-in point card

With the clock-in point subscribed, **Send card** emails the person their QR and their code. If you had already sent it, the button says **Resend card**. If they have no email, the panel says so and it cannot be sent.

---

## The home page alert

If someone's access email has not arrived, the panel's home page warns you under **Needs attention** with the **Access email not delivered** alert, with the names. The **View** button takes you to **Employees**. The alert disappears on its own once you fix the email and the access is delivered. It does not count people who have left.

---

## Who can do it

Anyone who can edit employee records: the owner, the administrators and the managers.

---

## Related articles

- [Create and manage employees](06-create-and-manage-employees.md)
- [First sign-in](../10-mobile-app/70-first-sign-in.md)
- [Email notifications](../09-notifications/68-email-notifications.md)
- [The home page: today, alerts and recent weeks](../07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md)
- [Common problems and solutions](../13-support-and-incidents/88-common-problems-and-solutions.md)
