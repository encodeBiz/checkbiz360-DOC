# Employee validation by QR

CheckBiz360 offers an optional identity verification mechanism prior to clocking in, called employee validation. When enabled in the branch configuration, it uses a QR code generated in the employee's app that the supervisor scans to confirm that the person present is who they say they are. This article explains how this mechanism works, when it applies and what it represents from a technical point of view.

> **Note:** QR validation is a mechanism configurable per branch, not a universal requirement of the system. Regardless of whether QR validation is enabled or not, the clocking process always automatically validates the trusted device, the geolocation within the geofence and the employee's active shift schedule.

---

## What employee validation is

Employee validation is an in-person identity verification mechanism that can be enabled as a step prior to the first clock-in of the workday. Its purpose is to add an extra layer of security against delegated or fraudulent recording, especially in environments where the employee's identity has to be confirmed in person.

This mechanism is fully configurable per branch: not every branch or organisation requires it. When it is enabled, the employee cannot complete the clock-in until the supervisor has scanned and validated their code. At branches where it is not enabled, the employee can clock in directly; the system still validates the trusted device, the geolocation and the active shift at that moment.

---

## The validation token

When the employee signs in to the app and selects their working organisation, the system generates a **verification code**. This code is a base64-format string containing the employee's identifier and the organisation's identifier.

The verification code has a limited validity and is used exclusively for the QR validation process. It is not reusable between sessions or transferable between devices.

---

## The QR code

From the verification code, the app generates a QR code visible on the screen of the employee's device. This code contains the information the system needs to identify the employee unambiguously.

The supervisor, using their own device with the CheckBiz360 app, scans this QR code. The system verifies the verification code, confirms the employee's identity and marks the validation as complete.

---

## The process flow when QR validation is enabled at the branch

1. The employee opens the CheckBiz360 app and signs in with their credentials.
2. They select the relevant working organisation.
3. The app detects that the branch has QR validation enabled and shows the validation screen with the QR code generated from the verification code.
4. The supervisor comes to the employee and scans the QR from their device.
5. The system verifies the token and records the identity validation.
6. The employee's app moves automatically to the clocking screen.
7. The employee records their entry; the system validates the trusted device, the geolocation and the active shift at that moment.

When QR validation is not enabled at the branch, the process starts directly at step 7: the employee reaches the clocking screen and the system applies the automatic device, geolocation and schedule validations just the same.

---

## Warming up the clocking system

When the supervisor scans the QR code and completes the validation, the system automatically and transparently runs a warm-up process on the clocking environment. This process prepares and checks in the background all the parameters needed for the clock-in to be processed immediately: active shift, geofence, device configuration and employee status.

The employee does not notice this process. From their perspective, they simply move from the validation screen to the clocking screen. However, this mechanism improves the speed and reliability of the record, especially in environments with many employees clocking in within the same time window.

---

## When QR validation is needed

QR validation is enabled according to the branch configuration. Some common scenarios where it is used:

- Environments with high staff turnover or temporary hires where the employee's identity may not be known to the supervisor.
- Premises with strict access control where dual verification is required.
- Sectors with regulatory obligations for in-person identification (security, healthcare, food).
- Companies that want to add an extra layer of control without needing physical biometric readers.

---

> **Privacy notice:** The QR code contains only the employee's identifier and the organisation's, both in encrypted format. It includes no personal data in plain text. The verification code expires after use or when the employee's session ends.

---

## Roles with access to this feature

The employee with the **employee** role generates the QR from their app. Scanning and validating the code is the responsibility of users with the **supervisor**, **manager** or **owner** role. Enabling QR validation as a prerequisite to clocking in is configurable by the **manager** or **owner** roles.

---

## Related articles

- [Check-in and check-out from the app](14-check-in-and-check-out-from-the-app.md)
- [How clocking in works](13-how-clocking-in-works.md)
- [Review and approval of clock records](20-reviewing-and-approving-clock-records.md)
- [Statuses and error codes](22-statuses-and-error-codes.md)
