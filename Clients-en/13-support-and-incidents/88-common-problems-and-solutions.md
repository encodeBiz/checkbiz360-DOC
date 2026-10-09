# Common problems and solutions

This article gathers the fourteen most frequent technical and operational situations in CheckBiz360, together with the recommended diagnostic and resolution steps. Consult this guide before opening an incident, since most of these problems can be solved directly with no need for support team intervention.

---

## 1. The employee cannot clock in (generic error)

**Symptom:** The employee presses the clocking button in the app and an error message appears with no specific code, or the operation does not complete.

**Resolution steps:**

1. Verify that the device has an active internet connection (Wi-Fi or mobile data). Without a connection, the clock-in cannot be processed.
2. Check that the device's GPS is enabled. Go to the operating system settings and confirm that location is enabled for CheckBiz360.
3. Check that the application has been granted location permissions: on iOS, go to **Settings > CheckBiz360 > Location** and select "While Using the App". On Android, go to **Settings > Apps > CheckBiz360 > Permissions > Location**.
4. Close the app completely and open it again.
5. If the problem persists, update the app to the most recent version from the app store.

---

## 2. Persistent "Outside the zone" error

**Symptom:** The employee receives the error `checklog/out_of_radius` repeatedly even when they are physically at the workplace.

**Resolution steps:**

1. In the back office, go to **Branches** and select the branch affected.
2. Verify the branch's coordinates: check that the latitude and longitude recorded correspond to the exact point of the premises and not to an approximate or incorrect address.
3. Review the clocking radius configured for the branch. If the building or its surroundings have imprecise GPS signal (interior floors, basements, areas with interference), consider widening the radius.
4. Ask the employee to check their device's GPS accuracy: outdoors, accuracy is usually 5 to 15 metres; indoors it can exceed 50 metres.
5. If the problem affects every employee at the branch, check whether the coordinates were recently modified accidentally.

---

## 3. The employee does not receive the welcome email

**Symptom:** An employee recently created on the platform has not received the invitation email with their access credentials.

**Resolution steps:**

1. Ask the employee to check their junk or spam folder.
2. Verify in the back office, inside the employee's profile, that the email address is written correctly (no spaces, no typos).
3. If the address is correct and the email does not appear in any folder, go to the employee's profile and press **Resend invitation**.
4. If after resending the email it still does not arrive, check with the employee whether their company has corporate mail filters that may be blocking messages from @encodebiz.com. In that case, that domain will have to be added to the allowed senders list.

---

## 4. The app does not open or closes on its own

**Symptom:** The CheckBiz360 application closes unexpectedly on opening or during normal use.

**Resolution steps:**

1. Check that the installed version is the most recent: go to the App Store or Google Play and update if a version is available.
2. Restart the device completely and try opening the app again.
3. If the problem persists after updating, uninstall the application and install it again from the official store.
4. After reinstalling, sign in with the same credentials. Server data is not lost by reinstalling.
5. If the app keeps closing, note the device model and the operating system version and include this information when opening an incident.

---

## 5. "Unauthorised device" error

**Symptom:** The employee receives the error message `auth/untrusted_device` when trying to sign in or clock in from a new device.

**Resolution steps:**

1. Sign in to the back office with your Owner or Manager account.
2. Go to the profile of the employee affected.
3. In the **Trusted devices** section, find the new device (it will be listed with its identifier).
4. Press **Authorise device** to mark it as trusted.
5. Tell the employee they can try signing in again.

> **Warning:** review the employee's trusted device list and remove those they no longer use. An old device that remains authorised is an open route to clocking in on that person's behalf.

---

## 6. The employee cannot see their documents

**Symptom:** An employee reports that they cannot find in the app the documents that should be available to them.

**Resolution steps:**

1. Go to the back office and open the **Documents** module.
2. Find the document in question and check its visibility configuration.
3. Review the document's **visibility by role**: if it does not include the employee's role, they will not see it.
4. Check the **scope** and the recipient: if it is employee-scoped, that it is the right one; if it is branch-scoped, that the employee belongs to that branch —otherwise the system responds `documents/employee_not_in_branch`.
5. Verify that the document is not **archived**: archived ones stop being displayed.
6. If the configuration is correct, ask the employee to sign out of the app and sign back in to force a synchronisation.

---

## 7. The push notification does not arrive

**Symptom:** The employee does not receive task, document or system alert notifications on their device.

**Resolution steps:**

1. Verify that the employee has granted notification permissions to CheckBiz360. On iOS: **Settings > CheckBiz360 > Notifications** and enable "Allow Notifications". On Android: **Settings > Apps > CheckBiz360 > Notifications** and enable.
2. Check that "Do not disturb" mode or any silent profile is not active on the device.
3. On some Android devices with aggressive battery management (Xiaomi, Huawei, OnePlus), CheckBiz360 has to be excluded from battery optimisation. Go to **Settings > Battery > Battery optimisation** and exclude the app.
4. Make sure the app is updated to the latest version.
5. If the problem persists, the employee can sign out and sign back in to register the notification token again.

---

## 8. The attendance history shows gaps

**Symptom:** The employee's history shows days or workdays with incomplete records, even though the employee says they worked those days.

**Resolution steps:**

1. Go to the back office and review the employee's attendance detail on the date affected.
2. Check whether there is a checkin record with no corresponding checkout. This generates an incomplete workday (`incomplete_workday`).
3. If the employee forgot to check out, use the **Manual workday** option to complete the record retroactively.
4. Check whether the employee has workdays with breaks (`restin` / `restout`) left open, which can also cause incomplete records.
5. Check whether on those dates there were disabled workdays in the branch's effective calendar.

---

## 9. The hours calculated do not match those expected

**Symptom:** The total hours worked the platform shows for an employee does not match the manual calculation the manager makes.

**Resolution steps:**

1. Check the **workday mode** of the applicable calendar. With a strict workday, time worked outside the official window is not counted; with a flexible workday, it is added. This is the most frequent cause of the report's hours not matching the raw hours from the clock records.
2. Check whether there are recorded breaks being deducted from the total time.
3. Verify whether any workday is marked as incomplete, which can exclude it from the total calculation.
4. Check the time zone configured at the branch and compare it with the time zone of the employee's device.
5. If you detect a systematic discrepancy, go to the branch configuration and review the workday calculation rules.

---

## 10. The app shows "Outside the schedule" when the employee is on shift

**Symptom:** The employee receives the error `checklog/out_of_schedule` even though they say they are clocking in within their usual schedule.

**Resolution steps:**

1. Go to the back office and review the branch's **effective schedule** for the day in question.
2. Verify the time zone configured at the branch. If the time zone is incorrect, the shift's limits may be calculated with an offset of several hours.
3. Check that the employee has the correct shift assigned for that day in the effective calendar.
4. Check whether there are exceptions or public holidays configured that may be disabling the shift.
5. If the schedule looks correct, check whether there is a clocking tolerance margin configured and whether the employee was trying to clock in right at the limit or outside it.

---

## 11. The employee appears as inactive in the back office

**Symptom:** When consulting the employee list, one of them appears with inactive status even though they should be active.

**Resolution steps:**

1. Go to the employee's profile in the back office.
2. Review the **Profile status** field. If it is set to "Inactive", press **Reactivate employee**.
3. Verify that the account was not deactivated as a result of temporary leave or an offboarding process started in error.
4. Check that the organisation's subscription is active and has no outstanding payments. There is no employee limit per plan —billing is per employee and month— but a subscription with payment issues can block operations.

---

## 12. A report for a previous period cannot be generated

**Symptom:** When trying to generate a report for a past date range, the system returns an error or shows no data.

**Resolution steps:**

1. Verify that the date range selected does not exceed the data retention period included in your subscription plan.
2. Check that your role has permissions to generate the selected report type. Cost and anomaly reports are restricted to Owner and Manager.
3. Make sure the filters applied (branch, employee) do not exclude all the records available for that period.
4. If the problem persists with a date range that should be within the retention period, open an incident with the exact range you are trying to consult.

---

## 13. The employee cannot clock in on a public holiday even though they have a shift

**Symptom:** The employee has a custom schedule with a shift that day, but the clock-in is rejected with `checklog/day_disabled`. The app explains that today is not a working day.

**Resolution steps:**

1. Check whether that date is a public holiday at the employee's **organisation** or **branch**. Public holidays apply to all the employees within their scope, even if one of them has their own shift that day.
2. If the whole branch works that day, remove the holiday from the branch (or from the organisation, and add it only at the branches that close).
3. If only part of the workforce works, do not mark the day as a holiday at the branch and record an absence for those who have the day off. See [Public holidays and non-working days](../04-calendar-and-schedules/29-public-holidays-and-non-working-days.md#what-happens-if-the-company-works-on-public-holidays).
4. For the workday already worked, record a manual workday.
5. If there is no holiday, check that the employee does not have an absence recorded that day (`checklog/absence`).

---

## 14. A task cannot be started, resumed or completed

**Symptom:** When starting, resuming or completing a task, an error appears and the task does not change.

**Resolution steps:**

1. `task/no_open_session`: the employee does not have an open workday. They must clock in and try again.
2. `task/out_of_worksite`: the task has its own work site and the employee is outside its margin. The warning states the distance. If they are at the site and the margin is too narrow —a car park, a warehouse—, widen the margin on the task.
3. `task/geo_required`: a task with its own work site has been attempted from the back office. Starting, resuming or completing it has to be done by the employee from the app.
4. If the action is **resume** and `task/not_paused` appears, another assignee has already resumed it: refresh the task.
5. If the task is rejected or validated and cannot be completed (`task/invalid_transition`), reopen it by returning it to *Assigned* from **Edit**.

---

> **Warning:** If any of the steps above does not solve the problem, do not repeat the same action several times. Gathering evidence (screenshots, error code, exact date and time) and opening an incident is always more effective than trying to force a solution that may make the problem worse.

---

## Role note

This article is aimed mainly at **Owner** and **Manager**, who are responsible for diagnosing and resolving their teams' operational problems. Employees with the Worker role who experience any of these problems should report them to their Manager.

---

## Related articles

| Article | Description |
|---|---|
| [Create an incident](./85-create-an-incident.md) | How to formally open a support case |
| [Contact technical support](./87-contact-technical-support.md) | Channels and response times of the support team |
| [Complete error codes](../14-reference/90-complete-error-codes.md) | Complete reference for every system error code |
| [Request a manual workday](../03-time-tracking/19-request-a-manual-workday.md) | How to correct an incorrect or missing clock record |
| [Managing trusted devices](../02-employees/10-biometrics-and-trusted-devices.md) | How to authorise new devices from the back office |
