# Document notifications

When a document is published in CheckBiz360, the system can automatically send a push notification to the recipient employee. This notification informs the employee that they have a new document available in the app and, on tapping it, takes them straight to the detail screen for that document.

Document notifications are part of CheckBiz360's communication system and use the same push notification channel as the rest of the platform.

## How the notification works when uploading a document

When the manager publishes a document, they can enable sending a push notification in the upload form itself. If the option is ticked and the document is not configured as private, the system sends the notification automatically at the moment of publication.

The complete flow is:

1. The manager uploads the document and enables the notification option.
2. The system verifies that the document is not marked as private.
3. A push notification is generated and sent to the employee's device.
4. The employee sees the notification on their lock screen or in their device's notification centre.
5. On tapping the notification, the CheckBiz360 app opens directly at the document detail.

> **Important:** If the document is marked as private, no push notification will be sent to the employee, even if the notification option is enabled. The notification is only sent for documents with public visibility.

## What the notification contains

The notification the employee receives includes the information the app needs to navigate directly to the correct document. From the employee's point of view, the notification shows the document title and the company name, similarly to other platform notifications.

## What the employee sees on receiving the notification

On the employee's device, the notification appears with the document title as the main subject. On tapping it, the app opens —or wakes from the background if it was already installed— and navigates directly to the document detail.

From that screen, the employee can:

- Read the complete document.
- Download it to their device.
- Acknowledge receipt if the document requires it.

If the employee does not have the app installed or has push notifications disabled on their device, they will not receive the alert. In that case, the document will still be available in the app in the documents section, but without the proactive alert.

## Configuring which documents generate a notification

The decision whether or not to generate a notification is taken at the moment of uploading the document, by ticking or unticking the corresponding option in the form. There is no global rule that enables or disables notifications for every upload; the choice is per document.

This allows different cases to be handled:

- **Documents that should always notify**: monthly payslips, new contracts, certificates requested by the employee. Always enable notification for this type of document.
- **Internal archive documents that need no alert**: corrected versions of documents already notified, backup copies or administrative documents the employee can consult on demand. In these cases you can upload the document without notification.

> **Note:** If you publish a document without notification and later want to inform the employee, you can send the notification manually from the document detail in the back office. This is useful when an error is detected in the original notification or when you want to resend the alert to an employee who did not open the document.

## Considerations on devices and permissions

For the employee to receive push notifications, it is necessary that:

1. They have the CheckBiz360 app installed on their device (iOS or Android).
2. They have granted notification permissions to the app during installation or in the operating system settings.
3. The device has an internet connection at the moment of sending, or at subsequent moments when the operating system attempts delivery.

If an employee reports that they are not receiving notifications, first check that notification permissions are enabled for the CheckBiz360 app in their device settings, before reviewing the configuration in the back office.

## Related articles

- [What the document module is](30-what-is-the-document-module.md)
- [Upload and organise documents](31-upload-and-organise-documents.md)
- [Private documents](33-private-documents.md)
- [Read receipt](35-electronic-signature.md)
- [Document access permissions](37-document-access-permissions.md)
