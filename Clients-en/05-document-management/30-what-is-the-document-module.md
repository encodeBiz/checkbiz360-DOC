# What the document module is

The CheckBiz360 document module lets companies manage, distribute and archive employment documents directly on the platform. Unlike a generic file repository, each document is linked to a specific employee and to their employment relationship with the organisation, which turns the system into a structured, traceable digital personnel file.

The module is part of the subscription: it is available under **Documents**, in the back office side menu, regardless of the plan contracted.

## What it is for

Document management in CheckBiz360 answers a common need in HR departments: distributing employment documents in an orderly way, guaranteeing that the employee receives them and can consult them, and maintaining a digital archive organised by document type and period.

With the document module you can:

- Upload payslips, contracts, certificates and other employment documents from the back office.
- Direct each document to a specific employee, to a whole branch or to the whole organisation.
- Send a push notification to the employee at the moment of publication.
- Control which roles can view each document.
- Require a **read receipt** and check who has given it and who has not.
- Archive a document when it is no longer current, without losing it.

## Types of document that can be managed

The module classifies documents into twelve types:

| Type | Common examples |
|---|---|
| Payslip | Monthly salary slip, final settlement |
| Contract | Initial contract, extensions, changes to terms |
| Reprimand | Disciplinary reprimand letter |
| Warning | Prior notice, formal warning |
| Supporting document | Absence and leave supporting documents |
| Certificate | Employer certificate, employment history, tax withholding |
| Policy | Company policy, code of conduct |
| Procedure | Work instruction, operational protocol |
| Risk prevention | Risk assessment, health and safety training, PPE issue |
| Branch protocol | Rules specific to one workplace |
| Project document | Documentation associated with a project or client |
| Other | Any document that does not fit the above |

The type is assigned when the document is uploaded and makes search filters easier, both for managers and for the employee from the app.

### Document scope

In addition to the type, each document has a **scope** that determines who it is addressed to:

- **Employee** — a personal document, such as a payslip or a contract.
- **Branch** — addressed to all the staff at one site, such as an opening protocol.
- **Organisation** — addressed to the whole workforce, such as a company policy.

## The difference from generic storage

A generic storage service —such as a shared folder in the cloud— stores files without context. CheckBiz360 is not that.

In CheckBiz360, each document knows who it belongs to, which employment relationship it corresponds to, which role can view it and whether the employee has acknowledged receipt. This means, for example, that when an employee opens the app they only see their own documents and not the rest of the team's, or that a manager can filter every current contract at their branch without having to organise folders manually.

This link with the employee and their employment relationship is what makes the module a personnel file rather than a file store.

## Use cases by role

### HR lead or Manager

Each month, the manager uploads the employees' payslips from the back office. They select the file, state the category, the period and the recipient employee, and mark whether they want to send a push notification. The employee receives the notification on their device and, on tapping it, goes straight to the document in the app.

If the document requires a **read receipt**, the manager enables that option before publishing. The system records the date and time the employee confirms they have read it, and which version of the document they did so on.

### Supervisor

The supervisor can consult the documents of the employees on their team whose visibility allows it. Uploading and configuring visibility are usually reserved to manager level or above; some document types are additionally restricted by role and return the error `documents/restricted_document_type` to anyone without a sufficient level.

### Employee (Worker)

The employee accesses their documents from the mobile app, in the documents section. They only see those that have been assigned to them and whose visibility reaches them. They can download them and, if asked to, **acknowledge receipt** from their own device.

> **Note:** the read receipt is not an electronic signature. It evidences that the employee accessed the document and when, but does not incorporate qualified certification. Advanced electronic signature (eIDAS) is on the roadmap.

> **Note:** Documents marked as private by the manager are not visible to the employee until the manager decides to publish them or changes their visibility status. See the article on private documents for more detail.

## Related articles

- [Upload and organise documents](31-upload-and-organise-documents.md)
- [Payslips and contracts](32-payslips-and-contracts.md)
- [Private documents](33-private-documents.md)
- [Document notifications](34-document-notifications.md)
- [Read receipt](35-electronic-signature.md)
- [Version history](36-version-history.md)
- [Document access permissions](37-document-access-permissions.md)
- [Export documents](38-export-documents.md)
