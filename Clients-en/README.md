# Documentation — CheckBiz360

Welcome to the CheckBiz360 documentation, the digital attendance control platform by EncodeBiz. This documentation gathers the complete material aimed at the end customer: account owners, human resources leads, area managers and team supervisors.

The articles are organised into 16 thematic sections. Each section covers a module or functional area of the platform and contains independent articles that can be read one at a time or as a sequence.

---

## Feature status

The following convention identifies the status of each feature in the current version of CheckBiz360 (V1). It applies across every article in the documentation and in the tables of each module on this page.

| Status | Meaning |
|---|---|
| **Available** | The feature is active in the current version and can be used straight away. |
| **Partially available** | The feature exists but with limited capabilities compared with the full description. |
| **Planned** | The feature is planned and will be included in a future version of the platform. |
| **Not available** | The feature is not implemented and has no delivery date planned at present. |

---

## Sections

### 01. Getting started

Introduction to the platform, how it differs from other systems, and the initial set-up guide.

| Feature | Status | Comment |
|---|---|---|
| Account registration and organisation set-up | **Available** | Complete process available from the back office. |
| Branch configuration | **Available** | Creating, editing and deactivating branches. |
| Quick start guide | **Available** | A 10-step flow to the first validated clock-in. |
| Back office onboarding guide, narrated by Merlin | **Available** | Five steps based on the real state of the account: subscription, schedule, workplace, employee and clock-in test. |
| Anti-bot verification at registration and password recovery | **Available** | Cloudflare challenge built into the form. |
| Organisation → branch → employee hierarchy | **Available** | Fully operational in V1. |

| Article | Description |
|---|---|
| [What CheckBiz360 is](01-getting-started/01-what-is-checkbiz360.md) | General description of the platform, its components and use cases |
| [How it differs from other software](01-getting-started/02-how-it-differs-from-other-software.md) | Comparison with traditional time-tracking systems |
| [Create an account and set up the organisation](01-getting-started/03-create-account-and-set-up-organisation.md) | Steps from registration to the first operational branch |
| [Quick start guide](01-getting-started/04-quick-start-guide.md) | The 10 steps to a first validated clock-in in 15 minutes |
| [Platform structure](01-getting-started/05-platform-structure.md) | The three hierarchical levels: organisation, branch and employee |

---

### 02. Employees

Creating, configuring and securing employees on the platform, and their roles.

| Feature | Status | Comment |
|---|---|---|
| Creating, editing and deactivating employees | **Available** | Full CRUD with employment statuses, and a *pending* status —not billed— for records that are only partly completed. |
| Relationship type: staff or collaborator | **Available** | Visible on the record; collaborators are left out of the working-time record report. |
| Teams (templates of people with job and rate) | **Available** | Applied to a branch to add the whole crew at once. Adding a whole team to a task: planned. |
| Roles and responsibility levels (worker, supervisor, manager, owner) | **Available** | Four levels with differentiated permissions. |
| Two-factor authentication (2FA) | **Available** | Compatible with TOTP apps (Google Authenticator, Authy). |
| Biometric verification and trusted devices | **Available** | Configurable per employee from the app. |
| Employees assigned to several organisations | **Available** | Organisation picker at sign-in. |
| Adding branches and staff from Excel | **Available** | One template with two sheets; you review what will be created before confirming; the app welcome goes out at the end, when you decide. |
| App access status, resending access and changing the email | **Available** | The record says whether the access email was delivered or bounced and whether the person already uses the app; the home page warns you about the one that has not arrived. |
| Exporting the employee directory | **Planned** | The list is viewed and filtered on screen, with no downloadable file. |

| Article | Description |
|---|---|
| [Create and manage employees](02-employees/06-create-and-manage-employees.md) | Creation, editing, employment statuses and deactivation |
| [Roles and responsibility levels](02-employees/07-roles-and-responsibility-levels.md) | The four levels: worker, supervisor, manager, owner |
| [Permission matrix by role](02-employees/08-permission-matrix-by-role.md) | Complete table of what each role can do |
| [Two-factor authentication (2FA)](02-employees/09-two-factor-authentication.md) | Set-up, compatible apps and access recovery |
| [Biometrics and trusted devices](02-employees/10-biometrics-and-trusted-devices.md) | Biometric verification and management of authorised devices |
| [Multi-organisation employees](02-employees/11-multi-organisation-employees.md) | One employee in several organisations, organisation picker |
| [Export the employee list](02-employees/12-export-employee-list.md) | Status of the feature, available alternatives and GDPR |
| [Teams](02-employees/99-teams.md) | Create teams, apply them to a branch and save a branch as a team |
| [Add branches and staff from Excel](02-employees/110-add-branches-and-staff-from-excel.md) | Sites and people in one go, reviewed before anything is created, with the welcome sent separately |
| [App access and email change](02-employees/116-app-access-and-email-change.md) | Knowing whether the access arrived, resending it, changing the email and sending the clock-in point card |

---

### 03. Time tracking

How the clock-in system works: validations, record types, geofences and workday management.

| Feature | Status | Comment |
|---|---|---|
| Clock-in with geofence, schedule and device validation | **Available** | Three validation layers applied simultaneously on every clock-in. |
| Check-in and check-out from the mobile app | **Available** | Complete process operational on iOS and Android. |
| Working off-site (formerly "remote clocking in") | **Available** | Enabled per employee with time-zone validation. |
| Breaks and pauses (restin/restout) | **Available** | Automatic deduction configurable per branch. |
| QR validation before clocking in | **Available** | Mechanism configurable per branch, not mandatory. |
| Manual workday request (Mode A and Mode B) | **Available** | Requires manager approval. |
| Review and approval of clock records by a manager | **Available** | Approval, rejection and resolution flow; a rejected correction leaves the clock record as it was. |
| Traceability and immutable change history | **Available** | Requests and changes recorded with an audit trail. |
| Suspicious clock-in detection | **Available** | Automatic indicator based on anomalous patterns. |
| Clock-in point: a device at the site with QR or code and a photo | **Partially available** | Paid add-on. Subscribed and managed in the panel; the device needs the next version of the app, which is being published. |

| Article | Description |
|---|---|
| [How clocking in works](03-time-tracking/13-how-clocking-in-works.md) | The three validation layers: geofence, schedule and device |
| [Check-in and check-out from the app](03-time-tracking/14-check-in-and-check-out-from-the-app.md) | Step by step through clocking in from the mobile app |
| [Working off-site](03-time-tracking/15-remote-clocking-in.md) | Clocking in without a geofence: field work, teleworking, activation and time zone |
| [Geofences and clocking radius](03-time-tracking/16-geofences-and-clocking-radius.md) | Configuring the radius, disabling it and recommended values |
| [Breaks and pauses](03-time-tracking/17-breaks-and-pauses.md) | Restin/restout, automatic deduction and per-branch configuration |
| [Employee validation by QR](03-time-tracking/18-employee-validation-qr.md) | QR token, supervisor flow and system warm-up |
| [Request a manual workday](03-time-tracking/19-request-a-manual-workday.md) | Mode A (full workday) and Mode B (check-out only) |
| [Review and approval of clock records](03-time-tracking/20-reviewing-and-approving-clock-records.md) | Approval, rejection and resolution flow for managers |
| [Traceability and change history](03-time-tracking/21-traceability-and-change-history.md) | requestUpdates, immutability and use in audits |
| [Statuses and error codes](03-time-tracking/22-statuses-and-error-codes.md) | Status and error-code tables with causes and solutions |
| [Clock-in point](03-time-tracking/113-clock-in-point.md) | Clocking in from a tablet at the site with a QR or code and a photo, no biometrics |

---

### 04. Calendar and schedules

Configuration of shifts, base schedules, work calendars and individual exceptions.

| Feature | Status | Comment |
|---|---|---|
| Base schedules and shifts per branch | **Available** | Single shift or multiple shifts per day. |
| Work calendar (national and local public holidays) | **Available** | Inheritance hierarchy: organisation → branch → employee. |
| Individual schedule exceptions | **Available** | One-off and recurring exceptions. |
| Strict or flexible workday | **Available** | Decides whether the official schedule or the time actually worked is counted. |
| Strict or flexible break | **Available** | A fixed duration deducted, or pauses marked by the employee. |
| Schedule templates | **Available** | Save a weekly schedule and apply it to other branches. |
| Employee absences by date range, with a paid mark | **Available** | Paid, unpaid or not set. |
| Availability board | **Available** | Coverage by branch and day, who is missing and why, adding days off from the board and export to Excel. |
| Cascading configuration inheritance | **Available** | Priority algorithm used to calculate the effective calendar. |
| Rotating shifts (automatic A/B alternation) | **Planned** | Covered today with one branch per shift or with an employee-specific schedule. |
| Weekly schedule from an Excel template | **Available** | A whole branch's week in one upload, one sheet per person, reviewed before applying; also one person's week from their profile. |
| Schedule from tasks (each day's working time is its tasks) | **Partially available** | Chosen per person on their profile. Their app needs the next version to show it: do not enable it yet. |
| Calendar: shifts loaded by date | **Available** | On the company, a branch or a person; weekly shift calendar, copy to next week and loading from the Excel roster. |
| Vacation and leave requested from the app | **Partially available** | Approved in Contact → Requests. The app screen and the panel tab arrive with their next version. |

| Article | Description |
|---|---|
| [Base schedules and shifts](04-calendar-and-schedules/23-base-schedules-and-shifts.md) | Single shift, multiple shifts per day, selecting the active shift |
| [Work calendar](04-calendar-and-schedules/24-work-calendar.md) | National and local holidays, entity→branch→employee hierarchy |
| [Schedule exceptions](04-calendar-and-schedules/25-schedule-exceptions.md) | One-off and recurring exceptions, reduced working day |
| [Configuration inheritance](04-calendar-and-schedules/26-configuration-inheritance.md) | The cascade algorithm and debugging the effective calendar |
| [Rotating shifts](04-calendar-and-schedules/27-rotating-shifts.md) | Not available in V1: how to cover rotation with branches or employee schedules |
| [Strict and flexible workday](04-calendar-and-schedules/28-flexible-schedule.md) | How hours and breaks are counted under each mode |
| [Public holidays and non-working days](04-calendar-and-schedules/29-public-holidays-and-non-working-days.md) | Holiday types, employee absences, blocking clock-ins, sectors that work on holidays |
| [Availability board](04-calendar-and-schedules/98-availability-board.md) | Coverage by branch and day, breakdown of who is missing and days off from the board |
| [Import the weekly schedule](04-calendar-and-schedules/108-import-the-weekly-schedule.md) | The week of a branch's whole staff in one upload, or one person's week from their profile |
| [Calendar: shifts loaded by date](04-calendar-and-schedules/114-shift-calendar-by-date.md) | The third schedule mode: each day with its shifts, loaded by hand, copied or from Excel |
| [Vacation and leave from the app](04-calendar-and-schedules/115-vacation-and-leave-from-the-app.md) | "My calendar" in the app, requesting vacation or leave and approving it in the panel |

---

### 05. Document management

Uploading, organising, acknowledging and controlling access to employment documents.

| Feature | Status | Comment |
|---|---|---|
| Uploading and organising documents | **Available** | Twelve types, organisation/branch/employee scope and visibility by role. Max. 10 MB per file. |
| Private documents with role-based access control | **Available** | Permission table differentiated by user level. |
| Push notifications when documents arrive | **Available** | Direct navigation to the document from the notification. |
| Read receipt (reading confirmation) | **Available** | The employee confirms they have read it; this is recorded in the system. |
| Individual document download | **Available** | Signed link per document, with expiry. |
| Logical archiving of documents (no permanent deletion) | **Available** | Archived documents stop being visible but are retained. |
| Confirmation signed from the phone | **Available** | Downloadable signature record and signed PDF for PDF documents addressed to a single employee. |
| Automatic version history | **Planned** | Planned for a future version. |
| Bulk document download (ZIP) | **Planned** | Planned for a future version. |

| Article | Description |
|---|---|
| [What the document module is](05-document-management/30-what-is-the-document-module.md) | What it is for, document types and the difference from generic storage |
| [Upload and organise documents](05-document-management/31-upload-and-organise-documents.md) | Fields, categories, recipients and visibility |
| [Payslips and contracts](05-document-management/32-payslips-and-contracts.md) | Monthly flow, notification, access from the app and legal retention |
| [Private documents](05-document-management/33-private-documents.md) | Visibility by role, access table and use cases |
| [Document notifications](05-document-management/34-document-notifications.md) | Push payload, direct navigation to the document from the notification |
| [Read receipt and electronic signature](05-document-management/35-electronic-signature.md) | Confirmation signed with the phone, signature record and signed PDF for single-person documents |
| [Version history](05-document-management/36-version-history.md) | Manual flow available in V1; automatic history on the roadmap |
| [Document access permissions](05-document-management/37-document-access-permissions.md) | Permission table by role: upload, view, confirm, archive |
| [Export documents](05-document-management/38-export-documents.md) | Individual download in V1; bulk download on the roadmap |

---

### 06. Tasks

Creating, assigning, tracking and rating operational tasks.

| Feature | Status | Comment |
|---|---|---|
| Create and assign tasks to employees | **Available** | Individual and bulk assignment with push notification; editing the task assigns and withdraws employees. |
| Own work site per task | **Available** | Its own address and margin; starting requires being there, from the app. |
| Duplicate a task | **Available** | Copies the job, unassigned and as a draft; asks for the dates again. |
| Pause and resume tasks | **Available** | From the back office and from app 1.4.0; time paused appears in the report. |
| Task history | **Available** | Who created, started, paused, completed, validated or cancelled it, with date and role. |
| Formatted description (lists, checklists, links) | **Available** | Editor with a formatting bar and preview. |
| Photo and video evidence | **Available** | Photo (JPG, PNG, WEBP) up to 5 MB; video up to 25 MB from the app. |
| Task statuses: draft, assigned, in progress, completed, validated, rejected, cancelled | **Available** | Seven statuses with full traceability. |
| Four priorities: low, medium, high and critical | **Available** | Colour-coded in the list. |
| Time-compliance indicator | **Available** | On time, at risk, overdue, completed on time or late. |
| Expected start date and late-start warning | **Available** | Notification after 15 minutes, configurable per task. |
| Task validation and rating by the manager | **Available** | Delegable to the supervisor per task; rejection requires a reason. |
| Task push notifications | **Available** | Assignment, validation, rejection, late start and overdue. |
| Exportable task report | **Available** | Excel (XLSX), filterable by branch, status and due period, with time spent and time paused; with inventory subscribed, also each task's material. |
| Document-type attachments (PDF, Word, Excel) | **Planned** | Evidence currently accepts photo and video. |
| Automatic "overdue" status once the deadline passes | **Planned** | Today the deadline is reflected in the time-compliance indicator. |
| Configuring how far in advance due warnings are sent | **Planned** | The warnings are issued; their lead time is not configurable. |
| Aggregate task metrics (completion rate, average time) | **Planned** | Calculable today from the Excel report. |
| Weekly task calendar | **Available** | A tab next to the list: the week by day and hour, with the gaps, the overlaps and what is due; same filters as the list. |

| Article | Description |
|---|---|
| [What the tasks module is](06-tasks/39-what-is-the-tasks-module.md) | What it is for and how it differs from attendance control |
| [Create a task](06-tasks/40-create-a-task.md) | Fields, own work site, duplicating a task and photo/video attachments |
| [Assign tasks to employees](06-tasks/41-assign-tasks-to-employees.md) | Individual and bulk assignment, reassignment, notification |
| [Task statuses](06-tasks/42-task-statuses.md) | Life cycle, reopening a task, paused task and the time-compliance indicator |
| [Tracking and updates](06-tasks/43-tracking-and-updates.md) | Starting, pausing and resuming, notes and the task history |
| [Priorities and deadlines](06-tasks/44-priorities-and-deadlines.md) | The priority system and the time-compliance indicator |
| [Task validation](06-tasks/45-task-validation.md) | Validation flow, acceptance and rejection with a reason |
| [Employee rating](06-tasks/46-employee-rating.md) | Rating scale and its impact on the efficiency index |
| [Task notifications](06-tasks/47-task-notifications.md) | Events notified in V1; reminders on the roadmap |
| [Task reports](06-tasks/48-task-reports.md) | Metrics in the back office and the Excel report, with its time columns |
| [Weekly task calendar](06-tasks/111-weekly-task-calendar.md) | The week at a glance: what there is each day, at what time, in what status and what is due |

---

### 07. Operational intelligence

Analysis of behaviour patterns, performance indices, costs and anomaly detection.

| Feature | Status | Comment |
|---|---|---|
| Operations dashboard (single view, monthly period) | **Available** | Read from top to bottom; three tabs: Branches, Employees and Analysis. |
| Reliability index | **Available** | Quality of behaviour, kept separate from how long it has been measured. |
| Site effect | **Available** | Compares each person with themselves across different sites. |
| Dependency (concentration of the operation) | **Available** | How much of the operation rests on a few people, with cover by position. |
| Data maturity states | **Available** | Gathering data / partial evidence / not enough data. |
| Operational efficiency and cost index | **Available** | Actual cost against the consolidated history; requires a configured rate. |
| Operational assessment of the employee | **Available** | Automatic diagnosis of the pattern, with a promotion-candidate signal. |
| Anomaly detection (suspicious clock-ins) | **Available** | Surfaces in the dashboard's Analysis tab. |
| AI assistant narrative on the dashboard | **Available** | Narrates and prioritises the figures already on screen. |
| Promotion score as a single comparable score | **Planned** | There is no single number and no ranking by that value. |
| Anomaly review workflow (pending/reviewed states) | **Planned** | Planned for a future version. |
| Configurable cost-overrun alerts | **Planned** | Planned for a future version. |
| Dashboard data export (CSV/PDF) | **Planned** | Planned for a future version. |
| "Home" page: today by site, alerts, recent weeks, this week's availability, headcount over time and estimated costs | **Available** | The first thing you see when you sign in; it refreshes on its own and shows only what needs attention. |

| Article | Description |
|---|---|
| [What operational intelligence is](07-operational-intelligence/49-what-is-operational-intelligence.md) | The module that sets CheckBiz360 apart and the idea of a behaviour pattern |
| [Behaviour pattern](07-operational-intelligence/50-behaviour-pattern.md) | How the pattern is built and why it beats a one-off report |
| [Reliability index](07-operational-intelligence/51-reliability-index.md) | What it measures, its ranges and how to improve it |
| [Operational efficiency index](07-operational-intelligence/52-efficiency-index.md) | Actual cost against history and how to read it |
| [Operational assessment of the employee](07-operational-intelligence/53-promotion-score.md) | Diagnosis of the pattern and the promotion-candidate signal |
| [Cost analysis](07-operational-intelligence/54-cost-analysis.md) | Rate per branch, cost indicators and alerts on the roadmap |
| [Anomaly detection](07-operational-intelligence/55-anomaly-detection.md) | Automatic indicator in V1; review workflow on the roadmap |
| [The Operations dashboard](07-operational-intelligence/56-dashboards.md) | The three indices, the three tabs and how to read them |
| [The home page: today, alerts and recent weeks](07-operational-intelligence/112-the-home-page-today-alerts-and-recent-weeks.md) | What you see on signing in: today's attendance, tasks and cost by site, alerts, weekly history, headcount and estimated costs |

---

### 08. Branches and organisation

Creating and configuring branches, assigning employees and the multi-branch global view.

| Feature | Status | Comment |
|---|---|---|
| Create and manage branches | **Available** | Creation, editing, geocoding and deactivation. |
| Advanced branch configuration (geofence, breaks, tolerance) | **Available** | All operational parameters configurable. |
| Assign employees to branches with responsibilities | **Available** | Multi-branch with an effective calendar per assignment. |
| Organisation configuration (tax details, time zone) | **Available** | Changes propagated to dependent branches. |
| Storage per company | **Available** | 2 GB included; above that, €0.25 per full GB if extra storage is turned on. Shown in Organisation → Subscriptions. |
| Back office collaborators (owner and administrator) | **Available** | Invitation, role change and removal; the organisation is never left without an active owner. |
| Multi-branch global view | **Available** | The home page shows today by site and the alerts; the Operations panel compares sites by period. |

| Article | Description |
|---|---|
| [Create and manage branches](08-branches-and-organisation/57-create-and-manage-branches.md) | Creation, required fields, geocoding and deactivation |
| [Advanced branch configuration](08-branches-and-organisation/58-advanced-branch-settings.md) | Advanced parameters: geofence, breaks, tolerance, timestamp adjustment |
| [Branch statuses](08-branches-and-organisation/59-branch-statuses.md) | Active/inactive, impact on clock-ins and history |
| [Assign employees to branches](08-branches-and-organisation/60-assign-employees-to-branches.md) | Multi-branch, responsibilities and the effective calendar |
| [Organisation configuration](08-branches-and-organisation/61-organisation-settings.md) | Tax details, workspace, collaborators, global time zone and propagation of changes |
| [Multi-branch global view](08-branches-and-organisation/62-multi-branch-global-view.md) | Where each overview lives: today's home page by site, the Operations panel and availability |

---

### 09. Notifications

Notification types generated automatically by the system for employees and managers.

| Feature | Status | Comment |
|---|---|---|
| Push notifications for events (attendance, documents, tasks) | **Available** | Sent automatically on every relevant event. |
| Alerts for managers (employee who did not clock in, suspicious clock-in) | **Available** | Visible in the back office and in the supervisor's app. |
| Notification centre in the app and back office | **Partially available** | Notifications visible until dismissed; no persistent history. |
| Welcome and password-reset emails | **Available** | With the delivery status on the employee's record and access resending. |
| Task and weekly schedule notices by email, for people who do not use the app | **Available** | A box per person in Schedules & holidays; nothing about clock-ins. |
| User-configurable notification preferences | **Planned** | Planned for a future version. |
| Persistent notification history | **Planned** | Planned for a future version. |
| Operational alerts by email to managers | **Planned** | Planned for a future version. |

| Article | Description |
|---|---|
| [Notification types](09-notifications/63-notification-types.md) | Attendance, documents, tasks, security and administrative |
| [Push notifications in the app](09-notifications/64-push-notifications-in-the-app.md) | Content, direct navigation to the resource and diagnosis |
| [Configure notification preferences](09-notifications/65-configure-notification-preferences.md) | Events notified in V1; configurable preferences on the roadmap |
| [Alerts for managers](09-notifications/66-alerts-for-managers.md) | Employee who did not clock in, suspicious clock-in, pending manual workday |
| [Notification history](09-notifications/67-notification-history.md) | Notification centre in V1; persistent history on the roadmap |
| [Email notifications](09-notifications/68-email-notifications.md) | Welcome and access status, work notices by email, storage warning; operational alerts on the roadmap |

---

### 10. Mobile app

Downloading, installing, navigating and using the CheckBiz360 app for employees.

| Feature | Status | Comment |
|---|---|---|
| Download and installation on iOS and Android | **Available** | Available on the App Store and Google Play. |
| Clocking in from the app with all three validations | **Available** | Geofence, schedule and device validated in real time. |
| Viewing your own attendance history | **Available** | Filters by period and detail of each record. |
| Access to documents and tasks from the app | **Available** | Navigation from the notification to the resource; task descriptions are shown with formatting. |
| Pausing and resuming tasks, time spent and history in the app | **Available** | From version 1.4.0. |
| Task work site with a link to Maps | **Available** | From version 1.3.2. |
| Profile, 2FA and biometrics configuration | **Available** | Managed from the app's profile section. |
| Viewing cached data offline | **Partially available** | Read-only for previously loaded data; clocking in and updating tasks require a connection. |
| Offline mode with a clock-in sync queue | **Planned** | Planned for a future version. |

| Article | Description |
|---|---|
| [Download and installation](10-mobile-app/69-download-and-installation.md) | iOS and Android, minimum requirements and required permissions |
| [First sign-in](10-mobile-app/70-first-sign-in.md) | Account activation, password and organisation selection |
| [Main app navigation](10-mobile-app/71-main-app-navigation.md) | The 5 sections: clock in, records, documents, tasks and profile |
| [Profile settings in the app](10-mobile-app/72-profile-settings-in-the-app.md) | Personal details, password, 2FA and biometrics from the app |
| [My attendance records](10-mobile-app/73-my-attendance-records.md) | Your own history, filters, detail and correction requests |
| [Offline use](10-mobile-app/74-offline-use.md) | What data is available offline and what requires connectivity |
| [App updates](10-mobile-app/75-app-updates.md) | What's new by version, how to update and the consequences of outdated versions |

---

### 11. Reports and exports

Generating, filtering and exporting attendance, cost and compliance reports.

| Feature | Status | Comment |
|---|---|---|
| Attendance report in PDF or Excel (XLSX) | **Available** | Generated on demand, with a report history; it gathers staff personnel, not collaborators. |
| Task report in Excel (XLSX) | **Available** | Filterable by branch, status and due period; includes time paused and, with inventory subscribed, material and its cost. |
| Employee directory export | **Planned** | The list is viewed and filtered on screen, with no downloadable file. |
| RDL 8/2019 compliance report for inspections | **Available** | Generated from the back office. |
| Export of the operational intelligence dashboards | **Planned** | Costs, anomalies and comparisons are consulted on screen. |
| Automatic periodic reports sent by email | **Planned** | Planned for a future version. |

| Article | Description |
|---|---|
| [Report types](11-reports-and-exports/76-report-types.md) | Attendance, punctuality, costs, anomalies and tasks |
| [Generate and filter reports](11-reports-and-exports/77-generate-and-filter-reports.md) | Available filters, preview and saved configurations |
| [Export data](11-reports-and-exports/78-export-to-excel-and-csv.md) | Attendance in PDF or Excel and tasks in Excel |
| [Regulatory compliance report](11-reports-and-exports/79-regulatory-compliance-report.md) | Report for audits and inspections under RDL 8/2019 |
| [Automatic reports](11-reports-and-exports/80-automatic-reports.md) | Feature planned on the roadmap; not available in V1 |

---

### 12. Regulatory compliance

Mandatory time recording in Spain, data protection and preparing for inspections.

| Feature | Status | Comment |
|---|---|---|
| Time recording compliant with RDL 8/2019 | **Available** | Immutable timestamp with full traceability. |
| Labour inspection report | **Available** | Generated from the back office with all the required data. |
| Data retention compliant with LOPD/GDPR | **Available** | Legal basis, retention periods and employee rights. |

| Article | Description |
|---|---|
| [Mandatory time recording in Spain](12-regulatory-compliance/81-mandatory-time-recording-in-spain.md) | RDL 8/2019: what it requires, its scope and the penalties |
| [How CheckBiz360 complies with RDL 8/2019](12-regulatory-compliance/82-how-checkbiz360-complies-with-rdl-8-2019.md) | Technical mechanisms: timestamp, immutability, traceability |
| [Data retention and protection](12-regulatory-compliance/83-data-retention-and-protection.md) | LOPD/GDPR: legal basis, retention and employee rights |
| [Preparing for a labour inspection](12-regulatory-compliance/84-preparing-for-a-labour-inspection.md) | What documentation to request, which report to present and prior recommendations |

---

### 13. Support and incidents

How to create and manage incidents and how to contact the support team.

| Feature | Status | Comment |
|---|---|---|
| Creating incidents from the back office | **Available** | Internal channel of the organisation: type, source/target role, branch and comment. |
| Tracking through a reply thread | **Available** | Three statuses (pending, under review, resolved); the status changes when you reply. |
| Contacting technical support by email | **Available** | Indicative response times, not contractual. |
| Automatic ticket numbering | **Not available** | Incidents do not generate an automatic reference number. |
| Priority and attachments on an incident | **Not available** | The form has neither priority nor attached files. |
| Reopening a resolved incident | **Not available** | A resolved incident accepts no further replies; a new one is created. |
| Exporting the incident history | **Not available** | It is viewed and filtered on screen. |

| Article | Description |
|---|---|
| [Create an incident](13-support-and-incidents/85-create-an-incident.md) | The organisation's internal channel: types, fields and creation |
| [Incident tracking and resolution](13-support-and-incidents/86-incident-tracking-and-resolution.md) | The three statuses, the reply thread and the history |
| [Contact technical support](13-support-and-incidents/87-contact-technical-support.md) | Channels, indicative times and what information to include |
| [Common problems and solutions](13-support-and-incidents/88-common-problems-and-solutions.md) | The 14 most frequent situations with diagnostic steps |

---

### 14. Reference

Glossary, error codes, plans and frequently asked questions.

| Feature | Status | Comment |
|---|---|---|
| Glossary of platform terms | **Available** | Main terms defined, including those for tasks and AI. |
| Complete error-code table | **Available** | Every code in the dictionary, by module, with cause and solution. |
| Plans and prices (Bronze and Enterprise) | **Available** | Price, trial period, included modules, add-ons, storage and roadmap. |
| Frequently asked evaluation questions | **Available** | 20 questions and answers for customers evaluating the platform. |

| Article | Description |
|---|---|
| [Glossary](14-reference/89-glossary.md) | Definitions of the main platform terms |
| [Complete error codes](14-reference/90-complete-error-codes.md) | Table of every error code with cause and solution |
| [Plans, prices and features](14-reference/91-plans-and-features.md) | Price of each plan, trial period, included modules, add-ons, storage and roadmap |
| [Frequently asked questions](14-reference/92-frequently-asked-questions.md) | 20 questions and answers for customers evaluating the platform |

### 15. Integrations

Add-ons that connect CheckBiz360 with other software your company already uses, so information travels on its own and nobody types the same thing twice.

| Feature | Status | Comment |
|---|---|---|
| Integration catalogue | **Available** | With description, capabilities and status |
| RentmanBiz — hours posted to Rentman | **Available** | Automatic every 15 minutes, or on demand |
| RentmanBiz — crew, sites and tasks import | **Available** | Incomplete data stays pending, never halfway |
| RentmanBiz — alert when hours are edited in Rentman | **Available** | The clock-in is never overwritten |
| Add-on configuration screen | **Pending development** | During the beta the Encodebiz team sets it up |
| Sending tasks to Rentman | **Pending development** | Planned for a future release |
| Operations manager in Claude or ChatGPT | **Available** | Connect your company to your assistant and ask it for the week, new hires and changes in your own words; nothing is saved without your confirmation |

| Article | Description |
|---|---|
| [What integrations are](15-integrations/93-what-are-integrations.md) | What an add-on is, how it is switched on and what happens when it is switched off |
| [RentmanBiz](15-integrations/94-rentmanbiz.md) | What the Rentman integration gives you, and what it does not do |
| [Connecting RentmanBiz step by step](15-integrations/95-connect-rentmanbiz.md) | From the Rentman token to the first import |
| [What gets imported and what stays pending](15-integrations/97-import-and-pending.md) | People, sites, responsibilities and tasks; and what to do with pending items |
| [Posted hours and alerts](15-integrations/96-posted-hours-and-alerts.md) | Reading the panel, discrepancies and FAQs |
| [Your operations manager in Claude or ChatGPT](15-integrations/109-your-operations-manager-in-claude-or-chatgpt.md) | Connecting your company to your assistant and what to ask it: the whole week, bulk onboarding, single changes |


---

### 16. Inventory

Paid add-on: material tied to the task, the person, the place and the time.

| Feature | Status | Comment |
|---|---|---|
| Warehouses linked to branches | **Available** | Every warehouse serves at least one branch. |
| Consumable and operable items, with units | **Available** | The item is created on its first receipt. |
| Stock with status, minimums and discrepancies | **Available** | Managers are alerted when stock drops below the minimum. |
| Material assigned when creating the task and tracked in its detail | **Available** | Reserve, issue, consume and settle on validation. |
| Issue and consumption from the app | **Available** | Preloaded with what was reserved and what is pending. |
| Unit calendar with clash warning | **Available** | Per unit, in the item record. |
| Consumption report and movement ledger | **Available** | Grouped by item, task, employee, branch or warehouse; CSV. |
| Material in the task report | **Available** | Only with the add-on subscribed. |
| Documents and inspections for each machine | **Available** | Expiry alert and red flag, without blocking. |
| PPE delivery confirmed by the worker | **Available** | With fingerprint or face from the app. |
| "Equipment and PPE" report for inspections | **Available** | Delivery record and dossier per machine. |
| Material import from an Excel template | **Available** | Per warehouse, one for consumables and one for operables; reviewed before importing and does not duplicate when uploaded again. |
| Where each piece of equipment is, and equipment away from base | **Available** | Releasing it does not return it to the warehouse: you say where it stays and it is received in the warehouse; history of where it has been. |
| Material without tasks: to a person or a workplace | **Available** | Issue, allocate allowances, declare from the working day in the app and settle from the record; "Outside the warehouse" in Stock. |

| Article | Description |
|---|---|
| [What is inventory](16-inventory/100-what-is-inventory.md) | What problems it solves, how it works and how to subscribe |
| [Stock, warehouses and receipts](16-inventory/101-stock-warehouses-and-receipts.md) | Adding material and controlling stock |
| [Material on tasks](16-inventory/102-material-on-tasks.md) | Reserve, issue, declare and settle |
| [Consumption report and movements](16-inventory/103-consumption-report-and-movements.md) | Where material goes and what it costs |
| [Equipment: documents, inspections and handovers](16-inventory/104-equipment-documents-inspections-and-handovers.md) | Each machine's paperwork, PPE handovers and the inspection report |
| [Import material from a template](16-inventory/105-import-material-from-a-template.md) | Load everything a warehouse holds at once |
| [Where each piece of equipment is](16-inventory/106-where-each-piece-of-equipment-is.md) | Free equipment away from the warehouse, collecting and receiving it |
| [Material without tasks: people and workplaces](16-inventory/107-material-without-tasks-people-and-workplaces.md) | Hand material to a person or a workplace and declare it from the working day |

---

## File structure

```
DOCS/Clients-en/
├── README.md                           (this index)
├── 01-getting-started/                 (5 articles)
├── 02-employees/                       (10 articles)
├── 03-time-tracking/                   (11 articles)
├── 04-calendar-and-schedules/          (11 articles)
├── 05-document-management/             (9 articles)
├── 06-tasks/                           (11 articles)
├── 07-operational-intelligence/        (9 articles)
├── 08-branches-and-organisation/       (6 articles)
├── 09-notifications/                   (6 articles)
├── 10-mobile-app/                      (7 articles)
├── 11-reports-and-exports/             (5 articles)
├── 12-regulatory-compliance/           (4 articles)
├── 13-support-and-incidents/           (4 articles)
├── 14-reference/                       (4 articles)
├── 15-integrations/                    (6 articles)
└── 16-inventory/                       (8 articles)
```

**Total: 116 articles**
