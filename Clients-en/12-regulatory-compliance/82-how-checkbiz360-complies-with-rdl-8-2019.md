# How CheckBiz360 complies with RDL 8/2019

## Why technology matters in regulatory compliance

RDL 8/2019 does not require a specific technological system, but it does establish requirements that in practice can only be guaranteed with digital tools: daily recording with a precise timestamp, retention for four years, worker access to their own data and complete traceability of any correction.

A paper record can be lost, modified without a trace or unavailable when an inspector asks for it. A spreadsheet can be edited retroactively without anybody detecting it. CheckBiz360 is designed so that none of those situations is possible.

This guide explains the specific technical mechanisms with which the platform guarantees compliance.

---

## Automatic timestamp recording

Every time an employee clocks in or out from the CheckBiz360 app, the system records an **immediate timestamp accurate to the second** on the platform's servers. This record requires no additional action from the manager or the employee beyond the clock-in itself.

The timestamp recorded includes:

- The exact date and time of the event.
- The employee's identification.
- The event type (entry, exit, break, resumption).
- Identification of the device the record was made from.
- GPS coordinates at the moment of the record, if the geofence is configured.

This record is produced at the moment of clocking and cannot be modified once created.

---

## Immutable storage of the history

CheckBiz360 guarantees the **immutability of the record history**. This means that:

- No platform user, regardless of their role, can delete a clock record from the history.
- No user can modify a record's original data (time, date, event type) without that modification being logged as a separate manual correction.
- The original history is always retained, even when corrections are made.

This design is fundamental to regulatory compliance: if an inspector requests the records for a period, the company can demonstrate not only which clock records occurred, but also whether any was corrected and for what reason.

---

## Complete traceability of manual corrections

In day-to-day operations, it is common for managers to need to correct erroneous records: an employee forgot to clock out, a one-off technical error occurred or a record for a special workday needs adjusting.

CheckBiz360 allows these corrections, but with one condition: **every manual correction is logged with full traceability**. For each correction, the system stores:

- The record's original value before the correction.
- The new value entered by the manager.
- The identity of the user who made the correction (name and role).
- The date and time the correction was made.
- The reason for the correction, which the manager has to enter as a mandatory field.

This traceability satisfies the record integrity requirement the regulations demand and which the Labour Inspectorate verifies in its actions.

---

## Employee access to their own history

RDL 8/2019 establishes the worker's right to consult their own records. In CheckBiz360, this right is satisfied directly: **each employee can consult their complete clocking history from the mobile app**, with no need to request it from any manager.

The employee sees in their app:

- All their entry and exit records, with exact timestamps.
- The validation status of each record.
- The corrections that have been made to their records, with the correction date.

This access is permanent and in real time. It does not require the manager to export any file or carry out any procedure.

---

## Why paper records and spreadsheets do not offer the same guarantees

The Labour Inspectorate has questioned in numerous actions the validity of recording systems based on paper or editable spreadsheets. The reasons are technical and legal:

| Aspect | Paper record | Spreadsheet | CheckBiz360 |
|---|---|---|---|
| Immutability | Not guaranteed | Not guaranteed | Guaranteed by design |
| Traceability of corrections | Impossible | Impossible without active auditing | Automatic and complete |
| Worker access | Depends on a manual process | Depends on a manual process | Direct access from the app |
| Four-year retention | Risk of loss or deterioration | Risk of loss or deletion | Retention on managed servers |
| Precise timestamp | Requires manual discipline | Requires manual discipline | Automatic at the moment of clocking |

When the ITSS detects that a company uses editable spreadsheets as its only recording system, it can consider that no reliable recording system exists and issue an infringement notice even if the data appears complete.

---

## Guaranteed retention period

CheckBiz360 retains all working-time records for the minimum period required by RDL 8/2019 (**four years**). The company does not need to carry out any procedure to meet this requirement while it keeps its account active.

> **Warning:** If the company decides to cancel its CheckBiz360 account, it has to export all the historical records before closure. The four-year retention obligation falls on the company, not on the provider. CheckBiz360 cannot be held responsible for the loss of historical records if the company does not export its data before closing the account.

---

> **Note:** This article describes the platform's technical mechanisms in relation to regulatory compliance. For specific legal advice on your company's situation, consult your employment advisers.

---

## Related articles

| Article | Description |
|---|---|
| [Mandatory time recording in Spain](./81-mandatory-time-recording-in-spain.md) | What RDL 8/2019 requires and who it applies to |
| [Regulatory compliance report](../11-reports-and-exports/79-regulatory-compliance-report.md) | How to generate the report for the Labour Inspectorate |
| [Data retention and protection](./83-data-retention-and-protection.md) | Legal bases for processing employee data |
| [Preparing for a labour inspection](./84-preparing-for-a-labour-inspection.md) | Practical guide to an ITSS visit |
| [Anomaly detection](../07-operational-intelligence/55-anomaly-detection.md) | How the system detects irregular clocking patterns |
