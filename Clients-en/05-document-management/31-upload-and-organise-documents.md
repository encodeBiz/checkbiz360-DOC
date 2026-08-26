# Upload and organise documents

The CheckBiz360 back office centralises the whole process of uploading and distributing employment documents. From a single panel you can upload files, assign them to the relevant employees, define their visibility and organise the document archive by category and period.

## Before you start

To upload documents you need the Manager or Owner role in the organisation. Supervisors can have access to this function if the manager has delegated that permission to them. If you do not see the upload option in your panel, check with the organisation's manager to verify your permissions.

The accepted formats are PDF and images (JPG, PNG), with a **maximum of 10 MB per file**. A larger file is rejected with the error `documents/file_too_large`, and an unsupported format with `documents/invalid_mime_type`.

PDF is recommended: it is the format that guarantees the document displays correctly on any device, especially in the employee's mobile app.

## How to upload a document

1. Sign in to the back office and navigate to the **Documents** section of the main menu.
2. Press the **New document** button.
3. Fill in the form fields as described in the next section.
4. Attach the file from your device.
5. Review the details and press **Save** or **Publish** as appropriate.

> **Important:** If you press **Save** without publishing, the document will remain in draft status and the employee will neither see it nor receive a notification. For the employee to have access, the document has to be published and with visibility enabled.

## Form fields

### Title

The title is the name under which the employee will see the document in their app. Be descriptive and consistent with the format your company uses. A common example is: `Payslip - March 2026`.

### Description

An optional field that lets you add context to the document. You can use it to state the period it covers, whether it contains a correction to previous versions or any instruction for the employee.

### Document type

Select the type that applies. There are twelve:

- **Payslip**: salary slips, settlements, supplements.
- **Contract**: employment contracts, extensions, changes to terms.
- **Reprimand** and **Warning**: disciplinary documentation.
- **Supporting document**: absence and leave supporting documents.
- **Certificate**: employer certificates, employment history, tax withholding.
- **Policy**: company policies, code of conduct.
- **Procedure**: work instructions, operational protocols.
- **Risk prevention**: risk assessments, health and safety training, PPE issue.
- **Branch protocol**: rules specific to one site.
- **Project document**: documentation associated with a project or client.
- **Other**: any document that does not fit the above.

> **Important:** unlike a simple label, **some types are restricted by role**. Anyone without a sufficient level for that type receives the error `documents/restricted_document_type`. The type therefore does affect access, as well as making searching easier.

### Scope

In addition to the type, each document has a scope that determines who it is addressed to:

- **Employee**: a personal document, such as a payslip or a contract.
- **Branch**: addressed to all the staff at one site, such as an opening protocol.
- **Organisation**: addressed to the whole workforce, such as a company policy.

The scope also determines the read receipt mode available: from a specific employee, from the employees of one branch or from the whole organisation.

### Recipient employee or employees

You can assign the document to a single employee or to several at once. When you assign the same document to several employees —for example, an information circular— the system creates one document entry per employee, so that each accesses their own copy and traceability is kept separate per person.

To assign multiple recipients, use the employee search field and select them one by one or through the branch or department filters if you have them configured.

### Visibility: the private field

The **Private** field controls whether the employee can see the document from their app.

- **Private off (public)**: the employee can view and download the document from the moment it is published.
- **Private on**: the document is only visible to managers with back office access. The employee will not see it in their app even though the document exists in the system.

This field is useful when you need to upload sensitive internal documentation —such as disciplinary notes or confidential appraisals— without the employee accessing it until you decide.

> **Note:** You can change the visibility of a document already uploaded at any time from the document's details. See the article on private documents for more information on the use cases for this field.

## Organising the document archive

As the volume of documents grows, keeping the archive tidy becomes essential for locating documents quickly.

Apply these conventions from the outset:

- **Consistent title**: always use the same naming format, for example `[Type] - [Employee/Period]`.
- **Correct type**: do not use "Other" as a catch-all. With twelve types available, almost everything has its place, and the type conditions who can see the document.
- **Clear periods in the description**: especially on payslips, state the month and year in the title or the description.

The document panel filters let you search by type, by scope, by employee and by upload date, which makes management easier even when the archive holds hundreds of documents.

## Related articles

- [What the document module is](30-what-is-the-document-module.md)
- [Payslips and contracts](32-payslips-and-contracts.md)
- [Private documents](33-private-documents.md)
- [Document notifications](34-document-notifications.md)
- [Document access permissions](37-document-access-permissions.md)
- [Export documents](38-export-documents.md)
