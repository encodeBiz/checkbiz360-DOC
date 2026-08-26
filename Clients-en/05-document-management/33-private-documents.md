# Private documents

The **Private** field on a document in CheckBiz360 controls whether the employee can see that document from their mobile app. When a document is marked as private, it exists in the system and is accessible to managers with the appropriate permissions, but the employee will neither see it nor receive notifications about it.

This mechanism allows sensitive documentation —such as performance appraisals, reprimand letters or disciplinary documents— to be managed without the employee accessing it before the manager considers it appropriate.

## What it means for a document to be private

When a document's `private` field is enabled:

- The document **does not appear** in the employee's document list in the mobile app.
- No push notification is sent to the employee, even if the notification option is ticked.
- The document **is visible** to managers (Manager, Owner) in the back office.
- The document can be consulted, edited or deleted from the back office by users with sufficient permissions.

When the `private` field is disabled and the document is published:

- The employee can view and download the document from the app.
- If notification was enabled at publication, the employee receives a push alert on their device.

## Visibility table by role

The following table shows what each role can see according to the document's visibility status:

| Role | Private document | Non-private document (published) |
|---|---|---|
| Owner | Visible in the back office | Visible in the back office |
| Manager | Visible in the back office | Visible in the back office |
| Supervisor | Subject to delegated permissions | Visible in the back office (if they have access) |
| Worker (employee) | Not visible | Visible in the mobile app |

> **Note:** A supervisor only has access to the documents of the employees on their team and only if the manager has granted them that explicit permission. See the article on document access permissions for the full detail.

## Common use cases

### Disciplinary documents

Reprimand letters, formal warnings and other disciplinary documents are usually prepared before being formally handed to the employee. Uploading them with private visibility allows them to be held ready in the system without the employee having access until the moment of the official communication.

Once the formal notification has taken place, the manager changes the visibility to public and the employee can access the document from the app and acknowledge receipt if asked to.

### Performance appraisals

Performance appraisals are confidential documents that have to be reviewed and validated internally before being shared with the employee. Keeping them private during the review process guarantees that the employee only accesses the final result once the manager has approved it.

### Internal HR documentation

Some documents are for the exclusive use of the HR department and are not intended for the employee at any point: internal notes, follow-up reports or administrative documentation. For these cases, the private field acts as permanent access control.

## How to change the visibility of an existing document

You can modify the privacy status of a document already uploaded at any time. The process is as follows:

1. Go to the **Documents** section of the back office.
2. Find the document you want to modify using the search filters.
3. Open the document detail by clicking on it.
4. Edit the document and change the value of the **Private** field.
5. Save the changes.

If you change a document from private to public, the employee will be able to see it immediately from their app. If you also want them to receive a notification, you will have to send it manually from the document panel, since the visibility change on its own does not generate an automatic notification.

> **Important:** The change of visibility from private to public is immediate. Make sure the document is in its final state before making it visible to the employee, as there is no grace period and no additional confirmation.

If you change a document from public to private, the employee will stop seeing it in their app immediately, even if they had already consulted or downloaded it.

## Considerations on notifications and privacy

When you upload a document marked as private, the system will not send the push notification to the employee even if the option is enabled. The notification is only sent at the moment of publication if the document is not private.

If you upload a document as private, work on it internally and subsequently make it public, the notification flow is handled manually: you will have to trigger the notification from the document detail if you want to inform the employee.

## Related articles

- [What the document module is](30-what-is-the-document-module.md)
- [Upload and organise documents](31-upload-and-organise-documents.md)
- [Document notifications](34-document-notifications.md)
- [Document access permissions](37-document-access-permissions.md)
- [Read receipt](35-electronic-signature.md)
