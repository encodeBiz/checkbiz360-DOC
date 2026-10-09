# Traceability and change history

Every clock record in CheckBiz360 carries a complete, immutable log of all the modifications made to it since it was created. This change history is the basis of the attendance control audit system and makes it possible to demonstrate, to any inspection or internal review, who made each change, when and to which data.

---

## What the change history is

The change history is a log linked to each attendance record that stores, in chronological order, every intervention that has modified that record. Each item represents a specific action and contains all the information needed to reconstruct the clock record's complete history.

Unlike other data in the system that can be edited, the change history is **immutable**. Entries cannot be modified or deleted once recorded. This guarantees the integrity of the history and its validity as documentary evidence.

---

## Structure of each history entry

Each record in the change history contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique identifier of the audit entry |
| Date and time | Exact timestamp of the moment the change was made |
| Action | Type of modification performed (see action table) |
| User UID | Identifier of the user who executed the action |
| Previous state | Record data before the change |
| New state | Record data after the change |

### Types of action recorded

| Action | Meaning |
|---|---|
| `created` | Creation of the original clock record by the employee |
| `updated` | Modification of a clock record field by a manager |
| `edited` | Correction proposed by a manager, pending the employee's acceptance |
| `rejected` | The employee rejected a proposed correction; it includes the reason, and the clock record keeps its previous data |
| `manual_request_created` | Creation of a full manual workday (Mode A) |
| `manual_checkout_created` | Creation of a manual checkout on an open checkin (Mode B) |

---

## Why the history is immutable

The immutability of the change history responds to two fundamental needs:

**Data integrity:** Once an action has been recorded, it cannot be altered. This means the history faithfully reflects what happened, with no possibility of later rewriting.

**Evidential validity:** In employment matters, time control records have value as evidence before the Labour Inspectorate. An immutable, traceable history is the guarantee that the data has not been manipulated after the fact. If a clock record is modified subsequently, the history shows both the original and the modified data, and who made the change.

---

## How to view a clock record's change history

1. Sign in to the back office with the **manager** or **owner** role.
2. Navigate to the **Attendance** section for the relevant employee.
3. Select the clock record or workday whose history you want to review.
4. Open the **Change history** or **Audit** tab or section.
5. The system will show all the change history entries in chronological order, with the details of each action.

Each entry shows the name or identifier of the user who made the change, the exact date and time, the action executed and the before and after values of the modified fields.

---

## Legal use case: labour inspection

Faced with a labour inspection, the company may need to demonstrate that the attendance records are intact, have not been fraudulently altered and faithfully reflect the employees' actual working time.

With CheckBiz360, the manager can access the history of any clock record and show:

- Who originally recorded the clock-in and from which device.
- Whether a manager made any subsequent modification, when and for what reason.
- Whether the employee validated or rejected any manual workday or any correction, and for what reason.
- What data the record held before and after any change.

This complete traceability covers the retention and transparency requirements demanded by the time-recording regulations in force.

---

## Exporting the history for audits

The change history can be exported from the back office for use in internal audits or in response to requests from the Labour Inspectorate.

1. From the attendance view or from the audit report, select the date range and the employees to include.
2. Choose the available export format (PDF, CSV or others depending on the organisation's configuration).
3. Download the generated file.

The exported document includes, for each record, both the clock record data and the complete history of interventions.

---

> **Compliance note:** Spanish legislation (Royal Decree-Law 8/2019) requires companies to retain working-time records for four years and to make them available to the Labour Inspectorate when requested. CheckBiz360's traceability system is designed to meet this requirement.

---

## Roles with access to this feature

Consulting the change history is available to the **manager** and **owner** roles. Employees have no direct access to the technical audit history, although they can see the current status of their clock records and the notifications of changes that affect them.

---

## Related articles

- [Request a manual workday](19-request-a-manual-workday.md)
- [Review and approval of clock records](20-reviewing-and-approving-clock-records.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
- [How clocking in works](13-how-clocking-in-works.md)
