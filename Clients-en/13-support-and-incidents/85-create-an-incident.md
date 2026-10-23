# Create an incident

CheckBiz360's incident module is the formal communication channel **within your organisation** between whoever detects an operational problem and whoever can resolve it.

It is important not to confuse it with CheckBiz360 technical support: an incident is an internal report —"I couldn't clock in when I arrived", "the break was recorded incorrectly", "this branch's geofence is badly configured"— addressed to a manager within the company itself. For problems with the platform itself, the channel is EncodeBiz support, described in [Contact technical support](./87-contact-technical-support.md).

---

## What it is for

The module solves a specific problem: stopping operational incidents from being resolved over WhatsApp or by word of mouth, so that they are recorded instead, with their history, alongside the clocking data they refer to.

Each incident captures who is reporting it, about which branch, what type it is, and maintains a reply thread until it is marked as resolved.

---

## Incident fields

| Field | Description |
|---|---|
| **Employee** | The person the incident relates to |
| **Branch** | The workplace where it occurred |
| **Source role** | The level it is reported from: worker or supervisor |
| **Target role** | The level it is addressed to: worker or supervisor |
| **Type** | Working-time record, break record, configuration or other |
| **Status** | Pending, under review or resolved |
| **Comment** | The description of the problem |
| **Include location** | Attaches the coordinates it is reported from, useful when the problem relates to the geofence |

### The four incident types

- **Working-time record** — problems with the check-in or check-out: it was not recorded, it was recorded at the wrong time, a workday was left open.
- **Break record** — problems with the start or end of a break.
- **Configuration** — something badly configured preventing normal work: a geofence that is too narrow, a schedule that does not match, a calendar that has not been resolved.
- **Other** — any situation that does not fit the above.

---

## How to create an incident from the back office

1. Go to **Contact** in the side menu (it used to be called *Incidents*) and stay on the **Issues** tab.
2. Press the create incident button.
3. Select the **employee** and the **branch** it relates to.
4. State the **source role** and the **target role**.
5. Choose the **type** that best describes the problem.
6. Write the **comment** with the detail: what happened, when and how often it recurs. The more specific it is, the less back and forth in the thread.
7. Enable **include location** if the problem relates to where the employee is.
8. Save. The incident is created **under review**.

> **Tip:** when describing a clocking problem, include the exact date and time and, if an error code appeared on screen, copy it literally. With the code, the diagnosis is immediate: see [Complete error codes](../14-reference/90-complete-error-codes.md).

---

## What happens next

The incident is listed in **Contact**, **Issues** tab, filterable by status, branch and employee. The manager reviews it and **replies** from its detail; each reply can also change the status. The exchange remains as a consultable thread.

While the incident is not resolved, it continues to accept replies. See [Incident tracking and resolution](./86-incident-tracking-and-resolution.md).

The other **Contact** tab, **Requests**, collects the vacation and leave that people request from the app. Only the owner and the administrators see it. See [Vacation and leave from the app](../04-calendar-and-schedules/115-vacation-and-leave-from-the-app.md).

---

## Role note

Managing incidents from the back office is the responsibility of **Owner** and **Manager**. The source and target roles of each incident —worker and supervisor— identify the parties involved in the operational problem, not who administers the module.

---

## Related articles

| Article | Description |
|---|---|
| [Incident tracking and resolution](./86-incident-tracking-and-resolution.md) | Statuses, replies and an incident's history |
| [Contact technical support](./87-contact-technical-support.md) | Channel with the EncodeBiz team for platform problems |
| [Common problems and solutions](./88-common-problems-and-solutions.md) | Diagnosis of the most frequent situations |
| [Complete error codes](../14-reference/90-complete-error-codes.md) | Cause and solution for each code |
| [Request a manual workday](../03-time-tracking/19-request-a-manual-workday.md) | The route for correcting a clock record that was not stored |
