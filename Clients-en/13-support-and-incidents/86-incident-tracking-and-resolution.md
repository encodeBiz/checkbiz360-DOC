# Incident tracking and resolution

Once created, the incident lives in the **Incidents** section of the back office until it is resolved. This article describes its statuses, how replies work and what is recorded.

Remember that incidents are an **internal channel of your organisation**. For platform problems, the channel is EncodeBiz support: see [Contact technical support](./87-contact-technical-support.md).

---

## Incident statuses

| Status | Meaning |
|---|---|
| **Pending** | Recorded, waiting for somebody to take it on |
| **Under review** | Somebody is investigating the problem. This is the status an incident created from the back office is born with |
| **Resolved** | The problem has been solved. The incident stops accepting replies |

There is no "closed" status and no automatic closure over time: an incident stays open until somebody marks it as resolved.

### Who can change the status

The status is changed in two ways: by editing the incident, or **when replying** in its thread, where each reply can carry an associated status change. Both actions belong to the roles with back office access: **Owner** and **Manager**.

---

## Replying to an incident

Tracking is done through replies. Each reply stays in the thread, with its author and its date, and can also move the status.

1. Go to **Incidents** in the side menu.
2. Find the incident using the status, branch or employee filters.
3. Open its detail.
4. Press **Reply**.
5. Write the message and, where appropriate, select the new **status**.
6. Confirm.

> **Important:** an incident in *Resolved* status no longer accepts replies. If the problem reappears, create a new incident and refer to the previous one in the comment.

> **Warning:** do not open a new incident to add information to a case that is still open. Use the reply thread to keep the context grouped together.

---

## The case history

The incident detail shows the initial statement and, below it, all the replies in chronological order, each with its author, the date and the status change it produced. The list also indicates how many replies each incident has accumulated, which makes it easy to spot at a glance those with the most back and forth.

---

## When to mark an incident as resolved

Mark it as resolved when you have verified that the problem has gone away and operations have returned to normal. It is worth leaving a final reply explaining **what was causing it and what was done**: that is what turns the incident history into something worth consulting when the same symptom reappears months later.

If the same symptom generates repeated incidents, it is a sign of an underlying cause —a badly sized geofence, a calendar that does not cover a shift— worth tackling in the configuration rather than resolving case by case.

---

## Exporting the incident history

> **Status: Not available**
> Exporting the incident list to CSV or PDF is not implemented in the current version and has no planned date.

Incidents are consulted and filtered on screen. If you need the history for an audit, request it from support at hola@encodebiz.com.

---

## Role note

This article is aimed at **Owner** and **Manager**, the only roles with access to the incident module in the back office.

---

## Related articles

| Article | Description |
|---|---|
| [Create an incident](./85-create-an-incident.md) | Fields, types and creation of an incident |
| [Contact technical support](./87-contact-technical-support.md) | Channel with the EncodeBiz team |
| [Common problems and solutions](./88-common-problems-and-solutions.md) | Diagnosis of the most frequent situations |
| [Complete error codes](../14-reference/90-complete-error-codes.md) | Cause and solution for each code |
