# Complete error codes

This article is the reference for the error codes that can appear in the mobile app or in the CheckBiz360 back office. When the system shows an error message, the code accompanying it makes it possible to identify the exact cause and the corrective action.

Codes always follow the format `module/reason`. They are grouped below by module.

> **Note:** if a code appears on screen that is not listed in this article, it means it comes from a service that does not yet have a translated message. Note the literal code and open it as an incident: it is enough information for support to identify it.

---

## Clocking and workday (`checklog`)

The most frequent errors in daily use. Unless stated otherwise, they are seen by the **employee in the app**.

| Code | What it means | What to do |
|---|---|---|
| `checklog/out_of_radius` | The employee is not within the selected branch's clocking radius | Check they are physically at the workplace and that the GPS has good accuracy. If it recurs, review the branch's coordinates and radius |
| `checklog/out_of_schedule` | The clock record falls outside the assigned shift's schedule | Review the effective schedule and the branch's time zone, and the shift assigned to the employee |
| `checklog/day_disabled` | The day is disabled in the effective calendar (public holiday, employee's day off or non-working day) | If the day should have been a working day, correct the calendar. If not, record the hours through a manual workday |
| `checklog/absence` | The employee has an absence recorded that covers that day | If the absence is not correct, remove it from their calendar and clock in again |
| `checklog/different_branches` | An attempt is made to clock the break or the exit at a branch other than the one where the employee clocked in | Clock in at the branch of the entry; if there was a change of site, close the workday and open another |
| `checklog_update/future_not_allowed` | The proposed correction has a future date or time | Enter a time that has already passed |
| `checklog/calendar_not_resolved` | There is no effective calendar resolved for that date | Review the calendar of the organisation, the branch and the employee for that date. In the meantime, enter the hours manually |
| `checklog/branch_geo_required` | The branch has no location configured | The Owner or Manager has to add the branch's coordinates in the back office |
| `checklog/two_type_followed` | An attempt was made to start the workday twice in a row | Close the open workday before starting a new one |
| `checklog/overlap_detected` | A valid workday already exists that overlaps with that time range | Review the employee's history and correct the overlapping record before retrying |
| `checklog/duplicate_pending` | There is already a pending request for that employee on that date | Wait for the manager to resolve the existing request instead of creating another |
| `checklog/checkin_not_found` | The reference check-in for the operation cannot be found | Verify that the entry record the exit is to be associated with exists |
| `checklog/checkin_not_open` | The check-in cannot be closed manually because of its current status | Review the record's status; if it is already closed or cancelled, it does not accept manual closure |
| `checklog/checkout_already_exists` | A pending or valid closure already exists for that check-in | Review the record: the workday already has an exit |
| `checklog/invalid_checki` | Invalid entry record | Retry the clock-in. If it persists, update the app |
| `checklog/invalid_checkout` | Invalid exit record | Check that there is an open entry to close |
| `checklog/invalid_restin` / `checklog/invalid_restout` | Invalid break start or end | Check the order of the records: the break has to be opened and closed within an active workday |
| `checklog/unknown_type` | Unknown record type | Update the app to the latest version |
| `checklog/invalid` | The related record cannot be found | Refresh the screen and retry |
| `checklog/bad_request` | The clock record's data is incorrect or incomplete | Update the app; if it continues, reinstall and sign in again |
| `checklog/internal_error` | Internal server error while processing the clock record | Retry after a few minutes. If it lasts more than 30 minutes, open an incident with the exact time and the employee affected |

> `checklog/manual_request_created` is not an error: it confirms that the manual workday request has been sent correctly and is pending approval.

---

## Access and session (`auth`)

| Code | What it means | What to do |
|---|---|---|
| `auth/invalid-credential` | Incorrect credentials | Check the email and password; use password recovery if necessary |
| `auth/invalid-email` | The email address is not in a valid format | Correct the email entered |
| `auth/missing-email` / `auth/missing-password` | The email or the password is missing | Complete the missing field |
| `auth/email-already-exists` / `auth/email-already-in-use` | That email is already in use | Sign in with that account or use another email |
| `auth/weak-password` | The password does not meet the minimum requirements | Choose a more secure password |
| `auth/too-many-requests` | Too many attempts in a short time | Wait a few minutes before retrying |
| `auth/user-disabled` | The account is disabled | Contact the organisation's Owner or support |
| `auth/operation-not-allowed` | Email and password access is not enabled | Contact support |
| `auth/network-request-failed` | Network error | Check the internet connection and retry |
| `auth/unauthorized` | Unauthorised access to the resource, or expired session | Sign out and back in. If the account was deactivated, contact the Owner |
| `auth/untrusted_device` | The device is not authorised and requires additional verification | The Owner or Manager has to authorise the device from the employee's profile |
| `employee/invalid_token` | The employee's validation has expired or is not valid. It expires after 30 days, like the employee's session in the app | The app signs in again on its own. If the warning persists, sign out of the app and sign in again |
| `turnstile/failed` | It has not been possible to check that the person registering or recovering the password is a human | Reload the page and repeat the verification challenge |

---

## Two-step verification (`twofactor`)

| Code | What it means | What to do |
|---|---|---|
| `twofactor/invalid_code` | The TOTP code entered is not valid | Check that the device's time is correct and generate a new code |
| `twofactor/invalid_token` | The session has expired | Sign in again |
| `twofactor/not_activated` | The employee does not have two-step verification enabled | Enable it from the employee's profile |
| `twofactor/user_not_activated` | The user account does not have 2FA enabled | Enable 2FA from the user profile |
| `twofactor/unauthorized` | The operation requires a 2FA token | Complete the two-step verification to continue |
| `twofactor/internal` | Internal error while processing the verification | Retry; if it persists, open an incident |

---

## Employees (`employee`) and branches (`branch`)

| Code | What it means | What to do |
|---|---|---|
| `employee/not_found` | The employee stated does not exist in the organisation | Verify that the employee is still registered |
| `employee/exist_employee` | An employee with that email or phone already exists | Look for the existing employee instead of creating a new one |
| `employee/branchId_required` | The branch is missing, and it is required | Assign at least one branch before saving |
| `employee/bad_request` | The employee identifier is missing from the operation | Repeat the action from the employee's record |
| `branch/not_found` | The branch stated does not exist | Verify that the branch exists and has not been deleted |
| `employee/fired` | The employee has left the company and cannot be added to a team | Choose another person or reactivate their record |
| `team/not_found` | The team no longer exists | Refresh the list of teams |
| `team/name_taken` | There is already a team with that name (capitals, accents and spaces are ignored) | Choose another name |
| `team/member_exists` | That person is already in the team | Edit their job or rate instead of adding them again |
| `team/member_not_found` | That person is no longer in the team | Refresh the team page |
| `team/branch_without_staff` | The branch has nobody active to save as a team | Add staff to the branch or create the team from scratch |
| `team/apply_conflict` | Someone added one of the members to that branch while the team was being applied; nothing was changed | Apply the team again: that person will be skipped |
| `team/too_large` | Too many people for a single operation | Split the team in two and apply them separately |
| `team/bad_request` | The team data is not valid | Check the name, the job and that the rate is a number |

---

## Documents (`documents`)

| Code | What it means | What to do |
|---|---|---|
| `documents/unauthorized` | No permissions to access the document | Review the document's visibility by role |
| `documents/not_found` | The document does not exist or is not visible to that user | Check that it is not archived and that the role has visibility |
| `documents/file_required` | No file has been attached | Attach the file before saving |
| `documents/file_too_large` | The file exceeds the maximum allowed of 10 MB | Compress the document or split it |
| `documents/invalid_mime_type` | File format not permitted | Convert the document to a supported format |
| `documents/invalid_visibility_roles` | The visibility configuration is not valid | Review the roles selected |
| `documents/invalid_acknowledgement_mode` | The read receipt configuration is not valid | Review the receipt mode chosen against the document's scope |
| `documents/acknowledgement_not_required` | The document does not require a read receipt | No action needed |
| `documents/acknowledgement_not_allowed` | That user cannot acknowledge receipt of the document | Check that the document is addressed to that employee |
| `documents/restricted_document_type` | No permissions for that document type | Review the role required for that type |
| `documents/already_archived` | The document is already archived | No action needed |
| `documents/branch_not_found` | The branch or project stated is not valid | Select an existing branch |
| `documents/employee_not_found` | The employee stated is not valid | Select an existing employee |
| `documents/employee_not_in_branch` | The employee does not belong to the selected branch | Correct the branch or the employee's assignment |
| `documents/bad_request` | The document's data is not valid | Review the form's required fields |

---

## Tasks (`task`)

| Code | What it means | What to do |
|---|---|---|
| `task/not_found` | The task does not exist or was deleted | Refresh the task list |
| `task/evidence_required` | The task requires evidence to be uploaded before completing it | Attach at least one photo or video and complete it again |
| `task/forbidden` | No permissions for that action on the task | Review the level of responsibility required |
| `task/unauthorized` | No permissions to carry out the action | Ask a manager with a sufficient level to carry out the action |
| `task/invalid_mime_type` | The attached file's format is not permitted | Upload the evidence as a photo or video in a standard format |
| `task/file_too_large` | The file exceeds the maximum size permitted | Reduce the file's resolution or duration |
| `task/bad_request` | The task's information is not valid | Review the required fields: title, branch and deadline |
| `task/no_open_session` | Starting, resuming or completing the task requires an open workday | Clock in and try again |
| `task/geo_required` | The task has its own work site and the location is needed; the back office does not send it | Start, resume or complete the task from the app, while at the site |
| `task/out_of_worksite` | The employee is outside the margin of the task's work site. The warning states the distance and the margin | Get closer to the task's address. If the margin is too narrow for that site, widen it on the task |
| `task/worksite_imprecise` | The work site address has only been located approximately (for example, at city level) | Add the street number and choose the address again in the search box |
| `task/worksite_invalid` | It has not been possible to place the address on the map | Choose the address from the search box instead of typing it by hand |
| `task/not_in_progress` | Only a task in progress can be paused | Start the task before pausing it |
| `task/already_paused` | The task is already paused; another assignee may have paused it first | Refresh the task |
| `task/not_paused` | An attempt was made to resume a task that is not paused | Refresh the task |
| `task/invalid_transition` | The status change is not allowed from the current status; for example, completing a rejected task | Reopen the task by returning it to *Assigned* from **Edit** |
| `task/invalid_status` | The action requires a different status; for example, validating a task that is not completed | Review the task's status |
| `task/invalid_employees` | Some employee cannot be assigned: they do not work at the task's branch or are not active | Assign them to that branch and check that they are active |
| `task/branch_inactive` | The task's branch is inactive and does not accept new tasks or copies | Activate the branch or use another one |
| `task/source_config_invalid` | The task you are trying to duplicate has a configuration that is no longer valid | Open the original task, save it again and duplicate it again |

---

## Subscription and billing

| Code | What it means | What to do |
|---|---|---|
| `subscription/limit_off` | The plan has reached the limit of operations permitted | Review the subscription's status or contact support |
| `suscription/entity_not_configured` | The organisation does not have the configuration needed to subscribe | Complete the legal details and the payment method under **Organisation** |
| `suscription_checkinbiz/entity_legal_not_configured` | The organisation's legal details for CheckBiz are missing | Complete the company details before subscribing |
| `suscription/already_subscribed_into_plan` | The organisation is already subscribed to that plan | No action needed |
| `suscription/ko` | The subscription could not be completed | Review the payment method and retry |
| `subscribe/not_found` | The service stated does not exist | Retry from the plans screen |
| `subscribe/invalid_entity_service` | The organisation or the service is not correct | Verify the organisation selected |
| `subscribe/internal` | Internal error in the subscriptions service | Retry later; if it persists, open an incident |
| `subscribe/plan_not_available` | The plan chosen is not available to subscribe to | Choose another of the plans offered on the plans screen |
| `sub/bad_request` | The data sent is not valid | Review the form and retry |
| `sub/entity_not_found` | The organisation does not exist | Verify the organisation selected |
| `payment/pending` | There are outstanding payments on the account | Settle the payment from the billing section |

---

## Other modules

| Code | What it means | What to do |
|---|---|---|
| `entity/not_found` | The organisation does not exist | Verify the organisation selected in the back office |
| `user/not_found` | There is no user with that email | Check the email entered |
| `user/internal` | Internal error in the users service | Retry; if it persists, open an incident |
| `report/internal_error` | Internal error while generating the report | Retry with a smaller date range; if it persists, open an incident |
| `stats/range_and_groupBy_tolong` | The date range or the grouping produces too much data to display | Select a smaller range or a different grouping |
| `analyze/insufficient_data` | There is not enough data to calculate the indicators | Wait to accumulate more clocking and task history |
| `media/not_found` | The file does not exist | Upload the file again |
| `media/invalid_meda_type` | File type not permitted | Use a supported format |
| `media/invalid_dimesions` | The image's dimensions are not valid | Adjust the image's size |
| `media/error` | Internal storage error | Retry; if it persists, open an incident |
| `internal` | Internal server error | Retry; if it persists, open an incident with the exact time |
| `unavailable` | Service temporarily unavailable | Retry after a few minutes |

---

> **Warning:** if the same code reappears systematically after applying the corrective action, open an incident in the back office including the exact code, the time of the failure and the employee affected.

---

## Role note

This article is for reference by **Owner** and **Manager**, who are responsible for diagnosing and resolving operational errors. Employees with the Worker role who see an error code in the app should report it to their manager with the exact code shown on screen.

---

## Related articles

| Article | Description |
|---|---|
| [Common problems and solutions](../13-support-and-incidents/88-common-problems-and-solutions.md) | Practical diagnostic guide for the most frequent situations |
| [Create an incident](../13-support-and-incidents/85-create-an-incident.md) | How to open a support case when the error has no direct solution |
| [Glossary](./89-glossary.md) | Definition of the technical terms used on the platform |
| [Contact technical support](../13-support-and-incidents/87-contact-technical-support.md) | Channels and response times of the support team |
